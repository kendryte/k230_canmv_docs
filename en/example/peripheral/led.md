# LED Routine Explanation

## Overview

The K230 development board comes with an onboard LED light that users can easily control using the `machine.LED` module. This feature can be used to indicate status or provide visual feedback.

## Example

The following example demonstrates how to use the LED module of the K230 to control the LED's on/off state and brightness:

```python
from machine import LED
import time

# Initialize LED objects
red_led = LED("LED_RED")          # Alternatively, use red_led = LED(1)
green_led = LED("LED_GREEN")      # Alternatively, use green_led = LED(2)
blue_led = LED("LED_BLUE")        # Alternatively, use blue_led = LED(3)

# Turn off all LEDs
blue_led.off()
green_led.off()
red_led.off()

while True:
    # Set the brightness of the green LED, range is 0-255
    green_led.value(50)    
    red_led.on()           # Turn on the red LED
    time.sleep_ms(250)     # Pause for 250 milliseconds

    green_led.value(200)   # Set the brightness of the green LED
    red_led.off()          # Turn off the red LED
    time.sleep_ms(250)     # Pause for 250 milliseconds
```

## Code Explanation

This routine demonstrates how to control the LED on the K230 development board using its LED module. By adjusting the LED's state and brightness, developers can achieve various visual effects to enhance the interactive experience.

- **Import Modules**: First, import the `machine` and `time` modules. The former is used to control the hardware, and the latter is used to set time delays.

- **Initialize LED Objects**:
  - `red_led = LED("LED_RED")`: Create a red LED object.
  - `green_led = LED("LED_GREEN")`: Create a green LED object.
  - `blue_led = LED("LED_BLUE")`: Create a blue LED object.

- **Turn Off LEDs**: Turn off all LEDs by calling the `off()` method to ensure the initial state is off.

- **Main Loop**:
  - Use `while True:` to start an infinite loop.
  - Inside the loop, first set the brightness of the green LED to 50 and turn on the red LED.
  - `time.sleep_ms(250)` pauses the program for 250 milliseconds to keep the red LED on.
  - Then, set the brightness of the green LED to 200 and turn off the red LED.
  - Pause again for 250 milliseconds.

```{admonition} Tip
For detailed interface information about the LED module, please refer to the [API documentation](../../api/machine/K230_CanMV_LED_Module_API_Manual.md).
```
