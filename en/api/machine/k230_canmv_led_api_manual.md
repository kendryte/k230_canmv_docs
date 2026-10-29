# `neopixel` Module API Manual

## Overview

This module is an upgraded version of the original machine.LED.

The `neopixel` module is used to drive RGB LED strips based on the **WS2812 / WS2812B** (also known as NeoPixel) chip. These strips communicate serially through a single data line, offering color control and cascading functionality, and are widely used in decorative lighting, status indication, and other scenarios.

This module supports RGB or RGBW types, with each pixel occupying 3 or 4 bytes, and provides a buffer-style operation interface for convenient batch updates.

---

CanMV K230 currently supports using GPIO to drive WS2812 LEDs.

```{attention}
Since GPIO is currently used to generate the timing for driving WS2812, interrupts need to be disabled when sending data. Therefore, controlling a large number of LEDs may affect the operation of other modules. Please choose the number of LEDs accordingly.
```

---

## `NeoPixel` Class

### Example Code

```python
from machine import Pin
import neopixel
import time

# Define the LED strip data pin and the number of LEDs
NEO_PIN = 42
NUM_PIXELS = 8

# Initialize the LED strip object
np = neopixel.NeoPixel(Pin(NEO_PIN), NUM_PIXELS)

# Set the first LED to red, the second to green, the third to blue
np[0] = (255, 0, 0)
np[1] = (0, 255, 0)
np[2] = (0, 0, 255)

# Write data (must call write() to take effect)
np.write()

# Turn off all LEDs
np.fill((0, 0, 0))
np.write()
```

---

### Constructor

```python
neopixel.NeoPixel(pin, n, bpp=3, timing=1)
```

**Parameters**

* `pin`: The data pin controlling the WS2812 LED strip, of type `machine.Pin` object.
* `n`: The number of LEDs.
* `bpp`: Bytes per pixel, 3 for RGB, 4 for RGBW, default is 3.
* `timing`: Send timing configuration, usually 1 (WS2812). If 0, it is used for WS2811/800kHz mode.

---

### `__getitem__` / `__setitem__` Index Operations

```python
np[i] = (r, g, b)
color = np[i]
```

**Description**

Access or set the color of the `i`th LED through indexing. The color is a tuple `(r, g, b)` (or `(r, g, b, w)`, depending on `bpp`).

---

### `write()` Method

```python
np.write()
```

**Description**

Writes the current color buffer to the LED strip. **This method must be called for the LED colors to update**.

---

### `fill()` Method

```python
np.fill((r, g, b))
```

**Description**

Sets all LEDs to the same color. The color format is the same as `__setitem__`.

---

### `__len__()` Method

```python
length = len(np)
```

**Description**

Gets the number of LEDs in the current LED strip object.

---

## Notes

* Before use, please ensure the data pin is correctly connected and configured as output mode.
* For long LED strips (e.g., >30 LEDs), it is recommended to use an external power supply and add a 330Ω resistor to the data line for protection.
* Interrupts will be disabled during data transmission to avoid timing errors.

---

## Advanced Example: Rainbow Animation

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
