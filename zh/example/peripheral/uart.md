# UART 例程

## 概述

K230 芯片内部集成了 5 个 UART 硬件模块，其中 UART0 被小核（sh）占用，UART3 被大核（sh）占用，剩余的 UART1、UART2 和 UART4 供用户使用。用户在使用时，可通过 IOMUX 模块进行 UART 引脚的配置。

## 示例

以下代码展示了如何使用 UART 模块进行串口通信的基本操作：

```python
from machine import UART

# 初始化 UART1，配置波特率为 115200，8 位数据位，无校验位，1 个停止位
u1 = UART(UART.UART1, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

# 通过 UART1 发送数据
u1.write("UART1 test")

# 从 UART1 读取数据
r = u1.read()

# 从 UART1 读取一行数据
r = u1.readline()

# 将数据读入指定的字节数组
b = bytearray(8)
r = u1.readinto(b)

# 释放 UART 资源
u1.deinit()
```

```{admonition} 提示
有关 UART 模块的详细接口和使用方法，请参考 [API 文档](../../api/machine/K230_CanMV_UART模块API手册.md)。
```
