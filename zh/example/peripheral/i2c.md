# I2C 使用教程(主机模式)

## 1. 概述

I2C（Inter-Integrated Circuit）是一种二线式通信协议，通过 SDA 和 SCL 两条线路进行数据传输。

K230 芯片内部集成5个硬件 I2C 控制器，支持下列通信模式：

* 标准模式（Standard，100kbps）
* 快速模式（Fast，400kbps）
* 高速模式（High Speed，3.4Mbps）

通过 FPIOA 模块，可将 I2C 接口选择分配到指定 IO 线路，应用类型包括 EEPROM 、IMU 传感器、OLED 显示器等外设。
> 注意：
>
> 1. 在进行如下I2C操作之前，需要确保已将相应的引脚切换为 I2C 功能。请参考 [FPIOA使用指南](./fpioa.md)了解如何切换芯片引脚功能。
> 1. I2C 总线需要在 SDA/SCL 上接上拉阻值，通常为 4.7kΩ。
> 1. 与官方 API 相比，K230 所有 I2C API 函数不支持 `stop=False` 参数, 即每个上层 API 调用后均会发送一个 I2C STOP 信号，相当于 `stop=True`。
> 1. 不提供 start(), stop(), readinto(), write() 4个底层 I2C API 的直接调用。

## 2. I2C 使用示例

### 常规 I2C 操作 API

| 方法         | 作用            |
| - | - |
| `init()`   | 重新初始化 I2C 控制器 |
| `scan()`   | 扫描总线上响应设备     |

#### 初始化 I2C 设备

```python
from machine import I2C
i2c = I2C(2, scl=11, sda=12, freq=40000)  # 默认为 100kHz
```

#### 扫描 I2C 总线设备列表

通过调用 scan() 方法，我们可以扫描出当前 I2C 总线上挂载的所有设备的地址。

```python
print(i2c.scan())  # 返回第一个响应的设备地址，如 [59]
```

输出如下：可以看出，在 I2C2 总线上我们扫描出来一个设备，它的地址是 80，实际是一颗 24C32 EEPROM。

```python
[80]
```

### 标准 I2C 总线操作

I2C 总线操作直接和 I2C 从设备交互，不涉及从设备的“内部寄存器”或“内存地址”。

I2C 总线操作方法列表如下：

| 方法              | 读/写 | 特点                         |
| - | - | - |
| `readfrom`      | 读   | 返回一个新的 `bytes`             |
| `readfrom_into` | 读   | 把数据写入现有 `buf` 中            |
| `writeto`       | 写   | 一次写入一个 `bytes`/`bytearray` |
| `writevto`      | 写   | 一次写入多个 buffer              |

#### `readfrom(addr, nbytes, stop=True)`

**功能：** 直接从设备读取 `nbytes` 字节数据。
**返回值：** bytes 对象。

**例：**

```python
data = i2c.readfrom(0x50, 4)  # 从设备地址 0x50 读 4 个字节
```

#### `readfrom_into(addr, buf, stop=True)`

**功能：** 和 `readfrom` 类似，但把数据**写入已有的 `bytearray` 缓冲区**中。
**返回值：** 无（直接填充 `buf`）

**例：**

```python
buf = bytearray(4)
i2c.readfrom_into(0x50, buf)
```

#### `writeto(addr, buf, stop=True)`

**功能：** 向设备写入一个 `buf` 数据。
**返回值：** 接收到 ACK 的字节数。

**例：**

```python
i2c.writeto(0x50, b'\x01\x02')
```

#### `writevto(addr, vector, stop=True)`

**功能：** 和 `writeto` 类似，但 `vector` 是多个 buffer 组成的列表或元组，会**一次性连续发送多个数据段**。
**返回值：** 接收到 ACK 的字节数。

**适合：** 需要先发命令再发数据的场景。

**例：**

```python
i2c.writevto(0x50, (b'\x00', b'\x01\x02'))  # 先发0x00，再发0x01 0x02
```

### 存储类 I2C 操作

很多 I2C 设备（如 EEPROM、RTC）内部有“寄存器地址”或“内存地址”。要先写地址再读写数据。

这些方法是 封装了 “写内存地址 + 读写数据” 的便捷函数。

| 方法                  | 读/写 | 特点                     |
| - | - | - |
| `readfrom_mem`      | 读   | 读取 memaddr 起始地址的 n 个字节 |
| `readfrom_mem_into` | 读   | 同上，但写入现有 buf           |
| `writeto_mem`       | 写   | 写入 memaddr 地址          |

#### `readfrom_mem(addr, memaddr, nbytes, *, addrsize=8)`

**功能：** 从 `memaddr` 处读取 `nbytes` 字节。
**内部相当于：** `write(memaddr)` → `read(nbytes)`
**返回值：** `bytes`

**例：**

```python
data = i2c.readfrom_mem(0x50, 0x0000, 4, addrsize=16)
```

#### `readfrom_mem_into(addr, memaddr, buf, *, addrsize=8)`

**功能：** 同上，但把数据写入 `buf` 中。
**返回值：** 无

**例：**

```python
buf = bytearray(4)
i2c.readfrom_mem_into(0x50, 0x0000, buf, addrsize=16)
```

#### `writeto_mem(addr, memaddr, buf, *, addrsize=8)`

**功能：** 向设备的 `memaddr` 地址写入数据。
**内部相当于：** `write(memaddr + buf)`
**返回值：** 无

**例：**

```python
i2c.writeto_mem(0x3b, 0xff, b'\x80', mem_size=8)  # 页地址 0xFF = 0x80
```

## 3. 常见问题 FAQ

### Q1: `i2c.scan()` 没有返回设备？

请确保：

* SDA/SCL 线路连接正确
* FPIOA 是否正确配置成 IIC 功能，并已启用上拉
* 是否加了外部上拉阻值 (4.7kΩ)
* 从设备是否正常供电

### Q2: I2C 地址是 7 位还是 8 位？

K230 采用 **7 位地址模式**，而某些设备手册或示例中使用的是 **8 位地址（含读写位）**，例如 `0x78`。这容易造成混淆。如果你看到设备手册中是 8 位（包括 R/W 位），请取高 7 位作为地址：

| 模式    | 示例地址   | 说明                    |
| ----- | ------ | --------------------- |
| 7 位地址 | `0x3C` | 实际设备地址，K230使用         |
| 8 位地址 | `0x78` | 通常用于传输（即 `0x3C << 1`） |

如果你发现地址对不上，请尝试将 8 位地址右移一位。

### Q3：执行 `i2c.scan()` 时卡住不响应？

通常是因为 SCL 或 SDA 缺失上拉电阻，导致通信失败。请确认：

* 电路中是否添加了 4.7k \~ 10k 的上拉电阻
* 所连接的 I2C 设备是否供电正常

## 4. 延伸阅读

* [FPIOA 模块教程](./fpioa.md)
* [K230 I2C API 手册](../../api/machine/K230_CanMV_I2C模块API手册.md)
* [K230 引脚定义列表](https://kendryte-download.canaan-creative.com/developer/k230/HDK/K230%E7%A1%AC%E4%BB%B6%E6%96%87%E6%A1%A3/K230_PINOUT_V1.2_20240822.xlsx)
* [Micropython I2C API](https://docs.micropython.org/en/latest/library/machine.I2C.html)
