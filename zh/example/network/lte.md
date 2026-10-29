# USB 4G LTE 例程讲解

## 例程位置

- 开发板固件路径：`/sdcard/examples/14-Socket/network_lte.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/network_lte.py`

该例程通过 USB 串口向 EC200M 类 4G 模组发送 AT 命令，先查询模组版本，再发起
ECM 数据拨号。拨号成功后，系统网络驱动会把模组的数据接口自动注册为 LAN 类型
的网络设备。

## 运行前准备

1. 为 4G 模组安装天线并插入可用的 SIM 卡。
1. 将模组接到开发板的 USB Host 接口。
1. 确认固件已启用该模组需要的 USB Serial 和 CDC ECM 驱动。
1. 在 RT-Smart 命令行检查模组枚举出的 `/dev/ttyUSB*` 设备。

具体驱动选项、SIM 卡检查和 AT 调试方法见 [EC200M-CN 模组说明](./modules/ec200m.md)。

## 代码流程

### 1. 打开 AT 串口

```python
from usb import Serial

ser = Serial("/dev/ttyUSB1", 200)

while True:
    if ser.open():
        break
    time.sleep(1)
```

例程默认使用 `/dev/ttyUSB1`，并在打开失败时每秒重试。不同模组、固件或 USB
枚举顺序可能产生不同节点；若没有响应，应先确认真正的 AT 命令端口并修改该路径。

### 2. 查询模组固件版本

```python
ser.write("AT+GMR\r\n")
time.sleep(0.1)
data = ser.read()
print(data)
```

`AT+GMR` 用于确认串口通信正常并读取模组版本。正常情况下输出中应包含版本信息和
`OK`；乱码通常表示串口参数或端口不正确，没有响应则应检查供电、USB 枚举和端口。

### 3. 发起 ECM 拨号

```python
ser.write("AT+QNETDEVCTL=1,1,1\r\n")
time.sleep(0.1)
data = ser.read()
print(data)
```

该命令请求模组建立数据连接。AT 命令返回 `OK` 只表示命令已受理，模组仍可能需要
一段时间完成驻网、拨号、USB 网络接口注册和地址配置。

### 4. 关闭 AT 串口

```python
ser.close()
```

关闭 Python 串口对象不会主动断开已经建立的数据连接。后续若仍要查询信号、注册
状态或拨号状态，应在应用中保留串口并按模组 AT 手册管理它。

## 验证网络接口

脚本完成后，可在 RT-Smart 命令行使用 `ifconfig` 检查新接口和 IP。在 Python 中
也可以运行公共网络管理例程，确认设备已动态注册并取得地址：

```python
import network
from libs.Network import connect_network

print(network.get_dev_list())
netif, ip = connect_network("lan")
print(netif.netdev_name(), ip)
```

`connect_network("lan")` 会等待 LAN 类型接口取得有效地址并设置默认上行，不需要
假设 4G 数据接口一定名为 `eth0`。

若没有出现网络接口，依次检查 SIM 状态、天线、信号、APN、ECM 模式和 CDC ECM
驱动。接口已出现但没有 IP 时，继续检查拨号状态和运营商数据业务。
