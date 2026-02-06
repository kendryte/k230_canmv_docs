# Display 示例讲解

## 概述

K230 配备 1 路 MIPI-DSI（1x4 lane），可驱动 MIPI 屏幕或通过接口芯片转换驱动 HDMI 显示器。此外，为了方便调试，我们还支持虚拟显示器，用户可以选择 `VIRT` 输出设备，即使没有 HDMI 显示器或 LCD 屏幕, 也可在 CanMV-IDE 中进行图像预览。

如需增加自定义屏幕，可参考[Display Debugger](./how_to_add_new_mipi_panel.md)

## 示例

### 使用 HDMI 输出图像

本示例通过 HDMI 显示屏输出 1080P 图像。

```python
import time
import os
import urandom
import sys

from media.display import *
from media.media import *

DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

def display_test():
    print("display test")

    # 创建用于绘图的图像
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 使用 HDMI 作为显示输出
    Display.init(Display.LT9611, to_ide=True)
    # 初始化媒体管理器
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
                # 在图像的坐标点绘制文字
                img.draw_string_advanced(x, y, size, "Hello World!，你好世界！！！", color=(r, g, b))

            # 将结果绘制到屏幕上
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("用户停止: ", e)
    except BaseException as e:
        print(f"异常: {e}")

    # 销毁显示
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()
```

### 使用 LCD 输出图像

本示例通过 LCD（ST7701）输出 800x480 图像。你也可以选择其他支持的面板类型（如 NT35516、GC9503 等），只需更换 `Display.ST7701` 为对应类型，并设置合适的分辨率。

```python
import time
import os
import urandom
import sys

from media.display import *
from media.media import *

# 支持的面板类型示例：Display.ST7701, Display.NT35516, Display.GC9503, Display.AML020T, 等
DISPLAY_TYPE = Display.ST7701
DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

def display_test():
    print("display test")

    # 创建用于绘图的图像
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    # 使用 LCD 作为显示输出
    Display.init(DISPLAY_TYPE, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    # 初始化媒体管理器
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
                # 在图像的坐标点绘制文字
                img.draw_string_advanced(x, y, size, "Hello World!，你好世界！！！", color=(r, g, b))

            # 将绘制的图像显示
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("用户停止: ", e)
    except BaseException as e:
        print(f"异常: {e}")

    # 销毁显示
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()
```

### 使用 VIRT 调试预览图像

本示例使用虚拟显示输出设备，用户可以自定义分辨率和帧率，以便在 CanMV-IDE 中进行调试。

```python
import time
import os
import urandom
import sys

from media.display import *
from media.media import *

DISPLAY_WIDTH = ALIGN_UP(640, 16)
DISPLAY_HEIGHT = 480

def display_test():
    print("display test")

    # 创建用于绘制的图像
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    # 使用 IDE 作为输出显示，可以设定任意分辨率和帧率
    Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=60)
    # 初始化媒体管理器
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
                # 在图像的坐标点绘制文字
                img.draw_string_advanced(x, y, size, "Hello World!，你好世界！！！", color=(r, g, b))

            # 将绘制的图像显示
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("用户停止: ", e)
    except BaseException as e:
        print(f"异常: {e}")

    # 销毁显示
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()
```

```{admonition} 提示
有关 Display 模块的详细接口、支持的面板类型和参数，请参考 [API 文档](../../api/mpp/K230_CanMV_Display模块API手册.md)。
```
