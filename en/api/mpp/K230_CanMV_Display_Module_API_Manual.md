# `Display` Module API Manual

```{attention}
This module has significant changes starting from firmware version V0.7. If you are using firmware prior to V0.7, please refer to the old version of the documentation.
```

## Overview

This manual is intended to guide developers on using the Micro Python API to call the CanMV Display module for image display functionality.

To add a custom screen, refer to [RTOS SDK / How to Add Panel](https://www.kendryte.com/k230_rtos/zh/main/advanced_development_guide/how_to_add_display.html).

## API Introduction

### init

**Description**

Initializes the Display path, including the VO module, DSI module, and LCD/HDMI.

**Syntax**  

```python
init(type, width=0, height=0, fps=0, flag=0, osd_num=1, to_ide=False, quality=90)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| type           | [Display device type](#type)         | Input          | Required |
| width          | Resolution width                     | Input          | Optional, default value depends on `type` |
| height         | Resolution height                    | Input          | Optional, default value depends on `type` |
| fps            | Display frame rate                   | Input          | Only supported by some display device types |
| flag           | Display [flag](#flag)                 | Input          | |
| osd_num        | Number of OSD layers supported in [show_image](#show_image) | Input | Larger values occupy more memory, default is 1 |
| to_ide         | Whether to transfer screen display to IDE display | Input | Occupies more memory when enabled, implemented via WBC function |
| quality        | Sets JPEG compression quality         | Input          | Effective only when `to_ide=True`, range [10-100], default 90 |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### deinit

**Description**

Performs deinitialization. The deinit method will shut down the entire Display path, including the VO module, DSI module, and LCD/HDMI.

**Syntax**  

```python
deinit()
```

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### inited

**Description**

Queries whether the Display module has been initialized.

**Syntax**  

```python
inited()
```

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| bool         | `True` indicates initialized, `False` indicates not initialized |

### config_layer

**Description**

Configures the properties of a display layer. This method is typically called before binding a layer to set the layer's display parameters.

**Syntax**  

```python
config_layer(rect, pix_format, layer, alpha=255, flag=0)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| rect           | Display area (x, y, w, h)            | Input          | Required, tuple format |
| pix_format     | Image pixel format                   | Input          | See [pix_format](#pix_format) |
| layer          | [Display layer](#layer) ID           | Input          | Required, specifies the layer to configure |
| alpha          | Layer blending transparency           | Input          | Range 0-255, default 255 (opaque) |
| flag           | Display [flag](#flag)                 | Input          | Default 0 |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| int          | Configured layer ID                    |

### bind_layer

**Description**

Binds the output of the `sensor` or `vdec` module to the screen display. This allows continuous image display without manual intervention.

**Syntax**  

```python
bind_layer(src, rect, pix_format, layer, alpha=255, flag=0)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| src            | Source channel info (mod, dev, chn)  | Input          | Obtainable via `sensor.bind_info()`, tuple format |
| rect           | Display area (x, y, w, h)            | Input          | Obtainable via `sensor.bind_info()` |
| pix_format     | Image pixel format                   | Input          | Obtainable via `sensor.bind_info()` |
| layer          | [Display layer](#layer) to bind to   | Input          | Can be bound to `video` or `osd` layer |
| alpha          | Layer blending transparency           | Input          | Range 0-255, default 255 |
| flag           | Display [flag](#flag)                 | Input          | Default 0 |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### unbind_layer

**Description**

Unbinds the binding relationship of a specified layer.

**Syntax**  

```python
unbind_layer(layer)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| layer          | [Display layer](#layer) ID           | Input          | Required |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| bool         | `True` indicates successful unbinding, `False` indicates failure |

### disable_layer

**Description**

Disables the specified display layer.

**Syntax**  

```python
disable_layer(layer)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| layer          | [Display layer](#layer) ID           | Input          | Required |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### show_image

**Description**

Displays an image on the screen.

**Syntax**  

```python
show_image(img, x=0, y=0, layer=Display.LAYER_OSD0, alpha=None, pixel_format=None, flag=0)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| img            | Image object to display              | Input          | Required |
| x              | X value of the starting coordinate   | Input          | Default 0 |
| y              | Y value of the starting coordinate   | Input          | Default 0 |
| layer          | Display on the [specified layer](#layer) | Input      | Only supports OSD layers, default `LAYER_OSD0` |
| alpha          | Layer blending transparency           | Input          | Range 0-255, `None` means use the layer's original setting |
| pixel_format   | Image pixel format                   | Input          | `None` means use the image's original format, see [pix_format](#pix_format) |
| flag           | Display [flag](#flag)                 | Input          | Default 0 |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### width

**Description**

Gets the display width of the screen or a specified layer.

**Syntax**

```python
width(layer=None)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| layer          | Specifies the [display layer](#layer) to query | Input | Optional, if not passed, returns the screen resolution width |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| width        | Width of the screen or specified layer, in pixels |

### height

**Description**

Gets the display height of the screen or a specified layer.

**Syntax**

```python
height(layer=None)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| layer          | Specifies the [display layer](#layer) to query | Input | Optional, if not passed, returns the screen resolution height |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| height       | Height of the screen or specified layer, in pixels |

### fps

**Description**

Gets the current display frame rate.

**Syntax**

```python
fps()
```

**Return Value**

| Return Value | Description                            |
|--------------|----------------------------------------|
| int          | Current display frame rate, in fps     |

### writeback

**Description**

Queries or sets the WriteBack (WBC) function status. The WBC function is used to capture screen display content, typically for transmission to IDE display.

**Syntax**

```python
writeback(enable=None)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| enable         | Sets the WBC function status         | Input          | Optional, `True` to enable, `False` to disable. If no parameter is passed, queries the current status |

**Return Value**

| Return Value | Description                            |
|--------------|----------------------------------------|
| bool         | Returns current WBC status when querying; returns operation result when setting |

### writeback_dump

**Description**

Captures one frame of display content from WBC. Requires `to_ide=True` to be set in [init](#init) and the WBC function to be enabled.

**Syntax**

```python
writeback_dump(timeout=1000)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| timeout        | Timeout in milliseconds              | Input          | Default 1000ms |

**Return Value**

| Return Value | Description                            |
|--------------|----------------------------------------|
| object       | Returns an object containing video frame information |

## Data Structure Description

### type

| Type      | Parameter Value | Notes |
|-----------|-----------------|-------|
| VIRT      | 640x480@90      | *Default* <br> IDE debugging only, not shown on external screens. Custom resolutions (64x64)-(4096x4096) and frame rates (1-200) supported. |
| DEBUGGER  |                 | For debugging screens |
| ST7701    | Display.init(Display.ST7701, width = 800, height = 480) | *Default*<br>800x480 |
|           | Display.init(Display.ST7701, width = 480, height = 800) | 480x800 |
|           | Display.init(Display.ST7701, width = 854, height = 480) | 854x480 |
|           | Display.init(Display.ST7701, width = 480, height = 854) | 480x854 |
|           | Display.init(Display.ST7701, width = 640, height = 480) | 640x480 |
|           | Display.init(Display.ST7701, width = 480, height = 640) | 480x640 |
|           | Display.init(Display.ST7701, width = 368, height = 544) | 368x544 |
|           | Display.init(Display.ST7701, width = 544, height = 368) | 544x368 |
| HX8399    | Display.init(Display.HX8399, width = 1920, height = 1080) | *Default*<br>1920x1080 |
|           | Display.init(Display.HX8399, width = 1080, height = 1920) | 1080x1920 |
| ILI9806   | Display.init(Display.ILI9806, width = 800, height = 480) | *Default*<br>800x480 |
|           | Display.init(Display.ILI9806, width = 480, height = 800) | 480x800 |
| LT9611    | Display.init(Display.LT9611, width = 1920, height = 1080, fps = 30) | *Default*<br>1920x1080@30 |
|           | Display.init(Display.LT9611, width = 1920, height = 1080, fps = 60) | 1920x1080@60 |
|           | Display.init(Display.LT9611, width = 1280, height = 720, fps = 60) | 1280x720@60 |
|           | Display.init(Display.LT9611, width = 1280, height = 720, fps = 50) | 1280x720@50 |
|           | Display.init(Display.LT9611, width = 1280, height = 720, fps = 30) | 1280x720@30 |
|           | Display.init(Display.LT9611, width = 640, height = 480, fps = 60) | 640x480@60 |
| ILI9881   | Display.init(Display.ILI9881, width = 1280, height = 800) | *Default*<br>1280x800 |
|           | Display.init(Display.ILI9881, width = 800, height = 1280) | 800x1280 |
| NT35516   | Display.init(Display.NT35516, width=960, height=536) | *Default*<br>960x536 |
|           | Display.init(Display.NT35516, width=536, height=960) | 536x960 |
| NT35532   | Display.init(Display.NT35532, width=1920, height=1080) | *Default*<br>1920x1080 |
|           | Display.init(Display.NT35532, width=1080, height=1920) | 1080x1920 |
| GC9503    | Display.init(Display.GC9503, width=800, height=480) | *Default*<br>800x480 |
|           | Display.init(Display.GC9503, width=480, height=800) | 480x800 |
| ST7102    | Display.init(Display.ST7102, width=640, height=480) | *Default*<br>640x480 |
|           | Display.init(Display.ST7102, width=480, height=640) | 480x640 |
| AML020T   | Display.init(Display.AML020T, width=480, height=360) | *Default*<br>480x360 |
|           | Display.init(Display.AML020T, width=360, height=480) | 360x480 |
| JD9852    | Display.init(Display.JD9852, width=320, height=240) | *Default*<br>320x240 |
|           | Display.init(Display.JD9852, width=240, height=320) | 240x320 |
| ST7789    | Display.init(Display.ST7789, width=320, height=240) | *Default*<br>320x240 |
|           | Display.init(Display.ST7789, width=240, height=320) | 240x320 |

### layer

K230 provides support for 3 video layers and 4 OSD layers. Classification is as follows:

| Display Layer | Constant Name | Description | Supported Formats |
|---------------|---------------|-------------|-------------------|
| Video Layer 1 | `Display.LAYER_VIDEO1` | Recommended for video data | Only supports `YUV420SP` |
| Video Layer 2 | `Display.LAYER_VIDEO2` | Recommended for video data | Only supports `YUV420SP` |
| Video Layer 3 | `Display.LAYER_VIDEO3` | Recommended for video data | Only supports `YUV420SP` |
| OSD Layer 0   | `Display.LAYER_OSD0`   | Graphics overlay layer | Only supports RGB color space |
| OSD Layer 1   | `Display.LAYER_OSD1`   | Graphics overlay layer | Only supports RGB color space |
| OSD Layer 2   | `Display.LAYER_OSD2`   | Graphics overlay layer | Only supports RGB color space |
| OSD Layer 3   | `Display.LAYER_OSD3`   | Graphics overlay layer | Only supports RGB color space |

### flag

| Flag | Constant Name | Description |
|------|---------------|-------------|
| No Rotation | `Display.FLAG_ROTATION_NONE` or `0` | No rotation |
| Rotate 0 degrees | `Display.FLAG_ROTATION_0` | Rotate 0 degrees |
| Rotate 90 degrees | `Display.FLAG_ROTATION_90` | Rotate 90 degrees |
| Rotate 180 degrees | `Display.FLAG_ROTATION_180` | Rotate 180 degrees |
| Rotate 270 degrees | `Display.FLAG_ROTATION_270` | Rotate 270 degrees |
| No Mirror | `Display.FLAG_MIRROR_NONE` or `0` | No mirroring |
| Horizontal Mirror | `Display.FLAG_MIRROR_HOR` | Horizontal mirroring |
| Vertical Mirror | `Display.FLAG_MIRROR_VER` | Vertical mirroring |
| Horizontal and Vertical Mirror | `Display.FLAG_MIRROR_BOTH` | Simultaneous horizontal and vertical mirroring |

### pix_format

| Color Format | Constant Name | Description |
|--------------|---------------|-------------|
| Grayscale    | `image.GRAYSCALE` or `PIXFORMAT_GRAYSCALE` | 8-bit grayscale format, 1 byte per pixel |
| RGB565       | `image.RGB565` or `PIXFORMAT_RGB565` | RGB format, 16 bits/pixel (5:6:5) |
| ARGB8888     | `image.ARGB8888` or `PIXFORMAT_ARGB8888` | ARGB format, 32 bits/pixel (A:R:G:B) |
| ABGR8888     | `image.ABGR8888` or `PIXFORMAT_ABGR8888` | ABGR format, 32 bits/pixel (A:B:G:R) |
| RGBA8888     | `image.RGBA8888` or `PIXFORMAT_RGBA8888` | RGBA format, 32 bits/pixel (R:G:B:A) |
| BGRA8888     | `image.BGRA8888` or `PIXFORMAT_BGRA8888` | BGRA format, 32 bits/pixel (B:G:R:A) |
| RGB888       | `image.RGB888` or `PIXFORMAT_RGB888` | RGB format, 24 bits/pixel (R:G:B) |
| BGR888       | `image.BGR888` or `PIXFORMAT_BGR888` | BGR format, 24 bits/pixel (B:G:R) |

## Notes

1. **Layer Support**: `show_image` only supports OSD layers. To use multiple OSD layers, set the `osd_num` parameter in `init`.
1. **Image Size**: When calling `show_image`, the image size cannot exceed the screen resolution.
1. **Rotation Handling**: Some screen types (such as ST7701's 368x544 mode) have differences between hardware size and application size; the API automatically handles this conversion.
1. **WBC Function**: To use `writeback_dump` to capture screen content, you must set `to_ide=True` in `init`.

## Example Programs

### Basic Display Example

```python
from media.display import *
from media.media import *
import os, time, image

# Use LCD as display output
Display.init(Display.ST7701, width=800, height=480, to_ide=True)
# Initialize media manager
MediaManager.init()

# Create an image for drawing
img = image.Image(800, 480, image.RGB565)
img.clear()
img.draw_string_advanced(0, 0, 32, "Hello World! 你好世界!!!", color=(255, 0, 0))

Display.show_image(img)

try:
    while True:
        time.sleep(1)
        os.exitpoint()
except KeyboardInterrupt as e:
    print("User stopped:", e)
except BaseException as e:
    print(f"Exception: {e}")

Display.deinit()
MediaManager.deinit()
```

### Sensor Binding Example

```python
from media.display import *
from media.sensor import *
from media.media import *
import time

# Initialize sensor
sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=800, height=480)
sensor.set_pixformat(Sensor.RGB565)

# Get sensor binding information
bind_info = sensor.bind_info()

# Configure and bind display layer
Display.config_layer(rect=(0, 0, 800, 480), 
                     pix_format=bind_info[2], 
                     layer=Display.LAYER_VIDEO1)
Display.bind_layer(src=bind_info[0], 
                   rect=bind_info[1], 
                   pix_format=bind_info[2], 
                   layer=Display.LAYER_VIDEO1)

# Initialize display
Display.init(Display.ST7701, width=800, height=480)
MediaManager.init()

# Start sensor
sensor.run()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("User stopped")
finally:
    sensor.stop()
    Display.deinit()
    MediaManager.deinit()
```
