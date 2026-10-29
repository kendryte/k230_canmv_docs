# `Ai2d` Module API Manual

## Overview

This manual is intended to guide developers using MicroPython to develop AI Demos, building preprocessing pipelines to configure and execute preprocessing on input images using `nncase_runtime.ai2d`. This module encapsulates the preprocessing methods supported by `ai2d` and provides methods to build and run the preprocessing process.

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

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| debug_mode   | Debug timing mode, int type, 0 for no timing, 1 for timing | Input | Default is 0 |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| Ai2d | Ai2d instance                          |

### set_ai2d_dtype

**Description**

Sets the data type and data format of ai2d preprocessing input and output.

**Syntax**  

```python
import ulab.numpy as np

my_ai2d.set_ai2d_dtype(input_format=nn.ai2d_format.NCHW_FMT,output_format=nn.ai2d_format.NCHW_FMT,input_type=np.uint8,output_type=np.uint8)

my_ai2d.set_ai2d_dtype(nn.ai2d_format.RGB_packed, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| input_format | Preprocessing input data format   | Input      | Required, see [ai2d_format](#ai2d_format) for values |
| output_format  | Preprocessing output data format | Input      | Required, see [ai2d_format](#ai2d_format) for values |
| input_type   | Preprocessing input data type   | Input      | Required, choose `np.uint8` or `np.float` based on data type |
| output_type  | Preprocessing output data type   | Input      | Required, choose `np.uint8` or `np.float` based on data type |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### crop

**Description**

crop preprocessing configuration method.

**Syntax**  

```python
my_ai2d.crop(0,0,200,300)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| start_x | Starting pixel in the width direction, int type   | Input      | Required |
| start_y  | Starting pixel in the height direction, int type | Input      | Required |
| width   | Crop length in the width direction, int type   | Input      | Required |
| height  | Crop length in the height direction, int type   | Input      | Required |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### shift

**Description**

shift preprocessing configuration method.

**Syntax**  

```python
my_ai2d.shift(shift_val=2)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| shift_val| Number of bits to shift right, int type  | Input      | Required |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### pad

**Description**

padding preprocessing configuration method.

**Syntax**  

```python
my_ai2d.pad(paddings=[0,0,0,0,5,5,15,15],pad_mode=0,pad_val=[114,114,114])
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| paddings| list type, padding size on each side of each dimension. For 4-dimensional images (NCHW), this parameter contains 8 values, representing the padding sizes on both sides of the N/C/H/W four dimensions. Typically only the last two dimensions are padded  | Input      | Required |
| pad_mode| Only constant padding is supported, set directly to 0  | Input      | Required |
| pad_val| list type, three-channel fill value for each pixel position, e.g., [114,114,114], [0,0,0]  | Input      | Required |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### resize

**Description**

resize preprocessing configuration method.

**Syntax**  

```python
my_ai2d.resize(interp_method=nn.interp_method.tf_bilinear, interp_mode=nn.interp_mode.half_pixel)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| interp_method | resize interpolation method  | Input      | Required, determined by `interp_method` |
| interp_mode | resize mode  | Input      | Required, determined by `interp_mode`|

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### affine

**Description**

affine preprocessing configuration method.

**Syntax**  

```python
affine_matrix=[0.2159457, -0.031286, -59.5312, 0.031286, 0.2159457, -35.30719]
my_ai2d.affine(interp_method=nn.interp_method.cv2_bilinear,crop_round=0, bound_ind=0, bound_val=127, bound_smooth=1,M=affine_matrix)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| interp_method | resize interpolation method  | Input | Required|
| crop_round | Coordinate rounding method, 0 or 1, uint32_t type  | Input | Required, generally set to 0 |
| bound_ind | Boundary pixel handling mode, 0 or 1, uint32_t type  | Input | Required, generally set to 0 |
| bound_val | Boundary fill value, uint32_t type  | Input      | Required, set to 127 |
| bound_smooth | Boundary smoothing, 0 or 1, uint32_t type | Input | Required, set to 1 |
| M | vector corresponding to the affine transformation matrix, list obtained from 2*3 matrix transformation, see the example above | Input | Required|

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

### build

**Description**

Constructs the preprocessor according to the configured preprocessing methods.

**Syntax**  

```python
my_ai2d=Ai2d(debug_mode=0) 
my_ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
my_ai2d.build([1,3,512,512],[1,3,640,640])
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| ai2d_input_shape | ai2d input data shape  | Input | Required |
| ai2d_output_shape | ai2d output data shape  | Input | Required |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None    |                                  |

### run

**Description**

Executes the preprocessing process using the configured ai2d preprocessor, and returns `nncase_runtime.tensor`.

**Syntax**  

```python
ai2d_output_tensor=my_ai2d.run(img)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| input_np | Preprocessing input data, `ulab.numpy.ndarray` type  | Input | Required |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| ai2d_output_tensor    | Data after ai2d preprocessing   |

```{admonition} Note
:class: warning
`run` returns the output tensor **reused** by the `Ai2d` instance; the next `run` will directly overwrite its contents. Therefore, do not `release()` the tensor yourself, and do not save its reference across frames; if you need to keep the result of a certain frame, please copy it out first.
```

### deinit

**Description**

Releases the builder, input/output tensors, and ai2d native objects held by the `Ai2d` instance. Must be called when the AI program exits or when the preprocessing configuration needs to be rebuilt.

**Syntax**  

```python
my_ai2d.deinit()
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

```{admonition} Tip
:class: note
- Successfully released resources can have `deinit()` called repeatedly without error.
- If a resource fails to be released, `Ai2d` will retain it for the next `deinit()` retry and throw the first failed exception; the remaining resources will still be attempted to be released.
- Custom AI classes that inherit `AIBase` and create **multiple** `Ai2d` instances (e.g., detection + alignment two-level preprocessing) need to override `deinit()` to release them one by one, then call `super().deinit()`, refer to [AI Demo Documentation](../../example/ai/ai_demo_user_manual.md).
```

## Data Structure Description

### ai2d_format

The values for the `input_format` / `output_format` parameters of `set_ai2d_dtype`, there are 6 in total, all located under `nn.ai2d_format`:

| Constant                     | Meaning                       | Can be Input | Can be Output |
| ---------------------------- | ----------------------------- | ------------ | ------------- |
| `nn.ai2d_format.YUV420_NV12` | YUV420 NV12 format            | ✅ | ✅ |
| `nn.ai2d_format.YUV420_NV21` | YUV420 NV21 format            | ✅ | ✅ |
| `nn.ai2d_format.YUV420_I420` | YUV420 I420 format            | ✅ | ✅ |
| `nn.ai2d_format.NCHW_FMT`    | NCHW planar layout (RGB planar) | ✅ | ✅ |
| `nn.ai2d_format.RGB_packed`  | HWC packed layout (RGB packed) | ✅ | ✅ |
| `nn.ai2d_format.RAW16`       | 16-bit single channel, scenarios such as depth maps | ✅ | ✅ |

Common input/output combinations:

| Input Format  | Output Format               | Description                                   |
| ------------- | --------------------------- | --------------------------------------------- |
| `YUV420_NV12` | `NCHW_FMT` / `YUV420_NV12` | Camera YUV data directly converted to model input |
| `YUV420_NV21` | `NCHW_FMT` / `YUV420_NV21` |                                               |
| `YUV420_I420` | `NCHW_FMT` / `YUV420_I420` |                                               |
| `NCHW_FMT`    | `NCHW_FMT`                  | **Most commonly used**, the RGBP888 data obtained by `pl.get_frame()` is in this layout |
| `RGB_packed`  | `NCHW_FMT` / `RGB_packed`  | HWC data (such as RGB888 obtained by `to_numpy_ref()`) converted to planar layout |
| `RAW16`       | `RAW16` / `NCHW_FMT`        | Used with `shift` to handle 16-bit data such as depth maps |

```{admonition} Note
:class: warning
The constant names in the table must be written exactly as shown. There is no constant such as `nn.ai2d_format.RGB_planar`; please use `NCHW_FMT` for planar layout.
```

### interp_method

The interpolation method in the resize preprocessing method. Listed as follows:

| Method                          | Description                              | Notes          |
|---------------------------------|------------------------------------------|----------------|
| nn.interp_method.tf_nearest     | tf's nearest neighbor interpolation      |                |
| nn.interp_method.tf_bilinear    | tf's bilinear interpolation              |                |
| nn.interp_method.cv2_nearest    | cv2's nearest neighbor interpolation     |                |
| nn.interp_method.cv2_bilinear   | cv2's bilinear interpolation             |                |

### interp_mode

| Mode                      | Description                  | Notes |
|---------------------------|------------------------------|-------|
| nn.interp_mode.none       | No special alignment strategy |       |
| nn.interp_mode.align_corner | Forced corner alignment      |       |
| nn.interp_mode.half_pixel | Center alignment             |       |

## Example Program

```{attention}
(1) Affine and Resize functions are mutually exclusive and cannot be enabled simultaneously;  
(2) The input format for the Shift function can only be Raw16;  
(3) Pad value is configured per channel, and the number of corresponding list elements must equal the number of channels;  
(4) When multiple functions are configured, the execution order is Crop->Shift->Resize/Affine->Pad, and parameter configuration should match this order; if this order is not met, multiple Ai2d instances need to be initialized to implement the preprocessing process;
```

The following is the example program:

```python
from libs.PipeLine import PipeLine
from libs.Utils import *
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os

if __name__ == "__main__":
    # Display mode, "auto" automatically selects the screen driver based on the development board model; can also explicitly specify "hdmi"/"lcd"/"st7701" etc.
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None

    # Initialize PipeLine for image processing workflow
    pl = PipeLine(rgb888p_size=[512,512], display_size=display_size, display_mode=display_mode)
    pl.create()  # Create PipeLine instance
    display_size = pl.get_display_size()    # Get actual display resolution after create
    my_ai2d=Ai2d(debug_mode=0) # Initialize Ai2d instance
    # Must explicitly set the input and output format and data type, Ai2d does not provide default values
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # Configure resize preprocessing method
    my_ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
    # Build preprocessing process
    my_ai2d.build([1,3,512,512],[1,3,640,640])
    try:
        while True:
            os.exitpoint()                      # Check for exit signal
            with ScopedTiming("total",1):
                img = pl.get_frame()            # Get current frame data
                print(img.shape)                # Original image shape is [3,512,512], get_frame returns CHW 3D data
                ai2d_output_tensor=my_ai2d.run(img) # Execute resize preprocessing
                ai2d_output_np=ai2d_output_tensor.to_numpy() # Type conversion
                print(ai2d_output_np.shape)        # Shape after preprocessing is [1,3,640,640]
                gc.collect()                    # Garbage collection
    except Exception as e:
        sys.print_exception(e)                  # Print exception information
    finally:
        my_ai2d.deinit()                        # Release ai2d resources
        pl.destroy()                            # Destroy PipeLine instance
```

In the above code, the resize preprocessing method is defined, with preprocessing input resolution of (512,512) and preprocessing output resolution of (640,640).
