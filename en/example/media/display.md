# Display Example Explanation

## Overview

The K230 is equipped with one MIPI-DSI (1x4 lane) interface, which can drive a MIPI screen or convert to drive an HDMI monitor through an interface chip. Additionally, for convenience during debugging, we also support a virtual display. Users can choose the `VIRT` output device to preview images in CanMV-IDE even without an HDMI monitor or LCD screen.

## Examples

### Using HDMI to Output Images

This example outputs a 1080P image via an HDMI display.

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

    # Create an image for drawing
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # Use HDMI as the display output
    Display.init(Display.LT9611, to_ide=True)
    # Initialize the media manager
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
                # Draw text at the coordinates on the image
                img.draw_string_advanced(x, y, size, "Hello World! 你好世界 ！！！", color=(r, g, b))

            # Display the result on the screen
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("User stopped: ", e)
    except BaseException as e:
        print(f"Exception: {e}")

    # Destroy the display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # Release the media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()
```

### Using LCD to Output Images

This example outputs an 800x480 image via an LCD (ST7701).

```python
import time
import os
import urandom
import sys

from media.display import *
from media.media import *

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

def display_test():
    print("display test")

    # Create an image for drawing
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    # Use LCD as the display output
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    # Initialize the media manager
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
                # Draw text at the coordinates on the image
                img.draw_string_advanced(x, y, size, "Hello World! 你好世界 ！！！", color=(r, g, b))

            # Display the drawn image
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("User stopped: ", e)
    except BaseException as e:
        print(f"Exception: {e}")

    # Destroy the display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # Release the media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()
```

### Using VIRT to Debug and Preview Images

This example uses a virtual display output device, allowing users to customize resolution and frame rate for debugging in CanMV-IDE.

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

    # Create an image for drawing
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    # Use IDE as the output display, allowing any resolution to be set
    Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=60)
    # Initialize the media manager
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
                # Draw text at the coordinates on the image
                img.draw_string_advanced(x, y, size, "Hello World! 你好世界 ！！！", color=(r, g, b))

            # Display the drawn image
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("User stopped: ", e)
    except BaseException as e:
        print(f"Exception: {e}")

    # Destroy the display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # Release the media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()
```

```{admonition} Tip
For detailed interfaces of the Display module, please refer to the [API documentation](../../api/mpp/K230_CanMV_Display_Module_API_Manual.md).
```
