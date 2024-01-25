# K230 CanMV nncase_runtime 使用说明

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

[toc]

## 前言

### 概述

此文档介绍CanMV nncase_runtime模块，用于指导开发人员使用MicroPython调用KPU和AI2D模块。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
|      |      |

### 修订记录

| 文档版本号 | 修改说明 | 修改者 | 日期       |
| ---------- | -------- | ------ | ---------- |
| V1.0       | 初版     | 杨浩琪 | 2023-11-21 |

## 1. 概述

此文档介绍CanMV nncase_runtime模块如何使用。

## 2. 功能介绍

### 2.1. 导入库

```Python
import nncase_runtime as nn
import ulab.numpy as np
```

### 2.2. KPU初始化

初始化模型推理模块

```Python
kpu = nn.kpu()
```

### 2.3. AI2D初始化

初始化图像处理模块

```Python
ai2d = nn.ai2d()
```

### 2.4. 读取模型

读取模型有两种方式，一种是通过文件路径，一种是通过二进制数据。

```Python
# 文件路径
model = nn.load_model('test.kmodel')

# 二进制数据
with open("test.kmodel", "rb") as f:
    data = f.read()
    kpu.load_kmodel(data)
```

### 2.5. 单独使用KPU进行推理

#### 2.5.1. 设置模型输入

开始模型推理前，需要设置对应的模型输入数据

```Python
data = np.zeros((1,3,320,320),dtype=np.uint8)
kpu_input = nn.from_numpy(data)
kpu.set_input_tensor(0, kpu_input)

# 模型存在多个输入
kpu.set_input_tensor(1, kpu_input_1)
kpu.set_input_tensor(2, kpu_input_2)
```

#### 2.5.2. 执行推理并获取推理结果

```Python
kpu.run()

result = kpu.get_output_tensor(i) # 返回第i个输出tensor
data = result.to_numpy() # 将输出tensor转换为numpy对象
```

### 2.6. 使用AI2D+KPU进行推理

这里使用AI2D对图像进行预处理，然后使用KPU进行推理。如果使用摄像头等输入设备，请参考[AI Demo示例说明](../example/K230_CanMV_AI_Demo示例说明.md#14-nncase使用ai2d)

#### 2.6.1. 配置AI2D参数

AI2D功能有：`crop`，`shift`，`pad`，`resize`，`affine`。可以根据实际需求配置对应的参数，不使用的功能不需要配置。
各个场景的不同用法请参考[AI demo](../example/K230_CanMV_AI_Demo示例说明.md)中第三章<<三、AI Demo多模型示例解析>>。

```Python
# 基础配置： 输入、输出layout，输入、输出dtype
ai2d.set_dtype(nncase_runtime.ai2d_format.NCHW_FMT,
               nncase_runtime.ai2d_format.NCHW_FMT, 
               np.uint8, np.uint8)
             
# 功能配置，以pad和resize为例
ai2d.set_pad_param(True, [0,0,0,0,1,1,2,2], 0, [127,127,127])
ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

# 执行配置,需要配置输入、输出shape
ai2d_builder = ai2d.build([1,3,224,224], [1,3,256,256])
```

#### 2.6.2. 串行使用AI2D和KPU

```Python
data = np.zeros((1,3,224,224),dtype=np.uint8)
ai2d_input = nn.from_numpy(data)

# 获取KPU的输入tensor
kpu_input = kpu.get_input_tensor(0)

# 将KPU的输入tensor设置为ai2d的输出
ai2d_builder.run(ai2d_input, kpu_input)
kpu.run()

# 获取KPU的输出tensor
result = kpu.get_output_tensor(i) # 返回第i个输出tensor
data = result.to_numpy() # 将输出tensor转换为numpy对象
```

### 2.7. 释放内存

如果定义了`global`变量，则需要确保在程序结束前，所有`global`变量的引用计数为0，否则无法释放内存。

```Python
import nncase_runtime as nn
import gc

del kpu
del ai2d
del ai2d_builder

# tensor = nn.from_numpy()
del tensor

# input_tensor = kpu.get_input_tensor(i)
del input_tensor

# output_tensor = kpu.get_output_tensor(i)
del output_tensor

gc.collect()
nn.shrink_memory_pool()
```
