# nncase_runtime Module Usage Guide

## Overview

This document introduces the CanMV nncase_runtime module, guiding developers on how to use MicroPython to call the `KPU` and `AI2D` modules.

## Function Introduction

### Import Libraries

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

There are two ways to load the model: by file path or binary data.

```Python
# By file path
model = nn.load_model('test.kmodel')

# By binary data
with open("test.kmodel", "rb") as f:
    data = f.read()
    kpu.load_kmodel(data)
```

### Using KPU for Inference Alone

#### Set Model Input

Before model inference, you need to set the corresponding model input data:

```Python
data = np.zeros((1, 3, 320, 320), dtype=np.uint8)
kpu_input = nn.from_numpy(data)
kpu.set_input_tensor(0, kpu_input)

# If the model has multiple inputs
kpu.set_input_tensor(1, kpu_input_1)
kpu.set_input_tensor(2, kpu_input_2)
```

#### Execute Inference and Get Results

Execute inference and get results:

```Python
kpu.run()

result = kpu.get_output_tensor(i)  # Returns the i-th output tensor
data = result.to_numpy()  # Converts the output tensor to a numpy object
```

### Using AI2D+KPU for Inference

Use AI2D to preprocess data collected from the camera, then use KPU for inference. For configuration of input devices such as cameras, refer to the [AI Demo Documentation](../../../zh/example/ai/AI_Demo说明文档.md).

#### Configure AI2D Parameters

AI2D functions include `crop`, `shift`, `pad`, `resize`, `affine`. Configure the corresponding parameters as needed; unused functions can be ignored.

```Python
# Basic configuration: input/output layout, input/output dtype
ai2d.set_dtype(nncase_runtime.ai2d_format.NCHW_FMT,
               nncase_runtime.ai2d_format.NCHW_FMT, 
               np.uint8, np.uint8)
              
# Function configuration, taking pad and resize as examples
ai2d.set_pad_param(True, [0, 0, 0, 0, 1, 1, 2, 2], 0, [127, 127, 127])
ai2d.set_resize_param(True, nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)

# Execute configuration, need to configure input/output shape
ai2d_builder = ai2d.build([1, 3, 224, 224], [1, 3, 256, 256])
```

#### AI2D+KPU Inference

Execute AI2D and KPU combined inference:

```Python
data = np.zeros((1, 3, 224, 224), dtype=np.uint8)
ai2d_input = nn.from_numpy(data)

# Get the input tensor for KPU
kpu_input = kpu.get_input_tensor(0)

# Set the output of AI2D as the input of KPU
ai2d_builder.run(ai2d_input, kpu_input)
kpu.run()

# Get the output tensor of KPU
result = kpu.get_output_tensor(i)  # Returns the i-th output tensor
data = result.to_numpy()  # Converts the output tensor to a numpy object
```

### Release Memory

Ensure that all `global` variable reference counts are zero before the program ends to avoid memory leaks. You can also call `gc.collect()` at the beginning of the program to release any unreleased memory.

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

## Summary

This module provides a basic framework for using KPU and AI2D for deep learning inference. Developers can configure models and parameters according to specific needs, perform image processing and inference tasks, and manage memory to improve program stability and performance.
