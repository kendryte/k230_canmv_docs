# UDP 组播例程讲解

## 例程位置

开发板收发例程：

- 开发板固件路径：`/sdcard/examples/14-Socket/udp_multicast.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/udp_multicast.py`

电脑端配套脚本也随固件提供，但应在电脑的 Python 环境中运行：

- 发送端固件路径：`/sdcard/examples/14-Socket/udp_multicast_sender_pc.py`
- 发送端源码路径：`src/canmv/resources/examples/14-Socket/udp_multicast_sender_pc.py`
- 接收端固件路径：`/sdcard/examples/14-Socket/udp_multicast_receiver_pc.py`
- 接收端源码路径：`src/canmv/resources/examples/14-Socket/udp_multicast_receiver_pc.py`

组播允许一个发送端把同一数据报发送给同一组播组中的多个接收端。开发板脚本通过
`IS_SENDER` 在发送与接收模式之间切换，电脑端脚本用于组成另一端进行验证。

## 参数配置

```python
MULTICAST_GROUP = "239.255.0.1"
MULTICAST_PORT = 5007
IS_SENDER = False

NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

开发板与电脑必须位于支持组播转发的同一局域网。交换机、无线路由器或热点若启用了
客户端隔离、组播过滤或 IGMP 限制，数据可能无法到达。

## 公共流程

```python
netif, ip = connect_network(...)

if IS_SENDER:
    multicast_sender(ip)
else:
    multicast_receiver()
```

脚本先取得有效 IP，再根据 `IS_SENDER` 选择角色。默认值 `False` 表示开发板作为
接收端。

## 开发板发送模式

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack("b", 1)
sock.setsockopt(0, 33, ttl)
sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
```

这里的选项 `0` 和 `33` 分别对应 `IPPROTO_IP` 与 `IP_MULTICAST_TTL`。TTL 设置为
`1`，让数据只在本地网络传播。脚本每 2 秒发送一次，并在消息中附带开发板 IP 和
递增计数。

测试步骤：

1. 在电脑上运行 `udp_multicast_receiver_pc.py`。
2. 将开发板脚本的 `IS_SENDER` 改为 `True` 后运行。
3. 电脑端应持续显示来自开发板的组播消息。

## 开发板接收模式

```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", MULTICAST_PORT))

mreq = struct.pack(
    "4s4s",
    inet_aton(MULTICAST_GROUP),
    inet_aton("0.0.0.0"),
)
sock.setsockopt(0, 35, mreq)
```

接收端先监听所有接口的 `5007` 端口，再通过成员请求加入 `239.255.0.1`。选项 `35`
对应 `IP_ADD_MEMBERSHIP`。收到数据后，脚本打印发送端地址和解码后的正文；不能按
UTF-8 解码的数据会标记为二进制内容。

测试步骤：

1. 保持开发板脚本的 `IS_SENDER = False` 并运行。
2. 在电脑上运行 `udp_multicast_sender_pc.py`。
3. 开发板串口应每秒显示一条 `Hello from PC multicast sender!`。

## 排查要点

- 确认两端的组播地址和端口完全一致。
- 确认系统防火墙允许 UDP `5007`。
- 多网卡电脑应确认组播流量从与开发板互通的接口发出。
- 普通 UDP 单播正常而组播无数据时，重点检查接入点的客户端隔离、IGMP Snooping
  和组播过滤设置。
