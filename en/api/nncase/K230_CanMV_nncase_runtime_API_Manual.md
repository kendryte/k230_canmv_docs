# 4.1 `nncase_runtime` Module API Manual

## 1. Overview

This manual aims to introduce the nncase_runtime module on the CanMV platform, guiding developers to call the KPU (Neural Network Processing Unit) and AI2D modules in a MicroPython environment to achieve efficient deep learning inference and image processing functions.

## 2. API Introduction

### 2.1 from_numpy

**Description**

This function is used to create a runtime_tensor from a ulab.numpy object in MicroPython.

**Syntax**

```python
runtime_tensor = nncase_runtime.from_numpy(ulab.numpy)
```

**Parameters**

| Parameter Name | Description     | Input/Output |
| -------------- | --------------- | ------------ |
| ulab.numpy     | numpy object    | Input        |

**Return Value**

| Return Value   | Description                             |
| -------------- | --------------------------------------- |
| runtime_tensor | Returns the created runtime_tensor object. |
| Others         | Throws a C++ exception if it fails.     |

### 2.2 to_numpy

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

| Return Value   | Description                                      |
| -------------- | ------------------------------------------------- |
| ulab.numpy     | Returns the ulab.numpy object converted from runtime_tensor. |
| Others         | Throws a C++ exception if it fails.               |

### 2.3 nncase_runtime.kpu

The kpu module provides basic functions for calling KPU hardware to perform neural network model inference, including loading models, setting input data, executing inference, and obtaining output results.

#### 2.3.1 load_kmodel

**Description**

Loads a neural network model in kmodel format that has been compiled.

**Syntax**

```python
load_kmodel(read_bin)
load_kmodel(path)
```

**Parameters**

| Parameter Name | Description          | Input/Output |
| -------------- | -------------------- | ------------ |
| read_bin       | Binary content of kmodel | Input        |
| path           | File path of kmodel   | Input        |

**Return Value**

| Return Value | Description            |
| ------------ | ---------------------- |
| None         | Successful load.       |
| Others       | Throws a C++ exception if it fails. |

#### 2.3.2 set_input_tensor

**Description**

Sets the input runtime_tensor for kmodel inference.

**Syntax**

```python
set_input_tensor(index, runtime_tensor)
```

**Parameters**

| Parameter Name | Description             | Input/Output |
| -------------- | ----------------------- | ------------ |
| index          | Input index of kmodel   | Input        |
| runtime_tensor | Tensor containing input data | Input        |

**Return Value**

| Return Value | Description            |
| ------------ | ---------------------- |
| None         | Successful setting.    |
| Others       | Throws a C++ exception if it fails. |

#### 2.3.3 get_input_tensor

**Description**

Gets the input runtime_tensor for kmodel inference.

**Syntax**

```python
get_input_tensor(index)
```

**Parameters**

| Parameter Name | Description            | Input/Output |
| -------------- | ---------------------- | ------------ |
| index          | Input index of kmodel  | Input        |

**Return Value**

| Return Value   | Description                     |
| -------------- | -------------------------------- |
| runtime_tensor | Tensor containing input data.   |
| Others         | Throws a C++ exception if it fails. |

#### 2.3.4 set_output_tensor

**Description**

Sets the output result after kmodel inference.

**Syntax**

```python
set_output_tensor(index, runtime_tensor)
```

**Parameters**

| Parameter Name | Description          | Input/Output |
| -------------- | -------------------- | ------------ |
| index          | Output index of kmodel | Input        |
| runtime_tensor | Tensor of output result | Input        |

**Return Value**

| Return Value | Description            |
| ------------ | ---------------------- |
| None         | Successful setting.    |
| Others       | Throws a C++ exception if it fails. |

#### 2.3.5 get_output_tensor

**Description**

Gets the output result after kmodel inference.

**Syntax**

```python
get_output_tensor(index)
```

**Parameters**

| Parameter Name | Description          | Input/Output |
| -------------- | -------------------- | ------------ |
| index          | Output index of kmodel | Input        |

**Return Value**

| Return Value   | Description                              |
| -------------- | ---------------------------------------- |
| runtime_tensor | Gets the runtime_tensor of the specified output index. |
| Others         | Throws a C++ exception if it fails.      |

#### 2.3.6 run

**Description**

Starts the kmodel inference process.

**Syntax**

```python
run()
```

**Return Value**

| Return Value | Description            |
| ------------ | ---------------------- |
| None         | Successful inference.  |
| Others       | Throws a C++ exception if it fails. |

#### 2.3.7 inputs_size

**Description**

Gets the number of inputs for the kmodel.

**Syntax**

```python
inputs_size()
```

**Return Value**

| Return Value | Description            |
| ------------ | ---------------------- |
| size_t       | Number of inputs for the kmodel. |
| Others       | Throws a C++ exception if it fails. |

#### 2.3.8 outputs_size

**Description**

Gets the number of outputs for the kmodel.

**Syntax**

```python
outputs_size()
```

**Return Value**

| Return Value | Description            |
| ------------ | ---------------------- |
| size_t       | Number of outputs for the kmodel. |
| Others       | Throws a C++ exception if it fails. |

#### 2.3.9 get_input_desc

**Description**

Gets the description information of the specified input index.

**Syntax**

```python
get_input_desc(index)
```

**Parameters**

| Parameter Name | Description          | Input/Output |
| -------------- | -------------------- | ------------ |
| index          | Input index of kmodel | Input        |

**Return Value**

| Return Value  | Description                                           |
| ------------- | ----------------------------------------------------- |
| MemoryRange   | Information of the specified input index, including `dtype`, `start`, `size`. |

#### 2.3.10 get_output_desc

**Description**

Gets the description information of the specified output index.

**Syntax**

```python
get_output_desc(index)
```

**Parameters**

| Parameter Name | Description          | Input/Output |
| -------------- | -------------------- | ------------ |
| index          | Output index of kmodel | Input        |

**Return Value**

| Return Value  | Description                                           |
| ------------- | ----------------------------------------------------- |
| MemoryRange   | Information of the specified output index, including `dtype`, `start`, `size`. |

### 2.4 nncase_runtime.ai2d  

#### 2.4.1 build  

**Description**  

Constructs an `ai2d_builder` object.  

**Syntax**  

```python
build(input_shape, output_shape)
```  

**Parameters**  

| Name         | Description        |
| ------------ | ----------------- |
| input_shape  | Input shape       |
| output_shape | Output shape      |

**Return Value**  

| Return Value  | Description                            |
| ------------- | -------------------------------------- |
| ai2d_builder  | Returns an `ai2d_builder` object for execution. |
| Others        | If the function fails, a C++ exception will be thrown. |

#### 2.4.2 run  

**Description**  

Configures registers and starts the AI2D computation.  

**Syntax**  

```python
ai2d_builder.run(input_tensor, output_tensor)
```  

**Parameters**  

| Name          | Description       |
| ------------- | ---------------- |
| input_tensor  | Input tensor      |
| output_tensor | Output tensor     |

**Return Value**  

| Return Value | Description                        |
| ------------ | --------------------------------- |
| None         | Success.                          |
| Others       | If the function fails, a C++ exception will be thrown. |

#### 2.4.3 set_dtype  

**Description**  

Sets the data type for the AI2D computation process.  

**Syntax**  

```python
set_dtype(src_format, dst_format, src_type, dst_type)
```  

**Parameters**  

| Name       | Type         | Description          |
| ---------- | ----------- | ------------------- |
| src_format | ai2d_format | Input data format  |
| dst_format | ai2d_format | Output data format |
| src_type   | datatype_t  | Input data type    |
| dst_type   | datatype_t  | Output data type   |

#### 2.4.4 set_crop_param  

**Description**  

Configures cropping-related parameters.  

**Syntax**  

```python
set_crop_param(crop_flag, start_x, start_y, width, height)
```  

**Parameters**  

| Name      | Type  | Description                |
| --------- | ---- | ------------------------- |
| crop_flag | bool | Whether to enable cropping |
| start_x   | int  | Starting pixel in width direction |
| start_y   | int  | Starting pixel in height direction |
| width     | int  | Crop width                 |
| height    | int  | Crop height                |

#### 2.4.5 set_shift_param  

**Description**  

Configures shift-related parameters.  

**Definition**  

```python
set_shift_param(shift_flag, shift_val)
```  

**Parameters**  

| Name       | Type | Description                     |
| ---------- | ---- | ----------------------------- |
| shift_flag | bool | Whether to enable shift       |
| shift_val  | int  | Number of bits to shift right |

#### 2.4.6 set_pad_param  

**Description**  

Configures padding-related parameters.  

**Definition**  

```python
set_pad_param(pad_flag, paddings, pad_mode, pad_val)
```  

**Parameters**  

| Name     | Type  | Description                                                                                       |
| -------- | ----- | ------------------------------------------------------------------------------------------------- |
| pad_flag | bool  | Whether to enable padding                                                                         |
| paddings | list  | Padding for each dimension (size = 8), representing front and back padding for dim0 to dim4. `dim0/dim1` are fixed as `{0, 0}`. |
| pad_mode | int   | Supports only `pad constant`, set to `0`.                                                         |
| pad_val  | list  | Padding values for each channel.                                                                 |

#### 2.4.7 set_resize_param  

**Description**  

Configures resize-related parameters.  

**Definition**  

```python
set_resize_param(resize_flag, interp_method, interp_mode)
```  

**Parameters**  

| Name          | Type               | Description          |
| ------------- | ------------------ | -------------------- |
| resize_flag   | bool               | Whether to enable resizing |
| interp_method | ai2d_interp_method | Resize interpolation method |
| interp_mode   | ai2d_interp_mode   | Resize mode |

#### 2.4.8 set_affine_param  

**Description**  

Configures affine transformation-related parameters.  

**Definition**  

```python
set_affine_param(affine_flag, interp_method, cord_round, bound_ind, bound_val, bound_smooth, M)
```  

**Parameters**  

| Name          | Type               | Description                                                                 |
| ------------- | ------------------ | --------------------------------------------------------------------------- |
| affine_flag   | bool               | Whether to enable affine transformation                                    |
| interp_method | ai2d_interp_method | Interpolation method used in affine transformation                         |
| cord_round    | uint32_t           | Integer boundary (0 or 1)                                                  |
| bound_ind     | uint32_t           | Boundary pixel mode (0 or 1)                                               |
| bound_val     | uint32_t           | Boundary fill value                                                        |
| bound_smooth  | uint32_t           | Boundary smoothing (0 or 1)                                                |
| M             | list               | Affine transformation matrix vector. The transformation is given by:  \[Y = \begin{bmatrix} a_0 & a_1 \\ a_2 & a_3 \end{bmatrix}\cdot X + \begin{bmatrix} b_0 \\ b_1 \end{bmatrix}\] Thus, `M = [a_0, a_1, b_0, a_2, a_3, b_1]`. |

### 2.5 Other Functions of nncase_runtime

- **Image Processing Functions:**  
  nncase_runtime also provides various image processing functions, including image scaling, rotation, flipping, etc.

- **Deep Learning Inference:**  
  This module supports inference of various deep learning models with good compatibility.

## 3. Reference Examples

### 3.1 Inference Using KPU

```python
import nncase_runtime as runtime

# Load model
with open("model.kmodel", "rb") as f:
    model_data = f.read()
runtime.load_kmodel(model_data)

# Set input
input_tensor = runtime.from_numpy(input_data)
runtime.set_input_tensor(0, input_tensor)

# Run inference
runtime.run()

# Get output
output_tensor = runtime.get_output_tensor(0)
result = output_tensor.to_numpy()
```

### 3.2 Image Processing Using AI2D

```python
import nncase_runtime as runtime

# Build AI2D
builder = runtime.build((input_height, input_width, channels), (output_height, output_width, channels))

# Set data type
builder.set_dtype(runtime.AI2D_FORMAT_RGB, runtime.AI2D_FORMAT_RGB, runtime.DTYPE_UINT8, runtime.DTYPE_UINT8)

# Configure cropping
builder.set_crop_param(True, 10, 10, 100, 100)

# Execute computation
builder.run(input_tensor, output_tensor)
```

## 4. Conclusion

By using the nncase_runtime module, developers can achieve efficient deep learning inference and image processing functions on the CanMV platform. This manual provides detailed descriptions and usage examples of the API, aiming to help developers get started quickly and develop related applications efficiently.
