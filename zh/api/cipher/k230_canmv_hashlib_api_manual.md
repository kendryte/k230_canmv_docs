# `uhashlib` 模块 API 手册

## 概述

`uhashlib` 该模块实现了二进制数据哈希算法。可用算法的具体清单取决于主板。可能实现的算法包括：

- `SHA256` - 当前的现代哈希算法（ SHA2 系列）。适用于密码学安全用途。包含在 MicroPython 核心中，任何主板都建议提供该算法，除非它有特定的代码大小限制。
- `SHA1` - 一种上一代算法。不推荐用于新用途，但 SHA1 是某些互联网标准和现有应用程序的一部分，因此针对网络连接性和互操作性的板会尝试提供这个。
- `MD5` - 一种遗留算法，不被认为是加密安全的。只有少数针对与遗留应用程序互操作性的板会提供这个。

***具体请参考 MicroPython [hash 官方文档](https://docs.micropython.org/en/latest/library/hashlib.html)***

### 构造函数

#### sha256

**描述**

创建一个 SHA256 哈希器对象，并可选地将 `data` 输入到其中。

**语法**

```python
obj = uhashlib.sha256([data])
```

**参数**

| 参数名称 | 描述       | 输入/输出 |
|----------|------------|-----------|
| data (可选)     | 二进制数据 | 输入      |

**返回值**

返回 SHA256 哈希器对象。

#### sha1

**描述**

创建一个 SHA1 哈希器对象，并可选择将 `data` 输入到其中。

**语法**

```python
obj = uhashlib.sha1([data])
```

**参数**

| 参数名称 | 描述       | 输入/输出 |
|----------|------------|-----------|
| data (可选)     | 二进制数据 | 输入      |

**返回值**

返回 SHA1 哈希器对象。

#### md5

**描述**

创建一个 MD5 哈希器对象，并可选择将 `data` 输入到其中。

**语法**

```python
obj = uhashlib.md5([data])
```

**参数**

| 参数名称 | 描述       | 输入/输出 |
|----------|------------|-----------|
| data (可选)     | 二进制数据 | 输入      |

**返回值**

返回 MD5 哈希器对象。

### 哈希器对象方法

#### 数据更新函数 `update()`

**描述**

将更多二进制数据输入到哈希中。

**语法**

```python
hash.update(data)
```

**参数**

| 参数名称 | 描述       | 输入/输出 |
|----------|------------|-----------|
| data     | 二进制数据 | 输入      |

**返回值**

无

#### 消息摘要函数 `digest()`

**描述**

返回通过 hash 传递的所有数据的哈希值，作为一个 bytes 对象。

***注意：调用此方法后，无法再向哈希中输入更多数据。***

**语法**  

```python
dgst = hash.digest()
```

**参数**

无

**返回值**  

返回通过 hash 传递的所有数据的哈希值。

#### 十六进制消息摘要函数 `hexdigest()`

该方法未实现。可以使用 `binascii.hexlify(hash.digest())` 达到类似效果。

## 示例程序

```python
import uhashlib

print('###################### SHA256 Test ##############################')
print('********************** Test-1: Only Call update() Once ******************')
# 初始化sha256对象
obj = uhashlib.sha256()
# 输入消息message
msg = b'\x45\x11\x01\x25\x0e\xc6\xf2\x66\x52\x24\x9d\x59\xdc\x97\x4b\x73\x61\xd5\x71\xa8\x10\x1c\xdf\xd3\x6a\xba\x3b\x58\x54\xd3\xae\x08\x6b\x5f\xdd\x45\x97\x72\x1b\x66\xe3\xc0\xdc\x5d\x8c\x60\x6d\x96\x57\xd0\xe3\x23\x28\x3a\x52\x17\xd1\xf5\x3f\x2f\x28\x4f\x57\xb8'
# 标准哈希值
dgst0 = b'\x1a\xaa\xf9\x28\x5a\xf9\x45\xb8\xa9\x7c\xf1\x4f\x86\x9b\x18\x90\x14\xc3\x84\xf3\xc7\xc2\xb7\xd2\xdf\x8a\x97\x13\xbf\xfe\x0b\xf1'
# 将消息更新到硬件IP中
obj.update(msg)
# 计算哈希值
dgst = obj.digest()
print(dgst0 == dgst)
# print(binascii.hexlify(dgst))
print('********************** Test-2: Call update() Twice ******************')
dgst0 = b'\x93\x6a\x18\x5c\xaa\xa2\x66\xbb\x9c\xbe\x98\x1e\x9e\x05\xcb\x78\xcd\x73\x2b\x0b\x32\x80\xeb\x94\x44\x12\xbb\x6f\x8f\x8f\x07\xaf'
obj = uhashlib.sha256()
# 向硬件多次更新消息
obj.update(b'hello')
obj.update(b'world')
dgst = obj.digest()
print(dgst0 == dgst)
# print('********************** Test-3: Call digest() Twice ******************')
# dgst0 = b'\x93\x6a\x18\x5c\xaa\xa2\x66\xbb\x9c\xbe\x98\x1e\x9e\x05\xcb\x78\xcd\x73\x2b\x0b\x32\x80\xeb\x94\x44\x12\xbb\x6f\x8f\x8f\x07\xaf'
# obj = uhashlib.sha256()
# obj.update(b'hello')
# obj.update(b'world')
# dgst = obj.digest()
# dgst1 = obj.digest() # 错误，digest() 只能调用一次
# print(dgst0 == dgst)
# print(dgst == dgst1)
```
