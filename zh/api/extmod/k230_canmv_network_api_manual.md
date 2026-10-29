# `network` 模块 API 手册

## 概述

本模块主要用于配置和查看网络参数，配置完成后，方可使用 `socket` 模块进行网络通信。

系统会在网卡驱动加载时自动注册网络设备。设备名由系统动态分配，例如 USB
以太网通常为 `eth0`，Wi-Fi STA/AP 通常为 `wlan0`/`wlan0ap`。应用不应写死设备名，
应通过本模块的设备查询接口或 `libs.Network` 获取当前名称。公共网络库在开发板
固件中的路径为 `/sdcard/libs/Network.py`，SDK 源码路径为
`src/canmv/resources/libs/Network.py`。

支持的 Wi-Fi vendor driver、固件配置和安全模式限制见
[Wi-Fi 驱动与设备选择](../../userguide/wifi_drivers.md)。

## 网络设备管理

### `network.get_dev_list()`

返回当前已注册的网络设备名称列表。设备热插拔后，列表会随之变化。

```python
import network

print(network.get_dev_list())
```

### `network.get_default_dev()`

返回当前默认上行网络设备的名称。没有满足路由条件的设备时返回 `None`。

### `network.set_default_dev(device)`

设置首选的默认上行设备。`device` 可以是 LAN/WLAN 对象、`get_dev_list()` 返回的
设备名，或逻辑接口常量。Wi-Fi AP 不能作为默认上行设备。

首选设备不可用时，系统会自动切换到其他可用上行设备；首选设备恢复后会自动
切回。传入 `None` 可清除首选设备并恢复全自动选择：

```python
import network

lan = network.LAN()
network.set_default_dev(lan)
print(network.get_default_dev())

# 恢复自动选择，而不是禁用默认路由
network.set_default_dev(None)
```

自动选择只考虑已启用、链路已连接、已取得非零 IP 和网关的 LAN 与 Wi-Fi STA
接口。多个接口同时可用时，默认优先 LAN。

### `network.get_netdev_name(interface_id)`

将逻辑接口解析为当前设备名。`interface_id` 可使用 `network.STA_IF`、
`network.AP_IF` 或 `network.LAN_IF`；接口尚不可用时返回 `None`。

## `LAN` 类

参考文档: [Micropython LAN](https://docs.micropython.org/en/latest/library/network.LAN.html)

此类为有线网络的配置接口。示例代码如下：

```python
import network
nic = network.LAN()
print(nic.ifconfig())

# 配置完成后，即可像往常一样使用 socket
...
```

### 构造函数

- **class** `network.LAN([interface_id])` [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN)

  创建一个有线以太网对象。推荐省略 `interface_id`，或传入
  `network.LAN_IF`。`LAN_RTL8152`、`LAN_NCM` 和 `LAN_ECM` 为兼容旧代码保留，
  新代码不应通过芯片型号选择 LAN。

### 方法

- **LAN.active([state])** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.active)

  不传参数时查询接口是否可用。传入 `True` 可确认接口已就绪；RT-Smart 不支持
  通过该方法停用网络接口，传入 `False` 不会关闭设备。

- **LAN.isconnected()** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.isconnected)

  返回 `True` 表示已连接到网络，返回 `False` 表示未连接。

- **LAN.ifconfig([(ip, subnet, gateway, dns)])** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.ifconfig)

  获取或设置 IP 级别的网络接口参数，包括 IP 地址、子网掩码、网关和 DNS 服务器。无参数调用时，返回一个包含上述信息的四元组；如需设置参数，传入包含 IP 地址、子网掩码、网关和 DNS 的四元组。例如：

  ```python
  nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  ```

- **LAN.config(*config_parameters*)** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.config)

  获取或设置网络接口参数。当前仅支持设置或获取 MAC 地址。例如：

  ```python
  import network
  lan = network.LAN()
  # 设置 MAC 地址
  lan.config(mac="42:EA:D0:C2:0D:83")
  # 获取 MAC 地址
  print(lan.config("mac"))
  ```

- **LAN.netdev_name()**

  返回该对象当前对应的动态网络设备名；设备不可用时返回 `None`。

## `WLAN` 类

参考文档: [Micropython WLAN](https://docs.micropython.org/en/latest/library/network.WLAN.html)

此类为 WiFi 网络配置接口。示例代码如下：

```python
import network
import time

SSID = "TEST"
PASSWORD = "12345678"

sta = network.WLAN(network.STA_IF)

sta.connect(SSID, PASSWORD)

timeout = 10  # 单位：秒
start_time = time.time()

while not sta.isconnected():
    if time.time() - start_time > timeout:
        print("连接超时")
        break
    time.sleep(1)  # 请稍等片刻再连接

print(sta.ifconfig())

print(sta.status())

# 这里的断开网络，只是一个测试。实际应用可不断开
sta.disconnect()
print("断开网络")
print(sta.status())

```

### 构造函数

- **class** `network.WLAN([interface_id[, wlan_device]])`

  创建 WLAN 网络接口对象。省略 `interface_id` 时默认为 STA。该参数支持
  `network.STA_IF`（站模式，连接
  上游 Wi-Fi 接入点）和 `network.AP_IF`（接入点模式）。可选的
  `wlan_device` 用于在多块 Wi-Fi 设备间选择物理传输类型：

  - `network.WLAN_AUTO`：自动选择，推荐使用；
  - `network.WLAN_USB`：USB Wi-Fi；
  - `network.WLAN_SDIO`：SDIO Wi-Fi；
  - `network.WLAN_SPI`：SPI Wi-Fi。

  自动选择优先使用已在当前角色工作的设备；否则按 SDIO、SPI、USB 的顺序
  查找。该参数选择传输类型，不选择 vendor model；只有确实需要固定某种硬件
  连接方式时才传第二个参数。

  ```python
  # 自动选择可用 Wi-Fi
  sta = network.WLAN(network.STA_IF, network.WLAN_AUTO)

  # 明确选择 USB Wi-Fi
  usb_sta = network.WLAN(network.STA_IF, network.WLAN_USB)
  ```

### 方法

- **WLAN.active()**

  不传参数时查询接口是否可用。传入 `True` 时等待所选 WLAN 设备完成注册；
  RT-Smart 不支持通过该方法停用接口，传入 `False` 不会关闭设备。

- **WLAN.connect(ssid=None, key=None, [info = None])**

  连接到指定 `ssid` 或者 `info`，`info` 是通过 `scan` 返回的结果。

  > 仅 `Sta` 模式可用

- **WLAN.disconnect()**

  `Sta` 模式时断开当前的 WiFi 网络连接。
  `Ap` 模式时，可传入指定 `mac` 来断开设备的连接。

- **WLAN.scan()**

  扫描可用的 WiFi 网络。此方法仅在 STA 模式下有效，返回的列表包含每个网络的信息，例如：

  ```bash
  # print(sta.scan())
  [{"ssid":"XCTech", "bssid":xxxxxxxxx, "channel":3, "rssi":-76, "security":"SECURITY_WPA_WPA2_MIXED_PSK", "band":"2.4G", "hidden":0},...]
  ```
  
- **WLAN.status([param])**

  返回当前网络连接的信息。当不传参数时，返回当前的连接状态。例如：

  ```python
  # 查看连接状态 等同与 sta.isconnected()
  print(sta.status())

  # 查看连接的信号质量
  print(sta.status("rssi"))
  ```

  支持的配置参数包括：

  - `Sta` 模式时
    - `rssi`: 连接信号质量
    - `ap`: 连接的热点名称
  - `Ap` 模式时
    - `stations`: 返回连接的设备信息
  
- **WLAN.isconnected()**

  返回是否连接到热点

  > 仅 `Sta` 模式可用

- **WLAN.ifconfig([(ip, subnet, gateway, dns)])**

  获取或设置 IP 级别的网络接口参数。无参数调用时，返回包含 IP 地址、子网掩码、网关和 DNS 服务器的四元组；传入参数则设置这些值。例如：

  ```python
  sta.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  ```

- **WLAN.config(param)**

  获取或设置网络接口的配置参数。设置参数时使用关键字参数语法；查询参数时，传递参数名即可。例如：

  ```python
  # 查看 auto_reconnect 配置
  print(sta.config('auto_reconnect'))

  # 设置自动重连
  sta.config(auto_reconnect = True)
  ```

  支持的配置参数包括：

  - `Sta` 模式时
    - `mac`: `mac` 地址
    - `auto_reconnect`: 是否自动重连
  - `Ap` 模式时
    - `ssid`: 热点名称。传入该参数时会配置并启动热点，可同时使用 `key` 和 `security` 指定密码及安全类型
    - `key`: 热点密码，加密模式下长度应为 8 到 64 个字符；开放模式下省略该参数
    - `security`: 热点安全类型。配置时须同时传入 `ssid`，也可通过 `ap.config('security')` 查询当前值
    - `info`: 当前热点信息，仅可查询
    - `country`: 国家代码

  AP 模式常用的安全类型如下。具体可用类型取决于开发板使用的 WiFi 驱动，不支持的类型会导致配置失败并返回 `False`。

  - `SECURITY_OPEN`: 开放热点，不使用密码
  - `SECURITY_WPA_TKIP_PSK`: WPA-PSK（TKIP）
  - `SECURITY_WPA2_AES_PSK`: WPA2-PSK（AES），推荐使用
  - `SECURITY_WPA2_MIXED_PSK`: WPA2-PSK（AES/TKIP 混合模式）

  创建 WPA2 加密热点：

  ```python
  import network

  ap = network.WLAN(network.AP_IF)
  result = ap.config(
      ssid='CanMV_AP',
      key='12345678',
      security=ap.SECURITY_WPA2_AES_PSK,
  )
  print(result)
  print(ap.config('security'))
  ```

  创建开放热点时省略 `key`，并将安全类型设为 `SECURITY_OPEN`：

  ```python
  ap.config(ssid='CanMV_Open', security=ap.SECURITY_OPEN)
  ```

  未指定 `security` 时，传入 `key` 默认使用 `SECURITY_WPA2_AES_PSK`；未传入 `key` 默认使用 `SECURITY_OPEN`。
  
- **WLAN.stop()**

  停止开启热点

  > 仅 `Ap` 模式可用

- **WLAN.info()**

  查询当前热点信息

  > 仅 `Ap` 模式可用

- **WLAN.netdev_name()**

  返回该 WLAN 对象所选物理设备在当前角色下的动态网络设备名；设备不可用时
  返回 `None`。

## `libs.Network` 公共网络库

CanMV 示例统一使用 `/sdcard/libs/Network.py` 管理网络。该库负责选择接口、等待
IP、设置默认上行、显示设备信息，并让一个应用的各组件复用同一个接口对象。

### 网络类型与 Wi-Fi 设备

`network_type` 支持：

- `"default"`：复用已经联网的默认/自动接口；
- `"lan"`：使用 LAN；
- `"wifi_sta"`：连接 Wi-Fi AP；
- `"wifi_ap"`：创建 Wi-Fi AP。

`wlan_device` 支持 `"auto"`、`"usb"`、`"sdio"` 和 `"spi"`，默认使用
`"auto"`。

### `connect_network()`

连接指定网络并返回 `(netif, ip)`：

```python
from libs.Network import connect_network

netif, ip = connect_network(
    "wifi_sta",
    ssid="TEST",
    password="12345678",
    wlan_device="auto",
    timeout=20,
)
print(ip)
```

常用参数包括 `ip_config`（`"dhcp"` 或静态 `ifconfig` 四元组）、`channel`、
`set_default` 和 `show`。LAN 与 Wi-Fi STA 默认会被设置为首选上行；Wi-Fi AP
不会被设置为默认上行。

### `NetworkManager`

`NetworkManager` 保存并复用接口，适合 HTTP、WebSocket、媒体推流等由多个组件
共享网络的应用。重复调用 `connect()` 时，若原接口仍然可用，不会创建第二个
接口。

```python
from libs.Network import NetworkManager

manager = NetworkManager(
    network_type="wifi_sta",
    ssid="TEST",
    password="12345678",
    wlan_device="auto",
    timeout=20,
)
netif, ip = manager.connect()
manager.show_info()
```

主要方法：

- `connect(**kwargs)`：连接或复用接口，返回 `(netif, ip)`；
- `disconnect(restore_default=True)`：停止 Wi-Fi，并按需恢复自动路由选择；
- `info()` / `show_info()`：返回或打印当前接口信息；
- `show_devices()`：打印并返回已注册设备列表；
- `wait_for_ip()`：等待当前接口取得 IP；
- `set_default()`：将当前接口设为首选上行；
- `scan()`：使用所选 Wi-Fi 设备扫描热点。

### 其他辅助函数

- `get_interface()`：取得接口对象，但不连接或修改默认路由；
- `get_devices()` / `get_default_device()` / `set_default_device()`：设备列表与默认
  上行管理；
- `configure_ip()` / `wait_for_ip()` / `has_ip()`：IP 配置与就绪检查；
- `network_device_name()` / `network_info()` / `show_network_info()`：查询接口运行
  信息；
- `mac_address()`：以小写冒号格式返回 MAC 地址；
- `scan_wifi()`：在指定 Wi-Fi 设备上扫描热点。
