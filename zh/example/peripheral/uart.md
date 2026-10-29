# UART 使用教程

## 什么是 UART？

**UART（通用异步收发传输器）**
是一种常见的串口通信协议，用于在设备间通过串行方式发送与接收数据。广泛用于：

* 串口终端调试
* 与传感器或外部模块通信（如 GPS、GSM 模块）
* 主从设备之间的数据交换

## 串口电平与转接模块安全

```{warning}
连接任何 USB 转 UART 模块或串口外设前，必须先查阅开发板原理图，确认所用 UART 引脚对应的 I/O 域电压。K230 的 I/O 域可能配置为 **1.8 V** 或 **3.3 V**，不同开发板和不同引脚不一定相同。外部设备的 TX/RX 逻辑电平必须与开发板匹配；不匹配时必须增加电平转换电路，禁止将 **5 V UART 信号**直接接入 K230。

请断电后接线，并确保 TX 接 RX、RX 接 TX、GND 共地。除非开发板文档明确要求，否则不要连接 USB 转串口模块的 VCC/5V 引脚。具体电气限制请参考 [K230 硬件设计指南](https://www.kendryte.com/k230/zh/main/00_hardware/K230_Hardware_Design_Guide.html)。

**禁止使用下图所示带黄色跳帽的 CH340G USB 转串口模块。** 这类劣质模块即使选择 3.3 V 档，部分样品的 TX 高电平仍可能达到约 3.8 V，存在永久损坏 K230 的风险，在 1.8 V I/O 域上尤其危险。此警告针对下图所示模块，并非否定所有采用 CH340G 芯片的产品。应使用电平经过验证的正规模块；首次连接前建议测量模块 TX 空闲高电平。
```

![禁止使用的 CH340G USB 转串口模块](https://www.kendryte.com/api/imagecdn/zh/bad_ch340.jpg)

## K230 UART 特性

| 特性     | 描述                                                  |
| ------ | --------------------------------------------------- |
| 支持通道数量 | 5 路 UART：UART0 \~ UART4                             |
| 可用通道说明 | UART0被系统调试占用，**UART1、2、3、4 可用**                      |
| 可配置参数  | 波特率、数据位、停止位、校验位等                                    |
| 引脚复用   | 支持通过 **IOMUX** 设置任意 IO 为 UART 功能                    |
| 数据操作方式 | 支持 `write()`、`read()`、`readline()`、`readinto()` 等方法 |

## 应用示例：串口收发测试

以下示例展示如何初始化 UART1 接口，进行数据的发送与接收操作。

### 示例代码

```python
from machine import UART

# ========== 初始化 UART1 ==========
u1 = UART(
    UART.UART1,           # UART1 通道
    baudrate=115200,      # 波特率 115200
    bits=UART.EIGHTBITS,  # 数据位 8 位
    parity=UART.PARITY_NONE,  # 无校验
    stop=UART.STOPBITS_ONE    # 停止位 1 位
)

# ========== 发送数据 ==========
u1.write("UART1 test")  # 发送字符串

# ========== 读取数据 ==========
r = u1.read()            # 读取接收到的字节数据（可能为 None）
r = u1.readline()        # 读取一整行数据（以换行符结尾）
b = bytearray(8)
u1.readinto(b)           # 将接收到的数据填充到 bytearray 中

# ========== 释放资源 ==========
u1.deinit()
```

## 接口说明

| 方法名             | 说明                         |
| --------------- | -------------------------- |
| `UART()`        | 创建 UART 对象，指定通道号和通信参数      |
| `write(data)`   | 向串口写入字符串或字节数据              |
| `read()`        | 读取所有可用数据，返回字节对象或 None      |
| `readline()`    | 读取一行数据，以换行符 `\n` 结尾        |
| `readinto(buf)` | 将数据读入指定的缓冲区（如 `bytearray`） |
| `deinit()`      | 停止串口并释放资源                  |

## 应用场景举例

* 串口调试输出：替代 `print()`，便于外部设备监听日志
* 与串口模块通信：如蓝牙、LoRa、4G 模块
* 多串口并发任务处理：通过 UART1/2/4 连接多个外设

## 常见问题排查

| 问题               | 排查建议                      |
| ---------------- | ------------------------- |
| 无法接收到数据          | 检查波特率设置、IO 映射是否正确         |
| 接收数据乱码           | 确认两端的通信参数一致（波特率、数据位等）     |
| 读取结果为 None       | 串口缓冲区中没有可读数据              |
| 无法使用 UART0/UART3 | 这两个通道为系统占用，建议使用 UART1/2/4 |

## 延伸阅读

* [K230 UART API 文档](../../api/machine/k230_canmv_uart_api_manual.md)
* [FPIOA 模块完整 API 手册](../../api/machine/k230_canmv_fpioa_api_manual.md)
* [K230 芯片引脚定义列表（Excel）](https://download.kendryte.com/developer/k230/HDK/K230%E7%A1%AC%E4%BB%B6%E6%96%87%E6%A1%A3/K230_PINOUT_V1.2_20240822.xlsx)
* [K230 IOMUX 配置工具](https://www.kendryte.com/zh/tools/dts_config_generation_tool)
