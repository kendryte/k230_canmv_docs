# K230 CanMV Hashlib 模块API手册

![cover](../images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍 CanMV 项目中加解密算法库-uhashlib。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| SHA1  | Secure Hash Algorithm 1   |
| SHA2  | Secure Hash Algorithm 2   |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 杨帆      | 2023-09-15 |
| V1.1       | 修改示例程序，新增使用指南         |        杨帆    |     2023-10-10       |
| V1.2       | 增加 SHA1 和 MD5 软件源生实现         |      杨帆      |   2023-10-13    |

## 1. 概述

Uhashlib 库提供了基于 MD5、SHA1、SHA2 二进制数据的哈希算法。

## 2. API描述

Uhashlib 库提供了三个类：md5、sha1 和 sha256，这些类分别实现了两个函数，数据更新函数 update()，消息摘要函数 digest()。其中，md5 和 sha1 是 micropython 的软件源生实现；sha256 由底层硬件加速器进行加速。

***注意：本文档不会介绍 md5 和 sha1 详细步骤，具体请参考 micropython [hash官方文档] <https://docs.micropython.org/en/latest/library/hashlib.html>***

### 2.1 类 sha256

【描述】

类 sha256 用于创建一个 SHA256 哈希对象，并有选择地向其中发送数据。

【语法】

```python
uhashlib.sha256([data])
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| data(可选)  | 二进制数据            | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

无

【举例】

```python
data = bytes([0]*64)
hash_obj = uhashlib.sha256(data)
hash_obj.update(data)
dgst = hash_obj.digest()
print(dgst)
```

【相关主题】

无

#### 2.1.1 数据更新函数 update()

【描述】

如果需要多次输入二进制数据，可以调用 update() 函数更新数据。

【语法】

```python
obj.update(data)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| data  | 输入二进制数据            | 输入      |

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

#### 2.1.2 消息摘要函数 digest()

【描述】

返回所有输入数据的哈希值。

***注意：在micropython中，使用此函数会完成最后的计算，不是单纯的将结果显示出来，所以只能调用一次，如果要多次使用该值，请保存到变量中。***

【语法】

```python
dgst = hash.digest()
print(dgst)

/*********** note ***********/
a = hash.digest()
b = hash.digest() # Error
```

【参数】

无

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

#### 2.1.3 十六进制消息摘要函数 hexdigest()

该方法未实现。使用 binascii.hexlify(hash.digest()) 可以达到类似的效果。

## 3. 示例程序

### 计算 hash 值

```python
import uhashlib
import binascii

# init sha256 obj
obj = uhashlib.sha256()
# input data1
obj.update(b'hello')
# input data2
obj.update(b'world')
# compute digest
dgst = obj.digest()
print(binascii.hexlify(dgst))
# b'936a185caaa266bb9cbe981e9e05cb78cd732b0b3280eb944412bb6f8f8f07af'
```

## 4. 使用指南

截止到当前版本，uhashlib 库已经测试了下列 case。测试程序参考 *./tests/cipher/cipher.py*，启动 canmv 开发板，进入 REPL 之后，通过命令 **import sdcard.app.tests.cipher.cipher** 可直接运行测试 demo。

| 类  | 测试 case | 测试结果 |
|--------|------------------------------------|-----------------|
| uhashlib | 调用一次 update() 更新数据   | pass |
| uhashlib | 调用多次 update() 更新数据   | pass |
