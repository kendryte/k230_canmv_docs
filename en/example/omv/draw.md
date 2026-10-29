# Common Image Drawing Routines Explained

## Overview

OpenMV is a small embedded machine vision module widely used for rapid development of computer vision applications. OpenMV's image drawing methods can be used to draw various shapes and text on images for visual feedback and debugging.

CanMV supports OpenMV image drawing methods, and adds some, such as drawing Chinese character strings [draw_string_advanced](../../api/openmv/image.md#draw_string_advanced)

## Common Functions

### draw_string_advanced

The `draw_string_advanced` function uses freetype to render text, supports Chinese, and allows users to specify the font.

- Syntax

```python
image.draw_string_advanced(x,y,char_size,str,[color, font])
```

- Parameter Explanation

  - `x, y`: Starting coordinates.
  - `char_size`: Character size
  - `str`: Chinese characters to be drawn
  - `color`: Text color.
  - `font`: Font file path

- Example

```python
img.draw_string_advanced(10, 10, 32, "你好世界", color=(255, 0, 0))  # 绘制红色线
```

### draw_line

The `draw_line` function can draw a line on an image.

- Syntax

```python
image.draw_line(x0, y0, x1, y1, color)
```

- Parameter Explanation

  - `x0, y0`: Starting coordinates.
  - `x1, y1`: Ending coordinates.
  - `color`: Line color.

- Example

```python
img.draw_line(10, 10, 100, 100, color=(255, 0, 0))  # 绘制红色线
```

### draw_rectangle

The `draw_rectangle` function can draw a rectangle on an image.

- Syntax

```python
image.draw_rectangle(x, y, w, h, color, thickness=1)
```

- Parameter Explanation

  - `x, y`: Upper-left corner coordinates of the rectangle.
  - `w, h`: Width and height of the rectangle.
  - `color`: Color of the rectangle.
  - `thickness`: Border thickness of the rectangle (default is 1).

- Example

```python
img.draw_rectangle(20, 20, 50, 30, color=(0, 255, 0), thickness=2)  # 绘制绿色矩形
```

### draw_circle

The `draw_circle` function can draw a circle on an image.

- Syntax

```python
image.draw_circle(x, y, r, color, thickness=1)
```

- Parameter Explanation

  - `x, y`: Circle center coordinates.
  - `r`: Radius of the circle.
  - `color`: Color of the circle.
  - `thickness`: Border thickness of the circle (default is 1).

- Example

```python
    img.draw_circle(60, 60, 30, color=(0, 0, 255), thickness=3)  # 绘制蓝色圆

```

### draw_cross

The `draw_cross` function can draw a cross on an image.

- Syntax

```python
image.draw_cross(x, y, color, size=5, thickness=1)
```

- Parameter Explanation

  - `x, y`: Cross point coordinates.
  - `color`: Color of the cross.
  - `size`: Size of the cross (default is 5).
  - `thickness`: Line thickness of the cross (default is 1).

- Example

```python
    img.draw_cross(40, 40, color=(255, 255, 0), size=10, thickness=2)  # 绘制黄色交叉

```

### draw_arrow

The `draw_arrow` function can draw an arrow line on an image.

- Syntax

```python
image.draw_arrow(x0, y0, x1, y1, color, thickness=1)
```

- Parameter Explanation

  - `x0, y0`: Starting coordinates.
  - `x1, y1`: Ending coordinates.
  - `color`: Color of the arrow.
  - `thickness`: Line thickness of the arrow (default is 1).

- Example

```python
img.draw_arrow(10, 10, 100, 100, color=(255, 0, 0), thickness=2)  # 绘制红色箭头
```

### draw_ellipse

The `draw_ellipse` function can draw an ellipse on an image.

- Syntax

```python
image.draw_ellipse(cx, cy, rx, ry, color, thickness=1)
```

- Parameter Explanation

  - `cx, cy`: Coordinates of the ellipse center.
  - `rx, ry`: Radii of the ellipse (x-axis and y-axis directions).
  - `color`: Color of the ellipse.
  - `thickness`: Border thickness of the ellipse (default is 1).

- Example

```python
img.draw_ellipse(60, 60, 30, 20, color=(0, 0, 255), thickness=3)  # 绘制蓝色椭圆
```

### draw_image

The `draw_image` function can draw another image on the current image.

- Syntax

```python
image.draw_image(img, x, y, alpha=128, scale=1.0)
```

- Parameter Explanation

  - `img`: The image object to be drawn.
  - `x, y`: Upper-left corner coordinates of the drawing position.
  - `alpha`: Transparency (0-256).
  - `scale`: Scale ratio (default is 1.0).

- Example

```python
  overlay = image.Image("overlay.bmp")
  img.draw_image(overlay, 10, 10, alpha=128, scale=1.0)  # 在(10, 10)位置绘制 overlay.bmp
```

### draw_keypoints

The `draw_keypoints` function can draw keypoints on an image.

- Syntax

```python
image.draw_keypoints(keypoints, size=10, color, thickness=1)
```

- Parameter Explanation

  - `keypoints`: List of keypoints, each keypoint is an (x, y) tuple.
  - `size`: Size of the keypoints (default is 10).
  - `color`: Color of the keypoints.
  - `thickness`: Border thickness of the keypoints (default is 1).

- Example

```python
keypoints = [(30, 30), (50, 50), (70, 70)]
img.draw_keypoints(keypoints, size=10, color=(255, 255, 0), thickness=2)  # 绘制黄色关键点
```

### flood_fill

The `flood_fill` function can perform a flood fill algorithm on an image, starting from the specified starting point and filling with the specified color.

- Syntax

```python
image.flood_fill(x, y, color, threshold, invert=False, clear_background=False)
```

- Parameter Explanation

  - `x, y`: Starting point coordinates.
  - `color`: Fill color.
  - `threshold`: Fill threshold, indicating the allowed color difference range between the starting pixel and adjacent pixels.
  - `invert`: Boolean value, if True, reverses the fill condition.
  - `clear_background`: Boolean value, if True, clears the background outside the fill area.

- Example

```python
img.flood_fill(30, 30, color=(255, 0, 0), threshold=30, invert=False, clear_background=False)  # 从(30, 30)开始填充红色
```

### draw_string

The `draw_string` function can draw a string on an image.

- Syntax

```python
image.draw_string(x, y, text, color, scale=1)
```

- Parameter Explanation

  - `x, y`: Starting coordinates of the string.
  - `text`: String content to be drawn.
  - `color`: Color of the string.
  - `scale`: Scale ratio of the string (default is 1).

- Example

```python
img.draw_string(10, 10, "Hello OpenMV", color=(255, 255, 255), scale=2)  # 绘制白色字符串
```

## Example

This example is for feature demonstration only

```python
import time, os, gc, sys, urandom

from media.display import *
from media.media import *

DISPLAY_IS_HDMI = False
DISPLAY_IS_LCD = True
DISPLAY_IS_IDE = False

try:
    # 设置默认大小
    width = 640
    height = 480
    if DISPLAY_IS_HDMI:
        # 使用HDMI作为显示输出，设置1080P
        Display.init(Display.LT9611, width = 1920, height = 1080, to_ide = True)
        width = 1920
        height = 1080
    elif DISPLAY_IS_LCD:
        # 使用LCD作为显示输出
        Display.init(Display.ST7701, width = 800, height = 480, to_ide = True)
        width = 800
        height = 480
    elif DISPLAY_IS_IDE:
        # 使用IDE作为显示输出
        Display.init(Display.VIRT, width = 800, height = 480, fps = 100)
        width = 800
        height = 480
    else:
        raise ValueError("Shoule select a display.")
    # 初始化媒体管理器
    MediaManager.init()

    fps = time.clock()
    # 创建绘制的图像
    img = image.Image(width, height, image.ARGB8888)

    while True:
        fps.tick()
        # 检查是否在退出点
        os.exitpoint()
        img.clear()

        # 绘制红色线
        img.draw_line(10, 10, 100, 100, color=(255, 0, 0))

        # 绘制绿色矩形
        img.draw_rectangle(20, 20, 50, 30, color=(0, 255, 0), thickness=2)

        # 绘制蓝色圆
        img.draw_circle(30, 30, 30, color=(0, 0, 255), thickness=3)

        # 绘制黄色交叉
        img.draw_cross(40, 40, color=(255, 255, 0), size=10, thickness=2)

        # 绘制红色字符串
        img.draw_string_advanced(50, 50, 32, "你好世界", color=(255, 0, 0))
        # 绘制白色字符串
        img.draw_string_advanced(50, 100, 32, "Hello CanMV", color=(255, 255, 255), scale=2)

        # 绘制红色箭头
        img.draw_arrow(60, 60, 100, 100, color=(255, 0, 0), thickness=2)

        # 绘制蓝色椭圆
        radius_x = urandom.getrandbits(30) % (max(img.height(), img.width())//2)
        radius_y = urandom.getrandbits(30) % (max(img.height(), img.width())//2)
        rot = urandom.getrandbits(30)
        img.draw_ellipse(70, 70, radius_x, radius_y, rot, color = (0, 0, 255), thickness = 2, fill = False)

        # 绘制另一个图像
        # overlay = image.Image("overlay.bmp")
        # img.draw_image(overlay, 10, 10, alpha=128, scale=1.0)

        # 绘制黄色关键点
        keypoints = [(30, 30), (50, 50), (70, 70)]
        img.draw_keypoints([(30, 40, rot)], color = (255, 255, 0), size = 20, thickness = 2, fill = False)

        # 执行洪水填充
        img.flood_fill(90, 90, color=(255, 0, 0), threshold=30, invert=False, clear_background=False)

        # 显示绘制结果
        Display.show_image(img)

        #print(fps.fps())

        time.sleep_ms(10)
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # 销毁 display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # 释放媒体缓冲区
    MediaManager.deinit()
```

```{admonition} Tip
For specific interface definitions, please refer to [image](../../api/openmv/image.md)
```
