# 2.1 `uctypes` 模块 API 手册

## 1. 概述

该模块提供一种以结构化方式访问二进制数据的方法。它是 MicroPython 中的“外部数据接口”模块，概念上类似于 CPython 的 `ctypes` 模块，但 API 经过简化和优化，适合嵌入式系统的需求。通过定义与 C 语言类似的数据结构布局，用户可以使用点语法来访问其中的子字段。

> **警告**
>
> `uctypes` 模块允许访问机器的任意内存地址（包括 I/O 和控制寄存器）。不慎使用可能导致系统崩溃、数据丢失，甚至硬件损坏。
>
> **也可参考 `ustruct` 模块**
>
> `ustruct` 模块是 Python 中处理二进制数据的标准方式，适合处理简单的数据结构，但不适用于复杂、嵌套的结构。

## 2. 结构说明

### 2.1 示例

```python
import uctypes

# 示例 1: 解析 ELF 文件头的一部分
ELF_HEADER = {
    "EI_MAG": (0x0 | uctypes.ARRAY, 4 | uctypes.UINT8),
    "EI_DATA": 0x5 | uctypes.UINT8,
    "e_machine": 0x12 | uctypes.UINT16,
}

# 假设 "f" 是一个以二进制模式打开的 ELF 文件
buf = f.read(uctypes.sizeof(ELF_HEADER, uctypes.LITTLE_ENDIAN))
header = uctypes.struct(uctypes.addressof(buf), ELF_HEADER, uctypes.LITTLE_ENDIAN)
assert header.EI_MAG == b"\x7fELF"
assert header.EI_DATA == 1, "Oops, endianness 错误。可以尝试使用 uctypes.BIG_ENDIAN。"
print("machine:", hex(header.e_machine))

# 示例 2: 内存中的数据结构（带有指针）
COORD = {
    "x": 0 | uctypes.FLOAT32,
    "y": 4 | uctypes.FLOAT32,
}

STRUCT1 = {
    "data1": 0 | uctypes.UINT8,
    "data2": 4 | uctypes.UINT32,
    "ptr": (8 | uctypes.PTR, COORD),
}

# 假设你有一个结构地址为 "addr"
struct1 = uctypes.struct(addr, STRUCT1, uctypes.NATIVE)
print("x:", struct1.ptr[0].x)

# 示例 3: 访问 CPU 寄存器， STM32F4xx WWDG 寄存器
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
print(" 当前计数器 :", WWDG.WWDG_CR.T)
```

### 2.2 结构布局定义

`uctypes` 使用 Python 字典来定义结构布局。字典中的键为字段名称，值为字段属性（例如偏移量、数据类型等）。字段的偏移量从结构的起始位置按字节计算。

示例：

- **标量类型**：

```python
"field_name": offset | uctypes.UINT32
```

即，字段的值是偏移量和标量类型的或运算结果。

- **嵌套结构**：

```python
"sub": (offset, {
    "b0": 0 | uctypes.UINT8,
    "b1": 1 | uctypes.UINT8,
})
```

- **数组**：

```python
"arr": (offset | uctypes.ARRAY, size | uctypes.UINT8)
```

- **指针**：

```python
"ptr": (offset | uctypes.PTR, uctypes.UINT8)
```

- **位域**：

```python
"bitf0": offset | uctypes.BFUINT16 | lsbit << uctypes.BF_POS | bitsize << uctypes.BF_LEN
```

在位域定义中，`lsbit` 为最右位的位置，`bitsize` 为位域长度。

## 3. API 介绍

### 3.1 `struct` 类

```python
class uctypes.struct(addr, descriptor, layout_type=NATIVE)
```

根据内存地址、描述符和布局类型来实例化一个结构对象。

**参数**：

- `addr`: 内存地址
- `descriptor`: 结构描述符（字典）
- `layout_type`: 可选，默认为 `NATIVE`（本机字节序）

**返回值**：返回结构对象

### 3.2 `sizeof`

```python
uctypes.sizeof(struct, layout_type=NATIVE)
```

返回数据结构的大小（以字节为单位）。

**参数**：

- `struct`: 结构类或实例
- `layout_type`: 可选，默认为 `NATIVE`

**返回值**：结构的大小

### 3.3 `addressof`

```python
uctypes.addressof(obj)
```

返回对象的内存地址。

**参数**：

- `obj`: 支持缓冲区协议的对象

**返回值**：对象的内存地址

### 3.4 `bytes_at`

```python
uctypes.bytes_at(addr, size)
```

捕获给定地址和大小的内存，返回不可变的 `bytes` 对象。

### 3.5 `bytearray_at`

```python
uctypes.bytearray_at(addr, size)
```

捕获给定地址和大小的内存，返回可变的 `bytearray` 对象。

### 3.6 `string_at`

```python
uctypes.string_at(addr, size=1048576)
```

从给定地址获取字符串，最大长度为指定的 `size`。

## 4. 常量定义

### 4.1 `uctypes.LITTLE_ENDIAN`

表示小端字节序布局类型。

### 4.2 `uctypes.BIG_ENDIAN`

表示大端字节序布局类型。

### 4.3 `uctypes.NATIVE`

表示本机字节序和对齐方式的布局类型。

### 4.4 整数类型

定义各种位数的整数类型，包括：

- `uctypes.UINT8`, `uctypes.INT8`
- `uctypes.UINT16`, `uctypes.INT16`
- `uctypes.UINT32`, `uctypes.INT32`
- `uctypes.UINT64`, `uctypes.INT64`

### 4.5 浮点数类型

- `uctypes.FLOAT32`, `uctypes.FLOAT64`

### 4.6 `uctypes.VOID`

用于表示空类型，常用于指针。

## 5. 结构描述符和结构对象实例化

可以通过结构描述符字典和布局类型，使用 `uctypes.struct()` 在指定内存地址上实例化结构对象。
