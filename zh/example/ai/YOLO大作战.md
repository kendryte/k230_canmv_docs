# 5. K230 YOLO 大作战

## 1. YOLOv5水果分类

### 1.1 YOLOv5源码及训练环境搭建

`YOLOv5` 训练环境搭建请参考[ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5)

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

如果您已搭建好环境，请忽略此步骤。

### 1.2 训练数据准备

请下载提供的示例数据集，示例数据集中包含以三类水果（apple，banana，orange）为场景分别提供了分类、检测和分割数据集。将数据集解压到 `yolov5` 目录下，请使用 `fruits_cls` 作为水果分类任务的数据集。示例数据集中还包含一个旋转目标检测的桌面签字笔场景数据集 `yolo_pen_obb`，该任务在k230 的 `YOLOv5` 模块中不支持。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注，分类任务数据不需要使用工具标注，仅按照格式划分目录即可。 将标注后的数据转换成 `yolov5` 官方支持的训练数据格式进行后续训练。

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 1.3 使用YOLOv5训练水果分类模型

在 `yolov5` 目录下执行命令，使用 `yolov5` 训练三类水果分类模型：

```shell
python classify/train.py --model yolov5n-cls.pt --data datasets/fruits_cls --epochs 100 --batch-size 8 --imgsz 224 --device '0'
```

### 1.4 转换水果分类kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolov5.zip` 解压到 `yolov5` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

按照如下命令，对 `runs/train-cls/exp/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
python export.py --weight runs/train-cls/exp/weights/best.pt --imgsz 224 --batch 1 --include onnx
cd test_yolov5/classify
# 转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/train-cls/exp/weights/best.onnx --dataset ../test --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

### 1.5 在k230上使用MicroPython部署模型

#### 1.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 1.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 1.5.3 YOLOv5 模块

`YOLOv5` 类集成了 `YOLOv5` 的三种任务，包括分类(classify)、检测(detect)、分割(segment)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLOv5` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLOv5
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持三类任务，可选项为'classify'/'detect'/'segment'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv5模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 1.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test_apple.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLOv5实例
    yolo=YOLOv5(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 1.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv5
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLOv5实例
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

## 2. YOLOv5水果检测

### 2.1 YOLOv5源码及训练环境搭建

`YOLOv5` 训练环境搭建请参考[ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5)

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

如果您已搭建好环境，请忽略此步骤。

### 2.2 训练数据准备

请下载提供的示例数据集，示例数据集中包含以三类水果（apple，banana，orange）为场景分别提供了分类、检测和分割数据集。将数据集解压到 `yolov5` 目录下，请使用 `fruits_yolo` 作为水果检测任务的数据集。示例数据集中还包含一个旋转目标检测的桌面签字笔场景数据集 `yolo_pen_obb`，该任务在k230 的 `YOLOv5` 模块中不支持。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注。 自行将标注后的数据转换成 `yolov5` 官方支持的训练数据格式进行后续训练。

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 2.3 使用YOLOv5训练水果检测模型

在 `yolov5` 目录下执行命令，使用 `yolov5` 训练三类水果检测模型：

```shell
python train.py --weight yolov5n.pt --cfg models/yolov5n.yaml --data datasets/fruits_yolo.yaml --epochs 300 --batch-size 8 --imgsz 320 --device '0'
```

### 2.4 转换水果检测kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolov5.zip` 解压到 `yolov5` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

按照如下命令，对 `runs/train/exp/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
python export.py --weight runs/train/exp/weights/best.pt --imgsz 320 --batch 1 --include onnx
cd test_yolov5/detect
# 转换kmodel,onnx模型路径请自定义，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/train/exp/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 2.5 在k230上使用MicroPython部署模型

#### 2.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 2.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 2.5.3 YOLOv5 模块

`YOLOv5` 类集成了 `YOLOv5` 的三种任务，包括分类(classify)、检测(detect)、分割(segment)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLOv5` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLOv5
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持三类任务，可选项为'classify'/'detect'/'segment'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv5模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 2.5.4  部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLOv5
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
    # 初始化YOLOv5实例
    yolo=YOLOv5(task_type="detect",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 2.5.5  部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[640,360]
    confidence_threshold = 0.8
    nms_threshold=0.45
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLOv5实例
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

## 3. YOLOv5水果分割

### 3.1 YOLOv5源码及训练环境搭建

`YOLOv5` 训练环境搭建请参考[ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5)

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

如果您已搭建好环境，请忽略此步骤。

### 3.2 训练数据准备

请下载提供的示例数据集，示例数据集中包含以三类水果（apple，banana，orange）为场景分别提供了分类、检测和分割数据集。将数据集解压到 `yolov5` 目录下，请使用 `fruits_seg` 作为水果分割任务的数据集。示例数据集中还包含一个旋转目标检测的桌面签字笔场景数据集 `yolo_pen_obb`，该任务在k230 的 `YOLOv5` 模块中不支持。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注。 自行将标注后的数据转换成 `yolov5` 官方支持的训练数据格式进行后续训练。

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 3.3 使用YOLOv5训练水果分割模型

在 `yolov5` 目录下执行命令，使用 `yolov5` 训练三类水果分割模型：

```shell
python segment/train.py --weight yolov5n-seg.pt --cfg models/segment/yolov5n-seg.yaml --data datasets/fruits_seg.yaml --epochs 100 --batch-size 8 --imgsz 320 --device '0'
```

### 3.4 转换水果分割kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolov5.zip` 解压到 `yolov5` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

按照如下命令，对 `runs/train-seg/exp/weights` 下的模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
python export.py --weight runs/train-seg/exp/weights/best.pt --imgsz 320 --batch 1 --include onnx
cd test_yolov5/segment
# 转换kmodel,onnx模型路径请自定义，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/train-seg/exp/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 3.5 在k230上使用MicroPython部署模型

#### 3.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 3.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 3.5.3 YOLOv5 模块

`YOLOv5` 类集成了 `YOLOv5` 的三种任务，包括分类(classify)、检测(detect)、分割(segment)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLOv5` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLOv5
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持三类任务，可选项为'classify'/'detect'/'segment'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv5模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 3.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLOv5
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
    mask_threshold=0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLOv5实例
    yolo=YOLOv5(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 3.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLOv5实例
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

## 4. YOLOv8水果分类

### 4.1 YOLOv8源码及训练环境搭建

`YOLOv8` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

### 4.2 训练数据准备

您可以先创建一个新文件夹 `yolov8`， 请下载提供的示例数据集，示例数据集中包含以三类水果（apple，banana，orange）为场景分别提供了分类、检测和分割数据集。将数据集解压到 `yolov8` 目录下，请使用 `fruits_cls` 作为水果分类任务的数据集。示例数据集中还包含一个旋转目标检测的桌面签字笔场景数据集 `yolo_pen_obb`。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注，分类任务数据不需要使用工具标注，仅按照格式划分目录即可。 将标注后的数据转换成 `yolov8` 官方支持的训练数据格式进行后续训练。

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 4.3 使用YOLOv8训练水果分类模型

在 `yolov8` 目录下执行命令，使用 `yolov8` 训练三类水果分类模型：

```shell
yolo classify train data=datasets/fruits_cls model=yolov8n-cls.pt epochs=100 imgsz=224
```

### 4.4 转换水果分类kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolov8.zip` 解压到 `yolov8` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

按照如下命令，对 `runs/classify/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/classify/train/weights/best.pt format=onnx imgsz=224
cd test_yolov8/classify
# 转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/classify/train/weights/best.onnx --dataset ../test --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

### 4.5 在k230上使用MicroPython部署模型

#### 4.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 4.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 4.5.3 YOLOv8 模块

`YOLOv8` 类集成了 `YOLOv8` 的四种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLOv8` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLOv8
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv8模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 4.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test_apple.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLOv8实例
    yolo=YOLOv8(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 4.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

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
    model_input_size=[224,224]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[640,360]
    confidence_threshold = 0.8
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLOv8实例
    yolo=YOLOv8(task_type="classify",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,debug_mode=0)
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

## 5. YOLOv8水果检测

### 5.1 YOLOv8源码及训练环境搭建

`YOLOv8` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

### 5.2 训练数据准备

您可以先创建一个新文件夹 `yolov8`， 请下载提供的示例数据集，示例数据集中包含以三类水果（apple，banana，orange）为场景分别提供了分类、检测和分割数据集。将数据集解压到 `yolov8` 目录下，请使用 `fruits_yolo` 作为水果检测任务的数据集。示例数据集中还包含一个旋转目标检测的桌面签字笔场景数据集 `yolo_pen_obb`。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注。 自行将标注后的数据转换成 `yolov8` 官方支持的训练数据格式进行后续训练。

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 5.3 使用YOLOv8训练水果检测模型

在 `yolov8` 目录下执行命令，使用 `yolov8` 训练三类水果检测模型：

```shell
yolo detect train data=datasets/fruits_yolo.yaml model=yolov8n.pt epochs=300 imgsz=320
```

### 5.4 转换水果检测kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolov8.zip` 解压到 `yolov8` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

按照如下命令，对 `runs/detect/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/detect
# 转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 5.5 在k230上使用MicroPython部署模型

#### 5.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 5.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 5.5.3 YOLOv8 模块

`YOLOv8` 类集成了 `YOLOv8` 的四种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLOv8` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLOv8
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv8模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 5.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

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

#### 5.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv8
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    nms_threshold=0.45
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
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

## 6. YOLOv8水果分割

### 6.1 YOLOv8源码及训练环境搭建

`YOLOv8` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

### 6.2 训练数据准备

您可以先创建一个新文件夹 `yolov8`， 请下载提供的示例数据集，示例数据集中包含以三类水果（apple，banana，orange）为场景分别提供了分类、检测和分割数据集。将数据集解压到 `yolov8` 目录下，请使用 `fruits_seg` 作为水果分割任务的数据集。示例数据集中还包含一个旋转目标检测的桌面签字笔场景数据集 `yolo_pen_obb`。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注。 自行将标注后的数据转换成 `yolov8` 官方支持的训练数据格式进行后续训练。

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 6.3 使用YOLOv8训练水果分割模型

在 `yolov8` 目录下执行命令，使用 `yolov8` 训练三类水果分割模型：

```shell
yolo segment train data=datasets/fruits_seg.yaml model=yolov8n-seg.pt epochs=100 imgsz=320
```

### 6.4 转换水果分割kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolov8.zip` 解压到 `yolov8` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

按照如下命令，对 `runs/segment/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/segment
# 转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 6.5 在k230上使用MicroPython部署模型

#### 6.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 6.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 6.5.3 YOLOv8 模块

`YOLOv8` 类集成了 `YOLOv8` 的四种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLOv8` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLOv8
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv8模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 6.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

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
    mask_threshold=0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLOv8实例
    yolo=YOLOv8(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 6.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

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

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLOv8实例
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

## 7. YOLOv8旋转目标检测

### 7.1 YOLOv8源码及训练环境搭建

`YOLOv8` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

### 7.2 训练数据准备

您可以先创建一个新文件夹 `yolov8`， 请下载提供的示例数据集，示例数据集中包含以一种旋转目标检测类别（pen）为场景分别提供了数据集。将数据集解压到 `yolov8` 目录下，请使用 `yolo_pen_obb` 作为旋转目标检测任务的数据集。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注。 自行将标注后的数据转换成 `yolov8` 官方支持的训练数据格式进行后续训练。

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 7.3 使用YOLOv8训练旋转目标检测模型

在 `yolov8` 目录下执行命令，使用 `yolov8` 训练一类旋转目标检测模型：

```shell
yolo obb train data=datasets/yolo_pen_obb model=yolov8n-obb.pt epochs=100 imgsz=320
```

### 4.4 转换旋转目标检测kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolov8.zip` 解压到 `yolov8` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

按照如下命令，对 `runs/obb/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/obb/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/obb
# 转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/obb/train/weights/best.onnx --dataset ../test_obb --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 7.5 在k230上使用MicroPython部署模型

#### 7.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 7.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 7.5.3 YOLOv8 模块

`YOLOv8` 类集成了 `YOLOv8` 的四种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLOv8` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLOv8
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv8模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 7.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test_obb.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    confidence_threshold = 0.1
    nms_threshold=0.6
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLOv8实例
    yolo=YOLOv8(task_type="obb",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 7.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv8
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best_yolov8n.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[640,360]
    confidence_threshold = 0.1
    nms_threshold=0.6
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLOv8实例
    yolo=YOLOv8(task_type="obb",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
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

## 8. YOLO11水果分类

### 8.1 YOLO11源码及训练环境搭建

`YOLO11` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

### 8.2 训练数据准备

您可以先创建一个新文件夹 `yolo11`， 请下载提供的示例数据集，示例数据集中包含以三类水果（apple，banana，orange）为场景分别提供了分类、检测和分割数据集。将数据集解压到 `yolo11` 目录下，请使用 `fruits_cls` 作为水果分类任务的数据集。示例数据集中还包含一个旋转目标检测的桌面签字笔场景数据集 `yolo_pen_obb`。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注，分类任务数据不需要使用工具标注，仅按照格式划分目录即可。 将标注后的数据转换成 `yolo11` 官方支持的训练数据格式进行后续训练。

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 8.3 使用YOLO11训练水果分类模型

在 `yolo11` 目录下执行命令，使用 `yolo11` 训练三类水果分类模型：

```shell
yolo classify train data=datasets/fruits_cls model=yolo11n-cls.pt epochs=100 imgsz=224
```

### 8.4 转换水果分类kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolo11.zip` 解压到 `yolo11` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

按照如下命令，对 `runs/classify/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/classify/train/weights/best.pt format=onnx imgsz=224
cd test_yolo11/classify
# 转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/classify/train/weights/best.onnx --dataset ../test --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

### 8.5 在k230上使用MicroPython部署模型

#### 8.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 8.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 8.5.3 YOLO11 模块

`YOLO11` 类集成了 `YOLO11` 的四种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLO11` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLO11
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLO11模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 8.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test_apple.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 8.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[224,224]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[640,360]
    confidence_threshold = 0.8
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLO11实例
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

## 9. YOLO11水果检测

### 9.1 YOLO11源码及训练环境搭建

`YOLO11` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

### 9.2 训练数据准备

您可以先创建一个新文件夹 `yolo11`， 请下载提供的示例数据集，示例数据集中包含以三类水果（apple，banana，orange）为场景分别提供了分类、检测和分割数据集。将数据集解压到 `yolo11` 目录下，请使用 `fruits_yolo` 作为水果检测任务的数据集。示例数据集中还包含一个旋转目标检测的桌面签字笔场景数据集 `yolo_pen_obb`。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注。 自行将标注后的数据转换成 `yolo11` 官方支持的训练数据格式进行后续训练。

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 9.3 使用YOLO11训练水果检测模型

在 `yolo11` 目录下执行命令，使用 `yolo11` 训练三类水果检测模型：

```shell
yolo detect train data=datasets/fruits_yolo.yaml model=yolo11n.pt epochs=300 imgsz=320
```

### 9.4 转换水果检测kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolo11.zip` 解压到 `yolo11` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

按照如下命令，对 `runs/detect/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/detect
# 转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 9.5 在k230上使用MicroPython部署模型

#### 9.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 9.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 9.5.3 YOLO11 模块

`YOLO11` 类集成了 `YOLO11` 的四种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLO11` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLO11
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLO11模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 9.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLO11
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
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="detect",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 9.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    nms_threshold=0.45
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="detect",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
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

## 10. YOLO11水果分割

### 10.1 YOLO11源码及训练环境搭建

`YOLO11` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

### 10.2 训练数据准备

您可以先创建一个新文件夹 `yolo11`， 请下载提供的示例数据集，示例数据集中包含以三类水果（apple，banana，orange）为场景分别提供了分类、检测和分割数据集。将数据集解压到 `yolo11` 目录下，请使用 `fruits_seg` 作为水果分割任务的数据集。示例数据集中还包含一个旋转目标检测的桌面签字笔场景数据集 `yolo_pen_obb`。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注。 自行将标注后的数据转换成 `yolo11` 官方支持的训练数据格式进行后续训练。

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 10.3 使用YOLO11训练水果分割模型

在 `yolo11` 目录下执行命令，使用 `yolo11` 训练三类水果分割模型：

```shell
yolo segment train data=datasets/fruits_seg.yaml model=yolo11n-seg.pt epochs=100 imgsz=320
```

### 10.4 转换水果分割kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolo11.zip` 解压到 `yolo11` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

按照如下命令，对 `runs/segment/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/segment
# 转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 10.5 在k230上使用MicroPython部署模型

#### 10.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 10.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 10.5.3 YOLO11 模块

`YOLO11` 类集成了 `YOLO11` 的四种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLO11` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLO11
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLO11模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 10.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLO11
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
    mask_threshold=0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 10.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="segment",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
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

## 11. YOLO11旋转目标检测

### 11.1 YOLO11源码及训练环境搭建

`YOLO11` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

### 11.2 训练数据准备

您可以先创建一个新文件夹 `yolo11`， 请下载提供的示例数据集，示例数据集中包含以单类旋转笔检测（pen）为场景分别提供了旋转目标检测数据集。将数据集解压到 `yolo11` 目录下，请使用 `yolo_pen_obb` 作为旋转目标检测任务的数据集。

如果您想使用自己的数据集进行训练，可以下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 完成标注。 自行将标注后的数据转换成 `yolo11` 官方支持的训练数据格式进行后续训练。

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/datasets.zip
unzip datasets.zip
```

如果您已下载好数据，请忽略此步骤。

### 11.3 使用YOLO11旋转目标检测模型

在 `yolo11` 目录下执行命令，使用 `yolo11` 训练单类旋转目标检测模型：

```shell
yolo obb train data=datasets/pen_obb.yaml model=yolo11n-obb.pt epochs=100 imgsz=320
```

### 11.4 转换旋转目标检测kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolo11.zip` 解压到 `yolo11` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

按照如下命令，对 `runs/obb/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/obb/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/obb
# 转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/obb/train/weights/best.onnx --dataset ../test_obb --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

### 11.5 在k230上使用MicroPython部署模型

#### 11.5.1 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](../../userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/resource?selected=0-2-1))，在 IDE 中编写代码并运行。

#### 11.5.2 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

#### 11.5.3 YOLO11 模块

`YOLO11` 类集成了 `YOLO11` 的四种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLO11` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLO11
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLO11模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

#### 11.5.4 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test_obb.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    confidence_threshold = 0.1
    nms_threshold=0.6
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="obb",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

#### 11.5.5 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.Utils import *
from libs.YOLO import YOLO11
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    rgb888p_size=[640,360]
    confidence_threshold = 0.1
    nms_threshold=0.6
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
    pl.create()
    display_size=pl.get_display_size()
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="obb",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
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

## 12. kmodel转换验证

不同模型下载的模型转换脚本工具包( `test_yolov5/test_yolov8/test_yolo11` )中包含 kmodel 验证的脚本。

>注意：执行验证脚本需要添加环境变量
>
>**linux**：
>
>```shell
># 下述命令中的路径为安装 nncase 的 Python 环境的路径，请按照您的环境适配修改
>export NNCASE_PLUGIN_PATH=$NNCASE_PLUGIN_PATH:/usr/local/lib/python3.9/site-packages/
>export PATH=$PATH:/usr/local/lib/python3.9/site-packages/
>source /etc/profile
>```
>
>**windows**：
>
>将安装 `nncase` 的 `Python` 环境下的 `Lib/site-packages` 路径添加到环境变量的系统变量 `Path` 中。

### 12.1 对比onnx输出和kmodel输出

#### 12.1.1 生成输入bin文件

进入到 `classify/detect/segment` 目录下，执行下述命令：

```shell
python save_bin.py --image ../test_images/test.jpg --input_width 224 --input_height 224
```

执行脚本将在当前目录下生成bin文件 `onnx_input_float32.bin` 和 `kmodel_input_uint8.bin` ，作为 onnx 模型和 kmodel 模型的输入文件。

#### 12.1.2 对比输出

将转换的模型 `best.onnx`  和 `best.kmodel`  拷贝到 `calssify/detect/segment`  目录下，然后执行验证脚本，执行命令如下：

```shell
python simulate.py --model best.onnx --model_input onnx_input_float32.bin --kmodel best.kmodel --kmodel_input kmodel_input_uint8.bin --input_width 224 --input_height 224
```

得到如下输出：

```shell
output 0 cosine similarity : 0.9985673427581787
```

脚本将依次对比输出的 cosine 相似度，如果相似度在0.99以上，一般认为模型是可用的；否则，需要实际推理测试或者更换量化参数重新导出 kmodel。如果模型有多个输出，会有多行相似度对比信息，比如分割任务，有两个输出，相似度对比信息如下：

```shell
output 0 cosine similarity : 0.9999530911445618
output 1 cosine similarity : 0.9983288645744324
```

### 12.2 onnx模型推理图片

进入 `classify/detect/segment` 目录下，打开 `test_cls_onnx.py`，修改 `main()` 中的参数以适配你的模型，然后执行命令：

```shell
python test_cls_onnx.py
```

命令执行成功后会保存结果到 `onnx_cls_results.jpg` 。

> 检测任务和分割任务类似，分别执行 `test_det_onnx.py` 和 `test_seg_onnx.py` 。

### 12.3 kmodel模型推理图片

进入 `classify/detect/segment` 目录下，打开 `test_cls_kmodel.py` , 修改 `main()` 中的参数以适配你的模型，然后执行命令：

```shell
python test_cls_kmodel.py
```

命令执行成功后会保存结果到 `kmodel_cls_results.jpg` 。

> 检测任务、分割任务和旋转目标检测任务类似，分别执行 `test_det_kmodel.py` 、`test_seg_kmodel.py`、`test_obb_kmodel.py` 。

## 13. 调优指南

当模型在 K230 上运行效果不理想时，一般考虑从阈值设置、模型大小、输入分辨率、量化方法、训练数据质量等方面入手进行调优。

### 13.1 调整阈值

调整置信度阈值、nms 阈值、mask 阈值，在不改变模型的前提下调优部署效果。在检测任务中，提高置信度阈值和降低nms阈值会导致检测框的数量减少，反之，降低置信度阈值和提高nms阈值会导致检测框的数量增多。在分割任务中mask阈值会影响分割区域的划分。您可以根据实际场景先进行调整，找到较优效果下的阈值。

### 13.2 更换模型

选择不同大小的模型以平衡速度、内存占用和准确性。可以根据实际需求选择n/s/m/l的模型进行训练和转换。

下述数据以三类水果数据集训练得到的kmodel为例，在 `01Studio CanMV K230`  开发板上运行***粗测***，实际部署中，后处理时间会受到结果数的影响增加，同时内存管理 `gc.collect()` 的耗时也会随着后处理的复杂程度增加：

| 模型    | 输入分辨率 | 任务 | kpu推理耗时 | kpu推理帧率 | 整帧推理耗时 | 整帧推理帧率 |
| ------- | ---------- | ---- | ----------- | ----------- | ------------ | ------------ |
| yolov5n | 224×224    | cls  | 3ms         | 333fps      | 17ms         | 58fps        |
| yolov5s | 224×224    | cls  | 7ms         | 142fps      | 19ms         | 52fps        |
| yolov5m | 224×224    | cls  | 12ms        | 83fps       | 24ms         | 41fps        |
| yolov5l | 224×224    | cls  | 22ms        | 45fps       | 33ms         | 30fps        |
| yolov8n | 224×224    | cls  | 6ms         | 166fps      | 16ms         | 62fps        |
| yolov8s | 224×224    | cls  | 13ms        | 76fps       | 24ms         | 41fps        |
| yolov8m | 224×224    | cls  | 27ms        | 37fps       | 39ms         | 25fps        |
| yolov8l | 224×224    | cls  | 53ms        | 18fps       | 65ms         | 15fps        |
| yolo11n | 224×224    | cls  | 7ms         | 142fps      | 19ms         | 52fps        |
| yolo11s | 224×224    | cls  | 15ms        | 66fps       | 26ms         | 38fps        |
| yolo11m | 224×224    | cls  | 23ms        | 43fps       | 35ms         | 28fps        |
| yolo11l | 224×224    | cls  | 31ms        | 32fps       | 43ms         | 23fps        |
| yolov5n | 320×320    | det  | 25ms        | 40fps       | 105ms        | 9fps         |
| yolov5s | 320×320    | det  | 30ms        | 33fps       | 109ms        | 9fps         |
| yolov5m | 320×320    | det  | 44ms        | 22fps       | 124ms        | 8fps         |
| yolov5l | 320×320    | det  | 73ms        | 13fps       | 149ms        | 6fps         |
| yolov8n | 320×320    | det  | 25ms        | 40fps       | 62ms         | 16fps        |
| yolov8s | 320×320    | det  | 44ms        | 22fps       | 77ms         | 12fps        |
| yolov8m | 320×320    | det  | 78ms        | 12fps       | 109ms        | 9fps         |
| yolov8l | 320×320    | det  | 126ms       | 7fps        | 160ms        | 6fps         |
| yolo11n | 320×320    | det  | 28ms        | 35fps       | 63ms         | 15fps        |
| yolo11s | 320×320    | det  | 49ms        | 20fps       | 81ms         | 12fps        |
| yolo11m | 320×320    | det  | 77ms        | 12fps       | 112ms        | 8fps         |
| yolo11l | 320×320    | det  | 94ms        | 10fps       | 132ms        | 7fps         |
| yolov5n | 320×320    | seg  | 67ms        | 14fps       | 178ms        | 5fps         |
| yolov5s | 320×320    | seg  | 80ms        | 12fps       | 180ms        | 5fps         |
| yolov5m | 320×320    | seg  | 95ms        | 10fps       | 206ms        | 4fps         |
| yolov5l | 320×320    | seg  | 122ms       | 8fps        | 235ms        | 4fps         |
| yolov8n | 320×320    | seg  | 28ms        | 35fps       | 131ms        | 7fps         |
| yolov8s | 320×320    | seg  | 52ms        | 19fps       | 151ms        | 6fps         |
| yolov8m | 320×320    | seg  | 87ms        | 11fps       | 215ms        | 4fps         |
| yolov8l | 320×320    | seg  | 143ms       | 6fps        | 246ms        | 4fps         |
| yolo11n | 320×320    | seg  | 31ms        | 32fps       | 135ms        | 7fps         |
| yolo11s | 320×320    | seg  | 55ms        | 18fps       | 156ms        | 6fps         |
| yolo11m | 320×320    | seg  | 97ms        | 10fps       | 205ms        | 4fps         |
| yolo11l | 320×320    | seg  | 112ms       | 8fps        | 214ms        | 4fps         |

### 13.3 更改输入分辨率

更改模型的输入分辨率以适配您的场景，较大的分辨率可以提升效果，但会耗费更多的推理时间。

下述数据以三类水果数据集训练得到的kmodel为例，在 `01Studio CanMV K230`  开发板上运行***粗测***，实际部署中，后处理时间会受到结果数的影响增加，同时内存管理 `gc.collect()` 的耗时也会随着后处理的复杂程度增加：

| 模型    | 输入分辨率 | 任务 | kpu推理耗时 | kpu推理帧率 | 整帧推理耗时 | 整帧推理帧率 |
| ------- | ---------- | ---- | ----------- | ----------- | ------------ | ------------ |
| yolov5n | 224×224    | cls  | 3ms         | 333fps      | 17ms         | 58fps        |
| yolov5n | 320×320    | cls  | 5ms         | 200fps      | 18ms         | 55fps        |
| yolov5n | 320×320    | det  | 25ms        | 40fps       | 105ms        | 9fps         |
| yolov5n | 640×640    | det  | 73ms        | 13fps       | 322ms        | 3fps         |
| yolov5n | 320×320    | seg  | 67ms        | 14fps       | 178ms        | 5fps         |
| yolov5n | 640×640    | seg  | 252ms       | 3fps        | 398ms        | 2fps         |
| yolov8n | 224×224    | cls  | 6ms         | 166fps      | 16ms         | 62fps        |
| yolov8n | 320×320    | cls  | 7ms         | 142fps      | 21ms         | 47fps        |
| yolov8n | 320×320    | det  | 25ms        | 40fps       | 62ms         | 16fps        |
| yolov8n | 640×640    | det  | 85ms        | 11fps       | 183ms        | 5fps         |
| yolov8n | 320×320    | seg  | 28ms        | 35fps       | 131ms        | 7fps         |
| yolov8n | 640×640    | seg  | 98ms        | 10fps       | 261ms        | 3fps         |
| yolo11n | 224×224    | cls  | 7ms         | 142fps      | 19ms         | 52fps        |
| yolo11n | 320×320    | cls  | 9ms         | 111fps      | 22ms         | 45fps        |
| yolo11n | 320×320    | det  | 28ms        | 35fps       | 63ms         | 15fps        |
| yolo11n | 640×640    | det  | 92ms        | 10fps       | 191ms        | 5fps         |
| yolo11n | 320×320    | seg  | 31ms        | 32fps       | 135ms        | 7fps         |
| yolo11n | 640×640    | seg  | 104ms       | 9fps        | 263ms        | 3fps         |

### 13.4 修改量化方法

模型转换脚本中提供了3种量化参数，对 `data` 和 `weights` 进行 `uint8` 量化或 `int16` 量化。

在转换kmodel脚本中，通过选择不同的 `ptq_option` 值指定不同的量化方式。

| ptq_option | data  | weights |
| ---------- | ----- | ------- |
| 0          | uint8 | uint8   |
| 1          | uint8 | int16   |
| 2          | int16 | uint8   |

下述数据以三类水果数据集训练得到的kmodel为例，在 `01Studio CanMV K230`  开发板上运行***粗测***，实际部署中，后处理时间会受到结果数的影响增加，同时内存管理 `gc.collect()` 的耗时也会随着后处理的复杂程度增加：

| 模型    | 输入分辨率 | 任务 | 量化参数[data,weights] | kpu推理耗时 | kpu推理帧率 | 整帧推理耗时 | 整帧推理帧率 |
| ------- | ---------- | ---- | ---------------------- | ----------- | ----------- | ------------ | ------------ |
| yolov5n | 320×320    | det  | [uint8,uint8]          | 25ms        | 40fps       | 105ms        | 9fps        |
| yolov5n | 320×320    | det  | [uint8,int16]          | 25ms        | 40fps       | 103ms        | 9fps        |
| yolov5n | 320×320    | det  | [int16,uint8]          | 30ms        | 33fps       | 110ms        | 9fps         |
| yolov8n | 320×320    | det  | [uint8,uint8]          | 25ms        | 40fps       | 62ms         | 16fps         |
| yolov8n | 320×320    | det  | [uint8,int16]          | 27ms        | 37fps       | 65ms         | 15fps         |
| yolov8n | 320×320    | det  | [int16,uint8]          | 33ms        | 30fps       | 72ms         | 13fps         |
| yolo11n | 320×320    | det  | [uint8,uint8]          | 28ms        | 35fps       | 63ms         | 15fps        |
| yolo11n | 320×320    | det  | [uint8,int16]          | 33ms        | 30fps       | 71ms         | 14fps        |
| yolo11n | 320×320    | det  | [int16,uint8]          | 35ms        | 28fps       | 78ms         | 12fps        |

### 13.5 提高数据质量

如果训练结果较差，请提高数据集质量，从数据量、合理的数据分布、标注质量、训练参数设置等方面优化。

### 13.6 调优技巧

- 量化参数在YOLOv8和YOLO11上对效果的影响比YOLOv5大，对比不同量化模型可见；
- 输入分辨率比模型大小对推理速度的影响更大；
- 训练数据和K230摄像头数据分布差异可能会对部署效果造成影响，可以使用K230采集部分数据，自行标注训练；
