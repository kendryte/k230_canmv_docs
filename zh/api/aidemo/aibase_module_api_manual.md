# `AIBase` 模块API手册

## 概述

本手册旨在指导开发人员使用 MicroPython 开发 AI Demo 时，构建完整的 AI 推理流程，实现从加载模型、预处理、推理、获取模型输出、后处理的功能。该模块封装了单个模型的推理过程，将预处理、推理、获取输出操作封装在框架内，用户在开发 AI 应用时只需要关注预处理配置和后处理过程即可。

## API 介绍

### init

**描述**

AIBase 构造函数，初始化 AI 程序获取图像的分辨率和显示相关的参数。

**语法**  

```python
from libs.AIBase import AIBase

aibase=AIBase(kmodel_path="**.kmodel", model_input_size=[224,224], rgb888p_size=[1280,720], debug_mode=0)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| kmodel_path | kmodel 模型路径 | 输入 | 必填 |
| model_input_size | 模型输入分辨率，list类型，包括宽高，如[512,512] | 输入 | 必填 |
| rgb888p_size | AI 程序的输入图像分辨率，list类型，包括宽高，如[1280,720] | 输入 |必填|
| debug_mode   | 调试计时模式，int类型，0为不计时，1为计时 | 输入 | 默认为0 |

**返回值**  

| 返回值 | 描述                            |备注|
|--------|---------------------------------|---|
| AIBase | AIBase实例                  | 该类一般作为父类被子类继承，基于该类编写不同场景的 AI Demo 类 |

### get_kmodel_inputs_num

**描述**

获取kmodel的输入数目。

**语法**  

```python
aibase.get_kmodel_inputs_num()
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| 无  |                   |       |   |

**返回值**  

| 返回值 | 描述                            |
|--------|--------------------------------|
| inputs_num     |  kmodel输入数目         |

### get_kmodel_outputs_num

**描述**

获取kmodel的输出数目。

**语法**  

```python
aibase.get_kmodel_outputs_num()
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| 无  |                   |       |   |

**返回值**  

| 返回值 | 描述                            |
|--------|--------------------------------|
| outputs_num     |  kmodel输出数目        |

### preprocess

**描述**

调用子类中定义的ai2d执行预处理的方法。如果预处理方法无法用ai2d实现或不需要预处理，需要在子类中重写。

**语法**  

```python
aibase.preprocess(input_np)
```

**参数**

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| input_np | `ulab.numpy.ndarray` 格式输入数据，shape 需要和 `Ai2d.build` 中配置的一致 | 输入 | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| input_tensors   | 长度为 1 的 list，元素是 ai2d 预处理后的输出 tensor。该 tensor 由 `Ai2d` 实例持有并**跨帧复用**，调用方不要自行 `release()` |

### inference

**描述**

 使用kmodel进行推理并获取模型输出的方法。

**语法**  

```python
results=aibase.inference(tensors)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| tensors | 输入 tensor 列表，按模型输入顺序排列，list 类型 | 输入 | 必填。tensor 的所有权仍归调用方，本方法不会释放它们 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| results| kmodel推理输出的列表，每个输出为 `ulab.numpy.ndarray` 格式 |

### postprocess

**描述**

后处理接口定义，因为不同的 AI 应用需要不同的后处理步骤，该方法需要在子类重写。

**语法**  

```python
aibase.postprocess(results)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| results | 模型输出的 `ulab.numpy.ndarray` 列表，按输出索引顺序排列 | 输入 | 必填。基类不做任何解析，由子类重写 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无    | 基类实现直接返回 `None`；子类重写后应返回本任务的后处理结果，该返回值会由 `run()` 原样传出 |

### run

**描述**

单模型推理全部过程，包含预处理、推理、获取输出、后处理，返回后处理输出，用于在 Display 绘制结果。

**语法**  

```python
res=aibase.run(input_np)
```

**参数**

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| input_np | `ulab.numpy.ndarray` 格式输入数据，shape 需要和 `Ai2d.build` 中配置的一致 | 输入 | 必填。该数据会被保存为 `self.cur_img`，在本次处理完成前必须保持有效 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| res    | 子类 `postprocess()` 的返回值，即本任务的后处理结果，可直接交给 `draw_result()` 使用 |

### deinit

**描述**

AIBase 反初始化方法，按顺序释放 kpu 实例、输入/输出 tensor 和 Ai2d 预处理资源，并把内存归还给 nncase 内存池。AI 程序退出或需要切换模型时**必须调用**。

具体做法是：先释放 kpu（解释器持有输入/输出 tensor 的引用，必须先于 tensor 释放），再清空 tensor 列表和结果列表，然后调用 `ai2d.deinit()`，最后执行 `gc.collect()` + `nncase_runtime.shrink_memory_pool()` + `gc.collect()`。

**语法**  

```python
aibase.deinit()
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| 无  |                   |       |   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无    |                                  |

```{admonition} 提示
:class: note
- **无需再手动调用 `gc.collect()` 和 `shrink_memory_pool()`**，`deinit()` 内部已经做了。
- **重复调用是安全的**，第二次调用会直接返回。
- 若某个原生资源释放失败，AIBase 会保留该资源的引用以便下次 `deinit()` 重试，并在其余资源都尝试释放后抛出第一个失败的异常。
- 子类如果额外创建了资源（例如**多个** `Ai2d` 实例、自行 `nn.from_numpy()` 创建的 tensor），需要重写 `deinit()` 先释放这些资源，再调用 `super().deinit()`。
```

**子类重写示例**

```python
class MyMultiStageApp(AIBase):
    def __init__(self, ...):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        self.ai2d_pad = Ai2d(debug_mode)      # 第一级预处理
        self.ai2d_crop = Ai2d(debug_mode)     # 第二级预处理
        self.ai2d = self.ai2d_pad             # 交给父类管理其中一个

    # 重写 deinit，释放父类不知道的那个 ai2d
    def deinit(self):
        with ScopedTiming("deinit", self.debug_mode > 0):
            self.ai2d_crop.deinit()
            super().deinit()      # 父类负责释放 kpu、tensor 和 self.ai2d
```

## 示例程序

```{attention}
AIBase 类基本上不单独使用，其作为 AI Demo 应用开发的父类，提供基础接口，子类继承 AIBase， 按照任务类型重写部分方法实现具体场景的开发。开发时需要在子类定义 draw_result 方法按照任务绘制结果。 
```

以下为人脸检测示例程序：

```python
from libs.PipeLine import PipeLine
from libs.Utils import *
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
import os,sys,gc,time,random,utime
import ujson
from media.media import *
from time import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import aidemo

# 自定义人脸检测类，继承自AIBase基类
class FaceDetectionApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, anchors, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)  # 调用基类的构造函数
        self.kmodel_path = kmodel_path  # 模型文件路径
        self.model_input_size = model_input_size  # 模型输入分辨率
        self.confidence_threshold = confidence_threshold  # 置信度阈值
        self.nms_threshold = nms_threshold  # NMS（非极大值抑制）阈值
        self.anchors = anchors  # 锚点数据，用于目标检测
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]  # sensor给到AI的图像分辨率，并对宽度进行16的对齐
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]  # 显示分辨率，并对宽度进行16的对齐
        self.debug_mode = debug_mode  # 是否开启调试模式
        self.ai2d = Ai2d(debug_mode)  # 实例化Ai2d，用于实现模型预处理
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)  # 设置Ai2d的输入输出格式和类型

    # 配置预处理操作，这里使用了pad和resize，Ai2d支持crop/shift/pad/resize/affine，具体代码请打开/sdcard/libs/AI2D.py查看
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):  # 计时器，如果debug_mode大于0则开启
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size  # 初始化ai2d预处理配置，默认为sensor给到AI的尺寸，可以通过设置input_image_size自行修改输入尺寸
            top, bottom, left, right = self.get_padding_param()  # 获取padding参数
            self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])  # 填充边缘
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)  # 缩放图像
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])  # 构建预处理流程

    # 自定义当前任务的后处理，results是模型输出array列表，这里使用了aidemo库的face_det_post_process接口
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
            post_ret = aidemo.face_det_post_process(self.confidence_threshold, self.nms_threshold, self.model_input_size[1], self.anchors, self.rgb888p_size, results)
            if len(post_ret) == 0:
                return post_ret
            else:
                return post_ret[0]

    # 绘制检测结果到画面上
    def draw_result(self, pl, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            if dets:
                pl.osd_img.clear()  # 清除OSD图像
                for det in dets:
                    # 将检测框的坐标转换为显示分辨率下的坐标
                    x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                    x = x * self.display_size[0] // self.rgb888p_size[0]
                    y = y * self.display_size[1] // self.rgb888p_size[1]
                    w = w * self.display_size[0] // self.rgb888p_size[0]
                    h = h * self.display_size[1] // self.rgb888p_size[1]
                    pl.osd_img.draw_rectangle(x, y, w, h, color=(255, 255, 0, 255), thickness=2)  # 绘制矩形框
            else:
                pl.osd_img.clear()

    # 获取padding参数
    def get_padding_param(self):
        dst_w = self.model_input_size[0]  # 模型输入宽度
        dst_h = self.model_input_size[1]  # 模型输入高度
        ratio_w = dst_w / self.rgb888p_size[0]  # 宽度缩放比例
        ratio_h = dst_h / self.rgb888p_size[1]  # 高度缩放比例
        ratio = min(ratio_w, ratio_h)  # 取较小的缩放比例
        new_w = int(ratio * self.rgb888p_size[0])  # 新宽度
        new_h = int(ratio * self.rgb888p_size[1])  # 新高度
        dw = (dst_w - new_w) / 2  # 宽度差
        dh = (dst_h - new_h) / 2  # 高度差
        top = int(round(0))
        bottom = int(round(dh * 2 + 0.1))
        left = int(round(0))
        right = int(round(dw * 2 - 0.1))
        return top, bottom, left, right

if __name__ == "__main__":
    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定"hdmi"/"lcd"/"st7701"等
    display_mode="auto"
    # None表示使用屏驱动的默认分辨率；需要指定时填[宽, 高]
    display_size=None
    # k230保持不变，k230d可调整为[640,360]
    rgb888p_size = [1920, 1080]
    # 设置模型路径和其他参数
    kmodel_path = "/sdcard/examples/kmodel/face_detection_320.kmodel"
    # 其它参数
    confidence_threshold = 0.5
    nms_threshold = 0.2
    anchor_len = 4200
    det_dim = 4
    anchors_path = "/sdcard/examples/utils/prior_data_320.bin"
    anchors = np.fromfile(anchors_path, dtype=np.float)
    anchors = anchors.reshape((anchor_len, det_dim))

    # 初始化PipeLine，rgb888p_size为传给AI的图像分辨率，display_size为显示分辨率
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode, display_size=display_size)
    # 创建PipeLine，可按需传入sensor_id选择摄像头，例如pl.create(sensor_id=2)
    pl.create()  # 创建PipeLine实例
    display_size = pl.get_display_size()        # create之后再取实际显示分辨率
    # 初始化自定义人脸检测实例
    face_det = FaceDetectionApp(kmodel_path, model_input_size=[320, 320], anchors=anchors, confidence_threshold=confidence_threshold, nms_threshold=nms_threshold, rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    face_det.config_preprocess()  # 配置预处理
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            res = face_det.run(img)         # 推理当前帧
            face_det.draw_result(pl, res)   # 绘制结果
            pl.show_image()                 # 显示结果
            gc.collect()                    # 垃圾回收
    face_det.deinit()                       # 反初始化
    pl.destroy()                            # 销毁PipeLine实例
```

## 开发Tips

对于开发中常见的数据类型转换，这里给出对应的示例供参考。

> **Tips:**
>
> Image对象转ulab.numpy.ndarray：
>
> ```python
> import image
> img.to_rgb888().to_numpy_ref() #返回的array是HWC排布
> ```
>
> ulab.numpy.ndarray转Image对象：
>
> ```python
> import ulab.numpy as np
> import image
> img_np = np.zeros((height,width,4),dtype=np.uint8)
> img = image.Image(width, height, image.ARGB8888, alloc=image.ALLOC_REF,data =img_np)
> ```
>
> ulab.numpy.ndarray转tensor类型：
>
> ```python
> import ulab.numpy as np
> import nncase_runtime as nn
> img_np = np.zeros((height,width,4),dtype=np.uint8)
> tensor = nn.from_numpy(img_np)
> ```
>
> tensor 类型转ulab.numpy.ndarray：
>
> ```python
> import ulab.numpy as np
> import nncase_runtime as nn
> img_np=tensor.to_numpy()
> ```
