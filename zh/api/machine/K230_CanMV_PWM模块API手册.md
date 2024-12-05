# 2.9 `PWM` 模块 API 手册

## 1. 概述

K230 内部包含两个 PWM 硬件模块，每个模块具有三个输出通道。每个模块的输出频率可调，但三个通道共享同一时钟，而占空比则可独立调整。因此，通道 0、1 和 2 输出频率相同，通道 3、4 和 5 输出频率也相同。通道输出的 I/O 配置请参考 IOMUX 模块。

## 2. API 介绍

PWM 类位于 `machine` 模块中。

### 2.1 示例代码

```python
from machine import PWM

# 初始化通道 0，输出频率 1 kHz，占空比 50%，并使能输出
pwm0 = PWM(0, 1000, 50, enable=True)

# 禁用通道 0 输出
pwm0.enable(False)

# 设置通道 0 输出频率为 2 kHz
pwm0.freq(2000)

# 设置通道 0 输出占空比为 10%
pwm0.duty(10)

# 重新启用通道 0 输出
pwm0.enable(True)

# 释放通道 0
pwm0.deinit()
```

### 2.2 构造函数

```python
pwm = PWM(channel, freq, duty=50, enable=False)
```

**参数**

- `channel`: PWM 通道号，取值范围为 [0, 5]
- `freq`: PWM 通道输出频率
- `duty`: PWM 通道输出占空比，表示高电平在整个周期中的百分比，取值范围为 [0, 100]，可选参数，默认值为 50
- `enable`: PWM 通道输出是否立即使能，可选参数，默认值为 False

### 2.3 `freq` 方法

```python
PWM.freq([freq])
```

获取或设置 PWM 通道的输出频率。

**参数**

- `freq`: PWM 通道输出频率，可选参数。如果不传入参数，则返回当前频率。

**返回值**

返回当前 PWM 通道的输出频率或空。

### 2.4 `duty` 方法

```python
PWM.duty([duty])
```

获取或设置 PWM 通道的输出占空比。

**参数**

- `duty`: PWM 通道输出占空比，可选参数。如果不传入参数，则返回当前占空比。

**返回值**

返回当前 PWM 通道的输出占空比或空。

### 2.5 `enable` 方法

```python
PWM.enable(enable)
```

使能或禁用 PWM 通道的输出。

**参数**

- `enable`: 是否使能 PWM 通道输出。

**返回值**

无

### 2.6 `deinit` 方法

```python
PWM.deinit()
```

释放 PWM 通道的资源。

**参数**

无

**返回值**

无
