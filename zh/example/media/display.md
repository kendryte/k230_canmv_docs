# Display 示例讲解

## 概述

K230 配备 1 路 MIPI-DSI（1x4 lane），可驱动 MIPI 屏幕或通过接口芯片转换驱动 HDMI 显示器。此外，为了方便调试，我们还支持虚拟显示器，用户可以选择 `VIRT` 输出设备，即使没有 HDMI 显示器或 LCD 屏幕, 也可在 CanMV-IDE 中进行图像预览。

## 示例

### 使用 HDMI 输出图像

本示例列出当前固件支持的显示模式，选择 LT9611 HDMI 的默认模式，并根据实际显示尺寸创建图像。

```{note}
在使用较大分辨率并开启 `to_ide=True` 将画面传输到 IDE 预览时，画面偶尔会出现闪烁。这是已知问题，我们将在后续版本中修复。
```

```python
import time
import os
import urandom
import sys

from media.display import *
from media.media import *

DISPLAY_TYPE = Display.LT9611

def display_test():
    print("display test")

    print("Available display modes:")
    for mode in Display.list_modes():
        print(mode)

    # 从上面显示的 Display.<TYPE> 值中选择一个
    Display.init(DISPLAY_TYPE, to_ide=True)
    # 初始化媒体管理器
    MediaManager.init()

    try:
        # 根据初始化后的显示尺寸创建用于绘图的图像
        img = image.Image(Display.width(), Display.height(), image.ARGB8888)

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

本示例列出当前固件支持的显示模式，并初始化 ST7701 LCD 的默认模式。如需使用其他 LCD，请将 `DISPLAY_TYPE` 修改为列表中对应的 `Display.<TYPE>` 常量。如需选择非默认模式，请将列表中的 `width`、`height` 和 `fps` 值传给 `Display.init`。

```python
import time
import os
import urandom
import sys

from media.display import *
from media.media import *

DISPLAY_TYPE = Display.ST7701

def display_test():
    print("display test")

    print("Available display modes:")
    for mode in Display.list_modes():
        print(mode)

    # 从上面显示的 Display.<TYPE> 值中选择一个
    Display.init(DISPLAY_TYPE, to_ide=True)
    # 初始化媒体管理器
    MediaManager.init()

    try:
        # 根据初始化后的显示尺寸创建用于绘图的图像
        img = image.Image(Display.width(), Display.height(), image.ARGB8888)

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
有关 Display 模块的详细接口、支持的面板类型和参数，请参考 [API 文档](../../api/mpp/k230_canmv_display_module_api_manual.md)。
```
