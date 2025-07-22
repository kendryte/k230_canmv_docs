# Explanation of Barcode Recognition Routine

## Overview

A barcode is a visual pattern used to represent data by encoding information through stripes or patterns of varying widths and spaces. Barcodes are widely used across various industries for automatic identification, storage, and data management.

CanMV supports the OpenMV algorithm and can recognize barcodes. The relevant interface is `find_barcodes`, which supports multiple barcode formats.

## Example

This example sets the camera output to a 640x480 grayscale image and uses `image.find_barcodes` to recognize barcodes.

```{tip}
If the recognition success rate is low, try adjusting the camera's mirror and flip settings, and ensure there is a white area on both sides of the barcode.
```

```python
# Barcode detection example
import time
import math
import os
import gc
import sys

from media.sensor import *
from media.display import *
from media.media import *

# Function: Get the name of the barcode type
def barcode_name(code):
    barcode_types = {
        image.EAN2: "EAN2",
        image.EAN5: "EAN5",
        image.EAN8: "EAN8",
        image.UPCE: "UPCE",
        image.ISBN10: "ISBN10",
        image.UPCA: "UPCA",
        image.EAN13: "EAN13",
        image.ISBN13: "ISBN13",
        image.I25: "I25",
        image.DATABAR: "DATABAR",
        image.DATABAR_EXP: "DATABAR_EXP",
        image.CODABAR: "CODABAR",
        image.CODE39: "CODE39",
        image.PDF417: "PDF417",
        image.CODE93: "CODE93",
        image.CODE128: "CODE128",
    }
    return barcode_types.get(code.type(), "Unknown Barcode")

# Define image detection width and height
DETECT_WIDTH = 640
DETECT_HEIGHT = 480

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

        # Recognize barcodes in the image
        for code in img.find_barcodes():
            img.draw_rectangle([v for v in code.rect()], color=(255, 0, 0))  # Draw rectangle around detected barcode
            print_args = (
                barcode_name(code), 
                code.payload(), 
                (180 * code.rotation()) / math.pi, 
                code.quality(), 
                fps.fps()
            )
            print("Barcode %s, Content \"%s\", Rotation %f (degrees), Quality %d, FPS %f" % print_args)

        # Draw the result on the screen
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

- **Import Modules**: Import necessary libraries to use sensor, display, and media management functions.
- **barcode_name Function**: Returns the name of the barcode type for further processing and display.
- **Sensor Configuration**: Create and configure the sensor object, including setting the width, height, and format (grayscale image) of the image output.
- **Display Initialization**: Configure the display output method, which can be HDMI, LCD, or IDE.
- **Main Loop**:
  - Capture images and check exit conditions.
  - Recognize barcodes in the image and draw a red rectangle around the barcode.
  - Print detailed information about the barcode, including type, content, rotation angle, quality, and current frame rate.
- **Exception Handling**: Capture user interruptions or other exceptions to ensure the sensor stops properly and resources are released.

```{admonition} Tip
For specific interface definitions, please refer to [find_barcodes](../../api/openmv/image.md#2284-find_barcodes).
```
