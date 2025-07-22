# `LED` 模块 API 手册

## 概述

开发板包含一个 LED 三原色灯珠，用户可以通过 API 控制三原色的亮度。

## API 介绍

LED 类位于 `machine` 模块下。

### 示例

```python
from machine import LED
import time

# 实例化 LED 对象
red_led = LED("LED_RED")          # 或者 red_led = LED(1)
green_led = LED("LED_GREEN")      # 或者 green_led = LED(2)
blue_led = LED("LED_BLUE")        # 或者 blue_led = LED(3)

# 关闭所有 LED
blue_led.off()
green_led.off()
red_led.off()

while True:
    # 设置绿色 LED 的亮度
    green_led.value(50)    # 亮度范围为 0-255
    red_led.on()           # 红色 LED 亮起
    time.sleep_ms(250)
    
    green_led.value(200)   # 设置绿色 LED 的亮度
    red_led.off()          # 红色 LED 熄灭
    time.sleep_ms(250)
```

### 构造函数

```python
led = LED(id)
```

**参数**

- `id`: LED 的标识符，1 或 "LED_RED" 表示红灯；2 或 "LED_GREEN" 表示绿灯；3 或 "LED_BLUE" 表示蓝灯。

### `value` 方法

```python
led.value(val)
```

控制 LED 的亮度。

**参数**

- `val`: 亮度级别，范围为 0 到 255。

**返回值**

无

### `on` 方法

```python
led.on()
```

以最大亮度点亮 LED。

**参数**

无

**返回值**

无

### `off` 方法

```python
led.off()
```

熄灭 LED。

**参数**

无

**返回值**

无
