# `Ucryptolib` 模块 API 手册

## 概述

`Ucryptolib` 库提供了以下加解密功能：AES-ECB、AES-CBC、AES-CTR。

***相关信息请参考 MicroPython 的 [cryptolib 官方文档](https://docs.micropython.org/en/latest/library/cryptolib.html)。***

## API 介绍

`Ucryptolib` 库提供了`aes` 类，实现了加密 (`encrypt`) 和解密 (`decrypt`) 操作。

### 类 `aes`

#### 构造函数

**描述**

初始化加密算法对象，适用于加密/解密。

***注意：初始化后，加密算法对象只能用于加密或解密。在加密操作后运行解密操作，或反之，均不受支持。***

**语法**

```python
ucryptolib.aes(key, mode[, IV])
```

**参数**

- **key** : 加密/解密密钥（字节类）。
- **mode** :
  - `1` 用于电子密码本（ECB）。
  - `2` 用于密码块链接（CBC）。
  - `6` 用于计数器模式（CTR）。
- **IV** : `CBC` 模式下的初始化向量。对于计数器模式，`IV` 是计数器的初始值。

#### encrypt 加密方法

**描述**

加密 `in_buf` 。如果没有给出 `out_buf` ，结果将作为新分配的 `bytes 对象` 返回。否则，结果将写入可变缓冲区 `out_buf` 。 `in_buf` 和 `out_buf` 也可以引用同一个可变缓冲区，在这种情况下，数据将原地加密。

**语法**

```python
enc = aes.encrypt(in_buf[, out_buf])
```

#### decrypt 解密

**描述**

与 `encrypt()` 类似，但用于解密。

**语法**

```python
dec = aes.decrypt(in_buf[, out_buf])
```

**示例**

```python
from ucryptolib import aes
# ECB mode
crypto = aes(b"1234" * 4, 1)
enc = crypto.encrypt(bytes(range(32)))
print(enc)
crypto = aes(b"1234" * 4, 1)
print(crypto.decrypt(enc))
```
