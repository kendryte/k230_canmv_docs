# Color Recognition (find_blobs) Routine Explanation

## Overview

`find_blobs` is an image processing function of OpenMV, used to find and identify "blobs" in an image. These blobs refer to regions in the image with similar color or brightness. This function is commonly used in visual detection and recognition applications, such as object tracking, color recognition, etc.

CanMV supports OpenMV algorithms and can also use `find_blobs`.

## Function Explanation

### Basic Usage

```python
blobs = img.find_blobs([thresholds], area_threshold=area_threshold, pixels_threshold=pixels_threshold, merge=True, margin=0)
```

### Parameter Explanation

- thresholds: This is a list containing color ranges, used to define the color range of the blobs to look for. It is usually a tuple containing two or three elements. For example, `(100, 200, -64, 127, -128, 127)` represents a range in the HSV color space, where the first and second values are Hue, the third and fourth are Saturation, and the last two are Value.

- area_threshold: The area threshold for blobs. Only blobs with an area greater than this value will be returned. The default value is 0.

- pixels_threshold: The pixel count threshold for blobs. Only blobs containing more pixels than this value will be returned. The default value is 0.

- merge: Whether to merge adjacent blobs. When set to `True`, adjacent blobs will be merged into one large blob; when set to `False`, blobs will not be merged. The default value is `True`.

- margin: The margin used when merging blobs. Set to a positive integer, indicating the maximum distance when merging blobs. The default value is 0.

### Return Value

The `find_blobs` function returns a list containing blob information. Each blob is a `Blob` object, which typically contains the following attributes:

- `cx` and `cy`: The center coordinates of the blob.
- `x` and `y`: The coordinates of the top-left corner of the blob.
- `w` and `h`: The width and height of the blob.
- `area`: The area of the blob (pixel count).

## Example

Only a single color tracking example is listed here. For specific demos, please refer to the routines in the virtual USB drive that comes with the firmware.

```python
# Single Color Code Tracking Example
#
# This example shows off single color code tracking using the CanMV camera.
#
# Color codes are or'ed blobs of two or more colors. The example below will
# only track the color objects which are a color blob that includes the
# following colors.
import time, os, gc, sys, math

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = 640
DETECT_HEIGHT = 480

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The thresholds below are used for tracking a red/green objects. You may
# need to tune them...
thresholds = [(12, 100, -47, 14, -1, 58), # generic red
              (30, 100, -64, -8, -32, 32)] # generic green
# When "merge=True" is passed to "find_blobs" the returned blobs will be
# "code" blobs where the code is a bitwise OR of the thresholds indices

# Only blobs that have pixels more than "pixel_threshold" and area more than
# "area_threshold" are returned by "find_blobs" below. You may want to
# adjust these thresholds to be larger if you are looking for a smaller object
# in the image. You must set "merge=True" to merge overlapping color blobs
# so that the code color blob is formed.

sensor = None

try:
    # Construct a Sensor object with default configuration
    sensor = Sensor(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # sensor reset
    sensor.reset()
    # set horizontal mirror
    # sensor.set_hmirror(False)
    # set vertical flip
    # sensor.set_vflip(False)
    # set channel 0 output size
    sensor.set_framesize(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # set channel 0 output format
    sensor.set_pixformat(Sensor.RGB565)

    # Set display configuration. If the screen you selected cannot be lit up,
    # please refer to the k230_canmv_display_module_api_manual in the API documentation
    # for self-configuration. Four display methods are provided below.
    # Use HDMI as display output, configured as VGA
    # Display.init(Display.LT9611, width = 640, height = 480, to_ide = True)

    # Use HDMI as display output, configured as 1080P
    # Display.init(Display.LT9611, width = 1920, height = 1080, to_ide = True)

    # Use LCD as display output
    # Display.init(Display.ST7701, to_ide = True)

    # Use IDE as output
    Display.init(Display.VIRT, width = DETECT_WIDTH, height = DETECT_HEIGHT, fps = 100)

    # Initialize the media manager
    MediaManager.init()
    # sensor start run
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()

        # Check if should exit
        os.exitpoint()
        img = sensor.snapshot()

        for blob in img.find_blobs(thresholds, pixels_threshold=100, area_threshold=100, merge=True):
            if blob.code() == 3: # r/g code == (1 << 1) | (1 << 0)
                # These values depend on the blob not being circular - otherwise they are unstable
                # if blob.elongation() > 0.5:
                #     img.draw_edges(blob.min_corners(), color=(255,0,0))
                #     img.draw_line(blob.major_axis_line(), color=(0,255,0))
                #     img.draw_line(blob.minor_axis_line(), color=(0,0,255))
                # These values are stable all the time
                img.draw_rectangle([v for v in blob.rect()])
                img.draw_cross(blob.cx(), blob.cy())
                # Note - the blob rotation is unique to 0-180 only.
                img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)

        # Draw results to the screen
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

```{admonition} Tip
For specific interface definitions, please refer to [find_blobs](../../api/openmv/image.md#find-blobs)
```
