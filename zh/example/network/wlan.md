# 使用无线网例程讲解

## 例程位置

Wi-Fi STA 例程：

- 开发板固件路径：`/sdcard/examples/14-Socket/network_wlan_sta.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/network_wlan_sta.py`

Wi-Fi AP 例程：

- 开发板固件路径：`/sdcard/examples/14-Socket/network_wlan_ap.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/network_wlan_ap.py`

## WLAN 设备选择

两个例程都使用：

```python
WLAN_DEVICE = "auto"
```

可选值为 `"auto"`、`"usb"`、`"sdio"` 和 `"spi"`。通常保留 `"auto"`，让
系统从已注册设备中选择。只有同时安装多块 Wi-Fi 且应用必须使用指定传输类型时，
才固定该参数。

当前 SDK 可使用 RTL8189FTV/RTL8733BS 和 Broadcom brcmfmac SDIO、RW007 SPI、
AIC8800 USB/SDIO，以及按固件配置启用的 ESP-Hosted SPI/SDIO 方案。具体驱动、
默认板级配置和安全模式限制见
[Wi-Fi 驱动与设备选择](../../userguide/wifi_drivers.md)。`WLAN_DEVICE` 只选择
传输类型，不能按厂商或型号选择同一总线上的设备。

## Wi-Fi STA 例程

STA 模式用于连接现有无线路由器或热点。

### 1. 配置凭据

```python
SSID = "TEST"
PASSWORD = "12345678"
WLAN_DEVICE = "auto"
```

将 SSID 和密码修改为现场热点信息。SSID 区分大小写。

### 2. 连接并等待地址

```python
from libs.Network import connect_network

sta, ip = connect_network(
    "wifi_sta",
    ssid=SSID,
    password=PASSWORD,
    wlan_device=WLAN_DEVICE,
    timeout=10,
)
```

这一步依次完成物理 WLAN 选择、设备注册等待、热点连接、DHCP 地址等待和默认
上行设置。失败或 10 秒内未取得地址时抛出异常，不需要应用自行无限轮询。

### 3. 查看状态

```python
print(sta.ifconfig())
print(sta.status())
```

`ifconfig()` 返回 IP 参数，`status()` 返回连接状态。如需查看当前 Wi-Fi STA
对应的动态设备名，可额外调用 `sta.netdev_name()`。

### 4. 断开测试

```python
sta.disconnect()
print("断开连接")
print(sta.status())
```

例程最后主动断开只用于演示。实际需要持续联网的程序应删除这几行。断开后，
默认路由管理会尝试选择其他已就绪的 LAN 或 Wi-Fi STA。

## Wi-Fi AP 例程

AP 模式用于让手机或电脑连接到开发板创建的热点。

### 1. 创建热点

```python
from libs.Network import connect_network

ap, ip = connect_network(
    "wifi_ap",
    ssid="k230_ap_wjx",
    password="12345678",
    wlan_device=WLAN_DEVICE,
)
```

公共网络库选择 WLAN AP 设备、创建加密热点并等待 AP 地址。Wi-Fi AP 是本地
接入接口，不会被设置为互联网默认上行。

### 2. 查看热点信息

```python
print(ap.info())
print(ap.status())
```

`info()` 返回热点配置，`status()` 返回 AP 状态。如需查看动态设备名，可调用
`ap.netdev_name()`；需要查看已连接终端时可使用 `ap.status("stations")`。

### 3. 停止热点

示例保持热点运行。应用退出前如需主动停止，可调用：

```python
ap.stop()
```

## 运行与验证

STA 测试：

1. 打开 `/sdcard/examples/14-Socket/network_wlan_sta.py`。
1. 修改 SSID 和密码后运行。
1. 确认 `ifconfig()` 中 IP 不为 `0.0.0.0`。
1. 例程执行到末尾后会主动断开。

AP 测试：

1. 打开 `/sdcard/examples/14-Socket/network_wlan_ap.py` 并运行。
1. 用手机搜索并连接 `k230_ap_wjx`，密码为 `12345678`。
1. 检查串口打印的 AP 信息和状态。

若指定 `WLAN_DEVICE` 后报告设备不可用，先改回 `"auto"`。完整接口定义见
[network 模块 API 手册](../../api/extmod/k230_canmv_network_api_manual.md)。
