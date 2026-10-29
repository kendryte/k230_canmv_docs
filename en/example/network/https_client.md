# HTTPS Client Example Walkthrough

## Example Location

Low-level Socket and TLS version:

- Board firmware path: `/sdcard/examples/14-Socket/https_client.py`
- SDK source path: `src/canmv/resources/examples/14-Socket/https_client.py`

`requests` high-level interface version:

- Board firmware path: `/sdcard/examples/14-Socket/https_client2.py`
- SDK source path: `src/canmv/resources/examples/14-Socket/https_client2.py`

Both examples access `https://www.baidu.com` and are used to compare the differences
between manually establishing a TLS connection and using a high-level HTTP client
library.

## Preparation Before Running

Both scripts use the same common network configuration. Modify the Wi-Fi credentials,
or change `NETWORK_TYPE` to `"lan"` or `"default"`:

```python
NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

The board must be able to access the Internet and resolve DNS. In real applications,
if certificate validity period verification is enabled in the TLS configuration, you
should also make sure the device time is correct first.

## Low-level TLS Version

### 1. Resolve and Connect to the HTTPS Port

```python
addr = usocket.getaddrinfo("www.baidu.com", 443)[0][-1]
sock = usocket.socket()
sock.connect(addr)
```

HTTPS uses TCP port `443` by default. At this point, only the TCP connection has
been established; the encrypted channel has not yet been set up.

### 2. Wrap the TLS Socket

```python
ssl_sock = ussl.wrap_socket(sock, server_hostname="www.baidu.com")
```

`server_hostname` provides SNI during the TLS handshake. When multiple websites share
the same IP, the server relies on SNI to select the corresponding certificate and
site.

### 3. Send the HTTP Request and Read in a Loop

```python
ssl_sock.write(
    b"GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: close\r\n\r\n"
)

while True:
    data = ssl_sock.read()
    if not data:
        break
    print(data.decode(), end="")
```

The request uses `Connection: close`, and the read loop ends when the server closes
the connection. Finally, `ssl_sock.close()` is called to release the TLS and TCP
resources.

## requests high-level version

```python
response = requests.get("https://www.baidu.com")
print(response.text)
response.close()
```

`requests.get()` internally handles DNS, TCP, TLS and HTTP processing, suitable for ordinary business requests. After reading
the response, you should still explicitly call `response.close()` to promptly release the Socket and memory.

## Running and Troubleshooting

1. When learning for the first time, run `https_client2.py` first to confirm that the network and HTTPS basic environment are normal.
2. Then run `https_client.py` to observe the raw HTTP status line, response headers, and body.
3. For DNS errors, check the network, gateway, and DNS; for connection timeouts, check the default uplink and firewall.
4. When the TLS handshake fails, check the system time, target domain name, SNI, and the TLS algorithms supported by the firmware.
