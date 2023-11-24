# spi - spi例程

本示例程序用于对 CanMV 开发板进行spi读取flash id的功能展示。

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

具体接口定义请参考 [I2C](../../../api/machine/K230_CanMV_SPI模块API手册.md)
