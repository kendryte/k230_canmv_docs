# TCP Client 例程讲解

## 例程位置

- 开发板固件路径：`/sdcard/examples/14-Socket/tcp_client.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/tcp_client.py`

该例程把开发板作为 TCP 客户端，连接电脑上的 TCP 服务，并连续发送 10 条测试
消息。

## 运行前准备

先在电脑上启动 TCP 调试工具并监听一个端口。然后修改脚本中的两类配置：

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

把 `192.168.1.110` 改为电脑的 IP，把 `8080` 改为调试工具监听的 TCP 端口。电脑与
开发板必须网络互通，电脑防火墙也必须允许该端口入站。

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

公共网络库负责选择网卡、等待 IP 和设置默认上行，应用无需写死 netdev 名称。

### 2. 创建 TCP Socket 并解析地址

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
addr = socket.getaddrinfo("192.168.1.110", 8080)[0][-1]
```

`AF_INET` 选择 IPv4，`SOCK_STREAM` 选择有连接、可靠且有序的 TCP 字节流。
`getaddrinfo()` 同时适用于 IPv4 字符串和域名。

### 3. 连接服务端

```python
s.connect(addr)
```

TCP 必须完成连接后才能发送数据。连接被拒绝通常表示目标地址可达，但对应端口没有
服务监听；连接超时通常与地址、路由或防火墙有关。

### 4. 连续发送消息

```python
for i in range(10):
    message = "K230 tcp client send test {0} \r\n".format(i)
    s.write(message)
    time.sleep(0.2)
```

例程每隔 `0.2` 秒发送一条带序号的消息。TCP 是字节流，不保留单次 `write()` 的
消息边界；示例用 `\r\n` 方便接收端按行显示或拆分数据。

### 5. 关闭连接

发送完成后脚本等待 1 秒，再调用 `s.close()` 释放连接并打印 `end`。

## 运行与验证

1. 先启动电脑端 TCP 服务并确认监听地址和端口。
2. 在 CanMV IDE 中运行开发板固件路径下的脚本。
3. 电脑端应收到序号 `0` 到 `9` 的 10 条消息。
4. 若电脑有多块网卡，目标 IP 应选择与开发板互通的那一个，而不是回环地址。
