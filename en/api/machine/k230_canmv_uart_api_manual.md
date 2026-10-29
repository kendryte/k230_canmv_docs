# `UART` Module API Manual

## Overview

K230 integrates five UART (Universal Asynchronous Receiver/Transmitter) hardware modules internally, where UART0 is occupied by the small-core SH, UART3 is occupied by the large-core SH, and the remaining UART1, UART2, and UART4 are available for users. For UART I/O configuration, refer to the IOMUX module.

```{warning}
Before physically connecting UART pins, you must confirm whether the corresponding I/O domain of the development board uses **1.8 V** or **3.3 V** to ensure external device level matching. Do not connect 5 V UART signals. Do not use the low-quality CH340G modules shown in the documentation. For wiring requirements, prohibited module images, and voltage check methods, see [Serial Port Level and Adapter Module Safety](../../example/peripheral/uart.md).
```

## API Introduction

The UART class is located in the `machine` module.

### Example Code

```python
from machine import UART

# Configure UART1: baud rate 115200, 8 data bits, no parity, 1 stop bit
u1 = UART(UART.UART1, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

# Write data to UART
u1.write("UART1 test")

# Read data from UART
r = u1.read()

# Read one line of data
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
- `baudrate`: UART baud rate, optional parameter, default value is 115200.
- `bits`: number of data bits per character, valid values are `FIVEBITS`, `SIXBITS`, `SEVENBITS`, `EIGHTBITS`, optional parameter, default value is `EIGHTBITS`.
- `parity`: parity check, valid values are `PARITY_NONE`, `PARITY_ODD`, `PARITY_EVEN`, optional parameter, default value is `PARITY_NONE`.
- `stop`: number of stop bits, valid values are `STOPBITS_ONE`, `STOPBITS_TWO`, optional parameter, default value is `STOPBITS_ONE`.
- `timeout`: data read timeout, in `ms`

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

Read characters. If `nbytes` is specified, at most that many bytes are read; otherwise, as much data as possible is read.

**Parameters**

- `nbytes`: maximum number of bytes to read, optional parameter.

**Return Value**

Returns a bytes object containing the read bytes.

### `readline` Method

```python
UART.readline()
```

Read one line of data, ending with a newline character.

**Parameters**

None

**Return Value**

Returns a bytes object containing the read bytes.

### `readinto` Method

```python
UART.readinto(buf[, nbytes])
```

Read bytes into `buf`. If `nbytes` is specified, at most that many bytes are read; otherwise, at most `len(buf)` bytes are read.

**Parameters**

- `buf`: a buffer object.
- `nbytes`: maximum number of bytes to read, optional parameter.

**Return Value**

Returns the number of bytes read and stored in `buf`.

### `write` Method

```python
UART.write(buf)
```

Write a byte buffer to the UART.

**Parameters**

- `buf`: a buffer object.

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
