# 1. FPIOA 使用教程

## 1. 概述

在嵌入式系统中，SoC（System on Chip）通常集成了多种外设模块，如 UART、SPI、I2C、PWM 和 GPIO 等。然而，由于物理引脚数量有限，这些模块往往需要**共享引脚**。为了解决这一冲突，就需要使用 **IOMUX（引脚复用）机制**。在 K230 芯片中，这一机制被称为 **FPIOA（Field Programmable IO Array）**。

FPIOA 允许我们为任意引脚分配所需的功能。例如，你可以将引脚 10 设置为 UART0 的发送脚，也可以设置为 GPIO 用于通用输入输出。

> **FPIOA 有什么作用？**
>
> * **提升灵活性**：开发者可根据实际应用需求自由分配引脚功能。
> * **减少限制**：一套硬件可适配多种引脚配置，便于模块化设计。

## 2. FPIOA 使用示例

K230 芯片内置多个外设资源，包括 5 路 UART、5 路 I2C、6 路 PWM 及最多 64 个 GPIO 输出等。这些外设通过 FPIOA 实现引脚复用，因此不同厂家的 K230 开发板可能存在不同的引脚分配方案。这些厂家一般都会提供相应的开发板接口资料，供软件开发时参考使用。

我们以 **立创·庐山派K230CanMV开发板** 开发板为例进行说明。该开发板提供了一张接口定义图，如下所示：

![立创·庐山派K230CanMV开发板](https://www.kendryte.com/api/post/attachment?id=637)

### 查看当前所有引脚功能状态

使用 `fpioa.help()` 可查看所有管脚的当前配置情况：

```python
from machine import FPIOA

fpioa = FPIOA()
fpioa.help()
```

输出如下：

```python
| pin  | cur func   |                can be func                              |
| ---- |------------|---------------------------------------------------------|
| 0    | GPIO0      | GPIO0/BOOT0/RESV/RESV/RESV                              |
| 1    | BOOT1      | GPIO1/BOOT1/RESV/RESV/RESV                              |
| 2    | JTAG_TCK   | GPIO2/JTAG_TCK/PULSE_CNTR0/RESV/RESV                    |
| 3    | JTAG_TDI   | GPIO3/JTAG_TDI/PULSE_CNTR1/UART1_TXD/RESV               |
| 4    | JTAG_TDO   | GPIO4/JTAG_TDO/PULSE_CNTR2/UART1_RXD/RESV               |
| 5    | JTAG_TMS   | GPIO5/JTAG_TMS/PULSE_CNTR3/UART2_TXD/RESV               |
| 6    | JTAG_RST   | GPIO6/JTAG_RST/PULSE_CNTR4/UART2_RXD/RESV               |
| 7    | IIC4_SCL   | GPIO7/PWM2/IIC4_SCL/RESV/RESV                           |
| 8    | IIC4_SDA   | GPIO8/PWM3/IIC4_SDA/RESV/RESV                           |
| 9    | GPIO9      | GPIO9/PWM4/UART1_TXD/IIC1_SCL/RESV                      |
| 10   | GPIO10     | GPIO10/CTRL_IN_3D/UART1_RXD/IIC1_SDA/RESV               |
| 11   | GPIO11     | GPIO11/CTRL_O1_3D/UART2_TXD/IIC2_SCL/RESV               |
| 12   | GPIO12     | GPIO12/CTRL_O2_3D/UART2_RXD/IIC2_SDA/RESV               |
| ...  | ...        | ...                                                     |
```

### 设置引脚的目标功能

假设我们希望将 IO11 和 IO12 设置为 I2C 接口(I2C2)，用于连接外部 I2C 设备。根据引脚功能表，它们默认是 GPIO，需要重新配置。

```python
fpioa.set_function(11, FPIOA.IIC2_SCL, pu=1)  # 启用上拉
fpioa.set_function(12, FPIOA.IIC2_SDA, pu=1)
```

设置后，我们可以通过 `help()` 查看状态是否生效：

```python
fpioa.help(11)
fpioa.help(12)
```

输出如下：

```python
|pin num         |11                                                           |
|current config  |IIC2_SCL,ie:1,oe:1,pd:0,pu:0,msc:0-3.3,ds:7,st:1,sl:0,di:1   |
|can be function |GPIO11/CTRL_O1_3D/UART2_TXD/IIC2_SCL/RESV                    |
```

此时，即可通过 `machine.I2C(2)` 使用该接口。

### 设置引脚的电气属性

除了功能设置外，FPIOA 还支持设置电气参数：

```python
fpioa.set_function(2, FPIOA.GPIO2, ie=1, oe=1, pu=0, pd=0, st=1, ds=7)
fpioa.help(2)
```

关于电气参数的更多详细配置，可以参考 [K230 IOMUX 配置工具](https://www.kendryte.com/zh/tools/dts_config_generation_tool)

### 获取功能与引脚的对应关系

查询功能对应的引脚号：

```python
fpioa.get_pin_num(FPIOA.UART0_TXD)  # → 38
```

查询引脚当前配置的功能号：

```python
fpioa.get_pin_func(0)  # → 0
```

## 3. 常见问题 FAQ

### Q1：我不知道某个功能可以映射到哪些引脚，怎么办？

你可以使用 `help()` 查询该功能支持的所有引脚：

```python
fpioa.help(FPIOA.IIC0_SDA, func=True)
```

输出：

```python
function IIC0_SDA can be set to PIN33, PIN49, PIN61
current set PIN49 as IIC0_SDA
```

更多引脚功能对应表请参考官方文档： [K230 芯片引脚定义列表](https://kendryte-download.canaan-creative.com/developer/k230/HDK/K230%E7%A1%AC%E4%BB%B6%E6%96%87%E6%A1%A3/K230_PINOUT_V1.2_20240822.xlsx)

### Q2：我设置了引脚功能，但通信仍然不正常，是什么原因？

请确认以下几点：

* 所选引脚是否支持该功能
* 引脚是否已被其他模块占用
* 是否正确设置输入/输出使能（`ie`/`oe`）
* 是否需要启用上拉/下拉电阻（特别是 I2C）

## 4. 延伸阅读

* [FPIOA 模块完整 API 手册](../../api/machine/K230_CanMV_FPIOA模块API手册.md)
* [K230 芯片引脚定义列表（Excel）](https://kendryte-download.canaan-creative.com/developer/k230/HDK/K230%E7%A1%AC%E4%BB%B6%E6%96%87%E6%A1%A3/K230_PINOUT_V1.2_20240822.xlsx)
* [K230 IOMUX 配置工具](https://www.kendryte.com/zh/tools/dts_config_generation_tool)
