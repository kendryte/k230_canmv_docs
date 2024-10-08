# 2.16 TOUCH Module API Manual

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
touch = TOUCH(index, rotation)
```

**Parameters**

- `index`: TOUCH device number, range [0, 9], the actual value depends on the number of touch devices present.
- `rotation`: Rotation of the panel output coordinates relative to the screen coordinates, range [0-3], see [Coordinate Rotation](#42-coordinate-rotation) for specific definitions.

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
