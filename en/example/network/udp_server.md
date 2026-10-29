# UDP Server Example Explanation

## Example Location

- Development board firmware path: `/sdcard/examples/14-Socket/udp_server.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/udp_server.py`

This example receives datagrams on UDP port `8080` of the development board, prints the sender's information, and replies to the original sender with data containing a counter.

## Preparation Before Running

Configure the network mode at the top of the script:

```python
NETWORK_TYPE = "wifi_sta"  # "default", "lan", "wifi_sta" or "wifi_ap"
WLAN_DEVICE = "auto"       # "auto", "usb", "sdio" or "spi"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

The computer needs a UDP debugging tool and must be able to access the IP obtained by the development board.

## Code Flow

### 1. Connect to the Network and Resolve the Listening Address

```python
netif, ip = connect_network(...)
addr = socket.getaddrinfo("0.0.0.0", 8080)[0][-1]
```

`ip` is used to print the address the client should visit, while `0.0.0.0` makes the service listen on all current IPv4 interfaces.

### 2. Create and Bind UDP Socket

```python
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.settimeout(0)
```

- `SOCK_DGRAM` creates a UDP Socket.
- `SO_REUSEADDR` makes it easy to rebind the port after restarting the script.
- `settimeout(0)` sets the Socket to non-blocking mode.

### 3. Receive Datagram

```python
data, peer_addr = s.recvfrom(800)
```

Reads up to 800 bytes at a time. `recvfrom()` returns both the data and the sender's address, so UDP can send replies back to the correct client without establishing a connection. The script waits 1 second before entering the loop; to prevent the non-blocking read from raising an error immediately when there is no data yet, the test client should send data promptly after the service starts.

### 4. Reply to the Sender

```python
s.sendto(b"%s have recv count=%d " % (data, counter), peer_addr)
```

The response contains the original data received and the current count. The count starts from `0`. After processing 11 non-empty datagrams, the Socket is closed and the script exits.

## Running and Verification

1. Run the script and check the development board IP and port `8080` from the serial output.
2. Set the development board address as the target in the computer's UDP tool and send text.
3. The serial port should print the count, data, and computer address, and the computer should receive the reply from the development board.
4. If there is no data, check the UDP `8080` firewall rules, target IP, and hotspot client isolation settings.
