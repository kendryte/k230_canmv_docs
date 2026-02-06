# `TOUCH` Module API Manual

## Overview

The touch module is based on RTT's touch framework and supports single-point and multi-point capacitive touch screens as well as resistive touch screens.

## API Introduction

The TOUCH class is located under the `machine` module.

**Example**

```python
from machine import TOUCH

# Instantiate TOUCH device 0
tp = TOUCH(0)
# Get TOUCH data
p = tp.read()
print(p)
# Print touch point coordinates
# print(p[0].x)
# print(p[0].y)
# print(p[0].event)
```

### Constructor

```python
# when index is 0
touch = TOUCH(index, type = TOUCH.TYPE_CST328, rotate = -1)

# when index is 1
touch = TOUCH(index, type = TOUCH.TYPE_CST328, rotate = -1, range_x = -1, range_y = -1, i2c : I2C = None, slave_addr = None, rst : Pin = None, int : Pin = None)
```

**Parameters**

### `read` Method

```python
TOUCH.read([count])
```

Get touch data.

**Parameters**

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

The TOUCH_INFO class is used to store information about touch points, which users can access through related read-only properties.

- `event`: Event code, see [Touch Events](#touch-events) for details.
- `track_id`: Touch point ID, used for multi-point touch.
- `width`: Touch point width.
- `x`: x-coordinate of the touch point.
- `y`: y-coordinate of the touch point.
- `timestamp`: Touch point timestamp.

## Constants

### Touch Events

- `TOUCH.EVENT_NONE`: No event
- `TOUCH.EVENT_UP`: Released
- `TOUCH.EVENT_DOWN`: Pressed
- `TOUCH.EVENT_MOVE`: Moved

### Coordinate Rotation

- `TOUCH.ROTATE_0`: No rotation
- `TOUCH.ROTATE_90`: Rotate coordinates 90 degrees
- `TOUCH.ROTATE_180`: Rotate coordinates 180 degrees
- `TOUCH.ROTATE_270`: Rotate coordinates 270 degrees
- `TOUCH.ROTATE_SWAP_XY`: Swap X and Y

### Touch Types (compatibility only, all values are 0)

- `TOUCH.TYPE_CST226SE`
- `TOUCH.TYPE_CST328`
- `TOUCH.TYPE_GT911`
