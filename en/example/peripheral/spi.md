# 5. SPI Examples

## 1. Overview

The K230 integrates three SPI hardware modules, supporting configuration of chip select polarity and clock rate. The output IO of the SPI channel can be configured through the IOMUX module, making it very suitable for high-speed data transmission.

## 2. Example

The following example demonstrates how to use the SPI interface to read the ID of a Flash memory.

```python
from machine import SPI
from machine import FPIOA

# Instantiate FPIOA for SPI GPIO configuration
a = FPIOA()

# Print the properties of GPIO14
a.help(14)
# Set GPIO14 to QSPI0_CS0 function
a.set_function(14, a.QSPI0_CS0)
a.help(14)

# Print the properties of GPIO15
a.help(15)
# Set GPIO15 to QSPI0_CLK function
a.set_function(15, a.QSPI0_CLK)
a.help(15)

# Print the properties of GPIO16
a.help(16)
# Set GPIO16 to QSPI0_D0 function
a.set_function(16, a.QSPI0_D0)
a.help(16)

# Print the properties of GPIO17
a.help(17)
# Set GPIO17 to QSPI0_D1 function
a.set_function(17, a.QSPI0_D1)
a.help(17)

# Instantiate SPI with 5MHz clock, polarity 0, and 8-bit data width
spi = SPI(1, baudrate=5000000, polarity=0, phase=0, bits=8)

# Enable gd25lq128 reset
spi.write(bytes([0x66]))
# Reset gd25lq128
spi.write(bytes([0x99]))

# Read ID command (0x9f)
a = bytes([0x9f])
# Create a receive buffer of length 3
b = bytearray(3)
# Read ID
spi.write_readinto(a, b)
# Print result: bytearray(b'\xc8`\x18')
print(b)

# Read ID command (0x90, 0, 0, 0)
a = bytes([0x90, 0, 0, 0])
# Create a receive buffer of length 2
b = bytearray(2)
# Read ID
spi.write_readinto(a, b)
# Print result: bytearray(b'\xc8\x17')
print(b)
```

## 3. Code Explanation

1. **FPIOA Configuration**:
   - Use the `FPIOA` module to configure the GPIO pins used for SPI (e.g., CS, CLK, and data lines).
   - Use the `help()` function to check the current state of the GPIO pins to ensure they are set correctly.

1. **SPI Initialization**:
   - Instantiate the `SPI` object, setting the baud rate to 5 MHz, polarity and phase to 0, and data width to 8 bits.

1. **Flash Memory Operations**:
   - Send reset commands (0x66 and 0x99) to initialize the Flash memory.
   - Read the memory ID using commands 0x9F and 0x90, read the ID, and print the results.

```{admonition} Tip
For detailed interfaces and usage of the SPI module, please refer to the [API documentation](../../api/machine/K230_CanMV_SPI_Module_API_Manual.md).
```
