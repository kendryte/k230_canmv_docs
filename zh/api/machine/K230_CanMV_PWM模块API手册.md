# K230 CanMV PWM 模块API手册

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

本文档主要介绍machine模块下的PWM类API。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| PWM  |  脉宽调制模块 |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 软件部      | 2023-09-17 |

## 1. 概述

K230内部包含两个PWM硬件模块，每个模块有3个输出通道，模块输出频率可调，但3通道共用，通道占空比独立可调。因此通道0、1、2共用频率，通道3、4、5共用频率。
通道输出IO配置参考IOMUX模块。

## 2. API描述

PWM类位于machine模块下

### 示例

```python
from machine import PWM
# channel 0 output freq 1kHz duty 50%, enable
pwm0 = PWM(0, 1000, 50, enable = True)
# disable channel 0 output
pwm0.enable(False)
# set channel 0 output freq 2kHz
pwm0.freq(2000)
# set channel 0 output duty 10%
pwm0.duty(10)
# enable channel 0 output
pwm0.enable(True)
# release channel 0
pwm0.deinit()
```

### 构造函数

```python
pwm = PWM(channel, freq, duty=50, enable=False)
```

【参数】

- channel: PWM通道号，取值:[0,5]
- freq: PWM通道输出频率
- duty: PWM通道输出占空比，指高电平占整个周期的百分比，取值:[0,100]，可选参数，默认50
- enable: PWM通道输出立即使能，可选参数，默认False

### freq

```python
PWM.freq([freq])
```

获取或设置PWM通道输出频率

【参数】

- freq: PWM通道输出频率，可选参数，如果不传参数则返回当前频率

【返回值】

返回空或当前PWM通道输出频率

### duty

```python
PWM.duty([duty])
```

获取或设置PWM通道输出占空比

【参数】

- duty: PWM通道输出占空比，可选参数，如果不传参数则返回当前占空比

【返回值】

返回空或当前PWM通道输出占空比

### enable

```python
PWM.enable(enable)
```

使能或禁止PWM通道输出

【参数】

- enable: 使能或禁止PWM通道输出

【返回值】

无

### deinit

```python
PWM.deinit()
```

释放PWM通道资源

【参数】

无

【返回值】

无
