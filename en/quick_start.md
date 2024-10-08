# CanMV-K230 Quick Start Guide

## 1. Introduction to CanMV-K230

The CanMV-K230 development board is based on the latest generation AIoT SoC K230 series chip from Canaan Technology's Kendryte® series AIoT chips. This chip adopts a new multi-heterogeneous unit accelerated computing architecture, integrates 2 RISC-V high-efficiency computing cores, and features a new generation KPU (Knowledge Process Unit) intelligent computing unit. It has multi-precision AI computing power, widely supports general AI computing frameworks, and achieves over 70% utilization in some typical networks.

The chip also supports a rich array of peripheral interfaces and integrates multiple dedicated hardware acceleration units such as 2D, 2.5D, etc., capable of accelerating various tasks such as image, video, audio, and AI. It features low latency, high performance, low power consumption, quick startup, and high security.

![K230_block_diagram](../zh/images/K230_block_diagram.png)

## 2. Getting Started

### 2.1 Acquiring the Development Board

```{list-table}
:header-rows: 1

* - Development Board
  - Photo
  - Description
* - [CanMV-K230](./userguide/boards/canmv_k230.md)
  - ```{image} images/CanMV-K230_front.png
    :width: 400
    :height: 400
    :align: "center"
    ```
  - Based on K230, with external 512MB LPDDR for larger memory
* - [CanMV-K230D](./userguide/boards/canmv_k230d.md)
  - TODO
  - Based on K230D, with built-in 128MB LPDDR4, compact size
```

### 2.2 Flashing the Firmware

Users can download the firmware from [Github](https://github.com/kendryte/canmv_k230/releases) or the [Canaan Developer Community](https://developer.canaan-creative.com/resource). After downloading the firmware for the corresponding development board, refer to the [Firmware Download Guide](./userguide/how_to_burn_firmware.md#2-烧录固件) to flash the firmware onto the development board.

### 2.3 Downloading the IDE

CanMV-K230 supports development using CanMV-IDE, allowing users to run code, view results, and preview images. For detailed usage, refer to the [IDE Download Guide](./userguide/how_to_use_ide.md#1-概述).

### 2.4 Running Demos

The CanMV-K230 firmware comes preloaded with numerous demo programs, allowing users to experience them without downloading from the internet. Use the IDE to open examples from the virtual U disk to quickly run them.

Refer to [How to Run Demo Programs](./userguide/how_to_run_examples.md#2-运行示例程序).

## 3. Camera Image Preview

Capture images using the camera and display them via HDMI:

```python
import time, os, sys

from media.sensor import *
from media.display import *
from media.media import *

sensor = None

try:
    print("camera_test")

    # Construct a Sensor object with default configuration
    sensor = Sensor()
    # Sensor reset
    sensor.reset()
    # Set horizontal mirror
    # sensor.set_hmirror(False)
    # Set vertical flip
    # sensor.set_vflip(False)

    # Set channel 0 output size, 1920x1080
    sensor.set_framesize(Sensor.FHD)
    # Set channel 0 output format
    sensor.set_pixformat(Sensor.YUV420SP)
    # Bind sensor channel 0 to display layer video 1
    bind_info = sensor.bind_info()
    Display.bind_layer(**bind_info, layer = Display.LAYER_VIDEO1)

    # Use HDMI as display output
    Display.init(Display.LT9611, to_ide = True, osd_num = 2)
    # Initialize media manager
    MediaManager.init()
    # Start sensor
    sensor.run()

    while True:
        os.exitpoint()
except KeyboardInterrupt as e:
    print("user stop: ", e)
except BaseException as e:
    print(f"Exception {e}")
finally:
    # Stop sensor
    if isinstance(sensor, Sensor):
        sensor.stop()
    # Deinitialize display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # Release media buffer
    MediaManager.deinit()
```

## 4. AI Demo

This is a face detection demo:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
import os
import ujson
from media.media import *
from time import *
import nncase_runtime as nn
import ulab.numpy as np
import time
import utime
import image
import random
import gc
import sys
import aidemo

# Custom face detection class, inheriting from AIBase base class
class FaceDetectionApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, anchors, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)  # Call base class constructor
        self.kmodel_path = kmodel_path  # Model file path
        self.model_input_size = model_input_size  # Model input resolution
        self.confidence_threshold = confidence_threshold  # Confidence threshold
        self.nms_threshold = nms_threshold  # NMS (Non-Maximum Suppression) threshold
        self.anchors = anchors  # Anchor data for object detection
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]  # Sensor image resolution, aligned to 16
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]  # Display resolution, aligned to 16
        self.debug_mode = debug_mode  # Debug mode
        self.ai2d = Ai2d(debug_mode)  # Instantiate Ai2d for model preprocessing
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)  # Set Ai2d input/output format and type

    # Configure preprocessing operations, using pad and resize here. Ai2d supports crop/shift/pad/resize/affine. See /sdcard/app/libs/AI2D.py for details
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):  # Timer, enabled if debug_mode > 0
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size  # Initialize ai2d preprocessing config, default to sensor size, can be modified via input_image_size
            top, bottom, left, right = self.get_padding_param()  # Get padding parameters
            self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])  # Pad edges
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)  # Resize image
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])  # Build preprocessing pipeline

    # Custom post-processing for current task, results is a list of model output arrays. Uses aidemo library's face_det_post_process interface
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
                    # Convert detection box coordinates to display resolution
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
    # Display mode, default "hdmi", can choose "hdmi" or "lcd"
    display_mode="hdmi"
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]
    # Set model path and other parameters
    kmodel_path = "/sdcard/app/tests/kmodel/face_detection_320.kmodel"
    # Other parameters
    confidence_threshold = 0.5
    nms_threshold = 0.2
    anchor_len = 4200
    det_dim = 4
    anchors_path = "/sdcard/app/tests/utils/prior_data_320.bin"
    anchors = np.fromfile(anchors_path, dtype=np.float)
    anchors = anchors.reshape((anchor_len, det_dim))
    rgb888p_size = [1920, 1080]

    # Initialize PipeLine for image processing
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()  # Create PipeLine instance
    # Initialize custom face detection instance
    face_det = FaceDetectionApp(kmodel_path, model_input_size=[320, 320], anchors=anchors, confidence_threshold=confidence_threshold, nms_threshold=nms_threshold, rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    face_det.config_preprocess()  # Configure preprocessing

    try:
        while True:
            os.exitpoint()                      # Check for exit signal
            with ScopedTiming("total",1):
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
