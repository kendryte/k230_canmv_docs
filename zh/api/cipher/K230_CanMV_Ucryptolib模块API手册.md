# 1.1 Ucryptolib 模块 API 手册

## 1. 概述

`Ucryptolib` 库提供了以下加解密功能：AES-ECB、AES-CBC、AES-CTR、AES-GCM 以及 SM4。其中，AES-ECB、AES-CBC 和 AES-CTR 模式由 MicroPython 的软件库原生实现，而 AES-GCM 和 SM4 则通过底层硬件加速器进行加速。

***注意：本文档不详细介绍 AES-ECB、AES-CBC 和 AES-CTR 模式的加解密步骤，相关信息请参考 MicroPython 的 [cryptolib 官方文档](https://docs.micropython.org/en/latest/library/cryptolib.html)。***

## 2. API 介绍

`Ucryptolib` 库提供了两个主要类：`aes` 和 `sm4`，这两个类分别实现了加密 (`encrypt`) 和解密 (`decrypt`) 操作。

### 2.1 类 `aes`

**描述**

类 `aes` 用于初始化一个 AES-GCM 加解密对象，支持执行加密和解密操作。在 AES-GCM 加解密算法中，初始化时必须指定密钥 (`key`)、模式 (`mode`)、初始化向量 (`IV`) 和附加认证数据 (`AAD`)。

***注意：初始化后，加密或解密对象只能用于单一操作，即加密或解密，不支持同时用于两者。***

**语法**

```python
ucryptolib.aes((key, mode, IV, AAD))
```

**参数**

| 参数名称 | 描述                                                       | 输入/输出 |
| -------- | ---------------------------------------------------------- | --------- |
| key      | 加解密密钥，支持长度为 256 比特的密钥                       | 输入      |
| mode     | 加解密模式，支持的模式为 AES-GCM，设置 `mode=0` 即可        | 输入      |
| IV       | 初始化向量，长度为 12 字节                                  | 输入      |
| AAD      | 附加认证数据，用于验证数据完整性，支持的长度为任意          | 输入      |

**示例**

```python
import ucryptolib

# 初始化AES-GCM对象
cipher = ucryptolib.aes(key, mode=0, IV=iv, AAD=aad)

# 执行加密操作
ciphertext = cipher.encrypt(plaintext)

# 执行解密操作
decrypted_text = cipher.decrypt(ciphertext)
```

### 2.2 类 `sm4`

**描述**

类 `sm4` 用于初始化一个 SM4 加解密对象，支持中国国家密码算法标准 SM4 的加密和解密操作。与 AES-GCM 相似，SM4 初始化时需要提供密钥 (`key`)、模式 (`mode`) 和初始化向量 (`IV`)。

**语法**

```python
ucryptolib.sm4((key, mode, IV))
```

**参数**

| 参数名称 | 描述                                                       | 输入/输出 |
| -------- | ---------------------------------------------------------- | --------- |
| key      | SM4 加解密密钥，支持的密钥长度为 128 比特                    | 输入      |
| mode     | 加解密模式，支持 ECB（电子密码本）和 CBC（加密块链）模式      | 输入      |
| IV       | 初始化向量，长度为 16 字节，CBC 模式下必须提供                | 输入      |

**示例**

```python
import ucryptolib

# 初始化SM4对象
cipher = ucryptolib.sm4(key, mode=1, IV=iv)

# 执行加密操作
ciphertext = cipher.encrypt(plaintext)

# 执行解密操作
decrypted_text = cipher.decrypt(ciphertext)
```
