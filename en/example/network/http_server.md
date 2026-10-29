# HTTP Server Example Explanation

## Example Location

- Development board firmware path: `/sdcard/examples/14-Socket/http_server.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/http_server.py`

This example starts a simple HTTP/1.1 service on the development board. After the browser connects to port `8081`, the service reads the request header and returns a device status webpage, displaying the system version, uptime, available memory, network interface, and client information, then closes the connection and exits.

## Preparation Before Running

Set the network type and Wi-Fi parameters at the top of the script:

```python
NETWORK_TYPE = "wifi_sta"  # "default"、"lan"、"wifi_sta" or "wifi_ap"
WLAN_DEVICE = "auto"       # "auto"、"usb"、"sdio" or "spi"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

The browser and the development board must be on an interoperable network. In `wifi_ap` mode, first let the computer connect to the hotspot created by the development board; in `wifi_sta` or `lan` mode, both ends should be on the same LAN or have reachable routes.

## Code Flow

### 1. Connect to Network and Obtain Service Address

```python
netif, ip = connect_network(
    NETWORK_TYPE,
    ssid=WIFI_SSID,
    password=WIFI_PASSWORD,
    wlan_device=WLAN_DEVICE,
    timeout=NETWORK_TIMEOUT,
)
```

The returned `ip` is used to print the browser access address.

### 2. Create Listening Socket

```python
s = socket.socket()
addr = socket.getaddrinfo("0.0.0.0", 8081)[0][-1]
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)
```

- `0.0.0.0` means listening on all current IPv4 interfaces, not relying on dynamically generated network interface names.
- `SO_REUSEADDR` allows the port to be rebound quickly after the script restarts.
- `listen(5)` starts listening for TCP connections; the parameter `5` is the upper limit of the queue waiting to process connections.

### 3. Accept Browser Connection

```python
while True:
    try:
        client, client_address = server.accept()
        break
    except OSError as error:
        if error.errno != 11:
            raise
    os.exitpoint()
    time.sleep_ms(10)
```

RT-Smart Socket's `accept()` returns `EAGAIN` when there is currently no connection. The example waits briefly and retries, while calling `os.exitpoint()` to keep the script exitable. After accepting the connection, the serial port prints the browser address, and then `read_request()` sets the client Socket to non-blocking mode.

### 4. Read Complete Request Header

```python
request = bytearray()
client.setblocking(False)

while len(request) < MAX_REQUEST_BYTES:
    chunk = client.recv(min(256, MAX_REQUEST_BYTES - len(request)))
    if chunk:
        request.extend(chunk)
        if request.find(b"\r\n\r\n") >= 0:
            break
```

The HTTP request header ends with an empty line, i.e., the byte sequence `\r\n\r\n`. A single `recv()` is not guaranteed to get the complete request, so the example appends each fragment to the `bytearray` until the request header is complete. The maximum request size is 4096 bytes, with a wait time of 2 seconds, to prevent abnormal clients from occupying the service indefinitely.

### 5. Generate Device Status Page

```python
info = network_info(netif)
config = info["ifconfig"]
system = os.uname()
```

`network_info()` aggregates the current interface name, default interface, connection status, IP configuration, and MAC address; `os.uname()` provides the development board name, CanMV firmware version, and MicroPython build information. The page also displays the available heap memory returned by `gc.mem_free()`, uptime, all registered network interfaces, and browser address.

All dynamic values are first passed through `html_escape()` before being written into the response body, to prevent device names or request endpoint information from breaking the HTML structure.

### 6. Return Response and Exit

```python
body = build_status_page(netif, client_address, counter)
header = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    "Content-Length: %d\r\n"
    "Connection: close\r\n"
    "\r\n"
) % len(body)

client.setblocking(True)
client.sendall(header.encode() + body)
```

The response uses the CRLF line terminator required by HTTP, and explicitly specifies the body length through `Content-Length`. `sendall()` will send the complete response before closing the connection. Both the client and listening Socket are closed in `finally`. This teaching example only handles one successful request; the script needs to be run again before accessing it again.

## Running and Verification

1. Run the script and check the serial port output for `http://<IP>:8081/`.
2. Open this address in a browser that can access the development board.
3. The page should display three groups of device information: System, Request, and Network, and the serial port will print the original request.

When the access times out, sequentially check whether both ends can communicate with each other, whether the IP is still valid, and whether TCP port `8081` is blocked by the firewall.
