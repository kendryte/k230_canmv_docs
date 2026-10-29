# OTP Usage Tutorial

## What is OTP?

**OTP (One-Time Programmable)** is a non-volatile area inside the chip used to store security configuration, key indices, calibration data, or device identity information. CanMV K230 currently provides OTP data read and read/write lock status query interfaces in `machine.OTP`.

OTP content is usually related to device security status, and read results may contain device-related information. The example only demonstrates reading and querying lock status. Please avoid exposing complete OTP output in actual use.

## K230 OTP Features

| Feature | Description |
| - | - |
| Instance model | `OTP()` returns a singleton object, multiple calls return the same instance |
| Address range | `0x000` to `0xFFF` |
| Address alignment | Address must be 4-byte aligned |
| Single read length | 1 to 1024 bytes |
| Boundary limit | A single read cannot cross the `0x400` boundary |
| Lock status | Supports querying `OTP.NA`, `OTP.RO`, `OTP.RW` |

## Application Example: Reading OTP and Querying Lock Status

This example demonstrates how to create an OTP object, read data from a specified address, and query the lock status of several 4-byte aligned addresses.

### Example Code

```python
from machine import OTP
import binascii


def lock_name(lock):
    if lock == OTP.NA:
        return "NA"
    if lock == OTP.RO:
        return "RO"
    if lock == OTP.RW:
        return "RW"
    return "UNKNOWN"


otp = OTP()

# OTP is a singleton object, calling OTP() again returns the same object.
print("same OTP object:", otp is OTP())

# Read data from a 4-byte aligned OTP address.
# Up to 1024 bytes can be read at a time, and cannot cross the 0x400 boundary.
data = otp.read(0x000, 32)
print("OTP[0x000:0x020]:", binascii.hexlify(data))

# Query the lock status of 4-byte aligned addresses.
for addr in (0x000, 0x004, 0x400, 0xC00):
    lock = otp.get_lock(addr)
    print("OTP[0x%03x] lock: %s (%d)" % (addr, lock_name(lock), lock))
```

## Interface Description

| Method Name | Description |
| - | - |
| `OTP()` | Get the OTP singleton object |
| `read(addr, length)` | Read byte data from the specified OTP address |
| `get_lock(addr)` | Query the OTP lock status of the specified address |

## Example Analysis

1. **Get the OTP object**
   `otp = OTP()` returns the OTP singleton object. When `OTP()` is called multiple times in a program, the same object is obtained.

1. **Read OTP data**
   `otp.read(0x000, 32)` reads 32 bytes of data starting from address `0x000`, and the return value type is `bytes`.

1. **Query lock status**
   `otp.get_lock(addr)` returns the lock status of the specified address, which can be compared with the constants `OTP.NA`, `OTP.RO`, `OTP.RW`.

## Lock Status Description

| Constant | Value | Meaning |
| - | - | - |
| `OTP.NA` | 0 | No Access, not accessible |
| `OTP.RO` | 1 | Read Only |
| `OTP.RW` | 2 | Read Write |

## Notes

- `addr` must be within the range `0x000` to `0xFFF`, and must be 4-byte aligned.
- `length` must be within the range of 1 to 1024 bytes.
- A single read cannot cross the `0x400` boundary, for example, reading 32 bytes from `0x3F0` will fail.
- The current `machine.OTP` only provides read and lock status query interfaces, and does not provide write or lock interfaces.
- OTP data may contain device security-related information. Please confirm the usage scenario before printing or saving.

## Further Reading

- [K230 OTP API Documentation](../../api/machine/k230_canmv_otp_api_manual.md)
