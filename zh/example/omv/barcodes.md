# 2. 识别条形码例程讲解

## 1. 概述

条形码（Barcode）是一种用来表示数据的视觉模式，通过使用不同宽度和间隔的条纹或图案来编码信息。条形码广泛应用于各种行业，用于自动识别、存储和管理数据。

CanMV支持OpenMV算法，支持识别条形码，相关接口为`find_barcodes`，支持多种条形码识别

## 2. 示例

本示例设置摄像头输出640x480灰度图像，使用`image.find_barcodes`来识别条形码

```{tip}
如果识别成功率低，可尝试修改摄像头输出的mirror和flip设置
以及注意条形码2边留出白色区域
```

```python
# Barcode Example
#
# This example shows off how easy it is to detect bar codes.
import time, math, os, gc, sys

from media.sensor import *
from media.display import *
from media.media import *

def barcode_name(code):
    if(code.type() == image.EAN2):
        return "EAN2"
    if(code.type() == image.EAN5):
        return "EAN5"
    if(code.type() == image.EAN8):
        return "EAN8"
    if(code.type() == image.UPCE):
        return "UPCE"
    if(code.type() == image.ISBN10):
        return "ISBN10"
    if(code.type() == image.UPCA):
        return "UPCA"
    if(code.type() == image.EAN13):
        return "EAN13"
    if(code.type() == image.ISBN13):
        return "ISBN13"
    if(code.type() == image.I25):
        return "I25"
    if(code.type() == image.DATABAR):
        return "DATABAR"
    if(code.type() == image.DATABAR_EXP):
        return "DATABAR_EXP"
    if(code.type() == image.CODABAR):
        return "CODABAR"
    if(code.type() == image.CODE39):
        return "CODE39"
    if(code.type() == image.PDF417):
        return "PDF417"
    if(code.type() == image.CODE93):
        return "CODE93"
    if(code.type() == image.CODE128):
        return "CODE128"

DETECT_WIDTH = 640
DETECT_HEIGHT = 480

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
    sensor.set_pixformat(Sensor.GRAYSCALE)

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

        for code in img.find_barcodes():
            img.draw_rectangle([v for v in code.rect()], color=(255, 0, 0))
            print_args = (barcode_name(code), code.payload(), (180 * code.rotation()) / math.pi, code.quality(), fps.fps())
            print("Barcode %s, Payload \"%s\", rotation %f (degrees), quality %d, FPS %f" % print_args)

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
具体接口定义请参考 [find_barcodes](../../api/openmv/image.md#2284-find_barcodes)
```
