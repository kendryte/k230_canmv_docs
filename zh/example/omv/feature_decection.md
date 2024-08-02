# 7. 特征值检测例程讲解

## 1. 概述

在 OpenMV 中，`find_hog`、`find_lines`、`find_rects`、`find_features` 和 `get_regression` 是一些用于图像处理和特征检测的函数。

CanMV支持OpenMV算法，同样可以使用这些函数

## 2. 函数说明

### 2.1 find_hog

`find_hog` 函数用于在图像中检测使用 HOG (Histogram of Oriented Gradients) 特征描述符的物体。HOG 是一种常用于对象检测的特征描述方法。

- 语法

```python
objects = img.find_hog(roi=None, threshold=0.5, min_size=(0, 0))
```

- 参数解释

  - roi: 可选参数，定义了一个感兴趣区域 (Region of Interest)。默认值为 `None`，表示在整个图像上进行检测。
  - threshold: 置信度阈值。只有置信度大于这个值的检测结果才会被返回。默认值是 `0.5`。
  - min_size: 最小检测对象的大小。指定为 `(width, height)` 的元组。默认值是 `(0, 0)`，表示没有最小大小限制。

- 返回值

返回一个包含检测到的对象的列表，每个对象是一个 `Rect` 对象，包含了对象的位置和大小。

### 2.2 find_lines

`find_lines` 函数用于在图像中检测直线。该函数适用于寻找图像中的长直线。

- 语法

```python
lines = img.find_lines(threshold=1000, theta_margin=20, rho_margin=20)
```

- 参数解释

  - threshold: 直线的最小长度。检测到的直线必须超过这个长度。默认值是 `1000`。
  - theta_margin: 角度的容忍度。单位是度。默认值是 `20`。
  - rho_margin: 距离的容忍度。单位是像素。默认值是 `20`。

- 返回值

  返回一个包含直线信息的列表。每条直线是一个 `Line` 对象，包含了直线的起点、终点、长度和角度。

### 2.3 find_rects

`find_rects` 函数用于检测图像中的矩形区域。这个函数可以用于找到图像中的方形或矩形物体。

- 语法

```python
rects = img.find_rects(threshold=2000, margin=10)
```

- 参数解释

  - threshold: 矩形的最小面积。默认值是 `2000`。
  - margin: 矩形检测的边距容忍度。默认值是 `10`。

- 返回值

  返回一个包含矩形信息的列表。每个矩形是一个 `Rect` 对象，包含矩形的坐标和大小。

### 2.4 find_features

`find_features` 函数用于检测图像中的特征点。这些特征点可以用于图像匹配、跟踪等任务。

- 语法

```python
features = img.find_features(algorithm, threshold=10)
```

- 参数解释

  - algorithm: 要使用的特征检测算法。常见的算法包括 `image.FORBIDDEN`、`image.BRIEF` 等。
  - threshold: 特征检测的阈值。默认值是 `10`。

- 返回值

  返回一个包含特征点信息的列表。每个特征点是一个 `Feature` 对象，包含了特征点的位置和其他信息。

### 2.5 get_regression

`get_regression` 函数用于从图像中检测回归线，即拟合数据点的直线。通常用于标记数据的趋势或方向。

- 语法

```python
line = img.get_regression(threshold=1000, min_length=10, max_distance=5)
```

- 参数解释

  - threshold:直线的最小长度。默认值是 `1000`。
  - min_length: 拟合线的最小长度。默认值是 `10`。
  - max_distance: 允许的数据点到回归线的最大距离。默认值是 `5`。

- 返回值

  返回一个包含回归线信息的 `Line` 对象，表示拟合的直线。

### 2.6 总结

这些函数是 OpenMV 图像处理库中的重要工具，分别用于不同的视觉任务：

- `find_hog`: 基于 HOG 特征检测物体。
- `find_lines`: 检测图像中的直线。
- `find_rects`: 检测图像中的矩形区域。
- `find_features`: 检测图像中的特征点。
- `get_regression`: 检测图像中的回归线。

## 3. 示例

这里只列举一个寻找线段的demo，具体demo还请查看固件自带虚拟U盘中的例程

```python
# Find Lines Example
#
# This example shows off how to find lines in the image. For each line object
# found in the image a line object is returned which includes the line's rotation.

# Note: Line detection is done by using the Hough Transform:
# http://en.wikipedia.org/wiki/Hough_transform
# Please read about it above for more information on what `theta` and `rho` are.

# find_lines() finds infinite length lines. Use find_line_segments() to find non-infinite lines.
import time, os, gc, sys

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = ALIGN_UP(640, 16)
DETECT_HEIGHT = 480

# All line objects have a `theta()` method to get their rotation angle in degrees.
# You can filter lines based on their rotation angle.

min_degree = 0
max_degree = 179

# All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points
# and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

# About negative rho values:
#
# A [theta+0:-rho] tuple is the same as [theta+180:+rho].
sensor = None

def camera_init():
    global sensor

    # construct a Sensor object with default configure
    sensor = Sensor(width=DETECT_WIDTH,height=DETECT_HEIGHT)
    # sensor reset
    sensor.reset()
    # set hmirror
    # sensor.set_hmirror(False)
    # sensor vflip
    # sensor.set_vflip(False)

    # set chn0 output size
    sensor.set_framesize(width=DETECT_WIDTH,height=DETECT_HEIGHT)
    # set chn0 output format
    sensor.set_pixformat(Sensor.GRAYSCALE)
    # use IDE as display output
    Display.init(Display.VIRT, width= DETECT_WIDTH, height = DETECT_HEIGHT,fps=100,to_ide = True)
    # init media manager
    MediaManager.init()
    # sensor start run
    sensor.run()

def camera_deinit():
    global sensor
    # sensor stop run
    sensor.stop()
    # deinit display
    Display.deinit()
    # sleep
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()

def capture_picture():

    fps = time.clock()
    while True:
        fps.tick()
        try:
            os.exitpoint()
            global sensor
            img = sensor.snapshot()

            # `threshold` controls how many lines in the image are found. Only lines with
            # edge difference magnitude sums greater than `threshold` are detected...

            # More about `threshold` - each pixel in the image contributes a magnitude value
            # to a line. The sum of all contributions is the magintude for that line. Then
            # when lines are merged their magnitudes are added togheter. Note that `threshold`
            # filters out lines with low magnitudes before merging. To see the magnitude of
            # un-merged lines set `theta_margin` and `rho_margin` to 0...

            # `theta_margin` and `rho_margin` control merging similar lines. If two lines
            # theta and rho value differences are less than the margins then they are merged.

            for l in img.find_lines(threshold = 1000, theta_margin = 25, rho_margin = 25):
                if (min_degree <= l.theta()) and (l.theta() <= max_degree):
                    img.draw_line([v for v in l.line()], color = (255, 0, 0))
                    print(l)

            # draw result to screen
            Display.show_image(img)
            img = None

            gc.collect()
            print(fps.fps())
        except KeyboardInterrupt as e:
            print("user stop: ", e)
            break
        except BaseException as e:
            print(f"Exception {e}")
            break

def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    camera_is_init = False
    try:
        print("camera init")
        camera_init()
        camera_is_init = True
        print("camera capture")
        capture_picture()
    except Exception as e:
        print(f"Exception {e}")
    finally:
        if camera_is_init:
            print("camera deinit")
            camera_deinit()

if __name__ == "__main__":
    main()

```

```{admonition} 提示
具体接口定义请参考 [image](../../api/openmv/image.md)
```
