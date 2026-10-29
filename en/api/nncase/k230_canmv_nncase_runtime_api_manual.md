# `nncase_runtime` Module API Manual

## Overview

This manual introduces the nncase_runtime module on the CanMV platform, guiding developers to invoke the KPU (Neural Network Processing Unit) and AI2D modules in a MicroPython environment to achieve efficient deep learning inference and image processing.

| Abbreviation         | Description                                      |
| -------------------- | ------------------------------------------------ |
| nncase_runtime       | k230 nncase runtime package, includes KPU module and AI2D module |
| nncase_runtime.kpu   | kpu module                                       |
| nncase_runtime.ai2d  | ai2d module                                      |

## API Introduction

### from_numpy

**Description**

This function is used to create a runtime_tensor from a ulab.numpy object in MicroPython.

**Syntax**

```python
runtime_tensor = nncase_runtime.from_numpy(ulab.numpy)
```

**Parameters**

| Parameter Name | Description   | Input/Output |
| -------------- | ------------- | ------------ |
| ulab.numpy     | numpy object  | Input        |

**Return Value**

| Return Value  | Description                              |
| ------------- | ---------------------------------------- |
| runtime_tensor | Returns the created runtime_tensor object. |
| Other         | If it fails, a C++ exception will be thrown. |

### to_numpy

**Description**

Converts a runtime_tensor object to a ulab.numpy object.

**Syntax**

```python
runtime_tensor = kpu.get_output_tensor(0)
result = runtime_tensor.to_numpy()
```

**Parameters**

None.

**Return Value**

| Return Value | Description                                            |
| ------------ | ------------------------------------------------------ |
| ulab.numpy   | Returns the ulab.numpy object converted from runtime_tensor. |
| Other        | If it fails, a C++ exception will be thrown.           |

<a id="nncase-runtime-kpu"></a>

### nncase_runtime.kpu

The kpu module provides basic functions for invoking the KPU hardware to perform neural network model inference, including loading models, setting input data, executing inference, and obtaining output results.

#### load_kmodel

**Description**

Loads a neural network model in kmodel format.

**Syntax**

```python
load_kmodel(read_bin)
load_kmodel(path)
```

**Parameters**

| Parameter Name | Description                | Input/Output |
| -------------- | -------------------------- | ------------ |
| read_bin       | Binary content of the kmodel | Input        |
| path           | File path of the kmodel      | Input        |

**Return Value**

| Return Value | Description                              |
| ------------ | ---------------------------------------- |
| None         | Loaded successfully.                     |
| Other        | If it fails, a C++ exception will be thrown. |

#### set_input_tensor

**Description**

Sets the input runtime_tensor for kmodel inference.

**Syntax**

```python
set_input_tensor(index, runtime_tensor)
```

**Parameters**

| Parameter Name | Description                  | Input/Output |
| -------------- | ---------------------------- | ------------ |
| index          | Input index of the kmodel    | Input        |
| runtime_tensor | Tensor containing input data information | Input        |

**Return Value**

| Return Value | Description                              |
| ------------ | ---------------------------------------- |
| None         | Set successfully.                        |
| Other        | If it fails, a C++ exception will be thrown. |

#### get_input_tensor

**Description**

Gets the input runtime_tensor for kmodel inference.

**Syntax**

```python
get_input_tensor(index)
```

**Parameters**

| Parameter Name | Description               | Input/Output |
| -------------- | ------------------------ | ------------ |
| index          | Input index of the kmodel | Input        |

**Return Value**

| Return Value  | Description                          |
| ------------- | ------------------------------------ |
| runtime_tensor | Tensor containing input data information. |
| Other         | If it fails, a C++ exception will be thrown. |

#### set_output_tensor

**Description**

Sets the output result after kmodel inference.

**Syntax**

```python
set_output_tensor(index, runtime_tensor)
```

**Parameters**

| Parameter Name | Description               | Input/Output |
| -------------- | ------------------------- | ------------ |
| index          | Output index of the kmodel | Input        |
| runtime_tensor | Tensor of the output result  | Input        |

**Return Value**

| Return Value | Description                              |
| ------------ | ---------------------------------------- |
| None         | Set successfully.                        |
| Other        | If it fails, a C++ exception will be thrown. |

#### get_output_tensor

**Description**

Gets the output result after kmodel inference.

**Syntax**

```python
get_output_tensor(index)
```

**Parameters**

| Parameter Name | Description               | Input/Output |
| -------------- | ------------------------- | ------------ |
| index          | Output index of the kmodel | Input        |

**Return Value**

| Return Value  | Description                              |
| :------------ | ---------------------------------------- |
| runtime_tensor | Gets the runtime_tensor of the index-th output. |
| Other         | If it fails, a C++ exception will be thrown. |

#### run

**Description**

Starts the kmodel inference process.

**Syntax**

```python
run()
```

**Return Value**

| Return Value | Description                              |
| :----------- | ---------------------------------------- |
| None         | Inference successful                     |
| Other        | If it fails, a C++ exception will be thrown. |

#### inputs_size

**Description**

Gets the number of inputs of the kmodel.

**Syntax**

```python
inputs_size()
```

**Return Value**

| Return Value | Description                              |
| :----------- | ---------------------------------------- |
| size_t       | Number of inputs of the kmodel.          |
| Other        | If it fails, a C++ exception will be thrown. |

#### outputs_size

**Description**

Gets the number of outputs of the kmodel.

**Syntax**

```python
outputs_size()
```

**Return Value**

| Return Value | Description                              |
| :----------- | ---------------------------------------- |
| size_t       | Number of outputs of the kmodel.         |
| Other        | If it fails, a C++ exception will be thrown. |

#### inputs_desc

**Description**

Gets the description information of the input at the specified index.

**Syntax**

```python
inputs_desc(index)
```

**Parameters**

| Parameter Name | Description               | Input/Output |
| -------------- | ------------------------- | ------------ |
| index          | Input index of the kmodel | Input        |

**Return Value**

| Return Value | Description                                          |
| :----------- | ----------------------------------------------------- |
| dict         | Description information of the index-th input, containing the following three keys:<br/>`tensor_datatype`: Data type string, such as `dt_uint8`, `dt_float32`;<br/>`tensor_start`: The start offset of the tensor in the model memory layout, int type;<br/>`tensor_size`: The number of bytes occupied by the tensor, int type. |

#### outputs_desc

**Description**

Gets the description information of the output at the specified index.

**Syntax**

```python
outputs_desc(index)
```

**Parameters**

| Parameter Name | Description               | Input/Output |
| -------------- | ------------------------- | ------------ |
| index          | Output index of the kmodel | Input        |

**Return Value**

| Return Value | Description                                          |
| :----------- | ----------------------------------------------------- |
| dict         | Description information of the index-th output, containing the following three keys:<br/>`tensor_datatype`: Data type string, such as `dt_uint8`, `dt_float32`;<br/>`tensor_start`: The start offset of the tensor in the model memory layout, int type;<br/>`tensor_size`: The number of bytes occupied by the tensor, int type. |

#### release

**Description**

Immediately destroys the model interpreter held by the kpu instance and frees the memory occupied by the kmodel. Equivalent to `__del__`, but does not need to wait for garbage collection to be triggered.

When sequentially loading multiple kmodels in the same application (e.g., multi-model concatenation, application switching), it is recommended to call `release()` immediately after using a model, together with `gc.collect()` and [`shrink_memory_pool`](#shrink-memory-pool) to return memory, otherwise the nncase memory pool may be exhausted and cause subsequent model loading to fail.

**Syntax**

```python
kpu.release()
```

**Parameters**

| Parameter Name | Description | Input/Output |
| -------------- | ----------- | ------------ |
| None           |             |              |

**Return Value**

| Return Value | Description                                       |
| :----------- | ------------------------------------------------- |
| None         | Safe to call repeatedly, the second call does nothing. |

<a id="nncase-runtime-ai2d"></a>

### nncase_runtime.ai2d

#### build

**Description**

Construct an ai2d_builder object.

**Syntax**

```python
build(input_shape, output_shape)
```

**Parameters**

| Name         | Description  |
| ------------ | ------------ |
| input_shape  | Input shape  |
| output_shape | Output shape |

**Return Value**

| Return Value | Description                                        |
| :----------- | -------------------------------------------------- |
| ai2d_builder | Returns the ai2d_builder object for execution.     |
| Other        | If failed, a C++ exception will be thrown.         |

#### run

**Description**

Configure registers and start AI2D computation.

**Syntax**

```python
ai2d_builder.run(input_tensor, output_tensor)
```

**Parameters**  

| Name          | Description   |
| ------------- | ------------- |
| input_tensor  | Input tensor  |
| output_tensor | Output tensor |

**Return Value**  

| Return Value | Description                          |
| ------------ | ------------------------------------ |
| None         | Success.                             |
| Other        | If failed, a C++ exception will be thrown. |

#### set_dtype

**Description**

Set the data type during AI2D computation.

**Syntax**  

```python
set_dtype(src_format, dst_format, src_type, dst_type)
```

**Parameters**

| Name       | Type        | Description         |
| ---------- | ----------- | ------------------- |
| src_format | ai2d_format | Input data format   |
| dst_format | ai2d_format | Output data format  |
| src_type   | datatype_t  | Input data type     |
| dst_type   | datatype_t  | Output data type    |

**Return Value**

| Return Value | Description                          |
| :----- | ------------------------------------ |
| None         | Configuration successful.            |
| Other        | If failed, a C++ exception will be thrown. |

#### set_crop_param

**Description**

Configure crop-related parameters.

**Syntax**  

```python
set_crop_param(crop_flag, start_x, start_y, width, height)
```

**Parameters**  

| Name      | Type | Description                       |
| --------- |---- | --------------------------------- |
| crop_flag | bool | Whether to enable the crop function |
| start_x   | int  | Starting pixel in the width direction |
| start_y   | int  | Starting pixel in the height direction |
| width     | int  | Width                             |
| height    | int  | Height                            |

**Return Value**

| Return Value | Description                          |
| :----- | ------------------------------------ |
| None         | Configuration successful.            |
| Other        | If failed, a C++ exception will be thrown. |

#### set_shift_param

**Description**

Used to configure shift-related parameters.

**Syntax**

```Python
set_shift_param(shift_flag, shift_val)
```

**Parameters**

| Name       | Type | Description                       |
| ---------- | ---- | --------------------------------- |
| shift_flag | bool | Whether to enable the shift function |
| shift_val  | int  | Number of bits to right shift     |

**Return Value**

| Return Value | Description                          |
| :----- | ------------------------------------ |
| None         | Configuration successful.            |
| Other        | If failed, a C++ exception will be thrown. |

#### set_pad_param

**Description**

Used to configure pad-related parameters.

**Syntax**

```Python
set_pad_param(pad_flag, paddings, pad_mode, pad_val)
```

**Parameters**

| Name     | Type | Description                                                                                                                                                                          |
| -------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| pad_flag | bool | Whether to enable the pad function                                                                                                                                                   |
| paddings | list | Padding for each dimension, size=8, in the order of dim0~dim3 (i.e., N/C/H/W), giving the number of paddings on the front and back sides for each dimension, where dim0/dim1 are fixed as {0, 0} |
| pad_mode | int  | Only supports pad constant, configure 0                                                                                                                                              |
| pad_val  | list | Padding value for each channel                                                                                                                                                      |

**Return Value**

| Return Value | Description                          |
| :----- | ------------------------------------ |
| None         | Configuration successful.            |
| Other        | If failed, a C++ exception will be thrown. |

#### set_resize_param

**Description**

Used to configure resize-related parameters.

**Syntax**

```Python
set_resize_param(resize_flag, interp_method, interp_mode)
```

**Parameters**

| Name          | Type               | Description                       |
| ------------- | ------------------ | --------------------------------- |
| resize_flag   | bool               | Whether to enable the resize function |
| interp_method | ai2d_interp_method | Resize interpolation method        |
| interp_mode   | ai2d_interp_mode   | Resize mode                        |

**Return Value**

| Return Value | Description                          |
| :----- | ------------------------------------ |
| None         | Configuration successful.            |
| Other        | If failed, a C++ exception will be thrown. |

#### set_affine_param

**Description**

Used to configure affine-related parameters.

**Syntax**

```Python
set_affine_param(affine_flag, interp_method, cord_round, bound_ind, bound_val, bound_smooth, M)
```

**Parameters**

| Name          | Type               | Description                                                                                                                                                                                     |
| ------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| affine_flag   | bool               | Whether to enable the affine function                                                                                                                                                           |
| interp_method | ai2d_interp_method | Interpolation method used by Affine                                                                                                                                                             |
| cord_round    | uint32_t           | Integer boundary 0 or 1                                                                                                                                                                         |
| bound_ind     | uint32_t           | Boundary pixel mode 0 or 1                                                                                                                                                                      |
| bound_val     | uint32_t           | Boundary fill value                                                                                                                                                                             |
| bound_smooth  | uint32_t           | Boundary smoothing 0 or 1                                                                                                                                                                       |
| M             | list               | Vector corresponding to the affine transformation matrix. If the affine transformation is Y=\[a_0, a_1; a_2, a_3\] \cdot  X + \[b_0, b_1\] $, then M=[a_0,a_1,b_0,a_2,a_3,b_1 ] |

**Return Value**

| Return Value | Description                          |
| :----- | ------------------------------------ |
| None         | Configuration successful.            |
| Other        | If failed, a C++ exception will be thrown. |

#### release

**Description**

Release the native resources held by the ai2d / ai2d_builder instance. Both `nncase_runtime.ai2d` and the `ai2d_builder` returned by `build()` provide this method, which is equivalent to their respective `__del__`, but does not need to wait for garbage collection to be triggered.

An ai2d instance can call `build()` multiple times to produce different builders. When switching preprocessing configurations, the old builder should be released first.

**Syntax**

```python
ai2d_builder.release()    # Release the builder
ai2d.release()            # Release the ai2d instance
```

**Parameters**

| Parameter Name | Description | Input/Output |
| -------------- | ----------- | ------------ |
| None           |             |              |

**Return Value**

| Return Value | Description                                          |
| :----- | ---------------------------------------------------- |
| None         | Safe to call repeatedly; the second call does nothing. |

<a id="shrink-memory-pool"></a>

### shrink_memory_pool

**Description**

Cleans up the memory pool created by nncase_runtime and returns memory that no longer has object references back to the system.

The nncase memory pool only grows and never shrinks. Even after the kpu instance is released, the memory from a loaded kmodel remains in the pool. Therefore, this function must be called **after unloading the model and before loading the next model**. Otherwise, when switching models consecutively, nncase will run out of memory, model loading will fail, or it may even abort directly. The correct sequence is: first call `release()`/`deinit()` to release the instance, then `gc.collect()` to reclaim Python objects, and finally `shrink_memory_pool()`.

**Syntax**

```Python
import gc
import nncase_runtime as nn

kpu.release()               # First release the model instance
gc.collect()                # Then reclaim Python objects
nn.shrink_memory_pool()     # Finally return the memory pool
```

**Parameters**

| Parameter Name | Description | Input/Output |
| -------- | ---- | --------- |
| None       |      |           |

**Return Value**

| Return Value | Description |
| :----- | ---- |
| None     |      |

### version

**Description**

Retrieves the version number of the nncase runtime integrated in the firmware. The version of the on-board runtime must match the **major version** of the nncase compiler used on the PC to convert the kmodel. When versions do not match, loading the kmodel will fail, and this interface can be used to troubleshoot.

**Syntax**

```Python
import nncase_runtime as nn

print(nn.version())
```

**Parameters**

| Parameter Name | Description | Input/Output |
| -------- | ---- | --------- |
| None       |      |           |

**Return Value**

| Return Value | Description                     |
| :----- | ------------------------ |
| str    | nncase runtime version string. |

## Reference Example

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

## Conclusion

By using the nncase_runtime module, developers can implement efficient deep learning inference and image processing functions on the CanMV platform. This manual provides detailed descriptions of the API and usage examples, aiming to help developers get started quickly and efficiently develop related applications.
