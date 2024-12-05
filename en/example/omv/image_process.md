# 8. Explanation of Image Processing Routines

## 1. Overview

In OpenMV, there are many image processing functions for different image operations and feature processing. These functions can help you achieve various vision tasks such as image enhancement, noise reduction, binarization, edge detection, etc.

CanMV supports OpenMV algorithms, and these functions can also be used.

## 2. Image Processing Functions Description

### 2.1 Image Enhancement and Correction

- **`histeq`**: Histogram Equalization
  - Used to enhance the contrast of the image, making the histogram distribution more uniform.

  ```python
  img = sensor.snapshot()
  img.histeq()
  ```

- **`gamma_corr`**: Gamma Correction
  - Adjusts the brightness and contrast of the image. A gamma value greater than 1 increases contrast, while a value less than 1 decreases contrast.

  ```python
  img = sensor.snapshot()
  img.gamma_corr(1.5)  # Gamma value is 1.5
  ```

- **`rotation_corr`**: Rotation Correction
  - Corrects rotational errors in the image.

  ```python
  img = sensor.snapshot()
  img.rotation_corr(0.5)  # Corrects rotational error, correction angle is 0.5 radians
  ```

- **`lens_corr`**: Lens Distortion Correction
  - Corrects geometric distortions from the lens, often used to correct fisheye lens distortions.

  ```python
  img = sensor.snapshot()
  img.lens_corr(1.0)  # Corrects distortion, correction coefficient is 1.0
  ```

### 2.2 Filtering and Noise Reduction

- **`gaussian`**: Gaussian Filtering
  - Used to smooth the image and reduce noise. Gaussian filtering performs weighted averaging through mean filtering.

  ```python
  img = sensor.snapshot()
  img.gaussian(2)  # Gaussian filtering, filter kernel size is 2
  ```

- **`bilateral`**: Bilateral Filtering
  - Aims to smooth the image while preserving edges. Bilateral filtering combines smoothing in both the spatial and color domains.

  ```python
  img = sensor.snapshot()
  img.bilateral(5, 75, 75)  # Bilateral filtering, standard deviations for spatial and color domains are 5 and 75 respectively
  ```

- **`median`**: Median Filtering
  - Removes noise from the image, especially salt-and-pepper noise.

  ```python
  img = sensor.snapshot()
  img.median(3)  # Median filtering, window size is 3x3
  ```

- **`mean`**: Mean Filtering
  - Smooths the image by calculating the mean of neighboring pixels to reduce noise.

  ```python
  img = sensor.snapshot()
  img.mean(3)  # Mean filtering, window size is 3x3
  ```

### 2.3 Binarization and Morphological Operations

- **`binary`**: Binarization
  - Converts the image to a binary image, dividing pixels into black and white based on a threshold.

  ```python
  img = sensor.snapshot()
  img.binary([(100, 255)])  # Binarization, threshold range is (100, 255)
  ```

- **`dilate`**: Dilation
  - A morphological operation that expands white areas in the image, often used to fill holes.

  ```python
  img = sensor.snapshot()
  img.dilate(2)  # Dilation operation, performed 2 times
  ```

- **`erode`**: Erosion
  - A morphological operation that shrinks white areas in the image, often used to remove small noise.

  ```python
  img = sensor.snapshot()
  img.erode(2)  # Erosion operation, performed 2 times
  ```

- **`morph`**: Morphological Operations
  - Performs complex morphological operations such as opening and closing operations.

  ```python
  img = sensor.snapshot()
  img.morph(2, morph.MORPH_CLOSE)  # Morphological operation, closing operation
  ```

### 2.4 Edge Detection

- **`laplacian`**: Laplacian Edge Detection
  - Used for detecting edges in the image.

  ```python
  img = sensor.snapshot()
  img.laplacian(3)  # Laplacian edge detection, window size is 3
  ```

- **`sobel`**: Sobel Edge Detection
  - Another filter used for edge detection.

  ```python
  img = sensor.snapshot()
  img.sobel(3)  # Sobel edge detection, window size is 3
  ```

### 2.5 Polar Coordinate Transformation

- **`linpolar`**: Linear Polar Transformation
  - Converts the image from Cartesian coordinates to polar coordinates.

  ```python
  img = sensor.snapshot()
  img.linpolar(10)  # Linear polar transformation, radius step is 10
  ```

- **`logpolar`**: Logarithmic Polar Transformation
  - Converts the image from Cartesian coordinates to logarithmic polar coordinates.

  ```python
  img = sensor.snapshot()
  img.logpolar(10)  # Logarithmic polar transformation, radius step is 10
  ```

### 2.6 Image Inversion and Modes

- **`negate`**: Invert Image
  - Inverts all pixel values in the image.

  ```python
  img = sensor.snapshot()
  img.negate()  # Invert image
  ```

- **`midpoint`**: Midpoint Mode
  - Returns the midpoint pixel value of the image.

  ```python
  img = sensor.snapshot()
  img.midpoint()
  ```

- **`mode`**: Mode Value
  - Returns the most common pixel value in the image.

  ```python
  img = sensor.snapshot()
  img.mode()
  ```

### 2.7 Summary

These functions can be used to perform various image processing tasks:

- **Image Enhancement and Correction**: `histeq`, `gamma_corr`, `rotation_corr`, `lens_corr`
- **Filtering and Noise Reduction**: `gaussian`, `bilateral`, `median`, `mean`
- **Binarization and Morphological Operations**: `binary`, `dilate`, `erode`, `morph`
- **Edge Detection**: `laplacian`, `sobel`
- **Polar Coordinate Transformation**: `linpolar`, `logpolar`
- **Image Inversion and Modes**: `negate`, `midpoint`, `mode`

You can choose the appropriate image processing functions to process and analyze images based on your actual needs.

## 3. Example

Here is a demo of image binarization. For more demos, please refer to the examples included in the firmware's virtual U-disk.

```python
# Color Binarization Filtering Example
#
# This script demonstrates binarization image filtering. You can pass any number of thresholds to segment the image.
import time, os, gc, sys

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = ALIGN_UP(640, 16)
DETECT_HEIGHT = 480

# Use the tool -> Machine Vision -> Threshold Editor to select better thresholds.
red_threshold = (0, 100, 0, 127, 0, 127)  # L A B
green_threshold = (0, 100, -128, 0, 0, 127)  # L A B
blue_threshold = (0, 100, -128, 127, -128, 0)  # L A B

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
    sensor.set_pixformat(Sensor.RGB565)

    # Use IDE as the display output. If the selected screen does not light up, please refer to the K230_CanMV_Display module API manual in the API documentation for configuration.
    Display.init(Display.VIRT, width=DETECT_WIDTH, height=DETECT_HEIGHT, fps=100, to_ide=True)
    # Initialize the media manager
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

    frame_count = 0
    fps = time.clock()
    while True:
        fps.tick()
        try:
            os.exitpoint()

            global sensor
            img = sensor.snapshot()

            # Test red threshold
            if frame_count < 100:
                img.binary([red_threshold])
            # Test green threshold
            elif frame_count < 200:
                img.binary([green_threshold])
            # Test blue threshold
            elif frame_count < 300:
                img.binary([blue_threshold])
            # Test non-red threshold
            elif frame_count < 400:
                img.binary([red_threshold], invert=1)
            # Test non-green threshold
            elif frame_count < 500:
                img.binary([green_threshold], invert=1)
            # Test non-blue threshold
            elif frame_count < 600:
                img.binary([blue_threshold], invert=1)
            else:
                frame_count = 0
            frame_count += 1
            # Draw the result on the screen
            Display.show_image(img)
            img = None
            gc.collect()
            # print(fps.fps())
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
