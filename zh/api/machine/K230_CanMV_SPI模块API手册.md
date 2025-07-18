# 2.11 `SPI` 模块 API 手册

## 1. 概述

K230 内部集成了三个 SPI 硬件模块，支持片选极性配置和可调时钟速率。通道输出的 I/O 配置可参考 IOMUX 模块。

## 2. API 介绍

SPI 类位于 `machine` 模块中。

### 2.1 示例代码

```python
from machine import SPI

# 初始化 SPI，时钟速率 5 MHz，极性 0，相位 0，数据位宽 8 位
spi = SPI(id, baudrate=5000000, polarity=0, phase=0, bits=8)

# 向从设备发送数据
spi.write(buf)

# 发送数据的同时将接收到的数据读入变量
spi.write_readinto(write_buf, read_buf)

# 关闭 SPI
spi.deinit()
```

### 2.2 构造函数

```python
spi = machine.SPI(id, baudrate=20, polarity=0, phase=0, bits=8)
```

**参数**

- `id`: SPI 模块 ID，取值范围为 [0~2]（对应 `spi.SPI0` 至 `spi.SPI2`）。
- `baudrate`: SPI 时钟速率，计算公式为 \( F_{sclk\_out} = \frac{F_{ssi\_clk}}{BAUDR} \)。
- `polarity`: 时钟极性。
- `phase`: 时钟相位。
- `bits`: 数据位宽。

### 2.3 `read` 方法

```python
spi.read(nbytes)
```

读取指定字节数的数据。

**参数**

- `nbytes`: 要读取的字节数。

**返回值**

返回一个 `bytes` 对象。

### 2.4 `readinto` 方法

```python
spi.readinto(buf)
```

将数据读取到指定的缓冲区中。

**参数**

- `buf`: 类型为 `bytearray` 的缓冲区。

**返回值**

无

### 2.5 `write` 方法

```python
spi.write(buf)
```

发送数据。

**参数**

- `buf`: 类型为 `bytearray` 的数据，定义了要发送的数据及其长度。

**返回值**

无

### 2.6 `write_readinto` 方法

```python
spi.write_readinto(write_buf, read_buf)
```

发送数据的同时，将接收到的数据读取到指定的变量中。

**参数**

- `write_buf`: 类型为 `bytearray` 的数据，定义了要发送的数据及其长度。
- `read_buf`: 类型为 `bytearray` 的缓冲区，用于存放接收到的数据。

**返回值**

无

### 2.7 `deinit` 方法

```python
spi.deinit()
```

注销 SPI 模块。

**参数**

无

**返回值**

无
