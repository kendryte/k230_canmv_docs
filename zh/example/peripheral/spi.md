# SPI 例程

## 概述

K230 内部集成了三个 SPI 硬件模块，支持配置片选的极性和时钟速率。SPI 通道的输出 IO 可以通过 IOMUX 模块进行配置，非常适合高速数据传输。

## 示例

以下示例展示了如何使用 SPI 接口读取 Flash 存储器的 ID。

```python
from machine import FPIOA, Pin, SPI
import time

fpioa = FPIOA()
fpioa.set_function(14, FPIOA.GPIO14)
fpioa.set_function(15, FPIOA.QSPI0_CLK)
fpioa.set_function(16, FPIOA.QSPI0_D0)
fpioa.set_function(17, FPIOA.QSPI0_D1)
cs = Pin(14, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
cs.value(1)
spi = SPI(1, baudrate=1000 * 1000, polarity=0, phase=0, bits=8)

def write_enable():
    cs.value(0)
    spi.write(bytearray([0x06]))  # 写使能
    cs.value(1)
def wait_busy():
    while True:
        cs.value(0)
        spi.write(bytearray([0x05]))
        busy = spi.read(1)[0] & 0x01
        cs.value(1)
        if not busy:
            break
        time.sleep(0.05)
def erase_sector(addr):
    write_enable()
    cs.value(0)
    spi.write(bytearray([0x20, (addr >> 16) & 0xFF, (addr >> 8) & 0xFF, addr & 0xFF]))
    cs.value(1)
    wait_busy()
def page_program(addr, data):
    assert len(data) <= 256
    write_enable()
    cs.value(0)
    cmd = bytearray([0x02, (addr >> 16) & 0xFF, (addr >> 8) & 0xFF, addr & 0xFF])
    spi.write(cmd + data)
    cs.value(1)
    wait_busy()
def read_data(addr, length):
    cs.value(0)
    cmd = bytearray([0x03, (addr >> 16) & 0xFF, (addr >> 8) & 0xFF, addr & 0xFF])
    spi.write(cmd)
    result = spi.read(length)
    cs.value(1)
    return result
def read_id():
    cs.value(0)
    write_buf = bytearray([0x9F,0xff, 0xff, 0xff])
    read_buf = bytearray(4)
    spi.write_readinto(write_buf, read_buf)
    cs.value(1)
    print("JEDEC ID:", [hex(b) for b in read_buf])

read_id()

test_addr = 0x000000
print("erase 4KB sector...")
erase_sector(test_addr)
print("writing data...")
test_data = bytearray(b"1234567890")
page_program(test_addr, test_data)
print("reading verification...")
read_back = read_data(test_addr, len(test_data))
print("READ_BACK:", read_back.decode())

```

## 代码说明

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
