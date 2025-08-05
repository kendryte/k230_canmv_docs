# Utils 模块 API 手册

## 概述

本手册旨在提供给开发人员使用 MicroPython 开发 AI Demo 时使用的一些共用处理方法。

## API 介绍

### 计时模块 ScopedTiming

**描述**

ScopedTiming 类是一个用来测量代码块执行时间的上下文管理器。上下文管理器通过定义包含 `__enter__` 和 `__exit__` 方法的类来创建。当在 with 语句中使用该类的实例，`__enter__` 在进入 with 块时被调用，`__exit__` 在离开时被调用。

```python
from libs.Utils import ScopedTiming

def test_time():
    with ScopedTiming("test",1):
        #####代码#####
        # ...
        ##############
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| info   | 计时部分的描述 | 输入 | 默认"" |
| enable_profile   | 是否调试打印计时信息 | 输入 | 默认True |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| - | 无返回值                        |

### read_json

**描述**

根据json文件路径读取json中的各字段，主要用于读取部署在线训练平台脚本的配置文件。

**语法**  

```python
import libs.Utils import read_json

json_path="/sdcard/examples/test.json"
json_data=read_json(json_path)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| json_path | json文件在开发板中的路径   | 输入      | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| dict  |       json字段内容       |

### read_image

**描述**

根据图片路径读取图片数据，用于AI推理过程中读取静态图，给到模型完成推理。

**语法**  

```python
import libs.Utils import read_image

img_path="/sdcard/examples/test.jpg"
img_chw,img_rgb888=read_image(img_path)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| img_path | 图片文件在开发板中的路径   | 输入      | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| img_chw  |       CHW排布的ulab.numpy.ndarray格式图片数据，可以用于创建nncase_runtime.tensor给AI模型推理       |
| img_rgb888  |       rgb888格式的Image实例，可以用于绘制结果      |

### get_colors

**描述**

按照标签数量获取ARGB颜色数组，比如[255,191,162,208]。预置80种颜色，大于80种时取余。

**语法**  

```python
import libs.Utils import get_colors

classes_num=30
colors=get_colors(classes_num)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| classes_num | 标签数量   | 输入      | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| list[list]  |       ARGB颜色数组       |

### center_crop_param

**描述**

center_crop_param 是正方形中心裁剪函数，接收一个表示图像尺寸的输入参数 input_size，它通常是一个包含两个元素的列表，分别代表图像的宽度和高度。函数会计算出以图像中心为基准进行裁剪时，裁剪区域的左上角坐标（top 和 left）以及裁剪区域的边长 m，最终返回这些参数。

**语法**  

```python
from libs.Utils import center_crop_param

input_size=[640,320]
top,left,m=center_crop_param(input_size)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| input_size | 输入宽高列表  | 输入      | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| top     | 裁左上角距离上边界距离                   |
| left    | 裁左上角距离左边界距离                   |
| m       | 裁边长                   |

### letterbox_pad_param

**描述**

letterbox_pad_param 函数用于计算对输入图像进行填充时所需的参数。该填充是一种在保持图像宽高比的前提下，将图像缩放到指定输出尺寸，并在周围添加填充的技术，常用于目标检测等计算机视觉任务中，确保输入图像能适配模型的输入尺寸。该函数会进行单边填充，即只在下侧和右侧进行填充，返回填充区域的上下左右边界宽度以及缩放比例。该方法计算结果一般和resize同时使用。

**语法**  

```python
from libs.Utils import letterbox_pad_param

input_size=[1920,1080]
output_size=[640,640]
top,bottom,left,right,scale=letterbox_pad_param(input_size,output_size)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| input_size| 缩放填充前的输入分辨率  | 输入      | 必填 |
| output_size| 缩放填充后的输出分辨率  | 输入      | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| top     |  上侧填充值                     |
| bottom  |  下侧填充值                     |
| left    |  左侧填充值                     |
| right   |  右侧填充值                     |
| scale   |  缩放比例                       |

### center_pad_param

**描述**

center_pad_param 函数的主要目的是计算将输入图像以居中的方式进行填充并缩放到指定输出尺寸时所需的参数。在处理图像时，为了让图像在保持其原始宽高比的情况下适配特定的输出尺寸，通常会进行缩放操作，然后在图像的周围添加填充，使图像在输出区域中居中显示。该函数会返回填充区域的上下左右边界宽度以及缩放比例。该方法计算结果一般和resize同时使用。

**语法**  

```python
from libs.Utils import center_pad_param

input_size=[1920,1080]
output_size=[640,640]
top,bottom,left,right,scale=center_pad_param(input_size,output_size)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| input_size| 缩放填充前的输入分辨率  | 输入      | 必填 |
| output_size| 缩放填充后的输出分辨率  | 输入      | 必填 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| top     |  上侧填充值                     |
| bottom  |  下侧填充值                     |
| left    |  左侧填充值                     |
| right   |  右侧填充值                     |
| scale   |  缩放比例                       |

### softmax

**描述**

softmax 函数在分类问题中广泛应用。它的主要作用是将一个实数向量转换为概率分布，使得向量中的每个元素都在 [0, 1] 区间内，并且所有元素之和为 1。通过这种方式，可以将模型的输出解释为每个类别对应的概率。

**语法**  

```python
from libs.Utils import softmax

input_data=[1,2,3]
output_data=softmax(input_data)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| x | 分类模型返回的一维数据  | 输入      | 必填|

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| softmax_res    |       类别的概率分布      |

### sigmoid

**描述**

sigmoid 函数广泛应用于二分类模型中。它的作用是将任意实数映射到 (0, 1) 区间内，常用于将模型输出转换为概率值，从而用于概率判断或分类决策。

**语法**  

```python
from libs.Utils import sigmoid

input_data = 0.5
output_data = sigmoid(input_data)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| input_data | 任意实数  | 输入      | 必填|

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| sigmoid_res|映射到 (0, 1) 区间的数值或数组  |

### chw2hwc

**描述**

将CHW排布的`ulab.numpy.ndarray`数据转换为HWC排布，仅适用于3维数据。

**语法**  

```python
from libs.Utils import chw2hwc

# chw_np是CHW排布的ulab.numpy.ndarray数据
hwc_np = chw2hwc(chw_np)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| chw_np | 3维ulab.numpy.ndarray数据  | 输入      | 必填|

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| hwc_np| 排布维HWC的3维ulab.numpy.ndarray数据 |

### hwc2chw

**描述**

将HWC排布的`ulab.numpy.ndarray`数据转换为CHW排布，仅适用于3维数据，常用于将Image实例数据转换后给AI模型使用。

**语法**  

```python
from libs.Utils import hwc2chw

# hwc_np是CHW排布的ulab.numpy.ndarray数据
chw_np = hwc2chw(hwc_np)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| hwc_np | 3维ulab.numpy.ndarray数据  | 输入      | 必填|

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| chw_np| 排布维CHW的3维ulab.numpy.ndarray数据 |
