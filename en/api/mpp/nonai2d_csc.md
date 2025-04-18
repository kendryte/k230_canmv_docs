# 3.13 NONAI2D CSC API Manual

## 1. Overview

The K230 chip has 24 built-in hardware Color Space Conversion (CSC) channels, which can efficiently perform image color space conversions. This module supports various image format conversions including common formats such as RGB/YUV, making it suitable for video processing, image display, and similar applications.

## 2. API Reference

### 2.1 Constructor

**Function**  
Initialize a CSC conversion channel

**Syntax**

```python
from nonai2d import CSC
csc = CSC(chn, fmt, max_width=1920, max_height=1080, buf_num=2)
```

**Parameter Description**

| Parameter    | Type | Description                                                                 | Default  |
|--------------|------|-----------------------------------------------------------------------------|----------|
| chn          | int  | CSC channel number, range: 0–23                                              | Required |
| fmt          | int  | Target image format (see constant definitions)                               | Required |
| max_width    | int  | Maximum image width supported (in pixels)                                    | 1920     |
| max_height   | int  | Maximum image height supported (in pixels)                                   | 1080     |
| buf_num      | int  | Number of VB buffers allocated, affects processing performance               | 2        |

**Return Value**  
Returns a CSC object on success, raises an exception on failure.

> **Important Notes**
>
> 1. The CSC object must be initialized *before* calling `MediaManager.init()`  
> 1. Channel numbers 0–23 must not be reused  
> 1. It’s recommended to set `max_width`/`max_height` according to actual image size to save memory

### 2.2 `convert` Method

**Function**  
Perform image color space conversion

**Syntax**

```python
result = csc.convert(frame, timeout_ms=1000, cvt=True)
```

**Parameter Description**

| Parameter     | Type                | Description                                                          | Default |
|---------------|---------------------|----------------------------------------------------------------------|---------|
| frame         | py_video_frame_info | Input image frame (from `Sensor.snapshot`)                           | Required|
| timeout_ms    | int                 | Conversion timeout in milliseconds                                   | 1000    |
| cvt           | bool                | `True` returns an `Image` object, `False` returns `py_video_frame_info` | True    |

**Return Value**  
Returns a converted `Image` object or `py_video_frame_info`, depending on the `cvt` parameter.

### 2.3 `destroy` Method

**Function**  
Release CSC channel resources

**Syntax**

```python
csc.destroy()
```

**Description**  
After calling this method, all resources used by the CSC channel will be released, and the object can no longer be used.

## 3. Constant Definitions

### Image Format Constants

| Constant Name                    | Description                          | Typical Use Case         |
|----------------------------------|--------------------------------------|--------------------------|
| PIXEL_FORMAT_GRAYSCALE           | Grayscale image format               | Black-and-white image processing |
| PIXEL_FORMAT_RGB_565             | RGB565 format (big-endian)           | LCD display              |
| PIXEL_FORMAT_RGB_565_LE          | RGB565 format (little-endian)        | Special display devices  |
| PIXEL_FORMAT_BGR_565             | BGR565 format (big-endian)           | OpenCV compatibility     |
| PIXEL_FORMAT_BGR_565_LE          | BGR565 format (little-endian)        | Special display devices  |
| PIXEL_FORMAT_RGB_888             | RGB888 format                        | High-quality image processing |
| PIXEL_FORMAT_BGR_888             | BGR888 format                        | OpenCV compatibility     |
| PIXEL_FORMAT_ARGB_8888           | ARGB8888 format (with transparency)  | GUI composition          |
| PIXEL_FORMAT_YVU_PLANAR_420      | YVU420 planar format                 | Video decoding output    |
| PIXEL_FORMAT_YUV_SEMIPLANAR_420  | YUV420 semi-planar format            | Video encoding input     |

## 4. Best Practice Example

```python
import time, os, urandom, sys

from media.display import *
from media.media import *
from media.uvc import *

from nonai2d import CSC

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# hardware Color Space Converter
csc = CSC(0, CSC.PIXEL_FORMAT_RGB_565)

# use lcd as display output
Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)
# init media manager
MediaManager.init()

while True:
    plugin, dev = UVC.probe()
    if plugin:
        print(f"detect USB Camera {dev}")
        break
    time.sleep_ms(100)

mode = UVC.video_mode(640, 480, UVC.FORMAT_MJPEG, 30)

succ, mode = UVC.select_video_mode(mode)
print(f"select mode success: {succ}, mode: {mode}")

UVC.start(cvt = True)

clock = time.clock()

while True:
    clock.tick()

    img = UVC.snapshot()
    if img is not None:
        img = csc.convert(img)
        Display.show_image(img)

    print(clock.fps())

# deinit display
Display.deinit()
csc.destroy()
UVC.stop()

time.sleep_ms(100)
# release media buffer
MediaManager.deinit()
```
