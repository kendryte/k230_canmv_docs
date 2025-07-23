# `PWM` 模块 API 手册

## 概述

K230 内部包含两个 PWM 硬件模块，每个模块具有三个输出通道。每个模块的输出频率可调，但三个通道共享同一时钟，而占空比则可独立调整。因此，通道 0、1 和 2 输出频率相同，通道 3、4 和 5 输出频率也相同。通道输出的 I/O 配置请参考 IOMUX 模块。

## API 介绍

PWM 类位于 `machine` 模块中。

### 示例代码

```python
import time
from machine import PWM, FPIOA

CONSTRUCT_WITH_FPIOA = False

PWM_CHANNEL = 0

PWM_PIN = 42
TEST_FREQ = 1000  # Hz


# Initialize PWM with 50% duty
try:
    if CONSTRUCT_WITH_FPIOA:
        fpioa = FPIOA()
        fpioa.set_function(PWM_PIN, fpioa.PWM0 + PWM_CHANNEL)
        pwm = PWM(PWM_CHANNEL, freq=TEST_FREQ, duty=50)
    else:
        pwm = PWM(PWM_PIN, freq=TEST_FREQ, duty=50)
except Exception:
    print("FPIOA setup skipped or failed")

print("[INIT] freq: {}Hz, duty: {}%".format(pwm.freq(), pwm.duty()))
time.sleep(0.5)

# duty() getter and setter
print("[TEST] duty()")
pwm.duty(25)
print("Set duty to 25%, got:", pwm.duty(), "→ duty_u16:", pwm.duty_u16(), "→ duty_ns:", pwm.duty_ns())
time.sleep(0.2)

# duty_u16()
print("[TEST] duty_u16()")
pwm.duty_u16(32768)  # 50%
print("Set duty_u16 to 32768, got:", pwm.duty_u16(), "→ duty():", pwm.duty(), "→ duty_ns():", pwm.duty_ns())
time.sleep(0.2)

# duty_ns()
print("[TEST] duty_ns()")
period_ns = 1000000000 // pwm.freq()
duty_ns_val = (period_ns * 75) // 100  # 75%
pwm.duty_ns(duty_ns_val)
print("Set duty_ns to", duty_ns_val, "ns (≈75%), got:", pwm.duty_ns(), "→ duty():", pwm.duty(), "→ duty_u16():", pwm.duty_u16())
time.sleep(0.2)

# Change frequency and re-check duty values
print("[TEST] Change frequency to 500Hz")
pwm.freq(500)
print("New freq:", pwm.freq())
print("Duty after freq change → duty():", pwm.duty(), "→ duty_u16():", pwm.duty_u16(), "→ duty_ns():", pwm.duty_ns())
time.sleep(0.2)

# Clean up
pwm.deinit()
print("[DONE] PWM test completed")
```

### 构造函数

```python
pwm = PWM(channel_or_pin, freq = -1, duty = -1, duty_u16 = -1, duty_ns = -1)
```

**参数**

- `channel_or_pin`: PWM 通道号，取值范围为 [0, 5]，或者引脚号，如42对应PWM0
- `freq`: PWM 通道输出频率
- `duty`: PWM 通道输出占空比，表示高电平在整个周期中的百分比，取值范围为 [0, 100]
- `duty_ns`: PWM 通道输出高电平的时间，单位为 `ns`
- `duty_u16`: PWM通道输出高电平的时间，取值范围为 [0,65535]

> `duty` 和 `duty_ns` 以及 `duty_u16` 只能设置其中的一个。

### `init` 方法

```python
PWM.init(freq = -1, duty = -1, duty_u16 = -1, duty_ns = -1)
```

**参数**

参考 [构造函数](#构造函数)

### `deinit` 方法

```python
PWM.deinit()
```

释放 PWM 通道的资源。

**参数**

无

**返回值**

无

### `freq` 方法

```python
PWM.freq([freq])
```

获取或设置 PWM 通道的输出频率。

**参数**

- `freq`: PWM 通道输出频率，可选参数。如果不传入参数，则返回当前频率。

**返回值**

返回当前 PWM 通道的输出频率或空。

### `duty` 方法

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

### `duty_u16` 方法

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

### `duty_ns` 方法

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
