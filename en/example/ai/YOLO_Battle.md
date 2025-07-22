# YOLO Battle

## YOLOv5 Fruit Classification

### Building YOLOv5 Source Code and Training Environment

For building the YOLOv5 training environment, please refer to [ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5).

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

If you have already set up the environment, you can skip this step.

### Preparing Training Data

Please download the provided sample dataset. The sample dataset contains classification, detection and segmentation datasets provided for the scenes using three types of fruits (apple, banana, orange). Unzip the dataset to `yolov5` in the directory, please use `fruits_cls` as a data set for fruit classification tasks. The sample dataset also contains a desktop signature scene dataset for rotation object detection `yolo_pen_obb`, the task is in k230 `YOLOv5` not supported in the module.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) after completing the annotation, the classification task data does not require tool annotation, and only the directory can be divided according to the format. Convert the annotated data to `yolov5` the officially supported training data format is carried out for subsequent training.

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### Training a Fruit Classification Model with YOLOv5

Execute the command in the `yolov5` directory to train a three - class fruit classification model using `yolov5`:

```shell
python classify/train.py --model yolov5n-cls.pt --data datasets/fruits_cls --epochs 100 --batch-size 8 --imgsz 224 --device '0'
```

### Converting the Fruit Classification kmodel

For model conversion, the following libraries need to be installed in the training environment:

```Shell
# Linux platform: nncase and nncase - kpu can be installed online, and dotnet - 7 needs to be installed for nncase - 2.x
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# Windows platform: Please install dotnet - 7 and add it to the environment variables. nncase can be installed online using pip, but the nncase - kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase - kpu, the following libraries are also used in the script:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool, unzip the model conversion script tool `test_yolov5.zip` to the `yolov5` directory;

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

According to the following commands, first export the `pt` model under `runs/train-cls/exp/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the path of the pt model by yourself
python export.py --weight runs/train-cls/exp/weights/best.pt --imgsz 224 --batch 1 --include onnx
cd test_yolov5/classify
# Convert kmodel, please select the path of the onnx model by yourself. The generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/train-cls/exp/weights/best.onnx --dataset../test --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### YOLOv5 Module

The `YOLOv5` class integrates three tasks of `YOLOv5`, including classification, detection, and segmentation; it supports two inference modes, including image and video stream; this class encapsulates the kmodel inference process of `YOLOv5`.

- **Import Method**

```python
from libs.YOLO import YOLOv5
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports three types of tasks, optional values are 'classify' / 'detect' /'segment'; | str |
| mode | Inference mode | Supports two inference modes, optional values are 'image' / 'video', 'image' means inferring images, and 'video' means inferring real - time video streams captured by the camera; | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board; | str |
| labels | List of class labels | Label names of different classes; | list[str] |
| rgb888p_size | Inference frame resolution | Resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640]; | list[int] |
| model_input_size | Model input resolution | Input resolution of the YOLOv5 model during training, such as [224,224], [320,320], [640,640]; | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int] |
| conf_thresh | Confidence threshold | Class confidence threshold for classification tasks, and object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh | NMS threshold | Non - maximum suppression threshold, required for detection and segmentation tasks; | float【0~1】 |
| mask_thresh | Mask threshold | Binarization threshold for segmenting objects in the detection box in segmentation tasks; | float【0~1】 |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of image; | int |
| debug_mode | Debug mode | Whether the timing function is effective, optional values are 0/1, 0 means no timing, 1 means timing; | int【0/1】 |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test images, model path, label names, and model input size.
    img_path = "/data/test_apple.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [224, 224]

    confidence_threshold = 0.5
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLOv5 instance
    yolo = YOLOv5(task_type="classify", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [224, 224]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd"
    rgb888p_size = [640, 360]
    confidence_threshold = 0.5
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLOv5 instance
    yolo = YOLOv5(task_type="classify", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, debug_mode=0)
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

## YOLOv5 Fruit Detection

### Building YOLOv5 Source Code and Training Environment

For building the YOLOv5 training environment, please refer to [ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5).

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

If you have already set up the environment, you can skip this step.

### Preparing Training Data

Please download the provided sample dataset. The sample dataset contains classification, detection and segmentation datasets provided for the scenes using three types of fruits (apple, banana, orange). Unzip the dataset to `yolov5` in the directory, please use `fruits_yolo` as a data set for fruit detection tasks. The sample dataset also contains a desktop signature scene dataset for rotation object detection `yolo_pen_obb`, the task is in k230 `YOLOv5` not supported in the module.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) complete the annotation. Convert the marked data to `yolov5` the officially supported training data format is carried out for subsequent training.

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### Training a Fruit Detection Model with YOLOv5

Execute the command in the `yolov5` directory to train a three - class fruit detection model using `yolov5`:

```shell
python train.py --weight yolov5n.pt --cfg models/yolov5n.yaml --data datasets/fruits_yolo.yaml --epochs 300 --batch-size 8 --imgsz 320 --device '0'
```

### Converting the Fruit Detection kmodel

For model conversion, the following libraries need to be installed in the training environment:

```Shell
# Linux platform: nncase and nncase - kpu can be installed online, and dotnet - 7 needs to be installed for nncase - 2.x
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# Windows platform: Please install dotnet - 7 and add it to the environment variables. nncase can be installed online using pip, but the nncase - kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase - kpu, the following libraries are also used in the script:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool, and unzip the model conversion script tool `test_yolov5.zip` to the `yolov5` directory;

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

According to the following commands, first export the `pt` model under `runs/train/exp/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the path of the pt model by yourself
python export.py --weight runs/train/exp/weights/best.pt --imgsz 320 --batch 1 --include onnx
cd test_yolov5/detect
# Convert kmodel, please customize the path of the onnx model. The generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/train/exp/weights/best.onnx --dataset../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### YOLOv5 Module

The `YOLOv5` class integrates three tasks of `YOLOv5`, including classification, detection, and segmentation; it supports two inference modes, including image and video stream; this class encapsulates the kmodel inference process of `YOLOv5`.

- **Import Method**

```python
from libs.YOLO import YOLOv5
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports three types of tasks, optional values are 'classify' / 'detect' /'segment'; | str |
| mode | Inference mode | Supports two inference modes, optional values are 'image' / 'video', 'image' means inferring images, and 'video' means inferring real - time video streams captured by the camera; | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board; | str |
| labels | List of class labels | Label names of different classes; | list[str] |
| rgb888p_size | Inference frame resolution | Resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640]; | list[int] |
| model_input_size | Model input resolution | Input resolution of the YOLOv5 model during training, such as [224,224], [320,320], [640,640]; | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int] |
| conf_thresh | Confidence threshold | Class confidence threshold for classification tasks, and object confidence threshold for detection and segmentation tasks, such as 0.5; | float [0 - 1] |
| nms_thresh | NMS threshold | Non - maximum suppression threshold, required for detection and segmentation tasks; | float [0 - 1] |
| mask_thresh | Mask threshold | Binarization threshold for segmenting objects in the detection box in segmentation tasks; | float [0 - 1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of image; | int |
| debug_mode | Debug mode | Whether the timing function is effective, optional values are 0/1, 0 means no timing, 1 means timing; | int [0/1] |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
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

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel"
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

## YOLOv5 Fruit Segmentation

### Setting up the YOLOv5 Source Code and Training Environment

For setting up the YOLOv5 training environment, please refer to [ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5).

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

If you have already set up the environment, you can skip this step.

### Preparing the Training Data

Please download the provided sample dataset. The sample dataset contains classification, detection and segmentation datasets provided for the scenes using three types of fruits (apple, banana, orange). Unzip the dataset to `yolov5` in the directory, please use `fruits_seg` as a dataset for the fruit segmentation task. The sample dataset also contains a desktop signature scene dataset for rotation object detection `yolo_pen_obb`, the task is in k230 `YOLOv5` not supported in the module.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) complete the annotation. Convert the marked data to `yolov5` the officially supported training data format is carried out for subsequent training.

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### Training a Fruit Segmentation Model with YOLOv5

Execute the command in the `yolov5` directory to train a three - class fruit segmentation model using `yolov5`:

```shell
python segment/train.py --weight yolov5n-seg.pt --cfg models/segment/yolov5n-seg.yaml --data datasets/fruits_seg.yaml --epochs 100 --batch-size 8 --imgsz 320 --device '0'
```

### Converting the Fruit Segmentation kmodel

For model conversion, the following libraries need to be installed in the training environment:

```Shell
# Linux platform: nncase and nncase - kpu can be installed online, and dotnet - 7 needs to be installed for nncase - 2.x
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# Windows platform: Please install dotnet - 7 and add it to the environment variables. nncase can be installed online using pip, but the nncase - kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# Besides nncase and nncase - kpu, the other libraries used in the script include:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool and unzip the model conversion script tool `test_yolov5.zip` into the `yolov5` directory.

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

Follow the following commands to first export the model under `runs/train-seg/exp/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
python export.py --weight runs/train-seg/exp/weights/best.pt --imgsz 320 --batch 1 --include onnx
cd test_yolov5/segment
# Convert kmodel. Please customize the path of the onnx model. The generated kmodel is in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/train-seg/exp/weights/best.onnx --dataset../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying the Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### The YOLOv5 Module

The `YOLOv5` class integrates three tasks of `YOLOv5`, including classification (classify), detection (detect), and segmentation (segment); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the kmodel inference process of `YOLOv5`.

- **Import Method**

```python
from libs.YOLO import YOLOv5
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports three types of tasks, with optional values 'classify' / 'detect' /'segment'; | str |
| mode | Inference mode | Supports two inference modes, with optional values 'image' / 'video'. 'image' means inferring images, and 'video' means inferring real - time video streams captured by the camera; | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board; | str |
| labels | List of class labels | Label names of different classes; | list[str] |
| rgb888p_size | Inference frame resolution | Resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640]; | list[int] |
| model_input_size | Model input resolution | Input resolution of the YOLOv5 model during training, such as [224,224], [320,320], [640,640]; | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supporting hdmi([1920,1080]) and lcd([800,480]); | list[int] |
| conf_thresh | Confidence threshold | Class confidence threshold for classification tasks, and object confidence threshold for detection and segmentation tasks, such as 0.5; | float [0 - 1] |
| nms_thresh | NMS threshold | Non - maximum suppression threshold, required for detection and segmentation tasks; | float [0 - 1] |
| mask_thresh | Mask threshold | Binarization threshold for segmenting objects in the detection box in segmentation tasks; | float [0 - 1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of an image; | int |
| debug_mode | Debug mode | Whether the timing function is effective, with optional values 0/1. 0 means no timing, and 1 means timing; | int [0 - 1] |

#### Deploying the Model for Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLOv5 instance
    yolo = YOLOv5(task_type="segment", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd"
    rgb888p_size = [320, 320]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLOv5 instance
    yolo = YOLOv5(task_type="segment", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
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

## YOLOv8 Fruit Classification

### Setting up YOLOv8 Source Code and Training Environment

For setting up the YOLOv8 training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### Preparing Training Data

You can create a new folder first `yolov8`, please download the provided sample dataset. The sample dataset contains classification, detection and segmentation datasets provided for the scenes using three types of fruits (apple, banana, orange). Unzip the dataset to `yolov8` in the directory, please use `fruits_cls` as a data set for fruit classification tasks. The sample dataset also contains a desktop signature scene dataset for rotation object detection `yolo_pen_obb`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) after completing the annotation, the classification task data does not require tool annotation, and only the directory can be divided according to the format. Convert the annotated data to `yolov8` the officially supported training data format is carried out for subsequent training.

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### Training a Fruit Classification Model with YOLOv8

Execute the command in the `yolov8` directory to train a three - class fruit classification model using `yolov8`:

```shell
yolo classify train data=datasets/fruits_cls model=yolov8n-cls.pt epochs=100 imgsz=224
```

### Converting the Fruit Classification kmodel

For model conversion, the following libraries need to be installed in the training environment:

```Shell
# Linux platform: nncase and nncase - kpu can be installed online, and dotnet - 7 needs to be installed for nncase - 2.x
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# Windows platform: Please install dotnet - 7 and add it to the environment variables. nncase can be installed online using pip, but the nncase - kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# Besides nncase and nncase - kpu, the other libraries used in the script include:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool and unzip the model - conversion script tool `test_yolov8.zip` into the `yolov8` directory.

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

Follow the following commands to first export the `pt` model under `runs/classify/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the path of the pt model by yourself
yolo export model=runs/classify/train/weights/best.pt format=onnx imgsz=224
cd test_yolov8/classify
# Convert kmodel, please select the path of the onnx model by yourself. The generated kmodel is in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/classify/train/weights/best.onnx --dataset../test --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### YOLOv8 Module

The `YOLOv8` class integrates four tasks of `YOLOv8`, including classification (classify), detection (detect), segmentation (segment) and obb; it supports two inference modes, including image (image) and video stream (video); this class encapsulates the kmodel inference process of `YOLOv8`.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports four types of tasks, with optional values 'classify' / 'detect' /'segment'/'obb'; | str |
| mode | Inference mode | Supports two inference modes, with optional values 'image' / 'video'. 'image' means inferring images, and 'video' means inferring real - time video streams captured by the camera; | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board; | str |
| labels | List of class labels | Label names of different classes; | list[str] |
| rgb888p_size | Inference frame resolution | Resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640]; | list[int] |
| model_input_size | Model input resolution | Input resolution of the YOLOv8 model during training, such as [224,224], [320,320], [640,640]; | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supporting hdmi([1920,1080]) and lcd([800,480]); | list[int] |
| conf_thresh | Confidence threshold | Class confidence threshold for classification tasks, and object confidence threshold for detection and segmentation tasks, such as 0.5; | float [0 - 1] |
| nms_thresh | NMS threshold | Non - maximum suppression threshold, required for detection and segmentation tasks; | float [0 - 1] |
| mask_thresh | Mask threshold | Binarization threshold for segmenting objects in the detection box in segmentation tasks; | float [0 - 1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of an image; | int |
| debug_mode | Debug mode | Whether the timing function is effective, with optional values 0/1. 0 means no timing, and 1 means timing; | int [0 - 1] |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test_apple.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [224, 224]

    confidence_threshold = 0.5
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLOv8 instance
    yolo = YOLOv8(task_type="classify", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [224, 224]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd"
    rgb888p_size = [640, 360]
    confidence_threshold = 0.8
    # Initialize PipeLine
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLOv8 instance
    yolo = YOLOv8(task_type="classify", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, debug_mode=0)
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

## YOLOv8 Fruit Detection

### Setting up YOLOv8 Source Code and Training Environment

For setting up the YOLOv8 training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### Preparing Training Data

You can create a new folder first `yolov8`, please download the provided sample dataset. The sample dataset contains classification, detection and segmentation datasets provided for the scenes using three types of fruits (apple, banana, orange). Unzip the dataset to `yolov8` in the directory, please use `fruits_yolo` as a data set for fruit detection tasks. The sample dataset also contains a desktop signature scene dataset for rotation object detection `yolo_pen_obb`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) complete the annotation. Convert the marked data to `yolov8` the officially supported training data format is carried out for subsequent training.

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### Training a Fruit Detection Model with YOLOv8

Execute the command in the `yolov8` directory to train a three - class fruit detection model using `yolov8`:

```shell
yolo detect train data=datasets/fruits_yolo.yaml model=yolov8n.pt epochs=300 imgsz=320
```

### Converting the Fruit Detection kmodel

For model conversion, the following libraries need to be installed in the training environment:

```Shell
# Linux platform: nncase and nncase - kpu can be installed online, and dotnet - 7 needs to be installed for nncase - 2.x
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# Windows platform: Please install dotnet - 7 and add it to the environment variables. nncase can be installed online using pip, but the nncase - kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# Besides nncase and nncase - kpu, the other libraries used in the script include:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool and unzip the model - conversion script tool `test_yolov8.zip` into the `yolov8` directory.

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

Follow the following commands to first export the `pt` model under `runs/detect/exp/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the path of the pt model by yourself
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/detect
# Convert kmodel, please select the path of the onnx model by yourself. The generated kmodel is in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### YOLOv8 Module

The `YOLOv8` class integrates four tasks of `YOLOv8`, namely classification (classify), detection (detect), segmentation (segment) and obb. It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of `YOLOv8`.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports four types of tasks, with optional values 'classify'/ 'detect'/'segment'/'obb'; | str |
| mode | Inference mode | Supports two inference modes, with optional values 'image' or 'video'. 'Image' means inferring images, and 'video' means inferring real - time video streams captured by the camera; | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board; | str |
| labels | List of class labels | Label names of different classes; | list[str] |
| rgb888p_size | Inference frame resolution | Resolution of the current inference frame, such as [1920, 1080], [1280, 720], or [640, 640]; | list[int] |
| model_input_size | Model input resolution | Input resolution of the YOLOv8 model during training, such as [224, 224], [320, 320], or [640, 640]; | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supporting hdmi([1920, 1080]) and lcd([800, 480]); | list[int] |
| conf_thresh | Confidence threshold | Class confidence threshold for classification tasks, and object confidence threshold for detection and segmentation tasks, such as 0.5; | float [0 - 1] |
| nms_thresh | NMS threshold | Non - maximum suppression threshold, required for detection and segmentation tasks; | float [0 - 1] |
| mask_thresh | Mask threshold | Binarization threshold for segmenting objects in the detection box in segmentation tasks; | float [0 - 1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of an image; | int |
| debug_mode | Debug mode | Whether the timing function is effective, with optional values 0 or 1. 0 means no timing, and 1 means timing; | int [0 - 1] |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
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

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv8
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel"
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

## YOLOv8 Fruit Segmentation

### Setting up YOLOv8 Source Code and Training Environment

For setting up the training environment of YOLOv8, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### Preparing Training Data

You can create a new folder first `yolov8`, please download the provided sample dataset. The sample dataset contains classification, detection and segmentation datasets provided for the scenes using three types of fruits (apple, banana, orange). Unzip the dataset to `yolov8` in the directory, please use `fruits_seg` as a dataset for the fruit segmentation task. The sample dataset also contains a desktop signature scene dataset for rotation object detection `yolo_pen_obb`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) complete the annotation. Convert the marked data to `yolov8` the officially supported training data format is carried out for subsequent training.

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### Training a Fruit Segmentation Model with YOLOv8

Execute the command in the `yolov8` directory to train a three - class fruit segmentation model using `yolov8`:

```shell
yolo segment train data=datasets/fruits_seg.yaml model=yolov8n-seg.pt epochs=100 imgsz=320
```

### Converting the Fruit Segmentation kmodel

For model conversion, the following libraries need to be installed in the training environment:

```Shell
# Linux platform: nncase and nncase - kpu can be installed online, and dotnet - 7 needs to be installed for nncase - 2.x
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# Windows platform: Please install dotnet - 7 and add it to the environment variables. nncase can be installed online using pip, but the nncase - kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# Besides nncase and nncase - kpu, the other libraries used in the script include:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool and unzip the model - conversion script tool `test_yolov8.zip` into the `yolov8` directory.

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

Follow the following commands to first export the `pt` model under `runs/segment/exp/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the path of the pt model by yourself
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/segment
# Convert kmodel, please select the path of the onnx model by yourself. The generated kmodel is in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### YOLOv8 Module

The `YOLOv8` class integrates four tasks of `YOLOv8`, namely classification (classify), detection (detect), segmentation (segment) and obb. It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of `YOLOv8`.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports four types of tasks, with optional values 'classify', 'detect', 'segment' or 'obb'; | str |
| mode | Inference mode | Supports two inference modes, with optional values 'image' or 'video'. 'Image' means inferring images, and 'video' means inferring real - time video streams captured by the camera; | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board; | str |
| labels | List of class labels | Label names of different classes; | list[str] |
| rgb888p_size | Inference frame resolution | Resolution of the current inference frame, such as [1920, 1080], [1280, 720], or [640, 640]; | list[int] |
| model_input_size | Model input resolution | Input resolution of the YOLOv8 model during training, such as [224, 224], [320, 320], or [640, 640]; | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supporting hdmi([1920, 1080]) and lcd([800, 480]); | list[int] |
| conf_thresh | Confidence threshold | Class confidence threshold for classification tasks, and object confidence threshold for detection and segmentation tasks, such as 0.5; | float [0 - 1] |
| nms_thresh | NMS threshold | Non - maximum suppression threshold, required for detection and segmentation tasks; | float [0 - 1] |
| mask_thresh | Mask threshold | Binarization threshold for segmenting objects in the detection box in segmentation tasks; | float [0 - 1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of an image; | int |
| debug_mode | Debug mode | Whether the timing function is effective, with optional values 0 or 1. 0 means no timing, and 1 means timing; | int [0 - 1] |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLOv8 instance
    yolo = YOLOv8(task_type="segment", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd"
    rgb888p_size = [320, 320]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLOv8 instance
    yolo = YOLOv8(task_type="segment", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
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

## YOLOv8 Rotation Object Detection

### Setting up YOLOv8 Source Code and Training Environment

 For setting up the training environment of YOLOv8, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### Training data preparation

You can create a new folder first `yolov8`, please download the provided sample dataset. The sample dataset contains datasets provided separately for the scenes using a rotation object detection category (pen). Unzip the dataset to `yolov8` in the directory, please use `yolo_pen_obb` as a data set for the rotation object detection task.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) complete the annotation. Convert the marked data to `yolov8` the officially supported training data format is carried out for subsequent training.

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have downloaded the data, please ignore this step.

### Training a Obb Model with YOLOv8

For model conversion, the following libraries need to be installed in the training environment:

```Shell
# Linux platform: nncase and nncase - kpu can be installed online, and dotnet - 7 needs to be installed for nncase - 2.x
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# Windows platform: Please install dotnet - 7 and add it to the environment variables. nncase can be installed online using pip, but the nncase - kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# Besides nncase and nncase - kpu, the other libraries used in the script include:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool and unzip the model - conversion script tool `test_yolov8.zip` into the `yolov8` directory.

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

Follow the following commands to first export the `pt` model under `runs/obb/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the path of the pt model by yourself
yolo export model=runs/obb/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/obb
# Convert kmodel, please select the path of the onnx model by yourself. The generated kmodel is in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/obb/train/weights/best.onnx --dataset ../test_obb --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying Model Files

Connect to the IDE and copy the converted model and test images to the path `CanMV/data` in the directory. This path can be customized, you only need to modify the corresponding path when writing the code.

#### YOLOv8 module

 The `YOLOv8` class integrates four tasks of `YOLOv8`, namely classification (classify), detection (detect), segmentation (segment) and obb. It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of `YOLOv8`.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports four types of tasks, with optional values 'classify', 'detect', 'segment' or 'obb'; | str |
| mode | Inference mode | Supports two inference modes, with optional values 'image' or 'video'. 'Image' means inferring images, and 'video' means inferring real - time video streams captured by the camera; | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board; | str |
| labels | List of class labels | Label names of different classes; | list[str] |
| rgb888p_size | Inference frame resolution | Resolution of the current inference frame, such as [1920, 1080], [1280, 720], or [640, 640]; | list[int] |
| model_input_size | Model input resolution | Input resolution of the YOLOv8 model during training, such as [224, 224], [320, 320], or [640, 640]; | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supporting hdmi([1920, 1080]) and lcd([800, 480]); | list[int] |
| conf_thresh | Confidence threshold | Class confidence threshold for classification tasks, and object confidence threshold for detection and segmentation tasks, such as 0.5; | float [0 - 1] |
| nms_thresh | NMS threshold | Non - maximum suppression threshold, required for detection and segmentation tasks; | float [0 - 1] |
| mask_thresh | Mask threshold | Binarization threshold for segmenting objects in the detection box in segmentation tasks; | float [0 - 1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of an image; | int |
| debug_mode | Debug mode | Whether the timing function is effective, with optional values 0 or 1. 0 means no timing, and 1 means timing; | int [0 - 1] |

#### Deploying the Model to Implement Image Inference

For picture reasoning, please refer to the following code.**Modify according to actual situation`__main__`Definition parameter variables in**;

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test_obb.jpg" 
    kmodel_path = "/data/best.kmodel" 
    labels = ['pen']
    model_input_size = [320, 320]

    confidence_threshold = 0.1
    nms_threshold = 0.6
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLOv8 instance
    yolo = YOLOv8(task_type="obb", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=100, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code.**Modify according to actual situation`__main__`Definition variables in**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best_yolov8n.kmodel" 
    labels = ['pen']
    model_input_size = [320, 320]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd" 
    rgb888p_size = [640, 360]
    confidence_threshold = 0.1
    nms_threshold = 0.6
    # Initialize PipeLine
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLOv8 instance
    yolo = YOLOv8(task_type="obb", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
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

## YOLO11 Fruit Classification

### Setting up YOLO11 Source Code and Training Environment

For setting up the training environment of YOLO11, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### Preparing Training Data

You can create a new folder first `yolo11`, please download the provided sample dataset. The sample dataset contains classification, detection and segmentation datasets provided for the scenes using three types of fruits (apple, banana, orange). Unzip the dataset to `yolo11` in the directory, please use `fruits_cls` as a data set for fruit classification tasks. The sample dataset also contains a desktop signature scene dataset for rotation object detection `yolo_pen_obb`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) after completing the annotation, the classification task data does not require tool annotation, and only the directory can be divided according to the format. Convert the annotated data to `yolo11` the officially supported training data format is carried out for subsequent training.

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### Training a Fruit Classification Model with YOLO11

Execute the command in the `yolo11` directory to train a three - class fruit classification model using `yolo11`:

```shell
yolo classify train data=datasets/fruits_cls model=yolo11n-cls.pt epochs=100 imgsz=224
```

### Converting the Fruit Classification kmodel

For model conversion, the following libraries need to be installed in the training environment:

```Shell
# Linux platform: nncase and nncase - kpu can be installed online, and dotnet - 7 needs to be installed for nncase - 2.x
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# Windows platform: Please install dotnet - 7 and add it to the environment variables. nncase can be installed online using pip, but the nncase - kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# Besides nncase and nncase - kpu, the other libraries used in the script include:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool and unzip the model - conversion script tool `test_yolo11.zip` into the `yolo11` directory.

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

Follow the following commands to first export the `pt` model under `runs/classify/exp/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the path of the pt model by yourself
yolo export model=runs/classify/train/weights/best.pt format=onnx imgsz=224
cd test_yolo11/classify
# Convert kmodel, please select the path of the onnx model by yourself. The generated kmodel is in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/classify/train/weights/best.onnx --dataset../test --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### YOLO11 Module

The `YOLO11` class integrates four tasks of `YOLO11`, namely classification (classify), detection (detect), segmentation (segment), obb. It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of `YOLO11`.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports four types of tasks, with optional values 'classify', 'detect', 'segment' or 'obb'; | str |
| mode | Inference mode | Supports two inference modes, with optional values 'image' or 'video'. 'Image' means inferring images, and 'video' means inferring real - time video streams captured by the camera; | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board; | str |
| labels | List of class labels | Label names of different classes; | list[str] |
| rgb888p_size | Inference frame resolution | Resolution of the current inference frame, such as [1920, 1080], [1280, 720], or [640, 640]; | list[int] |
| model_input_size | Model input resolution | Input resolution of the YOLO11 model during training, such as [224, 224], [320, 320], or [640, 640]; | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video', supporting hdmi([1920, 1080]) and lcd([800, 480]); | list[int] |
| conf_thresh | Confidence threshold | Class confidence threshold for classification tasks, and object confidence threshold for detection and segmentation tasks, such as 0.5; | float [0 - 1] |
| nms_thresh | NMS threshold | Non - maximum suppression threshold, required for detection and segmentation tasks; | float [0 - 1] |
| mask_thresh | Mask threshold | Binarization threshold for segmenting objects in the detection box in segmentation tasks; | float [0 - 1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of an image; | int |
| debug_mode | Debug mode | Whether the timing function is effective, with optional values 0 or 1. 0 means no timing, and 1 means timing; | int [0 - 1] |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test_apple.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [224, 224]

    confidence_threshold = 0.5
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLO11 instance
    yolo = YOLO11(task_type="classify", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [224, 224]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd"
    rgb888p_size = [640, 360]
    confidence_threshold = 0.8
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLO11 instance
    yolo = YOLO11(task_type="classify", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, debug_mode=0)
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

## YOLO11 Fruit Detection

### Setting up YOLO11 Source Code and Training Environment

For setting up the training environment of YOLO11, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### Preparing Training Data

You can create a new folder first `yolo11`, please download the provided sample dataset. The sample dataset contains classification, detection and segmentation datasets provided for the scenes using three types of fruits (apple, banana, orange). Unzip the dataset to `yolo11` in the directory, please use `fruits_yolo` as a data set for fruit detection tasks. The sample dataset also contains a desktop signature scene dataset for rotation object detection `yolo_pen_obb`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) complete the annotation. Convert the marked data to `yolo11` the officially supported training data format is carried out for subsequent training.

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### Training a Fruit Detection Model with YOLO11

Execute the command in the `yolo11` directory to train a three - class fruit detection model using `yolo11`:

```shell
yolo detect train data=datasets/fruits_yolo.yaml model=yolo11n.pt epochs=300 imgsz=320
```

### Converting the Fruit Detection kmodel

For model conversion, the following libraries need to be installed in the training environment:

```Shell
# On the Linux platform: nncase and nncase-kpu can be installed online. For nncase-2.x, dotnet-7 needs to be installed.
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# On the Windows platform: Please install dotnet-7 and add it to the environment variables. nncase can be installed online using pip, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install it in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl.
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used in the script include:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool and unzip the model conversion script tool `test_yolo11.zip` into the `yolo11` directory:

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

Follow the following commands to first export the `pt` model under `runs/detect/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export to onnx. Please select the path of the pt model by yourself.
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/detect
# Convert to kmodel. Please select the path of the onnx model by yourself. The generated kmodel will be in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying the Model Files

Connect to the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized; you just need to modify the corresponding path when writing the code.

#### The YOLO11 Module

The `YOLO11` class integrates four tasks of `YOLO11`, namely classification (`classify`), detection (`detect`), segmentation (`segment`), and obb. It supports two inference modes, namely image (`image`) and video stream (`video`). This class encapsulates the kmodel inference process of `YOLO11`.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name | Description | Explanation | Type |
| --- | --- | --- | --- |
| task_type | Task type | Supports four types of tasks. The available options are `classify`, `detect`, `segment` or `obb`. | str |
| mode | Inference mode | Supports two inference modes. The available options are `image` and `video`. `image` means inferring from images, and `video` means inferring from the real-time video stream captured by the camera. | str |
| kmodel_path | Path of the kmodel | The path of the kmodel copied to the development board. | str |
| labels | List of class labels | The label names of different classes. | list[str] |
| rgb888p_size | Resolution of the inference frame | The resolution of the current frame for inference, such as `[1920, 1080]`, `[1280, 720]`, or `[640, 640]`. | list[int] |
| model_input_size | Input resolution of the model | The input resolution of the YOLO11 model during training, such as `[224, 224]`, `[320, 320]`, or `[640, 640]`. | list[int] |
| display_size | Display resolution | Set when the inference mode is `video`. It supports HDMI (`[1920, 1080]`) and LCD (`[800, 480]`). | list[int] |
| conf_thresh | Confidence threshold | The class confidence threshold for classification tasks and the object confidence threshold for detection and segmentation tasks, e.g., 0.5. | float [0~1] |
| nms_thresh | NMS threshold | The non-maximum suppression threshold, which is required for detection and segmentation tasks. | float [0~1] |
| mask_thresh | Mask threshold | The binarization threshold for segmenting the objects within the detection boxes in segmentation tasks. | float [0~1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of the image. | int |
| debug_mode | Debug mode | Whether the timing function is enabled. The available options are 0 and 1. 0 means no timing, and 1 means timing is enabled. | int [0/1] |

#### Deploying the Model for Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
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

#### Deploying the Model for Video Inference

For video inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel"
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

## YOLO11 Fruit Segmentation

### Setting up the YOLO11 Source Code and Training Environment

To set up the YOLO11 training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Use pip to install the ultralytics package along with all its requirements in a Python environment where Python >= 3.8 and PyTorch >= 1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### Preparing the Training Data

You can create a new folder first `yolo11`, please download the provided sample dataset. The sample dataset contains classification, detection and segmentation datasets provided for the scenes using three types of fruits (apple, banana, orange). Unzip the dataset to `yolo11` in the directory, please use `fruits_seg` as a dataset for the fruit segmentation task. The sample dataset also contains a desktop signature scene dataset for rotation object detection `yolo_pen_obb`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) complete the annotation. Convert the marked data to `yolo11` the officially supported training data format is carried out for subsequent training.

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### Training a Fruit Segmentation Model with YOLO11

Execute the following command in the `yolo11` directory to train a three-class fruit segmentation model using YOLO11:

```shell
yolo segment train data=datasets/fruits_seg.yaml model=yolo11n-seg.pt epochs=100 imgsz=320
```

### Converting the Fruit Segmentation kmodel

The following libraries need to be installed in the training environment for model conversion:

```Shell
# On the Linux platform: nncase and nncase-kpu can be installed online. For nncase-2.x, dotnet-7 needs to be installed.
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# On the Windows platform: Please install dotnet-7 and add it to the environment variables. nncase can be installed online using pip, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install it in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl.
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used in the script include:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool and unzip the model conversion script tool `test_yolo11.zip` into the `yolo11` directory:

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

Follow the commands below to first export the `pt` model under `runs/segment/train/weights` to an `onnx` model and then convert it to a `kmodel` model:

```shell
# Export to onnx. Please select the path of the pt model by yourself.
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/segment
# Convert to kmodel. Please select the path of the onnx model by yourself. The generated kmodel will be in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying the Model Files

Connect to the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized; you just need to modify the corresponding path when writing the code.

#### YOLO11 Module

The `YOLO11` class integrates four tasks of YOLO11, namely classification (classify), detection (detect), segmentation (segment), and obb. It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of YOLO11.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name | Description | Explanation | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports four types of tasks. The available options are 'classify', 'detect', 'segment', and 'obb'. | str |
| mode | Inference mode | Supports two inference modes. The available options are 'image' and 'video'. 'Image' means inferring from images, and 'video' means inferring from the real-time video stream captured by the camera. | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board. | str |
| labels | List of class labels | The label names of different classes. | list[str] |
| rgb888p_size | Inference frame resolution | The resolution of the current inference frame, such as [1920, 1080], [1280, 720], or [640, 640]. | list[int] |
| model_input_size | Model input resolution | The input resolution of the YOLO11 model during training, such as [224, 224], [320, 320], or [640, 640]. | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video'. It supports HDMI ([1920, 1080]) and LCD ([800, 480]). | list[int] |
| conf_thresh | Confidence threshold | The class confidence threshold for classification tasks and the object confidence threshold for detection and segmentation tasks, such as 0.5. | float [0 - 1] |
| nms_thresh | NMS threshold | The non-maximum suppression threshold, which is required for detection and segmentation tasks. | float [0 - 1] |
| mask_thresh | Mask threshold | The binarization threshold for segmenting the objects in the detection box in segmentation tasks. | float [0 - 1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of the image. | int |
| debug_mode | Debug mode | Whether the timing function is enabled. The available options are 0 and 1. 0 means no timing, and 1 means timing is enabled. | int [0/1] |

#### Deploying the Model for Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLO11 instance
    yolo = YOLO11(task_type="segment", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    model_input_size = [320, 320]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd"
    rgb888p_size = [320, 320]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    # Initialize PipeLine
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLO11 instance
    yolo = YOLO11(task_type="segment", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
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

## YOLO11 Rotation Object Detection

### Setting up the YOLO11 Source Code and Training Environment

 To set up the YOLO11 training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Use pip to install the ultralytics package along with all its requirements in a Python environment where Python >= 3.8 and PyTorch >= 1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### Preparing the Training Data

You can create a new folder first `yolo11`, please download the provided sample dataset. The sample dataset contains a rotating object detection dataset provided by single-class rotating pen detection (pen) for the scenes. Unzip the dataset to `yolo11` in the directory, please use `yolo_pen_obb` as a data set for the rotation object detection task.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) complete the annotation. Convert the marked data to `yolo11` the officially supported training data format is carried out for subsequent training.

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have downloaded the data, please ignore this step.

### Training a Obb Model with YOLO11

The following libraries need to be installed in the training environment for model conversion:

```Shell
# On the Linux platform: nncase and nncase-kpu can be installed online. For nncase-2.x, dotnet-7 needs to be installed.
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# On the Windows platform: Please install dotnet-7 and add it to the environment variables. nncase can be installed online using pip, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases.
# Enter the corresponding Python environment and use pip to install it in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl.
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used in the script include:
pip install onnx
pip install onnxruntime
pip install onnxsim
```

Download the script tool and unzip the model conversion script tool `test_yolo11.zip` into the `yolo11` directory:

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

Follow the commands below to first export the `pt` model under `runs/obb/train/weights` to an `onnx` model and then convert it to a `kmodel` model:

```shell
# Export to onnx. Please select the path of the pt model by yourself.
yolo export model=runs/obb/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/obb
# Convert to kmodel. Please select the path of the onnx model by yourself. The generated kmodel will be in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/obb/train/weights/best.onnx --dataset ../test_obb --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Parameter description of model conversion script (to_kmodel.py)**:

| Parameter name | describe                       | illustrate                                                                                                      | type  |
| -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----- |
| target         | Target platform                | The optional option is k230/CPU, corresponding to k230 chip;                                                    | str   |
| model          | Model path                     | The path of the ONNX model to be converted;                                                                     | str   |
| dataset        | Calibration picture collection | Image data used during model conversion, used in the quantization stage                                         | str   |
| input_width    | Input width                    | Width of model input                                                                                            | int   |
| input_height   | Enter height                   | The height of the model input                                                                                   | int   |
| ptq_option     | Quantitative method            | The quantification method of data and weights is 0 as [uint8,uint8], 1 as [uint8,int16], and 2 as [int16,uint8] | 0/1/2 |

### Deploying the Model on K230 Using MicroPython

#### Burning the Image and Installing CanMV IDE

💡 **Firmware introduction**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link:[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), write code in the IDE and run it.

#### Copying the Model Files

Connect to the IDE and copy the converted model and test images to the path `CanMV/data` in the directory. This path can be customized, you only need to modify the corresponding path when writing the code.

#### YOLO11 module

The `YOLO11` class integrates four tasks of YOLO11, namely classification (classify), detection (detect), segmentation (segment), and obb. It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of YOLO11.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name | Description | Explanation | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports four types of tasks. The available options are 'classify', 'detect', 'segment', and 'obb'. | str |
| mode | Inference mode | Supports two inference modes. The available options are 'image' and 'video'. 'Image' means inferring from images, and 'video' means inferring from the real-time video stream captured by the camera. | str |
| kmodel_path | kmodel path | The path of the kmodel copied to the development board. | str |
| labels | List of class labels | The label names of different classes. | list[str] |
| rgb888p_size | Inference frame resolution | The resolution of the current inference frame, such as [1920, 1080], [1280, 720], or [640, 640]. | list[int] |
| model_input_size | Model input resolution | The input resolution of the YOLO11 model during training, such as [224, 224], [320, 320], or [640, 640]. | list[int] |
| display_size | Display resolution | Set when the inference mode is 'video'. It supports HDMI ([1920, 1080]) and LCD ([800, 480]). | list[int] |
| conf_thresh | Confidence threshold | The class confidence threshold for classification tasks and the object confidence threshold for detection and segmentation tasks, such as 0.5. | float [0 - 1] |
| nms_thresh | NMS threshold | The non-maximum suppression threshold, which is required for detection and segmentation tasks. | float [0 - 1] |
| mask_thresh | Mask threshold | The binarization threshold for segmenting the objects in the detection box in segmentation tasks. | float [0 - 1] |
| max_boxes_num | Maximum number of detection boxes | The maximum number of detection boxes allowed to be returned in one frame of the image. | int |
| debug_mode | Debug mode | Whether the timing function is enabled. The available options are 0 and 1. 0 means no timing, and 1 means timing is enabled. | int [0/1] |

#### Deploying the Model for Image Inference

For picture reasoning, please refer to the following code.**Modify according to actual situation`__main__`Definition parameter variables in**;

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own test image, model path, label names, and model input size.
    img_path = "/data/test_obb.jpg" 
    kmodel_path = "/data/best.kmodel" 
    labels = ['pen']
    model_input_size = [320, 320]

    confidence_threshold = 0.1
    nms_threshold = 0.6
    img, img_ori = read_image(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize YOLO11 instance
    yolo = YOLO11(task_type="obb", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=100, debug_mode=0)
    yolo.config_preprocess()
    res = yolo.run(img)
    yolo.draw_result(res, img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the following code.**Modify according to actual situation`__main__`Definition variables in**;

```python
from libs.PipeLine import PipeLine
from libs.Utils import *
from libs.YOLO import YOLO11
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # The following are examples only. Please modify them according to your own model path, label names, and model input size.
    kmodel_path = "/data/best.kmodel" 
    labels = ['pen']
    model_input_size = [320, 320]

    # Add display mode, default is hdmi, options are hdmi/lcd/lt9611/st7701/hx8399.
    # hdmi defaults to lt9611 with resolution 1920*1080; lcd defaults to st7701 with resolution 800*480.
    display_mode = "lcd" 
    rgb888p_size = [640, 360]
    confidence_threshold = 0.1
    nms_threshold = 0.6
    # Initialize PipeLine
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    pl.create()
    display_size = pl.get_display_size()
    # Initialize YOLO11 instance
    yolo = YOLO11(task_type="obb", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
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

## Verification of kmodel Conversion

The model conversion script toolkits (`test_yolov5/test_yolov8/test_yolo11`) downloaded for different models contain scripts for kmodel verification.

> Note: You need to add environment variables to execute the verification scripts.
>
> **Linux**:
>
> ```shell
> # The path in the following command is the path of the Python environment where nncase is installed. Please modify it according to your environment.
> export NNCASE_PLUGIN_PATH=$NNCASE_PLUGIN_PATH:/usr/local/lib/python3.9/5site-packages/
> export PATH=$PATH:/usr/local/lib/python3.9/site-packages/
> source /etc/profile
> ```
>
> **Windows**:
>
> Add the `Lib/site-packages` path under the `Python` environment where `nncase` is installed to the system variable `Path` of the environment variables.

### Comparing the Outputs of the onnx and kmodel

#### Generating the Input bin Files

Enter the `classify/detect/segment` directory and execute the following command:

```shell
python save_bin.py --image ../test_images/test.jpg --input_width 224 --input_height 224
```

After executing the script, the bin files `onnx_input_float32.bin` and `kmodel_input_uint8.bin` will be generated in the current directory, which will serve as the input files for the onnx model and the kmodel.

#### Comparing the Outputs

Copy the converted models `best.onnx` and `best.kmodel` to the `classify/detect/segment` directory, and then execute the verification script with the following command:

```shell
python simulate.py --model best.onnx --model_input onnx_input_float32.bin --kmodel best.kmodel --kmodel_input kmodel_input_uint8.bin --input_width 224 --input_height 224
```

You will get the following output:

```shell
output 0 cosine similarity : 0.9985673427581787
```

The script will compare the cosine similarity of the outputs one by one. If the similarity is above 0.99, the model is generally considered usable. Otherwise, you need to conduct actual inference tests or change the quantization parameters and re-export the kmodel. If the model has multiple outputs, there will be multiple lines of similarity comparison information. For example, for the segmentation task, which has two outputs, the similarity comparison information is as follows:

```shell
output 0 cosine similarity : 0.9999530911445618
output 1 cosine similarity : 0.9983288645744324
```

### Inference on Images Using the onnx Model

Enter the `classify/detect/segment` directory, open `test_cls_onnx.py`, modify the parameters in `main()` to adapt to your model, and then execute the command:

```shell
python test_cls_onnx.py
```

After the command is successfully executed, the result will be saved as `onnx_cls_results.jpg`.

> The detection and segmentation tasks are similar. Execute `test_det_onnx.py` and `test_seg_onnx.py` respectively.

### Inference on Images Using the kmodel

Enter the `classify/detect/segment` directory, open `test_cls_kmodel.py`, modify the parameters in `main()` to adapt to your model, and then execute the command:

```shell
python test_cls_kmodel.py
```

After the command is successfully executed, the result will be saved as `kmodel_cls_results.jpg`.

> The detection and segmentation tasks are similar. Execute `test_det_kmodel.py` and `test_seg_kmodel.py` respectively.

## Tuning Guide

When the performance of the model on the K230 is not satisfactory, you can generally consider tuning from aspects such as threshold settings, model size, input resolution, quantization methods, and the quality of training data.

### Adjusting Thresholds

Adjust the confidence threshold, nms threshold, and mask threshold to optimize the deployment effect without changing the model. In the detection task, increasing the confidence threshold and lowering the nms threshold will lead to a decrease in the number of detection boxes, and conversely, reducing the confidence threshold and increasing the nms threshold will lead to an increase in the number of detection boxes. In the segmentation task, the mask threshold will affect the partitioning of the segmentation area. You can first adjust according to the actual scenario to find the threshold value under the better effect.

### Changing the Model

Select models of different sizes to balance speed, memory footprint, and accuracy. The n/s/m/l model can be selected for training and transformation according to actual needs.

The following data takes the kmdel obtained by training in the example data set provided by this document as an example, and the operating performance of kmdel is measured on K230. During actual deployment, the post-processing time will be affected **Number of results** increased impact while memory management `gc.collect()` the time-consuming process will also increase with the complexity of post-processing, so the following data is only referenced for data comparison, you can **Business needs according to different scenarios** choose a different model:

| Model   | Input resolution | Task | kpu inference frame rate | Full frame inference frame rate |
| ------- | ---------------- | ---- | ------------------------ | ------------------------------- |
| yolov5n | 224×224          | cls  | 350fps                   | 57fps                           |
| yolov5s | 224×224          | cls  | 186fps                   | 56fps                           |
| yolov5m | 224×224          | cls  | 88fps                    | 47ps                            |
| yolov5l | 224×224          | cls  | 48fps                    | 31fps                           |
| yolov8n | 224×224          | cls  | 198fps                   | 57fps                           |
| yolov8s | 224×224          | cls  | 95fps                    | 48fps                           |
| yolov8m | 224×224          | cls  | 42fps                    | 28fps                           |
| yolov8l | 224×224          | cls  | 21fps                    | 16fps                           |
| yolo11n | 224×224          | cls  | 158fps                   | 56fps                           |
| yolo11s | 224×224          | cls  | 83fps                    | 43fps                           |
| yolo11m | 224 × 224        | cls  | 50fps                    | 31fps                           |
| yolo11l | 224 × 224        | cls  | 39fps                    | 26fps                           |
| ------- | ----------       | ---- | -----------              | ------------                    |
| yolov5n | 320 × 320        | det  | 54fps                    | 31fps                           |
| yolov5s | 320 × 320        | det  | 38fps                    | 24fps                           |
| yolov5m | 320 × 320        | det  | 25fps                    | 18fps                           |
| yolov5l | 320 × 320        | det  | 16FPS                    | 12fps                           |
| yolov8n | 320 × 320        | det  | 44fps                    | 27fps                           |
| yolov8s | 320 × 320        | det  | 25fps                    | 18fps                           |
| yolov8m | 320 × 320        | det  | 14FPS                    | 11fps                           |
| yolov8l | 320 × 320        | det  | 8fps                     | 7fps                            |
| yolo11n | 320 × 320        | det  | 41fps                    | 26fps                           |
| yolo11s | 320 × 320        | det  | 24fps                    | 17fps                           |
| yolo11m | 320 × 320        | det  | 14FPS                    | 11fps                           |
| yolo11l | 320 × 320        | det  | 12fps                    | 9fps                            |
| ------- | ----------       | ---- | -----------              | ------------                    |
| yolov5n | 320 × 320        | seg  | 18fps                    | 11fps                           |
| yolov5s | 320 × 320        | seg  | 15fps                    | 10fps                           |
| yolov5m | 320 × 320        | seg  | 12fps                    | 8fps                            |
| yolov5l | 320 × 320        | seg  | 9fps                     | 7fps                            |
| yolov8n | 320 × 320        | seg  | 39fps                    | 18fps                           |
| yolov8s | 320 × 320        | seg  | 22FPS                    | 11fps                           |
| yolov8m | 320 × 320        | seg  | 12fps                    | 8fps                            |
| yolov8l | 320 × 320        | seg  | 7fps                     | 5fps                            |
| yolo11n | 320 × 320        | seg  | 37fps                    | 17fps                           |
| yolo11s | 320 × 320        | seg  | 21FPS                    | 11fps                           |
| yolo11m | 320 × 320        | seg  | 12fps                    | 7fps                            |
| yolo11l | 320×320          | seg  | 10fps                    | 7fps                            |
| ------- | ----------       | ---- | -----------              | ------------                    |
| yolov8n | 320×320          | obb  | 44fps                    | 27fps                           |
| yolov8s | 320×320          | obb  | 25fps                    | 18fps                           |
| yolov8m | 320×320          | obb  | 13fps                    | 10fps                           |
| yolov8l | 320×320          | obb  | 8fps                     | 7fps                            |
| yolo11n | 320×320          | obb  | 40fps                    | 25fps                           |
| yolo11s | 320×320          | obb  | 24fps                    | 16fps                           |
| yolo11m | 320×320          | obb  | 14fps                    | 11fps                           |
| yolo11l | 320×320          | obb  | 12fps                    | 9fps                            |

### Changing the Input Resolution

Change the input resolution of the model to suit your scene. Larger resolutions may improve deployment results, but will take more inference time.

The following data takes the kmdel obtained by training in the example data set provided by this document as an example, and the operating performance of kmdel is measured on K230. During actual deployment, the post-processing time will be affected **Number of results** increased impact while memory management `gc.collect()` the time-consuming process will also increase with the complexity of post-processing, so the following data is only referenced for data comparison, you can **Business needs according to different scenarios** choose **Different input resolutions**:

| Model   | Input resolution | Task | kpu inference frame rate | Full frame inference frame rate |
| ------- | ---------------- | ---- | ------------------------ | ------------------------------- |
| yolov5n | 224×224          | cls  | 350fps                   | 57fps                           |
| yolov5n | 320×320          | cls  | 220fps                   | 56fps                           |
| yolov5n | 640 × 640        | cls  | 53fps                    | 32FPS                           |
| yolov5n | 320 × 320        | det  | 54fps                    | 31fps                           |
| yolov5n | 640 × 640        | det  | 16FPS                    | 11fps                           |
| yolov5n | 320 × 320        | seg  | 18fps                    | 11fps                           |
| yolov5n | 640 × 640        | seg  | 4FPS                     | 3FPS                            |
| ------- | ----------       | ---- | ------------             | ------------                    |
| yolov8n | 224 × 224        | cls  | 198fps                   | 57fps                           |
| yolov8n | 320 × 320        | cls  | 121fps                   | 55fps                           |
| yolov8n | 640 × 640        | cls  | 38fps                    | 24fps                           |
| yolov8n | 320 × 320        | det  | 44fps                    | 27fps                           |
| yolov8n | 640 × 640        | det  | 14FPS                    | 10fps                           |
| yolov8n | 320 × 320        | seg  | 39fps                    | 18fps                           |
| yolov8n | 640 × 640        | seg  | 12fps                    | 7fps                            |
| yolov8n | 320 × 320        | obb  | 44fps                    | 27fps                           |
| yolov8n | 640 × 640        | obb  | 13fps                    | 10fps                           |
| ------- | ----------       | ---- | ------------             | ------------                    |
| yolo11n | 224 × 224        | cls  | 158fps                   | 56fps                           |
| yolo11n | 320 × 320        | cls  | 102FPS                   | 49fps                           |
| yolo11n | 640×640          | cls  | 320fps                   | 25fps                           |
| yolo11n | 320×320          | det  | 41fps                    | 26fps                           |
| yolo11n | 640×640          | det  | 12fps                    | 9fps                            |
| yolo11n | 320×320          | seg  | 37fps                    | 17fps                           |
| yolo11n | 640×640          | seg  | 11fps                    | 7fps                            |
| yolo11n | 320×320          | obb  | 40fps                    | 25fps                           |
| yolo11n | 640×640          | obb  | 12fps                    | 9fps                            |

### Modifying the Quantization Method

The model conversion script provides 3 quantization parameters,`data` and `weights` conduct `uint8` quantitative or `int16` quantification.

In the convert kmdel script, select different `ptq_option` values ​​specify different quantization methods.

| ptq_option | data  | Weights |
| ---------- | ----- | ------- |
| 0          | uint8 | uint8   |
| 1          | uint8 | int16   |
| 2          | int16 | uint8   |

The following data takes the kmdel obtained by the detection example data set provided by this document as an example to measure the operating performance of kmdel on K230. During actual deployment, the post-processing time will be affected **Number of results** increased impact while memory management `gc.collect()` the time-consuming process will also increase with the complexity of post-processing, so the following data is only referenced for data comparison, you can **Business needs according to different scenarios** choose **Different quantification methods**:

| Model   | Input resolution | Task | Quantitative parameters [data, weights] | kpu inference frame rate | Full frame inference frame rate |
| ------- | ---------------- | ---- | --------------------------------------- | ------------------------ | ------------------------------- |
| yolov5n | 320×320          | det  | [uint8,uint8]                           | 54fps                    | 32fps                           |
| Yolov5n | 320 × 320        | det  | [Uint8, Int16]                          | 49fps                    | 30fps                           |
| Yolov5n | 320 × 320        | det  | [int16, uint8]                          | 39fps                    | 25fps                           |
| ------- | ----------       | ---- | ----------------------                  | -----------              | ------------                    |
| Yolov8n | 320 × 320        | det  | [Uint8, Uint8]                          | 44fps                    | 27fps                           |
| Yolov8n | 320 × 320        | det  | [Uint8, Int16]                          | 40fps                    | 25fps                           |
| Yolov8n | 320 × 320        | det  | [int16, uint8]                          | 34fps                    | 23fps                           |
| ------- | ----------       | ---- | ----------------------                  | -----------              | ------------                    |
| yolo11n | 320×320          | det  | [uint8,uint8]                           | 41fps                    | 26fps                           |
| yolo11n | 320×320          | det  | [uint8,int16]                           | 38fps                    | 24fps                           |
| yolo11n | 320×320          | det  | [int16,uint8]                           | 32fps                    | 22fps                           |

### Improving Data Quality

If the training results are poor, improve the quality of the dataset by optimizing aspects such as the data volume, reasonable data distribution, annotation quality, and training parameter settings.

### Tuning Tips

- The quantization parameters have a greater impact on the performance of YOLOv8 and YOLO11 than on YOLOv5, as can be seen by comparing different quantized models.
- The input resolution has a greater impact on the inference speed than the model size.
- The difference in data distribution between the training data and the data captured by the K230 camera may affect the deployment effect. You can collect some data using the K230 and annotate and train it yourself.
