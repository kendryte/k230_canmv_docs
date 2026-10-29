# HTTP Server 例程讲解

## 例程位置

- 开发板固件路径：`/sdcard/examples/14-Socket/http_server.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/http_server.py`

该例程在开发板上启动一个简单的 HTTP/1.1 服务。浏览器连接 `8081` 端口后，服务
读取请求头并返回设备状态网页，展示系统版本、运行时间、可用内存、网卡和客户端
信息，然后关闭连接并退出。

## 运行前准备

在脚本顶部设置网络类型和 Wi-Fi 参数：

```python
NETWORK_TYPE = "wifi_sta"  # "default"、"lan"、"wifi_sta" 或 "wifi_ap"
WLAN_DEVICE = "auto"       # "auto"、"usb"、"sdio" 或 "spi"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

浏览器和开发板必须处于可互通的网络。`wifi_ap` 模式下，先让电脑连接开发板创建的
热点；`wifi_sta` 或 `lan` 模式下，两端应位于同一局域网或具有可达路由。

## 代码流程

### 1. 联网并取得服务地址

```python
netif, ip = connect_network(
    NETWORK_TYPE,
    ssid=WIFI_SSID,
    password=WIFI_PASSWORD,
    wlan_device=WLAN_DEVICE,
    timeout=NETWORK_TIMEOUT,
)
```

返回的 `ip` 用于打印浏览器访问地址。

### 2. 创建监听 Socket

```python
s = socket.socket()
addr = socket.getaddrinfo("0.0.0.0", 8081)[0][-1]
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)
```

- `0.0.0.0` 表示监听当前所有 IPv4 接口，不依赖动态生成的网卡名称。
- `SO_REUSEADDR` 允许脚本重启后尽快重新绑定端口。
- `listen(5)` 开始监听 TCP 连接，参数 `5` 是等待处理连接的队列上限。

### 3. 接收浏览器连接

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

RT-Smart Socket 的 `accept()` 在当前没有连接时会返回 `EAGAIN`。例程对此进行
短暂等待并重试，同时调用 `os.exitpoint()` 保持脚本可退出。接受连接后，串口会
打印浏览器地址，再由 `read_request()` 把客户端 Socket 设为非阻塞模式。

### 4. 读取完整请求头

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

HTTP 请求头以空行结束，即字节序列 `\r\n\r\n`。一次 `recv()` 不保证取得完整
请求，因此例程把每个分片追加到 `bytearray`，直到请求头完整。请求最大为 4096
字节，等待时间为 2 秒，避免异常客户端无限占用服务。

### 5. 生成设备状态页

```python
info = network_info(netif)
config = info["ifconfig"]
system = os.uname()
```

`network_info()` 汇总当前接口名称、默认接口、连接状态、IP 配置和 MAC 地址；
`os.uname()` 提供开发板名称、CanMV 固件版本和 MicroPython 构建信息。页面还显示
`gc.mem_free()` 返回的可用堆内存、运行时间、全部已注册网卡和浏览器地址。

所有动态值先经过 `html_escape()`，再写入响应正文，避免设备名或请求端信息破坏
HTML 结构。

### 6. 返回响应并退出

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

响应使用 HTTP 要求的 CRLF 行结束符，并通过 `Content-Length` 明确正文长度。
`sendall()` 会在关闭连接前完整发送响应。客户端和监听 Socket 都在 `finally` 中
关闭。这个教学例程只处理一个成功请求；再次访问前需要重新运行脚本。

## 运行与验证

1. 运行脚本并查看串口打印的 `http://<IP>:8081/`。
2. 在可访问开发板的浏览器中打开该地址。
3. 页面应显示 System、Request 和 Network 三组设备信息，串口会打印原始请求。

访问超时时，依次检查两端是否互通、IP 是否仍有效，以及 TCP `8081` 端口是否被
防火墙拦截。
