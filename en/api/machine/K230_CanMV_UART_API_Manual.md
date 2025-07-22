# `UART` Module API Manual

## Overview

The K230 integrates five UART (Universal Asynchronous Receiver/Transmitter) hardware modules internally. Among them, UART0 is occupied by the small core SH, UART3 is occupied by the large core SH, and the remaining UART1, UART2, and UART4 are available for user use. The I/O configuration of the UART can be referenced from the IOMUX module.

## API Introduction

The UART class is located in the `machine` module.

### Example Code

```python
from machine import UART

# Configure UART1: Baud rate 115200, 8 data bits, no parity, 1 stop bit
u1 = UART(UART.UART1, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

# Write data to UART
u1.write("UART1 test")

# Read data from UART
r = u1.read()

# Read a line of data
r = u1.readline()

# Read data into a byte buffer
b = bytearray(8)
r = u1.readinto(b)

# Release UART resources
u1.deinit()
```

### Constructor

```python
uart = UART(id, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE, timeout = 0)
```

**Parameters**

- `id`: UART module number, valid values are `UART1`, `UART2`, `UART4`.
- `baudrate`: UART baud rate, optional, default value is 115200.
- `bits`: Number of data bits per character, valid values are `FIVEBITS`, `SIXBITS`, `SEVENBITS`, `EIGHTBITS`, optional, default value is `EIGHTBITS`.
- `parity`: Parity check, valid values are `PARITY_NONE`, `PARITY_ODD`, `PARITY_EVEN`, optional, default value is `PARITY_NONE`.
- `stop`: Number of stop bits, valid values are `STOPBITS_ONE`, `STOPBITS_TWO`, optional, default value is `STOPBITS_ONE`.
- `timeout`: Read data timeout time in ms.

### `init` Method

```python
UART.init(baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
```

Configure UART parameters.

**Parameters**

Refer to the constructor.

**Return Value**

None

### `read` Method

```python
UART.read([nbytes])
```

Read characters. If `nbytes` is specified, read up to that number of bytes; otherwise, read as much data as possible.

**Parameters**

- `nbytes`: Maximum number of bytes to read, optional.

**Return Value**

Returns a byte object containing the read bytes.

### `readline` Method

```python
UART.readline()
```

Read a line of data, ending with a newline character.

**Parameters**

None

**Return Value**

Returns a byte object containing the read bytes.

### `readinto` Method

```python
UART.readinto(buf[, nbytes])
```

Read bytes into `buf`. If `nbytes` is specified, read up to that number of bytes; otherwise, read up to `len(buf)` bytes.

**Parameters**

- `buf`: A buffer object.
- `nbytes`: Maximum number of bytes to read, optional.

**Return Value**

Returns the number of bytes read and stored in `buf`.

### `write` Method

```python
UART.write(buf)
```

Write a byte buffer to the UART.

**Parameters**

- `buf`: A buffer object.

**Return Value**

Returns the number of bytes written.

### `deinit` Method

```python
UART.deinit()
```

Release UART resources.

**Parameters**

None

**Return Value**

None
