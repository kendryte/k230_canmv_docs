# 2.2 network 模块API手册

![cover](../images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../images/canaan-cover.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍network模块API。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |

### 修订记录

| 文档版本号 | 修改说明 | 修改者 | 日期       |
| ---------- | -------- | ------ | ---------- |
| V1.0       | 初版     | 软件部 | 2023-11-09 |

## 1. 概述

本模块主要用于配置查看网络参数,配置完后才可以使用socket模块。

## 2. lan api

详见：`https://docs.micropython.org/en/latest/library/network.LAN.html`

此类为有线网络配置接口。用法示例：

```python
import network
nic = network.LAN()
print(nic.ifconfig())

# now use socket as usual
...
```

### 2.1构造函数

- *class*network.LAN()[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN)

  创建有线以太网对象。

### 2.2方法

- LAN.active([state])[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.active)

  如果传递布尔参数，则激活（“向上”）或停用（“向下”）网络接口。否则，如果没有提供参数，则查询当前状态。

- LAN.isconnected()[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.isconnected)

  返回 `True`如果连接到网络，否则返回`False`。

- LAN.ifconfig([(ip, *subnet*, *gateway*, *dns)***]**)[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.ifconfig)

  获取/设置 IP 级网络接口参数：IP 地址、子网掩码、网关和 DNS 服务器。当不带参数调用时，此方法返回一个包含上述信息的 4 元组。要设置上述值，请传递带有所需信息的 4 元组。例如：

  ```python
  nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  ```

- LAN.config(*config_parameters*)[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.config)

  获取或设置网络接口mac地址，例如：
  
  ```python
  import network
  lan=network.LAN()
  #设置网口mac地址
  print(lan.config(mac="42:EA:D0:C2:0D:83"))
  #查看网口mac地址
  print(lan.config("mac"))

  ```

## 2. wlan api

详见：`https://docs.micropython.org/en/latest/library/network.WLAN.html`

此类为 WiFi 配置接口。用法示例：

```python
import network
# enable station interface and connect to WiFi access point
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('your-ssid', 'your-password')
# now use sockets as usual
```

### 构造

- classnetwork.WLAN(*interface_id*)

创建 WLAN 网络接口对象。支持的接口是 `network.STA_IF`（站又名客户端，连接到上游 WiFi 接入点）和`network.AP_IF`（接入点，允许其他 WiFi 客户端连接）。以下方法的可用性取决于接口类型。例如，只有 STA 接口可以通过[`WLAN.connect()`](http://micropython.86x.net/en/latet/library/network.WLAN.html#network.WLAN.connect) 连接到接入点。

### 方法

- WLAN.active([is_active])

  如果传递布尔参数，则激活（“up”）或停用（“down”）网络接口。否则，如果没有提供参数，则查询当前状态。大多数其他方法需要活动接口。

- WLAN.connect(ssid=None, password=None, bssid=None)

  使用指定的密码连接到指定的无线网络。如果给出了bssid，则连接将被限制为具有该 MAC 地址的接入点（在这种情况下还必须指定ssid）。

- WLAN.disconnect()

  断开当前连接的无线网络。

- WLAN.scan()

  扫描可用的无线网络。扫描只能在 STA 接口上进行。返回包含 WiFi 接入点信息，内容类似如下。

  ```bash
  #print(sta.scan())
  bssid / frequency / signal level / flags / ssid
  da:c5:47:12:80:ab       2462    -30     [WPA2-PSK-CCMP][ESS]    Redmi Note 11 Pro
  72:a8:d3:ab:c8:2c       2412    -42     [WPA2-PSK-CCMP][WPS][ESS]       wifi_test
  e4:4e:2d:42:ee:60       2412    -61     [WPA2-EAP-CCMP][ESS]    CAN
  e4:4e:2d:43:0a:a1       2437    -61     [WPA2-EAP-CCMP][ESS]    Canaan
  e4:4e:2d:43:0a:a4       2437    -61     [WPA2-PSK-CCMP][ESS]    
  ```

- WLAN.status([param])

  返回无线连接的当前状态。当不带参数调用时，返回值描述网络链接状态,类似内容如下：

  ```bash
  #print(sta.status())
  bssid=c6:b5:b6:86:64:d7
  freq=2462
  ssid=wjx_pc
  id=2
  mode=station
  wifi_generation=4
  pairwise_cipher=CCMP
  group_cipher=CCMP
  key_mgmt=WPA2-PSK
  wpa_state=COMPLETED
  ip_address=192.168.137.221
  p2p_device_address=0a:fb:ea:2b:7b:1a
  address=08:fb:ea:2b:7b:1a
  uuid=f483700c-e90e-58a6-90f5-8d8312ec7412
  ```

- WLAN.isconnected()

  在 STA 模式的情况下，`True`如果连接到 WiFi 接入点并具有有效的 IP 地址，则返回。在 AP 模式下，`True` 当站点连接时返回。`False` 否则返回。

- WLAN.ifconfig([(ip, subnet, gateway, dns)])

  获取/设置 IP 级网络接口参数：IP 地址、子网掩码、网关和 DNS 服务器。当不带参数调用时，此方法返回一个包含上述信息的 4 元组。要设置上述值，请传递带有所需信息的 4 元组。例如：` nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8')) `

- WLAN.config(param)

- WLAN.config(param=value, ...)

  获取或设置一般网络接口参数。这些方法允许使用超出标准 IP 配置的附加参数（如 处理 [`WLAN.ifconfig()`](http://micropython.86x.net/en/latet/library/network.WLAN.html#network.WLAN.ifconfig)）。这些包括特定于网络和特定于硬件的参数。设置参数时，应使用关键字参数语法，可以一次设置多个参数。查询时，参数名应以字符串的形式引用，一次只能查询一个参数：
  
  ```python
  # Set WiFi access point name (formally known as SSID) and WiFi channel
  ap.config(ssid='k230_ap_wjx', channel=11, key='12345678')
  # Query params one by one
  print(ap.config('ssid'))
  print(ap.config('channel'))
  ```
  
  以下是支持的参数：
  
  | 参数     | 描述                      |
  | -------- | ------------------------- |
  | mac      | MAC地址（字节） (bytes)   |
  | ssid     | WiFi 接入点名称（字符串） |
  | channel  | WiFi通道（整数）          |
  | hidden   | SSID 是否隐藏（布尔值）   |
  | password | 访问密码（字符串）        |
