# K230 Touch Screen (TOUCH) Usage Tutorial

## Overview

K230 supports touch input for both **capacitive screens** and **resistive screens**, providing a `TOUCH` class interface based on the RT-Smart package. Developers can use it to read touch point coordinates, event types, and other information, making it widely applicable in scenarios such as HMI and interactive terminals.

## Quick Start Example

The following example demonstrates how to read touch point data from the touch screen:

```python
from machine import TOUCH

# Instantiate touch device 0 (system default touch)
tp = TOUCH(0)

# Read current touch point data (returns a tuple, each element is a TOUCH_INFO object)
p = tp.read()
print(p)

# If there are touch points, you can access the coordinates and event type of the first touch point
# print(p[0].x)       # X coordinate
# print(p[0].y)       # Y coordinate
# print(p[0].event)   # Event type (e.g., EVENT_DOWN, EVENT_MOVE, EVENT_UP)
```

## Interface Description

| Interface Name | Description |
| --- | --- |
| `TOUCH(dev, *, rotate=-1, range_x=-1, range_y=-1, i2c=None, rst=None, int=None)` | Creates a touch screen instance, `dev=0` indicates the system default, `dev!=0` is a custom device, see parameter details below |
| `read([count])` | Returns current touch point information, returns a tuple where each element is a TOUCH_INFO object, `count` is the maximum number of touch points to read (default 1) |
| `deinit()` | Releases touch resources |

### Constructor Parameter Description

- `dev`: Touch device number, 0 for system default, non-zero for custom device.
- `rotate`: Coordinate rotation, see [Constants](#constants), default -1 (use device default).
- `range_x`, `range_y`: Valid only for custom devices, specifies the touch screen resolution.
- `i2c`: Valid only for custom devices, I2C bus object, required.
- `rst`, `int`: Valid only for custom devices, reset/interrupt pin objects, optional.
- Other parameters are deprecated.

### TOUCH_INFO Object Properties

- `event`: Event code, see [Constants](#constants)
- `track_id`: Touch point ID
- `width`: Touch point width
- `x`: X coordinate
- `y`: Y coordinate
- `timestamp`: Timestamp

## Detailed Examples

### 1. Instantiating the Device

```python
# System default touch
tp = TOUCH(0)

# Custom touch device (need to specify i2c, resolution, etc.)
# tp = TOUCH(1, i2c=my_i2c, range_x=800, range_y=480)
```

### 2. Reading Touch Data

```python
p = tp.read()
print(p)
```

The returned `p` is a tuple, where each element is a TOUCH_INFO object. Each object contains:

- `x`: X coordinate
- `y`: Y coordinate
- `event`: Touch event (e.g., EVENT_DOWN, EVENT_MOVE, EVENT_UP)
- `track_id`, `width`, `timestamp`, etc.

### 3. Example Output Reference

```text
(<TOUCH_INFO x=120 y=65 event=0 ...>,)
```

If there are multiple touch points, e.g., supporting multi-finger operation:

```text
(<TOUCH_INFO x=120 y=65 event=0 ...>, <TOUCH_INFO x=250 y=130 event=0 ...>)
```

<a id="constants"></a>

## Constants

### Touch Events

- `TOUCH.EVENT_NONE`: No event
- `TOUCH.EVENT_UP`: Lift up
- `TOUCH.EVENT_DOWN`: Press down
- `TOUCH.EVENT_MOVE`: Move

### Coordinate Rotation

- `TOUCH.ROTATE_0`: No rotation
- `TOUCH.ROTATE_90`: Rotate 90 degrees
- `TOUCH.ROTATE_180`: Rotate 180 degrees
- `TOUCH.ROTATE_270`: Rotate 270 degrees
- `TOUCH.ROTATE_SWAP_XY`: XY swap

### Touch Types (reserved for compatibility, actual values are all 0)

- `TOUCH.TYPE_CST226SE`
- `TOUCH.TYPE_CST328`
- `TOUCH.TYPE_GT911`

## Application Scenarios

| Scenario | Example |
| --- | --- |
| GUI Interaction | Button clicks and slide toggles driven by touch points |
| Custom Gesture Recognition | Multi-point sliding, rotation and other gesture recognition |
| Simple Drawing Board or Signature Pad | Line drawing based on touch point trajectories |

## Frequently Asked Questions

**Q: No touch points read, and the returned value is an empty tuple?**
A: This means the screen is not being touched. `tp.read()` only returns touch points when the screen is pressed.

**Q: How to handle multi-touch?**
A: The read result is a tuple containing multiple `TOUCH_INFO` entries. Use a `for` loop to iterate through them.

**Q: Does it support coordinate rotation?**
A: Yes, coordinate rotation can be enabled through the `rotate` parameter (such as `TOUCH.ROTATE_90`).

## Further Reading

- 📄 [TOUCH Module API Documentation](../../api/machine/k230_canmv_touch_api_manual.md)
