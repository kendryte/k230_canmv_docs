# 2.1 `Uctypes` Module API Documentation

## 1. Overview

This module provides a way to access binary data in a structured manner. It is the "external data interface" module in MicroPython, conceptually similar to CPython's `ctypes` module, but with a simplified and optimized API tailored for embedded systems. By defining data structures with layouts similar to those in C, users can access subfields using dot notation.

> **Warning**
>
> The `uctypes` module allows access to arbitrary memory addresses on the machine (including I/O and control registers). Improper use can lead to system crashes, data loss, or even hardware damage.
>
> **Also see the `ustruct` module**
>
> The `ustruct` module is the standard way to handle binary data in Python. It is suitable for handling simple data structures but not for complex, nested structures.

## 2. Structure Description

### 2.1 Examples

```python
import uctypes

# Example 1: Parsing part of an ELF file header
ELF_HEADER = {
    "EI_MAG": (0x0 | uctypes.ARRAY, 4 | uctypes.UINT8),
    "EI_DATA": 0x5 | uctypes.UINT8,
    "e_machine": 0x12 | uctypes.UINT16,
}

# Assuming "f" is an ELF file opened in binary mode
buf = f.read(uctypes.sizeof(ELF_HEADER, uctypes.LITTLE_ENDIAN))
header = uctypes.struct(uctypes.addressof(buf), ELF_HEADER, uctypes.LITTLE_ENDIAN)
assert header.EI_MAG == b"\x7fELF"
assert header.EI_DATA == 1, "Oops, endianness error. Try using uctypes.BIG_ENDIAN."
print("machine:", hex(header.e_machine))

# Example 2: Data structure in memory (with pointers)
COORD = {
    "x": 0 | uctypes.FLOAT32,
    "y": 4 | uctypes.FLOAT32,
}

STRUCT1 = {
    "data1": 0 | uctypes.UINT8,
    "data2": 4 | uctypes.UINT32,
    "ptr": (8 | uctypes.PTR, COORD),
}

# Assuming you have a structure at address "addr"
struct1 = uctypes.struct(addr, STRUCT1, uctypes.NATIVE)
print("x:", struct1.ptr[0].x)

# Example 3: Accessing CPU registers, STM32F4xx WWDG registers
WWDG_LAYOUT = {
    "WWDG_CR": (0, {
        "WDGA": 7 << uctypes.BF_POS | 1 << uctypes.BF_LEN | uctypes.BFUINT32,
        "T": 0 << uctypes.BF_POS | 7 << uctypes.BF_LEN | uctypes.BFUINT32,
    }),
    "WWDG_CFR": (4, {
        "EWI": 9 << uctypes.BF_POS | 1 << uctypes.BF_LEN | uctypes.BFUINT32,
        "WDGTB": 7 << uctypes.BF_POS | 2 << uctypes.BF_LEN | uctypes.BFUINT32,
        "W": 0 << uctypes.BF_POS | 7 << uctypes.BF_LEN | uctypes.BFUINT32,
    }),
}

WWDG = uctypes.struct(0x40002c00, WWDG_LAYOUT)

WWDG.WWDG_CFR.WDGTB = 0b10
WWDG.WWDG_CR.WDGA = 1
print("Current counter:", WWDG.WWDG_CR.T)
```

### 2.2 Structure Layout Definition

`uctypes` uses Python dictionaries to define structure layouts. The keys in the dictionary are field names, and the values are field attributes (such as offset, data type, etc.). The offset of a field is calculated in bytes from the start of the structure.

Examples:

- **Scalar Types**:

```python
"field_name": offset | uctypes.UINT32
```

That is, the field value is the result of the bitwise OR operation between the offset and the scalar type.

- **Nested Structures**:

```python
"sub": (offset, {
    "b0": 0 | uctypes.UINT8,
    "b1": 1 | uctypes.UINT8,
})
```

- **Arrays**:

```python
"arr": (offset | uctypes.ARRAY, size | uctypes.UINT8)
```

- **Pointers**:

```python
"ptr": (offset | uctypes.PTR, uctypes.UINT8)
```

- **Bitfields**:

```python
"bitf0": offset | uctypes.BFUINT16 | lsbit << uctypes.BF_POS | bitsize << uctypes.BF_LEN
```

In bitfield definitions, `lsbit` is the position of the least significant bit, and `bitsize` is the length of the bitfield.

## 3. API Introduction

### 3.1 `struct` Class

```python
class uctypes.struct(addr, descriptor, layout_type=NATIVE)
```

Instantiates a structure object based on memory address, descriptor, and layout type.

**Parameters**:

- `addr`: Memory address
- `descriptor`: Structure descriptor (dictionary)
- `layout_type`: Optional, defaults to `NATIVE` (native byte order)

**Returns**: Returns a structure object

### 3.2 `sizeof`

```python
uctypes.sizeof(struct, layout_type=NATIVE)
```

Returns the size of the data structure (in bytes).

**Parameters**:

- `struct`: Structure class or instance
- `layout_type`: Optional, defaults to `NATIVE`

**Returns**: Size of the structure

### 3.3 `addressof`

```python
uctypes.addressof(obj)
```

Returns the memory address of an object.

**Parameters**:

- `obj`: An object that supports the buffer protocol

**Returns**: Memory address of the object

### 3.4 `bytes_at`

```python
uctypes.bytes_at(addr, size)
```

Captures memory at the given address and size, returning an immutable `bytes` object.

### 3.5 `bytearray_at`

```python
uctypes.bytearray_at(addr, size)
```

Captures memory at the given address and size, returning a mutable `bytearray` object.

### 3.6 `string_at`

```python
uctypes.string_at(addr, size=1048576)
```

Gets a string from the given address, with a maximum length specified by `size`.

## 4. Constant Definitions

### 4.1 `uctypes.LITTLE_ENDIAN`

Represents little-endian byte order layout type.

### 4.2 `uctypes.BIG_ENDIAN`

Represents big-endian byte order layout type.

### 4.3 `uctypes.NATIVE`

Represents native byte order and alignment layout type.

### 4.4 Integer Types

Defines various bit-width integer types, including:

- `uctypes.UINT8`, `uctypes.INT8`
- `uctypes.UINT16`, `uctypes.INT16`
- `uctypes.UINT32`, `uctypes.INT32`
- `uctypes.UINT64`, `uctypes.INT64`

### 4.5 Floating Point Types

- `uctypes.FLOAT32`, `uctypes.FLOAT64`

### 4.6 `uctypes.VOID`

Used to represent a void type, commonly used for pointers.

## 5. Structure Descriptor and Structure Object Instantiation

You can instantiate structure objects at specified memory addresses using the structure descriptor dictionary and layout type with `uctypes.struct()`.
