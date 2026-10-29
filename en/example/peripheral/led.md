# K230 Controlling NeoPixel Light Strip Tutorial

## 1. Introduction: What is NeoPixel?

NeoPixel is the commercial name for RGB LEDs based on the **WS2812** single-wire bus. Its features include:

* Each LED has an integrated control chip, single-wire control
* Supports RGB color settings
* Multiple LEDs can be cascaded, supporting individual control

The K230 provides native support for NeoPixel, suitable for creative lighting effects, status indicators, visual demonstrations, and other projects.

## 2. Hardware Connection Instructions

| Item            | Content                         |
| --------------- | ------------------------------- |
| Control Pin     | GPIO42 (used in example)        |
| LED Power Supply | External power supply recommended (5V) |
| GND Grounding   | Common ground with K230 board GND |
| LED Count Limit | Subject to actual test          |

> ⚠️ Note: Each WS2812 LED can draw up to 60mA at full brightness; external power is required for multiple LEDs.

## 3. Example Code: Quick Start

```python
import time
from machine import Pin
import neopixel

# === Parameter Configuration ===
NEOPIXEL_PIN = 42     # GPIO pin controlling WS2812
NUM_PIXELS   = 10     # Number of LEDs

# === Initialize NeoPixel ===
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

# === Function: Set uniform color ===
def test_colors():
    print("[TEST] Set uniform color for all LEDs")
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow
    for color in colors:
        np.fill(color)
        np.write()
        print(f" → Color: {color}")
        time.sleep(0.5)

# === Function: Light up LEDs one by one ===
def test_pixels():
    print("[TEST] Light up each LED in sequence")
    for i in range(NUM_PIXELS):
        np.fill((0, 0, 0))
        np[i] = (0, 255, 128)
        np.write()
        print(f" → LED {i} lit")
        time.sleep(0.2)

# === Function: Turn off all LEDs ===
def clear():
    np.fill((0, 0, 0))
    np.write()
    print("[TEST] All LEDs off")

# === Main test flow ===
def run_test():
    test_colors()
    test_pixels()
    clear()
    print("[Done] NeoPixel test completed")

run_test()
```

## 4. Code Structure Explanation

### 1️⃣ Initialize the light strip object

```python
np = neopixel.NeoPixel(Pin(42), 10)
```

* The first parameter is the GPIO control pin (e.g., 42)
* The second parameter is the number of LEDs (e.g., 10)

By default, the RGB format is used. You can set colors with `np[i] = (r, g, b)`.

### 2️⃣ Set uniform color

```python
np.fill((255, 0, 0))  # All red
np.write()            # Write update
```

You can use `fill()` to set the color of all LEDs at once, then send it to the LEDs with `write()`.

### 3️⃣ Light up LEDs one by one

```python
for i in range(NUM_PIXELS):
    np.fill((0, 0, 0))   # Clear
    np[i] = (0, 255, 128)
    np.write()
```

Lighting up individual LEDs is used for **LED number identification**, **installation direction debugging**, etc.

### 4️⃣ Turn off LEDs

```python
np.fill((0, 0, 0))
np.write()
```

Setting the color to black `(0, 0, 0)` will turn off all LEDs.

## V. Common Application Scenarios

| Scenario | Example Description |
| ------ | ------------------- |
| Status indicator light | Different colors represent different states |
| Rainbow light strip | Different LEDs display different colors |
| Interactive lighting effects | Touch or sensor triggers dynamic changes |
| Programming teaching demo | Used for Python hardware control teaching practice |

## VI. Usage Suggestions and Precautions

| Item | Suggestion Description |
| ---- | ---------------------- |
| Number of LEDs | Recommended not to exceed 16, too many may affect system timing |
| Power supply | Multiple LEDs require external 5V power supply (pay attention to current) |
| Performance | Disable interrupts during data transmission, frequent refreshing is not recommended |
| Stability | All GND must share a common ground, otherwise communication may fail |

## VII. Reference Materials and Advanced Extensions

* 📘 [MicroPython Official NeoPixel Module Documentation](https://docs.micropython.org/en/latest/library/neopixel.html)
