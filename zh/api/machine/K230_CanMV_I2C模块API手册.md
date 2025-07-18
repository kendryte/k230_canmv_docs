# 2.7 `I2C` 模块 API 手册

## 1. 概述

K230 芯片内部配备 5 个 I2C 硬件模块，支持标准 100 kb/s、快速 400 kb/s 以及高速 3.4 Mb/s 的通信模式。
另外 K230 也实现了 5 个软件 I2C 供用户选择使用。

## 2. 主设备 API 介绍

`I2C` 类位于 `machine` 模块中。

### 2.1 示例代码

```python
import time
from machine import I2C

# 24C32参数
EEPROM_ADDR = 0x50  # 24C32的I2C地址
PAGE_SIZE = 32      # 24C32的页大小(字节)
MEM_SIZE = 4096     # 24C32总容量(4KB)

# 初始化I2C
i2c = I2C(2, scl=11, sda=12, freq=40000)

def test_24c32():
    print("24C32 EEPROM测试开始...")

    # 测试数据 - 生成0x00-0xFF的循环模式
    test_data = bytearray([x & 0xFF for x in range(PAGE_SIZE)])
    test_addr = 0x0000  # 测试起始地址

    print("写入数据: [{}]".format(", ".join("0x{:02x}".format(x) for x in test_data)))

    # 写入一页数据 (24C32支持页写入)
    i2c.writeto_mem(EEPROM_ADDR, test_addr, test_data, addrsize=16)
    print("写入完成，地址: 0x{:04x}".format(test_addr))

    # 等待EEPROM完成写入(重要!)
    time.sleep_ms(10)  # 24C32页写入典型时间5ms

    # 读取回数据
    read_data = i2c.readfrom_mem(EEPROM_ADDR, test_addr, len(test_data), addrsize=16)
    print("读取数据: [{}]".format(", ".join("0x{:02x}".format(x) for x in read_data)))

    # 验证数据
    if test_data == read_data:
        print("测试成功! 写入和读取数据匹配")
    else:
        print("测试失败! 数据不匹配")

    # 随机地址读写测试
    print("\n随机地址读写测试...")
    import urandom
    test_addr = urandom.getrandbits(12)  # 生成12位随机地址(0-0xFFF)
    test_byte = urandom.getrandbits(8)   # 生成随机测试字节

    print("在地址0x{:04x}写入字节: 0x{:02x}".format(test_addr, test_byte))
    i2c.writeto_mem(EEPROM_ADDR, test_addr, bytearray([test_byte]), addrsize=16)
    time.sleep_ms(5)  # 等待写入完成

    read_byte = i2c.readfrom_mem(EEPROM_ADDR, test_addr, 1, addrsize=16)[0]
    print("读取到的字节: 0x{:02x}".format(read_byte))

    if test_byte == read_byte:
        print("随机地址测试成功!")
    else:
        print("随机地址测试失败!")

# 运行测试
test_24c32()

```

### 2.2 构造函数

```python
i2c = I2C(id, scl , sda, freq=400000, timeout = 50000)
```

**参数**

- `id`: I2C 设备 ID，硬件 I2C 为 [0~4]，软件 I2C 为 [5~9]
- `scl`: I2C 的 scl 脚
- `sda`: I2C 的 sda 脚
- `freq`: I2C 时钟频率，软件 I2C 可能无法设置出所有的频率，请以实际的为准
- `timeout`: I2C 通信超时时间

### 2.3 `scan` 方法

```python
i2c.scan()
```

扫描当前 I2C 总线上的从机设备，返回响应设备的7位地址列表

**参数**

无

**返回值**

返回一个列表，包含所有扫描到的从机地址。

### 2.4 `readfrom` 方法

```python
i2c.readfrom(addr, len, True)
```

从指定 I2C 地址的从机中读取指定长度的数据。

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

根据缓冲区的长度，从指定 I2C 地址的从机中读取数据到缓冲区中。

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

向指定 I2C 地址的从机发送缓冲区中的数据。

**参数**

- `addr`: 从机地址。
- `buf`: 需要发送的数据。
- `stop`: 是否发送停止信号，当前仅支持默认值 `True`。

**返回值**

成功发送的字节数。

### 2.7 `readfrom_mem` 方法

```python
i2c.readfrom_mem(addr, memaddr, nbytes, addrsize=8)
```

从存储器的指定内存地址读取指定长度数据。用于 I2C 操作存储器类型设备。

**参数**

- `addr`: I2C 从机地址。
- `memaddr`: 存储器的存储地址。
- `nbytes`: 读取的字节数。
- `addrsize`: 存储器地址宽度，默认为 8 位。

**返回值**

返回读取到的数据，类型为 `bytes`。

### 2.8 `readfrom_mem_into` 方法

```python
i2c.readfrom_mem_into(addr, memaddr, buf, addrsize=8)
```

根据缓冲区的长度，从存储器指定内存地址读取数据到缓冲区中。用于 I2C 操作存储器类型设备。

**参数**

- `addr`: I2C 从机地址。
- `memaddr`: 存储器的存储地址。
- `buf`: `bytearray` 类型，定义长度并用于存放读取到的数据。
- `addrsize`: 寄存地址宽度，默认为 8 位。

**返回值**

无

### 2.9 `writeto_mem` 方法

```python
i2c.writeto_mem(addr, memaddr, buf, mem_size=8)
```

将指定缓冲区的数据写入存储器指定内存地址。用于 I2C 操作存储器类型设备。

**参数**

- `addr`: I2C 从机地址。
- `memaddr`: 存储器存储地址。
- `buf`: 需要写入的数据。
- `mem_size`: 存储地址宽度，默认为 8 位。

**返回值**

无
