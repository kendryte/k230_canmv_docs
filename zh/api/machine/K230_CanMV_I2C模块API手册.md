# K230 CanMV I2C 模块API手册

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

本文档主要介绍machine模块下的I2C类API。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| I2C  |  二进制双向通信模块 |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 软件部      | 2023-09-21 |

## 1. 概述

K230内部包含五个I2C硬件模块，支持7/10比特地址；支持标准100kb/s，快速400kb/s模式，高速模式3.4Mb/s。
通道输出IO配置参考IOMUX模块。

## 2. API描述

I2C类位于machine模块下

### 示例

```python
from machine import I2C
# i2c0 init 100KHz clock,7 bit address mode
i2c = I2C(0, freq=100000, addr_size=7)
# Scan the slave on the I2C bus
i2c.scan()
# Reading data from the bus
i2c.readfrom(addr, len, True)
# Read data and place it in buff
i2c.readfrom_into(addr, buf, True)
# Sending data to the slave
i2c.writeto(addr, buf, True)
# Read slave register
i2c.readfrom_mem(addr, memaddr, nbytes, mem_size=8)
# Read slave register and place it in buff
i2c.readfrom_mem_into(addr, memaddr, buf, mem_size=8)
# Write data to slave register
i2c.writeto_mem(addr, memaddr, buf, mem_size=8)
```

### 构造函数

```python
i2c = I2C(id, freq=100000, addr_size=7)
```

【参数】

- id： I2C ID, [0~4] (I2C.I2C0~I2C.I2C4)
- freq: I2C时钟频率
- addr_size: 地址寻址模式

### scan

```python
i2c.scan()
```

扫描I2C总线上的从机

【参数】

无

【返回值】

list 对象， 包含了所有扫描到的从机地址

### readfrom

```python
i2c.readfrom(addr, len, True)
```

从总线读取数据

【参数】

- addr: 从机地址
- len： 数据长度
- stop： 是否产生停止信号，保留，目前只能使用默认值Ture

【返回值】

读取到的数据，bytes 类型

### readfrom_into

```python
i2c.readfrom_into(addr, buf, True)
```

读取数据并放到制定变量中

【参数】

- addr: 从机地址
- buf： bytearray类型， 定义了长度，读取到的数据存放在此
- stop： 是否产生停止信号，保留，目前只能使用默认值Ture

【返回值】

无

### writeto

```python
i2c.writeto(addr, buf, True)
```

发送数据到从机

【参数】

- addr: 从机地址
- buf： 需要发送的数据
- stop： 是否产生停止信号，保留，目前只能使用默认值Ture

【返回值】

成功发送的字节数

### readfrom_mem

```python
i2c.readfrom_mem(addr, memaddr, nbytes, mem_size=8)
```

读取从机寄存器

【参数】

- addr: 从机地址
- memaddr： 从机寄存器地址
- nbytes： 需要读取的长度
- mem_size： 寄存器宽度， 默认为8位

【返回值】

返回bytes类型的读取到的数据

### readfrom_mem_into

```python
i2c.readfrom_mem_into(addr, memaddr, buf, mem_size=8)
```

读取从机寄存器值到指定变量中

【参数】

- addr: 从机地址
- memaddr： 从机寄存器地址
- buf： bytearray类型， 定义了长度，读取到的数据存放在此
- mem_size： 寄存器宽度， 默认为8位

【返回值】

无

### writeto_mem

```python
i2c.writeto_mem(addr, memaddr, buf, mem_size=8)
```

写数据到从机寄存器

【参数】

- addr: 从机地址
- memaddr： 从机寄存器地址
- buf：  需要写的数据
- mem_size： 寄存器宽度， 默认为8位

【返回值】

无
