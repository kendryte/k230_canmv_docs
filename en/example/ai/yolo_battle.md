# K230 YOLO Showdown

## YOLOv5 Fruit Classification

### YOLOv5 Source Code and Training Environment Setup

For setting up the `YOLOv5` training environment, please refer to [ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5)

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

Please download the provided example dataset. The example dataset provides classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenarios. Extract the dataset into the `yolov5` directory, and please use `fruits_cls` as the dataset for the fruit classification task. The example dataset also includes a rotated target detection desktop pen scene dataset `yolo_pen_obb`, and a license plate keypoint dataset `car_plate`. These two tasks are not supported in the `YOLOv5` module of k230.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete annotation. Classification task data does not require annotation tools, just organize the directories according to the format. Convert the annotated data into the training data format officially supported by `yolov5` for subsequent training.

```shell
cd yolov5
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLOv5 to Train the Fruit Classification Model

Execute the command in the `yolov5` directory to train a three-class fruit classification model using `yolov5`:

```shell
python classify/train.py --model yolov5n-cls.pt --data datasets/fruits_cls --epochs 100 --batch-size 8 --imgsz 224 --device '0'
```

### Converting the Fruit Classification kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# Linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires installing dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# Windows platform: Please install dotnet-7 by yourself and add environment variables. pip online installation of nncase is supported, but the nncase-kpu library requires offline installation. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl at https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment and use pip to install in the directory where nncase_kpu-2.*-py2.py3-none-win_amd64.whl is downloaded
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, extract the model conversion script tool `test_yolov5.zip` into the `yolov5` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

According to the following commands, first export the `pt` model under `runs/train-cls/exp/weights` to an `onnx` model, then convert it to a `kmodel` model:

```shell
# Export onnx, please choose the pt model path yourself
python export.py --weight runs/train-cls/exp/weights/best.pt --imgsz 224 --batch 1 --include onnx
cd test_yolov5/classify
# Convert kmodel, please choose the onnx model path yourself, the generated kmodel will be in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/train-cls/exp/weights/best.onnx --dataset ../calibration_data --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description     | Explanation                                                                                                                                                                                                                                                                                       | Type      |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| target         | Target Platform | Optional values are k230/CPU, corresponding to the k230 chip;                                                                                                                                                                                                                                     | str       |
| model          | Model Path      | Path of the ONNX model to be converted;                                                                                                                                                                                                                                                           | str       |
| dataset        | Calibration Image Set | Image data used in model conversion, used during the quantization stage                                                                                                                                                                                                                      | str       |
| input_width    | Input Width     | Width of the model input                                                                                                                                                                                                                                                                          | int       |
| input_height   | Input Height    | Height of the model input                                                                                                                                                                                                                                                                         | int       |
| ptq_option     | Quantization Method | Quantization strategy is `Kld` and `NoClip`, combining data and weights quantization precision, 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model Using MicroPython on k230

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or use the latest code to compile the firmware yourself. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Copying Model Files

Connect to the IDE and copy the converted model and test images to the path `CanMV/data`. This path can be customized; you only need to modify the corresponding path when writing the code.

#### YOLOv5 Module

The `YOLOv5` class integrates the three tasks of `YOLOv5`, including classification (classify), detection (detect), and segmentation (segment); it supports two inference modes, including image and video stream (video); this class encapsulates the `YOLOv5` kmodel inference process.

- **Import Method**

```python
from libs.YOLO import YOLOv5
```

- **Parameter Description**

| Parameter Name    | Description              | Explanation                                                                                                                                                                                                                                                                                                                | Type         |
| ----------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| task_type         | Task Type                | Supports three types of tasks, optional values are 'classify'/'detect'/'segment';                                                                                                                                                                                                                                          | str          |
| mode              | Inference Mode           | Supports two inference modes, optional values are 'image'/'video'. 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera;                                                                                                                                       | str          |
| kmodel_path       | kmodel Path              | Path of the kmodel copied to the development board;                                                                                                                                                                                                                                                                        | str          |
| labels            | Category Label List      | Label names of different categories;                                                                                                                                                                                                                                                                                       | list[str]    |
| rgb888p_size      | Inference Frame Resolution | Resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];                                                                                                                                                                                                                                   | list[int]    |
| model_input_size  | Model Input Resolution   | Input resolution when training the YOLOv5 model, such as [224,224], [320,320], [640,640];                                                                                                                                                                                                                                 | list[int]    |
| display_size      | Display Resolution      | Set when the inference mode is 'video'. Supports hdmi([1920,1080]) and lcd([800,480]);                                                                                                                                                                                                                                       | list[int]    |
| conf_thresh       | Confidence Threshold     | Category confidence threshold for classification tasks, target confidence threshold for detection and segmentation tasks, such as 0.5;                                                                                                                                                                                     | float【0~1】 |
| nms_thresh        | nms Threshold            | Non-maximum suppression threshold, required for detection and segmentation tasks;                                                                                                                                                                                                                                          | float【0~1】 |
| mask_thresh       | mask Threshold             | Binarization threshold for segmenting objects in the detection box in the segmentation task;                                                                                                                                                                                                                              | float【0~1】 |
| max_boxes_num     | Maximum Detection Box Number | Maximum number of detection boxes allowed to be returned in one frame;                                                                                                                                                                                                                                                | int          |
| debug_mode        | Debug Mode               | Whether the timing function is active. Optional values are 0/1. 0 means no timing, 1 means timing;                                                                                                                                                                                                                        | int【0/1】   |

#### Deploying the Model for Image Inference

For image inference, please refer to the following code, **modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify to your own test images, model path, label names, and model input size
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the following code, **modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify to your own model path, label names, and model input size
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    # Display mode. "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/lt9611/st7701/hx8399/nt35516/nt35532/gc9503/aml020t/jd9852/ili9806/virt
    display_mode="auto"
    # Display resolution. None means using the default resolution of the current display screen; when using virt, you can set it manually here, for example [800, 480]
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode, display_size=display_size)
    # Create a PipeLine. You can pass sensor_id to select the camera as needed, for example pl.create(sensor_id=2)
    pl.create()
    display_size=pl.get_display_size()
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="classify",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,debug_mode=0)
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

## YOLOv5 Fruit Detection

### YOLOv5 Source Code and Training Environment Setup

For `YOLOv5` training environment setup, please refer to [ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5)

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

Please download the provided sample dataset. The sample dataset contains classification, detection, and segmentation datasets for three categories of fruits (apple, banana, orange) as scenarios. Extract the dataset to the `yolov5` directory. Please use `fruits_yolo` as the dataset for the fruit detection task. The sample dataset also includes a rotated object detection dataset for the desktop pen scenario `yolo_pen_obb`, and a license plate keypoint dataset `car_plate`. These two tasks are not supported in the `YOLOv5` module on the k230.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Manually convert the annotated data into the training data format officially supported by `yolov5` for subsequent training.

```shell
cd yolov5
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLOv5 to Train the Fruit Detection Model

Execute the command in the `yolov5` directory to use `yolov5` to train the three-category fruit detection model:

```shell
python train.py --weight yolov5n.pt --cfg models/yolov5n.yaml --data datasets/fruits_yolo.yaml --epochs 300 --batch-size 8 --imgsz 320 --device '0'
```

### Converting the Fruit Detection kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7 installation
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: please install dotnet-7 yourself and add environment variables. Online pip installation of nncase is supported, but the nncase-kpu library requires offline installation. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl at https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip to install in the directory where nncase_kpu-2.*-py2.py3-none-win_amd64.whl is downloaded
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tools and extract the model conversion script tool `test_yolov5.zip` to the `yolov5` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

According to the following commands, first export the `pt` model under `runs/train/exp/weights` to an `onnx` model, then convert it to a `kmodel` model:

```shell
# Export onnx, please choose the pt model path yourself
python export.py --weight runs/train/exp/weights/best.pt --imgsz 320 --batch 1 --include onnx
cd test_yolov5/detect
# Convert kmodel, please customize the onnx model path, the generated kmodel is in the same level directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/train/exp/weights/best.onnx --dataset ../calibration_data --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model conversion script (to_kmodel.py) parameter description**:

| Parameter Name | Description     | Description                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Optional values are k230/CPU, corresponding to k230 chip;                              | str   |
| model        | Model Path | Path to the ONNX model to be converted;                                        | str   |
| dataset      | Calibration Image Set  | Image data used during model conversion, used in the quantization stage                    | str   |
| input_width  | Input Width | The width of the model input                                             | int   |
| input_height | Input Height | The height of the model input                                             | int   |
| ptq_option   | Quantization Method | Quantization strategies are `Kld` and `NoClip`, combining data and weights quantization precision. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Alternatively, use the latest code to compile the firmware yourself. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE and copy the converted model and test images to the path `CanMV/data` directory. This path can be customized; you only need to modify the corresponding path when writing code.

#### YOLOv5 Module

The `YOLOv5` class integrates three tasks of `YOLOv5`, including classification (classify), detection (detect), and segmentation (segment); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the kmodel inference process of `YOLOv5`.

- **Import Method**

```python
from libs.YOLO import YOLOv5
```

- **Parameter Description**

| Parameter Name         | Description           | Description                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports three tasks, optional values are 'classify'/'detect'/'segment';        | str          |
| mode             | Inference Mode       | Supports two inference modes, optional values are 'image'/'video', 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | The kmodel path copied to the development board;                                   | str          |
| labels           | Category Label List   | The label names of different categories;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | The resolution of the current frame for inference, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | The input resolution when training the YOLOv5 model, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | Category confidence threshold for classification tasks, object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh       | nms Threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float【0~1】 |
| mask_thresh      | mask Threshold       | The binarization threshold when segmenting objects in the detection box in the segmentation task;             | float【0~1】 |
| max_boxes_num    | Maximum Number of Detection Boxes   | The maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function takes effect, optional value 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code, **modify the definition parameters in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify it to your own test images, model path, label names, and model input size
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
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

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code, **modify the definition variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify it to your own model path, label names, and model input size
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; can also explicitly specify hdmi/lcd/lt9611/st7701/hx8399/nt35516/nt35532/gc9503/aml020t/jd9852/ili9806/virt
    display_mode="auto"
    # Display resolution, None means using the default resolution of the current display screen; when using virt, it can be manually set here, for example [800, 480]
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.8
    nms_threshold=0.45
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode, display_size=display_size)
    # Create a PipeLine, you can pass in sensor_id to select the camera as needed, for example pl.create(sensor_id=2)
    pl.create()
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

## YOLOv5 Fruit Segmentation

### YOLOv5 Source Code and Training Environment Setup

For `YOLOv5` training environment setup, please refer to [ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5)

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

Please download the provided sample dataset. The sample dataset includes classification, detection, and segmentation datasets for three categories of fruits (apple, banana, orange) as scenarios. Extract the dataset to the `yolov5` directory. Please use `fruits_seg` as the dataset for the fruit segmentation task. The sample dataset also includes a rotated object detection desktop pen scenario dataset `yolo_pen_obb`, and a license plate keypoint dataset `car_plate`. These two tasks are not supported in the `YOLOv5` module of the k230.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert the annotated data into the training data format officially supported by `yolov5` for subsequent training.

```shell
cd yolov5
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLOv5 to Train the Fruit Segmentation Model

Execute the command in the `yolov5` directory, using `yolov5` to train the three-category fruit segmentation model:

```shell
python segment/train.py --weight yolov5n-seg.pt --cfg models/segment/yolov5n-seg.yaml --data datasets/fruits_seg.yaml --epochs 100 --batch-size 8 --imgsz 320 --device '0'
```

### Converting the Fruit Segmentation kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires installing dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: please install dotnet-7 yourself and add environment variables, support installing nncase online using pip, but the nncase-kpu library needs to be installed offline, download nncase_kpu-2.*-py2.py3-none-win_amd64.whl at https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl, use pip to install
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used in the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, extract the model conversion script tool `test_yolov5.zip` to the `yolov5` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

Follow the commands below to first export the model under `runs/train-seg/exp/weights` as an `onnx` model, then convert it to a `kmodel` model:

```shell
python export.py --weight runs/train-seg/exp/weights/best.pt --imgsz 320 --batch 1 --include onnx
cd test_yolov5/segment
# Convert kmodel, the onnx model path is customizable, the generated kmodel is in the same level directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/train-seg/exp/weights/best.onnx --dataset ../calibration_data --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Description                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Options are k230/CPU, corresponding to the k230 chip;                              | str   |
| model        | Model Path | The path of the ONNX model to be converted;                                        | str   |
| dataset      | Calibration Image Set  | The image data used during model conversion, used in the quantization phase                    | str   |
| input_width  | Input Width | The width of the model input                                             | int   |
| input_height | Input Height | The height of the model input                                             | int   |
| ptq_option   | Quantization Method | The quantization strategies are `Kld` and `NoClip`, combining the quantization precision of data and weights, 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flash the Image and Install CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or compile the firmware yourself using the latest code. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write code in the IDE and run it.

#### Model File Copy

Connect the IDE, copy the converted model and test images to the path `CanMV/data`. This path can be customized, you only need to modify the corresponding path when writing code.

#### YOLOv5 Module

The `YOLOv5` class integrates the three tasks of `YOLOv5`, including classification (classify), detection (detect), and segmentation (segment); it supports two inference modes, including image and video stream; this class encapsulates the `YOLOv5` kmodel inference process.

- **Import Method**

```python
from libs.YOLO import YOLOv5
```

- **Parameter Description**

| Parameter Name         | Description           | Description                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports three types of tasks, options are 'classify'/'detect'/'segment';        | str          |
| mode             | Inference Mode       | Supports two inference modes, options are 'image'/'video', 'image' means inferring an image, 'video' means inferring a real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | The kmodel path copied to the development board;                                   | str          |
| labels           | Category Label List   | The label names of different categories;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | The resolution of the current frame for inference, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | The input resolution when training the YOLOv5 model, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | The category confidence threshold for classification tasks, and the object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh       | nms Threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float【0~1】 |
| mask_thresh      | mask Threshold       | The binarization threshold for segmenting the object in the detection box in the segmentation task;             | float【0~1】 |
| max_boxes_num    | Maximum Number of Detection Boxes   | The maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function is effective, options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code, **modify the definition parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own test image, model path, label name, model input size for custom scenarios
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code, **modify the definition variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own model path, label name, model input size for custom scenarios
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for the values
    display_mode="auto"
    # None means using the default resolution of the screen driver; when you need to specify, fill in [width, height]
    display_size=None
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="segment",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
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

## YOLOv8 Fruit Classification

### YOLOv8 Source Code and Training Environment Setup

For setting up the `YOLOv8` training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolov8`. Please download the provided sample dataset. The sample dataset contains classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenarios. Extract the dataset to the `yolov8` directory. Please use `fruits_cls` as the dataset for the fruit classification task. The sample dataset also contains a rotated object detection dataset `yolo_pen_obb` for desktop pens, and a license plate keypoint dataset `car_plate`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete annotation. Classification task data does not need to be annotated using tools, just divide the directories according to the format. Convert the annotated data into the training data format officially supported by `yolov8` for subsequent training.

```shell
cd yolov8
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLOv8 to Train the Fruit Classification Model

Run the following command in the `yolov8` directory to use `yolov8` to train the three-class fruit classification model:

```shell
yolo classify train data=datasets/fruits_cls model=yolov8n-cls.pt epochs=100 imgsz=224
```

### Converting the Fruit Classification kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# Linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7 to be installed
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# Windows platform: Please install dotnet-7 yourself and add environment variables. pip online installation of nncase is supported, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding Python environment, and install using pip in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used in the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool and extract the model conversion script tool `test_yolov8.zip` to the `yolov8` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

Follow the commands below to first export the `pt` model under `runs/classify/train/weights` to an `onnx` model, and then convert it to a `kmodel`:

```shell
# Export onnx, please choose the pt model path yourself
yolo export model=runs/classify/train/weights/best.pt format=onnx imgsz=224
cd test_yolov8/classify
# Convert kmodel, please choose the onnx model path yourself, the generated kmodel will be in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/classify/train/weights/best.onnx --dataset ../calibration_data --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

💡 **Model conversion script (to_kmodel.py) parameter description**:

| Parameter Name | Description | Notes                                                          | Type       |
| -------------- | ----------- | ------------------------------------------------------------- | ---------- |
| target         | Target platform | Optional values are k230/CPU, corresponding to the k230 chip; | str        |
| model          | Model path | Path of the ONNX model to be converted;                        | str        |
| dataset        | Calibration image set | Image data used during model conversion, used in the quantization stage | str        |
| input_width    | Input width | Width of the model input                                    | int        |
| input_height   | Input height | Height of the model input                                   | int        |
| ptq_option     | Quantization method | Quantization strategies are `Kld` and `NoClip`, combining the quantization precision of data and weights. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Dalily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure **the latest features** are supported! Or use the latest code to compile the firmware yourself. See the tutorial: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Copying Model Files

Connect the IDE and copy the converted model and test images to the path `CanMV/data`. This path can be customized, just modify the corresponding path when writing code.

#### YOLOv8 Module

The `YOLOv8` class integrates five tasks of `YOLOv8`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the `YOLOv8` kmodel inference process.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name    | Description        | Notes                                                         | Type        |
| ----------------- | ------------------ | ------------------------------------------------------------- | ----------- |
| task_type         | Task type          | Supports four types of tasks, optional values are 'classify'/'detect'/'segment'/'obb'/'pose'; | str         |
| mode              | Inference mode     | Supports two inference modes, optional values are 'image'/'video'. 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera; | str         |
| kmodel_path       | kmodel path        | Path of the kmodel copied to the development board;           | str         |
| labels            | Category label list | Label names for different categories;                         | list[str]   |
| rgb888p_size      | Inference frame resolution | Resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640]; | list[int]   |
| model_input_size  | Model input resolution | Input resolution when training the YOLOv8 model, such as [224,224], [320,320], [640,640]; | list[int]   |
| display_size      | Display resolution | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]   |
| conf_thresh       | Confidence threshold | Category confidence threshold for classification tasks, object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】|
| nms_thresh        | NMS threshold      | Non-maximum suppression threshold, required for detection and segmentation tasks; | float【0~1】|
| mask_thresh       | Mask threshold      | Binarization threshold for segmenting the object in the detection box in the segmentation task; | float【0~1】|
| kp_num            | Number of keypoints | Number of keypoints in the keypoint detection task;           | int         |
| kp_dim            | Keypoint dimension | Dimension of keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model; | int【2/3】  |
| max_boxes_num     | Maximum number of detection boxes | Maximum number of detection boxes allowed to be returned in one frame of image; | int         |
| debug_mode        | Debug mode         | Whether the timing function takes effect, optional 0/1, 0 means no timing, 1 means timing; | int【0/1】  |

#### Deploying the Model for Image Inference

For image inference, please refer to the following code, **modify the definition parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is just an example. For custom scenarios, please modify it to your own test image, model path, label name, and model input size
    img_path="/data/test_apple.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv8 instance
    yolo=YOLOv8(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the following code, **modify the definition variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is just an example. For custom scenarios, please modify it to your own model path, label name, and model input size
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; can also explicitly specify hdmi/lcd/st7701, etc. See the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; specify [width, height] when needed
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.8
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLOv8 instance
    yolo=YOLOv8(task_type="classify",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,debug_mode=0)
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

## YOLOv8 Fruit Detection

### YOLOv8 Source Code and Training Environment Setup

For setting up the YOLOv8 training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolov8`. Please download the provided example dataset. The example dataset includes classification, detection, and segmentation datasets for three categories of fruits (apple, banana, orange) as scenarios. Extract the dataset into the `yolov8` directory and use `fruits_yolo` as the dataset for the fruit detection task. The example dataset also includes a rotated object detection desktop pen scenario dataset `yolo_pen_obb`, and a license plate keypoint dataset `car_plate`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete annotation. Convert the annotated data into the training data format officially supported by `yolov8` for subsequent training.

```shell
cd yolov8
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLOv8 to Train the Fruit Detection Model

Execute the command in the `yolov8` directory to train the three-category fruit detection model with `yolov8`:

```shell
yolo detect train data=datasets/fruits_yolo.yaml model=yolov8n.pt epochs=300 imgsz=320
```

### Convert Fruit Detection kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# Linux platform: nncase and nncase-kpu can be installed online; nncase-2.x requires installing dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# Windows platform: Please install dotnet-7 and add environment variables yourself. Installing nncase online with pip is supported, but the nncase-kpu library must be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, then use pip to install it in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, and extract the model conversion script tool `test_yolov8.zip` into the `yolov8` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

According to the following commands, first export the `pt` model under `runs/detect/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export to onnx; please select the pt model path yourself
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/detect
# Convert to kmodel; please select the onnx model path yourself. The generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset ../calibration_data --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Instructions                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Options are k230/CPU, corresponding to the k230 chip;                              | str   |
| model        | Model Path | Path to the ONNX model to be converted;                                        | str   |
| dataset      | Calibration Image Set  | Image data used during model conversion, used in the quantization stage                    | str   |
| input_width  | Input Width | Width of the model input                                             | int   |
| input_height | Input Height | Height of the model input                                             | int   |
| ptq_option   | Quantization Method | Quantization strategies are `Kld` and `NoClip`, combining the quantization precision of data and weights. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 using MicroPython

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or use the latest code to compile the firmware yourself. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE, and copy the converted model and test images to the path `CanMV/data`. This path can be customized; you only need to modify the corresponding path when writing code.

#### YOLOv8 Module

The `YOLOv8` class integrates the five tasks of `YOLOv8`, including classification, detection, segmentation, rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image and video stream; this class encapsulates the `YOLOv8` kmodel inference process.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name         | Description           | Instructions                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports four types of tasks, with options 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference Mode       | Supports two inference modes, with options 'image'/'video'. 'image' means inference on images, 'video' means inference on real-time video streams captured by the camera; | str          |
| kmodel_path      | kmodel Path     | Path to the kmodel copied to the development board;                                   | str          |
| labels           | Class Label List   | Label names for different classes;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | Inference frame resolution, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | Input resolution when training the YOLOv8 model, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | Confidence threshold for classification task categories, and object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh       | nms Threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float【0~1】 |
| mask_thresh      | mask Threshold       | Binarization threshold for segmenting objects in the detection box in segmentation tasks;             | float【0~1】 |
| kp_num           | Number of Keypoints     | Number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint Dimension     | Dimension of keypoints in the keypoint detection task. Only 2 and 3 are supported, determined by the training model;    | int【2/3】  |
| max_boxes_num    | Maximum Number of Detection Boxes   | Maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function is enabled, options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model for Image Inference

For image inference, please refer to the following code, **modify the definition parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    nms_threshold=0.45
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLOv8实例
    yolo=YOLOv8(task_type="detect",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the following code, **modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定hdmi/lcd/st7701等，取值见PipeLine手册
    display_mode="auto"
    # None表示使用屏驱动的默认分辨率；需要指定时填[宽, 高]
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    nms_threshold=0.45
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # create之后再取实际显示分辨率
    display_size=pl.get_display_size()
    # 初始化YOLOv8实例
    yolo=YOLOv8(task_type="detect",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            # 逐帧推理
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

## YOLOv8 Fruit Segmentation

### YOLOv8 Source Code and Training Environment Setup

For `YOLOv8` training environment setup, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please skip this step.

### Training Data Preparation

You can first create a new folder `yolov8`. Please download the provided sample dataset. The sample dataset includes three fruit categories (apple, banana, orange) as scenarios, and provides classification, detection, and segmentation datasets respectively. Extract the dataset to the `yolov8` directory, and use `fruits_seg` as the dataset for the fruit segmentation task. The sample dataset also includes a rotated object detection desktop pen scene dataset `yolo_pen_obb` and a license plate keypoint dataset `car_plate`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete annotation. Convert the annotated data into the training data format officially supported by `yolov8` for subsequent training.

```shell
cd yolov8
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please skip this step.

### Using YOLOv8 to Train the Fruit Segmentation Model

Execute the following command in the `yolov8` directory to use `yolov8` to train a three-class fruit segmentation model:

```shell
yolo segment train data=datasets/fruits_seg.yaml model=yolov8n-seg.pt epochs=100 imgsz=320
```

### Converting Fruit Segmentation kmodel

The model conversion requires installing the following libraries in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: please install dotnet-7 by yourself and add environment variables. nncase can be installed online via pip, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip to install in the directory where nncase_kpu-2.*-py2.py3-none-win_amd64.whl is downloaded
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, the other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, and extract the model conversion script tool `test_yolov8.zip` to the `yolov8` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

According to the following commands, first export the `pt` model under `runs/segment/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please choose the pt model path yourself
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/segment
# Convert kmodel, please choose the onnx model path yourself. The generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset ../calibration_data --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Notes                                                         | Type   |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Options are k230/CPU, corresponding to k230 chip;                              | str   |
| model        | Model Path | Path of the ONNX model to be converted;                                        | str   |
| dataset      | Calibration Image Set  | Image data used for model conversion, used in the quantization stage                    | str   |
| input_width  | Input Width | Width of the model input                                             | int   |
| input_height | Input Height | Height of the model input                                             | int   |
| ptq_option   | Quantization Method | The quantization strategies are `Kld` and `NoClip`, combining the quantization accuracy of data and weights. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that the **latest features** are supported! Or use the latest code to compile the firmware yourself. See the tutorial: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE, and copy the converted model and test images to the path `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing code.

#### YOLOv8 Module

The `YOLOv8` class integrates the five tasks of `YOLOv8`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image and video stream (video); this class encapsulates the `YOLOv8` kmodel inference process.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name         | Description           | Notes                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports four types of tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference Mode       | Supports two inference modes, options are 'image'/'video'. 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | Path of the kmodel copied to the development board;                                   | str          |
| labels           | Category Label List   | Label names for different categories;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | Resolution of the currently inferred frame, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | Input resolution when the YOLOv8 model is trained, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | Category confidence threshold for classification tasks, target confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh       | NMS Threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float【0~1】 |
| mask_thresh      | Mask Threshold       | Binarization threshold for segmenting objects in the detection box in the segmentation task;             | float【0~1】 |
| kp_num           | Number of Keypoints     | Number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint Dimension     | Dimension of the keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model;    | int【2/3】  |
| max_boxes_num    | Maximum Number of Detection Boxes   | Maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function is enabled, options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model for Image Inference

For image inference, please refer to the following code, and **modify the definition parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify it to your own test image, model path, label name, and model input size
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv8 instance
    yolo=YOLOv8(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the following code, and **modify the definition variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify it to your own model path, label name, and model input size
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLOv8 instance
    yolo=YOLOv8(task_type="segment",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
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

## YOLOv8 Rotated Object Detection

### YOLOv8 Source Code and Training Environment Setup

For `YOLOv8` training environment setup, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolov8`. Please download the provided example dataset, which contains one rotated object detection category (pen) as the scenario, and the dataset is provided for it. Extract the dataset to the `yolov8` directory, please use `yolo_pen_obb` as the dataset for the rotated object detection task.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Manually convert the annotated data into the training data format officially supported by `yolov8` for subsequent training.

```shell
cd yolov8
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLOv8 to Train a Rotated Object Detection Model

Execute the command in the `yolov8` directory to train a single-class rotated object detection model using `yolov8`:

```shell
yolo obb train data=datasets/pen_obb.yaml model=yolov8n-obb.pt epochs=100 imgsz=320
```

### Convert Rotated Object Detection kmodel

Model conversion requires the following libraries to be installed in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7 to be installed
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: please install dotnet-7 yourself and add environment variables. nncase supports online installation via pip, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl at https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and install using pip in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, extract the model conversion script tool `test_yolov8.zip` to the `yolov8` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

According to the following command, first export the `pt` model under `runs/obb/train/weights` to the `onnx` model, and then convert it to the `kmodel` model:

```shell
# Export onnx, please choose the pt model path yourself
yolo export model=runs/obb/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/obb
# Convert kmodel, please choose the onnx model path yourself, the generated kmodel is in the same level directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/obb/train/weights/best.onnx --dataset ../calibration_obb --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model conversion script (to_kmodel.py) parameter description**:

| Parameter Name | Description | Description                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target platform | The options are k230/CPU, corresponding to the k230 chip;                              | str   |
| model        | Model path | The path of the ONNX model to be converted;                                        | str   |
| dataset      | Calibration image set  | The image data used during model conversion, used in the quantization stage                    | str   |
| input_width  | Input width | The width of the model input                                             | int   |
| input_height | Input height | The height of the model input                                             | int   |
| ptq_option   | Quantization method | The quantization strategies are `Kld` and `NoClip`, combined with the quantization accuracy of data and weights. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flash Image and Install CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or use the latest code to compile the firmware yourself, see the tutorial: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE, copy the converted model and test images to the path `CanMV/data` directory. This path can be customized, you only need to modify the corresponding path when writing the code.

#### YOLOv8 Module

The `YOLOv8` class integrates five tasks of `YOLOv8`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the `YOLOv8` kmodel inference process.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name         | Description           | Description                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task type       | Supports four types of tasks, the options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference mode       | Supports two inference modes, the options are 'image'/'video', 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel path     | The kmodel path copied to the development board;                                   | str          |
| labels           | Category label list   | The label names of different categories;                                         | list[str]    |
| rgb888p_size     | Inference frame resolution   | The current frame resolution for inference, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model input resolution | The input resolution when training the YOLOv8 model, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence threshold     | The category confidence threshold for classification tasks, and the object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh       | nms threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float【0~1】 |
| mask_thresh      | mask threshold       | The binarization threshold when segmenting the objects in the detection box in the segmentation task;             | float【0~1】 |
| kp_num           | Number of key points     | The number of key points in the key point detection task;                              | int        |
| kp_dim           | Key point dimension     | The dimension of the key points in the key point detection task, only 2 and 3 are supported, determined by the trained model;    | int【2/3】  |
| max_boxes_num    | Maximum number of detection boxes   | The maximum number of detection boxes allowed to be returned in one frame of image;                         | int          |
| debug_mode       | Debug mode       | Whether the timing function is effective, the options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model for Image Inference

For image inference, please refer to the following code, **modify the parameters defined in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, for custom scenarios please modify it to your own test image, model path, label name, model input size
    img_path="/data/test_obb.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    confidence_threshold = 0.1
    nms_threshold=0.6
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv8 instance
    yolo=YOLOv8(task_type="obb",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the following code, **modify the variables defined in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, for custom scenarios please modify it to your own model path, label name, model input size
    kmodel_path="/data/best_yolov8n.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.1
    nms_threshold=0.6
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLOv8 instance
    yolo=YOLOv8(task_type="obb",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
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

## YOLOv8 License Plate Corner Detection

### YOLOv8 Source Code and Training Environment Setup

For setting up the `YOLOv8` training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolov8`, please download the provided example dataset. The example dataset contains datasets for license plate detection four-corner keypoint scenarios. Extract the dataset to the `yolov8` directory, and use `car_plate` as the dataset for the keypoint detection task.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert your annotated data into the training data format officially supported by `yolov8` for subsequent training.

```shell
cd yolov8
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLOv8 to Train Keypoint Detection Model

Execute the command in the `yolov8` directory to train a single-class rotated object detection model using `yolov8`:

```shell
yolo pose train data=datasets/car_plate.yaml model=yolov8n-pose.pt epochs=100 imgsz=320
```

### Converting Keypoint Detection kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# Linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires installing dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# Windows platform: Please install dotnet-7 yourself and add environment variables. nncase can be installed online using pip, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment and use pip to install in the directory where nncase_kpu-2.*-py2.py3-none-win_amd64.whl is downloaded
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script utility, and extract the model conversion script utility `test_yolov8.zip` to the `yolov8` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

According to the following command, first export the `pt` model under `runs/pose/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the pt model path yourself
yolo export model=runs/pose/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/pose
# Convert kmodel, please select the onnx model path yourself, the generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/pose/train/weights/best.onnx --dataset ../calibration_pose --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Notes                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Options are k230/CPU, corresponding to the k230 chip;                              | str   |
| model        | Model Path | The path of the ONNX model to be converted;                                        | str   |
| dataset      | Calibration Image Set  | Image data used during model conversion, used in the quantization stage                    | str   |
| input_width  | Input Width | The width of the model input                                             | int   |
| input_height | Input Height | The height of the model input                                             | int   |
| ptq_option   | Quantization Method | Quantization strategies are `Kld` and `NoClip`, combining data and weights quantization precision, 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying Model on k230 Using MicroPython

#### Flashing Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build Firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure the **latest features** are supported! Or use the latest code to compile the firmware yourself, see the tutorial: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE, and copy the converted model and test images to the path `CanMV/data`. This path can be customized, just modify the corresponding path when writing code.

#### YOLOv8 Module

The `YOLOv8` class integrates the five tasks of `YOLOv8`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image and video stream; this class encapsulates the kmodel inference process of `YOLOv8`.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name         | Description           | Notes                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports four tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference Mode       | Supports two inference modes, options are 'image'/'video', 'image' means inferring images, 'video' means inferring real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | The path of the kmodel copied to the development board;                                   | str          |
| labels           | Class Label List   | Label names for different classes;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | The resolution of the current frame for inference, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | The input resolution when the YOLOv8 model is trained, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | Class confidence threshold for classification tasks, object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh       | nms Threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float【0~1】 |
| mask_thresh      | mask Threshold       | The binarization threshold when segmenting objects in the detection box in the segmentation task;             | float【0~1】 |
| kp_num           | Number of Keypoints     | The number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint Dimension     | The dimension of keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model;    | int【2/3】  |
| max_boxes_num    | Maximum Detection Boxes   | The maximum number of detection boxes allowed to return in one frame of image;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function is enabled, options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying Model for Image Inference

For image inference, please refer to the following code, **modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify to your own test image, model path, label name, model input size, number of keypoints, and keypoint dimension
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ['plate']
    model_input_size=[320,320]
    kp_num=4
    kp_dim=2

    confidence_threshold = 0.5
    nms_threshold=0.45
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize YOLOv8 model
    yolo=YOLOv8(task_type="pose",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,kp_num=kp_num,kp_dim=kp_dim,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()

```

#### Deploying Model for Video Inference

For video inference, please refer to the following code, **modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify to your own model path, label name, model input size, number of keypoints, and keypoint dimension
    kmodel_path="/data/best.kmodel"
    labels = ["plate"]
    model_input_size=[320,320]
    kp_num=4
    kp_dim=2

    # Display mode, "auto" automatically selects the screen driver according to the development board model; can also explicitly specify hdmi/lcd/st7701, etc., see PipeLine manual for values
    display_mode="auto"
    # None means use the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize YOLOv8 model
    yolo=YOLOv8(task_type="pose",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,kp_num=kp_num,kp_dim=kp_dim,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
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

## YOLO11 Fruit Classification

### YOLO11 Source Code and Training Environment Setup

For `YOLO11` training environment setup, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolo11`, please download the provided sample dataset. The sample dataset includes classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenarios. Extract the dataset to the `yolo11` directory, please use `fruits_cls` as the dataset for the fruit classification task. The sample dataset also includes a rotated object detection scene dataset `yolo_pen_obb` for a desktop signature pen, and a license plate keypoint detection dataset `car_plate`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Classification task data does not need to be annotated using tools, just divide the directory according to the format. Convert the annotated data into the training data format officially supported by `yolo11` for subsequent training.

```shell
cd yolo11
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLO11 to Train the Fruit Classification Model

Execute the command in the `yolo11` directory, use `yolo11` to train the three-class fruit classification model:

```shell
yolo classify train data=datasets/fruits_cls model=yolo11n-cls.pt epochs=100 imgsz=224
```

### Convert Fruit Classification kmodel

Model conversion requires the following libraries to be installed in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7 to be installed
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: please install dotnet-7 yourself and add environment variables. Online installation of nncase via pip is supported, but the nncase-kpu library requires offline installation. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, and extract the model conversion script tool `test_yolo11.zip` to the `yolo11` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

According to the following commands, first export the `pt` model under `runs/classify/train/weights` to an `onnx` model, then convert it to a `kmodel` model:

```shell
# Export onnx, please choose the pt model path yourself
yolo export model=runs/classify/train/weights/best.pt format=onnx imgsz=224
cd test_yolo11/classify
# Convert kmodel, please choose the onnx model path yourself, the generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/classify/train/weights/best.onnx --dataset ../calibration_data --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Explanation | Type |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Options are k230/CPU, corresponding to the k230 chip;                              | str   |
| model        | Model Path | Path of the ONNX model to be converted;                                        | str   |
| dataset      | Calibration Image Set  | Image data used during model conversion, used during the quantization stage                    | str   |
| input_width  | Input Width | Width of the model input                                             | int   |
| input_height | Input Height | Height of the model input                                             | int   |
| ptq_option   | Quantization Method | Quantization strategies are `Kld` and `NoClip`, combining the quantization accuracy of data and weights, 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Dalily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure the **latest features** are supported! Or use the latest code to compile the firmware yourself, see the tutorial: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE, and copy the converted model and test images to the path `CanMV/data` directory. This path can be customized, you just need to modify the corresponding path when writing the code.

#### YOLO11 Module

The `YOLO11` class integrates five tasks of `YOLO11`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the `YOLO11` kmodel inference workflow.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name         | Description           | Explanation                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports four types of tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference Mode       | Supports two inference modes, options are 'image'/'video', 'image' means inferring on an image, 'video' means inferring on the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | Path of the kmodel copied to the development board;                                   | str          |
| labels           | Class Label List   | Label names for different classes;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | Resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | Input resolution when training the YOLO11 model, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | Class confidence threshold for classification task, object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh       | nms Threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float【0~1】 |
| mask_thresh      | mask Threshold       | Binarization threshold for segmenting the detected object within the detection box in the segmentation task;             | float【0~1】 |
| kp_num           | Number of Keypoints     | Number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint Dimension     | Dimension of keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model;    | int【2/3】  |
| max_boxes_num    | Maximum Number of Detection Boxes   | Maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function is active, options 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code, **modify the definition parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify to your own test image, model path, label name, and model input size for custom scenarios
    img_path="/data/test_apple.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code, **modify the definition variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify to your own model path, label name, and model input size for custom scenarios
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.8
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="classify",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,debug_mode=0)
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

<a id="yolo11-fruit-detection"></a>

## YOLO11 Fruit Detection

### YOLO11 Source Code and Training Environment Setup

For setting up the `YOLO11` training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolo11`, please download the provided sample dataset. The sample dataset includes classification, detection, and segmentation datasets for a three-class fruit (apple, banana, orange) scenario. Extract the dataset into the `yolo11` directory, and please use `fruits_yolo` as the dataset for the fruit detection task. The sample dataset also includes a rotated object detection desktop pen scenario dataset `yolo_pen_obb`, and a license plate keypoint detection dataset `car_plate`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert the annotated data into the training data format officially supported by `yolo11` for subsequent training.

```shell
cd yolo11
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLO11 to Train the Fruit Detection Model

Execute the command in the `yolo11` directory, using `yolo11` to train the three-class fruit detection model:

```shell
yolo detect train data=datasets/fruits_yolo.yaml model=yolo11n.pt epochs=300 imgsz=320
```

### Convert Fruit Detection kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires installing dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: please install dotnet-7 yourself and add environment variables. Online pip installation of nncase is supported, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# Besides nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, and extract the model conversion script tool `test_yolo11.zip` into the `yolo11` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

According to the following commands, first export the `pt` model under `runs/detect/train/weights` to an `onnx` model, then convert it to a `kmodel` model:

```shell
# Export onnx, please select the pt model path yourself
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/detect
# Convert kmodel, please select the onnx model path yourself, the generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset ../calibration_data --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Instructions                                                                                                                                                                                                                                                                  | Type       |
| -------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| target         | Target Platform | Optional values are k230/CPU, corresponding to the k230 chip;                                                                                                                                                                                                          | str        |
| model          | Model Path | The path of the ONNX model to be converted;                                                                                                                                                                                                                              | str        |
| dataset        | Calibration Image Set | Image data used during model conversion, used in the quantization stage                                                                                                                                                                                              | str        |
| input_width    | Input Width | The width of the model input                                                                                                                                                                                                                                              | int        |
| input_height   | Input Height | The height of the model input                                                                                                                                                                                                                                            | int        |
| ptq_option     | Quantization Method | Quantization strategies are `Kld` and `NoClip`, combining data and weights quantization precision. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploy Model on k230 with MicroPython

#### Flash Image and Install CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Dalily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or use the latest code to compile the firmware yourself, see the tutorial: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write code and run it in the IDE.

#### Model File Copy

Connect the IDE, copy the converted model and test images to the path `CanMV/data`. This path can be customized; you only need to modify the corresponding path when writing the code.

#### YOLO11 Module

The `YOLO11` class integrates five tasks of `YOLO11`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the kmodel inference process of `YOLO11`.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name    | Description                       | Instructions                                                                                                                                                                                              | Type          |
| ----------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| task_type         | Task Type                         | Supports four tasks, optional values are 'classify'/'detect'/'segment'/'obb'/'pose';                                                                                                                       | str           |
| mode              | Inference Mode                    | Supports two inference modes, optional values are 'image'/'video'. 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera;                          | str           |
| kmodel_path       | kmodel Path                       | The path of the kmodel copied to the development board;                                                                                                                                                     | str           |
| labels            | Class Label List                  | The label names of different classes;                                                                                                                                                                      | list[str]     |
| rgb888p_size      | Inference Frame Resolution        | The resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];                                                                                                                | list[int]     |
| model_input_size  | Model Input Resolution            | The input resolution when training the YOLO11 model, such as [224,224], [320,320], [640,640];                                                                                                            | list[int]     |
| display_size      | Display Resolution                | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]);                                                                                                                    | list[int]     |
| conf_thresh       | Confidence Threshold              | The class confidence threshold for classification tasks, and the object confidence threshold for detection/segmentation tasks, such as 0.5;                                                                | float【0~1】  |
| nms_thresh        | NMS Threshold                     | Non-maximum suppression threshold, required for detection and segmentation tasks;                                                                                                                          | float【0~1】  |
| mask_thresh       | Mask Threshold                    | The binarization threshold for segmenting objects in the detection box in segmentation tasks;                                                                                                            | float【0~1】  |
| kp_num            | Number of Keypoints               | The number of keypoints in the keypoint detection task;                                                                                                                                                    | int           |
| kp_dim            | Keypoint Dimension                | The dimension of keypoints in the keypoint detection task, only supports 2 and 3, determined by the trained model;                                                                                        | int【2/3】    |
| max_boxes_num     | Maximum Number of Detection Boxes | The maximum number of detection boxes allowed to be returned in one frame;                                                                                                                                | int           |
| debug_mode        | Debug Mode                        | Whether the timing function is effective, optional values 0/1, 0 means no timing, 1 means timing;                                                                                                         | int【0/1】    |

#### Deploy Model for Image Inference

For image inference, please refer to the following code, **modify the parameter variables defined in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own test image, model path, label name, and model input size for custom scenarios
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
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

#### Deploy Model for Video Inference

For video inference, please refer to the following code, **modify the parameter variables defined in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own model path, label name, and model input size for custom scenarios
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] if specified
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    nms_threshold=0.45
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
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

## YOLO11 Fruit Segmentation

### YOLO11 Source Code and Training Environment Setup

For `YOLO11` training environment setup, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolo11`. Please download the provided sample dataset. The sample dataset includes classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenarios. Extract the dataset to the `yolo11` directory, and use `fruits_seg` as the dataset for the fruit segmentation task. The sample dataset also includes a rotated object detection dataset `yolo_pen_obb` for desktop pen scenarios, and a license plate keypoint detection dataset `car_plate`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert the annotated data into the training data format officially supported by `yolo11` for subsequent training.

```shell
cd yolo11
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLO11 to Train the Fruit Segmentation Model

Execute the following command in the `yolo11` directory to train a segmentation model for three types of fruits using `yolo11`:

```shell
yolo segment train data=datasets/fruits_seg.yaml model=yolo11n-seg.pt epochs=100 imgsz=320
```

### Converting the Fruit Segmentation kmodel

Model conversion requires the following libraries to be installed in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7 to be installed
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: Please install dotnet-7 yourself and add environment variables. nncase can be installed online using pip, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, the other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, and extract the model conversion script tool `test_yolo11.zip` to the `yolo11` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

Follow the commands below to first export the `pt` model under `runs/segment/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please choose the pt model path yourself
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/segment
# Convert kmodel, please choose the onnx model path yourself. The generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset ../calibration_data --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Notes                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Options are k230/CPU, corresponding to k230 chip;                              | str   |
| model        | Model Path | The path of the ONNX model to be converted;                                        | str   |
| dataset      | Calibration Image Set  | Image data used during model conversion, used during the quantization stage                    | str   |
| input_width  | Input Width | The width of the model input                                             | int   |
| input_height | Input Height | The height of the model input                                             | int   |
| ptq_option   | Quantization Method | The quantization strategies are `Kld` and `NoClip`, which combine the quantization precision of data and weights. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Dalily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or use the latest code to compile the firmware yourself. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write code in the IDE and run it.

#### Model File Copy

Connect the IDE, and copy the converted model and test images to the path `CanMV/data` directory. This path can be customized, you just need to modify the corresponding path when writing code.

#### YOLO11 Module

The `YOLO11` class integrates the five tasks of `YOLO11`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the kmodel inference process of `YOLO11`.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name         | Description           | Notes                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports four types of tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference Mode       | Supports two inference modes, options are 'image'/'video'. 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | The kmodel path copied to the development board;                                   | str          |
| labels           | Class Label List   | Label names for different classes;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | The resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | The input resolution when training the YOLO11 model, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | The class confidence threshold for classification tasks, and the object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh       | nms Threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float【0~1】 |
| mask_thresh      | Mask Threshold       | The binarization threshold when segmenting the objects in the detection box in the segmentation task;             | float【0~1】 |
| kp_num           | Number of Keypoints     | The number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint Dimension     | The dimension of keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model;    | int【2/3】  |
| max_boxes_num    | Maximum Number of Detection Boxes   | The maximum number of detection boxes allowed to be returned in one frame of image;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function takes effect, options 0/1, 0 is no timing, 1 is timing;            | int【0/1】   |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code, **modify the definition parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. Please modify to your own test image, model path, label name, and model input size for custom scenarios
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code, **modify the definition variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. Please modify to your own model path, label name, and model input size for custom scenarios
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc. For values, see the PipeLine manual
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="segment",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
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

## YOLO11 Rotated Object Detection

### YOLO11 Source Code and Training Environment Setup

For `YOLO11` training environment setup, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolo11`, please download the provided example dataset. The example dataset includes a rotated object detection dataset with a single-class rotated pen detection (pen) scenario. Unzip the dataset to the `yolo11` directory, please use `yolo_pen_obb` as the dataset for the rotated object detection task.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert the annotated data into the training data format officially supported by `yolo11` for subsequent training.

```shell
cd yolo11
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using the YOLO11 Rotated Object Detection Model

Execute the following command in the `yolo11` directory to use `yolo11` to train a single-class rotated object detection model:

```shell
yolo obb train data=datasets/pen_obb.yaml model=yolo11n-obb.pt epochs=100 imgsz=320
```

### Converting Rotated Object Detection kmodel

The following libraries need to be installed in the training environment for model conversion:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires installing dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: please install dotnet-7 yourself and add environment variables. Online pip installation of nncase is supported, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip install in the directory where nncase_kpu-2.*-py2.py3-none-win_amd64.whl is downloaded
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, and unzip the model conversion script tool `test_yolo11.zip` to the `yolo11` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

According to the following command, first export the `pt` model under `runs/obb/train/weights` to the `onnx` model, then convert it to the `kmodel` model:

```shell
# Export onnx, please select the pt model path yourself
yolo export model=runs/obb/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/obb
# Convert kmodel, please select the onnx model path yourself, the generated kmodel is in the same level directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/obb/train/weights/best.onnx --dataset ../calibration_obb --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Notes                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Options are k230/CPU, corresponding to k230 chip;                              | str   |
| model        | Model Path | The ONNX model path to be converted;                                        | str   |
| dataset      | Calibration Image Set  | Image data used during model conversion, used in the quantization phase                    | str   |
| input_width  | Input Width | The width of the model input                                             | int   |
| input_height | Input Height | The height of the model input                                             | int   |
| ptq_option   | Quantization Method | Quantization strategies are `Kld` and `NoClip`, combining the quantization precision of data and weights. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying Models on k230 Using MicroPython

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or use the latest code to compile the firmware yourself. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE, and copy the converted model and test images to the path `CanMV/data` directory. This path can be customized, you only need to modify the corresponding path when writing code.

#### YOLO11 Module

The `YOLO11` class integrates the four tasks of `YOLO11`, including classify, detect, segment, and obb (rotated object detection); it supports two inference modes, including image and video; this class encapsulates the kmodel inference process of `YOLO11`.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name         | Description           | Notes                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports four types of tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference Mode       | Supports two inference modes, options are 'image'/'video'. 'image' means inferring an image, 'video' means inferring a real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | The kmodel path copied to the development board;                                   | str          |
| labels           | Category Label List   | The label names of different categories;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | The resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | The input resolution during YOLO11 model training, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | The category confidence threshold for classification tasks, the object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| nms_thresh       | nms Threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                       | float【0~1】 |
| mask_thresh      | mask Threshold       | The binarization threshold for segmenting the object in the detection box in the segmentation task;             | float【0~1】 |
| kp_num           | Number of Key Points     | The number of key points in the key point detection task;                              | int        |
| kp_dim           | Key Point Dimension     | The dimension of key points in the key point detection task, only 2 and 3 are supported, determined by the training model;    | int【2/3】  |
| max_boxes_num    | Maximum Number of Detection Boxes   | The maximum number of detection boxes allowed to be returned in one frame of image;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function takes effect, options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code, **modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own test image, model path, label name, and model input size for custom scenarios
    img_path="/data/test_obb.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    confidence_threshold = 0.1
    nms_threshold=0.6
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="obb",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code, **modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.Utils import *
from libs.YOLO import YOLO11
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own model path, label name, and model input size for custom scenarios
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; specify [width, height] when needed
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.1
    nms_threshold=0.6
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLO11 instance
    yolo=YOLO11(task_type="obb",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            # Inference frame by frame
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

## YOLO11 License Plate Corner Detection

### YOLO11 Source Code and Training Environment Setup

For YOLO11 training environment setup, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolo11`. Please download the provided example dataset, which contains datasets for license plate detection four-corner keypoint scenarios. Extract the dataset to the `yolo11` directory, and use `car_plate` as the dataset for the keypoint detection task.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert the annotated data into the training data format officially supported by `yolo11` for subsequent training.

```shell
cd yolo11
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLO11 to Train Keypoint Detection Model

Execute the command in the `yolo11` directory to train a single-class rotated object detection model using `yolo11`:

```shell
yolo pose train data=datasets/car_plate.yaml model=yolo11n-pose.pt epochs=100 imgsz=320
```

### Convert Keypoint Detection kmodel

The model conversion requires installing the following libraries in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7 to be installed
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: Please install dotnet-7 by yourself and add environment variables. Online installation of nncase via pip is supported, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip to install in the directory where nncase_kpu-2.*-py2.py3-none-win_amd64.whl is downloaded
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool and extract the model conversion script tool `test_yolo11.zip` to the `yolo11` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

According to the following command, first export the `pt` model under `runs/pose/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the pt model path yourself
yolo export model=runs/pose/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/pose
# Convert kmodel, please select the onnx model path yourself. The generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/pose/train/weights/best.onnx --dataset ../calibration_pose --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description  | Description                                                         | Type  |
| -------------- | ------------ | ------------------------------------------------------------------- | ----- |
| target         | Target Platform | Options are k230/CPU, corresponding to k230 chip;                 | str   |
| model          | Model Path   | The path of the ONNX model to be converted;                        | str   |
| dataset        | Calibration Image Set | Image data used during model conversion, used in the quantization phase | str   |
| input_width    | Input Width  | Width of the model input                                           | int   |
| input_height   | Input Height | Height of the model input                                          | int   |
| ptq_option     | Quantization Method | Quantization strategies are `Kld` and `NoClip`, combining data and weights quantization precision. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying Model on k230 Using MicroPython

#### Flash Image and Install CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Dalily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or use the latest code to compile the firmware yourself. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE, copy the converted model and test images to the path `CanMV/data` directory. This path can be customized, just modify the corresponding path when writing code.

#### YOLO11 Module

The `YOLO11` class integrates five tasks of `YOLO11`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the kmodel inference process of `YOLO11`.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name    | Description          | Description                                                                                                              | Type        |
| ----------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------ | ----------- |
| task_type         | Task Type            | Supports four types of tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';                                    | str         |
| mode              | Inference Mode       | Supports two inference modes, options are 'image'/'video'. 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera; | str         |
| kmodel_path       | kmodel Path          | The kmodel path copied to the development board;                                                                          | str         |
| labels            | Category Label List  | The label names of different categories;                                                                                  | list[str]   |
| rgb888p_size      | Inference Frame Resolution | The resolution of the current frame for inference, such as [1920,1080], [1280,720], [640,640];                  | list[int]   |
| model_input_size  | Model Input Resolution | The input resolution when training the YOLO11 model, such as [224,224], [320,320], [640,640];                       | list[int]   |
| display_size      | Display Resolution   | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]);                                    | list[int]   |
| conf_thresh       | Confidence Threshold | The category confidence threshold for classification tasks, and the object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】|
| nms_thresh        | nms Threshold        | Non-maximum suppression threshold, required for detection and segmentation tasks;                                         | float【0~1】|
| mask_thresh       | mask Threshold       | The binarization threshold for segmenting objects in the detection box in segmentation tasks;                            | float【0~1】|
| kp_num            | Number of Keypoints  | The number of keypoints in the keypoint detection task;                                                                  | int         |
| kp_dim            | Keypoint Dimension   | The dimension of keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model;   | int【2/3】  |
| max_boxes_num     | Maximum Detection Boxes | The maximum number of detection boxes allowed to be returned in one frame of image;                                  | int         |
| debug_mode        | Debug Mode           | Whether the timing function takes effect, options are 0/1, 0 means no timing, 1 means timing;                            | int【0/1】  |

#### Deploying Model for Image Inference

For image inference, please refer to the following code, **modify the definition parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is just an example. For custom scenarios, please modify it to your own test image, model path, label name, model input size, number of keypoints, and keypoint dimension
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ['plate']
    model_input_size=[320,320]
    kp_num=4
    kp_dim=2

    confidence_threshold = 0.5
    nms_threshold=0.45
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize YOLO11 model
    yolo=YOLO11(task_type="pose",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,kp_num=kp_num,kp_dim=kp_dim,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()

```

#### Deploying Model for Video Inference

For video inference, please refer to the following code, **modify the definition variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is just an example. For custom scenarios, please modify it to your own model path, label name, model input size, number of keypoints, and keypoint dimension
    kmodel_path="/data/best.kmodel"
    labels = ["plate"]
    model_input_size=[320,320]
    kp_num=4
    kp_dim=2

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize YOLO11 model
    yolo=YOLO11(task_type="pose",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,kp_num=kp_num,kp_dim=kp_dim,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
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

## YOLO26 Fruit Classification

### YOLO26 Source Code and Training Environment Setup

YOLO26 is the latest generation real-time object detection model released by Ultralytics, featuring a series of fundamental architectural innovations that enable end-to-end NMS-free inference, aiming to provide more powerful and easier-to-deploy solutions for edge computing and low-power devices.

For setting up the `YOLO26` training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolo26`. Please download the provided sample dataset. The sample dataset contains classification, detection, and segmentation datasets for three categories of fruits (apple, banana, orange) as scenarios. Extract the dataset into the `yolo26` directory. Please use `fruits_cls` as the dataset for the fruit classification task. The sample dataset also includes a rotated object detection desktop pen scenario dataset `yolo_pen_obb` and a license plate keypoint detection dataset `car_plate`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. The classification task data does not need to be annotated using tools, just divide the directories according to the format. Convert the annotated data into the `yolo26` officially supported training data format for subsequent training.

```shell
cd yolo11
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLO26 to Train the Fruit Classification Model

Execute the command in the `yolo26` directory to train a three-category fruit classification model using `yolo26`:

```shell
yolo classify train data=datasets/fruits_cls model=yolo26n-cls.pt epochs=100 imgsz=224
```

### Converting the Fruit Classification kmodel

The model conversion requires the following libraries to be installed in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires installing dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: Please install dotnet-7 yourself and add environment variables. Online installation of nncase via pip is supported, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool and extract the model conversion script tool `test_yolo26.zip` into the `yolo26` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo26.zip
unzip test_yolo26.zip
```

According to the following commands, first export the `pt` model under `runs/classify/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please choose the pt model path yourself
yolo export model=runs/classify/train/weights/best.pt format=onnx imgsz=224
cd test_yolo26/classify
# Convert kmodel, please choose the onnx model path yourself, the generated kmodel will be in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/classify/train/weights/best.onnx --dataset ../calibration_data --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Explanation | Type |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target platform | The options are k230/CPU, corresponding to the k230 chip;                              | str   |
| model        | Model path | The path of the ONNX model to be converted;                                        | str   |
| dataset      | Calibration image set  | The image data used during model conversion, used in the quantization phase                    | str   |
| input_width  | Input width | The width of the model input                                             | int   |
| input_height | Input height | The height of the model input                                             | int   |
| ptq_option   | Quantization method | The quantization strategies are `Kld` and `NoClip`, combining the quantization precision of data and weights. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flash Image and Install CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that the **latest features** are supported! Or use the latest code to compile the firmware yourself. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)). Write and run code in the IDE.

#### Model File Copying

Connect the IDE and copy the converted model and test images to the path `CanMV/data`. This path can be customized; you only need to modify the corresponding path when writing the code.

#### YOLO26 Module

The `YOLO26` class integrates five tasks of `YOLO26`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image and video stream; this class encapsulates the kmodel inference workflow of `YOLO26`.

- **Import Method**

```python
from libs.YOLO import YOLO26
```

- **Parameter Description**

| Parameter Name        | Description           | Explanation                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task type       | Supports five tasks, the options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference mode       | Supports two inference modes, the options are 'image'/'video'. 'image' means inferring images, and 'video' means inferring the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel path     | The kmodel path copied to the development board;                                   | str          |
| labels           | Category label list   | The label names of different categories;                                         | list[str]    |
| rgb888p_size     | Inference frame resolution   | The resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model input resolution | The input resolution when training the YOLO26 model, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display resolution     | Set when the inference mode is 'video', supports hdmi ([1920,1080]) and lcd ([800,480]); | list[int]    |
| conf_thresh      | Confidence threshold     | The category confidence threshold for classification tasks, and the object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| mask_thresh      | mask threshold       | The binarization threshold for segmenting objects in the detection box in the segmentation task;             | float【0~1】 |
| kp_num           | Number of keypoints     | The number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint dimension     | The dimension of keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model;    | int【2/3】  |
| max_boxes_num    | Maximum number of detection boxes   | The maximum number of detection boxes allowed to be returned in one frame of image;                         | int          |
| debug_mode       | Debug mode       | Whether the timing function is effective, the options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code, **modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is just an example. For custom scenarios, please modify it to your own test image, model path, label names, and model input size
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLO26 model
    yolo=YOLO26(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code, **modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is just an example. For custom scenarios, please modify it to your own model path, label names, and model input size
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc. For values, see the PipeLine manual
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.8
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLO26 model
    yolo=YOLO26(task_type="classify",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            # Frame by frame inference
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

## YOLO26 Fruit Detection

### YOLO11 Source Code and Training Environment Setup

YOLO26 is the latest generation real-time object detection model released by Ultralytics. It has undergone a series of fundamental architectural innovations and achieves end-to-end NMS-free inference, aiming to provide more powerful and easier-to-deploy solutions for edge computing and low-power devices.

For the `YOLO26` training environment setup, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolo26`. Please download the provided sample dataset. The sample dataset includes scenario data for three categories of fruits (apple, banana, orange), providing classification, detection, and segmentation datasets respectively. Extract the dataset to the `yolo26` directory. Please use `fruits_yolo` as the dataset for the fruit detection task. The sample dataset also includes a rotated object detection desktop pen scenario dataset `yolo_pen_obb`, and a license plate keypoint detection dataset `car_plate`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert the annotated data to the training data format officially supported by `yolo26` for subsequent training.

```shell
cd yolo26
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLO26 to Train the Fruit Detection Model

Execute the command in the `yolo26` directory to train the three-category fruit detection model using `yolo26`:

```shell
yolo detect train data=datasets/fruits_yolo.yaml model=yolo26n.pt epochs=300 imgsz=320
```

### Converting Fruit Detection kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7 to be installed
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: Please install dotnet-7 by yourself and add environment variables. Online installation of nncase via pip is supported, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment and use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, and extract the model conversion script tool `test_yolo26.zip` to the `yolo26` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo26.zip
unzip test_yolo26.zip
```

According to the following commands, first export the `pt` model under `runs/detect/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the pt model path by yourself
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolo26/detect
# Convert kmodel, please select the onnx model path by yourself. The generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset ../calibration_data --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model conversion script (to_kmodel.py) parameter description**:

| Parameter Name | Description | Explanation | Type |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target platform | Options are k230/CPU, corresponding to the k230 chip;                              | str   |
| model        | Model path | Path to the ONNX model to be converted;                                        | str   |
| dataset      | Calibration image set  | Image data used during model conversion, used in the quantization phase                    | str   |
| input_width  | Input width | Width of the model input                                             | int   |
| input_height | Input height | Height of the model input                                             | int   |
| ptq_option   | Quantization method | Quantization strategies are `Kld` and `NoClip`, combined with the quantization precision of data and weights, 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flashing Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Dalily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or use the latest code to compile the firmware yourself. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write code in the IDE and run it.

#### Model File Copy

Connect the IDE and copy the converted model and test images to the path `CanMV/data` directory. This path can be customized; you only need to modify the corresponding path when writing the code.

#### YOLO26 Module

The `YOLO26` class integrates the five tasks of `YOLO26`, including classification (classify), detection (detect), segmentation (segment), rotated object detection, and keypoint detection (pose); it supports two inference modes, including image and video stream (video); this class encapsulates the kmodel inference process of `YOLO26`.

- **Import Method**

```python
from libs.YOLO import YOLO26
```

- **Parameter Description**

| Parameter Name         | Description           | Explanation                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task type       | Supports four tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference mode       | Supports two inference modes, options are 'image'/'video', 'image' means inferring an image, 'video' means inferring the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel path     | Path of the kmodel copied to the development board;                                   | str          |
| labels           | Category label list   | Label names for different categories;                                         | list[str]    |
| rgb888p_size     | Inference frame resolution   | Resolution of the current frame for inference, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model input resolution | Input resolution during YOLO26 model training, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence threshold     | Category confidence threshold for classification tasks, object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| mask_thresh      | mask threshold       | Binarization threshold for segmenting objects in the detection box during the segmentation task;             | float【0~1】 |
| kp_num           | Number of keypoints     | Number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint dimension     | Dimension of keypoints in the keypoint detection task, only supports 2 and 3, determined by the trained model;    | int【2/3】  |
| max_boxes_num    | Maximum number of detection boxes   | Maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| debug_mode       | Debug mode       | Whether the timing function takes effect, options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying Model for Image Inference

For image inference, please refer to the code below, **modify the definition parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify to your own test image, model path, label names, and model input size for custom scenarios
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize YOLO26 model
    yolo=YOLO26(task_type="detect",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    print(res)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying Model for Video Inference

For video inference, please refer to the code below, **modify the definition variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify to your own model path, label names, and model input size for custom scenarios
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize YOLO26 model
    yolo=YOLO26(task_type="detect",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,max_boxes_num=50,debug_mode=0)
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

## YOLO26 Fruit Segmentation

### YOLO26 Source Code and Training Environment Setup

YOLO26 is the latest generation of real-time object detection models released by Ultralytics. It incorporates a series of fundamental architectural innovations and achieves end-to-end NMS-free inference, aiming to provide more powerful and easier-to-deploy solutions for edge computing and low-power devices.

For the `YOLO26` training environment setup, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please skip this step.

### Training Data Preparation

You can first create a new folder `yolo26`. Please download the provided example dataset. The example dataset contains three types of fruit (apple, banana, orange) scenarios and provides classification, detection, and segmentation datasets respectively. Unzip the dataset into the `yolo26` directory. Please use `fruits_seg` as the dataset for the fruit segmentation task. The example dataset also contains a rotated object detection desktop pen scenario dataset `yolo_pen_obb` and a license plate keypoint detection dataset `car_plate`.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert the annotated data into the training data format officially supported by `yolo26` for subsequent training.

```shell
cd yolo26
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please skip this step.

### Using YOLO26 to Train the Fruit Segmentation Model

Execute the following command in the `yolo26` directory to use `yolo26` to train a three-class fruit segmentation model:

```shell
yolo segment train data=datasets/fruits_seg.yaml model=yolo26n-seg.pt epochs=100 imgsz=320
```

### Converting the Fruit Segmentation kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: Please install dotnet-7 by yourself and add environment variables. nncase supports online installation via pip, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip to install in the directory where nncase_kpu-2.*-py2.py3-none-win_amd64.whl is downloaded
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# Besides nncase and nncase-kpu, the script also uses the following libraries:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, and unzip the model conversion script tool `test_yolo26.zip` into the `yolo26` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo26.zip
unzip test_yolo26.zip
```

According to the following commands, first export the `pt` model under `runs/segment/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please choose the pt model path yourself
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolo26/segment
# Convert kmodel, please choose the onnx model path yourself. The generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset ../calibration_data --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Instructions                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Options are k230/CPU, corresponding to k230 chip;                              | str   |
| model        | Model Path | Path of the ONNX model to be converted;                                        | str   |
| dataset      | Calibration Image Set | Image data used in model conversion, used in the quantization stage                    | str   |
| input_width  | Input Width | The width of the model input                                             | int   |
| input_height | Input Height | The height of the model input                                             | int   |
| ptq_option   | Quantization Method | The quantization strategy is `Kld` and `NoClip`, combining the quantization precision of data and weights, 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Dalily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that the **latest features** are supported! Or compile the firmware yourself using the latest code. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run the code in the IDE.

#### Model File Copy

Connect the IDE, and copy the converted model and test images to the path `CanMV/data`. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### YOLO26 Module

The `YOLO26` class integrates the five tasks of `YOLO26`, including classification (classify), detection (detect), segmentation (segment), rotated object detection (obb), and keypoint detection (pose); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the kmodel inference process of `YOLO26`.

- **Import Method**

```python
from libs.YOLO import YOLO26
```

- **Parameter Description**

| Parameter Name         | Description           | Instructions                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports four tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference Mode       | Supports two inference modes, options are 'image'/'video', 'image' means inferring on an image, 'video' means inferring on the real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | Path of the kmodel copied to the development board;                                   | str          |
| labels           | Class Label List   | Label names for different classes;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | The resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | The input resolution during YOLO26 model training, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | The class confidence threshold for classification tasks, and the object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| mask_thresh      | mask Threshold       | The binarization threshold when segmenting objects in the detection box in the segmentation task;             | float【0~1】 |
| kp_num           | Number of Keypoints     | The number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint Dimension     | The dimension of the keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the training model;    | int【2/3】  |
| max_boxes_num    | Maximum Number of Detection Boxes   | The maximum number of detection boxes allowed to be returned in one frame of image;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function is effective, options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model to Implement Image Inference

For image inference, please refer to the following code, **modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own test image, model path, label name, and model input size for custom scenarios
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    mask_threshold=0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLO26 model
    yolo=YOLO26(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model to Implement Video Inference

For video inference, please refer to the following code, **modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example, please modify it to your own model path, label name, and model input size for custom scenarios
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; it can also be explicitly specified as hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    mask_threshold=0.5
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize the YOLO26 model
    yolo=YOLO26(task_type="segment",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
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

## YOLO26 Rotated Object Detection

### YOLO26 Source Code and Training Environment Setup

YOLO26 is the latest generation real-time object detection model released by Ultralytics. It has undergone a series of fundamental architectural innovations, achieving end-to-end NMS-free inference, aiming to provide more powerful and easier-to-deploy solutions for edge computing and low-power devices.

For setting up the `YOLO26` training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please skip this step.

### Training Data Preparation

You can first create a new folder `yolo26`. Please download the provided sample dataset. The sample dataset includes a single-class rotated pen detection (pen) scenario and provides a rotated object detection dataset respectively. Extract the dataset to the `yolo26` directory, and please use `yolo_pen_obb` as the dataset for the rotated object detection task.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert the annotated data into the training data format officially supported by `yolo26` for subsequent training.

```shell
cd yolo26
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please skip this step.

### Using the YOLO26 Rotated Object Detection Model

Execute the command in the `yolo26` directory to train a single-class rotated object detection model using `yolo26`:

```shell
yolo obb train data=datasets/pen_obb.yaml model=yolo26n-obb.pt epochs=100 imgsz=320
```

### Converting Rotated Object Detection kmodel

Model conversion requires the following libraries to be installed in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires dotnet-7 to be installed
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: please install dotnet-7 yourself and add environment variables. Online installation of nncase via pip is supported, but the nncase-kpu library needs to be installed offline. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl from https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, and use pip to install in the directory where nncase_kpu-2.*-py2.py3-none-win_amd64.whl is downloaded
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, and extract the model conversion script tool `test_yolo26.zip` to the `yolo26` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo26.zip
unzip test_yolo26.zip
```

Follow the commands below to first export the `pt` model under `runs/obb/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the pt model path yourself
yolo export model=runs/obb/train/weights/best.pt format=onnx imgsz=320
cd test_yolo26/obb
# Convert kmodel, please select the onnx model path yourself. The generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/obb/train/weights/best.onnx --dataset ../calibration_obb --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Explanation                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target platform | Options are k230/CPU, corresponding to k230 chip;                              | str   |
| model        | Model path | Path of the ONNX model to be converted;                                        | str   |
| dataset      | Calibration image set  | Image data used during model conversion, used in the quantization phase                    | str   |
| input_width  | Input width | Width of the model input                                             | int   |
| input_height | Input height | Height of the model input                                             | int   |
| ptq_option   | Quantization method | Quantization strategies are `Kld` and `NoClip`, combining quantization precision of data and weights. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model on k230 Using MicroPython

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Dalily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Alternatively, you can use the latest code to compile the firmware yourself. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE, and copy the converted model and test images to the path `CanMV/data`. This path can be customized, you only need to modify the corresponding path when writing code.

#### YOLO26 Module

The `YOLO26` class integrates four tasks of `YOLO26`, including classification (classify), detection (detect), segmentation (segment), and rotated object detection (obb); it supports two inference modes, including image and video stream (video); this class encapsulates the kmodel inference process of `YOLO26`.

- **Import Method**

```python
from libs.YOLO import YOLO26
```

- **Parameter Description**

| Parameter Name         | Description           | Explanation                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task type       | Supports four types of tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference mode       | Supports two inference modes, options are 'image'/'video'. 'image' means inferring on an image, 'video' means inferring on a real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel path     | Path of the kmodel copied to the development board;                                   | str          |
| labels           | Class label list   | Label names of different classes;                                         | list[str]    |
| rgb888p_size     | Inference frame resolution   | Resolution of the current inference frame, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model input resolution | Input resolution during YOLOv8 model training, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence threshold     | Class confidence threshold for classification tasks, target confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| mask_thresh      | mask threshold       | Binarization threshold for segmenting the object in the detection box in segmentation tasks;             | float【0~1】 |
| kp_num           | Number of keypoints     | Number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint dimension     | Dimension of keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model;    | int【2/3】  |
| max_boxes_num    | Maximum number of detection boxes   | Maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| debug_mode       | Debug mode       | Whether the timing function takes effect, options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model for Image Inference

For image inference, please refer to the following code, **modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify it to your own test image, model path, label names, and model input size
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    confidence_threshold = 0.1
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize YOLO26 model
    yolo=YOLO26(task_type="obb",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the following code, **modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify it to your own model path, label names, and model input size
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; fill in [width, height] when specifying
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.1
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # Get the actual display resolution after create
    display_size=pl.get_display_size()
    # Initialize YOLO26 model
    yolo=YOLO26(task_type="obb",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,max_boxes_num=50,debug_mode=0)
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

## YOLO26 License Plate Corner Point Detection

### YOLO26 Source Code and Training Environment Setup

YOLO26 is the latest generation of real-time object detection models released by Ultralytics. It has undergone a series of fundamental architectural innovations, achieving end-to-end NMS-free inference, aiming to provide more powerful and easily deployable solutions for edge computing and low-power devices.

For setting up the `YOLO26` training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, please ignore this step.

### Training Data Preparation

You can first create a new folder `yolo26`, please download the provided sample dataset. The sample dataset contains datasets for the scenario of detecting four corner keypoints of license plates. Extract the dataset to the `yolo26` directory, and please use `car_plate` as the dataset for the keypoint detection task.

If you want to use your own dataset for training, you can download [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) to complete the annotation. Convert the annotated data into the training data format officially supported by `yolo26` for subsequent training.

```shell
cd yolo26
wget https://download.kendryte.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, please ignore this step.

### Using YOLO26 to Train the Keypoint Detection Model

Execute the command in the `yolo26` directory to use `yolo26` to train a single-class rotated object detection model:

```shell
yolo pose train data=datasets/car_plate.yaml model=yolo26n-pose.pt epochs=100 imgsz=320
```

### Converting the Keypoint Detection kmodel

Model conversion requires installing the following libraries in the training environment:

```Shell
# linux platform: nncase and nncase-kpu can be installed online, nncase-2.x requires installing dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows platform: please install dotnet-7 by yourself and add environment variables. pip online installation of nncase is supported, but the nncase-kpu library requires offline installation. Download nncase_kpu-2.*-py2.py3-none-win_amd64.whl at https://github.com/kendryte/nncase/releases
# Enter the corresponding python environment, use pip to install in the download directory of nncase_kpu-2.*-py2.py3-none-win_amd64.whl
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# In addition to nncase and nncase-kpu, other libraries used by the script include:
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

Download the script tool, extract the model conversion script tool `test_yolo26.zip` to the `yolo26` directory;

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo26.zip
unzip test_yolo26.zip
```

Follow the commands below to first export the `pt` model under `runs/pose/train/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please choose the pt model path yourself
yolo export model=runs/pose/train/weights/best.pt format=onnx imgsz=320
cd test_yolo26/pose
# Convert kmodel, please choose the onnx model path yourself, the generated kmodel is in the same directory as the onnx model
python to_kmodel.py --target k230 --model ../../runs/pose/train/weights/best.onnx --dataset ../calibration_pose --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **Model Conversion Script (to_kmodel.py) Parameter Description**:

| Parameter Name | Description | Notes                                                         | Type  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | Target Platform | Options are k230/CPU, corresponding to the k230 chip;                              | str   |
| model        | Model Path | Path to the ONNX model to be converted;                                        | str   |
| dataset      | Calibration Image Set | Image data used during model conversion, used in the quantization phase                    | str   |
| input_width  | Input Width | Width of the model input                                             | int   |
| input_height | Input Height | Height of the model input                                             | int   |
| ptq_option   | Quantization Method | Quantization strategies are `Kld` and `NoClip`, combining data and weights quantization accuracy. 0 is `NoClip`+[uint8,uint8], 1 is `NoClip`+[uint8,int16], 2 is `NoClip`+[int16,uint8], 3 is `Kld`+[uint8,uint8], 4 is `Kld`+[uint8,int16], 5 is `Kld`+[int16,uint8] | 0/1/2/3/4/5 |

### Deploying the Model Using MicroPython on k230

#### Flashing the Image and Installing CanMV IDE

💡 **Firmware Introduction**: Please download the latest [Daily Build firmware](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) according to your development board type to ensure that **the latest features** are supported! Or use the latest code to compile the firmware yourself, see the tutorial: [Firmware Compilation](../../userguide/how_to_build.md).

Download and install CanMV IDE (Download link: [CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230)), write and run code in the IDE.

#### Model File Copy

Connect the IDE, copy the converted model and test images to the path `CanMV/data` directory. This path can be customized; you only need to modify the corresponding path when writing the code.

#### YOLO26 Module

The `YOLO26` class integrates the five tasks of `YOLO26`, including classify, detect, segment, oriented object detection (obb), and keypoint detection (pose); it supports two inference modes, including image and video stream; this class encapsulates the `YOLO26` kmodel inference process.

- **Import Method**

```python
from libs.YOLO import YOLO26
```

- **Parameter Description**

| Parameter Name         | Description           | Notes                                                         | Type         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | Task Type       | Supports four types of tasks, options are 'classify'/'detect'/'segment'/'obb'/'pose';        | str          |
| mode             | Inference Mode       | Supports two inference modes, options are 'image'/'video'. 'image' means inference on an image, 'video' means inference on a real-time video stream captured by the camera; | str          |
| kmodel_path      | kmodel Path     | Path to the kmodel copied to the development board;                                   | str          |
| labels           | Class Label List   | Label names for different classes;                                         | list[str]    |
| rgb888p_size     | Inference Frame Resolution   | Resolution of the current frame being inferred, such as [1920,1080], [1280,720], [640,640];      | list[int]    |
| model_input_size | Model Input Resolution | Input resolution when training the YOLO11 model, such as [224,224], [320,320], [640,640]; | list[int]    |
| display_size     | Display Resolution     | Set when the inference mode is 'video', supports hdmi([1920,1080]) and lcd([800,480]); | list[int]    |
| conf_thresh      | Confidence Threshold     | Class confidence threshold for classification tasks, object confidence threshold for detection and segmentation tasks, such as 0.5; | float【0~1】 |
| mask_thresh      | Mask Threshold       | Binarization threshold for segmenting objects within detection boxes in segmentation tasks;             | float【0~1】 |
| kp_num           | Number of Keypoints     | Number of keypoints in the keypoint detection task;                              | int        |
| kp_dim           | Keypoint Dimension     | Dimension of keypoints in the keypoint detection task, only 2 and 3 are supported, determined by the trained model;    | int【2/3】  |
| max_boxes_num    | Maximum Number of Detection Boxes   | Maximum number of detection boxes allowed to be returned in one frame;                         | int          |
| debug_mode       | Debug Mode       | Whether the timing function is enabled, options are 0/1, 0 means no timing, 1 means timing;            | int【0/1】   |

#### Deploying the Model for Image Inference

For image inference, please refer to the code below, **modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify to your own test image, model path, label name, model input size, number of keypoints and keypoint dimension
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ['plate']
    model_input_size=[320,320]
    kp_num=4
    kp_dim=2

    confidence_threshold = 0.5
    nms_threshold=0.45
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize YOLO26 model
    yolo=YOLO26(task_type="pose",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,kp_num=kp_num,kp_dim=kp_dim,conf_thresh=confidence_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    print(res)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### Deploying the Model for Video Inference

For video inference, please refer to the code below, **modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO26
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify to your own model path, label name, model input size, number of keypoints and keypoint dimension
    kmodel_path="/data/best.kmodel"
    labels = ["plate"]
    model_input_size=[320,320]
    kp_num=4
    kp_dim=2           

    # Display mode, "auto" automatically selects the screen driver according to the development board model; you can also explicitly specify hdmi/lcd/st7701, etc., see the PipeLine manual for values
    display_mode="auto"
    # None means using the default resolution of the screen driver; specify [width, height] when needed
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

## YOLO Keypoint Detection

`YOLOv8`, `YOLO11`, and `YOLO26` all support the keypoint detection (pose) task, while `YOLOv5` does not. Keypoint detection, based on detection boxes, additionally outputs the coordinates of several predefined positions on each target. A typical application is human body skeleton keypoints (COCO format with 17 points).

### Training and Model Conversion

The training environment, data preparation, and model conversion workflow for keypoint detection are **exactly the same** as the previous detection and segmentation tasks, except that the dataset annotation format is changed to the keypoint format, and the `task` in the training command is changed to `pose`. Please refer to the "Source Code and Training Environment Setup", "Training Data Preparation", and "Converting kmodel" sections of the corresponding version chapter (such as [YOLO11 Fruit Detection](#yolo11-fruit-detection)), and replace the task type with `pose`.

After model conversion, you can use `test_pose_onnx.py` and `test_pose_kmodel.py` to verify the effect, see [kmodel Conversion Verification](#kmodel-verification).

### Deploying the Model Using MicroPython on k230

Keypoint detection has two more parameters than other tasks:

| Parameter | Description |
|------|------|
| `kp_num` | Number of keypoints for each target, determined by the trained model. Generally 17 for human pose |
| `kp_dim` | Keypoint dimension, only 2 and 3 are supported. When it is 3, the third value is the visibility score of the keypoint, determined by the trained model |

**Single Image Inference:**

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify to your own test image, model path, label name, model input size, number of keypoints and keypoint dimension
    img_path="/sdcard/examples/utils/test_pose.jpg"
    kmodel_path="/sdcard/examples/kmodel/yolo11n-pose.kmodel"
    labels = ['person']
    model_input_size=[320,320]
    kp_num=17
    kp_dim=3

    confidence_threshold = 0.5
    nms_threshold=0.45
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize YOLO11 instance, task_type is pose
    yolo=YOLO11(task_type="pose",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,kp_num=kp_num,kp_dim=kp_dim,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

**Video Stream Inference:**

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # This is only an example. For custom scenarios, please modify to your own model path, label name, model input size, number of keypoints and keypoint dimension
    kmodel_path="/sdcard/examples/kmodel/yolo11n-pose.kmodel"
    labels = ["person"]
    model_input_size=[320,320]
    kp_num=17
    kp_dim=3

    # auto selects the default driver according to the development board; you can manually override it to hdmi/lcd/st7701 etc.
    display_mode="auto"
    # None uses the SDK default resolution; specify [640, 480] etc. when changing screens
    display_size=None
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    display_size=pl.get_display_size()
    # Initialize YOLO11 instance
    yolo=YOLO11(task_type="pose",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,kp_num=kp_num,kp_dim=kp_dim,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
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

The above code corresponds to `20-YOLO-Module-Examples/yolo11_pose_image.py` and `yolo11_pose_video.py` on the development board. Replace `YOLO11` with `YOLOv8` or `YOLO26`, and replace the model path with the corresponding kmodel to switch to other versions. The corresponding routines are `yolov8_pose_*.py` and `yolo26_pose_*.py`.

```{admonition} Note
:class: warning
`YOLO26` directly outputs results with semantic information. The constructor **does not have the `nms_thresh` parameter**. When using `yolo26_pose_*.py`, please remove this parameter.
```

### Result Format

The result returned by `run()` is a list of length 4 `[boxes, ids, scores, keypoints]`:

- `boxes[i]`: Detection box of the i-th target `[x, y, w, h]`;
- `ids[i]`: Class index;
- `scores[i]`: Confidence;
- `keypoints[i]`: A one-dimensional array of length `kp_num * kp_dim`, **stored flatly**. The coordinates of the k-th keypoint are `keypoints[i][k*kp_dim+0]` and `keypoints[i][k*kp_dim+1]`. When `kp_dim` is 3, `keypoints[i][k*kp_dim+2]` is the visibility score of that point.

`draw_result` will draw the detection box, class label, and a solid circle for each keypoint (each keypoint uses a different color), but **will not draw skeleton connections**. When connections or other custom drawing methods are needed, you can refer to the `draw_result` implementation of the corresponding class in `libs/YOLO.py` to draw by yourself according to the `keypoints` data.

<a id="kmodel-verification"></a>

## kmodel Conversion Verification

The model conversion script toolkits downloaded for different models ( `test_yolov5/test_yolov8/test_yolo11/test_yolo26` ) contain kmodel verification scripts.

**yolo26 adds the nms process into the model for implementation, and the output data carries actual meaning, which is not suitable for measurement using cosine similarity. Moreover, the output shape is not large, so tiny differences will amplify the cosine computation differences. You can use the `test_***_onnx.py` and `test_***_kmodel.py` scripts to test the actual inference results.**

>Note: Executing the verification script requires adding environment variables
>
>**linux**:
>
>```shell
># The paths in the following commands are the paths of the Python environment where nncase is installed. Please adapt and modify them according to your environment
>export NNCASE_PLUGIN_PATH=$NNCASE_PLUGIN_PATH:/usr/local/lib/python3.9/site-packages/
>export PATH=$PATH:/usr/local/lib/python3.9/site-packages/
>source /etc/profile
>```
>
>**windows**:
>
>Add the `Lib/site-packages` path under the `Python` environment where `nncase` is installed to the system environment variable `Path`.

### Comparing onnx output and kmodel output

#### Generating input bin files

Navigate to the `classify/detect/segment/obb/pose` directory and execute the following command:

```shell
python save_bin.py --image ../test_images/test.jpg --input_width 224 --input_height 224
```

Executing the script will generate bin files `onnx_input_float32.bin` and `kmodel_input_uint8.bin` in the current directory, which serve as input files for the onnx model and kmodel model.

#### Comparing output

Copy the converted models `best.onnx`  and `best.kmodel`  to the `classify/detect/segment`  directory, then execute the verification script with the following command:

```shell
python simulate.py --model best.onnx --model_input onnx_input_float32.bin --kmodel best.kmodel --kmodel_input kmodel_input_uint8.bin --input_width 224 --input_height 224
```

The following output is obtained:

```shell
output 0 cosine similarity : 0.9985673427581787
```

The script will sequentially compare the cosine similarity of the outputs. If the similarity is above 0.99, the model is generally considered usable; otherwise, actual inference testing or re-exporting the kmodel with different quantization parameters is required. If the model has multiple outputs, there will be multiple lines of similarity comparison information. For example, for segmentation tasks with two outputs, the similarity comparison information is as follows:

```shell
output 0 cosine similarity : 0.9999530911445618
output 1 cosine similarity : 0.9983288645744324
```

### ONNX Model Inference on Images

Navigate to the `classify/detect/segment/obb/pose` directory. Taking the classification task as an example, open `test_cls_onnx.py`, modify the parameters in `main()` to fit your model, and then execute the command:

```shell
python test_cls_onnx.py
```

After the command executes successfully, the results will be saved to `onnx_cls_results.jpg` .

> The detection task, segmentation task, oriented object detection task, and keypoint detection task are similar. Execute `test_det_onnx.py`, `test_seg_onnx.py`, `test_obb_onnx.py`, `test_pose_onnx.py` respectively.

### Kmodel Model Inference on Images

Navigate to the `classify/detect/segment/obb/pose` directory. Taking the classification task as an example, open `test_cls_kmodel.py`, modify the parameters in `main()` to fit your model, and then execute the command:

```shell
python test_cls_kmodel.py
```

After the command executes successfully, the results will be saved to `kmodel_cls_results.jpg` .

> The detection task, segmentation task, oriented object detection task, and keypoint detection task are similar. Execute `test_det_kmodel.py`, `test_seg_kmodel.py`, `test_obb_kmodel.py`, `test_pose_kmodel.py` respectively.

## Tuning Guide

When the model does not perform well on K230, consider tuning from aspects such as threshold settings, model size, input resolution, quantization methods, and training data quality.

### Adjusting Thresholds

Adjust the confidence threshold, nms threshold, and mask threshold to tune the deployment effect without changing the model. In detection tasks, increasing the confidence threshold and decreasing the nms threshold will reduce the number of detection boxes; conversely, decreasing the confidence threshold and increasing the nms threshold will increase the number of detection boxes. In segmentation tasks, the mask threshold affects the division of segmentation regions. You can adjust according to the actual scenario to find the threshold that yields better results.

### Changing the Model

Choose models of different sizes to balance speed, memory usage, and accuracy. You can select n/s/m/l models for training and conversion based on actual requirements.

### Changing Input Resolution

Change the input resolution of the model to fit your scenario. A larger resolution may improve the deployment effect but will consume more inference time.

### Modifying Quantization Methods

The model conversion script provides 6 quantization combinations: 3 `uint8`/`int16` combinations for `data`/`weights`, each paired with either `NoClip` or `Kld` calibration method.

In the kmodel conversion script, different quantization methods are specified by selecting different `ptq_option` values.

| ptq_option | data  | weights | calibrate_method |
| ---------- | ----- | ------- | -----------------|
| 0          | uint8 | uint8   | NoClip           |
| 1          | uint8 | int16   | NoClip           |
| 2          | int16 | uint8   | NoClip           |
| 3          | uint8 | uint8   | Kld              |
| 4          | uint8 | int16   | Kld              |
| 5          | int16 | uint8   | Kld              |

### Improving Data Quality

If the training results are poor, please improve the dataset quality by optimizing the data volume, reasonable data distribution, annotation quality, and training parameter settings.

### Tuning Tips

- The impact of quantization parameters on performance is greater on YOLOv8 and YOLO11 than on YOLOv5; comparison across different quantized models can be observed;
- Input resolution has a greater impact on inference speed than model size;
- Differences in distribution between training data and K230 camera data may affect deployment performance. You can use K230 to collect part of the data and annotate it for training;
