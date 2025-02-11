# 3.2 `Display` Module API Manual

```{attention}
This module has significant changes starting from firmware version V0.7. If you are using firmware prior to V0.7, please refer to the old version of the documentation.
```

## 1. Overview

This manual is intended to guide developers on using the Micro Python API to call the CanMV Display module for image display functionality.

To add a custom screen, refer to [Display Debugger](../../example/media/how_to_add_new_mipi_panel.md).

## 2. API Introduction

### 2.1 init

**Description**

Initializes the Display path, including the VO module, DSI module, and LCD/HDMI.
**`Must be called before MediaManager.init()`**

**Syntax**  

```python
init(type=None, width=None, height=None, osd_num=1, to_ide=False, fps=None, quality=90)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| type           | [Display device type](#31-type)      | Input          | Required |
| width          | Resolution width                     | Input          | Default value depends on `type` |
| height         | Resolution height                    | Input          | Default value depends on `type` |
| osd_num        | Number of layers supported in [show_image](#22-show_image) | Input | Larger values occupy more memory |
| to_ide         | Whether to transfer screen display to IDE display | Input | Occupies more memory when enabled |
| fps            | Display frame rate                   | Input          | Only supports `VIRT` type |
| quality        | Sets `Jpeg` compression quality      | Input          | Effective only when `to_ide=True`, range [10-100] |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### 2.2 show_image

**Description**

Displays an image on the screen.

**Syntax**  

```python
show_image(img, x=0, y=0, layer=None, alpha=255, flag=0)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| img            | Image to display                     | Input          |       |
| x              | X value of the starting coordinate   | Input          |       |
| y              | Y value of the starting coordinate   | Input          |       |
| layer          | Display on the [specified layer](#32-layer) | Input | Only supports `OSD` layer. For multiple layers, set `osd_num` in [init](#21-init) |
| alpha          | Layer blending alpha                 | Input          |       |
| flag           | Display [flag](#33-flag)             | Input          |       |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### 2.3 deinit

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

### 2.4 bind_layer

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
| dstlayer       | Display layer to bind to [display layer](#32-layer) | Input | Can be bound to `video` or `osd` layer |
| rect           | Display area                         | Input          | Obtainable via `sensor.bind_info()` |
| pix_format     | Image pixel format                   | Input          | Obtainable via `sensor.bind_info()` |
| alpha          | Layer blending alpha                 | Input          |       |
| flag           | Display [flag](#33-flag)             | Input          | `LAYER_VIDEO1` not supported |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| None         |                                        |

### 2.5 width

**Description**

Gets the display width of the screen or a specified layer.

**Syntax**

```python
width(layer=None)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| layer          | Specifies the [display layer](#32-layer) to query. If `None`, returns the screen resolution width. | Input | Optional |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| width        | Width of the screen or specified layer |

### 2.6 height

**Description**

Gets the display height of the screen or a specified layer.

**Syntax**

```python
height(layer=None)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| layer          | Specifies the [display layer](#32-layer) to query. If `None`, returns the screen resolution height. | Input | Optional |

**Return Value**  

| Return Value | Description                            |
|--------------|----------------------------------------|
| height       | Height of the screen or specified layer |

## 3. Data Structure Description

### 3.1 type

| Type    | Example Initialization Parameters               | Notes                              |
|---------|-------------------------------------------------|-----------------------------------|
| VIRT    | `Display.init(Display.VIRT, width=640, height=480)` | *Default: 640x480@90* <br> For IDE debugging only. Does not display on external screens. <br> Custom resolutions (64x64)-(4096x4096) and frame rates (1-200) supported. |
| DEBUGGER |                                                | For debugging screens.            |
| ST7701  | `Display.init(Display.ST7701, width=800, height=480)` | *Default: 800x480*                |
|         | `Display.init(Display.ST7701, width=480, height=800)` | Portrait mode: 480x800            |
|         | `Display.init(Display.ST7701, width=854, height=480)` | 854x480                           |
|         | `Display.init(Display.ST7701, width=480, height=854)` | Portrait mode: 480x854            |
|         | `Display.init(Display.ST7701, width=640, height=480)` | 640x480                           |
|         | `Display.init(Display.ST7701, width=480, height=640)` | Portrait mode: 480x640            |
|         | `Display.init(Display.ST7701, width=368, height=552)` | 368x552                           |
|         | `Display.init(Display.ST7701, width=552, height=368)` | Portrait mode: 552x368            |
| HX8399  | `Display.init(Display.HX8399, width=1920, height=1080)` | *Default: 1920x1080*              |
|         | `Display.init(Display.HX8399, width=1080, height=1920)` | Portrait mode: 1080x1920          |
| ILI9806 | `Display.init(Display.ILI9806, width=800, height=480)` | *Default: 800x480*                |
|         | `Display.init(Display.ILI9806, width=480, height=800)` | Portrait mode: 480x800            |
| LT9611  | `Display.init(Display.LT9611, width=1920, height=1080, fps=30)` | *Default: 1920x1080@30*           |
|         | `Display.init(Display.LT9611, width=1920, height=1080, fps=60)` | 1920x1080@60                     |
|         | `Display.init(Display.LT9611, width=1280, height=720, fps=60)` | 1280x720@60                      |
|         | `Display.init(Display.LT9611, width=1280, height=720, fps=50)` | 1280x720@50                      |
|         | `Display.init(Display.LT9611, width=1280, height=720, fps=30)` | 1280x720@30                      |
|         | `Display.init(Display.LT9611, width=640, height=480, fps=60)` | 640x480@60                       |

### 3.2 layer

K230 supports 2 video layers and 4 OSD layers:

| Display Layer  | Description                                     | Notes          |
|----------------|-------------------------------------------------|----------------|
| LAYER_VIDEO1   |                                                 | Only usable in [bind_layer](#24-bind_layer), supports hardware rotation |
| LAYER_VIDEO2   |                                                 | Only usable in [bind_layer](#24-bind_layer), no hardware rotation support |
| LAYER_OSD0     |                                                 | Usable in [show_image](#22-show_image) and [bind_layer](#24-bind_layer) |
| LAYER_OSD1     |                                                 | Usable in [show_image](#22-show_image) and [bind_layer](#24-bind_layer) |
| LAYER_OSD2     |                                                 | Usable in [show_image](#22-show_image) and [bind_layer](#24-bind_layer) |
| LAYER_OSD3     |                                                 | Usable in [show_image](#22-show_image) and [bind_layer](#24-bind_layer) |

### 3.3 flag

| Flag               | Description            | Notes |
|--------------------|------------------------|-------|
| FLAG_ROTATION_0    | Rotate `0°`            |       |
| FLAG_ROTATION_90   | Rotate `90°`           |       |
| FLAG_ROTATION_180  | Rotate `180°`          |       |
| FLAG_ROTATION_270  | Rotate `270°`          |       |
| FLAG_MIRROR_NONE   | No mirroring           |       |
| FLAG_MIRROR_HOR    | Horizontal mirroring   |       |
| FLAG_MIRROR_VER    | Vertical mirroring     |       |
| FLAG_MIRROR_BOTH   | Horizontal & vertical mirroring |       |

## 4. Sample Program

```python
from media.display import *  # Import the display module to use display related interfaces
from media.media import *    # Import the media module to use media related interfaces
import os, time, image       # Import the image module to use image related interfaces

# Use LCD as display output
Display.init(Display.ST7701, width=800, height=480, to_ide=True)
# Initialize media manager
MediaManager.init()

# Create an image for drawing
img = image.Image(800, 480, image.RGB565)
img.clear()
img.draw_string_advanced(0, 0, 32, "Hello World!，你好世界 ！ ！ ！ ", color=(255, 0, 0))

Display.show_image(img)

try:
    while True:
        time.sleep(1)
        os.exitpoint()
except KeyboardInterrupt as e:
    print(" User stopped:", e)
except BaseException as e:
    print(f" Exception: {e}")

Display.deinit()
MediaManager.deinit()
```
