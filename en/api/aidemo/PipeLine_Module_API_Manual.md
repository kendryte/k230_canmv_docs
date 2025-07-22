# PipeLine Module API Manual

## Overview

This manual is intended to guide developers to build a complete Media process when developing AI Demos using MicroPython, achieving the functions of acquiring images from the Camera and displaying AI inference results. This module encapsulates the default configuration of a single camera with dual channels. One channel directly sends the images from the Camera to the Display module for display; the other channel uses the `get_frame` interface to obtain a frame of image for use by the AI program.

## API Introduction

### init

**Description**

The PipeLine constructor, which initializes the resolution of the images acquired by the AI program and the parameters related to display.

**Syntax**  

```python
from libs.PipeLine import PipeLine

pl=PipeLine(rgb888p_size=[1920,1080],display_mode='hdmi',display_size=None,osd_layer_num=1,debug_mode=0)
```

**Parameters**  

| Parameter Name | Description | Input / Output | Remarks |
|----------|-------------------------------|-----------|------|
| rgb888p_size | The input image resolution of the AI program, of list type, including width and height, such as [1920,1080] | Input | Default is [224,224], determined by the AI program |
| display_size | The display resolution, of list type, including width and height, such as [1920,1080]. If it is None, it is determined by the display screen; otherwise, it is set according to the input. | Input | Default is None, determined by the display screen |
| display_mode | The display mode, supporting `hdmi` and `lcd`, of str type | Input | Default is `lcd`, determined by the display configuration |
| osd_layer_num| The number of OSD display layers, the number of layers superimposed by the user program on the original image | Input | Default is 1 |
| debug_mode   | The debugging timing mode, 0 for timing, 1 for no timing, of int type | Input | Default is 0 |

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| PipeLine | PipeLine instance |

### create

**Description**

The PipeLine initialization function, which initializes the Sensor/Display/OSD configuration in the Media process.

**Syntax**  

```python
# Default configuration
pl.create()
# Users can also create an instance and pass it in by themselves
from media.sensor import *
sensor=Sensor()
pl.create(sensor=sensor)
```

**Parameters**  

| Parameter Name | Description | Input / Output | Remarks |
|----------|-------------------------------|-----------|------|
| sensor   | Sensor instance. Users can create a sensor instance externally and pass it in. | Input | Optional, there are default configurations for different development boards |
| hmirror  | Horizontal mirroring parameter | Input | Optional, the default is `None`, determined by the default configuration of different development boards; when setting, it is of bool type, set to True or False |
| vflip    | Vertical flipping parameter | Input | Optional, the default is `None`, determined by the default configuration of different development boards; when setting, it is of bool type, set to True or False |
| fps      | Sensor frame rate parameter | Input | Optional, the default is 60, used to set the frame rate of the Sensor |

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| None |  |

### get_frame

**Description**

Obtain a frame of image for use by the AI program. The resolution of the obtained image is the rgb888p_size set by the PipeLine constructor, and the image format is Sensor.RGBP888. It is converted to the ulab.numpy.ndarray format when returned.

**Syntax**  

```python
img=pl.get_frame()
```

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| img | Image data in the format of ulab.numpy.ndarray with a resolution of rgb888p_size |

### show_image

**Description**

Superimpose and display the AI results drawn on `pl.osd_img` on the Display. `pl.osd_img` is a blank image in the format of `image.ARGB8888` initialized by the `create` interface, used for drawing AI results.

**Syntax**  

```python
pl.show_image()
```

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| None |  |

### get_display_size

**Description**

Get the width and height of the current screen configuration.

**Syntax**  

```python
display_size=pl.get_display_size()
```

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| list | Return the display width and height [display_width, display_height] of the screen configuration |

### destroy

**Description**

De-initialize the PipeLine instance.

**Syntax**  

```python
img=pl.destroy()
```

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| None |  |

## Example Program

The following is an example program:

```python
from libs.PipeLine import PipeLine
from libs.Utils import ScopedTiming
from media.media import *
import gc
import sys,os

if __name__ == "__main__":
    # Display mode, default is "hdmi", you can choose "hdmi" or "lcd"
    display_mode="hdmi"
    # Initialize PipeLine for image processing process
    pl = PipeLine(rgb888p_size=[1920,1080], display_mode=display_mode)
    pl.create()  # Create a PipeLine instance
    display_size = pl.get_display_size()
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # Get the current frame data
            print(img.shape)
            gc.collect()                    # Garbage collection
    pl.destroy()                            # Destroy the PipeLine instance
```

In the above code, a frame of image with a resolution of rgb888p_size is obtained through the `pl.get_frame()` interface. The type is ulab.numpy.ndarray, and the arrangement is CHW. Based on this code, you can focus on the operations of the AI inference part.
