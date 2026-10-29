# HTTP Client Routine Explanation

## Routine Location

- Development board firmware path: `/sdcard/examples/14-Socket/http_client.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/http_client.py`

This routine first establishes a network connection, then accesses `http://www.baidu.com/index.html`, and demonstrates both the Socket file stream interface and the regular send/receive interface.

## Preparation Before Running

Modify the network configuration at the top of the script:

```python
NETWORK_TYPE = "wifi_sta"  # "default", "lan", "wifi_sta" or "wifi_ap"
WLAN_DEVICE = "auto"       # "auto", "usb", "sdio" or "spi"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

The HTTP client requires internet access and proper DNS resolution. When using a wired network, change `NETWORK_TYPE` to `"lan"`; use `"default"` to reuse the already-connected default interface.

## Code Flow

### 1. Connect to the Network

```python
netif, _ = connect_network(
    NETWORK_TYPE,
    ssid=WIFI_SSID,
    password=WIFI_PASSWORD,
    wlan_device=WLAN_DEVICE,
    timeout=NETWORK_TIMEOUT,
)
```

`connect_network()` waits for the interface to obtain a valid IP and sets it as the default uplink interface. An exception is thrown if the network is not ready within `NETWORK_TIMEOUT` seconds, and the HTTP request will not proceed.

### 2. Resolve the Server Address

```python
ai = socket.getaddrinfo("www.baidu.com", 80)
addr = ai[0][-1]
```

The routine retries DNS resolution up to 3 times. The `Address infos` in the serial console is the resolution result, and `Connect address` is the actual address used by this connection.

### 3. Establish a TCP Connection

```python
s = socket.socket()
s.connect(addr)
```

HTTP/1.0 runs on TCP, so you must first connect to the server's port `80`.

### 4. Send and Receive Using the File Stream Interface

```python
s = s.makefile("rwb", 0)
s.write(b"GET /index.html HTTP/1.0\r\n\r\n")
print(s.read())
```

`makefile()` wraps the Socket into a stream that can call `read()` and `write()`. After the HTTP/1.0 request is complete, the server closes the connection, so `read()` can read until the response ends.

### 5. Send and Receive Using the Regular Socket Interface

```python
s.send(b"GET /index.html HTTP/1.0\r\n\r\n")
print(s.recv(4096))
```

The regular interface uses `send()` and `recv()`. A single `recv(4096)` reads at most 4096 bytes and does not guarantee obtaining the complete response; practical applications should read in a loop until the server closes the connection or the protocol provides a complete length.

At the end of the script, `main(use_stream=True)` and `main(use_stream=False)` are called in sequence, so two independent requests are initiated.

## Running and Troubleshooting

1. Open the script under the development board firmware path in CanMV IDE and run it.
2. Confirm that the serial console first outputs network connection information, then outputs the DNS address and HTTP response.
3. If `getaddrinfo again` keeps appearing, check DNS, gateway, and internet connection.
4. If the domain name resolves but the connection fails, check the target service, default uplink, and network firewall.

For related interfaces, see [network module](../../api/extmod/k230_canmv_network_api_manual.md) and [socket module](../../api/extmod/k230_canmv_socket_api_manual.md).
