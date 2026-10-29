# `uhashlib` Module API Manual

## Overview

The `uhashlib` module implements binary data hashing algorithms. The specific list of available algorithms depends on the board. Possible algorithms include:

- `SHA256` - The current modern hash algorithm (SHA2 family). Suitable for cryptographically secure purposes. Included in the MicroPython core, and any board is recommended to provide this algorithm unless it has specific code size constraints.
- `SHA1` - A previous-generation algorithm. Not recommended for new uses, but SHA1 is part of some internet standards and existing applications, so boards targeting network connectivity and interoperability will try to provide this.
- `MD5` - A legacy algorithm not considered cryptographically secure. Only a few boards targeting interoperability with legacy applications will provide this.

***Please refer to the MicroPython [official hash documentation](https://docs.micropython.org/en/latest/library/hashlib.html) for details***

### Constructor

#### sha256

**Description**

Creates a SHA256 hash object, and optionally feeds `data` into it.

**Syntax**

```python
obj = uhashlib.sha256([data])
```

**Parameters**

| Parameter | Description | Input/Output |
|----------|------------|-----------|
| data (optional)     | Binary data | Input      |

**Return Value**

Returns the SHA256 hash object.

#### sha1

**Description**

Creates a SHA1 hash object, and optionally feeds `data` into it.

**Syntax**

```python
obj = uhashlib.sha1([data])
```

**Parameters**

| Parameter | Description | Input/Output |
|----------|------------|-----------|
| data (optional)     | Binary data | Input      |

**Return Value**

Returns the SHA1 hash object.

#### md5

**Description**

Creates an MD5 hash object, and optionally feeds `data` into it.

**Syntax**

```python
obj = uhashlib.md5([data])
```

**Parameters**

| Parameter | Description | Input/Output |
|----------|------------|-----------|
| data (optional)     | Binary data | Input      |

**Return Value**

Returns the MD5 hash object.

### Hasher Object Methods

#### Data Update Function `update()`

**Description**

Inputs more binary data into the hash.

**Syntax**

```python
hash.update(data)
```

**Parameters**

| Parameter | Description  | Input/Output |
|----------|------------|-----------|
| data     | Binary data | Input      |

**Return Value**

None

#### Message Digest Function `digest()`

**Description**

Returns the hash value of all data passed through the hash as a bytes object.

***Note: After calling this method, no more data can be input into the hash.***

**Syntax**  

```python
dgst = hash.digest()
```

**Parameters**

None

**Return Value**  

Returns the hash value of all data passed through the hash.

#### Hexadecimal Message Digest Function `hexdigest()`

This method is not implemented. You can use `binascii.hexlify(hash.digest())` to achieve a similar effect.

## Example Program

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
