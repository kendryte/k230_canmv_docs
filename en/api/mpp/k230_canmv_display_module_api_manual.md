# `Display` Module API Manual

```{attention}
This module has undergone significant changes since firmware version V0.7. If you are using firmware prior to V0.7, please refer to the older version documentation.
```

## Overview

This manual is intended to guide developers in using the Micro Python API to call the CanMV Display module to implement image display functionality.

To add a custom screen, please refer to [RTOS SDK / How to Add Panel](https://www.kendryte.com/k230_rtos/zh/main/advanced_development_guide/how_to_add_display.html)

## API Introduction

### init

**Description**

Initializes the Display pipeline, including the VO module, DSI module, and LCD/HDMI.

**Syntax**

```python
init(type, width=0, height=0, fps=0, flag=0, osd_num=1, to_ide=False, quality=90)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| type     | [Display device type](#type)     | Input      | Required |
| width    | Resolution width                   | Input      | Optional parameter, default value determined by `type` |
| height   | Resolution height                   | Input      | Optional parameter, default value determined by `type` |
| fps      | Display frame rate                     | Input      | Only some display device types support specifying frame rate |
| flag     | Display [flags](#flag)           | Input      |                   |
| osd_num  | Number of OSD layers supported in [show_image](#show_image) | Input | Larger values consume more memory, default value is 1 |
| to_ide   | Whether to transmit the screen display to the IDE | Input      | Enabling this consumes more memory, implemented via WBC functionality |
| quality  | Sets JPEG compression quality          | Input      | Only valid when `to_ide=True`, range [10-100], default 90 |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### deinit

**Description**

Performs deinitialization. The deinit method closes the entire Display pipeline, including the VO module, DSI module, and LCD/HDMI.

**Syntax**

```python
deinit()
```

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### inited

**Description**

Queries whether the Display module has been initialized.

**Syntax**

```python
inited()
```

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| bool   | `True` indicates initialized, `False` indicates not initialized |

### list_modes

**Description**

Returns the display modes supported by the current firmware. Each mode contains the `type`, `width`, `height`, and `fps` parameters accepted by [init](#init). This method can be called before the Display module is initialized.

The returned results only contain display device types enabled when compiling the firmware. The `type` field is the name of the corresponding Display constant, for example `"Display.ST7701"`.

**Syntax**

```python
list_modes()
```

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| list | A list of display mode dictionaries. Each dictionary contains `type`, `width`, `height`, and `fps`. |

**Example**

```python
for mode in Display.list_modes():
    print(mode)

# Select the corresponding Display constant from the printed modes.
Display.init(Display.ST7701, to_ide=True)
```

### config_layer

**Description**

Configures the properties of a display layer. This method is typically called before binding a layer, used to set the display parameters of the layer.

**Syntax**

```python
config_layer(rect, pix_format, layer, alpha=255, flag=0)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| rect     | Display area (x, y, w, h)          | Input      | Required, in tuple form |
| pix_format | Image pixel format                | Input      | See [pix_format](#pix_format) |
| layer    | [Display layer](#layer) ID           | Input      | Required, specifies the layer to configure |
| alpha    | Layer blending transparency                | Input      | Range 0-255, default 255 (opaque) |
| flag     | Display [flags](#flag)             | Input      | Default 0 |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| int    | Configured layer ID                   |

### bind_layer

**Description**

Binds the output of the `sensor` or `vdec` module to the screen display. It continuously displays images without requiring manual user intervention.

**Syntax**

```python
bind_layer(src, rect, pix_format, layer, alpha=255, flag=0)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| src      | Source channel information (mod, dev, chn)    | Input      | Can be obtained via `sensor.bind_info()`, in tuple format |
| rect     | Display area (x, y, w, h)          | Input      | Can be obtained via `sensor.bind_info()` |
| pix_format | Image pixel format                | Input      | Can be obtained via `sensor.bind_info()` |
| layer    | [Display layer](#layer) bound to Display | Input      | Can be bound to `video` or `osd` layers |
| alpha    | Layer blending transparency                | Input      | Range 0-255, default 255 |
| flag     | Display [flags](#flag)             | Input      | Default 0 |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### unbind_layer

**Description**

Unbinds the binding relationship of the specified layer.

**Syntax**

```python
unbind_layer(layer)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| layer    | [Display layer](#layer) ID           | Input      | Required |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| bool   | `True` indicates successful unbinding, `False` indicates failure |

### disable_layer

**Description**

Disables the specified display layer.

**Syntax**

```python
disable_layer(layer)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| layer    | [Display layer](#layer) ID           | Input      | Required |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### show_image

**Description**

Displays an image on the screen.

**Syntax**

```python
show_image(img, x=0, y=0, layer=Display.LAYER_OSD0, alpha=None, pixel_format=None, flag=0)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| img      | Image object to display             | Input      | Required |
| x        | x value of starting coordinate              | Input      | Default 0 |
| y        | y value of starting coordinate              | Input      | Default 0 |
| layer    | Display on [specified layer](#layer)       | Input      | Only supports OSD layers, default `LAYER_OSD0` |
| alpha    | Layer blending transparency               | Input      | Range 0-255, `None` means use the layer's original setting |
| pixel_format | Image pixel format             | Input      | `None` means use the image's original format, see [pix_format](#pix_format) |
| flag     | Display [flags](#flag)            | Input      | Default 0 |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### width

**Description**

Gets the display width of the screen or a specific layer.

**Syntax**

```python
width(layer=None)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| layer    | Specifies the [display layer](#layer) to get the width of | Input      | Optional, if not specified, gets the resolution width of the screen |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| width  | Width information of the screen or display layer, in pixels |

### height

**Description**

Gets the display height of the screen or a specific layer.

**Syntax**

```python
height(layer=None)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| layer    | Specifies the [display layer](#layer) to get the height of | Input      | Optional, if not specified, gets the resolution height of the screen |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| height | Height information of the screen or display layer, in pixels |

### fps

**Description**

Gets the current display frame rate.

**Syntax**

```python
fps()
```

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| int    | Current display frame rate, in fps        |

### writeback

**Description**

Queries or sets the WriteBack (WBC) functionality status. WBC is used to read back the screen display content, typically used for transmission to the IDE display.

**Syntax**

```python
writeback(enable=None)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| enable   | Sets WBC functionality status             | Input      | Optional, `True` means enable, `False` means disable. No parameter means query current status |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| bool   | When querying, returns the current WBC status; when setting, returns the operation result |

### writeback_dump

**Description**

Captures one frame of display content from WBC. Requires `to_ide=True` to be set during [init](#init) and WBC functionality to be enabled.

**Syntax**

```python
writeback_dump(timeout=1000)
```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| timeout  | Timeout duration (milliseconds)              | Input      | Default 1000ms |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| object | Returns an object containing video frame information        |

## Data Structure Description

### type

| Type    | Parameter Value | Notes                              |
|---------|-----------------------------------|-----------------------------------|
| VIRT    | 640x480@90                        | *Default* <br> Dedicated to `IDE` debugging; nothing is shown on an external screen <br> The resolution (64x64)-(4096x4096) and frame rate (1-200) can be customized |
| DEBUGGER | | Dedicated to the debug screen |
| ST7701  | Display.init(Display.ST7701, width = 800, height = 480) | *Default*<br>800x480 |
|         | Display.init(Display.ST7701, width = 480, height = 800) | 480x800 |
|         | Display.init(Display.ST7701, width = 854, height = 480) | 854x480 |
|         | Display.init(Display.ST7701, width = 480, height = 854) | 480x854 |
|         | Display.init(Display.ST7701, width = 640, height = 480) | 640x480 |
|         | Display.init(Display.ST7701, width = 480, height = 640) | 480x640 |
|         | Display.init(Display.ST7701, width = 368, height = 544) | 368x544 |
|         | Display.init(Display.ST7701, width = 544, height = 368) | 544x368 |
| HX8399  | Display.init(Display.HX8399, width = 1920, height = 1080) | *Default*<br>1920x1080 |
|         | Display.init(Display.HX8399, width = 1080, height = 1920) | 1920x1080 |
| ILI9806 | Display.init(Display.ILI9806, width = 800, height = 480) | *Default*<br>800x480 |
|         | Display.init(Display.ILI9806, width = 480, height = 800) | 480x800 |
| LT9611  | Display.init(Display.LT9611, width = 1920, height = 1080, fps = 30) | *Default*<br>1920x1080@30 |
|         | Display.init(Display.LT9611, width = 1920, height = 1080, fps = 60) | 1920x1080@60 |
|         | Display.init(Display.LT9611, width = 1280, height = 720, fps = 60) | 1280x720@60 |
|         | Display.init(Display.LT9611, width = 1280, height = 720, fps = 50) | 1280x720@50 |
|         | Display.init(Display.LT9611, width = 1280, height = 720, fps = 30) | 1280x720@30 |
|         | Display.init(Display.LT9611, width = 640, height = 480, fps = 60) | 640x480@60 |
| ILI9881 | Display.init(Display.ILI9881, width = 1280, height = 800) | *Default*<br>1280x800 |
|         | Display.init(Display.ILI9881, width = 800, height = 1280) | 800x1280 |
| NT35516 | Display.init(Display.NT35516, width=960, height=536) | *Default*<br>960x536 |
|         | Display.init(Display.NT35516, width=536, height=960) | 536x960 |
| NT35532 | Display.init(Display.NT35532, width=1920, height=1080) | *Default*<br>1920x1080 |
|         | Display.init(Display.NT35532, width=1080, height=1920) | 1080x1920 |
| GC9503  | Display.init(Display.GC9503, width=800, height=480) | *Default*<br>800x480 |
|         | Display.init(Display.GC9503, width=480, height=800) | 480x800 |
| ST7102  | Display.init(Display.ST7102, width=640, height=480) | *Default*<br>640x480 |
|         | Display.init(Display.ST7102, width=480, height=640) | 480x640 |
| AML020T | Display.init(Display.AML020T, width=480, height=360) | *Default*<br>480x360 |
|         | Display.init(Display.AML020T, width=360, height=480) | 360x480 |
| JD9852  | Display.init(Display.JD9852, width=320, height=240) | *Default*<br>320x240 |
|         | Display.init(Display.JD9852, width=240, height=320) | 240x320 |
| ST7789  | Display.init(Display.ST7789, width=320, height=240) | *Default*<br>320x240 |
|         | Display.init(Display.ST7789, width=240, height=320) | 240x320 |

### layer

The K230 provides 3 video layers and 4 OSD layers, classified as follows:

| Display Layer | Constant Name | Description | Supported Formats |
|--------|--------|------|----------|
| Video layer 1 | `Display.LAYER_VIDEO1` | Recommended for displaying video data | Only supports `YUV420SP` |
| Video layer 2 | `Display.LAYER_VIDEO2` | Recommended for displaying video data | Only supports `YUV420SP` |
| Video layer 3 | `Display.LAYER_VIDEO3` | Recommended for displaying video data | Only supports `YUV420SP` |
| OSD layer 0 | `Display.LAYER_OSD0` | Graphics overlay layer | Only supports the RGB color space |
| OSD layer 1 | `Display.LAYER_OSD1` | Graphics overlay layer | Only supports the RGB color space |
| OSD layer 2 | `Display.LAYER_OSD2` | Graphics overlay layer | Only supports the RGB color space |
| OSD layer 3 | `Display.LAYER_OSD3` | Graphics overlay layer | Only supports the RGB color space |

### flag

| Flag | Constant Name | Description |
|------|--------|------|
| No rotation | `Display.FLAG_ROTATION_NONE` or `0` | No rotation is applied |
| Rotate 0 degrees | `Display.FLAG_ROTATION_0` | Rotate by 0 degrees |
| Rotate 90 degrees | `Display.FLAG_ROTATION_90` | Rotate by 90 degrees |
| Rotate 180 degrees | `Display.FLAG_ROTATION_180` | Rotate by 180 degrees |
| Rotate 270 degrees | `Display.FLAG_ROTATION_270` | Rotate by 270 degrees |
| No mirroring | `Display.FLAG_MIRROR_NONE` or `0` | No mirroring is applied |
| Horizontal mirroring | `Display.FLAG_MIRROR_HOR` | Mirror horizontally |
| Vertical mirroring | `Display.FLAG_MIRROR_VER` | Mirror vertically |
| Horizontal and vertical mirroring | `Display.FLAG_MIRROR_BOTH` | Mirror both horizontally and vertically |

### pix_format

| Color Format | Constant Name | Description |
|---------|--------|------|
| Grayscale | `image.GRAYSCALE` or `PIXFORMAT_GRAYSCALE` | 8-bit grayscale format, 1 byte per pixel |
| RGB565 | `image.RGB565` or `PIXFORMAT_RGB565` | RGB format, 16 bits/pixel (5:6:5) |
| ARGB8888 | `image.ARGB8888` or `PIXFORMAT_ARGB8888` | ARGB format, 32 bits/pixel (A:R:G:B) |
| ABGR8888 | `image.ABGR8888` or `PIXFORMAT_ABGR8888` | ABGR format, 32 bits/pixel (A:B:G:R) |
| RGBA8888 | `image.RGBA8888` or `PIXFORMAT_RGBA8888` | RGBA format, 32 bits/pixel (R:G:B:A) |
| BGRA8888 | `image.BGRA8888` or `PIXFORMAT_BGRA8888` | BGRA format, 32 bits/pixel (B:G:R:A) |
| RGB888 | `image.RGB888` or `PIXFORMAT_RGB888` | RGB format, 24 bits/pixel (R:G:B) |
| BGR888 | `image.BGR888` or `PIXFORMAT_BGR888` | BGR format, 24 bits/pixel (B:G:R) |

## Notes

1. **Layer support**: `show_image` only supports OSD layers. To use multiple OSD layers, set the `osd_num` parameter in `init`.
1. **Image size**: when calling `show_image`, the image size must not exceed the screen resolution.
1. **Rotation handling**: some screen types (such as the 368x544 mode of the ST7701) have a difference between the hardware size and the application size; the API handles this conversion automatically.
1. **WBC function**: to capture screen content with `writeback_dump`, `to_ide=True` must be set in `init`.
1. **IDE preview flicker**: when using a large resolution together with `to_ide=True` to send the picture to the IDE preview, the picture occasionally flickers. This is a known issue and will be fixed in a later release.

## Example Programs

### Basic Display Example

```python
from media.display import *
from media.media import *
import os, time, image

# Use the LCD as the display output
Display.init(Display.ST7701, width=800, height=480, to_ide=True)
# Initialize the media manager
MediaManager.init()

# Create an image for drawing
img = image.Image(800, 480, image.RGB565)
img.clear()
img.draw_string_advanced(0, 0, 32, "Hello World!，你好世界！！！", color=(255, 0, 0))

Display.show_image(img)

try:
    while True:
        time.sleep(1)
        os.exitpoint()
except KeyboardInterrupt as e:
    print("User stopped: ", e)
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

# Initialize the sensor
sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=800, height=480)
sensor.set_pixformat(Sensor.RGB565)

# Get the sensor binding information
bind_info = sensor.bind_info()

# Configure and bind the display layer
Display.config_layer(rect=(0, 0, 800, 480), 
                     pix_format=bind_info[2], 
                     layer=Display.LAYER_VIDEO1)
Display.bind_layer(src=bind_info[0], 
                   rect=bind_info[1], 
                   pix_format=bind_info[2], 
                   layer=Display.LAYER_VIDEO1)

# Initialize the display
Display.init(Display.ST7701, width=800, height=480)
MediaManager.init()

# Start the sensor
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
