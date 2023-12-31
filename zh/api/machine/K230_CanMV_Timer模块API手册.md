# K230 CanMV Timer API手册

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

硬件定时器，可以用来定时触发任务或者处理任务。

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
| V1.0       | 初版     | 史文涛      | 2023-09-22 |

## 1. 概述

硬件定时器，可以用来定时触发任务或者处理任务，设定时间到了后可以触发中断（调用回调函数），精度比软件定时器高。需要注意的是，定时器在不同的硬件中可能会有不同的表现。MicroPython 的 Timer 类定义了在给定时间段内（或在一段延迟后执行一次回调）执行回调的基本操作

## 2. API描述

Timer提供了一个类 Timer，实现了六个函数

### 2.1 类 machine.Timer

【描述】

通过指定的参数新建一个 Timer 对象。

【语法】

```python
from machine import Timer
tim = machine.Timer(mode=Timer.MODE_ONE_SHOT,period=1000, unit=Timer.UNIT_MS, callback=None, arg=None, start=True)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| mode  |    Timer模式，MODE_ONE_SHOT或MODE_PERIODIC       | 输入      |
| period  |  TImer周期, 在启动定时器后 period 时间， 回调函数将会被调用       | 输入      |
| unit  |    设置周期的单位，默认位毫秒（ms），Timer.UNIT_S 或者 Timer.UNIT_MS 或者 Timer.UNIT_US 或者Timer.UNIT_NS          | 输入      |
| callback  |    定时器回调函数， 定义了两个参数， 一个是定时器对象Timer， 第二个是在定义对象是希望传的参数arg，更多请看arg参数解释         | 输入      |
| arg  |    希望传给回调函数的参数,作为回调函数的第二个参数         | 输入      |
| start  |     是否在对象构建成功后立即开始定时器,True：立即开始,False:不立即开启,需要调用start()函数来启动定时器         | 输入      |
【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【举例】

无

【相关主题】

无

#### 2.1.1 init

【描述】

类似构造函数。

【语法】

```python
tim = machine.Timer(mode=Timer.MODE_ONE_SHOT,period=1000, unit=Timer.UNIT_MS, callback=None, arg=None, start=True)
```

【参数】

与构造函数相同

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

无

【相关主题】

无

#### 2.1.2 callback

【描述】

获取或者设置回调函数

【语法】

```python
tim.callback(callback)
```

【参数】

• callback： 设置的回调函数，可选参数， 如果不传参数，则只返回先有的回调函数

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

无

【相关主题】

无

#### 2.1.3 period

【描述】

获取或者设置定时周期

【语法】

```python
tim.period(period)
```

【参数】

• period： 可选参数，配置周期， 如果不传参数， 则只返回当前周期值

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

无

【相关主题】

无

#### 2.1.4 start

【描述】

启动定时器

【语法】

```python
tim.start()
```

【参数】

无

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

无

【相关主题】

无

#### 2.1.5 stop

【描述】

停止定时器

【语法】

```python
tim.stop()
```

【参数】

无

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

无

【相关主题】

无

#### 2.1.6 deinit

【描述】

注销定时器，并且注销硬件的占用，关闭硬件的时钟

【语法】

```python
tim.deinit()
```

【参数】

无

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

无

【相关主题】

无

### 常量

• UNIT_S: 单位秒 (s)

• UNIT_MS: 单位毫秒 (ms)

• UNIT_US: 单位微秒 (us)

• UNIT_NS: 单位纳秒 (ns)

• MACHINE_TIMER_MODE_ONE_SHOT: 只运行一次（回调一次）

• MACHINE_TIMER_MODE_PERIODIC: 始终运行（连续回调）
