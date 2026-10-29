# I2C Usage Tutorial (Master Mode)

## Overview

I2C (Inter-Integrated Circuit) is a two-wire communication protocol that transmits data through two lines: SDA and SCL.

The K230 chip integrates 5 hardware I2C controllers internally, supporting the following communication modes:

* Standard mode (Standard, 100kbps)
* Fast mode (Fast, 400kbps)
* High Speed mode (High Speed, 3.4Mbps)

Through the FPIOA module, the I2C interface can be assigned to specified IO lines. Application types include peripherals such as EEPROM, IMU sensors, OLED displays, etc.
> Note:
>
> 1. Before performing the following I2C operations, ensure that the corresponding pins have been switched to the I2C function. Please refer to the [FPIOA Usage Guide](./fpioa.md) to learn how to switch chip pin functions.
> 1. The I2C bus requires pull-up resistors on SDA/SCL, typically 4.7kΩ.
> 1. Compared with the official API, all K230 I2C API functions do not support the `stop=False` parameter, meaning that each upper-layer API call will send an I2C STOP signal, equivalent to `stop=True`.
> 1. Direct calls to the 4 low-level I2C APIs start(), stop(), readinto(), write() are not provided.

## I2C Usage Example

### Regular I2C Operation API

| Method         | Function            |
| - | - |
| `init()`   | Reinitialize I2C controller |
| `scan()`   | Scan devices responding on the bus     |

#### Initialize I2C Device

```python
from machine import I2C
i2c = I2C(2, scl=11, sda=12, freq=40000)  # Default is 100kHz
```

#### Scan I2C Bus Device List

By calling the scan() method, we can scan out the addresses of all devices mounted on the current I2C bus.

```python
print(i2c.scan())  # Returns the first responding device address, e.g., [59]
```

The output is as follows: As can be seen, on the I2C2 bus we scanned one device, whose address is 80, which is actually a 24C32 EEPROM.

```python
[80]
```

### Standard I2C Bus Operations

I2C bus operations interact directly with I2C slave devices and do not involve the slave device's "internal registers" or "memory addresses".

The list of I2C bus operation methods is as follows:

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

### Memory I2C Operations

Many I2C devices (such as EEPROM, RTC) have internal "register addresses" or "memory addresses". You need to write the address first and then read/write data.

These methods are convenience functions that wrap "write memory address + read/write data".

| Method                  | Read/Write | Feature                     |
| - | - | - |
| `readfrom_mem`      | Read   | Read n bytes starting from the memaddr address |
| `readfrom_mem_into` | Read   | Same as above, but writes into an existing buf           |
| `writeto_mem`       | Write   | Write to the memaddr address          |

#### `readfrom_mem(addr, memaddr, nbytes, *, addrsize=8)`

**Function:** Read `nbytes` bytes from `memaddr`.
**Internally equivalent to:** `write(memaddr)` → `read(nbytes)`
**Return value:** `bytes`

**Example:**

```python
data = i2c.readfrom_mem(0x50, 0x0000, 4, addrsize=16)
```

#### `readfrom_mem_into(addr, memaddr, buf, *, addrsize=8)`

**Function:** Same as above, but writes the data into `buf`.
**Return value:** None

**Example:**

```python
buf = bytearray(4)
i2c.readfrom_mem_into(0x50, 0x0000, buf, addrsize=16)
```

#### `writeto_mem(addr, memaddr, buf, *, addrsize=8)`

**Function:** Write data to the device's `memaddr` address.
**Internally equivalent to:** `write(memaddr + buf)`
**Return value:** None

**Example:**

```python
i2c.writeto_mem(0x3b, 0xff, b'\x80', mem_size=8)  # Page address 0xFF = 0x80
```

## Frequently Asked Questions FAQ

### Q1: `i2c.scan()` returns no devices?

Please ensure:

* SDA/SCL lines are connected correctly
* FPIOA is correctly configured for IIC function, with pull-ups enabled
* Whether an external pull-up resistor (4.7kΩ) has been added
* Whether the slave device is properly powered

### Q2: Is the I2C address 7-bit or 8-bit?

The K230 uses **7-bit address mode**, while some device manuals or examples use **8-bit addresses (including R/W bit)**, such as `0x78`. This can easily cause confusion. If you see that the device manual uses 8-bit addresses (including the R/W bit), please take the upper 7 bits as the address:

| Mode       | Example Address | Description                          |
| ---------- | --------------- | ------------------------------------ |
| 7-bit address | `0x3C`        | Actual device address, used by K230  |
| 8-bit address | `0x78`        | Usually used for transmission (i.e., `0x3C << 1`) |

If you find the address doesn't match, try shifting the 8-bit address one bit to the right.

### Q3: `i2c.scan()` gets stuck and does not respond?

This is usually because SCL or SDA is missing pull-up resistors, causing communication failure. Please confirm:

* Whether a pull-up resistor of 4.7k \~ 10k has been added to the circuit
* Whether the connected I2C device is powered normally

## Further Reading

* [FPIOA Module Tutorial](./fpioa.md)
* [K230 I2C API Manual](../../api/machine/k230_canmv_i2c_api_manual.md)
* [K230 Pin Definition List](https://download.kendryte.com/developer/k230/HDK/K230%E7%A1%AC%E4%BB%B6%E6%96%87%E6%A1%A3/K230_PINOUT_V1.2_20240822.xlsx)
* [Micropython I2C API](https://docs.micropython.org/en/latest/library/machine.I2C.html)
