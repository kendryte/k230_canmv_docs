# TCP Server Example Explanation

## Example Location

- Development board firmware path: `/sdcard/examples/14-Socket/tcp_server.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/tcp_server.py`

This example uses the development board as a TCP server, waits for connections on port `8080`, sends a welcome message to the client, and echoes back received data.

## Preparation Before Running

Configure the network connection method at the top of the script:

```python
NETWORK_TYPE = "wifi_sta"  # "default", "lan", "wifi_sta" or "wifi_ap"
WLAN_DEVICE = "auto"       # "auto", "usb", "sdio" or "spi"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

A TCP client or network debugging tool is required on the computer side, and it must be able to access the IP address obtained by the development board.

## Code Flow

### 1. Connect to Network and Obtain IP

```python
netif, ip = connect_network(...)
```

After a successful connection, `ip` is used to output `tcp server <IP> port:8080`, which is the address the client should connect to.

### 2. Create and configure the listening Socket

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
addr = socket.getaddrinfo("0.0.0.0", 8080)[0][-1]
s.bind(addr)
s.settimeout(0)
s.listen(5)
```

- `SOCK_STREAM` creates a TCP Socket.
- `SO_REUSEADDR` makes it easier to rebind to the same port after the script restarts.
- `0.0.0.0` listens on all IPv4 interfaces and does not rely on dynamic netdev names.
- `settimeout(0)` uses non-blocking mode, and `os.exitpoint()` can still be called during the wait to respond to exit requests.

### 3. Accept connection

```python
client_sock, client_addr = s.accept()
client_sock.setblocking(False)
```

When there are no pending connections, a non-blocking `accept()` may return `errno == 11`, and the example will continue to wait. After the connection is established, the client address is printed, and a welcome message containing the connection count is sent.

### 4. Read and echo data

```python
h = client_stream.read()
if h is None:
    continue
if h != b"":
    print(h)
    client_stream.write("recv :%s" % h)
```

`None` means there is currently no data; non-empty data will be printed to the serial port and echoed back with `recv :` prepended. Since TCP does not preserve message boundaries, formal applications should define their own fixed-length, delimiter-based, or length-field protocols.

### 5. Connection lifecycle

The example uses data containing `end` as the end marker for the current connection, closes the client Socket, and then returns to `accept()` to wait for the next connection:

```python
if b"end" in h:
    client_stream.close()
    break
```

`read()` returns byte data, so the end marker should also use `b"end"`. If the current script still uses the string `"end"`, please fix it according to the writing method above first; otherwise, the runtime, which strictly distinguishes between strings and bytes, will report a type error. After the count exceeds 10, the service closes the listening Socket and exits. This example handles connections one client at a time; when persistent concurrent service is needed, connection state management and multi-client scheduling should be added.

## Running and verification

1. Run the script and note the IP and `8080` port output on the serial port.
2. Connect to this address in a computer TCP client.
3. Confirm that the computer receives the welcome message, then send text.
4. The serial port should print the received bytes, and the computer side should receive the echo with the `recv :` prefix.
5. Send `end` to end the current connection.

When the connection fails, check whether the development board's IP has changed, whether both ends are in a reachable network, and whether TCP `8080` is blocked by a firewall.
