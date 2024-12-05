# 4. I2C Example

## 1. Overview

The K230 chip integrates 5 I2C hardware modules, supporting standard mode (100 kb/s), fast mode (400 kb/s), and high-speed mode (3.4 Mb/s). These modules are ideal for I2C communication on development boards, such as connecting peripherals (like sensors or displays). The output IO of the I2C channels can be configured through the IOMUX module.

## 2. Example

The following example demonstrates how to use the I2C 4 module to read the ID of an HDMI device.

```python
from machine import I2C

# Instantiate I2C4, using the default 100KHz clock and 7-bit address mode
i2c4 = I2C(4)

# Scan for devices connected to I2C4, find the HDMI address
a = i2c4.scan()
print(a)  # Output the device address, usually 59 (0x3B)

# Write 0x80 to HDMI page address register 0xFF, data width is 8 bits
i2c4.writeto_mem(0x3b, 0xff, bytes([0x80]), mem_size=8)

# Read HDMI ID address 0, data width is 8 bits, expected to return 0x17
i2c4.readfrom_mem(0x3b, 0x00, 1, mem_size=8)

# Read HDMI ID address 1, data width is 8 bits, expected to return 0x02
i2c4.readfrom_mem(0x3b, 0x01, 1, mem_size=8)

# More detailed operations, including read and write operations
i2c4.writeto(0x3b, bytes([0xff, 0x80]), True)
i2c4.writeto(0x3b, bytes([0x00]), True)
i2c4.readfrom(0x3b, 1)
```

```{admonition} Tip
For detailed interfaces and usage of the I2C module, please refer to the [API documentation](../../api/machine/K230_CanMV_I2C_Module_API_Manual.md).
```
