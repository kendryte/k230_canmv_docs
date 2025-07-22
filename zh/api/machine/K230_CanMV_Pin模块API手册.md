# `Pin` 模块 API 手册

## 概述

K230 芯片内部包含 64 个 GPIO（通用输入输出）引脚，每个引脚均可配置为输入或输出模式，并支持上下拉电阻配置和驱动能力设置。这些引脚能够灵活用于各种数字输入输出场景。

## API 介绍

`Pin` 类位于 `machine` 模块中，用于控制 K230 芯片的 GPIO 引脚。

**示例**

```python
from machine import Pin

# 将引脚 2 配置为输出模式，无上下拉，驱动能力为 7
pin = Pin(2, Pin.OUT, pull=Pin.PULL_NONE, drive=7)

# 设置引脚 2 输出高电平
pin.value(1)

# 设置引脚 2 输出低电平
pin.value(0)
```

### 构造函数

```python
pin = Pin(index, mode, pull=Pin.PULL_NONE, value = -1, drive=7, alt = -1)
```

**参数**

- `index`: 引脚编号，范围为 [0, 63]。
- `mode`: 引脚的模式，支持输入模式或输出模式。
- `pull`: 上下拉配置（可选），默认为 `Pin.PULL_NONE`。
- `drive`: 驱动能力配置（可选），默认值为 7。
- `value`: 设置引脚默认输出值
- `alt`: 目前未使用

### `init` 方法

```python
Pin.init(mode, pull=Pin.PULL_NONE, drive=7)
```

用于初始化引脚的模式、上下拉配置及驱动能力。

**参数**

- `mode`: 引脚的模式（输入或输出）。
- `pull`: 上下拉配置（可选），默认值为 `Pin.PULL_NONE`。
- `drive`: 驱动能力（可选），默认值为 7。

**返回值**

无

### `value` 方法

```python
Pin.value([value])
```

获取引脚的输入电平值或设置引脚的输出电平。

**参数**

- `value`: 输出值（可选），如果传递该参数则设置引脚输出为指定值。如果不传参则返回引脚的当前输入电平值。

**返回值**

返回空或当前引脚的输入电平值。

### `mode` 方法

```python
Pin.mode([mode])
```

获取或设置引脚的模式。

**参数**

- `mode`: 引脚模式（输入或输出），如果不传参则返回当前引脚的模式。

**返回值**

返回空或当前引脚模式。

### `pull` 方法

```python
Pin.pull([pull])
```

获取或设置引脚的上下拉配置。

**参数**

- `pull`: 上下拉配置（可选），如果不传参则返回当前上下拉配置。

**返回值**

返回空或当前引脚的上下拉配置。

### `drive` 方法

```python
Pin.drive([drive])
```

获取或设置引脚的驱动能力。

**参数**

- `drive`: 驱动能力（可选），如果不传参则返回当前驱动能力。

**返回值**

返回空或当前引脚的驱动能力。

### `on` 方法

```python
Pin.on()
```

将引脚输出设置为高电平。

**参数**

无

**返回值**

无

### `off` 方法

```python
Pin.off()
```

将引脚输出设置为低电平。

**参数**

无

**返回值**

无

### `high` 方法

```python
Pin.high()
```

将引脚输出设置为高电平。

**参数**

无

**返回值**

无

### `low` 方法

```python
Pin.low()
```

将引脚输出设置为低电平。

**参数**

无

**返回值**

无

### `irq` 方法

```python
Pin.irq(handler=None, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, *, priority=1, wake=None, hard=False, debounce = 10)
```

使能 IO 中断功能

- `handler`: 回调函数，必须设置
- `trigger`: 触发模式
- `priority`: 不支持
- `wake`: 不支持
- `hard`: 不支持
- `debounce`: 高电平和低电平触发时，最小触发间隔，单位为 `ms`，最小值为 `5`

**返回值**

mq_irq 对象

## 常量定义

### 模式

- Pin.IN: 输入模式
- Pin.OUT: 输出模式

### 上下拉模式

- PULL_NONE: 关掉上下拉
- PULL_UP: 使能上拉
- PULL_DOWN: 使能下拉

### 中断触发模式

- IRQ_FALLING: 下降沿触发
- IRQ_RISING: 上升沿触发
- IRQ_LOW_LEVEL: 低电平触发
- IRQ_HIGH_LEVEL: 高电平触发
- IRQ_BOTH: 边沿触发

### 驱动能力

具体配置对应的电流输出能力参见[fpioa](./K230_CanMV_FPIOA模块API手册.md#31-io-配置说明)

- DRIVE_0
- DRIVE_1
- DRIVE_2
- DRIVE_3
- DRIVE_4
- DRIVE_5
- DRIVE_6
- DRIVE_7
- DRIVE_8
- DRIVE_9
- DRIVE_10
- DRIVE_11
- DRIVE_12
- DRIVE_13
- DRIVE_14
- DRIVE_15
