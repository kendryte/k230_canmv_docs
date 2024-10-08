# 11. FFT 例程

## 1. 概述

FFT（快速傅里叶变换）模块可以对输入数据进行傅里叶变换，并返回相应的频率幅值。通过 FFT 运算，时域信号可以转换为频域信号，有助于分析信号的频率成分。

## 2. 示例

以下示例展示了如何使用 FFT 模块进行傅里叶变换。

```python
from machine import FFT
import array
import math
from ulab import numpy as np

PI = 3.14159265358979323846264338327950288419716939937510

rx = []

def input_data():
    for i in range(64):
        data0 = 10 * math.cos(2 * PI * i / 64)
        data1 = 20 * math.cos(2 * 2 * PI * i / 64)
        data2 = 30 * math.cos(3 * 2 * PI * i / 64)
        data3 = 0.2 * math.cos(4 * 2 * PI * i / 64)
        data4 = 1000 * math.cos(5 * 2 * PI * i / 64)
        rx.append(int(data0 + data1 + data2 + data3 + data4))

input_data()  # 初始化需要进行 FFT 的数据，列表类型
print(rx)

data = np.array(rx, dtype=np.uint16)  # 把列表数据转换成数组
print(data)

fft1 = FFT(data, 64, 0x555)  # 创建一个 FFT 对象，运算点数为 64，偏移是 0x555
res = fft1.run()  # 获取 FFT 转换后的数据
print(res)

res = fft1.amplitude(res)  # 获取各个频率点的幅值
print(res)

res = fft1.freq(64, 38400)  # 获取所有频率点的频率值
print(res)
```

## 3. 代码说明

1. **导入模块**：
   - 导入所需的模块，包括 `FFT`、`array`、`math` 和 `numpy`。

1. **输入数据函数**：
   - 定义 `input_data()` 函数生成 64 个数据点，模拟不同频率的余弦波并将其存储在 `rx` 列表中。

1. **数据转换**：
   - 将列表 `rx` 转换为 NumPy 数组 `data`，并指定数据类型为无符号 16 位整型。

1. **创建 FFT 对象**：
   - 使用 `FFT(data, 64, 0x555)` 创建一个 FFT 对象，设置运算点数为 64，偏移量为 `0x555`。

1. **运行 FFT**：
   - 调用 `fft1.run()` 执行傅里叶变换，返回结果存储在 `res` 中。

1. **获取幅值**：
   - 使用 `fft1.amplitude(res)` 获取转换后的各个频率点的幅值，并打印。

1. **获取频率值**：
   - 调用 `fft1.freq(64, 38400)` 获取所有频率点的频率值，并打印。

```{admonition} 提示
FFT 模块具体接口请参考 [API 文档](../../api/machine/K230_CanMV_FFT模块API手册.md)
```
