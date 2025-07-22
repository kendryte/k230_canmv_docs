# Explanation of AprilTags Recognition Routine

## Overview

AprilTags is a visual marker system widely used in the field of computer vision for localization, identification, and tracking. Developed by April Robotics, AprilTags is an efficient binary identification tag system, particularly suited for applications such as robotics and augmented reality.

CanMV supports the OpenMV algorithm and can recognize AprilTags through the `find_apriltags` interface.

## Example

This example sets the camera output to a 320x240 grayscale image and uses `image.find_apriltags` to recognize AprilTags.

```{tip}
If the recognition success rate is low, try adjusting the camera's mirror and flip settings.
```

```python
# AprilTags Example
# This example demonstrates the powerful capabilities of CanMV in detecting April Tags.

import time
import math
import os
import gc
import sys

from media.sensor import *
from media.display import *
from media.media import *

# Define the width and height of the detection image
DETECT_WIDTH = 320
DETECT_HEIGHT = 240

# Define available tag families
tag_families = 0
tag_families |= image.TAG16H5  # 4x4 square tag
tag_families |= image.TAG25H7  # 5x7 square tag
tag_families |= image.TAG25H9  # 5x9 square tag
tag_families |= image.TAG36H10 # 6x10 square tag
tag_families |= image.TAG36H11 # 6x11 square tag (default)
tag_families |= image.ARTOOLKIT # ARToolKit tag

# Function: Get the name of the tag family
def family_name(tag):
    family_dict = {
        image.TAG16H5: "TAG16H5",
        image.TAG25H7: "TAG25H7",
        image.TAG25H9: "TAG25H9",
        image.TAG36H10: "TAG36H10",
        image.TAG36H11: "TAG36H11",
        image.ARTOOLKIT: "ARTOOLKIT",
    }
    return family_dict.get(tag.family(), "Unknown Tag Family")

sensor = None

try:
    # Construct Sensor object with default configuration
    sensor = Sensor(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    # Reset sensor
    sensor.reset()

    # Set output size and format
    sensor.set_framesize(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    sensor.set_pixformat(Sensor.GRAYSCALE)

    # Initialize display
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
        for tag in img.find_apriltags(families=tag_families):
            # Draw rectangle and center cross for recognized tags
            img.draw_rectangle([v for v in tag.rect()], color=(255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))
            print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
            print("Tag Family %s, Tag ID %d, Rotation %f (degrees)" % print_args)

        # Draw results on screen
        Display.show_image(img)
        gc.collect()

except KeyboardInterrupt:
    print("User stopped")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # Stop sensor
    if isinstance(sensor, Sensor):
        sensor.stop()
    # Destroy display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # Release media buffer
    MediaManager.deinit()
```

### Code Explanation

- **Import Modules**: Import necessary libraries for sensor, display, and media management functionality.
- **Define Image Size**: Set the detection image width and height to 320x240.
- **Define Tag Families**: Configure the recognizable tag families, including TAG16H5, TAG25H7, TAG25H9, TAG36H10, TAG36H11, and ARToolkit. You can disable some tag families by commenting out the relevant lines.
- **Family Name Function**: Returns the name of the tag based on its type, facilitating subsequent processing and display.
- **Sensor Configuration**: Create and configure the sensor object, setting the image output size and format (grayscale image).
- **Display Initialization**: Configure display output method, choosing IDE output.
- **Main Loop**:
  - Capture images and check exit conditions.
  - Recognize AprilTags in the image and draw red rectangles and center crosses around the tags.
  - Print detailed tag information, including tag family, tag ID, and rotation angle.
- **Exception Handling**: Capture user interruptions or other exceptions, ensuring the sensor stops normally and resources are released.

```{admonition} Tip
For specific interface definitions, refer to [find_apriltags](../../api/openmv/image.md#2282-find_apriltags).
```
