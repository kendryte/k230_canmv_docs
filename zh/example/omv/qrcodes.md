# 1. 识别二维码例程讲解

## 1. 概述

CanMV 支持 OpenMV 算法，可以识别二维码。相关接口为 `find_qrcodes`。

## 2. 示例

本示例设置摄像头输出为 640x480 的灰度图像，并使用 `image.find_qrcodes` 来识别二维码。

```{tip}
如果识别成功率低，可尝试调整摄像头的镜像和翻转设置。
```

```python
# QR 码示例
import time
import os
import gc
import sys

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = 640
DETECT_HEIGHT = 480

sensor = None

try:
    # 使用默认配置构造 Sensor 对象
    sensor = Sensor(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    # 重置 sensor
    sensor.reset()
    # 设置水平镜像
    # sensor.set_hmirror(False)
    # 设置垂直翻转
    # sensor.set_vflip(False)
    # 设置输出大小
    sensor.set_framesize(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    # 设置输出格式
    sensor.set_pixformat(Sensor.GRAYSCALE)

    # 初始化显示，如果选择的屏幕无法点亮，请参考 API 文档中的 K230_CanMV_Display 模块 API 手册进行配置
    # 使用 HDMI 输出，设置为 VGA
    # Display.init(Display.LT9611, width=640, height=480, to_ide=True)

    # 使用 HDMI 输出，设置为 1080P
    # Display.init(Display.LT9611, width=1920, height=1080, to_ide=True)

    # 使用 LCD 输出
    # Display.init(Display.ST7701, to_ide=True)

    # 使用 IDE 输出
    Display.init(Display.VIRT, width=DETECT_WIDTH, height=DETECT_HEIGHT, fps=100)

    # 初始化媒体管理器
    MediaManager.init()
    # 启动 sensor
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()

        # 检查是否应该退出
        os.exitpoint()
        img = sensor.snapshot()

        for code in img.find_qrcodes():
            rect = code.rect()
            img.draw_rectangle([v for v in rect], color=(255, 0, 0), thickness=5)
            img.draw_string_advanced(rect[0], rect[1], 32, code.payload())
            print(code)

        # 将结果绘制到屏幕上
        Display.show_image(img)
        gc.collect()

        # print(fps.fps())
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # 停止 sensor
    if isinstance(sensor, Sensor):
        sensor.stop()
    # 取消初始化显示
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # 释放媒体缓冲区
    MediaManager.deinit()
```

```{admonition} 提示
具体接口定义请参考 [find_qrcodes](../../api/openmv/image.md#2281-find_qrcodes)。
```
