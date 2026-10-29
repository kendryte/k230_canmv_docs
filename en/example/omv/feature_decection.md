# Feature Detection Routine Explanation

## Overview

In OpenMV, `find_hog`, `find_lines`, `find_rects`, `find_features`, and `get_regression` are some of the functions used for image processing and feature detection.

CanMV supports OpenMV algorithms and can also use these functions.

## Function Description

### find_hog

The `find_hog` function is used to detect objects in an image using HOG (Histogram of Oriented Gradients) feature descriptors. HOG is a feature description method commonly used for object detection.

- Syntax

```python
objects = img.find_hog(roi=None, threshold=0.5, min_size=(0, 0))
```

- Parameter Explanation

  - roi: Optional parameter that defines a Region of Interest. The default value is `None`, which means detection is performed on the entire image.
  - threshold: Confidence threshold. Only detection results with confidence greater than this value will be returned. The default value is `0.5`.
  - min_size: The minimum size of the detected object. Specified as a tuple of `(width, height)`. The default value is `(0, 0)`, which means there is no minimum size limit.

- Return Value

Returns a list containing the detected objects, where each object is a `Rect` object containing the position and size of the object.

### find_lines

The `find_lines` function is used to detect straight lines in an image. This function is suitable for finding long straight lines in an image.

- Syntax

```python
lines = img.find_lines(threshold=1000, theta_margin=20, rho_margin=20)
```

- Parameter Explanation

  - threshold: The minimum length of a line. The detected line must exceed this length. The default value is `1000`.
  - theta_margin: Tolerance for the angle. The unit is degrees. The default value is `20`.
  - rho_margin: Tolerance for the distance. The unit is pixels. The default value is `20`.

- Return Value

  Returns a list containing line information. Each line is a `Line` object containing the start point, end point, length, and angle of the line.

### find_rects

The `find_rects` function is used to detect rectangular regions in an image. This function can be used to find square or rectangular objects in an image.

- Syntax

```python
rects = img.find_rects(threshold=2000, margin=10)
```

- Parameter Explanation

  - threshold: The minimum area of the rectangle. The default value is `2000`.
  - margin: The margin tolerance for rectangle detection. The default value is `10`.

- Return Value

  Returns a list containing rectangle information. Each rectangle is a `Rect` object containing the coordinates and size of the rectangle.

### find_features

The `find_features` function is used to detect feature points in an image. These feature points can be used for tasks such as image matching and tracking.

- Syntax

```python
features = img.find_features(algorithm, threshold=10)
```

- Parameter Explanation

  - algorithm: The feature detection algorithm to use. Common algorithms include `image.FORBIDDEN`, `image.BRIEF`, etc.
  - threshold: The threshold for feature detection. The default value is `10`.

- Return Value

  Returns a list containing feature point information. Each feature point is a `Feature` object containing the position of the feature point and other information.

### get_regression

The `get_regression` function is used to detect regression lines from an image, i.e., straight lines that fit the data points. It is typically used to mark the trend or direction of data.

- Syntax

```python
line = img.get_regression(threshold=1000, min_length=10, max_distance=5)
```

- Parameter Explanation

  - threshold: The minimum length of the line. The default value is `1000`.
  - min_length: The minimum length of the fitted line. The default value is `10`.
  - max_distance: The maximum distance allowed from a data point to the regression line. The default value is `5`.

- Return Value

  Returns a `Line` object containing the regression line information, representing the fitted line.

### Summary

These functions are important tools in the OpenMV image processing library, each used for different vision tasks:

- `find_hog`: Detects objects based on HOG features.
- `find_lines`: Detects straight lines in an image.
- `find_rects`: Detects rectangular regions in an image.
- `find_features`: Detects feature points in an image.
- `get_regression`: Detects regression lines in an image.

## Example

Only a demo for finding line segments is listed here. For specific demos, please refer to the routines in the virtual USB drive that comes with the firmware.

```python
# 直线检测示例
#
# 这个示例展示了如何在图像中找到直线。对于在图像中找到的每个直线对象，
# 将返回一个包含该直线旋转的直线对象。

# 注意：直线检测是通过霍夫变换完成的：
# http://en.wikipedia.org/wiki/Hough_transform
# 请阅读上述链接以获取有关 `theta` 和 `rho` 的更多信息。

# find_lines() 找到的是无限长的直线。使用 find_line_segments() 可以找到非无限长的直线。
import time, os, gc, sys

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = ALIGN_UP(640, 16)
DETECT_HEIGHT = 480

# 所有的直线对象都有一个 `theta()` 方法来获取其旋转角度（以度为单位）。
# 你可以根据其旋转角度来过滤直线。

min_degree = 0
max_degree = 179

# 所有的直线对象还有 `x1()`, `y1()`, `x2()`, 和 `y2()` 方法来获取它们的端点，
# 以及一个 `line()` 方法来将上述所有值作为一个包含 4 个值的元组返回给 `draw_line()` 使用。

# 关于负的 rho 值：
#
# 一个 [theta+0:-rho] 元组与 [theta+180:+rho] 是一样的。
sensor = None

def camera_init():
    global sensor

    # 使用默认配置构造一个Sensor对象
    sensor = Sensor(width=DETECT_WIDTH,height=DETECT_HEIGHT)
    # sensor复位
    sensor.reset()
    # 设置水平镜像
    # sensor.set_hmirror(False)
    # 设置垂直翻转
    # sensor.set_vflip(False)

    # 设置通道 0 输出大小
    sensor.set_framesize(width=DETECT_WIDTH,height=DETECT_HEIGHT)
    # 设置通道 0 输出格式
    sensor.set_pixformat(Sensor.GRAYSCALE)
    # 使用 IDE 作为显示输出，如果您选择的屏幕无法点亮，请参考API文档中的k230_canmv_display_module_api_manual自行配置
    Display.init(Display.VIRT, width= DETECT_WIDTH, height = DETECT_HEIGHT,fps=100,to_ide = True)
    # 初始化媒体管理器
    MediaManager.init()
    # sensor开始运行
    sensor.run()

def camera_deinit():
    global sensor
    # sensor停止运行
    sensor.stop()
    # 销毁显示
    Display.deinit()
    # 休眠
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()

def capture_picture():

    fps = time.clock()
    while True:
        fps.tick()
        try:
            os.exitpoint()
            global sensor
            img = sensor.snapshot()

            # `threshold` 控制在图像中找到的直线数量。只有边缘差异幅度和大于 `threshold` 的直线才会被检测到。

            # 关于 `threshold` 的更多信息 - 图像中的每个像素都会为直线贡献一个幅度值。
            # 所有贡献的总和就是该直线的幅度。然后，当直线合并时，它们的幅度会被相加。
            # 注意，`threshold` 会在合并前过滤掉低幅度的直线。要查看未合并直线的幅度，请将 `theta_margin` 和 `rho_margin` 设置为 0。

            # `theta_margin` 和 `rho_margin` 控制合并相似的直线。如果两条直线的 theta 和 rho 值差异小于该边界，它们会被合并。

            for l in img.find_lines(threshold = 1000, theta_margin = 25, rho_margin = 25):
                if (min_degree <= l.theta()) and (l.theta() <= max_degree):
                    img.draw_line([v for v in l.line()], color = (255, 0, 0))
                    print(l)

            # 将结果绘制到屏幕上
            Display.show_image(img)
            img = None

            gc.collect()
            #print(fps.fps())
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

```{admonition} Tip
For specific interface definitions, please refer to [image](../../api/openmv/image.md)
```
