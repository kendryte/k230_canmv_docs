# OTP 使用教程

## 什么是 OTP？

**OTP（One-Time Programmable，一次性可编程存储器）** 是芯片内部用于保存安全配置、密钥索引、校准数据或设备身份信息的非易失性区域。CanMV K230 当前在 `machine.OTP` 中提供 OTP 数据读取和读写锁状态查询接口。

OTP 内容通常与设备安全状态相关，读取结果可能包含设备相关信息。示例仅演示读取和查询锁状态，实际使用时请避免公开完整 OTP 输出。

## K230 OTP 特性

| 特性 | 描述 |
| - | - |
| 实例模型 | `OTP()` 返回单例对象，多次调用得到同一个实例 |
| 地址范围 | `0x000` 到 `0xFFF` |
| 地址对齐 | 地址必须 4 字节对齐 |
| 单次读取长度 | 1 到 1024 字节 |
| 边界限制 | 单次读取不能跨越 `0x400` 边界 |
| 锁状态 | 支持查询 `OTP.NA`、`OTP.RO`、`OTP.RW` |

## 应用示例：读取 OTP 并查询锁状态

本示例展示如何创建 OTP 对象、读取指定地址的数据，并查询几个 4 字节对齐地址的锁状态。

### 示例代码

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

# OTP 是单例对象，再次调用 OTP() 会返回同一个对象。
print("same OTP object:", otp is OTP())

# 从 4 字节对齐的 OTP 地址读取数据。
# 单次最多读取 1024 字节，且不能跨越 0x400 边界。
data = otp.read(0x000, 32)
print("OTP[0x000:0x020]:", binascii.hexlify(data))

# 查询 4 字节对齐地址的锁状态。
for addr in (0x000, 0x004, 0x400, 0xC00):
    lock = otp.get_lock(addr)
    print("OTP[0x%03x] lock: %s (%d)" % (addr, lock_name(lock), lock))
```

## 接口说明

| 方法名 | 说明 |
| - | - |
| `OTP()` | 获取 OTP 单例对象 |
| `read(addr, length)` | 从 OTP 指定地址读取字节数据 |
| `get_lock(addr)` | 查询指定地址的 OTP 锁状态 |

## 示例解析

1. **获取 OTP 对象**
   `otp = OTP()` 返回 OTP 单例对象。程序中多次调用 `OTP()` 时，得到的是同一个对象。

1. **读取 OTP 数据**
   `otp.read(0x000, 32)` 从 `0x000` 地址开始读取 32 字节数据，返回值类型为 `bytes`。

1. **查询锁状态**
   `otp.get_lock(addr)` 返回指定地址的锁状态，可与 `OTP.NA`、`OTP.RO`、`OTP.RW` 常量比较。

## 锁状态说明

| 常量 | 数值 | 含义 |
| - | - | - |
| `OTP.NA` | 0 | No Access，不可访问 |
| `OTP.RO` | 1 | Read Only，只读 |
| `OTP.RW` | 2 | Read Write，可读写 |

## 注意事项

- `addr` 必须在 `0x000` 到 `0xFFF` 范围内，并且必须 4 字节对齐。
- `length` 必须在 1 到 1024 字节范围内。
- 单次读取不能越过 `0x400` 边界，例如从 `0x3F0` 读取 32 字节会失败。
- 当前 `machine.OTP` 仅提供读取和锁状态查询接口，不提供写入或锁定接口。
- OTP 数据可能包含设备安全相关信息，打印或保存前请确认使用场景。

## 延伸阅读

- [K230 OTP API 文档](../../api/machine/k230_canmv_otp_api_manual.md)
