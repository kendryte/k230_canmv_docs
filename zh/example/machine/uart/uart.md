# uart - uart例程

本示例程序用于对 CanMV 开发板进行一个UART的功能展示。  

```python
from machine import UART
# UART1: baudrate 115200, 8bits, parity none, one stopbits
uart = UART(UART.UART2, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
# UART write
r = uart.write("UART test")
print(r)
# UART read
r = uart.read()
print(r)
# UART readline
r = uart.readline()
print(r)
# UART readinto
b = bytearray(8)
r = uart.readinto(b)
print(r)

```

具体接口定义请参考 [UART](../../../api/machine/K230_CanMV_UART模块API手册.md)
