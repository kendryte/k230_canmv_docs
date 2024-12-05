# 2.18 `SPI_LCD` 模块 API 手册

## 1. 概述

`SPI_LCD` 模块提供了通过 SPI 总线与 LCD 显示屏进行交互的接口，包括屏幕初始化、绘图、文本显示等操作。

## 2. API 介绍

### 2.1 构造函数

```python
SPI_LCD(spi: SPI, dc: Pin, cs: Pin = None, rst: Pin = None, bl: Pin = None, type: int = SPI_LCD.ST7789)
```

初始化一个 SPI_LCD 对象，创建与指定的 SPI 总线和引脚的连接。

**参数**:

- `spi`: SPI 对象，用于与 LCD 通信。
- `dc`: 数据/命令控制引脚。
- `cs`: （可选）片选引脚。强烈建议用软件 `CS`
- `rst`: （可选）复位引脚。
- `bl`: （可选）背光引脚。
- `type`: LCD 类型（例如 `SPI_LCD.ST7789`）。

**返回**:

- `SPI_LCD` 对象。

### 2.2 `configure` 方法

```python
lcd.configure(width, height, hmirror=False, vflip=False, bgr=False)
```

配置 LCD 显示屏的基本参数。

**参数**:

- `width`: 屏幕宽度。
- `height`: 屏幕高度。
- `hmirror`: （可选）是否启用水平镜像，默认 `False`。
- `vflip`: （可选）是否启用垂直翻转，默认 `False`。
- `bgr`: （可选）是否启用 BGR 颜色格式，为 `True` 时，会设置屏幕为 `BGR565`, 为 `False` 时，设置屏幕为 `RGB565`，默认 `False`。

**返回**:

- 无返回值。

```{admonition} 提示
必须在 init 之前配置模块参数
```

### 2.3 `init` 方法

```python
lcd.init(custom_command=False)
```

初始化 LCD 屏幕。

**参数**:

- `custom_command`: （可选）默认为 `False` ，会自动发送指令初始化屏幕（HD24019C18），如果为 `True` ，用户需要使用 `commnand` 来进行初始化屏幕。

**返回**:

- img: `Image` 对象，用户可使用该buffer进行图像绘制操作

### 2.4 `command` 方法

```python
lcd.command(cmd, data)
```

向 LCD 发送命令。

**参数**:

- `cmd`: 要发送的命令。
- `data`: 要传输的数据。

**返回**:

- 无返回值。

### 2.5 `deinit` 方法

```python
lcd.deinit()
```

关闭并释放 LCD 显示屏。

**返回**:

- 无返回值。

### 2.6 显示尺寸获取方法

```python
lcd.width()
```

获取 LCD 的宽度。

**返回**:

- 宽度值。

```python
lcd.height()
```

获取 LCD 的高度。

**返回**:

- 高度值。

### 2.7 显示方向与属性

```python
lcd.hmirror()
lcd.vflip()
lcd.bgr()
```

这些方法分别返回是否启用了水平镜像、垂直翻转和 BGR 颜色格式。

传入参数 `True` 或者 `False` 进行属性设置，不传参数则返回当前配置

#### 2.8 `get_direction` 方法

```python
lcd.get_direction()
```

获取当前配置的方向寄存器值，通常是 `0x36`。

**返回**:

- 方向寄存器的值

### 2.9 背光控制

```python
lcd.light(value)
```

设置 LCD 背光亮度。

**参数**:

- `value`: 亮度值（0-100）。

**返回**:

- 无返回值。

### 2.10 像素操作

```python
lcd.get(x,y)
```

获取指定位置的像素值

```python
lcd.set(x, y, color)
lcd.pixel(x, y, color)
```

在指定位置绘制一个像素。

`get` 和 `set`、`pixel` 都是操作在 `init` 时返回的 `Image`，需要调用 `show` 才会显示到屏幕

**参数**:

- `x`, `y`: 像素的坐标。
- `color`: 像素的颜色。

**返回**:

- 无返回值。

### 2.11 屏幕填充

```python
lcd.fill(color)
```

用指定颜色填充整个屏幕。

`fill` 是操作在 `init` 时返回的 `Image`，需要调用 `show` 才会显示到屏幕

**参数**:

- `color`: 填充颜色。

**返回**:

- 无返回值。

### 2.12 图片显示

```python
lcd.show(img=None, x = 0, y = 0)
lcd.show_image(img=None, x = 0, y = 0)
```

在 LCD 上显示图像。
如果不传入 `img` 则显示内部图像缓存

**参数**:

- `img`: （可选）要显示的图像对象。
- `x`: （可选）显示图像的起始坐标
- `y`: （可选）显示图像的起始坐标

**返回**:

- 无返回值。

## 3. 屏幕类型

`SPI_LCD.ST7789`: `ST7789` 主控，4线 `SPI` 接口

## 4. 示例代码

### 4.1 在屏幕上显示字符

```python
import time, image
from machine import FPIOA, Pin, SPI, SPI_LCD

fpioa = FPIOA()

# 使用 gpio 19 接屏幕 cs脚
fpioa.set_function(19, FPIOA.GPIO19)
pin_cs = Pin(19, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
pin_cs.value(1)

# 使用 gpio 20 接屏幕 dc 脚
fpioa.set_function(20, FPIOA.GPIO20)
pin_dc = Pin(20, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
pin_dc.value(1)

# 使用 gpio 44 接屏幕 reset 脚
fpioa.set_function(44, FPIOA.GPIO44, pu = 1)
pin_rst = Pin(44, Pin.OUT, pull=Pin.PULL_UP, drive=15)

# spi
fpioa.set_function(15, fpioa.QSPI0_CLK) # scl
fpioa.set_function(16, fpioa.QSPI0_D0) # mosi

spi1 = SPI(1,baudrate=1000*1000*50, polarity=1, phase=1, bits=8)

lcd = SPI_LCD(spi1, pin_dc, pin_cs, pin_rst)

lcd.configure(320, 240, hmirror = False, vflip = True, bgr = False)

print(lcd)

img = lcd.init()
print(img)

img.clear()
img.draw_string_advanced(0,0,32, "RED, 你好世界~", color = (255, 0, 0))
img.draw_string_advanced(0,40,32, "GREEN, 你好世界~", color = (0, 255, 0))
img.draw_string_advanced(0,80,32, "BLUE, 你好世界~", color = (0, 0, 255))

lcd.show()
```

该例程会在屏幕上显示红绿蓝三种颜色的 `你好世界~` 字符串

![hello-world](https://developer.canaan-creative.com/api/post/attachment?id=438)
