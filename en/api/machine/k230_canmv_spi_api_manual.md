# `SPI` Module API Manual

## Overview

The K230 integrates three SPI hardware modules internally, supporting chip select polarity configuration and adjustable clock rates. The I/O configuration for channel output can refer to the IOMUX module.

## API Introduction

The SPI class is located in the `machine` module.

### Example Code

```python
from machine import SPI

# Initialize SPI, clock rate 5 MHz, polarity 0, phase 0, data bit width 8 bits
spi = SPI(id, baudrate=5000000, polarity=0, phase=0, bits=8)

# Send data to the slave device
spi.write(buf)

# Send data while reading received data into a variable
spi.write_readinto(write_buf, read_buf)

# Close SPI
spi.deinit()
```

### Constructor

```python
spi = machine.SPI(id, baudrate=20, polarity=0, phase=0, bits=8)
```

**Parameters**

- `id`: SPI module ID, with a value range of [0~2] (corresponding to `spi.SPI0` to `spi.SPI2`).
- `baudrate`: SPI clock rate, calculated as \( F_{sclk\_out} = \frac{F_{ssi\_clk}}{BAUDR} \).
- `polarity`: Clock polarity.
- `phase`: Clock phase.
- `bits`: Data bit width.

### `read` Method

```python
spi.read(nbytes)
```

Reads the specified number of bytes of data.

**Parameters**

- `nbytes`: The number of bytes to read.

**Return Value**

Returns a `bytes` object.

### `readinto` Method

```python
spi.readinto(buf)
```

Reads data into the specified buffer.

**Parameters**

- `buf`: A buffer of type `bytearray`.

**Return Value**

None

### `write` Method

```python
spi.write(buf)
```

Sends data.

**Parameters**

- `buf`: Data of type `bytearray`, defining the data to be sent and its length.

**Return Value**

None

### `write_readinto` Method

```python
spi.write_readinto(write_buf, read_buf)
```

Sends data while reading received data into the specified variable.

**Parameters**

- `write_buf`: Data of type `bytearray`, defining the data to be sent and its length.
- `read_buf`: A buffer of type `bytearray`, used to store the received data.

**Return Value**

None

### `deinit` Method

```python
spi.deinit()
```

Deinitializes the SPI module.

**Parameters**

None

**Return Value**

None
