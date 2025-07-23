# `neopixel` Module API Manual

## Overview

This module is an enhanced version of the original `machine.LED`.

The `neopixel` module is used to drive RGB LED strips based on **WS2812 / WS2812B** (also known as NeoPixel) chips. These strips use a single data line for serial communication, support color control and cascading, and are widely used for decorative lighting, status indicators, and similar applications.

This module supports both RGB and RGBW formats, where each pixel occupies 3 or 4 bytes. It provides a buffer-based interface for convenient batch updates.

---

The CanMV K230 currently supports driving WS2812 LEDs via GPIO.

```{attention}
Since GPIO is currently used to generate WS2812 timing signals, interrupts must be disabled during data transmission.  
Therefore, if controlling a large number of LEDs, it may affect the operation of other modules. Please choose the number of LEDs accordingly.
```

---

## `NeoPixel` Class

### Example Code

```python
from machine import Pin
import neopixel
import time

# Define the NeoPixel data pin and number of LEDs
NEO_PIN = 42
NUM_PIXELS = 8

# Initialize the NeoPixel object
np = neopixel.NeoPixel(Pin(NEO_PIN), NUM_PIXELS)

# Set the first LED to red, second to green, third to blue
np[0] = (255, 0, 0)
np[1] = (0, 255, 0)
np[2] = (0, 0, 255)

# Write the data (must call write() to update the LEDs)
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

* `pin`: The GPIO pin used to control the WS2812 LED strip. Must be a `machine.Pin` object.
* `n`: Number of LEDs.
* `bpp`: Bytes per pixel. `3` for RGB, `4` for RGBW. Default is `3`.
* `timing`: Protocol timing configuration. Use `1` for WS2812 (default), or `0` for WS2811/800kHz compatibility mode.

---

### `__getitem__` / `__setitem__` Indexing

```python
np[i] = (r, g, b)
color = np[i]
```

**Description**

Access or set the color of the `i`-th pixel using a tuple in the format `(r, g, b)` or `(r, g, b, w)` depending on `bpp`.

---

### `write()` Method

```python
np.write()
```

**Description**

Send the current color buffer to the LED strip.
**This method must be called for any changes to take effect.**

---

### `fill()` Method

```python
np.fill((r, g, b))
```

**Description**

Set all pixels in the LED strip to the same color. The color format is the same as in `__setitem__`.

---

### `__len__()` Method

```python
length = len(np)
```

**Description**

Returns the number of pixels in the current NeoPixel object.

---

## Notes

* Ensure the data pin is correctly connected and configured as an output before use.
* For long LED strips (e.g., more than 30 LEDs), external power supply is recommended. Also consider adding a 330Ω resistor in series with the data line for protection.
* Interrupts are disabled during data transmission to maintain timing accuracy.

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
