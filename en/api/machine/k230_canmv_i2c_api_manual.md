# `I2C` Module API Manual

## Overview

The K230 chip is equipped with 5 I2C hardware modules internally, supporting standard 100 kb/s, fast 400 kb/s, and high-speed 3.4 Mb/s communication modes.
In addition, K230 also implements 5 software I2C modules for users to choose from.

## Master Device API Introduction

The `I2C` class is located in the `machine` module.

### Example Code

```python
import time
from machine import I2C

# C32 parameters
EEPROM_ADDR = 0x50  # I2C address of 24C32
PAGE_SIZE = 32      # Page size of 24C32 (bytes)
MEM_SIZE = 4096     # Total capacity of 24C32 (4KB)

# Initialize I2C
i2c = I2C(2, scl=11, sda=12, freq=40000)

def test_24c32():
    print("24C32 EEPROM test started...")

    # Test data - generate cyclic pattern of 0x00-0xFF
    test_data = bytearray([x & 0xFF for x in range(PAGE_SIZE)])
    test_addr = 0x0000  # Test starting address

    print("Write data: [{}]".format(", ".join("0x{:02x}".format(x) for x in test_data)))

    # Write a page of data (24C32 supports page write)
    i2c.writeto_mem(EEPROM_ADDR, test_addr, test_data, addrsize=16)
    print("Write completed, address: 0x{:04x}".format(test_addr))

    # Wait for EEPROM to complete write (important!)
    time.sleep_ms(10)  # 24C32 page write typical time is 5ms

    # Read back data
    read_data = i2c.readfrom_mem(EEPROM_ADDR, test_addr, len(test_data), addrsize=16)
    print("Read data: [{}]".format(", ".join("0x{:02x}".format(x) for x in read_data)))

    # Verify data
    if test_data == read_data:
        print("Test successful! Write and read data match")
    else:
        print("Test failed! Data mismatch")

    # Random address read/write test
    print("\nRandom address read/write test...")
    import urandom
    test_addr = urandom.getrandbits(12)  # Generate 12-bit random address (0-0xFFF)
    test_byte = urandom.getrandbits(8)   # Generate random test byte

    print("Write byte at address 0x{:04x}: 0x{:02x}".format(test_addr, test_byte))
    i2c.writeto_mem(EEPROM_ADDR, test_addr, bytearray([test_byte]), addrsize=16)
    time.sleep_ms(5)  # Wait for write to complete

    read_byte = i2c.readfrom_mem(EEPROM_ADDR, test_addr, 1, addrsize=16)[0]
    print("Read byte: 0x{:02x}".format(read_byte))

    if test_byte == read_byte:
        print("Random address test successful!")
    else:
        print("Random address test failed!")

# Run test
test_24c32()

```

### Constructor

```python
i2c = I2C(id, scl , sda, freq=400000, timeout = 50000)
```

**Parameters**

- `id`: I2C device ID, hardware I2C is [0~4], software I2C is [5~9]
- `scl`: I2C scl pin
- `sda`: I2C sda pin
- `freq`: I2C clock frequency. Software I2C may not be able to set all frequencies, please refer to the actual result.
- `timeout`: I2C communication timeout

### `scan` Method

```python
i2c.scan()
```

Scans the slave devices on the current I2C bus and returns a list of 7-bit addresses of responding devices.

**Parameters**

None

**Return Value**

Returns a list containing all scanned slave addresses.

### `readfrom` Method

```python
i2c.readfrom(addr, len, True)
```

Reads data of the specified length from the slave at the specified I2C address.

**Parameters**

- `addr`: Slave address.
- `len`: Length of data to read.
- `stop`: Whether to send a stop signal. Currently only the default value `True` is supported.

**Return Value**

Returns the read data, type is `bytes`.

### `readfrom_into` Method

```python
i2c.readfrom_into(addr, buf, True)
```

Reads data from the slave at the specified I2C address into the buffer according to the buffer length.

**Parameters**

- `addr`: Slave address.
- `buf`: `bytearray` type, defines the length and is used to store the read data.
- `stop`: Whether to send a stop signal. Currently only the default value `True` is supported.

**Return Value**

None

### `writeto` Method

```python
i2c.writeto(addr, buf, True)
```

Sends the data in the buffer to the slave at the specified I2C address.

**Parameters**

- `addr`: Slave address.
- `buf`: Data to be sent.
- `stop`: Whether to send a stop signal. Currently only the default value `True` is supported.

**Return Value**

Number of bytes successfully sent.

### `readfrom_mem` Method

```python
i2c.readfrom_mem(addr, memaddr, nbytes, addrsize=8)
```

Reads data of the specified length from the specified memory address of the memory. Used for I2C operations on memory-type devices.

**Parameters**

- `addr`: I2C slave address.
- `memaddr`: Memory storage address.
- `nbytes`: Number of bytes to read.
- `addrsize`: Memory address width, default is 8 bits.

**Return Value**

Returns the read data, type is `bytes`.

### `readfrom_mem_into` Method

```python
i2c.readfrom_mem_into(addr, memaddr, buf, addrsize=8)
```

Reads data from the specified memory address of the memory into the buffer according to the buffer length. Used for I2C operations on memory-type devices.

**Parameters**

- `addr`: I2C slave address.
- `memaddr`: Memory storage address.
- `buf`: `bytearray` type, defines the length and is used to store the read data.
- `addrsize`: Register address width, default is 8 bits.

**Return Value**

None

### `writeto_mem` Method

```python
i2c.writeto_mem(addr, memaddr, buf, mem_size=8)
```

Writes the data in the specified buffer to the specified memory address of the memory. Used for I2C operations on memory-type devices.

**Parameters**

- `addr`: I2C slave address.
- `memaddr`: Memory storage address.
- `buf`: Data to be written.
- `mem_size`: Storage address width, default is 8 bits.

**Return Value**

None
