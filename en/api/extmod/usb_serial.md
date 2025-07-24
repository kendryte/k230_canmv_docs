# `USB Serial` Module API Manual

## Overview

The USB Serial module provides functionality for data communication via USB serial ports. This module implements the standard stream protocol interface and supports read/write operations.

This module supports communication with 4G modules via AT commands.

## API Definition

The Serial class is located in the `usb` module.

## Constructor

### `Sserial(path, timeout_ms=300)`

Creates a USB Serial object.

**Parameters:**

- `path` (str): Serial device path
- `timeout_ms` (int): Read/write timeout in milliseconds, defaults to 300ms

**Returns:**
USB Serial object

**Example:**

```python
from usb import Serial

# Create USB Serial object
serial = Serial("/dev/ttyUSB1", timeout_ms=300)
```

## Methods

### `open([path])`

Opens the USB serial device.

**Parameters:**

- `path` (str, optional): If provided, will use this path instead of the one specified in the constructor

**Returns:**

- `True`: Open successful
- `False`: Open failed

**Example:**

```python
serial.open()  # Use path specified in constructor
serial.open("/dev/ttyUSB2")  # Use new path
```

### `close()`

Closes the USB serial device.

**Example:**

```python
serial.close()
```

### `read(size)`

Reads data from the serial port.

**Parameters:**

- `size` (int): Number of bytes to read

**Returns:**
Read data (bytes type)

### `readinto(buf)`

Reads data into a buffer.

**Parameters:**

- `buf` (bytearray): Target buffer

**Returns:**
Number of bytes actually read

### `readline()`

Reads a line of data until encountering a newline character or timeout.

**Returns:**
Line data read (bytes type)

### `write(buf)`

Writes data to the serial port.

**Parameters:**

- `buf` (bytes/bytearray): Data to write

**Returns:**
Number of bytes actually written

## Properties

### `path`

Gets or sets the serial device path.

**Example:**

```python
print(serial.path)  # Get current path
serial.path = "/dev/ttyUSB1"  # Set new path
```

### `timeout_ms`

Gets or sets the read/write timeout (milliseconds).

**Example:**

```python
print(serial.timeout_ms)  # Get current timeout
serial.timeout_ms = 1000  # Set timeout to 1 second
```

## Stream Protocol Support

The USB Serial object implements the standard stream protocol and can be directly used in contexts requiring stream objects.

**Example:**

```python
# Read a line of data using readline()
line = serial.readline()

# Write data using write()
serial.write(b"Hello World\n")
```

## Notes

1. The `close()` method is automatically called when the object is destroyed
1. All read/write operations are controlled by the `timeout_ms` parameter
1. Calling read/write methods when the serial port is not open will raise an OSError exception
1. The default device path is "/dev/ttyUSB1" - please modify according to actual device
