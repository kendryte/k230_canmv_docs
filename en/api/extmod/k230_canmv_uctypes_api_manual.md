# `uctypes` Module API Manual

## Overview

This module provides a way to access binary data in a structured manner. It is the "external data interface" module in MicroPython, conceptually similar to CPython's `ctypes` module, but with a simplified and optimized API suitable for embedded systems requirements. By defining data structure layouts similar to C, users can use dot syntax to access subfields within them.

***Please refer to MicroPython [uctypes official documentation](https://docs.micropython.org/en/latest/library/uctypes.html#module-uctypes) for details***

> **Warning**
>
> The `uctypes` module allows access to arbitrary memory addresses of the machine (including I/O and control registers). Inadvertent use may cause system crashes, data loss, or even hardware damage.
>
> **Also refer to the `ustruct` module**
>
> The `ustruct` module is the standard way to handle binary data in Python, suitable for handling simple data structures, but not suitable for complex, nested structures.

## Structure Description

### Examples

```python
import uctypes

# Example 1: Parsing part of an ELF file header
ELF_HEADER = {
    "EI_MAG": (0x0 | uctypes.ARRAY, 4 | uctypes.UINT8),
    "EI_DATA": 0x5 | uctypes.UINT8,
    "e_machine": 0x12 | uctypes.UINT16,
}

# Assume "f" is an ELF file opened in binary mode
buf = f.read(uctypes.sizeof(ELF_HEADER, uctypes.LITTLE_ENDIAN))
header = uctypes.struct(uctypes.addressof(buf), ELF_HEADER, uctypes.LITTLE_ENDIAN)
assert header.EI_MAG == b"\x7fELF"
assert header.EI_DATA == 1, "Oops, endianness error. You can try using uctypes.BIG_ENDIAN."
print("machine:", hex(header.e_machine))

# Example 2: Data structure in memory (with pointer)
COORD = {
    "x": 0 | uctypes.FLOAT32,
    "y": 4 | uctypes.FLOAT32,
}

STRUCT1 = {
    "data1": 0 | uctypes.UINT8,
    "data2": 4 | uctypes.UINT32,
    "ptr": (8 | uctypes.PTR, COORD),
}

# Assume you have a structure address of "addr"
struct1 = uctypes.struct(addr, STRUCT1, uctypes.NATIVE)
print("x:", struct1.ptr[0].x)

# Example 3: Accessing CPU registers, STM32F4xx WWDG register
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
print(" Current counter :", WWDG.WWDG_CR.T)
```

### Structure Layout Definition

`uctypes` uses Python dictionaries to define structure layouts. The keys in the dictionary are field names, and the values are field attributes (such as offset, data type, etc.). The offset of a field is calculated in bytes from the starting position of the structure.

Examples:

- **Scalar type**:

```python
"field_name": offset | uctypes.UINT32
```

That is, the value of the field is the result of OR-ing the offset and the scalar type.

- **Nested structure**:

```python
"sub": (offset, {
    "b0": 0 | uctypes.UINT8,
    "b1": 1 | uctypes.UINT8,
})
```

That is, the value is a 2-tuple, where the first element is an offset, and the second is a structure descriptor dictionary (note: the offset in the recursive descriptor is relative to the structure it defines). Of course, recursive structures can be specified not only through literal dictionaries, but also by referencing the name of a previously defined structure descriptor dictionary.

- **Array of basic types**:

```python
"arr": (offset | uctypes.ARRAY, size | uctypes.UINT8)
```

That is, the value is a 2-tuple, where the first element is the bitwise OR of the `ARRAY` flag and the offset, and the second is the bitwise OR of the scalar element type and the number of elements in the array.

- **Array of aggregate types**:

```python
"arr2": (offset | uctypes.ARRAY, size, {"b": 0 | uctypes.UINT8})
```

That is, the value is a 3-tuple, where the first element is the result of bitwise OR-ing the `ARRAY` flag with the offset, the second element is the number of elements in the array, and the third element is the descriptor of the element type.

- **Pointer to basic type**:

```python
"ptr": (offset | uctypes.PTR, uctypes.UINT8)
```

That is, the value is a 2-tuple, where the first element is the result of bitwise OR-ing the `PTR` flag with the offset, and the second element is the scalar element type.

- **Pointer to aggregate type**:

```python
"ptr2": (offset | uctypes.PTR, {"b": 0 | uctypes.UINT8})
```

That is, the value is a 2-tuple, where the first element is the result of bitwise OR-ing the `PTR` flag with the offset, and the second element is the descriptor of the pointed-to type.

- **Bitfield**:

```python
"bitf0": offset | uctypes.BFUINT16 | lsbit << uctypes.BF_POS | bitsize << uctypes.BF_LEN
```

That is, `value` is a scalar value type containing the given bitfield (the type name is similar to a scalar type, but prefixed with `BF`), bitwise OR-ed with the offset of the scalar value containing the bitfield, and further bitwise OR-ed with the position and length values of the bitfield within the scalar value, shifted by the `BF_POS` and `BF_LEN` bits, respectively. The position of the bitfield is counted starting from the least significant bit of the scalar (position `0`), and is the rightmost bit of the field (in other words, it is the number of bits the scalar needs to be right-shifted to extract the bitfield).

In the above example, first a `UINT16` value will be extracted at offset `0` (this detail may be important when accessing hardware registers, as specific access sizes and alignments are required), and then a bitfield is extracted, whose rightmost bit is the `lsbit` bit of this `UINT16`, with a length of `bitsize` bits. For example, if `lsbit` is `0` and `bitsize` is `8`, it will actually access the least significant byte of `UINT16`.

Note that bitfield operations are independent of target endianness, in particular the above example will access the least significant byte of `UINT16`, regardless of whether the structure is little-endian or big-endian. But this depends on the least significant bit being numbered as `0`. Some targets may use different numbering in their native ABI, but `uctypes` always uses the standardized numbering described above.

## API Introduction

### `struct` Class

```python
class uctypes.struct(addr, descriptor, layout_type=NATIVE)
```

Instantiate a structure object based on a memory address, descriptor, and layout type.

**Parameters**:

- `addr`: Memory address
- `descriptor`: Structure descriptor (dictionary)
- `layout_type`: Optional, defaults to `NATIVE` (native byte order) (see below)

**Return value**: Returns a structure object

### `sizeof`

```python
uctypes.sizeof(struct, layout_type=NATIVE)
```

Returns the size of the data structure in bytes. The struct argument can be a structure class or a specific instantiated structure object (or its aggregate fields).

**Parameters**:

- `struct`: Structure class or instance
- `layout_type`: Optional, defaults to `NATIVE` (see below).

**Return value**: Size of the structure

### `addressof`

```python
uctypes.addressof(obj)
```

Returns the memory address of an object.

**Parameters**:

- `obj`: An object that supports the buffer protocol

**Return value**: The memory address of the object

### `bytes_at`

```python
uctypes.bytes_at(addr, size)
```

Captures memory at the given address and size, returning an immutable `bytes` object.

### `bytearray_at`

```python
uctypes.bytearray_at(addr, size)
```

Captures memory at the given address and size, returning a mutable `bytearray` object.

### `string_at`

```python
uctypes.string_at(addr, size=1048576)
```

Fetches a string from the given address, with a maximum length of the specified `size`.

## Constant Definitions

### `uctypes.LITTLE_ENDIAN`

Represents the little-endian byte order layout type.

### `uctypes.BIG_ENDIAN`

Represents the big-endian byte order layout type.

### `uctypes.NATIVE`

Represents the layout type with native byte order and alignment.

### Integer Types

Defines integer types of various bit widths, including:

- `uctypes.UINT8`, `uctypes.INT8`
- `uctypes.UINT16`, `uctypes.INT16`
- `uctypes.UINT32`, `uctypes.INT32`
- `uctypes.UINT64`, `uctypes.INT64`

### Floating-Point Types

- `uctypes.FLOAT32`, `uctypes.FLOAT64`

### `uctypes.VOID`

Used to represent the void type, commonly used for pointers.

### `uctypes.PTR` `uctypes.ARRAY`

Type constants for pointers and arrays. Note that structures do not have an explicit constant; it is implicit: an aggregate type without the `PTR` or `ARRAY` flag is a structure.

## Structure Descriptors and Structure Object Instantiation

Structure objects can be instantiated at a specified memory address using `uctypes.struct()` with a structure descriptor dictionary and layout type.
