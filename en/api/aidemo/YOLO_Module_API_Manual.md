# YOLO Module API Manual

## Overview

This manual aims to guide developers in deploying and using models trained and converted with YOLOv5, YOLOv8, and YOLO11 through the YOLO module. The models support three types of tasks: classification, detection, and segmentation. It helps users quickly integrate with the YOLO source code and deploy the trained models on the K230. For YOLO usage examples, refer to the documentation: [YOLO Battle](../../example/ai/YOLO_Battle.md).

## API Introduction

### YOLOv5 Class

#### Constructor

**Description**
This is the constructor of the encapsulated `YOLOv5` module, which initializes a `YOLOv5` type to obtain a `YOLOv5` instance.

**Syntax**

```python
from libs.YOLO import YOLOv5

yolo=YOLOv5(task_type="classify",mode="image",kmodel_path="yolov5_det.kmodel",labels=["apple","banana","orange"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,nms_thresh=0.25,max_boxes_num=50,debug_mode=0)
```

**Parameters**

| Parameter Name | Description | Explanation | Type |
| --- | --- | --- | --- |
| task_type | Task type | Supports three types of tasks, with options 'classify'/'detect'/'segment'. | str |
| mode | Inference mode | Supports two inference modes, with options 'image'/'video'. 'image' indicates image inference, and 'video' indicates real - time video stream inference from the camera. | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board. | str |
| labels | Class label list | The label names of different classes. | list[str] |
| rgb888p_size | Inference frame resolution | The resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640]. | list[int] |
| model_input_size | Model input resolution | The input resolution during YOLOv5 model training, such as [224,224], [320,320], [640,640]. | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supporting hdmi ([1920,1080]) and lcd ([800,480]). | list[int] |
| conf_thresh | Confidence threshold | The class confidence threshold for classification tasks and the target confidence threshold for detection and segmentation tasks, such as 0.5. | float [0~1] |
| nms_thresh | NMS threshold | The non - maximum suppression threshold, required for detection and segmentation tasks. | float [0~1] |
| mask_thresh | Mask threshold | The binary threshold for segmenting objects in the detection box in segmentation tasks. | float [0~1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of image. | int |
| debug_mode | Debug mode | Whether the timing function is enabled, with options 0/1. 0 means no timing, and 1 means timing. | int [0/1] |

**Return Value**

| Return Value | Description |
| --- | --- |
| YOLOv5 | YOLOv5 instance |

#### config_preprocess

**Description**
This is the YOLOv5 pre - processing configuration function.

**Syntax**

```python
yolo.config_preprocess()
```

**Parameters**

| Parameter Name | Description | Input/Output | Explanation |
| --- | --- | --- | --- |
| None |  |  |  |

**Return Value**

| Return Value | Description |
| --- | --- |
| None |  |

#### run

**Description**
Infer one frame of image and return the inference result for use in the `draw_result` method. For classification tasks, it returns the class index and score. For detection tasks, it returns a list of detection box positions, scores, and class indices. For segmentation tasks, it returns the mask result and a list of detection box positions, scores, and class indices.

**Syntax**

```python
res=yolo.run(img)
```

**Parameters**

| Parameter Name | Description | Input/Output | Explanation |
| --- | --- | --- | --- |
| img | The image to be inferred in the format of ulab.numpy.ndarray, or one frame of image obtained from the video stream through `get_frame`. | Input |  |

**Return Value**

| Return Value | Description |
| --- | --- |
| res | The post - processing result of the model. The return values vary for different tasks. For classification tasks, it returns the class index and score. For detection tasks, it returns a list of detection box positions, scores, and class indices. For segmentation tasks, it returns the mask result and a list of detection box positions, scores, and class indices. |

#### draw_result

**Description**
Draw the `YOLOv5` inference result on the screen or image.

**Syntax**

```python
yolo.draw_result(res,img_ori)
```

**Parameters**

| Parameter Name | Description | Input/Output | Explanation |
| --- | --- | --- | --- |
| res | The inference result of `YOLOv5` | Input |  |
| img_ori | The Image instance to be drawn on | Input | From `read_img` or `pl.osd_img` |

**Return Value**

| Return Value | Description |
| --- | --- |
| None |  |

#### Example Programs

The following is an example program for the `YOLOv5` detection task:

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/sdcard/examples/utils/test_fruit.jpg"
    kmodel_path = "/sdcard/examples/kmodel/fruit_det_yolov5n_320.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    confidence_threshold = 0.5
    nms_threshold = 0.45
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLOv5 instance
    yolo = YOLOv5(task_type="detect", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

The above code shows how to use `YOLOv5` for image inference.

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/sdcard/examples/kmodel/fruit_det_yolov5n_320.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd"
    rgb888p_size = [640, 360]
    confidence_threshold = 0.8
    nms_threshold = 0.45
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLOv5 instance
    yolo = YOLOv5(task_type="detect", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total", 1):
            img = pl.get_frame()
            res = yolo.run(img)
            yolo.draw_result(res, pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

The above code shows how to use `YOLOv5` for video inference.

### YOLOv8 Class

#### Constructor

**Description**
This is the constructor of the encapsulated `YOLOv8` module, which initializes a `YOLOv8` type to obtain a `YOLOv8` instance.

**Syntax**

```python
from libs.YOLO import YOLOv8

yolo=YOLOv8(task_type="classify",mode="image",kmodel_path="yolov8_det.kmodel",labels=["apple","banana","orange"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,nms_thresh=0.25,max_boxes_num=50,debug_mode=0)
```

**Parameters**

| Parameter Name | Description | Explanation | Type |
| --- | --- | --- | --- |
| task_type | Task type | Supports four types of tasks, with options 'classify'/'detect'/'segment'/'obb'. | str |
| mode | Inference mode | Supports two inference modes, with options 'image'/'video'. 'image' indicates image inference, and 'video' indicates real - time video stream inference from the camera. | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board. | str |
| labels | Class label list | The label names of different classes. | list[str] |
| rgb888p_size | Inference frame resolution | The resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640]. | list[int] |
| model_input_size | Model input resolution | The input resolution during YOLOv8 model training, such as [224,224], [320,320], [640,640]. | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supporting hdmi ([1920,1080]) and lcd ([800,480]). | list[int] |
| conf_thresh | Confidence threshold | The class confidence threshold for classification tasks and the target confidence threshold for detection and segmentation tasks, such as 0.5. | float [0~1] |
| nms_thresh | NMS threshold | The non - maximum suppression threshold, required for detection and segmentation tasks. | float [0~1] |
| mask_thresh | Mask threshold | The binary threshold for segmenting objects in the detection box in segmentation tasks. | float [0~1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of image. | int |
| debug_mode | Debug mode | Whether the timing function is enabled, with options 0/1. 0 means no timing, and 1 means timing. | int [0/1] |

**Return Value**

| Return Value | Description |
| --- | --- |
| YOLOv8 | YOLOv8 instance |

#### config_preprocess

**Description**
This is the YOLOv8 pre - processing configuration function.

**Syntax**

```python
yolo.config_preprocess()
```

**Parameters**

| Parameter Name | Description | Input/Output | Explanation |
| --- | --- | --- | --- |
| None |  |  |  |

**Return Value**

| Return Value | Description |
| --- | --- |
| None |  |

#### run

**Description**
Infer one frame of image and return the inference result for use in the `draw_result` method. For classification tasks, it returns the class index and score. For detection tasks, it returns a list of detection box positions, scores, and class indices. For segmentation tasks, it returns the mask result and a list of detection box positions, scores, and class indices.

**Syntax**

```python
res=yolo.run(img)
```

**Parameters**

| Parameter Name | Description | Input/Output | Explanation |
| --- | --- | --- | --- |
| img | The image to be inferred in the format of ulab.numpy.ndarray, or one frame of image obtained from the video stream through `get_frame`. | Input |  |

**Return Value**

| Return Value | Description |
| --- | --- |
| res | The post - processing result of the model. The return values vary for different tasks. For classification tasks, it returns the class index and score. For detection tasks, it returns a list of detection box positions, scores, and class indices. For segmentation tasks, it returns the mask result and a list of detection box positions, scores, and class indices. |

#### draw_result

**Description**
Draw the `YOLOv8` inference result on the screen or image.

**Syntax**

```python
yolo.draw_result(res,img_ori)
```

**Parameters**

| Parameter Name | Description | Input/Output | Explanation |
| --- | --- | --- | --- |
| res | The inference result of `YOLOv8` | Input |  |
| img_ori | The Image instance to be drawn on | Input | From `read_img` or `pl.osd_img` |

**Return Value**

| Return Value | Description |
| --- | --- |
| None |  |

#### Example Programs

The following is an example program for the `YOLOv8` classification task:

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/sdcard/examples/utils/test_fruit.jpg"
    kmodel_path = "/sdcard/examples/kmodel/fruit_det_yolov8n_320.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    confidence_threshold = 0.5
    nms_threshold = 0.45
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLOv8 instance
    yolo = YOLOv8(task_type="detect", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

The above code shows how to use `YOLOv8` for image inference.

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/sdcard/examples/kmodel/fruit_det_yolov8n_320.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd"
    rgb888p_size = [640, 360]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    # Initialize PipeLine
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLOv8 instance
    yolo = YOLOv8(task_type="detect", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total", 1):
            # Process each frame
            img = pl.get_frame()
            res = yolo.run(img)
            yolo.draw_result(res, pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

The above code shows how to use `YOLOv8` for video inference.

### YOLO11 Class

#### Constructor

**Description**
This is the constructor of the encapsulated YOLO11 module, which initializes the YOLO11 type to obtain a YOLO11 instance.

**Syntax**

```python
from libs.YOLO import YOLO11

yolo=YOLO11(task_type="segment",mode="image",kmodel_path="yolo11_det.kmodel",labels=["apple","banana","orange"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,nms_thresh=0.25,mask_thresh=0.5,max_boxes_num=50,debug_mode=0)
```

**Parameters**

| Parameter Name | Description | Explanation | Type |
| --- | --- | --- | --- |
| task_type | Task type | Supports four types of tasks, with available options: 'classify', 'detect', 'segment', 'obb'. | str |
| mode | Inference mode | Supports two inference modes, with available options: 'image' and 'video'. 'image' means inferring images, and 'video' means inferring real - time video streams captured by the camera. | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board. | str |
| labels | Class label list | The label names of different classes. | list[str] |
| rgb888p_size | Inference frame resolution | The resolution of the current inference frame, such as [1920, 1080], [1280, 720], [640, 640]. | list[int] |
| model_input_size | Model input resolution | The input resolution during the training of the YOLO11 model, such as [224, 224], [320, 320], [640, 640]. | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supporting HDMI ([1920, 1080]) and LCD ([800, 480]). | list[int] |
| conf_thresh | Confidence threshold | The class confidence threshold for classification tasks and the target confidence threshold for detection and segmentation tasks, e.g., 0.5. | float [0~1] |
| nms_thresh | NMS threshold | The non - maximum suppression threshold, required for detection and segmentation tasks. | float [0~1] |
| mask_thresh | Mask threshold | The binary threshold for segmenting objects within the detection box in segmentation tasks. | float [0~1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of an image. | int |
| debug_mode | Debug mode | Whether the timing function is enabled. Options are 0 or 1, where 0 means no timing and 1 means timing. | int [0/1] |

**Return Value**

| Return Value | Description |
| --- | --- |
| YOLO11 | YOLO11 instance |

#### config_preprocess

**Description**
This is the YOLO11 pre - processing configuration function.

**Syntax**

```python
yolo.config_preprocess()
```

**Parameters**

| Parameter Name | Description | Input/Output | Explanation |
| --- | --- | --- | --- |
| None |  |  |  |

**Return Value**

| Return Value | Description |
| --- | --- |
| None |  |

#### run

**Description**
Infer one frame of an image and return the inference result for use in the `draw_result` method. For classification tasks, it returns the class index and score. For detection tasks, it returns a list of detection box positions, scores, and class indices. For segmentation tasks, it returns the mask result and a list of detection box positions, scores, and class indices.

**Syntax**

```python
res=yolo.run(img)
```

**Parameters**

| Parameter Name | Description | Input/Output | Explanation |
| --- | --- | --- | --- |
| img | The image to be inferred in the format of `ulab.numpy.ndarray`, or one frame of an image obtained from the video stream through `get_frame`. | Input |  |

**Return Value**

| Return Value | Description |
| --- | --- |
| res | The post - processing result of the model. The return values vary for different tasks. For classification tasks, it returns the class index and score. For detection tasks, it returns a list of detection box positions, scores, and class indices. For segmentation tasks, it returns the mask result and a list of detection box positions, scores, and class indices. |

#### draw_result

**Description**
Draw the `YOLO11` inference result on the screen or an image.

**Syntax**

```python
yolo.draw_result(res,img_ori)
```

**Parameters**

| Parameter Name | Description | Input/Output | Explanation |
| --- | --- | --- | --- |
| res | The inference result of `YOLO11` | Input |  |
| img_ori | The Image instance to be drawn on | Input | From `read_img` or `pl.osd_img` |

**Return Value**

| Return Value | Description |
| --- | --- |
| None |  |

#### Example Programs

The following is an example program for the `YOLO11` segmentation task:

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/sdcard/examples/utils/test_fruit.jpg"
    kmodel_path = "/sdcard/examples/kmodel/fruit_det_yolo11n_320.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    confidence_threshold = 0.5
    nms_threshold = 0.45
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLO11 instance
    yolo = YOLO11(task_type="detect", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

The above code shows how to use `YOLO11` for image inference.

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/sdcard/examples/kmodel/fruit_det_yolo11n_320.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd"
    rgb888p_size = [640, 360]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    # Initialize PipeLine
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLO11 instance
    yolo = YOLO11(task_type="detect", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total", 1):
            # Process each frame
            img = pl.get_frame()
            res = yolo.run(img)
            yolo.draw_result(res, pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

The above code shows how to use `YOLO11` for video inference.
