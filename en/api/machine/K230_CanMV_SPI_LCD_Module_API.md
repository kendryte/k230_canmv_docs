# 2.18 `SPI_LCD` Module API Manual

## 1. Overview

The `SPI_LCD` module provides interfaces to interact with an LCD display through the SPI bus, including screen initialization, drawing, and text display operations.

## 2. API Introduction

### 2.1 Constructor

```python
SPI_LCD(spi: SPI, dc: Pin, cs: Pin = None, rst: Pin = None, bl: Pin = None, type: int = SPI_LCD.ST7789)
```

Initializes an `SPI_LCD` object, creating a connection with the specified SPI bus and pins.

**Parameters**:

- `spi`: SPI object for communication with the LCD.
- `dc`: Data/command control pin.
- `cs`: (Optional) Chip select pin. It is highly recommended to use software `CS`.
- `rst`: (Optional) Reset pin.
- `bl`: (Optional) Backlight pin.
- `type`: LCD type (e.g., `SPI_LCD.ST7789`).

**Returns**:

- `SPI_LCD` object.

### 2.2 `configure` Method

```python
lcd.configure(width, height, hmirror=False, vflip=False, bgr=False)
```

Configures basic parameters for the LCD display.

**Parameters**:

- `width`: Screen width.
- `height`: Screen height.
- `hmirror`: (Optional) Whether to enable horizontal mirroring, default `False`.
- `vflip`: (Optional) Whether to enable vertical flipping, default `False`.
- `bgr`: (optional) whether to enable BGR color format. When `True`, the screen will be set to `BGR565`. When `False`, the screen will be set to `RGB565`. The default value is `False`.

**Returns**:

- No return value.

```{admonition} Note
The module parameters must be configured before calling `init`.
```

### 2.3 `init` Method

```python
lcd.init(custom_command=False)
```

Initializes the LCD screen.

**Parameters**:

- `custom_command`: (Optional) Whether to use custom initialization commands, default `False`. If set to `True`, initialization commands are not automatically sent.

**Returns**:

- `img`: `Image` object, which users can use for drawing operations on the buffer.

### 2.4 `command` Method

```python
lcd.command(cmd, data)
```

Sends a command to the LCD.

**Parameters**:

- `cmd`: The command to send.
- `data`: The data to transfer.

**Returns**:

- No return value.

### 2.5 `deinit` Method

```python
lcd.deinit()
```

Shuts down and releases the LCD display.

**Returns**:

- No return value.

### 2.6 Display Size Retrieval Methods

```python
lcd.width()
```

Retrieves the LCD width.

**Returns**:

- Width value.

```python
lcd.height()
```

Retrieves the LCD height.

**Returns**:

- Height value.

### 2.7 Display Orientation and Properties

```python
lcd.hmirror()
lcd.vflip()
lcd.bgr()
```

These methods return whether horizontal mirroring, vertical flipping, and BGR color format are enabled.

Passing `True` or `False` as parameters will set the properties, while not passing parameters will return the current configuration.

#### 2.8 `get_direction` Method

```python
lcd.get_direction()
```

Retrieves the current configuration of the direction register, usually `0x36`.

**Returns**:

- The value of the direction register.

### 2.9 Backlight Control

```python
lcd.light(value)
```

Sets the LCD backlight brightness.

**Parameters**:

- `value`: Brightness value (0-100).

**Returns**:

- No return value.

### 2.10 Pixel Operations

```python
lcd.get(x, y)
```

Retrieves the pixel value at the specified position.

```python
lcd.set(x, y, color)
lcd.pixel(x, y, color)
```

Draws a pixel at the specified position.

Both `get`, `set`, and `pixel` operate on the `Image` returned by `init`, and you need to call `show` to display it on the screen.

**Parameters**:

- `x`, `y`: The coordinates of the pixel.
- `color`: The color of the pixel.

**Returns**:

- No return value.

### 2.11 Screen Fill

```python
lcd.fill(color)
```

Fills the entire screen with the specified color.

`fill` operates on the `Image` returned by `init`, and you need to call `show` to display it on the screen.

**Parameters**:

- `color`: The fill color.

**Returns**:

- No return value.

### 2.12 Image Display

```python
lcd.show(img=None, x=0, y=0)
lcd.show_image(img=None, x=0, y=0)
```

Displays an image on the LCD.
If no `img` is provided, it displays the internal image buffer.

**Parameters**:

- `img`: (Optional) The image object to display.
- `x`: (Optional) The starting x-coordinate of the image.
- `y`: (Optional) The starting y-coordinate of the image.

**Returns**:

- No return value.

## 3. LCD Type

`SPI_LCD.ST7789`: `1`, `SPI` 4 Line `ST7789`

## 4. Example Code

### 4.1 Displaying Text on the Screen

```python
import time, image
from machine import FPIOA, Pin, SPI, SPI_LCD

fpioa = FPIOA()

fpioa.set_function(19, FPIOA.GPIO19)
pin_cs = Pin(19, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
pin_cs.value(1)

fpioa.set_function(20, FPIOA.GPIO20)
pin_dc = Pin(20, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
pin_dc.value(1)

fpioa.set_function(44, FPIOA.GPIO44, pu=1)
pin_rst = Pin(44, Pin.OUT, pull=Pin.PULL_UP, drive=15)

# spi
fpioa.set_function(15, fpioa.QSPI0_CLK)
fpioa.set_function(16, fpioa.QSPI0_D0)

spi1 = SPI(1, baudrate=1000*1000*50, polarity=1, phase=1, bits=8)

lcd = SPI_LCD(spi1, pin_dc, pin_cs, pin_rst)

lcd.configure(320, 240, hmirror=False, vflip=True, bgr=False)

print(lcd)

img = lcd.init()
print(img)

img.clear()
img.draw_string_advanced(0, 0, 32, "RED, Hello World~", color=(255, 0, 0))
img.draw_string_advanced(0, 40, 32, "GREEN, Hello World~", color=(0, 255, 0))
img.draw_string_advanced(0, 80, 32, "BLUE, Hello World~", color=(0, 0, 255))

lcd.show()
```

This example will display "Hello World~" in red, green, and blue on the screen.

![hello-world](https://developer.canaan-creative.com/api/post/attachment?id=438)
