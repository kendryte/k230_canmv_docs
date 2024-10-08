# 4.1 nncase_runtime 模块 API 手册

## 1. 概述

本手册旨在介绍 CanMV 平台的 nncase_runtime 模块，指导开发人员在 MicroPython 环境下调用 KPU（神经网络处理单元）及 AI2D 模块，以实现高效的深度学习推理和图像处理功能。

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
| --------- |

 ---- | ------------------ |
| crop_flag | bool | 是否启用裁剪功能   |
| start_x   | int  | 宽度方向的起始像素 |
| start_y   | int  | 高度方向的起始像素 |
| width     | int  | 宽度               |
| height    | int  | 高度               |

### 2.5 nncase_runtime 其他功能

- **图像处理功能：**  
  nncase_runtime 还提供了多种图像处理功能，包括图像缩放、旋转、翻转等。

- **深度学习推理：**  
  该模块支持多种深度学习模型的推理，具有良好的兼容性。

## 3. 参考示例

### 3.1 使用 KPU 进行推理

```python
import nncase_runtime as runtime

# 加载模型
with open("model.kmodel", "rb") as f:
    model_data = f.read()
runtime.load_kmodel(model_data)

# 设置输入
input_tensor = runtime.from_numpy(input_data)
runtime.set_input_tensor(0, input_tensor)

# 执行推理
runtime.run()

# 获取输出
output_tensor = runtime.get_output_tensor(0)
result = output_tensor.to_numpy()
```

### 3.2 使用 AI2D 进行图像处理

```python
import nncase_runtime as runtime

# 构建 AI2D
builder = runtime.build((input_height, input_width, channels), (output_height, output_width, channels))

# 设置数据类型
builder.set_dtype(runtime.AI2D_FORMAT_RGB, runtime.AI2D_FORMAT_RGB, runtime.DTYPE_UINT8, runtime.DTYPE_UINT8)

# 配置裁剪
builder.set_crop_param(True, 10, 10, 100, 100)

# 执行计算
builder.run(input_tensor, output_tensor)
```

## 4. 结论

通过使用 nncase_runtime 模块，开发人员能够在 CanMV 平台上实现高效的深度学习推理和图像处理功能。本手册提供了 API 的详细描述和使用示例，旨在帮助开发人员快速上手并高效开发相关应用。
