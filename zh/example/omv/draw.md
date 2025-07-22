# 常用图像绘制例程讲解

## 概述

OpenMV 是一个小型嵌入式机器视觉模块，广泛用于快速开发计算机视觉应用。OpenMV 的图像绘制方法可以用于在图像上绘制各种形状和文字，以便进行视觉反馈和调试。

CanMV支持OpenMV 图像绘制方法，并增加了一些，如绘制中文字符串的[draw_string_advanced](../../api/openmv/image.md#129-draw_string_advanced)

## 常用函数

### draw_string_advanced

`draw_string_advanced` 函数使用freetype渲染文字，支持中文，用户也可指定字体

- 语法

```python
image.draw_string_advanced(x,y,char_size,str,[color, font])
```

- 参数解释

  - `x, y`起点坐标。
  - `char_size`:字符大小
  - `str`:需要绘制的中文字符
  - `color`：字的颜色。
  - `font`： 字体文件路径

- 示例

```python
img.draw_string_advanced(10, 10, 32, "你好世界", color=(255, 0, 0))  # 绘制红色线
```

### draw_line

`draw_line` 函数可实现在图像上绘制一条线。

- 语法

```python
image.draw_line(x0, y0, x1, y1, color)
```

- 参数解释

  - `x0, y0`：起点坐标。
  - `x1, y1`：终点坐标。
  - `color`：线的颜色。

- 示例

```python
img.draw_line(10, 10, 100, 100, color=(255, 0, 0))  # 绘制红色线
```

### draw_rectangle

`draw_rectangle` 函数可实现在图像上绘制一个矩形。

- 语法

```python
image.draw_rectangle(x, y, w, h, color, thickness=1)
```

- 参数解释

  - `x, y`：矩形的左上角坐标。
  - `w, h`：矩形的宽度和高度。
  - `color`：矩形的颜色。
  - `thickness`：矩形边框的厚度（默认为1）。

- 示例

```python
img.draw_rectangle(20, 20, 50, 30, color=(0, 255, 0), thickness=2)  # 绘制绿色矩形
```

### draw_circle

`draw_circle`函数可实现在图像上绘制一个圆。

- 语法

```python
image.draw_circle(x, y, r, color, thickness=1)
```

- 参数解释

  - `x, y`：圆心坐标。
  - `r`：圆的半径。
  - `color`：圆的颜色。
  - `thickness`：圆边框的厚度（默认为1）。

- 示例

```python
    img.draw_circle(60, 60, 30, color=(0, 0, 255), thickness=3)  # 绘制蓝色圆

```

### draw_cross

`draw_cross`函数可实现在图像上绘制一个十字交叉。

- 语法

```python
image.draw_cross(x, y, color, size=5, thickness=1)
```

- 参数解释

  - `x, y`：交叉点坐标。
  - `color`：交叉的颜色。
  - `size`：交叉的大小（默认为5）。
  - `thickness`：交叉线条的厚度（默认为1）。

- 示例

```python
    img.draw_cross(40, 40, color=(255, 255, 0), size=10, thickness=2)  # 绘制黄色交叉

```

### draw_arrow

`draw_arrow`函数可实现在图像上绘制一条箭头线。

- 语法

```python
image.draw_arrow(x0, y0, x1, y1, color, thickness=1)
```

- 参数解释

  - `x0, y0`：起点坐标。
  - `x1, y1`：终点坐标。
  - `color`：箭头的颜色。
  - `thickness`：箭头线条的厚度（默认为1）。

- 示例

```python
img.draw_arrow(10, 10, 100, 100, color=(255, 0, 0), thickness=2)  # 绘制红色箭头
```

### draw_ellipse

`draw_ellipse`函数可实现在图像上绘制一个椭圆。

- 语法

```python
image.draw_ellipse(cx, cy, rx, ry, color, thickness=1)
```

- 参数解释

  - `cx, cy`：椭圆中心的坐标。
  - `rx, ry`：椭圆的半径（x轴和y轴方向）。
  - `color`：椭圆的颜色。
  - `thickness`：椭圆边框的厚度（默认为1）。

- 示例

```python
img.draw_ellipse(60, 60, 30, 20, color=(0, 0, 255), thickness=3)  # 绘制蓝色椭圆
```

### draw_image

`draw_image`函数可实现在当前图像上绘制另一个图像。

- 语法

```python
image.draw_image(img, x, y, alpha=128, scale=1.0)
```

- 参数解释

  - `img`：要绘制的图像对象。
  - `x, y`：绘制位置的左上角坐标。
  - `alpha`：透明度（0-256）。
  - `scale`：缩放比例（默认为1.0）。

- 示例

```python
  overlay = image.Image("overlay.bmp")
  img.draw_image(overlay, 10, 10, alpha=128, scale=1.0)  # 在(10, 10)位置绘制 overlay.bmp
```

### draw_keypoints

`draw_keypoints`函数可实现在图像上绘制关键点。

- 语法

```python
image.draw_keypoints(keypoints, size=10, color, thickness=1)
```

- 参数解释

  - `keypoints`：关键点列表，每个关键点是一个(x, y)元组。
  - `size`：关键点的大小（默认为10）。
  - `color`：关键点的颜色。
  - `thickness`：关键点边框的厚度（默认为1）。

- 示例

```python
keypoints = [(30, 30), (50, 50), (70, 70)]
img.draw_keypoints(keypoints, size=10, color=(255, 255, 0), thickness=2)  # 绘制黄色关键点
```

### flood_fill

`flood_fill`函数可实现在图像上执行洪水填充算法，从指定的起点开始填充指定的颜色。

- 语法

```python
image.flood_fill(x, y, color, threshold, invert=False, clear_background=False)
```

- 参数解释

  - `x, y`：起点坐标。
  - `color`：填充的颜色。
  - `threshold`：填充阈值，表示起点像素与相邻像素颜色的允许差异范围。
  - `invert`：布尔值，如果为 True，则反转填充条件。
  - `clear_background`：布尔值，如果为 True，则清除填充区域以外的背景。

- 示例

```python
img.flood_fill(30, 30, color=(255, 0, 0), threshold=30, invert=False, clear_background=False)  # 从(30, 30)开始填充红色
```

### draw_string

`draw_string`函数可实现在图像上绘制字符串。

- 语法

```python
image.draw_string(x, y, text, color, scale=1)
```

- 参数解释

  - `x, y`：字符串的起始坐标。
  - `text`：要绘制的字符串内容。
  - `color`：字符串的颜色。
  - `scale`：字符串的缩放比例（默认为1）。

- 示例

```python
img.draw_string(10, 10, "Hello OpenMV", color=(255, 255, 255), scale=2)  # 绘制白色字符串
```

## 示例

本示例仅做功能展示

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

```{admonition} 提示
具体接口定义请参考 [image](../../api/openmv/image.md)
```
