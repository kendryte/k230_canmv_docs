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
    # 使用 IDE 作为显示输出，如果您选择的屏幕无法点亮，请参考API文档中的K230_CanMV_Display模块API手册自行配置
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

```{admonition} 提示
具体接口定义请参考 [image](../../api/openmv/image.md)
```
