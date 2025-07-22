# `Machine` Module API Documentation

## Overview

The `machine` module contains functions related to specific hardware boards. Most functions in this module allow direct and unrestricted access to and control of hardware components on the system. Improper use may lead to motherboard malfunction, system crashes, or even hardware damage in extreme cases.

## API Introduction

### `reset` Method

```python
machine.reset()
```

Immediately resets the SoC (System on Chip).

**Parameters**

None

**Return Value**

None

### `mem_copy` Method

```python
machine.mem_copy(dst, src, size)
```

Copies a specified amount of data from the source memory address to the destination memory address.

**Parameters**

- `dst`: Destination address.
- `src`: Source address.
- `size`: Number of bytes to copy.

**Return Value**

None

### `temperature` Method

```python
temp = machine.temperature()
```

Get chip temperature from tsensor.

**Parameters**

None

**Return Value**

Temperature.

### `chipid` Method

```python
chipid = machine.chipid()
```

get chip ID

**Parameters**

None

**Return Value**

bytearray, lenght 32.
