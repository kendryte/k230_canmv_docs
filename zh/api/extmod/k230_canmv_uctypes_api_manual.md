# `uctypes` 模块 API 手册

## 概述

该模块提供一种以结构化方式访问二进制数据的方法。它是 MicroPython 中的“外部数据接口”模块，概念上类似于 CPython 的 `ctypes` 模块，但 API 经过简化和优化，适合嵌入式系统的需求。通过定义与 C 语言类似的数据结构布局，用户可以使用点语法来访问其中的子字段。

***具体请参考 MicroPython [uctypes 官方文档](https://docs.micropython.org/en/latest/library/uctypes.html#module-uctypes)***

> **警告**
>
> `uctypes` 模块允许访问机器的任意内存地址（包括 I/O 和控制寄存器）。不慎使用可能导致系统崩溃、数据丢失，甚至硬件损坏。
>
> **也可参考 `ustruct` 模块**
>
> `ustruct` 模块是 Python 中处理二进制数据的标准方式，适合处理简单的数据结构，但不适用于复杂、嵌套的结构。

## 结构说明

### 示例

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

### 结构布局定义

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

即，值是一个2元组，第一个元素是一个偏移量，第二个是一个结构描述符字典（注意：递归描述符中的偏移量是相对于它所定义的结构）。当然，递归结构不仅可以通过字面量字典指定，还可以通过引用先前定义的结构描述符字典的名称来指定。

- **基本类型数组**：

```python
"arr": (offset | uctypes.ARRAY, size | uctypes.UINT8)
```

即，值是一个 2 元组，第一个元素是 `ARRAY` 标志与偏移量按位或，第二个是标量元素类型与数组中元素数量的按位或数。

- **聚合类型的数组**：

```python
"arr2": (offset | uctypes.ARRAY, size, {"b": 0 | uctypes.UINT8})
```

即，值是一个 3 元组，第一个元素是 `ARRAY` 标志与偏移量按位或的结果，第二个元素是数组中的元素数量，第三个元素是元素类型的描述符。

- **指向基本类型的指针**：

```python
"ptr": (offset | uctypes.PTR, uctypes.UINT8)
```

即，值是一个 2 元组，第一个元素是 `PTR` 标志与偏移量进行按位或运算的结果，第二个元素是标量元素类型。

- **指向聚合类型的指针**：

```python
"ptr2": (offset | uctypes.PTR, {"b": 0 | uctypes.UINT8})
```

即，值是一个 2 元组，第一个元素是 `PTR` 标志与偏移量进行按位或运算的结果，第二个元素是指向的类型描述符。

- **位域**：

```python
"bitf0": offset | uctypes.BFUINT16 | lsbit << uctypes.BF_POS | bitsize << uctypes.BF_LEN
```

即，`value` 是一个包含给定位字段的标量值类型（类型名称类似于标量类型，但以 `BF` 为前缀），与包含位字段的标量值的偏移量进行按位或运算，并进一步与位字段在标量值中的位置和长度值进行按位或运算，分别通过 `BF_POS` 和 `BF_LEN` 位进行移位。位字段的位置从标量的最低有效位（位置为 `0`）开始计数，并且是字段最右边的位数（换句话说，它是标量需要右移的位数以提取位字段）。

在上述示例中，首先将在偏移量 `0` 处提取一个 `UINT16` 值（当访问硬件寄存器时，这一细节可能很重要，因为需要特定的访问大小和对齐方式），然后提取一个位域，其最右边的一位是此 `UINT16` 的 `lsbit` 位，长度为 `bitsize` 位。例如，如果 `lsbit` 为 `0`， `bitsize` 为 `8` 时，实际上它将访问 `UINT16` 的最低有效字节。

请注意，位域操作与目标字节序无关，特别是上述示例将访问 `UINT16` 的最小有效字节，无论结构是小端还是大端。但这取决于最小有效位编号为 `0`。某些目标可能在其原生 ABI 中使用不同的编号方式，但 `uctypes` 始终使用上述描述的标准化编号。

## API 介绍

### `struct` 类

```python
class uctypes.struct(addr, descriptor, layout_type=NATIVE)
```

根据内存地址、描述符和布局类型来实例化一个结构对象。

**参数**：

- `addr`: 内存地址
- `descriptor`: 结构描述符（字典）
- `layout_type`: 可选，默认为 `NATIVE`（本机字节序）（见下文）

**返回值**：返回结构对象

### `sizeof`

```python
uctypes.sizeof(struct, layout_type=NATIVE)
```

返回数据结构的大小（以字节为单位）。struct 参数可以是结构类或特定的实例化结构对象（或其聚合字段）。

**参数**：

- `struct`: 结构类或实例
- `layout_type`: 可选，默认为 `NATIVE`（见下文）。

**返回值**：结构的大小

### `addressof`

```python
uctypes.addressof(obj)
```

返回对象的内存地址。

**参数**：

- `obj`: 支持缓冲区协议的对象

**返回值**：对象的内存地址

### `bytes_at`

```python
uctypes.bytes_at(addr, size)
```

捕获给定地址和大小的内存，返回不可变的 `bytes` 对象。

### `bytearray_at`

```python
uctypes.bytearray_at(addr, size)
```

捕获给定地址和大小的内存，返回可变的 `bytearray` 对象。

### `string_at`

```python
uctypes.string_at(addr, size=1048576)
```

从给定地址获取字符串，最大长度为指定的 `size`。

## 常量定义

### `uctypes.LITTLE_ENDIAN`

表示小端字节序布局类型。

### `uctypes.BIG_ENDIAN`

表示大端字节序布局类型。

### `uctypes.NATIVE`

表示本机字节序和对齐方式的布局类型。

### 整数类型

定义各种位数的整数类型，包括：

- `uctypes.UINT8`, `uctypes.INT8`
- `uctypes.UINT16`, `uctypes.INT16`
- `uctypes.UINT32`, `uctypes.INT32`
- `uctypes.UINT64`, `uctypes.INT64`

### 浮点数类型

- `uctypes.FLOAT32`, `uctypes.FLOAT64`

### `uctypes.VOID`

用于表示空类型，常用于指针。

### `uctypes.PTR` `uctypes.ARRAY`

指针和数组的类型常量。注意结构体没有显式的常量，它是隐式的：一个没有 `PTR` 或 `ARRAY` 标志的聚合类型是结构体。

## 结构描述符和结构对象实例化

可以通过结构描述符字典和布局类型，使用 `uctypes.struct()` 在指定内存地址上实例化结构对象。
