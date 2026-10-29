# HTTP Client 例程讲解

## 例程位置

- 开发板固件路径：`/sdcard/examples/14-Socket/http_client.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/http_client.py`

该例程先建立网络连接，再访问 `http://www.baidu.com/index.html`，并分别演示 Socket
的文件流接口与普通收发接口。

## 运行前准备

在脚本顶部修改网络配置：

```python
NETWORK_TYPE = "wifi_sta"  # "default"、"lan"、"wifi_sta" 或 "wifi_ap"
WLAN_DEVICE = "auto"       # "auto"、"usb"、"sdio" 或 "spi"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

HTTP 客户端需要可访问互联网并能正常解析 DNS。使用有线网络时，将
`NETWORK_TYPE` 改为 `"lan"`；复用已经联网的默认接口时使用 `"default"`。

## 代码流程

### 1. 连接网络

```python
netif, _ = connect_network(
    NETWORK_TYPE,
    ssid=WIFI_SSID,
    password=WIFI_PASSWORD,
    wlan_device=WLAN_DEVICE,
    timeout=NETWORK_TIMEOUT,
)
```

`connect_network()` 会等待接口取得有效 IP，并将它设为默认上行接口。网络未在
`NETWORK_TIMEOUT` 秒内就绪时会抛出异常，HTTP 请求不会继续执行。

### 2. 解析服务器地址

```python
ai = socket.getaddrinfo("www.baidu.com", 80)
addr = ai[0][-1]
```

例程最多重试 DNS 解析 3 次。串口中的 `Address infos` 是解析结果，
`Connect address` 是本次连接实际使用的地址。

### 3. 建立 TCP 连接

```python
s = socket.socket()
s.connect(addr)
```

HTTP/1.0 运行在 TCP 上，因此必须先连接服务器的 `80` 端口。

### 4. 使用文件流接口收发

```python
s = s.makefile("rwb", 0)
s.write(b"GET /index.html HTTP/1.0\r\n\r\n")
print(s.read())
```

`makefile()` 将 Socket 包装为可调用 `read()` 和 `write()` 的流。HTTP/1.0 请求完成
后服务器关闭连接，`read()` 因而能够读取到响应结束。

### 5. 使用普通 Socket 接口收发

```python
s.send(b"GET /index.html HTTP/1.0\r\n\r\n")
print(s.recv(4096))
```

普通接口使用 `send()` 和 `recv()`。一次 `recv(4096)` 最多读取 4096 字节，不保证
取得完整响应；实际应用应循环读取，直到服务器关闭连接或协议已给出完整长度。

脚本末尾依次调用 `main(use_stream=True)` 和 `main(use_stream=False)`，因此会发起两次
独立请求。

## 运行与排查

1. 在 CanMV IDE 中打开开发板固件路径下的脚本并运行。
2. 确认串口先输出联网信息，再输出 DNS 地址和 HTTP 响应。
3. 若一直出现 `getaddrinfo again`，检查 DNS、网关和互联网连接。
4. 若域名可解析但连接失败，检查目标服务、默认上行和网络防火墙。

相关接口见 [network 模块](../../api/extmod/k230_canmv_network_api_manual.md) 和
[socket 模块](../../api/extmod/k230_canmv_socket_api_manual.md)。
