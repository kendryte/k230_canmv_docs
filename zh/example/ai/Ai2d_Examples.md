# Ai2d预处理示例

## 概述

基于 `nncase_runtime` 模块提供的接口，AIDemo 部分对 `nncase_runtime.ai2d` 进行了二次封装，封装文件在 `/sdcard/libs/AI2D.py` 模块内，提供的接口见：[Ai2d 模块 API 手册](../../api/aidemo/Ai2d%20模块%20API%20手册.md)。针对Ai2d提供的5种预处理方法，本文档提供示例，将预处理的结果可视化，帮助用户更好的理解使用Ai2d预处理过程。未封装的 `nncase_runtime.ai2d` 接口见：[nncase_usage](./nncase_usage.md)。

## resize 方法

resize方法是一种在图片预处理中广泛使用的操作，它主要用于改变图像的尺寸大小。无论是放大还是缩小图像，都可以通过这个方法来实现。这里给出使用 `Ai2d` 实现resize过程的示例代码。

```python
from libs.PipeLine import PipeLine
from libs.AI2D import Ai2d
from libs.Utils import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os

if __name__ == "__main__":
    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="hdmi"

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=[512,512], display_mode=display_mode)
    pl.create()  # 创建PipeLine实例
    display_size=pl.get_display_size()
    my_ai2d=Ai2d(debug_mode=0) #初始化Ai2d实例
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # 配置resize预处理方法
    my_ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
    # 构建预处理过程
    my_ai2d.build([1,3,512,512],[1,3,640,640])
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)                # 原图shape为[3,512,512]
            ai2d_output_tensor=my_ai2d.run(img) # 执行resize预处理
            ai2d_output_np=ai2d_output_tensor.to_numpy() # 类型转换
            print(ai2d_output_np.shape)        # 预处理后的shape为[1,3,640,640]
            gc.collect()                    # 垃圾回收
    pl.destroy()                            # 销毁PipeLine实例
```

## crop 方法

crop方法是一种用于从原始图像中提取（裁剪）出感兴趣区域（ROI，Region of Interest）的操作。它可以根据指定的坐标和尺寸，从图像中选取一部分作为新的图像。这里给出使用 `Ai2d` 实现crop过程的示例代码。

```python
from libs.PipeLine import PipeLine
from libs.AI2D import Ai2d
from libs.Utils import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os
import image

if __name__ == "__main__":
    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="hdmi"

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=[512,512], display_mode=display_mode)
    pl.create()  # 创建PipeLine实例
    display_size=pl.get_display_size()
    my_ai2d=Ai2d(debug_mode=0) #初始化Ai2d实例
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # 配置crop预处理方法
    my_ai2d.crop(100,100,300,300)
    # 构建预处理过程
    my_ai2d.build([1,3,512,512],[1,3,200,200])
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)                # 原图shape为[1,3,512,512]
            ai2d_output_tensor=my_ai2d.run(img) # 执行crop预处理，H/W维度均裁剪100~300px范围内的数据
            ai2d_output_np=ai2d_output_tensor.to_numpy() # 类型转换
            print(ai2d_output_np.shape)        # 预处理后的shape为[1,3,200,200]
            # 使用transpose处理输出为HWC排布的np数据，然后在np数据上创建RGB888格式的Image实例用于在IDE显示效果
            shape=ai2d_output_np.shape
            ai2d_output_tmp = ai2d_output_np.reshape((shape[0] * shape[1], shape[2]*shape[3]))
            ai2d_output_tmp_trans = ai2d_output_tmp.transpose()
            ai2d_output_hwc=ai2d_output_tmp_trans.copy().reshape((shape[2],shape[3],shape[1]))
            out_img=image.Image(200, 200, image.RGB888,alloc=image.ALLOC_REF,data=ai2d_output_hwc)
            out_img.compress_for_ide()
            gc.collect()                    # 垃圾回收
    pl.destroy()                            # 销毁PipeLine实例
```

## pad 方法

pad（填充）方法是一种在图片预处理阶段，对图像边缘进行填充操作的技术。它通过在图像的四周（上下左右）添加像素值，来改变图像的尺寸大小。这些添加的像素值可以自定义。这里给出使用 `Ai2d` 实现pad过程的示例代码。

```python
from libs.PipeLine import PipeLine
from libs.AI2D import Ai2d
from libs.Utils import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os
import image

if __name__ == "__main__":
    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="hdmi"

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=[512,512],display_mode=display_mode)
    pl.create()  # 创建PipeLine实例
    display_size=pl.get_display_size()
    my_ai2d=Ai2d(debug_mode=0) #初始化Ai2d实例
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # 配置pad预处理方法
    my_ai2d.pad(paddings=[0,0,0,0,15,15,30,30],pad_mode=0,pad_val=[114,114,114])
    # 构建预处理过程
    my_ai2d.build([1,3,512,512],[1,3,512+15+15,512+30+30])
    while True:
        os.exitpoint()                      # 检查是否有退出信号
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)                # 原图shape为[1,3,512,512]
            ai2d_output_tensor=my_ai2d.run(img) # 执行pad预处理，H维度上下padding 15px,W维度左右padding 30px
            ai2d_output_np=ai2d_output_tensor.to_numpy() # 类型转换
            print(ai2d_output_np.shape)        # 预处理后的shape为[1,3,542,572]
            # 使用transpose处理输出为HWC排布的np数据，然后在np数据上创建RGB888格式的Image实例用于在IDE显示效果
            shape=ai2d_output_np.shape
            ai2d_output_tmp = ai2d_output_np.reshape((shape[0] * shape[1], shape[2]*shape[3]))
            ai2d_output_tmp_trans = ai2d_output_tmp.transpose()
            ai2d_output_hwc=ai2d_output_tmp_trans.copy().reshape((shape[2],shape[3],shape[1]))
            out_img=image.Image(512+30+30, 512+15+15, image.RGB888,alloc=image.ALLOC_REF,data=ai2d_output_hwc)
            out_img.compress_for_ide()
            gc.collect()                    # 垃圾回收
    pl.destroy()                            # 销毁PipeLine实例
```

## affine 方法

affine（仿射变换）方法是一种在图像预处理中用于对图像进行几何变换的技术。它可以实现图像的旋转、平移、缩放等多种几何变换操作，并且能够保持图像的 “平直性”（即直线在变换后仍然是直线）和 “平行性”（即平行的线在变换后仍然平行）。这里给出使用 `Ai2d` 实现affine过程的示例代码。

```python
from libs.PipeLine import PipeLine
from libs.AI2D import Ai2d
from libs.Utils import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os
import image

if __name__ == "__main__":
    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="hdmi"

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=[512,512], display_mode=display_mode)
    pl.create()  # 创建PipeLine实例
    display_size=pl.get_display_size()
    my_ai2d=Ai2d(debug_mode=0) #初始化Ai2d实例
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # 创建仿射变换矩阵，缩放0.5倍，X/Y方向各平移50px
    affine_matrix = [0.5,0,50,
                     0,0.5,50]
    # 设置仿射变换预处理
    my_ai2d.affine(nn.interp_method.cv2_bilinear,0, 0, 127, 1,affine_matrix)
    # 构建预处理过程
    my_ai2d.build([1,3,512,512],[1,3,256,256])
    while True:
        os.exitpoint()                      # 检查是否有退出信号
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)                # 原图shape为[1,3,512,512]
            ai2d_output_tensor=my_ai2d.run(img) # 执行affine预处理，H/W维度各缩小为0.5倍，同时向X/Y方向平移50px
            ai2d_output_np=ai2d_output_tensor.to_numpy() # 类型转换
            print(ai2d_output_np.shape)        # 预处理后的shape为[1,3,256,256]
            # 使用transpose处理输出为HWC排布的np数据，然后在np数据上创建RGB888格式的Image实例用于在IDE显示效果
            shape=ai2d_output_np.shape
            ai2d_output_tmp = ai2d_output_np.reshape((shape[0] * shape[1], shape[2]*shape[3]))
            ai2d_output_tmp_trans = ai2d_output_tmp.transpose()
            ai2d_output_hwc=ai2d_output_tmp_trans.copy().reshape((shape[2],shape[3],shape[1]))
            out_img=image.Image(256, 256, image.RGB888,alloc=image.ALLOC_REF,data=ai2d_output_hwc)
            out_img.compress_for_ide()
            gc.collect()                    # 垃圾回收
    pl.destroy()                            # 销毁PipeLine实例
```

## shift 方法

shift方法是数据预处理中比特位右移的方法，每右移一位原数据变为原来的1/2。这里给出使用 `Ai2d` 实现affine过程的示例代码。

```python
from libs.PipeLine import PipeLine
from libs.AI2D import Ai2d
from libs.Utils import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os
import image

if __name__ == "__main__":
    background=np.ones((1,3,512,512),dtype=np.uint8)

    data_input=np.ones((1,3,256,256),dtype=np.uint8)*240
    background[:,:,0:256,0:256]=data_input.copy()

    my_ai2d=Ai2d(debug_mode=0) #初始化Ai2d实例
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.RAW16, nn.ai2d_format.NCHW_FMT, np.int16, np.uint8)
    # 设置shift预处理，右移一位，值变为1/2
    my_ai2d.shift(1)
    # 构建预处理过程
    my_ai2d.build([1,3,256,256],[1,3,256,256])
    with ScopedTiming("total",1):
        print(data_input.shape)                        # 原图shape为[1,3,256,256],原值都是240
        ai2d_output_tensor=my_ai2d.run(data_input)     # 执行shift操作后，右移一位，值变为原来的1/2，也就是120
        ai2d_output_np=ai2d_output_tensor.to_numpy()   # 类型转换
        print(ai2d_output_np.shape)                    # 预处理后的shape为[1,3,256,256],值从240变为120

        background[:,:,256:,256:]=ai2d_output_np.copy()
        # 使用transpose处理输出为HWC排布的np数据，然后在np数据上创建RGB888格式的Image实例用于在IDE显示效果
        shape=background.shape
        background_tmp = background.reshape((shape[0] * shape[1], shape[2]*shape[3]))
        background_trans = background_tmp.transpose()
        background_hwc=background_trans.copy().reshape((shape[2],shape[3],shape[1]))
        img=image.Image(512, 512, image.RGB888,alloc=image.ALLOC_REF,data=background_hwc)
        img.compress_for_ide()
        gc.collect()                                   # 垃圾回收
```
