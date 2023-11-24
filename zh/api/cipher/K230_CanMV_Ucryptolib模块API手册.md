# K230 CanMV Ucryptolib 模块API手册

![cover](images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍 CanMV 项目中加解密算法库-ucryptolib。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| AES  | Advanced Encryption Standard   |
| GCM  | Galois/Counter Mode   |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 杨帆      | 2023-09-15 |
| V1.1       | 修改示例程序，新增使用指南         |        杨帆    |     2023-10-10       |
| V1.2       | 增加 AES-ECB/CBC/CTR 软件源生实现    |   杨帆     |   2023-10-13         |

## 1. 概述

Ucryptolib 库提供了 AES-ECB/CBC/CTR、AES-GCM、SM4 加解密功能。其中，AES-ECB/CBC/CTR 三种模式是由 micropython 的软件源生实现，AES-GCM 和 SM4 由底层硬件加速器进行加速。

***注意：本文档不会介绍 AES-ECB/CBC/CTR 三种模式的加解密详细步骤，具体请参考 micropython [cryptolib官方文档](https://docs.micropython.org/en/latest/library/cryptolib.html)***

## 2. API描述

Ucryptolib 库提供了两个类，分别是 aes 和 sm4，它们分别实现了两个函数，加密 encrypt() 和解密 decrypt()。

### 2.1 类 aes

【描述】

类 aes 用于初始化一个 AES-GCM 国际加解密对象，从而完成加密/解密操作。同时，在 AES-GCM 加解密算法中，初始化时必须输入 key、mode、IV 和 AAD。

***注意：初始化后，加解密对象只能用于加密或解密操作，不允许创建一个密码对象同时用于加密、解密操作***

【语法】

```python
ucryptolib.aes((key, mode, IV, AAD))
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| key  | 加解密密钥，支持的密钥长度为 256 bits           | 输入      |
| mode  | 加解密模式，支持的加解密模式为 AES-GCM，这里设置 mode=0 即可            | 输入      |
| IV  | 初始化向量，支持的 IV 长度为 12 bytes            | 输入      |
| AAD  | 附加数据            | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

```python
/**********encrypt************/
key = b'\x24\x50\x1a\xd3\x84\xe4\x73\x96\x3d\x47\x6e\xdc\xfe\x08\x20\x52\x37\xac\xfd\x49\xb5\xb8\xf3\x38\x57\xf8\x11\x4e\x86\x3f\xec\x7f'
iv = b'\x9f\xf1\x85\x63\xb9\x78\xec\x28\x1b\x3f\x27\x94'
aad = b'\xad\xb5\xec\x72\x0c\xcf\x98\x98\x50\x00\x28\xbf\x34\xaf\xcc\xbc\xac\xa1\x26\xef'
pt = b'\x27'

crypto = ucryptolib.aes(key, 0, iv, aad)
inbuf = pt
outbuf = bytearray(17)
crypto.encrypt(inbuf, outbuf)

/**********decrypt************/
ct = b'\xeb'
tag = b'\x63\x35\xe1\xd4\x9e\x89\x88\xea\xc4\x8e\x42\x19\x4e\x5f\x56\xdb'
crypto = ucryptolib.aes(key, 0, iv, aad)
inbuf = ct + tag
outbuf = bytearray(1)
crypto.decrypt(inbuf, outbuf)
```

【相关主题】

无

#### 2.1.1 加密函数 encrypt()

【描述】

对输入数据进行加密运算。输入数据存放在 inbuf 中，加密结果将存储到输出缓冲区 outbuf 中，如果：

1. 没有给定 outbuf，加密函数 encrypt() 将返回一个 bytes 类型的对象；
1. 如果给定 outbuf 且 outbuf = inbuf，数据将被就地加密。

【语法】

```python
crypto.encrypt(inbuf[, outbuf])
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| inbuf  | 输入缓冲区，存放待加密的明文数据            | 输入      |
| outbuf(可选)  | 输出缓冲区，存放加密完成的密文数据       | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

加密后返回的数据(密文数据)格式为：密文 + TAG，TAG 长度固定为 16 bytes。

【举例】

无

【相关主题】

无

#### 2.1.2 解密函数 decrypt()

【描述】

对输入数据进行解密运算。输入数据存放在 inbuf 中，解密结果将存储到输出缓冲区 outbuf 中，如果：

1. 没有给定 outbuf，解密函数 decrypt() 将返回一个 bytes 类型的对象；
1. 如果给定 outbuf 且 outbuf = inbuf，数据将被就地解密。

【语法】

```python
crypto.decrypt(inbuf[, outbuf])
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| inbuf  | 输入缓冲区，存放待解密的密文数据            | 输入      |
| outbuf(可选)  | 输出缓冲区，存放解密完成的明文数据       | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

解密后返回的数据(明文数据)格式为：明文。

【举例】

无

【相关主题】

无

### 2.2 类 sm4

【描述】

类 sm4 用于初始化一个国密加解密对象，从而完成加密/解密操作。

***注意：初始化后，加解密对象只能用于加密或解密操作，不允许创建一个密码对象同时用于加密、解密操作***

【语法】

```python
ucryptolib.sm4((key, mode[, IV]))
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| key  | 加解密密钥，支持的密钥长度为 128 bits            | 输入      |
| mode  | 加解密模式，支持的模式有 ecb/cbc/cfb/ofb/ctr，mode 分别为 1/2/3/5/6           | 输入      |
| IV(可选)  | 初始化向量，支持的 IV 长度为 20 bytes            | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

```python
/**********encrypt************/
key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10'
iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
pt = b'\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb\xcc\xcc\xcc\xcc\xdd\xdd\xdd\xdd\xee\xee\xee\xee\xff\xff\xff\xff\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb'
crypto = ucryptolib.sm4(key, 2, iv)
inbuf = pt
outbuf = bytearray(32)
crypto.encrypt(inbuf, outbuf)

/**********decrypt************/
ct = b'\x78\xeb\xb1\x1c\xc4\x0b\x0a\x48\x31\x2a\xae\xb2\x04\x02\x44\xcb\x4c\xb7\x01\x69\x51\x90\x92\x26\x97\x9b\x0d\x15\xdc\x6a\x8f\x6d'
crypto = ucryptolib.sm4(key, 2, iv)
inbuf = ct
outbuf = bytearray(32)
crypto.decrypt(inbuf, outbuf)
```

【相关主题】

无

#### 2.2.1 加密函数 encrypt()

【描述】

对输入数据进行加密运算。输入数据存放在 inbuf 中，加密结果将存储到输出缓冲区 outbuf 中，如果：

1. 没有给定 outbuf，加密函数 encrypt() 将返回一个 bytes 类型的对象；
1. 如果给定 outbuf 且 outbuf = inbuf，数据将被就地加密。

【语法】

```python
crypto.encrypt(inbuf[, outbuf])
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| inbuf  | 输入缓冲区，存放待加密的明文数据            | 输入      |
| outbuf(可选)  | 输出缓冲区，存放加密完成的密文数据       | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

无

【相关主题】

无

#### 2.2.2 解密函数 decrypt()

【描述】

对输入数据进行解密运算。输入数据存放在 inbuf 中，解密结果将存储到输出缓冲区 outbuf 中，如果：

1. 没有给定 outbuf，解密函数 decrypt() 将返回一个 bytes 类型的对象；
1. 如果给定 outbuf 且 outbuf = inbuf，数据将被就地解密。

【语法】

```python
crypto.decrypt(inbuf[, outbuf])
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| inbuf  | 输入缓冲区，存放待解密的密文数据            | 输入      |
| outbuf(可选)  | 输出缓冲区，存放解密完成的明文数据       | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

无

【相关主题】

无

## 3. 示例程序

### 3.1 aes 加解密

```python
/********** AES-GCM encrypt ************/
import ucryptolib

# key(256 bytes)
key = b'\x24\x50\x1a\xd3\x84\xe4\x73\x96\x3d\x47\x6e\xdc\xfe\x08\x20\x52\x37\xac\xfd\x49\xb5\xb8\xf3\x38\x57\xf8\x11\x4e\x86\x3f\xec\x7f'
# iv(12 bytes)
iv = b'\x9f\xf1\x85\x63\xb9\x78\xec\x28\x1b\x3f\x27\x94'
# aad(20 bytes)
aad = b'\xad\xb5\xec\x72\x0c\xcf\x98\x98\x50\x00\x28\xbf\x34\xaf\xcc\xbc\xac\xa1\x26\xef'
# plaintext(51 bytes)
pt = b'\x27\xf3\x48\xf9\xcd\xc0\xc5\xbd\x5e\x66\xb1\xcc\xb6\x3a\xd9\x20\xff\x22\x19\xd1\x4e\x8d\x63\x1b\x38\x72\x26\x5c\xf1\x17\xee\x86\x75\x7a\xcc\xb1\x58\xbd\x9a\xbb\x38\x68\xfd\xc0\xd0\xb0\x74\xb5\xf0\x1b\x2c'
ct = b'\xeb\x7c\xb7\x54\xc8\x24\xe8\xd9\x6f\x7c\x6d\x9b\x76\xc7\xd2\x6f\xb8\x74\xff\xbf\x1d\x65\xc6\xf6\x4a\x69\x8d\x83\x9b\x0b\x06\x14\x5d\xae\x82\x05\x7a\xd5\x59\x94\xcf\x59\xad\x7f\x67\xc0\xfa\x5e\x85\xfa\xb8'
tag = b'\xbc\x95\xc5\x32\xfe\xcc\x59\x4c\x36\xd1\x55\x02\x86\xa7\xa3\xf0'
# init cipher object(aes-gcm)
crypto = ucryptolib.aes(key, 0, iv, aad)
inbuf = pt
# outbuf = ciphertext + tag
outbuf = bytearray(67)
crypto.encrypt(inbuf, outbuf).hex(' ')

/********** AES-GCM decrypt ************/
crypto = ucryptolib.aes(key, 0, iv, aad)
# ciphertext + tag
inbuf = ct + tag
outbuf = bytearray(51)
crypto.decrypt(inbuf, outbuf).hex(' ')
```

### 3.2 sm4 加解密

```python
import ucryptolib

/********** SM4-ECB encrypt ************/
# key(128 bits)
key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10'
iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
# plaintext(32 bytes)
pt = b'\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb\xcc\xcc\xcc\xcc\xdd\xdd\xdd\xdd\xee\xee\xee\xee\xff\xff\xff\xff\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb'
ct = b'\x5e\xc8\x14\x3d\xe5\x09\xcf\xf7\xb5\x17\x9f\x8f\x47\x4b\x86\x19\x2f\x1d\x30\x5a\x7f\xb1\x7d\xf9\x85\xf8\x1c\x84\x82\x19\x23\x04'
# init cipher object(sm4-ebc)
crypto = ucryptolib.sm4(key, 1)
inbuf = pt
outbuf = bytearray(32)
crypto.encrypt(inbuf, outbuf).hex(' ')

/********** SM4-EBC decrypt ************/
# init cipher object(aes-ebc)
crypto = ucryptolib.sm4(key, 1)
inbuf = ct
outbuf = bytearray(32)
crypto.decrypt(inbuf, outbuf).hex(' ')
```

## 4. 使用指南

截止到当前版本，ucryptolib 库已经测试了下列 case。测试程序参考 *./tests/cipher/cipher.py*，启动 canmv 开发板，进入 REPL 之后，通过命令 **import sdcard.app.tests.cipher.cipher** 可直接运行测试 demo。

| 类  | 方法  | 测试 case | 测试结果 |
|---------|--------|------------------------------------|-----------------|
| aes-gcm       | encrypt / decrypt  | ivlen=12, ptlen=0, aadlen=0   | pass |
|           |           | ivlen=12, ptlen=1, aadlen=20   | pass |
|           |           | ivlen=12, ptlen=51, aadlen=0   | pass |
|           |           | ivlen=12, ptlen=51, aadlen=20   | pass |
| sm4-ecb    | encrypt / decrypt | keybits=128, ptlen=32 | pass |
| sm4-cbc    | encrypt / decrypt | keybits=128, ivlen=16, ptlen=32 | pass |
| sm4-cfb    | encrypt / decrypt | keybits=128, ivlen=16, ptlen=32 | pass |
| sm4-ofb    | encrypt / decrypt | keybits=128, ivlen=16, ptlen=32 | pass |
| sm4-ctr    | encrypt / decrypt | keybits=128, ivlen=16, ptlen=64 | pass |
