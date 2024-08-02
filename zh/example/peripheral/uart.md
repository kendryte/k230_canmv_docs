# 3. UART 例程

## 1. 概述

K230内部包含五个UART硬件模块，其中UART0被小核sh占用，UART3被大核sh占用，剩余UART1，UART2，UART4可供用户使用。
UART IO配置参考IOMUX模块。

## 2. 示例

```python
from machine import UART
# UART1: baudrate 115200, 8bits, parity none, one stopbits
u1 = UART(UART.UART1, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
# UART write
u1.write("UART1 test")
# UART read
r = u1.read()
# UART readline
r = u1.readline()
# UART readinto
b = bytearray(8)
r = u1.readinto(b)
# UART deinit
u1.deinit()
```

```{admonition} 提示
UART模块具体接口请参考[API文档](../../api/machine/K230_CanMV_UART模块API手册.md)
```
