# `machine` Module API Manual

## Overview

The `machine` module contains functions related to specific hardware boards. Most of the functions in this module allow direct and unrestricted access to and control over hardware components on the system. Improper use may cause board malfunction, deadlock, or crash, and may even result in hardware damage in extreme cases.

## API Introduction

### `reset` Method

```python
machine.reset()
```

Immediately reset the SoC (System on Chip).

**Parameters**

None

**Return Value**

None

### `bootloader` Method

```python
machine.bootloader()
```

Enter the bootloader.

**Parameters**

None

**Return Value**

None

### `mem_copy` Method

```python
machine.mem_copy(dst, src, size)
```

Copy a specified amount of data from the source memory address to the destination memory address.

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

Get the result from the chip's internal temperature sensor

**Parameters**

None

**Return Value**

Temperature value, floating-point number

### `chipid` Method

```python
chipid = machine.chipid()
```

Get the chip `ID`

**Parameters**

None

**Return Value**

`bytearray` of length `32`
