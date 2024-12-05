# 2.4 `ADC` 模块 API 手册

## 1. 概述

K230 处理器内部集成了一个 ADC（模数转换）硬件模块，提供 6 个独立通道。该模块的采样分辨率为 12 位，即输出范围为 0-4095，采样速率为 1 MHz。

## 2. API 介绍

ADC 类属于 `machine` 模块。

### 2.1 示例

```python
from machine import ADC

# 实例化 ADC 通道 0
adc = ADC(0)

# 获取 ADC 通道 0 的采样值
print(adc.read_u16())

# 获取 ADC 通道 0 的电压值（单位为微伏）
print(adc.read_uv(), "uV")
```

### 2.2 构造函数

```python
adc = ADC(channel)
```

**参数**

- `channel`: 表示要使用的 ADC 通道号，范围为 [0, 5]。

### 2.3 `read_u16`

```python
ADC.read_u16()
```

#### 功能

获取指定通道的当前采样值。

**参数**

无

**返回值**

返回该 ADC 通道的采样值，范围为 [0, 4095]。

### 2.4 `read_uv`

```python
ADC.read_uv()
```

#### 功能

获取指定通道的当前电压值 (微伏)。

**参数**

无

**返回值**

返回该 ADC 通道的电压值，单位为微伏（uV），范围为 [0, 1800000] 微伏。
