# Common Image Drawing Routines Explanation

## Overview

OpenMV is a small embedded machine vision module widely used for rapid development of computer vision applications. OpenMV's image drawing methods can be used to draw various shapes and text on images for visual feedback and debugging.

CanMV supports OpenMV image drawing methods and adds some, such as [draw_string_advanced](../../api/openmv/image.md#129-draw_string_advanced) for drawing Chinese strings.

## Common Functions

### draw_string_advanced

The `draw_string_advanced` function uses freetype to render text and supports Chinese, and users can also specify the font.

- Syntax

```python
image.draw_string_advanced(x, y, char_size, str, [color, font])
```

- Parameter Explanation

  - `x, y`: Starting coordinates.
  - `char_size`: Character size.
  - `str`: The Chinese characters to be drawn.
  - `color`: Color of the text.
  - `font`: Font file path.

- Example

```python
img.draw_string_advanced(10, 10, 32, "你好世界", color=(255, 0, 0))  # Draw red text
```

### draw_line

The `draw_line` function can draw a line on the image.

- Syntax

```python
image.draw_line(x0, y0, x1, y1, color)
```

- Parameter Explanation

  - `x0, y0`: Starting coordinates.
  - `x1, y1`: Ending coordinates.
  - `color`: Color of the line.

- Example

```python
img.draw_line(10, 10, 100, 100, color=(255, 0, 0))  # Draw red line
```

### draw_rectangle

The `draw_rectangle` function can draw a rectangle on the image.

- Syntax

```python
image.draw_rectangle(x, y, w, h, color, thickness=1)
```

- Parameter Explanation

  - `x, y`: Coordinates of the top-left corner of the rectangle.
  - `w, h`: Width and height of the rectangle.
  - `color`: Color of the rectangle.
  - `thickness`: Thickness of the rectangle border (default is 1).

- Example

```python
img.draw_rectangle(20, 20, 50, 30, color=(0, 255, 0), thickness=2)  # Draw green rectangle
```

### draw_circle

The `draw_circle` function can draw a circle on the image.

- Syntax

```python
image.draw_circle(x, y, r, color, thickness=1)
```

- Parameter Explanation

  - `x, y`: Coordinates of the center of the circle.
  - `r`: Radius of the circle.
  - `color`: Color of the circle.
  - `thickness`: Thickness of the circle border (default is 1).

- Example

```python
img.draw_circle(60, 60, 30, color=(0, 0, 255), thickness=3)  # Draw blue circle
```

### draw_cross

The `draw_cross` function can draw a cross on the image.

- Syntax

```python
image.draw_cross(x, y, color, size=5, thickness=1)
```

- Parameter Explanation

  - `x, y`: Coordinates of the cross point.
  - `color`: Color of the cross.
  - `size`: Size of the cross (default is 5).
  - `thickness`: Thickness of the cross lines (default is 1).

- Example

```python
img.draw_cross(40, 40, color=(255, 255, 0), size=10, thickness=2)  # Draw yellow cross
```

### draw_arrow

The `draw_arrow` function can draw an arrow line on the image.

- Syntax

```python
image.draw_arrow(x0, y0, x1, y1, color, thickness=1)
```

- Parameter Explanation

  - `x0, y0`: Starting coordinates.
  - `x1, y1`: Ending coordinates.
  - `color`: Color of the arrow.
  - `thickness`: Thickness of the arrow line (default is 1).

- Example

```python
img.draw_arrow(10, 10, 100, 100, color=(255, 0, 0), thickness=2)  # Draw red arrow
```

### draw_ellipse

The `draw_ellipse` function can draw an ellipse on the image.

- Syntax

```python
image.draw_ellipse(cx, cy, rx, ry, color, thickness=1)
```

- Parameter Explanation

  - `cx, cy`: Coordinates of the center of the ellipse.
  - `rx, ry`: Radii of the ellipse (x-axis and y-axis directions).
  - `color`: Color of the ellipse.
  - `thickness`: Thickness of the ellipse border (default is 1).

- Example

```python
img.draw_ellipse(60, 60, 30, 20, color=(0, 0, 255), thickness=3)  # Draw blue ellipse
```

### draw_image

The `draw_image` function can draw another image on the current image.

- Syntax

```python
image.draw_image(img, x, y, alpha=128, scale=1.0)
```

- Parameter Explanation

  - `img`: The image object to be drawn.
  - `x, y`: Coordinates of the top-left corner of the drawing position.
  - `alpha`: Transparency (0-256).
  - `scale`: Scale factor (default is 1.0).

- Example

```python
overlay = image.Image("overlay.bmp")
img.draw_image(overlay, 10, 10, alpha=128, scale=1.0)  # Draw overlay.bmp at (10, 10)
```

### draw_keypoints

The `draw_keypoints` function can draw keypoints on the image.

- Syntax

```python
image.draw_keypoints(keypoints, size=10, color, thickness=1)
```

- Parameter Explanation

  - `keypoints`: List of keypoints, each keypoint is a tuple (x, y).
  - `size`: Size of the keypoints (default is 10).
  - `color`: Color of the keypoints.
  - `thickness`: Thickness of the keypoints border (default is 1).

- Example

```python
keypoints = [(30, 30), (50, 50), (70, 70)]
img.draw_keypoints(keypoints, size=10, color=(255, 255, 0), thickness=2)  # Draw yellow keypoints
```

### flood_fill

The `flood_fill` function can perform a flood fill algorithm on the image, starting from a specified point and filling with a specified color.

- Syntax

```python
image.flood_fill(x, y, color, threshold, invert=False, clear_background=False)
```

- Parameter Explanation

  - `x, y`: Starting coordinates.
  - `color`: Fill color.
  - `threshold`: Fill threshold, representing the allowable color difference range between the starting pixel and adjacent pixels.
  - `invert`: Boolean, if True, inverts the fill condition.
  - `clear_background`: Boolean, if True, clears the background outside the fill area.

- Example

```python
img.flood_fill(30, 30, color=(255, 0, 0), threshold=30, invert=False, clear_background=False)  # Start flood fill with red color from (30, 30)
```

### draw_string

The `draw_string` function can draw a string on the image.

- Syntax

```python
image.draw_string(x, y, text, color, scale=1)
```

- Parameter Explanation

  - `x, y`: Starting coordinates of the string.
  - `text`: Content of the string to be drawn.
  - `color`: Color of the string.
  - `scale`: Scale factor of the string (default is 1).

- Example

```python
img.draw_string(10, 10, "Hello OpenMV", color=(255, 255, 255), scale=2)  # Draw white string
```

## Example

This example is for demonstration purposes only.

```python
import time, os, gc, sys, urandom

from media.display import *
from media.media import *

DISPLAY_IS_HDMI = False
DISPLAY_IS_LCD = True
DISPLAY_IS_IDE = False

try:
    # Set default size
    width = 640
    height = 480
    if DISPLAY_IS_HDMI:
        # Use HDMI as display output, set to 1080P
        Display.init(Display.LT9611, width=1920, height=1080, to_ide=True)
        width = 1920
        height = 1080
    elif DISPLAY_IS_LCD:
        # Use LCD as display output
        Display.init(Display.ST7701, width=800, height=480, to_ide=True)
        width = 800
        height = 480
    elif DISPLAY_IS_IDE:
        # Use IDE as display output
        Display.init(Display.VIRT, width=800, height=480, fps=100)
        width = 800
        height = 480
    else:
        raise ValueError("Should select a display.")
    # Initialize media manager
    MediaManager.init()

    fps = time.clock()
    # Create the drawing image
    img = image.Image(width, height, image.ARGB8888)

    while True:
        fps.tick()
        # Check if at exit point
        os.exitpoint()
        img.clear()

        # Draw red line
        img.draw_line(10, 10, 100, 100, color=(255, 0, 0))

        # Draw green rectangle
        img.draw_rectangle(20, 20, 50, 30, color=(0, 255, 0), thickness=2)

        # Draw blue circle
        img.draw_circle(30, 30, 30, color=(0, 0, 255), thickness=3)

        # Draw yellow cross
        img.draw_cross(40, 40, color=(255, 255, 0), size=10, thickness=2)

        # Draw red Chinese string
        img.draw_string_advanced(50, 50, 32, "你好世界", color=(255, 0, 0))
        # Draw white string
        img.draw_string_advanced(50, 100, 32, "Hello CanMV", color=(255, 255, 255), scale=2)

        # Draw red arrow
        img.draw_arrow(60, 60, 100, 100, color=(255, 0, 0), thickness=2)

        # Draw blue ellipse
        radius_x = urandom.getrandbits(30) % (max(img.height(), img.width()) // 2)
        radius_y = urandom.getrandbits(30) % (max(img.height(), img.width()) // 2)
        rot = urandom.getrandbits(30)
        img.draw_ellipse(70, 70, radius_x, radius_y, rot, color=(0, 0, 255), thickness=2, fill=False)

        # Draw another image
        # overlay = image.Image("overlay.bmp")
        # img.draw_image(overlay, 10, 10, alpha=128, scale=1.0)

        # Draw yellow keypoints
        keypoints = [(30, 30), (50, 50), (70, 70)]
        img.draw_keypoints([(30, 40, rot)], color=(255, 255, 0), size=20, thickness=2, fill=False)

        # Perform flood fill
        img.flood_fill(90, 90, color=(255, 0, 0), threshold=30, invert=False, clear_background=False)

        # Display drawing results
        Display.show_image(img)

        # print(fps.fps())

        time.sleep_ms(10)
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # Destroy display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # Release media buffer
    MediaManager.deinit()
```

```{admonition} Note
For specific interface definitions, please refer to [image](../../api/openmv/image.md).
```
