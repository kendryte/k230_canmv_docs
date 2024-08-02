# 4. I2C 例程

## 1. 概述

K230内部包含五个I2C硬件模块，支持标准100kb/s，快速400kb/s模式，高速模式3.4Mb/s。
通道输出IO配置参考IOMUX模块。

## 2. 示例

本示例程序用于对 CanMV 开发板进行i2c读取hdmi id的功能展示。

```python
from machine import I2C
# 实例化I2C4,使用默认100KHz时钟,7 bit地址模式
i2c4=I2C(4)

# 扫描I2C4连接的hdmi地址
a=i2c4.scan()
# 打印I2C4连接的hdmi地址，59
print(a)

# hdmi地址0x3b(即59),写hdmi页地址寄存器（0xff）为0x80,位宽为8bits
i2c4.writeto_mem(0x3b,0xff,bytes([0x80]),mem_size=8)
# hdmi地址0x3b(即59),读id地址0,位宽为8bits,值为0x17
i2c4.readfrom_mem(0x3b,0x00,1,mem_size=8)
# hdmi地址0x3b(即59),读id地址1,位宽为8bits,值为0x2
i2c4.readfrom_mem(0x3b,0x01,1,mem_size=8)

# hdmi地址0x3b(即59),写hdmi页地址寄存器（0xff）为0x80
i2c4.writeto(0x3b,bytes([0xff,0x80]),True)
# hdmi地址0x3b(即59)，发送要被读取的id地址0
i2c4.writeto(0x3b,bytes([0x00]),True)
# hdmi地址0x3b(即59)，读返回的id,值为0x17
i2c4.readfrom(0x3b,1)
# hdmi地址0x3b(即59)，发送要被读取的id地址1
i2c4.writeto(0x3b,bytes([0x01]),True)
# hdmi地址0x3b(即59)，读返回的id,值为0x2
i2c4.readfrom(0x3b,1)

# hdmi地址0x3b(即59),写hdmi页地址寄存器（0xff）为0x80,位宽为8bits
i2c4.writeto_mem(0x3b,0xff,bytes([0x80]),mem_size=8)
# 创建长度为1的接收buff
a=bytearray(1)
# hdmi地址0x3b(即59),读id地址0,位宽为8bits
i2c4.readfrom_mem_into(0x3b,0x0,a,mem_size=8)
# 打印buff,值为0x17
print(a)

# hdmi地址0x3b(即59),写hdmi页地址寄存器（0xff）为0x80
i2c4.writeto(0x3b,bytes([0xff,0x80]),True)
# hdmi地址0x3b(即59),发送要被读取的id地址0
i2c4.writeto(0x3b,bytes([0x00]),True)
# 创建长度为1的接收buff
b=bytearray(1)
# hdmi地址0x3b(即59),读返回的id,
i2c4.readfrom_into(0x3b,b)
# 打印buff,值为0x17
print(b)
```

```{admonition} 提示
I2C模块具体接口请参考[API文档](../../api/machine/K230_CanMV_I2C模块API手册.md)
```
