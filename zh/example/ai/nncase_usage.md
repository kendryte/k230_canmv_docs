# nncase_runtime 模块使用说明

## 概述

此文档介绍 CanMV nncase_runtime 模块，指导开发人员使用 MicroPython 调用 `KPU` 和 `AI2D` 模块。

## 功能介绍

### 导入库

在使用nncase_runtime模块之前，需要导入相关库：

```Python
import nncase_runtime as nn
import ulab.numpy as np
```

### KPU 初始化

初始化模型推理模块：

```Python
kpu = nn.kpu()
```

### AI2D初始化

初始化图像处理模块：

```Python
ai2d = nn.ai2d()
```

### 读取模型

读取模型有两种方式：通过文件路径或二进制数据。

```Python
# 文件路径
model = nn.load_model('test.kmodel')

# 二进制数据
with open("test.kmodel", "rb") as f:
    data = f.read()
    kpu.load_kmodel(data)
```

### 单独使用 KPU 进行推理

#### 设置模型输入

在模型推理之前，需要设置对应的模型输入数据：

```Python
data = np.zeros((1, 3, 320, 320), dtype=np.uint8)
kpu_input = nn.from_numpy(data)
kpu.set_input_tensor(0, kpu_input)

# 模型存在多个输入
kpu.set_input_tensor(1, kpu_input_1)
kpu.set_input_tensor(2, kpu_input_2)
```

#### 执行推理并获取推理结果

执行推理并获取结果：

```Python
kpu.run()

result = kpu.get_output_tensor(i)  # 返回第i个输出tensor
data = result.to_numpy()  # 将输出tensor转换为numpy对象
```

### 使用 AI2D+KPU 进行推理

使用 AI2D 对摄像头采集的数据进行预处理，然后使用 KPU 进行推理。有关摄像头等输入设备的配置，请参考[AI Demo说明文档](./AI_Demo说明文档.md)。

#### 配置 AI2D 参数

AI2D 功能包括`crop`、`shift`、`pad`、`resize`、`affine`。根据需求配置相应参数，未使用的功能可忽略。

```Python
# 基础配置：输入、输出layout，输入、输出dtype
ai2d.set_dtype(nncase_runtime.ai2d_format.NCHW_FMT,
               nncase_runtime.ai2d_format.NCHW_FMT, 
               np.uint8, np.uint8)
             
# 功能配置，以pad和resize为例
ai2d.set_pad_param(True, [0, 0, 0, 0, 1, 1, 2, 2], 0, [127, 127, 127])
ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

# 执行配置，需要配置输入、输出shape
ai2d_builder = ai2d.build([1, 3, 224, 224], [1, 3, 256, 256])
```

#### AI2D+KPU 推理

执行 AI2D 与 KPU 结合的推理：

```Python
data = np.zeros((1, 3, 224, 224), dtype=np.uint8)
ai2d_input = nn.from_numpy(data)

# 获取KPU的输入tensor
kpu_input = kpu.get_input_tensor(0)

# 将KPU的输入tensor设置为AI2D的输出
ai2d_builder.run(ai2d_input, kpu_input)
kpu.run()

# 获取KPU的输出tensor
result = kpu.get_output_tensor(i)  # 返回第i个输出tensor
data = result.to_numpy()  # 将输出tensor转换为numpy对象
```

### 释放内存

确保在程序结束前，所有`global`变量的引用计数为0，以避免内存泄漏。也可以在程序开始时调用`gc.collect()`，释放未被释放的内存。

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

## 总结

本模块提供了使用 KPU 和 AI2D 进行深度学习推理的基本框架。开发人员可以根据具体需求配置模型和参数，执行图像处理和推理任务，并注意内存管理以提高程序的稳定性和性能。
