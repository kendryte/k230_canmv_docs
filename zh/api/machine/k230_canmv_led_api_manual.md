# `neopixel` 模块 API 手册

## 概述

本模块是原有 machine.LED 的升级版本。

`neopixel` 模块用于驱动基于 **WS2812 / WS2812B**（也叫 NeoPixel）芯片的 RGB LED 灯带。这些灯带通过单根数据线进行串行通信，具有颜色控制和级联功能，广泛用于装饰照明、状态指示等场景。

该模块支持 RGB 或 RGBW 类型，每个像素占用 3 或 4 字节，并提供缓冲区式操作接口，方便批量更新。

---

CanMV K230 目前支持使用 GPIO 驱动 WS2812 灯珠。

```{attention}
由于目前使用 GPIO 生成驱动 WS2812 的时序，在发送数据的时候需要关闭中断，因此如果控制比较多的灯珠时，可能会影响其他模块的工作，请酌情选择灯珠数量。
```

---

## `NeoPixel` 类

### 示例代码

```python
from machine import Pin
import neopixel
import time

# 定义灯带数据引脚和灯珠数量
NEO_PIN = 42
NUM_PIXELS = 8

# 初始化灯带对象
np = neopixel.NeoPixel(Pin(NEO_PIN), NUM_PIXELS)

# 设置第一个灯珠为红色，第二个为绿色，第三个为蓝色
np[0] = (255, 0, 0)
np[1] = (0, 255, 0)
np[2] = (0, 0, 255)

# 写入数据（必须调用 write() 才能生效）
np.write()

# 熄灭所有灯
np.fill((0, 0, 0))
np.write()
```

---

### 构造函数

```python
neopixel.NeoPixel(pin, n, bpp=3, timing=1)
```

**参数**

* `pin`: 控制 WS2812 灯带的数据引脚，类型为 `machine.Pin` 对象。
* `n`: 灯珠数量。
* `bpp`: 每个像素的字节数，3 表示 RGB，4 表示 RGBW，默认为 3。
* `timing`: 发送时序配置，通常为 1（WS2812）。若为 0，则用于 WS2811/800kHz 模式。

---

### `__getitem__` / `__setitem__` 下标操作

```python
np[i] = (r, g, b)
color = np[i]
```

**说明**

通过索引访问或设置第 `i` 个灯珠的颜色。颜色为元组 `(r, g, b)`（或 `(r, g, b, w)`，取决于 `bpp`）。

---

### `write()` 方法

```python
np.write()
```

**说明**

将当前颜色缓冲区写入灯带。**必须调用该方法，灯珠颜色才会更新**。

---

### `fill()` 方法

```python
np.fill((r, g, b))
```

**说明**

将所有灯珠设置为相同的颜色。颜色格式与 `__setitem__` 相同。

---

### `__len__()` 方法

```python
length = len(np)
```

**说明**

获取当前灯带对象的灯珠数量。

---

## 注意事项

* 使用前请确保数据引脚已正确连接并配置为输出模式。
* 对于长灯带（如 >30 灯），建议使用外部电源供电，并在数据线加入 330Ω 电阻以保护。
* 数据发送期间会禁止中断，避免时序错误。

---

## 示例进阶：彩虹动画

```python
import time
import neopixel
from machine import Pin

np = neopixel.NeoPixel(Pin(42), 10)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

while True:
    for j in range(256):
        for i in range(len(np)):
            np[i] = wheel((i * 10 + j) % 256)
        np.write()
        time.sleep_ms(20)
```

---
