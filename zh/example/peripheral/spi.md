# SPI 使用教程

## 什么是 SPI？

**SPI（Serial Peripheral Interface）**
是一种**高速全双工串行通信协议**，常用于与外设（如 Flash、LCD、传感器、DAC/ADC 芯片等）通信。其典型结构包括：

- **主设备（Master）**：控制通信（K230 为主）
- **从设备（Slave）**：响应主机命令
- **信号线**：

  - `MOSI`：主机输出 / 从机输入
  - `MISO`：主机输入 / 从机输出
  - `SCLK`：时钟
  - `CS/SS`：片选信号

## K230 SPI 模块特点

- 内置 **3 个 SPI 控制器**
- 支持配置：

  - 通信速率（如 5 MHz）
  - 时钟极性 `polarity`
  - 时钟相位 `phase`
  - 数据位宽（默认为 8 位）
- 可通过 `FPIOA` 灵活映射引脚

## 应用示例：读取 SPI Flash 的 JEDEC ID

此示例展示 K230 使用 SPI 读取外接 Flash 存储器的 ID，同时进行擦除、写入和读取验证。

### 示例代码

```python
from machine import FPIOA, Pin, SPI
import time

# ========== 引脚绑定 ========== #
fpioa = FPIOA()
fpioa.set_function(14, FPIOA.GPIO14)      # CS 引脚
fpioa.set_function(15, FPIOA.QSPI0_CLK)   # SPI 时钟
fpioa.set_function(16, FPIOA.QSPI0_D0)    # MOSI
fpioa.set_function(17, FPIOA.QSPI0_D1)    # MISO

# ========== 初始化引脚 ========== #
cs = Pin(14, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
cs.value(1)  # 默认拉高（不选中）

# ========== 初始化 SPI ========== #
spi = SPI(1, baudrate=1_000_000, polarity=0, phase=0, bits=8)
```

### 发送指令与读取 ID

```python
def read_id():
    cs.value(0)
    spi.write_readinto(bytearray([0x9F, 0xFF, 0xFF, 0xFF]), read_buf := bytearray(4))
    cs.value(1)
    print("JEDEC ID:", [hex(b) for b in read_buf])
```

### 写入/擦除操作（以 4KB Sector 为单位）

```python
def write_enable():
    cs.value(0)
    spi.write(bytearray([0x06]))  # 写使能命令
    cs.value(1)

def wait_busy():
    while True:
        cs.value(0)
        spi.write(bytearray([0x05]))  # 读取状态寄存器
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
```

### 写入数据 + 读取验证

```python
def page_program(addr, data):
    assert len(data) <= 256  # 写入最大 256 字节
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
    data = spi.read(length)
    cs.value(1)
    return data
```

### 测试流程：完整 Flash 操作流程

```python
test_addr = 0x000000
test_data = bytearray(b"1234567890")

read_id()  # 读取 JEDEC ID

print("擦除 4KB 扇区...")
erase_sector(test_addr)

print("写入数据...")
page_program(test_addr, test_data)

print("读取验证...")
read_back = read_data(test_addr, len(test_data))
print("READ_BACK:", read_back.decode())
```

## SPI 关键配置说明

| 参数         | 说明                                 |
| ---------- | ---------------------------------- |
| `baudrate` | 通信速率（单位 Hz），如 `1_000_000` 表示 1 MHz |
| `polarity` | 时钟极性：0 = 空闲时为低电平，1 = 空闲时为高电平       |
| `phase`    | 时钟相位：0 = 第一个边沿采样，1 = 第二个边沿采样       |
| `bits`     | 每帧数据位数，常用为 8 位                     |
| `cs`       | 片选信号由用户手动控制（Pin 对象）                |

## 应用场景

- Flash、EEPROM 存储器读写
- OLED、TFT 等显示驱动
- 传感器通信（如陀螺仪、温湿度、加速度等）
- ADC/DAC 数模转换器控制
- 多设备总线管理（通过多个 CS 控制多从机）

## 注意事项

| 事项     | 说明                                              |
| ------ | ----------------------------------------------- |
| 引脚映射   | 使用 FPIOA 进行 SPI 相关引脚的映射，确保与外设连接正确               |
| 通信协议匹配 | 注意 SPI 设备的 `CPOL/CPHA` 配置必须匹配（极性、相位）            |
| 写入限制   | Flash 写入通常需 4KB 对齐擦除，最多每次写入 256 字节页数据           |
| 读取指令不同 | 有些 SPI 设备使用不同的命令（如 `0x9F` / `0x90` 读取 JEDEC ID） |
| 多片设备管理 | 多个 SPI 从设备需使用不同的 `CS` 引脚进行片选                    |

## 延伸阅读

- 📘 [K230 SPI 模块 API 文档](../../api/machine/k230_canmv_spi_api_manual.md)
