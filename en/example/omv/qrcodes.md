# QR Code Recognition Routine Explanation

## Overview

CanMV supports OpenMV algorithms and can recognize QR codes. The relevant interface is `find_qrcodes`.

## Example

This example sets the camera output to a 640x480 grayscale image and uses `image.find_qrcodes` to recognize QR codes.

```{tip}
If the recognition success rate is low, try adjusting the camera's mirror and flip settings.
```

```python
# QR Code Example
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
    # Construct Sensor object with default configuration
    sensor = Sensor(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    # Reset sensor
    sensor.reset()
    # Set horizontal mirror
    # sensor.set_hmirror(False)
    # Set vertical flip
    # sensor.set_vflip(False)
    # Set output size
    sensor.set_framesize(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    # Set output format
    sensor.set_pixformat(Sensor.GRAYSCALE)

    # Initialize display. If the selected screen cannot be lit, refer to the K230_CanMV_Display module API manual in the API documentation for configuration
    # Use HDMI output, set to VGA
    # Display.init(Display.LT9611, width=640, height=480, to_ide=True)

    # Use HDMI output, set to 1080P
    # Display.init(Display.LT9611, width=1920, height=1080, to_ide=True)

    # Use LCD output
    # Display.init(Display.ST7701, to_ide=True)

    # Use IDE output
    Display.init(Display.VIRT, width=DETECT_WIDTH, height=DETECT_HEIGHT, fps=100)

    # Initialize media manager
    MediaManager.init()
    # Start sensor
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()

        # Check if should exit
        os.exitpoint()
        img = sensor.snapshot()

        for code in img.find_qrcodes():
            rect = code.rect()
            img.draw_rectangle([v for v in rect], color=(255, 0, 0), thickness=5)
            img.draw_string_advanced(rect[0], rect[1], 32, code.payload())
            print(code)

        # Draw the result on the screen
        Display.show_image(img)
        gc.collect()

        # print(fps.fps())
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # Stop sensor
    if isinstance(sensor, Sensor):
        sensor.stop()
    # Deinitialize display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # Release media buffer
    MediaManager.deinit()
```

```{admonition} Tip
For specific interface definitions, refer to [find_qrcodes](../../api/openmv/image.md#2281-find_qrcodes).
```
