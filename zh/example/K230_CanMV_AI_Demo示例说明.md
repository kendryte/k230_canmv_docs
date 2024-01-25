# K230 CanMV AI Demo示例说明

![cover](images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍如何写AI Demo。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

## 一、概述

本文档包括27个AI Demo，这些示例程序都实现从摄像头采集数据、kpu推理到显示器展示的流程，应用到了K230 CanMV 平台的多个硬件模块：AI2D，KPU，Camera，Display等。

这些AI Demo分为两种类型：单模型、多模型，涵盖物体、人脸、人手、人体、车牌、OCR，KWS等方向；参考该文档，k230用户可以更快上手K230 AI应用的开发，实现预期效果。

更多AI Demo后续即将解锁。

| 单模型示例   | 多模型示例     |
| ------------ | -------------- |
| 人脸检测     | 人脸关键点检测 |
| COCO目标检测 | 人脸识别       |
| yolov8-seg   | 人脸姿态角     |
| 车牌检测     | 人脸解析       |
| OCR检测      | 车牌识别       |
| 手掌检测     | 石头剪刀布     |
| 人体检测 | OCR识别    |
| 人体姿态估计 | 手掌关键点检测 |
| KWS | 静态手势识别   |
| 跌倒检测 | 人脸mesh   |
|  | 注视估计 |
|  | 动态手势识别 |
|  | 单目标跟踪 |
|  | 隔空放大 |
|  | 拼图游戏 |
|  | 基于关键点的手势识别 |
|  | 自学习 |

## 二、AI Demo单模型示例解析

### 1.分模块解析

#### 1.1 模块引入

```python
import ulab.numpy as np          #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn      #nncase运行时模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *       #摄像头模块
from media.display import *      #显示模块
from media.media import *        #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import aidemo                #aidemo模块，封装ai demo相关后处理、画图操作
import image                 #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                  #时间统计
import gc                    #垃圾回收模块
```

| 模块           | 说明                             |
| ---------------------- | ------------------------------------------------------------ |
| image（必选）      | 图像模块，主要用于读取、图像绘制元素（框、点等）等操作       |
| media.camera（必选）   | [摄像头模块](../api/mpp/K230_CanMV_Camera%E6%A8%A1%E5%9D%97API%E6%89%8B%E5%86%8C.md) |
| media.display （必选） | [显示模块](../api/mpp/K230_CanMV_Display%E6%A8%A1%E5%9D%97API%E6%89%8B%E5%86%8C.md) |
| media.media（必选）    | [媒体软件抽象模块，主要封装媒体数据链路以及媒体缓冲区](../api/mpp/K230_CanMV_Media%E6%A8%A1%E5%9D%97API%E6%89%8B%E5%86%8C.md) |
| nncase_runtime（必选） | nncase运行时模块，  封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作 |
| aidemo（可选）     | 封装部分ai demo相关后处理、复杂画图操作              |
| aicube（可选）     | 封装基于ai cube训练的检测分割等任务的后处理          |
| ulab.numpy  （可选）   | [类似python numpy操作，但也会有一些接口不同](https://micropython-ulab.readthedocs.io/en/latest/ ) |
| time（可选）       | 时间统计                             |
| gc（可选）         | [垃圾回收模块](https://docs.micropython.org/en/latest/library/gc.html)，自动回收 |

#### 1.2 参数配置

不同模型（kmodel）根据自己需要设置参数信息，包括显示、AI原图、kmodel参数、文件配置、调试模式等。

```python
#********************for config.py********************
# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)           # 显示宽度要求16位对齐
DISPLAY_HEIGHT = 1080

# ai原图分辨率，sensor默认出图为16:9，若需不形变原图，最好按照16:9比例设置宽高
OUT_RGB888P_WIDTH = ALIGN_UP(1024, 16)           # ai原图宽度要求16位对齐
OUT_RGB888P_HEIGH = 576

# kmodel相关参数设置
# kmodel输入shape,NCHW,RGB
kmodel_input_shape = (1,3,320,320)
# ai原图padding
rgb_mean = [104,117,123]   
# 其它kmodel参数
......

# 文件配置
root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/face_detection_320.kmodel'   # kmodel路径
anchors_path = root_dir + 'utils/prior_data_320.bin'      # kmodel anchor
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0
```

#### 1.3 时间统计工具

ScopedTiming 类是一个用来测量代码块执行时间的上下文管理器。上下文管理器通过定义包含 `__enter__` 和 `__exit__` 方法的类来创建。当在 with 语句中使用该类的实例时，`__enter__` 在进入 with 块时被调用，`__exit__` 在离开时被调用。

```python
#********************for scoped_timing.py********************
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")
```

**使用示例：**

```python
import ulab.numpy as np
debug_mode = 1
a = np.ones(10**6, dtype=np.float)
with ScopedTiming("kpu_pre_process",debug_mode > 0):
    a = a * 1.000001 + 0.000001
```

#### 1.4 nncase使用：ai2d

ai2d主要是用于对输入原图预处理进行硬件加速，然后把预处理结果喂给kmodel。

##### （1）ai2d基础用法示例

```python
import nncase_runtime as nn
# 注：此示例仅为基础用法，其它demo可根据实际情况调整
def get_pad_one_side_param():
    # 右padding或下padding，获取padding参数
    dst_w = kmodel_input_shape[3]                         # kmodel输入宽（w）
    dst_h = kmodel_input_shape[2]                          # kmodel输入高（h）

    # OUT_RGB888P_WIDTH：原图宽（w）
    # OUT_RGB888P_HEIGH：原图高（h）
    # 计算最小的缩放比例，等比例缩放
    ratio_w = dst_w / OUT_RGB888P_WIDTH
    ratio_h = dst_h / OUT_RGB888P_HEIGH
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h
    # 计算经过缩放后的新宽和新高
    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGH)

    # 计算需要添加的padding，以使得kmodel输入的宽高和原图一致
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2
    # 四舍五入，确保padding是整数
    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

def ai2d_demo(rgb888p_img):
    # 初始化AI2D模块
    # rgb888p_img为Image对象
    with ScopedTiming("ai2d_init",debug_mode > 0):
    # (1)创建ai2d实例
    ai2d = nn.ai2d()
    # (2)设置ai2d参数
    # 设置ai2d输入、输出格式和数据类型
    ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
              nn.ai2d_format.NCHW_FMT,
              np.uint8, np.uint8)
    # 设置padding参数
    ai2d.set_pad_param(True, get_pad_one_side_param(), 0, rgb_mean)
    # 设置resize参数
    ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
        
        # （3）根据ai2d参数构建ai2d_builder
    global ai2d_builder
    ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], kmodel_input_shape)
        
        # （4）创建ai2d输出，用于保存ai2d输出结果
    global ai2d_output_tensor
    data = np.ones(kmodel_input_shape, dtype=np.uint8)
    ai2d_output_tensor = nn.from_numpy(data)
        
        # （5）创建ai2d输入对象，并将对象从numpy转换为tensor
    ai2d_input = rgb888p_img.to_numpy_ref()
    ai2d_input_tensor = nn.from_numpy(ai2d_input)
        
        # （6）根据输入，ai2d参数，运行得到ai2d输出，将结果保存到ai2d_output_tensor中
    ai2d_builder.run(ai2d_input_tensor, ai2d_output_tensor)
        # dump ai2d结果查看，查看结果是否正确（此时保存格式为nn.ai2d_format.NCHW_FMT，NCHW、RGB格式，需要转换为图片格式后再查看）
        #ai2d_out_data = fp_ai2d_output_tensor.to_numpy()     #
    #with open("/sdcard/app/ai2d_out.bin", "wb") as file:
    #file.write(ai2d_out_data.tobytes())
        
        # （7）删除 ai2d、ai2d_input_tensor、ai2d_output_tensor、ai2d_builder 变量，释放对它所引用对象的内存引用
    del ai2d
    del ai2d_input_tensor
    del ai2d_output_tensor
    del ai2d_builder
```

##### （2）ai2d示例用法一：ai2d参数固定

**ai2d参数固定**：针对视频流的不同帧，ai2d参数固定使用示例

eg：人脸检测模型，对于模型输入，需要将原图进行预处理（padding、resize）之后，然后再喂给kmodel；若是原图从sensor中取出，分辨率固定，则padding的上下左右位置是固定的，此时可以使用以下模板对原图进行预处理

```python
import nncase_runtime as nn
#ai2d：ai2d实例
#ai2d_input_tensor：ai2d输入
#ai2d_output_tensor：ai2d输出
#ai2d_builder：根据ai2d参数，构建的ai2d_builder对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder

def get_pad_one_side_param():
    # 右padding或下padding，获取padding参数
    .....
    return [0, 0, 0, 0, top, bottom, left, right]

def ai2d_init():
    # 初始化AI2D模块
    with ScopedTiming("ai2d_init",debug_mode > 0):
        global ai2d
        # （1）创建ai2d实例
        ai2d = nn.ai2d()
        # （2）设置ai2d参数
        # 设置ai2d输入、输出格式和数据类型
        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                           nn.ai2d_format.NCHW_FMT,
                           np.uint8, np.uint8)
        # 设置padding参数
        ai2d.set_pad_param(True, get_pad_one_side_param(), 0, rgb_mean)
        # 设置resize参数
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            
            # （3）创建ai2d输出，用于保存ai2d输出结果
        global ai2d_output_tensor
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_output_tensor = nn.from_numpy(data)
            
            # （4）根据ai2d参数构建ai2d_builder，因为ai2d的参数不变，因此只需创建一次ai2d_builder
        global ai2d_builder
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], kmodel_input_shape)


def ai2d_run(rgb888p_img):
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d_input_tensor,ai2d_output_tensor
        # （1）创建ai2d输入对象，并将对象从numpy转换为tensor
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)
            
            # （2）根据输入，ai2d参数，运行得到ai2d输出，将结果保存到ai2d_output_tensor中
        ai2d_builder.run(ai2d_input_tensor, ai2d_output_tensor)

def ai2d_release():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor
        # 删除 ai2d_input_tensor 变量，释放对它所引用对象的内存引用
        del ai2d_input_tensor
```

**使用示例：**

```python
ai2d_init()                                     # ai2d初始化
while True:
    rgb888p_img = camera_read(CAM_DEV_ID_0)     # 从sensor拿到一帧图像
    ai2d_run(rgb888p_img)                    # 对sensor原图像预处理
    ai2d_release()                    # 释放ai2d_input_tensor，因为每帧原图不同，ai2d_input_tensor指向的对象都会改变，所以每次都需释放内存
......
global ai2d,ai2d_output_tensor,ai2d_builder  #只需释放一次
del ai2d           # 释放ai2d，因为ai2d指向的对象是固定的               
del ai2d_output_tensor # 释放ai2d_output_tensor，因为ai2d_output_tensor指向的对象是固定的
del ai2d_builder       # 释放ai2d_builder，因为ai2d的参数未变，ai2d_builder指向的对象是固定的
```

##### （3）ai2d示例用法二：ai2d参数不固定

**ai2d参数不固定**：针对视频流的不同帧，ai2d参数实时变化

eg：人脸关键点检测模型，对于模型输入，需要将原图进行预处理（affine）之后，然后再喂给kmodel；即使原图从sensor中取出，分辨率固定，但是affine的参数是实时改变的，此时可以使用以下模板对原图进行预处理。

```python
import nncase_runtime as nn
# fld_ai2d：人脸关键点ai2d实例
# fld_ai2d_input_tensor：人脸关键点ai2d输入
# fld_ai2d_output_tensor：人脸关键点ai2d输出
# fld_ai2d_builder：根据人脸关键点ai2d参数，构建的人脸关键点ai2d_builder对象
global fld_ai2d,fld_ai2d_input_tensor,fld_ai2d_output_tensor,fld_ai2d_builder
# affine参数
global matrix_dst

def get_affine_matrix(bbox):
    # 根据人脸检测框获取仿射矩阵，用于将边界框映射到模型输入空间
    with ScopedTiming("get_affine_matrix", debug_mode > 1):
    ......
    return matrix_dst

def fld_ai2d_init():
    with ScopedTiming("fld_ai2d_init",debug_mode > 0):
        #for face landmark
        global fld_ai2d
        # （1）创建人脸关键点ai2d对象
        fld_ai2d = nn.ai2d()
    
        global fld_ai2d_output_tensor
        # （2）创建人脸关键点ai2d_output_tensor对象
        data = np.ones(fld_kmodel_input_shape, dtype=np.uint8)
        fld_ai2d_output_tensor = nn.from_numpy(data)

def fld_ai2d_run(rgb888p_img,det):
    # 人脸关键点ai2d运行，rgb888p_img是Image对象，det为人脸检测框
    with ScopedTiming("fld_ai2d_run",debug_mode > 0):
        global fld_ai2d,fld_ai2d_input_tensor,fld_ai2d_output_tensor
        # （1）创建ai2d_input_tensor
        # Image对象转换为numpy对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        # 将numpy对象转换为ai2d_tensor
        fld_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        
        # （2）设置ai2d参数
        # 设置ai2d输入、输出格式、数据类型
        fld_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                           nn.ai2d_format.NCHW_FMT,
                           np.uint8, np.uint8)
        global matrix_dst
        # 根据检测框获取affine参数
        matrix_dst = get_affine_matrix(det)
        affine_matrix = [matrix_dst[0][0],matrix_dst[0][1],matrix_dst[0][2],
            matrix_dst[1][0],matrix_dst[1][1],matrix_dst[1][2]]
        # 设置affine参数
        fld_ai2d.set_affine_param(True,nn.interp_method.cv2_bilinear,0, 0, 127, 1,affine_matrix)
    
        global fld_ai2d_builder
        # （3）根据新的ai2d affine参数，创建新的ai2d_builder对象
        fld_ai2d_builder = fld_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fld_kmodel_input_shape)
        # （4）ai2d_builder运行，将结果保存到fld_ai2d_output_tensor
        fld_ai2d_builder.run(fld_ai2d_input_tensor, fld_ai2d_output_tensor)

def fld_ai2d_release():
    with ScopedTiming("fld_ai2d_release",debug_mode > 0):
        global fld_ai2d_input_tensor,fld_ai2d_builder
        del fld_ai2d_input_tensor  #删除fld_ai2d_input_tensor变量，释放对它所引用对象的内存引用
        del fld_ai2d_builder       #删除fld_ai2d_builder变量，释放对它所引用对象的内存引用
```

**使用示例：**

```python
# ************main************    
fld_ai2d_init()                                 # ai2d初始化
while True:
    rgb888p_img = camera_read(CAM_DEV_ID_0)     # 从sensor拿到一帧图像
    fld_ai2d_run(rgb888p_img,det)                # 根据det，对sensor原图预处理
    fld_ai2d_release()                    # 释放ai2d_input_tensor、ai2d_builder，因为每帧原图不同，ai2d_input_tensor指向的对象都会改变，所以每次都需释放内存;因为ai2d的参数实时改变，ai2d_builder对象需要每次创建，也需要每次都释放内存
......
global fld_ai2d,fld_ai2d_output_tensor          #只需释放一次
del fld_ai2d           # 释放fld_ai2d，因为ai2d指向的对象是固定的             
del fld_ai2d_output_tensor # 释放fld_ai2d_output_tensor，因为fld_ai2d_output_tensor指向的对象是固定的
```

#### 1.5 nncase使用：kpu

##### （1）kpu基础用法

```python
import nncase_runtime as nn

# （1）初始化kpu对象
kpu_obj = nn.kpu()
# （2）加载kmodel
kpu_obj.load_kmodel(kmodel_file)

# （3）设置kpu输入
kmodel_input_shape = (1,3,320,320)
data = np.ones(kmodel_input_shape, dtype=np.uint8)
kmodel_input_tensor = nn.from_numpy(data)
kpu_obj.set_input_tensor(0, kmodel_input_tensor)

# （4）kpu运行
kpu_obj.run()

# （5）获取kpu模型输出
results = []
for i in range(current_kmodel_obj.outputs_size()):
    data = current_kmodel_obj.get_output_tensor(i)
    result = data.to_numpy()
    del data #tensor对象用完之后释放内存
    results.append(result)

#（6）kpu后处理
......

# （7）释放kpu对象
del kpu_obj
nn.shrink_memory_pool()
```

##### （2）kpu示例用法：kpu配合ai2d使用

```python
import nncase_runtime as nn
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder  #ai2d相关对象
global current_kmodel_obj                      #当前kpu对象

def kpu_init(kmodel_file):
    # 初始化kpu对象，并加载kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        # （1）初始化kpu对象
        kpu_obj = nn.kpu()
        # （2）加载kmodel
        kpu_obj.load_kmodel(kmodel_file)
            # （3）ai2d初始化，模型输入需要预处理的情况下，kpu需要配合ai2d使用
        ai2d_init()
    return kpu_obj

def kpu_pre_process(rgb888p_img):
    # kpu预处理，rgb888p_img是Image对象，原图
    # （1）ai2d运行，对原图进行预处理
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_output_tensor
        # （2）将ai2d输出tensor设置为kpu模型输入
        current_kmodel_obj.set_input_tensor(0, ai2d_output_tensor)

def kpu_get_output():
    # 获取kpu输出
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取kpu输出，将输出转换为numpy格式，以便进行后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data             #tensor对象用完之后释放内存
            results.append(result)
    return results
    
def kpu_run(kpu_obj,rgb888p_img):
    # kpu推理运行
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）kpu预处理
    kpu_pre_process(rgb888p_img)
    with ScopedTiming("kpu_run",debug_mode > 0):
        # （2）kpu运行
        kpu_obj.run()
    # （3）ai2d释放
    ai2d_release()
    # （4）获取模型输出
    results = kpu_get_output()
    # （5）kpu后处理，获取检测结果
    with ScopedTiming("kpu_post",debug_mode > 0):
        post_ret = aidemo.face_det_post_process(confidence_threshold,nms_threshold,kmodel_input_shape[2],prior_data,[OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH],results)
    
    # （6）返回人脸检测框
    if len(post_ret)==0:
        return post_ret
    else:
        return post_ret[0]

# kpu释放
def kpu_deinit():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        global ai2d,ai2d_output_tensor
        del ai2d                    #删除ai2d变量，释放对它所引用对象的内存引用
        del ai2d_output_tensor        #删除ai2d_output_tensor变量，释放对它所引用对象的内存引用
```

使用示例：

```python
kmodel_file = "/sdcard/app/kmodel/face_detection_320.kmodel"
fd_kmodel = kpu_init(kmodel_file)
while True:
    rgb888p_img = camera_read(CAM_DEV_ID_0)     # 从sensor拿到一帧图像
    dets = kpu_run(fd_kmodel,rgb888p_img)            # kmodel推理
    ......
......
kpu_deinit()                   # 释放kmodel
global current_kmodel_obj
del current_kmodel_obj
del fd_kmodel
nn.shrink_memory_pool()        # 释放所有nncase内存
```

#### 1.6 媒体使用

##### 1.6.1 camera

```python
from media.camera import *
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

OUT_RGB888P_WIDTH = ALIGN_UP(1024, 16)
OUT_RGB888P_HEIGH = 576

def camera_init(dev_id):
    # 根据设备id初始化camera
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)
    
    # 设置camera的两路输出，一路输出用于显示，一路输出用于ai
    
    # （1）设置显示输出
    # 设置指定设备id的chn0的输出宽高
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    # 设置指定设备id的chn0的输出格式为yuv420sp
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)
    
    # （2）设置AI输出
    # 设置指定设备id的chn2的输出宽高
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    # 设置指定设备id的chn2的输出格式为rgb88planar
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

def camera_start(dev_id):
    # 启动sensor
    camera.start_stream(dev_id)

def camera_read(dev_id):
    # 读取指定设备chn2的一帧图像，即获取一帧AI原图
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
    return rgb888p_img

def camera_release_image(dev_id,rgb888p_img):
    # 释放指定设备chn2一帧图像
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

def camera_stop(dev_id):
    # 释放sensor
    camera.stop_stream(dev_id)
```

**使用示例：**

```python
from media.camera import *
import os,sys                                

# 初始化camera 0
camera_init(CAM_DEV_ID_0)
......（camera_start还要配合其它操作，稍后在media模块介绍）
# 启动sensor
camera_start(CAM_DEV_ID_0)
time.sleep(5)
rgb888p_img = None
while True:
    os.exitpoint()              #加退出点，确保当前当次循环执行完全，保证释放图像函数调用
    # 读取一帧图像
    rgb888p_img = camera_read(CAM_DEV_ID_0)
    .......
    # 释放当前图像
    camera_release_image(CAM_DEV_ID_0,rgb888p_img)
```

##### 1.6.2 display

```python
from media.display import *
# draw_img：用于画图
# osd_img：用于显示
global draw_img,osd_img                 

#for display
def display_init():
    # 使用hdmi用于显示
    display.init(LT9611_1920X1080_30FPS)
    # 设置显示宽高、格式等
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

def display_deinit():
    # 释放与显示相关的资源
    display.deinit()

def display_draw(dets):
    # 将检测框画到显示上
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if dets:
            # 清空draw_img
            draw_img.clear()
            
            # 画检测框
            for det in dets:
            x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
            x = x * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
            y = y * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
            w = w * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
            h = h * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
            # 先将框画到draw_img，argb
            draw_img.draw_rectangle(x,y, w, h, color=(255, 255, 0, 255))
            # 将draw_img拷贝到osd_img
            draw_img.copy_to(osd_img)
            # 将osd_img显示到hdmi上
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            # 清空draw_img
            draw_img.clear()
            # 将draw_img拷贝到osd_img
            draw_img.copy_to(osd_img)
            # 将透明图显示到hdmi上
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
```

**使用示例：**

```python
from media.display import *
# 显示初始化
display_init()
while True:
    ......
    dets = kpu_run(kpu_face_detect,rgb888p_img)
    # 将检测框画到显示屏幕
    display_draw(dets)
    ......
# 显示资源释放
display_deinit()
```

##### 1.6.3 media

```python
from media.media import *

global buffer,media_source,media_sink               #for media
def media_init():
    # （1）配置媒体缓冲区
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE
    ret = media.buffer_config(config)
    
    # （2）创建由参数media_source和media_sink指定的媒体链路，链路创建成功后，数据流会自动从media_source流入media_sink，无需用户干预
    global media_source, media_sink
    # 创建指向指定sensor id，chn0的source
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    # 创建指向指定显示的sink
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    # 创建子sensor的chn0的输出，到指定显示的链路
    media.create_link(media_source, media_sink)

    # （3）初始化K230 CanMV平台媒体缓冲区
    media.buffer_init()
    
    global buffer, draw_img, osd_img
    # （4）构建用于画图的对象
    # 使用media模块构建osd_image内存，用于显示
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 创建用于画框、画点的Image
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, alloc=image.ALLOC_MPGC)
    # 用于画框、画点结果，防止画的过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
              phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

def media_deinit():
    # 释放media资源
    global buffer,media_source, media_sink
    # （1）释放buffer
    media.release_buffer(buffer)
    # （2）销毁已经创建的媒体链路
    media.destroy_link(media_source, media_sink)
    
    # （3）去初始化K230 CanMV平台媒体缓冲区
    media.buffer_deinit()
```

**使用示例：**

```python
# camera初始化
camera_init(CAM_DEV_ID_0)
# 显示初始化
display_init()

rgb888p_img = None
try:
    media_init()      #媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）   

    camera_start(CAM_DEV_ID_0)        # 启动camera
    while True:
        with ScopedTiming("total",1):
            os.exitpoint()            # 添加退出点，保证图像释放
            # （1）读取一帧图像
            rgb888p_img = camera_read(CAM_DEV_ID_0)          
    
            # for rgb888planar
            if rgb888p_img.format() == image.RGBP888:
                # （2）kpu推理，获取推理结果
                dets = kpu_run(kpu_face_detect,rgb888p_img)
                # （3）将推理结果画到原图
                display_draw(dets)
                    
                # （4）释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)
except KeyboardInterrupt as e:
    print("user stop: ", e)
except BaseException as e:
    sys.print_exception(e)
finally:    
    # 释放camera资源
    camera_stop(CAM_DEV_ID_0)
    # 释放显示资源
    display_deinit()
    # 释放kpu资源
    kpu_deinit()
    global current_kmodel_obj
    if 'current_kmodel_obj' in globals():
        global current_kmodel_obj
        del current_kmodel_obj
    del kpu_face_detect
    # 垃圾回收
    gc.collect()
    nn.shrink_memory_pool()              # 保证nncase资源的完全释放
    # 释放媒体资源
    media_deinit()
```

### 2.人脸检测

```python
import ulab.numpy as np                  #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn              #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *               #摄像头模块
from media.display import *              #显示模块
from media.media import *                #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import aidemo                            #aidemo模块，封装ai demo相关后处理、画图操作
import image                             #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                              #时间统计
import gc                                #垃圾回收模块
import os, sys                           #操作系统接口模块

#********************for config.py********************
# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)                   # 显示宽度要求16位对齐
DISPLAY_HEIGHT = 1080

# ai原图分辨率，sensor默认出图为16:9，若需不形变原图，最好按照16:9比例设置宽高
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)               # ai原图宽度要求16位对齐
OUT_RGB888P_HEIGH = 1080

# kmodel参数设置
# kmodel输入shape
kmodel_input_shape = (1,3,320,320)
# ai原图padding
rgb_mean = [104,117,123]
# kmodel其它参数设置
confidence_threshold = 0.5
top_k = 5000
nms_threshold = 0.2
keep_top_k = 750
vis_thres = 0.5
variance = [0.1, 0.2]
anchor_len = 4200
score_dim = 2
det_dim = 4
keypoint_dim = 10

# 文件配置
# kmodel文件配置
root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/face_detection_320.kmodel'
# anchor文件配置
anchors_path = root_dir + 'utils/prior_data_320.bin'
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0

#********************for scoped_timing.py********************
# 时间统计类
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#********************for ai_utils.py********************
# 当前kmodel
global current_kmodel_obj
# ai2d：              ai2d实例
# ai2d_input_tensor： ai2d输入
# ai2d_output_tensor：ai2d输出
# ai2d_builder：      根据ai2d参数，构建的ai2d_builder对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder    #for ai2d
print('anchors_path:',anchors_path)
# 读取anchor文件，为后处理做准备
prior_data = np.fromfile(anchors_path, dtype=np.float)
prior_data = prior_data.reshape((anchor_len,det_dim))

def get_pad_one_side_param():
    # 右padding或下padding，获取padding参数
    dst_w = kmodel_input_shape[3]                         # kmodel输入宽（w）
    dst_h = kmodel_input_shape[2]                          # kmodel输入高（h）

    # OUT_RGB888P_WIDTH：原图宽（w）
    # OUT_RGB888P_HEIGH：原图高（h）
    # 计算最小的缩放比例，等比例缩放
    ratio_w = dst_w / OUT_RGB888P_WIDTH
    ratio_h = dst_h / OUT_RGB888P_HEIGH
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h
    # 计算经过缩放后的新宽和新高
    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGH)

    # 计算需要添加的padding，以使得kmodel输入的宽高和原图一致
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2
    # 四舍五入，确保padding是整数
    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

def ai2d_init():
    # 人脸检测模型ai2d初始化
    with ScopedTiming("ai2d_init",debug_mode > 0):
        # （1）创建ai2d对象
        global ai2d
        ai2d = nn.ai2d()
        # （2）设置ai2d参数
        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d.set_pad_param(True, get_pad_one_side_param(), 0, rgb_mean)
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        # （3）创建ai2d_output_tensor，用于保存ai2d输出
        global ai2d_output_tensor
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_output_tensor = nn.from_numpy(data)

        # （4）ai2d_builder，根据ai2d参数、输入输出大小创建ai2d_builder对象
        global ai2d_builder
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], kmodel_input_shape)


def ai2d_run(rgb888p_img):
    # 对原图rgb888p_img进行预处理
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d_input_tensor,ai2d_output_tensor
        # （1）根据原图构建ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)
        # （2）运行ai2d_builder，将结果保存到ai2d_output_tensor中
        ai2d_builder.run(ai2d_input_tensor, ai2d_output_tensor)

def ai2d_release():
    # 释放ai2d_input_tensor
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor
        del ai2d_input_tensor

def kpu_init(kmodel_file):
    # 初始化kpu对象，并加载kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        # 初始化kpu对象
        kpu_obj = nn.kpu()
        # 加载kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化ai2d
        ai2d_init()
        return kpu_obj

def kpu_pre_process(rgb888p_img):
    # 使用ai2d对原图进行预处理（padding，resize）
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_output_tensor
        # 将ai2d输出设置为kpu输入
        current_kmodel_obj.set_input_tensor(0, ai2d_output_tensor)

def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取模型输出，并将结果转换为numpy，以便进行人脸检测后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

def kpu_run(kpu_obj,rgb888p_img):
    # kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）原图预处理，并设置模型输入
    kpu_pre_process(rgb888p_img)
    # （2）kpu推理
    with ScopedTiming("kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放ai2d资源
    ai2d_release()
    # （4）获取kpu输出
    results = kpu_get_output()
    # （5）kpu结果后处理
    with ScopedTiming("kpu_post",debug_mode > 0):
        post_ret = aidemo.face_det_post_process(confidence_threshold,nms_threshold,kmodel_input_shape[2],prior_data,[OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH],results)

    # （6）返回人脸检测框
    if len(post_ret)==0:
        return post_ret
    else:
        return post_ret[0]


def kpu_deinit():
    # kpu释放
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        if 'ai2d' in globals():       #删除ai2d变量，释放对它所引用对象的内存引用
            global ai2d
            del ai2d

        if 'ai2d_output_tensor' in globals():       #删除ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global ai2d_output_tensor
            del ai2d_output_tensor

#********************for media_utils.py********************
global draw_img,osd_img                                     #for display
global buffer,media_source,media_sink                       #for media

# for display，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.2
def display_init():
    # hdmi显示初始化
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

def display_deinit():
    # 释放显示资源
    display.deinit()

def display_draw(dets):
    # hdmi画检测框
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if dets:
            draw_img.clear()
            for det in dets:
                x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                x = x * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                y = y * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
                w = w * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                h = h * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
                draw_img.draw_rectangle(x,y, w, h, color=(255, 255, 0, 255), thickness = 2)
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.1
def camera_init(dev_id):
    # camera初始化
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

def camera_start(dev_id):
    # camera启动
    camera.start_stream(dev_id)

def camera_read(dev_id):
    # 读取一帧图像
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

def camera_release_image(dev_id,rgb888p_img):
    # 释放一帧图像
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

def camera_stop(dev_id):
    # 停止camera
    camera.stop_stream(dev_id)

#for media，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.3
def media_init():
    # meida初始化
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

def media_deinit():
    # meida资源释放
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#********************for face_detect.py********************
def face_detect_inference():
    print("face_detect_test start")
    # kpu初始化
    kpu_face_detect = kpu_init(kmodel_file)
    # camera初始化
    camera_init(CAM_DEV_ID_0)
    # 显示初始化
    display_init()

    # 注意：将一定要将一下过程包在try中，用于保证程序停止后，资源释放完毕；确保下次程序仍能正常运行
    try:
        # 注意：媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）
        media_init()
        # 启动camera
        camera_start(CAM_DEV_ID_0)
#        time.sleep(5)
        gc_count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                # （1）读取一帧图像
                rgb888p_img = camera_read(CAM_DEV_ID_0)

                # （2）若读取成功，推理当前帧
                if rgb888p_img.format() == image.RGBP888:
                    # （2.1）推理当前图像，并获取检测结果
                    dets = kpu_run(kpu_face_detect,rgb888p_img)
                    # （2.2）将结果画到显示器
                    display_draw(dets)

                # （3）释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)
                if gc_count > 5:
                    gc.collect()
                    nn.shrink_memory_pool()
                    gc_count = 0
                else:
                    gc_count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        # 停止camera
        camera_stop(CAM_DEV_ID_0)
        # 释放显示资源
        display_deinit()
        # 释放kpu资源
        kpu_deinit()
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_face_detect

        # 垃圾回收
        gc.collect()
        nn.shrink_memory_pool()
        # 释放媒体资源
        media_deinit()


    print("face_detect_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    face_detect_inference()
```

### 3.COCO目标检测

```python
import ulab.numpy as np             #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn         #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *          #摄像头模块
from media.display import *         #显示模块
from media.media import *           #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import image                        #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                         #时间统计
import gc                           #垃圾回收模块
import os, sys                      #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

#ai 原图输入分辨率
OUT_RGB888P_WIDTH = ALIGN_UP(320, 16)
OUT_RGB888P_HEIGHT = 320

#多目标检测 kmodel 输入 shape
kmodel_input_shape = (1,3,320,320)

#多目标检测 相关参数设置
confidence_threshold = 0.2                                      # 多目标检测分数阈值
nms_threshold = 0.2                                             # 非最大值抑制阈值
x_factor = float(OUT_RGB888P_WIDTH)/kmodel_input_shape[3]       # 原始图像分辨率宽与kmodel宽输入大小比值
y_factor = float(OUT_RGB888P_HEIGHT)/kmodel_input_shape[2]      # 原始图像分辨率高与kmodel高输入大小比值
keep_top_k = 50                                                 # 最大输出检测框的数量

#文件配置
root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/yolov8n_320.kmodel'           # kmodel文件的路径
debug_mode = 0                                                  # debug模式 大于0（调试）、 反之 （不调试）

#颜色板 用于作图
color_four = [(255, 220, 20, 60), (255, 119, 11, 32), (255, 0, 0, 142), (255, 0, 0, 230),
        (255, 106, 0, 228), (255, 0, 60, 100), (255, 0, 80, 100), (255, 0, 0, 70),
        (255, 0, 0, 192), (255, 250, 170, 30), (255, 100, 170, 30), (255, 220, 220, 0),
        (255, 175, 116, 175), (255, 250, 0, 30), (255, 165, 42, 42), (255, 255, 77, 255),
        (255, 0, 226, 252), (255, 182, 182, 255), (255, 0, 82, 0), (255, 120, 166, 157),
        (255, 110, 76, 0), (255, 174, 57, 255), (255, 199, 100, 0), (255, 72, 0, 118),
        (255, 255, 179, 240), (255, 0, 125, 92), (255, 209, 0, 151), (255, 188, 208, 182),
        (255, 0, 220, 176), (255, 255, 99, 164), (255, 92, 0, 73), (255, 133, 129, 255),
        (255, 78, 180, 255), (255, 0, 228, 0), (255, 174, 255, 243), (255, 45, 89, 255),
        (255, 134, 134, 103), (255, 145, 148, 174), (255, 255, 208, 186),
        (255, 197, 226, 255), (255, 171, 134, 1), (255, 109, 63, 54), (255, 207, 138, 255),
        (255, 151, 0, 95), (255, 9, 80, 61), (255, 84, 105, 51), (255, 74, 65, 105),
        (255, 166, 196, 102), (255, 208, 195, 210), (255, 255, 109, 65), (255, 0, 143, 149),
        (255, 179, 0, 194), (255, 209, 99, 106), (255, 5, 121, 0), (255, 227, 255, 205),
        (255, 147, 186, 208), (255, 153, 69, 1), (255, 3, 95, 161), (255, 163, 255, 0),
        (255, 119, 0, 170), (255, 0, 182, 199), (255, 0, 165, 120), (255, 183, 130, 88),
        (255, 95, 32, 0), (255, 130, 114, 135), (255, 110, 129, 133), (255, 166, 74, 118),
        (255, 219, 142, 185), (255, 79, 210, 114), (255, 178, 90, 62), (255, 65, 70, 15),
        (255, 127, 167, 115), (255, 59, 105, 106), (255, 142, 108, 45), (255, 196, 172, 0),
        (255, 95, 54, 80), (255, 128, 76, 255), (255, 201, 57, 1), (255, 246, 0, 122),
        (255, 191, 162, 208)]

#标签 多目标检测的所有可识别类别
labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")


#ai_utils.py
global current_kmodel_obj                                           # 定义全局的 kpu 对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder       # 定义全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder


# 多目标检测 非最大值抑制方法实现
def py_cpu_nms(boxes,scores,thresh):
    """Pure Python NMS baseline."""
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = np.argsort(scores,axis = 0)[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        new_x1 = []
        new_x2 = []
        new_y1 = []
        new_y2 = []
        new_areas = []
        for order_i in order:
            new_x1.append(x1[order_i])
            new_x2.append(x2[order_i])
            new_y1.append(y1[order_i])
            new_y2.append(y2[order_i])
            new_areas.append(areas[order_i])
        new_x1 = np.array(new_x1)
        new_x2 = np.array(new_x2)
        new_y1 = np.array(new_y1)
        new_y2 = np.array(new_y2)
        xx1 = np.maximum(x1[i], new_x1)
        yy1 = np.maximum(y1[i], new_y1)
        xx2 = np.minimum(x2[i], new_x2)
        yy2 = np.minimum(y2[i], new_y2)

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h

        new_areas = np.array(new_areas)
        ovr = inter / (areas[i] + new_areas - inter)
        new_order = []
        for ovr_i,ind in enumerate(ovr):
            if ind < thresh:
                new_order.append(order[ovr_i])
        order = np.array(new_order,dtype=np.uint8)
    return keep

# 多目标检测 接收kmodel输出的后处理方法
def kpu_post_process(output_data):
    with ScopedTiming("kpu_post_process", debug_mode > 0):
        boxes_ori = output_data[:,0:4]
        scores_ori = output_data[:,4:]
        confs_ori = np.max(scores_ori,axis=-1)
        inds_ori = np.argmax(scores_ori,axis=-1)

        boxes = []
        scores = []
        inds = []

        for i in range(len(boxes_ori)):
            if confs_ori[i] > confidence_threshold:
                scores.append(confs_ori[i])
                inds.append(inds_ori[i])
                x = boxes_ori[i,0]
                y = boxes_ori[i,1]
                w = boxes_ori[i,2]
                h = boxes_ori[i,3]
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                right = int((x + 0.5 * w) * x_factor)
                bottom = int((y + 0.5 * h) * y_factor)
                boxes.append([left,top,right,bottom])

        if len(boxes)==0:
            return []

        boxes = np.array(boxes)
        scores = np.array(scores)
        inds = np.array(inds)

        # do NMS
        keep = py_cpu_nms(boxes,scores,nms_threshold)
        dets = np.concatenate((boxes, scores.reshape((len(boxes),1)), inds.reshape((len(boxes),1))), axis=1)

        dets_out = []
        for keep_i in keep:
            dets_out.append(dets[keep_i])
        dets_out = np.array(dets_out)

        # keep top-K faster NMS
        dets_out = dets_out[:keep_top_k, :]
        return dets_out

# ai2d 初始化
def ai2d_init():
    with ScopedTiming("ai2d_init",debug_mode > 0):
        global ai2d
        ai2d = nn.ai2d()
        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        global ai2d_out_tensor
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_out_tensor = nn.from_numpy(data)

        global ai2d_builder
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], kmodel_input_shape)

# ai2d 运行
def ai2d_run(rgb888p_img):
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d_input_tensor,ai2d_out_tensor,ai2d_builder
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)

        ai2d_builder.run(ai2d_input_tensor, ai2d_out_tensor)

# ai2d 释放内存
def ai2d_release():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor
        del ai2d_input_tensor

# kpu 初始化
def kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        ai2d_init()
        return kpu_obj

# kpu 输入预处理
def kpu_pre_process(rgb888p_img):
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_out_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, ai2d_out_tensor)

# kpu 获得 kmodel 输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()

        result = result.reshape((result.shape[0] * result.shape[1], result.shape[2]))
        result = result.transpose()
        tmp2 = result.copy()
        del data
        results.append(tmp2)
        return results

# kpu 运行
def kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1) 原图预处理，并设置模型输入
    kpu_pre_process(rgb888p_img)
    # (2) kpu运行
    with ScopedTiming("kpu_run",debug_mode > 0):
        kpu_obj.run()
    # (3) 释放ai2d资源
    ai2d_release()
    # (4) 获取kpu输出
    results = kpu_get_output()
    # (5) kpu结果后处理
    dets = kpu_post_process(results[0])
    # (6) 返回多目标检测结果
    return dets

# kpu 释放内存
def kpu_deinit():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        if 'ai2d' in globals():
            global ai2d
            del ai2d
        if 'ai2d_out_tensor' in globals():
            global ai2d_out_tensor
            del ai2d_out_tensor
        if 'ai2d_builder' in globals():
            global ai2d_builder
            del ai2d_builder

#media_utils.py
global draw_img,osd_img                                     #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 将所有目标检测框以及类别、分数值的作图
def display_draw(dets):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if dets:
            draw_img.clear()
            for det in dets:
                x1, y1, x2, y2 = map(lambda x: int(round(x, 0)), det[:4])
                w = (x2 - x1) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                h = (y2 - y1) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT
                draw_img.draw_rectangle(x1 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH,
                                        y1 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT, w, h, color=color_four[int(det[5])],thickness=4)
                draw_img.draw_string( int(x1 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH) , int(y1 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)-50,
                                         " " + labels[int(det[5])] + " " + str(round(det[4],2)) , color=color_four[int(det[5])] , scale=4)
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()


#**********for ob_detect.py**********
def ob_detect_inference():
    print("ob_detect start")
    kpu_ob_detect = kpu_init(kmodel_file)                           # 创建多目标检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                       # 初始化 camera
    display_init()                                                  # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)

        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)             # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    dets = kpu_run(kpu_ob_detect,rgb888p_img)       # 执行多目标检测 kpu运行 以及 后处理过程
                    display_draw(dets)                              # 将得到的检测结果 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)      # camera 释放图像

                if (count > 5):
                    gc.collect()
                    count = 0
                else:
                    count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        camera_stop(CAM_DEV_ID_0)                                   # 停止camera
        display_deinit()                                            # 释放 display
        kpu_deinit()                                                # 释放 kpu

        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_ob_detect

        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                        # 释放 整个media

    print("ob_detect_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    ob_detect_inference()
```

### 4.yolov8-seg

```python
import ulab.numpy as np             #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn         #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *          #摄像头模块
from media.display import *         #显示模块
from media.media import *           #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import image                        #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                         #时间统计
import gc                           #垃圾回收模块
import aidemo                       #aidemo模块，封装ai demo相关后处理、画图操作
import os, sys                      #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

#ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(320, 16)
OUT_RGB888P_HEIGHT = 320

#多目标分割 kmodel 输入参数配置
kmodel_input_shape = (1,3,320,320)          # kmodel输入分辨率
rgb_mean = [114,114,114]                    # ai2d padding 值

#多目标分割 相关参数设置
confidence_threshold = 0.2                  # 多目标分割分数阈值
nms_threshold = 0.5                         # 非最大值抑制阈值
mask_thres = 0.5                            # 多目标分割掩码阈值

#文件配置
root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/yolov8n_seg_320.kmodel'       # kmodel文件的路径
debug_mode = 0                                                  # debug模式 大于0（调试）、 反之 （不调试）

#标签 多目标分割的所有可识别类别
labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

#颜色板 用于作图
color_four = [(255, 220, 20, 60), (255, 119, 11, 32), (255, 0, 0, 142), (255, 0, 0, 230),
        (255, 106, 0, 228), (255, 0, 60, 100), (255, 0, 80, 100), (255, 0, 0, 70),
        (255, 0, 0, 192), (255, 250, 170, 30), (255, 100, 170, 30), (255, 220, 220, 0),
        (255, 175, 116, 175), (255, 250, 0, 30), (255, 165, 42, 42), (255, 255, 77, 255),
        (255, 0, 226, 252), (255, 182, 182, 255), (255, 0, 82, 0), (255, 120, 166, 157),
        (255, 110, 76, 0), (255, 174, 57, 255), (255, 199, 100, 0), (255, 72, 0, 118),
        (255, 255, 179, 240), (255, 0, 125, 92), (255, 209, 0, 151), (255, 188, 208, 182),
        (255, 0, 220, 176), (255, 255, 99, 164), (255, 92, 0, 73), (255, 133, 129, 255),
        (255, 78, 180, 255), (255, 0, 228, 0), (255, 174, 255, 243), (255, 45, 89, 255),
        (255, 134, 134, 103), (255, 145, 148, 174), (255, 255, 208, 186),
        (255, 197, 226, 255), (255, 171, 134, 1), (255, 109, 63, 54), (255, 207, 138, 255),
        (255, 151, 0, 95), (255, 9, 80, 61), (255, 84, 105, 51), (255, 74, 65, 105),
        (255, 166, 196, 102), (255, 208, 195, 210), (255, 255, 109, 65), (255, 0, 143, 149),
        (255, 179, 0, 194), (255, 209, 99, 106), (255, 5, 121, 0), (255, 227, 255, 205),
        (255, 147, 186, 208), (255, 153, 69, 1), (255, 3, 95, 161), (255, 163, 255, 0),
        (255, 119, 0, 170), (255, 0, 182, 199), (255, 0, 165, 120), (255, 183, 130, 88),
        (255, 95, 32, 0), (255, 130, 114, 135), (255, 110, 129, 133), (255, 166, 74, 118),
        (255, 219, 142, 185), (255, 79, 210, 114), (255, 178, 90, 62), (255, 65, 70, 15),
        (255, 127, 167, 115), (255, 59, 105, 106), (255, 142, 108, 45), (255, 196, 172, 0),
        (255, 95, 54, 80), (255, 128, 76, 255), (255, 201, 57, 1), (255, 246, 0, 122),
        (255, 191, 162, 208)]

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")


#ai_utils.py
global current_kmodel_obj                                           # 定义全局的 kpu 对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder       # 定义全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder

# 多目标分割 接收kmodel输出的后处理方法
def kpu_post_process(output_datas):
    with ScopedTiming("kpu_post_process", debug_mode > 0):
        global masks
        mask_dets = aidemo.segment_postprocess(output_datas,[OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH],[kmodel_input_shape[2],kmodel_input_shape[3]],[DISPLAY_HEIGHT,DISPLAY_WIDTH],confidence_threshold,nms_threshold,mask_thres,masks)
        return mask_dets

# 获取kmodel输入图像resize比例 以及 padding的上下左右像素数量
def get_pad_param():
    #右padding或下padding
    dst_w = kmodel_input_shape[3]
    dst_h = kmodel_input_shape[2]

    ratio_w = float(dst_w) / OUT_RGB888P_WIDTH
    ratio_h = float(dst_h) / OUT_RGB888P_HEIGHT
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h

    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGHT)
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2

    top = (int)(round(dh - 0.1))
    bottom = (int)(round(dh + 0.1))
    left = (int)(round(dw - 0.1))
    right = (int)(round(dw + 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

# ai2d 初始化
def ai2d_init():
    with ScopedTiming("ai2d_init",debug_mode > 0):
        global ai2d
        ai2d = nn.ai2d()
        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d.set_pad_param(True, get_pad_param(), 0, rgb_mean)
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        global ai2d_out_tensor
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_out_tensor = nn.from_numpy(data)

        global ai2d_builder
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], kmodel_input_shape)

# ai2d 运行
def ai2d_run(rgb888p_img):
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d_input_tensor,ai2d_out_tensor,ai2d_builder
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)

        ai2d_builder.run(ai2d_input_tensor, ai2d_out_tensor)

# ai2d 释放内存
def ai2d_release():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor
        del ai2d_input_tensor

# kpu 初始化
def kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        ai2d_init()
        return kpu_obj

# kpu 输入预处理
def kpu_pre_process(rgb888p_img):
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_out_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, ai2d_out_tensor)

# kpu 获得 kmodel 输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        data_0 = current_kmodel_obj.get_output_tensor(0)
        result_0 = data_0.to_numpy()
        del data_0
        results.append(result_0)

        data_1 = current_kmodel_obj.get_output_tensor(1)
        result_1 = data_1.to_numpy()
        del data_1
        results.append(result_1)

        return results

# kpu 运行
def kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1) 原图预处理，并设置模型输入
    kpu_pre_process(rgb888p_img)
    # (2) kpu 运行
    with ScopedTiming("kpu_run",debug_mode > 0):
        kpu_obj.run()
    # (3) 释放ai2d资源
    ai2d_release()
    # (4) 获取kpu输出
    results = kpu_get_output()
    # (5) kpu结果后处理
    seg_res = kpu_post_process(results)
    # (6) 返回 分割 mask 结果
    return seg_res

# kpu 释放内存
def kpu_deinit():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        if 'ai2d' in globals():
            global ai2d
            del ai2d
        if 'ai2d_out_tensor' in globals():
            global ai2d_out_tensor
            del ai2d_out_tensor
        if 'ai2d_builder' in globals():
            global ai2d_builder
            del ai2d_builder

#media_utils.py
global draw_img,osd_img,masks                               #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 将所有目标分割对象以及类别、分数值的作图
def display_draw(seg_res):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img,masks
        if seg_res[0]:
            dets = seg_res[0]
            ids = seg_res[1]
            scores = seg_res[2]

            for i, det in enumerate(dets):
                x1, y1, w, h = map(lambda x: int(round(x, 0)), det)
                draw_img.draw_string( int(x1) , int(y1)-50, " " + labels[int(ids[i])] + " " + str(round(scores[i],2)) , color=color_four[int(ids[i])], scale=4)
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img, masks
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    masks = np.zeros((1,DISPLAY_HEIGHT,DISPLAY_WIDTH,4))
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888,alloc=image.ALLOC_REF,data=masks)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()


#**********for seg.py**********
def seg_inference():
    print("seg start")
    kpu_seg = kpu_init(kmodel_file)                                 # 创建多目标分割的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                       # 初始化 camera
    display_init()                                                  # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)

        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)             # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    seg_res = kpu_run(kpu_seg,rgb888p_img)          # 执行多目标分割 kpu 运行 以及 后处理过程
                    display_draw(seg_res)                           # 将得到的分割结果 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)      # camera 释放图像
                gc.collect()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        camera_stop(CAM_DEV_ID_0)                                   # 停止 camera
        display_deinit()                                            # 释放 display
        kpu_deinit()                                         # 释放 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_seg

        if 'draw_img' in globals():
            global draw_img
            del draw_img
        if 'masks' in globals():
            global masks
            del masks
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                        # 释放 整个media

    print("seg end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    seg_inference()
```

### 5.车牌检测

```python
import ulab.numpy as np             #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn         #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *          #摄像头模块
from media.display import *         #显示模块
from media.media import *           #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import image                        #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                         #时间统计
import gc                           #垃圾回收模块
import aidemo                       #aidemo模块，封装ai demo相关后处理、画图操作
import os, sys                      #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

#ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

#车牌检测 kmodel 输入shape
kmodel_input_shape = (1,3,640,640)

#车牌检测 相关参数设置
obj_thresh = 0.2            #车牌检测分数阈值
nms_thresh = 0.2            #检测框 非极大值抑制 阈值

#文件配置
root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/LPD_640.kmodel'       # kmodel 文件的路径
debug_mode = 0                                          # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")


#ai_utils.py
global current_kmodel_obj                                        # 定义全局的 kpu 对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder    # 定义全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder

# 车牌检测 接收kmodel输出的后处理方法
def kpu_post_process(output_data):
    with ScopedTiming("kpu_post_process", debug_mode > 0):
        results = aidemo.licence_det_postprocess(output_data,[OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH],[kmodel_input_shape[2],kmodel_input_shape[3]],obj_thresh,nms_thresh)
        return results

# ai2d 初始化
def ai2d_init():
    with ScopedTiming("ai2d_init",debug_mode > 0):
        global ai2d
        ai2d = nn.ai2d()
        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        global ai2d_out_tensor
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_out_tensor = nn.from_numpy(data)

        global ai2d_builder
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], kmodel_input_shape)

# ai2d 运行
def ai2d_run(rgb888p_img):
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d_input_tensor,ai2d_out_tensor,ai2d_builder
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)

        ai2d_builder.run(ai2d_input_tensor, ai2d_out_tensor)

# ai2d 释放内存
def ai2d_release():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor
        del ai2d_input_tensor

# kpu 初始化
def kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        ai2d_init()
        return kpu_obj

# kpu 输入预处理
def kpu_pre_process(rgb888p_img):
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_out_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, ai2d_out_tensor)

# kpu 获得 kmodel 输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            tmp2 = result.copy()
            del data
            results.append(tmp2)
        return results

# kpu 运行
def kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1) 原图预处理，并设置模型输入
    kpu_pre_process(rgb888p_img)
    # (2) kpu 运行
    with ScopedTiming("kpu_run",debug_mode > 0):
        kpu_obj.run()
    # (3) 释放ai2d资源
    ai2d_release()
    # (4) 获取kpu输出
    results = kpu_get_output()
    # (5) kpu结果后处理
    dets = kpu_post_process(results)
    # (6) 返回 车牌检测框 结果
    return dets

# kpu 释放内存
def kpu_deinit():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        if 'ai2d' in globals():
            global ai2d
            del ai2d
        if 'ai2d_out_tensor' in globals():
            global ai2d_out_tensor
            del ai2d_out_tensor
        if 'ai2d_builder' in globals():
            global ai2d_builder
            del ai2d_builder

#media_utils.py
global draw_img,osd_img                                     #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media 定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 将所有车牌检测框绘制到屏幕上
def display_draw(dets):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if dets:
            draw_img.clear()
            point_8 = np.zeros((8),dtype=np.int16)
            for det in dets:
                for i in range(4):
                    x = det[i * 2 + 0]/OUT_RGB888P_WIDTH*DISPLAY_WIDTH
                    y = det[i * 2 + 1]/OUT_RGB888P_HEIGHT*DISPLAY_HEIGHT
                    point_8[i * 2 + 0] = int(x)
                    point_8[i * 2 + 1] = int(y)
                for i in range(4):
                    draw_img.draw_line(point_8[i * 2 + 0],point_8[i * 2 + 1],point_8[(i+1) % 4 * 2 + 0],point_8[(i+1) % 4 * 2 + 1],color=(255, 0, 255, 0),thickness=4)
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_BGR_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()


#**********for licence_det.py**********
def licence_det_inference():
    print("licence_det start")
    kpu_licence_det = kpu_init(kmodel_file)                                             # 创建车牌检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                                           # 初始化 camera
    display_init()                                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)

        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    dets = kpu_run(kpu_licence_det,rgb888p_img)                         # 执行车牌检测 kpu 运行 以及后处理过程
                    display_draw(dets)                                                  # 将得到的 检测结果 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)                          # camera 释放图像

                if (count > 5):
                    gc.collect()
                    count = 0
                else:
                    count += 1

    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        camera_stop(CAM_DEV_ID_0)                                                       # 停止 camera
        display_deinit()                                                                # 释放 display
        kpu_deinit()                                                                    # 释放 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_licence_det
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                                            # 释放整个media

    print("licence_det end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    licence_det_inference()
```

### 6.OCR检测

```python
import ulab.numpy as np             #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn         #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *          #摄像头模块
from media.display import *         #显示模块
from media.media import *           #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import image                        #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                         #时间统计
import gc                           #垃圾回收模块
import os,sys                       #操作系统接口模块
import aicube                       #aicube模块，封装检测分割等任务相关后处理

# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

# ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(640, 16)
OUT_RGB888P_HEIGH = 360

# kmodel输入参数配置
kmodel_input_shape_det = (1,3,640,640)      # kmodel输入分辨率
rgb_mean = [0,0,0]                          # ai2d padding的值

# kmodel相关参数设置
mask_threshold = 0.25                       # 二值化mask阈值
box_threshold = 0.3                         # 检测框分数阈值

# 文件配置
root_dir = '/sdcard/app/tests/'
kmodel_file_det = root_dir + 'kmodel/ocr_det_int16.kmodel'    # kmodel加载路径
debug_mode = 0                                                # 调试模式 大于0（调试）、 反之 （不调试）

# scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

# ai utils
# 当前kmodel
global current_kmodel_obj                                                                  # 定义全局kpu对象
# ai2d_det: ai2d实例
# ai2d_input_tensor_det: ai2d输入
# ai2d_output_tensor_det: ai2d输出
# ai2d_builder_det: 根据ai2d参数，构建的ai2d_builder_det对象
# ai2d_input_det: ai2d输入的numpy数据
global ai2d_det,ai2d_input_tensor_det,ai2d_output_tensor_det,ai2d_builder_det,ai2d_input_det    # 定义全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder

# padding方法，一边padding，右padding或者下padding
def get_pad_one_side_param(out_img_size,input_img_size):
    # 右padding或下padding
    dst_w = out_img_size[0]
    dst_h = out_img_size[1]

    input_width = input_img_size[0]
    input_high = input_img_size[1]

    ratio_w = dst_w / input_width
    ratio_h = dst_h / input_high
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h

    new_w = (int)(ratio * input_width)
    new_h = (int)(ratio * input_high)
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2

    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]


# ai2d 初始化，用于实现输入的预处理
def ai2d_init_det():
    with ScopedTiming("ai2d_init",debug_mode > 0):
        # 创建ai2d对象
        global ai2d_det
        ai2d_det = nn.ai2d()
        # 设置ai2d参数
        ai2d_det.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d_det.set_pad_param(True, get_pad_one_side_param([kmodel_input_shape_det[3],kmodel_input_shape_det[2]], [OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH]), 0, [0, 0, 0])
        ai2d_det.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
        # 创建ai2d_output_tensor_det，用于保存ai2d的输出
        global ai2d_output_tensor_det
        data = np.ones(kmodel_input_shape_det, dtype=np.uint8)
        ai2d_output_tensor_det = nn.from_numpy(data)

        # ai2d_builder_det，根据ai2d参数、输入输出大小创建ai2d_builder_det对象
        global ai2d_builder_det
        ai2d_builder_det = ai2d_det.build([1, 3, OUT_RGB888P_HEIGH, OUT_RGB888P_WIDTH], [1, 3, kmodel_input_shape_det[2], kmodel_input_shape_det[3]])


# ai2d 运行，完成ai2d_init_det设定的预处理
def ai2d_run_det(rgb888p_img):
    # 对原图rgb888p_img进行预处理
    with ScopedTiming("ai2d_run",debug_mode > 0):
        # 根据原图构建ai2d_input_tensor_det
        global ai2d_input_tensor_det,ai2d_builder_det,ai2d_input_det,ai2d_output_tensor_det
        ai2d_input_det = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor_det = nn.from_numpy(ai2d_input_det)
        # 运行ai2d_builder_det，将结果保存到ai2d_output_tensor_det
        ai2d_builder_det.run(ai2d_input_tensor_det, ai2d_output_tensor_det)


# ai2d 释放输入tensor
def ai2d_release_det():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor_det
        del ai2d_input_tensor_det

# kpu 初始化
def kpu_init_det(kmodel_file):
    # 初始化kpu对象，并加载kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        # 初始化kpu对象
        kpu_obj = nn.kpu()
        # 加载kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化ai2d
        ai2d_init_det()
        return kpu_obj

# 预处理方法
def kpu_pre_process_det(rgb888p_img):
    # 运行ai2d，将ai2d预处理的输出设置为kmodel的输入tensor
    ai2d_run_det(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_output_tensor_det
        # 将ai2d的输出设置为kmodel的输入
        current_kmodel_obj.set_input_tensor(0, ai2d_output_tensor_det)

# 获取kmodel的推理输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        # 获取模型输出，并将结果转换为numpy,以便后续处理
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

# kpu 运行
def kpu_run_det(kpu_obj,rgb888p_img):
    # kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    #（1）原图像预处理并设置模型输入
    kpu_pre_process_det(rgb888p_img)
    #（2）kpu推理
    with ScopedTiming("kpu_run",debug_mode > 0):
        kpu_obj.run()
    #（3）释放ai2d资源
    ai2d_release_det()
    #（4）获取kpu输出
    results = kpu_get_output()
    #（5）CHW转HWC
    global ai2d_input_det
    tmp = (ai2d_input_det.shape[0], ai2d_input_det.shape[1], ai2d_input_det.shape[2])
    ai2d_input_det = ai2d_input_det.reshape((ai2d_input_det.shape[0], ai2d_input_det.shape[1] * ai2d_input_det.shape[2]))
    ai2d_input_det = ai2d_input_det.transpose()
    tmp2 = ai2d_input_det.copy()
    tmp2 = tmp2.reshape((tmp[1], tmp[2], tmp[0]))
    #（6）后处理，aicube.ocr_post_process接口说明：
    #  接口：aicube.ocr_post_process(threshold_map,ai_isp,kmodel_input_shape,isp_shape,mask_threshold,box_threshold);
    #  参数说明：
    #     threshold_map: DBNet模型的输出为（N,kmodel_input_shape_det[2],kmodel_input_shape_det[3],2），两个通道分别为threshold map和segmentation map
    #     后处理过程只使用threshold map，因此将results[0][:,:,:,0] reshape成一维传给接口使用。
    #     ai_isp：后处理还会返回基于原图的检测框裁剪数据，因此要将原图数据reshape为一维传给接口处理。
    #     kmodel_input_shape：kmodel输入分辨率。
    #     isp_shape：AI原图分辨率。要将kmodel输出分辨率的检测框坐标映射到原图分辨率上，需要使用这两个分辨率的值。
    #     mask_threshold：用于二值化图像获得文本区域。
    #     box_threshold：检测框分数阈值，低于该阈值的检测框不计入结果。
    with ScopedTiming("kpu_post",debug_mode > 0):
        # 调用aicube模块的ocr_post_process完成ocr检测的后处理
        # det_results结构为[[crop_array_nhwc,[p1_x,p1_y,p2_x,p2_y,p3_x,p3_y,p4_x,p4_y]],...]
        det_results = aicube.ocr_post_process(results[0][:, :, :, 0].reshape(-1), tmp2.reshape(-1),
                                                  [kmodel_input_shape_det[3], kmodel_input_shape_det[2]],
                                                  [OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH], mask_threshold, box_threshold)
    return det_results


# kpu 释放内存
def kpu_deinit_det():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        global ai2d_det,ai2d_output_tensor_det,ai2d_input_tensor_det
        if "ai2d" in globals():
            del ai2d_det
        if "ai2d_output_tensor_det" in globals():
            del ai2d_output_tensor_det

#********************for media_utils.py********************

global draw_img,osd_img                                     #for display
global buffer,media_source,media_sink                       #for media

#display 初始化
def display_init():
    # hdmi显示初始化
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程，将OCR检测后处理得到的框绘制到OSD上并显示
def display_draw(det_results):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if det_results:
            draw_img.clear()
            # 循环绘制所有检测到的框
            for j in det_results:
                # 将原图的坐标点转换成显示的坐标点，循环绘制四条直线，得到一个矩形框
                for i in range(4):
                    x1 = j[1][(i * 2)] / OUT_RGB888P_WIDTH * DISPLAY_WIDTH
                    y1 = j[1][(i * 2 + 1)] / OUT_RGB888P_HEIGH * DISPLAY_HEIGHT
                    x2 = j[1][((i + 1) * 2) % 8] / OUT_RGB888P_WIDTH * DISPLAY_WIDTH
                    y2 = j[1][((i + 1) * 2 + 1) % 8] / OUT_RGB888P_HEIGH * DISPLAY_HEIGHT
                    draw_img.draw_line((int(x1), int(y1), int(x2), int(y2)), color=(255, 0, 0, 255),
                                       thickness=5)
                draw_img.copy_to(osd_img)
                display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 启动视频流
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 捕获一帧图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 释放内存
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# 停止视频流
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    ret = media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()
    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)
    return ret

# media 释放buffer，销毁link
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    global buffer,media_source, media_sink
    if "buffer" in globals():
        media.release_buffer(buffer)
    if 'media_source' in globals() and 'media_sink' in globals():
        media.destroy_link(media_source, media_sink)
    media.buffer_deinit()


def ocr_det_inference():
    print("ocr_det_test start")
    kpu_ocr_det = kpu_init_det(kmodel_file_det)     # 创建ocr检测任务的kpu对象
    camera_init(CAM_DEV_ID_0)                       # 初始化 camera
    display_init()                                  # 初始化 display

    # 注意：将一定要将一下过程包在try中，用于保证程序停止后，资源释放完毕；确保下次程序仍能正常运行
    try:
        # 注意：媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）
        media_init()
        # 启动camera
        camera_start(CAM_DEV_ID_0)
        gc_count=0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                # 读取一帧图像
                rgb888p_img = camera_read(CAM_DEV_ID_0) # 读取一帧图像
                # 若图像获取成功，推理当前帧
                if rgb888p_img.format() == image.RGBP888:
                    det_results = kpu_run_det(kpu_ocr_det,rgb888p_img)  # kpu运行获取kmodel的推理输出
                    display_draw(det_results)                           # 绘制检测结果，并显示
                # 释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)          # 释放内存
                if (gc_count>2):
                    gc.collect()
                    gc_count = 0
                else:
                    gc_count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        camera_stop(CAM_DEV_ID_0)                                       # 停止camera
        display_deinit()                                                # 释放display
        kpu_deinit_det()                                                # 释放kpu
        if "current_kmodel_obj" in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_ocr_det
        gc.collect()
        nn.shrink_memory_pool()
        time.sleep(1)
        media_deinit()                                                  # 释放整个media
    print("ocr_det_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    ocr_det_inference()
```

### 7.手掌检测

```python
import aicube                   #aicube模块，封装检测分割等任务相关后处理
from media.camera import *      #摄像头模块
from media.display import *     #显示模块
from media.media import *       #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区

import nncase_runtime as nn     #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np         #类似python numpy操作，但也会有一些接口不同

import time                     #时间统计
import image                    #图像模块，主要用于读取、图像绘制元素（框、点等）等操作

import gc                       #垃圾回收模块
import os, sys                  #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

##ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

#kmodel输入shape
kmodel_input_shape = (1,3,512,512)                  # kmodel输入分辨率

#kmodel相关参数设置
confidence_threshold = 0.2                          # 手掌检测阈值，用于过滤roi
nms_threshold = 0.5                                 # 手掌检测框阈值，用于过滤重复roi
kmodel_frame_size = [512,512]                       # 手掌检测输入图片尺寸
frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGHT] # 直接输入图片尺寸
strides = [8,16,32]                                 # 输出特征图的尺寸与输入图片尺寸的比
num_classes = 1                                     # 模型输出类别数
nms_option = False                                  # 是否所有检测框一起做NMS，False则按照不同的类分别应用NMS
labels = ["hand"]                                   # 模型输出类别名称

root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/hand_det.kmodel'   # kmodel文件的路径
anchors = [26,27, 53,52, 75,71, 80,99, 106,82, 99,134, 140,113, 161,172, 245,276]   #anchor设置

debug_mode = 0                                      # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                       # 定义全局的 kpu 对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder   # 定义全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder


# ai2d 初始化
def ai2d_init():
    with ScopedTiming("ai2d_init",debug_mode > 0):
        global ai2d
        global ai2d_builder
        global ai2d_output_tensor
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = kmodel_frame_size[0]
        height = kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        ai2d = nn.ai2d()
        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,height,width])
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_output_tensor = nn.from_numpy(data)

# ai2d 运行
def ai2d_run(rgb888p_img):
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d_input_tensor, ai2d_output_tensor, ai2d_builder
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)
        ai2d_builder.run(ai2d_input_tensor, ai2d_output_tensor)

# ai2d 释放内存
def ai2d_release():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor
        del ai2d_input_tensor

# kpu 初始化
def kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        ai2d_init()
        return kpu_obj

# kpu 输入预处理
def kpu_pre_process(rgb888p_img):
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, ai2d_output_tensor)

# kpu 获得 kmodel 输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# kpu 运行
def kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    kpu_pre_process(rgb888p_img)
    # (2)手掌检测 kpu 运行
    with ScopedTiming("kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌检测 ai2d 资源
    ai2d_release()
    # (4)获取手掌检测 kpu 输出
    results = kpu_get_output()
    # (5)手掌检测 kpu 结果后处理
    dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], kmodel_frame_size, frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)
    # (6)返回手掌检测结果
    return dets

# kpu 释放内存
def kpu_deinit():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        if 'ai2d' in globals():                             #删除ai2d变量，释放对它所引用对象的内存引用
            global ai2d
            del ai2d
        if 'ai2d_output_tensor' in globals():               #删除ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global ai2d_output_tensor
            del ai2d_output_tensor
        if 'ai2d_builder' in globals():                     #删除ai2d_builder变量，释放对它所引用对象的内存引用
            global ai2d_builder
            del ai2d_builder

#media_utils.py
global draw_img,osd_img                                     #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 框出所有检测到的手以及标出得分
def display_draw(dets):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img

        if dets:
            draw_img.clear()
            for det_box in dets:
                x1, y1, x2, y2 = det_box[2],det_box[3],det_box[4],det_box[5]
                w = float(x2 - x1) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                h = float(y2 - y1) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT

                x1 = int(x1 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                y1 = int(y1 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)
                x2 = int(x2 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                y2 = int(y2 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)

                if (h<(0.1*DISPLAY_HEIGHT)):
                    continue
                if (w<(0.25*DISPLAY_WIDTH) and ((x1<(0.03*DISPLAY_WIDTH)) or (x2>(0.97*DISPLAY_WIDTH)))):
                    continue
                if (w<(0.15*DISPLAY_WIDTH) and ((x1<(0.01*DISPLAY_WIDTH)) or (x2>(0.99*DISPLAY_WIDTH)))):
                    continue
                draw_img.draw_rectangle(x1 , y1 , int(w) , int(h), color=(255, 0, 255, 0), thickness = 2)
                draw_img.draw_string( x1 , y1-50, " " + labels[det_box[0]] + " " + str(round(det_box[1],2)), color=(255,0, 255, 0), scale=4)
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)
    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for hand_detect.py**********
def hand_detect_inference():
    print("hand_detect_test start")
    kpu_hand_detect = kpu_init(kmodel_file)                             # 创建手掌检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)
        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    dets = kpu_run(kpu_hand_detect,rgb888p_img)         # 执行手掌检测 kpu 运行 以及 后处理过程
                    display_draw(dets)                                  # 将得到的检测结果 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)          # camera 释放图像
                if (count>10):
                    gc.collect()
                    count = 0
                else:
                    count += 1

    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        camera_stop(CAM_DEV_ID_0)                                       # 停止 camera
        display_deinit()                                                # 释放 display
        kpu_deinit()                                                    # 释放 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_hand_detect
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                                  # 释放 整个media

    print("hand_detect_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    hand_detect_inference()
```

### 8.人体检测

```python
import aicube                   #aicube模块，封装检测分割等任务相关后处理
from media.camera import *      #摄像头模块
from media.display import *     #显示模块
from media.media import *       #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区

import nncase_runtime as nn     #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np         #类似python numpy操作，但也会有一些接口不同

import time                     #时间统计
import image                    #图像模块，主要用于读取、图像绘制元素（框、点等）等操作

import gc                       #垃圾回收模块
import os, sys                  #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

##ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGH = 1080

#kmodel输入shape
kmodel_input_shape = (1,3,640,640)                  # kmodel输入分辨率

#kmodel相关参数设置
confidence_threshold = 0.2                          # 行人检测阈值，用于过滤roi
nms_threshold = 0.6                                 # 行人检测框阈值，用于过滤重复roi
kmodel_frame_size = [640,640]                       # 行人检测输入图片尺寸
frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH]  # 直接输入图片尺寸
strides = [8,16,32]                                 # 输出特征图的尺寸与输入图片尺寸的比
num_classes = 1                                     # 模型输出类别数
nms_option = False                                  # 是否所有检测框一起做NMS，False则按照不同的类分别应用NMS
labels = ["person"]                                 # 模型输出类别名称

root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/person_detect_yolov5n.kmodel'     # kmodel文件的路径
anchors = [10, 13, 16, 30, 33, 23, 30, 61, 62, 45, 59, 119, 116, 90, 156, 198, 373, 326]   #anchor设置

debug_mode = 0                                      # debug模式 大于0（调试）、 反之 （不调试）
total_debug_mode = 1

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                       # 定义全局的 kpu 对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder   # 定义全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder


# ai2d 初始化
def ai2d_init():
    with ScopedTiming("ai2d_init",debug_mode > 0):
        global ai2d
        global ai2d_builder
        global ai2d_output_tensor
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGH
        width = kmodel_frame_size[0]
        height = kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        ai2d = nn.ai2d()
        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], [1,3,height,width])
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_output_tensor = nn.from_numpy(data)

# ai2d 运行
def ai2d_run(rgb888p_img):
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d_input_tensor,ai2d_output_tensor,ai2d_builder
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)
        ai2d_builder.run(ai2d_input_tensor, ai2d_output_tensor)

# ai2d 释放内存
def ai2d_release():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor
        del ai2d_input_tensor

# kpu 初始化
def kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        ai2d_init()
        return kpu_obj

# kpu 输入预处理
def kpu_pre_process(rgb888p_img):
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, ai2d_output_tensor)

# kpu 获得 kmodel 输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# kpu 运行
def kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    kpu_pre_process(rgb888p_img)
    # (2)行人检测 kpu 运行
    with ScopedTiming("kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放行人检测 ai2d 资源
    ai2d_release()
    # (4)获取行人检测 kpu 输出
    results = kpu_get_output()
    # (5)行人检测 kpu 结果后处理
    with ScopedTiming("kpu_post_process",debug_mode > 0):
        dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], kmodel_frame_size, frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)
    # (6)返回行人检测结果
    return dets

# kpu 释放内存
def kpu_deinit():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        if 'ai2d' in globals():
            global ai2d
            del ai2d
        if 'ai2d_output_tensor' in globals():
            global ai2d_output_tensor
            del ai2d_output_tensor
        if 'ai2d_builder' in globals():
            global ai2d_builder
            del ai2d_builder

#media_utils.py
global draw_img,osd_img,masks                               #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 框出所有检测到的人以及标出得分
def display_draw(dets):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img

        if dets:
            draw_img.clear()
            for det_box in dets:
                x1, y1, x2, y2 = det_box[2],det_box[3],det_box[4],det_box[5]
                w = float(x2 - x1) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                h = float(y2 - y1) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH

                x1 = int(x1 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                y1 = int(y1 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH)
                x2 = int(x2 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                y2 = int(y2 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH)

                if (h<(0.1*DISPLAY_HEIGHT)):
                    continue
                if (w<(0.25*DISPLAY_WIDTH) and ((x1<(0.03*DISPLAY_WIDTH)) or (x2>(0.97*DISPLAY_WIDTH)))):
                    continue
                if (w<(0.15*DISPLAY_WIDTH) and ((x1<(0.01*DISPLAY_WIDTH)) or (x2>(0.99*DISPLAY_WIDTH)))):
                    continue
                draw_img.draw_rectangle(x1 , y1 , int(w) , int(h) , color=(255, 0, 255, 0),thickness = 4)
                draw_img.draw_string( x1 , y1-50, " " + labels[det_box[0]] + " " + str(round(det_box[1],2)) , color=(255,0, 255, 0), scale=4)
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for person_detect.py**********
def person_detect_inference():
    print("person_detect_test start")
    kpu_person_detect = kpu_init(kmodel_file)                           # 创建行人检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)

        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",total_debug_mode):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    dets = kpu_run(kpu_person_detect,rgb888p_img)       # 执行行人检测 kpu 运行 以及 后处理过程
                    display_draw(dets)                                  # 将得到的检测结果 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)          # camera 释放图像

                if (count > 5):
                    gc.collect()
                    count = 0
                else:
                    count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        camera_stop(CAM_DEV_ID_0)                                       # 停止 camera
        display_deinit()                                                # 释放 display
        kpu_deinit()                                                    # 释放 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_person_detect

        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                            # 释放 整个media

    print("person_detect_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    person_detect_inference()
```

### 9.人体姿态估计

```python
import ulab.numpy as np             #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn         #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *          #摄像头模块
from media.display import *         #显示模块
from media.media import *           #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import image                        #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                         #时间统计
import gc                           #垃圾回收模块
import aidemo                       #aidemo模块，封装ai demo相关后处理、画图操作
import os, sys                  #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

#ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

#人体关键点检测 kmodel 输入参数配置
kmodel_input_shape = (1,3,640,640)          # kmodel输入分辨率
rgb_mean = [114,114,114]                    # ai2d padding 值

#人体关键点 相关参数设置
confidence_threshold = 0.2                  # 人体关键点检测分数阈值
nms_threshold = 0.5                         # 非最大值抑制阈值

#文件配置
root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/yolov8n-pose.kmodel'       # kmodel文件的路径
debug_mode = 0                                              # debug模式 大于0（调试）、 反之 （不调试）

#骨骼信息
SKELETON = [(16, 14),(14, 12),(17, 15),(15, 13),(12, 13),(6,  12),(7,  13),(6,  7),(6,  8),(7,  9),(8,  10),(9,  11),(2,  3),(1,  2),(1,  3),(2,  4),(3,  5),(4,  6),(5,  7)]
#肢体颜色
LIMB_COLORS = [(255, 51,  153, 255),(255, 51,  153, 255),(255, 51,  153, 255),(255, 51,  153, 255),(255, 255, 51,  255),(255, 255, 51,  255),(255, 255, 51,  255),(255, 255, 128, 0),(255, 255, 128, 0),(255, 255, 128, 0),(255, 255, 128, 0),(255, 255, 128, 0),(255, 0,   255, 0),(255, 0,   255, 0),(255, 0,   255, 0),(255, 0,   255, 0),(255, 0,   255, 0),(255, 0,   255, 0),(255, 0,   255, 0)]
#关键点颜色
KPS_COLORS = [(255, 0,   255, 0),(255, 0,   255, 0),(255, 0,   255, 0),(255, 0,   255, 0),(255, 0,   255, 0),(255, 255, 128, 0),(255, 255, 128, 0),(255, 255, 128, 0),(255, 255, 128, 0),(255, 255, 128, 0),(255, 255, 128, 0),(255, 51,  153, 255),(255, 51,  153, 255),(255, 51,  153, 255),(255, 51,  153, 255),(255, 51,  153, 255),(255, 51,  153, 255)]

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")


#ai_utils.py
global current_kmodel_obj                                           # 定义全局的 kpu 对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder       # 定义全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder

# 人体关键点检测 接收kmodel输出的后处理方法
def kpu_post_process(output_datas):
    with ScopedTiming("kpu_post_process", debug_mode > 0):
        results = aidemo.person_kp_postprocess(output_datas,[OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH],[kmodel_input_shape[2],kmodel_input_shape[3]],confidence_threshold,nms_threshold)
        return results

# 获取kmodel输入图像resize比例 以及 padding的上下左右像素数量
def get_pad_param():
    #右padding或下padding
    dst_w = kmodel_input_shape[3]
    dst_h = kmodel_input_shape[2]

    ratio_w = float(dst_w) / OUT_RGB888P_WIDTH
    ratio_h = float(dst_h) / OUT_RGB888P_HEIGHT
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h

    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGHT)
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2

    top = (int)(round(dh))
    bottom = (int)(round(dh))
    left = (int)(round(dw))
    right = (int)(round(dw))
    return [0, 0, 0, 0, top, bottom, left, right]

# ai2d 初始化
def ai2d_init():
    with ScopedTiming("ai2d_init",debug_mode > 0):
        global ai2d
        ai2d = nn.ai2d()
        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d.set_pad_param(True, get_pad_param(), 0, rgb_mean)
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        global ai2d_out_tensor
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_out_tensor = nn.from_numpy(data)

        global ai2d_builder
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], kmodel_input_shape)

# ai2d 运行
def ai2d_run(rgb888p_img):
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d_input_tensor,ai2d_out_tensor,ai2d_builder
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)

        ai2d_builder.run(ai2d_input_tensor, ai2d_out_tensor)

# ai2d 释放内存
def ai2d_release():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor
        del ai2d_input_tensor

# kpu 初始化
def kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        ai2d_init()
        return kpu_obj

# kpu 输入预处理
def kpu_pre_process(rgb888p_img):
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_out_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, ai2d_out_tensor)

# kpu 获得 kmodel 输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        del data

        return result

# kpu 运行
def kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1) 原图预处理，并设置模型输入
    kpu_pre_process(rgb888p_img)
    # (2) kpu 运行
    with ScopedTiming("kpu_run",debug_mode > 0):
        kpu_obj.run()
    # (3) 释放ai2d资源
    ai2d_release()
    # (4) 获取kpu输出
    results = kpu_get_output()
    # (5) kpu结果后处理
    kp_res = kpu_post_process(results)
    # (6) 返回 人体关键点检测 结果
    return kp_res

# kpu 释放内存
def kpu_deinit():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        if 'ai2d' in globals():
            global ai2d
            del ai2d
        if 'ai2d_out_tensor' in globals():
            global ai2d_out_tensor
            del ai2d_out_tensor
        if 'ai2d_builder' in globals():
            global ai2d_builder
            del ai2d_builder

#media_utils.py
global draw_img,osd_img                                     #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 将所有目标关键点作图
def display_draw(res):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if res[0]:
            draw_img.clear()
            kpses = res[1]
            for i in range(len(res[0])):
                for k in range(17+2):
                    if (k < 17):
                        kps_x = round(kpses[i][k][0])
                        kps_y = round(kpses[i][k][1])
                        kps_s = kpses[i][k][2]

                        kps_x1 = int(float(kps_x) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                        kps_y1 = int(float(kps_y) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)

                        if (kps_s > 0):
                            draw_img.draw_circle(kps_x1,kps_y1,5,KPS_COLORS[k],4)
                    ske = SKELETON[k]
                    pos1_x = round(kpses[i][ske[0]-1][0])
                    pos1_y = round(kpses[i][ske[0]-1][1])

                    pos1_x_ = int(float(pos1_x) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                    pos1_y_ = int(float(pos1_y) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)

                    pos2_x = round(kpses[i][(ske[1] -1)][0])
                    pos2_y = round(kpses[i][(ske[1] -1)][1])

                    pos2_x_ = int(float(pos2_x) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                    pos2_y_ = int(float(pos2_y) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)

                    pos1_s = kpses[i][(ske[0] -1)][2]
                    pos2_s = kpses[i][(ske[1] -1)][2]

                    if (pos1_s > 0.0 and pos2_s >0.0):
                        draw_img.draw_line(pos1_x,pos1_y,pos2_x,pos2_y,LIMB_COLORS[k],4)

        else:
            draw_img.clear()
        draw_img.copy_to(osd_img)
        display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()


#**********for person_kp_detect.py**********
def person_kp_detect_inference():
    print("person_kp_detect start")
    kpu_person_kp_detect = kpu_init(kmodel_file)                    # 创建人体关键点检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                       # 初始化 camera
    display_init()                                                  # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)

        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)             # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    person_kp_detect_res = kpu_run(kpu_person_kp_detect,rgb888p_img)            # 执行人体关键点检测 kpu 运行 以及 后处理过程
                    display_draw(person_kp_detect_res)                                          # 将得到的人体关键点结果 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)      # camera 释放图像

                if (count > 5):
                    gc.collect()
                    count = 0
                else:
                    count += 1

    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        camera_stop(CAM_DEV_ID_0)                                   # 停止 camera
        display_deinit()                                            # 释放 display
        kpu_deinit()                                                # 释放 kpu

        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_person_kp_detect

        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                        # 释放 整个media

    print("person_kp_detect end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    person_kp_detect_inference()
```

### 10.KWS

```python
from media.pyaudio import *                     # 音频模块
from media.media import *                       # 软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import media.wave as wave                       # wav音频处理模块
import nncase_runtime as nn                     # nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np                         # 类似python numpy操作，但也会有一些接口不同
import aidemo                                   # aidemo模块，封装ai demo相关前处理、后处理等操作
import time                                     # 时间统计
import struct                                   # 字节字符转换模块
import gc                                       # 垃圾回收模块
import os,sys                                   # 操作系统接口模块

# key word spotting任务
# 检测阈值
THRESH = 0.5
# 有关音频流的宏变量
SAMPLE_RATE = 16000         # 采样率16000Hz,即每秒采样16000次
CHANNELS = 1                # 通道数 1为单声道，2为立体声
FORMAT = paInt16            # 音频输入输出格式 paInt16
CHUNK = int(0.3 * 16000)    # 每次读取音频数据的帧数，设置为0.3s的帧数16000*0.3=4800

root_dir='/sdcard/app/tests/'
kmodel_file_kws = root_dir+"kmodel/kws.kmodel"      # kmodel加载路径
reply_wav_file = root_dir+"utils/wozai.wav"         # kws唤醒词回复音频路径
debug_mode = 0                                      # 调试模式，大于0（调试）、 反之 （不调试）


# scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

# 当前kmodel
global current_kmodel_obj                                                               # 定义全局kpu对象
global p,cache_np,fp,input_stream,output_stream,audio_input_tensor,cache_input_tensor   # 定义全局音频流对象，输入输出流对象，并且定义kws处理接口FeaturePipeline对象fp,输入输出tensor和缓冲cache_np

# 初始化kws音频流相关变量
def init_kws():
    with ScopedTiming("init_kws",debug_mode > 0):
        global p,cache_np,fp,input_stream,output_stream,cache_input_tensor
        # 初始化模型的cache输入
        cache_np = np.zeros((1, 256, 105), dtype=np.float)
        cache_input_tensor = nn.from_numpy(cache_np)
        # 初始化音频预处理接口
        fp = aidemo.kws_fp_create()
        # 初始化音频流
        p = PyAudio()
        p.initialize(CHUNK)
        media.buffer_init()
        # 用于采集实时音频数据
        input_stream = p.open(
                        format=FORMAT,
                        channels=CHANNELS,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=CHUNK
                        )

        # 用于播放回复音频
        output_stream = p.open(
                        format=FORMAT,
                        channels=CHANNELS,
                        rate=SAMPLE_RATE,
                        output=True,
                        frames_per_buffer=CHUNK
                        )

# kws 初始化kpu
def kpu_init_kws():
    with ScopedTiming("init_kpu",debug_mode > 0):
        # 初始化kpu并加载kmodel
        kpu = nn.kpu()
        kpu.load_kmodel(kmodel_file_kws)
        return kpu

# kws 释放kpu
def kpu_deinit():
    # kpu释放
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        global current_kmodel_obj,audio_input_tensor,cache_input_tensor
        if "current_kmodel_obj" in globals():
            del current_kmodel_obj
        if "audio_input_tensor" in globals():
            del audio_input_tensor
        if "cache_input_tensor" in globals():
            del cache_input_tensor

# kws音频预处理
def kpu_pre_process_kws(pcm_data_list):
    global current_kmodel_obj
    global fp,input_stream,audio_input_tensor,cache_input_tensor
    with ScopedTiming("pre_process",debug_mode > 0):
        # 将pcm数据处理为模型输入的特征向量
        mp_feats = aidemo.kws_preprocess(fp, pcm_data_list)[0]
        mp_feats_np = np.array(mp_feats)
        mp_feats_np = mp_feats_np.reshape((1, 30, 40))
        audio_input_tensor = nn.from_numpy(mp_feats_np)
        cache_input_tensor = nn.from_numpy(cache_np)
        current_kmodel_obj.set_input_tensor(0, audio_input_tensor)
        current_kmodel_obj.set_input_tensor(1, cache_input_tensor)

# kws任务kpu运行并完成后处理
def kpu_run_kws(kpu_obj,pcm_data_list):
    global current_kmodel_obj,cache_np,output_stream
    current_kmodel_obj = kpu_obj
    # （1）kws音频数据预处理
    kpu_pre_process_kws(pcm_data_list)
    # （2）kpu推理
    with ScopedTiming("kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）获取模型输出
    logits = kpu_obj.get_output_tensor(0)
    cache_tensor = kpu_obj.get_output_tensor(1)     # 更新缓存输入
    logits_np = logits.to_numpy()
    cache_np=cache_tensor.to_numpy()
    del logits
    del cache_tensor
    # （4）后处理argmax
    max_logits = np.max(logits_np, axis=1)[0]
    max_p = np.max(max_logits)
    idx = np.argmax(max_logits)
    # 如果分数大于阈值，且idx==1(即包含唤醒词)，播放回复音频
    if max_p > THRESH and idx == 1:
        print("====Detected XiaonanXiaonan!====")
        wf = wave.open(reply_wav_file, "rb")
        wav_data = wf.read_frames(CHUNK)
        while wav_data:
            output_stream.write(wav_data)
            wav_data = wf.read_frames(CHUNK)
        time.sleep(1) # 时间缓冲，用于播放声音
        wf.close()
    else:
        print("Deactivated!")


# kws推理过程
def kws_inference():
    # 记录音频帧帧数
    global p,fp,input_stream,output_stream,current_kmodel_obj
    # 初始化
    init_kws()
    kpu_kws=kpu_init_kws()
    pcm_data_list = []
    try:
        gc_count=0
        while True:
            os.exitpoint()
            with ScopedTiming("total", 1):
                pcm_data_list.clear()
                # 对实时音频流进行推理
                pcm_data = input_stream.read()  # 获取的音频流数据字节数，len(pcm_data)=0.3*16000*2=9600，即以16000Hz的采样率采样0.3s，每次采样数据为paInt16格式占2个字节
                # 获取音频流数据
                for i in range(0, len(pcm_data), 2):
                    # 每两个字节组织成一个有符号整数，然后将其转换为浮点数，即为一次采样的数据，加入到当前一帧（0.3s）的数据列表中
                    int_pcm_data = struct.unpack("<h", pcm_data[i:i+2])[0]
                    float_pcm_data = float(int_pcm_data)
                    pcm_data_list.append(float_pcm_data)
                # kpu运行和后处理
                kpu_run_kws(kpu_kws,pcm_data_list)
                if gc_count > 10:
                    gc.collect()
                    gc_count = 0
                else:
                    gc_count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        input_stream.stop_stream()
        output_stream.stop_stream()
        input_stream.close()
        output_stream.close()
        p.terminate()
        media.buffer_deinit()
        aidemo.kws_fp_destroy(fp)
        kpu_deinit()
        del kpu_kws
        if "current_kmodel_obj" in globals():
            del current_kmodel_obj
        gc.collect()
        nn.shrink_memory_pool()

if __name__=="__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    kws_inference()
```

### 11.跌倒检测

```python
import aicube                   #aicube模块，封装检测分割等任务相关后处理
from media.camera import *      #摄像头模块
from media.display import *     #显示模块
from media.media import *       #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区

import nncase_runtime as nn     #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np         #类似python numpy操作，但也会有一些接口不同

import time                     #时间统计
import image                    #图像模块，主要用于读取、图像绘制元素（框、点等）等操作

import gc                       #垃圾回收模块
import os, sys                  #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

##ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

#kmodel输入shape
kmodel_input_shape = (1,3,640,640)                  # kmodel输入分辨率

#kmodel相关参数设置
confidence_threshold = 0.3                          # 摔倒检测阈值，用于过滤roi
nms_threshold = 0.45                                # 摔倒检测框阈值，用于过滤重复roi
kmodel_frame_size = [640,640]                       # 摔倒检测输入图片尺寸
frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGHT] # 直接输入图片尺寸
strides = [8,16,32]                                 # 输出特征图的尺寸与输入图片尺寸的比
num_classes = 2                                     # 模型输出类别数
nms_option = False                                  # 是否所有检测框一起做NMS，False则按照不同的类分别应用NMS
labels = ["Fall","NoFall"]                          # 模型输出类别名称

root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/yolov5n-falldown.kmodel'                         # kmodel文件的路径
anchors = [10,13, 16,30, 33,23, 30,61, 62,45, 50,119, 116,90, 156,198, 373,326]   # anchor设置

colors = [(255,0, 0, 255), (255,0, 255, 0), (255,255,0, 0), (255,255,0, 255)]     # 颜色设置

debug_mode = 0                                      # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                       # 定义全局的 kpu 对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder   # 定义全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder


# ai2d 初始化
def ai2d_init():
    with ScopedTiming("ai2d_init",debug_mode > 0):
        global ai2d
        global ai2d_builder
        global ai2d_output_tensor
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = kmodel_frame_size[0]
        height = kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        ai2d = nn.ai2d()
        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,height,width])
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_output_tensor = nn.from_numpy(data)

# ai2d 运行
def ai2d_run(rgb888p_img):
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d_input_tensor,ai2d_output_tensor, ai2d_builder
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)
        ai2d_builder.run(ai2d_input_tensor, ai2d_output_tensor)

# ai2d 释放内存
def ai2d_release():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor
        del ai2d_input_tensor

# kpu 初始化
def kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        ai2d_init()
        return kpu_obj

# kpu 输入预处理
def kpu_pre_process(rgb888p_img):
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, ai2d_output_tensor)

# kpu 获得 kmodel 输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# kpu 运行
def kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    kpu_pre_process(rgb888p_img)
    # (2)摔倒检测 kpu 运行
    with ScopedTiming("kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放摔倒检测 ai2d 资源
    ai2d_release()
    # (4)获取摔倒检测 kpu 输出
    results = kpu_get_output()
    # (5)摔倒检测 kpu 结果后处理
    dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], kmodel_frame_size, frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)
    # (6)返回摔倒检测结果
    return dets

# kpu 释放内存
def kpu_deinit():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        global ai2d, ai2d_output_tensor, ai2d_builder
        if 'ai2d' in globals():                             #删除ai2d变量，释放对它所引用对象的内存引用
            global ai2d
            del ai2d
        if 'ai2d_output_tensor' in globals():               #删除ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global ai2d_output_tensor
            del ai2d_output_tensor
        if 'ai2d_builder' in globals():                     #删除ai2d_builder变量，释放对它所引用对象的内存引用
            global ai2d_builder
            del ai2d_builder

#media_utils.py
global draw_img,osd_img                                     #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 框出所有检测到的行人以及标出是否摔倒的结果
def display_draw(dets):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img

        if dets:
            draw_img.clear()
            for det_box in dets:
                x1, y1, x2, y2 = det_box[2],det_box[3],det_box[4],det_box[5]
                w = float(x2 - x1) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                h = float(y2 - y1) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT

                x1 = int(x1 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                y1 = int(y1 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)
                x2 = int(x2 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                y2 = int(y2 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)

                draw_img.draw_rectangle(x1 , y1 , int(w) , int(h) , color=colors[det_box[0]], thickness = 2)
                draw_img.draw_string( x1 , y1-20, " " + labels[det_box[0]] + " " + str(round(det_box[1],2)) , color=colors[det_box[0]+2], scale=4)
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()
    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)
    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for falldown_detect.py**********
def falldown_detect_inference():
    print("falldown_detect_test start")
    kpu_falldown_detect = kpu_init(kmodel_file)                         # 创建摔倒检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)
        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    dets = kpu_run(kpu_falldown_detect,rgb888p_img)     # 执行摔倒检测 kpu 运行 以及 后处理过程
                    display_draw(dets)                                  # 将得到的检测结果 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)          # camera 释放图像
                if (count>10):
                    gc.collect()
                    count = 0
                else:
                    count += 1

    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        camera_stop(CAM_DEV_ID_0)                                       # 停止 camera
        display_deinit()                                                # 释放 display
        kpu_deinit()                                                    # 释放 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_falldown_detect
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                                  # 释放 整个media

    print("falldown_detect_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    falldown_detect_inference()
```

## 三、AI Demo多模型示例解析

### 1. 人脸关键点检测

```python
import ulab.numpy as np                  # 类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn              # nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *               # 摄像头模块
from media.display import *              # 显示模块
from media.media import *                # 软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import aidemo                            # aidemo模块，封装ai demo相关后处理、画图操作
import image                             # 图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                              # 时间统计
import gc                                # 垃圾回收模块
import os, sys                           # 操作系统接口模块
import math                              # 数学模块


#********************for config.py********************
# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)                   # 显示宽度要求16位对齐
DISPLAY_HEIGHT = 1080

# ai原图分辨率，sensor默认出图为16:9，若需不形变原图，最好按照16:9比例设置宽高
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)               # ai原图宽度要求16位对齐
OUT_RGB888P_HEIGH = 1080

# kmodel参数设置
# 人脸检测kmodel输入shape
fd_kmodel_input_shape = (1,3,320,320)
# 人脸关键点kmodel输入shape
fld_kmodel_input_shape = (1,3,192,192)
# ai原图padding
rgb_mean = [104,117,123]

#人脸检测kmodel其它参数设置
confidence_threshold = 0.5               # 人脸检测阈值
top_k = 5000
nms_threshold = 0.2
keep_top_k = 750
vis_thres = 0.5
variance = [0.1, 0.2]
anchor_len = 4200
score_dim = 2
det_dim = 4
keypoint_dim = 10

# 文件配置
# 人脸检测kmodel
root_dir = '/sdcard/app/tests/'
fd_kmodel_file = root_dir + 'kmodel/face_detection_320.kmodel'
# 人脸关键点kmodel
fr_kmodel_file = root_dir + 'kmodel/face_landmark.kmodel'
# anchor文件
anchors_path = root_dir + 'utils/prior_data_320.bin'
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0

# 人脸关键点不同部位关键点列表
dict_kp_seq = [
    [43, 44, 45, 47, 46, 50, 51, 49, 48],              # left_eyebrow
    [97, 98, 99, 100, 101, 105, 104, 103, 102],        # right_eyebrow
    [35, 36, 33, 37, 39, 42, 40, 41],                  # left_eye
    [89, 90, 87, 91, 93, 96, 94, 95],                  # right_eye
    [34, 88],                                          # pupil
    [72, 73, 74, 86],                                  # bridge_nose
    [77, 78, 79, 80, 85, 84, 83],                      # wing_nose
    [52, 55, 56, 53, 59, 58, 61, 68, 67, 71, 63, 64],  # out_lip
    [65, 54, 60, 57, 69, 70, 62, 66],                  # in_lip
    [1, 9, 10, 11, 12, 13, 14, 15, 16, 2, 3, 4, 5, 6, 7, 8, 0, 24, 23, 22, 21, 20, 19, 18, 32, 31, 30, 29, 28, 27, 26, 25, 17]  # basin
]

# 人脸关键点不同部位（顺序同dict_kp_seq）颜色配置，argb
color_list_for_osd_kp = [
    (255, 0, 255, 0),
    (255, 0, 255, 0),
    (255, 255, 0, 255),
    (255, 255, 0, 255),
    (255, 255, 0, 0),
    (255, 255, 170, 0),
    (255, 255, 255, 0),
    (255, 0, 255, 255),
    (255, 255, 220, 50),
    (255, 30, 30, 255)
]

#********************for scoped_timing.py********************
# 时间统计类
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#********************for ai_utils.py********************
global current_kmodel_obj #当前kpu对象
# fd_ai2d：               人脸检测ai2d实例
# fd_ai2d_input_tensor：  人脸检测ai2d输入
# fd_ai2d_output_tensor： 人脸检测ai2d输入
# fd_ai2d_builder：       根据人脸检测ai2d参数，构建的人脸检测ai2d_builder对象
global fd_ai2d,fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
# fld_ai2d：              人脸关键点ai2d实例
# fld_ai2d_input_tensor： 人脸关键点ai2d输入
# fld_ai2d_output_tensor：人脸关键点ai2d输入
# fld_ai2d_builder：      根据人脸关键点ai2d参数，构建的人脸关键点ai2d_builder对象
global fld_ai2d,fld_ai2d_input_tensor,fld_ai2d_output_tensor,fld_ai2d_builder
global matrix_dst         #人脸仿射变换矩阵

#读取anchor文件，为人脸检测后处理做准备
print('anchors_path:',anchors_path)
prior_data = np.fromfile(anchors_path, dtype=np.float)
prior_data = prior_data.reshape((anchor_len,det_dim))

def get_pad_one_side_param():
    # 右padding或下padding，获取padding参数
    dst_w = fd_kmodel_input_shape[3]                         # kmodel输入宽（w）
    dst_h = fd_kmodel_input_shape[2]                          # kmodel输入高（h）

    # OUT_RGB888P_WIDTH：原图宽（w）
    # OUT_RGB888P_HEIGH：原图高（h）
    # 计算最小的缩放比例，等比例缩放
    ratio_w = dst_w / OUT_RGB888P_WIDTH
    ratio_h = dst_h / OUT_RGB888P_HEIGH
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h
    # 计算经过缩放后的新宽和新高
    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGH)

    # 计算需要添加的padding，以使得kmodel输入的宽高和原图一致
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2
    # 四舍五入，确保padding是整数
    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

def fd_ai2d_init():
    # 人脸检测模型ai2d初始化
    with ScopedTiming("fd_ai2d_init",debug_mode > 0):
        # （1）创建人脸检测ai2d对象
        global fd_ai2d
        fd_ai2d = nn.ai2d()
        # （2）设置人脸检测ai2d参数
        fd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        fd_ai2d.set_pad_param(True, get_pad_one_side_param(), 0, rgb_mean)
        fd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        #（3）人脸检测ai2d_builder，根据人脸检测ai2d参数、输入输出大小创建ai2d_builder对象
        global fd_ai2d_builder
        fd_ai2d_builder = fd_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fd_kmodel_input_shape)

        #（4）创建人脸检测ai2d_output_tensor，用于保存人脸检测ai2d输出
        global fd_ai2d_output_tensor
        data = np.ones(fd_kmodel_input_shape, dtype=np.uint8)
        fd_ai2d_output_tensor = nn.from_numpy(data)

def fd_ai2d_run(rgb888p_img):
    # 根据人脸检测ai2d参数，对原图rgb888p_img进行预处理
    with ScopedTiming("fd_ai2d_run",debug_mode > 0):
        global fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
        # （1）根据原图构建ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        fd_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        # （2）运行人脸检测ai2d_builder，将结果保存到人脸检测ai2d_output_tensor中
        fd_ai2d_builder.run(fd_ai2d_input_tensor, fd_ai2d_output_tensor)

def fd_ai2d_release():
    # 释放人脸检测ai2d_input_tensor
    with ScopedTiming("fd_ai2d_release",debug_mode > 0):
        global fd_ai2d_input_tensor
        del fd_ai2d_input_tensor


def fd_kpu_init(kmodel_file):
    # 初始化人脸检测kpu对象，并加载kmodel
    with ScopedTiming("fd_kpu_init",debug_mode > 0):
        # 初始化人脸检测kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸检测kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸检测ai2d
        fd_ai2d_init()
        return kpu_obj

def fd_kpu_pre_process(rgb888p_img):
    # 设置人脸检测kpu输入
    # 使用人脸检测ai2d对原图进行预处理（padding，resize）
    fd_ai2d_run(rgb888p_img)
    with ScopedTiming("fd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fd_ai2d_output_tensor
        # 设置人脸检测kpu输入
        current_kmodel_obj.set_input_tensor(0, fd_ai2d_output_tensor)

def fd_kpu_get_output():
    # 获取人脸检测kpu输出
    with ScopedTiming("fd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取模型输出，并将结果转换为numpy，以便进行人脸检测后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

def fd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）原图预处理，并设置模型输入
    fd_kpu_pre_process(rgb888p_img)
    # （2）人脸检测kpu推理
    with ScopedTiming("fd kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸检测ai2d资源
    fd_ai2d_release()
    # （4）获取人俩检测kpu输出
    results = fd_kpu_get_output()
    # （5）人脸检测kpu结果后处理
    with ScopedTiming("fd kpu_post",debug_mode > 0):
        post_ret = aidemo.face_det_post_process(confidence_threshold,nms_threshold,fd_kmodel_input_shape[2],prior_data,
                [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH],results)
    # （6）返回人脸检测框
    if len(post_ret)==0:
        return post_ret
    else:
        return post_ret[0]          #0:det,1:landm,2:score

def fd_kpu_deinit():
    # kpu释放
    with ScopedTiming("fd_kpu_deinit",debug_mode > 0):
        if 'fd_ai2d' in globals():
            global fd_ai2d
            del fd_ai2d               #删除人脸检测ai2d变量，释放对它所引用对象的内存引用
        if 'fd_ai2d_output_tensor' in globals():
            global fd_ai2d_output_tensor
            del fd_ai2d_output_tensor   #删除人脸检测ai2d_output_tensor变量，释放对它所引用对象的内存引用

###############for face recognition###############
def get_affine_matrix(bbox):
    # 获取仿射矩阵，用于将边界框映射到模型输入空间
    with ScopedTiming("get_affine_matrix", debug_mode > 1):
        # 从边界框提取坐标和尺寸
        x1, y1, w, h = map(lambda x: int(round(x, 0)), bbox[:4])
        # 计算缩放比例，使得边界框映射到模型输入空间的一部分
        scale_ratio = (fld_kmodel_input_shape[2]) / (max(w, h) * 1.5)
        # 计算边界框中心点在模型输入空间的坐标
        cx = (x1 + w / 2) * scale_ratio
        cy = (y1 + h / 2) * scale_ratio
        # 计算模型输入空间的一半长度
        half_input_len = fld_kmodel_input_shape[2] / 2

        # 创建仿射矩阵并进行设置
        matrix_dst = np.zeros((2, 3), dtype=np.float)
        matrix_dst[0, 0] = scale_ratio
        matrix_dst[0, 1] = 0
        matrix_dst[0, 2] = half_input_len - cx
        matrix_dst[1, 0] = 0
        matrix_dst[1, 1] = scale_ratio
        matrix_dst[1, 2] = half_input_len - cy
        return matrix_dst

def fld_ai2d_init():
    # 人脸关键点ai2d初始化
    with ScopedTiming("fld_ai2d_init",debug_mode > 0):
        # （1）创建人脸关键点ai2d对象
        global fld_ai2d
        fld_ai2d = nn.ai2d()

        # （2）创建人脸关键点ai2d_output_tensor对象，用于存放ai2d输出
        global fld_ai2d_output_tensor
        data = np.ones(fld_kmodel_input_shape, dtype=np.uint8)
        fld_ai2d_output_tensor = nn.from_numpy(data)

def fld_ai2d_run(rgb888p_img,det):
    # 人脸关键点ai2d推理
    with ScopedTiming("fld_ai2d_run",debug_mode > 0):
        global fld_ai2d,fld_ai2d_input_tensor,fld_ai2d_output_tensor
        #（1）根据原图ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        fld_ai2d_input_tensor = nn.from_numpy(ai2d_input)

        # （2）根据新的det设置新的人脸关键点ai2d参数
        fld_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        global matrix_dst
        matrix_dst = get_affine_matrix(det)
        affine_matrix = [matrix_dst[0][0],matrix_dst[0][1],matrix_dst[0][2],
            matrix_dst[1][0],matrix_dst[1][1],matrix_dst[1][2]]
        fld_ai2d.set_affine_param(True,nn.interp_method.cv2_bilinear,0, 0, 127, 1,affine_matrix)

        # （3）根据新的人脸关键点ai2d参数，构建人脸关键点ai2d_builder
        global fld_ai2d_builder
        fld_ai2d_builder = fld_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fld_kmodel_input_shape)
        # （4）推理人脸关键点ai2d，将预处理的结果保存到fld_ai2d_output_tensor
        fld_ai2d_builder.run(fld_ai2d_input_tensor, fld_ai2d_output_tensor)

def fld_ai2d_release():
    # 释放人脸关键点ai2d_input_tensor、ai2d_builder
    with ScopedTiming("fld_ai2d_release",debug_mode > 0):
        global fld_ai2d_input_tensor,fld_ai2d_builder
        del fld_ai2d_input_tensor
        del fld_ai2d_builder

def fld_kpu_init(kmodel_file):
    # 人脸关键点kpu初始化
    with ScopedTiming("fld_kpu_init",debug_mode > 0):
        # 初始化人脸关键点kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸关键点kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸关键点ai2d
        fld_ai2d_init()
        return kpu_obj

def fld_kpu_pre_process(rgb888p_img,det):
    # 人脸关键点kpu预处理
    # 人脸关键点ai2d推理，根据det对原图进行预处理
    fld_ai2d_run(rgb888p_img,det)
    with ScopedTiming("fld_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fld_ai2d_output_tensor
        # 将人脸关键点ai2d输出设置为人脸关键点kpu输入
        current_kmodel_obj.set_input_tensor(0, fld_ai2d_output_tensor)
        #ai2d_out_data = fld_ai2d_output_tensor.to_numpy()
        #with open("/sdcard/app/ai2d_out.bin", "wb") as file:
            #file.write(ai2d_out_data.tobytes())

def fld_kpu_get_output():
    with ScopedTiming("fld_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取人脸关键点kpu输出
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        del data
        return result

def fld_kpu_post_process(pred):
    # 人脸关键点kpu推理结果后处理
    with ScopedTiming("fld_kpu_post_process",debug_mode > 0):
        # （1）将人脸关键点输出变换模型输入
        half_input_len = fld_kmodel_input_shape[2] // 2
        pred = pred.flatten()
        for i in range(len(pred)):
            pred[i] += (pred[i] + 1) * half_input_len

        # （2）获取仿射矩阵的逆矩阵
        global matrix_dst
        matrix_dst_inv = aidemo.invert_affine_transform(matrix_dst)
        matrix_dst_inv = matrix_dst_inv.flatten()

        # （3）对每个关键点进行逆变换
        half_out_len = len(pred) // 2
        for kp_id in range(half_out_len):
            old_x = pred[kp_id * 2]
            old_y = pred[kp_id * 2 + 1]

            # 逆变换公式
            new_x = old_x * matrix_dst_inv[0] + old_y * matrix_dst_inv[1] + matrix_dst_inv[2]
            new_y = old_x * matrix_dst_inv[3] + old_y * matrix_dst_inv[4] + matrix_dst_inv[5]

            pred[kp_id * 2] = new_x
            pred[kp_id * 2 + 1] = new_y

    return pred

def fld_kpu_run(kpu_obj,rgb888p_img,det):
    # 人脸关键点kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）人脸关键点kpu预处理，设置kpu输入
    fld_kpu_pre_process(rgb888p_img,det)
    # （2）人脸关键点kpu推理
    with ScopedTiming("fld_kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸关键点ai2d
    fld_ai2d_release()
    # （4）获取人脸关键点kpu输出
    result = fld_kpu_get_output()
    # （5）人脸关键点后处理
    result = fld_kpu_post_process(result)
    return result

def fld_kpu_deinit():
    # 人脸关键点kpu释放
    with ScopedTiming("fld_kpu_deinit",debug_mode > 0):
        if 'fld_ai2d' in globals():
            global fld_ai2d
            del fld_ai2d
        if 'fld_ai2d_output_tensor' in globals():
            global fld_ai2d_output_tensor
            del fld_ai2d_output_tensor

#********************for media_utils.py********************
global draw_img_ulab,draw_img,osd_img                       #for display
global buffer,media_source,media_sink                       #for media

# for display，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.2
def display_init():
    # 设置使用hdmi进行显示
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

def display_deinit():
    # 释放显示资源
    display.deinit()

def display_draw(dets,landmark_preds):
    # 在显示器画人脸轮廓
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img_ulab,draw_img,osd_img
        if dets:
            draw_img.clear()
            for pred in landmark_preds:
                # （1）获取单个人脸框对应的人脸关键点
                for sub_part_index in range(len(dict_kp_seq)):
                    # （2）构建人脸某个区域关键点集
                    sub_part = dict_kp_seq[sub_part_index]
                    face_sub_part_point_set = []
                    for kp_index in range(len(sub_part)):
                        real_kp_index = sub_part[kp_index]
                        x, y = pred[real_kp_index * 2], pred[real_kp_index * 2 + 1]

                        x = int(x * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                        y = int(y * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH)
                        face_sub_part_point_set.append((x, y))

                    # （3）画人脸不同区域的轮廓
                    if sub_part_index in (9, 6):
                        color = np.array(color_list_for_osd_kp[sub_part_index],dtype = np.uint8)
                        face_sub_part_point_set = np.array(face_sub_part_point_set)

                        aidemo.polylines(draw_img_ulab, face_sub_part_point_set,False,color,5,8,0)

                    elif sub_part_index == 4:
                        color = color_list_for_osd_kp[sub_part_index]
                        for kp in face_sub_part_point_set:
                            x,y = kp[0],kp[1]
                            draw_img.draw_circle(x,y ,2, color, 1)
                    else:
                        color = np.array(color_list_for_osd_kp[sub_part_index],dtype = np.uint8)
                        face_sub_part_point_set = np.array(face_sub_part_point_set)
                        aidemo.contours(draw_img_ulab, face_sub_part_point_set,-1,color,2,8)

            # （4）将轮廓结果拷贝到osd
            draw_img.copy_to(osd_img)
            # （5）将osd显示到屏幕
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            # （1）清空用来画框的图像
            draw_img.clear()
            # （2）清空osd
            draw_img.copy_to(osd_img)
            # （3）显示透明图层
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.1
def camera_init(dev_id):
    # camera初始化
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

def camera_start(dev_id):
    # camera启动
    camera.start_stream(dev_id)

def camera_read(dev_id):
    # 读取一帧图像
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

def camera_release_image(dev_id,rgb888p_img):
    # 释放一帧图像
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

def camera_stop(dev_id):
    # 停止camera
    camera.stop_stream(dev_id)

#for media，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.3
def media_init():
    # meida初始化
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img_ulab,draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 用于画框
    draw_img_ulab = np.zeros((DISPLAY_HEIGHT,DISPLAY_WIDTH,4),dtype=np.uint8)
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, alloc=image.ALLOC_REF,data = draw_img_ulab)
    # 用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

def media_deinit():
    # meida资源释放
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#********************for face_detect.py********************
def face_landmark_inference():
    print("face_landmark_test start")
    # 人脸检测kpu初始化
    kpu_face_detect = fd_kpu_init(fd_kmodel_file)
    # 人脸关键点kpu初始化
    kpu_face_landmark = fld_kpu_init(fr_kmodel_file)
    # camera初始化
    camera_init(CAM_DEV_ID_0)
    # 显示初始化
    display_init()

    # 注意：将一定要将一下过程包在try中，用于保证程序停止后，资源释放完毕；确保下次程序仍能正常运行
    try:
        # 注意：媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）
        media_init()

        # 启动camera
        camera_start(CAM_DEV_ID_0)
        gc_count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                # （1）读取一帧图像
                rgb888p_img = camera_read(CAM_DEV_ID_0)
                # （2）若读取成功，推理当前帧
                if rgb888p_img.format() == image.RGBP888:
                    # （2.1）推理当前图像，并获取人脸检测结果
                    dets = fd_kpu_run(kpu_face_detect,rgb888p_img)
                    # （2.2）针对每个人脸框，推理得到对应人脸关键点
                    landmark_result = []
                    for det in dets:
                        ret = fld_kpu_run(kpu_face_landmark,rgb888p_img,det)
                        landmark_result.append(ret)
                    # （2.3）将人脸关键点画到屏幕上
                    display_draw(dets,landmark_result)

                # （3）释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)
                if gc_count > 5:
                    gc.collect()
                    gc_count = 0
                else:
                    gc_count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        # 捕捉运行运行中异常，并打印错误
        sys.print_exception(e)
    finally:
        # 停止camera
        camera_stop(CAM_DEV_ID_0)
        # 释放显示资源
        display_deinit()
        # 释放kpu资源
        fd_kpu_deinit()
        fld_kpu_deinit()
        global current_kmodel_obj
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_face_detect
        del kpu_face_landmark
        nn.shrink_memory_pool()
        if 'draw_img' in globals():
            global draw_img
            del draw_img
        if 'draw_img_ulab' in globals():
            global draw_img_ulab
            del draw_img_ulab
        # 垃圾回收
        gc.collect()
        # 释放媒体资源
        media_deinit()

    print("face_landmark_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    face_landmark_inference()
```

### 2. 人脸识别

**人脸注册：**

```python
import ulab.numpy as np                  #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn              #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import aidemo                            #aidemo模块，封装ai demo相关后处理、画图操作
import image                             #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                              #时间统计
import gc                                #垃圾回收模块
import os,sys                                #操作系统接口模块
import math                              #数学模块

#********************for config.py********************
# kmodel输入shape
# 人脸检测kmodel输入shape
fd_kmodel_input_shape = (1,3,320,320)
# 人脸识别kmodel输入shape
fr_kmodel_input_shape = (1,3,112,112)
# ai原图padding
rgb_mean = [104,117,123]

#kmodel相关参数设置
#人脸检测
confidence_threshold = 0.5           #人脸检测阈值
top_k = 5000
nms_threshold = 0.2
keep_top_k = 750
vis_thres = 0.5
variance = [0.1, 0.2]
anchor_len = 4200
score_dim = 2
det_dim = 4
keypoint_dim = 10
#人脸识别
max_register_face = 100              #数据库最多人脸个数
feature_num = 128                    #人脸识别特征维度

# 文件配置
# 人脸检测kmodel
root_dir = '/sdcard/app/tests/'
fd_kmodel_file = root_dir + 'kmodel/face_detection_320.kmodel'
# 人脸识别kmodel
fr_kmodel_file = root_dir + 'kmodel/face_recognition.kmodel'
# 人脸检测anchor
anchors_path = root_dir + 'utils/prior_data_320.bin'
# 人脸注册数据库
database_dir = root_dir + 'utils/db/'
# 人脸注册数据库原图
database_img_dir = root_dir + 'utils/db_img/'
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0

#********************for scoped_timing.py********************
# 时间统计类
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#********************for ai_utils.py********************
global current_kmodel_obj #当前kpu实例
# fd_ai2d：               人脸检测ai2d实例
# fd_ai2d_input_tensor：  人脸检测ai2d输入
# fd_ai2d_output_tensor： 人脸检测ai2d输入
# fd_ai2d_builder：       根据人脸检测ai2d参数，构建的人脸检测ai2d_builder对象
global fd_ai2d,fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
# fr_ai2d：               人脸识别ai2d实例
# fr_ai2d_input_tensor：  人脸识别ai2d输入
# fr_ai2d_output_tensor： 人脸识别ai2d输入
# fr_ai2d_builder：       根据人脸识别ai2d参数，构建的人脸识别ai2d_builder对象
global fr_ai2d,fr_ai2d_input_tensor,fr_ai2d_output_tensor,fr_ai2d_builder
global valid_register_face #数据库中有效人脸个数

#读取anchor文件，为人脸检测后处理做准备
print('anchors_path:',anchors_path)
prior_data = np.fromfile(anchors_path, dtype=np.float)
prior_data = prior_data.reshape((anchor_len,det_dim))

def get_pad_one_side_param(rgb888p_img):
    # 右padding或下padding，获取padding参数
    with ScopedTiming("get_pad_one_side_param", debug_mode > 1):
        dst_w = fd_kmodel_input_shape[3]                         # kmodel输入宽（w）
        dst_h = fd_kmodel_input_shape[2]                         # kmodel输入高（h）

        # 计算最小的缩放比例，等比例缩放
        ratio_w = dst_w / rgb888p_img.shape[3]
        ratio_h = dst_h / rgb888p_img.shape[2]
        if ratio_w < ratio_h:
            ratio = ratio_w
        else:
            ratio = ratio_h

        # 计算经过缩放后的新宽和新高
        new_w = (int)(ratio * rgb888p_img.shape[3])
        new_h = (int)(ratio * rgb888p_img.shape[2])

        # 计算需要添加的padding，以使得kmodel输入的宽高和原图一致
        dw = (dst_w - new_w) / 2
        dh = (dst_h - new_h) / 2
        # 四舍五入，确保padding是整数
        top = (int)(round(0))
        bottom = (int)(round(dh * 2 + 0.1))
        left = (int)(round(0))
        right = (int)(round(dw * 2 - 0.1))
        return [0, 0, 0, 0, top, bottom, left, right]

def fd_ai2d_init():
    # 人脸检测模型ai2d初始化
    with ScopedTiming("fd_ai2d_init",debug_mode > 0):
        # （1）创建人脸检测ai2d对象
        global fd_ai2d
        fd_ai2d = nn.ai2d()

        #（2）创建人脸检测ai2d_output_tensor，用于保存人脸检测ai2d输出
        global fd_ai2d_output_tensor
        data = np.ones(fd_kmodel_input_shape, dtype=np.uint8)
        fd_ai2d_output_tensor = nn.from_numpy(data)

def fd_ai2d_run(rgb888p_img):
    # 根据人脸检测ai2d参数，对原图rgb888p_img进行预处理
    with ScopedTiming("fd_ai2d_run",debug_mode > 0):
        global fd_ai2d,fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
        # （1）根据原图构建ai2d_input_tensor对象
        fd_ai2d_input_tensor = nn.from_numpy(rgb888p_img)
        # （2）根据新的图像设置新的人脸检测ai2d参数
        fd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        fd_ai2d.set_pad_param(True, get_pad_one_side_param(rgb888p_img), 0, rgb_mean)
        fd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
        # （3）根据新的人脸检测ai2d参数，构建人脸检测ai2d_builder
        fd_ai2d_builder = fd_ai2d.build(rgb888p_img.shape, fd_kmodel_input_shape)
        # （4）运行人脸检测ai2d_builder，将结果保存到人脸检测ai2d_output_tensor中
        fd_ai2d_builder.run(fd_ai2d_input_tensor, fd_ai2d_output_tensor)

def fd_ai2d_release():
    # 释放人脸检测ai2d部分资源
    with ScopedTiming("fd_ai2d_release",debug_mode > 0):
        global fd_ai2d_input_tensor,fd_ai2d_builder
        del fd_ai2d_input_tensor
        del fd_ai2d_builder


def fd_kpu_init(kmodel_file):
    # 初始化人脸检测kpu对象，并加载kmodel
    with ScopedTiming("fd_kpu_init",debug_mode > 0):
        # 初始化人脸检测kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸检测kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸检测ai2d
        fd_ai2d_init()
        return kpu_obj

def fd_kpu_pre_process(rgb888p_img):
    # 设置人脸检测kpu输入
    # 使用人脸检测ai2d对原图进行预处理（padding，resize）
    fd_ai2d_run(rgb888p_img)
    with ScopedTiming("fd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fd_ai2d_output_tensor
        # 设置人脸检测kpu输入
        current_kmodel_obj.set_input_tensor(0, fd_ai2d_output_tensor)

def fd_kpu_get_output():
    # 获取人脸检测kpu输出
    with ScopedTiming("fd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取模型输出，并将结果转换为numpy，以便进行人脸检测后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

def fd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）原图预处理，并设置模型输入
    fd_kpu_pre_process(rgb888p_img)
    # （2）人脸检测kpu推理
    with ScopedTiming("fd kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸检测ai2d资源
    fd_ai2d_release()
    # （4）获取人俩检测kpu输出
    results = fd_kpu_get_output()
    # （5）人脸检测kpu结果后处理
    with ScopedTiming("fd kpu_post",debug_mode > 0):
        post_ret = aidemo.face_det_post_process(confidence_threshold,nms_threshold,fd_kmodel_input_shape[2],prior_data,
                [rgb888p_img.shape[3],rgb888p_img.shape[2]],results)
    # （6）返回人脸关键点
    if len(post_ret)==0:
        return post_ret
    else:
        return post_ret[0],post_ret[1]          #0:det,1:landm,2:score

def fd_kpu_deinit():
    # kpu释放
    with ScopedTiming("fd_kpu_deinit",debug_mode > 0):
        if 'fd_ai2d' in globals():     #删除人脸检测ai2d变量，释放对它所引用对象的内存引用
            global fd_ai2d
            del fd_ai2d
        if 'fd_ai2d_output_tensor' in globals():#删除人脸检测ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global fd_ai2d_output_tensor
            del fd_ai2d_output_tensor


###############for face recognition###############
# 标准5官
umeyama_args_112 = [
    38.2946 , 51.6963 ,
    73.5318 , 51.5014 ,
    56.0252 , 71.7366 ,
    41.5493 , 92.3655 ,
    70.7299 , 92.2041
]

def svd22(a):
    # svd
    s = [0.0, 0.0]
    u = [0.0, 0.0, 0.0, 0.0]
    v = [0.0, 0.0, 0.0, 0.0]

    s[0] = (math.sqrt((a[0] - a[3]) ** 2 + (a[1] + a[2]) ** 2) + math.sqrt((a[0] + a[3]) ** 2 + (a[1] - a[2]) ** 2)) / 2
    s[1] = abs(s[0] - math.sqrt((a[0] - a[3]) ** 2 + (a[1] + a[2]) ** 2))
    v[2] = math.sin((math.atan2(2 * (a[0] * a[1] + a[2] * a[3]), a[0] ** 2 - a[1] ** 2 + a[2] ** 2 - a[3] ** 2)) / 2) if \
    s[0] > s[1] else 0
    v[0] = math.sqrt(1 - v[2] ** 2)
    v[1] = -v[2]
    v[3] = v[0]
    u[0] = -(a[0] * v[0] + a[1] * v[2]) / s[0] if s[0] != 0 else 1
    u[2] = -(a[2] * v[0] + a[3] * v[2]) / s[0] if s[0] != 0 else 0
    u[1] = (a[0] * v[1] + a[1] * v[3]) / s[1] if s[1] != 0 else -u[2]
    u[3] = (a[2] * v[1] + a[3] * v[3]) / s[1] if s[1] != 0 else u[0]
    v[0] = -v[0]
    v[2] = -v[2]

    return u, s, v


def image_umeyama_112(src):
    # 使用Umeyama算法计算仿射变换矩阵
    SRC_NUM = 5
    SRC_DIM = 2
    src_mean = [0.0, 0.0]
    dst_mean = [0.0, 0.0]

    for i in range(0,SRC_NUM * 2,2):
        src_mean[0] += src[i]
        src_mean[1] += src[i + 1]
        dst_mean[0] += umeyama_args_112[i]
        dst_mean[1] += umeyama_args_112[i + 1]

    src_mean[0] /= SRC_NUM
    src_mean[1] /= SRC_NUM
    dst_mean[0] /= SRC_NUM
    dst_mean[1] /= SRC_NUM

    src_demean = [[0.0, 0.0] for _ in range(SRC_NUM)]
    dst_demean = [[0.0, 0.0] for _ in range(SRC_NUM)]

    for i in range(SRC_NUM):
        src_demean[i][0] = src[2 * i] - src_mean[0]
        src_demean[i][1] = src[2 * i + 1] - src_mean[1]
        dst_demean[i][0] = umeyama_args_112[2 * i] - dst_mean[0]
        dst_demean[i][1] = umeyama_args_112[2 * i + 1] - dst_mean[1]

    A = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(SRC_DIM):
        for k in range(SRC_DIM):
            for j in range(SRC_NUM):
                A[i][k] += dst_demean[j][i] * src_demean[j][k]
            A[i][k] /= SRC_NUM

    T = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    U, S, V = svd22([A[0][0], A[0][1], A[1][0], A[1][1]])

    T[0][0] = U[0] * V[0] + U[1] * V[2]
    T[0][1] = U[0] * V[1] + U[1] * V[3]
    T[1][0] = U[2] * V[0] + U[3] * V[2]
    T[1][1] = U[2] * V[1] + U[3] * V[3]

    scale = 1.0
    src_demean_mean = [0.0, 0.0]
    src_demean_var = [0.0, 0.0]
    for i in range(SRC_NUM):
        src_demean_mean[0] += src_demean[i][0]
        src_demean_mean[1] += src_demean[i][1]

    src_demean_mean[0] /= SRC_NUM
    src_demean_mean[1] /= SRC_NUM

    for i in range(SRC_NUM):
        src_demean_var[0] += (src_demean_mean[0] - src_demean[i][0]) * (src_demean_mean[0] - src_demean[i][0])
        src_demean_var[1] += (src_demean_mean[1] - src_demean[i][1]) * (src_demean_mean[1] - src_demean[i][1])

    src_demean_var[0] /= SRC_NUM
    src_demean_var[1] /= SRC_NUM

    scale = 1.0 / (src_demean_var[0] + src_demean_var[1]) * (S[0] + S[1])
    T[0][2] = dst_mean[0] - scale * (T[0][0] * src_mean[0] + T[0][1] * src_mean[1])
    T[1][2] = dst_mean[1] - scale * (T[1][0] * src_mean[0] + T[1][1] * src_mean[1])
    T[0][0] *= scale
    T[0][1] *= scale
    T[1][0] *= scale
    T[1][1] *= scale
    return T

def get_affine_matrix(sparse_points):
    # 获取affine变换矩阵
    with ScopedTiming("get_affine_matrix", debug_mode > 1):
        # 使用Umeyama算法计算仿射变换矩阵
        matrix_dst = image_umeyama_112(sparse_points)
        matrix_dst = [matrix_dst[0][0],matrix_dst[0][1],matrix_dst[0][2],
            matrix_dst[1][0],matrix_dst[1][1],matrix_dst[1][2]]
        return matrix_dst

def fr_ai2d_init():
    with ScopedTiming("fr_ai2d_init",debug_mode > 0):
        # （1）人脸识别ai2d初始化
        global fr_ai2d
        fr_ai2d = nn.ai2d()

        # （2）人脸识别ai2d_output_tensor初始化，用于存放ai2d输出
        global fr_ai2d_output_tensor
        data = np.ones(fr_kmodel_input_shape, dtype=np.uint8)
        fr_ai2d_output_tensor = nn.from_numpy(data)

def fr_ai2d_run(rgb888p_img,sparse_points):
    # 人脸识别ai2d推理
    with ScopedTiming("fr_ai2d_run",debug_mode > 0):
        global fr_ai2d,fr_ai2d_input_tensor,fr_ai2d_output_tensor
        #（1）根据原图创建人脸识别ai2d_input_tensor对象
        fr_ai2d_input_tensor = nn.from_numpy(rgb888p_img)
        #（2）根据新的人脸关键点设置新的人脸识别ai2d参数
        fr_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        affine_matrix = get_affine_matrix(sparse_points)
        fr_ai2d.set_affine_param(True,nn.interp_method.cv2_bilinear,0, 0, 127, 1,affine_matrix)
        global fr_ai2d_builder
        # （3）根据新的人脸识别ai2d参数，构建识别ai2d_builder
        fr_ai2d_builder = fr_ai2d.build(rgb888p_img.shape, fr_kmodel_input_shape)
        # （4）推理人脸识别ai2d，将预处理的结果保存到fr_ai2d_output_tensor
        fr_ai2d_builder.run(fr_ai2d_input_tensor, fr_ai2d_output_tensor)

def fr_ai2d_release():
    # 释放人脸识别ai2d_input_tensor、ai2d_builder
    with ScopedTiming("fr_ai2d_release",debug_mode > 0):
        global fr_ai2d_input_tensor,fr_ai2d_builder
        del fr_ai2d_input_tensor
        del fr_ai2d_builder

def fr_kpu_init(kmodel_file):
    # 人脸识别kpu初始化
    with ScopedTiming("fr_kpu_init",debug_mode > 0):
        # 初始化人脸识别kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸识别kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸识别ai2d
        fr_ai2d_init()
        return kpu_obj

def fr_kpu_pre_process(rgb888p_img,sparse_points):
    # 人脸识别kpu预处理
    # 人脸识别ai2d推理，根据关键点对原图进行预处理
    fr_ai2d_run(rgb888p_img,sparse_points)
    with ScopedTiming("fr_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fr_ai2d_output_tensor
        # 将人脸识别ai2d输出设置为人脸识别kpu输入
        current_kmodel_obj.set_input_tensor(0, fr_ai2d_output_tensor)

        #ai2d_out_data = fr_ai2d_output_tensor.to_numpy()
        #print('ai2d_out_data.shape:',ai2d_out_data.shape)
        #with open("/sdcard/app/ai2d_out.bin", "wb") as file:
            #file.write(ai2d_out_data.tobytes())

def fr_kpu_get_output():
    # 获取人脸识别kpu输出
    with ScopedTiming("fr_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        del data
        return result[0]

def fr_kpu_run(kpu_obj,rgb888p_img,sparse_points):
    # 人脸识别kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）人脸识别kpu预处理,设置kpu输入
    fr_kpu_pre_process(rgb888p_img,sparse_points)
    # （2）人脸识别kpu推理
    with ScopedTiming("fr kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸识别ai2d
    fr_ai2d_release()
    # （4）获取人脸识别kpu输出
    results = fr_kpu_get_output()
    return results

def fr_kpu_deinit():
    # 人脸识别kpu相关资源释放
    with ScopedTiming("fr_kpu_deinit",debug_mode > 0):
        if 'fr_ai2d' in globals():
            global fr_ai2d
            del fr_ai2d
        if 'fr_ai2d_output_tensor' in globals():
            global fr_ai2d_output_tensor
            del fr_ai2d_output_tensor

#********************for face_detect.py********************
def image2rgb888array(img):   #4维
    # 将Image转换为rgb888格式
    with ScopedTiming("fr_kpu_deinit",debug_mode > 0):
        img_data_rgb888=img.to_rgb888()
        # hwc,rgb888
        img_hwc=img_data_rgb888.to_numpy_ref()
        shape=img_hwc.shape
        img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
        img_tmp_trans = img_tmp.transpose()
        img_res=img_tmp_trans.copy()
        # chw,rgb888
        img_return=img_res.reshape((1,shape[2],shape[0],shape[1]))
    return  img_return

def face_registration_inference():
    print("face_registration_test start")
    # 人脸检测kpu初始化
    kpu_face_detect = fd_kpu_init(fd_kmodel_file)
    # 人脸识别kpu初始化
    kpu_face_reg = fr_kpu_init(fr_kmodel_file)
    try:
        # 获取图像列表
        img_list = os.listdir(database_img_dir)
        for img_file in img_list:
            os.exitpoint()
            with ScopedTiming("total",1):
                # （1）读取一张图像
                full_img_file = database_img_dir + img_file
                print(full_img_file)
                img = image.Image(full_img_file)
                rgb888p_img_ndarry = image2rgb888array(img)

                #（2）推理得到人脸检测kpu，得到人脸检测框、人脸五点
                dets,landms = fd_kpu_run(kpu_face_detect,rgb888p_img_ndarry)
                if dets:
                    if dets.shape[0] == 1:
                        #（3）若是只检测到一张人脸，则将该人脸注册到数据库
                        db_i_name = img_file.split('.')[0]
                        for landm in landms:
                            reg_result = fr_kpu_run(kpu_face_reg,rgb888p_img_ndarry,landm)
                            #print('\nwrite bin:',database_dir+'{}.bin'.format(db_i_name))
                            with open(database_dir+'{}.bin'.format(db_i_name), "wb") as file:
                                file.write(reg_result.tobytes())
                    else:
                        print('Only one person in a picture when you sign up')
                else:
                    print('No person detected')

                gc.collect()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        # 释放kpu资源
        fd_kpu_deinit()
        fr_kpu_deinit()
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_face_detect
        del kpu_face_reg
        # 垃圾回收
        gc.collect()
        nn.shrink_memory_pool()

    print("face_registration_test end")
    return 0

if __name__ == '__main__':
    nn.shrink_memory_pool()
    face_registration_inference()
```

**人脸识别：**

```python
import ulab.numpy as np                  # 类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn              # nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *               # 摄像头模块
from media.display import *              # 显示模块
from media.media import *                # 软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import aidemo                            # aidemo模块，封装ai demo相关后处理、画图操作
import image                             # 图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                              # 时间统计
import gc                                # 垃圾回收模块
import os,sys                                # 操作系统接口模块
import math                              # 数学模块

#********************for config.py********************
# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)                   # 显示宽度要求16位对齐
DISPLAY_HEIGHT = 1080

# ai原图分辨率，sensor默认出图为16:9，若需不形变原图，最好按照16:9比例设置宽高
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)               # ai原图宽度要求16位对齐
OUT_RGB888P_HEIGH = 1080

# kmodel输入shape
# 人脸检测kmodel输入shape
fd_kmodel_input_shape = (1,3,320,320)
# 人脸识别kmodel输入shape
fr_kmodel_input_shape = (1,3,112,112)
# ai原图padding
rgb_mean = [104,117,123]

#kmodel相关参数设置
#人脸检测
confidence_threshold = 0.5               #人脸检测阈值
top_k = 5000
nms_threshold = 0.2
keep_top_k = 750
vis_thres = 0.5
variance = [0.1, 0.2]
anchor_len = 4200
score_dim = 2
det_dim = 4
keypoint_dim = 10
#人脸识别
max_register_face = 100                  # 数据库最多人脸个数
feature_num = 128                        # 人脸识别特征维度
face_recognition_threshold = 0.75        # 人脸识别阈值

#文件配置
# 人脸检测kmodel
root_dir = '/sdcard/app/tests/'
fd_kmodel_file = root_dir + 'kmodel/face_detection_320.kmodel'
# 人脸识别kmodel
fr_kmodel_file = root_dir + 'kmodel/face_recognition.kmodel'
# 人脸检测anchor
anchors_path = root_dir + 'utils/prior_data_320.bin'
# 人脸数据库
database_dir = root_dir + 'utils/db/'
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0

#********************for scoped_timing.py********************
# 时间统计类
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#********************for ai_utils.py********************
global current_kmodel_obj #当前kpu实例
# fd_ai2d：               人脸检测ai2d实例
# fd_ai2d_input_tensor：  人脸检测ai2d输入
# fd_ai2d_output_tensor： 人脸检测ai2d输入
# fd_ai2d_builder：       根据人脸检测ai2d参数，构建的人脸检测ai2d_builder对象
global fd_ai2d,fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
# fr_ai2d：               人脸识别ai2d实例
# fr_ai2d_input_tensor：  人脸识别ai2d输入
# fr_ai2d_output_tensor： 人脸识别ai2d输入
# fr_ai2d_builder：       根据人脸识别ai2d参数，构建的人脸识别ai2d_builder对象
global fr_ai2d,fr_ai2d_input_tensor,fr_ai2d_output_tensor,fr_ai2d_builder
# valid_register_face：   数据库中有效人脸个数
# db_name：               数据库人名列表
# db_data：               数据库特征列表
global valid_register_face,db_name，db_data

#读取anchor文件，为人脸检测后处理做准备
print('anchors_path:',anchors_path)
prior_data = np.fromfile(anchors_path, dtype=np.float)
prior_data = prior_data.reshape((anchor_len,det_dim))

def get_pad_one_side_param():
    # 右padding或下padding，获取padding参数
    dst_w = fd_kmodel_input_shape[3]                         # kmodel输入宽（w）
    dst_h = fd_kmodel_input_shape[2]                          # kmodel输入高（h）

    # OUT_RGB888P_WIDTH：原图宽（w）
    # OUT_RGB888P_HEIGH：原图高（h）
    # 计算最小的缩放比例，等比例缩放
    ratio_w = dst_w / OUT_RGB888P_WIDTH
    ratio_h = dst_h / OUT_RGB888P_HEIGH
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h
    # 计算经过缩放后的新宽和新高
    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGH)

    # 计算需要添加的padding，以使得kmodel输入的宽高和原图一致
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2
    # 四舍五入，确保padding是整数
    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

def fd_ai2d_init():
    # 人脸检测模型ai2d初始化
    with ScopedTiming("fd_ai2d_init",debug_mode > 0):
        # （1）创建人脸检测ai2d对象
        global fd_ai2d
        fd_ai2d = nn.ai2d()
        # （2）设置人脸检测ai2d参数
        fd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        fd_ai2d.set_pad_param(True, get_pad_one_side_param(), 0, rgb_mean)
        fd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        #（3）人脸检测ai2d_builder，根据人脸检测ai2d参数、输入输出大小创建ai2d_builder对象
        global fd_ai2d_builder
        fd_ai2d_builder = fd_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fd_kmodel_input_shape)

        #（4）创建人脸检测ai2d_output_tensor，用于保存人脸检测ai2d输出
        global fd_ai2d_output_tensor
        data = np.ones(fd_kmodel_input_shape, dtype=np.uint8)
        fd_ai2d_output_tensor = nn.from_numpy(data)

def fd_ai2d_run(rgb888p_img):
    # 根据人脸检测ai2d参数，对原图rgb888p_img进行预处理
    with ScopedTiming("fd_ai2d_run",debug_mode > 0):
        global fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
        # （1）根据原图构建ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        fd_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        # （2）运行人脸检测ai2d_builder，将结果保存到人脸检测ai2d_output_tensor中
        fd_ai2d_builder.run(fd_ai2d_input_tensor, fd_ai2d_output_tensor)

def fd_ai2d_release():
    # 释放人脸检测ai2d_input_tensor
    with ScopedTiming("fd_ai2d_release",debug_mode > 0):
        global fd_ai2d_input_tensor
        del fd_ai2d_input_tensor


def fd_kpu_init(kmodel_file):
    # 初始化人脸检测kpu对象，并加载kmodel
    with ScopedTiming("fd_kpu_init",debug_mode > 0):
        # 初始化人脸检测kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸检测kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸检测ai2d
        fd_ai2d_init()
        return kpu_obj

def fd_kpu_pre_process(rgb888p_img):
    # 设置人脸检测kpu输入
    # 使用人脸检测ai2d对原图进行预处理（padding，resize）
    fd_ai2d_run(rgb888p_img)
    with ScopedTiming("fd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fd_ai2d_output_tensor
        # 设置人脸检测kpu输入
        current_kmodel_obj.set_input_tensor(0, fd_ai2d_output_tensor)

def fd_kpu_get_output():
    # 获取人脸检测kpu输出
    with ScopedTiming("fd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取模型输出，并将结果转换为numpy，以便进行人脸检测后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

def fd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）原图预处理，并设置模型输入
    fd_kpu_pre_process(rgb888p_img)
    # （2）人脸检测kpu推理
    with ScopedTiming("fd kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸检测ai2d资源
    fd_ai2d_release()
    # （4）获取人俩检测kpu输出
    results = fd_kpu_get_output()
    # （5）人脸检测kpu结果后处理
    with ScopedTiming("fd kpu_post",debug_mode > 0):
        post_ret = aidemo.face_det_post_process(confidence_threshold,nms_threshold,fd_kmodel_input_shape[2],prior_data,
                [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH],results)
    # （6）返回人脸检测框
    if len(post_ret)==0:
        return post_ret,post_ret
    else:
        return post_ret[0],post_ret[1]          #0:det,1:landm,2:score

def fd_kpu_deinit():
    # kpu释放
    with ScopedTiming("fd_kpu_deinit",debug_mode > 0):
        if 'fd_ai2d' in globals():     #删除人脸检测ai2d变量，释放对它所引用对象的内存引用
            global fd_ai2d
            del fd_ai2d
        if 'fd_ai2d_output_tensor' in globals():#删除人脸检测ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global fd_ai2d_output_tensor
            del fd_ai2d_output_tensor

###############for face recognition###############
##for database
def database_init():
    # 数据初始化，构建数据库人名列表和数据库特征列表
    with ScopedTiming("database_init", debug_mode > 1):
        global valid_register_face,db_name,db_data
        valid_register_face = 0
        db_name = []
        db_data = []

        db_file_list = os.listdir(database_dir)
        for db_file in db_file_list:
            if not db_file.endswith('.bin'):
                continue
            if valid_register_face >= max_register_face:
                break
            valid_index = valid_register_face
            full_db_file = database_dir + db_file
            with open(full_db_file, 'rb') as f:
                data = f.read()
            feature = np.frombuffer(data, dtype=np.float)
            db_data.append(feature)
            name = db_file.split('.')[0]
            db_name.append(name)
            valid_register_face += 1

def database_reset():
    # 数据库清空
    with ScopedTiming("database_reset", debug_mode > 1):
        global valid_register_face,db_name,db_data
        print("database clearing...")
        db_name = []
        db_data = []
        valid_register_face = 0
        print("database clear Done!")

def database_search(feature):
    # 数据库查询
    with ScopedTiming("database_search", debug_mode > 1):
        global valid_register_face,db_name,db_data
        v_id = -1
        v_score_max = 0.0

        # 将当前人脸特征归一化
        feature /= np.linalg.norm(feature)
        # 遍历当前人脸数据库，统计最高得分
        for i in range(valid_register_face):
            db_feature = db_data[i]
            db_feature /= np.linalg.norm(db_feature)
            # 计算数据库特征与当前人脸特征相似度
            v_score = np.dot(feature, db_feature)/2 + 0.5
            if v_score > v_score_max:
                v_score_max = v_score
                v_id = i

        if v_id == -1:
            # 数据库中无人脸
            return 'unknown'
        elif v_score_max < face_recognition_threshold:
            # 小于人脸识别阈值，未识别
#            print('v_score_max:',v_score_max)
            return 'unknown'
        else:
            # 识别成功
            result = 'name: {}, score:{}'.format(db_name[v_id],v_score_max)
            return result

# 标准5官
umeyama_args_112 = [
    38.2946 , 51.6963 ,
    73.5318 , 51.5014 ,
    56.0252 , 71.7366 ,
    41.5493 , 92.3655 ,
    70.7299 , 92.2041
]

def svd22(a):
    # svd
    s = [0.0, 0.0]
    u = [0.0, 0.0, 0.0, 0.0]
    v = [0.0, 0.0, 0.0, 0.0]

    s[0] = (math.sqrt((a[0] - a[3]) ** 2 + (a[1] + a[2]) ** 2) + math.sqrt((a[0] + a[3]) ** 2 + (a[1] - a[2]) ** 2)) / 2
    s[1] = abs(s[0] - math.sqrt((a[0] - a[3]) ** 2 + (a[1] + a[2]) ** 2))
    v[2] = math.sin((math.atan2(2 * (a[0] * a[1] + a[2] * a[3]), a[0] ** 2 - a[1] ** 2 + a[2] ** 2 - a[3] ** 2)) / 2) if \
    s[0] > s[1] else 0
    v[0] = math.sqrt(1 - v[2] ** 2)
    v[1] = -v[2]
    v[3] = v[0]
    u[0] = -(a[0] * v[0] + a[1] * v[2]) / s[0] if s[0] != 0 else 1
    u[2] = -(a[2] * v[0] + a[3] * v[2]) / s[0] if s[0] != 0 else 0
    u[1] = (a[0] * v[1] + a[1] * v[3]) / s[1] if s[1] != 0 else -u[2]
    u[3] = (a[2] * v[1] + a[3] * v[3]) / s[1] if s[1] != 0 else u[0]
    v[0] = -v[0]
    v[2] = -v[2]

    return u, s, v


def image_umeyama_112(src):
    # 使用Umeyama算法计算仿射变换矩阵
    SRC_NUM = 5
    SRC_DIM = 2
    src_mean = [0.0, 0.0]
    dst_mean = [0.0, 0.0]

    for i in range(0,SRC_NUM * 2,2):
        src_mean[0] += src[i]
        src_mean[1] += src[i + 1]
        dst_mean[0] += umeyama_args_112[i]
        dst_mean[1] += umeyama_args_112[i + 1]

    src_mean[0] /= SRC_NUM
    src_mean[1] /= SRC_NUM
    dst_mean[0] /= SRC_NUM
    dst_mean[1] /= SRC_NUM

    src_demean = [[0.0, 0.0] for _ in range(SRC_NUM)]
    dst_demean = [[0.0, 0.0] for _ in range(SRC_NUM)]

    for i in range(SRC_NUM):
        src_demean[i][0] = src[2 * i] - src_mean[0]
        src_demean[i][1] = src[2 * i + 1] - src_mean[1]
        dst_demean[i][0] = umeyama_args_112[2 * i] - dst_mean[0]
        dst_demean[i][1] = umeyama_args_112[2 * i + 1] - dst_mean[1]

    A = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(SRC_DIM):
        for k in range(SRC_DIM):
            for j in range(SRC_NUM):
                A[i][k] += dst_demean[j][i] * src_demean[j][k]
            A[i][k] /= SRC_NUM

    T = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    U, S, V = svd22([A[0][0], A[0][1], A[1][0], A[1][1]])

    T[0][0] = U[0] * V[0] + U[1] * V[2]
    T[0][1] = U[0] * V[1] + U[1] * V[3]
    T[1][0] = U[2] * V[0] + U[3] * V[2]
    T[1][1] = U[2] * V[1] + U[3] * V[3]

    scale = 1.0
    src_demean_mean = [0.0, 0.0]
    src_demean_var = [0.0, 0.0]
    for i in range(SRC_NUM):
        src_demean_mean[0] += src_demean[i][0]
        src_demean_mean[1] += src_demean[i][1]

    src_demean_mean[0] /= SRC_NUM
    src_demean_mean[1] /= SRC_NUM

    for i in range(SRC_NUM):
        src_demean_var[0] += (src_demean_mean[0] - src_demean[i][0]) * (src_demean_mean[0] - src_demean[i][0])
        src_demean_var[1] += (src_demean_mean[1] - src_demean[i][1]) * (src_demean_mean[1] - src_demean[i][1])

    src_demean_var[0] /= SRC_NUM
    src_demean_var[1] /= SRC_NUM

    scale = 1.0 / (src_demean_var[0] + src_demean_var[1]) * (S[0] + S[1])
    T[0][2] = dst_mean[0] - scale * (T[0][0] * src_mean[0] + T[0][1] * src_mean[1])
    T[1][2] = dst_mean[1] - scale * (T[1][0] * src_mean[0] + T[1][1] * src_mean[1])
    T[0][0] *= scale
    T[0][1] *= scale
    T[1][0] *= scale
    T[1][1] *= scale
    return T

def get_affine_matrix(sparse_points):
    # 获取放射变换矩阵
    with ScopedTiming("get_affine_matrix", debug_mode > 1):
        # 使用Umeyama算法计算仿射变换矩阵
        matrix_dst = image_umeyama_112(sparse_points)
        matrix_dst = [matrix_dst[0][0],matrix_dst[0][1],matrix_dst[0][2],
            matrix_dst[1][0],matrix_dst[1][1],matrix_dst[1][2]]
        return matrix_dst

def fr_ai2d_init():
    with ScopedTiming("fr_ai2d_init",debug_mode > 0):
        # （1）人脸识别ai2d初始化
        global fr_ai2d
        fr_ai2d = nn.ai2d()

        # （2）人脸识别ai2d_output_tensor初始化，用于存放ai2d输出
        global fr_ai2d_output_tensor
        data = np.ones(fr_kmodel_input_shape, dtype=np.uint8)
        fr_ai2d_output_tensor = nn.from_numpy(data)

def fr_ai2d_run(rgb888p_img,sparse_points):
    # 人脸识别ai2d推理
    with ScopedTiming("fr_ai2d_run",debug_mode > 0):
        global fr_ai2d,fr_ai2d_input_tensor,fr_ai2d_output_tensor
        #（1）根据原图创建人脸识别ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        fr_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        #（2）根据新的人脸关键点设置新的人脸识别ai2d参数
        fr_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        affine_matrix = get_affine_matrix(sparse_points)
        fr_ai2d.set_affine_param(True,nn.interp_method.cv2_bilinear,0, 0, 127, 1,affine_matrix)
        global fr_ai2d_builder
        # （3）根据新的人脸识别ai2d参数，构建识别ai2d_builder
        fr_ai2d_builder = fr_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fr_kmodel_input_shape)
        # （4）推理人脸识别ai2d，将预处理的结果保存到fr_ai2d_output_tensor
        fr_ai2d_builder.run(fr_ai2d_input_tensor, fr_ai2d_output_tensor)

def fr_ai2d_release():
    # 释放人脸识别ai2d_input_tensor、ai2d_builder
    with ScopedTiming("fr_ai2d_release",debug_mode > 0):
        global fr_ai2d_input_tensor,fr_ai2d_builder
        del fr_ai2d_input_tensor
        del fr_ai2d_builder

def fr_kpu_init(kmodel_file):
    # 人脸识别kpu初始化
    with ScopedTiming("fr_kpu_init",debug_mode > 0):
        # 初始化人脸识别kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸识别kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸识别ai2d
        fr_ai2d_init()
        # 数据库初始化
        database_init()
        return kpu_obj

def fr_kpu_pre_process(rgb888p_img,sparse_points):
    # 人脸识别kpu预处理
    # 人脸识别ai2d推理，根据关键点对原图进行预处理
    fr_ai2d_run(rgb888p_img,sparse_points)
    with ScopedTiming("fr_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fr_ai2d_output_tensor
        # 将人脸识别ai2d输出设置为人脸识别kpu输入
        current_kmodel_obj.set_input_tensor(0, fr_ai2d_output_tensor)

def fr_kpu_get_output():
    # 获取人脸识别kpu输出
    with ScopedTiming("fr_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        del data
        return result[0]

def fr_kpu_run(kpu_obj,rgb888p_img,sparse_points):
    # 人脸识别kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）人脸识别kpu预处理,设置kpu输入
    fr_kpu_pre_process(rgb888p_img,sparse_points)
    # （2）人脸识别kpu推理
    with ScopedTiming("fr kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸识别ai2d
    fr_ai2d_release()
    # （4）获取人脸识别kpu输出
    results = fr_kpu_get_output()
    # （5）在数据库中查找当前人脸特征
    recg_result = database_search(results)
    return recg_result

def fr_kpu_deinit():
    # 人脸识别kpu相关资源释放
    with ScopedTiming("fr_kpu_deinit",debug_mode > 0):
        if 'fr_ai2d' in globals():
            global fr_ai2d
            del fr_ai2d
        if 'fr_ai2d_output_tensor' in globals():
            global fr_ai2d_output_tensor
            del fr_ai2d_output_tensor

#********************for media_utils.py********************
global draw_img,osd_img                                     #for display
global buffer,media_source,media_sink                       #for media

# for display，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.2
def display_init():
    # hdmi显示初始化
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

def display_deinit():
    # 释放显示资源
    display.deinit()

def display_draw(dets,recg_results):
    # 在显示器上写人脸识别结果
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if dets:
            draw_img.clear()
            for i,det in enumerate(dets):
                # （1）画人脸框
                x1, y1, w, h = map(lambda x: int(round(x, 0)), det[:4])
                x1 = x1 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                y1 = y1 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
                w =  w * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                h = h * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
                draw_img.draw_rectangle(x1,y1, w, h, color=(255,0, 0, 255), thickness = 4)

                # （2）写人脸识别结果
                recg_text = recg_results[i]
                draw_img.draw_string(x1,y1,recg_text,color=(255, 255, 0, 0),scale=4)

            # （3）将画图结果拷贝到osd
            draw_img.copy_to(osd_img)
            # （4）将osd显示到屏幕
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            # （1）清空用来画框的图像
            draw_img.clear()
            # （2）清空osd
            draw_img.copy_to(osd_img)
            # （3）显示透明图层
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.1
def camera_init(dev_id):
    # camera初始化
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_BGR_888_PLANAR)

def camera_start(dev_id):
    # camera启动
    camera.start_stream(dev_id)

def camera_read(dev_id):
    # 读取一帧图像
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

def camera_release_image(dev_id,rgb888p_img):
    # 释放一帧图像
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

def camera_stop(dev_id):
    # 停止camera
    camera.stop_stream(dev_id)

#for media，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.3
def media_init():
    # meida初始化
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

def media_deinit():
    # meida资源释放
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#********************for face_detect.py********************
def face_recognition_inference():
    print("face_recognition_test start")
    # 人脸检测kpu初始化
    kpu_face_detect = fd_kpu_init(fd_kmodel_file)
    # 人脸关键点kpu初始化
    kpu_face_recg = fr_kpu_init(fr_kmodel_file)
    # camera初始化
    camera_init(CAM_DEV_ID_0)
    # 显示初始化
    display_init()

    # 注意：将一定要将一下过程包在try中，用于保证程序停止后，资源释放完毕；确保下次程序仍能正常运行
    try:
        # 注意：媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）
        media_init()

        # 启动camera
        camera_start(CAM_DEV_ID_0)
        gc_count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                # （1）读取一帧图像
                rgb888p_img = camera_read(CAM_DEV_ID_0)

                # （2）若读取成功，推理当前帧
                if rgb888p_img.format() == image.RGBP888:
                    # （2.1）推理当前图像，并获取人脸检测结果
                    dets,landms = fd_kpu_run(kpu_face_detect,rgb888p_img)
                    recg_result = []
                    for landm in landms:
                        # （2.2）针对每个人脸五官点，推理得到人脸特征，并计算特征在数据库中相似度
                        ret = fr_kpu_run(kpu_face_recg,rgb888p_img,landm)
                        recg_result.append(ret)
                    # （2.3）将识别结果画到显示器上
                    display_draw(dets,recg_result)

                # （3）释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)
                if gc_count > 5:
                    gc.collect()
                    gc_count = 0
                else:
                    gc_count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        # 停止camera
        camera_stop(CAM_DEV_ID_0)
        # 释放显示资源
        display_deinit()
        # 释放kpu资源
        fd_kpu_deinit()
        fr_kpu_deinit()
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_face_detect
        del kpu_face_recg
        # 垃圾回收
        gc.collect()
        nn.shrink_memory_pool()
        # 释放媒体资源
        media_deinit()

    print("face_recognition_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    face_recognition_inference()
```

### 3.人脸姿态角

```python
import ulab.numpy as np                  # 类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn              # nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *               # 摄像头模块
from media.display import *              # 显示模块
from media.media import *                # 软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import aidemo                            # aidemo模块，封装ai demo相关后处理、画图操作
import image                             # 图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                              # 时间统计
import gc                                # 垃圾回收模块
import os,sys                            # 操作系统接口模块
import math                              # 数学模块

#********************for config.py********************
# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)                   # 显示宽度要求16位对齐
DISPLAY_HEIGHT = 1080

# ai原图分辨率，sensor默认出图为16:9，若需不形变原图，最好按照16:9比例设置宽高
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)               # ai原图宽度要求16位对齐
OUT_RGB888P_HEIGH = 1080

# kmodel参数设置
# 人脸检测kmodel输入shape
fd_kmodel_input_shape = (1,3,320,320)
# 人脸姿态估计kmodel输入shape
fp_kmodel_input_shape = (1,3,120,120)
# ai原图padding
rgb_mean = [104,117,123]

#人脸检测kmodel其它参数设置
confidence_threshold = 0.5                     # 人脸检测阈值
top_k = 5000
nms_threshold = 0.2
keep_top_k = 750
vis_thres = 0.5
variance = [0.1, 0.2]
anchor_len = 4200
score_dim = 2
det_dim = 4
keypoint_dim = 10

# 文件配置
# 人脸检测kmodel文件配置
root_dir = '/sdcard/app/tests/'
fd_kmodel_file = root_dir + 'kmodel/face_detection_320.kmodel'
# 人脸姿态估计kmodel文件配置
fp_kmodel_file = root_dir + 'kmodel/face_pose.kmodel'
# anchor文件配置
anchors_path = root_dir + 'utils/prior_data_320.bin'
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0

#********************for scoped_timing.py********************
# 时间统计类
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#********************for ai_utils.py********************
global current_kmodel_obj #当前kpu对象
# fd_ai2d：               人脸检测ai2d实例
# fd_ai2d_input_tensor：  人脸检测ai2d输入
# fd_ai2d_output_tensor： 人脸检测ai2d输入
# fd_ai2d_builder：       根据人脸检测ai2d参数，构建的人脸检测ai2d_builder对象
global fd_ai2d,fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
# fld_ai2d：              人脸姿态估计ai2d实例
# fld_ai2d_input_tensor： 人脸姿态估计ai2d输入
# fld_ai2d_output_tensor：人脸姿态估计ai2d输入
# fld_ai2d_builder：      根据人脸姿态估计ai2d参数，构建的人脸姿态估计ai2d_builder对象
global fp_ai2d,fp_ai2d_input_tensor,fp_ai2d_output_tensor,fp_ai2d_builder
global matrix_dst         #人脸仿射变换矩阵
#读取anchor文件，为人脸检测后处理做准备
print('anchors_path:',anchors_path)
prior_data = np.fromfile(anchors_path, dtype=np.float)
prior_data = prior_data.reshape((anchor_len,det_dim))

def get_pad_one_side_param():
    # 右padding或下padding，获取padding参数
    dst_w = fd_kmodel_input_shape[3]                         # kmodel输入宽（w）
    dst_h = fd_kmodel_input_shape[2]                          # kmodel输入高（h）

    # OUT_RGB888P_WIDTH：原图宽（w）
    # OUT_RGB888P_HEIGH：原图高（h）
    # 计算最小的缩放比例，等比例缩放
    ratio_w = dst_w / OUT_RGB888P_WIDTH
    ratio_h = dst_h / OUT_RGB888P_HEIGH
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h
    # 计算经过缩放后的新宽和新高
    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGH)

    # 计算需要添加的padding，以使得kmodel输入的宽高和原图一致
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2
    # 四舍五入，确保padding是整数
    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

def fd_ai2d_init():
    # 人脸检测模型ai2d初始化
    with ScopedTiming("fd_ai2d_init",debug_mode > 0):
        # （1）创建人脸检测ai2d对象
        global fd_ai2d
        fd_ai2d = nn.ai2d()
        # （2）设置人脸检测ai2d参数
        fd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        fd_ai2d.set_pad_param(True, get_pad_one_side_param(), 0, rgb_mean)
        fd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        #（3）人脸检测ai2d_builder，根据人脸检测ai2d参数、输入输出大小创建ai2d_builder对象
        global fd_ai2d_builder
        fd_ai2d_builder = fd_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fd_kmodel_input_shape)

        #（4）创建人脸检测ai2d_output_tensor，用于保存人脸检测ai2d输出
        global fd_ai2d_output_tensor
        data = np.ones(fd_kmodel_input_shape, dtype=np.uint8)
        fd_ai2d_output_tensor = nn.from_numpy(data)

def fd_ai2d_run(rgb888p_img):
    # 根据人脸检测ai2d参数，对原图rgb888p_img进行预处理
    with ScopedTiming("fd_ai2d_run",debug_mode > 0):
        global fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
        # （1）根据原图构建ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        fd_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        # （2）运行人脸检测ai2d_builder，将结果保存到人脸检测ai2d_output_tensor中
        fd_ai2d_builder.run(fd_ai2d_input_tensor, fd_ai2d_output_tensor)

def fd_ai2d_release():
    # 释放人脸检测ai2d_input_tensor
    with ScopedTiming("fd_ai2d_release",debug_mode > 0):
        global fd_ai2d_input_tensor
        del fd_ai2d_input_tensor


def fd_kpu_init(kmodel_file):
    # 初始化人脸检测kpu对象，并加载kmodel
    with ScopedTiming("fd_kpu_init",debug_mode > 0):
        # 初始化人脸检测kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸检测kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸检测ai2d
        fd_ai2d_init()
        return kpu_obj

def fd_kpu_pre_process(rgb888p_img):
    # 设置人脸检测kpu输入
    # 使用人脸检测ai2d对原图进行预处理（padding，resize）
    fd_ai2d_run(rgb888p_img)
    with ScopedTiming("fd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fd_ai2d_output_tensor
        # 设置人脸检测kpu输入
        current_kmodel_obj.set_input_tensor(0, fd_ai2d_output_tensor)

def fd_kpu_get_output():
    # 获取人脸检测kpu输出
    with ScopedTiming("fd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取模型输出，并将结果转换为numpy，以便进行人脸检测后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

def fd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）原图预处理，并设置模型输入
    fd_kpu_pre_process(rgb888p_img)
    # （2）人脸检测kpu推理
    with ScopedTiming("fd kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸检测ai2d资源
    fd_ai2d_release()
    # （4）获取人俩检测kpu输出
    results = fd_kpu_get_output()
    # （5）人脸检测kpu结果后处理
    with ScopedTiming("fd kpu_post",debug_mode > 0):
        post_ret = aidemo.face_det_post_process(confidence_threshold,nms_threshold,fd_kmodel_input_shape[2],prior_data,
                [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH],results)
    # （6）返回人脸检测框
    if len(post_ret)==0:
        return post_ret
    else:
        return post_ret[0]          #0:det,1:landm,2:score

def fd_kpu_deinit():
    # kpu释放
    with ScopedTiming("fd_kpu_deinit",debug_mode > 0):
        if 'fd_ai2d' in globals():     #删除人脸检测ai2d变量，释放对它所引用对象的内存引用
            global fd_ai2d
            del fd_ai2d
        if 'fd_ai2d_output_tensor' in globals():#删除人脸检测ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global fd_ai2d_output_tensor
            del fd_ai2d_output_tensor


###############for face recognition###############
def get_affine_matrix(bbox):
    # 获取仿射矩阵，用于将边界框映射到模型输入空间
    with ScopedTiming("get_affine_matrix", debug_mode > 1):
        # 设置缩放因子
        factor = 2.7
        # 从边界框提取坐标和尺寸
        x1, y1, w, h = map(lambda x: int(round(x, 0)), bbox[:4])
        # 模型输入大小
        edge_size = fp_kmodel_input_shape[2]
        # 平移距离，使得模型输入空间的中心对准原点
        trans_distance = edge_size / 2.0
        # 计算边界框中心点的坐标
        center_x = x1 + w / 2.0
        center_y = y1 + h / 2.0
        # 计算最大边长
        maximum_edge = factor * (h if h > w else w)
        # 计算缩放比例
        scale = edge_size * 2.0 / maximum_edge
        # 计算平移参数
        cx = trans_distance - scale * center_x
        cy = trans_distance - scale * center_y
        # 创建仿射矩阵
        affine_matrix = [scale, 0, cx, 0, scale, cy]
        return affine_matrix

def build_projection_matrix(det):
    x1, y1, w, h = map(lambda x: int(round(x, 0)), det[:4])

    # 计算边界框中心坐标
    center_x = x1 + w / 2.0
    center_y = y1 + h / 2.0

    # 定义后部（rear）和前部（front）的尺寸和深度
    rear_width = 0.5 * w
    rear_height = 0.5 * h
    rear_depth = 0
    factor = np.sqrt(2.0)
    front_width = factor * rear_width
    front_height = factor * rear_height
    front_depth = factor * rear_width  # 使用宽度来计算深度，也可以使用高度，取决于需求

    # 定义立方体的顶点坐标
    temp = [
        [-rear_width, -rear_height, rear_depth],
        [-rear_width, rear_height, rear_depth],
        [rear_width, rear_height, rear_depth],
        [rear_width, -rear_height, rear_depth],
        [-front_width, -front_height, front_depth],
        [-front_width, front_height, front_depth],
        [front_width, front_height, front_depth],
        [front_width, -front_height, front_depth]
    ]

    projections = np.array(temp)
    # 返回投影矩阵和中心坐标
    return projections, (center_x, center_y)

def rotation_matrix_to_euler_angles(R):
    # 将旋转矩阵（3x3 矩阵）转换为欧拉角（pitch、yaw、roll）
    # 计算 sin(yaw)
    sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)

    if sy < 1e-6:
        # 若 sin(yaw) 过小，说明 pitch 接近 ±90 度
        pitch = np.arctan2(-R[1, 2], R[1, 1]) * 180 / np.pi
        yaw = np.arctan2(-R[2, 0], sy) * 180 / np.pi
        roll = 0
    else:
        # 计算 pitch、yaw、roll 的角度
        pitch = np.arctan2(R[2, 1], R[2, 2]) * 180 / np.pi
        yaw = np.arctan2(-R[2, 0], sy) * 180 / np.pi
        roll = np.arctan2(R[1, 0], R[0, 0]) * 180 / np.pi
    return [pitch,yaw,roll]

def get_euler(data):
    # 获取旋转矩阵和欧拉角
    R = data[:3, :3].copy()
    eular = rotation_matrix_to_euler_angles(R)
    return R,eular

def fp_ai2d_init():
    # 人脸姿态估计ai2d初始化
    with ScopedTiming("fp_ai2d_init",debug_mode > 0):
        # （1）创建人脸姿态估计ai2d对象
        global fp_ai2d
        fp_ai2d = nn.ai2d()

        # （2）创建人脸姿态估计ai2d_output_tensor对象
        global fp_ai2d_output_tensor
        data = np.ones(fp_kmodel_input_shape, dtype=np.uint8)
        fp_ai2d_output_tensor = nn.from_numpy(data)

def fp_ai2d_run(rgb888p_img,det):
    # 人脸姿态估计ai2d推理
    with ScopedTiming("fp_ai2d_run",debug_mode > 0):
        global fp_ai2d,fp_ai2d_input_tensor,fp_ai2d_output_tensor
        #（1）根据原图构建人脸姿态估计ai2d_input_tensor
        ai2d_input = rgb888p_img.to_numpy_ref()
        fp_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        #（2）设置人脸姿态估计ai2d参数
        fp_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        global matrix_dst
        matrix_dst = get_affine_matrix(det)
        fp_ai2d.set_affine_param(True,nn.interp_method.cv2_bilinear,0, 0, 127, 1,matrix_dst)
        # （3）构建人脸姿态估计ai2d_builder
        global fp_ai2d_builder
        fp_ai2d_builder = fp_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fp_kmodel_input_shape)
        # （4）推理人脸姿态估计ai2d，将结果保存到ai2d_output_tensor
        fp_ai2d_builder.run(fp_ai2d_input_tensor, fp_ai2d_output_tensor)

def fp_ai2d_release():
    # 释放部分人脸姿态估计ai2d资源
    with ScopedTiming("fp_ai2d_release",debug_mode > 0):
        global fp_ai2d_input_tensor,fp_ai2d_builder
        del fp_ai2d_input_tensor
        del fp_ai2d_builder

def fp_kpu_init(kmodel_file):
    # 初始化人脸姿态估计kpu及ai2d
    with ScopedTiming("fp_kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)
        fp_ai2d_init()
        return kpu_obj

def fp_kpu_pre_process(rgb888p_img,det):
    # 人脸姿态估计kpu预处理
    fp_ai2d_run(rgb888p_img,det)
    with ScopedTiming("fp_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fp_ai2d_output_tensor
        current_kmodel_obj.set_input_tensor(0, fp_ai2d_output_tensor)
        #ai2d_out_data = _ai2d_output_tensor.to_numpy()
        #with open("/sdcard/app/ai2d_out.bin", "wb") as file:
            #file.write(ai2d_out_data.tobytes())

def fp_kpu_get_output():
    # 获取人脸姿态估计kpu输出
    with ScopedTiming("fp_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        result = result[0]
        del data
        return result

def fp_kpu_post_process(pred):
    # 人脸姿态估计kpu推理结果后处理
    R,eular = get_euler(pred)
    return R,eular

def fp_kpu_run(kpu_obj,rgb888p_img,det):
    # 人脸姿态估计kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）根据人脸检测框进行人脸姿态估计kpu预处理
    fp_kpu_pre_process(rgb888p_img,det)
    # （2）人脸姿态估计kpu推理
    with ScopedTiming("fp_kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸姿态估计ai2d资源
    fp_ai2d_release()
    # （4）释放人脸姿态估计kpu推理输出
    result = fp_kpu_get_output()
    # （5）释放人脸姿态估计后处理
    R,eular = fp_kpu_post_process(result)
    return R,eular

def fp_kpu_deinit():
    # 释放人脸姿态估计kpu及ai2d资源
    with ScopedTiming("fp_kpu_deinit",debug_mode > 0):
        if 'fp_ai2d' in globals():
            global fp_ai2d
            del fp_ai2d
        if 'fp_ai2d_output_tensor' in globals():
            global fp_ai2d_output_tensor
            del fp_ai2d_output_tensor

#********************for media_utils.py********************
global draw_img_ulab,draw_img,osd_img                                     #for display
global buffer,media_source,media_sink                       #for media

# for display，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.2
def display_init():
    # 设置使用hdmi进行显示
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

def display_deinit():
    # 释放显示资源
    display.deinit()

def display_draw(dets,pose_results):
    # 在显示器画人脸轮廓
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img_ulab,draw_img,osd_img
        if dets:
            draw_img.clear()
            line_color = np.array([255, 0, 0 ,255],dtype = np.uint8)    #bgra
            for i,det in enumerate(dets):
                # （1）获取人脸姿态矩阵和欧拉角
                projections,center_point = build_projection_matrix(det)
                R,euler = pose_results[i]

                # （2）遍历人脸投影矩阵的关键点，进行投影，并将结果画在图像上
                first_points = []
                second_points = []
                for pp in range(8):
                    sum_x, sum_y = 0.0, 0.0
                    for cc in range(3):
                        sum_x += projections[pp][cc] * R[cc][0]
                        sum_y += projections[pp][cc] * (-R[cc][1])

                    center_x,center_y = center_point[0],center_point[1]
                    x = (sum_x + center_x) / OUT_RGB888P_WIDTH * DISPLAY_WIDTH
                    y = (sum_y + center_y) / OUT_RGB888P_HEIGH * DISPLAY_HEIGHT
                    x = max(0, min(x, DISPLAY_WIDTH))
                    y = max(0, min(y, DISPLAY_HEIGHT))

                    if pp < 4:
                        first_points.append((x, y))
                    else:
                        second_points.append((x, y))
                first_points = np.array(first_points,dtype=np.float)
                aidemo.polylines(draw_img_ulab,first_points,True,line_color,2,8,0)
                second_points = np.array(second_points,dtype=np.float)
                aidemo.polylines(draw_img_ulab,second_points,True,line_color,2,8,0)

                for ll in range(4):
                    x0, y0 = int(first_points[ll][0]),int(first_points[ll][1])
                    x1, y1 = int(second_points[ll][0]),int(second_points[ll][1])
                    draw_img.draw_line(x0, y0, x1, y1, color = (255, 0, 0 ,255), thickness = 2)

            # （3）将绘制好的图像拷贝到显示缓冲区，并在显示器上展示
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            # （1）清空用来画框的图像
            draw_img.clear()
            # （2）清空osd
            draw_img.copy_to(osd_img)
            # （3）显示透明图层
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.1
def camera_init(dev_id):
    # camera初始化
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

def camera_start(dev_id):
    # camera启动
    camera.start_stream(dev_id)

def camera_read(dev_id):
    # 读取一帧图像
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

def camera_release_image(dev_id,rgb888p_img):
    # 释放一帧图像
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

def camera_stop(dev_id):
    # 停止camera
    camera.stop_stream(dev_id)

#for media，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.3
def media_init():
    # meida初始化
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img_ulab,draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 用于画框，draw_img->draw_img_ulab(两者指向同一块内存)
    draw_img_ulab = np.zeros((DISPLAY_HEIGHT,DISPLAY_WIDTH,4),dtype=np.uint8)
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, alloc=image.ALLOC_REF,data = draw_img_ulab)
    # 用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

def media_deinit():
    # meida资源释放
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#********************for face_detect.py********************
def face_pose_inference():
    print("face_pose_test start")
    # 人脸检测kpu初始化
    kpu_face_detect = fd_kpu_init(fd_kmodel_file)
    # 人脸姿态估计kpu初始化
    kpu_face_pose = fp_kpu_init(fp_kmodel_file)
    # camera初始化
    camera_init(CAM_DEV_ID_0)
    # 显示初始化
    display_init()

    rgb888p_img = None
    # 注意：将一定要将一下过程包在try中，用于保证程序停止后，资源释放完毕；确保下次程序仍能正常运行
    try:
        # 注意：媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）
        media_init()

        # 启动camera
        camera_start(CAM_DEV_ID_0)
        gc_count = 0
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                # （1）读取一帧图像
                rgb888p_img = camera_read(CAM_DEV_ID_0)

                # （2）若读取成功，推理当前帧
                if rgb888p_img.format() == image.RGBP888:
                    # （2.1）推理当前图像，并获取人脸检测结果
                    dets = fd_kpu_run(kpu_face_detect,rgb888p_img)
                    # （2.2）针对每个人脸框，推理得到对应人脸旋转矩阵、欧拉角
                    pose_results = []
                    for det in dets:
                        R,eular = fp_kpu_run(kpu_face_pose,rgb888p_img,det)
                        pose_results.append((R,eular))
                    # （2.3）将人脸姿态估计结果画到显示器上
                    display_draw(dets,pose_results)

                # （3）释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)
                if gc_count > 5:
                    gc.collect()
                    gc_count = 0
                else:
                    gc_count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        # 停止camera
        camera_stop(CAM_DEV_ID_0)
        # 释放显示资源
        display_deinit()
        # 释放kpu资源
        fd_kpu_deinit()
        fp_kpu_deinit()
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_face_detect
        del kpu_face_pose
        if 'draw_img' in globals():
            global draw_img
            del draw_img
        if 'draw_img_ulab' in globals():
            global draw_img_ulab
            del draw_img_ulab
        # 垃圾回收
        gc.collect()
        nn.shrink_memory_pool()
        # 释放媒体资源
        media_deinit()

    print("face_pose_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    face_pose_inference()
```

### 4. 人脸解析

```python
import ulab.numpy as np                  # 类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn              # nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *               # 摄像头模块
from media.display import *              # 显示模块
from media.media import *                # 软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import aidemo                            # aidemo模块，封装ai demo相关后处理、画图操作
import image                             # 图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                              # 时间统计
import gc                                # 垃圾回收模块
import os,sys                            # 操作系统接口模块
import math                              # 数学模块

#********************for config.py********************
# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)                   # 显示宽度要求16位对齐
DISPLAY_HEIGHT = 1080

# ai原图分辨率，sensor默认出图为16:9，若需不形变原图，最好按照16:9比例设置宽高
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)               # ai原图宽度要求16位对齐
OUT_RGB888P_HEIGH = 1080

# kmodel参数设置
# 人脸检测kmodel输入shape
fd_kmodel_input_shape = (1,3,320,320)
# 人脸解析kmodel输入shape
fp_kmodel_input_shape = (1,3,320,320)
# ai原图padding
rgb_mean = [104,117,123]

#人脸检测kmodel其它参数设置
confidence_threshold = 0.5                      # 人脸检测阈值
top_k = 5000
nms_threshold = 0.2
keep_top_k = 750
vis_thres = 0.5
variance = [0.1, 0.2]
anchor_len = 4200
score_dim = 2
det_dim = 4
keypoint_dim = 10

# 文件配置
# 人脸检测kmodel
root_dir = '/sdcard/app/tests/'
fd_kmodel_file = root_dir + 'kmodel/face_detection_320.kmodel'
# 人脸解析kmodel
fp_kmodel_file = root_dir + 'kmodel/face_parse.kmodel'
# anchor文件
anchors_path = root_dir + 'utils/prior_data_320.bin'
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0

#********************for scoped_timing.py********************
# 时间统计类
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#********************for ai_utils.py********************
global current_kmodel_obj #当前kpu对象
# fd_ai2d：               人脸检测ai2d实例
# fd_ai2d_input_tensor：  人脸检测ai2d输入
# fd_ai2d_output_tensor： 人脸检测ai2d输入
# fd_ai2d_builder：       根据人脸检测ai2d参数，构建的人脸检测ai2d_builder对象
global fd_ai2d,fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
# fld_ai2d：              人脸解析ai2d实例
# fld_ai2d_input_tensor： 人脸解析ai2d输入
# fld_ai2d_output_tensor：人脸解析ai2d输入
# fld_ai2d_builder：      根据人脸解析ai2d参数，构建的人脸解析ai2d_builder对象
global fp_ai2d,fp_ai2d_input_tensor,fp_ai2d_output_tensor,fp_ai2d_builder
global matrix_dst         #人脸仿射变换矩阵

#读取anchor文件，为人脸检测后处理做准备
print('anchors_path:',anchors_path)
prior_data = np.fromfile(anchors_path, dtype=np.float)
prior_data = prior_data.reshape((anchor_len,det_dim))

def get_pad_one_side_param():
    # 右padding或下padding，获取padding参数
    dst_w = fd_kmodel_input_shape[3]                         # kmodel输入宽（w）
    dst_h = fd_kmodel_input_shape[2]                          # kmodel输入高（h）

    # OUT_RGB888P_WIDTH：原图宽（w）
    # OUT_RGB888P_HEIGH：原图高（h）
    # 计算最小的缩放比例，等比例缩放
    ratio_w = dst_w / OUT_RGB888P_WIDTH
    ratio_h = dst_h / OUT_RGB888P_HEIGH
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h
    # 计算经过缩放后的新宽和新高
    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGH)

    # 计算需要添加的padding，以使得kmodel输入的宽高和原图一致
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2
    # 四舍五入，确保padding是整数
    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

def fd_ai2d_init():
    # 人脸检测模型ai2d初始化
    with ScopedTiming("fd_ai2d_init",debug_mode > 0):
        # （1）创建人脸检测ai2d对象
        global fd_ai2d
        fd_ai2d = nn.ai2d()
        # （2）设置人脸检测ai2d参数
        fd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        fd_ai2d.set_pad_param(True, get_pad_one_side_param(), 0, rgb_mean)
        fd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        #（3）人脸检测ai2d_builder，根据人脸检测ai2d参数、输入输出大小创建ai2d_builder对象
        global fd_ai2d_builder
        fd_ai2d_builder = fd_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fd_kmodel_input_shape)

        #（4）创建人脸检测ai2d_output_tensor，用于保存人脸检测ai2d输出
        global fd_ai2d_output_tensor
        data = np.ones(fd_kmodel_input_shape, dtype=np.uint8)
        fd_ai2d_output_tensor = nn.from_numpy(data)

def fd_ai2d_run(rgb888p_img):
    # 根据人脸检测ai2d参数，对原图rgb888p_img进行预处理
    with ScopedTiming("fd_ai2d_run",debug_mode > 0):
        global fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
        # （1）根据原图构建ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        fd_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        # （2）运行人脸检测ai2d_builder，将结果保存到人脸检测ai2d_output_tensor中
        fd_ai2d_builder.run(fd_ai2d_input_tensor, fd_ai2d_output_tensor)

def fd_ai2d_release():
    # 释放人脸检测ai2d_input_tensor
    with ScopedTiming("fd_ai2d_release",debug_mode > 0):
        global fd_ai2d_input_tensor
        del fd_ai2d_input_tensor


def fd_kpu_init(kmodel_file):
    # 初始化人脸检测kpu对象，并加载kmodel
    with ScopedTiming("fd_kpu_init",debug_mode > 0):
        # 初始化人脸检测kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸检测kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸检测ai2d
        fd_ai2d_init()
        return kpu_obj

def fd_kpu_pre_process(rgb888p_img):
    # 设置人脸检测kpu输入
    # 使用人脸检测ai2d对原图进行预处理（padding，resize）
    fd_ai2d_run(rgb888p_img)
    with ScopedTiming("fd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fd_ai2d_output_tensor
        # 设置人脸检测kpu输入
        current_kmodel_obj.set_input_tensor(0, fd_ai2d_output_tensor)

def fd_kpu_get_output():
    # 获取人脸检测kpu输出
    with ScopedTiming("fd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取模型输出，并将结果转换为numpy，以便进行人脸检测后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

def fd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）原图预处理，并设置模型输入
    fd_kpu_pre_process(rgb888p_img)
    # （2）人脸检测kpu推理
    with ScopedTiming("fd kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸检测ai2d资源
    fd_ai2d_release()
    # （4）获取人俩检测kpu输出
    results = fd_kpu_get_output()
    # （5）人脸检测kpu结果后处理
    with ScopedTiming("fd kpu_post",debug_mode > 0):
        post_ret = aidemo.face_det_post_process(confidence_threshold,nms_threshold,fd_kmodel_input_shape[2],prior_data,
                [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH],results)
    # （6）返回人脸检测框
    if len(post_ret)==0:
        return post_ret
    else:
        return post_ret[0]          #0:det,1:landm,2:score

def fd_kpu_deinit():
    # kpu释放
    with ScopedTiming("fd_kpu_deinit",debug_mode > 0):
        if 'fd_ai2d' in globals():     #删除人脸检测ai2d变量，释放对它所引用对象的内存引用
            global fd_ai2d
            del fd_ai2d
        if 'fd_ai2d_output_tensor' in globals():#删除人脸检测ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global fd_ai2d_output_tensor
            del fd_ai2d_output_tensor

###############for face recognition###############
def get_affine_matrix(bbox):
    # 获取仿射矩阵，用于将边界框映射到模型输入空间
    with ScopedTiming("get_affine_matrix", debug_mode > 1):
        # 设置缩放因子
        factor = 2.7
        # 从边界框提取坐标和尺寸
        x1, y1, w, h = map(lambda x: int(round(x, 0)), bbox[:4])
        # 模型输入大小
        edge_size = fp_kmodel_input_shape[2]
        # 平移距离，使得模型输入空间的中心对准原点
        trans_distance = edge_size / 2.0
        # 计算边界框中心点的坐标
        center_x = x1 + w / 2.0
        center_y = y1 + h / 2.0
        # 计算最大边长
        maximum_edge = factor * (h if h > w else w)
        # 计算缩放比例
        scale = edge_size * 2.0 / maximum_edge
        # 计算平移参数
        cx = trans_distance - scale * center_x
        cy = trans_distance - scale * center_y
        # 创建仿射矩阵
        affine_matrix = [scale, 0, cx, 0, scale, cy]
        return affine_matrix

def fp_ai2d_init():
    # 人脸解析ai2d初始化
    with ScopedTiming("fp_ai2d_init",debug_mode > 0):
        # （1）创建人脸解析ai2d对象
        global fp_ai2d
        fp_ai2d = nn.ai2d()

        # （2）创建人脸解析ai2d_output_tensor对象
        global fp_ai2d_output_tensor
        data = np.ones(fp_kmodel_input_shape, dtype=np.uint8)
        fp_ai2d_output_tensor = nn.from_numpy(data)

def fp_ai2d_run(rgb888p_img,det):
    # 人脸解析ai2d推理
    with ScopedTiming("fp_ai2d_run",debug_mode > 0):
        global fp_ai2d,fp_ai2d_input_tensor,fp_ai2d_output_tensor
        #（1）根据原图构建人脸解析ai2d_input_tensor
        ai2d_input = rgb888p_img.to_numpy_ref()
        fp_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        #（2）设置人脸解析ai2d参数
        fp_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        global matrix_dst
        matrix_dst = get_affine_matrix(det)
        fp_ai2d.set_affine_param(True,nn.interp_method.cv2_bilinear,0, 0, 127, 1,matrix_dst)

        # （3）构建人脸解析ai2d_builder
        global fp_ai2d_builder
        fp_ai2d_builder = fp_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fp_kmodel_input_shape)
        # （4）推理人脸解析ai2d，将结果保存到ai2d_output_tensor
        fp_ai2d_builder.run(fp_ai2d_input_tensor, fp_ai2d_output_tensor)

def fp_ai2d_release():
    # 释放部分人脸解析ai2d资源
    with ScopedTiming("fp_ai2d_release",debug_mode > 0):
        global fp_ai2d_input_tensor,fp_ai2d_builder
        del fp_ai2d_input_tensor
        del fp_ai2d_builder

def fp_kpu_init(kmodel_file):
    # 初始化人脸解析kpu及ai2d
    with ScopedTiming("fp_kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)
        fp_ai2d_init()
        return kpu_obj

def fp_kpu_pre_process(rgb888p_img,det):
    # 人脸解析kpu预处理
    fp_ai2d_run(rgb888p_img,det)
    with ScopedTiming("fp_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fp_ai2d_output_tensor
        current_kmodel_obj.set_input_tensor(0, fp_ai2d_output_tensor)
        #ai2d_out_data = fp_ai2d_output_tensor.to_numpy()
        #with open("/sdcard/app/ai2d_out.bin", "wb") as file:
            #file.write(ai2d_out_data.tobytes())

def fp_kpu_get_output():
    # 获取人脸解析kpu输出
    with ScopedTiming("fp_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        del data
        return result

def fp_kpu_run(kpu_obj,rgb888p_img,det):
    # 人脸解析kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）根据人脸检测框进行人脸解析kpu预处理
    fp_kpu_pre_process(rgb888p_img,det)
    # （2）人脸解析kpu推理
    with ScopedTiming("fp_kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸解析ai2d资源
    fp_ai2d_release()
    # （4）释放人脸解析kpu输出
    result = fp_kpu_get_output()
    return result

def fp_kpu_deinit():
    # 释放人脸解析kpu和ai2d资源
    with ScopedTiming("fp_kpu_deinit",debug_mode > 0):
        if 'fp_ai2d' in globals():
            global fp_ai2d
            del fp_ai2d
        if 'fp_ai2d_output_tensor' in globals():
            global fp_ai2d_output_tensor
            del fp_ai2d_output_tensor

#********************for media_utils.py********************
global draw_img_ulab,draw_img,osd_img                                     #for display
global buffer,media_source,media_sink                       #for media

#for display
def display_init():
    # 设置使用hdmi进行显示
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

def display_deinit():
    # 释放显示资源
    display.deinit()

def display_draw(dets,parse_results):
    # 在显示器画出人脸解析结果
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img_ulab,draw_img,osd_img
        if dets:
            draw_img.clear()
            for i,det in enumerate(dets):
                # （1）将人脸检测框画到draw_img
                x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                x = x * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                y = y * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                w = w * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                h = h * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
                draw_img.draw_rectangle(x,y, w, h, color=(255, 255, 0, 255))
                # （2）将人脸解析结果画到draw_img（draw_img_ulab和draw_img指同一内存）
                aidemo.face_parse_post_process(draw_img_ulab,[OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH],
                    [DISPLAY_WIDTH,DISPLAY_HEIGHT],fp_kmodel_input_shape[2],det.tolist(),parse_results[i])
            # （3）将绘制好的图像拷贝到显示缓冲区，并在显示器上展示
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            # （1）清空用来画框的图像
            draw_img.clear()
            # （2）清空osd
            draw_img.copy_to(osd_img)
            # （3）显示透明图层
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.1
def camera_init(dev_id):
    # camera初始化
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

def camera_start(dev_id):
    # camera启动
    camera.start_stream(dev_id)

def camera_read(dev_id):
    # 读取一帧图像
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

def camera_release_image(dev_id,rgb888p_img):
    # 释放一帧图像
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

def camera_stop(dev_id):
    # 停止camera
    camera.stop_stream(dev_id)

#for media，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.3
def media_init():
    # meida初始化
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    ret = media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img_ulab,draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 用于画框，draw_img->draw_img_ulab(两者指向同一块内存)
    draw_img_ulab = np.zeros((DISPLAY_HEIGHT,DISPLAY_WIDTH,4),dtype=np.uint8)
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, alloc=image.ALLOC_REF,data = draw_img_ulab)
    # 用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

def media_deinit():
    # meida资源释放
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#********************for face_detect.py********************
def face_parse_inference():
    print("face_parse_test start")
    # 人脸检测kpu初始化
    kpu_face_detect = fd_kpu_init(fd_kmodel_file)
    # 人脸解析kpu初始化
    kpu_face_parse = fp_kpu_init(fp_kmodel_file)
    # camera初始化
    camera_init(CAM_DEV_ID_0)
    # 显示初始化
    display_init()

    # 注意：将一定要将一下过程包在try中，用于保证程序停止后，资源释放完毕；确保下次程序仍能正常运行
    try:
        # 注意：媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）
        media_init()
        # 启动camera
        camera_start(CAM_DEV_ID_0)
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                # （1）读取一帧图像
                rgb888p_img = camera_read(CAM_DEV_ID_0)

                # （2）若读取成功，推理当前帧
                if rgb888p_img.format() == image.RGBP888:
                    # （2.1）推理当前图像，并获取人脸检测结果
                    dets = fd_kpu_run(kpu_face_detect,rgb888p_img)
                    # （2.2）针对每个人脸框，推理得到对应人脸解析结果
                    parse_results = []
                    for det in dets:
                        parse_ret = fp_kpu_run(kpu_face_parse,rgb888p_img,det)
                        parse_results.append(parse_ret)
                    # （2.3）将人脸解析结果画到显示器上
                    display_draw(dets,parse_results)

                # （3）释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)
                gc.collect()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        # 停止camera
        camera_stop(CAM_DEV_ID_0)
        # 释放显示资源
        display_deinit()
        # 释放kpu资源
        fd_kpu_deinit()
        fp_kpu_deinit()
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_face_detect
        del kpu_face_parse
        if 'draw_img' in globals():
            global draw_img
            del draw_img
        if 'draw_img_ulab' in globals():
            global draw_img_ulab
            del draw_img_ulab
        # 垃圾回收
        gc.collect()
        nn.shrink_memory_pool()
        # 释放媒体资源
        media_deinit()

    print("face_parse_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    face_parse_inference()
```

### 5. 车牌识别

```python
import ulab.numpy as np             #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn         #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *          #摄像头模块
from media.display import *         #显示模块
from media.media import *           #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import image                        #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                         #时间统计
import gc                           #垃圾回收模块
import aidemo                       #aidemo模块，封装ai demo相关后处理、画图操作
import os, sys                           #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

#ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(640, 16)
OUT_RGB888P_HEIGHT = 360

#车牌检测 和 车牌识别 kmodel输入shape
det_kmodel_input_shape = (1,3,640,640)
rec_kmodel_input_shape = (1,1,32,220)

#车牌检测 相关参数设置
obj_thresh = 0.2            #车牌检测分数阈值
nms_thresh = 0.2            #检测框 非极大值抑制 阈值

#文件配置
root_dir = '/sdcard/app/tests/'
det_kmodel_file = root_dir + 'kmodel/LPD_640.kmodel'                               # 车牌检测 kmodel 文件路径
rec_kmodel_file = root_dir + 'kmodel/licence_reco.kmodel'                          # 车牌识别 kmodel 文件路径
#dict_rec = ["挂", "使", "领", "澳", "港", "皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "_", "-"]
dict_rec = ["gua","shi","ling","ao","gang","wan","hu","jin","yu","ji","jin","meng","liao","ji","hei","su","zhe","jing","min","gan","lu","yu","e","xiang","yue","gui","qiong","chuan","gui","yun","zang","shan","gan","qing","ning","xin","jing","xue","0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "_", "-"]
dict_size = len(dict_rec)
debug_mode = 0                                                                      # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")


#ai_utils.py
global current_kmodel_obj                                                           # 定义全局的 kpu 对象
global det_ai2d,det_ai2d_input_tensor,det_ai2d_output_tensor,det_ai2d_builder       # 定义车牌检测 ai2d 对象 ，并且定义 ai2d 的输入、输出 以及 builder
global rec_ai2d,rec_ai2d_input_tensor,rec_ai2d_output_tensor,rec_ai2d_builder       # 定义车牌识别 ai2d 对象 ，并且定义 ai2d 的输入、输出 以及 builder

# 车牌检测 接收kmodel输出的后处理方法
def det_kpu_post_process(output_data):
    with ScopedTiming("det_kpu_post_process", debug_mode > 0):
        results = aidemo.licence_det_postprocess(output_data,[OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH],[det_kmodel_input_shape[2],det_kmodel_input_shape[3]],obj_thresh,nms_thresh)
        return results

# 车牌识别 接收kmodel输出的后处理方法
def rec_kpu_post_process(output_data):
    with ScopedTiming("rec_kpu_post_process", debug_mode > 0):
        size = rec_kmodel_input_shape[3] / 4
        result = []
        for i in range(size):
            maxs = float("-inf")
            index = -1
            for j in range(dict_size):
                if (maxs < float(output_data[i * dict_size +j])):
                    index = j
                    maxs = output_data[i * dict_size +j]
            result.append(index)

        result_str = ""
        for i in range(size):
            if (result[i] >= 0 and result[i] != 0 and not(i > 0 and result[i-1] == result[i])):
                result_str += dict_rec[result[i]-1]
        return result_str

# 车牌检测 ai2d 初始化
def det_ai2d_init():
    with ScopedTiming("det_ai2d_init",debug_mode > 0):
        global det_ai2d
        det_ai2d = nn.ai2d()
        det_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        det_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        global det_ai2d_out_tensor
        data = np.ones(det_kmodel_input_shape, dtype=np.uint8)
        det_ai2d_out_tensor = nn.from_numpy(data)

        global det_ai2d_builder
        det_ai2d_builder = det_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], det_kmodel_input_shape)

# 车牌识别 ai2d 初始化
def rec_ai2d_init():
    with ScopedTiming("rec_ai2d_init",debug_mode > 0):
        global rec_ai2d
        rec_ai2d = nn.ai2d()
        rec_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)

        global rec_ai2d_out_tensor
        data = np.ones(rec_kmodel_input_shape, dtype=np.uint8)
        rec_ai2d_out_tensor = nn.from_numpy(data)

        rec_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

# 车牌检测 ai2d 运行
def det_ai2d_run(rgb888p_img):
    with ScopedTiming("det_ai2d_run",debug_mode > 0):
        global det_ai2d_input_tensor,det_ai2d_out_tensor,det_ai2d_builder
        det_ai2d_input = rgb888p_img.to_numpy_ref()
        det_ai2d_input_tensor = nn.from_numpy(det_ai2d_input)

        det_ai2d_builder.run(det_ai2d_input_tensor, det_ai2d_out_tensor)

# 车牌识别 ai2d 运行
def rec_ai2d_run(img_array):
    with ScopedTiming("rec_ai2d_run",debug_mode > 0):
        global rec_ai2d_input_tensor,rec_ai2d_out_tensor,rec_ai2d_builder
        rec_ai2d_builder = rec_ai2d.build([1,1,img_array.shape[2],img_array.shape[3]], rec_kmodel_input_shape)
        rec_ai2d_input_tensor = nn.from_numpy(img_array)

        rec_ai2d_builder.run(rec_ai2d_input_tensor, rec_ai2d_out_tensor)

# 车牌检测 ai2d 释放内存
def det_ai2d_release():
    with ScopedTiming("det_ai2d_release",debug_mode > 0):
        global det_ai2d_input_tensor
        del det_ai2d_input_tensor

# 车牌识别 ai2d 释放内存
def rec_ai2d_release():
    with ScopedTiming("rec_ai2d_release",debug_mode > 0):
        global rec_ai2d_input_tensor, rec_ai2d_builder
        del rec_ai2d_input_tensor
        del rec_ai2d_builder

# 车牌检测 kpu 初始化
def det_kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("det_kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        det_ai2d_init()
        return kpu_obj

# 车牌识别 kpu 初始化
def rec_kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("rec_kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        rec_ai2d_init()
        return kpu_obj

# 车牌检测 kpu 输入预处理
def det_kpu_pre_process(rgb888p_img):
    det_ai2d_run(rgb888p_img)
    with ScopedTiming("det_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,det_ai2d_out_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, det_ai2d_out_tensor)

# 车牌识别 kpu 输入预处理
def rec_kpu_pre_process(img_array):
    rec_ai2d_run(img_array)
    with ScopedTiming("rec_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,rec_ai2d_out_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, rec_ai2d_out_tensor)

# 车牌识别 抠图
def rec_array_pre_process(rgb888p_img,dets):
    with ScopedTiming("rec_array_pre_process",debug_mode > 0):
        isp_image = rgb888p_img.to_numpy_ref()
        imgs_array_boxes = aidemo.ocr_rec_preprocess(isp_image,[OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH],dets)
    return imgs_array_boxes

# 车牌检测 获取 kmodel 输出
def det_kpu_get_output():
    with ScopedTiming("det_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            tmp2 = result.copy()
            del data
            results.append(tmp2)
        return results

# 车牌识别 获取 kmodel 输出
def rec_kpu_get_output():
    with ScopedTiming("rec_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        result = result.reshape((result.shape[0] * result.shape[1] * result.shape[2]))
        tmp = result.copy()
        del data
        return tmp

# 车牌检测 kpu 运行
def det_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1) 原图预处理，并设置模型输入
    det_kpu_pre_process(rgb888p_img)
    # (2) kpu 运行
    with ScopedTiming("det_kpu_run",debug_mode > 0):
        kpu_obj.run()
     # (3) 释放ai2d资源
    det_ai2d_release()
    # (4) 获取kpu输出
    results = det_kpu_get_output()
    # (5) kpu结果后处理
    dets = det_kpu_post_process(results)
    # 返回 车牌检测结果
    return dets

# 车牌识别 kpu 运行
def rec_kpu_run(kpu_obj,rgb888p_img,dets):
    global current_kmodel_obj
    if (len(dets) == 0):
        return []
    current_kmodel_obj = kpu_obj
    # (1) 原始图像抠图，车牌检测结果 points 排序
    imgs_array_boxes = rec_array_pre_process(rgb888p_img,dets)
    imgs_array = imgs_array_boxes[0]
    boxes = imgs_array_boxes[1]
    recs = []
    for img_array in imgs_array:
        # (2) 抠出后的图像 进行预处理，设置模型输入
        rec_kpu_pre_process(img_array)
        # (3) kpu 运行
        with ScopedTiming("rec_kpu_run",debug_mode > 0):
            kpu_obj.run()
        # (4) 释放ai2d资源
        rec_ai2d_release()
        # (5) 获取 kpu 输出
        result = rec_kpu_get_output()
        # (6) kpu 结果后处理
        rec = rec_kpu_post_process(result)
        recs.append(rec)
    # (7) 返回 车牌检测 和 识别结果
    return [boxes,recs]


# 车牌检测 kpu 释放内存
def det_kpu_deinit():
    with ScopedTiming("det_kpu_deinit",debug_mode > 0):
        if 'det_ai2d' in globals():
            global det_ai2d
            del det_ai2d
        if 'det_ai2d_builder' in globals():
            global det_ai2d_builder
            del det_ai2d_builder
        if 'det_ai2d_out_tensor' in globals():
            global det_ai2d_out_tensor
            del det_ai2d_out_tensor

# 车牌识别 kpu 释放内存
def rec_kpu_deinit():
    with ScopedTiming("rec_kpu_deinit",debug_mode > 0):
        if 'rec_ai2d' in globals():
            global rec_ai2d
            del rec_ai2d
        if 'rec_ai2d_out_tensor' in globals():
            global rec_ai2d_out_tensor
            del rec_ai2d_out_tensor


#media_utils.py
global draw_img,osd_img                                     #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 将所有车牌检测框 和 识别结果绘制到屏幕
def display_draw(dets_recs):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if dets_recs:
            dets = dets_recs[0]
            recs = dets_recs[1]
            draw_img.clear()
            point_8 = np.zeros((8),dtype=np.int16)
            for det_index in range(len(dets)):
                for i in range(4):
                    x = dets[det_index][i * 2 + 0]/OUT_RGB888P_WIDTH*DISPLAY_WIDTH
                    y = dets[det_index][i * 2 + 1]/OUT_RGB888P_HEIGHT*DISPLAY_HEIGHT
                    point_8[i * 2 + 0] = int(x)
                    point_8[i * 2 + 1] = int(y)
                for i in range(4):
                    draw_img.draw_line(point_8[i * 2 + 0],point_8[i * 2 + 1],point_8[(i+1) % 4 * 2 + 0],point_8[(i+1) % 4 * 2 + 1],color=(255, 0, 255, 0),thickness=4)
                draw_img.draw_string( point_8[6], point_8[7] + 20, recs[det_index] , color=(255,255,153,18) , scale=4)
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_BGR_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()


#**********for licence_det_rec.py**********
def licence_det_rec_inference():
    print("licence_det_rec start")
    kpu_licence_det = det_kpu_init(det_kmodel_file)                     # 创建车牌检测的 kpu 对象
    kpu_licence_rec = rec_kpu_init(rec_kmodel_file)                     # 创建车牌识别的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)

        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    dets = det_kpu_run(kpu_licence_det,rgb888p_img)                 # 执行车牌检测 kpu 运行 以及 后处理过程
                    dets_recs = rec_kpu_run(kpu_licence_rec,rgb888p_img,dets)       # 执行车牌识别 kpu 运行 以及 后处理过程
                    display_draw(dets_recs)                                         # 将得到的检测结果和识别结果 绘制到display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)                      # camera 释放图像

                if (count > 5):
                    gc.collect()
                    count = 0
                else:
                    count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        camera_stop(CAM_DEV_ID_0)                                                   # 停止 camera
        display_deinit()                                                            # 释放 display
        det_kpu_deinit()                                                            # 释放 车牌检测 kpu
        rec_kpu_deinit()                                                            # 释放 车牌识别 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_licence_det
        del kpu_licence_rec
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                                        # 释放 整个media

    print("licence_det_rec end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    licence_det_rec_inference()
```

### 6. 石头剪刀布

```python
import ulab.numpy as np                 #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn             #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *              #摄像头模块
from media.display import *             #显示模块
from media.media import *               #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
from random import randint              #随机整数生成
import image                            #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                             #时间统计
import gc                               #垃圾回收模块
import aicube                           #aicube模块，封装ai cube 相关后处理
import os, sys                          #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

#ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

#手掌检测 和 手掌关键点检测 kmodel输入shape
hd_kmodel_input_shape = (1,3,512,512)
hk_kmodel_input_shape = (1,3,256,256)

#手掌检测 相关参数设置
confidence_threshold = 0.2                                  #手掌检测 分数阈值
nms_threshold = 0.5                                         #非极大值抑制 阈值
hd_kmodel_frame_size = [512,512]                            #手掌检测kmodel输入  w h
hd_frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGHT]       #手掌检测原始输入图像 w h
strides = [8,16,32]                                         #手掌检测模型 下采样输出倍数
num_classes = 1                                             #检测类别数， 及手掌一种
nms_option = False                                          #控制最大值抑制的方式 False 类内  True 类间
labels = ["hand"]                                           #标签名称
anchors = [26,27,53,52,75,71,80,99,106,82,99,134,140,113,161,172,245,276]   #手掌检测模型 锚框
#手掌关键点检测 相关参数
hk_kmodel_frame_size = [256,256]                            #手掌关键点检测 kmodel 输入 w h

# kmodel 路径
root_dir = '/sdcard/app/tests/'
hd_kmodel_file = root_dir + 'kmodel/hand_det.kmodel'          #手掌检测kmodel路径
hk_kmodel_file = root_dir + 'kmodel/handkp_det.kmodel'        #手掌关键点kmodel路径
debug_mode = 0                                                          # debug模式 大于0（调试）、 反之 （不调试）

# 猜拳模式  0 玩家稳赢 ， 1 玩家必输 ， n > 2 多局多胜
guess_mode = 3

# 读取石头剪刀布的bin文件方法
def read_file(file_name):
    image_arr = np.fromfile(file_name,dtype=np.uint8)
    image_arr = image_arr.reshape((400,400,4))
    return image_arr
# 石头剪刀布的 array
five_image = read_file(root_dir + "utils/five.bin")
fist_image = read_file(root_dir + "utils/fist.bin")
shear_image = read_file(root_dir + "utils/shear.bin")


#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                                       # 定义全局的 kpu 对象
global hd_ai2d,hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder       # 定义手掌检测 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor,hk_ai2d_builder       # 定义手掌关键点检测 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global counts_guess, player_win, k230_win, sleep_end, set_stop_id               # 定义猜拳游戏的参数：猜拳次数、玩家赢次、k230赢次、是否停顿、是狗暂停

# 手掌检测 ai2d 初始化
def hd_ai2d_init():
    with ScopedTiming("hd_ai2d_init",debug_mode > 0):
        global hd_ai2d
        global hd_ai2d_builder
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = hd_kmodel_frame_size[0]
        height = hd_kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        # init kpu and load kmodel
        hd_ai2d = nn.ai2d()
        hd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        hd_ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        hd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        hd_ai2d_builder = hd_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,height,width])

        global hd_ai2d_output_tensor
        data = np.ones(hd_kmodel_input_shape, dtype=np.uint8)
        hd_ai2d_output_tensor = nn.from_numpy(data)

# 手掌检测 ai2d 运行
def hd_ai2d_run(rgb888p_img):
    with ScopedTiming("hd_ai2d_run",debug_mode > 0):
        global hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder
        hd_ai2d_input = rgb888p_img.to_numpy_ref()
        hd_ai2d_input_tensor = nn.from_numpy(hd_ai2d_input)

        hd_ai2d_builder.run(hd_ai2d_input_tensor, hd_ai2d_output_tensor)

# 手掌检测 ai2d 释放内存
def hd_ai2d_release():
    with ScopedTiming("hd_ai2d_release",debug_mode > 0):
        global hd_ai2d_input_tensor
        del hd_ai2d_input_tensor

# 手掌检测 kpu 初始化
def hd_kpu_init(hd_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hd_kpu_init",debug_mode > 0):
        hd_kpu_obj = nn.kpu()
        hd_kpu_obj.load_kmodel(hd_kmodel_file)

        hd_ai2d_init()
        return hd_kpu_obj

# 手掌检测 kpu 输入预处理
def hd_kpu_pre_process(rgb888p_img):
    hd_ai2d_run(rgb888p_img)
    with ScopedTiming("hd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hd_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hd_ai2d_output_tensor)

# 手掌检测 kpu 获取 kmodel 输出
def hd_kpu_get_output():
    with ScopedTiming("hd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌检测 kpu 运行
def hd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1) 原始图像预处理，并设置模型输入
    hd_kpu_pre_process(rgb888p_img)
    # (2) kpu 运行
    with ScopedTiming("hd_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3) 释放ai2d资源
    hd_ai2d_release()
    # (4) 获取kpu输出
    results = hd_kpu_get_output()
    # (5) kpu结果后处理
    dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], hd_kmodel_frame_size, hd_frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)
    # (6) 返回 手掌检测 结果
    return dets

# 手掌检测 kpu 释放内存
def hd_kpu_deinit():
    with ScopedTiming("hd_kpu_deinit",debug_mode > 0):
        if 'hd_ai2d' in globals():
            global hd_ai2d
            del hd_ai2d
        if 'hd_ai2d_output_tensor' in globals():
            global hd_ai2d_output_tensor
            del hd_ai2d_output_tensor
        if 'hd_ai2d_builder' in globals():
            global hd_ai2d_builder
            del hd_ai2d_builder

# 手掌关键点检测 ai2d 初始化
def hk_ai2d_init():
    with ScopedTiming("hk_ai2d_init",debug_mode > 0):
        global hk_ai2d
        hk_ai2d = nn.ai2d()
        hk_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)

        global hk_ai2d_output_tensor
        data = np.ones(hk_kmodel_input_shape, dtype=np.uint8)
        hk_ai2d_output_tensor = nn.from_numpy(data)

# 手掌关键点检测 ai2d 运行
def hk_ai2d_run(rgb888p_img, x, y, w, h):
    with ScopedTiming("hk_ai2d_run",debug_mode > 0):
        global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor
        hk_ai2d_input = rgb888p_img.to_numpy_ref()
        hk_ai2d_input_tensor = nn.from_numpy(hk_ai2d_input)

        hk_ai2d.set_crop_param(True, x, y, w, h)
        hk_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )

        global hk_ai2d_builder
        hk_ai2d_builder = hk_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,hk_kmodel_frame_size[1],hk_kmodel_frame_size[0]])
        hk_ai2d_builder.run(hk_ai2d_input_tensor, hk_ai2d_output_tensor)

# 手掌关键点检测 ai2d 释放内存
def hk_ai2d_release():
    with ScopedTiming("hk_ai2d_release",debug_mode > 0):
        global hk_ai2d_input_tensor,hk_ai2d_builder
        del hk_ai2d_input_tensor
        del hk_ai2d_builder

# 手掌关键点检测 kpu 初始化
def hk_kpu_init(hk_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hk_kpu_init",debug_mode > 0):
        hk_kpu_obj = nn.kpu()
        hk_kpu_obj.load_kmodel(hk_kmodel_file)

        hk_ai2d_init()
        return hk_kpu_obj

# 手掌关键点检测 kpu 输入预处理
def hk_kpu_pre_process(rgb888p_img, x, y, w, h):
    hk_ai2d_run(rgb888p_img, x, y, w, h)
    with ScopedTiming("hk_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hk_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hk_ai2d_output_tensor)

# 手掌关键点检测 kpu 获得 kmodel 输出
def hk_kpu_get_output():
    with ScopedTiming("hk_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌关键点检测 接收kmodel结果的后处理
def hk_kpu_post_process(results, x, y, w, h):
    results_show = np.zeros(results.shape,dtype=np.int16)
    # results_show = np.zeros(len(results),dtype=np.int16)
    results_show[0::2] = results[0::2] * w + x
    results_show[1::2] = results[1::2] * h + y
    return results_show

# 手掌关键点检测 kpu 运行
def hk_kpu_run(kpu_obj,rgb888p_img, x, y, w, h):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1) 原图预处理，并设置模型输入
    hk_kpu_pre_process(rgb888p_img, x, y, w, h)
    # (2) kpu 运行
    with ScopedTiming("hk_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3) 释放ai2d资源
    hk_ai2d_release()
    # (4) 获取kpu输出
    results = hk_kpu_get_output()
    # (5) kpu结果后处理
    result = hk_kpu_post_process(results[0],x,y,w,h)
    # (6) 返回 关键点检测 结果
    return result

# 手掌关键点检测 kpu 释放内存
def hk_kpu_deinit():
    with ScopedTiming("hk_kpu_deinit",debug_mode > 0):
        if 'hk_ai2d' in globals():
            global hk_ai2d
            del hk_ai2d
        if 'hk_ai2d_output_tensor' in globals():
            global hk_ai2d_output_tensor
            del hk_ai2d_output_tensor

# 手掌关键点检测 计算角度
def hk_vector_2d_angle(v1,v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    v1_norm = np.sqrt(v1_x * v1_x+ v1_y * v1_y)
    v2_norm = np.sqrt(v2_x * v2_x + v2_y * v2_y)
    dot_product = v1_x * v2_x + v1_y * v2_y
    cos_angle = dot_product/(v1_norm*v2_norm)
    angle = np.acos(cos_angle)*180/np.pi
    # if (angle>180):
    #     return 65536
    return angle

# 利用手掌关键点检测的结果 判断手掌手势
def hk_gesture(kpu_hand_keypoint_detect,rgb888p_img,det_box):
    x1, y1, x2, y2 = int(det_box[2]),int(det_box[3]),int(det_box[4]),int(det_box[5])
    w = int(x2 - x1)
    h = int(y2 - y1)

    if (h<(0.1*OUT_RGB888P_HEIGHT)):
        return
    if (w<(0.25*OUT_RGB888P_WIDTH) and ((x1<(0.03*OUT_RGB888P_WIDTH)) or (x2>(0.97*OUT_RGB888P_WIDTH)))):
        return
    if (w<(0.15*OUT_RGB888P_WIDTH) and ((x1<(0.01*OUT_RGB888P_WIDTH)) or (x2>(0.99*OUT_RGB888P_WIDTH)))):
        return

    length = max(w,h)/2
    cx = (x1+x2)/2
    cy = (y1+y2)/2
    ratio_num = 1.26*length

    x1_kp = int(max(0,cx-ratio_num))
    y1_kp = int(max(0,cy-ratio_num))
    x2_kp = int(min(OUT_RGB888P_WIDTH-1, cx+ratio_num))
    y2_kp = int(min(OUT_RGB888P_HEIGHT-1, cy+ratio_num))
    w_kp = int(x2_kp - x1_kp + 1)
    h_kp = int(y2_kp - y1_kp + 1)

    results = hk_kpu_run(kpu_hand_keypoint_detect,rgb888p_img, x1_kp, y1_kp, w_kp, h_kp)

    angle_list = []
    for i in range(5):
        angle = hk_vector_2d_angle([(results[0]-results[i*8+4]), (results[1]-results[i*8+5])],[(results[i*8+6]-results[i*8+8]),(results[i*8+7]-results[i*8+9])])
        angle_list.append(angle)

    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = None
    if 65535. not in angle_list:
        if (angle_list[0]>thr_angle_thumb)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "fist"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]<thr_angle_s):
            gesture_str = "five"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "gun"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
            gesture_str = "love"
        elif (angle_list[0]>5)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "one"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
            gesture_str = "six"
        elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]>thr_angle):
            gesture_str = "three"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "thumbUp"
        elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "yeah"

    return gesture_str


#media_utils.py
global draw_img,osd_img,masks                                               #for display 定义全局 作图image对象
global buffer,media_source,media_sink                                       #for media  定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()
    global buffer, draw_img, osd_img, masks
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    masks = np.zeros((DISPLAY_HEIGHT,DISPLAY_WIDTH,4),dtype=np.uint8)
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888,alloc=image.ALLOC_REF,data=masks)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()


#**********for finger_guessing.py**********
def finger_guessing_inference():
    print("finger_guessing_test start")
    kpu_hand_detect = hd_kpu_init(hd_kmodel_file)                                       # 创建手掌检测的 kpu 对象
    kpu_hand_keypoint_detect = hk_kpu_init(hk_kmodel_file)                              # 创建手掌关键点检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                                           # 初始化 camera
    display_init()                                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)                                                      # 开启 camera
        counts_guess = -1                                                               # 猜拳次数 计数
        player_win = 0                                                                  # 玩家 赢次计数
        k230_win = 0                                                                    # k230 赢次计数
        sleep_end = False                                                               # 是否 停顿
        set_stop_id = True                                                              # 是否 暂停猜拳
        LIBRARY = ["fist","yeah","five"]                                                # 猜拳 石头剪刀布 三种方案的dict

        count = 0
        global draw_img,masks,osd_img
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()

            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                                 # 读取一帧图像

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    with ScopedTiming("trigger time", debug_mode > 0):
                        dets_no_pro = hd_kpu_run(kpu_hand_detect,rgb888p_img)                  # 执行手掌检测 kpu 运行 以及 后处理过程
                        gesture = ""
                        draw_img.clear()

                        dets = []
                        for det_box in dets_no_pro:
                            if det_box[4] < OUT_RGB888P_WIDTH - 10 :
                                dets.append(det_box)

                        for det_box in dets:
                            gesture = hk_gesture(kpu_hand_keypoint_detect,rgb888p_img,det_box)      # 执行手掌关键点检测 kpu 运行 以及 后处理过程 得到手势类型
                        if (len(dets) >= 2):
                            draw_img.draw_string( 300 , 500, "Must have one hand !", color=(255,255,0,0), scale=7)
                            draw_img.copy_to(osd_img)
                        elif (guess_mode == 0):
                            if (gesture == "fist"):
                                masks[:400,:400,:] = shear_image
                            elif (gesture == "five"):
                                masks[:400,:400,:] = fist_image
                            elif (gesture == "yeah"):
                                masks[:400,:400,:] = five_image
                            draw_img.copy_to(osd_img)
                        elif (guess_mode == 1):
                            if (gesture == "fist"):
                                masks[:400,:400,:] = five_image
                            elif (gesture == "five"):
                                masks[:400,:400,:] = shear_image
                            elif (gesture == "yeah"):
                                masks[:400,:400,:] = fist_image
                            draw_img.copy_to(osd_img)
                        else:
                            if (sleep_end):
                                time.sleep_ms(2000)
                                sleep_end = False
                            if (len(dets) == 0):
                                set_stop_id = True
                            if (counts_guess == -1 and gesture != "fist" and gesture != "yeah" and gesture != "five"):
                                draw_img.draw_string( 400 , 450, "G A M E   S T A R T", color=(255,255,0,0), scale=7)
                                draw_img.draw_string( 400 , 550, "     1   S E T     ", color=(255,255,0,0), scale=7)
                                draw_img.copy_to(osd_img)
                            elif (counts_guess == guess_mode):
                                draw_img.clear()
                                if (k230_win > player_win):
                                    draw_img.draw_string( 400 , 450, "Y O U    L O S E", color=(255,255,0,0), scale=7)
                                elif (k230_win < player_win):
                                    draw_img.draw_string( 400 , 450, "Y O U    W I N", color=(255,255,0,0), scale=7)
                                else:
                                    draw_img.draw_string( 400 , 450, "T I E    G A M E", color=(255,255,0,0), scale=7)
                                draw_img.copy_to(osd_img)
                                counts_guess = -1
                                player_win = 0
                                k230_win = 0

                                sleep_end = True
                            else:
                                if (set_stop_id):
                                    if (counts_guess == -1 and (gesture == "fist" or gesture == "yeah" or gesture == "five")):
                                        counts_guess = 0
                                    if (counts_guess != -1 and (gesture == "fist" or gesture == "yeah" or gesture == "five")):
                                        k230_guess = randint(1,10000) % 3
                                        if (gesture == "fist" and LIBRARY[k230_guess] == "yeah"):
                                            player_win += 1
                                        elif (gesture == "fist" and LIBRARY[k230_guess] == "five"):
                                            k230_win += 1
                                        if (gesture == "yeah" and LIBRARY[k230_guess] == "fist"):
                                            k230_win += 1
                                        elif (gesture == "yeah" and LIBRARY[k230_guess] == "five"):
                                            player_win += 1
                                        if (gesture == "five" and LIBRARY[k230_guess] == "fist"):
                                            player_win += 1
                                        elif (gesture == "five" and LIBRARY[k230_guess] == "yeah"):
                                            k230_win += 1

                                        if (LIBRARY[k230_guess] == "fist"):
                                            masks[:400,:400,:] = fist_image
                                        elif (LIBRARY[k230_guess] == "five"):
                                            masks[:400,:400,:] = five_image
                                        elif (LIBRARY[k230_guess] == "yeah"):
                                            masks[:400,:400,:] = shear_image

                                        counts_guess += 1;
                                        draw_img.draw_string( 400 , 450, "     " + str(counts_guess) + "   S E T     ", color=(255,255,0,0), scale=7)
                                        draw_img.copy_to(osd_img)
                                        set_stop_id = False
                                        sleep_end = True

                                    else:
                                        draw_img.draw_string( 400 , 450, "     " + str(counts_guess+1) + "   S E T     ", color=(255,255,0,0), scale=7)
                                        draw_img.copy_to(osd_img)
                                else:
                                    draw_img.copy_to(osd_img)
                        display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)                             # 将得到的图像 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)                                          # camera 释放图形

                if (count > 5):
                    gc.collect()
                    count = 0
                else:
                    count += 1

    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        camera_stop(CAM_DEV_ID_0)                           # 停止 camera
        display_deinit()                                    # 停止 display
        hd_kpu_deinit()                                     # 释放手掌检测 kpu
        hk_kpu_deinit()                                     # 释放手掌关键点检测 kpu

        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_hand_detect
        del kpu_hand_keypoint_detect

        if 'draw_img' in globals():
            global draw_img
            del draw_img
        if 'masks' in globals():
            global masks
            del masks
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                # 释放 整个 media


    print("finger_guessing_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    finger_guessing_inference()
```

### 7. OCR识别

```python
import ulab.numpy as np             #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn         #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *          #摄像头模块
from media.display import *         #显示模块
from media.media import *           #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import image                        #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                         #时间统计
import gc                           #垃圾回收模块
import aicube                       #aicube模块，封装检测分割等任务相关后处理
import os, sys

# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

# ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(640, 16)
OUT_RGB888P_HEIGH = 360

#kmodel输入参数设置
kmodel_input_shape_det = (1,3,640,640)      # OCR检测模型的kmodel输入分辨率
kmodel_input_shape_rec = (1,3,32,512)       # OCR识别模型的kmodel输入分辨率
rgb_mean = [0,0,0]                          # ai2d padding的值

#检测步骤kmodel相关参数设置
mask_threshold = 0.25                       # 二值化mask阈值
box_threshold = 0.3                         # 检测框分数阈值

#文件配置
root_dir = '/sdcard/app/tests/'
kmodel_file_det = root_dir + 'kmodel/ocr_det_int16.kmodel'    # 检测模型路径
kmodel_file_rec = root_dir + "kmodel/ocr_rec_int16.kmodel"    # 识别模型路径
dict_path = root_dir + 'utils/dict.txt'                      # 调试模式 大于0（调试）、 反之 （不调试）
debug_mode = 0

# OCR字典读取
with open(dict_path, 'r') as file:
    line_one = file.read(100000)
    line_list = line_one.split("\r\n")
DICT = {num: char.replace("\r", "").replace("\n", "") for num, char in enumerate(line_list)}

# scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

# utils 设定全局变量
# 当前kmodel
global current_kmodel_obj                                                                       # 设置全局kpu对象
# 检测阶段预处理应用的ai2d全局变量
global ai2d_det,ai2d_input_tensor_det,ai2d_output_tensor_det,ai2d_builder_det,ai2d_input_det    # 设置检测模型的ai2d对象，并定义ai2d的输入、输出和builder
# 识别阶段预处理应用的ai2d全局变量
global ai2d_rec,ai2d_input_tensor_rec,ai2d_output_tensor_rec,ai2d_builder_rec                   # 设置识别模型的ai2d对象，并定义ai2d的输入、输出和builder

# padding方法，一边padding，右padding或者下padding
def get_pad_one_side_param(out_img_size,input_img_size):
    dst_w = out_img_size[0]
    dst_h = out_img_size[1]

    input_width = input_img_size[0]
    input_high = input_img_size[1]

    ratio_w = dst_w / input_width
    ratio_h = dst_h / input_high
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h

    new_w = (int)(ratio * input_width)
    new_h = (int)(ratio * input_high)
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2

    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

# 检测步骤ai2d初始化
def ai2d_init_det():
    with ScopedTiming("ai2d_init_det",debug_mode > 0):
        global ai2d_det
        ai2d_det = nn.ai2d()
        ai2d_det.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d_det.set_pad_param(True, get_pad_one_side_param([kmodel_input_shape_det[3],kmodel_input_shape_det[2]], [OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH]), 0, [0, 0, 0])
        ai2d_det.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
        global ai2d_output_tensor_det
        data = np.ones(kmodel_input_shape_det, dtype=np.uint8)
        ai2d_output_tensor_det = nn.from_numpy(data)
        global ai2d_builder_det
        ai2d_builder_det = ai2d_det.build([1, 3, OUT_RGB888P_HEIGH, OUT_RGB888P_WIDTH], [1, 3, kmodel_input_shape_det[2], kmodel_input_shape_det[3]])


# 检测步骤的ai2d 运行，完成ai2d_init_det预设的预处理
def ai2d_run_det(rgb888p_img):
    with ScopedTiming("ai2d_run_det",debug_mode > 0):
        global ai2d_input_tensor_det,ai2d_builder_det,ai2d_input_det
        ai2d_input_det = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor_det = nn.from_numpy(ai2d_input_det)
        global ai2d_output_tensor_det
        ai2d_builder_det.run(ai2d_input_tensor_det, ai2d_output_tensor_det)

# 识别步骤ai2d初始化
def ai2d_init_rec():
    with ScopedTiming("ai2d_init_res",debug_mode > 0):
        global ai2d_rec,ai2d_output_tensor_rec
        ai2d_rec = nn.ai2d()
        ai2d_rec.set_dtype(nn.ai2d_format.RGB_packed,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        ai2d_out_data = np.ones((1, 3, kmodel_input_shape_rec[2], kmodel_input_shape_rec[3]), dtype=np.uint8)
        ai2d_output_tensor_rec = nn.from_numpy(ai2d_out_data)


# 识别步骤ai2d运行
def ai2d_run_rec(rgb888p_img):
    with ScopedTiming("ai2d_run_rec",debug_mode > 0):
        global ai2d_rec,ai2d_builder_rec,ai2d_input_tensor_rec,ai2d_output_tensor_rec
        ai2d_rec.set_pad_param(True, get_pad_one_side_param([kmodel_input_shape_rec[3],kmodel_input_shape_rec[2]],[rgb888p_img.shape[2],rgb888p_img.shape[1]]), 0, [0, 0, 0])
        ai2d_rec.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
        ai2d_builder_rec = ai2d_rec.build([rgb888p_img.shape[0], rgb888p_img.shape[1], rgb888p_img.shape[2],rgb888p_img.shape[3]],
                                                  [1, 3, kmodel_input_shape_rec[2], kmodel_input_shape_rec[3]])
        ai2d_input_tensor_rec = nn.from_numpy(rgb888p_img)
        ai2d_builder_rec.run(ai2d_input_tensor_rec, ai2d_output_tensor_rec)

# 检测步骤ai2d释放内存
def ai2d_release_det():
    with ScopedTiming("ai2d_release_det",debug_mode > 0):
        if "ai2d_input_tensor_det" in globals():
            global ai2d_input_tensor_det
            del ai2d_input_tensor_det

# 识别步骤ai2d释放内存
def ai2d_release_rec():
    with ScopedTiming("ai2d_release_rec",debug_mode > 0):
        if "ai2d_input_tensor_rec" in globals():
            global ai2d_input_tensor_rec
            del ai2d_input_tensor_rec

# 检测步骤kpu初始化
def kpu_init_det(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("kpu_init_det",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)
        ai2d_init_det()
        return kpu_obj

# 识别步骤kpu初始化
def kpu_init_rec(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("kpu_init_rec",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)
        ai2d_init_rec()
        return kpu_obj

# 检测步骤预处理，调用ai2d_run_det实现，并将ai2d的输出设置为kmodel的输入
def kpu_pre_process_det(rgb888p_img):
    ai2d_run_det(rgb888p_img)
    with ScopedTiming("kpu_pre_process_det",debug_mode > 0):
        global current_kmodel_obj,ai2d_output_tensor_det
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, ai2d_output_tensor_det)

# 识别步骤预处理，调用ai2d_init_run_rec实现，并将ai2d的输出设置为kmodel的输入
def kpu_pre_process_rec(rgb888p_img):
    ai2d_run_rec(rgb888p_img)
    with ScopedTiming("kpu_pre_process_rec",debug_mode > 0):
        global current_kmodel_obj,ai2d_output_tensor_rec
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, ai2d_output_tensor_rec)


# 获取kmodel的输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

# 检测步骤kpu运行
def kpu_run_det(kpu_obj,rgb888p_img):
    # kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    #（1）原图像预处理并设置模型输入
    kpu_pre_process_det(rgb888p_img)
    #（2）kpu推理
    with ScopedTiming("kpu_run_det",debug_mode > 0):
        # 检测运行
        kpu_obj.run()
    #（3）检测释放ai2d资源
    ai2d_release_det()
    #（4）获取检测kpu输出
    results = kpu_get_output()
    #（5）CHW转HWC
    global ai2d_input_det
    tmp = (ai2d_input_det.shape[0], ai2d_input_det.shape[1], ai2d_input_det.shape[2])
    ai2d_input_det = ai2d_input_det.reshape((ai2d_input_det.shape[0], ai2d_input_det.shape[1] * ai2d_input_det.shape[2]))
    ai2d_input_det = ai2d_input_det.transpose()
    tmp2 = ai2d_input_det.copy()
    tmp2 = tmp2.reshape((tmp[1], tmp[2], tmp[0]))
    #（6）后处理，aicube.ocr_post_process接口说明：
    #  接口：aicube.ocr_post_process(threshold_map,ai_isp,kmodel_input_shape,isp_shape,mask_threshold,box_threshold);
    #  参数说明：
    #     threshold_map: DBNet模型的输出为（N,kmodel_input_shape_det[2],kmodel_input_shape_det[3],2），两个通道分别为threshold map和segmentation map
    #     后处理过程只使用threshold map，因此将results[0][:,:,:,0] reshape成一维传给接口使用。
    #     ai_isp：后处理还会返回基于原图的检测框裁剪数据，因此要将原图数据reshape为一维传给接口处理。
    #     kmodel_input_shape：kmodel输入分辨率。
    #     isp_shape：AI原图分辨率。要将kmodel输出分辨率的检测框坐标映射到原图分辨率上，需要使用这两个分辨率的值。
    #     mask_threshold：用于二值化图像获得文本区域。
    #     box_threshold：检测框分数阈值，低于该阈值的检测框不计入结果。
    with ScopedTiming("kpu_post",debug_mode > 0):
        # 调用aicube模块的ocr_post_process完成ocr检测的后处理
        # det_results结构为[[crop_array_nhwc,[p1_x,p1_y,p2_x,p2_y,p3_x,p3_y,p4_x,p4_y]],...]
        det_results = aicube.ocr_post_process(results[0][:, :, :, 0].reshape(-1), tmp2.reshape(-1),
                                                  [kmodel_input_shape_det[3], kmodel_input_shape_det[2]],
                                                  [OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH], mask_threshold, box_threshold)
    return det_results

# 识别步骤后处理
def kpu_run_rec(kpu_obj,rgb888p_img):
    # kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    #（1）识别预处理并设置模型输入
    kpu_pre_process_rec(rgb888p_img)
    #（2）kpu推理
    with ScopedTiming("kpu_run_rec",debug_mode > 0):
        # 识别运行
        kpu_obj.run()
    #（3）识别释放ai2d资源
    ai2d_release_rec()
    #（4）获取识别kpu输出
    results = kpu_get_output()
    #（5）识别后处理，results结构为[(N,MAX_LENGTH,DICT_LENGTH),...],在axis=2维度上取argmax获取当前识别字符在字典中的索引
    preds = np.argmax(results[0], axis=2).reshape((-1))
    output_txt = ""
    for i in range(len(preds)):
        # 当前识别字符不是字典的最后一个字符并且和前一个字符不重复（去重），加入识别结果字符串
        if preds[i] != (len(DICT) - 1) and (not (i > 0 and preds[i - 1] == preds[i])):
            output_txt = output_txt + DICT[preds[i]]
    return output_txt

# 释放检测步骤kpu、ai2d以及ai2d相关的tensor
def kpu_deinit_det():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        global ai2d_det,ai2d_output_tensor_det
        if "ai2d_det" in globals():
            del ai2d_det
        if "ai2d_output_tensor_det" in globals():
            del ai2d_output_tensor_det

# 释放识别步骤kpu
def kpu_deinit_rec():
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        global ai2d_rec,ai2d_output_tensor_rec
        if "ai2d_rec" in globals():
            del ai2d_rec
        if "ai2d_output_tensor_rec" in globals():
            del ai2d_output_tensor_rec


#********************for media_utils.py********************

global draw_img,osd_img                                     #for display
global buffer,media_source,media_sink                       #for media

# display初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# 释放display
def display_deinit():
    display.deinit()

# display显示检测识别框
def display_draw(det_results):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if det_results:
            draw_img.clear()
            # 循环绘制所有检测到的框
            for j in det_results:
                # 将原图的坐标点转换成显示的坐标点，循环绘制四条直线，得到一个矩形框
                for i in range(4):
                    x1 = j[1][(i * 2)] / OUT_RGB888P_WIDTH * DISPLAY_WIDTH
                    y1 = j[1][(i * 2 + 1)] / OUT_RGB888P_HEIGH * DISPLAY_HEIGHT
                    x2 = j[1][((i + 1) * 2) % 8] / OUT_RGB888P_WIDTH * DISPLAY_WIDTH
                    y2 = j[1][((i + 1) * 2 + 1) % 8] / OUT_RGB888P_HEIGH * DISPLAY_HEIGHT
                    draw_img.draw_line((int(x1), int(y1), int(x2), int(y2)), color=(255, 0, 0, 255),
                                       thickness=5)
                draw_img.copy_to(osd_img)
                display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            draw_img.clear()
            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

# camera初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)
    # camera获取的通道0图像送display显示
    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)
    # camera获取的通道2图像送ai处理
    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 启动视频流
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 捕获一帧图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 释放内存
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 停止视频流
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()
    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放buffer，销毁link
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    global buffer,media_source, media_sink
    if "buffer" in globals():
        media.release_buffer(buffer)
    if 'media_source' in globals() and 'media_sink' in globals():
        media.destroy_link(media_source, media_sink)
    media.buffer_deinit()

def ocr_rec_inference():
    print("ocr_rec_test start")
    kpu_ocr_det = kpu_init_det(kmodel_file_det)     # 创建OCR检测kpu对象
    kpu_ocr_rec = kpu_init_rec(kmodel_file_rec)     # 创建OCR识别kpu对象
    camera_init(CAM_DEV_ID_0)                       # camera初始化
    display_init()                                  # display初始化
    try:
        media_init()
        camera_start(CAM_DEV_ID_0)
        gc_count=0
        while True:
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)     # 读取一帧图像
                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    det_results = kpu_run_det(kpu_ocr_det,rgb888p_img)      # kpu运行获取OCR检测kmodel的推理输出
                    ocr_results=""
                    if det_results:
                        for j in det_results:
                            ocr_result = kpu_run_rec(kpu_ocr_rec,j[0])      # j[0]为检测框的裁剪部分，kpu运行获取OCR识别kmodel的推理输出
                            ocr_results = ocr_results+" ["+ocr_result+"] "
                            gc.collect()
                    print("\n"+ocr_results)
                    display_draw(det_results)
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)
                if (gc_count>1):
                    gc.collect()
                    gc_count = 0
                else:
                    gc_count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        camera_stop(CAM_DEV_ID_0)                                           # 停止camera
        display_deinit()                                                    # 释放display
        kpu_deinit_det()                                                    # 释放OCR检测步骤kpu
        kpu_deinit_rec()                                                    # 释放OCR识别步骤kpu
        if "current_kmodel_obj" in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_ocr_det
        del kpu_ocr_rec
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                                # 释放整个media
    print("ocr_rec_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    ocr_rec_inference()
```

### 8. 手掌关键点检测

```python
import aicube                   #aicube模块，封装检测分割等任务相关后处理
from media.camera import *      #摄像头模块
from media.display import *     #显示模块
from media.media import *       #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区

import nncase_runtime as nn     #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np         #类似python numpy操作，但也会有一些接口不同

import time                     #时间统计
import image                    #图像模块，主要用于读取、图像绘制元素（框、点等）等操作

import gc                       #垃圾回收模块
import os, sys                  #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

##ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

#--------for hand detection----------
#kmodel输入shape
hd_kmodel_input_shape = (1,3,512,512)                           # 手掌检测kmodel输入分辨率

#kmodel相关参数设置
confidence_threshold = 0.2                                      # 手掌检测阈值，用于过滤roi
nms_threshold = 0.5                                             # 手掌检测框阈值，用于过滤重复roi
hd_kmodel_frame_size = [512,512]                                # 手掌检测输入图片尺寸
hd_frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGHT]          # 手掌检测直接输入图片尺寸
strides = [8,16,32]                                             # 输出特征图的尺寸与输入图片尺寸的比
num_classes = 1                                                 # 手掌检测模型输出类别数
nms_option = False                                              # 是否所有检测框一起做NMS，False则按照不同的类分别应用NMS

root_dir = '/sdcard/app/tests/'
hd_kmodel_file = root_dir + "kmodel/hand_det.kmodel"            # 手掌检测kmodel文件的路径
anchors = [26,27, 53,52, 75,71, 80,99, 106,82, 99,134, 140,113, 161,172, 245,276]   #anchor设置

#--------for hand keypoint detection----------
#kmodel输入shape
hk_kmodel_input_shape = (1,3,256,256)                           # 手掌关键点检测kmodel输入分辨率

#kmodel相关参数设置
hk_kmodel_frame_size = [256,256]                                # 手掌关键点检测输入图片尺寸
hk_kmodel_file = root_dir + 'kmodel/handkp_det.kmodel'          # 手掌关键点检测kmodel文件的路径

debug_mode = 0                                                  # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                                   # 定义全局的 kpu 对象
global hd_ai2d,hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder   # 定义手掌检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor,hk_ai2d_builder   # 定义手掌关键点检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder

#-------hand detect--------:
# 手掌检测ai2d 初始化
def hd_ai2d_init():
    with ScopedTiming("hd_ai2d_init",debug_mode > 0):
        global hd_ai2d
        global hd_ai2d_builder
        global hd_ai2d_output_tensor
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = hd_kmodel_frame_size[0]
        height = hd_kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        hd_ai2d = nn.ai2d()
        hd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        hd_ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        hd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        hd_ai2d_builder = hd_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,height,width])
        data = np.ones(hd_kmodel_input_shape, dtype=np.uint8)
        hd_ai2d_output_tensor = nn.from_numpy(data)

# 手掌检测 ai2d 运行
def hd_ai2d_run(rgb888p_img):
    with ScopedTiming("hd_ai2d_run",debug_mode > 0):
        global hd_ai2d_input_tensor, hd_ai2d_output_tensor, hd_ai2d_builder
        hd_ai2d_input = rgb888p_img.to_numpy_ref()
        hd_ai2d_input_tensor = nn.from_numpy(hd_ai2d_input)

        hd_ai2d_builder.run(hd_ai2d_input_tensor, hd_ai2d_output_tensor)

# 手掌检测 ai2d 释放内存
def hd_ai2d_release():
    with ScopedTiming("hd_ai2d_release",debug_mode > 0):
        global hd_ai2d_input_tensor
        del hd_ai2d_input_tensor

# 手掌检测 kpu 初始化
def hd_kpu_init(hd_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hd_kpu_init",debug_mode > 0):
        hd_kpu_obj = nn.kpu()
        hd_kpu_obj.load_kmodel(hd_kmodel_file)

        hd_ai2d_init()
        return hd_kpu_obj

# 手掌检测 kpu 输入预处理
def hd_kpu_pre_process(rgb888p_img):
    hd_ai2d_run(rgb888p_img)
    with ScopedTiming("hd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hd_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hd_ai2d_output_tensor)

# 手掌检测 kpu 获得 kmodel 输出
def hd_kpu_get_output():
    with ScopedTiming("hd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌检测 kpu 运行
def hd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hd_kpu_pre_process(rgb888p_img)
    # (2)手掌检测 kpu 运行
    with ScopedTiming("hd_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌检测 ai2d 资源
    hd_ai2d_release()
    # (4)获取手掌检测 kpu 输出
    results = hd_kpu_get_output()
    # (5)手掌检测 kpu 结果后处理
    dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], hd_kmodel_frame_size, hd_frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)
    # (6)返回手掌检测结果
    return dets

# 手掌检测 kpu 释放内存
def hd_kpu_deinit():
    with ScopedTiming("hd_kpu_deinit",debug_mode > 0):
        if 'hd_ai2d' in globals():                             #删除hd_ai2d变量，释放对它所引用对象的内存引用
            global hd_ai2d
            del hd_ai2d
        if 'hd_ai2d_output_tensor' in globals():               #删除hd_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global hd_ai2d_output_tensor
            del hd_ai2d_output_tensor
        if 'hd_ai2d_builder' in globals():                     #删除hd_ai2d_builder变量，释放对它所引用对象的内存引用
            global hd_ai2d_builder
            del hd_ai2d_builder


#-------hand keypoint detection------:
# 手掌关键点检测 ai2d 初始化
def hk_ai2d_init():
    with ScopedTiming("hk_ai2d_init",debug_mode > 0):
        global hk_ai2d, hk_ai2d_output_tensor
        hk_ai2d = nn.ai2d()
        hk_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        data = np.ones(hk_kmodel_input_shape, dtype=np.uint8)
        hk_ai2d_output_tensor = nn.from_numpy(data)

# 手掌关键点检测 ai2d 运行
def hk_ai2d_run(rgb888p_img, x, y, w, h):
    with ScopedTiming("hk_ai2d_run",debug_mode > 0):
        global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor
        hk_ai2d_input = rgb888p_img.to_numpy_ref()
        hk_ai2d_input_tensor = nn.from_numpy(hk_ai2d_input)

        hk_ai2d.set_crop_param(True, x, y, w, h)
        hk_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )

        global hk_ai2d_builder
        hk_ai2d_builder = hk_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,hk_kmodel_frame_size[1],hk_kmodel_frame_size[0]])
        hk_ai2d_builder.run(hk_ai2d_input_tensor, hk_ai2d_output_tensor)

# 手掌关键点检测 ai2d 释放内存
def hk_ai2d_release():
    with ScopedTiming("hk_ai2d_release",debug_mode > 0):
        global hk_ai2d_input_tensor, hk_ai2d_builder
        del hk_ai2d_input_tensor
        del hk_ai2d_builder

# 手掌关键点检测 kpu 初始化
def hk_kpu_init(hk_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hk_kpu_init",debug_mode > 0):
        hk_kpu_obj = nn.kpu()
        hk_kpu_obj.load_kmodel(hk_kmodel_file)

        hk_ai2d_init()
        return hk_kpu_obj

# 手掌关键点检测 kpu 输入预处理
def hk_kpu_pre_process(rgb888p_img, x, y, w, h):
    hk_ai2d_run(rgb888p_img, x, y, w, h)
    with ScopedTiming("hk_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hk_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hk_ai2d_output_tensor)

# 手掌关键点检测 kpu 获得 kmodel 输出
def hk_kpu_get_output():
    with ScopedTiming("hk_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌关键点检测 kpu 运行
def hk_kpu_run(kpu_obj,rgb888p_img, x, y, w, h):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hk_kpu_pre_process(rgb888p_img, x, y, w, h)
    # (2)手掌关键点检测 kpu 运行
    with ScopedTiming("hk_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌关键点检测 ai2d 资源
    hk_ai2d_release()
    # (4)获取手掌关键点检测 kpu 输出
    results = hk_kpu_get_output()
    # (5)返回手掌关键点检测结果
    return results

# 手掌关键点检测 kpu 释放内存
def hk_kpu_deinit():
    with ScopedTiming("hk_kpu_deinit",debug_mode > 0):
        if 'hk_ai2d' in globals():                          #删除hk_ai2d变量，释放对它所引用对象的内存引用
            global hk_ai2d
            del hk_ai2d
        if 'hk_ai2d_output_tensor' in globals():            #删除hk_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global hk_ai2d_output_tensor
            del hk_ai2d_output_tensor


#media_utils.py
global draw_img,osd_img                              #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 标出检测到的21个关键点并用不同颜色的线段连接
def display_draw(results, x, y, w, h):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img

        if results:
            results_show = np.zeros(results.shape,dtype=np.int16)
            results_show[0::2] = (results[0::2] * w + x) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
            results_show[1::2] = (results[1::2] * h + y) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT
            for i in range(len(results_show)/2):
                draw_img.draw_circle(results_show[i*2], results_show[i*2+1], 1, color=(255, 0, 255, 0),fill=False)
            for i in range(5):
                j = i*8
                if i==0:
                    R = 255; G = 0; B = 0
                if i==1:
                    R = 255; G = 0; B = 255
                if i==2:
                    R = 255; G = 255; B = 0
                if i==3:
                    R = 0; G = 255; B = 0
                if i==4:
                    R = 0; G = 0; B = 255
                draw_img.draw_line(results_show[0], results_show[1], results_show[j+2], results_show[j+3], color=(255,R,G,B), thickness = 3)
                draw_img.draw_line(results_show[j+2], results_show[j+3], results_show[j+4], results_show[j+5], color=(255,R,G,B), thickness = 3)
                draw_img.draw_line(results_show[j+4], results_show[j+5], results_show[j+6], results_show[j+7], color=(255,R,G,B), thickness = 3)
                draw_img.draw_line(results_show[j+6], results_show[j+7], results_show[j+8], results_show[j+9], color=(255,R,G,B), thickness = 3)

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)
    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for hand_keypoint_detect.py**********
def hand_keypoint_detect_inference():
    print("hand_keypoint_detect_test start")
    kpu_hand_detect = hd_kpu_init(hd_kmodel_file)                       # 创建手掌检测的 kpu 对象
    kpu_hand_keypoint_detect = hk_kpu_init(hk_kmodel_file)              # 创建手掌关键点检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)
        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    dets = hd_kpu_run(kpu_hand_detect,rgb888p_img)                                                  # 执行手掌检测 kpu 运行 以及 后处理过程
                    draw_img.clear()

                    for det_box in dets:
                        x1, y1, x2, y2 = int(det_box[2]),int(det_box[3]),int(det_box[4]),int(det_box[5])
                        w = int(x2 - x1)
                        h = int(y2 - y1)

                        if (h<(0.1*OUT_RGB888P_HEIGHT)):
                            continue
                        if (w<(0.25*OUT_RGB888P_WIDTH) and ((x1<(0.03*OUT_RGB888P_WIDTH)) or (x2>(0.97*OUT_RGB888P_WIDTH)))):
                            continue
                        if (w<(0.15*OUT_RGB888P_WIDTH) and ((x1<(0.01*OUT_RGB888P_WIDTH)) or (x2>(0.99*OUT_RGB888P_WIDTH)))):
                            continue

                        w_det = int(float(x2 - x1) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                        h_det = int(float(y2 - y1) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)
                        x_det = int(x1*DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                        y_det = int(y1*DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)

                        length = max(w,h)/2
                        cx = (x1+x2)/2
                        cy = (y1+y2)/2
                        ratio_num = 1.26*length

                        x1_kp = int(max(0,cx-ratio_num))
                        y1_kp = int(max(0,cy-ratio_num))
                        x2_kp = int(min(OUT_RGB888P_WIDTH-1, cx+ratio_num))
                        y2_kp = int(min(OUT_RGB888P_HEIGHT-1, cy+ratio_num))
                        w_kp = int(x2_kp - x1_kp + 1)
                        h_kp = int(y2_kp - y1_kp + 1)

                        hk_results = hk_kpu_run(kpu_hand_keypoint_detect,rgb888p_img, x1_kp, y1_kp, w_kp, h_kp)     # 执行手掌关键点检测 kpu 运行 以及 后处理过程

                        draw_img.draw_rectangle(x_det, y_det, w_det, h_det, color=(255, 0, 255, 0), thickness = 2)  # 将得到的手掌检测结果 绘制到 display
                        display_draw(hk_results[0], x1_kp, y1_kp, w_kp, h_kp)                                       # 将得到的手掌关键点检测结果 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)         # camera 释放图像
                if (count>10):
                    gc.collect()
                    count = 0
                else:
                    count += 1

            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        camera_stop(CAM_DEV_ID_0)                                       # 停止 camera
        display_deinit()                                                # 释放 display
        hd_kpu_deinit()                                                 # 释放手掌检测 kpu
        hk_kpu_deinit()                                                 # 释放手掌关键点检测 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_hand_detect
        del kpu_hand_keypoint_detect
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                                  # 释放 整个media

    print("hand_detect_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    hand_keypoint_detect_inference() 
```

### 9. 静态手势识别

```python
import aicube                   #aicube模块，封装检测分割等任务相关后处理
from media.camera import *      #摄像头模块
from media.display import *     #显示模块
from media.media import *       #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区

import nncase_runtime as nn     #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np         #类似python numpy操作，但也会有一些接口不同

import time                     #时间统计
import image                    #图像模块，主要用于读取、图像绘制元素（框、点等）等操作

import gc                       #垃圾回收模块
import os, sys                  #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

##ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

#--------for hand detection----------
#kmodel输入shape
hd_kmodel_input_shape = (1,3,512,512)                           # 手掌检测kmodel输入分辨率

#kmodel相关参数设置
confidence_threshold = 0.2                                      # 手掌检测阈值，用于过滤roi
nms_threshold = 0.5                                             # 手掌检测框阈值，用于过滤重复roi
hd_kmodel_frame_size = [512,512]                                # 手掌检测输入图片尺寸
hd_frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGHT]          # 手掌检测直接输入图片尺寸
strides = [8,16,32]                                             # 输出特征图的尺寸与输入图片尺寸的比
num_classes = 1                                                 # 手掌检测模型输出类别数
nms_option = False                                              # 是否所有检测框一起做NMS，False则按照不同的类分别应用NMS

root_dir = '/sdcard/app/tests/'
hd_kmodel_file = root_dir + 'kmodel/hand_det.kmodel'            # 手掌检测kmodel文件的路径
anchors = [26,27, 53,52, 75,71, 80,99, 106,82, 99,134, 140,113, 161,172, 245,276]   #anchor设置

#--------for hand recognition----------
#kmodel输入shape
hr_kmodel_input_shape = (1,3,224,224)                           # 手势识别kmodel输入分辨率

#kmodel相关参数设置
hr_kmodel_frame_size = [224,224]                                # 手势识别输入图片尺寸
labels = ["gun","other","yeah","five"]                          # 模型输出类别名称

hr_kmodel_file = root_dir + "kmodel/hand_reco.kmodel"           # 手势识别kmodel文件的路径

debug_mode = 0                                                  # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                                   # 定义全局的 kpu 对象
global hd_ai2d,hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder   # 定义手掌检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global hr_ai2d,hr_ai2d_input_tensor,hr_ai2d_output_tensor,hr_ai2d_builder   # 定义手势识别全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder

#-------hand detect--------:
# 手掌检测 ai2d 初始化
def hd_ai2d_init():
    with ScopedTiming("hd_ai2d_init",debug_mode > 0):
        global hd_ai2d
        global hd_ai2d_builder
        global hd_ai2d_output_tensor
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = hd_kmodel_frame_size[0]
        height = hd_kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        hd_ai2d = nn.ai2d()
        hd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        hd_ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        hd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        hd_ai2d_builder = hd_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,height,width])
        data = np.ones(hd_kmodel_input_shape, dtype=np.uint8)
        hd_ai2d_output_tensor = nn.from_numpy(data)

# 手掌检测 ai2d 运行
def hd_ai2d_run(rgb888p_img):
    with ScopedTiming("hd_ai2d_run",debug_mode > 0):
        global hd_ai2d_input_tensor, hd_ai2d_output_tensor, hd_ai2d_builder
        hd_ai2d_input = rgb888p_img.to_numpy_ref()
        hd_ai2d_input_tensor = nn.from_numpy(hd_ai2d_input)

        hd_ai2d_builder.run(hd_ai2d_input_tensor, hd_ai2d_output_tensor)

# 手掌检测 ai2d 释放内存
def hd_ai2d_release():
    with ScopedTiming("hd_ai2d_release",debug_mode > 0):
        global hd_ai2d_input_tensor
        del hd_ai2d_input_tensor

# 手掌检测 kpu 初始化
def hd_kpu_init(hd_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hd_kpu_init",debug_mode > 0):
        hd_kpu_obj = nn.kpu()
        hd_kpu_obj.load_kmodel(hd_kmodel_file)

        hd_ai2d_init()
        return hd_kpu_obj

# 手掌检测 kpu 输入预处理
def hd_kpu_pre_process(rgb888p_img):
    hd_ai2d_run(rgb888p_img)
    with ScopedTiming("hd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hd_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hd_ai2d_output_tensor)

# 手掌检测 kpu 获得 kmodel 输出
def hd_kpu_get_output():
    with ScopedTiming("hd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌检测 kpu 运行
def hd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hd_kpu_pre_process(rgb888p_img)
    # (2)手掌检测 kpu 运行
    with ScopedTiming("hd_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌检测 ai2d 资源
    hd_ai2d_release()
    # (4)获取手掌检测 kpu 输出
    results = hd_kpu_get_output()
    # (5)手掌检测 kpu 结果后处理
    dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], hd_kmodel_frame_size, hd_frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)
    # (6)返回手掌检测结果
    return dets

# 手掌检测 kpu 释放内存
def hd_kpu_deinit():
    with ScopedTiming("hd_kpu_deinit",debug_mode > 0):
        if 'hd_ai2d' in globals():                             #删除hd_ai2d变量，释放对它所引用对象的内存引用
            global hd_ai2d
            del hd_ai2d
        if 'hd_ai2d_output_tensor' in globals():               #删除hd_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global hd_ai2d_output_tensor
            del hd_ai2d_output_tensor
        if 'hd_ai2d_builder' in globals():                     #删除hd_ai2d_builder变量，释放对它所引用对象的内存引用
            global hd_ai2d_builder
            del hd_ai2d_builder


#-------hand recognition--------:
# 手势识别 ai2d 初始化
def hr_ai2d_init():
    with ScopedTiming("hr_ai2d_init",debug_mode > 0):
        global hr_ai2d, hr_ai2d_output_tensor
        hr_ai2d = nn.ai2d()
        hr_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        data = np.ones(hr_kmodel_input_shape, dtype=np.uint8)
        hr_ai2d_output_tensor = nn.from_numpy(data)

# 手势识别 ai2d 运行
def hr_ai2d_run(rgb888p_img, x, y, w, h):
    with ScopedTiming("hr_ai2d_run",debug_mode > 0):
        global hr_ai2d,hr_ai2d_input_tensor,hr_ai2d_output_tensor
        hr_ai2d_input = rgb888p_img.to_numpy_ref()
        hr_ai2d_input_tensor = nn.from_numpy(hr_ai2d_input)

        hr_ai2d.set_crop_param(True, x, y, w, h)
        hr_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )

        global hr_ai2d_builder
        hr_ai2d_builder = hr_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,hr_kmodel_frame_size[1],hr_kmodel_frame_size[0]])
        hr_ai2d_builder.run(hr_ai2d_input_tensor, hr_ai2d_output_tensor)

# 手势识别 ai2d 释放内存
def hr_ai2d_release():
    with ScopedTiming("hr_ai2d_release",debug_mode > 0):
        global hr_ai2d_input_tensor, hr_ai2d_builder
        del hr_ai2d_input_tensor
        del hr_ai2d_builder

# 手势识别 kpu 初始化
def hr_kpu_init(hr_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hr_kpu_init",debug_mode > 0):
        hr_kpu_obj = nn.kpu()
        hr_kpu_obj.load_kmodel(hr_kmodel_file)

        hr_ai2d_init()
        return hr_kpu_obj

# 手势识别 kpu 输入预处理
def hr_kpu_pre_process(rgb888p_img, x, y, w, h):
    hr_ai2d_run(rgb888p_img, x, y, w, h)
    with ScopedTiming("hr_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hr_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hr_ai2d_output_tensor)

# 手势识别 kpu 获得 kmodel 输出
def hr_kpu_get_output():
    with ScopedTiming("hr_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# softmax实现
def softmax(x):
    x -= np.max(x)
    x = np.exp(x) / np.sum(np.exp(x))
    return x

# 手势识别 kpu 输出后处理
def hr_kpu_post_process(results):
    x_softmax = softmax(results[0])
    result = np.argmax(x_softmax)
    text = " " + labels[result] + ": " + str(round(x_softmax[result],2))
    return text

# 手势识别 kpu 运行
def hr_kpu_run(kpu_obj,rgb888p_img, x, y, w, h):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hr_kpu_pre_process(rgb888p_img, x, y, w, h)
    # (2)手势识别 kpu 运行
    with ScopedTiming("hr_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手势识别 ai2d 资源
    hr_ai2d_release()
    # (4)获取手势识别 kpu 输出
    results = hr_kpu_get_output()
    # (5)手势识别 kpu 结果后处理
    result = hr_kpu_post_process(results)
    # (6)返回手势识别结果
    return result

# 手势识别 kpu 释放内存
def hr_kpu_deinit():
    with ScopedTiming("hr_kpu_deinit",debug_mode > 0):
        if 'hr_ai2d' in globals():                          #删除hr_ai2d变量，释放对它所引用对象的内存引用
            global hr_ai2d
            del hr_ai2d
        if 'hr_ai2d_output_tensor' in globals():            #删除hr_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global hr_ai2d_output_tensor
            del hr_ai2d_output_tensor

#media_utils.py
global draw_img,osd_img                                     #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)
    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for hand_recognition.py**********
def hand_recognition_inference():
    print("hand_recognition start")
    kpu_hand_detect = hd_kpu_init(hd_kmodel_file)                       # 创建手掌检测的 kpu 对象
    kpu_hand_recognition = hr_kpu_init(hr_kmodel_file)                  # 创建手势识别的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)
        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    dets = hd_kpu_run(kpu_hand_detect,rgb888p_img)                                                  # 执行手掌检测 kpu 运行 以及 后处理过程
                    draw_img.clear()

                    for det_box in dets:
                        x1, y1, x2, y2 = det_box[2],det_box[3],det_box[4],det_box[5]
                        w = int(x2 - x1)
                        h = int(y2 - y1)

                        if (h<(0.1*OUT_RGB888P_HEIGHT)):
                            continue
                        if (w<(0.25*OUT_RGB888P_WIDTH) and ((x1<(0.03*OUT_RGB888P_WIDTH)) or (x2>(0.97*OUT_RGB888P_WIDTH)))):
                            continue
                        if (w<(0.15*OUT_RGB888P_WIDTH) and ((x1<(0.01*OUT_RGB888P_WIDTH)) or (x2>(0.99*OUT_RGB888P_WIDTH)))):
                            continue

                        w_det = int(float(x2 - x1) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                        h_det = int(float(y2 - y1) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)
                        x_det = int(x1*DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                        y_det = int(y1*DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)

                        length = max(w,h)/2
                        cx = (x1+x2)/2
                        cy = (y1+y2)/2
                        ratio_num = 1.1*length

                        x1_kp = int(max(0,cx-ratio_num))
                        y1_kp = int(max(0,cy-ratio_num))
                        x2_kp = int(min(OUT_RGB888P_WIDTH-1, cx+ratio_num))
                        y2_kp = int(min(OUT_RGB888P_HEIGHT-1, cy+ratio_num))
                        w_kp = int(x2_kp - x1_kp + 1)
                        h_kp = int(y2_kp - y1_kp + 1)

                        hr_results = hr_kpu_run(kpu_hand_recognition,rgb888p_img, x1_kp, y1_kp, w_kp, h_kp)          # 执行手势识别 kpu 运行 以及 后处理过程
                        draw_img.draw_rectangle(x_det, y_det, w_det, h_det, color=(255, 0, 255, 0), thickness = 2)   # 将得到的手掌检测结果 绘制到 display
                        draw_img.draw_string( x_det, y_det-50, hr_results, color=(255,0, 255, 0), scale=4)           # 将得到的手势识别结果 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)          # camera 释放图像
                if (count>10):
                    gc.collect()
                    count = 0
                else:
                    count += 1

            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        camera_stop(CAM_DEV_ID_0)                                       # 停止 camera
        display_deinit()                                                # 释放 display
        hd_kpu_deinit()                                                 # 释放手掌检测 kpu
        hr_kpu_deinit()                                                 # 释放手势识别 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_hand_detect
        del kpu_hand_recognition

        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                                  # 释放 整个media

    print("hand_recognition_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    hand_recognition_inference()
```

### 10.人脸mesh

```python
import ulab.numpy as np                  # 类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn              # nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *               # 摄像头模块
from media.display import *              # 显示模块
from media.media import *                # 软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import aidemo                            # aidemo模块，封装ai demo相关后处理、画图操作
import image                             # 图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                              # 时间统计
import gc                                # 垃圾回收模块
import os,sys                                # 操作系统接口模块
import math                              # 数学模块


#********************for config.py********************
# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)                   # 显示宽度要求16位对齐
DISPLAY_HEIGHT = 1080

# ai原图分辨率，sensor默认出图为16:9，若需不形变原图，最好按照16:9比例设置宽高
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)               # ai原图宽度要求16位对齐
OUT_RGB888P_HEIGH = 1080

# kmodel参数设置
# 人脸检测kmodel输入shape
fd_kmodel_input_shape = (1,3,320,320)
# 人脸mesh kmodel输入shape
fm_kmodel_input_shape = (1,3,120,120)
fmpost_kmodel_input_shapes = [(3,3),(3,1),(40,1),(10,1)]
# ai原图padding
rgb_mean = [104,117,123]

#人脸检测kmodel其它参数设置
confidence_threshold = 0.5               # 人脸检测阈值
top_k = 5000
nms_threshold = 0.2
keep_top_k = 750
vis_thres = 0.5
variance = [0.1, 0.2]
anchor_len = 4200
score_dim = 2
det_dim = 4
keypoint_dim = 10

# 文件配置
# 人脸检测kmodel
root_dir = '/sdcard/app/tests/'
fd_kmodel_file = root_dir + 'kmodel/face_detection_320.kmodel'
# 人脸mesh kmodel
fm_kmodel_file = root_dir + 'kmodel/face_alignment.kmodel'
# 人脸mesh后处理kmodel
fmpost_kmodel_file = root_dir + 'kmodel/face_alignment_post.kmodel'
# anchor文件
anchors_path = root_dir + 'utils/prior_data_320.bin'
# 人脸mesh参数均值
param_mean = np.array([0.0003492636315058917,2.52790130161884e-07,-6.875197868794203e-07,60.1679573059082,-6.295513230725192e-07,0.0005757200415246189,-5.085391239845194e-05,74.2781982421875,5.400917189035681e-07,6.574138387804851e-05,0.0003442012530285865,-66.67157745361328,-346603.6875,-67468.234375,46822.265625,-15262.046875,4350.5888671875,-54261.453125,-18328.033203125,-1584.328857421875,-84566.34375,3835.960693359375,-20811.361328125,38094.9296875,-19967.85546875,-9241.3701171875,-19600.71484375,13168.08984375,-5259.14404296875,1848.6478271484375,-13030.662109375,-2435.55615234375,-2254.20654296875,-14396.5615234375,-6176.3291015625,-25621.919921875,226.39447021484375,-6326.12353515625,-10867.2509765625,868.465087890625,-5831.14794921875,2705.123779296875,-3629.417724609375,2043.9901123046875,-2446.6162109375,3658.697021484375,-7645.98974609375,-6674.45263671875,116.38838958740234,7185.59716796875,-1429.48681640625,2617.366455078125,-1.2070955038070679,0.6690792441368103,-0.17760828137397766,0.056725528091192245,0.03967815637588501,-0.13586315512657166,-0.09223993122577667,-0.1726071834564209,-0.015804484486579895,-0.1416848599910736],dtype=np.float)
# 人脸mesh参数方差
param_std = np.array([0.00017632152594160289,6.737943476764485e-05,0.00044708489440381527,26.55023193359375,0.0001231376954820007,4.493021697271615e-05,7.923670636955649e-05,6.982563018798828,0.0004350444069132209,0.00012314890045672655,0.00017400001524947584,20.80303955078125,575421.125,277649.0625,258336.84375,255163.125,150994.375,160086.109375,111277.3046875,97311.78125,117198.453125,89317.3671875,88493.5546875,72229.9296875,71080.2109375,50013.953125,55968.58203125,47525.50390625,49515.06640625,38161.48046875,44872.05859375,46273.23828125,38116.76953125,28191.162109375,32191.4375,36006.171875,32559.892578125,25551.1171875,24267.509765625,27521.3984375,23166.53125,21101.576171875,19412.32421875,19452.203125,17454.984375,22537.623046875,16174.28125,14671.640625,15115.6884765625,13870.0732421875,13746.3125,12663.1337890625,1.5870834589004517,1.5077009201049805,0.5881357789039612,0.5889744758605957,0.21327851712703705,0.2630201280117035,0.2796429395675659,0.38030216097831726,0.16162841022014618,0.2559692859649658],dtype=np.float)
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0

#********************for scoped_timing.py********************
# 时间统计类
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#********************for ai_utils.py********************
global current_kmodel_obj #当前kpu对象
# fd_ai2d：               人脸检测ai2d实例
# fd_ai2d_input_tensor：  人脸检测ai2d输入
# fd_ai2d_output_tensor： 人脸检测ai2d输入
# fd_ai2d_builder：       根据人脸检测ai2d参数，构建的人脸检测ai2d_builder对象
global fd_ai2d,fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
# fm_ai2d：              人脸mesh ai2d实例
# fm_ai2d_input_tensor： 人脸mesh ai2d输入
# fm_ai2d_output_tensor：人脸mesh ai2d输入
# fm_ai2d_builder：      根据人脸mesh ai2d参数，构建的人脸mesh ai2d_builder对象
global fm_ai2d,fm_ai2d_input_tensor,fm_ai2d_output_tensor,fm_ai2d_builder
global roi               #人脸区域
global vertices          #3D关键点

#读取anchor文件，为人脸检测后处理做准备
print('anchors_path:',anchors_path)
prior_data = np.fromfile(anchors_path, dtype=np.float)
prior_data = prior_data.reshape((anchor_len,det_dim))

def get_pad_one_side_param():
    # 右padding或下padding，获取padding参数
    dst_w = fd_kmodel_input_shape[3]                         # kmodel输入宽（w）
    dst_h = fd_kmodel_input_shape[2]                          # kmodel输入高（h）

    # OUT_RGB888P_WIDTH：原图宽（w）
    # OUT_RGB888P_HEIGH：原图高（h）
    # 计算最小的缩放比例，等比例缩放
    ratio_w = dst_w / OUT_RGB888P_WIDTH
    ratio_h = dst_h / OUT_RGB888P_HEIGH
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h
    # 计算经过缩放后的新宽和新高
    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGH)

    # 计算需要添加的padding，以使得kmodel输入的宽高和原图一致
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2
    # 四舍五入，确保padding是整数
    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

def fd_ai2d_init():
    # 人脸检测模型ai2d初始化
    with ScopedTiming("fd_ai2d_init",debug_mode > 0):
        # （1）创建人脸检测ai2d对象
        global fd_ai2d
        fd_ai2d = nn.ai2d()
        # （2）设置人脸检测ai2d参数
        fd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        fd_ai2d.set_pad_param(True, get_pad_one_side_param(), 0, rgb_mean)
        fd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        #（3）人脸检测ai2d_builder，根据人脸检测ai2d参数、输入输出大小创建ai2d_builder对象
        global fd_ai2d_builder
        fd_ai2d_builder = fd_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fd_kmodel_input_shape)

        #（4）创建人脸检测ai2d_output_tensor，用于保存人脸检测ai2d输出
        global fd_ai2d_output_tensor
        data = np.ones(fd_kmodel_input_shape, dtype=np.uint8)
        fd_ai2d_output_tensor = nn.from_numpy(data)

def fd_ai2d_run(rgb888p_img):
    # 根据人脸检测ai2d参数，对原图rgb888p_img进行预处理
    with ScopedTiming("fd_ai2d_run",debug_mode > 0):
        global fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
        # （1）根据原图构建ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        fd_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        # （2）运行人脸检测ai2d_builder，将结果保存到人脸检测ai2d_output_tensor中
        fd_ai2d_builder.run(fd_ai2d_input_tensor, fd_ai2d_output_tensor)

def fd_ai2d_release():
    # 释放人脸检测ai2d_input_tensor
    with ScopedTiming("fd_ai2d_release",debug_mode > 0):
        global fd_ai2d_input_tensor
        del fd_ai2d_input_tensor

def fd_kpu_init(kmodel_file):
    # 初始化人脸检测kpu对象，并加载kmodel
    with ScopedTiming("fd_kpu_init",debug_mode > 0):
        # 初始化人脸检测kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸检测kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸检测ai2d
        fd_ai2d_init()
        return kpu_obj

def fd_kpu_pre_process(rgb888p_img):
    # 设置人脸检测kpu输入
    # 使用人脸检测ai2d对原图进行预处理（padding，resize）
    fd_ai2d_run(rgb888p_img)
    with ScopedTiming("fd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fd_ai2d_output_tensor
        # 设置人脸检测kpu输入
        current_kmodel_obj.set_input_tensor(0, fd_ai2d_output_tensor)

def fd_kpu_get_output():
    # 获取人脸检测kpu输出
    with ScopedTiming("fd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取模型输出，并将结果转换为numpy，以便进行人脸检测后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

def fd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）原图预处理，并设置模型输入
    fd_kpu_pre_process(rgb888p_img)
    # （2）人脸检测kpu推理
    with ScopedTiming("fd kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸检测ai2d资源
    fd_ai2d_release()
    # （4）获取人俩检测kpu输出
    results = fd_kpu_get_output()
    # （5）人脸检测kpu结果后处理
    with ScopedTiming("fd kpu_post",debug_mode > 0):
        post_ret = aidemo.face_det_post_process(confidence_threshold,nms_threshold,fd_kmodel_input_shape[2],prior_data,
                [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH],results)
    # （6）返回人脸检测框
    if len(post_ret)==0:
        return post_ret
    else:
        return post_ret[0]          #0:det,1:landm,2:score

def fd_kpu_deinit():
    # kpu释放
    with ScopedTiming("fd_kpu_deinit",debug_mode > 0):
        if 'fd_ai2d' in globals():         #删除人脸检测ai2d变量，释放对它所引用对象的内存引用
            global fd_ai2d
            del fd_ai2d
        if 'fd_ai2d_output_tensor' in globals():  #删除人脸检测ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global fd_ai2d_output_tensor
            del fd_ai2d_output_tensor

###############for face recognition###############
def parse_roi_box_from_bbox(bbox):
    # 获取人脸roi
    x1, y1, w, h = map(lambda x: int(round(x, 0)), bbox[:4])
    old_size = (w + h) / 2
    center_x = x1 + w / 2
    center_y = y1 + h / 2 + old_size * 0.14
    size = int(old_size * 1.58)

    x0 = center_x - float(size) / 2
    y0 = center_y - float(size) / 2
    x1 = x0 + size
    y1 = y0 + size

    x0 = max(0, min(x0, OUT_RGB888P_WIDTH))
    y0 = max(0, min(y0, OUT_RGB888P_HEIGH))
    x1 = max(0, min(x1, OUT_RGB888P_WIDTH))
    y1 = max(0, min(y1, OUT_RGB888P_HEIGH))

    roi = (x0, y0, x1 - x0, y1 - y0)
    return roi

def fm_ai2d_init():
    # 人脸mesh ai2d初始化
    with ScopedTiming("fm_ai2d_init",debug_mode > 0):
        # （1）创建人脸mesh ai2d对象
        global fm_ai2d
        fm_ai2d = nn.ai2d()

        # （2）创建人脸mesh ai2d_output_tensor对象，用于存放ai2d输出
        global fm_ai2d_output_tensor
        data = np.ones(fm_kmodel_input_shape, dtype=np.uint8)
        fm_ai2d_output_tensor = nn.from_numpy(data)

def fm_ai2d_run(rgb888p_img,det):
    # 人脸mesh ai2d推理
    with ScopedTiming("fm_ai2d_run",debug_mode > 0):
        global fm_ai2d,fm_ai2d_input_tensor,fm_ai2d_output_tensor
        #（1）根据原图ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        fm_ai2d_input_tensor = nn.from_numpy(ai2d_input)

        # （2）根据新的det设置新的人脸mesh ai2d参数
        fm_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        global roi
        roi = parse_roi_box_from_bbox(det)
        fm_ai2d.set_crop_param(True,int(roi[0]),int(roi[1]),int(roi[2]),int(roi[3]))
        fm_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
        # （3）根据新的人脸mesh ai2d参数，构建人脸mesh ai2d_builder
        global fm_ai2d_builder
        fm_ai2d_builder = fm_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fm_kmodel_input_shape)
        # （4）推理人脸mesh ai2d，将预处理的结果保存到fm_ai2d_output_tensor
        fm_ai2d_builder.run(fm_ai2d_input_tensor, fm_ai2d_output_tensor)

def fm_ai2d_release():
    # 释放人脸mesh ai2d_input_tensor、ai2d_builder
    with ScopedTiming("fm_ai2d_release",debug_mode > 0):
        global fm_ai2d_input_tensor,fm_ai2d_builder
        del fm_ai2d_input_tensor
        del fm_ai2d_builder

def fm_kpu_init(kmodel_file):
    # 人脸mesh kpu初始化
    with ScopedTiming("fm_kpu_init",debug_mode > 0):
        # 初始化人脸mesh kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸mesh kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸mesh ai2d
        fm_ai2d_init()
        return kpu_obj

def fm_kpu_pre_process(rgb888p_img,det):
    # 人脸mesh kpu预处理
    # 人脸mesh ai2d推理，根据det对原图进行预处理
    fm_ai2d_run(rgb888p_img,det)
    with ScopedTiming("fm_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fm_ai2d_output_tensor
        # 将人脸mesh ai2d输出设置为人脸mesh kpu输入
        current_kmodel_obj.set_input_tensor(0, fm_ai2d_output_tensor)

def fm_kpu_get_output():
    with ScopedTiming("fm_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取人脸mesh kpu输出
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        del data
        return result

def fm_kpu_post_process(param):
    # 人脸mesh kpu结果后处理，反标准化
    with ScopedTiming("fm_kpu_post_process",debug_mode > 0):
        param = param * param_std + param_mean
    return param

def fm_kpu_run(kpu_obj,rgb888p_img,det):
    # 人脸mesh kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）人脸mesh kpu预处理，设置kpu输入
    fm_kpu_pre_process(rgb888p_img,det)
    # （2）人脸mesh kpu推理
    with ScopedTiming("fm_kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸mesh ai2d
    fm_ai2d_release()
    # （4）获取人脸mesh kpu输出
    param = fm_kpu_get_output()
    # （5）人脸mesh 后处理
    param = fm_kpu_post_process(param)
    return param

def fm_kpu_deinit():
    # 人脸mesh kpu释放
    with ScopedTiming("fm_kpu_deinit",debug_mode > 0):
        if 'fm_ai2d' in globals():         # 删除fm_ai2d变量，释放对它所引用对象的内存引用
            global fm_ai2d
            del fm_ai2d
        if 'fm_ai2d_output_tensor' in globals():  # 删除fm_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global fm_ai2d_output_tensor
            del fm_ai2d_output_tensor

def fmpost_kpu_init(kmodel_file):
    # face mesh post模型初始化
    with ScopedTiming("fmpost_kpu_init",debug_mode > 0):
        # 初始化人脸mesh kpu post对象
        kpu_obj = nn.kpu()
        # 加载人脸mesh后处理kmodel
        kpu_obj.load_kmodel(kmodel_file)
        return kpu_obj

def fmpost_kpu_pre_process(param):
    # face mesh post模型预处理，param解析
    with ScopedTiming("fmpost_kpu_pre_process",debug_mode > 0):
        param = param[0]
        trans_dim, shape_dim, exp_dim = 12, 40, 10

        # reshape前务必进行copy，否则会导致模型输入错误
        R_ = param[:trans_dim].copy().reshape((3, -1))
        R = R_[:, :3].copy()
        offset = R_[:, 3].copy()
        offset = offset.reshape((3, 1))
        alpha_shp = param[trans_dim:trans_dim + shape_dim].copy().reshape((-1, 1))
        alpha_exp = param[trans_dim + shape_dim:].copy().reshape((-1, 1))

        R_tensor = nn.from_numpy(R)
        current_kmodel_obj.set_input_tensor(0, R_tensor)
        del R_tensor

        offset_tensor = nn.from_numpy(offset)
        current_kmodel_obj.set_input_tensor(1, offset_tensor)
        del offset_tensor

        alpha_shp_tensor = nn.from_numpy(alpha_shp)
        current_kmodel_obj.set_input_tensor(2, alpha_shp_tensor)
        del alpha_shp_tensor

        alpha_exp_tensor = nn.from_numpy(alpha_exp)
        current_kmodel_obj.set_input_tensor(3, alpha_exp_tensor)
        del alpha_exp_tensor

    return

def fmpost_kpu_get_output():
    # 获取face mesh post模型输出
    with ScopedTiming("fmpost_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取人脸mesh kpu输出
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        del data
        return result

def fmpost_kpu_post_process(roi):
    # face mesh post模型推理结果后处理
    with ScopedTiming("fmpost_kpu_post_process",debug_mode > 0):
        x, y, w, h = map(lambda x: int(round(x, 0)), roi[:4])
        x = x * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
        y = y * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
        w = w * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
        h = h * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
        roi_array = np.array([x,y,w,h],dtype=np.float)
        global vertices
        aidemo.face_mesh_post_process(roi_array,vertices)
    return

def fmpost_kpu_run(kpu_obj,param):
    # face mesh post模型推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    fmpost_kpu_pre_process(param)
    with ScopedTiming("fmpost_kpu_run",debug_mode > 0):
        kpu_obj.run()
    global vertices
    vertices = fmpost_kpu_get_output()
    global roi
    fmpost_kpu_post_process(roi)
    return
#********************for media_utils.py********************
global draw_img_ulab,draw_img,osd_img                       #for display
global buffer,media_source,media_sink                       #for media

# for display，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.2
def display_init():
    # 设置使用hdmi进行显示
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

def display_deinit():
    # 释放显示资源
    display.deinit()

def display_draw(dets,vertices_list):
    # 在显示器画人脸轮廓
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img_ulab,draw_img,osd_img
        if dets:
            draw_img.clear()
            for vertices in vertices_list:
                aidemo.face_draw_mesh(draw_img_ulab, vertices)
            # （4）将轮廓结果拷贝到osd
            draw_img.copy_to(osd_img)
            # （5）将osd显示到屏幕
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            # （1）清空用来画框的图像
            draw_img.clear()
            # （2）清空osd
            draw_img.copy_to(osd_img)
            # （3）显示透明图层
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.1
def camera_init(dev_id):
    # camera初始化
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

def camera_start(dev_id):
    # camera启动
    camera.start_stream(dev_id)

def camera_read(dev_id):
    # 读取一帧图像
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

def camera_release_image(dev_id,rgb888p_img):
    # 释放一帧图像
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

def camera_stop(dev_id):
    # 停止camera
    camera.stop_stream(dev_id)

#for media，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.3
def media_init():
    # meida初始化
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img_ulab,draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 用于画框
    draw_img_ulab = np.zeros((DISPLAY_HEIGHT,DISPLAY_WIDTH,4),dtype=np.uint8)
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, alloc=image.ALLOC_REF,data = draw_img_ulab)
    # 用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

def media_deinit():
    # meida资源释放
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#********************for face_detect.py********************
def face_mesh_inference():
    # 人脸检测kpu初始化
    kpu_face_detect = fd_kpu_init(fd_kmodel_file)
    # 人脸mesh kpu初始化
    kpu_face_mesh = fm_kpu_init(fm_kmodel_file)
    # face_mesh_post kpu初始化
    kpu_face_mesh_post = fmpost_kpu_init(fmpost_kmodel_file)
    # camera初始化
    camera_init(CAM_DEV_ID_0)
    # 显示初始化
    display_init()

    # 注意：将一定要将一下过程包在try中，用于保证程序停止后，资源释放完毕；确保下次程序仍能正常运行
    try:
        # 注意：媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）
        media_init()
        # 启动camera
        camera_start(CAM_DEV_ID_0)
        gc_count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                # （1）读取一帧图像
                rgb888p_img = camera_read(CAM_DEV_ID_0)
                # （2）若读取成功，推理当前帧
                if rgb888p_img.format() == image.RGBP888:
                    # （2.1）推理当前图像，并获取人脸检测结果
                    dets = fd_kpu_run(kpu_face_detect,rgb888p_img)
                    ## （2.2）针对每个人脸框，推理得到对应人脸mesh
                    mesh_result = []
                    for det in dets:
                        param = fm_kpu_run(kpu_face_mesh,rgb888p_img,det)
                        fmpost_kpu_run(kpu_face_mesh_post,param)
                        global vertices
                        mesh_result.append(vertices)
                    ## （2.3）将人脸mesh 画到屏幕上
                    display_draw(dets,mesh_result)

                # （3）释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)
                if gc_count > 5:
                    gc.collect()
                    gc_count = 0
                else:
                    gc_count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        # 停止camera
        camera_stop(CAM_DEV_ID_0)
        # 释放显示资源
        display_deinit()
        # 释放kpu资源
        fd_kpu_deinit()
        fm_kpu_deinit()
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_face_detect
        del kpu_face_mesh
        del kpu_face_mesh_post
        if 'draw_img' in globals():
            global draw_img
            del draw_img
        if 'draw_img_ulab' in globals():
            global draw_img_ulab
            del draw_img_ulab
        # 垃圾回收
        gc.collect()
        nn.shrink_memory_pool()
        # 释放媒体资源
        media_deinit()

    print("face_mesh_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    face_mesh_inference()
```

### 11.注视估计

```python
import ulab.numpy as np                  # 类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn              # nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *               # 摄像头模块
from media.display import *              # 显示模块
from media.media import *                # 软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import aidemo                            # aidemo模块，封装ai demo相关后处理、画图操作
import image                             # 图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                              # 时间统计
import gc                                # 垃圾回收模块
import os,sys                            # 操作系统接口模块
import math                              # 数学模块


#********************for config.py********************
# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)                   # 显示宽度要求16位对齐
DISPLAY_HEIGHT = 1080

# ai原图分辨率，sensor默认出图为16:9，若需不形变原图，最好按照16:9比例设置宽高
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)               # ai原图宽度要求16位对齐
OUT_RGB888P_HEIGH = 1080

# kmodel参数设置
# 人脸检测kmodel输入shape
fd_kmodel_input_shape = (1,3,320,320)
# 注视估计kmodel输入shape
feg_kmodel_input_shape = (1,3,448,448)
# ai原图padding
rgb_mean = [104,117,123]

#人脸检测kmodel其它参数设置
confidence_threshold = 0.5               # 人脸检测阈值
top_k = 5000
nms_threshold = 0.2
keep_top_k = 750
vis_thres = 0.5
variance = [0.1, 0.2]
anchor_len = 4200
score_dim = 2
det_dim = 4
keypoint_dim = 10

# 文件配置
# 人脸检测kmodel
root_dir = '/sdcard/app/tests/'
fd_kmodel_file = root_dir + 'kmodel/face_detection_320.kmodel'
# 注视估计kmodel
fr_kmodel_file = root_dir + 'kmodel/eye_gaze.kmodel'
# anchor文件
anchors_path = root_dir + 'utils/prior_data_320.bin'
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0

#********************for scoped_timing.py********************
# 时间统计类
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#********************for ai_utils.py********************
global current_kmodel_obj #当前kpu对象
# fd_ai2d：               人脸检测ai2d实例
# fd_ai2d_input_tensor：  人脸检测ai2d输入
# fd_ai2d_output_tensor： 人脸检测ai2d输入
# fd_ai2d_builder：       根据人脸检测ai2d参数，构建的人脸检测ai2d_builder对象
global fd_ai2d,fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
# feg_ai2d：              注视估计ai2d实例
# feg_ai2d_input_tensor： 注视估计ai2d输入
# feg_ai2d_output_tensor：注视估计ai2d输入
# feg_ai2d_builder：      根据注视估计ai2d参数，构建的注视估计ai2d_builder对象
global feg_ai2d,feg_ai2d_input_tensor,feg_ai2d_output_tensor,feg_ai2d_builder
global matrix_dst         #人脸仿射变换矩阵

#读取anchor文件，为人脸检测后处理做准备
print('anchors_path:',anchors_path)
prior_data = np.fromfile(anchors_path, dtype=np.float)
prior_data = prior_data.reshape((anchor_len,det_dim))

def get_pad_one_side_param():
    # 右padding或下padding，获取padding参数
    dst_w = fd_kmodel_input_shape[3]                         # kmodel输入宽（w）
    dst_h = fd_kmodel_input_shape[2]                          # kmodel输入高（h）

    # OUT_RGB888P_WIDTH：原图宽（w）
    # OUT_RGB888P_HEIGH：原图高（h）
    # 计算最小的缩放比例，等比例缩放
    ratio_w = dst_w / OUT_RGB888P_WIDTH
    ratio_h = dst_h / OUT_RGB888P_HEIGH
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h
    # 计算经过缩放后的新宽和新高
    new_w = (int)(ratio * OUT_RGB888P_WIDTH)
    new_h = (int)(ratio * OUT_RGB888P_HEIGH)

    # 计算需要添加的padding，以使得kmodel输入的宽高和原图一致
    dw = (dst_w - new_w) / 2
    dh = (dst_h - new_h) / 2
    # 四舍五入，确保padding是整数
    top = (int)(round(0))
    bottom = (int)(round(dh * 2 + 0.1))
    left = (int)(round(0))
    right = (int)(round(dw * 2 - 0.1))
    return [0, 0, 0, 0, top, bottom, left, right]

def fd_ai2d_init():
    # 人脸检测模型ai2d初始化
    with ScopedTiming("fd_ai2d_init",debug_mode > 0):
        # （1）创建人脸检测ai2d对象
        global fd_ai2d
        fd_ai2d = nn.ai2d()
        # （2）设置人脸检测ai2d参数
        fd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        fd_ai2d.set_pad_param(True, get_pad_one_side_param(), 0, rgb_mean)
        fd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        #（3）人脸检测ai2d_builder，根据人脸检测ai2d参数、输入输出大小创建ai2d_builder对象
        global fd_ai2d_builder
        fd_ai2d_builder = fd_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], fd_kmodel_input_shape)

        #（4）创建人脸检测ai2d_output_tensor，用于保存人脸检测ai2d输出
        global fd_ai2d_output_tensor
        data = np.ones(fd_kmodel_input_shape, dtype=np.uint8)
        fd_ai2d_output_tensor = nn.from_numpy(data)

def fd_ai2d_run(rgb888p_img):
    # 根据人脸检测ai2d参数，对原图rgb888p_img进行预处理
    with ScopedTiming("fd_ai2d_run",debug_mode > 0):
        global fd_ai2d_input_tensor,fd_ai2d_output_tensor,fd_ai2d_builder
        # （1）根据原图构建ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        fd_ai2d_input_tensor = nn.from_numpy(ai2d_input)
        # （2）运行人脸检测ai2d_builder，将结果保存到人脸检测ai2d_output_tensor中
        fd_ai2d_builder.run(fd_ai2d_input_tensor, fd_ai2d_output_tensor)

def fd_ai2d_release():
    # 释放人脸检测ai2d_input_tensor
    with ScopedTiming("fd_ai2d_release",debug_mode > 0):
        global fd_ai2d_input_tensor
        del fd_ai2d_input_tensor


def fd_kpu_init(kmodel_file):
    # 初始化人脸检测kpu对象，并加载kmodel
    with ScopedTiming("fd_kpu_init",debug_mode > 0):
        # 初始化人脸检测kpu对象
        kpu_obj = nn.kpu()
        # 加载人脸检测kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化人脸检测ai2d
        fd_ai2d_init()
        return kpu_obj

def fd_kpu_pre_process(rgb888p_img):
    # 设置人脸检测kpu输入
    # 使用人脸检测ai2d对原图进行预处理（padding，resize）
    fd_ai2d_run(rgb888p_img)
    with ScopedTiming("fd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,fd_ai2d_output_tensor
        # 设置人脸检测kpu输入
        current_kmodel_obj.set_input_tensor(0, fd_ai2d_output_tensor)

def fd_kpu_get_output():
    # 获取人脸检测kpu输出
    with ScopedTiming("fd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取模型输出，并将结果转换为numpy，以便进行人脸检测后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

def fd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）原图预处理，并设置模型输入
    fd_kpu_pre_process(rgb888p_img)
    # （2）人脸检测kpu推理
    with ScopedTiming("fd kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放人脸检测ai2d资源
    fd_ai2d_release()
    # （4）获取人俩检测kpu输出
    results = fd_kpu_get_output()
    # （5）人脸检测kpu结果后处理
    with ScopedTiming("fd kpu_post",debug_mode > 0):
        post_ret = aidemo.face_det_post_process(confidence_threshold,nms_threshold,fd_kmodel_input_shape[2],prior_data,
                [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGH],results)
    # （6）返回人脸检测框
    if len(post_ret)==0:
        return post_ret
    else:
        return post_ret[0]          #0:det,1:landm,2:score

def fd_kpu_deinit():
    # kpu释放
    with ScopedTiming("fd_kpu_deinit",debug_mode > 0):
        if 'fd_ai2d' in globals():               #删除人脸检测ai2d变量，释放对它所引用对象的内存引用
            global fd_ai2d
            del fd_ai2d
        if 'fd_ai2d_output_tensor' in globals(): #删除人脸检测ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global fd_ai2d_output_tensor
            del fd_ai2d_output_tensor

###############for face recognition###############
def feg_ai2d_init():
    # 注视估计ai2d初始化
    with ScopedTiming("feg_ai2d_init",debug_mode > 0):
        # （1）创建注视估计ai2d对象
        global feg_ai2d
        feg_ai2d = nn.ai2d()

        # （2）创建注视估计ai2d_output_tensor对象，用于存放ai2d输出
        global feg_ai2d_output_tensor
        data = np.ones(feg_kmodel_input_shape, dtype=np.uint8)
        feg_ai2d_output_tensor = nn.from_numpy(data)

def feg_ai2d_run(rgb888p_img,det):
    # 注视估计ai2d推理
    with ScopedTiming("feg_ai2d_run",debug_mode > 0):
        global feg_ai2d,feg_ai2d_input_tensor,feg_ai2d_output_tensor
        #（1）根据原图ai2d_input_tensor对象
        ai2d_input = rgb888p_img.to_numpy_ref()
        feg_ai2d_input_tensor = nn.from_numpy(ai2d_input)

        # （2）根据新的det设置新的注视估计ai2d参数
        feg_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)

        x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
        feg_ai2d.set_crop_param(True,x,y,w,h)
        feg_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        # （3）根据新的注视估计ai2d参数，构建注视估计ai2d_builder
        global feg_ai2d_builder
        feg_ai2d_builder = feg_ai2d.build([1,3,OUT_RGB888P_HEIGH,OUT_RGB888P_WIDTH], feg_kmodel_input_shape)
        # （4）推理注视估计ai2d，将预处理的结果保存到feg_ai2d_output_tensor
        feg_ai2d_builder.run(feg_ai2d_input_tensor, feg_ai2d_output_tensor)

def feg_ai2d_release():
    # 释放注视估计ai2d_input_tensor、ai2d_builder
    with ScopedTiming("feg_ai2d_release",debug_mode > 0):
        global feg_ai2d_input_tensor,feg_ai2d_builder
        del feg_ai2d_input_tensor
        del feg_ai2d_builder

def feg_kpu_init(kmodel_file):
    # 注视估计kpu初始化
    with ScopedTiming("feg_kpu_init",debug_mode > 0):
        # 初始化注视估计kpu对象
        kpu_obj = nn.kpu()
        # 加载注视估计kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化注视估计ai2d
        feg_ai2d_init()
        return kpu_obj

def feg_kpu_pre_process(rgb888p_img,det):
    # 注视估计kpu预处理
    # 注视估计ai2d推理，根据det对原图进行预处理
    feg_ai2d_run(rgb888p_img,det)
    with ScopedTiming("feg_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,feg_ai2d_output_tensor
        # 将注视估计ai2d输出设置为注视估计kpu输入
        current_kmodel_obj.set_input_tensor(0, feg_ai2d_output_tensor)

def feg_kpu_get_output():
    with ScopedTiming("feg_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取注视估计kpu输出
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

def feg_kpu_post_process(results):
    # 注视估计kpu推理结果后处理
    with ScopedTiming("feg_kpu_post_process",debug_mode > 0):
        post_ret = aidemo.eye_gaze_post_process(results)
    return post_ret[0],post_ret[1]

def feg_kpu_run(kpu_obj,rgb888p_img,det):
    # 注视估计kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）注视估计kpu预处理，设置kpu输入
    feg_kpu_pre_process(rgb888p_img,det)
    # （2）注视估计kpu推理
    with ScopedTiming("feg_kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放注视估计ai2d
    feg_ai2d_release()
    # （4）获取注视估计kpu输出
    results = feg_kpu_get_output()
    # （5）注视估计后处理
    pitch,yaw = feg_kpu_post_process(results)
    return pitch,yaw

def feg_kpu_deinit():
    # 注视估计kpu释放
    with ScopedTiming("feg_kpu_deinit",debug_mode > 0):
        if 'feg_ai2d' in globals():                # 删除feg_ai2d变量，释放对它所引用对象的内存引用
            global feg_ai2d
            del feg_ai2d
        if 'feg_ai2d_output_tensor' in globals():  # 删除feg_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global feg_ai2d_output_tensor
            del feg_ai2d_output_tensor

#********************for media_utils.py********************
global draw_img,osd_img                       #for display
global buffer,media_source,media_sink                       #for media

# for display，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.2
def display_init():
    # 设置使用hdmi进行显示
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

def display_deinit():
    # 释放显示资源
    display.deinit()

def display_draw(dets,gaze_results):
    # 在显示器画人脸轮廓
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img
        if dets:
            draw_img.clear()
            for det,gaze_ret in zip(dets,gaze_results):
                pitch , yaw = gaze_ret
                length = DISPLAY_WIDTH / 2
                x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                x = x * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                y = y * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
                w = w * DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                h = h * DISPLAY_HEIGHT // OUT_RGB888P_HEIGH
                center_x = (x + w / 2.0)
                center_y = (y + h / 2.0)
                dx = -length * math.sin(pitch) * math.cos(yaw)
                target_x = int(center_x + dx)
                dy = -length * math.sin(yaw)
                target_y = int(center_y + dy)

                draw_img.draw_arrow(int(center_x), int(center_y), target_x, target_y, color = (255,255,0,0), size = 30, thickness = 2)

            # （4）将轮廓结果拷贝到osd
            draw_img.copy_to(osd_img)
            # （5）将osd显示到屏幕
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
        else:
            # （1）清空用来画框的图像
            draw_img.clear()
            # （2）清空osd
            draw_img.copy_to(osd_img)
            # （3）显示透明图层
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

#for camera，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.1
def camera_init(dev_id):
    # camera初始化
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGH)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

def camera_start(dev_id):
    # camera启动
    camera.start_stream(dev_id)

def camera_read(dev_id):
    # 读取一帧图像
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

def camera_release_image(dev_id,rgb888p_img):
    # 释放一帧图像
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

def camera_stop(dev_id):
    # 停止camera
    camera.stop_stream(dev_id)

#for media，已经封装好，无需自己再实现，直接调用即可，详细解析请查看1.6.3
def media_init():
    # meida初始化
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer,draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

def media_deinit():
    # meida资源释放
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#********************for face_detect.py********************
def eye_gaze_inference():
    print("eye_gaze_test start")
    # 人脸检测kpu初始化
    kpu_face_detect = fd_kpu_init(fd_kmodel_file)
    # 注视估计kpu初始化
    kpu_eye_gaze = feg_kpu_init(fr_kmodel_file)
    # camera初始化
    camera_init(CAM_DEV_ID_0)
    # 显示初始化
    display_init()

    # 注意：将一定要将一下过程包在try中，用于保证程序停止后，资源释放完毕；确保下次程序仍能正常运行
    try:
        # 注意：媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）
        media_init()

        # 启动camera
        camera_start(CAM_DEV_ID_0)
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                # （1）读取一帧图像
                rgb888p_img = camera_read(CAM_DEV_ID_0)
                # （2）若读取成功，推理当前帧
                if rgb888p_img.format() == image.RGBP888:
                    # （2.1）推理当前图像，并获取人脸检测结果
                    dets = fd_kpu_run(kpu_face_detect,rgb888p_img)
                    # （2.2）针对每个人脸框，推理得到对应注视估计
                    gaze_results = []
                    for det in dets:
                        pitch ,yaw = feg_kpu_run(kpu_eye_gaze,rgb888p_img,det)
                        gaze_results.append([pitch ,yaw])
                    # （2.3）将注视估计画到屏幕上
                    display_draw(dets,gaze_results)

                # （3）释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)
                with ScopedTiming("gc collect", debug_mode > 0):
                    gc.collect()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        # 停止camera
        camera_stop(CAM_DEV_ID_0)
        # 释放显示资源
        display_deinit()
        # 释放kpu资源
        fd_kpu_deinit()
        feg_kpu_deinit()
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_face_detect
        del kpu_eye_gaze
        # 垃圾回收
        gc.collect()
        nn.shrink_memory_pool()
        # 释放媒体资源
        media_deinit()

    print("eye_gaze_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    eye_gaze_inference()
```

### 12.动态手势识别

```python
import aicube                   #aicube模块，封装检测分割等任务相关后处理
from media.camera import *      #摄像头模块
from media.display import *     #显示模块
from media.media import *       #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区

import nncase_runtime as nn     #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np         #类似python numpy操作，但也会有一些接口不同

import time                     #时间统计
import image                    #图像模块，主要用于读取、图像绘制元素（框、点等）等操作

import gc                       #垃圾回收模块
import os, sys                  #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

##ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

root_dir = '/sdcard/app/tests/'

#--------for hand detection----------
#kmodel输入shape
hd_kmodel_input_shape = (1,3,512,512)                               # 手掌检测kmodel输入分辨率

#kmodel相关参数设置
confidence_threshold = 0.2                                          # 手掌检测阈值，用于过滤roi
nms_threshold = 0.5                                                 # 手掌检测框阈值，用于过滤重复roi
hd_kmodel_frame_size = [512,512]                                    # 手掌检测输入图片尺寸
hd_frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGHT]              # 手掌检测直接输入图片尺寸
strides = [8,16,32]                                                 # 输出特征图的尺寸与输入图片尺寸的比
num_classes = 1                                                     # 手掌检测模型输出类别数
nms_option = False                                                  # 是否所有检测框一起做NMS，False则按照不同的类分别应用NMS

hd_kmodel_file = root_dir + 'kmodel/hand_det.kmodel'                # 手掌检测kmodel文件的路径
anchors = [26,27, 53,52, 75,71, 80,99, 106,82, 99,134, 140,113, 161,172, 245,276]   #anchor设置

#--------for hand keypoint detection----------
#kmodel输入shape
hk_kmodel_input_shape = (1,3,256,256)                               # 手掌关键点检测kmodel输入分辨率

#kmodel相关参数设置
hk_kmodel_frame_size = [256,256]                                    # 手掌关键点检测输入图片尺寸
hk_kmodel_file = root_dir + 'kmodel/handkp_det.kmodel'              # 手掌关键点检测kmodel文件的路径

#--------for hand gesture----------
#kmodel输入shape
gesture_kmodel_input_shape = [[1, 3, 224, 224],                     # 动态手势识别kmodel输入分辨率
                            [1,3,56,56],
                            [1,4,28,28],
                            [1,4,28,28],
                            [1,8,14,14],
                            [1,8,14,14],
                            [1,8,14,14],
                            [1,12,14,14],
                            [1,12,14,14],
                            [1,20,7,7],
                            [1,20,7,7]]

#kmodel相关参数设置
resize_shape = 256
mean_values = np.array([0.485, 0.456, 0.406]).reshape((3,1,1))      # 动态手势识别预处理均值
std_values = np.array([0.229, 0.224, 0.225]).reshape((3,1,1))       # 动态手势识别预处理方差
gesture_kmodel_frame_size = [224,224]                               # 动态手势识别输入图片尺寸

gesture_kmodel_file = root_dir + 'kmodel/gesture.kmodel'            # 动态手势识别kmodel文件的路径

shang_bin = root_dir + "utils/shang.bin"                            # 动态手势识别屏幕坐上角标志状态文件的路径
xia_bin = root_dir + "utils/xia.bin"                                # 动态手势识别屏幕坐上角标志状态文件的路径
zuo_bin = root_dir + "utils/zuo.bin"                                # 动态手势识别屏幕坐上角标志状态文件的路径
you_bin = root_dir + "utils/you.bin"                                # 动态手势识别屏幕坐上角标志状态文件的路径

bin_width = 150                                                     # 动态手势识别屏幕坐上角标志状态文件的短边尺寸
bin_height = 216                                                    # 动态手势识别屏幕坐上角标志状态文件的长边尺寸
shang_argb = np.fromfile(shang_bin, dtype=np.uint8)
shang_argb = shang_argb.reshape((bin_height, bin_width, 4))
xia_argb = np.fromfile(xia_bin, dtype=np.uint8)
xia_argb = xia_argb.reshape((bin_height, bin_width, 4))
zuo_argb = np.fromfile(zuo_bin, dtype=np.uint8)
zuo_argb = zuo_argb.reshape((bin_width, bin_height, 4))
you_argb = np.fromfile(you_bin, dtype=np.uint8)
you_argb = you_argb.reshape((bin_width, bin_height, 4))

TRIGGER = 0                                                         # 动态手势识别应用的结果状态
MIDDLE = 1
UP = 2
DOWN = 3
LEFT = 4
RIGHT = 5

max_hist_len = 20                                                   # 最多存储多少帧的结果

debug_mode = 0                                                      # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                                                                                     # 定义全局的 kpu 对象
global hd_ai2d,hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder                                                     # 定义手掌检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor,hk_ai2d_builder                                                     # 定义手掌关键点检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global gesture_ai2d_resize, gesture_ai2d_resize_builder, gesture_ai2d_crop, gesture_ai2d_crop_builder                         # 定义动态手势识别全局 ai2d 对象，以及 builder
global gesture_ai2d_input_tensor, gesture_kpu_input_tensors, gesture_ai2d_middle_output_tensor, gesture_ai2d_output_tensor    # 定义动态手势识别全局 ai2d 的输入、输出

#-------hand detect--------:
# 手掌检测ai2d 初始化
def hd_ai2d_init():
    with ScopedTiming("hd_ai2d_init",debug_mode > 0):
        global hd_ai2d
        global hd_ai2d_builder
        global hd_ai2d_output_tensor
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = hd_kmodel_frame_size[0]
        height = hd_kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        hd_ai2d = nn.ai2d()
        hd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        hd_ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        hd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        hd_ai2d_builder = hd_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,height,width])

        data = np.ones(hd_kmodel_input_shape, dtype=np.uint8)
        hd_ai2d_output_tensor = nn.from_numpy(data)

# 手掌检测 ai2d 运行
def hd_ai2d_run(rgb888p_img):
    with ScopedTiming("hd_ai2d_run",debug_mode > 0):
        global hd_ai2d_input_tensor,hd_ai2d_output_tensor, hd_ai2d_builder
        hd_ai2d_input = rgb888p_img.to_numpy_ref()
        hd_ai2d_input_tensor = nn.from_numpy(hd_ai2d_input)

        hd_ai2d_builder.run(hd_ai2d_input_tensor, hd_ai2d_output_tensor)

# 手掌检测 ai2d 释放内存
def hd_ai2d_release():
    with ScopedTiming("hd_ai2d_release",debug_mode > 0):
        global hd_ai2d_input_tensor
        del hd_ai2d_input_tensor

# 手掌检测 kpu 初始化
def hd_kpu_init(hd_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hd_kpu_init",debug_mode > 0):
        hd_kpu_obj = nn.kpu()
        hd_kpu_obj.load_kmodel(hd_kmodel_file)

        hd_ai2d_init()
        return hd_kpu_obj

# 手掌检测 kpu 输入预处理
def hd_kpu_pre_process(rgb888p_img):
    hd_ai2d_run(rgb888p_img)
    with ScopedTiming("hd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hd_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hd_ai2d_output_tensor)

# 手掌检测 kpu 获得 kmodel 输出
def hd_kpu_get_output():
    with ScopedTiming("hd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌检测 kpu 运行
def hd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hd_kpu_pre_process(rgb888p_img)
    # (2)手掌检测 kpu 运行
    with ScopedTiming("hd_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌检测 ai2d 资源
    hd_ai2d_release()
    # (4)获取手掌检测 kpu 输出
    results = hd_kpu_get_output()
    # (5)手掌检测 kpu 结果后处理
    dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], hd_kmodel_frame_size, hd_frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)  # kpu结果后处理
    # (6)返回手掌检测结果
    return dets

# 手掌检测 kpu 释放内存
def hd_kpu_deinit():
    with ScopedTiming("hd_kpu_deinit",debug_mode > 0):
        if 'hd_ai2d' in globals():                             #删除hd_ai2d变量，释放对它所引用对象的内存引用
            global hd_ai2d
            del hd_ai2d
        if 'hd_ai2d_output_tensor' in globals():               #删除hd_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global hd_ai2d_output_tensor
            del hd_ai2d_output_tensor
        if 'hd_ai2d_builder' in globals():                     #删除hd_ai2d_builder变量，释放对它所引用对象的内存引用
            global hd_ai2d_builder
            del hd_ai2d_builder


#-------hand keypoint detection------:
# 手掌关键点检测 ai2d 初始化
def hk_ai2d_init():
    with ScopedTiming("hk_ai2d_init",debug_mode > 0):
        global hk_ai2d, hk_ai2d_output_tensor
        hk_ai2d = nn.ai2d()
        hk_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        data = np.ones(hk_kmodel_input_shape, dtype=np.uint8)
        hk_ai2d_output_tensor = nn.from_numpy(data)

# 手掌关键点检测 ai2d 运行
def hk_ai2d_run(rgb888p_img, x, y, w, h):
    with ScopedTiming("hk_ai2d_run",debug_mode > 0):
        global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor
        hk_ai2d_input = rgb888p_img.to_numpy_ref()
        hk_ai2d_input_tensor = nn.from_numpy(hk_ai2d_input)

        hk_ai2d.set_crop_param(True, x, y, w, h)
        hk_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )

        global hk_ai2d_builder
        hk_ai2d_builder = hk_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,hk_kmodel_frame_size[1],hk_kmodel_frame_size[0]])
        hk_ai2d_builder.run(hk_ai2d_input_tensor, hk_ai2d_output_tensor)

# 手掌关键点检测 ai2d 释放内存
def hk_ai2d_release():
    with ScopedTiming("hk_ai2d_release",debug_mode > 0):
        global hk_ai2d_input_tensor, hk_ai2d_builder
        del hk_ai2d_input_tensor
        del hk_ai2d_builder

# 手掌关键点检测 kpu 初始化
def hk_kpu_init(hk_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hk_kpu_init",debug_mode > 0):
        hk_kpu_obj = nn.kpu()
        hk_kpu_obj.load_kmodel(hk_kmodel_file)

        hk_ai2d_init()
        return hk_kpu_obj

# 手掌关键点检测 kpu 输入预处理
def hk_kpu_pre_process(rgb888p_img, x, y, w, h):
    hk_ai2d_run(rgb888p_img, x, y, w, h)
    with ScopedTiming("hk_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hk_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hk_ai2d_output_tensor)

# 手掌关键点检测 kpu 获得 kmodel 输出
def hk_kpu_get_output():
    with ScopedTiming("hk_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌关键点检测 kpu 输出后处理
def hk_kpu_post_process(results, x, y, w, h):
    results_show = np.zeros(results.shape,dtype=np.int16)
    results_show[0::2] = results[0::2] * w + x
    results_show[1::2] = results[1::2] * h + y
    return results_show

# 手掌关键点检测 kpu 运行
def hk_kpu_run(kpu_obj,rgb888p_img, x, y, w, h):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hk_kpu_pre_process(rgb888p_img, x, y, w, h)
    # (2)手掌关键点检测 kpu 运行
    with ScopedTiming("hk_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌关键点检测 ai2d 资源
    hk_ai2d_release()
    # (4)获取手掌关键点检测 kpu 输出
    results = hk_kpu_get_output()
    # (5)手掌关键点检测 kpu 结果后处理
    result = hk_kpu_post_process(results[0],x,y,w,h)
    # (6)返回手掌关键点检测结果
    return result

# 手掌关键点检测 kpu 释放内存
def hk_kpu_deinit():
    with ScopedTiming("hk_kpu_deinit",debug_mode > 0):
        if 'hk_ai2d' in globals():                             #删除hk_ai2d变量，释放对它所引用对象的内存引用
            global hk_ai2d
            del hk_ai2d
        if 'hk_ai2d_output_tensor' in globals():               #删除hk_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global hk_ai2d_output_tensor
            del hk_ai2d_output_tensor

# 求两个vector之间的夹角
def hk_vector_2d_angle(v1,v2):
    with ScopedTiming("hk_vector_2d_angle",debug_mode > 0):
        v1_x = v1[0]
        v1_y = v1[1]
        v2_x = v2[0]
        v2_y = v2[1]
        v1_norm = np.sqrt(v1_x * v1_x+ v1_y * v1_y)
        v2_norm = np.sqrt(v2_x * v2_x + v2_y * v2_y)
        dot_product = v1_x * v2_x + v1_y * v2_y
        cos_angle = dot_product/(v1_norm*v2_norm)
        angle = np.acos(cos_angle)*180/np.pi
        return angle

# 根据手掌关键点检测结果判断手势类别
def hk_gesture(results):
    with ScopedTiming("hk_gesture",debug_mode > 0):
        angle_list = []
        for i in range(5):
            angle = hk_vector_2d_angle([(results[0]-results[i*8+4]), (results[1]-results[i*8+5])],[(results[i*8+6]-results[i*8+8]),(results[i*8+7]-results[i*8+9])])
            angle_list.append(angle)

        thr_angle = 65.
        thr_angle_thumb = 53.
        thr_angle_s = 49.
        gesture_str = None
        if 65535. not in angle_list:
            if (angle_list[0]>thr_angle_thumb)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "fist"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]<thr_angle_s):
                gesture_str = "five"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "gun"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
                gesture_str = "love"
            elif (angle_list[0]>5)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "one"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
                gesture_str = "six"
            elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]>thr_angle):
                gesture_str = "three"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "thumbUp"
            elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "yeah"

        return gesture_str

#-------dynamic gesture--------:
# 动态手势识别 ai2d 初始化
def gesture_ai2d_init(kpu_obj, resize_shape):
    with ScopedTiming("gesture_ai2d_init",debug_mode > 0):
        global gesture_ai2d_resize, gesture_ai2d_resize_builder
        global gesture_ai2d_crop, gesture_ai2d_crop_builder
        global gesture_ai2d_middle_output_tensor, gesture_ai2d_output_tensor

        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = gesture_kmodel_frame_size[0]
        height = gesture_kmodel_frame_size[1]
        ratiow = float(resize_shape) / ori_w
        ratioh = float(resize_shape) / ori_h
        if ratiow < ratioh:
            ratio = ratioh
        else:
            ratio = ratiow
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)

        top = int((new_h-height)/2)
        left = int((new_w-width)/2)

        gesture_ai2d_resize = nn.ai2d()
        gesture_ai2d_resize.set_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
        gesture_ai2d_resize.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
        gesture_ai2d_resize_builder = gesture_ai2d_resize.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,new_h,new_w])

        gesture_ai2d_crop = nn.ai2d()
        gesture_ai2d_crop.set_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
        gesture_ai2d_crop.set_crop_param(True, left, top, width, height)
        gesture_ai2d_crop_builder = gesture_ai2d_crop.build([1,3,new_h,new_w], [1,3,height,width])

        global gesture_kpu_input_tensor, gesture_kpu_input_tensors, current_kmodel_obj
        current_kmodel_obj = kpu_obj
        gesture_kpu_input_tensors = []
        for i in range(current_kmodel_obj.inputs_size()):
            data = np.zeros(gesture_kmodel_input_shape[i], dtype=np.float)
            gesture_kpu_input_tensor = nn.from_numpy(data)
            gesture_kpu_input_tensors.append(gesture_kpu_input_tensor)

        data = np.ones(gesture_kmodel_input_shape[0], dtype=np.uint8)
        gesture_ai2d_output_tensor = nn.from_numpy(data)

        global data_float
        data_float = np.ones(gesture_kmodel_input_shape[0], dtype=np.float)

        data_middle = np.ones((1,3,new_h,new_w), dtype=np.uint8)
        gesture_ai2d_middle_output_tensor = nn.from_numpy(data_middle)

def gesture_ai2d_run(rgb888p_img):
    with ScopedTiming("gesture_ai2d_run",debug_mode > 0):
        global gesture_ai2d_input_tensor, gesture_kpu_input_tensors, gesture_ai2d_middle_output_tensor, gesture_ai2d_output_tensor
        global gesture_ai2d_resize_builder, gesture_ai2d_crop_builder

        gesture_ai2d_input = rgb888p_img.to_numpy_ref()
        gesture_ai2d_input_tensor = nn.from_numpy(gesture_ai2d_input)

        gesture_ai2d_resize_builder.run(gesture_ai2d_input_tensor, gesture_ai2d_middle_output_tensor)
        gesture_ai2d_crop_builder.run(gesture_ai2d_middle_output_tensor, gesture_ai2d_output_tensor)

        result = gesture_ai2d_output_tensor.to_numpy()
        global data_float
        data_float[0] = result[0].copy()
        data_float[0] = (data_float[0]*1.0/255 -mean_values)/std_values
        tmp = nn.from_numpy(data_float)
        gesture_kpu_input_tensors[0] = tmp

# 动态手势识别 ai2d 释放内存
def gesture_ai2d_release():
    with ScopedTiming("gesture_ai2d_release",debug_mode > 0):
        global gesture_ai2d_input_tensor
        del gesture_ai2d_input_tensor

# 动态手势识别 kpu 初始化
def gesture_kpu_init(gesture_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("gesture_kpu_init",debug_mode > 0):
        gesture_kpu_obj = nn.kpu()
        gesture_kpu_obj.load_kmodel(gesture_kmodel_file)
        gesture_ai2d_init(gesture_kpu_obj, resize_shape)
        return gesture_kpu_obj

# 动态手势识别 kpu 输入预处理
def gesture_kpu_pre_process(rgb888p_img):
    gesture_ai2d_run(rgb888p_img)
    with ScopedTiming("gesture_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,gesture_kpu_input_tensors
        # set kpu input
        for i in range(current_kmodel_obj.inputs_size()):
            current_kmodel_obj.set_input_tensor(i, gesture_kpu_input_tensors[i])

# 动态手势识别 kpu 获得 kmodel 输出
def gesture_kpu_get_output():
    with ScopedTiming("gesture_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj, gesture_kpu_input_tensors
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            if (i==0):
                result = data.to_numpy()
                tmp2 = result.copy()
            else:
                gesture_kpu_input_tensors[i] = data
        return tmp2

# 动态手势识别结果处理
def gesture_process_output(pred,history):
    if (pred == 7 or pred == 8 or pred == 21 or pred == 22 or pred == 3 ):
        pred = history[-1]
    if (pred == 0 or pred == 4 or pred == 6 or pred == 9 or pred == 14 or pred == 1 or pred == 19 or pred == 20 or pred == 23 or pred == 24) :
        pred = history[-1]
    if (pred == 0) :
        pred = 2
    if (pred != history[-1]) :
        if (len(history)>= 2) :
            if (history[-1] != history[len(history)-2]) :
                pred = history[-1]
    history.append(pred)
    if (len(history) > max_hist_len) :
        history = history[-max_hist_len:]
    return history[-1]

# 动态手势识别结果后处理
def gesture_kpu_post_process(results, his_logit, history):
    with ScopedTiming("gesture_kpu_post_process",debug_mode > 0):
        his_logit.append(results[0])
        avg_logit = sum(np.array(his_logit))
        idx_ = np.argmax(avg_logit)

        idx = gesture_process_output(idx_, history)
        if (idx_ != idx):
            his_logit_last = his_logit[-1]
            his_logit = []
            his_logit.append(his_logit_last)
        return idx, avg_logit

# 动态手势识别 kpu 运行
def gesture_kpu_run(kpu_obj,rgb888p_img, his_logit, history):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    gesture_kpu_pre_process(rgb888p_img)
    # (2)动态手势识别 kpu 运行
    with ScopedTiming("gesture_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放动态手势识别 ai2d 资源
    gesture_ai2d_release()
    # (4)获取动态手势识别 kpu 输出
    results = gesture_kpu_get_output()
    # (5)动态手势识别 kpu 结果后处理
    result,  avg_logit= gesture_kpu_post_process(results,his_logit, history)
    # (6)返回动态手势识别结果
    return result, avg_logit

def gesture_kpu_deinit():
    with ScopedTiming("gesture_kpu_deinit",debug_mode > 0):
        if 'gesture_ai2d_resize' in globals():                             #删除gesture_ai2d_resize变量，释放对它所引用对象的内存引用
            global gesture_ai2d_resize
            del gesture_ai2d_resize
        if 'gesture_ai2d_middle_output_tensor' in globals():               #删除gesture_ai2d_middle_output_tensor变量，释放对它所引用对象的内存引用
            global gesture_ai2d_middle_output_tensor
            del gesture_ai2d_middle_output_tensor
        if 'gesture_ai2d_crop' in globals():                               #删除gesture_ai2d_crop变量，释放对它所引用对象的内存引用
            global gesture_ai2d_crop
            del gesture_ai2d_crop
        if 'gesture_ai2d_output_tensor' in globals():                      #删除gesture_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global gesture_ai2d_output_tensor
            del gesture_ai2d_output_tensor
        if 'gesture_kpu_input_tensors' in globals():                       #删除gesture_kpu_input_tensors变量，释放对它所引用对象的内存引用
            global gesture_kpu_input_tensors
            del gesture_kpu_input_tensors
        if 'gesture_ai2d_resize_builder' in globals():                     #删除gesture_ai2d_resize_builder变量，释放对它所引用对象的内存引用
            global gesture_ai2d_resize_builder
            del gesture_ai2d_resize_builder
        if 'gesture_ai2d_crop_builder' in globals():                       #删除gesture_ai2d_crop_builder变量，释放对它所引用对象的内存引用
            global gesture_ai2d_crop_builder
            del gesture_ai2d_crop_builder


#media_utils.py
global draw_img,osd_img,draw_numpy                          #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img, draw_numpy
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_numpy = np.zeros((DISPLAY_HEIGHT, DISPLAY_WIDTH,4), dtype=np.uint8)
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, alloc=image.ALLOC_REF, data=draw_numpy)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)
    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for dynamic_gesture.py**********
def dynamic_gesture_inference():
    print("dynamic_gesture_test start")
    cur_state = TRIGGER
    pre_state = TRIGGER
    draw_state = TRIGGER

    kpu_hand_detect = hd_kpu_init(hd_kmodel_file)                       # 创建手掌检测的 kpu 对象
    kpu_hand_keypoint_detect = hk_kpu_init(hk_kmodel_file)              # 创建手掌关键点检测的 kpu 对象
    kpu_dynamic_gesture = gesture_kpu_init(gesture_kmodel_file)         # 创建动态手势识别的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)
        vec_flag = []
        his_logit = []
        history = [2]
        s_start = time.time_ns()

        count = 0
        global draw_img,draw_numpy,osd_img
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    draw_img.clear()
                    if (cur_state == TRIGGER):
                        with ScopedTiming("trigger time", debug_mode > 0):
                            dets = hd_kpu_run(kpu_hand_detect,rgb888p_img)                                                  # 执行手掌检测 kpu 运行 以及 后处理过程

                            for det_box in dets:
                                x1, y1, x2, y2 = int(det_box[2]),int(det_box[3]),int(det_box[4]),int(det_box[5])
                                w = int(x2 - x1)
                                h = int(y2 - y1)

                                if (h<(0.1*OUT_RGB888P_HEIGHT)):
                                    continue
                                if (w<(0.25*OUT_RGB888P_WIDTH) and ((x1<(0.03*OUT_RGB888P_WIDTH)) or (x2>(0.97*OUT_RGB888P_WIDTH)))):
                                    continue
                                if (w<(0.15*OUT_RGB888P_WIDTH) and ((x1<(0.01*OUT_RGB888P_WIDTH)) or (x2>(0.99*OUT_RGB888P_WIDTH)))):
                                    continue

                                length = max(w,h)/2
                                cx = (x1+x2)/2
                                cy = (y1+y2)/2
                                ratio_num = 1.26*length

                                x1_kp = int(max(0,cx-ratio_num))
                                y1_kp = int(max(0,cy-ratio_num))
                                x2_kp = int(min(OUT_RGB888P_WIDTH-1, cx+ratio_num))
                                y2_kp = int(min(OUT_RGB888P_HEIGHT-1, cy+ratio_num))
                                w_kp = int(x2_kp - x1_kp + 1)
                                h_kp = int(y2_kp - y1_kp + 1)

                                hk_results = hk_kpu_run(kpu_hand_keypoint_detect,rgb888p_img, x1_kp, y1_kp, w_kp, h_kp)     # 执行手掌关键点检测 kpu 运行 以及 后处理过程
                                gesture = hk_gesture(hk_results)                                                            # 根据关键点检测结果判断手势类别

                                if ((gesture == "five") or (gesture == "yeah")):
                                    v_x = hk_results[24]-hk_results[0]
                                    v_y = hk_results[25]-hk_results[1]
                                    angle = hk_vector_2d_angle([v_x,v_y],[1.0,0.0])                                         # 计算手指（中指）的朝向

                                    if (v_y>0):
                                        angle = 360-angle

                                    if ((70.0<=angle) and (angle<110.0)):                                                   # 手指向上
                                        if ((pre_state != UP) or (pre_state != MIDDLE)):
                                            vec_flag.append(pre_state)
                                        if ((len(vec_flag)>10)or(pre_state == UP) or (pre_state == MIDDLE) or(pre_state == TRIGGER)):
                                            draw_numpy[:bin_height,:bin_width,:] = shang_argb
                                            cur_state = UP

                                    elif ((110.0<=angle) and (angle<225.0)):                                                # 手指向右(实际方向)
                                        if (pre_state != RIGHT):
                                            vec_flag.append(pre_state)
                                        if ((len(vec_flag)>10)or(pre_state == RIGHT)or(pre_state == TRIGGER)):
                                            draw_numpy[:bin_width,:bin_height,:] = you_argb
                                            cur_state = RIGHT

                                    elif((225.0<=angle) and (angle<315.0)):                                                 # 手指向下
                                        if (pre_state != DOWN):
                                            vec_flag.append(pre_state)
                                        if ((len(vec_flag)>10)or(pre_state == DOWN)or(pre_state == TRIGGER)):
                                            draw_numpy[:bin_height,:bin_width,:] = xia_argb
                                            cur_state = DOWN

                                    else:                                                                                   # 手指向左(实际方向)
                                        if (pre_state != LEFT):
                                            vec_flag.append(pre_state)
                                        if ((len(vec_flag)>10)or(pre_state == LEFT)or(pre_state == TRIGGER)):
                                            draw_numpy[:bin_width,:bin_height,:] = zuo_argb
                                            cur_state = LEFT

                                    m_start = time.time_ns()
                            his_logit = []
                    else:
                        with ScopedTiming("swip time",debug_mode > 0):
                            idx, avg_logit = gesture_kpu_run(kpu_dynamic_gesture,rgb888p_img, his_logit, history)           # 执行动态手势识别 kpu 运行 以及 后处理过程
                            if (cur_state == UP):
                                draw_numpy[:bin_height,:bin_width,:] = shang_argb
                                if ((idx==15) or (idx==10)):
                                    vec_flag.clear()
                                    if (((avg_logit[idx] >= 0.7) and (len(his_logit) >= 2)) or ((avg_logit[idx] >= 0.3) and (len(his_logit) >= 4))):
                                        s_start = time.time_ns()
                                        cur_state = TRIGGER
                                        draw_state = DOWN
                                        history = [2]
                                    pre_state = UP
                                elif ((idx==25)or(idx==26)) :
                                    vec_flag.clear()
                                    if (((avg_logit[idx] >= 0.4) and (len(his_logit) >= 2)) or ((avg_logit[idx] >= 0.3) and (len(his_logit) >= 3))):
                                        s_start = time.time_ns()
                                        cur_state = TRIGGER
                                        draw_state = MIDDLE
                                        history = [2]
                                    pre_state = MIDDLE
                                else:
                                    his_logit.clear()
                            elif (cur_state == RIGHT):
                                draw_numpy[:bin_width,:bin_height,:] = you_argb
                                if  ((idx==16)or(idx==11)) :
                                    vec_flag.clear()
                                    if (((avg_logit[idx] >= 0.4) and (len(his_logit) >= 2)) or ((avg_logit[idx] >= 0.3) and (len(his_logit) >= 3))):
                                        s_start = time.time_ns()
                                        cur_state = TRIGGER
                                        draw_state = RIGHT
                                        history = [2]
                                    pre_state = RIGHT
                                else:
                                    his_logit.clear()
                            elif (cur_state == DOWN):
                                draw_numpy[:bin_height,:bin_width,:] = xia_argb
                                if  ((idx==18)or(idx==13)):
                                    vec_flag.clear()
                                    if (((avg_logit[idx] >= 0.4) and (len(his_logit) >= 2)) or ((avg_logit[idx] >= 0.3) and (len(his_logit) >= 3))):
                                        s_start = time.time_ns()
                                        cur_state = TRIGGER
                                        draw_state = UP
                                        history = [2]
                                    pre_state = DOWN
                                else:
                                    his_logit.clear()
                            elif (cur_state == LEFT):
                                draw_numpy[:bin_width,:bin_height,:] = zuo_argb
                                if ((idx==17)or(idx==12)):
                                    vec_flag.clear()
                                    if (((avg_logit[idx] >= 0.4) and (len(his_logit) >= 2)) or ((avg_logit[idx] >= 0.3) and (len(his_logit) >= 3))):
                                        s_start = time.time_ns()
                                        cur_state = TRIGGER
                                        draw_state = LEFT
                                        history = [2]
                                    pre_state = LEFT
                                else:
                                    his_logit.clear()

                        elapsed_time = round((time.time_ns() - m_start)/1000000)

                        if ((cur_state != TRIGGER) and (elapsed_time>2000)):
                            cur_state = TRIGGER
                            pre_state = TRIGGER

                    elapsed_ms_show = round((time.time_ns()-s_start)/1000000)
                    if (elapsed_ms_show<1000):
                        if (draw_state == UP):
                            draw_img.draw_arrow(1068,330,1068,130, (255,170,190,230), thickness=13)                             # 判断为向上挥动时，画一个向上的箭头
                        elif (draw_state == RIGHT):
                            draw_img.draw_arrow(1290,540,1536,540, (255,170,190,230), thickness=13)                             # 判断为向右挥动时，画一个向右的箭头
                        elif (draw_state == DOWN):
                            draw_img.draw_arrow(1068,750,1068,950, (255,170,190,230), thickness=13)                             # 判断为向下挥动时，画一个向下的箭头
                        elif (draw_state == LEFT):
                            draw_img.draw_arrow(846,540,600,540, (255,170,190,230), thickness=13)                               # 判断为向左挥动时，画一个向左的箭头
                        elif (draw_state == MIDDLE):
                            draw_img.draw_circle(1068,540,100, (255,170,190,230), thickness=2, fill=True)                       # 判断为五指捏合手势时，画一个实心圆
                    else:
                        draw_state = TRIGGER

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)         # camera 释放图像
                if (count>5):
                    gc.collect()
                    count = 0
                else:
                    count += 1

            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        camera_stop(CAM_DEV_ID_0)                                       # 停止 camera
        display_deinit()                                                # 释放 display
        hd_kpu_deinit()                                                 # 释放手掌检测 kpu
        hk_kpu_deinit()                                                 # 释放手掌关键点检测 kpu
        gesture_kpu_deinit()                                            # 释放动态手势识别 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_hand_detect
        del kpu_hand_keypoint_detect
        del kpu_dynamic_gesture

        if 'draw_numpy' in globals():
            global draw_numpy
            del draw_numpy

        if 'draw_img' in globals():
            global draw_img
            del draw_img

        gc.collect()
#        nn.shrink_memory_pool()
        media_deinit()                                                  # 释放 整个media

    print("dynamic_gesture_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    dynamic_gesture_inference()
```

### 13.单目标跟踪

```python
import ulab.numpy as np             #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn         #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *          #摄像头模块
from media.display import *         #显示模块
from media.media import *           #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import image                        #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                         #时间统计
import gc                           #垃圾回收模块
import aidemo                       #aidemo模块，封装ai demo相关后处理、画图操作
import os, sys                      #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

#ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1280, 16)
OUT_RGB888P_HEIGHT = 720

#单目标跟踪 kmodel 输入 shape
crop_kmodel_input_shape = (1,3,127,127)
src_kmodel_input_shape = (1,3,255,255)


#单目标跟踪 相关参数设置
head_thresh = 0.1                                           #单目标跟踪分数阈值
CONTEXT_AMOUNT = 0.5                                        #跟踪框宽、高调整系数
rgb_mean = [114,114,114]                                    #padding颜色值
ratio_src_crop = float(src_kmodel_input_shape[2])/float(crop_kmodel_input_shape[2])     #src模型和crop模型输入比值
track_x1 = float(300)                                       #起始跟踪目标框左上角点x
track_y1 = float(300)                                       #起始跟踪目标框左上角点y
track_w = float(100)                                        #起始跟踪目标框w
track_h = float(100)                                        #起始跟踪目标框h


#文件配置
root_dir = '/sdcard/app/tests/'
crop_kmodel_file = root_dir + 'kmodel/cropped_test127.kmodel'                               #单目标跟踪 crop kmodel 文件路径
src_kmodel_file = root_dir + 'kmodel/nanotrack_backbone_sim.kmodel'                         #单目标跟踪 src kmodel 文件路径
track_kmodel_file = root_dir + 'kmodel/nanotracker_head_calib_k230.kmodel'                  #单目标跟踪 head kmodel 文件路径

debug_mode = 0                                                                              # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")


#ai_utils.py
global current_kmodel_obj                                                                               # 定义全局的 kpu 对象
global crop_ai2d,crop_ai2d_input_tensor,crop_ai2d_output_tensor,crop_ai2d_builder                       # 对应crop模型： ai2d 对象 ，并且定义 ai2d 的输入、输出 以及 builder
global crop_pad_ai2d,crop_pad_ai2d_input_tensor,crop_pad_ai2d_output_tensor,crop_pad_ai2d_builder       # 对应crop模型： ai2d 对象 ，并且定义 ai2d 的输入、输出 以及 builder
global src_ai2d,src_ai2d_input_tensor,src_ai2d_output_tensor,src_ai2d_builder                           # 对应src模型： ai2d 对象 ，并且定义 ai2d 的输入、输出 以及 builder
global src_pad_ai2d,src_pad_ai2d_input_tensor,src_pad_ai2d_output_tensor,src_pad_ai2d_builder           # 对应src模型： ai2d 对象 ，并且定义 ai2d 的输入、输出 以及 builder
global track_kpu_input_0,track_kpu_input_1                                                              # 对应head模型： 两个输入


# 单目标跟踪的后处理
def track_kpu_post_process(output_data,center_xy_wh):
    with ScopedTiming("track_kpu_post_process", debug_mode > 0):
        det = aidemo.nanotracker_postprocess(output_data[0],output_data[1],[OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH],head_thresh,center_xy_wh,crop_kmodel_input_shape[2],CONTEXT_AMOUNT)
        return det

# 单目标跟踪 对应crop模型的 ai2d 初始化
def crop_ai2d_init():
    with ScopedTiming("crop_ai2d_init",debug_mode > 0):
        global crop_ai2d, crop_pad_ai2d
        crop_ai2d = nn.ai2d()
        crop_pad_ai2d = nn.ai2d()

        crop_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,nn.ai2d_format.NCHW_FMT,np.uint8, np.uint8)
        crop_pad_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,nn.ai2d_format.NCHW_FMT,np.uint8, np.uint8)

        crop_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        crop_pad_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        global crop_ai2d_out_tensor
        data = np.ones(crop_kmodel_input_shape, dtype=np.uint8)
        crop_ai2d_out_tensor = nn.from_numpy(data)

# 单目标跟踪 对应crop模型的 ai2d 运行
def crop_ai2d_run(rgb888p_img,center_xy_wh):
    with ScopedTiming("crop_ai2d_run",debug_mode > 0):
        global crop_ai2d, crop_pad_ai2d
        global crop_ai2d_input_tensor,crop_ai2d_out_tensor,crop_ai2d_builder
        global crop_pad_ai2d_input_tensor,crop_pad_ai2d_out_tensor,crop_pad_ai2d_builder

        s_z = round(np.sqrt((center_xy_wh[2] + CONTEXT_AMOUNT * (center_xy_wh[2] + center_xy_wh[3])) * (center_xy_wh[3] + CONTEXT_AMOUNT * (center_xy_wh[2] + center_xy_wh[3]))))
        c = (s_z + 1) / 2
        context_xmin = np.floor(center_xy_wh[0] - c + 0.5)
        context_xmax = int(context_xmin + s_z - 1)
        context_ymin = np.floor(center_xy_wh[1] - c + 0.5)
        context_ymax = int(context_ymin + s_z - 1)

        left_pad = int(max(0, -context_xmin))
        top_pad = int(max(0, -context_ymin))
        right_pad = int(max(0, int(context_xmax - OUT_RGB888P_WIDTH + 1)))
        bottom_pad = int(max(0, int(context_ymax - OUT_RGB888P_HEIGHT + 1)))
        context_xmin = context_xmin + left_pad
        context_xmax = context_xmax + left_pad
        context_ymin = context_ymin + top_pad
        context_ymax = context_ymax + top_pad

        if (left_pad != 0 or right_pad != 0 or top_pad != 0 or bottom_pad != 0):
            crop_pad_ai2d.set_pad_param(True, [0, 0, 0, 0, top_pad, bottom_pad, left_pad, right_pad], 0, rgb_mean)
            crop_pad_ai2d_builder = crop_pad_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1, 3, OUT_RGB888P_HEIGHT + top_pad + bottom_pad, OUT_RGB888P_WIDTH + left_pad + right_pad])
            crop_pad_ai2d_input = rgb888p_img.to_numpy_ref()
            crop_pad_ai2d_input_tensor = nn.from_numpy(crop_pad_ai2d_input)
            crop_pad_ai2d_output = np.ones([1, 3, OUT_RGB888P_HEIGHT + top_pad + bottom_pad, OUT_RGB888P_WIDTH + left_pad + right_pad], dtype=np.uint8)
            crop_pad_ai2d_out_tensor = nn.from_numpy(crop_pad_ai2d_output)
            crop_pad_ai2d_builder.run(crop_pad_ai2d_input_tensor, crop_pad_ai2d_out_tensor)

            crop_ai2d.set_crop_param(True, int(context_xmin), int(context_ymin), int(context_xmax - context_xmin + 1), int(context_ymax - context_ymin + 1))
            crop_ai2d_builder = crop_ai2d.build([1, 3, OUT_RGB888P_HEIGHT + top_pad + bottom_pad, OUT_RGB888P_WIDTH + left_pad + right_pad], crop_kmodel_input_shape)
            crop_ai2d_input_tensor = crop_pad_ai2d_out_tensor
            crop_ai2d_builder.run(crop_ai2d_input_tensor, crop_ai2d_out_tensor)
            del crop_pad_ai2d_input_tensor
            del crop_pad_ai2d_out_tensor
            del crop_pad_ai2d_builder
        else:
            crop_ai2d.set_crop_param(True, int(center_xy_wh[0] - s_z/2.0), int(center_xy_wh[1] - s_z/2.0), int(s_z), int(s_z))
            crop_ai2d_builder = crop_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], crop_kmodel_input_shape)
            crop_ai2d_input = rgb888p_img.to_numpy_ref()
            crop_ai2d_input_tensor = nn.from_numpy(crop_ai2d_input)
            crop_ai2d_builder.run(crop_ai2d_input_tensor, crop_ai2d_out_tensor)

# 单目标跟踪 对应crop模型的 ai2d 释放
def crop_ai2d_release():
    with ScopedTiming("crop_ai2d_release",debug_mode > 0):
        global crop_ai2d_input_tensor,crop_ai2d_builder
        del crop_ai2d_input_tensor
        del crop_ai2d_builder


# 单目标跟踪 对应src模型的 ai2d 初始化
def src_ai2d_init():
    with ScopedTiming("src_ai2d_init",debug_mode > 0):
        global src_ai2d, src_pad_ai2d
        src_ai2d = nn.ai2d()
        src_pad_ai2d = nn.ai2d()

        src_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,nn.ai2d_format.NCHW_FMT,np.uint8, np.uint8)
        src_pad_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,nn.ai2d_format.NCHW_FMT,np.uint8, np.uint8)

        src_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        src_pad_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        global src_ai2d_out_tensor
        data = np.ones(src_kmodel_input_shape, dtype=np.uint8)
        src_ai2d_out_tensor = nn.from_numpy(data)

# 单目标跟踪 对应src模型的 ai2d 运行
def src_ai2d_run(rgb888p_img,center_xy_wh):
    with ScopedTiming("src_ai2d_run",debug_mode > 0):
        global src_ai2d, src_pad_ai2d
        global src_ai2d_input_tensor,src_ai2d_out_tensor,src_ai2d_builder
        global src_pad_ai2d_input_tensor,src_pad_ai2d_out_tensor,src_pad_ai2d_builder

        s_z = round(np.sqrt((center_xy_wh[2] + CONTEXT_AMOUNT * (center_xy_wh[2] + center_xy_wh[3])) * (center_xy_wh[3] + CONTEXT_AMOUNT * (center_xy_wh[2] + center_xy_wh[3])))) * ratio_src_crop
        c = (s_z + 1) / 2
        context_xmin = np.floor(center_xy_wh[0] - c + 0.5)
        context_xmax = int(context_xmin + s_z - 1)
        context_ymin = np.floor(center_xy_wh[1] - c + 0.5)
        context_ymax = int(context_ymin + s_z - 1)

        left_pad = int(max(0, -context_xmin))
        top_pad = int(max(0, -context_ymin))
        right_pad = int(max(0, int(context_xmax - OUT_RGB888P_WIDTH + 1)))
        bottom_pad = int(max(0, int(context_ymax - OUT_RGB888P_HEIGHT + 1)))
        context_xmin = context_xmin + left_pad
        context_xmax = context_xmax + left_pad
        context_ymin = context_ymin + top_pad
        context_ymax = context_ymax + top_pad

        if (left_pad != 0 or right_pad != 0 or top_pad != 0 or bottom_pad != 0):
            src_pad_ai2d.set_pad_param(True, [0, 0, 0, 0, top_pad, bottom_pad, left_pad, right_pad], 0, rgb_mean)
            src_pad_ai2d_builder = src_pad_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1, 3, OUT_RGB888P_HEIGHT + top_pad + bottom_pad, OUT_RGB888P_WIDTH + left_pad + right_pad])
            src_pad_ai2d_input = rgb888p_img.to_numpy_ref()
            src_pad_ai2d_input_tensor = nn.from_numpy(src_pad_ai2d_input)
            src_pad_ai2d_output = np.ones([1, 3, OUT_RGB888P_HEIGHT + top_pad + bottom_pad, OUT_RGB888P_WIDTH + left_pad + right_pad], dtype=np.uint8)
            src_pad_ai2d_out_tensor = nn.from_numpy(src_pad_ai2d_output)
            src_pad_ai2d_builder.run(src_pad_ai2d_input_tensor, src_pad_ai2d_out_tensor)

            src_ai2d.set_crop_param(True, int(context_xmin), int(context_ymin), int(context_xmax - context_xmin + 1), int(context_ymax - context_ymin + 1))
            src_ai2d_builder = src_ai2d.build([1, 3, OUT_RGB888P_HEIGHT + top_pad + bottom_pad, OUT_RGB888P_WIDTH + left_pad + right_pad], src_kmodel_input_shape)
            src_ai2d_input_tensor = src_pad_ai2d_out_tensor
            src_ai2d_builder.run(src_ai2d_input_tensor, src_ai2d_out_tensor)
            del src_pad_ai2d_input_tensor
            del src_pad_ai2d_out_tensor
            del src_pad_ai2d_builder
        else:
            src_ai2d.set_crop_param(True, int(center_xy_wh[0] - s_z/2.0), int(center_xy_wh[1] - s_z/2.0), int(s_z), int(s_z))
            src_ai2d_builder = src_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], src_kmodel_input_shape)
            src_ai2d_input = rgb888p_img.to_numpy_ref()
            src_ai2d_input_tensor = nn.from_numpy(src_ai2d_input)
            src_ai2d_builder.run(src_ai2d_input_tensor, src_ai2d_out_tensor)

# 单目标跟踪 对应src模型的 ai2d 释放
def src_ai2d_release():
    with ScopedTiming("src_ai2d_release",debug_mode > 0):
        global src_ai2d_input_tensor,src_ai2d_builder
        del src_ai2d_input_tensor
        del src_ai2d_builder


# 单目标跟踪 crop kpu 初始化
def crop_kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("crop_kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        crop_ai2d_init()
        return kpu_obj

# 单目标跟踪 crop kpu 输入预处理
def crop_kpu_pre_process(rgb888p_img,center_xy_wh):
    crop_ai2d_run(rgb888p_img,center_xy_wh)
    with ScopedTiming("crop_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,crop_ai2d_out_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, crop_ai2d_out_tensor)

# 单目标跟踪 crop kpu 获取输出
def crop_kpu_get_output():
    with ScopedTiming("crop_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        del data
        return result

# 单目标跟踪 crop kpu 运行
def crop_kpu_run(kpu_obj,rgb888p_img,center_xy_wh):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1) 原图预处理，并设置模型输入
    crop_kpu_pre_process(rgb888p_img,center_xy_wh)
    # (2) kpu 运行
    with ScopedTiming("crop_kpu_run",debug_mode > 0):
        kpu_obj.run()
    # (3) 释放ai2d资源
    crop_ai2d_release()
    # (4) 获取kpu输出
    result = crop_kpu_get_output()
    # 返回 crop kpu 的输出
    return result

# 单目标跟踪 crop kpu 释放
def crop_kpu_deinit():
    with ScopedTiming("crop_kpu_deinit",debug_mode > 0):
        if 'crop_ai2d' in globals():
            global crop_ai2d
            del crop_ai2d
        if 'crop_pad_ai2d' in globals():
            global crop_pad_ai2d
            del crop_pad_ai2d
        if 'crop_ai2d_out_tensor' in globals():
            global crop_ai2d_out_tensor
            del crop_ai2d_out_tensor

# 单目标跟踪 src kpu 初始化
def src_kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("src_kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)

        src_ai2d_init()
        return kpu_obj

# 单目标跟踪 src kpu 输入预处理
def src_kpu_pre_process(rgb888p_img,center_xy_wh):
    src_ai2d_run(rgb888p_img,center_xy_wh)
    with ScopedTiming("src_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,src_ai2d_out_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, src_ai2d_out_tensor)

# 单目标跟踪 src kpu 获取输出
def src_kpu_get_output():
    with ScopedTiming("src_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        data = current_kmodel_obj.get_output_tensor(0)
        result = data.to_numpy()
        del data
        return result

# 单目标跟踪 src kpu 运行
def src_kpu_run(kpu_obj,rgb888p_img,center_xy_wh):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1) 原图预处理，并设置模型输入
    src_kpu_pre_process(rgb888p_img,center_xy_wh)
    # (2) kpu 运行
    with ScopedTiming("src_kpu_run",debug_mode > 0):
        kpu_obj.run()
    # (3) 释放ai2d资源
    src_ai2d_release()
    # (4) 获取kpu输出
    result = src_kpu_get_output()
    # 返回 src kpu 的输出
    return result

# 单目标跟踪 src kpu 释放
def src_kpu_deinit():
    with ScopedTiming("src_kpu_deinit",debug_mode > 0):
        if 'src_ai2d' in globals():
            global src_ai2d
            del src_ai2d
        if 'src_pad_ai2d' in globals():
            global src_pad_ai2d
            del src_pad_ai2d
        if 'src_ai2d_out_tensor' in globals():
            global src_ai2d_out_tensor
            del src_ai2d_out_tensor

# 单目标跟踪 track kpu 初始化
def track_kpu_init(kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("track_kpu_init",debug_mode > 0):
        kpu_obj = nn.kpu()
        kpu_obj.load_kmodel(kmodel_file)
        return kpu_obj

# 单目标跟踪 track kpu 输入预处理
def track_kpu_pre_process():
    with ScopedTiming("track_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,track_kpu_input_0,track_kpu_input_1
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, track_kpu_input_0)
        current_kmodel_obj.set_input_tensor(1, track_kpu_input_1)

# 单目标跟踪 track kpu 获取输出
def track_kpu_get_output():
    with ScopedTiming("track_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            del data
            results.append(result)
        return results

# 单目标跟踪 track kpu 运行
def track_kpu_run(kpu_obj,center_xy_wh):
    global current_kmodel_obj,track_kpu_input_1
    current_kmodel_obj = kpu_obj
    # (1) 原图预处理，并设置模型输入
    track_kpu_pre_process()
    # (2) kpu 运行
    with ScopedTiming("track_kpu_run",debug_mode > 0):
        kpu_obj.run()

    del track_kpu_input_1
    # (4) 获取kpu输出
    results = track_kpu_get_output()
    # (5) track 后处理
    det = track_kpu_post_process(results,center_xy_wh)
    # 返回 跟踪的结果
    return det

# 单目标跟踪 track kpu 释放
def track_kpu_deinit():
    with ScopedTiming("track_kpu_deinit",debug_mode > 0):
        if 'track_kpu_input_0' in globals():
            global track_kpu_input_0
            del track_kpu_input_0



#media_utils.py
global draw_img,osd_img                                     #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()


#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_BGR_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for nanotracker.py**********
def nanotracker_inference():
    print("nanotracker start")
    kpu_crop = crop_kpu_init(crop_kmodel_file)                  # 创建单目标跟踪 crop kpu 对象
    kpu_src = src_kpu_init(src_kmodel_file)                     # 创建单目标跟踪 src kpu 对象
    kpu_track = track_kpu_init(track_kmodel_file)               # 创建单目标跟踪 track kpu 对象
    camera_init(CAM_DEV_ID_0)                                   # 初始化 camera
    display_init()                                              # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)

        run_bool = True
        if (track_x1 < 50 or track_y1 < 50 or track_x1+track_w >= OUT_RGB888P_WIDTH-50 or track_y1+track_h >= OUT_RGB888P_HEIGHT-50):
            print("**剪切范围超出图像范围**")
            run_bool = False

        track_mean_x = track_x1 + track_w / 2.0
        track_mean_y = track_y1 + track_h / 2.0
        draw_mean_w = int(track_w / OUT_RGB888P_WIDTH * DISPLAY_WIDTH)
        draw_mean_h = int(track_h / OUT_RGB888P_HEIGHT * DISPLAY_HEIGHT)
        draw_mean_x = int(track_mean_x / OUT_RGB888P_WIDTH * DISPLAY_WIDTH - draw_mean_w / 2.0)
        draw_mean_y = int(track_mean_y / OUT_RGB888P_HEIGHT * DISPLAY_HEIGHT - draw_mean_h / 2.0)
        track_w_src = track_w
        track_h_src = track_h

        center_xy_wh = [track_mean_x,track_mean_y,track_w_src,track_h_src]
        center_xy_wh_tmp = [track_mean_x,track_mean_y,track_w_src,track_h_src]

        seconds = 8
        endtime = time.time() + seconds
        enter_init = True

        track_boxes = [track_x1,track_y1,track_w,track_h,1]
        track_boxes_tmp = np.array([track_x1,track_y1,track_w,track_h,1])
        global draw_img,osd_img

        count = 0
        while run_bool:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    nowtime = time.time()
                    draw_img.clear()
                    if (enter_init and nowtime <= endtime):
                        print("倒计时: " + str(endtime - nowtime) + " 秒")
                        draw_img.draw_rectangle(draw_mean_x , draw_mean_y , draw_mean_w , draw_mean_h , color=(255, 0, 255, 0),thickness = 4)
                        print(" >>>>>> get trackWindow <<<<<<<<")
                        global track_kpu_input_0
                        track_kpu_input_0 = nn.from_numpy(crop_kpu_run(kpu_crop,rgb888p_img,center_xy_wh))

                        time.sleep(1)
                        if (nowtime > endtime):
                            print(">>>>>>>  Play  <<<<<<<")
                            enter_init = False
                    else:
                        global track_kpu_input_1
                        track_kpu_input_1 = nn.from_numpy(src_kpu_run(kpu_src,rgb888p_img,center_xy_wh))
                        det = track_kpu_run(kpu_track,center_xy_wh)
                        track_boxes = det[0]
                        center_xy_wh = det[1]
                        track_bool = True
                        if (len(track_boxes) != 0):
                            track_bool = track_boxes[0] > 10 and track_boxes[1] > 10 and track_boxes[0] + track_boxes[2] < OUT_RGB888P_WIDTH - 10 and track_boxes[1] + track_boxes[3] < OUT_RGB888P_HEIGHT - 10
                        else:
                            track_bool = False

                        if (len(center_xy_wh) != 0):
                            track_bool = track_bool and center_xy_wh[2] * center_xy_wh[3] < 40000
                        else:
                            track_bool = False

                        if (track_bool):
                            center_xy_wh_tmp = center_xy_wh
                            track_boxes_tmp = track_boxes
                            x1 = int(float(track_boxes[0]) * DISPLAY_WIDTH / OUT_RGB888P_WIDTH)
                            y1 = int(float(track_boxes[1]) * DISPLAY_HEIGHT / OUT_RGB888P_HEIGHT)
                            w = int(float(track_boxes[2]) * DISPLAY_WIDTH / OUT_RGB888P_WIDTH)
                            h = int(float(track_boxes[3]) * DISPLAY_HEIGHT / OUT_RGB888P_HEIGHT)
                            draw_img.draw_rectangle(x1, y1, w, h, color=(255, 255, 0, 0),thickness = 4)
                        else:
                            center_xy_wh = center_xy_wh_tmp
                            track_boxes = track_boxes_tmp
                            x1 = int(float(track_boxes[0]) * DISPLAY_WIDTH / OUT_RGB888P_WIDTH)
                            y1 = int(float(track_boxes[1]) * DISPLAY_HEIGHT / OUT_RGB888P_HEIGHT)
                            w = int(float(track_boxes[2]) * DISPLAY_WIDTH / OUT_RGB888P_WIDTH)
                            h = int(float(track_boxes[3]) * DISPLAY_HEIGHT / OUT_RGB888P_HEIGHT)
                            draw_img.draw_rectangle(x1, y1, w, h, color=(255, 255, 0, 0),thickness = 4)
                            draw_img.draw_string( x1 , y1-50, "Step away from the camera, please !" , color=(255, 255 ,0 , 0), scale=4, thickness = 1)
                            draw_img.draw_string( x1 , y1-100, "Near the center, please !" , color=(255, 255 ,0 , 0), scale=4, thickness = 1)


                    draw_img.copy_to(osd_img)
                    display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)                      # camera 释放图像

                if (count > 5):
                    gc.collect()
                    count = 0
                else:
                    count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        camera_stop(CAM_DEV_ID_0)                                                   # 停止 camera
        display_deinit()                                                            # 释放 display
        crop_kpu_deinit()                                                           # 释放 单目标跟踪 crop kpu
        src_kpu_deinit()                                                            # 释放 单目标跟踪 src kpu
        track_kpu_deinit()                                                          # 释放 单目标跟踪 track kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_crop
        del kpu_src
        del kpu_track

        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                                        # 释放 整个media

    print("nanotracker end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    nanotracker_inference()
```

### 14.隔空放大

```python
import aicube                   #aicube模块，封装检测分割等任务相关后处理
from media.camera import *      #摄像头模块
from media.display import *     #显示模块
from media.media import *       #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区

import nncase_runtime as nn     #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np         #类似python numpy操作，但也会有一些接口不同

import time                     #时间统计
import image                    #图像模块，主要用于读取、图像绘制元素（框、点等）等操作

import gc                       #垃圾回收模块
import os, sys                  #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

##ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

#--------for hand detection----------
#kmodel输入shape
hd_kmodel_input_shape = (1,3,512,512)                           # 手掌检测kmodel输入分辨率

#kmodel相关参数设置
confidence_threshold = 0.2                                      # 手掌检测阈值，用于过滤roi
nms_threshold = 0.5                                             # 手掌检测框阈值，用于过滤重复roi
hd_kmodel_frame_size = [512,512]                                # 手掌检测输入图片尺寸
hd_frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGHT]           # 手掌检测直接输入图片尺寸
strides = [8,16,32]                                             # 输出特征图的尺寸与输入图片尺寸的比
num_classes = 1                                                 # 手掌检测模型输出类别数
nms_option = False                                              # 是否所有检测框一起做NMS，False则按照不同的类分别应用NMS

root_dir = '/sdcard/app/tests/'
hd_kmodel_file = root_dir + "kmodel/hand_det.kmodel"      # 手掌检测kmodel文件的路径
anchors = [26,27, 53,52, 75,71, 80,99, 106,82, 99,134, 140,113, 161,172, 245,276]   #anchor设置

#--------for hand keypoint detection----------
#kmodel输入shape
hk_kmodel_input_shape = (1,3,256,256)                           # 手掌关键点检测kmodel输入分辨率

#kmodel相关参数设置
hk_kmodel_frame_size = [256,256]                                # 手掌关键点检测输入图片尺寸
hk_kmodel_file = root_dir + 'kmodel/handkp_det.kmodel'    # 手掌关键点检测kmodel文件的路径

debug_mode = 0                                                  # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                                   # 定义全局的 kpu 对象
global hd_ai2d,hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder   # 定义手掌检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor,hk_ai2d_builder   # 定义手掌关键点检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global space_ai2d,space_ai2d_input_tensor,space_ai2d_output_tensor,space_ai2d_builder,space_draw_ai2d_release    # 定义缩放剪切图像全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
space_draw_ai2d_release = False

#-------hand detect--------:
# 手掌检测ai2d 初始化
def hd_ai2d_init():
    with ScopedTiming("hd_ai2d_init",debug_mode > 0):
        global hd_ai2d
        global hd_ai2d_builder
        global hd_ai2d_output_tensor
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = hd_kmodel_frame_size[0]
        height = hd_kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        # init kpu and load kmodel
        hd_ai2d = nn.ai2d()
        hd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        hd_ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        hd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        hd_ai2d_builder = hd_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,height,width])
        data = np.ones(hd_kmodel_input_shape, dtype=np.uint8)
        hd_ai2d_output_tensor = nn.from_numpy(data)

# 手掌检测 ai2d 运行
def hd_ai2d_run(rgb888p_img):
    with ScopedTiming("hd_ai2d_run",debug_mode > 0):
        global hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder
        hd_ai2d_input = rgb888p_img.to_numpy_ref()
        hd_ai2d_input_tensor = nn.from_numpy(hd_ai2d_input)

        hd_ai2d_builder.run(hd_ai2d_input_tensor, hd_ai2d_output_tensor)

# 手掌检测 ai2d 释放内存
def hd_ai2d_release():
    with ScopedTiming("hd_ai2d_release",debug_mode > 0):
        global hd_ai2d_input_tensor
        del hd_ai2d_input_tensor

# 手掌检测 kpu 初始化
def hd_kpu_init(hd_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hd_kpu_init",debug_mode > 0):
        hd_kpu_obj = nn.kpu()
        hd_kpu_obj.load_kmodel(hd_kmodel_file)

        hd_ai2d_init()
        return hd_kpu_obj

# 手掌检测 kpu 输入预处理
def hd_kpu_pre_process(rgb888p_img):
    hd_ai2d_run(rgb888p_img)
    with ScopedTiming("hd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hd_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hd_ai2d_output_tensor)

# 手掌检测 kpu 获得 kmodel 输出
def hd_kpu_get_output():
    with ScopedTiming("hd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌检测 kpu 运行
def hd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hd_kpu_pre_process(rgb888p_img)
     # (2)手掌检测 kpu 运行
    with ScopedTiming("hd_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌检测 ai2d 资源
    hd_ai2d_release()
    # (4)获取手掌检测 kpu 输出
    results = hd_kpu_get_output()
    # (5)手掌检测 kpu 结果后处理
    dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], hd_kmodel_frame_size, hd_frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)
    # (6)返回手掌检测结果
    return dets

# 手掌检测 kpu 释放内存
def hd_kpu_deinit():
    with ScopedTiming("hd_kpu_deinit",debug_mode > 0):
        if 'hd_ai2d' in globals():
            global hd_ai2d
            del hd_ai2d
        if 'hd_ai2d_output_tensor' in globals():
            global hd_ai2d_output_tensor
            del hd_ai2d_output_tensor
        if 'hd_ai2d_builder' in globals():
            global hd_ai2d_builder
            del hd_ai2d_builder

#-------hand keypoint detection------:
# 手掌关键点检测 ai2d 初始化
def hk_ai2d_init():
    with ScopedTiming("hk_ai2d_init",debug_mode > 0):
        global hk_ai2d, hk_ai2d_output_tensor
        hk_ai2d = nn.ai2d()
        hk_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        data = np.ones(hk_kmodel_input_shape, dtype=np.uint8)
        hk_ai2d_output_tensor = nn.from_numpy(data)

# 手掌关键点检测 ai2d 运行
def hk_ai2d_run(rgb888p_img, x, y, w, h):
    with ScopedTiming("hk_ai2d_run",debug_mode > 0):
        global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor
        hk_ai2d_input = rgb888p_img.to_numpy_ref()
        hk_ai2d_input_tensor = nn.from_numpy(hk_ai2d_input)

        hk_ai2d.set_crop_param(True, x, y, w, h)
        hk_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )

        global hk_ai2d_builder
        hk_ai2d_builder = hk_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,hk_kmodel_frame_size[1],hk_kmodel_frame_size[0]])
        hk_ai2d_builder.run(hk_ai2d_input_tensor, hk_ai2d_output_tensor)

# 手掌关键点检测 ai2d 释放内存
def hk_ai2d_release():
    with ScopedTiming("hk_ai2d_release",debug_mode > 0):
        global hk_ai2d_input_tensor,hk_ai2d_builder
        del hk_ai2d_input_tensor
        del hk_ai2d_builder

# 手掌关键点检测 kpu 初始化
def hk_kpu_init(hk_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hk_kpu_init",debug_mode > 0):
        hk_kpu_obj = nn.kpu()
        hk_kpu_obj.load_kmodel(hk_kmodel_file)

        hk_ai2d_init()
        return hk_kpu_obj

# 手掌关键点检测 kpu 输入预处理
def hk_kpu_pre_process(rgb888p_img, x, y, w, h):
    hk_ai2d_run(rgb888p_img, x, y, w, h)
    with ScopedTiming("hk_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hk_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hk_ai2d_output_tensor)

# 手掌关键点检测 kpu 获得 kmodel 输出
def hk_kpu_get_output():
    with ScopedTiming("hk_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌关键点检测 kpu 运行
def hk_kpu_run(kpu_obj,rgb888p_img, x, y, w, h):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hk_kpu_pre_process(rgb888p_img, x, y, w, h)
    # (2)手掌关键点检测 kpu 运行
    with ScopedTiming("hk_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌关键点检测 ai2d 资源
    hk_ai2d_release()
    # (4)获取手掌关键点检测 kpu 输出
    results = hk_kpu_get_output()
    # (5)返回手掌关键点检测结果
    return results

# 手掌关键点检测 kpu 释放内存
def hk_kpu_deinit():
    with ScopedTiming("hk_kpu_deinit",debug_mode > 0):
        if 'hk_ai2d' in globals():
            global hk_ai2d
            del hk_ai2d
        if 'hk_ai2d_output_tensor' in globals():
            global hk_ai2d_output_tensor
            del hk_ai2d_output_tensor

# 隔空缩放剪切 ai2d 初始化
def space_ai2d_init():
    with ScopedTiming("space_ai2d_init",debug_mode > 0):
        global space_ai2d
        space_ai2d = nn.ai2d()
        space_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.RGB_packed,
                                       np.uint8, np.uint8)

# 隔空缩放剪切 ai2d 运行
def space_ai2d_run(rgb888p_img, x, y, w, h, out_w, out_h):
    with ScopedTiming("space_ai2d_run",debug_mode > 0):
        global space_ai2d,space_ai2d_input_tensor,space_ai2d_output_tensor,space_draw_ai2d_release
        space_draw_ai2d_release = True
        space_ai2d_input = rgb888p_img.to_numpy_ref()
        space_ai2d_input_tensor = nn.from_numpy(space_ai2d_input)

        space_ai2d.set_crop_param(True, x, y, w, h)
        space_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )

        data = np.ones((1,out_h, out_w,3), dtype=np.uint8)
        space_ai2d_output_tensor = nn.from_numpy(data)

        global space_ai2d_builder
        space_ai2d_builder = space_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,out_h, out_w,3])
        space_ai2d_builder.run(space_ai2d_input_tensor, space_ai2d_output_tensor)

        space_np_out = space_ai2d_output_tensor.to_numpy()
        return space_np_out

# 隔空缩放剪切 ai2d 释放内存
def space_ai2d_release(re_ai2d):
    with ScopedTiming("space_ai2d_release",debug_mode > 0):
        global space_ai2d_input_tensor,space_ai2d_output_tensor,space_ai2d_builder,space_draw_ai2d_release,space_ai2d
        if (space_draw_ai2d_release):
            del space_ai2d_input_tensor
            del space_ai2d_output_tensor
            del space_ai2d_builder
            space_draw_ai2d_release = False
        if (re_ai2d):
            del space_ai2d

#media_utils.py
global draw_img,osd_img,masks                               #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img, masks
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    masks = np.zeros((DISPLAY_HEIGHT,DISPLAY_WIDTH,4),dtype=np.uint8)
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888,alloc=image.ALLOC_REF,data=masks)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for space_resize.py**********
def space_resize_inference():
    print("space_resize start")
    kpu_hand_detect = hd_kpu_init(hd_kmodel_file)                       # 创建手掌检测的 kpu 对象
    kpu_hand_keypoint_detect = hk_kpu_init(hk_kmodel_file)              # 创建手掌关键点检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display
    space_ai2d_init()                                                   # 初始化 隔空缩放剪切 ai2d 对象

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)

        global draw_img,osd_img
        first_start = True                                              # 首次手掌入镜参数
        two_point_left_x = 0                                            # 中指食指包括范围 x
        two_point_top_y = 0                                             # 中指食指包括范围 y
        two_point_mean_w = 0                                            # 中指食指首次入镜包括范围 w
        two_point_mean_h = 0                                            # 中指食指首次入镜包括范围 h
        two_point_crop_w = 0                                            # 中指食指包括范围 w
        two_point_crop_h = 0                                            # 中指食指包括范围 h
        osd_plot_x = 0                                                  # osd 画缩放图起始点 x
        osd_plot_y = 0                                                  # osd 画缩放图起始点 y
        ori_new_ratio = 0                                               # 缩放比例
        new_resize_w = 0                                                # 缩放后 w
        new_resize_h = 0                                                # 缩放后 h
        crop_area = 0                                                   # 剪切区域
        rect_frame_x = 0                                                # osd绘画起始点 x
        rect_frame_y = 0                                                # osd绘画起始点 y

        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    two_point = np.zeros((4),dtype=np.int16)
                    dets_no_pro = hd_kpu_run(kpu_hand_detect,rgb888p_img)                      # 执行手掌检测 kpu 运行 以及 后处理过程
                    draw_img.clear()

                    dets = []
                    for det_box in dets_no_pro:
                        if det_box[4] < OUT_RGB888P_WIDTH - 10 :
                            dets.append(det_box)

                    if (len(dets)==1):
                        for det_box in dets:
                            x1, y1, x2, y2 = int(det_box[2]),int(det_box[3]),int(det_box[4]),int(det_box[5])
                            w = int(x2 - x1)
                            h = int(y2 - y1)

                            if (h<(0.1*OUT_RGB888P_HEIGHT)):
                                continue
                            if (w<(0.25*OUT_RGB888P_WIDTH) and ((x1<(0.03*OUT_RGB888P_WIDTH)) or (x2>(0.97*OUT_RGB888P_WIDTH)))):
                                continue
                            if (w<(0.15*OUT_RGB888P_WIDTH) and ((x1<(0.01*OUT_RGB888P_WIDTH)) or (x2>(0.99*OUT_RGB888P_WIDTH)))):
                                continue

                            length = max(w,h)/2
                            cx = (x1+x2)/2
                            cy = (y1+y2)/2
                            ratio_num = 1.26*length

                            x1_kp = int(max(0,cx-ratio_num))
                            y1_kp = int(max(0,cy-ratio_num))
                            x2_kp = int(min(OUT_RGB888P_WIDTH-1, cx+ratio_num))
                            y2_kp = int(min(OUT_RGB888P_HEIGHT-1, cy+ratio_num))
                            w_kp = int(x2_kp - x1_kp + 1)
                            h_kp = int(y2_kp - y1_kp + 1)

                            hk_results = hk_kpu_run(kpu_hand_keypoint_detect,rgb888p_img, x1_kp, y1_kp, w_kp, h_kp)     # 执行手掌关键点检测 kpu 运行 以及 后处理过程

                            results_show = np.zeros(hk_results[0].shape,dtype=np.int16)
                            results_show[0::2] = hk_results[0][0::2] * w_kp + x1_kp
                            results_show[1::2] = hk_results[0][1::2] * h_kp + y1_kp

                            two_point[0] = results_show[8]
                            two_point[1] = results_show[9]
                            two_point[2] = results_show[16+8]
                            two_point[3] = results_show[16+9]

                        if (first_start):
                            if (two_point[0] > 0 and two_point[0] < OUT_RGB888P_WIDTH and two_point[2] > 0 and two_point[2] < OUT_RGB888P_WIDTH and two_point[1] > 0 and two_point[1] < OUT_RGB888P_HEIGHT and two_point[3] > 0 and two_point[3] < OUT_RGB888P_HEIGHT):
                                two_point_mean_w = np.sqrt(pow(two_point[0] - two_point[2],2) + pow(two_point[1] - two_point[3],2))*0.8
                                two_point_mean_h = np.sqrt(pow(two_point[0] - two_point[2],2) + pow(two_point[1] - two_point[3],2))*0.8
                                first_start = False
                        else:
                            two_point_left_x = int(max((two_point[0] + two_point[2]) / 2 - two_point_mean_w / 2, 0))
                            two_point_top_y = int(max((two_point[1] + two_point[3]) / 2 - two_point_mean_h / 2, 0))
                            two_point_crop_w = int(min(min((two_point[0] + two_point[2]) / 2 - two_point_mean_w / 2 + two_point_mean_w , two_point_mean_w), OUT_RGB888P_WIDTH - ((two_point[0] + two_point[2]) / 2 - two_point_mean_w / 2)))
                            two_point_crop_h = int(min(min((two_point[1] + two_point[3]) / 2 - two_point_mean_h / 2 + two_point_mean_h , two_point_mean_h), OUT_RGB888P_HEIGHT - ((two_point[1] + two_point[3]) / 2 - two_point_mean_h / 2)))

                            ori_new_ratio = np.sqrt(pow((two_point[0] - two_point[2]),2) + pow((two_point[1] - two_point[3]),2))*0.8 / two_point_mean_w

                            new_resize_w = min(int(two_point_crop_w * ori_new_ratio / OUT_RGB888P_WIDTH * DISPLAY_WIDTH),600)
                            new_resize_h = min(int(two_point_crop_h * ori_new_ratio / OUT_RGB888P_HEIGHT * DISPLAY_HEIGHT),600)

                            rect_frame_x = int(two_point_left_x * 1.0 / OUT_RGB888P_WIDTH * DISPLAY_WIDTH)
                            rect_frame_y = int(two_point_top_y * 1.0 / OUT_RGB888P_HEIGHT * DISPLAY_HEIGHT)

                            draw_w = min(new_resize_w,DISPLAY_WIDTH-rect_frame_x-1)
                            draw_h = min(new_resize_h,DISPLAY_HEIGHT-rect_frame_y-1)

                            space_np_out = space_ai2d_run(rgb888p_img, two_point_left_x, two_point_top_y, two_point_crop_w, two_point_crop_h, new_resize_w, new_resize_h)      # 运行 隔空缩放检测 ai2d
                            global masks
                            masks[rect_frame_y:rect_frame_y + draw_h,rect_frame_x:rect_frame_x + draw_w,0] = 255
                            masks[rect_frame_y:rect_frame_y + draw_h,rect_frame_x:rect_frame_x + draw_w,1:4] = space_np_out[0][0:draw_h,0:draw_w,:]
                            space_ai2d_release(False)                       # 释放 隔空缩放检测 ai2d 相关对象


                            draw_img.draw_rectangle(rect_frame_x, rect_frame_y, new_resize_w, new_resize_h, color=(255, 0, 255, 0),thickness = 4)
                    else:
                        draw_img.draw_string( 300 , 500, "Must have one hand !", color=(255,255,0,0), scale=7)
                        first_start = True

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)         # camera 释放图像

                if (count > 5):
                    gc.collect()
                    count = 0
                else:
                    count += 1

                draw_img.copy_to(osd_img)
                display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        camera_stop(CAM_DEV_ID_0)                                       # 停止 camera
        display_deinit()                                                # 释放 display
        space_ai2d_release(True)                                        # 释放 隔空缩放检测 ai2d 相关对象
        hd_kpu_deinit()                                  # 释放手掌检测 kpu
        hk_kpu_deinit()                         # 释放手掌关键点检测 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_hand_detect
        del kpu_hand_keypoint_detect
        
        if 'draw_img' in globals():
            global draw_img
            del draw_img
        if 'masks' in globals():
            global masks
            del masks
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                            # 释放 整个media

    print("space_resize end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    space_resize_inference()
```

### 15.拼图游戏

```python
import aicube                   #aicube模块，封装检测分割等任务相关后处理
from media.camera import *      #摄像头模块
from media.display import *     #显示模块
from media.media import *       #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区

import nncase_runtime as nn     #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np         #类似python numpy操作，但也会有一些接口不同

import time                     #时间统计
import image                    #图像模块，主要用于读取、图像绘制元素（框、点等）等操作

import gc                       #垃圾回收模块
import random
import os, sys                           #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

##ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

#--------for hand detection----------
#kmodel输入shape
hd_kmodel_input_shape = (1,3,512,512)                           # 手掌检测kmodel输入分辨率

#kmodel相关参数设置
confidence_threshold = 0.2                                      # 手掌检测阈值，用于过滤roi
nms_threshold = 0.5                                             # 手掌检测框阈值，用于过滤重复roi
hd_kmodel_frame_size = [512,512]                                # 手掌检测输入图片尺寸
hd_frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGHT]           # 手掌检测直接输入图片尺寸
strides = [8,16,32]                                             # 输出特征图的尺寸与输入图片尺寸的比
num_classes = 1                                                 # 手掌检测模型输出类别数
nms_option = False                                              # 是否所有检测框一起做NMS，False则按照不同的类分别应用NMS

level = 3                                                       # 游戏级别 目前只支持设置为 3


root_dir = '/sdcard/app/tests/'
hd_kmodel_file = root_dir + "kmodel/hand_det.kmodel"      # 手掌检测kmodel文件的路径
anchors = [26,27, 53,52, 75,71, 80,99, 106,82, 99,134, 140,113, 161,172, 245,276]   #anchor设置

#--------for hand keypoint detection----------
#kmodel输入shape
hk_kmodel_input_shape = (1,3,256,256)                           # 手掌关键点检测kmodel输入分辨率

#kmodel相关参数设置
hk_kmodel_frame_size = [256,256]                                # 手掌关键点检测输入图片尺寸
hk_kmodel_file = root_dir + 'kmodel/handkp_det.kmodel'    # 手掌关键点检测kmodel文件的路径

debug_mode = 0                                                  # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                                   # 定义全局的 kpu 对象
global hd_ai2d,hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder   # 定义手掌检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor,hk_ai2d_builder   # 定义手掌关键点检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder


#-------hand detect--------:
# 手掌检测ai2d 初始化
def hd_ai2d_init():
    with ScopedTiming("hd_ai2d_init",debug_mode > 0):
        global hd_ai2d
        global hd_ai2d_builder
        global hd_ai2d_output_tensor
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = hd_kmodel_frame_size[0]
        height = hd_kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        # init kpu and load kmodel
        hd_ai2d = nn.ai2d()
        hd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        hd_ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        hd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        hd_ai2d_builder = hd_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,height,width])
        data = np.ones(hd_kmodel_input_shape, dtype=np.uint8)
        hd_ai2d_output_tensor = nn.from_numpy(data)

# 手掌检测 ai2d 运行
def hd_ai2d_run(rgb888p_img):
    with ScopedTiming("hd_ai2d_run",debug_mode > 0):
        global hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder
        hd_ai2d_input = rgb888p_img.to_numpy_ref()
        hd_ai2d_input_tensor = nn.from_numpy(hd_ai2d_input)

        hd_ai2d_builder.run(hd_ai2d_input_tensor, hd_ai2d_output_tensor)

# 手掌检测 ai2d 释放内存
def hd_ai2d_release():
    with ScopedTiming("hd_ai2d_release",debug_mode > 0):
        global hd_ai2d_input_tensor
        del hd_ai2d_input_tensor

# 手掌检测 kpu 初始化
def hd_kpu_init(hd_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hd_kpu_init",debug_mode > 0):
        hd_kpu_obj = nn.kpu()
        hd_kpu_obj.load_kmodel(hd_kmodel_file)

        hd_ai2d_init()
        return hd_kpu_obj

# 手掌检测 kpu 输入预处理
def hd_kpu_pre_process(rgb888p_img):
    hd_ai2d_run(rgb888p_img)
    with ScopedTiming("hd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hd_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hd_ai2d_output_tensor)

# 手掌检测 kpu 获得 kmodel 输出
def hd_kpu_get_output():
    with ScopedTiming("hd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌检测 kpu 运行
def hd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hd_kpu_pre_process(rgb888p_img)
     # (2)手掌检测 kpu 运行
    with ScopedTiming("hd_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌检测 ai2d 资源
    hd_ai2d_release()
    # (4)获取手掌检测 kpu 输出
    results = hd_kpu_get_output()
    # (5)手掌检测 kpu 结果后处理
    dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], hd_kmodel_frame_size, hd_frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)
    # (6)返回手掌检测结果
    return dets

# 手掌检测 kpu 释放内存
def hd_kpu_deinit():
    with ScopedTiming("hd_kpu_deinit",debug_mode > 0):
        if 'hd_ai2d' in globals():
            global hd_ai2d
            del hd_ai2d
        if 'hd_ai2d_output_tensor' in globals():
            global hd_ai2d_output_tensor
            del hd_ai2d_output_tensor
        if 'hd_ai2d_builder' in globals():
            global hd_ai2d_builder
            del hd_ai2d_builder

#-------hand keypoint detection------:
# 手掌关键点检测 ai2d 初始化
def hk_ai2d_init():
    with ScopedTiming("hk_ai2d_init",debug_mode > 0):
        global hk_ai2d, hk_ai2d_output_tensor
        hk_ai2d = nn.ai2d()
        hk_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        data = np.ones(hk_kmodel_input_shape, dtype=np.uint8)
        hk_ai2d_output_tensor = nn.from_numpy(data)

# 手掌关键点检测 ai2d 运行
def hk_ai2d_run(rgb888p_img, x, y, w, h):
    with ScopedTiming("hk_ai2d_run",debug_mode > 0):
        global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor
        hk_ai2d_input = rgb888p_img.to_numpy_ref()
        hk_ai2d_input_tensor = nn.from_numpy(hk_ai2d_input)

        hk_ai2d.set_crop_param(True, x, y, w, h)
        hk_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )

        global hk_ai2d_builder
        hk_ai2d_builder = hk_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,hk_kmodel_frame_size[1],hk_kmodel_frame_size[0]])
        hk_ai2d_builder.run(hk_ai2d_input_tensor, hk_ai2d_output_tensor)

# 手掌关键点检测 ai2d 释放内存
def hk_ai2d_release():
    with ScopedTiming("hk_ai2d_release",debug_mode > 0):
        global hk_ai2d_input_tensor,hk_ai2d_builder
        del hk_ai2d_input_tensor
        del hk_ai2d_builder

# 手掌关键点检测 kpu 初始化
def hk_kpu_init(hk_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hk_kpu_init",debug_mode > 0):
        hk_kpu_obj = nn.kpu()
        hk_kpu_obj.load_kmodel(hk_kmodel_file)

        hk_ai2d_init()
        return hk_kpu_obj

# 手掌关键点检测 kpu 输入预处理
def hk_kpu_pre_process(rgb888p_img, x, y, w, h):
    hk_ai2d_run(rgb888p_img, x, y, w, h)
    with ScopedTiming("hk_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hk_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hk_ai2d_output_tensor)

# 手掌关键点检测 kpu 获得 kmodel 输出
def hk_kpu_get_output():
    with ScopedTiming("hk_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌关键点检测 kpu 运行
def hk_kpu_run(kpu_obj,rgb888p_img, x, y, w, h):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hk_kpu_pre_process(rgb888p_img, x, y, w, h)
    # (2)手掌关键点检测 kpu 运行
    with ScopedTiming("hk_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌关键点检测 ai2d 资源
    hk_ai2d_release()
    # (4)获取手掌关键点检测 kpu 输出
    results = hk_kpu_get_output()
    # (5)返回手掌关键点检测结果
    return results

# 手掌关键点检测 kpu 释放内存
def hk_kpu_deinit():
    with ScopedTiming("hk_kpu_deinit",debug_mode > 0):
        if 'hk_ai2d' in globals():
            global hk_ai2d
            del hk_ai2d
        if 'hk_ai2d_output_tensor' in globals():
            global hk_ai2d_output_tensor
            del hk_ai2d_output_tensor

#media_utils.py
global draw_img,osd_img,masks                               #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img, masks
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    masks = np.zeros((DISPLAY_HEIGHT,DISPLAY_WIDTH,4),dtype=np.uint8)
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888,alloc=image.ALLOC_REF,data=masks)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for puzzle_game.py**********
def puzzle_game_inference():
    print("puzzle_game_inference start")
    kpu_hand_detect = hd_kpu_init(hd_kmodel_file)                       # 创建手掌检测的 kpu 对象
    kpu_hand_keypoint_detect = hk_kpu_init(hk_kmodel_file)              # 创建手掌关键点检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)

        global draw_img,osd_img
        puzzle_width = DISPLAY_HEIGHT                                   # 设定 拼图宽
        puzzle_height = DISPLAY_HEIGHT                                  # 设定 拼图高
        puzzle_ori_width = DISPLAY_WIDTH - puzzle_width - 50            # 设定 原始拼图宽
        puzzle_ori_height = DISPLAY_WIDTH - puzzle_height - 50          # 设定 原始拼图高

        every_block_width = int(puzzle_width/level)                     # 设定 拼图块宽
        every_block_height = int(puzzle_height/level)                   # 设定 拼图块高
        ori_every_block_width = int(puzzle_ori_width/level)             # 设定 原始拼图宽
        ori_every_block_height = int(puzzle_ori_height/level)           # 设定 原始拼图高
        ratio_num = every_block_width/360.0                             # 字体比例
        blank_x = 0                                                     # 空白块 角点x
        blank_y = 0                                                     # 空白块 角点y
        direction_vec = [-1,1,-1,1]                                     # 空白块四种移动方向

        exact_division_x = 0                                            # 交换块 角点x
        exact_division_y = 0                                            # 交换块 角点y
        distance_tow_points = DISPLAY_WIDTH                             # 两手指距离
        distance_thred = every_block_width*0.4                          # 两手指距离阈值

        move_mat = np.zeros((every_block_height,every_block_width,4),dtype=np.uint8)

        osd_frame_tmp = np.zeros((DISPLAY_HEIGHT,DISPLAY_WIDTH,4),dtype=np.uint8)
        osd_frame_tmp_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888,alloc=image.ALLOC_REF,data=osd_frame_tmp)
        osd_frame_tmp[0:puzzle_height,0:puzzle_width,3] = 100
        osd_frame_tmp[0:puzzle_height,0:puzzle_width,2] = 150
        osd_frame_tmp[0:puzzle_height,0:puzzle_width,1] = 130
        osd_frame_tmp[0:puzzle_height,0:puzzle_width,0] = 127
        osd_frame_tmp[(1080-puzzle_ori_height)//2:(1080-puzzle_ori_height)//2+puzzle_ori_width,puzzle_width+25:puzzle_width+25+puzzle_ori_height,3] = 100
        osd_frame_tmp[(1080-puzzle_ori_height)//2:(1080-puzzle_ori_height)//2+puzzle_ori_width,puzzle_width+25:puzzle_width+25+puzzle_ori_height,2] = 150
        osd_frame_tmp[(1080-puzzle_ori_height)//2:(1080-puzzle_ori_height)//2+puzzle_ori_width,puzzle_width+25:puzzle_width+25+puzzle_ori_height,1] = 130
        osd_frame_tmp[(1080-puzzle_ori_height)//2:(1080-puzzle_ori_height)//2+puzzle_ori_width,puzzle_width+25:puzzle_width+25+puzzle_ori_height,0] = 127
        for i in range(level*level):
            osd_frame_tmp_img.draw_rectangle((i%level)*every_block_width,(i//level)*every_block_height,every_block_width,every_block_height,(255,0,0,0),5)
            osd_frame_tmp_img.draw_string((i%level)*every_block_width + 55,(i//level)*every_block_height + 45,str(i),(255,0,0,255),30*ratio_num)
            osd_frame_tmp_img.draw_rectangle(puzzle_width+25 + (i%level)*ori_every_block_width,(1080-puzzle_ori_height)//2 + (i//level)*ori_every_block_height,ori_every_block_width,ori_every_block_height,(255,0,0,0),5)
            osd_frame_tmp_img.draw_string(puzzle_width+25 + (i%level)*ori_every_block_width + 50,(1080-puzzle_ori_height)//2 + (i//level)*ori_every_block_height + 25,str(i),(255,0,0,255),20*ratio_num)
        osd_frame_tmp[0:every_block_height,0:every_block_width,3] = 114
        osd_frame_tmp[0:every_block_height,0:every_block_width,2] = 114
        osd_frame_tmp[0:every_block_height,0:every_block_width,1] = 114
        osd_frame_tmp[0:every_block_height,0:every_block_width,0] = 220

        for i in range(level*10):
            k230_random = int(random.random() * 100) % 4
            blank_x_tmp = blank_x
            blank_y_tmp = blank_y
            if (k230_random < 2):
                blank_x_tmp = blank_x + direction_vec[k230_random]
            else:
                blank_y_tmp = blank_y + direction_vec[k230_random]

            if ((blank_x_tmp >= 0 and blank_x_tmp < level) and (blank_y_tmp >= 0 and blank_y_tmp < level) and (abs(blank_x - blank_x_tmp) <= 1 and abs(blank_y - blank_y_tmp) <= 1)):
                move_rect = [blank_x_tmp*every_block_width,blank_y_tmp*every_block_height,every_block_width,every_block_height]
                blank_rect = [blank_x*every_block_width,blank_y*every_block_height,every_block_width,every_block_height]

                move_mat[:] = osd_frame_tmp[move_rect[1]:move_rect[1]+move_rect[3],move_rect[0]:move_rect[0]+move_rect[2],:]
                osd_frame_tmp[move_rect[1]:move_rect[1]+move_rect[3],move_rect[0]:move_rect[0]+move_rect[2],:] = osd_frame_tmp[blank_rect[1]:blank_rect[1]+blank_rect[3],blank_rect[0]:blank_rect[0]+blank_rect[2],:]
                osd_frame_tmp[blank_rect[1]:blank_rect[1]+blank_rect[3],blank_rect[0]:blank_rect[0]+blank_rect[2],:] = move_mat[:]

                blank_x = blank_x_tmp
                blank_y = blank_y_tmp

        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    two_point = np.zeros((4),dtype=np.int16)
                    dets_no_pro = hd_kpu_run(kpu_hand_detect,rgb888p_img)                      # 执行手掌检测 kpu 运行 以及 后处理过程
                    draw_img.clear()

                    osd_frame_tmp_img.copy_to(draw_img)

                    dets = []
                    for det_box in dets_no_pro:
                        if det_box[4] < OUT_RGB888P_WIDTH - 10 :
                            dets.append(det_box)

                    if (len(dets)==1):
                        for det_box in dets:
                            x1, y1, x2, y2 = int(det_box[2]),int(det_box[3]),int(det_box[4]),int(det_box[5])
                            w = int(x2 - x1)
                            h = int(y2 - y1)

                            if (h<(0.1*OUT_RGB888P_HEIGHT)):
                                continue
                            if (w<(0.25*OUT_RGB888P_WIDTH) and ((x1<(0.03*OUT_RGB888P_WIDTH)) or (x2>(0.97*OUT_RGB888P_WIDTH)))):
                                continue
                            if (w<(0.15*OUT_RGB888P_WIDTH) and ((x1<(0.01*OUT_RGB888P_WIDTH)) or (x2>(0.99*OUT_RGB888P_WIDTH)))):
                                continue

                            length = max(w,h)/2
                            cx = (x1+x2)/2
                            cy = (y1+y2)/2
                            ratio_num = 1.26*length

                            x1_kp = int(max(0,cx-ratio_num))
                            y1_kp = int(max(0,cy-ratio_num))
                            x2_kp = int(min(OUT_RGB888P_WIDTH-1, cx+ratio_num))
                            y2_kp = int(min(OUT_RGB888P_HEIGHT-1, cy+ratio_num))
                            w_kp = int(x2_kp - x1_kp + 1)
                            h_kp = int(y2_kp - y1_kp + 1)

                            hk_results = hk_kpu_run(kpu_hand_keypoint_detect,rgb888p_img, x1_kp, y1_kp, w_kp, h_kp)     # 执行手掌关键点检测 kpu 运行 以及 后处理过程

                            results_show = np.zeros(hk_results[0].shape,dtype=np.int16)
                            results_show[0::2] = (hk_results[0][0::2] * w_kp + x1_kp) #* DISPLAY_WIDTH // OUT_RGB888P_WIDTH
                            results_show[1::2] = (hk_results[0][1::2] * h_kp + y1_kp) #* DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT

                            two_point[0] = results_show[8+8]
                            two_point[1] = results_show[8+9]
                            two_point[2] = results_show[16+8]
                            two_point[3] = results_show[16+9]

                        if (two_point[1] <= OUT_RGB888P_WIDTH):
                            distance_tow_points = np.sqrt(pow((two_point[0]-two_point[2]),2) + pow((two_point[1] - two_point[3]),2))* 1.0 / OUT_RGB888P_WIDTH * DISPLAY_WIDTH
                            exact_division_x = int((two_point[0] * 1.0 / OUT_RGB888P_WIDTH * DISPLAY_WIDTH)//every_block_width)
                            exact_division_y = int((two_point[1] * 1.0 / OUT_RGB888P_HEIGHT * DISPLAY_HEIGHT)//every_block_height)


                            if (distance_tow_points < distance_thred and exact_division_x >= 0 and exact_division_x < level and exact_division_y >= 0 and exact_division_y < level):
                                if (abs(blank_x - exact_division_x) == 1 and abs(blank_y - exact_division_y) == 0):
                                    move_rect = [exact_division_x*every_block_width,exact_division_y*every_block_height,every_block_width,every_block_height]
                                    blank_rect = [blank_x*every_block_width,blank_y*every_block_height,every_block_width,every_block_height]

                                    move_mat[:] = osd_frame_tmp[move_rect[1]:move_rect[1]+move_rect[3],move_rect[0]:move_rect[0]+move_rect[2],:]
                                    osd_frame_tmp[move_rect[1]:move_rect[1]+move_rect[3],move_rect[0]:move_rect[0]+move_rect[2],:] = osd_frame_tmp[blank_rect[1]:blank_rect[1]+blank_rect[3],blank_rect[0]:blank_rect[0]+blank_rect[2],:]
                                    osd_frame_tmp[blank_rect[1]:blank_rect[1]+blank_rect[3],blank_rect[0]:blank_rect[0]+blank_rect[2],:] = move_mat[:]

                                    blank_x = exact_division_x
                                elif (abs(blank_y - exact_division_y) == 1 and abs(blank_x - exact_division_x) == 0):
                                    move_rect = [exact_division_x*every_block_width,exact_division_y*every_block_height,every_block_width,every_block_height]
                                    blank_rect = [blank_x*every_block_width,blank_y*every_block_height,every_block_width,every_block_height]

                                    move_mat[:] = osd_frame_tmp[move_rect[1]:move_rect[1]+move_rect[3],move_rect[0]:move_rect[0]+move_rect[2],:]
                                    osd_frame_tmp[move_rect[1]:move_rect[1]+move_rect[3],move_rect[0]:move_rect[0]+move_rect[2],:] = osd_frame_tmp[blank_rect[1]:blank_rect[1]+blank_rect[3],blank_rect[0]:blank_rect[0]+blank_rect[2],:]
                                    osd_frame_tmp[blank_rect[1]:blank_rect[1]+blank_rect[3],blank_rect[0]:blank_rect[0]+blank_rect[2],:] = move_mat[:]

                                    blank_y = exact_division_y

                                osd_frame_tmp_img.copy_to(draw_img)
                                x1 = int(two_point[0] * 1.0 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                                y1 = int(two_point[1] * 1.0 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)
                                draw_img.draw_circle(x1, y1, 1, color=(255, 0, 255, 255),thickness=4,fill=False)
                            else:
                                osd_frame_tmp_img.copy_to(draw_img)
                                x1 = int(two_point[0] * 1.0 * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                                y1 = int(two_point[1] * 1.0 * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)
                                draw_img.draw_circle(x1, y1, 1, color=(255, 255, 255, 0),thickness=4,fill=False)
                    else:
                        draw_img.draw_string( 300 , 500, "Must have one hand !", color=(255,255,0,0), scale=7)
                        first_start = True
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)         # camera 释放图像

                if (count > 5):
                    gc.collect()
                    count = 0
                else:
                    count += 1

            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        camera_stop(CAM_DEV_ID_0)                                       # 停止 camera
        display_deinit()                                                # 释放 display
        hd_kpu_deinit()                                                 # 释放手掌检测 kpu
        hk_kpu_deinit()                                                 # 释放手掌关键点检测 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_hand_detect
        del kpu_hand_keypoint_detect

        if 'draw_img' in globals():
            global draw_img
            del draw_img
        if 'masks' in globals():
            global masks
            del masks
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                            # 释放 整个media

    print("puzzle_game_inference end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    puzzle_game_inference()
```

### 16.基于关键点的手势识别

```python
import aicube                   #aicube模块，封装检测分割等任务相关后处理
from media.camera import *      #摄像头模块
from media.display import *     #显示模块
from media.media import *       #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区

import nncase_runtime as nn     #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np         #类似python numpy操作，但也会有一些接口不同

import time                     #时间统计
import image                    #图像模块，主要用于读取、图像绘制元素（框、点等）等操作

import gc                       #垃圾回收模块
import os, sys                  #操作系统接口模块

##config.py
#display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

##ai原图分辨率输入
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)
OUT_RGB888P_HEIGHT = 1080

root_dir = '/sdcard/app/tests/'

#--------for hand detection----------
#kmodel输入shape
hd_kmodel_input_shape = (1,3,512,512)                               # 手掌检测kmodel输入分辨率

#kmodel相关参数设置
confidence_threshold = 0.2                                          # 手掌检测阈值，用于过滤roi
nms_threshold = 0.5                                                 # 手掌检测框阈值，用于过滤重复roi
hd_kmodel_frame_size = [512,512]                                    # 手掌检测输入图片尺寸
hd_frame_size = [OUT_RGB888P_WIDTH,OUT_RGB888P_HEIGHT]              # 手掌检测直接输入图片尺寸
strides = [8,16,32]                                                 # 输出特征图的尺寸与输入图片尺寸的比
num_classes = 1                                                     # 手掌检测模型输出类别数
nms_option = False                                                  # 是否所有检测框一起做NMS，False则按照不同的类分别应用NMS

hd_kmodel_file = root_dir + 'kmodel/hand_det.kmodel'                # 手掌检测kmodel文件的路径
anchors = [26,27, 53,52, 75,71, 80,99, 106,82, 99,134, 140,113, 161,172, 245,276]   #anchor设置

#--------for hand keypoint detection----------
#kmodel输入shape
hk_kmodel_input_shape = (1,3,256,256)                               # 手掌关键点检测kmodel输入分辨率

#kmodel相关参数设置
hk_kmodel_frame_size = [256,256]                                    # 手掌关键点检测输入图片尺寸
hk_kmodel_file = root_dir + 'kmodel/handkp_det.kmodel'              # 手掌关键点检测kmodel文件的路径

debug_mode = 0                                                      # debug模式 大于0（调试）、 反之 （不调试）

#scoped_timing.py 用于debug模式输出程序块运行时间
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#ai_utils.py
global current_kmodel_obj                                                   # 定义全局的 kpu 对象
global hd_ai2d,hd_ai2d_input_tensor,hd_ai2d_output_tensor,hd_ai2d_builder   # 定义手掌检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder
global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor,hk_ai2d_builder   # 定义手掌关键点检测全局 ai2d 对象，并且定义 ai2d 的输入、输出 以及 builder

#-------hand detect--------:
# 手掌检测ai2d 初始化
def hd_ai2d_init():
    with ScopedTiming("hd_ai2d_init",debug_mode > 0):
        global hd_ai2d
        global hd_ai2d_builder
        global hd_ai2d_output_tensor
        # 计算padding值
        ori_w = OUT_RGB888P_WIDTH
        ori_h = OUT_RGB888P_HEIGHT
        width = hd_kmodel_frame_size[0]
        height = hd_kmodel_frame_size[1]
        ratiow = float(width) / ori_w
        ratioh = float(height) / ori_h
        if ratiow < ratioh:
            ratio = ratiow
        else:
            ratio = ratioh
        new_w = int(ratio * ori_w)
        new_h = int(ratio * ori_h)
        dw = float(width - new_w) / 2
        dh = float(height - new_h) / 2
        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw - 0.1))

        hd_ai2d = nn.ai2d()
        hd_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        hd_ai2d.set_pad_param(True, [0,0,0,0,top,bottom,left,right], 0, [114,114,114])
        hd_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )
        hd_ai2d_builder = hd_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,height,width])

        data = np.ones(hd_kmodel_input_shape, dtype=np.uint8)
        hd_ai2d_output_tensor = nn.from_numpy(data)

# 手掌检测 ai2d 运行
def hd_ai2d_run(rgb888p_img):
    with ScopedTiming("hd_ai2d_run",debug_mode > 0):
        global hd_ai2d_input_tensor,hd_ai2d_output_tensor, hd_ai2d_builder
        hd_ai2d_input = rgb888p_img.to_numpy_ref()
        hd_ai2d_input_tensor = nn.from_numpy(hd_ai2d_input)

        hd_ai2d_builder.run(hd_ai2d_input_tensor, hd_ai2d_output_tensor)

# 手掌检测 ai2d 释放内存
def hd_ai2d_release():
    with ScopedTiming("hd_ai2d_release",debug_mode > 0):
        global hd_ai2d_input_tensor
        del hd_ai2d_input_tensor

# 手掌检测 kpu 初始化
def hd_kpu_init(hd_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hd_kpu_init",debug_mode > 0):
        hd_kpu_obj = nn.kpu()
        hd_kpu_obj.load_kmodel(hd_kmodel_file)

        hd_ai2d_init()
        return hd_kpu_obj

# 手掌检测 kpu 输入预处理
def hd_kpu_pre_process(rgb888p_img):
    hd_ai2d_run(rgb888p_img)
    with ScopedTiming("hd_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hd_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hd_ai2d_output_tensor)

# 手掌检测 kpu 获得 kmodel 输出
def hd_kpu_get_output():
    with ScopedTiming("hd_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            result = result.reshape((result.shape[0]*result.shape[1]*result.shape[2]*result.shape[3]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌检测 kpu 运行
def hd_kpu_run(kpu_obj,rgb888p_img):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hd_kpu_pre_process(rgb888p_img)
    # (2)手掌检测 kpu 运行
    with ScopedTiming("hd_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌检测 ai2d 资源
    hd_ai2d_release()
    # (4)获取手掌检测 kpu 输出
    results = hd_kpu_get_output()
    # (5)手掌检测 kpu 结果后处理
    dets = aicube.anchorbasedet_post_process( results[0], results[1], results[2], hd_kmodel_frame_size, hd_frame_size, strides, num_classes, confidence_threshold, nms_threshold, anchors, nms_option)  # kpu结果后处理
    # (6)返回手掌检测结果
    return dets

# 手掌检测 kpu 释放内存
def hd_kpu_deinit():
    with ScopedTiming("hd_kpu_deinit",debug_mode > 0):
        if 'hd_ai2d' in globals():                             #删除hd_ai2d变量，释放对它所引用对象的内存引用
            global hd_ai2d
            del hd_ai2d
        if 'hd_ai2d_output_tensor' in globals():               #删除hd_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global hd_ai2d_output_tensor
            del hd_ai2d_output_tensor
        if 'hd_ai2d_builder' in globals():                     #删除hd_ai2d_builder变量，释放对它所引用对象的内存引用
            global hd_ai2d_builder
            del hd_ai2d_builder

#-------hand keypoint detection------:
# 手掌关键点检测 ai2d 初始化
def hk_ai2d_init():
    with ScopedTiming("hk_ai2d_init",debug_mode > 0):
        global hk_ai2d, hk_ai2d_output_tensor
        hk_ai2d = nn.ai2d()
        hk_ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)
        data = np.ones(hk_kmodel_input_shape, dtype=np.uint8)
        hk_ai2d_output_tensor = nn.from_numpy(data)

# 手掌关键点检测 ai2d 运行
def hk_ai2d_run(rgb888p_img, x, y, w, h):
    with ScopedTiming("hk_ai2d_run",debug_mode > 0):
        global hk_ai2d,hk_ai2d_input_tensor,hk_ai2d_output_tensor
        hk_ai2d_input = rgb888p_img.to_numpy_ref()
        hk_ai2d_input_tensor = nn.from_numpy(hk_ai2d_input)

        hk_ai2d.set_crop_param(True, x, y, w, h)
        hk_ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel )

        global hk_ai2d_builder
        hk_ai2d_builder = hk_ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], [1,3,hk_kmodel_frame_size[1],hk_kmodel_frame_size[0]])
        hk_ai2d_builder.run(hk_ai2d_input_tensor, hk_ai2d_output_tensor)

# 手掌关键点检测 ai2d 释放内存
def hk_ai2d_release():
    with ScopedTiming("hk_ai2d_release",debug_mode > 0):
        global hk_ai2d_input_tensor, hk_ai2d_builder
        del hk_ai2d_input_tensor
        del hk_ai2d_builder

# 手掌关键点检测 kpu 初始化
def hk_kpu_init(hk_kmodel_file):
    # init kpu and load kmodel
    with ScopedTiming("hk_kpu_init",debug_mode > 0):
        hk_kpu_obj = nn.kpu()
        hk_kpu_obj.load_kmodel(hk_kmodel_file)

        hk_ai2d_init()
        return hk_kpu_obj

# 手掌关键点检测 kpu 输入预处理
def hk_kpu_pre_process(rgb888p_img, x, y, w, h):
    hk_ai2d_run(rgb888p_img, x, y, w, h)
    with ScopedTiming("hk_kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,hk_ai2d_output_tensor
        # set kpu input
        current_kmodel_obj.set_input_tensor(0, hk_ai2d_output_tensor)

# 手掌关键点检测 kpu 获得 kmodel 输出
def hk_kpu_get_output():
    with ScopedTiming("hk_kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()

            result = result.reshape((result.shape[0]*result.shape[1]))
            tmp2 = result.copy()
            del result
            results.append(tmp2)
        return results

# 手掌关键点检测 kpu 输出后处理
def hk_kpu_post_process(results, x, y, w, h):
    results_show = np.zeros(results.shape,dtype=np.int16)
    results_show[0::2] = results[0::2] * w + x
    results_show[1::2] = results[1::2] * h + y
    return results_show

# 手掌关键点检测 kpu 运行
def hk_kpu_run(kpu_obj,rgb888p_img, x, y, w, h):
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # (1)原图预处理，并设置模型输入
    hk_kpu_pre_process(rgb888p_img, x, y, w, h)
    # (2)手掌关键点检测 kpu 运行
    with ScopedTiming("hk_kpu_run",debug_mode > 0):
        current_kmodel_obj.run()
    # (3)释放手掌关键点检测 ai2d 资源
    hk_ai2d_release()
    # (4)获取手掌关键点检测 kpu 输出
    results = hk_kpu_get_output()
    # (5)手掌关键点检测 kpu 结果后处理
    result = hk_kpu_post_process(results[0],x,y,w,h)
    # (6)返回手掌关键点检测结果
    return result

# 手掌关键点检测 kpu 释放内存
def hk_kpu_deinit():
    with ScopedTiming("hk_kpu_deinit",debug_mode > 0):
        if 'hk_ai2d' in globals():                                  #删除hk_ai2d变量，释放对它所引用对象的内存引用
            global hk_ai2d
            del hk_ai2d
        if 'hk_ai2d_output_tensor' in globals():                    #删除hk_ai2d_output_tensor变量，释放对它所引用对象的内存引用
            global hk_ai2d_output_tensor
            del hk_ai2d_output_tensor

# 求两个vector之间的夹角
def hk_vector_2d_angle(v1,v2):
    with ScopedTiming("hk_vector_2d_angle",debug_mode > 0):
        v1_x = v1[0]
        v1_y = v1[1]
        v2_x = v2[0]
        v2_y = v2[1]
        v1_norm = np.sqrt(v1_x * v1_x+ v1_y * v1_y)
        v2_norm = np.sqrt(v2_x * v2_x + v2_y * v2_y)
        dot_product = v1_x * v2_x + v1_y * v2_y
        cos_angle = dot_product/(v1_norm*v2_norm)
        angle = np.acos(cos_angle)*180/np.pi
        return angle

# 根据手掌关键点检测结果判断手势类别
def hk_gesture(results):
    with ScopedTiming("hk_gesture",debug_mode > 0):
        angle_list = []
        for i in range(5):
            angle = hk_vector_2d_angle([(results[0]-results[i*8+4]), (results[1]-results[i*8+5])],[(results[i*8+6]-results[i*8+8]),(results[i*8+7]-results[i*8+9])])
            angle_list.append(angle)

        thr_angle = 65.
        thr_angle_thumb = 53.
        thr_angle_s = 49.
        gesture_str = None
        if 65535. not in angle_list:
            if (angle_list[0]>thr_angle_thumb)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "fist"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]<thr_angle_s):
                gesture_str = "five"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "gun"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
                gesture_str = "love"
            elif (angle_list[0]>5)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "one"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
                gesture_str = "six"
            elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]>thr_angle):
                gesture_str = "three"
            elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "thumbUp"
            elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
                gesture_str = "yeah"

        return gesture_str

#media_utils.py
global draw_img,osd_img                                     #for display 定义全局 作图image对象
global buffer,media_source,media_sink                       #for media   定义 media 程序中的中间存储对象

#for display 初始化
def display_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

# display 释放内存
def display_deinit():
    display.deinit()

# display 作图过程 标出检测到的21个关键点并用不同颜色的线段连接
def display_draw(results, x, y, w, h):
    with ScopedTiming("display_draw",debug_mode >0):
        global draw_img,osd_img

        if results:
            results_show = np.zeros(results.shape,dtype=np.int16)
            results_show[0::2] = results[0::2] * (DISPLAY_WIDTH / OUT_RGB888P_WIDTH)
            results_show[1::2] = results[1::2] * (DISPLAY_HEIGHT / OUT_RGB888P_HEIGHT)

            for i in range(len(results_show)/2):
                draw_img.draw_circle(results_show[i*2], results_show[i*2+1], 1, color=(255, 0, 255, 0),fill=False)
            for i in range(5):
                j = i*8
                if i==0:
                    R = 255; G = 0; B = 0
                if i==1:
                    R = 255; G = 0; B = 255
                if i==2:
                    R = 255; G = 255; B = 0
                if i==3:
                    R = 0; G = 255; B = 0
                if i==4:
                    R = 0; G = 0; B = 255
                draw_img.draw_line(results_show[0], results_show[1], results_show[j+2], results_show[j+3], color=(255,R,G,B), thickness = 3)
                draw_img.draw_line(results_show[j+2], results_show[j+3], results_show[j+4], results_show[j+5], color=(255,R,G,B), thickness = 3)
                draw_img.draw_line(results_show[j+4], results_show[j+5], results_show[j+6], results_show[j+7], color=(255,R,G,B), thickness = 3)
                draw_img.draw_line(results_show[j+6], results_show[j+7], results_show[j+8], results_show[j+9], color=(255,R,G,B), thickness = 3)


#for camera 初始化
def camera_init(dev_id):
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

# camera 开启
def camera_start(dev_id):
    camera.start_stream(dev_id)

# camera 读取图像
def camera_read(dev_id):
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

# camera 图像释放
def camera_release_image(dev_id,rgb888p_img):
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

# camera 结束
def camera_stop(dev_id):
    camera.stop_stream(dev_id)

#for media 初始化
def media_init():
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化多媒体buffer
    media.buffer_init()
    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 图层1，用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 图层2，用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

# media 释放内存
def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)
    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#**********for hand_keypoint_class.py**********
def hand_keypoint_class_inference():
    print("hand_keypoint_class_test start")

    kpu_hand_detect = hd_kpu_init(hd_kmodel_file)                       # 创建手掌检测的 kpu 对象
    kpu_hand_keypoint_detect = hk_kpu_init(hk_kmodel_file)              # 创建手掌关键点检测的 kpu 对象
    camera_init(CAM_DEV_ID_0)                                           # 初始化 camera
    display_init()                                                      # 初始化 display

    try:
        media_init()

        camera_start(CAM_DEV_ID_0)
        count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total", 1):
                rgb888p_img = camera_read(CAM_DEV_ID_0)                 # 读取一帧图片

                # for rgb888planar
                if rgb888p_img.format() == image.RGBP888:
                    draw_img.clear()
                    dets = hd_kpu_run(kpu_hand_detect,rgb888p_img)                                                                # 执行手掌检测 kpu 运行 以及 后处理过程

                    for det_box in dets:
                        x1, y1, x2, y2 = det_box[2],det_box[3],det_box[4],det_box[5]
                        w = int(x2 - x1)
                        h = int(y2 - y1)

                        if (h<(0.1*OUT_RGB888P_HEIGHT)):
                            continue
                        if (w<(0.25*OUT_RGB888P_WIDTH) and ((x1<(0.03*OUT_RGB888P_WIDTH)) or (x2>(0.97*OUT_RGB888P_WIDTH)))):
                            continue
                        if (w<(0.15*OUT_RGB888P_WIDTH) and ((x1<(0.01*OUT_RGB888P_WIDTH)) or (x2>(0.99*OUT_RGB888P_WIDTH)))):
                            continue

                        w_det = int(float(x2 - x1) * DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                        h_det = int(float(y2 - y1) * DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)
                        x_det = int(x1*DISPLAY_WIDTH // OUT_RGB888P_WIDTH)
                        y_det = int(y1*DISPLAY_HEIGHT // OUT_RGB888P_HEIGHT)

                        length = max(w, h)/2
                        cx = (x1+x2)/2
                        cy = (y1+y2)/2
                        ratio_num = 1.26*length

                        x1_kp = int(max(0,cx-ratio_num))
                        y1_kp = int(max(0,cy-ratio_num))
                        x2_kp = int(min(OUT_RGB888P_WIDTH-1, cx+ratio_num))
                        y2_kp = int(min(OUT_RGB888P_HEIGHT-1, cy+ratio_num))
                        w_kp = int(x2_kp - x1_kp + 1)
                        h_kp = int(y2_kp - y1_kp + 1)

                        hk_results = hk_kpu_run(kpu_hand_keypoint_detect,rgb888p_img, x1_kp, y1_kp, w_kp, h_kp)                   # 执行手掌关键点检测 kpu 运行 以及 后处理过程
                        gesture = hk_gesture(hk_results)                                                                          # 根据关键点检测结果判断手势类别

                        draw_img.draw_rectangle(x_det, y_det, w_det, h_det, color=(255, 0, 255, 0), thickness = 2)                # 将得到的手掌检测结果 绘制到 display
                        display_draw(hk_results, x1_kp, y1_kp, w_kp, h_kp)                                                        # 将得到的手掌关键点检测结果 绘制到 display
                        draw_img.draw_string( x_det , y_det-50, " " + str(gesture), color=(255,0, 255, 0), scale=4)               # 将根据关键点检测结果判断的手势类别 绘制到 display

                camera_release_image(CAM_DEV_ID_0,rgb888p_img)          # camera 释放图像
                if (count>10):
                    gc.collect()
                    count = 0
                else:
                    count += 1

            draw_img.copy_to(osd_img)
            display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:
        camera_stop(CAM_DEV_ID_0)                                       # 停止 camera
        display_deinit()                                                # 释放 display
        hd_kpu_deinit()                                                 # 释放手掌检测 kpu
        hk_kpu_deinit()                                                 # 释放手掌关键点检测 kpu
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_hand_detect
        del kpu_hand_keypoint_detect
        gc.collect()
        nn.shrink_memory_pool()
        media_deinit()                                                  # 释放 整个media

    print("hand_keypoint_class_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    hand_keypoint_class_inference()
```

### 17.自学习

```python
import ulab.numpy as np                  #类似python numpy操作，但也会有一些接口不同
import nncase_runtime as nn              #nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
from media.camera import *               #摄像头模块
from media.display import *              #显示模块
from media.media import *                #软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import aidemo                            #aidemo模块，封装ai demo相关后处理、画图操作
import image                             #图像模块，主要用于读取、图像绘制元素（框、点等）等操作
import time                              #时间统计
import gc                                #垃圾回收模块
import os                                #基本的操作系统交互功能
import os, sys                           #操作系统接口模块

#********************for config.py********************
# display分辨率
DISPLAY_WIDTH = ALIGN_UP(1920, 16)                   # 显示宽度要求16位对齐
DISPLAY_HEIGHT = 1080

# ai原图分辨率，sensor默认出图为16:9，若需不形变原图，最好按照16:9比例设置宽高
OUT_RGB888P_WIDTH = ALIGN_UP(1920, 16)               # ai原图宽度要求16位对齐
OUT_RGB888P_HEIGHT = 1080

# kmodel参数设置
# kmodel输入shape
kmodel_input_shape = (1,3,224,224)
# kmodel其它参数设置
crop_w = 400                                         #图像剪切范围w
crop_h = 400                                         #图像剪切范围h
crop_x = OUT_RGB888P_WIDTH / 2.0 - crop_w / 2.0      #图像剪切范围x
crop_y = OUT_RGB888P_HEIGHT / 2.0 - crop_h / 2.0     #图像剪切范围y
thres = 0.5                                          #特征判别阈值
top_k = 3                                            #识别范围
categories = ['apple','banana']                      #识别类别
features = [2,2]                                     #对应类别注册特征数量
time_one = 100                                       #注册单个特征中途间隔帧数

# 文件配置
# kmodel文件配置
root_dir = '/sdcard/app/tests/'
kmodel_file = root_dir + 'kmodel/recognition.kmodel'
# 调试模型，0：不调试，>0：打印对应级别调试信息
debug_mode = 0

#********************for scoped_timing.py********************
# 时间统计类
class ScopedTiming:
    def __init__(self, info="", enable_profile=True):
        self.info = info
        self.enable_profile = enable_profile

    def __enter__(self):
        if self.enable_profile:
            self.start_time = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_profile:
            elapsed_time = time.time_ns() - self.start_time
            print(f"{self.info} took {elapsed_time / 1000000:.2f} ms")

#********************for ai_utils.py********************
# 当前kmodel
global current_kmodel_obj
# ai2d：              ai2d实例
# ai2d_input_tensor： ai2d输入
# ai2d_output_tensor：ai2d输出
# ai2d_builder：      根据ai2d参数，构建的ai2d_builder对象
global ai2d,ai2d_input_tensor,ai2d_output_tensor,ai2d_builder    #for ai2d

# 获取两个特征向量的相似度
def getSimilarity(output_vec,save_vec):
    tmp = sum(output_vec * save_vec)
    mold_out = np.sqrt(sum(output_vec * output_vec))
    mold_save = np.sqrt(sum(save_vec * save_vec))
    return tmp / (mold_out * mold_save)

# 自学习 ai2d 初始化
def ai2d_init():
    with ScopedTiming("ai2d_init",debug_mode > 0):
        global ai2d
        ai2d = nn.ai2d()
        global ai2d_output_tensor
        data = np.ones(kmodel_input_shape, dtype=np.uint8)
        ai2d_output_tensor = nn.from_numpy(data)

# 自学习 ai2d 运行
def ai2d_run(rgb888p_img):
    with ScopedTiming("ai2d_run",debug_mode > 0):
        global ai2d,ai2d_input_tensor,ai2d_output_tensor
        ai2d_input = rgb888p_img.to_numpy_ref()
        ai2d_input_tensor = nn.from_numpy(ai2d_input)

        ai2d.set_dtype(nn.ai2d_format.NCHW_FMT,
                                       nn.ai2d_format.NCHW_FMT,
                                       np.uint8, np.uint8)

        ai2d.set_crop_param(True,int(crop_x),int(crop_y),int(crop_w),int(crop_h))
        ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

        global ai2d_builder
        ai2d_builder = ai2d.build([1,3,OUT_RGB888P_HEIGHT,OUT_RGB888P_WIDTH], kmodel_input_shape)
        ai2d_builder.run(ai2d_input_tensor, ai2d_output_tensor)

# 自学习 ai2d 释放
def ai2d_release():
    with ScopedTiming("ai2d_release",debug_mode > 0):
        global ai2d_input_tensor,ai2d_builder
        del ai2d_input_tensor
        del ai2d_builder

# 自学习 kpu 初始化
def kpu_init(kmodel_file):
    # 初始化kpu对象，并加载kmodel
    with ScopedTiming("kpu_init",debug_mode > 0):
        # 初始化kpu对象
        kpu_obj = nn.kpu()
        # 加载kmodel
        kpu_obj.load_kmodel(kmodel_file)
        # 初始化ai2d
        ai2d_init()
        return kpu_obj

# 自学习 kpu 输入预处理
def kpu_pre_process(rgb888p_img):
    # 使用ai2d对原图进行预处理（crop，resize）
    ai2d_run(rgb888p_img)
    with ScopedTiming("kpu_pre_process",debug_mode > 0):
        global current_kmodel_obj,ai2d_output_tensor
        # 将ai2d输出设置为kpu输入
        current_kmodel_obj.set_input_tensor(0, ai2d_output_tensor)

# 自学习 kpu 获取输出
def kpu_get_output():
    with ScopedTiming("kpu_get_output",debug_mode > 0):
        global current_kmodel_obj
        # 获取模型输出，并将结果转换为numpy，以便进行人脸检测后处理
        results = []
        for i in range(current_kmodel_obj.outputs_size()):
            data = current_kmodel_obj.get_output_tensor(i)
            result = data.to_numpy()
            result = result.reshape(-1)
            del data
            results.append(result)
        return results

# 自学习 kpu 运行
def kpu_run(kpu_obj,rgb888p_img):
    # kpu推理
    global current_kmodel_obj
    current_kmodel_obj = kpu_obj
    # （1）原图预处理，并设置模型输入
    kpu_pre_process(rgb888p_img)
    # （2）kpu推理
    with ScopedTiming("kpu_run",debug_mode > 0):
        kpu_obj.run()
    # （3）释放ai2d资源
    ai2d_release()
    # （4）获取kpu输出
    results = kpu_get_output()

    # （5）返回输出
    return results

# 自学习 kpu 释放
def kpu_deinit():
    # kpu释放
    with ScopedTiming("kpu_deinit",debug_mode > 0):
        if 'ai2d' in globals():
            global ai2d
            del ai2d
        if 'ai2d_output_tensor' in globals():
            global ai2d_output_tensor
            del ai2d_output_tensor

#********************for media_utils.py********************
global draw_img,osd_img                                     #for display
global buffer,media_source,media_sink                       #for media

# for display，已经封装好，无需自己再实现，直接调用即可
def display_init():
    # hdmi显示初始化
    display.init(LT9611_1920X1080_30FPS)
    display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

def display_deinit():
    # 释放显示资源
    display.deinit()

#for camera，已经封装好，无需自己再实现，直接调用即可
def camera_init(dev_id):
    # camera初始化
    camera.sensor_init(dev_id, CAM_DEFAULT_SENSOR)

    # set chn0 output yuv420sp
    camera.set_outsize(dev_id, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

    # set chn2 output rgb88planar
    camera.set_outsize(dev_id, CAM_CHN_ID_2, OUT_RGB888P_WIDTH, OUT_RGB888P_HEIGHT)
    camera.set_outfmt(dev_id, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

def camera_start(dev_id):
    # camera启动
    camera.start_stream(dev_id)

def camera_read(dev_id):
    # 读取一帧图像
    with ScopedTiming("camera_read",debug_mode >0):
        rgb888p_img = camera.capture_image(dev_id, CAM_CHN_ID_2)
        return rgb888p_img

def camera_release_image(dev_id,rgb888p_img):
    # 释放一帧图像
    with ScopedTiming("camera_release_image",debug_mode >0):
        camera.release_image(dev_id, CAM_CHN_ID_2, rgb888p_img)

def camera_stop(dev_id):
    # 停止camera
    camera.stop_stream(dev_id)

#for media，已经封装好，无需自己再实现，直接调用即可
def media_init():
    # meida初始化
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4 * DISPLAY_WIDTH * DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

    media.buffer_config(config)

    global media_source, media_sink
    media_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    media_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    media.create_link(media_source, media_sink)

    # 初始化媒体buffer
    media.buffer_init()

    global buffer, draw_img, osd_img
    buffer = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # 用于画框
    draw_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # 用于拷贝画框结果，防止画框过程中发生buffer搬运
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, poolid=buffer.pool_id, alloc=image.ALLOC_VB,
                          phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr)

def media_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    if 'buffer' in globals():
        global buffer
        media.release_buffer(buffer)

    if 'media_source' in globals() and 'media_sink' in globals():
        global media_source, media_sink
        media.destroy_link(media_source, media_sink)

    media.buffer_deinit()

#********************for self_learning.py********************
def self_learning_inference():
    print("self_learning_test start")
    # kpu初始化
    kpu_self_learning = kpu_init(kmodel_file)
    # camera初始化
    camera_init(CAM_DEV_ID_0)
    # 显示初始化
    display_init()

    # 注意：将一定要将一下过程包在try中，用于保证程序停止后，资源释放完毕；确保下次程序仍能正常运行
    try:
        # 注意：媒体初始化（注：媒体初始化必须在camera_start之前，确保media缓冲区已配置完全）
        media_init()

        # 启动camera
        camera_start(CAM_DEV_ID_0)

        crop_x_osd = int(crop_x / OUT_RGB888P_WIDTH * DISPLAY_WIDTH)
        crop_y_osd = int(crop_y / OUT_RGB888P_HEIGHT * DISPLAY_HEIGHT)
        crop_w_osd = int(crop_w / OUT_RGB888P_WIDTH * DISPLAY_WIDTH)
        crop_h_osd = int(crop_h / OUT_RGB888P_HEIGHT * DISPLAY_HEIGHT)

#        stat_info = os.stat(root_dir + 'utils/features')
#        if (not (stat_info[0] & 0x4000)):
#            os.mkdir(root_dir + 'utils/features')

        time_all = 0
        time_now = 0
        category_index = 0
        for i in range(len(categories)):
            for j in range(features[i]):
                time_all += time_one

        gc_count = 0
        while True:
            # 设置当前while循环退出点，保证rgb888p_img正确释放
            os.exitpoint()
            with ScopedTiming("total",1):
                # （1）读取一帧图像
                rgb888p_img = camera_read(CAM_DEV_ID_0)

                # （2）若读取成功，推理当前帧
                if rgb888p_img.format() == image.RGBP888:
                    # （2.1）推理当前图像，并获取检测结果
                    results = kpu_run(kpu_self_learning,rgb888p_img)
                    global draw_img, osd_img
                    draw_img.clear()
                    draw_img.draw_rectangle(crop_x_osd,crop_y_osd, crop_w_osd, crop_h_osd, color=(255, 255, 0, 255), thickness = 4)

                    if (category_index < len(categories)):
                        time_now += 1
                        draw_img.draw_string( 50 , 200, categories[category_index] + "_" + str(int(time_now-1) // time_one) + ".bin", color=(255,255,0,0), scale=7)
                        with open(root_dir + 'utils/features/' + categories[category_index] + "_" + str(int(time_now-1) // time_one) + ".bin", 'wb') as f:
                            f.write(results[0].tobytes())
                        if (time_now // time_one == features[category_index]):
                            category_index += 1
                            time_all -= time_now
                            time_now = 0
                    else:
                        results_learn = []
                        list_features = os.listdir(root_dir + 'utils/features/')
                        for feature in list_features:
                            with open(root_dir + 'utils/features/' + feature, 'rb') as f:
                                data = f.read()
                            save_vec = np.frombuffer(data, dtype=np.float)
                            score = getSimilarity(results[0], save_vec)

                            if (score > thres):
                                res = feature.split("_")
                                is_same = False
                                for r in results_learn:
                                    if (r["category"] ==  res[0]):
                                        if (r["score"] < score):
                                            r["bin_file"] = feature
                                            r["score"] = score
                                        is_same = True

                                if (not is_same):
                                    if(len(results_learn) < top_k):
                                        evec = {}
                                        evec["category"] = res[0]
                                        evec["score"] = score
                                        evec["bin_file"] = feature
                                        results_learn.append( evec )
                                        results_learn = sorted(results_learn, key=lambda x: -x["score"])
                                    else:
                                        if( score <= results_learn[top_k-1]["score"] ):
                                            continue
                                        else:
                                            evec = {}
                                            evec["category"] = res[0]
                                            evec["score"] = score
                                            evec["bin_file"] = feature
                                            results_learn.append( evec )
                                            results_learn = sorted(results_learn, key=lambda x: -x["score"])

                                            results_learn.pop()
                        draw_y = 200
                        for r in results_learn:
                            draw_img.draw_string( 50 , draw_y, r["category"] + " : " + str(r["score"]), color=(255,255,0,0), scale=7)
                            draw_y += 50

                    draw_img.copy_to(osd_img)
                    display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD3)

                # （3）释放当前帧
                camera_release_image(CAM_DEV_ID_0,rgb888p_img)

                if gc_count > 5:
                    gc.collect()
                    gc_count = 0
                else:
                    gc_count += 1
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    finally:

        # 停止camera
        camera_stop(CAM_DEV_ID_0)
        # 释放显示资源
        display_deinit()
        # 释放kpu资源
        kpu_deinit()
        if 'current_kmodel_obj' in globals():
            global current_kmodel_obj
            del current_kmodel_obj
        del kpu_self_learning
        # 删除features文件夹
        stat_info = os.stat(root_dir + 'utils/features')
        if (stat_info[0] & 0x4000):
            list_files = os.listdir(root_dir + 'utils/features')
            for l in list_files:
                os.remove(root_dir + 'utils/features/' + l)
        # 垃圾回收
        gc.collect()
        # 释放媒体资源
        nn.shrink_memory_pool()
        media_deinit()

    print("self_learning_test end")
    return 0

if __name__ == '__main__':
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    self_learning_inference()
```
