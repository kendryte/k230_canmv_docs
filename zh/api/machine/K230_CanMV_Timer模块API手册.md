# 2.11 Timer 模块API手册

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

本文档主要介绍machine模块下的Timer类API。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| Timer  |  定时器  |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 软件部      | 2023-09-22 |

## 1. 概述

K230内部包含6个Timer硬件模块，最小定时周期为1us。

## 2. API描述

Timer类位于machine模块下

### 2.1 示例

```python
from machine import Timer
# 实例化一个软定时器
tim = Timer(-1)
tim.init(period=100, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
tim.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:print(2))
tim.deinit()
```

### 2.2 构造函数

```python
timer = Timer(index, mode=Timer.PERIODIC, freq=-1, period=-1, callback=None, arg=None)
```

【参数】

- index: Timer号，取值:[-1,5]，-1代表软件定时器
- mode: 运行模式，单次或周期，可选参数
- freq: Timer运行频率，支持浮点，单位Hz，可选参数，优先级高于`period`
- period: Timer运行周期，单位ms，可选参数
- callback: 超时回调函数，必须设置，要带一个参数
- arg: 超时回调函数参数，可选参数

**注意：** [0-5]硬件Timer暂不可用

### 2.3 init

```python
Timer.init(mode=Timer.PERIODIC, freq=-1, period=-1, callback=None, arg=None)
```

初始化定时器参数

【参数】

- mode: 运行模式，单次或周期，可选参数
- freq: Timer运行频率，支持浮点，单位Hz，可选参数，优先级高于`period`
- period: Timer运行周期，单位ms，可选参数
- callback: 超时回调函数，必须设置，要带一个参数
- arg: 超时回调函数参数，可选参数

【返回值】

无

### 2.4 deinit

```python
Timer.deinit()
```

释放Timer资源

【参数】

无

【返回值】

无
