# Rotary Encoder Tutorial

## What is a Rotary Encoder?

**Rotary Encoder** is a sensor that converts rotational position or motion into digital signals. Common incremental rotary encoders provide position feedback by detecting rotation direction and amount. Common applications include:

- Volume control knobs
- Menu navigation controls
- Precise position control
- Speed and direction detection
- Industrial automation equipment

K230 supports connecting incremental rotary encoders by reading the encoder's CLK (clock), DT (data), and SW (switch) signals through GPIO pins, enabling:

- Rotation direction detection (clockwise/counterclockwise)
- Rotation counting (incremental values and total count)
- Button state detection (encoders typically include a push switch)

## Example Overview

The following examples demonstrate how to use K230's `ENCODER` module to:

- Initialize a rotary encoder
- Read rotation data and button state
- Reset encoder count
- Release encoder resources

### 1. Import Module and Initialize Encoder

```python
from machine import ENCODER

# Initialize encoder 0, connect CLK to pin 42, DT to pin 43, SW to pin 5
encoder = ENCODER(id=0, pin_clk=42, pin_dt=43, pin_sw=5)
```

- `id`: Encoder instance number (required, different ids distinguish multiple encoder instances, e.g., id=0,1,2,3...)
- `pin_clk`: Clock signal pin (required)
- `pin_dt`: Data signal pin (required)
- `pin_sw`: Button signal pin (optional, set to -1 if not used)

### 2. Read Encoder Data

```python
# Blocking read, wait for encoder event
data = encoder.read()
if data:
    print(f"Delta change: {data.delta}")
    print(f"Total count: {data.total_count}")
    print(f"Rotation direction: {data.direction}")
    print(f"Button state: {data.button_state}")
    print(f"Timestamp: {data.timestamp}")

# Read with timeout (in milliseconds)
data = encoder.read(timeout_ms=1000)
if data is None:
    print("No encoder event within 1 second")
```

The returned data object contains the following attributes:

- `delta`: Incremental change value for this event
- `total_count`: Total count value since initialization
- `direction`: Rotation direction (DIR_CW clockwise / DIR_CCW counterclockwise / DIR_NONE none)
- `button_state`: Button state (0 released / 1 pressed)
- `timestamp`: Event timestamp

### 3. Reset Encoder Count

```python
# Reset encoder's total count to 0
encoder.reset()
```

### 4. Release Encoder Resources

```python
# Release encoder resources
del encoder
# Or explicitly call
encoder.__del__()
```

## Direction Constants

The ENCODER class provides the following direction constants:

| Constant | Value | Description |
|----------|-------|-------------|
| DIR_NONE | 0 | No rotation |
| DIR_CW | 1 | Clockwise rotation |
| DIR_CCW | 2 | Counterclockwise rotation |

Usage example:

```python
if data.direction == ENCODER.DIR_CW:
    print("Clockwise rotation")
elif data.direction == ENCODER.DIR_CCW:
    print("Counterclockwise rotation")
```

## Complete Usage Example

```python
from machine import ENCODER
import time

# Initialize encoder
encoder = ENCODER(id=0, pin_clk=42, pin_dt=43, pin_sw=5)

# Menu selection example
menu_items = ["Option 1", "Option 2", "Option 3", "Option 4"]
current_index = 0

print("Rotate to select menu item, press to confirm")

while True:
    # Read encoder event with 100ms timeout
    data = encoder.read(100)
    
    if data:
        # Update menu index based on rotation direction
        if data.direction == ENCODER.DIR_CW:
            current_index = (current_index + 1) % len(menu_items)
        elif data.direction == ENCODER.DIR_CCW:
            current_index = (current_index - 1) % len(menu_items)
        
        # Display current selection
        print(f"Current selection: {menu_items[current_index]}")
        
        # Detect button press
        if data.button_state == 1:
            print(f"Confirmed: {menu_items[current_index]}")
            break

# Clean up resources
del encoder
```

## Application Scenarios

- **User Interface Control** (menu navigation, parameter adjustment)
- **Volume/Brightness Adjustment** (precise value adjustment)
- **Position Control** (stepper motor control, robotic arm positioning)
- **Measuring Instruments** (angle measurement, length measurement)
- **Game Controllers** (steering wheels, knob controls)

## Important Notes

- CLK and DT pins are required, SW pin is optional
- Pull-up resistors are recommended for CLK and DT pins (usually built into encoder modules)
- Fast rotation may require more frequent reading to avoid missing events

## Compilation Switch

- Rotary encoder support is disabled by default. To enable it, run `make menuconfig` and enable the following compilation option:

```c
> RT-Smart Configuration > RT-Thread Smart System Features
        [*] Enable Rotary Encoder Support
```
