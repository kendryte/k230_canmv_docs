# 2.9 `PWM` 模块 API 手册

## 1. 概述

K230 内部包含两个 PWM 硬件模块，每个模块具有三个输出通道。每个模块的输出频率可调，但三个通道共享同一时钟，而占空比则可独立调整。因此，通道 0、1 和 2 输出频率相同，通道 3、4 和 5 输出频率也相同。通道输出的 I/O 配置请参考 IOMUX 模块。

## 2. API 介绍

PWM 类位于 `machine` 模块中。

### 2.1 示例代码

```python
import time
from machine import PWM
from machine import FPIOA

# 实例化FPIOA
fpioa = FPIOA()

# 设置PIN42为PWM通道0
fpioa.set_function(42, fpioa.PWM0)

# 实例化PWM通道0，频率为1000Hz，占空比为50%，默认使能输出
pwm0 = PWM(0)

# 调整通道0频率为2000Hz
pwm0.freq(2000)

# 调整通道0的占空比为 50% (32768 / 65535)
pwm0.duty_u16(32768)
print(pwm0.duty_u16())

# 输出1s之后关闭输出
time.sleep(1)
pwm0.deinit()
time.sleep(1)

# 调整通道0频率为10KHz，占空比为 30%
pwm0.freq(10000)
pwm0.duty(30)
print(pwm0.duty())

# 输出1s之后关闭输出
time.sleep(1)
pwm0.deinit()
```

### 2.2 构造函数

```python
pwm = PWM(channel, freq = -1, duty = -1, duty_u16 = -1, duty_ns = -1)
```

**参数**

- `channel`: PWM 通道号，取值范围为 [0, 5]
- `freq`: PWM 通道输出频率
- `duty`: PWM 通道输出占空比，表示高电平在整个周期中的百分比，取值范围为 [0, 100]
- `duty_ns`: PWM 通道输出高电平的时间，单位为 `ns`
- `duty_u16`: PWM通道输出高电平的时间，取值范围为 [0,65535]

> `duty` 和 `duty_ns` 以及 `duty_u16` 只能设置其中的一个。

### 2.3 `init` 方法

```python
PWM.init(freq = -1, duty = -1, duty_u16 = -1, duty_ns = -1)
```

**参数**

参考 [构造函数](#22-构造函数)

### 2.4 `deinit` 方法

```python
PWM.deinit()
```

释放 PWM 通道的资源。

**参数**

无

**返回值**

无

### 2.5 `freq` 方法

```python
PWM.freq([freq])
```

获取或设置 PWM 通道的输出频率。

**参数**

- `freq`: PWM 通道输出频率，可选参数。如果不传入参数，则返回当前频率。

**返回值**

返回当前 PWM 通道的输出频率或空。

### 2.6 `duty` 方法

```python
PWM.duty([duty])
```

获取或设置 PWM 通道的输出占空比。

**参数**

- `duty`: PWM 通道输出占空比，可选参数。如果不传入参数，则返回当前占空比。

**返回值**

返回当前 PWM 通道的输出占空比或空。

**返回值**

无

### 2.7 `duty_u16` 方法

```python
PWM.duty_u16([duty_u16])
```

获取或设置 PWM 通道的输出占空比。

**参数**

- `duty_u16`: PWM 通道输出占空比，可选参数。如果不传入参数，则返回当前占空比。

**返回值**

返回当前 PWM 通道的输出占空比或空。

**返回值**

无

### 2.8 `duty_ns` 方法

```python
PWM.duty_ns([duty_ns])
```

获取或设置 PWM 通道的输出占空比。

**参数**

- `duty_ns`: PWM 通道输出占空比，可选参数。如果不传入参数，则返回当前占空比。

**返回值**

返回当前 PWM 通道的输出占空比或空。

**返回值**

无
