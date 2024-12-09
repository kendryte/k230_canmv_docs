# 2.14 `Machine` Module API Documentation

## 1. Overview

The `machine` module contains functions related to specific hardware boards. Most functions in this module allow direct and unrestricted access to and control of hardware components on the system. Improper use may lead to motherboard malfunction, system crashes, or even hardware damage in extreme cases.

## 2. API Introduction

### 2.1 `reset` Method

```python
machine.reset()
```

Immediately resets the SoC (System on Chip).

**Parameters**

None

**Return Value**

None

### 2.2 `mem_copy` Method

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

### 2.3 `temperature` Method

```python
temp = machine.temperature()
```

Get chip temperature from tsensor.

**Parameters**

None

**Return Value**

Temperature.
