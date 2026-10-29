# UDP Client Example Explanation

## Example Location

- Development board firmware path: `/sdcard/examples/14-Socket/udp_clinet.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/udp_clinet.py`

The `clinet` in the filename follows the actual spelling used in the current firmware and source code directories. This example uses the development board as a UDP sender, continuously sending 10 datagrams to the computer.

## Preparation Before Running

First, start a UDP debugging tool on the computer and listen on a port, then modify the network parameters and target address in the script:

```python
NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

```python
ai = socket.getaddrinfo("192.168.1.110", 8080)
```

Change `192.168.1.110` to the IP that allows communication between the computer and the development board, change `8080` to the UDP listening port on the computer side, and allow that UDP port through the firewall.

## Code Flow

### 1. Connect to the Network

```python
netif, _ = connect_network(...)
```

The common network library waits for the interface to obtain an IP and selects the default uplink interface.

### 2. Resolve the Target Address and Create a UDP Socket

```python
addr = socket.getaddrinfo("192.168.1.110", 8080)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

`SOCK_DGRAM` indicates UDP. Unlike TCP, it does not need to establish a connection beforehand; each send specifies the target address directly.

### 3. Send 10 Datagrams

```python
for i in range(10):
    message = "K230 udp client send test {0} \r\n".format(i)
    s.sendto(message, addr)
    time.sleep(0.2)
```

Each `sendto()` corresponds to an independent UDP datagram, and the receiving end can preserve the datagram boundaries. UDP does not guarantee delivery, ordering, or deduplication; application-layer acknowledgment and retransmission are required when reliability is needed.

### 4. Close the Socket

After the script finishes sending, it waits for 1 second, closes the Socket, and prints `end`. This example only sends data and does not call `recvfrom()`, so it will not read the server's reply.

## Running and Verification

1. First, start the UDP receiving tool on the computer.
2. Run `/sdcard/examples/14-Socket/udp_clinet.py`.
3. The computer should receive 10 datagrams with sequence numbers `0` to `9`.
4. If the serial port shows the message was sent successfully but the computer didn't receive it, focus on checking the target IP, UDP port, firewall, and the client isolation settings of the Wi-Fi
   hotspot.
