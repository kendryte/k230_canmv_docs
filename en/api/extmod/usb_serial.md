# `USB Serial` Module API Manual

## Overview

The USB Serial module provides data communication functionality through a USB serial port. This module implements the standard stream protocol interface and supports read/write operations.

This module supports communication with 4G modules through AT commands.

## API Introduction

The Serial class belongs to the usb module.

## Constructor

### `Serial(path, timeout_ms=300)`

Creates a USB Serial object.

**Parameters:**

- `path` (str): Serial port device path
- `timeout_ms` (int): Read/write timeout in milliseconds, default is 300ms

**Return Value:**

USB Serial object

**Example:**

```python
from usb import Serial

# Create USB Serial object
serial = Serial("/dev/ttyUSB1", timeout_ms=300)
```

## Methods

### `open([path])`

Open the USB serial port device.

**Parameters:**

- `path` (str, optional): If provided, this path will be used instead of the path specified in the constructor

**Return value:**

- `True`: Opened successfully
- `False`: Failed to open

**Example:**

```python
serial.open()  # Use the path specified in the constructor
serial.open("/dev/ttyUSB2")  # Use a new path
```

### `close()`

Close the USB serial port device.

**Example:**

```python
serial.close()
```

### `read(size)`

Read data from the serial port.

**Parameters:**

- `size` (int): Number of bytes to read

**Return value:**
The data read (bytes type)

### `readinto(buf)`

Read data into the buffer.

**Parameters:**

- `buf` (bytearray): Target buffer

**Return value:**
Actual number of bytes read

### `readline()`

Read a line of data until a newline character or timeout is encountered.

**Return value:**
The line data read (bytes type)

### `write(buf)`

Write data to the serial port.

**Parameters:**

- `buf` (bytes/bytearray): The data to write

**Return value:**
Actual number of bytes written

## Properties

### `path`

Gets or sets the serial device path.

**Example:**

```python
print(serial.path)  # Get the current path
serial.path = "/dev/ttyUSB1"  # Set a new path
```

### `timeout_ms`

Gets or sets the read/write timeout duration (in milliseconds).

**Example:**

```python
print(serial.timeout_ms)  # Get the current timeout duration
serial.timeout_ms = 1000  # Set the timeout duration to 1 second
```

## Stream Protocol Support

The USB Serial object implements the standard stream protocol and can be used directly in scenarios requiring a stream object.

**Example:**

```python
# Use the readline() method to read a line of data
line = serial.readline()

# Use the write() method to write data
serial.write(b"Hello World\n")
```

## Notes

1. The `close()` method is automatically called when the object is destroyed to close the serial port
1. All read and write operations are controlled by the `timeout_ms` parameter
1. If the serial port is not opened, calling read/write methods will raise an OSError exception
1. The default device path is "/dev/ttyUSB1", please modify it according to the actual device
