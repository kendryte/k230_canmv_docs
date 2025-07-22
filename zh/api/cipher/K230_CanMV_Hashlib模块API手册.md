# `Hashlib` 模块 API 手册

## 概述

`uhashlib` 库提供了基于 MD5、SHA1 和 SHA2 算法的二进制数据哈希功能。

## API 介绍

`uhashlib` 库提供了三个类：`md5`、`sha1` 和 `sha256`。这些类分别实现了两个函数：数据更新函数 `update()` 和消息摘要函数 `digest()`。其中，`md5` 和 `sha1` 是 MicroPython 的软件实现；`sha256` 则由底层硬件加速器加速。

***注意：本文档不详细介绍 `md5` 和 `sha1` 的使用步骤，具体请参考 MicroPython [hash 官方文档](https://docs.micropython.org/en/latest/library/hashlib.html)***

### 类 `sha256`

**描述**

`sha256` 类用于创建一个 SHA256 哈希对象，并可选择性地向其中发送数据。

**语法**  

```python
uhashlib.sha256([data])
```

**参数**  

| 参数名称 | 描述       | 输入/输出 |
|----------|------------|-----------|
| data (可选) | 二进制数据 | 输入      |

**返回值**  

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非 0   | 失败   |

**示例**  

```python
data = bytes([0]*64)
hash_obj = uhashlib.sha256(data)
hash_obj.update(data)
dgst = hash_obj.digest()
print(dgst)
```

#### 数据更新函数 `update()`

**描述**

如果需要多次输入二进制数据，可以调用 `update()` 函数更新数据。

**语法**

```python
obj.update(data)
```

**参数**

| 参数名称 | 描述       | 输入/输出 |
|----------|------------|-----------|
| data     | 输入二进制数据 | 输入      |

**返回值**

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非 0   | 失败   |

#### 消息摘要函数 `digest()`

**描述**
返回所有输入数据的哈希值。

***注意：在 MicroPython 中，使用此函数会完成最后的计算，而不仅仅是显示结果。因此只能调用一次，如果需要多次使用该值，请保存到变量中。***

**语法**  

```python
dgst = hash.digest()
print(dgst)

/*********** 注意 ***********/
a = hash.digest()
b = hash.digest() # 错误
```

**参数**

无

**返回值**  

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非 0   | 失败   |

#### 十六进制消息摘要函数 `hexdigest()`

该方法未实现。可以使用 `binascii.hexlify(hash.digest())` 达到类似效果。

## 示例程序

### 计算哈希值

```python
import uhashlib
import binascii

# 初始化 sha256 对象
obj = uhashlib.sha256()
# 输入数据1
obj.update(b'hello')
# 输入数据2
obj.update(b'world')
# 计算摘要
dgst = obj.digest()
print(binascii.hexlify(dgst))
# b'936a185caaa266bb9cbe981e9e05cb78cd732b0b3280eb944412bb6f8f8f07af'
```
