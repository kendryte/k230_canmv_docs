# Display Example Explanation

## Overview

K230 is equipped with 1 MIPI-DSI channel (1x4 lane), which can drive a MIPI screen or drive an HDMI display through an interface chip conversion. In addition, for debugging convenience, we also support a virtual display. Users can select the `VIRT` output device, and even without an HDMI display or LCD screen, image preview can still be performed in CanMV-IDE.

## Examples

### Output Image Using HDMI

This example lists the display modes supported by the current firmware, selects the default mode of LT9611 HDMI, and creates an image based on the actual display size.

```{note}
When using a larger resolution and enabling `to_ide=True` to transfer the image to the IDE for preview, the image occasionally flickers. This is a known issue and will be fixed in subsequent versions.
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

### Output Image Using LCD

This example lists the display modes supported by the current firmware and initializes the default mode of ST7701 LCD. To use other LCDs, modify `DISPLAY_TYPE` to the corresponding `Display.<TYPE>` constant in the list. To select a non-default mode, pass the `width`, `height`, and `fps` values from the list to `Display.init`.

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

### Debug and Preview Image Using VIRT

This example uses a virtual display output device. Users can customize the resolution and frame rate for debugging in CanMV-IDE.

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

```{admonition} Tip
For detailed interfaces, supported panel types, and parameters of the Display module, please refer to the [API Documentation](../../api/mpp/k230_canmv_display_module_api_manual.md).
```
