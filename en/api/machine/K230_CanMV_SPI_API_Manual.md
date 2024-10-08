# 2.10 SPI Module API Manual

## 1. Overview

The K230 integrates three SPI hardware modules internally, supporting chip select polarity configuration and adjustable clock rates. The I/O configuration for channel output can refer to the IOMUX module.

## 2. API Introduction

The SPI class is located in the `machine` module.

### 2.1 Example Code

```python
from machine import SPI

# Initialize SPI with a clock rate of 5 MHz, polarity 0, phase 0, and data width of 8 bits
spi = SPI(id, baudrate=5000000, polarity=0, phase=0, bits=8)

# Send data to the slave device
spi.write(buf)

# Read data into a variable while sending data
spi.write_readinto(write_buf, read_buf)

# Close the SPI
spi.deinit()
```

### 2.2 Constructor

```python
spi = machine.SPI(id, baudrate=20, polarity=0, phase=0, bits=8)
```

**Parameters**

- `id`: SPI module ID, range [0~2] (corresponding to `spi.SPI0` to `spi.SPI2`).
- `baudrate`: SPI clock rate, calculated as \( F_{sclk\_out} = \frac{F_{ssi\_clk}}{BAUDR} \).
- `polarity`: Clock polarity.
- `phase`: Clock phase.
- `bits`: Data width.

### 2.3 `read` Method

```python
spi.read(nbytes)
```

Reads the specified number of bytes.

**Parameters**

- `nbytes`: Number of bytes to read.

**Return Value**

Returns a `bytes` object.

### 2.4 `readinto` Method

```python
spi.readinto(buf)
```

Reads data into the specified buffer.

**Parameters**

- `buf`: A buffer of type `bytearray`.

**Return Value**

None

### 2.5 `write` Method

```python
spi.write(buf)
```

Sends data.

**Parameters**

- `buf`: Data of type `bytearray`, defining the data to be sent and its length.

**Return Value**

None

### 2.6 `write_readinto` Method

```python
spi.write_readinto(write_buf, read_buf)
```

Reads data into the specified variable while sending data.

**Parameters**

- `write_buf`: Data of type `bytearray`, defining the data to be sent and its length.
- `read_buf`: A buffer of type `bytearray` to store the received data.

**Return Value**

None

### 2.7 `deinit` Method

```python
spi.deinit()
```

Unregisters the SPI module.

**Parameters**

None

**Return Value**

None
