# `PlatTasks` Module API Manual

## Overview

`libs/PlatTasks.py` is a deployment library that encapsulates models produced by the [Canaan Cloud Training Platform](https://www.kendryte.com/zh/training/start) and the [AICube](../../ai_dev_doc.md#aicube) offline training tool. Each type of task trained on the platform has a fixed model structure and post-processing method. This module encapsulates these details into ready-to-use classes. Users only need to provide the kmodel path and configuration from the deployment package to complete deployment.

All classes inherit from [`AIBase`](./aibase_module_api_manual.md), so they all have basic capabilities such as `run`, `config_preprocess`, `deinit`, and uniformly implement three methods: `postprocess`, `draw_result`, and `get_cur_result`.

| Class | Corresponding Platform Task | Post-processing Dependency |
|----|--------------|------------|
| `ClassificationApp` | Image classification | softmax |
| `DetectionApp` | Image detection | `aicube` native module |
| `SegmentationApp` | Semantic segmentation | `aicube` native module |
| `OCRDetectionApp` | OCR detection | `aicube` native module |
| `OCRRecognitionApp` | OCR recognition | CTC greedy decoding |
| `MetricLearningApp` | Metric learning (self-learning) | Cosine similarity comparison |
| `MultiLabelClassificationApp` | Multi-label classification | sigmoid |

```{admonition} Hint
:class: note
The corresponding examples are located in the development board's `CanMV/sdcard/examples/19-CloudPlatScripts` directory. Each type of task provides two scripts: `deploy_*_image.py` (single image inference) and `deploy_*_video.py` (video stream inference). For the complete deployment process, see [Cloud Training Platform Model Deployment](../../example/ai/cloudplat_deploy.md).
```

## Common Description

<a id="common-constructor-params"></a>

### Common Constructor Parameters

Except for `OCRDetectionApp` and `OCRRecognitionApp`, the constructors of each class include the following parameters:

| Parameter Name | Description | Notes | Type |
|----------|------|------|------|
| mode | Inference mode | `'image'` means inferring a single image, `'video'` means inferring a real-time camera video stream. This parameter affects the drawing target of `draw_result` | str |
| kmodel_path | kmodel path | The path of the kmodel on the development board from the deployment package | str |
| labels | Category label list | From the deployment package configuration file | list[str] |
| model_input_size | Model input resolution | The input resolution specified during training, from the deployment package configuration file | list[int] |
| confidence_threshold | Confidence threshold | Results below this value are discarded | float [0~1] |
| rgb888p_size | Inference frame resolution | The image resolution fed into AI | list[int] |
| display_size | Display resolution | Set when `mode='video'`. It is recommended to pass the return value of `PipeLine.get_display_size()` | list[int] |
| debug_mode | Debug mode | 0 means no timing, 1 means timing | int [0/1] |

### Common Methods

| Method | Description |
|------|------|
| `config_preprocess(input_image_size=None)` | Configure AI2D preprocessing. When `input_image_size` is `None`, the `rgb888p_size` from construction is used |
| `run(input_np)` | Inherited from `AIBase`, completes the full "preprocessing → inference → post-processing" flow, and returns the post-processing result |
| `postprocess(results)` | Post-processing, the return value is a dict with different fields for each class, see below for details |
| `draw_result(draw_img, res)` | Draw the result onto `draw_img`. When `mode='video'`, pass `pl.osd_img`; when `mode='image'`, pass the original image returned by `read_image()` |
| `get_cur_result()` | Get the result of the most recent `postprocess`. The content is the same as the return value of `postprocess`. Suitable for fetching results in places other than drawing (such as reporting, linked control) |
| `deinit()` | Release native resources such as kmodel and AI2D. Must be called before exit |

## API Introduction

### ClassificationApp

**Description**

Image classification task. Classifies the entire image and outputs the category with the highest probability.

**Syntax**

```python
from libs.PlatTasks import ClassificationApp

app = ClassificationApp(mode="video", kmodel_path="best.kmodel", labels=labels,
                        model_input_size=[224,224], confidence_threshold=0.7,
                        rgb888p_size=[224,224], display_size=display_size, debug_mode=0)
```

**Parameters**

See [Common Constructor Parameters](#common-constructor-params), where `confidence_threshold` defaults to 0.7 and `model_input_size` defaults to `[224,224]`.

**Return Values**

The constructor returns a `ClassificationApp` instance. `postprocess` returns a dict:

| Key | Type | Description |
|----|------|------|
| label | str | The category name of the classification result |
| score | float | The corresponding score |

```{admonition} Hint
:class: note
This class automatically switches its computation method based on the length of `labels`:

- **Number of classes > 2**: Applies softmax to the model output and takes the maximum. Only when the score **exceeds** `confidence_threshold` is a result returned; otherwise `label` is an empty string and `score` is `0.0`.
- **Number of classes = 2**: Treated as binary classification. Applies sigmoid to the model output. When the score exceeds the threshold, returns `labels[1]` along with that score; otherwise returns `labels[0]` along with `1 - score`. Therefore, in binary classification, a non-empty `label` is **always** returned.
```

### DetectionApp

**Description**

Object detection task. The platform generates models with three different detection heads based on the training configuration. This class automatically selects the corresponding `aicube` post-processing interface through `model_type`.

**Syntax**

```python
from libs.PlatTasks import DetectionApp

app = DetectionApp(mode="video", kmodel_path="best.kmodel", labels=labels,
                   model_input_size=[640,640], anchors=anchors,
                   model_type="AnchorBaseDet", confidence_threshold=0.5,
                   nms_threshold=0.25, rgb888p_size=[1280,720],
                   display_size=display_size, debug_mode=0)
```

**Parameters**

In addition to [Common Constructor Parameters](#common-constructor-params), it also includes:

| Parameter Name | Description | Notes | Type |
|----------|------|------|------|
| anchors | Anchor box size list | When `model_type='AnchorBaseDet'`, **must contain 18 values**, otherwise an exception is raised. Taken from the deployment package configuration file | list |
| model_type | Detection head type | Optional values are `'AnchorBaseDet'`, `'AnchorFreeDet'`, `'GFLDet'`, taken from the deployment package configuration file; do not change arbitrarily | str |
| nms_threshold | NMS threshold | Non-maximum suppression threshold, defaults to 0.25 | float [0~1] |

**Return Values**

The constructor returns a `DetectionApp` instance. `postprocess` returns a dict:

| Key | Type | Description |
|----|------|------|
| boxes | ndarray | List of detection boxes, each box is `[x1, y1, x2, y2]`, coordinates based on `rgb888p_size` |
| scores | ndarray | Confidence corresponding to each box |
| idx | ndarray | Class index corresponding to each box, can be used to index `labels` |

### SegmentationApp

**Description**

Semantic segmentation task. Outputs a mask image with the same resolution as `display_size`, which can be directly overlaid on the OSD layer for display.

**Syntax**

```python
from libs.PlatTasks import SegmentationApp

app = SegmentationApp(mode="video", kmodel_path="best.kmodel", labels=labels,
                      model_input_size=[320,320], rgb888p_size=[320,320],
                      display_size=display_size, debug_mode=0)
```

**Parameters**

All are [Common Constructor Parameters](#common-constructor-params), where `model_input_size` defaults to `[320,320]`. This class does not use `confidence_threshold`.

**Return Values**

The constructor returns a `SegmentationApp` instance. `postprocess` returns a dict:

| Key | Type | Description |
|----|------|------|
| mask | image.Image | Mask image with the same resolution as `display_size`. When `mode='video'`, it is in ARGB8888 format and can be directly overlaid on OSD; when `mode='image'`, it is in RGB888 format |

```{admonition} Note
:class: warning
The `input_np` parameter of `postprocess` is retained only for interface compatibility and is not actually used. The method internally reads the output from the previous inference step.
```

### OCRDetectionApp

**Description**

OCR detection task. Finds text regions in the image, returns quadrilateral box coordinates, and simultaneously crops out each text region, which can be directly sent to `OCRRecognitionApp` for recognition.

**Syntax**

```python
from libs.PlatTasks import OCRDetectionApp

app = OCRDetectionApp(mode="video", kmodel_path="ocr_det.kmodel",
                      model_input_size=[640,640], mask_threshold=0.5,
                      box_threshold=0.5, rgb888p_size=[1280,720],
                      display_size=display_size, debug_mode=0)
```

**Parameters**

Does not include `labels` and `confidence_threshold`; the rest are the same as [Common Constructor Parameters](#common-constructor-params), with additional:

| Parameter Name | Description | Notes | Type |
|----------|------|------|------|
| mask_threshold | Text region binarization threshold | Threshold for probability map binarization, defaults to 0.5 | float [0~1] |
| box_threshold | Text box confidence threshold | Text boxes with confidence lower than this value are discarded, defaults to 0.5 | float [0~1] |

**Return Values**

The constructor returns an `OCRDetectionApp` instance. `postprocess` returns a dict:

| Key | Type | Description |
|----|------|------|
| boxes | list | Each element contains 8 coordinate values `[p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y]`, which are the top-left, top-right, bottom-right, and bottom-left corners of the text box in sequence, coordinates based on `rgb888p_size` |
| crop_images | list | Cropped images (HWC layout arrays) corresponding one-to-one with `boxes`, can be directly fed into `OCRRecognitionApp` |

### OCRRecognitionApp

**Description**

OCR recognition task. Recognizes the text content in a single elongated text image, using CTC greedy decoding.

```{admonition} Note
:class: warning
The platform's OCR recognition model takes an **elongated text image** as input for a single inference. The full camera frame cannot be fed directly to it. The text regions must first be detected and cropped using `OCRDetectionApp`, and then sent in one by one for recognition.

This is unrelated to the constructor parameter `mode`: `mode` only affects the drawing target of `draw_result`/`print_result`. In the "detection + recognition" video stream application (corresponding to the example `deploy_ocr_video.py`), this class also uses `mode="video"`, and the input is still the text strips cut out by `OCRDetectionApp`. For single-image scenarios (`deploy_ocrrec_image.py`), `mode="image"` is used.
```

**Syntax**

```python
from libs.PlatTasks import OCRRecognitionApp

app = OCRRecognitionApp(mode="video", kmodel_path="ocr_rec.kmodel",
                        model_input_size=[512,32], ocr_dict=ocr_dict,
                        rgb888p_size=[1280,720], display_size=display_size, debug_mode=0)
```

**Parameters**

Does not include `labels` and `confidence_threshold`; the rest are the same as [Common Constructor Parameters](#common-constructor-params), with additional:

| Parameter Name | Description | Notes | Type |
|----------|------|------|------|
| ocr_dict | Character dictionary | From the dictionary file in the deployment package, **the last element is treated as the CTC blank symbol** | list[str] |

**Return Values**

The constructor returns an `OCRRecognitionApp` instance. `postprocess` returns a dict:

| Key | Type | Description |
|----|------|------|
| text | str | Recognized text content |

**Proprietary Methods**

| Method | Description |
|------|------|
| `print_result(osd_img, res)` | Prints the recognized text. When `mode='video'`, also clears the OSD |
| `draw_result(osd_img, det_boxes, ocr_texts)` | Has a different signature from other classes; requires both detection boxes and recognized text to be passed in, used to draw detection + recognition results together |

### MetricLearningApp

**Description**

Metric learning task, also known as self-learning. The model maps images into feature vectors, and classification is performed by computing cosine similarity with vectors in the feature database. **New categories can be added without retraining the model**; just add new reference images to the feature database.

**Syntax**

```python
from libs.PlatTasks import MetricLearningApp

app = MetricLearningApp(mode="video", kmodel_path="best.kmodel",
                        model_input_size=[224,224], confidence_threshold=0.5,
                        rgb888p_size=[224,224], display_size=display_size, debug_mode=0)
# Register reference images to build the feature database
app.load_image("/sdcard/examples/utils/db_img/apple.jpg", "apple")
app.load_image("/sdcard/examples/utils/db_img/banana.jpg", "banana")
```

**Proprietary Methods**

| Method | Description |
|------|------|
| `load_image(image_path, label)` | Extracts features from the image and stores them in the feature database with `label` as the tag. The preprocessing configuration is temporarily switched internally and automatically restored after the call, so it can be invoked at any time |
| `compute_similar(embedding)` | Searches the feature database for the vector with the highest cosine similarity to `embedding`, returns `(index, similarity)`. Returns `(-1, 0.0)` when the feature database is empty or no valid match exists |

**Parameters**

Does not include `labels` (categories come from the feature database); the rest are [Common Constructor Parameters](#common-constructor-params), where `confidence_threshold` is the cosine similarity threshold, defaulting to 0.5.

**Return Values**

The constructor returns a `MetricLearningApp` instance. `postprocess` returns a dict:

| Key | Type | Description |
|----|------|------|
| label | str | The matched label. Empty string when the feature database is empty, no match is found, or similarity is below the threshold |
| score | float | Cosine similarity |

```{admonition} Note
:class: warning
The feature database is stored in memory and **is not persisted**. It will be lost after power-off or `deinit()`. There is no upper limit on the number of entries in the database; registering too many will occupy a large amount of memory and needs to be controlled manually.
```

### MultiLabelClassificationApp

**Description**

Multi-label classification task. An image may belong to multiple categories at the same time (e.g., "sky" and "sea"). Binary classification is performed independently for each category, and all categories whose scores exceed the threshold are output.

**Syntax**

```python
from libs.PlatTasks import MultiLabelClassificationApp

app = MultiLabelClassificationApp(mode="video", kmodel_path="best.kmodel", labels=labels,
                                  model_input_size=[224,224], confidence_threshold=0.5,
                                  rgb888p_size=[224,224], display_size=display_size, debug_mode=0)
```

**Parameters**

All are [Common Constructor Parameters](#common-constructor-params), where `confidence_threshold` is the threshold for independent binary classification of each category, defaulting to 0.5.

**Return Values**

The constructor returns a `MultiLabelClassificationApp` instance. `postprocess` returns a dict:

| Key | Type | Description |
|----|------|------|
| labels | list[str] | Category names whose sigmoid scores exceed `confidence_threshold` |
| scores | list[float] | Scores corresponding one-to-one with `labels` |

## Example Program

Below is a general framework for video stream inference, using image classification as an example:

```python
from libs.PipeLine import PipeLine
from libs.PlatTasks import ClassificationApp
from libs.Utils import *
import os, ujson, gc

if __name__ == "__main__":
    # Read parameters from the deployment package configuration file
    deploy_conf = read_json("/sdcard/mp_deployment_source/deploy_config.json")
    kmodel_path = "/sdcard/mp_deployment_source/best.kmodel"
    labels = deploy_conf["categories"]
    model_input_size = [deploy_conf["img_size"][0], deploy_conf["img_size"][1]]

    rgb888p_size = [224, 224]
    pl = None
    app = None
    try:
        pl = PipeLine(rgb888p_size=rgb888p_size, display_mode="auto")
        pl.create()
        display_size = pl.get_display_size()

        app = ClassificationApp(mode="video", kmodel_path=kmodel_path, labels=labels,
                                model_input_size=model_input_size,
                                confidence_threshold=0.7, rgb888p_size=rgb888p_size,
                                display_size=display_size, debug_mode=0)
        app.config_preprocess()

        while True:
            img = pl.get_frame()
            res = app.run(img)
            app.draw_result(pl.osd_img, res)
            pl.show_image()
            gc.collect()
    finally:
        if app is not None:
            app.deinit()
        if pl is not None:
            pl.destroy()
        gc.collect()
```
