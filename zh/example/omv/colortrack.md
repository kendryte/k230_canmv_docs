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
# Single Color Code Tracking Example
#
# This example shows off single color code tracking using the CanMV Cam.
#
# A color code is a blob composed of two or more colors. The example below will
# only track colored objects which have both the colors below in them.
import time, os, gc, sys, math

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = 640
DETECT_HEIGHT = 480

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green things. You may wish to tune them...
thresholds = [(12, 100, -47, 14, -1, 58), # generic_red_thresholds -> index is 0 so code == (1 << 0)
              (30, 100, -64, -8, -32, 32)] # generic_green_thresholds -> index is 1 so code == (1 << 1)
# Codes are or'ed together when "merge=True" for "find_blobs"

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" must be set to merge overlapping color blobs for color codes.

sensor = None

try:
    # construct a Sensor object with default configure
    sensor = Sensor(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # sensor reset
    sensor.reset()
    # set hmirror
    # sensor.set_hmirror(False)
    # sensor vflip
    # sensor.set_vflip(False)
    # set chn0 output size
    sensor.set_framesize(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # set chn0 output format
    sensor.set_pixformat(Sensor.RGB565)

    # use hdmi as display output, set to VGA
    # Display.init(Display.LT9611, width = 640, height = 480, to_ide = True)

    # use hdmi as display output, set to 1080P
    # Display.init(Display.LT9611, width = 1920, height = 1080, to_ide = True)

    # use lcd as display output
    # Display.init(Display.ST7701, to_ide = True)

    # use IDE as output
    Display.init(Display.VIRT, width = DETECT_WIDTH, height = DETECT_HEIGHT, fps = 100)

    # init media manager
    MediaManager.init()
    # sensor start run
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()

        # check if should exit.
        os.exitpoint()
        img = sensor.snapshot()

        for blob in img.find_blobs(thresholds, pixels_threshold=100, area_threshold=100, merge=True):
            if blob.code() == 3: # r/g code == (1 << 1) | (1 << 0)
                # These values depend on the blob not being circular - otherwise they will be shaky.
                # if blob.elongation() > 0.5:
                #     img.draw_edges(blob.min_corners(), color=(255,0,0))
                #     img.draw_line(blob.major_axis_line(), color=(0,255,0))
                #     img.draw_line(blob.minor_axis_line(), color=(0,0,255))
                # These values are stable all the time.
                img.draw_rectangle([v for v in blob.rect()])
                img.draw_cross(blob.cx(), blob.cy())
                # Note - the blob rotation is unique to 0-180 only.
                img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)

        # draw result to screen
        Display.show_image(img)
        gc.collect()

        print(fps.fps())
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # sensor stop run
    if isinstance(sensor, Sensor):
        sensor.stop()
    # deinit display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # release media buffer
    MediaManager.deinit()
```

```{admonition} 提示
具体接口定义请参考 [find_blobs](../../api/openmv/image.md#2276-find_blobs)
```
