# 使用有线网例程讲解

## 例程位置

- 开发板固件路径：`/sdcard/examples/14-Socket/network_lan.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/network_lan.py`

## 环境准备

将开发板支持的 USB 以太网适配器或 USB 4G ECM/NCM 网卡接入开发板，并连接到
能够提供 DHCP 的路由器或网络。USB LAN 的设备名会动态分配，例程通过逻辑 LAN
接口选择设备，不依赖固定名称。

## 代码流程

### 1. 导入公共网络函数

```python
from libs.Network import configure_ip, connect_network, network_device_name
```

- `connect_network()`：选择 LAN、启动 DHCP、等待 IP，并设置默认上行；
- `configure_ip()`：应用静态地址或 DHCP，并等待地址生效；
- `network_device_name()`：读取当前 LAN 对应的实际 netdev 名称。

### 2. 使用 DHCP 连接 LAN

```python
a, ip = connect_network("lan")
print(a.active())
print(a.ifconfig())
```

`a` 是 `network.LAN` 对象，`ip` 是等待成功后取得的 IPv4 地址。`active()` 在
RT-Smart 上用于查询接口是否可用，不用于关闭设备。`ifconfig()` 返回：

```text
(IP 地址, 子网掩码, 默认网关, DNS 服务器)
```

### 3. 临时切换为静态地址

```python
configure_ip(a, (
    "192.168.0.4",
    "255.255.255.0",
    "192.168.0.1",
    "8.8.8.8",
))
print(a.ifconfig())
```

四个值必须与实际网络匹配。示例地址只用于演示；若网段或网关不匹配，切换后
网络通信会中断。

### 4. 恢复 DHCP

```python
ip = configure_ip(a, "dhcp")
print("LAN device:", network_device_name(a))
print("LAN address:", ip)
```

`configure_ip()` 不只发起 DHCP，还会等待非零 IP，因此后续 Socket 代码无需
自行轮询 `ifconfig()`。

### 5. 查询 MAC 地址

```python
print(a.config("mac"))
```

返回值为 6 字节 MAC。需要冒号分隔字符串时，可使用
`libs.Network.mac_address(a)`。

## 运行与验证

1. 在 CanMV IDE 中打开 `/sdcard/examples/14-Socket/network_lan.py`。
1. 确认网卡和网线已连接，再运行脚本。
1. 第一次 `ifconfig()` 应显示 DHCP 地址。
1. 静态地址阶段应显示示例四元组。
1. 恢复 DHCP 后，`LAN address` 应重新显示路由器分配的地址。

```{important}
静态地址 `192.168.0.4` 可能与现有设备冲突。正式使用前必须根据实际网段修改，
或删去静态地址测试，只保留 DHCP 部分。
```

USB 4G ECM/NCM 的 Python 使用方式与 LAN 相同。支持的模组和驱动配置可参考
[EC200M-CN](./modules/ec200m.md)。完整接口见
[network 模块 API 手册](../../api/extmod/k230_canmv_network_api_manual.md)。
