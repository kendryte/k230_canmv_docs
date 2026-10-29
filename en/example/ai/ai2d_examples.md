# Ai2d Preprocessing Examples

## Overview

Based on the interfaces provided by the `nncase_runtime` module, AIDemo has performed secondary encapsulation on `nncase_runtime.ai2d`. The encapsulation file is in the `/sdcard/libs/AI2D.py` module. The provided interfaces are documented in: [ai2d_module_api_manual](../../api/aidemo/ai2d_module_api_manual.md). For the 5 preprocessing methods provided by Ai2d, this document provides examples and visualizes the preprocessing results to help users better understand the Ai2d preprocessing process. The unencapsulated `nncase_runtime.ai2d` interface is documented in: [nncase_usage](./nncase_usage.md).

The writing style of the examples in this article is consistent with the development board examples, and `display_mode` uniformly uses `"auto"` to automatically adapt to the screen. The `deinit()`/`destroy()` at the end of the example is after `while True`, and will not actually execute; when writing your own application, please refer to [Two Main Loop Patterns](../../ai_dev_doc.md#main-loop-patterns) and use `try/finally` to ensure resource release.

## resize Method

The resize method is an operation widely used in image preprocessing. It is primarily used to change the size of an image. Whether enlarging or shrinking an image, this method can achieve it. Here is example code for implementing the resize process using `Ai2d`.

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
    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定hdmi/lcd/lt9611/st7701/hx8399等，取值见PipeLine手册
    display_mode="auto"

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
            print(img.shape)                # 原图shape为[3,512,512]，get_frame返回CHW三维数据
            ai2d_output_tensor=my_ai2d.run(img) # 执行resize预处理
            ai2d_output_np=ai2d_output_tensor.to_numpy() # 类型转换
            print(ai2d_output_np.shape)        # 预处理后的shape为[1,3,640,640]
            gc.collect()                    # 垃圾回收
    my_ai2d.deinit()                        # 释放ai2d资源
    pl.destroy()                            # 销毁PipeLine实例
```

## crop Method

The crop method is an operation used to extract (crop) a Region of Interest (ROI) from the original image. It can select a portion of the image as a new image based on specified coordinates and dimensions. Here is example code for implementing the crop process using `Ai2d`.

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
    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定hdmi/lcd/lt9611/st7701/hx8399等，取值见PipeLine手册
    display_mode="auto"

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=[512,512], display_mode=display_mode)
    pl.create()  # 创建PipeLine实例
    display_size=pl.get_display_size()
    my_ai2d=Ai2d(debug_mode=0) #初始化Ai2d实例
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # 配置crop预处理方法，参数为(start_x, start_y, width, height)，即从(100,100)起裁剪200x200区域
    my_ai2d.crop(100,100,200,200)
    # 构建预处理过程
    my_ai2d.build([1,3,512,512],[1,3,200,200])
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)                # 原图shape为[3,512,512]，get_frame返回CHW三维数据
            ai2d_output_tensor=my_ai2d.run(img) # 执行crop预处理，H/W维度均裁剪100~300px范围内的数据（起点100，宽高200）
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
    my_ai2d.deinit()                        # 释放ai2d资源
    pl.destroy()                            # 销毁PipeLine实例
```

## pad Method

The pad (padding) method is a technique used in the image preprocessing stage to pad the edges of an image. It changes the image size by adding pixel values around the image (top, bottom, left, and right). These added pixel values can be customized. Here is example code for implementing the pad process using `Ai2d`.

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
    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定hdmi/lcd/lt9611/st7701/hx8399等，取值见PipeLine手册
    display_mode="auto"

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
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)                # 原图shape为[3,512,512]，get_frame返回CHW三维数据
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
    my_ai2d.deinit()                        # 释放ai2d资源
    pl.destroy()                            # 销毁PipeLine实例
```

## affine Method

The affine (affine transformation) method is a technique used in image preprocessing to perform geometric transformations on an image. It can achieve various geometric transformation operations such as rotation, translation, and scaling of an image, and can maintain the "straightness" of the image (i.e., straight lines remain straight after transformation) and "parallelism" (i.e., parallel lines remain parallel after transformation). Here is example code for implementing the affine process using `Ai2d`.

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
    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定hdmi/lcd/lt9611/st7701/hx8399等，取值见PipeLine手册
    display_mode="auto"

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
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)                # 原图shape为[3,512,512]，get_frame返回CHW三维数据
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
    my_ai2d.deinit()                        # 释放ai2d资源
    pl.destroy()                            # 销毁PipeLine实例
```

## shift Method

The shift method is a bit-right-shift method in data preprocessing. Each right shift by one bit changes the original data to 1/2 of its original value. Here is example code for implementing the affine process using `Ai2d`.

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
        print(data_input.shape)                        # 输入shape为[1,3,256,256],原值都是240
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
    my_ai2d.deinit()                               # 释放ai2d资源
    gc.collect()                                   # 垃圾回收
```
