# 2. Display例程讲解

## 1. 概述

K230有1路MIPI-DSI(1x4lane),可驱动mipi屏幕或者通过接口芯片转接驱动HDMI显示器

同时，为了方便调试，我们还添加了虚拟显示器支持，用户如果没有HDMI显示器和LCD屏幕是，也可通过选择`VIRT`输出设备，在CanMV-IDE中进行图像预览

## 2. 示例

### 2.1 使用HDMI输出图像

驱动HDMI显示屏输出1080P图像

```python
import time, os, urandom, sys

from media.display import *
from media.media import *

DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

def display_test():
    print("display test")

    # create image for drawing
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    # use hdmi as display output
    Display.init(Display.LT9611, to_ide = True)
    # init media manager
    MediaManager.init()

    try:
        while True:
            img.clear()
            for i in range(10):
                x = (urandom.getrandbits(11) % img.width())
                y = (urandom.getrandbits(11) % img.height())
                r = (urandom.getrandbits(8))
                g = (urandom.getrandbits(8))
                b = (urandom.getrandbits(8))
                size = (urandom.getrandbits(30) % 64) + 32
                # If the first argument is a scaler then this method expects
                # to see x, y, and text. Otherwise, it expects a (x,y,text) tuple.
                # Character and string rotation can be done at 0, 90, 180, 270, and etc. degrees.
                img.draw_string_advanced(x,y,size, "Hello World!，你好世界！！！", color = (r, g, b),)

            # draw result to screen
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        print(f"Exception {e}")

    # deinit display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()
```

### 2.2 使用LCD输出图像

通过LCD（ST7701）输出800x480图像

```python
import time, os, urandom, sys

from media.display import *
from media.media import *

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

def display_test():
    print("display test")

    # create image for drawing
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    # use lcd as display output
    Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)
    # init media manager
    MediaManager.init()

    try:
        while True:
            img.clear()
            for i in range(10):
                x = (urandom.getrandbits(11) % img.width())
                y = (urandom.getrandbits(11) % img.height())
                r = (urandom.getrandbits(8))
                g = (urandom.getrandbits(8))
                b = (urandom.getrandbits(8))
                size = (urandom.getrandbits(30) % 64) + 32
                # If the first argument is a scaler then this method expects
                # to see x, y, and text. Otherwise, it expects a (x,y,text) tuple.
                # Character and string rotation can be done at 0, 90, 180, 270, and etc. degrees.
                img.draw_string_advanced(x,y,size, "Hello World!，你好世界！！！", color = (r, g, b),)

            # draw result to screen
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        print(f"Exception {e}")

    # deinit display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()
```

### 2.3 使用VIRT调试预览图像

使用虚拟显示输出设备，用户可自定义分辨了和帧率，方便使用CanMV-IDE调试使用

```python
import time, os, urandom, sys

from media.display import *
from media.media import *

DISPLAY_WIDTH = ALIGN_UP(640, 16)
DISPLAY_HEIGHT = 480

def display_test():
    print("display test")

    # create image for drawing
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    # use lcd as display output
    Display.init(Display.VIRT, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, fps = 60)
    # init media manager
    MediaManager.init()

    try:
        while True:
            img.clear()
            for i in range(10):
                x = (urandom.getrandbits(11) % img.width())
                y = (urandom.getrandbits(11) % img.height())
                r = (urandom.getrandbits(8))
                g = (urandom.getrandbits(8))
                b = (urandom.getrandbits(8))
                size = (urandom.getrandbits(30) % 64) + 32
                # If the first argument is a scaler then this method expects
                # to see x, y, and text. Otherwise, it expects a (x,y,text) tuple.
                # Character and string rotation can be done at 0, 90, 180, 270, and etc. degrees.
                img.draw_string_advanced(x,y,size, "Hello World!，你好世界！！！", color = (r, g, b),)

            # draw result to screen
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        print(f"Exception {e}")

    # deinit display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()
```

```{admonition} 提示
Display模块具体接口请参考[API文档](../../api/mpp/K230_CanMV_Display模块API手册.md)
```
