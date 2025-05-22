# 5.4 YOLO 模块 API 手册

## 1. 概述

本手册旨在指导开发人员使用 YOLO 模块部署使用YOLOv5、YOLOv8和YOLO11训练并转换的模型，模型支持分类、检测、分割三类任务。帮助用户快速对接YOLO源码，将训练的模型在K230上部署运行。YOLO 使用示例参考文档：[YOLO大作战](../../example/ai/YOLO大作战.md)

## 2. API 介绍

### 2.1 YOLOv5 类

#### 2.1.1 构造函数

**描述**

封装的 `YOLOv5` 模块构造函数，初始化 `YOLOv5` 类型获取 `YOLOv5` 实例。

**语法**  

```python
from libs.YOLO import YOLOv5

yolo=YOLOv5(task_type="classify",mode="image",kmodel_path="yolov5_det.kmodel",labels=["apple","banana","orange"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,nms_thresh=0.25,max_boxes_num=50,debug_mode=0)
```

**参数**  

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持三类任务，可选项为'classify'/'detect'/'segment'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv5模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float [0~1] |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float [0~1] |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float [0~1] |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int [0/1]   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| YOLOv5 | YOLOv5实例                  |

#### 2.1.2 config_preprocess

**描述**

YOLOv5 预处理配置函数。

**语法**  

```python
yolo.config_preprocess()
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| 无  |                   |       |   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

#### 2.1.3 run

**描述**

推理一帧图像，返回推理结果给 `draw_result` 方法使用。分类任务返回的是类别索引和分数，检测任务返回的是检测框位置、分数、类别索引的列表，分割任务返回的是 mask 结果和检测框位置、分数、类别索引的列表。

**语法**  

```python
res=yolo.run(img)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| img   | 格式为ulab.numpy.ndarray的待推理图片，或从视频流中通过 `get_frame` 获取的一帧图像               |   输入    |   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| res     | 模型后处理结果，不同任务返回值不同，分类任务返回的是类别索引和分数，检测任务返回的是检测框位置、分数、类别索引的列表，分割任务返回的是 mask 结果和检测框位置、分数、类别索引列表。|

#### 2.1.4 draw_result

**描述**

将在屏幕或图像上绘制的 `YOLOv5` 推理结果。

**语法**  

```python
yolo.draw_result(res,img_ori)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| res  | `YOLOv5` 的推理结果                   |   输入    |   |
| img_ori  | 待绘制Image实例                   |   输入    | 来自 `read_img` 或 `pl.osd_img`  |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

#### 2.1.5 示例程序

以下给出 `YOLOv5` 检测任务示例程序：

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/sdcard/examples/utils/test_fruit.jpg"
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolov5n_320.kmodel"
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

上述代码给出了使用 `YOLOv5` 进行图片推理的代码。

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolov5n_320.kmodel"
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

上述代码给出了使用 `YOLOv5` 进行视频推理的代码。

### 2.2 YOLOv8 类

#### 2.2.1 构造函数

**描述**

封装的 `YOLOv8` 模块构造函数，初始化 `YOLOv8` 类型获取 `YOLOv8` 实例。

**语法**  

```python
from libs.YOLO import YOLOv8

yolo=YOLOv8(task_type="classify",mode="image",kmodel_path="yolov8_det.kmodel",labels=["apple","banana","orange"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,nms_thresh=0.25,max_boxes_num=50,debug_mode=0)
```

**参数**  

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv8模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float [0~1] |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float [0~1] |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float [0~1] |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int [0/1]   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| YOLOv8 | YOLOv8实例                  |

#### 2.2.2 config_preprocess

**描述**

YOLOv8 预处理配置函数。

**语法**  

```python
yolo.config_preprocess()
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| 无  |                   |       |   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

#### 2.2.3 run

**描述**

推理一帧图像，返回推理结果给 `draw_result` 方法使用。分类任务返回的是类别索引和分数，检测任务返回的是检测框位置、分数、类别索引的列表，分割任务返回的是 mask 结果和检测框位置、分数、类别索引的列表。

**语法**  

```python
res=yolo.run(img)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| img   | 格式为ulab.numpy.ndarray的待推理图片，或从视频流中通过 `get_frame` 获取的一帧图像               |   输入    |   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| res     | 模型后处理结果，不同任务返回值不同，分类任务返回的是类别索引和分数，检测任务返回的是检测框位置、分数、类别索引的列表，分割任务返回的是 mask 结果和检测框位置、分数、类别索引列表。|

#### 2.2.4 draw_result

**描述**

将在屏幕或图像上绘制的 `YOLOv8` 推理结果。

**语法**  

```python
yolo.draw_result(res,img_ori)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| res  | `YOLOv8` 的推理结果                   |   输入    |   |
| img_ori  | 待绘制Image实例                   |   输入    | 来自 `read_img` 或 `pl.osd_img`  |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

#### 2.2.5 示例程序

以下给出 `YOLOv8` 分类任务示例程序：

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/sdcard/examples/utils/test_fruit.jpg"
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolov8n_320.kmodel"
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

上述代码给出了使用 `YOLOv8` 进行图片推理的代码。

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.YOLO import YOLOv8
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolov8n_320.kmodel"
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

上述代码给出了使用 `YOLOv8` 进行视频推理的代码。

### 2.3 YOLO11 类

#### 2.3.1 构造函数

**描述**

封装的 YOLO11 模块构造函数，初始化 YOLO11 类型获取 YOLO11 实例。

**语法**  

```python
from libs.YOLO import YOLO11

yolo=YOLO11(task_type="segment",mode="image",kmodel_path="yolo11_det.kmodel",labels=["apple","banana","orange"],rgb888p_size=[1280,720],model_input_size=[320,320],conf_thresh=0.5,nms_thresh=0.25,mask_thresh=0.5,max_boxes_num=50,debug_mode=0)
```

**参数**  

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLO11模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float [0~1] |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float [0~1] |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float [0~1] |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int [0/1]   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| YOLO11 | YOLO11实例                  |

#### 2.3.2 config_preprocess

**描述**

YOLO11 预处理配置函数。

**语法**  

```python
yolo.config_preprocess()
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| 无  |                   |       |   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

#### 2.3.3 run

**描述**

推理一帧图像，返回推理结果给 `draw_result` 方法使用。分类任务返回的是类别索引和分数，检测任务返回的是检测框位置、分数、类别索引的列表，分割任务返回的是 mask 结果和检测框位置、分数、类别索引的列表。

**语法**  

```python
res=yolo.run(img)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| img   | 格式为ulab.numpy.ndarray的待推理图片，或从视频流中通过 `get_frame` 获取的一帧图像               |   输入    |   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| res     | 模型后处理结果，不同任务返回值不同，分类任务返回的是类别索引和分数，检测任务返回的是检测框位置、分数、类别索引的列表，分割任务返回的是 mask 结果和检测框位置、分数、类别索引列表。|

#### 2.3.4 draw_result

**描述**

将在屏幕或图像上绘制的 `YOLO11` 推理结果。

**语法**  

```python
yolo.draw_result(res,img_ori)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| res  | `YOLO11` 的推理结果                   |   输入    |   |
| img_ori  | 待绘制Image实例                   |   输入    | 来自 `read_img` 或 `pl.osd_img`  |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

#### 2.3.5 示例程序

以下给出 `YOLO11` 分割任务示例程序：

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/sdcard/examples/utils/test_fruit.jpg"
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolo11n_320.kmodel"
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

上述代码给出了使用 `YOLO11` 进行图片推理的代码。

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/sdcard/examples/kmodel/fruit_det_yolo11n_320.kmodel"
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

上述代码给出了使用 `YOLO11` 进行视频推理的代码。
