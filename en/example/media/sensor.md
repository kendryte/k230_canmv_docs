# Sensor Example Explanation

## Overview

The K230 has three MIPI-CSI inputs (3x2 lane/1x4+1x2 lane) and can connect up to three cameras. Each camera supports outputting three channels, providing different resolutions and image formats.

## Examples

### Capture and Display Images from Three Channels of a Single Camera on an HDMI Monitor

This example opens a camera, captures images from three channels, and displays them on an HDMI monitor. Channel 0 captures a 1080P image, while channels 1 and 2 capture VGA resolution images and overlay them on the image from channel 0.

```python
# Camera Example
import time
import os
import sys

from media.sensor import *
from media.display import *
from media.media import *

sensor = None

try:
    print("camera_test")

    # Construct Sensor object with default configuration
    sensor = Sensor()
    # Reset the sensor
    sensor.reset()

    # Set resolution for channel 0 to 1920x1080
    sensor.set_framesize(Sensor.FHD)
    # Set format for channel 0 to YUV420SP
    sensor.set_pixformat(Sensor.YUV420SP)
    # Bind channel 0 to display VIDEO1 layer
    bind_info = sensor.bind_info()
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1)

    # Set resolution and format for channel 1
    sensor.set_framesize(width=640, height=480, chn=CAM_CHN_ID_1)
    sensor.set_pixformat(Sensor.RGB888, chn=CAM_CHN_ID_1)

    # Set resolution and format for channel 2
    sensor.set_framesize(width=640, height=480, chn=CAM_CHN_ID_2)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_2)

    # Initialize HDMI and IDE output display. If the screen cannot light up, refer to the K230_CanMV_Display module API manual in the API documentation for configuration.
    Display.init(Display.LT9611, to_ide=True, osd_num=2)
    # Initialize media manager
    MediaManager.init()
    # Start the sensor
    sensor.run()

    while True:
        os.exitpoint()

        img = sensor.snapshot(chn=CAM_CHN_ID_1)
        Display.show_image(img, alpha=128)

        img = sensor.snapshot(chn=CAM_CHN_ID_2)
        Display.show_image(img, x=1920 - 640, layer=Display.LAYER_OSD1)

except KeyboardInterrupt as e:
    print("User stopped: ", e)
except BaseException as e:
    print(f"Exception: {e}")
finally:
    # Stop the sensor
    if isinstance(sensor, Sensor):
        sensor.stop()
    # Destroy display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # Release media buffer
    MediaManager.deinit()
```

### Capture and Display Images from Two Cameras on an HDMI Monitor

This example configures two cameras to output 960x540 images and displays them side by side on an HDMI monitor.

```python
# Dual Camera Example
import time
import os
import sys

from media.sensor import *
from media.display import *
from media.media import *

sensor0 = None
sensor1 = None

try:
    print("camera_test")

    # Construct Sensor object sensor0
    sensor0 = Sensor(id=0)
    sensor0.reset()
    # Set resolution for channel 0 to 960x540
    sensor0.set_framesize(width=960, height=540)
    # Set format for channel 0 to YUV420
    sensor0.set_pixformat(Sensor.YUV420SP)
    # Bind channel 0 to display VIDEO1 layer
    bind_info = sensor0.bind_info(x=0, y=0)
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1)

    # Construct Sensor object sensor1
    sensor1 = Sensor(id=1)
    sensor1.reset()
    # Set resolution for channel 0 to 960x540
    sensor1.set_framesize(width=960, height=540)
    # Set format for channel 0 to YUV420
    sensor1.set_pixformat(Sensor.YUV420SP)
    # Bind channel 0 to display VIDEO2 layer
    bind_info = sensor1.bind_info(x=960, y=0)
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO2)

    # Initialize HDMI and IDE output display. If the screen cannot light up, refer to the K230_CanMV_Display module API manual in the API documentation for configuration.
    Display.init(Display.LT9611, to_ide=True)
    # Initialize media manager
    MediaManager.init()

    # In a multi-camera scenario, run needs to be executed only once
    sensor0.run()

    while True:
        os.exitpoint()
        time.sleep(1)
except KeyboardInterrupt as e:
    print("User stopped")
except BaseException as e:
    print(f"Exception: '{e}'")
finally:
    # Stop each sensor
    if isinstance(sensor0, Sensor):
        sensor0.stop()
    if isinstance(sensor1, Sensor):
        sensor1.stop()
    # Destroy display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # Release media buffer
    MediaManager.deinit()
```

```{admonition} Note
For detailed interfaces of the Sensor module, please refer to the [API documentation](../../api/mpp/K230_CanMV_Sensor模块API手册.md).
```
