# 5. YOLO Battle

## 1. YOLOv5 Fruit Classification

### 1.1 Building YOLOv5 Source Code and Training Environment

For building the YOLOv5 training environment, please refer to [ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5).

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

If you have already set up the environment, you can skip this step.

### 1.2 Preparing Training Data

Please download the provided example dataset. The example dataset contains classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenes. Unzip the dataset to the `yolov5` directory. Use `fruits_cls` as the dataset for the fruit classification task.

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### 1.3 Training a Fruit Classification Model with YOLOv5

Execute the command in the `yolov5` directory to train a three - class fruit classification model using `yolov5`:

```shell
python classify/train.py --model yolov5n-cls.pt --data datasets/fruits_cls --epochs 100 --batch-size 8 --imgsz 224 --device '0'
```

### 1.4 Converting the Fruit Classification kmodel

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

### 1.5 Deploying the Model on K230 Using MicroPython

#### 1.5.1 Burning the Image and Installing CanMV IDE

Please download the image according to the development board download link and burn it: [Release PreRelease · kendryte/canmv_k230](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease). Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), and write code in the IDE to implement deployment.

#### 1.5.2 Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### 1.5.3 YOLOv5 Module

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

#### 1.5.4 Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv5
import os,sys,gc
import ulab.numpy as np
import image

# Read the image from local and implement HWC to CHW conversion
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
    img_path="/data/test_apple.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.5
    model_input_size=[224,224]
    img,img_ori=read_img(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
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

#### 1.5.5 Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv5
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # Display mode, default "hdmi", can be selected as "hdmi" and "lcd"
    display_mode="hdmi"
    rgb888p_size=[1280,720]
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]
    # Model path
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.5
    model_input_size=[224,224]
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_size=display_size,display_mode=display_mode)
    pl.create()
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="classify",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                # Inference frame by frame
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

## 2. YOLOv5 Fruit Detection

### 2.1 Building YOLOv5 Source Code and Training Environment

For building the YOLOv5 training environment, please refer to [ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5).

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

If you have already set up the environment, you can skip this step.

### 2.2 Preparing Training Data

Please download the provided example dataset. The example dataset contains classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenes. Unzip the dataset to the `yolov5` directory. Use `fruits_yolo` as the dataset for the fruit detection task.

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### 2.3 Training a Fruit Detection Model with YOLOv5

Execute the command in the `yolov5` directory to train a three - class fruit detection model using `yolov5`:

```shell
python train.py --weight yolov5n.pt --cfg models/yolov5n.yaml --data datasets/fruits_yolo.yaml --epochs 300 --batch-size 8 --imgsz 320 --device '0'
```

### 2.4 Converting the Fruit Detection kmodel

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

### 2.5 Deploying the Model on K230 Using MicroPython

#### 2.5.1 Burning the Image and Installing CanMV IDE

Please download the image according to the development board download link and burn it: [Release PreRelease · kendryte/canmv_k230](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease). Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), and write code in the IDE to implement deployment.

#### 2.5.2 Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### 2.5.3 YOLOv5 Module

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

#### 2.5.4 Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**;

```python
from libs.YOLO import YOLOv5
import os,sys,gc
import ulab.numpy as np
import image

# Read the image from local and implement HWC to CHW conversion
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
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
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

#### 2.5.5 Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**;

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv5
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # Display mode, default "hdmi", can be selected as "hdmi" and "lcd"
    display_mode="hdmi"
    rgb888p_size=[1280,720]
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.8
    nms_threshold=0.45
    model_input_size=[320,320]
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_size=display_size,display_mode=display_mode)
    pl.create()
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="detect",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                # Inference frame by frame
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

## 3. YOLOv5 Fruit Segmentation

### 3.1 Setting up the YOLOv5 Source Code and Training Environment

For setting up the YOLOv5 training environment, please refer to [ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5).

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

If you have already set up the environment, you can skip this step.

### 3.2 Preparing the Training Data

Please download the provided example dataset. The example dataset contains classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenes. Unzip the dataset into the `yolov5` directory. Use `fruits_seg` as the dataset for the fruit segmentation task.

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### 3.3 Training a Fruit Segmentation Model with YOLOv5

Execute the command in the `yolov5` directory to train a three - class fruit segmentation model using `yolov5`:

```shell
python segment/train.py --weight yolov5n-seg.pt --cfg models/segment/yolov5n-seg.yaml --data datasets/fruits_seg.yaml --epochs 100 --batch-size 8 --imgsz 320 --device '0'
```

### 3.4 Converting the Fruit Segmentation kmodel

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

### 3.5 Deploying the Model on K230 Using MicroPython

#### 3.5.1 Burning the Image and Installing CanMV IDE

Please download the image according to the development board download link and burn it: [Release PreRelease · kendryte/canmv_k230](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease). Download and install CanMV IDE (download link: [CanMV IDE download](<https://www.kendryte.com/resource?selected=0> - 2 - 1)), and write code in the IDE to implement the deployment.

#### 3.5.2 Copying the Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### 3.5.3 The YOLOv5 Module

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

#### 3.5.4 Deploying the Model for Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv5
import os,sys,gc
import ulab.numpy as np
import image

# Read the image from local and perform HWC to CHW conversion
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
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    model_input_size=[320,320]
    img,img_ori=read_img(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
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

#### 3.5.5 Deploying the Model for Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv5
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # Display mode, with the default "hdmi", and options "hdmi" and "lcd" available
    display_mode="hdmi"
    rgb888p_size=[320,320]
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    model_input_size=[320,320]
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_size=display_size,display_mode=display_mode)
    pl.create()
    # Initialize the YOLOv5 instance
    yolo=YOLOv5(task_type="segment",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                # Inference frame by frame
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

## 4. YOLOv8 Fruit Classification

### 4.1 Setting up YOLOv8 Source Code and Training Environment

For setting up the YOLOv8 training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### 4.2 Preparing Training Data

You can first create a new folder `yolov8`. Then, download the provided example dataset. The example dataset contains classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenes. Unzip the dataset into the `yolov8` directory. Use `fruits_cls` as the dataset for the fruit classification task.

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### 4.3 Training a Fruit Classification Model with YOLOv8

Execute the command in the `yolov8` directory to train a three - class fruit classification model using `yolov8`:

```shell
yolo classify train data=datasets/fruits_cls model=yolov8n-cls.pt epochs=100 imgsz=224
```

### 4.4 Converting the Fruit Classification kmodel

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

Follow the following commands to first export the `pt` model under `runs/classify/exp/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export onnx, please select the path of the pt model by yourself
yolo export model=runs/classify/train/weights/best.pt format=onnx imgsz=224
cd test_yolov8/classify
# Convert kmodel, please select the path of the onnx model by yourself. The generated kmodel is in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/classify/train/weights/best.onnx --dataset../test --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

### 4.5 Deploying the Model on K230 Using MicroPython

#### 4.5.1 Burning the Image and Installing CanMV IDE

Please download the image according to the development board download link and burn it: [Release PreRelease · kendryte/canmv_k230](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease). Download and install CanMV IDE (download link: [CanMV IDE download](<https://www.kendryte.com/resource?selected=0> - 2 - 1)), and write code in the IDE to implement deployment.

#### 4.5.2 Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### 4.5.3 YOLOv8 Module

The `YOLOv8` class integrates three tasks of `YOLOv8`, including classification (classify), detection (detect), and segmentation (segment); it supports two inference modes, including image (image) and video stream (video); this class encapsulates the kmodel inference process of `YOLOv8`.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports three types of tasks, with optional values 'classify' / 'detect' /'segment'; | str |
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

#### 4.5.4 Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLOv8
import os,sys,gc
import ulab.numpy as np
import image

# Read the image from local and perform HWC to CHW conversion
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
    img_path="/data/test_apple.jpg"
    kmodel_path="/data/best.kmodel"
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

#### 4.5.5 Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv8
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # Display mode, with the default "hdmi", and options "hdmi" and "lcd" available
    display_mode="hdmi"
    rgb888p_size=[1280,720]
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    confidence_threshold = 0.8
    model_input_size=[224,224]
    # Initialize PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_size=display_size,display_mode=display_mode)
    pl.create()
    # Initialize the YOLOv8 instance
    yolo=YOLOv8(task_type="classify",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                # Inference frame by frame
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

## 5. YOLOv8 Fruit Detection

### 5.1 Setting up YOLOv8 Source Code and Training Environment

For setting up the YOLOv8 training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### 5.2 Preparing Training Data

You can first create a new folder named `yolov8`. Then, download the provided example dataset. The example dataset contains classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenes. Unzip the dataset into the `yolov8` directory. Use `fruits_yolo` as the dataset for the fruit detection task.

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### 5.3 Training a Fruit Detection Model with YOLOv8

Execute the command in the `yolov8` directory to train a three - class fruit detection model using `yolov8`:

```shell
yolo detect train data=datasets/fruits_yolo.yaml model=yolov8n.pt epochs=300 imgsz=320
```

### 5.4 Converting the Fruit Detection kmodel

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

### 5.5 Deploying the Model on K230 Using MicroPython

#### 5.5.1 Burning the Image and Installing CanMV IDE

Please download the image according to the development board download link and burn it: [Release PreRelease · kendryte/canmv_k230](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease). Download and install CanMV IDE (download link: [CanMV IDE download](<https://www.kendryte.com/resource?selected=0> - 2 - 1)), and write code in the IDE to implement deployment.

#### 5.5.2 Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### 5.5.3 YOLOv8 Module

The `YOLOv8` class integrates three tasks of `YOLOv8`, namely classification (classify), detection (detect), and segmentation (segment). It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of `YOLOv8`.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports three types of tasks, with optional values 'classify', 'detect', or'segment'; | str |
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

#### 5.5.4 Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLOv8
import os, sys, gc
import ulab.numpy as np
import image

# Read the image from local and perform HWC to CHW conversion
def read_img(img_path):
    img_data = image.Image(img_path)
    img_data_rgb888 = img_data.to_rgb888()
    img_hwc = img_data_rgb888.to_numpy_ref()
    shape = img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_tmp_trans = img_tmp.transpose()
    img_res = img_tmp_trans.copy()
    img_return = img_res.reshape((shape[2], shape[0], shape[1]))
    return img_return, img_data_rgb888

if __name__ == "__main__":
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    model_input_size = [320, 320]
    img, img_ori = read_img(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize the YOLOv8 instance
    yolo = YOLOv8(task_type="detect", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    try:
        res = yolo.run(img)
        yolo.draw_result(res, img_ori)
        gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
```

#### 5.5.5 Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv8
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # Display mode, with the default "hdmi", and options "hdmi" and "lcd" available
    display_mode = "hdmi"
    rgb888p_size = [1280, 720]
    if display_mode == "hdmi":
        display_size = [1920, 1080]
    else:
        display_size = [800, 480]
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.8
    nms_threshold = 0.45
    model_input_size = [320, 320]
    # Initialize PipeLine
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()
    # Initialize the YOLOv8 instance
    yolo = YOLOv8(task_type="detect", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total", 1):
                # Inference frame by frame
                img = pl.get_frame()
                res = yolo.run(img)
                yolo.draw_result(res, pl.osd_img)
                pl.show_image()
                gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
        pl.destroy()
```

## 6. YOLOv8 Fruit Segmentation

### 6.1 Setting up YOLOv8 Source Code and Training Environment

For setting up the training environment of YOLOv8, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### 6.2 Preparing Training Data

You can first create a new folder named `yolov8`. Then, download the provided example dataset. The example dataset contains classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenes. Unzip the dataset into the `yolov8` directory. Use `fruits_seg` as the dataset for the fruit segmentation task.

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### 6.3 Training a Fruit Segmentation Model with YOLOv8

Execute the command in the `yolov8` directory to train a three - class fruit segmentation model using `yolov8`:

```shell
yolo segment train data=datasets/fruits_seg.yaml model=yolov8n-seg.pt epochs=100 imgsz=320
```

### 6.4 Converting the Fruit Segmentation kmodel

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

### 6.5 Deploying the Model on K230 Using MicroPython

#### 6.5.1 Burning the Image and Installing CanMV IDE

Please download the image according to the development board download link and burn it: [Release PreRelease · kendryte/canmv_k230](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease). Download and install CanMV IDE (download link: [CanMV IDE download](<https://www.kendryte.com/resource?selected=0> - 2 - 1)), and write code in the IDE to implement deployment.

#### 6.5.2 Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### 6.5.3 YOLOv8 Module

The `YOLOv8` class integrates three tasks of `YOLOv8`, namely classification (classify), detection (detect), and segmentation (segment). It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of `YOLOv8`.

- **Import Method**

```python
from libs.YOLO import YOLOv8
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports three types of tasks, with optional values 'classify', 'detect', or'segment'; | str |
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

#### 6.5.4 Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLOv8
import os, sys, gc
import ulab.numpy as np
import image

# Read the image from local and perform HWC to CHW conversion
def read_img(img_path):
    img_data = image.Image(img_path)
    img_data_rgb888 = img_data.to_rgb888()
    img_hwc = img_data_rgb888.to_numpy_ref()
    shape = img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_tmp_trans = img_tmp.transpose()
    img_res = img_tmp_trans.copy()
    img_return = img_res.reshape((shape[2], shape[0], shape[1]))
    return img_return, img_data_rgb888

if __name__ == "__main__":
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    model_input_size = [320, 320]
    img, img_ori = read_img(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize the YOLOv8 instance
    yolo = YOLOv8(task_type="segment", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    try:
        res = yolo.run(img)
        yolo.draw_result(res, img_ori)
        gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
```

#### 6.5.5 Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv8
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # Display mode, with the default "hdmi", and options "hdmi" and "lcd" available
    display_mode = "hdmi"
    rgb888p_size = [320, 320]
    if display_mode == "hdmi":
        display_size = [1920, 1080]
    else:
        display_size = [800, 480]
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    model_input_size = [320, 320]
    # Initialize PipeLine
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()
    # Initialize the YOLOv8 instance
    yolo = YOLOv8(task_type="segment", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total", 1):
                # Inference frame by frame
                img = pl.get_frame()
                res = yolo.run(img)
                yolo.draw_result(res, pl.osd_img)
                pl.show_image()
                gc.collect()
    except Exception as e:
        print(e)
    finally:
        yolo.deinit()
        pl.destroy()
```

## 7. YOLO11 Fruit Classification

### 7.1 Setting up YOLO11 Source Code and Training Environment

For setting up the training environment of YOLO11, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### 7.2 Preparing Training Data

You can first create a new folder named `yolo11`. Then, download the provided example dataset. The example dataset contains classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenes. Unzip the dataset into the `yolo11` directory. Use `fruits_cls` as the dataset for the fruit classification task.

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### 7.3 Training a Fruit Classification Model with YOLO11

Execute the command in the `yolo11` directory to train a three - class fruit classification model using `yolo11`:

```shell
yolo classify train data=datasets/fruits_cls model=yolo11n-cls.pt epochs=100 imgsz=224
```

### 7.4 Converting the Fruit Classification kmodel

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

### 7.5 Deploying the Model on K230 Using MicroPython

#### 7.5.1 Burning the Image and Installing CanMV IDE

Please download the image according to the development board download link and burn it: [Release PreRelease · kendryte/canmv_k230](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease). Download and install CanMV IDE (download link: [CanMV IDE download](<https://www.kendryte.com/resource?selected=0> - 2 - 1)), and write code in the IDE to implement deployment.

#### 7.5.2 Copying Model Files

Connect the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized, and you only need to modify the corresponding path when writing the code.

#### 7.5.3 YOLO11 Module

The `YOLO11` class integrates three tasks of `YOLO11`, namely classification (classify), detection (detect), and segmentation (segment). It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of `YOLO11`.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name | Description | Instructions | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports three types of tasks, with optional values 'classify', 'detect', or'segment'; | str |
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

#### 7.5.4 Deploying the Model to Implement Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLO11
import os, sys, gc
import ulab.numpy as np
import image

# Read the image from local and perform HWC to CHW conversion
def read_img(img_path):
    img_data = image.Image(img_path)
    img_data_rgb888 = img_data.to_rgb888()
    img_hwc = img_data_rgb888.to_numpy_ref()
    shape = img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_tmp_trans = img_tmp.transpose()
    img_res = img_tmp_trans.copy()
    img_return = img_res.reshape((shape[2], shape[0], shape[1]))
    return img_return, img_data_rgb888

if __name__ == "__main__":
    img_path = "/data/test_apple.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.5
    model_input_size = [224, 224]
    img, img_ori = read_img(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize the YOLO11 instance
    yolo = YOLO11(task_type="classify", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, debug_mode=0)
    yolo.config_preprocess()
    try:
        res = yolo.run(img)
        yolo.draw_result(res, img_ori)
        gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
```

#### 7.5.5 Deploying the Model to Implement Video Inference

For video inference, please refer to the following code. **Modify the defined variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLO11
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # Display mode, with the default "hdmi", and options "hdmi" and "lcd" available
    display_mode = "hdmi"
    rgb888p_size = [1280, 720]
    if display_mode == "hdmi":
        display_size = [1920, 1080]
    else:
        display_size = [800, 480]
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.8
    model_input_size = [224, 224]
    # Initialize PipeLine
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()
    # Initialize the YOLO11 instance
    yolo = YOLO11(task_type="classify", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total", 1):
                # Inference frame by frame
                img = pl.get_frame()
                res = yolo.run(img)
                yolo.draw_result(res, pl.osd_img)
                pl.show_image()
                gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
        pl.destroy()
```

## 8. YOLO11 Fruit Detection

### 8.1 Setting up YOLO11 Source Code and Training Environment

For setting up the training environment of YOLO11, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### 8.2 Preparing Training Data

You can first create a new folder named `yolo11`. Then, download the provided example dataset. The example dataset contains classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange) as scenes. Unzip the dataset into the `yolo11` directory. Use `fruits_yolo` as the dataset for the fruit detection task.

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### 8.3 Training a Fruit Detection Model with YOLO11

Execute the command in the `yolo11` directory to train a three - class fruit detection model using `yolo11`:

```shell
yolo detect train data=datasets/fruits_yolo.yaml model=yolo11n.pt epochs=300 imgsz=320
```

### 8.4 Converting the Fruit Detection kmodel

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

Follow the following commands to first export the `pt` model under `runs/detect/exp/weights` to an `onnx` model, and then convert it to a `kmodel` model:

```shell
# Export to onnx. Please select the path of the pt model by yourself.
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/detect
# Convert to kmodel. Please select the path of the onnx model by yourself. The generated kmodel will be in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 8.5 Deploying the Model on K230 Using MicroPython

#### 8.5.1 Burning the Image and Installing CanMV IDE

Please download the image according to the link provided for the development board and burn it: [Release PreRelease · kendryte/canmv_k230](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease). Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), and write code in the IDE to implement the deployment.

#### 8.5.2 Copying the Model Files

Connect to the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized; you just need to modify the corresponding path when writing the code.

#### 8.5.3 The YOLO11 Module

The `YOLO11` class integrates three tasks of `YOLO11`, namely classification (`classify`), detection (`detect`), and segmentation (`segment`). It supports two inference modes, namely image (`image`) and video stream (`video`). This class encapsulates the kmodel inference process of `YOLO11`.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name | Description | Explanation | Type |
| --- | --- | --- | --- |
| task_type | Task type | Supports three types of tasks. The available options are `classify`, `detect`, and `segment`. | str |
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

#### 8.5.4 Deploying the Model for Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLO11
import os, sys, gc
import ulab.numpy as np
import image

# Read an image from the local storage and convert it from HWC to CHW format.
def read_img(img_path):
    img_data = image.Image(img_path)
    img_data_rgb888 = img_data.to_rgb888()
    img_hwc = img_data_rgb888.to_numpy_ref()
    shape = img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_tmp_trans = img_tmp.transpose()
    img_res = img_tmp_trans.copy()
    img_return = img_res.reshape((shape[2], shape[0], shape[1]))
    return img_return, img_data_rgb888

if __name__ == "__main__":
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    model_input_size = [320, 320]
    img, img_ori = read_img(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize the YOLO11 instance.
    yolo = YOLO11(task_type="detect", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    try:
        res = yolo.run(img)
        yolo.draw_result(res, img_ori)
        gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
```

#### 8.5.5 Deploying the Model for Video Inference

For video inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLO11
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # Display mode. The default is "hdmi". You can choose between "hdmi" and "lcd".
    display_mode = "hdmi"
    rgb888p_size = [1280, 720]
    if display_mode == "hdmi":
        display_size = [1920, 1080]
    else:
        display_size = [800, 480]
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.8
    nms_threshold = 0.45
    model_input_size = [320, 320]
    # Initialize the PipeLine.
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()
    # Initialize the YOLO11 instance.
    yolo = YOLO11(task_type="detect", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total", 1):
                # Perform inference frame by frame.
                img = pl.get_frame()
                res = yolo.run(img)
                yolo.draw_result(res, pl.osd_img)
                pl.show_image()
                gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
        pl.destroy()
```

## 9. YOLO11 Fruit Segmentation

### 9.1 Setting up the YOLO11 Source Code and Training Environment

To set up the YOLO11 training environment, please refer to [ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics).

```shell
# Use pip to install the ultralytics package along with all its requirements in a Python environment where Python >= 3.8 and PyTorch >= 1.8.
pip install ultralytics
```

If you have already set up the environment, you can skip this step.

### 9.2 Preparing the Training Data

You can first create a new folder named `yolo11`. Then, download the provided example dataset. This dataset includes classification, detection, and segmentation datasets for three types of fruits (apple, banana, orange). Unzip the dataset into the `yolo11` directory and use `fruits_seg` as the dataset for the fruit segmentation task.

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

If you have already downloaded the data, you can skip this step.

### 9.3 Training a Fruit Segmentation Model with YOLO11

Execute the following command in the `yolo11` directory to train a three-class fruit segmentation model using YOLO11:

```shell
yolo segment train data=datasets/fruits_seg.yaml model=yolo11n-seg.pt epochs=100 imgsz=320
```

### 9.4 Converting the Fruit Segmentation kmodel

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

Follow the commands below to first export the `pt` model under `runs/segment/exp/weights` to an `onnx` model and then convert it to a `kmodel` model:

```shell
# Export to onnx. Please select the path of the pt model by yourself.
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/segment
# Convert to kmodel. Please select the path of the onnx model by yourself. The generated kmodel will be in the same directory as the onnx model.
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 9.5 Deploying the Model on K230 Using MicroPython

#### 9.5.1 Burning the Image and Installing CanMV IDE

Please download the image according to the link provided for the development board and burn it: [Release PreRelease · kendryte/canmv_k230](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease). Download and install CanMV IDE (download link: [CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1)), and write code in the IDE to implement the deployment.

#### 9.5.2 Copying the Model Files

Connect to the IDE and copy the converted model and test images to the `CanMV/data` directory. This path can be customized; you just need to modify the corresponding path when writing the code.

#### 9.5.3 YOLO11 Module

The `YOLO11` class integrates three tasks of YOLO11, namely classification (classify), detection (detect), and segmentation (segment). It supports two inference modes, namely image (image) and video stream (video). This class encapsulates the kmodel inference process of YOLO11.

- **Import Method**

```python
from libs.YOLO import YOLO11
```

- **Parameter Description**

| Parameter Name | Description | Explanation | Type |
| ---- | ---- | ---- | ---- |
| task_type | Task type | Supports three types of tasks. The available options are 'classify', 'detect', and 'segment'. | str |
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

#### 9.5.4 Deploying the Model for Image Inference

For image inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.YOLO import YOLO11
import os, sys, gc
import ulab.numpy as np
import image

# Read an image from the local storage and convert it from HWC to CHW format.
def read_img(img_path):
    img_data = image.Image(img_path)
    img_data_rgb888 = img_data.to_rgb888()
    img_hwc = img_data_rgb888.to_numpy_ref()
    shape = img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_tmp_trans = img_tmp.transpose()
    img_res = img_tmp_trans.copy()
    img_return = img_res.reshape((shape[2], shape[0], shape[1]))
    return img_return, img_data_rgb888

if __name__ == "__main__":
    img_path = "/data/test.jpg"
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    model_input_size = [320, 320]
    img, img_ori = read_img(img_path)
    rgb888p_size = [img.shape[2], img.shape[1]]
    # Initialize the YOLO11 instance.
    yolo = YOLO11(task_type="segment", mode="image", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    try:
        res = yolo.run(img)
        yolo.draw_result(res, img_ori)
        gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
```

#### 9.5.5 Deploying the Model for Video Inference

For video inference, please refer to the following code. **Modify the defined parameter variables in `__main__` according to the actual situation**:

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLO11
import os, sys, gc
import ulab.numpy as np
import image

if __name__ == "__main__":
    # Display mode. The default is "hdmi". You can choose between "hdmi" and "lcd".
    display_mode = "hdmi"
    rgb888p_size = [320, 320]
    if display_mode == "hdmi":
        display_size = [1920, 1080]
    else:
        display_size = [800, 480]
    kmodel_path = "/data/best.kmodel"
    labels = ["apple", "banana", "orange"]
    confidence_threshold = 0.5
    nms_threshold = 0.45
    mask_threshold = 0.5
    model_input_size = [320, 320]
    # Initialize the PipeLine.
    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    pl.create()
    # Initialize the YOLO11 instance.
    yolo = YOLO11(task_type="segment", mode="video", kmodel_path=kmodel_path, labels=labels, rgb888p_size=rgb888p_size, model_input_size=model_input_size, display_size=display_size, conf_thresh=confidence_threshold, nms_thresh=nms_threshold, mask_thresh=mask_threshold, max_boxes_num=50, debug_mode=0)
    yolo.config_preprocess()
    try:
        while True:
            os.exitpoint()
            with ScopedTiming("total", 1):
                # Perform inference frame by frame.
                img = pl.get_frame()
                res = yolo.run(img)
                yolo.draw_result(res, pl.osd_img)
                pl.show_image()
                gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        yolo.deinit()
        pl.destroy()
```

## 10. Verification of kmodel Conversion

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

### 10.1 Comparing the Outputs of the onnx and kmodel

#### 10.1.1 Generating the Input bin Files

Enter the `classify/detect/segment` directory and execute the following command:

```shell
python save_bin.py --image ../test_images/test.jpg --input_width 224 --input_height 224
```

After executing the script, the bin files `onnx_input_float32.bin` and `kmodel_input_uint8.bin` will be generated in the current directory, which will serve as the input files for the onnx model and the kmodel.

#### 10.1.2 Comparing the Outputs

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

### 10.2 Inference on Images Using the onnx Model

Enter the `classify/detect/segment` directory, open `test_cls_onnx.py`, modify the parameters in `main()` to adapt to your model, and then execute the command:

```shell
python test_cls_onnx.py
```

After the command is successfully executed, the result will be saved as `onnx_cls_results.jpg`.

> The detection and segmentation tasks are similar. Execute `test_det_onnx.py` and `test_seg_onnx.py` respectively.

### 10.3 Inference on Images Using the kmodel

Enter the `classify/detect/segment` directory, open `test_cls_kmodel.py`, modify the parameters in `main()` to adapt to your model, and then execute the command:

```shell
python test_cls_kmodel.py
```

After the command is successfully executed, the result will be saved as `kmodel_cls_results.jpg`.

> The detection and segmentation tasks are similar. Execute `test_det_kmodel.py` and `test_seg_kmodel.py` respectively.

## 11. Tuning Guide

When the performance of the model on the K230 is not satisfactory, you can generally consider tuning from aspects such as threshold settings, model size, input resolution, quantization methods, and the quality of training data.

### 11.1 Adjusting Thresholds

Adjust the confidence threshold, NMS threshold, and mask threshold to optimize the deployment effect without changing the model. In the detection task, increasing the confidence threshold and decreasing the NMS threshold will result in a decrease in the number of detection boxes. Conversely, decreasing the confidence threshold and increasing the NMS threshold will lead to an increase in the number of detection boxes. In the segmentation task, the mask threshold will affect the division of the segmentation area. You can make adjustments according to the actual scenario first to find the optimal thresholds.

### 11.2 Changing the Model

Select models of different sizes to balance speed, memory usage, and accuracy. You can choose models of n/s/m/l according to your actual needs for training and conversion.

The following data is a ***rough measurement*** of the kmodel trained on the three - class fruit dataset when running on the `01Studio CanMV K230` development board. In actual deployment, the post - processing time will increase due to the number of results, and the time consumption of memory management `gc.collect()` will also increase with the complexity of post - processing:

| Model | Input Resolution | Task | KPU Inference Time | KPU Inference FPS | Whole - Frame Inference Time | Whole - Frame Inference FPS |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| yolov5n | 224×224 | cls | 3ms | 333fps | 17ms | 58fps |
| yolov5s | 224×224 | cls | 7ms | 142fps | 19ms | 52fps |
| yolov5m | 224×224 | cls | 12ms | 83fps | 24ms | 41fps |
| yolov5l | 224×224 | cls | 22ms | 45fps | 33ms | 30fps |
| yolov8n | 224×224 | cls | 6ms | 166fps | 16ms | 62fps |
| yolov8s | 224×224 | cls | 13ms | 76fps | 24ms | 41fps |
| yolov8m | 224×224 | cls | 27ms | 37fps | 39ms | 25fps |
| yolov8l | 224×224 | cls | 53ms | 18fps | 65ms | 15fps |
| yolo11n | 224×224 | cls | 7ms | 142fps | 19ms | 52fps |
| yolo11s | 224×224 | cls | 15ms | 66fps | 26ms | 38fps |
| yolo11m | 224×224 | cls | 23ms | 43fps | 35ms | 28fps |
| yolo11l | 224×224 | cls | 31ms | 32fps | 43ms | 23fps |
| yolov5n | 320×320 | det | 25ms | 40fps | 105ms | 9fps |
| yolov5s | 320×320 | det | 30ms | 33fps | 109ms | 9fps |
| yolov5m | 320×320 | det | 44ms | 22fps | 124ms | 8fps |
| yolov5l | 320×320 | det | 73ms | 13fps | 149ms | 6fps |
| yolov8n | 320×320 | det | 25ms | 40fps | 62ms | 16fps |
| yolov8s | 320×320 | det | 44ms | 22fps | 77ms | 12fps |
| yolov8m | 320×320 | det | 78ms | 12fps | 109ms | 9fps |
| yolov8l | 320×320 | det | 126ms | 7fps | 160ms | 6fps |
| yolo11n | 320×320 | det | 28ms | 35fps | 63ms | 15fps |
| yolo11s | 320×320 | det | 49ms | 20fps | 81ms | 12fps |
| yolo11m | 320×320 | det | 77ms | 12fps | 112ms | 8fps |
| yolo11l | 320×320 | det | 94ms | 10fps | 132ms | 7fps |
| yolov5n | 320×320 | seg | 67ms | 14fps | 178ms | 5fps |
| yolov5s | 320×320 | seg | 80ms | 12fps | 180ms | 5fps |
| yolov5m | 320×320 | seg | 95ms | 10fps | 206ms | 4fps |
| yolov5l | 320×320 | seg | 122ms | 8fps | 235ms | 4fps |
| yolov8n | 320×320 | seg | 28ms | 35fps | 131ms | 7fps |
| yolov8s | 320×320 | seg | 52ms | 19fps | 151ms | 6fps |
| yolov8m | 320×320 | seg | 87ms | 11fps | 215ms | 4fps |
| yolov8l | 320×320 | seg | 143ms | 6fps | 246ms | 4fps |
| yolo11n | 320×320 | seg | 31ms | 32fps | 135ms | 7fps |
| yolo11s | 320×320 | seg | 55ms | 18fps | 156ms | 6fps |
| yolo11m | 320×320 | seg | 97ms | 10fps | 205ms | 4fps |
| yolo11l | 320×320 | seg | 112ms | 8fps | 214ms | 4fps |

### 11.3 Changing the Input Resolution

Change the input resolution of the model to adapt to your scenario. A larger resolution can improve the performance but will consume more inference time.

The following data is a ***rough measurement*** of the kmodel trained on the three - class fruit dataset when running on the `01Studio CanMV K230` development board. In actual deployment, the post - processing time will increase due to the number of results, and the time consumption of memory management `gc.collect()` will also increase with the complexity of post - processing:

| Model | Input Resolution | Task | KPU Inference Time | KPU Inference FPS | Whole - Frame Inference Time | Whole - Frame Inference FPS |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| yolov5n | 224×224 | cls | 3ms | 333fps | 17ms | 58fps |
| yolov5n | 320×320 | cls | 5ms | 200fps | 18ms | 55fps |
| yolov5n | 320×320 | det | 25ms | 40fps | 105ms | 9fps |
| yolov5n | 640×640 | det | 73ms | 13fps | 322ms | 3fps |
| yolov5n | 320×320 | seg | 67ms | 14fps | 178ms | 5fps |
| yolov5n | 640×640 | seg | 252ms | 3fps | 398ms | 2fps |
| yolov8n | 224×224 | cls | 6ms | 166fps | 16ms | 62fps |
| yolov8n | 320×320 | cls | 7ms | 142fps | 21ms | 47fps |
| yolov8n | 320×320 | det | 25ms | 40fps | 62ms | 16fps |
| yolov8n | 640×640 | det | 85ms | 11fps | 183ms | 5fps |
| yolov8n | 320×320 | seg | 28ms | 35fps | 131ms | 7fps |
| yolov8n | 640×640 | seg | 98ms | 10fps | 261ms | 3fps |
| yolo11n | 224×224 | cls | 7ms | 142fps | 19ms | 52fps |
| yolo11n | 320×320 | cls | 9ms | 111fps | 22ms | 45fps |
| yolo11n | 320×320 | det | 28ms | 35fps | 63ms | 15fps |
| yolo11n | 640×640 | det | 92ms | 10fps | 191ms | 5fps |
| yolo11n | 320×320 | seg | 31ms | 32fps | 135ms | 7fps |
| yolo11n | 640×640 | seg | 104ms | 9fps | 263ms | 3fps |

### 11.4 Modifying the Quantization Method

The model conversion script provides three quantization parameters for `uint8` or `int16` quantization of `data` and `weights`.

In the script for converting to kmodel, different quantization methods can be specified by selecting different values of `ptq_option`.

| ptq_option | data | weights |
| ---- | ---- | ---- |
| 0 | uint8 | uint8 |
| 1 | uint8 | int16 |
| 2 | int16 | uint8 |

The following data is a ***rough measurement*** of the kmodel trained on the three - class fruit dataset when running on the `01Studio CanMV K230` development board. In actual deployment, the post - processing time will increase due to the number of results, and the time consumption of memory management `gc.collect()` will also increase with the complexity of post - processing:

| Model | Input Resolution | Task | Quantization Parameters [data, weights] | KPU Inference Time | KPU Inference FPS | Whole - Frame Inference Time | Whole - Frame Inference FPS |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| yolov5n | 320×320 | det | [uint8, uint8] | 25ms | 40fps | 105ms | 9fps |
| yolov5n | 320×320 | det | [uint8, int16] | 25ms | 40fps | 103ms | 9fps |
| yolov5n | 320×320 | det | [int16, uint8] | 30ms | 33fps | 110ms | 9fps |
| yolov8n | 320×320 | det | [uint8, uint8] | 25ms | 40fps | 62ms | 16fps |
| yolov8n | 320×320 | det | [uint8, int16] | 27ms | 37fps | 65ms | 15fps |
| yolov8n | 320×320 | det | [int16, uint8] | 33ms | 30fps | 72ms | 13fps |
| yolo11n | 320×320 | det | [uint8, uint8] | 28ms | 35fps | 63ms | 15fps |
| yolo11n | 320×320 | det | [uint8, int16] | 33ms | 30fps | 71ms | 14fps |
| yolo11n | 320×320 | det | [int16, uint8] | 35ms | 28fps | 78ms | 12fps |

### 11.5 Improving Data Quality

If the training results are poor, improve the quality of the dataset by optimizing aspects such as the data volume, reasonable data distribution, annotation quality, and training parameter settings.

### 11.6 Tuning Tips

- The quantization parameters have a greater impact on the performance of YOLOv8 and YOLO11 than on YOLOv5, as can be seen by comparing different quantized models.
- The input resolution has a greater impact on the inference speed than the model size.
- The difference in data distribution between the training data and the data captured by the K230 camera may affect the deployment effect. You can collect some data using the K230 and annotate and train it yourself.
