# 2.12 `Timer` 模块 API 手册

## 1. 概述

K230 内部集成了 6 个 Timer 硬件模块，最小定时周期为 1 毫秒（ms）。

## 2. API 介绍

Timer 类位于 `machine` 模块中。

### 2.1 示例代码

```python
from machine import Timer

# 实例化一个软定时器
tim = Timer(-1)

# 配置定时器，单次模式，周期 100 毫秒，回调函数打印 1
tim.init(period=100, mode=Timer.ONE_SHOT, callback=lambda t: print(1))

# 配置定时器，周期模式，周期 1000 毫秒，回调函数打印 2
tim.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: print(2))

# 关闭定时器
tim.deinit()
```

### 2.2 构造函数

```python
timer = Timer(index, mode=Timer.PERIODIC, freq=-1, period=-1, callback=None)
```

**参数**

- `index`: Timer 模块编号，取值范围为 [-1, 5]，其中 -1 表示软件定时器。
- `mode`: 定时器运行模式，可以是单次或周期模式（可选参数）。
- `freq`: 定时器运行频率，支持浮点数，单位为赫兹（Hz），此参数优先级高于 `period`（可选参数）。
- `period`: 定时器运行周期，单位为毫秒（ms）（可选参数）。
- `callback`: 超时回调函数，必须设置并应带有一个参数。

### 2.3 `init` 方法

```python
Timer.init(mode=Timer.PERIODIC, freq=-1, period=-1, callback=None)
```

初始化定时器参数。

**参数**

- `mode`: 定时器运行模式，可以是单次或周期模式（可选参数）。
- `freq`: 定时器运行频率，支持浮点数，单位为赫兹（Hz），此参数优先级高于 `period`（可选参数）。
- `period`: 定时器运行周期，单位为毫秒（ms）（可选参数）。
- `callback`: 超时回调函数，必须设置并应带有一个参数。

**返回值**

无

### 2.4 `deinit` 方法

```python
Timer.deinit()
```

释放定时器资源。

**参数**

无

**返回值**

无
