# Explanation of the DM Code Recognition Routine

## Overview

The Data Matrix code is a type of two-dimensional barcode widely used for identifying and tracking small products. It consists of small black and white squares arranged in a rectangular or square grid.

CanMV supports the OpenMV algorithm capable of recognizing Data Matrix codes. The relevant interface is `find_datamatrices`.

## Example

This example sets the camera output to a 640x480 grayscale image and uses `image.find_datamatrices` to recognize Data Matrix codes.

```{tip}
If the recognition success rate is low, try adjusting the camera's mirror and flip settings.
```

```python
# Data Matrix Example
import time
import math
import os
import gc
import sys

from media.sensor import *
from media.display import *
from media.media import *

# Define the width and height of the detection image
DETECT_WIDTH = 640
DETECT_HEIGHT = 480

sensor = None

try:
    # Construct the Sensor object using default configuration
    sensor = Sensor(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    # Reset the sensor
    sensor.reset()

    # Set output size and format
    sensor.set_framesize(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    sensor.set_pixformat(Sensor.GRAYSCALE)

    # Initialize display
    Display.init(Display.VIRT, width=DETECT_WIDTH, height=DETECT_HEIGHT, fps=100)

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
        for matrix in img.find_datamatrices():
            # Draw a rectangle around the recognized Data Matrix code
            img.draw_rectangle([v for v in matrix.rect()], color=(255, 0, 0))
            print_args = (matrix.rows(), matrix.columns(), matrix.payload(), (180 * matrix.rotation()) / math.pi, fps.fps())
            print("Matrix [%d:%d], Content \"%s\", Rotation %f (degrees), FPS %f" % print_args)

        # Render the result to the screen
        Display.show_image(img)
        gc.collect()

except KeyboardInterrupt:
    print("User stopped")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # Stop the sensor
    if isinstance(sensor, Sensor):
        sensor.stop()
    # Deinitialize the display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # Release media buffers
    MediaManager.deinit()
```

### Code Explanation

- **Import Modules**: Import necessary libraries to use sensor, display, and media management functionalities.
- **Define Image Dimensions**: Set the width and height of the detection image to 640x480.
- **Sensor Configuration**: Create and configure the sensor object, setting the image output size and format (grayscale image).
- **Display Initialization**: Configure the display output method, choosing IDE output.
- **Main Loop**:
  - Capture images and check exit conditions.
  - Recognize Data Matrix codes in the image and draw a red rectangle around the codes.
  - Print detailed information about the Data Matrix codes, including the number of rows, columns, content, rotation angle, and frame rate.
- **Exception Handling**: Capture user interruptions or other exceptions, ensuring the sensor stops properly and resources are released.

```{admonition} Tip
For specific interface definitions, please refer to [find_datamatrices](../../api/openmv/image.md#2283-find_datamatrices).
```
