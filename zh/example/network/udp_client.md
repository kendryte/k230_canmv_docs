# UDP Client 例程讲解

## 例程位置

- 开发板固件路径：`/sdcard/examples/14-Socket/udp_clinet.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/udp_clinet.py`

文件名中的 `clinet` 沿用当前固件和源码目录中的实际拼写。该例程把开发板作为 UDP
发送端，向电脑连续发送 10 个数据报。

## 运行前准备

先在电脑上启动 UDP 调试工具并监听一个端口，再修改脚本中的网络参数和目标地址：

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

把 `192.168.1.110` 改为电脑与开发板互通的 IP，把 `8080` 改为电脑端 UDP 监听
端口，并允许该 UDP 端口通过防火墙。

## 代码流程

### 1. 连接网络

```python
netif, _ = connect_network(...)
```

公共网络库等待接口取得 IP，并选择默认上行接口。

### 2. 解析目标地址并创建 UDP Socket

```python
addr = socket.getaddrinfo("192.168.1.110", 8080)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

`SOCK_DGRAM` 表示 UDP。它不需要像 TCP 那样先建立连接，每次发送时直接指定目标
地址。

### 3. 发送 10 个数据报

```python
for i in range(10):
    message = "K230 udp client send test {0} \r\n".format(i)
    s.sendto(message, addr)
    time.sleep(0.2)
```

每次 `sendto()` 对应一个独立 UDP 数据报，接收端能保留数据报边界。UDP 不保证
到达、顺序或去重；对可靠性有要求时需要应用层确认和重传。

### 4. 关闭 Socket

脚本发送完成后等待 1 秒，关闭 Socket 并打印 `end`。该例程只发送数据，没有调用
`recvfrom()`，因此不会读取服务端的回复。

## 运行与验证

1. 先启动电脑端 UDP 接收工具。
2. 运行 `/sdcard/examples/14-Socket/udp_clinet.py`。
3. 电脑端应收到序号 `0` 到 `9` 的 10 个数据报。
4. 若串口显示发送成功但电脑没有收到，重点检查目标 IP、UDP 端口、防火墙和 Wi-Fi
   热点的客户端隔离设置。
