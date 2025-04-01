# 4.1 `nncase_runtime` 模块 API 手册

## 1. 概述

本手册旨在介绍 CanMV 平台的 nncase_runtime 模块，指导开发人员在 MicroPython 环境下调用 KPU（神经网络处理单元）及 AI2D 模块，以实现高效的深度学习推理和图像处理功能。

| 简称                | 说明                                        |
| ------------------- | ------------------------------------------- |
| nncase_runtime      | k230 nncase runtime包,包含KPU模块和AI2D模块 |
| nncase_runtime.kpu  | kpu模块                                     |
| nncase_runtime.ai2d | ai2d模块                                    |

## 2. API 介绍

### 2.1 from_numpy

**描述**

该函数用于从 MicroPython 中的 ulab.numpy 对象创建 runtime_tensor。

**语法**

```python
runtime_tensor = nncase_runtime.from_numpy(ulab.numpy)
```

**参数**

| 参数名称   | 描述         | 输入/输出 |
| ---------- | ------------ | --------- |
| ulab.numpy | numpy 对象   | 输入      |

**返回值**

| 返回值         | 描述                             |
| -------------- | -------------------------------- |
| runtime_tensor | 返回创建的 runtime_tensor 对象。  |
| 其他           | 如果失败，将抛出 C++ 异常。     |

### 2.2 to_numpy

**描述**

将 runtime_tensor 对象转换为 ulab.numpy 对象。

**语法**

```python
runtime_tensor = kpu.get_output_tensor(0)
result = runtime_tensor.to_numpy()
```

**参数**

无。

**返回值**

| 返回值     | 描述                                           |
| ---------- | ---------------------------------------------- |
| ulab.numpy | 返回从 runtime_tensor 转换后的 ulab.numpy 对象。 |
| 其他       | 如果失败，将抛出 C++ 异常。                    |

### 2.3 nncase_runtime.kpu

kpu 模块提供了用于调用 KPU 硬件执行神经网络模型推理的基本功能，包括加载模型、设置输入数据、执行推理及获取输出结果等。

#### 2.3.1 load_kmodel

**描述**

加载编译生成的 kmodel 格式的神经网络模型。

**语法**

```python
load_kmodel(read_bin)
load_kmodel(path)
```

**参数**

| 参数名称 | 描述               | 输入/输出 |
| -------- | ------------------ | --------- |
| read_bin | kmodel 的二进制内容 | 输入      |
| path     | kmodel 的文件路径   | 输入      |

**返回值**

| 返回值 | 描述                |
| ------ | ------------------- |
| 无     | 加载成功。          |
| 其他   | 如果失败，将抛出 C++ 异常。 |

#### 2.3.2 set_input_tensor

**描述**

设置 kmodel 推理时的输入 runtime_tensor。

**语法**

```python
set_input_tensor(index, runtime_tensor)
```

**参数**

| 参数名称       | 描述               | 输入/输出 |
| -------------- | ------------------ | --------- |
| index          | kmodel 的输入索引   | 输入      |
| runtime_tensor | 包含输入数据信息的 tensor | 输入      |

**返回值**

| 返回值 | 描述                |
| ------ | ------------------- |
| 无     | 设置成功。          |
| 其他   | 如果失败，将抛出 C++ 异常。 |

#### 2.3.3 get_input_tensor

**描述**

获取 kmodel 推理时的输入 runtime_tensor。

**语法**

```python
get_input_tensor(index)
```

**参数**

| 参数名称 | 描述               | 输入/输出 |
| -------- | ------------------ | --------- |
| index    | kmodel 的输入索引   | 输入      |

**返回值**

| 返回值         | 描述                       |
| -------------- | -------------------------- |
| runtime_tensor | 包含输入数据信息的 tensor。 |
| 其他           | 如果失败，将抛出 C++ 异常。 |

#### 2.3.4 set_output_tensor

**描述**

设置 kmodel 推理后的输出结果。

**语法**

```python
set_output_tensor(index, runtime_tensor)
```

**参数**

| 参数名称       | 描述               | 输入/输出 |
| -------------- | ------------------ | --------- |
| index          | kmodel 的输出索引   | 输入      |
| runtime_tensor | 输出结果的 tensor    | 输入      |

**返回值**

| 返回值 | 描述                |
| ------ | ------------------- |
| 无     | 设置成功。          |
| 其他   | 如果失败，将抛出 C++ 异常。 |

#### 2.3.5 get_output_tensor

**描述**

获取 kmodel 推理后的输出结果。

**语法**

```python
get_output_tensor(index)
```

**参数**

| 参数名称 | 描述               | 输入/输出 |
| -------- | ------------------ | --------- |
| index    | kmodel 的输出索引   | 输入      |

**返回值**

| 返回值         | 描述                            |
| :------------- | ------------------------------- |
| runtime_tensor | 获取第 index 个输出的 runtime_tensor。 |
| 其他           | 如果失败，将抛出 C++ 异常。      |

#### 2.3.6 run

**描述**

启动 kmodel 推理过程。

**语法**

```python
run()
```

**返回值**

| 返回值 | 描述                |
| :----- | ------------------- |
| 无     | 推理成功            |
| 其他   | 如果失败，将抛出 C++ 异常。 |

#### 2.3.7 inputs_size

**描述**

获取 kmodel 的输入个数。

**语法**

```python
inputs_size()
```

**返回值**

| 返回值 | 描述                |
| :----- | ------------------- |
| size_t | kmodel 的输入个数。  |
| 其他   | 如果失败，将抛出 C++ 异常。 |

#### 2.3.8 outputs_size

**描述**

获取 kmodel 的输出个数。

**语法**

```python
outputs_size()
```

**返回值**

| 返回值 | 描述                |
| :----- | ------------------- |
| size_t | kmodel 的输出个数。  |
| 其他   | 如果失败，将抛出 C++ 异常。 |

#### 2.3.9 get_input_desc

**描述**

获取指定索引的输入描述信息。

**语法**

```python
get_input_desc(index)
```

**参数**

| 参数名称 | 描述               | 输入/输出 |
| -------- | ------------------ | --------- |
| index    | kmodel 的输入索引   | 输入      |

**返回值**

| 返回值      | 描述                                          |
| :---------- | --------------------------------------------- |
| MemoryRange | 第 index 个输入的信息，包括 `dtype`, `start`, `size`。 |

#### 2.3.10 get_output_desc

**描述**

获取指定索引的输出描述信息。

**语法**

```python
get_output_desc(index)
```

**参数**

| 参数名称 | 描述               | 输入/输出 |
| -------- | ------------------ | --------- |
| index    | kmodel 的输出索引   | 输入      |

**返回值**

| 返回值      | 描述                                          |
| :---------- | --------------------------------------------- |
| MemoryRange | 第 index 个输出的信息，包括 `dtype`, `start`, `size`。 |

### 2.4 nncase_runtime.ai2d

#### 2.4.1 build

**描述**

构造 ai2d_builder 对象。

**语法**

```python
build(input_shape, output_shape)
```

**参数**

| 名称         | 描述     |
| ------------ | -------- |
| input_shape  | 输入形状 |
| output_shape | 输出形状 |

**返回值**

| 返回值       | 描述                          |
| :----------- | ----------------------------- |
| ai2d_builder | 返回用于执行的 ai2d_builder 对象。 |
| 其他         | 如果失败，将抛出 C++ 异常。    |

#### 2.4.2 run

**描述**

配置寄存器并启动 AI2D 计算。

**语法**

```python
ai2d_builder.run(input_tensor, output_tensor)
```

**参数**  

| 名称          | 描述       |
| ------------- | ---------- |
| input_tensor  | 输入 tensor |
| output_tensor | 输出 tensor |

**返回值**  

| 返回值 | 描述                |
| ------ | ------------------- |
| 无     | 成功。              |
| 其他   | 如果失败，将抛出 C++ 异常。 |

#### 2.4.3 set_dtype

**描述**

设置 AI2D 计算过程中的数据类型。

**语法**  

```python
set_dtype(src_format, dst_format, src_type, dst_type)
```

**参数**

| 名称       | 类型        | 描述         |
| ---------- | ----------- | ------------ |
| src_format | ai2d_format | 输入数据格式 |
| dst_format | ai2d_format | 输出数据格式 |
| src_type   | datatype_t  | 输入数据类型 |
| dst_type   | datatype_t  | 输出数据类型 |

#### 2.4.4 set_crop_param

**描述**

配置裁剪相关参数。

**语法**  

```python
set_crop_param(crop_flag, start_x, start_y, width, height)
```

**参数**  

| 名称      | 类型 | 描述               |
| --------- |---- | ------------------ |
| crop_flag | bool | 是否启用裁剪功能   |
| start_x   | int  | 宽度方向的起始像素 |
| start_y   | int  | 高度方向的起始像素 |
| width     | int  | 宽度               |
| height    | int  | 高度               |

#### 2.4.5 set_shift_param

【描述】

用于配置shift相关的参数.

【定义】

```Python
set_shift_param(shift_flag, shift_val)
```

【参数】

| 名称       | 类型 | 描述              |
| ---------- | ---- | ----------------- |
| shift_flag | bool | 是否开启shift功能 |
| shift_val  | int  | 右移的比特数      |

#### 2.4.6 set_pad_param

【描述】

用于配置pad相关的参数.

【定义】

```Python
set_pad_param(pad_flag, paddings, pad_mode, pad_val)
```

【参数】

| 名称     | 类型 | 描述                                                                                          |
| -------- | ---- | --------------------------------------------------------------------------------------------- |
| pad_flag | bool | 是否开启pad功能                                                                               |
| paddings | list | 各个维度的padding, size=8，分别表示dim0到dim4的前后padding的个数，其中dim0/dim1固定配置{0, 0} |
| pad_mode | int  | 只支持pad constant，配置0即可                                                                 |
| pad_val  | list | 每个channel的padding value                                                                    |

#### 2.4.7 set_resize_param

【描述】

用于配置resize相关的参数.

【定义】

```Python
set_resize_param(resize_flag, interp_method, interp_mode)
```

【参数】

| 名称          | 类型               | 描述               |
| ------------- | ------------------ | ------------------ |
| resize_flag   | bool               | 是否开启resize功能 |
| interp_method | ai2d_interp_method | resize插值方法     |
| interp_mode   | ai2d_interp_mode   | resize模式         |

#### 2.4.8 set_affine_param

【描述】

用于配置affine相关的参数.

【定义】

```Python
set_affine_param(affine_flag, interp_method, cord_round, bound_ind, bound_val, bound_smooth, M)
```

【参数】

| 名称          | 类型               | 描述                                                                                                                     |
| ------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| affine_flag   | bool               | 是否开启affine功能                                                                                                       |
| interp_method | ai2d_interp_method | Affine采用的插值方法                                                                                                     |
| cord_round    | uint32_t           | 整数边界0或者1                                                                                                           |
| bound_ind     | uint32_t           | 边界像素模式0或者1                                                                                                       |
| bound_val     | uint32_t           | 边界填充值                                                                                                               |
| bound_smooth  | uint32_t           | 边界平滑0或者1                                                                                                           |
| M             | list               | 仿射变换矩阵对应的vector，仿射变换为Y=\[a_0, a_1; a_2, a_3\] \cdot  X + \[b_0, b_1\] $, 则  M=[a_0,a_1,b_0,a_2,a_3,b_1 ] |

### 2.5 shrink_memory_pool

【描述】

清理nncase_runtime产生的内存池，释放内存。

【语法】

```Python
import gc
import nncase_runtime

gc.collect()
nncase_runtime.shrink_memory_pool()
```

## 3. 参考示例

```python
import os
import ujson
import nncase_runtime as nn
import ulab.numpy as np
import image
import sys

# 加载kmodel
kmodel_path="/sdcard/examples/kmodel/face_detection_320.kmodel"
kpu=nn.kpu()
kpu.load_kmodel(kmodel_path)

# 读取一张图片，并将其transpose成chw数据
img_path="/sdcard/examples/utils/db_img/id_1.jpg"
img_data = image.Image(img_path).to_rgb888()
img_hwc=img_data.to_numpy_ref()
shape=img_hwc.shape
img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
img_tmp_trans = img_tmp.transpose().copy()
img_chw=img_tmp_trans.reshape((shape[2],shape[0],shape[1]))

# 初始化ai2d预处理，并运行ai2d预处理，输出模型输入分辨率320*320
ai2d=nn.ai2d()
output_data = np.ones((1,3,320,320),dtype=np.uint8)
ai2d_output_tensor = nn.from_numpy(output_data)
ai2d.set_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
ai2d.set_resize_param(True,nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
ai2d_builder = ai2d.build([1,3,img_chw.shape[1],img_chw.shape[2]], [1,3,320,320])   
ai2d_input_tensor = nn.from_numpy(img_chw)
ai2d_builder.run(ai2d_input_tensor, ai2d_output_tensor)

# kmodel运行，并获取输出，输出从tensor转成ulab.numpy.ndarray数据
kpu.set_input_tensor(0, ai2d_output_tensor)
kpu.run()
for i in range(kpu.outputs_size()):
    output_data = kpu.get_output_tensor(i)
    result = output_data.to_numpy()
    print(result.shape)
```

## 4. 结论

通过使用 nncase_runtime 模块，开发人员能够在 CanMV 平台上实现高效的深度学习推理和图像处理功能。本手册提供了 API 的详细描述和使用示例，旨在帮助开发人员快速上手并高效开发相关应用。
