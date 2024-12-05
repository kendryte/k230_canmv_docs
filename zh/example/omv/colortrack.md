# 6. 颜色识别(find_blobs)例程讲解

## 1. 概述

`find_blobs` 是 OpenMV 的图像处理函数，用于在图像中寻找并识别“斑点”（blobs）。这些斑点是指图像中具有相似颜色或亮度的区域。这个函数通常用于视觉检测和识别应用中，例如物体跟踪、颜色识别等。

CanMV支持OpenMV算法，同样可以使用`find_blobs`

## 2. 函数讲解

### 2.1 基本用法

```python
blobs = img.find_blobs([thresholds], area_threshold=area_threshold, pixels_threshold=pixels_threshold, merge=True, margin=0)
```

### 2.2 参数解释

- thresholds: 这是一个包含颜色范围的列表，用于定义要查找的斑点的颜色范围。通常是一个包含两个或三个元素的元组。例如，`(100, 200, -64, 127, -128, 127)` 表示 HSV 颜色空间中的范围，其中第一个和第二个值是 Hue，第三和第四值是 Saturation，最后两个值是 Value。

- area_threshold: 斑点的面积阈值。只有面积大于这个值的斑点才会被返回。默认值是 0。

- pixels_threshold: 斑点的像素数阈值。只有包含的像素数大于这个值的斑点才会被返回。默认值是 0。

- merge: 是否合并相邻的斑点。设为 `True` 时，相邻的斑点会被合并成一个大斑点；设为 `False` 时，斑点不会合并。默认值是 `True`。

- margin: 用于合并斑点时的边距。设置为一个正整数，表示合并斑点时的最大距离。默认值是 0。

### 2.3 返回值

`find_blobs` 函数返回一个包含斑点信息的列表。每个斑点都是一个 `Blob` 对象，通常包含以下属性：

- `cx` 和 `cy`：斑点的中心坐标。
- `x` 和 `y`：斑点的左上角坐标。
- `w` 和 `h`：斑点的宽度和高度。
- `area`：斑点的面积（像素数）。

## 3. 示例

这里只列举一个单独的颜色追踪例子，具体demo还请查看固件自带虚拟U盘中的例程

```python
# 单色代码跟踪示例
#
# 这个示例展示了使用 CanMV 相机进行单色代码跟踪。
#
# 颜色代码是由两种或更多颜色组成的斑点。下面的示例将
# 仅跟踪包含以下颜色的彩色物体。
import time, os, gc, sys, math

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = 640
DETECT_HEIGHT = 480

# 颜色跟踪阈值 (L Min, L Max, A Min, A Max, B Min, B Max)
# 以下阈值通常用于跟踪红色/绿色物体。您可能需要调整它们...
thresholds = [(12, 100, -47, 14, -1, 58), # 通用红色阈值 -> 索引为 0，所以代码 == (1 << 0)
              (30, 100, -64, -8, -32, 32)] # 通用绿色阈值 -> 索引为 1，所以代码 == (1 << 1)
# 当 "merge=True" 时，代码会被“或”在一起以进行 "find_blobs"

# 只有那些像素数量超过 "pixel_threshold" 且面积超过 "area_threshold" 的斑点
# 才会被下面的 "find_blobs" 返回。如果更改相机分辨率，请更改 "pixel_threshold" 和 "area_threshold"。
# 必须设置 "merge=True" 以合并重叠的颜色斑点以形成颜色代码。

sensor = None

try:
    # 使用默认配置构造一个Sensor对象
    sensor = Sensor(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # sensor复位
    sensor.reset()
    # 设置水平镜像
    # sensor.set_hmirror(False)
    # 设置垂直翻转
    # sensor.set_vflip(False)
    # 设置通道 0 输出大小
    sensor.set_framesize(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # 设置通道 0 输出格式
    sensor.set_pixformat(Sensor.RGB565)

    # 设置显示，如果您选择的屏幕无法点亮，请参考API文档中的K230_CanMV_Display模块API手册自行配置,下面给出四种显示方式
    # 使用 HDMI 作为显示输出，设置为 VGA
    # Display.init(Display.LT9611, width = 640, height = 480, to_ide = True)

    # 使用 HDMI 作为显示输出，设置为 1080P
    # Display.init(Display.LT9611, width = 1920, height = 1080, to_ide = True)

    # 使用 LCD 作为显示输出
    # Display.init(Display.ST7701, to_ide = True)

    # 使用 IDE 作为输出
    Display.init(Display.VIRT, width = DETECT_WIDTH, height = DETECT_HEIGHT, fps = 100)

    # 初始化媒体管理器
    MediaManager.init()
    # sensor开始运行
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()

        # 检查是否应该退出
        os.exitpoint()
        img = sensor.snapshot()

        for blob in img.find_blobs(thresholds, pixels_threshold=100, area_threshold=100, merge=True):
            if blob.code() == 3: # r/g 代码 == (1 << 1) | (1 << 0)
                # 这些值依赖于斑点不是圆形的 - 否则它们会不稳定
                # if blob.elongation() > 0.5:
                #     img.draw_edges(blob.min_corners(), color=(255,0,0))
                #     img.draw_line(blob.major_axis_line(), color=(0,255,0))
                #     img.draw_line(blob.minor_axis_line(), color=(0,0,255))
                # 这些值在任何时候都是稳定的
                img.draw_rectangle([v for v in blob.rect()])
                img.draw_cross(blob.cx(), blob.cy())
                # 注意 - 斑点的旋转是唯一的，仅限于 0-180
                img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)

        # 将结果绘制到屏幕上
        Display.show_image(img)
        gc.collect()

        print(fps.fps())
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # sensor停止运行
    if isinstance(sensor, Sensor):
        sensor.stop()
    # 销毁display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # 释放媒体缓冲区
    MediaManager.deinit()
```

```{admonition} 提示
具体接口定义请参考 [find_blobs](../../api/openmv/image.md#2276-find_blobs)
```
