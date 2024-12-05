# 5.1 PipeLine Module API Manual

## 1. Overview

This manual aims to guide developers in using MicroPython to develop AI Demos by constructing a complete Media pipeline to achieve the functionality of capturing images from a Camera and displaying AI inference results. The module encapsulates a single-camera dual-channel default configuration, with one channel sending the Camera's images directly to the Display module, and the other channel using the `get_frame` interface to obtain an image frame for the AI program.

## 2. API Introduction

### 2.1 init

**Description**

The PipeLine constructor, which initializes the resolution for image acquisition by the AI program and parameters related to display.

**Syntax**

```python
from libs.PipeLine import PipeLine

pl = PipeLine(rgb888p_size=[1920,1080], display_size=[1920,1080], display_mode='hdmi', debug_mode=0)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------------|-------------|----------------|-------|
| rgb888p_size   | The input image resolution for the AI program, a list type including width and height, such as [1920,1080] | Input | Default is [224,224], determined by the AI program |
| display_size   | Display resolution, a list type including width and height, such as [1920,1080] | Input | Default is [1920,1080], determined by the display screen |
| display_mode   | Display mode, supports `hdmi` and `lcd`, string type | Input | Default is `lcd`, based on display configuration |
| debug_mode     | Debug timing mode, 0 for timing, 1 for no timing, integer type | Input | Default is 0 |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| PipeLine     | PipeLine instance |

### 2.2 create

**Description**

PipeLine initialization function, initializes the Sensor/Display/OSD configuration in the Media pipeline.

**Syntax**

```python
pl.create()
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------------|-------------|----------------|-------|
| sensor         | Sensor instance | Input | Optional, different development boards have default configurations |
| hmirror        | Horizontal mirror parameter | Input | Optional, default is `None`, based on different development board defaults; set as bool type, True or False |
| vflip          | Vertical flip parameter | Input | Optional, default is `None`, based on different development board defaults; set as bool type, True or False |
| fps            | Sensor frame rate parameter | Input | Optional, default is 60, sets the Sensor's frame rate |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### 2.3 get_frame

**Description**

Obtains an image frame for use by the AI program, with image resolution set by the PipeLine constructor's rgb888p_size. The image format is Sensor.RGBP888, and it is converted to ulab.numpy.ndarray format upon return.

**Syntax**

```python
img = pl.get_frame()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| img          | Image data in ulab.numpy.ndarray format, with resolution of rgb888p_size |

### 2.4 show_image

**Description**

Displays the AI result drawn on `pl.osd_img` overlaid on the Display. `pl.osd_img` is a blank image initialized by the `create` interface in the `image.ARGB8888` format, used for drawing AI results.

**Syntax**

```python
pl.show_image()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### 2.5 destroy

**Description**

Deinitializes the PipeLine instance.

**Syntax**

```python
img = pl.destroy()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

## 3. Example Program

Below is an example program:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from media.media import *
import gc
import sys, os

if __name__ == "__main__":
    # Display mode, default is "hdmi", can choose between "hdmi" and "lcd"
    display_mode = "hdmi"
    if display_mode == "hdmi":
        display_size = [1920, 1080]
    else:
        display_size = [800, 480]

    # Initialize PipeLine for image processing pipeline
    pl = PipeLine(rgb888p_size=[1920, 1080], display_size=display_size, display_mode=display_mode)
    pl.create()  # Create PipeLine instance
    try:
        while True:
            os.exitpoint()                      # Check for exit signal
            with ScopedTiming("total", 1):
                img = pl.get_frame()            # Get current frame data
                print(img.shape)
                gc.collect()                    # Garbage collection
    except Exception as e:
        sys.print_exception(e)                  # Print exception information
    finally:
        pl.destroy()                            # Destroy PipeLine instance
```

In the code above, the `pl.get_frame()` interface is used to obtain an image frame with a resolution of rgb888p_size, in the format of ulab.numpy.ndarray, arranged as CHW. Based on this code, you can focus on the operations involved in AI inference.

> **Timing Tool ScopedTiming**
>
> The ScopedTiming class in the PipeLine.py module is a context manager used to measure the execution time of a code block. Context managers are created by defining a class with `__enter__` and `__exit__` methods. When using an instance of this class in a with statement, `__enter__` is called upon entering the with block, and `__exit__` is called upon leaving.
>
> ```python
> from libs.PipeLine import ScopedTiming
> 
> def test_time():
>    with ScopedTiming("test", 1):
>        ##### Code #####
>        # ...
>        ##############
> ```
