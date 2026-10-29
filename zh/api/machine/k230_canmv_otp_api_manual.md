# `OTP` 模块 API 手册

## 概述

CanMV K230 提供 `OTP`（One-Time Programmable，一次性可编程存储器）类，用于读取芯片 OTP 数据并查询指定地址的读写锁状态。

OTP 对象为单例对象，重复调用 `OTP()` 会返回同一个实例。

## API 介绍

OTP 类位于 `machine` 模块下。

### 示例

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

### 构造函数

```python
otp = OTP()
```

**参数**

无

**返回值**

返回 OTP 单例对象。

### `read` 方法

```python
data = otp.read(addr, length)
```

#### 功能

从 OTP 指定地址读取字节数据。

**参数**

- `addr`: 读取起始地址，范围为 `0x000` 到 `0xFFF`，必须 4 字节对齐。
- `length`: 读取长度，范围为 1 到 1024 字节。

**返回值**

返回读取到的 OTP 数据，类型为 `bytes`。

**限制**

- `addr + length` 不能超过 OTP 总范围。
- 单次读取不能跨越 `0x400` 边界。

### `get_lock` 方法

```python
lock = otp.get_lock(addr)
```

#### 功能

查询指定 OTP 地址的读写锁状态。

**参数**

- `addr`: 要查询的 OTP 地址，范围为 `0x000` 到 `0xFFF`，必须 4 字节对齐。

**返回值**

返回锁状态整数，可与以下常量比较：

| 常量 | 数值 | 说明 |
| - | - | - |
| `OTP.NA` | 0 | No Access，不可访问 |
| `OTP.RO` | 1 | Read Only，只读 |
| `OTP.RW` | 2 | Read Write，可读写 |

## 常量

| 常量 | 说明 |
| - | - |
| `OTP.NA` | OTP 地址不可访问 |
| `OTP.RO` | OTP 地址只读 |
| `OTP.RW` | OTP 地址可读写 |

## 注意事项

- OTP 可能保存设备安全配置或身份相关信息，打印和保存前请确认使用场景。
- 当前 `machine.OTP` 仅提供读取和锁状态查询接口，不提供写入或锁定接口。
