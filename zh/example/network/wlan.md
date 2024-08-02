# 2. 使用无线网例程讲解

## 1. 概述

本教程将指导您如何在CanMV使用MicroPython的 `network`模块进行无线网络（WiFi）的基本操作，包括作为站点（STA）连接到无线访问点（AP）和创建自己的访问点（AP）。

* **sta_test()**: 演示了如何作为站点（STA）连接到无线网络，包括查看当前连接状态、扫描可用网络、连接特定AP、查看IP配置以及断开连接。
* **ap_test()**: 展示了如何配置并启动一个无线访问点（AP），包括设置SSID、信道和密码，并检查AP的配置和状态。

## 2. 接口调用与功能说明

### 2.1 sta_test

* **`network.WLAN(id)`**: 初始化一个WLAN对象，`id`为0时表示STA模式。
* **`sta.active(bool)`**: 激活或关闭STA模式。当传入 `True`（或等效的1）时激活，传入 `False`时关闭。如果不带参数调用，则返回当前激活状态。
* **`sta.status()`**: 返回STA的当前状态，如是否已连接到AP。
* **`sta.connect(ssid, password)`**: 尝试连接到指定的SSID和密码的AP。此方法不返回是否连接成功的直接结果，但可以通过检查 `sta.status()`或 `sta.isconnected()`来获取连接状态。
* **`sta.ifconfig()`**: 返回STA的IP配置信息，如IP地址、子网掩码、网关和DNS服务器等。
* **`sta.isconnected()`**: 返回 `True`如果STA已连接到AP，否则返回 `False`。
* **`sta.disconnect()`**: 断开STA与当前AP的连接。

#### 2.1.1 完整例程

```python
import network

def sta_test():
    sta=network.WLAN(0)
    if(sta.active() == False):
        sta.active(1)
    #查看sta是否激活
    print(sta.active())
    #查看sta状态
    print(sta.status())
    #sta连接ap
    print(sta.connect("Canaan","Canaan314"))
    #状态
    print(sta.status())
    #查看ip配置
    print(sta.ifconfig())
    #查看是否连接
    print(sta.isconnected())
    #断开连接
    print(sta.disconnect())
    #连接ap
    print(sta.connect("Canaan","Canaan314"))
    #查看状态
    print(sta.status())

sta_test()
```

### 2.2 ap_test

* **`network.WLAN(network.AP_IF)`**: 初始化一个WLAN对象，并设置为AP模式。
* **`ap.active(bool)`**: 激活或关闭AP模式。当传入 `True`（或等效的1）时激活，传入 `False`时关闭。如果不带参数调用，则返回当前激活状态。
* **`ap.config(ssid=None, password=None, channel=None, ...)`**: 配置AP的参数，如SSID、密码、频道等。如果不带任何参数调用，则返回当前配置。
* **`ap.config(key)`**: 如果 `key`是 `'ssid'`、`'channel'`等配置项的字符串表示，则返回该配置项的值。
* **`ap.status()`**: 返回AP的当前状态。

#### 2.2.1 完整例程

```python
import network

def ap_test():
    ap=network.WLAN(network.AP_IF)
    if(ap.active() == False):
        ap.active(1)
    #查看ap是否激活
    print(ap.active())
    #配置并创建ap
    ap.config(ssid='k230_ap_wjx', channel=11, key='12345678')
    #查看ap的ssid号
    print(ap.config('ssid'))
    #查看ap的channel
    print(ap.config('channel'))
    #查看ap的所有配置
    print(ap.config())
    #查看ap的状态
    print(ap.status())
    #sta是否连接ap
    print(ap.isconnected())

ap_test()
```

具体接口定义请参考 [network](../../api/extmod/K230_CanMV_network模块API手册.md)
