# K230 CanMV IOMUX API手册

![cover](../../template/images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../../template/images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍 canmv中IOMUX的使用

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| GPIO  |  General Purpose Input Output （通用输入/输出）  |
| iomux | Pin multiplexing(管脚功能选择) |
| FPIOA | Field Programmable Input and Output Array(现场可编程 IO 阵列) |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 王建新 | 2023-10-08 |

## 1. 概述

IOMUX主要配置物理PAD(管脚)的功能，由于soc功能多管脚(pads)少，多个功能共享同一个I/O管脚(pads),但是一个pads同一时间只能使用其中一个功能,所以需要IOMUX进行功能选择。IOMUX也叫FPIOA，Pin multiplexing，管脚功能选择等。

## 2. API描述

IOMUX提供了一个类FPIOA，实现设置I/O管脚的功能函数set_function，和查看功能对应管脚的函数

### 2.1 类 machine.FPIOA

【描述】

FPIOA主要功能是选择I/O管脚的功能。

【语法】

```python
FPIOA()
```

【参数】

无

【返回值】

无

【注意】

无

【举例】

```python
fpioa = FPIOA()
fpioa.set_function(26, fm.fpioa.MMC1_CLK)
```

【相关主题】

无

#### 2.1.1 set_function(pin, func)

【描述】

设置管脚对应的外设功能。

【语法】

```python
set_function(pin, func)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| pin | pin(pad)管脚号,取值 [0, 63] | 输入      |
| func | 外设功能，取值和pin有关，请输入help命令查看管脚的可配置功能 | 输入 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

每个管脚可配的功能都不一样，请输入help命令查看管脚的可配置功能。

【举例】

```python
fpioa = FPIOA()
fpioa.set_function(26, fm.fpioa.MMC1_CLK)
```

【相关主题】

无

#### 2.1.2 get_Pin_num

【描述】

查看外设功能对应的管脚

【语法】

```python
fpioa.get_Pin_num(func)
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
| -------- | ---- | --------- |
| func     | 功能 | 输入      |

【返回值】

| 返回值 | 描述           |
| ------ | -------------- |
| 0-64   | 成功,pin管脚号 |
| -1     | 失败           |

【注意】

无

【举例】

```python
fpioa = FPIOA()
fpioa.get_Pin_num(fm.fpioa.MMC1_CLK)
```

【相关主题】

无

#### 2.1.3 help

【描述】

显示所有管脚的可选功能

【语法】

```python
help()
```

【参数】

无

【返回值】

| pin  | func                                                    |
| ---- | ------------------------------------------------------- |
| 0    | GPIO0/BOOT0/TEST_PIN0                                   |
| 1    | GPIO1/BOOT1/TEST_PIN1                                   |
| 2    | GPIO2/JTAG_TCK/PULSE_CNTR0/TEST_PIN2                    |
| 3    | GPIO3/JTAG_TDI/PULSE_CNTR1/UART1_TXD/TEST_PIN0          |
| 4    | GPIO4/JTAG_TDO/PULSE_CNTR2/UART1_RXD/TEST_PIN1          |
| 5    | GPIO5/JTAG_TMS/PULSE_CNTR3/UART2_TXD/TEST_PIN2          |
| 6    | GPIO6/JTAG_RST/PULSE_CNTR4/UART2_RXD/TEST_PIN3          |
| 7    | GPIO7/PWM2/IIC4_SCL/TEST_PIN3/DI0                       |
| 8    | GPIO8/PWM3/IIC4_SDA/TEST_PIN4/DI1                       |
| 9    | GPIO9/PWM4/UART1_TXD/IIC1_SCL/DI2                       |
| 10   | GPIO10/3D_CTRL_IN/UART1_RXD/IIC1_SDA/DI3                |
| 11   | GPIO11/3D_CTRL_OUT1/UART2_TXD/IIC2_SCL/DO0              |
| 12   | GPIO12/3D_CTRL_OUT2/UART2_RXD/IIC2_SDA/DO1              |
| 13   | GPIO13/M_CLK1/DO2                                       |
| 14   | GPIO14/OSPI_CS/TEST_PIN5/QSPI0_CS0/DO3                  |
| 15   | GPIO15/OSPI_CLK/TEST_PIN6/QSPI0_CLK/CO3                 |
| 16   | GPIO16/OSPI_D0/QSPI1_CS4/QSPI0_D0/CO2                   |
| 17   | GPIO17/OSPI_D1/QSPI1_CS3/QSPI0_D1/CO1                   |
| 18   | GPIO18/OSPI_D2/QSPI1_CS2/QSPI0_D2/CO0                   |
| 19   | GPIO19/OSPI_D3/QSPI1_CS1/QSPI0_D3/TEST_PIN4             |
| 20   | GPIO20/OSPI_D4/QSPI1_CS0/PULSE_CNTR0/TEST_PIN5          |
| 21   | GPIO21/OSPI_D5/QSPI1_CLK/PULSE_CNTR1/TEST_PIN6          |
| 22   | GPIO22/OSPI_D6/QSPI1_D0/PULSE_CNTR2/TEST_PIN7           |
| 23   | GPIO23/OSPI_D7/QSPI1_D1/PULSE_CNTR3/TEST_PIN8           |
| 24   | GPIO24/OSPI_DQS/QSPI1_D2/PULSE_CNTR4/TEST_PIN9          |
| 25   | GPIO25/PWM5/QSPI1_D3/PULSE_CNTR5/TEST_PIN10             |
| 26   | GPIO26/MMC1_CLK/TEST_PIN7PDM_CLK                        |
| 27   | GPIO27/MMC1_CMD/PULSE_CNTR5/PDM_IN0/CI0                 |
| 28   | GPIO28/MMC1_D0/UART3_TXD/PDM_IN1/CI1                    |
| 29   | GPIO29/MMC1_D1/UART3_RXD/3D_CTRL_IN/CI2                 |
| 30   | GPIO30/MMC1_D2/UART3_RTS/3D_CTRL_OUT1/CI3               |
| 31   | GPIO31/MMC1_D3/UART3_CTS/3D_CTRL_OUT2/TEST_PIN11        |
| 32   | GPIO32/IIC0_SCL/IIS_CLK/UART3_TXD/TEST_PIN12            |
| 33   | GPIO33/IIC0_SDA/IIS_WS/UART3_RXD/TEST_PIN13             |
| 34   | GPIO34/IIC1_SCL/IIS_D_IN0/PDM_IN3/UART3_RTS/TEST_PIN14  |
| 35   | GPIO35/IIC1_SDA/IIS_D_OUT0/PDM_IN1/UART3_CTS/TEST_PIN15 |
| 36   | GPIO36/IIC3_SCL/IIS_D_IN1/PDM_IN2/UART4_TXD/TEST_PIN16  |
| 37   | GPIO37/IIC3_SDA/IIS_D_OUT1/PDM_IN0/UART4_RXD/TEST_PIN17 |
| 38   | GPIO38/UART0_TXD/TEST_PIN8/QSPI1_CS0/HSYNC0             |
| 39   | GPIO39/UART0_RXD/TEST_PIN9/QSPI1_CLK/VSYNC0             |
| 40   | GPIO40/UART1_TXD/IIC1_SCL/QSPI1_D0/TEST_PIN18           |
| 41   | GPIO41/UART1_RXD/IIC1_SDA/QSPI1_D1/TEST_PIN19           |
| 42   | GPIO42/UART1_RTS/PWM0/QSPI1_D2/TEST_PIN20               |
| 43   | GPIO43/UART1_CTS/PWM1/QSPI1_D3/TEST_PIN21               |
| 44   | GPIO44/UART2_TXD/IIC3_SCL/TEST_PIN10/SPI2AXI_CLK        |
| 45   | GPIO45/UART2_RXD/IIC3_SDA/TEST_PIN11/SPI2AXI_CS         |
| 46   | GPIO46/UART2_RTS/PWM2/IIC4_SCL/TEST_PIN22               |
| 47   | GPIO47/UART2_CTS/PWM3/IIC4_SDA/TEST_PIN23               |
| 48   | GPIO48/UART4_TXD/TEST_PIN12/IIC0_SCL/SPI2AXI_DIN        |
| 49   | GPIO49/UART4_RXD/TEST_PIN13/IIC0_SDA/SPI2AXI_DOUT       |
| 50   | GPIO50/UART3_TXD/IIC2_SCL/QSPI0_CS4/TEST_PIN24          |
| 51   | GPIO51/UART3_RXD/IIC2_SDA/QSPI0_CS3/TEST_PIN25          |
| 52   | GPIO52/UART3_RTS/PWM4/IIC3_SCL/TEST_PIN26               |
| 53   | GPIO53/UART3_CTS/PWM5/IIC3_SDA                          |
| 54   | GPIO54/QSPI0_CS0/MMC1_CMD/PWM0/TEST_PIN27               |
| 55   | GPIO55/QSPI0_CLK/MMC1_CLK/PWM1/TEST_PIN28               |
| 56   | GPIO56/QSPI0_D0/MMC1_D0/PWM2/TEST_PIN29                 |
| 57   | GPIO57/QSPI0_D1/MMC1_D1/PWM3/TEST_PIN30                 |
| 58   | GPIO58/QSPI0_D2/MMC1_D2/PWM4/TEST_PIN31                 |
| 59   | GPIO59/QSPI0_D3/MMC1_D3/PWM5                            |
| 60   | GPIO60/PWM0/IIC0_SCL/QSPI0_CS2/HSYNC1                   |
| 61   | GPIO61/PWM1/IIC0_SDA/QSPI0_CS1/VSYNC1                   |
| 62   | GPIO62/M_CLK2/UART3_DE/TEST_PIN14                       |
| 63   | GPIO63/M_CLK3/UART3_RE/TEST_PIN15                       |

【注意】

无

【举例】

无

【相关主题】

无
