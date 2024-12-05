# 5. SPI 例程

## 1. 概述

K230 内部集成了三个 SPI 硬件模块，支持配置片选的极性和时钟速率。SPI 通道的输出 IO 可以通过 IOMUX 模块进行配置，非常适合高速数据传输。

## 2. 示例

以下示例展示了如何使用 SPI 接口读取 Flash 存储器的 ID。

```python
from machine import SPI
from machine import FPIOA

# 实例化SPI的gpio
a = FPIOA()

# 打印gpio14的属性
a.help(14)
# 设置gpio14为QSPI0_CS0功能
a.set_function(14,a.QSPI0_CS0)
a.help(14)

# 打印gpio15的属性
a.help(15)
# 设置gpio15为QSPI0_CLK功能
a.set_function(15,a.QSPI0_CLK)
a.help(15)

# 打印gpio16的属性
a.help(16)
# 设置gpio16为QSPI0_D0功能
a.set_function(16,a.QSPI0_D0)
a.help(16)

# 打印gpio17的属性
a.help(17)
# 设置gpio17为QSPI0_D1功能
a.set_function(17,a.QSPI0_D1)
a.help(17)

# 实例化SPI，使用5MHz时钟，极性为0，数据位宽为8bit
spi=SPI(1,baudrate=5000000, polarity=0, phase=0, bits=8)

# 使能 gd25lq128 复位
spi.write(bytes([0x66]))
# gd25lq128 复位
spi.write(bytes([0x99]))

# 读id命令（0x9f）
a=bytes([0x9f])
# 创建长度为3的接收buff
b=bytearray(3)
# 读id
spi.write_readinto(a,b)
# 打印为：bytearray(b'\xc8`\x18')
print(b)

# 读id命令（0x90,0,0,0）
a=bytes([0x90,0,0,0])
# 创建长度为2的接收buff
b=bytearray(2)
# 读id
spi.write_readinto(a,b)
# 打印为：bytearray(b'\xc8\x17')
print(b)
```

## 3.代码说明

1. **FPIOA 配置**：
   - 通过 `FPIOA` 模块，配置用于 SPI 的 GPIO 引脚（如 CS、CLK 和数据线）。
   - 使用 `help()` 函数查看 GPIO 引脚的当前状态，确保其正确设置。

1. **SPI 初始化**：
   - 实例化 `SPI` 对象，设置波特率为 5 MHz，极性和相位均为 0，数据位宽为 8 位。

1. **Flash 存储器操作**：
   - 发送复位命令（0x66 和 0x99）以初始化 Flash 存储器。
   - 读取存储器 ID，使用命令 0x9F 和 0x90，读取 ID 并打印结果。

```{admonition} 提示
有关 SPI 模块的详细接口和使用方法，请参考[API文档](../../api/machine/K230_CanMV_SPI模块API手册.md)
```
