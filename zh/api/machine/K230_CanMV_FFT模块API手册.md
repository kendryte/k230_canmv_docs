# `FFT` 模块 API 手册

## 概述

FFT（快速傅里叶变换）模块用于对输入的时域数据进行傅里叶变换，将其转换为频域数据并返回相应的频率幅值。通过 FFT 运算，可以有效地将时域信号转换为频域信号，便于分析信号的频率成分。

## API 介绍

FFT 模块提供了一个 `FFT` 类，支持三个主要函数：`run()`、`freq()` 和 `amplitude()`，用于分别进行快速傅里叶变换、频率计算及幅值计算。

### 类 `machine.FFT`

**描述**

该类用于创建 FFT 对象，并对输入的数据进行傅里叶变换。

**语法**

```python
from machine import FFT
import array

# 定义时域数据
data = array.array('i', [1, 2, 3, 4, 5, 6, 7, 8])

# 创建一个 FFT 对象，执行 64 点 FFT 运算，偏移量为 0
fft1 = FFT(data, 64, 0)
```

**参数**

| 参数名称  | 描述                                             | 类型   | 输入/输出 |
|-----------|--------------------------------------------------|--------|-----------|
| `data`    | 输入的时域数据，`bytearray` 类型。               |          | 输入   |
| `points`  | FFT 运算的点数，支持 64、128、256、512、1024、2048 和 4096 点。 |     | 输入   |
| `shift`   | 数据的偏移量，默认为 0。                         |          | 输入   |

**返回值**

| 返回值  | 描述   |
|---------|--------|
| 0       | 操作成功。 |
| 非 0    | 操作失败。 |

### `run()` 方法

**描述**

该函数用于获取经过傅里叶变换后的频域数据。

**语法**

```python
res = fft1.run()
```

**参数**

无

**返回值**

| 返回值  | 描述                                       |
|---------|--------------------------------------------|
| `res`   | 返回一个包含频域数据的 `list`，其中包含 `points` 个元组，每个元组包含 2 个元素：实部和虚部。 |

### `freq()` 方法

**描述**
该函数用于获取计算后的频率值。

**语法**

```python
res = FFT.freq(points, sample_rate)
```

**参数**

| 参数名称     | 描述                   | 输入/输出 |
|--------------|------------------------|-----------|
| `points`     | 参与 FFT 运算的点数。   | 输入      |
| `sample_rate`| 数据采样率。            | 输入      |

**返回值**

| 返回值  | 描述                                 |
|---------|--------------------------------------|
| `res`   | 返回一个列表，包含运算后各频率点的频率值。 |

### `amplitude()` 方法

**描述**
该函数用于计算各个频率点的幅值，主要用于测试用途，用户可自行在 Python 中编写更加复杂的幅值处理函数。

**语法**

```python
amp = FFT.amplitude(FFT_res)
```

**参数**

| 参数名称     | 描述                               | 输入/输出 |
|--------------|------------------------------------|-----------|
| `FFT_res`    | 函数 `run()` 返回的 FFT 计算结果。 | 输入      |

**返回值**

| 返回值  | 描述                              |
|---------|-----------------------------------|
| `amp`   | 返回一个列表，包含各个频率点的幅值。 |
