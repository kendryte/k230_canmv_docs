# 2.8 `I2C_Slave` 模块 API 手册

## 1. 概述

K230 I2C 控制器默认工作在主机模式，但也能通过定制固件，切换为从机模式。要想开启从模式，请在编译固件时使用 `make rtsmart-menuconfig` 配置打开 `Enable I2Cx SLAVE mode` 选项（路径：Drivers Configuration > InterDriver > Enable I2C > Enable I2Cx SLAVE mode），然后重新编译固件。

![menuconfig](https://www.kendryte.com/api/post/attachment?id=639)

## 2. 从设备 API 介绍

`I2C_Slave` 类位于 `machine` 模块中。

### 2.1 示例代码

以下示例应用中，我们将一个 K230 作为主设备，使用另一个 K230 作为从设备，演示主机和从机通过 I2C 总线进行通信。其中从机 IO14 用于在数据发生变化时通知主设备读取数据。

**从机代码**：

```python
from machine import Pin, FPIOA, I2C_Slave
import time
import os

# 实例化 FPIOA
fpioa = FPIOA()
# 设置 Pin14 为 GPIO输出模式，用于通知主机有数据更新，初始化为输出高电平
fpioa.set_function(14, FPIOA.GPIO14)
pin = Pin(14, Pin.OUT, pull=Pin.PULL_UP, drive=7)
pin.value(1)

# 设置I2C2的iomux，gpio11为SCL，gpio12为SDA
fpioa.set_function(11, FPIOA.IIC2_SCL, pu = 1)
fpioa.set_function(12, FPIOA.IIC2_SDA, pu = 1)


# I2C 从设备 ID 列表
device_id = I2C_Slave.list()
print("Find I2C slave device:", device_id)

# 构造 I2C 从设备，设备地址为 0x10，模拟 EEPROM 映射的内存大小为 20 字节
i2c_slave = I2C_Slave(device_id[0], addr=0x10, mem_size=20)

# 等待主设备发送数据，并读取映射内存中的值
last_dat = i2c_slave.readfrom_mem(0, 20)
dat = last_dat
while dat == last_dat:
    dat = i2c_slave.readfrom_mem(0, 20)
    time.sleep_ms(1)
    os.exitpoint()

# 等待总线数据传输完毕
time.sleep_ms(100)

print(dat.hex())

i2c_slave.writeto_mem(0, dat)
# 通知主机数据已经写入成功
pin.value(0)
time.sleep_ms(1000)

```

**主机代码**：

```python
from machine import Pin, FPIOA, I2C

fpioa = FPIOA()

fpioa.set_function(14, FPIOA.GPIO14)

pin = Pin(14, Pin.IN, pull=Pin.PULL_UP, drive=7)

i2c = I2C(2, scl=11, sda=12, freq=100000)

buf = b"01234567890123456789"
i2c.writeto_mem(0x10, 0, buf)

while pin.value() == 1:
    pass

buf = i2c.readfrom_mem(0x10, 0, 20)
print(buf.hex())
```

### 2.2 `list` 方法

获取当前系统中所有可用的 I2C 从机设备 ID 列表。该列表在初始化 `I2C_Slave` 对象时指定正确的设备 ID 至关重要。

**参数**

- 此方法不接受任何参数。

**返回值**

返回一个列表，包含系统中所有可用的 I2C 从机设备 ID。这些 ID 是整数或类似标识符，用于在创建 `I2C_Slave` 对象时指定具体的从机设备。

**注意事项**

- ID 值及其所代表的设备取决于硬件平台和系统配置。
- 在没有可用从机设备的情况下，返回的列表可能为空。

### 2.3 构造函数

```python
i2c = I2C_Slave(id, addr=0x01, mem_size=10)
```

此构造函数用于创建一个 I2C 从机对象，使设备能够以从机模式运行，并模拟具有指定内存大小的 EEPROM。

**参数**

- `id`: I2C 从设备的 ID，唯一标识符。可通过调用 `I2C_Slave.list()` 方法获取可用的从设备 ID 列表。
- `addr`: 从机模式下的 I2C 地址，用于主设备识别并与之通信。
- `mem_size`: 模拟 EEPROM 映射的内存大小，以字节为单位。

**返回值**

返回创建的 I2C 从设备对象。

### 2.4 `readfrom_mem` 方法

```python
i2c.readfrom_mem(addr, n)
```

从映射的内存地址读取数据（主设备通过 EEPROM 时序写入的数据）。

**参数**

- `addr`: 起始内存地址，从该地址开始读取数据。
- `n`: 要读取的字节数。

**返回值**

返回一个字节数组（`bytearray`），包含从指定地址读取的 n 个字节的数据。

### 2.5 `writeto_mem` 方法

```python
i2c.writeto_mem(addr, data)
```

向映射的内存地址写入数据（主设备通过 EEPROM 时序读取的数据）。

**参数**

- `addr`: 起始内存地址，从该地址开始写入数据。
- `data`: 一个字节数组（`bytearray`），包含要写入的数据。

**返回值**

无
