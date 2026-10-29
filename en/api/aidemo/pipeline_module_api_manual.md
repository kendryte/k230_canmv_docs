# `Pipeline` Module API Manual

## Overview

This manual is intended to guide developers in building a complete Media pipeline when developing AI Demos with MicroPython, implementing the functionality of capturing images from a Camera and displaying AI inference results. This module encapsulates the default configuration of a single-camera dual-channel setup: one channel sends the Camera image directly to the Display module for display; the other channel uses the `get_frame` interface to obtain a frame of image for use by the AI program.

## API Introduction

### init

**Description**

PipeLine constructor that initializes the resolution for the AI program to obtain images and display-related parameters.

**Syntax**

```python
from libs.PipeLine import PipeLine

pl=PipeLine(rgb888p_size=[1920,1080],display_mode='hdmi',display_size=None,osd_layer_num=1,debug_mode=0)
```

**Parameters**

| Parameter | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| rgb888p_size | Input image resolution for the AI program, list type, including width and height, e.g. [1920,1080] | Input | Default [224,224], depends on the AI program |
| display_mode | Display mode, str type, see the table below for values | Input | Default `hdmi`. Recommended to use `auto`, automatically selected based on the development board model |
| display_size | Display resolution, list type, including width and height, e.g. [1920,1080]; if None, depends on the display screen; otherwise, set according to input | Input | Default None, determined by the display screen |
| osd_layer_num| Number of osd display layers, the number of layers the user program overlays on the original image | Input | Default is 1 |
| debug_mode   | Debug timing mode, int type, 0 for no timing, 1 for timing | Input | Default is 0 |

💡 **display_mode values**:

| Value | Corresponding Display Driver | Description |
|------|--------------|------|
| `auto` | Determined by the development board model | **Recommended**. Based on `os.uname()[-1]`, look up a table to select the default screen driver for that board, allowing the same code to run across different boards without modification. If the board type is not included, a `ValueError` will be raised; in that case, please specify the driver explicitly |
| `hdmi` / `lt9611` | LT9611 | HDMI output, default 1920x1080 |
| `lcd` / `st7701` | ST7701 | Common MIPI LCD, default 800x480 |
| `hx8399` | HX8399 | |
| `nt35516` | NT35516 | This screen will force the sensor frame rate to be limited to 30fps |
| `nt35532` | NT35532 | |
| `gc9503` | GC9503 | |
| `aml020t` | AML020T | |
| `jd9852` | JD9852 | |
| `ili9806` | ILI9806 | |
| `virt` | VIRT | Virtual display, only displayed in CanMV IDE, customizable resolution via `display_size` |

```{admonition} Note
:class: note
Passing an unrecognized string will not throw an error and will fall back to ST7701. This behavior is preserved for backward compatibility with old code; please use the values in the table above or `auto` for new code.
```

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| PipeLine | PipeLine instance |

### create

**Description**

PipeLine initialization function, initializes Sensor/Display/OSD configuration in the Media pipeline.

**Syntax**

```python
# Default configuration
pl.create()
# Users can also create an instance and pass it in
from media.sensor import *
sensor=Sensor()
pl.create(sensor=sensor)
```

```{admonition} Tip
:class: note
It is recommended to use it with `display_mode="auto"`, so that the same script can produce correct output on different development boards:

    pl = PipeLine(rgb888p_size=[1280,720], display_mode="auto")
    pl.create()
    display_size = pl.get_display_size()   # Obtain the actual display resolution after create
```

**Parameters**

| Parameter | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| sensor   | Sensor instance; users can create a sensor instance externally and pass it in | Input | Optional; different development boards have default configurations |
| sensor_id| Sensor ID; users can configure this parameter to set the camera | Input | Optional; different development boards have default configurations |
| hmirror  | Horizontal mirror parameter | Input | Optional, default is `None`, depending on the development board default configuration; when set, it is of bool type, set to True or False |
| vflip    | Vertical flip parameter | Input | Optional, default is `None`, depending on the development board default configuration; when set, it is of bool type, set to True or False |
| fps      | sensor frame rate parameter | Input | Optional, default 60. Some development boards (`k230d_canmv_bpi_zero`, `k230_canmv_lckfb`, `k230d_canmv_atk_dnk230d`) and the `nt35516` screen will force 30fps, and this parameter will not take effect |
| to_ide   | Whether to transmit the screen display to the IDE | Input | Enabling this will consume more memory |
| crop_vertical   | Whether to adapt to vertical screen display | Input | When the sensor outputs a horizontal image but the display is a vertical screen, cropping is used to achieve vertical screen display |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| None     |                                 |

```{admonition} Note
:class: warning
- **Cannot be called repeatedly**. If PipeLine has already been initialized, calling `create()` again will raise `RuntimeError: PipeLine must be destroyed before create`. If you need to reconfigure, please call [`destroy`](#destroy) first, then `create`.
- The passed-in `sensor` instance will be taken over by PipeLine and will be stopped along with `destroy()`.
- After `create()` succeeds, the `display_size` set in the constructor will be **overridden by the actual resolution of the display driver**, so please use [`get_display_size`](#get_display_size) to obtain the display resolution after `create()`, rather than directly using the value passed in during construction.
- If any step fails during the initialization process, PipeLine will automatically roll back the requested sensor/display resources before throwing an exception, no manual cleanup is required.
```

### get_frame

**Description**

Obtain a frame of image for use by the AI program. The obtained image resolution is the rgb888p_size set by the PipeLine constructor, the image format is Sensor.RGBP888, and it is converted to the ulab.numpy.ndarray format when returned.

**Syntax**

```python
img=pl.get_frame()
```

**Parameters**

| Parameter | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| img     | Type `ulab.numpy.ndarray`, **3-dimensional CHW** data with shape `[3, height, width]`, where the width and height are determined by the `rgb888p_size` at construction time (width is 16-byte aligned). Note that it is not four-dimensional `[1,3,H,W]` |

```{admonition} Note
:class: warning
What is returned is a **reference** to the current frame, not a copy. It must be processed before the next `get_frame()` or `destroy()`; if you need to retain it across frames, please `copy()` it yourself first.
```

### show_image

**Description**

Overlay the AI result drawn on `pl.osd_img` onto the Display. `pl.osd_img` is a blank image with format `image.ARGB8888` initialized by the `create` interface, used for drawing AI results.

**Syntax**

```python
pl.show_image()
```

**Parameters**

| Parameter | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| flag | Flag bit transparently passed to `Display.show_image()` | Input | Optional, default `None` means not passed |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| None     |                                 |

### get_display_size

**Description**

Obtain the width and height of the current screen configuration.

**Syntax**

```python
display_size=pl.get_display_size()
```

**Parameters**

| Parameter | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| list    | Returns the configured display width and height [display_width,display_height] |

### destroy

**Description**

De-initialize the PipeLine instance.

**Syntax**

```python
pl.destroy()
```

**Parameters**

| Parameter | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| None    |                                  |

## Example Program

The following is an example program:

```python
from libs.PipeLine import PipeLine
from libs.Utils import ScopedTiming
from media.media import *
import gc
import sys,os

if __name__ == "__main__":
    # 显示模式，推荐"auto"由开发板型号自动选择屏驱动，也可显式指定"hdmi"/"lcd"/"st7701"等
    display_mode="auto"
    # None表示使用屏驱动的默认分辨率；需要指定时填[宽, 高]
    display_size=None

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=[1920,1080], display_mode=display_mode, display_size=display_size)
    pl.create()  # 创建PipeLine实例
    display_size = pl.get_display_size()    # create之后再取实际显示分辨率
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)                # CHW三维数据，shape为[3, height, width]
            gc.collect()                    # 垃圾回收
    pl.destroy()                            # 销毁PipeLine实例
```

In the above code, the `pl.get_frame()` interface is used to obtain a frame of image with resolution rgb888p_size, of type ulab.numpy.ndarray, arranged in CHW format. Based on this code, you can focus on the AI inference operations.

For the complete recommended writing method (including AI model creation and release), see [Two Main Loop Patterns](../../ai_dev_doc.md#main-loop-patterns).
