# FFT 例程

## 什么是 FFT？

**FFT（Fast Fourier Transform）快速傅里叶变换**
是一种高效的算法，用于将信号从时域转换到频域，从而分析信号中包含的频率成分及其幅度。换句话说，FFT 能告诉我们：

* 信号中有哪些频率
* 各个频率对应的强度（幅值）

**FFT** 广泛应用于：

* 音频频谱分析（如音乐可视化）
* 图像频率分析（如滤波）
* 通信系统（调制、解调）
* 振动分析、雷达信号处理

## FFT 使用示例

本示例将先合成一个已知的复合信号，然后利用 FFT 对其进行分析，直观展示时域波形与频域频谱之间的对应关系。

### 1. 导入必要模块

```python
import ulab
from ulab import numpy as np
import math
```

### 2. 合成复合信号

正弦波的数学表达式通常表示为：

$$
y(t) = A \cdot \sin(2\pi f t + \phi)
$$

其中含义如下：

* $A$：振幅（Amplitude）——波峰的高度；
* $f$：频率（Frequency）——每秒钟震动次数，单位是 Hz；
* $t$：时间（Time）；
* $\phi$：初相位（Phase）——波形的初始偏移，单位是弧度（radians）；
* $2\pi f$：角频率（Angular frequency）——单位是 rad/s。

在嵌入式系统中，浮点计算（尤其是双精度）代价较高，因此常用定点数进行运算。

下面的代码将合成一个由 50 Hz 基频及其 3 倍频（150 Hz）、5 倍频（250 Hz）组成的信号，并使幅度依次递减。

```python
fs = 1280       # 采样率
duration = 1     # 秒
amplitude = 32767 # 定点数最大幅度（int16）
N = 128  # FFT 点数

n_samples = int(fs * duration)
# 创建一个从0到n_samples-1的数组
n = np.arange(n_samples, dtype=np.int16)

# 设定三个基频
f1, f2, f3 = 50, 150, 250

# 生成三个正弦波
sin_f1 = np.sin(2 * math.pi * f1 * n / fs)/3
sin_f2 = np.sin(2 * math.pi * f2 * n / fs)/3
sin_f3 = np.sin(2 * math.pi * f3 * n / fs)/3

# 组合波形
signal = amplitude * 0.5 * sin_f1 + amplitude * 0.25 * sin_f2 + amplitude * 0.125 * sin_f3

# 将浮点数结果转换为 int16 类型
signal_fixed = np.zeros(len(signal), dtype=np.int16)
for i in range(len(signal)):
    signal_fixed[i] = int(signal[i])

# 打印前20个采样点
print(signal_fixed[0:20])
```

合成波形示意：
![Origal Waveform](https://www.kendryte.com/api/post/attachment?id=644)

### 3. FFT 分析

使用 K230 的 FFT 硬件模块对信号进行分析：

```python
# N 为 FFT 点数，0x555 为硬件缩放因子（推荐默认值）
fft = FFT(signal_fixed, N, 0x555)   
res = fft.run()

amps = fft.amplitude(res)  # 获取各个频率点的幅值
print(amps)

freqs = fft.freq(N, 1280)  # 获取所有频率点的频率值
print(freqs)
```

频谱结果如下图所示，可见 50 Hz、150 Hz、250 Hz 处存在显著峰值，且幅度比约为 4 : 2 : 1，与信号合成时的设置一致。
![FFT waveform](https://www.kendryte.com/api/post/attachment?id=643)

## 4. 频率分辨率 Δf

FFT 点数 \$N\$ 表示一次变换所使用的采样点数量，**频率分辨率**为：

$$
\Delta f = \frac{f_s}{N}
$$

其中 \$f\_s\$ 为采样率。

例如，当 \$f\_s = 16,\text{kHz}\$ 时：

| FFT 点数 | 时间窗长度 (ms) | 频率分辨率 Δf (Hz) |
| -------- | --------------- | ------------------ |
| 64       | 4.0             | 250                |
| 128      | 8.0             | 125                |
| 256      | 16.0            | 62.5               |

说明：

* N 越大，Δf 越小，频率分辨率越高
* N 越小，时间分辨率越高，更适合捕捉瞬态信号

## ⚠ 注意事项

| 项目                        | 说明                                                                    |
| --------------------------- | ----------------------------------------------------------------------- |
| **采样率（Sampling Rate）** | 影响你能检测的最大频率（最高只能检测 `采样率的一半`，称为奈奎斯特频率） |
| **信号长度**                | FFT 输出的频率分辨率 = 采样率 / 信号长度                                |
| **复数结果**                | FFT 输出是复数，通常取其 **模（magnitude）** 表示能量                   |
| **归一化处理**              | 输出的幅值往往需要乘以某些系数（如 `2 / N`）进行归一化                  |

## 延伸阅读

* [K230 FFT API 文档](../../api/machine/K230_CanMV_FFT模块API手册.md)
