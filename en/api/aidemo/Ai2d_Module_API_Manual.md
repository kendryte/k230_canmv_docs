# Ai2d Module API Manual

## Overview

This manual aims to guide developers in using MicroPython to develop AI Demos, construct preprocessing workflows, and implement functions to configure and execute preprocessing on input images using `nncase_runtime.ai2d`. The module encapsulates the preprocessing methods supported by `ai2d` and provides methods to construct and run the preprocessing process.

## API Introduction

### init

**Description**

Ai2d constructor.

**Syntax**

```python
from libs.AI2D import Ai2d

my_ai2d = Ai2d(debug_mode=0)
```

**Parameters**

| Parameter Name | Description                        | Input / Output | Note |
|----------------|------------------------------------|----------------|------|
| debug_mode     | Debug timing mode, 0 for timing, 1 for no timing, int type | Input | Default is 0 |

**Return Value**

| Return Value | Description                        |
|--------------|------------------------------------|
| Ai2d         | Ai2d instance                      |

### set_ai2d_dtype

**Description**

Set the data type and format for ai2d preprocessing input and output.

**Syntax**

```python
import ulab.numpy as np

my_ai2d.set_ai2d_dtype(input_format=nn.ai2d_format.NCHW_FMT, output_format=nn.ai2d_format.NCHW_FMT, input_type=np.uint8, output_type=np.uint8)

my_ai2d.set_ai2d_dtype(nn.ai2d_format.RGB_packed, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
```

**Parameters**

| Parameter Name | Description                        | Input / Output | Note |
|----------------|------------------------------------|----------------|------|
| input_format   | Preprocessing input data format    | Input          | Required, determined by `type` |
| output_format  | Preprocessing output data format   | Input          | Required, determined by `type` |
| input_type     | Preprocessing input data type      | Input          | Required, choose `np.uint8` or `np.float` |
| output_type    | Preprocessing output data type     | Input          | Required, choose `np.uint8` or `np.float` |

**Return Value**

| Return Value | Description                        |
|--------------|------------------------------------|
| None         |                                    |

### crop

**Description**

Crop preprocessing configuration method.

**Syntax**

```python
my_ai2d.crop(0, 0, 200, 300)
```

**Parameters**

| Parameter Name | Description                        | Input / Output | Note |
|----------------|------------------------------------|----------------|------|
| start_x        | Starting pixel in the width direction, int type | Input | Required |
| start_y        | Starting pixel in the height direction, int type | Input | Required |
| width          | Crop length in the width direction, int type | Input | Required |
| height         | Crop length in the height direction, int type | Input | Required |

**Return Value**

| Return Value | Description                        |
|--------------|------------------------------------|
| None         |                                    |

### shift

**Description**

Shift preprocessing configuration method.

**Syntax**

```python
my_ai2d.shift(shift_val=2)
```

**Parameters**

| Parameter Name | Description                        | Input / Output | Note |
|----------------|------------------------------------|----------------|------|
| shift_val      | Number of bits to shift right, int type | Input | Required |

**Return Value**

| Return Value | Description                        |
|--------------|------------------------------------|
| None         |                                    |

### pad

**Description**

Padding preprocessing configuration method.

**Syntax**

```python
my_ai2d.pad(paddings=[0, 0, 0, 0, 5, 5, 15, 15], pad_mode=0, pad_val=[114, 114, 114])
```

**Parameters**

| Parameter Name | Description                        | Input / Output | Note |
|----------------|------------------------------------|----------------|------|
| paddings       | List type, size of padding on both sides of each dimension for a 4D image (NCHW), this parameter contains 8 values representing the padding size for both sides of the N/C/H/W dimensions, usually only padding is done on the last two dimensions | Input | Required |
| pad_mode       | Only supports constant padding, set to 0 | Input | Required |
| pad_val        | List type, three-channel values filled at each pixel position, e.g., [114, 114, 114], [0, 0, 0] | Input | Required |

**Return Value**

| Return Value | Description                        |
|--------------|------------------------------------|
| None         |                                    |

### resize

**Description**

Resize preprocessing configuration method.

**Syntax**

```python
my_ai2d.resize(interp_method=nn.interp_method.tf_bilinear, interp_mode=nn.interp_mode.half_pixel)
```

**Parameters**

| Parameter Name | Description                        | Input / Output | Note |
|----------------|------------------------------------|----------------|------|
| interp_method  | Resize interpolation method        | Input          | Required, determined by `interp_method` |
| interp_mode    | Resize mode                        | Input          | Required, determined by `interp_mode` |

**Return Value**

| Return Value | Description                        |
|--------------|------------------------------------|
| None         |                                    |

### affine

**Description**

Affine preprocessing configuration method.

**Syntax**

```python
affine_matrix = [0.2159457, -0.031286, -59.5312, 0.031286, 0.2159457, -35.30719]
my_ai2d.affine(interp_method=nn.interp_method.cv2_bilinear, cord_round=0, bound_ind=0, bound_val=127, bound_smooth=1, M=affine_matrix)
```

**Parameters**

| Parameter Name | Description                        | Input / Output | Note |
|----------------|------------------------------------|----------------|------|
| interp_method  | Resize interpolation method        | Input          | Required |
| cord_round     | Coordinate rounding method, 0 or 1, uint32_t type | Input | Required, usually set to 0 |
| bound_ind      | Boundary pixel processing mode, 0 or 1, uint32_t type | Input | Required, usually set to 0 |
| bound_val      | Boundary fill value, uint32_t type | Input          | Required, set to 127 |
| bound_smooth   | Boundary smoothing, 0 or 1, uint32_t type | Input | Required, set to 1 |
| M              | Affine transformation matrix corresponding vector, list obtained from 2x3 matrix transformation, see example above | Input | Required |

**Return Value**

| Return Value | Description                        |
|--------------|------------------------------------|
| None         |                                    |

### build

**Description**

Construct the preprocessor according to the configured preprocessing methods.

**Syntax**

```python
my_ai2d = Ai2d(debug_mode=0) 
my_ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
my_ai2d.build([1, 3, 512, 512], [1, 3, 640, 640])
```

**Parameters**

| Parameter Name | Description                        | Input / Output | Note |
|----------------|------------------------------------|----------------|------|
| ai2d_input_shape | ai2d input data shape            | Input          | Required |
| ai2d_output_shape | ai2d output data shape          | Input          | Required |

**Return Value**

| Return Value | Description                        |
|--------------|------------------------------------|
| None         |                                    |

### run

**Description**

Execute the preprocessing process using the configured ai2d preprocessor, returning `nncase_runtime.tensor`.

**Syntax**

```python
ai2d_output_tensor = my_ai2d.run(img)
```

**Parameters**

| Parameter Name | Description                        | Input / Output | Note |
|----------------|------------------------------------|----------------|------|
| input_np       | Preprocessing input data, `ulab.numpy.ndarray` type | Input | Required |

**Return Value**

| Return Value | Description                        |
|--------------|------------------------------------|
| ai2d_output_tensor | Data after ai2d preprocessing |

## Data Structure Description

### type

| Input Format      | Output Format            | Note                |
|-------------------|--------------------------|---------------------|
| YUV420_NV12       | RGB_planar/YUV420_NV12   |                     |
| YUV420_NV21       | RGB_planar/YUV420_NV21   |                     |
| YUV420_I420       | RGB_planar/YUV420_I420   |                     |
| YUV400            | YUV400                   |                     |
| NCHW(RGB_planar)  | NCHW(RGB_planar)         |                     |
| RGB_packed        | RGB_planar/RGB_packed    |                     |
| RAW16             | RAW16/8                  | Depth map, perform shift operation |

### interp_method

Interpolation methods in the resize preprocessing method. Listed as follows:

| Method                           | Description                           | Note          |
|----------------------------------|---------------------------------------|---------------|
| nn.interp_method.tf_nearest      | tf's nearest neighbor interpolation   |               |
| nn.interp_method.tf_bilinear     | tf's bilinear interpolation           |               |
| nn.interp_method.cv2_nearest     | cv2's nearest neighbor interpolation  |               |
| nn.interp_method.cv2_bilinear    | cv2's bilinear interpolation          |               |

### interp_mode

| Mode                              | Description               | Note |
|-----------------------------------|---------------------------|------|
| nn.interp_mode.none               | No special alignment strategy |      |
| nn.interp_mode.align_corner       | Corner forced alignment   |      |
| nn.interp_mode.half_pixel         | Center alignment          |      |

## Example Program

```{attention}
(1) Affine and Resize functions are mutually exclusive and cannot be enabled simultaneously;  
(2) The input format for the Shift function can only be Raw16;  
(3) Pad value is configured per channel, and the number of elements in the corresponding list must equal the number of channels;   
(4) When multiple functions are configured, the execution order is Crop->Shift->Resize/Affine->Pad. Ensure that configuration parameters match this order. If not, multiple Ai2d instances need to be initialized to implement the preprocessing process; 
```

Below is an example program:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import gc
import sys, os

if __name__ == "__main__":
    # Display mode, default is "hdmi", can choose "hdmi" or "lcd"
    display_mode = "hdmi"
    if display_mode == "hdmi":
        display_size = [1920, 1080]
    else:
        display_size = [800, 480]

    # Initialize PipeLine for image processing workflow
    pl = PipeLine(rgb888p_size=[512, 512], display_size=display_size, display_mode=display_mode)
    pl.create()  # Create PipeLine instance
    my_ai2d = Ai2d(debug_mode=0)  # Initialize Ai2d instance
    # Configure resize preprocessing method
    my_ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
    # Construct preprocessing process
    my_ai2d.build([1, 3, 512, 512], [1, 3, 640, 640])
    try:
        while True:
            os.exitpoint()  # Check for exit signal
            with ScopedTiming("total", 1):
                img = pl.get_frame()  # Get current frame data
                print(img.shape)  # Original image shape is [1, 3, 512, 512]
                ai2d_output_tensor = my_ai2d.run(img)  # Execute resize preprocessing
                ai2d_output_np = ai2d_output_tensor.to_numpy()  # Type conversion
                print(ai2d_output_np.shape)  # Preprocessed shape is [1, 3, 640, 640]
                gc.collect()  # Garbage collection
    except Exception as e:
        sys.print_exception(e)  # Print exception information
    finally:
        pl.destroy()  # Destroy PipeLine instance
```

In the above code, the resize preprocessing method is defined, with a preprocessing input resolution of (512, 512) and a preprocessing output resolution of (640, 640).
