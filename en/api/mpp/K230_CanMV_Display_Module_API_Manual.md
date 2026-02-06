# `Display` Module API Manual

```{attention}
This module has significant changes starting from firmware version V0.7. If you are using firmware prior to V0.7, please refer to the old version of the documentation.
```

## Overview

This manual is intended to guide developers on using the Micro Python API to call the CanMV Display module for image display functionality.

To add a custom screen, refer to [Display Debugger](../../example/media/how_to_add_new_mipi_panel.md).

## API Introduction

### init

**Description**

Initializes the Display path, including the VO module, DSI module, and LCD/HDMI.
**`Must be called before MediaManager.init()`**

**Syntax**  

```python
init(type=None, width=None, height=None, osd_num=1, to_ide=False, flag=None, fps=None, quality=90)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| type           | [Display device type](#type)      | Input          | Required |
| width          | Resolution width                     | Input          | Default value depends on `type` |
| height         | Resolution height                    | Input          | Default value depends on `type` |
| osd_num        | Number of layers supported in [show_image](#show_image) | Input | Larger values occupy more memory |
| flag           | Display [flag](#flag)             | Input          | |
| to_ide         | Whether to transfer screen display to IDE display | Input | Occupies more memory when enabled |
| fps            | Display frame rate                   | Input          | Only supports `VIRT` type |
| quality        | Sets `Jpeg` compression quality      | Input          | Effective only when `to_ide=True`, range [10-100] |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### show_image

**Description**

Displays an image on the screen.

**Syntax**  

```python
show_image(img, x=0, y=0, layer=None, alpha=255, flag=None)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| img            | Image to display                     | Input          |       |
| x              | X value of the starting coordinate   | Input          |       |
| y              | Y value of the starting coordinate   | Input          |       |
| layer          | Display on the [specified layer](#layer) | Input | Only supports `OSD` layer. For multiple layers, set `osd_num` in [init](#init) |
| alpha          | Layer blending alpha                 | Input          |       |
| flag           | Display [flag](#flag)             | Input          |       |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### deinit

**Description**

Performs deinitialization. The deinit method will shut down the entire Display path, including the VO module, DSI module, and LCD/HDMI.
**`Must be called before MediaManager.deinit()`**  
**`Must be called after sensor.stop()`**

**Syntax**  

```python
deinit()
```

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### bind_layer

**Description**

Binds the output of the `sensor` or `vdec` module to the screen display. This allows continuous image display without manual intervention.
**`Must be called before init`**

**Syntax**  

```python
bind_layer(src=(mod, dev, layer), dstlayer, rect=(x, y, w, h), pix_format, alpha, flag)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| src            | Output information of `sensor` or `vdec` | Input      | Obtainable via `sensor.bind_info()` |
| dstlayer       | Display layer to bind to [display layer](#layer) | Input | Can be bound to `video` or `osd` layer |
| rect           | Display area                         | Input          | Obtainable via `sensor.bind_info()` |
| pix_format     | Image pixel format                   | Input          | Obtainable via `sensor.bind_info()` |
| alpha          | Layer blending alpha                 | Input          |       |
| flag           | Display [flag](#flag)             | Input          | `LAYER_VIDEO1` not supported |

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
| layer          | Specifies the [display layer](#layer) to query. If `None`, returns the screen resolution width. | Input | Optional |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| width        | Width of the screen or specified layer |

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
| layer          | Specifies the [display layer](#layer) to query. If `None`, returns the screen resolution height. | Input | Optional |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| height       | Height of the screen or specified layer |

## Data Structure Description

### type

> **Supported Panel Types**

| Type        | Example Initialization Parameters | Notes |
|-------------|----------------------------------------------------------|-------------------------------------------------------------|
| VIRT        | Display.init(Display.VIRT, width=640, height=480, fps=90) | *Default* <br> IDE debugging only, not shown on external screens. Custom resolutions (64x64)-(4096x4096) and frame rates (1-200) supported. |
| DEBUGGER    | Display.init(Display.DEBUGGER) | For debugging screens |
| ST7701      | Display.init(Display.ST7701, width=800, height=480) | *Default: 800x480*, also supports 480x800, 854x480, 480x854, 640x480, 480x640, 368x544, 544x368 |
| HX8399      | Display.init(Display.HX8399, width=1920, height=1080) | *Default: 1920x1080*, also supports 1080x1920 |
| ILI9806     | Display.init(Display.ILI9806, width=800, height=480) | *Default: 800x480*, also supports 480x800 |
| LT9611      | Display.init(Display.LT9611, width=1920, height=1080, fps=30) | *Default: 1920x1080@30*, also supports 1920x1080@60, 1280x720@60/50/30, 640x480@60 |
| ILI9881     | Display.init(Display.ILI9881, width=1280, height=800) | *Default: 1280x800*, also supports 800x1280 |
| NT35516     | Display.init(Display.NT35516, width=960, height=536) | Also supports 536x960 |
| NT35532     | Display.init(Display.NT35532, width=1920, height=1080) | Also supports 1080x1920 |
| GC9503      | Display.init(Display.GC9503, width=800, height=480) | Also supports 480x800 |
| ST7102      | Display.init(Display.ST7102, width=640, height=480) | Also supports 480x640 |
| AML020T     | Display.init(Display.AML020T, width=480, height=360) | |
| JD9852      | Display.init(Display.JD9852, width=320, height=240) | Also supports 240x320 |

> New panel types: NT35516, NT35532, GC9503, ST7102, AML020T, JD9852.

For more resolutions or custom panels, refer to the source code or contact the developers.

### layer

K230 provides 2 video layers and 4 OSD layers:

| Display Layer | Description | Notes |
|---------------|-------------|-------|
| LAYER_VIDEO1 | | Only supports `NV12` (`YUV420SP`), recommended for video data |
| LAYER_VIDEO2 | | Only supports `NV12` (`YUV420SP`), recommended for video data |
| LAYER_VIDEO3 | | Only supports `NV12` (`YUV420SP`), recommended for video data |
| LAYER_OSD0 | | Only supports `RGB` color space |
| LAYER_OSD1 | | Only supports `RGB` color space |
| LAYER_OSD2 | | Only supports `RGB` color space |
| LAYER_OSD3 | | Only supports `RGB` color space |

### flag

| Flag | Description | Notes |
|-------------------|---------------------|------|
| FLAG_ROTATION_0 | Rotate 0 degrees | |
| FLAG_ROTATION_90 | Rotate 90 degrees | |
| FLAG_ROTATION_180 | Rotate 180 degrees | |
| FLAG_ROTATION_270 | Rotate 270 degrees | |
| FLAG_MIRROR_NONE | No mirroring | |
| FLAG_MIRROR_HOR | Horizontal mirroring | |
| FLAG_MIRROR_VER | Vertical mirroring | |
| FLAG_MIRROR_BOTH | Horizontal and vertical mirroring | |

### pix_format

| Color Format | Description | Notes |
|------------------------|----------------------|------|
| PIXFORMAT_GRAYSCALE | 8-bit grayscale | 1 byte per pixel, value 0 (black) to 255 (white) |
| PIXFORMAT_RGB565 | RGB, 16 bits/pixel | 5 bits red, 6 bits green, 5 bits blue, no alpha |
| PIXFORMAT_ARGB8888 | ARGB, 32 bits/pixel | 8 bits per channel, order: alpha, red, green, blue |
| PIXFORMAT_ABGR8888 | ABGR, 32 bits/pixel | 8 bits per channel, order: alpha, blue, green, red |
| PIXFORMAT_RGBA8888 | RGBA, 32 bits/pixel | 8 bits per channel, order: red, green, blue, alpha |
| PIXFORMAT_BGRA8888 | BGRA, 32 bits/pixel | 8 bits per channel, order: blue, green, red, alpha |
| PIXFORMAT_RGB888 | RGB, 24 bits/pixel | 8 bits per channel, order: red, green, blue, no alpha |
| PIXFORMAT_BGR888 | BGR, 24 bits/pixel | 8 bits per channel, order: blue, green, red, no alpha |

## Sample Program

```python
from media.display import *  # Import display module for display interfaces
from media.media import *    # Import media module for media interfaces
import os, time, image       # Import image module for image interfaces

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
