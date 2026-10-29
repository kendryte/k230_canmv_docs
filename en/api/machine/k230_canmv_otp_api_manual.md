# `OTP` Module API Manual

## Overview

CanMV K230 provides the `OTP` (One-Time Programmable) class for reading chip OTP data and querying the read/write lock status of a specified address.

The OTP object is a singleton object, and repeated calls to `OTP()` return the same instance.

## API Introduction

The OTP class is located under the `machine` module.

### Example

```python
from machine import OTP
import binascii

otp = OTP()

data = otp.read(0x000, 32)
print(binascii.hexlify(data))

lock = otp.get_lock(0x000)
if lock == OTP.NA:
    print("No Access")
elif lock == OTP.RO:
    print("Read Only")
elif lock == OTP.RW:
    print("Read Write")
```

### Constructor

```python
otp = OTP()
```

**Parameters**

None

**Return Value**

Returns the OTP singleton object.

### `read` Method

```python
data = otp.read(addr, length)
```

#### Function

Reads byte data from the specified address in OTP.

**Parameters**

- `addr`: The starting address to read from, ranging from `0x000` to `0xFFF`, must be 4-byte aligned.
- `length`: The read length, ranging from 1 to 1024 bytes.

**Return Value**

Returns the read OTP data, of type `bytes`.

**Restrictions**

- `addr + length` cannot exceed the total OTP range.
- A single read cannot cross the `0x400` boundary.

### `get_lock` Method

```python
lock = otp.get_lock(addr)
```

#### Function

Query the read/write lock status of the specified OTP address.

**Parameters**

- `addr`: The OTP address to query, ranging from `0x000` to `0xFFF`, must be 4-byte aligned.

**Return Value**

Returns a lock status integer, which can be compared with the following constants:

| Constant | Value | Description |
| - | - | - |
| `OTP.NA` | 0 | No Access |
| `OTP.RO` | 1 | Read Only |
| `OTP.RW` | 2 | Read Write |

## Constants

| Constant | Description |
| - | - |
| `OTP.NA` | OTP address is not accessible |
| `OTP.RO` | OTP address is read-only |
| `OTP.RW` | OTP address is readable and writable |

## Notes

- OTP may store device security configuration or identity-related information. Please confirm the usage scenario before printing or saving.
- Currently, `machine.OTP` only provides read and lock status query interfaces, and does not provide write or lock interfaces.
