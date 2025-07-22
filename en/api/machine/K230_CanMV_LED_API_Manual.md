# `LED` Module API Manual

## Overview

The development board includes an RGB LED, which users can control the brightness of each color through the API.

## API Introduction

The LED class is located under the `machine` module.

### Example

```python
from machine import LED
import time

# Instantiate LED objects
red_led = LED("LED_RED")          # Or red_led = LED(1)
green_led = LED("LED_GREEN")      # Or green_led = LED(2)
blue_led = LED("LED_BLUE")        # Or blue_led = LED(3)

# Turn off all LEDs
blue_led.off()
green_led.off()
red_led.off()

while True:
    # Set the brightness of the green LED
    green_led.value(50)    # Brightness range is 0-255
    red_led.on()           # Turn on the red LED
    time.sleep_ms(250)
    
    green_led.value(200)   # Set the brightness of the green LED
    red_led.off()          # Turn off the red LED
    time.sleep_ms(250)
```

### Constructor

```python
led = LED(id)
```

**Parameters**

- `id`: Identifier of the LED, 1 or "LED_RED" for the red LED; 2 or "LED_GREEN" for the green LED; 3 or "LED_BLUE" for the blue LED.

### `value` Method

```python
led.value(val)
```

Controls the brightness of the LED.

**Parameters**

- `val`: Brightness level, ranging from 0 to 255.

**Return Value**

None

### `on` Method

```python
led.on()
```

Turns on the LED at maximum brightness.

**Parameters**

None

**Return Value**

None

### `off` Method

```python
led.off()
```

Turns off the LED.

**Parameters**

None

**Return Value**

None
