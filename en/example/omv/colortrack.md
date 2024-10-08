# 6. Color Recognition (find_blobs) Routine Explanation

## 1. Overview

`find_blobs` is an image processing function in OpenMV used to find and recognize "blobs" in an image. These blobs refer to areas with similar colors or brightness in the image. This function is commonly used in visual detection and recognition applications, such as object tracking and color recognition.

CanMV supports OpenMV algorithms and can also use `find_blobs`.

## 2. Function Explanation

### 2.1 Basic Usage

```python
blobs = img.find_blobs([thresholds], area_threshold=area_threshold, pixels_threshold=pixels_threshold, merge=True, margin=0)
```

### 2.2 Parameter Explanation

- thresholds: This is a list containing color ranges used to define the color range of the blobs to be found. It is usually a tuple containing two or three elements. For example, `(100, 200, -64, 127, -128, 127)` represents a range in the HSV color space, where the first and second values are Hue, the third and fourth values are Saturation, and the last two values are Value.

- area_threshold: The area threshold for blobs. Only blobs with an area greater than this value will be returned. The default value is 0.

- pixels_threshold: The pixel count threshold for blobs. Only blobs containing more pixels than this value will be returned. The default value is 0.

- merge: Whether to merge adjacent blobs. When set to `True`, adjacent blobs will be merged into a larger blob; when set to `False`, blobs will not be merged. The default value is `True`.

- margin: The margin used when merging blobs. Set to a positive integer to indicate the maximum distance for merging blobs. The default value is 0.

### 2.3 Return Value

The `find_blobs` function returns a list containing information about the blobs. Each blob is a `Blob` object and typically includes the following attributes:

- `cx` and `cy`: The center coordinates of the blob.
- `x` and `y`: The top-left coordinates of the blob.
- `w` and `h`: The width and height of the blob.
- `area`: The area of the blob (in pixels).

## 3. Example

Here is an example of single-color tracking. For more detailed demos, please refer to the examples included in the firmware's virtual U-disk.

```python
# Single Color Code Tracking Example
#
# This example demonstrates single color code tracking using the CanMV camera.
#
# Color codes are blobs composed of two or more colors. The example below will
# only track colored objects containing the following colors.
import time, os, gc, sys, math

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = 640
DETECT_HEIGHT = 480

# Color tracking thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The thresholds below are used to track red/green objects. You may need to adjust them...
thresholds = [(12, 100, -47, 14, -1, 58), # Generic red threshold -> index 0, so code == (1 << 0)
              (30, 100, -64, -8, -32, 32)] # Generic green threshold -> index 1, so code == (1 << 1)
# When "merge=True", the codes are "OR"-ed together for "find_blobs"

# Only blobs with pixels exceeding "pixel_threshold" and area exceeding "area_threshold"
# will be returned by "find_blobs" below. If changing the camera resolution, adjust
# "pixel_threshold" and "area_threshold". "merge=True" must be set to merge overlapping
# color blobs to form color codes.

sensor = None

try:
    # Construct a Sensor object with default configuration
    sensor = Sensor(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # Reset the sensor
    sensor.reset()
    # Set horizontal mirror
    # sensor.set_hmirror(False)
    # Set vertical flip
    # sensor.set_vflip(False)
    # Set channel 0 output size
    sensor.set_framesize(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # Set channel 0 output format
    sensor.set_pixformat(Sensor.RGB565)

    # Set display; if the chosen screen does not light up, refer to the API documentation
    # for the K230_CanMV_Display module API manual. Four display methods are provided below.
    # Use HDMI as display output, set to VGA
    # Display.init(Display.LT9611, width = 640, height = 480, to_ide = True)

    # Use HDMI as display output, set to 1080P
    # Display.init(Display.LT9611, width = 1920, height = 1080, to_ide = True)

    # Use LCD as display output
    # Display.init(Display.ST7701, to_ide = True)

    # Use IDE as output
    Display.init(Display.VIRT, width = DETECT_WIDTH, height = DETECT_HEIGHT, fps = 100)

    # Initialize media manager
    MediaManager.init()
    # Start the sensor
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()

        # Check if should exit
        os.exitpoint()
        img = sensor.snapshot()

        for blob in img.find_blobs(thresholds, pixels_threshold=100, area_threshold=100, merge=True):
            if blob.code() == 3: # r/g code == (1 << 1) | (1 << 0)
                # These values depend on the blob not being circular - otherwise, they are unstable
                # if blob.elongation() > 0.5:
                #     img.draw_edges(blob.min_corners(), color=(255,0,0))
                #     img.draw_line(blob.major_axis_line(), color=(0,255,0))
                #     img.draw_line(blob.minor_axis_line(), color=(0,0,255))
                # These values are always stable
                img.draw_rectangle([v for v in blob.rect()])
                img.draw_cross(blob.cx(), blob.cy())
                # Note - blob rotation is unique and limited to 0-180
                img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)

        # Draw the result on the screen
        Display.show_image(img)
        gc.collect()

        print(fps.fps())
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # Stop the sensor
    if isinstance(sensor, Sensor):
        sensor.stop()
    # Destroy the display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # Release media buffers
    MediaManager.deinit()
```

```{admonition} Tip
For detailed interface definitions, please refer to [find_blobs](../../api/openmv/image.md#2276-find_blobs)
```
