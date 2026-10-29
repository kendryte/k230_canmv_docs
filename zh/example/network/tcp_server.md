# TCP Server 例程讲解

## 例程位置

- 开发板固件路径：`/sdcard/examples/14-Socket/tcp_server.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/tcp_server.py`

该例程把开发板作为 TCP 服务端，在 `8080` 端口等待连接，向客户端发送欢迎消息，
并回显收到的数据。

## 运行前准备

在脚本顶部配置联网方式：

```python
NETWORK_TYPE = "wifi_sta"  # "default"、"lan"、"wifi_sta" 或 "wifi_ap"
WLAN_DEVICE = "auto"       # "auto"、"usb"、"sdio" 或 "spi"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

电脑端需要 TCP 客户端或网络调试工具，并且能够访问开发板取得的 IP。

## 代码流程

### 1. 联网并取得 IP

```python
netif, ip = connect_network(...)
```

连接成功后，`ip` 会用于输出 `tcp server <IP> port:8080`，这是客户端应连接的地址。

### 2. 创建并配置监听 Socket

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
addr = socket.getaddrinfo("0.0.0.0", 8080)[0][-1]
s.bind(addr)
s.settimeout(0)
s.listen(5)
```

- `SOCK_STREAM` 创建 TCP Socket。
- `SO_REUSEADDR` 便于脚本重启后重新绑定同一端口。
- `0.0.0.0` 监听所有 IPv4 接口，不依赖动态 netdev 名称。
- `settimeout(0)` 使用非阻塞模式，等待期间仍可调用 `os.exitpoint()` 响应退出。

### 3. 接受连接

```python
client_sock, client_addr = s.accept()
client_sock.setblocking(False)
```

没有待处理连接时，非阻塞 `accept()` 可能返回 `errno == 11`，例程会继续等待。连接
建立后会打印客户端地址，并发送一条包含连接计数的欢迎消息。

### 4. 读取并回显数据

```python
h = client_stream.read()
if h is None:
    continue
if h != b"":
    print(h)
    client_stream.write("recv :%s" % h)
```

`None` 表示当前暂时没有数据；非空数据会打印到串口并加上 `recv :` 回发。由于 TCP
不保留消息边界，正式应用应自行定义定长、分隔符或长度字段协议。

### 5. 连接生命周期

例程把包含 `end` 的数据作为当前连接的结束标记，关闭客户端 Socket 后返回
`accept()` 等待下一个连接：

```python
if b"end" in h:
    client_stream.close()
    break
```

`read()` 返回字节数据，因此结束标记也应使用 `b"end"`。若当前脚本仍使用字符串
`"end"`，请先按上面的写法修正，否则严格区分字符串和字节的运行时会报告类型
错误。计数超过 10 后，服务关闭监听 Socket 并退出。这个例程按客户端逐个处理
连接；需要持续并发服务时，应增加连接状态管理和多客户端调度。

## 运行与验证

1. 运行脚本并记下串口输出的 IP 和 `8080` 端口。
2. 在电脑 TCP 客户端中连接该地址。
3. 确认电脑收到欢迎消息，然后发送文本。
4. 串口应打印收到的字节，电脑端应收到带 `recv :` 前缀的回显。
5. 发送 `end` 结束当前连接。

连接失败时检查开发板 IP 是否变化、两端是否处于可达网络，以及 TCP `8080` 是否被
防火墙拦截。
