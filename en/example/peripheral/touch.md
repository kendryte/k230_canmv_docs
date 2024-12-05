# 12. TOUCH Routine

## 1. Overview

The touch module of the K230 is based on the touch framework encapsulated by RT-Smart, supporting operations for single-point and multi-point capacitive touch screens as well as resistive touch screens.

## 2. Example

The following example demonstrates how to use the TOUCH module to read touch data.

```python
from machine import TOUCH

# Instantiate TOUCH device 0
tp = TOUCH(0)
# Initialize touch device 0, with coordinates rotated by 90 degrees
# tp = TOUCH(0, 1)

# Get TOUCH data
p = tp.read()
print(p)

# Output the coordinates and event information of the touch points
# print(p[0].x)
# print(p[0].y)
# print(p[0].event)
```

## 3. Code Explanation

1. **Import the module**:
   - Import the `TOUCH` module.

1. **Instantiate the touch device**:
   - Use `TOUCH(0)` to instantiate touch device 0. If coordinate rotation is needed, use `TOUCH(0, 1)`.

1. **Read touch data**:
   - Call `tp.read()` to get touch data, and the returned data is stored in `p`.

1. **Output touch information**:
   - You can print out the detailed touch data using `print(p)`. The commented-out parts `print(p[0].x)`, `print(p[0].y)`, and `print(p[0].event)` are used to output the x and y coordinates of the first touch point and the touch event type, respectively.

```{admonition} Note
For specific interfaces of the TOUCH module, please refer to the [API documentation](../../api/machine/K230_CanMV_TOUCH_Module_API_Manual.md)
```
