# 2.16 `TOUCH` Module API Manual

## 1. Overview

The touch module is based on RTT's touch framework and supports single-point and multi-point capacitive touch screens as well as resistive touch screens.

## 2. API Introduction

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

- `index`: TOUCH device number. When `0`, it indicates the use of the system's built-in touch. When `1`, it indicates the use of the CanMV-specific touch driver.
- `type`: The touch driver type, refer to [Touch Types](#43-touch-device-type) for specific definitions.
- `rotate`: The rotation of the panel output coordinates relative to the screen coordinates, range [0-3]. Refer to [Coordinate Rotation](#42-coordinate-rotation) for specific definitions.
- `range_x`: Valid when `index=1`. The maximum width of the touch output coordinates.
- `range_y`: Valid when `index=1`. The maximum height of the touch output coordinates.
- `i2c`: Valid when `index=1`. The I2C bus object used for touch.
- `slave_addr`: Valid when `index=1`. The touch device i2c slave address, if not set, use driver default.
- `rst`: Valid when `index=1`. The reset pin object for the touch device.
- `int`: Valid when `index=1`. The interrupt pin object for the touch device, `currently not supported`.

### `read` Method

```python
TOUCH.read([count])
```

Get touch data.

**Parameters**

- `count`: Maximum number of touch points to read, range [0:10], default is 0, which means to read all touch points.

**Return Value**

Returns touch point data, type is a tuple `([tp[, tp...]])`, where each `tp` is an instance of the `touch_info` class.

### `deinit` Method

```python
TOUCH.deinit()
```

Release TOUCH resources.

**Parameters**

None

**Return Value**

None

## 3. TOUCH_INFO Class

The TOUCH_INFO class is used to store information about touch points, which users can access through related read-only properties.

- `event`: Event code, see [Touch Events](#41-touch-events) for details.
- `track_id`: Touch point ID, used for multi-point touch.
- `width`: Touch point width.
- `x`: x-coordinate of the touch point.
- `y`: y-coordinate of the touch point.
- `timestamp`: Touch point timestamp.

## 4. Constants

### 4.1 Touch Events

- `EVENT_NONE`: No event.
- `EVENT_UP`: Touch released after pressing.
- `EVENT_DOWN`: Touch started when pressed.
- `EVENT_MOVE`: Touch moved after pressing.

### 4.2 Coordinate Rotation

- `ROTATE_0`: No rotation.
- `ROTATE_90`: Rotate coordinates 90 degrees.
- `ROTATE_180`: Rotate coordinates 180 degrees.
- `ROTATE_270`: Rotate coordinates 270 degrees.

### 4.3 Touch device Type

- `TYPE_CST328`: `CanMV` Drive Touch
- `TYPE_CST226SE`: `CanMV` Drive Touch
- `TYPE_GT911`: `CanMV` Drive Touch
