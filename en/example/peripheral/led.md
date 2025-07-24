# NeoPixel Control Example Explanation (K230)

## Overview

This example demonstrates how to control **WS2812 (NeoPixel) RGB LEDs** on the K230 development board using the `neopixel` module.
With this module, users can flexibly control the color of each individual RGB LED, enabling dynamic lighting effects, smooth color transitions, and pixel-level testing.

NeoPixel (WS2812) LEDs use single-wire serial communication, allowing multiple LEDs to be daisy-chained and controlled simultaneously.

This example includes:

* Setting all pixels to a solid color
* Lighting up LEDs one by one
* Clearing (turning off) all LEDs

---

## Example Code

```python
import time
from machine import Pin
import neopixel

# === CONFIGURATION ===
NEOPIXEL_PIN = 42     # GPIO pin number (adjust based on your wiring)
NUM_PIXELS   = 10     # Number of WS2812 LEDs

# === INITIALIZE NEOPIXEL OBJECT ===
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

# === FUNCTION: Show solid colors ===
def test_colors():
    print("[TEST] Setting colors...")
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 0)]  # Red, Green, Blue, Yellow

    for i, color in enumerate(colors):
        for j in range(NUM_PIXELS):
            np[j] = color
        np.write()
        print(f"  → Color: {color}")
        time.sleep(0.5)

# === FUNCTION: Test individual pixel addressing ===
def test_pixels():
    print("[TEST] Lighting up pixels one by one...")
    for i in range(NUM_PIXELS):
        np.fill((0, 0, 0))         # Clear all pixels
        np[i] = (0, 255, 128)      # Light up pixel i in teal
        np.write()
        print(f"  → Pixel {i} ON")
        time.sleep(0.2)

# === FUNCTION: Clear all pixels ===
def clear():
    np.fill((0, 0, 0))
    np.write()
    print("[TEST] Cleared all pixels.")

# === MAIN TEST SEQUENCE ===
def run_test():
    test_colors()
    test_pixels()
    clear()
    print("[DONE] NeoPixel test completed.")

run_test()
```

---

## Code Structure Explained

### 1. **Initialize NeoPixel**

```python
np = neopixel.NeoPixel(Pin(42), 10)
```

* Uses GPIO 42 to control the LED strip
* Configured for 10 LEDs
* Each LED is RGB (default `bpp=3`)

---

### 2. **Set All Pixels to Solid Colors (`test_colors`)**

```python
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 0)]
```

* Sets all pixels to red, green, blue, and yellow in sequence
* Can use either `np.fill()` or set each pixel manually
* `np.write()` sends the data to the LED strip

---

### 3. **Light Pixels One by One (`test_pixels`)**

```python
np[i] = (0, 255, 128)
```

* Lights up one LED at a time, clears the rest
* Useful for verifying pixel order and direction

---

### 4. **Clear All Pixels (`clear`)**

```python
np.fill((0, 0, 0)); np.write()
```

* Turns off all pixels by setting color to black `(0, 0, 0)`

---

## Notes & Recommendations

| Item           | Description                                                                 |
| -------------- | --------------------------------------------------------------------------- |
| GPIO Selection | Choose an unused GPIO, e.g., GPIO42 or GPIO43                               |
| Max Pixels     | Due to timing and interrupt constraints, it's recommended to use ≤ 16 LEDs  |
| Power Supply   | Each WS2812 LED can draw up to 60 mA at full brightness; use external power |
| Performance    | Interrupts are disabled during data transmission; limit length/refresh rate |

---

## More Information

For advanced effects like **rainbow animations**, **fading**, or **brightness control**, refer to the MicroPython official documentation:
👉 [https://docs.micropython.org/en/latest/library/neopixel.html](https://docs.micropython.org/en/latest/library/neopixel.html)

---
