# UDP Server 例程讲解

## 例程位置

- 开发板固件路径：`/sdcard/examples/14-Socket/udp_server.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/udp_server.py`

该例程在开发板的 UDP `8080` 端口接收数据报，打印发送端信息，并向原发送端回复
带计数的数据。

## 运行前准备

在脚本顶部配置联网方式：

```python
NETWORK_TYPE = "wifi_sta"  # "default"、"lan"、"wifi_sta" 或 "wifi_ap"
WLAN_DEVICE = "auto"       # "auto"、"usb"、"sdio" 或 "spi"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

电脑需要 UDP 调试工具，并且能访问开发板取得的 IP。

## 代码流程

### 1. 联网并解析监听地址

```python
netif, ip = connect_network(...)
addr = socket.getaddrinfo("0.0.0.0", 8080)[0][-1]
```

`ip` 用于打印客户端应访问的地址，`0.0.0.0` 则让服务监听所有当前 IPv4 接口。

### 2. 创建并绑定 UDP Socket

```python
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.settimeout(0)
```

- `SOCK_DGRAM` 创建 UDP Socket。
- `SO_REUSEADDR` 便于重启脚本后重新绑定端口。
- `settimeout(0)` 将 Socket 设为非阻塞模式。

### 3. 接收数据报

```python
data, peer_addr = s.recvfrom(800)
```

一次最多读取 800 字节。`recvfrom()` 同时返回数据和发送端地址，因此 UDP 不建立
连接也能把响应发回正确的客户端。脚本在进入循环前等待 1 秒；为避免非阻塞读取在
暂无数据时立即报错，测试端应在服务启动后及时发送数据。

### 4. 回复发送端

```python
s.sendto(b"%s have recv count=%d " % (data, counter), peer_addr)
```

响应包含收到的原始数据和当前计数。计数从 `0` 开始，处理 11 个非空数据报后关闭
Socket 并退出。

## 运行与验证

1. 运行脚本并查看串口输出的开发板 IP 和 `8080` 端口。
2. 在电脑 UDP 工具中将开发板地址设为目标并发送文本。
3. 串口应打印计数、数据和电脑地址，电脑端应收到开发板回复。
4. 没有数据时检查 UDP `8080` 防火墙规则、目标 IP 和热点客户端隔离设置。
