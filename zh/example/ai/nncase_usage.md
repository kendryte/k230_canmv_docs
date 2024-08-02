# 1. nncase_runtime 模块使用说明

## 1. 概述

此文档介绍CanMV nncase_runtime模块，用于指导开发人员使用MicroPython调用KPU和AI2D模块。

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

使用AI2D对摄像头采集的数据进行预处理，然后使用KPU进行推理。摄像头等输入设备的配置请参考[AI Demo说明文档](./AI_Demo说明文档.md)，这里仅介绍AI2D+KPU的使用流程。

#### 2.6.1. 配置AI2D参数

AI2D功能有：`crop`，`shift`，`pad`，`resize`，`affine`。可以根据实际需求配置对应的参数，不使用的功能不需要配置。

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

#### 2.6.2. AI2D+KPU推理

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

如果定义了`global`变量，则需要确保在程序结束前，所有`global`变量的引用计数为0，否则程序异常退出时无法释放内存。或者在程序开始时调用一次`gc.collect()`，可以将上一个程序因异常退出而未释放的内存释放掉。

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
