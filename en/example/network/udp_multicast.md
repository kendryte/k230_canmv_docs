# UDP Multicast Example Explanation

## Example Location

Development board send/receive example:

- Development board firmware path: `/sdcard/examples/14-Socket/udp_multicast.py`
- SDK source path: `src/canmv/resources/examples/14-Socket/udp_multicast.py`

The companion scripts for the PC are also provided with the firmware, but they should run in the PC's Python environment:

- Sender firmware path: `/sdcard/examples/14-Socket/udp_multicast_sender_pc.py`
- Sender source path: `src/canmv/resources/examples/14-Socket/udp_multicast_sender_pc.py`
- Receiver firmware path: `/sdcard/examples/14-Socket/udp_multicast_receiver_pc.py`
- Receiver source path: `src/canmv/resources/examples/14-Socket/udp_multicast_receiver_pc.py`

Multicast allows a single sender to deliver the same datagram to multiple receivers in the same multicast group. The development board script switches between sender and receiver modes via
`IS_SENDER`, and the PC-side scripts serve as the other end for verification.

## Parameter Configuration

```python
MULTICAST_GROUP = "239.255.0.1"
MULTICAST_PORT = 5007
IS_SENDER = False

NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

The development board and the PC must be on the same LAN that supports multicast forwarding. If a switch, wireless router, or hotspot has client isolation, multicast filtering, or IGMP restrictions enabled, the data may not reach its destination.

## Common Flow

```python
netif, ip = connect_network(...)

if IS_SENDER:
    multicast_sender(ip)
else:
    multicast_receiver()
```

The script first obtains a valid IP, then selects the role based on `IS_SENDER`. The default value `False` means the development board acts as the receiver.

## Development Board Sender Mode

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack("b", 1)
sock.setsockopt(0, 33, ttl)
sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
```

Here, the options `0` and `33` correspond to `IPPROTO_IP` and `IP_MULTICAST_TTL` respectively. TTL is set to
`1`, so that the data only propagates on the local network. The script sends once every 2 seconds, and includes the development board's IP and an incrementing counter in the message.

Test steps:

1. Run `udp_multicast_receiver_pc.py` on the PC.
2. Change `IS_SENDER` in the development board script to `True` and run it.
3. The PC side should continuously display multicast messages from the development board.

## Development Board Receiver Mode

```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", MULTICAST_PORT))

mreq = struct.pack(
    "4s4s",
    inet_aton(MULTICAST_GROUP),
    inet_aton("0.0.0.0"),
)
sock.setsockopt(0, 35, mreq)
```

The receiver first listens on port `5007` across all interfaces, then joins `239.255.0.1` via a membership request. Option `35` corresponds to `IP_ADD_MEMBERSHIP`. After receiving data, the script prints the sender's address and the decoded payload; data that cannot be decoded as UTF-8 will be flagged as binary content.

Test steps:

1. Keep `IS_SENDER = False` in the development board script and run it.
2. Run `udp_multicast_sender_pc.py` on the PC.
3. The development board's serial port should display `Hello from PC multicast sender!` once per second.

## Troubleshooting Points

- Confirm that the multicast address and port on both ends match exactly.
- Confirm that the system firewall allows UDP `5007`.
- On PCs with multiple network cards, confirm that the multicast traffic is sent out from the interface that can communicate with the development board.
- When regular UDP unicast works but multicast has no data, focus on checking the access point's client isolation, IGMP Snooping, and multicast filtering settings.
