# AI Demo Documentation

<a id="ai-demo-list"></a>

## AI Demo Application

K230 supports a rich set of AI applications. To facilitate user experience and trial, the CanMV K230 image comes with multiple AI Demo applications built in, divided into single-model applications and multi-model applications, covering object, face, hand, human body, license plate, OCR, audio (KWS, TTS), and other application domains. Users can easily run them by opening the source code via CanMV IDE. The source code of the AI Demo applications is located in the `/CanMV/sdcard/examples/05-AI-Demo` directory. The list of AI Demo applications is as follows. Some Demos cannot run on the K230D chip due to memory limitations, please pay attention to the compatibility list.

| Demo Name                | Scenario            | Task Type   | K230 | K230D |
| ----------------------- | --------------- | ---------- | ---- | ---- |
| body_seg                | Human Body Part Segmentation    | Single-model task | ✅ | ❌ |
| dynamic_gesture         | Dynamic Gesture Recognition    | Multi-model task | ✅ | ✅ |
| eye_gaze                | Gaze Estimation        | Multi-model task | ✅ | ❌ |
| face_detection          | Face Detection        | Single-model task | ✅ | ✅ |
| face_landmark           | Face Key Points    | Multi-model task | ✅ | ✅ |
| face_liveness_rgb       | Face Liveness Detection    | Multi-model task | ✅ | ✅ |
| face_mesh               | Face 3D Mesh      | Multi-model task | ✅ | ❌ |
| face_parse              | Face Parsing        | Multi-model task | ✅ | ❌ |
| face_pose               | Face Pose        | Multi-model task | ✅ | ✅ |
| face_registration       | Face Registration        | Multi-model task | ✅ | ❌ |
| face_recognition        | Face Recognition        | Multi-model task | ✅ | ❌ |
| face_registration_lite  | Lightweight Face Registration     | Multi-model task | ✅ | ✅ |
| face_recognition_lite   | Lightweight Face Recognition     | Multi-model task | ✅ | ✅ |
| falldown_detect         | Fall Detection        | Single-model task | ✅ | ✅ |
| finger_guessing         | Finger Guessing Game        | Multi-model task | ✅ | ✅ |
| hand_detection          | Hand Detection        | Single-model task | ✅ | ✅ |
| hand_keypoint_class     | Hand Key Point Classification  | Multi-model task | ✅ | ✅ |
| hand_keypoint_detection | Hand Key Point Detection  | Multi-model task | ✅ | ✅ |
| hand_recognition        | Hand Gesture Recognition        | Multi-model task | ✅ | ✅ |
| keyword_spotting        | Keyword Wake-up      | Single-model task | ✅ | ✅ |
| multi_kws               | Multi-Command Keyword Wake-up | Single-model task | ✅ | ✅ |
| license_plate_det       | License Plate Detection        | Single-model task | ✅ | ✅ |
| license_plate_det_rec   | License Plate Recognition    | Multi-model task | ✅ | ✅ |
| license_plate_det_yolo   | YOLO License Plate Detection   | Single-model task | ✅ | ✅ |
| license_plate_det_rec_yolo| YOLO License Plate Detection + Recognition | Multi-model task | ✅ | ✅ |
| nanotracker             | Single Object Tracking      | Multi-model task | ✅ | ✅ |
| object_detect_yolov8n   | YOLOv8n Object Detection | Single-model task | ✅ | ✅ |
| ocr_det                 | OCR Detection         | Single-model task | ✅ | ❌ |
| ocr_rec                 | OCR Recognition         | Multi-model task | ✅ | ❌ |
| person_detection        | Person Detection        | Single-model task | ✅ | ✅ |
| person_keypoint_detect  | Person Key Point Detection  | Multi-model task | ✅ | ✅ |
| puzzle_game             | Puzzle Game        | Multi-model task | ✅ | ✅ |
| segment_yolov8n         | YOLOv8 Segmentation      | Single-model task | ✅ | ❌ |
| self_learning           | Self Learning          | Single-model task | ✅ | ✅ |
| space_resize            | Local Magnifier      | Multi-model task | ✅ | ✅ |
| tts_zh                  | Chinese Text-to-Speech  | Multi-model task | ✅ | ❌ |
| yolo11n_obb             | YOLO11n Rotated Object Detection| Single-model task | ✅ | ✅ |
| yolov8n_obb             | YOLOv8n Rotated Object Detection| Single-model task | ✅ | ✅ |
| yolo26_person_kp        | YOLO26 Person Key Point Detection| Single-model task | ✅ | ✅ |
| face_detect_yunet       | YuNet Face Detection    | Single-model task | ✅ | ✅ |
| face_masking_count      | Face Masking and Counting    | Single-model task | ✅ | ✅ |
| bytetrack               | ByteTrack Multi-Object Tracking | Single-model task | ✅ | ✅ |
| ocsort                  | OC-SORT Multi-Object Tracking | Single-model task | ✅ | ✅ |
| deepsort                | DeepSort Multi-Object Tracking | Multi-model task | ✅ | ✅ |
| botsort                 | BoT-SORT Multi-Object Tracking | Multi-model task | ✅ | ✅ |

```{admonition} Tip
- **Display Adaptation**: The `display_mode` of most demos has been changed to `auto`, which automatically selects the display driver according to the development board model, so no manual modification is required. For details, see the [DisplayConfig Module API Manual](../../api/aidemo/display_config_module_api_manual.md). A few scripts that have not yet been updated need to change `display_mode` to `lcd` on K230D.
- **Resolution Adaptation**: K230D has relatively little memory. To run some demos, the `rgb888p_size` must be reduced according to the script comments. The demos marked ❌ in the table cannot run on K230D due to excessive memory usage.
```

```{admonition} Note
:class: warning
The example code in this document is consistent with the example scripts on the development board. In most examples, to highlight the algorithm logic, `deinit()`/`destroy()` are placed after the `while True:` loop, and these two lines **will never actually execute**—running the demo poses no problem, but resources will not be released after the IDE stops, and the next run may fail due to insufficient nncase memory (power cycling will restore it).

When writing your own application, refer to new examples such as `bytetrack.py`, and use `try/finally` to wrap the main loop. For details, see [Two Main Loop Patterns](../../ai_dev_doc.md#main-loop-patterns).
```

## AI Demo Development Framework Introduction

### AI Demo Development Framework

To help users simplify the development of the AI part, based on the API interfaces provided by K230_CanMV, we have built a matching AI development framework. The framework structure is shown in the figure below:

![Development Framework](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/framework.png)

The Camera outputs two streams of images by default: one in YUV420SP format (Sensor.YUV420SP), provided directly to the Display for display; the other in RGBP888 format (Sensor.RGBP888), used for AI processing. The AI is mainly responsible for the pre-processing, inference, and post-processing flow of the task. After processing is complete, the results will be drawn on the OSD image instance and sent to the Display for overlay display.

```{admonition} Tip
The PipeLine process encapsulation mainly simplifies the development of vision tasks. You can use 'get_frame' to obtain a frame of image for machine vision processing; if you wish to customize the AI process, please refer to the [Face Detection](#face-detection-demo) example later in this document. For audio-related AI, please refer to the two examples keyword_spotting and tts_zh in the demo.

```

### Interface Encapsulation

To facilitate user development, based on the above framework, the general functions of obtaining images from Camera, AI2D preprocessing, and kmodel model inference are encapsulated. Please refer to the encapsulated interfaces: [AI Demo API](../../api/aidemo_libs.md)

### Application Methods and Examples

#### Overview

Users can write custom task classes that inherit from AIBase based on specific AI scenarios, and tasks can be divided into the following four categories: single-model tasks, multi-model tasks, custom preprocessing tasks, and no-preprocessing tasks. Different tasks require different code implementations, as shown in the figure below:

![Different Task Types](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/task_diff.png)

Introduction to different tasks:

| Task Type         | Task Description                                                     | Code Description                                                     |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Single-model task       | This task has only one model, and you only need to focus on the preprocessing, inference, and post-processing of that model. The preprocessing of this type of task is implemented using Ai2d, which may use one Ai2d instance or multiple Ai2d instances. The post-processing is customized based on the scenario. | Write a custom task class, mainly focusing on the config_preprocess, postprocess of the task class, and other methods required by the task such as: draw_result, etc.<br />If the task contains multiple Ai2d instances, you need to override preprocess and set the calculation process of the preprocessing stage according to the order of preprocessing. |
| Custom preprocessing task | This task has only one model, and you only need to focus on the preprocessing, inference, and post-processing of that model. The preprocessing of this type of task is not implemented using Ai2d but can be customized using ulab.numpy. The post-processing is customized based on the scenario. | Write a custom task class, mainly focusing on the preprocess, postprocess of the task class, and other methods required by the task such as: draw_result, etc. |
| No-preprocessing task     | This task has only one model and does not require preprocessing. You only need to focus on the inference and post-processing of the model. This type of task is generally used as part of a multi-model task, directly using the output of the previous model as input for inference. The post-processing is customized based on requirements. | Write a custom task class, mainly focusing on the run (the entire process of model inference, including all or some steps in preprocess, inference, postprocess), postprocess, and other methods required by the task such as: draw_results, etc. |
| Multi-model task       | This task contains multiple models, which may be in series or in other combinations. Each model basically belongs to one of the first three types of models, and finally a complete task class is used to unify the above model subtasks. | Write multiple sub-model task classes, and refer to the first three task definitions for different sub-model tasks. Different tasks focus on different methods.<br />Write a multi-model task class to unify the sub-model task classes to implement the entire scenario. |

#### Single-model task

The pseudocode structure for a single-model task is as follows:

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import os
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import gc
import sys

# Custom AI task class, inheriting from the AIBase base class
class MyAIApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        # Call the constructor of the base class
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        # Model file path
        self.kmodel_path = kmodel_path
        # Model input resolution
        self.model_input_size = model_input_size
        # Image resolution provided by the sensor to the AI, with the width aligned to a multiple of 16
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        # Display resolution, with the width aligned to a multiple of 16
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        # Whether to enable debug mode
        self.debug_mode = debug_mode
        # Instantiate Ai2d for model preprocessing
        self.ai2d = Ai2d(debug_mode)
        # Set the input and output formats and types of Ai2d
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)

    # Configure preprocessing operations. Here, resize is used. Ai2d supports crop/shift/pad/resize/affine. For details, please open /sdcard/libs/AI2D.py
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            # Initialize the ai2d preprocessing configuration. By default, it uses the size provided by the sensor to the AI. You can modify the input size by setting input_image_size
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            # Configure the resize preprocessing method
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            # Build the preprocessing pipeline
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])

    # Customize the postprocessing for the current task. results is a list of model output arrays and needs to be rewritten according to the actual task
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
           pass

    # Draw the results onto the screen. This needs to be implemented according to the task
    def draw_result(self, pl, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            pass

if __name__ == "__main__":
    # Display mode. "auto" automatically selects the display driver according to the development board model; you can also explicitly specify "hdmi"/"lcd"/"st7701", etc.
    display_mode="auto"
    # None means using the default resolution of the display driver; fill in [width, height] when specifying one
    display_size=None
    # Set the model path. Replace this with the model for the current task
    kmodel_path = "example_test.kmodel"
    rgb888p_size = [1920, 1080]
    ###### Other parameters########
    ...
    ######################

    # Initialize PipeLine for the image processing pipeline
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()  # Create the PipeLine instance
    display_size = pl.get_display_size()
    # Initialize the custom AI task instance
    my_ai = MyAIApp(kmodel_path, model_input_size=[320, 320],rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    my_ai.config_preprocess()  # Configure preprocessing
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # Get the current frame data
            res = my_ai.run(img)              # Perform inference on the current frame
            my_ai.draw_result(pl, res)        # Draw the results
            pl.show_image()                 # Display the results
            gc.collect()                    # Garbage collection
    my_ai.deinit()                          # Deinitialize
    pl.destroy()                            # Destroy the PipeLine instance

```

The following example code uses face detection:

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import time,os,sys,ujson,gc,random
import image
import aidemo

# Custom face detection class, inheriting from the AIBase base class
class FaceDetectionApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, anchors, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)  # Call the constructor of the base class
        self.kmodel_path = kmodel_path  # Model file path
        self.model_input_size = model_input_size  # Model input resolution
        self.confidence_threshold = confidence_threshold  # Confidence threshold
        self.nms_threshold = nms_threshold  # NMS (non-maximum suppression) threshold
        self.anchors = anchors  # Anchor data used for object detection
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]  # Image resolution provided by the sensor to the AI, with the width aligned to a multiple of 16
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]  # Display resolution, with the width aligned to a multiple of 16
        self.debug_mode = debug_mode  # Whether to enable debug mode
        self.ai2d = Ai2d(debug_mode)  # Instantiate Ai2d for model preprocessing
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)  # Set the input and output formats and types of Ai2d

    # Configure preprocessing operations. Here, pad and resize are used. Ai2d supports crop/shift/pad/resize/affine. For details, please open /sdcard/libs/AI2D.py
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):  # Timer, enabled when debug_mode is greater than 0
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size  # Initialize the ai2d preprocessing configuration. By default, it uses the size provided by the sensor to the AI. You can modify the input size by setting input_image_size
            top, bottom, left, right = self.get_padding_param()  # Get the padding parameters
            self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])  # Pad the edges
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)  # Resize the image
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])  # Build the preprocessing pipeline

    # Customize the postprocessing for the current task. results is a list of model output arrays. Here, the face_det_post_process interface of the aidemo library is used
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
            post_ret = aidemo.face_det_post_process(self.confidence_threshold, self.nms_threshold, self.model_input_size[1], self.anchors, self.rgb888p_size, results)
            if len(post_ret) == 0:
                return post_ret
            else:
                return post_ret[0]

    # Draw the detection results onto the screen
    def draw_result(self, pl, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            if dets:
                pl.osd_img.clear()  # Clear the OSD image
                for det in dets:
                    # Convert the coordinates of the detection box to coordinates at the display resolution
                    x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                    x = x * self.display_size[0] // self.rgb888p_size[0]
                    y = y * self.display_size[1] // self.rgb888p_size[1]
                    w = w * self.display_size[0] // self.rgb888p_size[0]
                    h = h * self.display_size[1] // self.rgb888p_size[1]
                    pl.osd_img.draw_rectangle(x, y, w, h, color=(255, 255, 0, 255), thickness=2)  # Draw the rectangle
            else:
                pl.osd_img.clear()

    # Get the padding parameters
    def get_padding_param(self):
        dst_w = self.model_input_size[0]  # Model input width
        dst_h = self.model_input_size[1]  # Model input height
        ratio_w = dst_w / self.rgb888p_size[0]  # Width scaling ratio
        ratio_h = dst_h / self.rgb888p_size[1]  # Height scaling ratio
        ratio = min(ratio_w, ratio_h)  # Select the smaller scaling ratio
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
    # Display mode. "auto" automatically selects the display driver according to the development board model; you can also explicitly specify "hdmi"/"lcd"/"st7701", etc.
    display_mode="auto"
    # None means using the default resolution of the display driver; fill in [width, height] when specifying one
    display_size=None
    # Keep k230 unchanged; k230d can be adjusted to [640,360]
    rgb888p_size = [1920, 1080]
    # Set the model path and other parameters
    kmodel_path = "/sdcard/examples/kmodel/face_detection_320.kmodel"
    # Other parameters
    confidence_threshold = 0.5
    nms_threshold = 0.2
    anchor_len = 4200
    det_dim = 4
    anchors_path = "/sdcard/examples/utils/prior_data_320.bin"
    anchors = np.fromfile(anchors_path, dtype=np.float)
    anchors = anchors.reshape((anchor_len, det_dim))

    # Initialize PipeLine for the image processing pipeline
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()  # Create the PipeLine instance
    display_size = pl.get_display_size()
    # Initialize the custom face detection instance
    face_det = FaceDetectionApp(kmodel_path, model_input_size=[320, 320], anchors=anchors, confidence_threshold=confidence_threshold, nms_threshold=nms_threshold, rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    face_det.config_preprocess()  # Configure preprocessing
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # Get the current frame data
            res = face_det.run(img)              # Perform inference on the current frame
            face_det.draw_result(pl, res)        # Draw the results
            pl.show_image()                 # Display the results
            gc.collect()                    # Garbage collection
    face_det.deinit()                          # Deinitialize
    pl.destroy()                            # Destroy the PipeLine instance
```

The pseudocode for multiple Ai2d instances is as follows:

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import os
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import gc
import sys

# Custom AI task class, inheriting from the AIBase base class
class MyAIApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        # Call the constructor of the base class
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        # Model file path
        self.kmodel_path = kmodel_path
        # Model input resolution
        self.model_input_size = model_input_size
        # Image resolution provided by the sensor to the AI, with the width aligned to a multiple of 16
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        # Display resolution, with the width aligned to a multiple of 16
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        # Whether to enable debug mode
        self.debug_mode = debug_mode
        # Instantiate Ai2d for model preprocessing
        self.ai2d_resize = Ai2d(debug_mode)
        # Set the input and output formats and types of Ai2d
        self.ai2d_resize.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
        # Instantiate Ai2d for model preprocessing
        self.ai2d_resize = Ai2d(debug_mode)
        # Set the input and output formats and types of Ai2d
        self.ai2d_resize.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
        # Instantiate Ai2d for model preprocessing
        self.ai2d_crop = Ai2d(debug_mode)
        # Set the input and output formats and types of Ai2d
        self.ai2d_crop.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)

    # Configure preprocessing operations. Here, resize and crop are used. Ai2d supports crop/shift/pad/resize/affine. For details, please open /sdcard/libs/AI2D.py
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            # Initialize the ai2d preprocessing configuration. By default, it uses the size provided by the sensor to the AI. You can modify the input size by setting input_image_size
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            # Configure the resize preprocessing method
            self.ai2d_resize.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            # Build the preprocessing pipeline
            self.ai2d_resize.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,640,640])
            # Configure the crop preprocessing method
            self.ai2d_crop.crop(0,0,320,320)
            # Build the preprocessing pipeline
            self.ai2d_crop.build([1,3,640,640],[1,3,320,320])

    # Assume that this task requires crop and resize preprocessing. The order is resize first and then crop, which does not conform to the processing order of ai2d. Therefore, two Ai2d instances need to be set up to process them separately
    def preprocess(self,input_np):
        resize_tensor=self.ai2d_resize.run(input_np)
        resize_np=resize_tensor.to_numpy()
        crop_tensor=self.ai2d_crop.run(resize_np)
        return [crop_tensor]


    # Customize the postprocessing for the current task. results is a list of model output arrays and needs to be rewritten according to the actual task
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
           pass

    # Draw the results onto the screen. This needs to be implemented according to the task
    def draw_result(self, pl, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            pass

    # Override deinit to release multiple ai2d resources
    def deinit(self):
        with ScopedTiming("deinit",self.debug_mode > 0):
            del self.ai2d_resize
            del self.ai2d_crop
            super().deinit()

if __name__ == "__main__":
    # Display mode. "auto" automatically selects the display driver according to the development board model; you can also explicitly specify "hdmi"/"lcd"/"st7701", etc.
    display_mode="auto"
    # None means using the default resolution of the display driver; fill in [width, height] when specifying one
    display_size=None
    # Set the model path. Replace this with the model for the current task
    kmodel_path = "example_test.kmodel"
    rgb888p_size = [1920, 1080]
    ###### Other parameters########
    ...
    ######################

    # Initialize PipeLine for the image processing pipeline
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()  # Create the PipeLine instance
    display_size = pl.get_display_size()
    # Initialize the custom AI task instance
    my_ai = MyAIApp(kmodel_path, model_input_size=[320, 320],rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    my_ai.config_preprocess()  # Configure preprocessing
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # Get the current frame data
            res = my_ai.run(img)              # Perform inference on the current frame
            my_ai.draw_result(pl, res)        # Draw the results
            pl.show_image()                 # Display the results
            gc.collect()                    # Garbage collection
    my_ai.deinit()                          # Deinitialize
    pl.destroy()                            # Destroy the PipeLine instance
```

#### Custom Preprocessing Task

For AI tasks that need to override the preprocessing (do not use the provided ai2d class, write the preprocessing manually), the pseudocode is as follows:

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import os
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import gc
import sys

# Custom AI task class, inherits from the AIBase base class
class MyAIApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        # Call the base class constructor
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        # Model file path
        self.kmodel_path = kmodel_path
        # Model input resolution
        self.model_input_size = model_input_size
        # Image resolution provided by the sensor to the AI, with the width aligned to 16
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        # Display resolution, with the width aligned to 16
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        # Whether to enable debug mode
        self.debug_mode = debug_mode
        # Instantiate Ai2d to implement model preprocessing
        self.ai2d = Ai2d(debug_mode)
        # Set the Ai2d input and output formats and types
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)

    # For AI tasks that do not use ai2d to complete preprocessing, use the encapsulated interfaces or ulab.numpy to implement preprocessing, and this function must be overridden in the subclass
    def preprocess(self,input_np):
        #############
        #Pay attention to the custom preprocessing process
        #############
        return [tensor]

    # Customize the postprocessing of the current task; results is a list of model output arrays and must be rewritten according to the actual task
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
           pass

    # Draw the results on the screen; this must be written according to the task
    def draw_result(self, pl, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            pass

if __name__ == "__main__":
    # Display mode; "auto" automatically selects the screen driver according to the development board model; "hdmi"/"lcd"/"st7701", etc. can also be specified explicitly
    display_mode="auto"
    # None means to use the default resolution of the screen driver; enter [width, height] when specifying one
    display_size=None
    # Set the model path; replace this with the model for the current task
    kmodel_path = "example_test.kmodel"
    rgb888p_size = [1920, 1080]
    ###### Other parameters########
    ...
    ######################

    # Initialize PipeLine for the image processing pipeline
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()  # Create the PipeLine instance
    display_size = pl.get_display_size()
    # Initialize the custom AI task instance
    my_ai = MyAIApp(kmodel_path, model_input_size=[320, 320],rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    my_ai.config_preprocess()  # Configure preprocessing
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # Get the current frame data
            res = my_ai.run(img)              # Run inference on the current frame
            my_ai.draw_result(pl, res)        # Draw the results
            pl.show_image()                 # Display the results
            gc.collect()                    # Garbage collection
    my_ai.deinit()                          # Deinitialize
    pl.destroy()                            # Destroy the PipeLine instance

```

Take keyword wake-up keyword_spotting as an example:

```python
from libs.Utils import ScopedTiming
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from media.pyaudio import *                     # Audio module
from media.media import *                       # Software abstraction module, mainly encapsulating the media data chain and media buffers
import media.wave as wave                       # WAV audio processing module
import nncase_runtime as nn                     # nncase runtime module, encapsulating kpu (kmodel inference) and ai2d (image preprocessing acceleration) operations
import ulab.numpy as np                         # Similar to Python numpy operations, but some interfaces are different
import aidemo                                   # aidemo module, encapsulating AI demo-related preprocessing, postprocessing, and other operations
import time                                     # Time statistics
import struct                                   # Byte and character conversion module
import gc                                       # Garbage collection module
import os,sys                                   # Operating system interface module

# Custom keyword wake-up class, inherits from the AIBase base class
class KWSApp(AIBase):
    def __init__(self, kmodel_path, threshold, debug_mode=0):
        super().__init__(kmodel_path)  # Call the base class constructor
        self.kmodel_path = kmodel_path  # Model file path
        self.threshold=threshold
        self.debug_mode = debug_mode  # Whether to enable debug mode
        self.cache_np = np.zeros((1, 256, 105), dtype=np.float)

    # Custom preprocessing, returns a list of model input tensors
    def preprocess(self,pcm_data):
        pcm_data_list=[]
        # Get audio stream data
        for i in range(0, len(pcm_data), 2):
            # Every two bytes are organized into a signed integer and then converted to a float, representing one sample, which is added to the data list for the current frame (0.3s)
            int_pcm_data = struct.unpack("<h", pcm_data[i:i+2])[0]
            float_pcm_data = float(int_pcm_data)
            pcm_data_list.append(float_pcm_data)
        # Process the PCM data into the feature vector used as the model input
        mp_feats = aidemo.kws_preprocess(fp, pcm_data_list)[0]
        mp_feats_np = np.array(mp_feats).reshape((1, 30, 40))
        audio_input_tensor = nn.from_numpy(mp_feats_np)
        cache_input_tensor = nn.from_numpy(self.cache_np)
        return [audio_input_tensor,cache_input_tensor]

    # Customize the postprocessing of the current task; results is a list of model output arrays
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
            logits_np = results[0]
            self.cache_np= results[1]
            max_logits = np.max(logits_np, axis=1)[0]
            max_p = np.max(max_logits)
            idx = np.argmax(max_logits)
            # If the score is greater than the threshold and idx==1 (that is, the wake word is included), play the response audio
            if max_p > self.threshold and idx == 1:
                return 1
            else:
                return 0


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    # Set the model path and other parameters
    kmodel_path = "/sdcard/examples/kmodel/kws.kmodel"
    # Other parameters
    THRESH = 0.5                # Detection threshold
    SAMPLE_RATE = 16000         # Sampling rate of 16000Hz, meaning 16000 samples are taken per second
    CHANNELS = 1                # Number of channels: 1 for mono, 2 for stereo
    FORMAT = paInt16            # Audio input/output format paInt16
    CHUNK = int(0.3 * 16000)    # Number of frames read each time audio data is read, set to the number of frames in 0.3s: 16000*0.3=4800
    reply_wav_file = "/sdcard/examples/utils/wozai.wav"         # Path to the kws wake-word response audio

    # Initialize the audio preprocessing interface
    fp = aidemo.kws_fp_create()
    # Initialize the audio stream
    p = PyAudio()
    MediaManager.init()    # Initialize the vb buffer
    # Used to collect real-time audio data
    input_stream = p.open(format=FORMAT,channels=CHANNELS,rate=SAMPLE_RATE,input=True,frames_per_buffer=CHUNK)
    # Used to play the response audio
    output_stream = p.open(format=FORMAT,channels=CHANNELS,rate=SAMPLE_RATE,output=True,frames_per_buffer=CHUNK)
    # Initialize the custom keyword wake-up instance
    kws = KWSApp(kmodel_path,threshold=THRESH,debug_mode=0)

    try:
        while True:
            os.exitpoint()                      # Check whether there is an exit signal
            with ScopedTiming("total",1):
                pcm_data=input_stream.read()
                res=kws.run(pcm_data)
                if res:
                    print("====Detected XiaonanXiaonan!====")
                    wf = wave.open(reply_wav_file, "rb")
                    wav_data = wf.read_frames(CHUNK)
                    while wav_data:
                        output_stream.write(wav_data)
                        wav_data = wf.read_frames(CHUNK)
                    time.sleep(1) # Time buffer for playing the response sound
                    wf.close()
                else:
                    print("Deactivated!")
                gc.collect()                    # Garbage collection
    except Exception as e:
        sys.print_exception(e)                  # Print exception information
    finally:
        input_stream.stop_stream()
        output_stream.stop_stream()
        input_stream.close()
        output_stream.close()
        p.terminate()
        MediaManager.deinit()              # Release the vb buffer
        aidemo.kws_fp_destroy(fp)
        kws.deinit()                       # Deinitialize
```

#### No-preprocessing Task

For AI tasks that do not require preprocessing (direct input inference), the pseudocode is as follows:

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import * 
import os
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import gc
import sys

# Custom AI task class, inheriting from the AIBase base class
class MyAIApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        # Call the constructor of the base class
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        # Model file path
        self.kmodel_path = kmodel_path
        # Model input resolution
        self.model_input_size = model_input_size
        # Image resolution provided by the sensor to the AI, with the width aligned to 16
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        # Display resolution, with the width aligned to 16
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        # Whether to enable debug mode
        self.debug_mode = debug_mode

    # Customize the postprocessing of the current task. results is a list of model output arrays and must be rewritten according to the actual task
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
           pass

    # For AI tasks without preprocessing, this function must be overridden in the subclass
    def run(self,inputs_np):
        # First convert the ulab.numpy.ndarray list into a tensor list
        tensors=[]
        for input_np in inputs_np:
            tensors.append(nn.from_numpy(input_np))
        # Call the inference function in AIBase to perform model inference
        results=self.inference(tensors)
        # Call the postprocess method of the current subclass for custom postprocessing
        outputs=self.postprocess(results)
        return outputs

    # Draw the results onto the screen; this must be written according to the task
    def draw_result(self, pl, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            pass

if __name__ == "__main__":
    # Display mode: "auto" automatically selects the screen driver according to the development board model; "hdmi"/"lcd"/"st7701", etc. can also be specified explicitly
    display_mode="auto"
    # None means using the default resolution of the screen driver; enter [width, height] when specifying it
    display_size=None
    # Set the model path; replace this with the current task model
    kmodel_path = "example_test.kmodel"
    rgb888p_size = [1920, 1080]
    ###### Other parameters########
    ...
    ######################

    # Initialize PipeLine for the image processing pipeline
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()  # Create the PipeLine instance
    display_size = pl.get_display_size()
    # Initialize the custom AI task instance
    my_ai = MyAIApp(kmodel_path, model_input_size=[320, 320],rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    my_ai.config_preprocess()  # Configure preprocessing
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # Get the current frame data
            res = my_ai.run(img)              # Infer the current frame
            my_ai.draw_result(pl, res)        # Draw the results
            pl.show_image()                 # Display the results
            gc.collect()                    # Garbage collection
    my_ai.deinit()                          # Deinitialize
    pl.destroy()                            # Destroy the PipeLine instance

```

For example, the tracking module in single object tracking (nanotracker.py) only needs the output of the template model and the real-time inference model as the input of the tracking model, and does not require preprocessing:

```python
class TrackerApp(AIBase):
    def __init__(self,kmodel_path,crop_input_size,thresh,rgb888p_size=[1280,720],display_size=[1920,1080],debug_mode=0):
        super().__init__(kmodel_path,rgb888p_size,debug_mode)
        # kmodel path
        self.kmodel_path=kmodel_path
        # crop model input size
        self.crop_input_size=crop_input_size
        # Tracking box threshold
        self.thresh=thresh
        # Tracking box width and height adjustment coefficient
        self.CONTEXT_AMOUNT = 0.5
        # Image resolution provided by the sensor to the AI, with the width aligned to 16 bytes
        self.rgb888p_size=[ALIGN_UP(rgb888p_size[0],16),rgb888p_size[1]]
        # Video output VO resolution, with the width aligned to 16 bytes
        self.display_size=[ALIGN_UP(display_size[0],16),display_size[1]]
        # debug mode
        self.debug_mode=debug_mode
        # May be omitted
        self.ai2d=Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT,nn.ai2d_format.NCHW_FMT,np.uint8, np.uint8)

    # May be omitted
    def config_preprocess(self,input_image_size=None):
        with ScopedTiming("set preprocess config",self.debug_mode > 0):
            pass

    # Override the run function. Since there is no preprocessing process, the preprocess->inference->postprocess operations originally included in run are inappropriate; here, only inference->postprocess is included
    def run(self,input_np_1,input_np_2,center_xy_wh):
        input_tensors=[]
        input_tensors.append(nn.from_numpy(input_np_1))
        input_tensors.append(nn.from_numpy(input_np_2))
        results=self.inference(input_tensors)
        return self.postprocess(results,center_xy_wh)


    # Custom postprocessing. results is a list of model output arrays; here, the aidemo nanotracker_postprocess list is used
    def postprocess(self,results,center_xy_wh):
        with ScopedTiming("postprocess",self.debug_mode > 0):
            det = aidemo.nanotracker_postprocess(results[0],results[1],[self.rgb888p_size[1],self.rgb888p_size[0]],self.thresh,center_xy_wh,self.crop_input_size[0],self.CONTEXT_AMOUNT)
            return det
```

#### Multi-model Task

Taking dual-model cascaded inference as an example, the pseudocode is given as follows:

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import os
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import gc
import sys

# Custom AI task class, inheriting from the AIBase base class
class MyAIApp_1(AIBase):
    def __init__(self, kmodel_path, model_input_size, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        # Call the constructor of the base class
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        # Model file path
        self.kmodel_path = kmodel_path
        # Model input resolution
        self.model_input_size = model_input_size
        # Image resolution provided by the sensor to the AI, with the width aligned to 16
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        # Display resolution, with the width aligned to 16
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        # Whether to enable debug mode
        self.debug_mode = debug_mode
        # Instantiate Ai2d for model preprocessing
        self.ai2d = Ai2d(debug_mode)
        # Set the input/output formats and types of Ai2d
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)

    # Configure preprocessing operations. Here resize is used. Ai2d supports crop/shift/pad/resize/affine. For details, open /sdcard/libs/AI2D.py
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            # Initialize the ai2d preprocessing configuration. It defaults to the dimensions provided by the sensor to the AI. The input dimensions can be changed by setting input_image_size
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            # Configure the resize preprocessing method
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            # Build the preprocessing pipeline
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])

    # Customize the postprocessing of the current task. results is a list of model output arrays and must be rewritten according to the actual task
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
           pass


# Custom AI task class, inheriting from the AIBase base class
class MyAIApp_2(AIBase):
    def __init__(self, kmodel_path, model_input_size, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        # Call the constructor of the base class
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        # Model file path
        self.kmodel_path = kmodel_path
        # Model input resolution
        self.model_input_size = model_input_size
        # Image resolution provided by the sensor to the AI, with the width aligned to 16
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        # Display resolution, with the width aligned to 16
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        # Whether to enable debug mode
        self.debug_mode = debug_mode
        # Instantiate Ai2d for model preprocessing
        self.ai2d = Ai2d(debug_mode)
        # Set the input/output formats and types of Ai2d
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)

    # Configure preprocessing operations. Here resize is used. Ai2d supports crop/shift/pad/resize/affine. For details, open /sdcard/libs/AI2D.py
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            # Initialize the ai2d preprocessing configuration. It defaults to the dimensions provided by the sensor to the AI. The input dimensions can be changed by setting input_image_size
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            # Configure the resize preprocessing method
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            # Build the preprocessing pipeline
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])

    # Customize the postprocessing of the current task. results is a list of model output arrays and must be rewritten according to the actual task
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
           pass


class MyApp:
    def __init__(kmodel1_path,kmodel2_path,kmodel1_input_size,kmodel2_input_size,rgb888p_size,display_size,debug_mode):
        # Create instances for inference with two models
        self.app_1=MyApp_1(kmodel1_path,kmodel1_input_size,rgb888p_size,display_size,debug_mode)
        self.app_2=MyApp_2(kmodel2_path,kmodel2_input_size,rgb888p_size,display_size,debug_mode)
        self.app_1.config_preprocess()

    # Write the run function. Write the code according to the requirements of the AI task. This is only an example
    def run(self,input_np):
        outputs_1=self.app_1.run(input_np)
        outputs_2=[]
        for out in outputs_1:
            self.app_2.config_preprocess(out)
            out_2=self.app_2.run(input_np)
            outputs_2.append(out_2)
        return outputs_1,outputs_2

    # Draw
    def draw_result(self,pl,outputs_1,outputs_2):
        pass

    ######Other functions########
    # Omitted
    ####################


if __name__ == "__main__":
    # Display mode. "auto" automatically selects the screen driver according to the development board model; "hdmi"/"lcd"/"st7701", etc. can also be explicitly specified
    display_mode="auto"
    # None indicates the default resolution of the screen driver; enter [width, height] when specifying one
    display_size=None
    rgb888p_size = [1920, 1080]
    # Set the model paths, which must be replaced with the models for the current task
    kmodel1_path = "test_kmodel1.kmodel"
    kmdoel1_input_size=[320,320]
    kmodel2_path = "test_kmodel2.kmodel"
    kmodel2_input_size=[48,48]

    ###### Other parameters ########
    # Omitted
    ######################

    # Initialize PipeLine for the image processing pipeline
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()  # Create the PipeLine instance
    display_size = pl.get_display_size()
    # Initialize the custom AI task instance
    my_ai = MyApp(kmodel1_path,kmodel2_path, kmodel1_input_size,kmodel2_input_size,rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    my_ai.config_preprocess()  # Configure preprocessing
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()                        # Get the current frame data
            outputs_1,outputs_2 = my_ai.run(img)          # Infer the current frame
            my_ai.draw_result(pl, outputs_1,outputs_2)    # Draw the results
            pl.show_image()                             # Display the results
            gc.collect()                                # Garbage collection
    my_ai.app_1.deinit()                    # Deinitialize
    my_ai.app_2.deinit()
    pl.destroy()                            # Destroy the PipeLine instance

```

For example code, please refer to license plate detection and recognition: flash the firmware, open the IDE, select File -> Open File, and select the corresponding script according to the following path: **This PC -> CanMV -> sdcard -> examples -> 05-AI-Demo -> license_plate_det_rec.py**.

### Reference Documentation

#### k230 canmv Documentation

Documentation link: [Welcome to K230 CanMV's documentation! — K230 CanMV Documentation (canaan-creative.com)](https://www.kendryte.com/zh/sdkResource/230canmv)

#### Ulab Library Support

Link: [ulab – Manipulate numeric data similar to numpy — Adafruit CircuitPython 9.1.0-beta.3 documentation](https://docs.circuitpython.org/en/latest/shared-bindings/ulab/index.html)

github link: [v923z/micropython-ulab: a numpy-like fast vector module for micropython, circuitpython, and their derivatives (github.com)](https://github.com/v923z/micropython-ulab)

## AI Demo

```{admonition} Tip
The development board with the K230D chip needs to change the `display_mode` in `__main__` to `lcd` to adapt the display output when running the above demos, and also needs to reduce the resolution according to the comments. At the same time, some demos cannot run on K230D. For details, see the table above.
```

Please download the latest version of the image according to the type of development board you have from [K230 MicroPython Image Download List](https://www.kendryte.com/resource?selected=0-0-3-0) and [K230D MicroPython Image Download List](https://www.kendryte.com/resource?selected=1-0-2-0), and complete the burning. For the burning method, please refer to the document: [Burn Firmware](../../../zh/userguide/how_to_burn_firmware.md).

After the image burning is complete, connect to the IDE. For instructions on how to use the IDE, please refer to the document: [How to Use IDE](../../../zh/userguide/how_to_use_ide.md).

### Dynamic Gesture Recognition

#### Demo Description

Dynamic gesture recognition implements the recognition of five dynamic gestures, which include: waving up, waving down, waving left, waving right, and finger pinching.

#### Code

Open the IDE, select File->Open File, and select the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->dynamic_gesture.py**. You can refer to the source code displayed by the IDE. Click the run button in the lower left corner of the IDE to demonstrate the demo.

#### Demonstration Effect

Please point your palm at the camera. After the corresponding direction palm appears in the upper left corner of the screen, make the actions of left, right, up, down, and five-finger pinching. After the action is recognized, the category of the dynamic gesture will be displayed and marked with an arrow.

### Gaze Estimation

#### Demo Description

Gaze estimation predicts the direction of human eye gaze based on facial features. This application is a dual-model application. It first performs face detection, then predicts the gaze direction of the detected face, and marks it on the screen with arrows.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->eye_gaze.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to demonstrate the demo.

#### Demonstration Effect

The original image is as follows:

![eye_gaze](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/eye_gaze.jpg)

Here, taking the 01studio LCD screen (800*480) as an example to show the demonstration effect, please change `display_mode` in the `__main__` function to `lcd` and then run it. The hdmi effect is similar.

![eye_gaze_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/eye_gaze_res.jpg)

<a id="face-detection-demo"></a>

### Face Detection

#### Demo Description

The face detection application detects every face in the video and marks them with detection boxes. At the same time, it marks the positions of five key points for each face: the left eye, right eye, nose tip, left mouth corner, and right mouth corner.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_detection.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to run the demo.

#### Demonstration Effect

The original image is as follows:

![face_det](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face_det.jpg)

Here, the LCD screen of 01studio (800*480) is used as an example to show the demonstration effect. Please change `display_mode` in the `__main__` function to `lcd` and then run it. The HDMI effect is similar.

![face_det_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face_det_res.jpg)

### Face Key Parts

#### Demo Description

The face key parts application is a dual-model application. It first performs face detection on each frame of the video, then identifies 106 key points on each detected face, and draws the contours of the face, mouth, eyes, nose, and eyebrow areas based on the 106 key points.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_landmark.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo.

#### Demo Effect

The original image is as follows:

![face_landmark](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face.jpg)

Here, the 01studio LCD screen (800*480) is used as an example to show the demo effect. Please change `display_mode` to `lcd` in the `__main__` function before running. The hdmi effect is similar.

![face_landmark_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face_landmark_res.jpg)

### Face Liveness Detection

#### Demo Description

Face liveness detection is a single-model liveness detection example based on RGB images. The application first performs face detection on each frame of the video, and then performs liveness detection on each detected face to determine whether it is a live face.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_liveness_rgb.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

### Face 3D Mesh

#### Demo Description

Face 3D Mesh is a multi-model application. First, face detection is performed on each frame of the video, then face alignment is performed using the face alignment model (3DDFA, 3D Dense Face Alignment), and finally the face mesh model is used to reconstruct the 3D mesh of each face in the image, obtaining the mesh of each face.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_mesh.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo.

#### Demo Effect

The original image is as follows:

![face_mesh](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face.jpg)

Taking the 01studio LCD screen (800*480) as an example, the demo effect is shown below. Please change `display_mode` to `lcd` in the `__main__` function before running. The hdmi effect is similar.

![face_mesh_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face_mesh_res.jpg)

### Face Parsing

#### Demo Description

The Face Parsing (also known as Face Segmentation) application is a dual-model application. It first performs face detection, and then achieves segmentation of different parts of the face. Face segmentation includes pixel-level classification of regions such as eyes, nose, and mouth, with different areas marked in different colors on the screen.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_parse.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demo Effect

The original image is as follows:

![face_parse](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face.jpg)

Here, the 01studio LCD screen (800*480) is taken as an example to show the demo effect. Please change `display_mode` in the `__main__` function to `lcd` before running. The hdmi effect is similar.

![face_parse_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face_parse_res.jpg)

### Face Pose

#### Demo Description

Face pose is a dual-model application. First, face detection is performed on each frame of the video, and then the face orientation is predicted for each detected face. Face orientation is represented using Euler angles (roll/yaw/pitch), where roll represents the degree of face tilting left and right, yaw represents the degree of face rotating left and right, and pitch represents the degree of face looking down and up. This application visualizes the face orientation on the screen by constructing a projection matrix.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_pose.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demo Effect

The original image is as follows:

![face_pose](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face_pose.jpg)

Here, taking the 01studio LCD screen (800*480) as an example, the demo effect is given. Please change `display_mode` in the `__main__` function to `lcd` and run it. The HDMI effect is similar.

![face_pose_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face_pose_res.jpg)

### Face Registration

#### Demo Description

Face registration is a prerequisite task for face recognition. It performs feature extraction on each image containing a face in the face database, and writes the face features to the face database directory in the form of a bin file, ready to be called by the face recognition program. The face feature dimension output by face registration is 512.

#### Code

Open the IDE, select File -> Open File, and choose the corresponding script according to the following path: **This PC -> CanMV -> sdcard -> examples -> 05-AI-Demo -> face_registration.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE for demo demonstration.

#### Demonstration Effect

Register the image containing a face as face features and store them in the face feature database. The image below is one of the face images:

![id_2](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/id_2.png)

### Face Recognition

#### Demo Description

The face recognition application identifies the identity of faces in each frame of the video based on registered face information. If the recognized face is found in the registration database, the identity information of the recognized face is annotated; otherwise, it is displayed as unknown.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_recognition.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo.

#### Demonstration Effect

The registered face original image is as follows:

![face_recognition](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/id_2.png)

Here is a demonstration effect using the 01studio LCD screen (800*480) as an example. Please change the `display_mode` in the `__main__` function to `lcd` and then run it. The HDMI effect is similar.

![face_recognition_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/face_recognition_res.jpg)

### Fall Detection

#### Demo Description

The fall detection application checks whether there is a human in each frame of the video and detects the human's fall status. It labels the status as `NoFall` if not falling, and `Fall` if a fall is detected.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script following this path: **This PC->CanMV->sdcard->examples->05-AI-Demo->falldown_detect.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demonstration Effect

The original image is as follows:

![falldown_det](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/falldown_detect.jpg)

Here is a demonstration using the 01studio LCD screen (800*480) as an example. Please change `display_mode` to `lcd` in the `__main__` function before running. The HDMI effect is similar.

![falldown_det_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/falldown_det_res.jpg)

### Rock-Paper-Scissors Game

#### Demo Description

The Rock-Paper-Scissors Game is an entertaining game based on hand applications. First, keep no other palms in the screen, then one hand enters the camera to show rock/paper/scissors, while the machine will randomly show rock/paper/scissors at the same time. Finally, the winner is determined based on the best-of-three principle.

#### Code

Open the IDE, select File -> Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->finger_guessing.py**. You can refer to the source code displayed in the IDE. Click the run button at the bottom left of the IDE to perform the demo.

#### Demonstration Effect

Initially, please ensure the camera range is empty. When one hand enters the camera, show rock/paper/scissors. The rule follows a best-of-three system. Please experience it yourself.

### Palm Detection

#### Demo Description

The palm detection application detects palms present in each frame of the video and marks palm detection boxes on the screen.

#### Code

Open the IDE, select File->Open File, and select the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->hand_detection.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to run the demo.

#### Demonstration Effect

The original image is as follows:

![hand_det](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_det.jpg)

Here, the LCD screen of 01studio (800*480) is used as an example to show the demonstration effect. Please change `display_mode` in the `__main__` function to `lcd` before running. The HDMI effect is similar.

![hand_det_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_det_res.jpg)

### Hand Keypoint Classification

#### Demo Description

The hand keypoint classification application is a dual-model task. First, it detects the hands present in the video, then performs keypoint regression on the detected hands. After obtaining the keypoint information, it distinguishes different gestures by calculating the angle information between fingers. Currently, 9 gestures are supported as shown in the figure below.

![Supported Gestures Illustration](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_class.jpg)

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->hand_keypoint_class.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demo Effect

The original image is as follows:

![hand_kp_cls](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_rec.jpg)

Here, the 01studio LCD screen (800*480) is used as an example to show the demo effect. Please change `display_mode` in the `__main__` function to `lcd` before running. The HDMI effect is similar.

![hand_kp_cls_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_kp_cls_res.jpg)

### Hand Keypoint Detection

#### Demo Description

Hand keypoint detection is a dual-model task. First, palm detection is performed on each frame of the video. Then, keypoint regression is applied to each detected palm to obtain 21 palm skeletal keypoint positions. The keypoints and the lines connecting them are marked on the screen.

#### Code

Open the IDE, select File -> Open File, and choose the corresponding script according to the following path: **This PC -> CanMV -> sdcard -> examples -> 05-AI-Demo -> hand_keypoint_detection.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demo Effect

The original image is as follows:

![hand_kp_det](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_kp_cls.jpg)

Here is a demonstration using the 01studio LCD screen (800*480) as an example. Please change `display_mode` in the `__main__` function to `lcd` before running; the HDMI effect is similar.

![hand_kp_det_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_kp_det.jpg)

### Gesture Recognition

#### Demo Description

The gesture recognition application is a classification-based gesture recognition task. First, palm detection is performed on each frame of the video, and then the detected palm is fed into a classification model to obtain the recognized gesture. This is just an example, supporting 3 types of gestures as shown in the figure below.

![Gesture Recognition](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_reco.jpg)

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->hand_recognition.py**, you can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo.

#### Demo Effect

The original image is as follows:

![hand_rec](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_rec.jpg)

Taking the 01studio LCD screen (800*480) as an example, the demo effect is shown. Please change `display_mode` to `lcd` in the `__main__` function before running. The hdmi effect is similar.

![hand_rec_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/hand_rec_res.jpg)

### Keyword Wake-up

#### Demo Description

The keyword wake-up application is a typical audio application. After the application starts, please wake it up by saying "小楠小楠" near the microphone. After the application recognizes the wake word, it will respond with "我在". Other applications that need to collect audio data can also refer to this application.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->keyword_spotting.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to demonstrate the demo.

#### Demonstration Effect

Please get close to the microphone and wake it up with "小楠小楠". After being woken up, the k230 will reply "我在"!

### License Plate Detection

#### Demo Description

The license plate detection application detects license plates appearing in the video and marks them with a detection box on the screen.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->license_plate_det.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demonstration Effect

Please find your own license plate images for detection. This example involves license plate privacy, so no demonstration effect is provided.

### License Plate Recognition

#### Demo Description

The license plate recognition application is a dual-model task. First, it detects license plates appearing in the video, then it performs recognition on each detected license plate, and annotates the recognized license plate content near the corresponding detection box.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->license_plate_det_rec.py**, you can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demonstration Effect

Please find license plate images yourself for recognition. This example involves license plate privacy, so no demonstration effect is provided.

### YOLO License Plate Detection

#### Demo Description

The license plate detection application detects license plates appearing in videos and marks them with detection boxes on the screen. Different from the similar tasks above, the model for this task is trained using the CCPD2019 and CCPD2020 datasets, and the detection model uses the yolo11n pose model.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->license_plate_det_yolo.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demo Effect

Please find license plate images on your own for detection. This example involves license plate privacy, so no demo effect is provided.

### YOLO License Plate Detection and Recognition

#### Demo Description

The license plate recognition application is a dual-model task. It first detects license plates appearing in the video, then recognizes each detected license plate, and marks the recognized license plate content near the corresponding detection box. Different from the similar tasks mentioned above, the models used in this task are trained with the CCPD2019 and CCPD2020 datasets, and the detection model uses the yolo11n pose model.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->license_plate_det_rec_yolo.py**. You can refer to the source code displayed in the IDE. Click the run button at the bottom left of the IDE to perform the demo demonstration.

#### Demonstration Effect

Please find license plate images by yourself for recognition. This example involves license plate privacy, so no demonstration effect is provided.

### Single Object Tracking

#### Demo Description

The single object tracking application tracks and recognizes the object registered in the object box. After the application starts, it will wait for a period of time. During this period, place the object to be tracked (preferably with a color different from the background) into the object box. Once registration is complete, it will automatically enter the tracking state, and the object tracking box will move along with the object.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->nanotracker.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demonstration Effect

The original image is as follows:

![nanotracker](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/nanotracker.jpg)

Here, taking the 01studio LCD screen (800*480) as an example, the demonstration effect is shown. Please change `display_mode` in the `__main__` function to `lcd` before running. The HDMI effect is similar.

![nanotracker_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/nanotracker_res.jpg)

### yolov8n Object Detection

#### Demo Description

The yolov8n object detection application uses the yolov8n model to detect the 80 categories of COCO, and the detection results are marked on the screen in the form of detection boxes.

#### Code

Open the IDE, select File -> Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->object_detect_yolov8n.py**, you can refer to the source code displayed by the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demonstration Effect

The original image is as follows:

![yolov8n_det](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/yolov8n_det.jpg)

Here, taking the 01studio LCD screen (800*480) as an example, the demonstration effect is given. Please change the `display_mode` in the `__main__` function to `lcd` and run it. The hdmi effect is similar.

![yolov8n_det_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/yolov8n_det_res.jpg)

### OCR Detection

#### Demo Description

The OCR detection application detects text appearing in the video, and the detection results are marked on the screen in the form of detection boxes.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->ocr_det.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demonstration Effect

The original image is as follows:

![ocr_det](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/ocr_det.jpg)

Here, taking the 01studio LCD screen (800*480) as an example to give the demonstration effect, please change `display_mode` to `lcd` in the `__main__` function and run it. The hdmi effect is similar.

![ocr_det_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/ocr_det_res.jpg)

### OCR Recognition

#### Demo Description

The OCR recognition application is a dual-model task. First, it detects the text in each frame of the video, then recognizes the detected text. Finally, the detection boxes are marked on the screen and the recognized text content is added near the detection boxes.

#### Code

Open the IDE, select File->Open File, and select the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->ocr_rec.py**, you can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo.

#### Demo Effect

The original image is as follows:

![ocr_rec](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/ocr_rec.jpg)

Here, the 01studio LCD screen (800*480) is taken as an example to show the demo effect. Please change `display_mode` in the `__main__` function to `lcd` and then run it. The hdmi effect is similar.

![ocr_rec_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/ocr_rec_res.jpg)

### Human Body Detection

#### Demo Description

The human body detection application detects people in the video and marks them on the screen in the form of detection boxes.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->person_detection.py**. You can refer to the source code displayed in the IDE. Click the Run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demonstration Effect

The original image is as follows:

![person_det](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/person_det.jpg)

Here is an example of the demonstration effect using a 01studio LCD screen (800*480). Please change `display_mode` in the `__main__` function to `lcd` before running. The HDMI effect is similar.

![person_det_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/person_det_res.jpg)

### Human Body Keypoint Detection

#### Demo Description

The human body keypoint detection application uses the yolov8n-pose model to detect human posture. The detection results obtain the positions of 17 human skeletal keypoints and connect them with lines of different colors to display on the screen.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->person_keypoint_detect.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demo Effect

The original image is as follows:

![person_kp_det](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/person_kp_det.jpg)

Here is a demonstration effect using 01studio's LCD screen (800*480) as an example. Please change `display_mode` to `lcd` in the `__main__` function and run it. The HDMI effect is similar.

![person_kp_det_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/person_kp_det_res.jpg)

### Puzzle Game

#### Demo Description

The puzzle game is an entertaining hand-based game. When the application starts, keep the hand out of the camera's view and wait for the screen to initialize. The left side shows the randomly shuffled puzzle, and the right side shows the target puzzle. Once the hand enters the frame, spread the thumb and middle finger apart; the yellow point between the two fingers is used to locate the moving block. Quickly pinch the two fingers together and then open them again, and the yellow point turns into a blue point. Then the corresponding block moves to the adjacent empty space.

#### Code

Open the IDE, select File -> Open File, and choose the corresponding script to open following the path below: **This PC->CanMV->sdcard->examples->05-AI-Demo->puzzle_game.py**. You can refer to the source code displayed in the IDE. Click the Run button at the bottom-left corner of the IDE to perform the demo.

#### Demo Effect

Here, we use the 01studio LCD screen (800*480) as an example to show the demo effect. Please change `display_mode` in the `__main__` function to `lcd` before running; the HDMI effect is similar. Keep a certain distance from the camera, spread the thumb and middle finger apart, and pinch the thumb and middle finger together on a block adjacent to the empty space. The empty block and the current block will swap positions.

![puzzle_game_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/puzzle_game_res.jpg)

### yolov8n Segmentation

#### Demo Description

The yolov8n segmentation application uses the yolov8n model to segment the 80 categories of objects from the COCO dataset that appear in the video, and displays them on the screen in the form of masks.

#### Code

Open the IDE, select File->Open File, and select the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->segment_yolov8n.py**, you can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE for demo demonstration.

#### Demonstration Effect

The original image is as follows:

![yolov8n_seg](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/yolov8n_seg.jpg)

Here is a demonstration effect using the 01studio LCD screen (800*480) as an example, please change `display_mode` in the `__main__` function to `lcd` before running, the hdmi effect is similar.

![yolov8n_seg_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/yolov8n_seg_res.jpg)

### Self Learning

#### Demo Description

Self learning is a feature-based classification method. First, set labels in the code to specify the names of the items to be collected, then start the application. Follow the on-screen prompts to place the items to be collected into the feature collection box. After feature collection is complete, it will automatically enter the recognition state. Place the items to be recognized into the collection box, and the features of the items will be compared with those of the registered items. Classification is completed based on the similarity.

#### Code

Open the IDE, select File -> Open File, and choose the corresponding script according to the following path: **This PC -> CanMV -> sdcard -> examples -> 05-AI-Demo -> self_learning.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demo Effect

The pictures of apples and bananas to be learned are as follows:

![apple](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/apple.jpg)

![banana](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/banana.jpg)

Here, the LCD screen of 01studio (800*480) is taken as an example to show the demo effect. Please change `display_mode` in the `__main__` function to `lcd` before running. The hdmi effect is similar. Follow the on-screen prompts to place the apples and bananas into the box for learning, then it will automatically enter the recognition state. The objects in the box will be recognized as apples and bananas, and a similarity score will be given.

![self_learning_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/self_learning_res.jpg)

### Magnifier

#### Demo Description

The magnifier is a fun application based on hand features. After launching the application, ensure one hand is within the camera frame. Pinch your thumb and middle finger, position them at a certain location, then spread the two fingers apart. The magnified image of that area will be displayed near the two fingers.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->space_resize.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

#### Demo Effect

Here we use the 01studio LCD screen (800*480) as an example to show the demo effect. Please change `display_mode` in the `__main__` function to `lcd` before running. The HDMI effect is similar. Pinch your thumb and middle finger, put them into the camera, then open and close the thumb and middle finger, and a small surrounding area will be zoomed and displayed.

![space_resize_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/example/images/ai_demo/space_resize_res.jpg)

### Text-to-Speech (Chinese)

#### Demo Description

Text-to-Speech (TTS, Chinese) is a typical audio application. You can modify the text in the main function. After the audio is generated, you can hear the generated audio through earphones. This application is relatively time-consuming, and the complete audio playback time is also relatively long, with the duration limited by the length of the generated text.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **此电脑->CanMV->sdcard->examples->05-AI-Demo->tts_zh.py**. You can refer to the source code displayed in the IDE. Click the run button at the bottom left corner of the IDE to perform the demo.

#### Demonstration Effect

Please insert earphones or speakers, run the program, and the generated audio will be played after the generation is complete. Please experience it yourself!

### Human Body Segmentation

#### Demo Description

The human body segmentation task divides the entire human body into 15 parts and represents them with different colors.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->body_seg.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

### Multi-command Word Wake-up

#### Demo Description

Multi-command word wake-up is an extended version of keyword wake-up. It supports wake-up with four keywords: `xiaonanxiaonan`, `go`, `stop`, and `wow`, making it suitable for voice command control scenarios.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->multi_kws.py**. You can refer to the source code displayed in the IDE. Click the run button at the bottom left corner of the IDE to start the demo.

### Lightweight Face Registration

#### Demo Description

The lightweight face registration uses a new face recognition model. Compared to the heavyweight model (44M), its model is less than 3M, making it suitable for the K230D face recognition registration process!

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_registration_lite.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower-left corner of the IDE to perform the demo.

### Lightweight Face Recognition

#### Demo Description

The lightweight face recognition uses a new face recognition model. Compared to the heavyweight model (44M), its model size is less than 3M, making it suitable for face recognition processes that require frame rate performance or run on K230D!

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_recognition_lite.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to run the demo.

### YOLO11n Rotating Object Detection

#### Demo Description

YOLO11n rotating object detection implements the detection of 15 types of objects with angles, including airplanes, ships, and more.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->yolo11n_obb.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

### YOLOv8n Rotating Object Detection

#### Demo Description

YOLOv8n Rotating Object Detection implements 15 types of object detection with angle, including airplanes, ships, etc.

#### Code

Open the IDE, select File->Open File, and choose the corresponding script according to the following path: **This PC->CanMV->sdcard->examples->05-AI-Demo->yolov8n_obb.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower left corner of the IDE to perform the demo demonstration.

### YOLO26 Human Pose Keypoint Detection

#### demo description

YOLO26 human pose keypoint detection uses YOLO26's pose model to detect people in the image and output 17 skeletal keypoints for each person (COCO format). Compared with YOLOv8's pose model, YOLO26 directly outputs results with semantic information, so **NMS is not required** during post-processing; therefore, the script does not have an `nms_threshold` parameter.

#### Code

Open the IDE, select File->Open File, and follow the path below to open the corresponding script: **This PC->CanMV->sdcard->examples->05-AI-Demo->yolo26_person_kp.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower-left corner of the IDE to run the demo.

### YuNet Face Detection

#### demo description

YuNet is a lightweight face detection model. Compared with the retinaface class model used by default in the demo, it requires less computation and provides higher frame rates, making it suitable for speed-sensitive scenarios or scenarios where it needs to coexist with other models. Post-processing uses the `aidemo.yunet_postprocess` interface, which supports limiting the maximum number of faces returned per frame through the `top_k` parameter.

#### Code

Open the IDE, select File -> Open File, and follow the path below to open the corresponding script: **This PC -> CanMV -> sdcard -> examples -> 05-AI-Demo -> face_detect_yunet.py**. You can refer to the source code displayed in the IDE. Click the run button in the lower-left corner of the IDE to run the demo.

```{admonition} Tip
`21-AI-With-Others/face_detect_yunet_from_mp4.py` provides a version of the same model for inference on local MP4 files, which can be used for batch analysis of offline videos.
```

### Face Pixelation and Counting

#### Demo Description

Face mosaicking and counting are intended for privacy-protection scenarios: mosaic every face detected in the frame while also counting the number of people who have appeared in the frame. To ensure detection even when faces are small, the script performs multiple tiled detections on the frame by default (`FACE_TILES`).

A set of adjustable parameters is provided at the top of the script. Common parameters include:

| Parameter | Description |
|------|------|
| `PAD_RATIO` | Face-box expansion ratio, used to cover the hair and chin |
| `BLOCKS` | Number of mosaic blocks per face; a smaller value produces a coarser mosaic |
| `MASK_HOLD_MS` | Duration for which masking continues after a face is briefly lost, used to suppress flickering |
| `COUNT_PEOPLE` | Whether to enable people counting |
| `TRACK_MIN_HITS` | Number of consecutive detections required before a person is counted, used to suppress false detections |
| `TRACK_TIMEOUT_MS` | Track timeout duration; counting restarts after the timeout |
| `DRAW_BOXES` / `SHOW_COUNT` | Whether to draw face boxes and display the count |

```{admonition} Warning
:class: warning
This demo is based on **face detection** rather than person segmentation, so it can only cover relatively frontal faces. Faces in profile or facing away from the camera are neither mosaicked nor counted. `MASK_HOLD_MS` can only mitigate momentary flickering and cannot resolve the case of faces remaining in profile.
```

#### Code

Open the IDE, select File->Open File, and follow the path below to open the corresponding script: **This PC->CanMV->sdcard->examples->05-AI-Demo->face_masking_count.py**. You can refer to the source code displayed in the IDE. Click the Run button in the lower-left corner of the IDE to run the demo.

### Multi-Object Tracking

#### Demo Description

Multi-object tracking (MOT) builds on object detection by assigning each object a **stable ID**, ensuring that the same object retains the same number throughout the entire video, enabling applications such as people counting, trajectory plotting, and out-of-bounds detection.

The firmware includes the native `mot` module, which provides four tracking algorithms corresponding to four demo scripts:

| Script | Algorithm | Model | Description |
|------|------|------|------|
| bytetrack.py | ByteTrack | YOLOv8n pedestrian detection | Pure IoU association, fastest speed, **recommended as the first choice** |
| ocsort.py | OC-SORT | YOLOv8n pedestrian detection | Enhanced motion modeling, performs better when object motion is irregular |
| deepsort.py | DeepSort | YOLOv8n pedestrian detection + ReID feature model | Fuses appearance features, maintains IDs even after prolonged occlusion, with a significant frame-rate drop |
| botsort.py | BoT-SORT | YOLOv8n pedestrian detection + ReID feature model | Enhanced ByteTrack, highest accuracy, and also the greatest overhead |

For the complete parameter documentation of the `mot` module, see the [`mot` Module API Manual](../../api/aidemo/mot_module_api_manual.md).

```{admonition} Tip
`deepsort.py` and `botsort.py` additionally need to load `feature.kmodel` to extract ReID features for each detection box, resulting in a significant frame-rate drop when there are many objects. If only stable IDs are needed without recovering from prolonged occlusions, use `bytetrack.py` preferentially.
```

#### Code

Open the IDE, select File->Open File, and follow the path below to select and open the corresponding script: **This PC->CanMV->sdcard->examples->05-AI-Demo->bytetrack.py** (or `ocsort.py`, `deepsort.py`, `botsort.py`). You can refer to the source code displayed in the IDE. Click the run button in the lower-left corner of the IDE to run the demo.

#### Demonstration

Point the camera at a scene where people are walking. Each detected pedestrian will be boxed and labeled with an `ID`. When the same person is briefly occluded and reappears, the ID should remain unchanged; if the ID frequently changes, refer to the development tips in the [`mot` module API manual](../../api/aidemo/mot_module_api_manual.md#mot-tips) to adjust the parameters.
