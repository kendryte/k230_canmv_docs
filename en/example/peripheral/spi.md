# SPI Usage Tutorial

## What is SPI?

**SPI (Serial Peripheral Interface)**
is a **high-speed full-duplex serial communication protocol**, commonly used to communicate with peripherals (such as Flash, LCD, sensors, DAC/ADC chips, etc.). Its typical structure includes:

- **Master device**: Controls communication (K230 is the master)
- **Slave device**: Responds to master commands
- **Signal lines**:

  - `MOSI`: Master Output / Slave Input
  - `MISO`: Master Input / Slave Output
  - `SCLK`: Clock
  - `CS/SS`: Chip Select signal

## K230 SPI Module Features

- Built-in **3 SPI controllers**
- Supports configuration of:

  - Communication rate (e.g., 5 MHz)
  - Clock polarity `polarity`
  - Clock phase `phase`
  - Data bit width (default is 8 bits)
- Pins can be flexibly mapped via `FPIOA`

## Application Example: Reading JEDEC ID of SPI Flash

This example demonstrates how the K230 uses SPI to read the ID of an external Flash memory, while performing erase, write, and read verification.

### Example Code

```python
from machine import FPIOA, Pin, SPI
import time

# ========== Pin Binding ========== #
fpioa = FPIOA()
fpioa.set_function(14, FPIOA.GPIO14)      # CS pin
fpioa.set_function(15, FPIOA.QSPI0_CLK)   # SPI clock
fpioa.set_function(16, FPIOA.QSPI0_D0)    # MOSI
fpioa.set_function(17, FPIOA.QSPI0_D1)    # MISO

# ========== Initialize Pins ========== #
cs = Pin(14, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
cs.value(1)  # Default pulled high (not selected)

# ========== Initialize SPI ========== #
spi = SPI(1, baudrate=1_000_000, polarity=0, phase=0, bits=8)
```

### Send Command and Read ID

```python
def read_id():
    cs.value(0)
    spi.write_readinto(bytearray([0x9F, 0xFF, 0xFF, 0xFF]), read_buf := bytearray(4))
    cs.value(1)
    print("JEDEC ID:", [hex(b) for b in read_buf])
```

### Write/Erase Operations (in 4KB Sectors)

```python
def write_enable():
    cs.value(0)
    spi.write(bytearray([0x06]))  # Write enable command
    cs.value(1)

def wait_busy():
    while True:
        cs.value(0)
        spi.write(bytearray([0x05]))  # Read status register
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

### Write Data + Read Verification

```python
def page_program(addr, data):
    assert len(data) <= 256  # Write up to 256 bytes
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

### Test Flow: Complete Flash Operation Flow

```python
test_addr = 0x000000
test_data = bytearray(b"1234567890")

read_id()  # Read JEDEC ID

print("Erasing 4KB sector...")
erase_sector(test_addr)

print("Writing data...")
page_program(test_addr, test_data)

print("Reading for verification...")
read_back = read_data(test_addr, len(test_data))
print("READ_BACK:", read_back.decode())
```

## SPI Key Configuration Description

| Parameter   | Description                                              |
| ---------- | -------------------------------------------------------- |
| `baudrate` | Communication rate (in Hz), e.g., `1_000_000` means 1 MHz |
| `polarity` | Clock polarity: 0 = low when idle, 1 = high when idle       |
| `phase`    | Clock phase: 0 = sample on first edge, 1 = sample on second edge |
| `bits`     | Number of data bits per frame, commonly 8                    |
| `cs`       | Chip select signal manually controlled by the user (Pin object) |

## Application Scenarios

- Flash and EEPROM memory read/write
- OLED, TFT and other display drivers
- Sensor communication (e.g., gyroscope, temperature and humidity, accelerometer, etc.)
- ADC/DAC digital-to-analog converter control
- Multi-device bus management (controlling multiple slaves via multiple CS)

## Notes

| Item              | Description                                                                          |
| ------ | ------------------------------------------------------------------------- |
| Pin mapping       | Use FPIOA to map SPI-related pins to ensure correct connection with peripherals       |
| Protocol matching | Note that the SPI device's `CPOL/CPHA` configuration must match (polarity, phase)       |
| Write limitations | Flash writes typically require 4KB aligned erase, with a maximum of 256 bytes per page write |
| Read commands     | Some SPI devices use different commands (e.g., `0x9F` / `0x90` to read JEDEC ID)     |
| Multi-chip management | Multiple SPI slave devices need to use different `CS` pins for chip select           |

## Further Reading

- 📘 [K230 SPI Module API Documentation](../../api/machine/k230_canmv_spi_api_manual.md)
