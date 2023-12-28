# K230 CanMV network 模块API手册

![cover](C:\Users\wangjianxin\images\canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](C:\Users\wangjianxin\images\logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

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

本模块主要用于配置查看网络参数

## 2. lan api

详见：`https://docs.micropython.org/en/latest/library/network.LAN.html`

This class allows you to control the Ethernet interface. The PHY hardware type is board-specific.

Example usage:

```python
import network
nic = network.LAN(0)
print(nic.ifconfig())

# now use socket as usual
...
```

### 2.1结构体

- *class*network.LAN(*id*, ***, *phy_type=<board_default>*, *phy_addr=<board_default>*, *ref_clk_mode=<board_default>*)[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN)

  Create a LAN driver object, initialise the LAN module using the given PHY driver name, and return the LAN object.Arguments are:*id* is the number of the Ethernet port, either 0 or 1.*phy_type* is the name of the PHY driver. For most board the on-board PHY has to be used and is the default. Suitable values are port specific.*phy_addr* specifies the address of the PHY interface. As with *phy_type*, the hardwired value has to be used for most boards and that value is the default.*ref_clk_mode* specifies, whether the data clock is provided by the Ethernet controller or the PYH interface. The default value is the one that matches the board. If set to `LAN.OUT` or `Pin.OUT` or `True`, the clock is driven by the Ethernet controller, if set to `LAN.IN` or `Pin.IN` or `False`, the clock is driven by the PHY interface.For example, with the Seeed Arch Mix board you can use:`nic = LAN(0, phy_type=LAN.PHY_LAN8720, phy_addr=1, ref_clk_mode=Pin.IN)`

### 2.2函数

- LAN.active(**[***state***]**)[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.active)

  With a parameter, it sets the interface active if *state* is true, otherwise it sets it inactive. Without a parameter, it returns the state.

- LAN.isconnected()[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.isconnected)

  Returns `True` if the physical Ethernet link is connected and up. Returns `False` otherwise.

- LAN.ifconfig(**[***(ip*, *subnet*, *gateway*, *dns)***]**)[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.ifconfig)

  Get/set IP address, subnet mask, gateway and DNS.When called with no arguments, this method returns a 4-tuple with the above information.To set the above values, pass a 4-tuple with the required information. For example:`nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))`

- LAN.config(*config_parameters*)[¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.config)

  Sets or gets parameters of the LAN interface. The only parameter that can be retrieved is the MAC address, using:`mac = LAN.config("mac")`The parameters that can be set are:`trace=n` sets trace levels; suitable values are:2: trace TX4: trace RX8: full trace`low_power=bool` sets or clears low power mode, valid values being `False` or `True`.
