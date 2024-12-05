# 2.7 `I2C` 模块 API 手册

## 1. 概述

K230 芯片内部配备 5 个 I2C 硬件模块，支持标准 100 kb/s、快速 400 kb/s 以及高速 3.4 Mb/s 的通信模式。通道输出的 IO 配置请参考 IOMUX 模块。

## 2. 主设备 API 介绍

`I2C` 类位于 `machine` 模块中。

### 2.1 示例代码

```python
from machine import I2C

# 初始化 I2C0，设置时钟频率为 100 kHz
i2c = I2C(0, freq=100000)

# 初始化软件I2C, 设置时钟 100kHz
# i2c = I2C(5, scl = 10, sda = 11, freq = 100000, timeout = 1000)

# 扫描 I2C 总线上的从机
i2c.scan()

# 从总线读取数据
i2c.readfrom(addr, len, True)

# 将读取的数据存入指定缓冲区
i2c.readfrom_into(addr, buf, True)

# 向从机发送数据
i2c.writeto(addr, buf, True)

# 读取从机寄存器
i2c.readfrom_mem(addr, memaddr, nbytes, mem_size=8)

# 将读取的寄存器值存入缓冲区
i2c.readfrom_mem_into(addr, memaddr, buf, mem_size=8)

# 向从机寄存器写入数据
i2c.writeto_mem(addr, memaddr, buf, mem_size=8)

# 释放 I2C 资源
i2c.deinit()
```

### 2.2 构造函数

```python
i2c = I2C(id, freq=100000, timeout = 1000, [scl, sda)
```

**参数**

- `id`: I2C 设备 ID，硬件 I2C 为 [0~4]（即 I2C.I2C0~I2C.I2C4），软件 I2C 为 [5~9]
- `freq`: I2C 时钟频率，软件 I2C 可能无法设置出所有的频率，请以实际的为准
- `timeout`: 软件 I2C 通信超时时间
- `scl`: 软件 I2C 的 scl 脚
- `sda`: 软件 I2C 的 sda 脚

### 2.3 `scan` 方法

```python
i2c.scan()
```

扫描当前 I2C 总线上的从机设备。

**参数**

无

**返回值**

返回一个列表，包含所有扫描到的从机地址。

### 2.4 `readfrom` 方法

```python
i2c.readfrom(addr, len, True)
```

从总线读取指定长度的数据。

**参数**

- `addr`: 从机地址。
- `len`: 要读取的数据长度。
- `stop`: 是否发送停止信号，当前仅支持默认值 `True`。

**返回值**

返回读取到的数据，类型为 `bytes`。

### 2.5 `readfrom_into` 方法

```python
i2c.readfrom_into(addr, buf, True)
```

根据缓冲区的长度，从指定 I2C 地址读取数据到指定的缓冲区。

**参数**

- `addr`: 从机地址。
- `buf`: `bytearray` 类型，定义长度并用于存放读取到的数据。
- `stop`: 是否发送停止信号，当前仅支持默认值 `True`。

**返回值**

无

### 2.6 `writeto` 方法

```python
i2c.writeto(addr, buf, True)
```

向从机发送数据。

**参数**

- `addr`: 从机地址。
- `buf`: 需要发送的数据。
- `stop`: 是否发送停止信号，当前仅支持默认值 `True`。

**返回值**

成功发送的字节数。

### 2.7 `readfrom_mem` 方法

```python
i2c.readfrom_mem(addr, memaddr, nbytes, mem_size=8)
```

从存储器读取值。用于 I2C 操作存储器类型设备。

**参数**

- `addr`: I2C 从机地址。
- `memaddr`: 存储器的存储地址。
- `nbytes`: 读取的字节数。
- `mem_size`: 存储器地址宽度，默认为 8 位。

**返回值**

返回读取到的数据，类型为 `bytes`。

### 2.8 `readfrom_mem_into` 方法

```python
i2c.readfrom_mem_into(addr, memaddr, buf, mem_size=8)
```

读取数据到缓冲区。用于 I2C 操作存储器类型设备。

**参数**

- `addr`: I2C 从机地址。
- `memaddr`: 存储器的存储地址。
- `buf`: `bytearray` 类型，定义长度并用于存放读取到的数据。
- `mem_size`: 寄存地址宽度，默认为 8 位。

**返回值**

无

### 2.9 `writeto_mem` 方法

```python
i2c.writeto_mem(addr, memaddr, buf, mem_size=8)
```

向从机写入数据。用于 I2C 操作存储器类型设备。

**参数**

- `addr`: I2C 从机地址。
- `memaddr`: 存储器存储地址。
- `buf`: 需要写入的数据。
- `mem_size`: 存储地址宽度，默认为 8 位。

**返回值**

无

### 2.10 `deinit` 方法

```python
i2c.deinit()
```

释放 I2C 资源。

**参数**

无

**返回值**

无

## 3. 从设备 API 介绍

`I2C_Slave` 类位于 `machine` 模块中。

K230 I2C 控制器默认工作在主机模式，但也能通过定制固件，切换为从机模式。要想开启从模式，请在编译固件时使用 `make rtsmart-menuconfig` 配置打开 `Enable I2Cx SLAVE mode` 选项（路径：Drivers Configuration/Enable/I2C/Enable I2Cx/Enable I2Cx SLAVE mode），然后重新编译固件。

![menuconfig](../images/i2c_slave_menuconfig.png)

### 3.1 示例代码

以下示例应用中，我们将 K210 作为主设备，使用 K230 作为从设备，演示主机和从机通过 I2C 总线进行通信。其中 K230 的 IO5 用于在数据发生变化时通知主设备读取数据。

**K230 代码**：

```python
from machine import Pin, FPIOA, I2C_Slave
import time
import os

# 初始化 GPIO，用于通知主机有数据更新
def gpio_int_init():
    # 实例化 FPIOA
    fpioa = FPIOA()
    # 设置 Pin5 为 GPIO5
    fpioa.set_function(5, FPIOA.GPIO5)
    # 实例化 Pin5 为输出
    pin = Pin(5, Pin.OUT, pull=Pin.PULL_NONE, drive=7)
    # 设置输出为高
    pin.value(1)
    return pin

pin = gpio_int_init()
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
    time.sleep_ms(100)
    os.exitpoint()
print(dat)

# 修改映射内存中的值
for i in range(len(dat)):
    dat[i] = i
i2c_slave.writeto_mem(0, dat)
# 通知主机有数据更新
pin.value(0)
time.sleep_ms(1)
pin.value(1)
```

**K210 代码**：

```python
from machine import I2C
from fpioa_manager import fm
from maix import GPIO

fm.register(8, fm.fpioa.GPIO2)

int_io = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

i2c = I2C(I2C.I2C3, freq=100000, scl=6, sda=7)

i2c.writeto_mem(0x10, 0, bytearray("abcdefghijklnmopqrst"))

while int_io.value() == 1:
    pass

buf = i2c.readfrom_mem(0x10, 0, 20)
print(buf)
```

### 3.2 `list` 方法

获取当前系统中所有可用的 I2C 从机设备 ID 列表。该列表在初始化 `I2C_Slave` 对象时指定正确的设备 ID 至关重要。

**参数**

- 此方法不接受任何参数。

**返回值**

返回一个列表，包含系统中所有可用的 I2C 从机设备 ID。这些 ID 是整数或类似标识符，用于在创建 `I2C_Slave` 对象时指定具体的从机设备。

**注意事项**

- ID 值及其所代表的设备取决于硬件平台和系统配置。
- 在没有可用从机设备的情况下，返回的列表可能为空。

### 3.3 构造函数

```python
i2c = I2C_Slave(id, addr=0x10, mem_size=20)
```

此构造函数用于创建一个 I2C 从机对象，使设备能够以从机模式运行，并模拟具有指定内存大小的 EEPROM。

**参数**

- `id`: I2C 从设备的 ID，唯一标识符。可通过调用 `I2C_Slave.list()` 方法获取可用的从设备 ID 列表。
- `addr`: 从机模式下的 I2C 地址，用于主设备识别并与之通信。
- `mem_size`: 模拟 EEPROM 映射的内存大小，以字节为单位。

**返回值**

返回创建的 I2C 从设备对象。

### 3.4 `readfrom_mem` 方法

```python
i2c.readfrom_mem(addr, n)
```

从映射的内存地址读取数据（主设备通过 EEPROM 时序写入的数据）。

**参数**

- `addr`: 起始内存地址，从该地址开始读取数据。
- `n`: 要读取的字节数。

**返回值**

返回一个字节数组（`bytearray`），包含从指定地址读取的 n 个字节的数据。

### 3.5 `writeto_mem` 方法

```python
i2c.writeto_mem(addr, data)
```

向映射的内存地址写入数据（主设备通过 EEPROM 时序读取的数据）。

**参数**

- `addr`: 起始内存地址，从该地址开始写入数据。
- `data`: 一个字节数组（`bytearray`），包含要写入的数据。

**返回值**

无
