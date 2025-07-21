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

def sta_test():
    sta=network.WLAN(network.STA_IF)
    if(sta.active() == False):
        sta.active(1)
    # 查看 sta 是否激活
    print(sta.active())
    # 查看 sta 状态
    print(sta.status())
    #sta 连接 ap
    print(sta.connect("Canaan","Canaan314"))
    # 状态
    print(sta.status())
    # 查看 ip 配置
    print(sta.ifconfig())
    # 查看是否连接
    print(sta.isconnected())
    # 断开连接
    print(sta.disconnect())
    # 连接 ap
    print(sta.connect("Canaan","Canaan314"))
    # 查看状态
    print(sta.status())

sta_test()
```

### 3.1 构造函数

- **class** `network.WLAN(*interface_id*)`

  创建 WLAN 网络接口对象。支持的接口类型包括 `network.STA_IF`（即站模式，连接到上游 WiFi 接入点）和 `network.AP_IF`（即接入点模式，允许其他设备连接）。不同接口类型的方法有所不同，例如，只有 STA 模式支持通过 [`WLAN.connect()`](https://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.connect) 连接到接入点。

### 3.2 方法

- **WLAN.active()**

  查询当前接口是否激活

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

  获取或设置网络接口的配置参数。支持的参数包括 MAC 地址、SSID、WiFi 通道、是否隐藏 SSID、密码等。设置参数时使用关键字参数语法；查询参数时，传递参数名即可。例如：

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
    - `info`: 当前热点信息，仅可查询
    - `country`: 国家代码
  
- **WLAN.stop()**

  停止开启热点

  > 仅 `Ap` 模式可用

- **WLAN.info()**

  查询当前热点信息

  > 仅 `Ap` 模式可用
