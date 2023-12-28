# K230 CanMV UART 模块API手册

![cover](../images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍machine模块下的UART类API。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 软件部      | 2023-09-17 |

## 1. 概述

K230内部包含五个UART硬件模块，其中UART0被小核sh占用，UART3被大核sh占用，剩余UART1，UART2，UART4可供用户使用。
UART IO配置参考IOMUX模块。

## 2. API描述

UART类位于machine模块下

### 示例

```python
from machine import UART
# UART1: baudrate 115200, 8bits, parity none, one stopbits
u1 = UART(UART.UART1, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
# UART write
u1.write("UART1 test")
# UART read
r = u1.read()
# UART readline
r = u1.readline()
# UART readinto
b = bytearray(8)
r = u1.readinto(b)
```

### 构造函数

```python
uart = UART(id, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
```

【参数】

- id: UART号，有效值 UART1、UART2、UART4
- baudrate: UART波特率，可选参数，默认115200
- bits: 每个字符的位数，有效值 FIVEBITS、SIXBITS、SEVENBITS、EIGHTBITS，可选参数，默认EIGHTBITS
- parity: 奇偶校验，有效值 PARITY_NONE、PARITY_ODD、PARITY_EVEN，可选参数，默认PARITY_NONE
- stop: 停止位的数目，有效值 STOPBITS_ONE、STOPBITS_TWO，可选参数，默认STOPBITS_ONE

### init

```python
UART.init(baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
```

配置UART

【参数】

参考构造函数

【返回值】

无

### read

```python
UART.read([nbytes])
```

读取字符。若指定nbytes，则最多读取该数量的字节。否则可读取尽可能多的数据。

【参数】

- nbytes: 最多读取nbytes字节，可选参数

【返回值】

一个包括读入字节的字节对象

### readline

```python
UART.readline()
```

读取一行，并以一个换行符结束。

【参数】

无

【返回值】

一个包括读入字节的字节对象

### readinto

```python
UART.readinto(buf[, nbytes])
```

将字节读取入buf。若指定nbytes，则最多读取该数量的字节。否则，最多读取len(buf)数量的字节。

【参数】

- buf: 一个buffer对象
- nbytes: 最多读取nbytes字节，可选参数

【返回值】

读取并存入buf的字节数

### write

```python
UART.write(buf)
```

将字节缓冲区写入UART。

【参数】

- buf: 一个buffer对象

【返回值】

写入的字节数
