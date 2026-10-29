# `TOUCH` Module API Manual

## Overview

The touch module is based on RTT's touch framework, supporting single-point and multi-point capacitive touch screens as well as resistive touch screens.

## API Introduction

The TOUCH class is located under the `machine` module.

**Example**

```python
from machine import TOUCH

# Instantiate TOUCH device 0 (system default touch)
tp = TOUCH(0)
# Get TOUCH data (returns a tuple, each element is a TOUCH_INFO object)
p = tp.read()
print(p)
# Print touch point coordinates
# print(p[0].x)
# print(p[0].y)
# print(p[0].event)
```

### Constructor

```python
# System default touch
touch = TOUCH(dev)

# Custom touch device (dev != 0, requires specifying i2c, resolution, etc.)
touch = TOUCH(dev, i2c=my_i2c, range_x=800, range_y=480, rotate=TOUCH.ROTATE_0)
```

**Parameters**

- `dev`: Touch device number, 0 is the system default, non-zero is a custom device.
- `rotate`: Coordinate rotation, see [Constants](#constants), default -1 (use device default).
- `range_x`, `range_y`: Only valid for custom devices, specifies touch screen resolution.
- `i2c`: Only valid for custom devices, I2C bus object, required.
- `rst`, `int`: Only valid for custom devices, reset/interrupt pin objects, optional.
- Other parameters (such as type, slave_addr) are deprecated.

### `read` Method

```python
TOUCH.read([count])
```

Get touch data.

**Parameters**

- `count`: Maximum number of touch points to read, range [1, maximum supported number], default 1.

**Return Value**

Returns touch point data, type is tuple `(<TOUCH_INFO object>, ...)`, each element is a `TOUCH_INFO` instance.

### `deinit` Method

```python
TOUCH.deinit()
```

Release TOUCH resources.

**Parameters**

None

**Return Value**

None

## TOUCH_INFO Class

The TOUCH_INFO class is used to store information about touch points. Users can access it through the relevant read-only properties:

- `event`: Event code, see [Constants](#constants)
- `track_id`: Touch point ID, used for multi-touch.
- `width`: Touch point width.
- `x`: The x coordinate of the touch point.
- `y`: The y coordinate of the touch point.
- `timestamp`: Touch point timestamp.

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
- `TOUCH.ROTATE_SWAP_XY`: Swap XY

### Touch Types (Kept for compatibility, actual values are all 0)

- `TOUCH.TYPE_CST226SE`
- `TOUCH.TYPE_CST328`
- `TOUCH.TYPE_GT911`
