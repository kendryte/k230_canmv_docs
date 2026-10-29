# nncase_runtime Module Usage Instructions

## Overview

This document introduces the CanMV nncase_runtime module, guiding developers to use MicroPython to call the `KPU` and `AI2D` modules.

## Functionality Description

### Import Library

Before using the nncase_runtime module, you need to import the relevant libraries:

```Python
import nncase_runtime as nn
import ulab.numpy as np
```

### KPU Initialization

Initialize the model inference module:

```Python
kpu = nn.kpu()
```

### AI2D Initialization

Initialize the image processing module:

```Python
ai2d = nn.ai2d()
```

### Load Model

Load the kmodel using `kpu.load_kmodel()`, which supports passing a file path or binary data.

```Python
# 方式一：传入文件路径
kpu.load_kmodel('/sdcard/examples/kmodel/test.kmodel')

# 方式二：传入二进制数据
with open("/sdcard/examples/kmodel/test.kmodel", "rb") as f:
    data = f.read()
    kpu.load_kmodel(data)
```

After loading is complete, you can use the following interfaces to query the model's input and output information:

```Python
print(kpu.inputs_size())        # 输入个数
print(kpu.outputs_size())       # 输出个数
print(kpu.inputs_desc(0))       # 第0个输入的描述，dict，含 tensor_datatype/tensor_start/tensor_size
print(kpu.outputs_desc(0))      # 第0个输出的描述
```

### Using KPU Standalone for Inference

#### Set Model Input

Before model inference, you need to set the corresponding model input data:

```Python
data = np.zeros((1, 3, 320, 320), dtype=np.uint8)
kpu_input = nn.from_numpy(data)
kpu.set_input_tensor(0, kpu_input)

# 模型存在多个输入
kpu.set_input_tensor(1, kpu_input_1)
kpu.set_input_tensor(2, kpu_input_2)
```

#### Execute Inference and Get Inference Results

Execute inference and get results:

```Python
kpu.run()

result = kpu.get_output_tensor(i)  # 返回第i个输出tensor
data = result.to_numpy()  # 将输出tensor转换为numpy对象
```

### Using AI2D+KPU for Inference

Use AI2D to preprocess data collected by the camera, then use KPU for inference. For configuration of input devices such as the camera, please refer to the [AI Demo User Manual](./ai_demo_user_manual.md).

#### Configuring AI2D Parameters

The AI2D features include `crop`, `shift`, `pad`, `resize`, and `affine`. Configure the corresponding parameters according to your requirements. Unused features can be ignored.

```Python
# Basic configuration: input and output layout, input and output dtype
ai2d.set_dtype(nncase_runtime.ai2d_format.NCHW_FMT,
               nncase_runtime.ai2d_format.NCHW_FMT, 
               np.uint8, np.uint8)
             
# Feature configuration, taking pad and resize as examples
ai2d.set_pad_param(True, [0, 0, 0, 0, 1, 1, 2, 2], 0, [127, 127, 127])
ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

# Execution configuration, needs to configure input and output shape
ai2d_builder = ai2d.build([1, 3, 224, 224], [1, 3, 256, 256])
```

#### AI2D+KPU Inference

Perform inference combining AI2D and KPU:

```Python
data = np.zeros((1, 3, 224, 224), dtype=np.uint8)
ai2d_input = nn.from_numpy(data)

# Get the input tensor of the KPU
kpu_input = kpu.get_input_tensor(0)

# Set the KPU's input tensor as the output of AI2D
ai2d_builder.run(ai2d_input, kpu_input)
kpu.run()

# Get the output tensor of the KPU
result = kpu.get_output_tensor(i)  # Returns the i-th output tensor
data = result.to_numpy()  # Convert the output tensor to a numpy object
```

### Releasing Memory

nncase's memory pool **only grows, never shrinks**: even if a previously loaded kmodel's object is reclaimed, the memory remains in the pool. Therefore, before the program ends or switches models, it must be explicitly released; otherwise, the next model will fail to load due to insufficient memory.

It is recommended to actively release each object using its `release()` method rather than relying on the timing of garbage collection:

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
    # ... configure and build, run inference ...
finally:
    # 1) Release the interpreter first: it holds references to input/output tensors
    if kpu is not None:
        kpu.release()
    # 2) Then release ai2d_builder and ai2d
    if ai2d_builder is not None:
        ai2d_builder.release()
    if ai2d is not None:
        ai2d.release()
    # 3) Reclaim Python objects
    gc.collect()
    # 4) Finally return memory to the nncase memory pool
    nn.shrink_memory_pool()
```

```{admonition} Note
:class: warning
- **The release order cannot be reversed**. The interpreter holds references to input/output tensors; you must call `kpu.release()` before releasing tensors and ai2d.
- `release()` can be called repeatedly; the second call does nothing.
- `shrink_memory_pool()` must be called **after** `gc.collect()`; otherwise objects still hold references and the memory cannot be returned.
- For tensors obtained via `kpu.get_input_tensor(i)` / `get_output_tensor(i)`, set them to `None` for `gc.collect()` to reclaim them after use; do not release them separately before `kpu.release()`.
```

```{admonition} Tip
:class: note
If you use the [`AIBase`](../../api/aidemo/aibase_module_api_manual.md) wrapper library, the entire flow above has already been handled by `AIBase.deinit()` (**including `gc.collect()` and `shrink_memory_pool()`**); you only need to call `app.deinit()` in `finally`. See [Two Main Loop Patterns](../../ai_dev_doc.md#main-loop-patterns) for the complete usage.
```

## Summary

This module provides the basic framework for deep learning inference using KPU and AI2D. Developers can configure models and parameters according to specific needs, perform image processing and inference tasks, and pay attention to memory management to improve program stability and performance.
