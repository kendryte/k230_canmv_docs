# 5.4 YOLO Module API Manual

## 1. Overview

This manual aims to guide developers in deploying and using models trained and converted with YOLOv5, YOLOv8, and YOLO11 through the YOLO module. The models support three types of tasks: classification, detection, and segmentation. It helps users quickly integrate with the YOLO source code and deploy the trained models on the K230. For YOLO usage examples, refer to the documentation: [YOLO Battle](../../example/ai/YOLO_Battle.md).

## 2. API Introduction

### 2.1 YOLOv5 Class

#### 2.1.1 Constructor

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

#### 2.1.2 config_preprocess

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

#### 2.1.3 run

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

#### 2.1.4 draw_result

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

#### 2.1.5 Example Programs

The following is an example program for the `YOLOv5` detection task:

```python
from libs.YOLO import YOLOv5
import os,sys,gc
import ulab.numpy as np
import image

# Read an image from the local disk and convert from HWC to CHW
def read_img(img_path):
    img_data = image.Image(img_path)
    img_data_rgb888=img_data.to_rgb888()
    img_hwc=img_data_rgb888.to_numpy_ref()
    shape=img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_tmp_trans = img_tmp.transpose()
    img_res=img_tmp_trans.copy()
    img_return=img_res.reshape((shape[2],shape[0],shape[1]))
    return img_return,img_data_rgb888

if __name__=="__main__":
    # You can modify the path to fit your own model
    img_path="/data/test_images/test.jpg"
    kmodel_path="/data/yolo_kmodels/det_yolov5n_320.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.5
    nms_threshold=0.45
    model_input_size=[320,320]
    img,img_ori=read_img(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="detect",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    try:
        res=yolo.run(img)
        yolo.draw_result(res,img_ori)
        gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
```

The above code shows how to use `YOLOv5` for image inference.

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv5
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # Display mode, default is "hdmi", can choose "hdmi" or "lcd"
    display_mode="hdmi"
    rgb888p_size=[1280,720]
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]
    # You can modify the path to fit your own model
    kmodel_path="/data/yolo_kmodels/det_yolov5n_320.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.8
    nms_threshold=0.45
    model_input_size=[320,320]
    # Initialize the PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_size=display_size,display_mode=display_mode)
    pl.create()
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="detect",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                # Infer frame by frame
                img=pl.get_frame()
                res=yolo.run(img)
                yolo.draw_result(res,pl.osd_img)
                pl.show_image()
                gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
        pl.destroy()
```

The above code shows how to use `YOLOv5` for video inference.

### 2.2 YOLOv8 Class

#### 2.2.1 Constructor

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
| task_type | Task type | Supports three types of tasks, with options 'classify'/'detect'/'segment'. | str |
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

#### 2.2.2 config_preprocess

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

#### 2.2.3 run

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

#### 2.2.4 draw_result

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

#### 2.2.5 Example Programs

The following is an example program for the `YOLOv8` classification task:

```python
from libs.YOLO import YOLOv8
import os,sys,gc
import ulab.numpy as np
import image

# Read an image from the local disk and convert from HWC to CHW
def read_img(img_path):
    img_data = image.Image(img_path)
    img_data_rgb888=img_data.to_rgb888()
    img_hwc=img_data_rgb888.to_numpy_ref()
    shape=img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_tmp_trans = img_tmp.transpose()
    img_res=img_tmp_trans.copy()
    img_return=img_res.reshape((shape[2],shape[0],shape[1]))
    return img_return,img_data_rgb888

if __name__=="__main__":
    # You can modify the path parameters according to your model
    img_path="/data/test_images/test_apple.jpg"
    kmodel_path="/data/yolo_kmodels/cls_yolov8n_224.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.5
    model_input_size=[224,224]
    img,img_ori=read_img(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv8 instance
    yolo=YOLOv8(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    try:
        res=yolo.run(img)
        yolo.draw_result(res,img_ori)
        gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
```

The above code shows how to use `YOLOv8` for image inference.

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv8
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # Display mode, default is "hdmi", can choose "hdmi" or "lcd"
    display_mode="hdmi"
    rgb888p_size=[1280,720]
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]
    # You can modify the path parameters according to your model
    kmodel_path="/data/yolo_kmodels/cls_yolov8n_224.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.8
    model_input_size=[224,224]
    # Initialize the PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_size=display_size,display_mode=display_mode)
    pl.create()
    # Initialize the YOLOv8 instance
    yolo=YOLOv8(task_type="classify",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                # Infer frame by frame
                img=pl.get_frame()
                res=yolo.run(img)
                yolo.draw_result(res,pl.osd_img)
                pl.show_image()
                gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
        pl.destroy()
```

The above code shows how to use `YOLOv8` for video inference.

### 2.3 YOLO11 Class

#### 2.3.1 Constructor

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
| task_type | Task type | Supports three types of tasks, with available options: 'classify', 'detect', 'segment'. | str |
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

#### 2.3.2 config_preprocess

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

#### 2.3.3 run

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

#### 2.3.4 draw_result

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

#### 2.3.5 Example Programs

The following is an example program for the `YOLO11` segmentation task:

```python
from libs.YOLO import YOLO11
import os,sys,gc
import ulab.numpy as np
import image

# Read an image from the local disk and convert from HWC to CHW
def read_img(img_path):
    img_data = image.Image(img_path)
    img_data_rgb888=img_data.to_rgb888()
    img_hwc=img_data_rgb888.to_numpy_ref()
    shape=img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_tmp_trans = img_tmp.transpose()
    img_res=img_tmp_trans.copy()
    img_return=img_res.reshape((shape[2],shape[0],shape[1]))
    return img_return,img_data_rgb888

if __name__=="__main__":
    # You can modify the path parameters according to your model
    img_path="/data/test_images/test.jpg"
    kmodel_path="/data/yolo_kmodels/seg_yolo11n_320.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    model_input_size=[320,320]
    img,img_ori=read_img(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    try:
        res=yolo.run(img)
        yolo.draw_result(res,img_ori)
        gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
```

The above code shows how to use `YOLO11` for image inference.

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLO11
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # Display mode, default is "hdmi", can choose "hdmi" or "lcd"
    display_mode="hdmi"
    rgb888p_size=[320,320]
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]
    # You can modify the path parameters according to your model
    kmodel_path="/data/yolo_kmodels/seg_yolo11n_320.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    model_input_size=[320,320]
    # Initialize the PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_size=display_size,display_mode=display_mode)
    pl.create()
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="segment",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                # Infer frame by frame
                img=pl.get_frame()
                res=yolo.run(img)
                yolo.draw_result(res,pl.osd_img)
                pl.show_image()
                gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
        pl.destroy()
```

The above code shows how to use `YOLO11` for video inference.
