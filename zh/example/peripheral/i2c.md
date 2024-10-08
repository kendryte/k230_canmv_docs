# 4. I2C 例程

## 1. 概述

K230 芯片内部集成了 5 个 I2C 硬件模块，支持标准模式（100 kb/s）、快速模式（400 kb/s）以及高速模式（3.4 Mb/s）。这些模块非常适合在开发板上进行 I2C 通信，例如连接外设（如传感器或显示器）。I2C 通道的输出 IO 可通过 IOMUX 模块进行配置。

## 2. 示例

以下示例展示了如何使用 I2C 4 模块读取 HDMI 设备的 ID。

```python
from machine import I2C

# 实例化 I2C4，使用默认的 100KHz 时钟和 7 位地址模式
i2c4 = I2C(4)

# 扫描 I2C4 连接的设备，找到 HDMI 地址
a = i2c4.scan()
print(a)  # 输出设备地址，通常为 59 (0x3B)

# 向 HDMI 页地址寄存器 0xFF 写入 0x80，数据宽度为 8 位
i2c4.writeto_mem(0x3b, 0xff, bytes([0x80]), mem_size=8)

# 读取 HDMI ID 地址 0，数据宽度为 8 位，期望返回 0x17
i2c4.readfrom_mem(0x3b, 0x00, 1, mem_size=8)

# 读取 HDMI ID 地址 1，数据宽度为 8 位，期望返回 0x02
i2c4.readfrom_mem(0x3b, 0x01, 1, mem_size=8)

# 更详细的操作，包括读写操作
i2c4.writeto(0x3b, bytes([0xff, 0x80]), True)
i2c4.writeto(0x3b, bytes([0x00]), True)
i2c4.readfrom(0x3b, 1)

```

```{admonition} 提示
有关 I2C 模块的详细接口和使用方法，请参考[API文档](../../api/machine/K230_CanMV_I2C模块API手册.md)
```
