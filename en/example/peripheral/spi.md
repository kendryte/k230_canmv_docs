# SPI Examples

## Overview

The K230 integrates three SPI hardware modules, supporting configuration of chip select polarity and clock rate. The output IO of the SPI channel can be configured through the IOMUX module, making it very suitable for high-speed data transmission.

## Example

The following example demonstrates how to use the SPI interface to read the ID of a Flash memory.

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
    spi.write(bytearray([0x06]))
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

## Code Explanation

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
