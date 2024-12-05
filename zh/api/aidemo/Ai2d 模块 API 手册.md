# 5.2 Ai2d 模块 API 手册

## 1. 概述

本手册旨在指导开发人员使用 MicroPython 开发 AI Demo 时，构建预处理流程，实现使用 `nncase_runtime.ai2d` 对输入图像配置并执行预处理的功能。该模块封装了 `ai2d` 支持的预处理方法，并给出了预处理过程构建和运行的方法。

## 2. API 介绍

### 2.1 init

**描述**

Ai2d 构造函数。

**语法**  

```python
from libs.AI2D import Ai2d

my_ai2d = Ai2d(debug_mode=0)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| debug_mode   | 调试计时模式，0计时，1不计时，int类型 | 输入 | 默认为0 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| Ai2d | Ai2d实例                          |

### 2.2 set_ai2d_dtype

**描述**

设置ai2d预处理输入输出的数据类型和数据格式。

**语法**  

```python
import ulab.numpy as np

my_ai2d.set_ai2d_dtype(input_format=nn.ai2d_format.NCHW_FMT,output_format=nn.ai2d_format.NCHW_FMT,input_type=np.uint8,output_type=np.uint8)

my_ai2d.set_ai2d_dtype(nn.ai2d_format.RGB_packed, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| input_format | 预处理输入数据格式   | 输入      | 必填，根据 `type` 决定 |
| output_format  | 预处理输出数据格式 | 输入      | 必填，根据 `type` 决定 |
| input_type   | 预处理输入数据类型   | 输入      | 必填，根据数据类型选择`np.uint8`和`np.float` |
| output_type  | 预处理输出数据类型   | 输入      | 必填，根据数据类型选择`np.uint8`和`np.float` |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.3 crop

**描述**

crop 预处理配置方法。

**语法**  

```python
my_ai2d.crop(0,0,200,300)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| start_x | 宽度方向的起始像素,int类型   | 输入      | 必填 |
| start_y  | 高度方向的起始像素,int类型 | 输入      | 必填 |
| width   | 宽度方向的 crop 长度,int类型   | 输入      | 必填 |
| height  | 高度方向的 crop 长度,int类型   | 输入      | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.4 shift

**描述**

shift 预处理配置方法。

**语法**  

```python
my_ai2d.shift(shift_val=2)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| shift_val| 右移的比特数,int类型  | 输入      | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.5 pad

**描述**

padding 预处理配置方法。

**语法**  

```python
my_ai2d.pad(paddings=[0,0,0,0,5,5,15,15],pad_mode=0,pad_val=[114,114,114])
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| paddings| list类型，各维度两侧 padding 的大小，对于4维的图像(NCHW)，该参数包含8个值，分别表示 N/C/H/W 四个维度两侧的 padding 大小，通常只在后两个维度做 padding  | 输入      | 必填 |
| pad_mode| 只支持 constant padding，直接设为0  | 输入      | 必填 |
| pad_val| list 类型，每个像素位置填充的三通道值，比如[114,114,114]、[0,0,0]  | 输入      | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.6 resize

**描述**

resize预处理配置方法。

**语法**  

```python
my_ai2d.resize(interp_method=nn.interp_method.tf_bilinear, interp_mode=nn.interp_mode.half_pixel)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| interp_method | resize 插值方法  | 输入      | 必填，根据 `interp_method` 决定|
| interp_mode | resize 模式  | 输入      | 必填，根据 `interp_mode` 决定|

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.7 affine

**描述**

affine预处理配置方法。

**语法**  

```python
affine_matrix=[0.2159457, -0.031286, -59.5312, 0.031286, 0.2159457, -35.30719]
my_ai2d.affine(interp_method=nn.interp_method.cv2_bilinear,cord_round=0, bound_ind=0, bound_val=127, bound_smooth=1,M=affine_matrix)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| interp_method | resize 插值方法  | 输入 | 必填|
| cord_round | 坐标取整方式，0或者1, uint32_t类型  | 输入 | 必填，一般设为0 |
| bound_ind | 边界像素处理模式，0或者1, uint32_t类型  | 输入 | 必填，一般设为0 |
| bound_val | 边界填充值, uint32_t类型  | 输入      | 必填，设为127 |
| bound_smooth | 边界平滑处理，0或者1, uint32_t类型 | 输入 | 必填，设为1 |
| M | 仿射变换矩阵对应的 vector，2*3矩阵变换得到的 list，见上述示例 | 输入 | 必填|

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.8 build

**描述**

按照配置好的预处理方法构造预处理器。

**语法**  

```python
my_ai2d=Ai2d(debug_mode=0) 
my_ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
my_ai2d.build([1,3,512,512],[1,3,640,640])
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| ai2d_input_shape | ai2d 输入数据 shape  | 输入 | 必填 |
| ai2d_output_shape | ai2d 输出数据 shape  | 输入 | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无    |                                  |

### 2.9 run

**描述**

使用配置的ai2d预处理器执行预处理过程，返回 `nncase_runtime.tensor`。

**语法**  

```python
ai2d_output_tensor=my_ai2d.run(img)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| input_np | 预处理输入数据，`ulab.numpy.ndarray` 类型  | 输入 | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| ai2d_output_tensor    | 经过ai2d预处理后的数据   |

## 3. 数据结构描述

### 3.1 type

| 输入格式         | 输出格式               | 备注                  |
| ---------------- | ---------------------- | --------------------- |
| YUV420_NV12      | RGB_planar/YUV420_NV12 |                       |
| YUV420_NV21      | RGB_planar/YUV420_NV21 |                       |
| YUV420_I420      | RGB_planar/YUV420_I420 |                       |
| YUV400           | YUV400                 |                       |
| NCHW(RGB_planar) | NCHW(RGB_planar)       |                       |
| RGB_packed       | RGB_planar/RGB_packed  |                       |
| RAW16            | RAW16/8                | 深度图，执行shift操作 |

### 3.2 interp_method

resize预处理方法中的插值方法。分列如下：

| 方法     | 说明                                     | 备注          |
|------------|------------------------------------------|---------------|
| nn.interp_method.tf_nearest |       tf的最近邻插值      |            |
| nn.interp_method.tf_bilinear |      tf的双线性插值      |            |
| nn.interp_method.cv2_nearest  |     cv2的最近邻插值     |            |
| nn.interp_method.cv2_bilinear  |    cv2的双线性插值     |            |

### 3.3 interp_mode

| 模式              | 说明            | 备注 |
|-------------------|-----------------|------|
| nn.interp_mode.none   | 不用特殊的对齐策略      |      |
| nn.interp_mode.align_corner  | 角点强制对齐     |      |
| nn.interp_mode.half_pixel | 中心对齐    |      |

## 4. 示例程序

```{attention}
(1) Affine和Resize功能是互斥的，不能同时开启;  
(2) Shift功能的输入格式只能是Raw16;  
(3) Pad value是按通道配置的，对应的list元素个数要与channel数相等；  
(4) 当配置了多个功能时，执行顺序是Crop->Shift->Resize/Affine->Pad, 配置参数时注意要匹配；如果不符合该顺序，需要初始化多个Ai2d实例实现预处理过程；
```

以下为示例程序：

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import gc
import sys,os

if __name__ == "__main__":
    # 显示模式，默认"hdmi",可以选择"hdmi"和"lcd"
    display_mode="hdmi"
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=[512,512], display_size=display_size, display_mode=display_mode)
    pl.create()  # 创建PipeLine实例
    my_ai2d=Ai2d(debug_mode=0) #初始化Ai2d实例
    # 配置resize预处理方法
    my_ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
    # 构建预处理过程
    my_ai2d.build([1,3,512,512],[1,3,640,640])
    try:
        while True:
            os.exitpoint()                      # 检查是否有退出信号
            with ScopedTiming("total",1):
                img = pl.get_frame()            # 获取当前帧数据
                print(img.shape)                # 原图shape为[1,3,512,512]
                ai2d_output_tensor=my_ai2d.run(img) # 执行resize预处理
                ai2d_output_np=ai2d_output_tensor.to_numpy() # 类型转换
                print(ai2d_output_np.shape)        # 预处理后的shape为[1,3,640,640]
                gc.collect()                    # 垃圾回收
    except Exception as e:
        sys.print_exception(e)                  # 打印异常信息
    finally:
        pl.destroy()                            # 销毁PipeLine实例
```

上述代码中，定义了resize的预处理方法，预处理输入分辨率为(512,512)，预处理输出分辨率为(640,640)。
