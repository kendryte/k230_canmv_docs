# UART Example

## Overview

The K230 chip integrates 5 UART hardware modules. UART0 is occupied by the small core (sh), UART3 is occupied by the large core (sh), and the remaining UART1, UART2, and UART4 are available for user use. Users can configure UART pins through the IOMUX module when using them.

## Example

The following code demonstrates the basic operations of serial communication using the UART module:

```python
from machine import UART

# Initialize UART1 with a baud rate of 115200, 8 data bits, no parity, and 1 stop bit
u1 = UART(UART.UART1, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

# Send data via UART1
u1.write("UART1 test")

# Read data from UART1
r = u1.read()

# Read a line of data from UART1
r = u1.readline()

# Read data into a specified byte array
b = bytearray(8)
r = u1.readinto(b)

# Release UART resources
u1.deinit()
```

```{admonition} Tip
For detailed interfaces and usage methods of the UART module, please refer to the [API Documentation](../../api/machine/K230_CanMV_UART_Module_API_Manual.md).
```
