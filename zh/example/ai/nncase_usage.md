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

加载 kmodel 使用 `kpu.load_kmodel()`，支持传入文件路径或二进制数据两种方式。

```Python
# 方式一：传入文件路径
kpu.load_kmodel('/sdcard/examples/kmodel/test.kmodel')

# 方式二：传入二进制数据
with open("/sdcard/examples/kmodel/test.kmodel", "rb") as f:
    data = f.read()
    kpu.load_kmodel(data)
```

加载完成后，可以通过下面的接口查询模型的输入输出信息：

```Python
print(kpu.inputs_size())        # 输入个数
print(kpu.outputs_size())       # 输出个数
print(kpu.inputs_desc(0))       # 第0个输入的描述，dict，含 tensor_datatype/tensor_start/tensor_size
print(kpu.outputs_desc(0))      # 第0个输出的描述
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

使用 AI2D 对摄像头采集的数据进行预处理，然后使用 KPU 进行推理。有关摄像头等输入设备的配置，请参考[AI Demo说明文档](./ai_demo_user_manual.md)。

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

nncase 的内存池**只增不减**：加载过的 kmodel 即使对象被回收，内存仍然留在池中。因此程序结束或切换模型前必须显式释放，否则下一个模型会因内存不足而加载失败。

推荐使用各对象的 `release()` 方法主动释放，不要依赖垃圾回收的时机：

```Python
import nncase_runtime as nn
import gc

kpu = None
ai2d = None
ai2d_builder = None
try:
    kpu = nn.kpu()
    kpu.load_kmodel(kmodel_path)
    ai2d = nn.ai2d()
    # ... 配置并 build、推理 ...
finally:
    # 1) 先释放解释器：它持有输入/输出 tensor 的引用
    if kpu is not None:
        kpu.release()
    # 2) 再释放 ai2d_builder 和 ai2d
    if ai2d_builder is not None:
        ai2d_builder.release()
    if ai2d is not None:
        ai2d.release()
    # 3) 回收 Python 对象
    gc.collect()
    # 4) 最后把内存归还给 nncase 内存池
    nn.shrink_memory_pool()
```

```{admonition} 注意
:class: warning
- **释放顺序不能颠倒**。解释器持有输入/输出 tensor 的引用，必须先 `kpu.release()` 再释放 tensor 和 ai2d。
- `release()` 可以重复调用，第二次调用不做任何事。
- `shrink_memory_pool()` 必须在 `gc.collect()` **之后**调用，否则还有对象持有引用，内存归还不掉。
- 通过 `kpu.get_input_tensor(i)` / `get_output_tensor(i)` 取出的 tensor，用完后置 `None` 让 `gc.collect()` 回收即可，不要在 `kpu.release()` 之前单独释放它们。
```

```{admonition} 提示
:class: note
如果使用 [`AIBase`](../../api/aidemo/aibase_module_api_manual.md) 封装库，上面这一整套流程已经由 `AIBase.deinit()` 完成（**包含 `gc.collect()` 和 `shrink_memory_pool()`**），只需在 `finally` 里调用 `app.deinit()`。完整写法见 [两种主循环写法](../../ai_dev_doc.md#main-loop-patterns)。
```

## 总结

本模块提供了使用 KPU 和 AI2D 进行深度学习推理的基本框架。开发人员可以根据具体需求配置模型和参数，执行图像处理和推理任务，并注意内存管理以提高程序的稳定性和性能。
