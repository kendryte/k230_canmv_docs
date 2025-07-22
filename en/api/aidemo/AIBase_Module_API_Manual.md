# AIBase Module API Manual

## Overview

This manual aims to guide developers in using MicroPython to develop AI Demos by constructing a complete AI inference process, which includes loading models, preprocessing, inference, obtaining model outputs, and post-processing. The module encapsulates the inference process of a single model, wrapping preprocessing, inference, and output retrieval operations within the framework, allowing users to focus only on preprocessing configuration and post-processing when developing AI applications.

## API Introduction

### init

**Description**

AIBase constructor, initializes AI program to get image resolution and display-related parameters.

**Syntax**

```python
from libs.AIBase import AIBase

aibase = AIBase(kmodel_path="**.kmodel", model_input_size=[224,224], rgb888p_size=[1280,720], debug_mode=0)
```

**Parameters**

| Parameter Name | Description | Input / Output | Note |
|----------------|-------------|----------------|------|
| kmodel_path    | kmodel model path | Input | Required |
| model_input_size | Model input resolution, list type, including width and height, e.g., [512,512] | Input | Required |
| rgb888p_size   | AI program input image resolution, list type, including width and height, e.g., [1280,720] | Input | Required |
| debug_mode     | Debug timing mode, 0 for timing, 1 for no timing, int type | Input | Default is 0 |

**Return Value**

| Return Value | Description | Note |
|--------------|-------------|------|
| AIBase       | AIBase instance | This class is generally inherited by subclasses to write AI Demo classes for different scenarios |

### get_kmodel_inputs_num

**Description**

Get the number of inputs for the kmodel.

**Syntax**

```python
aibase.get_kmodel_inputs_num()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| inputs_num   | Number of kmodel inputs |

### get_kmodel_outputs_num

**Description**

Get the number of outputs for the kmodel.

**Syntax**

```python
aibase.get_kmodel_outputs_num()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| outputs_num  | Number of kmodel outputs |

### preprocess

**Description**

Call the ai2d method defined in the subclass to perform preprocessing. If preprocessing cannot be achieved with ai2d or is not needed, it must be overridden in the subclass.

**Syntax**

```python
aibase.preprocess(input_np)
```

**Parameters**

| Parameter Name | Description | Input / Output | Note |
|----------------|-------------|----------------|------|
| input_np       | `ulab.numpy.ndarray` format input data, shape must be consistent with the configuration in `Ai2d.build` | Input | Required |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| input_tensors | List of input tensors obtained after ai2d preprocessing |

### inference

**Description**

Method to perform inference using kmodel and obtain model outputs.

**Syntax**

```python
results = aibase.inference()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| results      | List of kmodel inference outputs, each output is in `ulab.numpy.ndarray` format |

### postprocess

**Description**

Definition of post-processing interface. Since different AI applications require different post-processing steps, this method must be overridden in the subclass.

**Syntax**

```python
aibase.postprocess()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### run

**Description**

The complete process of single-model inference, including preprocessing, inference, output retrieval, and post-processing, returning post-processing output for drawing results on Display.

**Syntax**

```python
aibase.run(input_np)
```

**Parameters**

| Parameter Name | Description | Input / Output | Note |
|----------------|-------------|----------------|------|
| input_np       | `ulab.numpy.ndarray` format input data, shape must be consistent with the configuration in `Ai2d.build` | Input | Required |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### deinit

**Description**

AIBase deinitialization method, destroys the kpu instance and releases memory.

**Syntax**

```python
aibase.deinit()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

## Example Program

```{attention}
The AIBase class is generally not used alone. It serves as a parent class for AI Demo application development, providing basic interfaces. Subclasses inherit AIBase and rewrite some methods according to task types to develop specific scenarios. During development, the draw_result method must be defined in the subclass to draw results according to the task.
```

Below is a face detection example program:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
import os, sys, gc, time, random, utime
import ujson
from media.media import *
from time import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import aidemo

# Custom face detection class, inheriting from AIBase base class
class FaceDetectionApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, anchors, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)  # Call the base class constructor
        self.kmodel_path = kmodel_path  # Model file path
        self.model_input_size = model_input_size  # Model input resolution
        self.confidence_threshold = confidence_threshold  # Confidence threshold
        self.nms_threshold = nms_threshold  # NMS (Non-Maximum Suppression) threshold
        self.anchors = anchors  # Anchor data for object detection
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]  # Sensor image resolution for AI, aligned to 16 for width
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]  # Display resolution, aligned to 16 for width
        self.debug_mode = debug_mode  # Debug mode
        self.ai2d = Ai2d(debug_mode)  # Instantiate Ai2d for model preprocessing
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)  # Set Ai2d input-output format and type

    # Configure preprocessing operations, using pad and resize here. Ai2d supports crop/shift/pad/resize/affine. Check /sdcard/app/libs/AI2D.py for details.
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):  # Timer, activated if debug_mode > 0
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size  # Initialize ai2d preprocessing config, default is sensor size for AI, can be modified by setting input_image_size
            top, bottom, left, right = self.get_padding_param()  # Get padding parameters
            self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])  # Pad edges
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)  # Resize image
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]], [1,3,self.model_input_size[1],self.model_input_size[0]])  # Build preprocessing flow

    # Custom post-process for the current task, results is a list of model output arrays, using aidemo's face_det_post_process interface here
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
            post_ret = aidemo.face_det_post_process(self.confidence_threshold, self.nms_threshold, self.model_input_size[1], self.anchors, self.rgb888p_size, results)
            if len(post_ret) == 0:
                return post_ret
            else:
                return post_ret[0]

    # Draw detection results on the screen
    def draw_result(self, pl, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            if dets:
                pl.osd_img.clear()  # Clear OSD image
                for det in dets:
                    # Convert detection box coordinates to display resolution coordinates
                    x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                    x = x * self.display_size[0] // self.rgb888p_size[0]
                    y = y * self.display_size[1] // self.rgb888p_size[1]
                    w = w * self.display_size[0] // self.rgb888p_size[0]
                    h = h * self.display_size[1] // self.rgb888p_size[1]
                    pl.osd_img.draw_rectangle(x, y, w, h, color=(255, 255, 0, 255), thickness=2)  # Draw rectangle
            else:
                pl.osd_img.clear()

    # Get padding parameters
    def get_padding_param(self):
        dst_w = self.model_input_size[0]  # Model input width
        dst_h = self.model_input_size[1]  # Model input height
        ratio_w = dst_w / self.rgb888p_size[0]  # Width scaling ratio
        ratio_h = dst_h / self.rgb888p_size[1]  # Height scaling ratio
        ratio = min(ratio_w, ratio_h)  # Choose the smaller scaling ratio
        new_w = int(ratio * self.rgb888p_size[0])  # New width
        new_h = int(ratio * self.rgb888p_size[1])  # New height
        dw = (dst_w - new_w) / 2  # Width difference
        dh = (dst_h - new_h) / 2  # Height difference
        top = int(round(0))
        bottom = int(round(dh * 2 + 0.1))
        left = int(round(0))
        right = int(round(dw * 2 - 0.1))
        return top, bottom, left, right

if __name__ == "__main__":
    # Display mode, default is "hdmi", options are "hdmi" and "lcd"
    display_mode = "hdmi"
    # k230 remains unchanged, k230d can be adjusted to [640,360]
    rgb888p_size = [1920, 1080]

    if display_mode == "hdmi":
        display_size = [1920, 1080]
    else:
        display_size = [800, 480]
    # Set model path and other parameters
    kmodel_path = "/sdcard/examples/kmodel/face_detection_320.kmodel"
    # Other parameters
    confidence_threshold = 0.5
    nms_threshold = 0.2
    anchor_len = 4200
    det_dim = 4
    anchors_path = "/sdcard/examples/utils/prior_data_320.bin"
    anchors = np.fromfile(anchors_path, dtype=np.float)
    anchors = anchors.reshape((anchor_len, det_dim))

    # Initialize PipeLine for image processing flow
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()  # Create PipeLine instance
    # Initialize custom face detection instance
    face_det = FaceDetectionApp(kmodel_path, model_input_size=[320, 320], anchors=anchors, confidence_threshold=confidence_threshold, nms_threshold=nms_threshold, rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    face_det.config_preprocess()  # Configure preprocessing

    try:
        while True:
            os.exitpoint()                      # Check for exit signal
            with ScopedTiming("total", 1):
                img = pl.get_frame()            # Get current frame data
                res = face_det.run(img)         # Infer current frame
                face_det.draw_result(pl, res)   # Draw results
                pl.show_image()                 # Display results
                gc.collect()                    # Garbage collection
    except Exception as e:
        sys.print_exception(e)                  # Print exception info
    finally:
        face_det.deinit()                       # Deinitialize
        pl.destroy()                            # Destroy PipeLine instance
```

## Development Tips

For common data type conversions in development, here are corresponding examples for reference.

> **Tips:**
>
> Converting Image object to `ulab.numpy.ndarray`:
>
> ```python
> import image
> img.to_rgb888().to_numpy_ref() # Returns an array in HWC layout
> ```
>
> Converting `ulab.numpy.ndarray` to Image object:
>
> ```python
> import ulab.numpy as np
> import image
> img_np = np.zeros((height, width, 4), dtype=np.uint8)
> img = image.Image(width, height, image.ARGB8888, alloc=image.ALLOC_REF, data=img_np)
> ```
>
> Converting `ulab.numpy.ndarray` to tensor type:
>
> ```python
> import ulab.numpy as np
> import nncase_runtime as nn
> img_np = np.zeros((height, width, 4), dtype=np.uint8)
> tensor = nn.from_numpy(img_np)
> ```
>
> Converting tensor type to `ulab.numpy.ndarray`:
>
> ```python
> import ulab.numpy as np
> import nncase_runtime as nn
> img_np = tensor.to_numpy()
> ```
