
# K230 TOUCH Usage Guide

## Overview

The K230 supports both capacitive and resistive touch input, providing a `TOUCH` class interface based on the RT-Smart framework. Developers can use it to read touch point coordinates, event types, and more, suitable for HMI, interactive terminals, and similar scenarios.

## Quick Start Example

The following example demonstrates how to read touch point data from the screen:

```python
from machine import TOUCH

# Instantiate default touch device 0
tp = TOUCH(0)

# Read current touch point data (returns a tuple of TOUCH_INFO objects)
p = tp.read()
print(p)

# If there are touch points, access the first point's coordinates and event type
# print(p[0].x)       # X coordinate
# print(p[0].y)       # Y coordinate
# print(p[0].event)   # Event type (e.g. EVENT_DOWN, EVENT_MOVE, EVENT_UP)
```

## API Overview

| API | Description |
| --- | --- |
| `TOUCH(dev, *, rotate=-1, range_x=-1, range_y=-1, i2c=None, rst=None, int=None)` | Create a touch instance. `dev=0` for system default, `dev!=0` for custom device. See below for parameters. |
| `read([count])` | Returns current touch point info as a tuple of TOUCH_INFO objects. `count` is the max number of points to read (default 1). |
| `deinit()` | Release touch resources. |

### Constructor Parameters

- `dev`: Touch device index. 0 for system default, non-0 for custom device.
- `rotate`: Coordinate rotation, see [Constants](#constants), default -1 (use device default).
- `range_x`, `range_y`: Only valid for custom devices, specify touch screen resolution.
- `i2c`: Only valid for custom devices, I2C bus object, required.
- `rst`, `int`: Only valid for custom devices, reset/interrupt pin objects, optional.
- Other parameters (e.g. type, slave_addr) are deprecated.

### TOUCH_INFO Object Attributes

- `event`: Event code, see [Constants](#constants)
- `track_id`: Touch point ID
- `width`: Touch point width
- `x`: X coordinate
- `y`: Y coordinate
- `timestamp`: Timestamp

## Example Details

### 1. Instantiate Device

```python
# System default touch
tp = TOUCH(0)

# Custom touch device (must specify i2c, resolution, etc.)
# tp = TOUCH(1, i2c=my_i2c, range_x=800, range_y=480)
```

### 2. Read Touch Data

```python
p = tp.read()
print(p)
```

The returned `p` is a tuple, each element is a TOUCH_INFO object. Each object contains:

- `x`: X coordinate
- `y`: Y coordinate
- `event`: Touch event (e.g. EVENT_DOWN, EVENT_MOVE, EVENT_UP)
- `track_id`, `width`, `timestamp`, etc.

### 3. Example Output

```text
(<TOUCH_INFO x=120 y=65 event=0 ...>,)
```

If there are multiple touch points (multi-touch):

```text
(<TOUCH_INFO x=120 y=65 event=0 ...>, <TOUCH_INFO x=250 y=130 event=0 ...>)
```

## Constants

### Touch Events

- `TOUCH.EVENT_NONE`: No event
- `TOUCH.EVENT_UP`: Released
- `TOUCH.EVENT_DOWN`: Pressed
- `TOUCH.EVENT_MOVE`: Moved

### Coordinate Rotation

- `TOUCH.ROTATE_0`: No rotation
- `TOUCH.ROTATE_90`: Rotate 90 degrees
- `TOUCH.ROTATE_180`: Rotate 180 degrees
- `TOUCH.ROTATE_270`: Rotate 270 degrees
- `TOUCH.ROTATE_SWAP_XY`: Swap X and Y

### Touch Types (compatibility only, all values are 0)

- `TOUCH.TYPE_CST226SE`
- `TOUCH.TYPE_CST328`
- `TOUCH.TYPE_GT911`

## FAQ

**Q: No touch points are read, returns an empty tuple?**
A: This means the screen is not being touched. `tp.read()` only returns points when the screen is pressed.

**Q: How to handle multi-touch?**
A: The result is a tuple of `TOUCH_INFO` objects, use a `for` loop to iterate through them.

**Q: Is coordinate rotation supported?**
A: Yes, use the `rotate` parameter (e.g. `TOUCH.ROTATE_90`) to enable coordinate rotation.

## Further Reading

- 📄 [TOUCH Module API Manual](../../api/machine/K230_CanMV_TOUCH_API_Manual.md)
