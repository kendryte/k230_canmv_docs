# `NONAI2D CSC` Module API Manual

## Overview

The K230 chip has 24 built-in hardware Color Space Conversion (CSC) channels, capable of efficiently performing image color space conversion processing. This module supports multiple image format conversions, including common formats such as RGB/YUV, and is suitable for scenarios such as video processing and image display.

## API Reference

### Constructor

**Function**  
Initializes the CSC conversion channel. The channel number is automatically allocated by the system, with no need for the user to specify.

**Syntax**  

```python
from nonai2d import CSC
csc = CSC(fmt, max_width=1920, max_height=1080, buf_num=2)
```

**Parameter Description**  

| Parameter   | Type  | Description                                                          | Default  |
|-------------|-------|----------------------------------------------------------------------|----------|
| fmt         | int   | Target image format (see constant definitions)                       | None     |
| max_width   | int   | Maximum image width supported for processing (pixels)                | 1920     |
| max_height  | int   | Maximum image height supported for processing (pixels)               | 1080     |
| buf_num     | int   | Number of VB buffers allocated, affecting processing performance     | 2        |

**Return Value**  
Returns a CSC object on success, throws an exception on failure

> **Important Notes**  
>
> 1. The channel number is automatically allocated by the system (within the range 0-23), and the user neither needs to nor can specify it  
> 1. It is recommended to set max_width/max_height according to the actual image size to save memory  
> 1. When `fmt=PIXEL_FORMAT_GRAYSCALE`, it will first be internally converted to YUV420SP before extracting the grayscale channel

**Properties**  

| Property   | Type | Description                     |
|------------|------|---------------------------------|
| `chn`      | int  | System-allocated CSC channel number |
| `dst_fmt`  | int  | Target image format             |

### convert Method

**Function**  
Performs image color space conversion

**Syntax**  

```python
result = csc.convert(frame, timeout_ms=1000, cvt=True)
```

**Parameter Description**  

| Parameter    | Type                | Description                                                              | Default  |
|--------------|---------------------|--------------------------------------------------------------------------|----------|
| frame        | py_video_frame_info | Input image frame (obtained from Sensor.snapshot)                        | None     |
| timeout_ms   | int                 | Conversion timeout duration (milliseconds)                               | 1000     |
| cvt          | bool                | True returns Image object, False returns py_video_frame_info             | True     |

**Return Value**  
Returns the converted Image object or py_video_frame_info based on the cvt parameter

### get_frame Method

**Function**  
Retrieves the converted frame from the CSC channel (low-level interface, does not automatically convert to Image).

**Syntax**  

```python
frame = csc.get_frame(timeout_ms=1000)
```

**Parameter Description**  

| Parameter    | Type  | Description                  | Default  |
|--------------|-------|------------------------------|----------|
| timeout_ms   | int   | Timeout duration (milliseconds) | 1000     |

**Return Value**  
Returns a `py_video_frame_info` object on success, returns `None` on timeout

> **Note**: Frames obtained using `get_frame` need to be manually released by calling `release_frame`.

### release_frame Method

**Function**  
Releases a frame obtained via `get_frame`.

**Syntax**  

```python
csc.release_frame(frame)
```

**Parameter Description**  

| Parameter    | Type                | Description                  |
|--------------|---------------------|------------------------------|
| frame        | py_video_frame_info | The frame object to be released |

### destroy Method

**Function**  
Releases CSC channel resources

**Syntax**  

```python
csc.destroy()
```

**Description**  
After being called, all resources occupied by this CSC channel will be released, and the object can no longer be used

## Constant Definitions

### Image Format Constants

| Constant Name                          | Description                          | Typical Application Scenarios              |
|-----------------------------------|-----------------------------|-------------------------|
| PIXEL_FORMAT_GRAYSCALE            | Grayscale image format                  | Black and white image processing             |
| PIXEL_FORMAT_RGB_565              | RGB565 format (big-endian)              | LCD display                 |
| PIXEL_FORMAT_RGB_565_LE           | RGB565 format (little-endian)              | Special display devices             |
| PIXEL_FORMAT_BGR_565              | BGR565 format (big-endian)              | OpenCV compatible processing          |
| PIXEL_FORMAT_BGR_565_LE           | BGR565 format (little-endian)              | Special display devices             |
| PIXEL_FORMAT_RGB_888              | RGB888 format                   | High-quality image processing           |
| PIXEL_FORMAT_BGR_888              | BGR888 format                   | OpenCV compatible processing          |
| PIXEL_FORMAT_ARGB_8888            | ARGB8888 format (with transparency)        | Graphical interface composition             |
| PIXEL_FORMAT_ARGB_1555            | ARGB1555 format (with transparency)        | Low color depth UI             |
| PIXEL_FORMAT_ARGB_4444            | ARGB4444 format (with transparency)        | Low color depth UI             |
| PIXEL_FORMAT_BGR_888_PLANAR       | BGR888 planar format               | Professional image processing             |
| PIXEL_FORMAT_RGB_888_PLANAR       | RGB888 planar format               | Professional image processing             |
| PIXEL_FORMAT_YVU_PLANAR_420       | YVU420 planar format               | Video decoding output             |
| PIXEL_FORMAT_YUV_SEMIPLANAR_420   | YUV420 semi-planar format             | Video encoding input             |
| PIXEL_FORMAT_YVU_SEMIPLANAR_420   | YVU420 semi-planar format             | Video processing                 |
| PIXEL_FORMAT_YVU_PLANAR_444       | YVU444 planar format               | High-quality video processing           |
| PIXEL_FORMAT_YUV_PACKAGE_444      | YUV444 packed format               | High-quality video processing           |
| PIXEL_FORMAT_YUV_SEMIPLANAR_444   | YUV444 semi-planar format             | High-quality video processing           |
| PIXEL_FORMAT_YVU_SEMIPLANAR_444   | YVU444 semi-planar format             | High-quality video processing           |

## Best Practice

```python
import time, os, urandom, sys

from media.display import *
from media.media import *
from media.uvc import *

from nonai2d import CSC

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# hardware Color Space Converter (通道号自动分配)
csc = CSC(CSC.PIXEL_FORMAT_RGB_565)

# use lcd as display output
Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)

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
```
