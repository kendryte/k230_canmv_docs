# Explanation of Eigenvalue Detection Routines

## Overview

In OpenMV, `find_hog`, `find_lines`, `find_rects`, `find_features`, and `get_regression` are functions used for image processing and feature detection.

CanMV supports OpenMV algorithms and can also use these functions.

## Function Description

### find_hog

The `find_hog` function is used to detect objects in an image using HOG (Histogram of Oriented Gradients) feature descriptors. HOG is a commonly used feature description method for object detection.

- Syntax

```python
objects = img.find_hog(roi=None, threshold=0.5, min_size=(0, 0))
```

- Parameter Explanation

  - roi: Optional parameter that defines a Region of Interest. The default value is `None`, meaning detection is performed on the entire image.
  - threshold: Confidence threshold. Only detection results with confidence greater than this value will be returned. The default value is `0.5`.
  - min_size: Minimum size of the detected object. Specified as a tuple `(width, height)`. The default value is `(0, 0)`, meaning there is no minimum size limit.

- Return Value

Returns a list of detected objects, each represented as a `Rect` object containing the position and size of the object.

### find_lines

The `find_lines` function is used to detect lines in an image. This function is suitable for finding long lines in the image.

- Syntax

```python
lines = img.find_lines(threshold=1000, theta_margin=20, rho_margin=20)
```

- Parameter Explanation

  - threshold: Minimum length of the line. Detected lines must exceed this length. The default value is `1000`.
  - theta_margin: Tolerance for the angle in degrees. The default value is `20`.
  - rho_margin: Tolerance for the distance in pixels. The default value is `20`.

- Return Value

Returns a list of line information. Each line is represented as a `Line` object containing the start point, end point, length, and angle of the line.

### find_rects

The `find_rects` function is used to detect rectangular regions in an image. This function can be used to find square or rectangular objects in the image.

- Syntax

```python
rects = img.find_rects(threshold=2000, margin=10)
```

- Parameter Explanation

  - threshold: Minimum area of the rectangle. The default value is `2000`.
  - margin: Tolerance for the margin of rectangle detection. The default value is `10`.

- Return Value

Returns a list of rectangle information. Each rectangle is represented as a `Rect` object containing the coordinates and size of the rectangle.

### find_features

The `find_features` function is used to detect feature points in an image. These feature points can be used for tasks such as image matching and tracking.

- Syntax

```python
features = img.find_features(algorithm, threshold=10)
```

- Parameter Explanation

  - algorithm: The feature detection algorithm to use. Common algorithms include `image.FORBIDDEN`, `image.BRIEF`, etc.
  - threshold: Threshold for feature detection. The default value is `10`.

- Return Value

Returns a list of feature point information. Each feature point is represented as a `Feature` object containing the position and other information of the feature point.

### get_regression

The `get_regression` function is used to detect regression lines from an image, i.e., lines that fit data points. It is typically used to mark trends or directions in the data.

- Syntax

```python
line = img.get_regression(threshold=1000, min_length=10, max_distance=5)
```

- Parameter Explanation

  - threshold: Minimum length of the line. The default value is `1000`.
  - min_length: Minimum length of the fitted line. The default value is `10`.
  - max_distance: Maximum allowed distance from data points to the regression line. The default value is `5`.

- Return Value

Returns a `Line` object containing the regression line information, representing the fitted line.

### Summary

These functions are important tools in the OpenMV image processing library, each serving different vision tasks:

- `find_hog`: Detect objects based on HOG features.
- `find_lines`: Detect lines in the image.
- `find_rects`: Detect rectangular regions in the image.
- `find_features`: Detect feature points in the image.
- `get_regression`: Detect regression lines in the image.

## Example

Here is a demo for finding lines. For more demos, please refer to the examples included in the firmware's virtual USB drive.

```python
# Line Detection Example
#
# This example demonstrates how to find lines in an image. For each line
# object found in the image, it will return a line object containing the rotation of the line.
#
# Note: Line detection is done via the Hough transform:
# http://en.wikipedia.org/wiki/Hough_transform
# Please read the above link for more information about `theta` and `rho`.

# find_lines() finds infinitely long lines. Use find_line_segments() to find non-infinite lines.
import time, os, gc, sys

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = ALIGN_UP(640, 16)
DETECT_HEIGHT = 480

# All line objects have a `theta()` method to get their rotation angle (in degrees).
# You can filter lines based on their rotation angle.

min_degree = 0
max_degree = 179

# All line objects also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their endpoints,
# and a `line()` method to return all these values as a 4-tuple for use with `draw_line()`.

# About negative rho values:
#
# A [theta+0:-rho] tuple is the same as [theta+180:+rho].
sensor = None

def camera_init():
    global sensor

    # Construct a Sensor object with default configuration
    sensor = Sensor(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    # Reset the sensor
    sensor.reset()
    # Set horizontal mirror
    # sensor.set_hmirror(False)
    # Set vertical flip
    # sensor.set_vflip(False)

    # Set the output size of channel 0
    sensor.set_framesize(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    # Set the output format of channel 0
    sensor.set_pixformat(Sensor.GRAYSCALE)
    # Use IDE as the display output. If the screen you selected does not light up, please refer to the API documentation of the K230_CanMV_Display module for configuration.
    Display.init(Display.VIRT, width=DETECT_WIDTH, height=DETECT_HEIGHT, fps=100, to_ide=True)
    # Initialize media manager
    MediaManager.init()
    # Start the sensor
    sensor.run()

def camera_deinit():
    global sensor
    # Stop the sensor
    sensor.stop()
    # Destroy the display
    Display.deinit()
    # Sleep
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # Release media buffer
    MediaManager.deinit()

def capture_picture():

    fps = time.clock()
    while True:
        fps.tick()
        try:
            os.exitpoint()
            global sensor
            img = sensor.snapshot()

            # `threshold` controls the number of lines found in the image. Only lines with edge differences greater than `threshold` will be detected.

            # More about `threshold` - Each pixel in the image contributes a magnitude value to the line.
            # The sum of all contributions is the magnitude of the line. Then, when lines merge, their magnitudes are summed.
            # Note that `threshold` filters out low-magnitude lines before merging. To see the magnitude of unmerged lines, set `theta_margin` and `rho_margin` to 0.

            # `theta_margin` and `rho_margin` control the merging of similar lines. If the theta and rho values of two lines differ by less than this margin, they will be merged.

            for l in img.find_lines(threshold=1000, theta_margin=25, rho_margin=25):
                if (min_degree <= l.theta()) and (l.theta() <= max_degree):
                    img.draw_line([v for v in l.line()], color=(255, 0, 0))
                    print(l)

            # Draw the result on the screen
            Display.show_image(img)
            img = None

            gc.collect()
            #print(fps.fps())
        except KeyboardInterrupt as e:
            print("user stop: ", e)
            break
        except BaseException as e:
            print(f"Exception {e}")
            break

def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    camera_is_init = False
    try:
        print("camera init")
        camera_init()
        camera_is_init = True
        print("camera capture")
        capture_picture()
    except Exception as e:
        print(f"Exception {e}")
    finally:
        if camera_is_init:
            print("camera deinit")
            camera_deinit()

if __name__ == "__main__":
    main()
```

```{admonition} Tip
For specific interface definitions, please refer to [image](../../api/openmv/image.md)
```
