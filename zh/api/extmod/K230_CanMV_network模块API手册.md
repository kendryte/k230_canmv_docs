# 2.2 `network` 模块 API 手册

## 1. 概述

本模块主要用于配置和查看网络参数，配置完成后，方可使用 `socket` 模块进行网络通信。

## 2. `LAN` 类

参考文档: [Micropython LAN](https://docs.micropython.org/en/latest/library/network.LAN.html)

此类为有线网络的配置接口。示例代码如下：

```python
import network
nic = network.LAN()
print(nic.ifconfig())

# 配置完成后，即可像往常一样使用 socket
...
```

### 2.1 构造函数

- **class** `network.LAN()` [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN)

  创建一个有线以太网对象。

### 2.2 方法

- **LAN.active([state])** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.active)

  激活或停用网络接口。传递布尔参数 `True` 表示激活，`False` 表示停用。如果不传参数，则返回当前状态。

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

## 3. `WLAN` 类

参考文档: [Micropython WLAN](https://docs.micropython.org/en/latest/library/network.WLAN.html)

此类为 WiFi 网络配置接口。示例代码如下：

```python
import network
# 启用 STA 模式并连接到 WiFi 接入点
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('your-ssid', 'your-password')
# 配置完成后，即可像往常一样使用 socket
```

### 3.1 构造函数

- **class** `network.WLAN(*interface_id*)`

  创建 WLAN 网络接口对象。支持的接口类型包括 `network.STA_IF`（即站模式，连接到上游 WiFi 接入点）和 `network.AP_IF`（即接入点模式，允许其他设备连接）。不同接口类型的方法有所不同，例如，只有 STA 模式支持通过 [`WLAN.connect()`](https://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.connect) 连接到接入点。

### 3.2 方法

- **WLAN.active([is_active])**

  通过传递布尔参数来激活（`True`）或停用（`False`）网络接口。如果未传递参数，则返回接口的当前状态。

- **WLAN.connect(ssid=None, password=None, bssid=None)**

  使用指定的 SSID 和密码连接到 WiFi 网络。如果提供了 `bssid`，则只连接到该 MAC 地址的接入点（此时也需要指定 `ssid`）。

- **WLAN.disconnect()**

  断开当前的 WiFi 网络连接。

- **WLAN.scan()**

  扫描可用的 WiFi 网络。此方法仅在 STA 模式下有效，返回的列表包含每个网络的信息，例如：

  ```bash
  # print(sta.scan())
  bssid / 频率 / 信号强度 / 安全协议 / ssid
  da:c5:47:12:80:ab       2462    -30     [WPA2-PSK-CCMP][ESS]    Redmi Note 11 Pro
  72:a8:d3:ab:c8:2c       2412    -42     [WPA2-PSK-CCMP][WPS][ESS]       wifi_test
  ```
  
- **WLAN.status([param])**

  返回当前网络连接的状态。当不传参数时，返回详细的连接信息，包括 BSSID、频率、SSID、加密方式、IP 地址等。例如：

  ```bash
  # print(sta.status())
  bssid=c6:b5:b6:86:64:d7
  freq=2462
  ssid=wjx_pc
  ip_address=192.168.137.221
  ```
  
- **WLAN.isconnected()**

  在 STA 模式下，如果已连接到 WiFi 接入点并拥有有效的 IP 地址，返回 `True`，否则返回 `False`。在 AP 模式下，如果有设备连接到接入点，则返回 `True`。

- **WLAN.ifconfig([(ip, subnet, gateway, dns)])**

  获取或设置 IP 级别的网络接口参数。无参数调用时，返回包含 IP 地址、子网掩码、网关和 DNS 服务器的四元组；传入参数则设置这些值。例如：

  ```python
  nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  ```

- **WLAN.config(param)**

  获取或设置网络接口的配置参数。支持的参数包括 MAC 地址、SSID、WiFi 通道、是否隐藏 SSID、密码等。设置参数时使用关键字参数语法；查询参数时，传递参数名即可。例如：

  ```python
  # 设置接入点的 SSID 和频道
  ap.config(ssid='k230_ap_wjx', channel=11, key='12345678')
  # 查询配置参数
  print(ap.config('ssid'))
  print(ap.config('channel'))
  ```

  支持的配置参数包括：

  | 参数     | 描述                      |
  | -------- | ------------------------- |
  | mac      | MAC 地址（字节）           |
  | ssid     | WiFi 接入点名称（字符串） |
  | channel  | WiFi 频道（整数）         |
  | hidden   | 是否隐藏 SSID（布尔值）   |
  | password | WiFi 连接密码（字符串）   |
