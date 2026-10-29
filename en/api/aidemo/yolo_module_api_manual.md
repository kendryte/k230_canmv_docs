# `YOLO` Module API Manual

## Overview

This manual is intended to guide developers in using the YOLO module to deploy models trained and converted using YOLOv5, YOLOv8, YOLO11, and YOLO26, helping users quickly interface with the YOLO source code and run trained models on the K230. For YOLO usage examples, refer to the documentation: [yolo_battle](../../example/ai/yolo_battle.md)

The task types supported by each class are as follows:

| Class | classify | detect | segment | obb (rotated object detection) | pose (keypoint detection) |
|----|------|------|------|------|------|
| `YOLOv5`  | ✅ | ✅ | ✅ | ❌ | ❌ |
| `YOLOv8`  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `YOLO11`  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `YOLO26`  | ✅ | ✅ | ✅ | ✅ | ✅ |

The corresponding examples are located in the development board's `CanMV/sdcard/examples/20-YOLO-Module-Examples` directory, and each task type provides two scripts: `*_image.py` (single image inference) and `*_video.py` (video stream inference).

## API Introduction

### YOLOv5 Class

#### Constructor

**Description**

The constructor of the encapsulated `YOLOv5` module initializes the `YOLOv5` type to obtain a `YOLOv5` instance.

**Syntax**  

```python
from libs.YOLO import YOLOv5

yolo=YOLOv5(task_type="classify",mode="image",kmodel_path="yolov5_det.kmodel",labels=["apple","banana","orange"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,nms_thresh=0.25,max_boxes_num=50,debug_mode=0)
```

**Parameters**  

| Parameter Name  | Description           | Notes                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task type       | Supports three types of tasks, options are 'classify'/'detect'/'segment';        | str          |
| mode             | Inference mode       | Supports two inference modes, options are 'image'/'video', 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel path     | The path of the kmodel copied to the development board;                                   | str          |
| labels           | Class label list   | Label names for different classes;                                         | list[str]    |
| rgb888p_size     | Inference frame resolution   | The resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model input resolution | The input resolution when the YOLOv5 model was trained, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence threshold     | Class confidence threshold for classification tasks, object confidence threshold for detection and segmentation tasks, such as 0.5; | float [0~1] |
| nms_thresh       | nms threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float [0~1] |
| mask_thresh      | mask threshold       | The binarization threshold for segmenting objects within the detection box in segmentation tasks;             | float [0~1] |
| max_boxes_num    | Maximum number of detection boxes   | The maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| debug_mode       | Debug mode       | Whether the timing function is enabled, options are 0/1, 0 for no timing, 1 for timing;            | int [0/1]   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| YOLOv5 | YOLOv5 instance                  |

#### config_preprocess

**Description**

YOLOv5 preprocessing configuration function.

**Syntax**  

```python
yolo.config_preprocess()
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

#### run

**Description**

Infer one frame of image, and return the inference result for use by the `draw_result` method. The classification task returns the class index and score, the detection task returns a list of detection box positions, scores, and class indices, and the segmentation task returns the mask results and a list of detection box positions, scores, and class indices.

**Syntax**  

```python
res=yolo.run(img)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| img   | The image to be inferred in the format of ulab.numpy.ndarray, or a frame of image obtained from the video stream via `get_frame`               |   Input    |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| res     | Model post-processing result, which differs depending on the task. The classification task returns the class index and score, the detection task returns a list of detection box positions, scores, and class indices, and the segmentation task returns the mask results and a list of detection box positions, scores, and class indices.|

#### draw_result

**Description**

Draw the `YOLOv5` inference result on the screen or image.

**Syntax**  

```python
yolo.draw_result(res,img_ori)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| res  | The inference result of `YOLOv5`                   |   Input    |   |
| img_ori  | The Image instance to be drawn                   |   Input    | From `read_img` or `pl.osd_img`  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

#### deinit

**Description**

Release the native resources occupied by the `YOLOv5` instance, such as the kmodel, AI2D, and the mask cache for segmentation tasks. This must be called when inference ends or when switching models; otherwise, repeatedly creating instances will exhaust the nncase memory pool.

**Syntax**  

```python
yolo.deinit()
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     | Safe to call repeatedly.                   |

```{admonition} Tip
:class: note
`deinit()` internally completes `gc.collect()` and `nncase_runtime.shrink_memory_pool()`, which returns memory to the nncase memory pool, so there is no need to manually call these again when subsequently loading another kmodel in the same script. Repeated calls to `deinit()` are safe; if a native resource fails to be released, the instance will retain it for the next retry and throw an exception.
```

#### Example Program

The following is an example program for the `YOLOv5` detection task:

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify it to your own test image, model path, label names, and model input size
    img_path="/sdcard/examples/utils/test_fruit.jpg"
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolov5n_320.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    nms_threshold=0.45
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="detect",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

The above code shows the code for performing image inference using `YOLOv5`.

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify it to your own model path, label names, and model input size
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolov5n_320.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc. Refer to the PipeLine manual for valid values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.8
    nms_threshold=0.45
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="detect",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

The above code shows the code for performing video inference using `YOLOv5`.

### YOLOv8 Class

#### Constructor

**Description**

Encapsulated `YOLOv8` module constructor, initializes the `YOLOv8` type to get a `YOLOv8` instance.

**Syntax**  

```python
from libs.YOLO import YOLOv8

yolo=YOLOv8(task_type="classify",mode="image",kmodel_path="yolov8_det.kmodel",labels=["apple","banana","orange"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,nms_thresh=0.25,max_boxes_num=50,debug_mode=0)
```

**Parameters**  

| Parameter Name   | Description       | Instructions                                                                                                                                                                            | Type         |
| ---------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| task_type        | Task Type         | Supports five types of tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';                                                                                                  | str          |
| mode             | Inference Mode    | Supports two inference modes, options are 'image'/'video', 'image' means inference on an image, 'video' means inference on a real-time video stream captured by the camera;            | str          |
| kmodel_path      | kmodel Path       | Path of the kmodel copied to the development board;                                                                                                                                     | str          |
| labels           | Category Label List | Names of labels for different categories;                                                                                                                                               | list[str]    |
| rgb888p_size     | Inference Frame Resolution | Resolution of the current frame to infer, such as [1920,1080], [1280,720], [640,640];                                                                                            | list[int]    |
| model_input_size | Model Input Resolution | Input resolution used during YOLOv8 model training, such as [224,224], [320,320], [640,640];                                                                                       | list[int]    |
| display_size     | Display Resolution | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]);                                                                                                  | list[int]    |
| conf_thresh      | Confidence Threshold | Category confidence threshold for classification tasks, target confidence threshold for detection and segmentation tasks, such as 0.5;                                                | float [0~1] |
| nms_thresh       | nms Threshold     | Non-maximum suppression threshold, required for detection and segmentation tasks;                                                                                                       | float [0~1] |
| mask_thresh      | mask Threshold    | Binarization threshold for segmenting objects in the detection box in segmentation tasks;                                                                                              | float [0~1] |
| max_boxes_num    | Max Detection Boxes | Max number of detection boxes allowed to be returned in one frame;                                                                                                                       | int          |
| kp_num           | Number of Keypoints | Number of keypoints in the keypoint detection task;                                                                                                                                     | int          |
| kp_dim           | Keypoint Dimension | Dimension of keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model;                                                                    | int【2/3】    |
| debug_mode       | Debug Mode        | Whether the timing function is enabled, options 0/1, 0 means no timing, 1 means timing;                                                                                               | int [0/1]   |

**Return Value**  

| Return Value | Description                  |
|--------|---------------------------------|
| YOLOv8 | YOLOv8 instance                  |

#### config_preprocess

**Description**

YOLOv8 preprocessing configuration function.

**Syntax**  

```python
yolo.config_preprocess()
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Instructions |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

#### run

**Description**

Infer one frame of image, return the inference result for use by the `draw_result` method. The classification task returns the category index and score, the detection task returns the list of detection box positions, scores, and category indices, the segmentation task returns the mask results and the list of detection box positions, scores, and category indices, the rotated object detection returns the list of four-point coordinates of the rotated detection box, and the keypoint detection returns the detection box positions, category indices, scores, and keypoint list.

**Syntax**  

```python
res=yolo.run(img)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Instructions |
|----------|-------------------------------|-----------|------|
| img   | An image to be inferred in the format of ulab.numpy.ndarray, or a frame of image obtained from the video stream via `get_frame`               |   Input    |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| res     | Model post-processing result, different tasks return different values. The classification task returns the category index and score, the detection task returns the list of detection box positions, scores, and category indices, the segmentation task returns the mask results and the list of detection box positions, scores, and category indices, the rotated object detection returns the list of four-point coordinates of the rotated detection box, and the keypoint detection returns the detection box positions, category indices, scores, and keypoint list.|

#### draw_result

**Description**

Draw the `YOLOv8` inference result on the screen or image.

**Syntax**  

```python
yolo.draw_result(res,img_ori)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Instructions |
|----------|-------------------------------|-----------|------|
| res  | Inference result of `YOLOv8`                   |   Input    |   |
| img_ori  | Image instance to be drawn                   |   Input    | From `read_img` or `pl.osd_img`  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

#### deinit

**Description**

Release the native resources occupied by the `YOLOv8` instance, such as kmodel, AI2D, and the mask cache for segmentation tasks. Must be called when inference ends or when switching models, otherwise repeatedly creating instances will exhaust the nncase memory pool.

**Syntax**  

```python
yolo.deinit()
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Instructions |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     | Safe to call repeatedly.                   |

```{admonition} Tip
:class: note
`deinit()` internally completes `gc.collect()` and `nncase_runtime.shrink_memory_pool()`, which will return memory to the nncase memory pool, so there is no need to manually call again when loading another kmodel in the same script. Repeated calls to `deinit()` are safe; if a certain native resource release fails, the instance will keep it for the next retry and throw an exception.
```

#### Example Program

The following gives an example program for the `YOLOv8` classification task:

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is just an example. For custom scenarios, please modify to your own test image, model path, label name, and model input size
    img_path="/sdcard/examples/utils/test_fruit.jpg"
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolov8n_320.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    nms_threshold=0.45
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize YOLOv8 instance
    yolo=YOLOv8(task_type="detect",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

The above code shows the code for image inference using `YOLOv8`.

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is just an example. For custom scenarios, please modify to your own model path, label name, and model input size
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolov8n_320.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when you need to specify
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    nms_threshold=0.45
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize YOLOv8 instance
    yolo=YOLOv8(task_type="detect",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            # Infer frame by frame
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

The above code shows the code for video inference using `YOLOv8`.

### YOLO11 Class

#### Constructor

**Description**

Encapsulated YOLO11 module constructor. Initializes the YOLO11 type to obtain a YOLO11 instance.

**Syntax**  

```python
from libs.YOLO import YOLO11

yolo=YOLO11(task_type="segment",mode="image",kmodel_path="yolo11_det.kmodel",labels=["apple","banana","orange"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,nms_thresh=0.25,mask_thresh=0.5,max_boxes_num=50,debug_mode=0)
```

**Parameters**  

| Parameter Name    | Description      | Notes                                                         | Type         |
| ---------------- | ---------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task type        | Supports five task types, with optional values 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference mode   | Supports two inference modes, with optional values 'image'/'video'; 'image' indicates inferring images, 'video' indicates inferring real-time video streams captured by the camera; | str          |
| kmodel_path      | kmodel path      | Path of the kmodel copied to the development board;                                   | str          |
| labels           | Class label list | Label names for different classes;                                         | list[str]    |
| rgb888p_size     | Inference frame resolution | Resolution of the current frame being inferred, e.g., [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model input resolution | Input resolution when the YOLO11 model was trained, e.g., [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display resolution | Set when the inference mode is 'video'; supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence threshold | Class confidence threshold for classification tasks, object confidence threshold for detection and segmentation tasks, e.g., 0.5; | float [0~1] |
| nms_thresh       | nms threshold    | Non-maximum suppression threshold; required for detection and segmentation tasks;                       | float [0~1] |
| mask_thresh      | mask threshold   | Binarization threshold for segmenting the object inside the detection box in segmentation tasks;             | float [0~1] |
| max_boxes_num    | Maximum number of detection boxes | Maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| kp_num           | Number of keypoints | Number of keypoints in a keypoint detection task;                              | int        |
| kp_dim           | Keypoint dimension | Dimension of keypoints in a keypoint detection task; only 2 and 3 are supported, determined by the trained model;    | int【2/3】  |
| debug_mode       | Debug mode       | Whether the timing function is enabled; optional values 0/1, 0 means no timing, 1 means timing;            | int [0/1]   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| YOLO11 | YOLO11 instance                  |

#### config_preprocess

**Description**

YOLO11 preprocessing configuration function.

**Syntax**  

```python
yolo.config_preprocess()
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

#### run

**Description**

Infer one frame of image and return the inference result for use by the `draw_result` method. For classification tasks, it returns the class index and score; for detection tasks, it returns a list of detection box positions, scores, and class indices; for segmentation tasks, it returns the mask results along with a list of detection box positions, scores, and class indices; for oriented object detection, it returns a list of the four point coordinates of the rotated detection box; for keypoint detection, it returns the detection box positions, class indices, scores, and keypoints list.

**Syntax**  

```python
res=yolo.run(img)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| img   | Image to be inferred in the format of ulab.numpy.ndarray, or a frame obtained from the video stream via `get_frame`               |   Input    |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| res     | Model post-processing result; different tasks return different values. For classification tasks, it returns the class index and score; for detection tasks, it returns a list of detection box positions, scores, and class indices; for segmentation tasks, it returns the mask results along with a list of detection box positions, scores, and class indices; for oriented object detection, it returns a list of the four point coordinates of the rotated detection box; for keypoint detection, it returns the detection box positions, class indices, scores, and keypoints list.|

#### draw_result

**Description**

Draw the `YOLO11` inference result on the screen or image.

**Syntax**  

```python
yolo.draw_result(res,img_ori)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| res  | Inference result of `YOLO11`                   |   Input    |   |
| img_ori  | Image instance to be drawn                   |   Input    | Comes from `read_img` or `pl.osd_img`  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

#### deinit

**Description**

Releases the native resources occupied by the `YOLO11` instance, such as the kmodel, AI2D, and the mask cache of segmentation tasks. Must be called when inference ends or when switching models; otherwise, repeatedly creating instances will exhaust the nncase memory pool.

**Syntax**  

```python
yolo.deinit()
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     | Safe to call repeatedly.                   |

```{admonition} Tip
:class: note
`deinit()` internally completes `gc.collect()` and `nncase_runtime.shrink_memory_pool()`, which returns memory to the nncase memory pool. Therefore, there is no need to manually call these when loading another kmodel subsequently in the same script. Repeatedly calling `deinit()` is safe; if the release of a native resource fails, the instance will retain it for the next retry and raise an exception.
```

#### Example Program

The following gives an example program for the `YOLO11` segmentation task:

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example; please modify it to your own test image, model path, label names, and model input size for your custom scenario
    img_path="/sdcard/examples/utils/test_fruit.jpg"
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolo11n_320.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    nms_threshold=0.45
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="detect",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

The code above gives an example of using `YOLO11` for image inference.

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example; please modify it to your own model path, label names, and model input size for your custom scenario
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolo11n_320.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for valid values
    display_mode="auto"
    # None means using the default resolution of the screen driver; specify [width, height] if needed
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    nms_threshold=0.45
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create()
    display_size=pl.get_display_size()
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="detect",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            # Frame-by-frame inference
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

The code above gives an example of using `YOLO11` for video inference.

### YOLO26 Class

#### Constructor

**Description**

Constructor of the encapsulated YOLO26 module, initializes the YOLO26 type to obtain a YOLO26 instance.

**Syntax**  

```python
from libs.YOLO import YOLO26

yolo=YOLO26(task_type="pose",mode="image",kmodel_path="yolo26n_pose.kmodel",labels=["people"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,mask_thresh=0.5,kp_num=17,kp_dim=3,max_boxes_num=50,debug_mode=0)
```

**Parameters**  

| Parameter Name   | Description       | Specification                                                         | Type         |
| ---------------- | ------------------ | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports five types of tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference Mode       | Supports two inference modes, options are 'image'/'video', 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | kmodel path copied to the development board;                                   | str          |
| labels           | Category Labels List   | Label names for different categories;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | Resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | Input resolution when training YOLO11 model, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | Category confidence threshold for classification tasks, target confidence threshold for detection and segmentation tasks, such as 0.5; | float [0~1] |
| mask_thresh      | Mask Threshold       | Binarization threshold for segmenting objects in detection boxes in segmentation tasks;             | float [0~1] |
| max_boxes_num    | Maximum Detection Box Count   | Maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| kp_num           | Number of Keypoints     | Number of keypoints in keypoint detection tasks;                              | int        |
| kp_dim           | Keypoint Dimension     | Dimension of keypoints in keypoint detection tasks, only 2 and 3 are supported, determined by the training model;    | int【2/3】  |
| debug_mode       | Debug Mode       | Whether the timing function takes effect, options 0/1, 0 means no timing, 1 means timing;            | int [0/1]   |

> Note: The YOLO26 module no longer includes the `nms_thresh` parameter because the YOLO26 model directly outputs results with semantic information.

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| YOLO26 | YOLO26 instance                  |

#### config_preprocess

**Description**

YOLO26 preprocessing configuration function.

**Syntax**  

```python
yolo.config_preprocess()
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

#### run

**Description**

Infer one frame of image and return the inference result for use by the `draw_result` method. Classification tasks return category index and score, detection tasks return a list of detection box positions, scores, and category indices, segmentation tasks return mask results and a list of detection box positions, scores, and category indices, rotated object detection returns a list of the four point coordinates of the rotated detection box, and keypoint detection returns a list of detection box positions, category indices, scores, and keypoints.

**Syntax**  

```python
res=yolo.run(img)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| img   | Image to be inferred in the format of ulab.numpy.ndarray, or a frame obtained from the video stream through `get_frame`               |   Input    |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| res     | Model post-processing results, different return values for different tasks. Classification tasks return category index and score, detection tasks return a list of detection box positions, scores, and category indices, segmentation tasks return mask results and a list of detection box positions, scores, and category indices, rotated object detection returns a list of the four point coordinates of the rotated detection box, and keypoint detection returns a list of detection box positions, category indices, scores, and keypoints. |

#### draw_result

**Description**

Draws `YOLO26` inference results on the screen or image.

**Syntax**  

```python
yolo.draw_result(res,img_ori)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| res  | `YOLO26` inference result                   |   Input    |   |
| img_ori  | Image instance to be drawn                   |   Input    | From `read_img` or `pl.osd_img`  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     |                                 |

#### deinit

**Description**

Releases native resources such as the kmodel, AI2D, and mask cache for segmentation tasks occupied by the `YOLO26` instance. Must be called after inference is finished or when switching models; otherwise, repeatedly creating instances will exhaust the nncase memory pool.

**Syntax**  

```python
yolo.deinit()
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| None  |                   |       |   |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| None     | Safe to call repeatedly.                   |

```{admonition} Tip
:class: note
`deinit()` internally has completed `gc.collect()` and `nncase_runtime.shrink_memory_pool()`, which will return memory to the nncase memory pool, so there is no need to manually call it again when subsequently loading another kmodel in the same script. Repeatedly calling `deinit()` is safe; if a certain native resource fails to be released, the instance will retain it for the next retry and throw an exception.
```

#### Example Programs

The following is an example program for the `YOLO26` segmentation task:

```python
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own test image, model path, label name, model input size, number of keypoints, and keypoint dimension for custom scenarios
    img_path="/sdcard/examples/utils/test_pose.jpg"
    kmodel_path="/sdcard/examples/kmodel/yolo26n-pose.kmodel"
    labels = ['person']
    model_input_size=[320,320]
    kp_num=17
    kp_dim=3

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize YOLO26 model (YOLO26 has no nms_thresh parameter)
    yolo=YOLO26(task_type="pose",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,kp_num=kp_num,kp_dim=kp_dim,conf_thresh=confidence_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    print(res)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

The above code shows the code for using `YOLO26` for image inference.

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own model path, label name, model input size, number of keypoints, and keypoint dimension for custom scenarios
    kmodel_path="/sdcard/examples/kmodel/yolo26n-pose.kmodel"
    labels = ["person"]
    model_input_size=[320,320]
    kp_num=17
    kp_dim=3           

    # Display mode, "auto" automatically selects screen driver according to development board model; can also explicitly specify hdmi/lcd/st7701, etc., see PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize YOLO26 model
    yolo=YOLO26(task_type="pose",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,kp_num=kp_num,kp_dim=kp_dim,conf_thresh=confidence_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

The above code shows the code for using `YOLO26` for video inference.
