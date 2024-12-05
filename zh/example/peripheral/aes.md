# 13. AES 例程讲解

## 1. 概述

K230 内置加解密算法加速器，支持 AES 和 SM4 国密算法的加解密操作。

## 2. 示例

### 2.1 AES-GCM 示例

该示例演示了 AES-GCM 加解密计算。

```python
print('\n###################### AES-GCM Test ##############################')
import ucryptolib
import collections

# 创建一个具名元组
Aes = collections.namedtuple('Aes', ['key', 'iv', 'aad', 'pt', 'ct', 'tag'])
aes = [
    Aes(b'\xb5\x2c\x50\x5a\x37\xd7\x8e\xda\x5d\xd3\x4f\x20\xc2\x25\x40\xea\x1b\x58\x96\x3c\xf8\xe5\xbf\x8f\xfa\x85\xf9\xf2\x49\x25\x05\xb4',
        b'\x51\x6c\x33\x92\x9d\xf5\xa3\x28\x4f\xf4\x63\xd7',
        b'',
        b'',
        b'',
        b'\xbd\xc1\xac\x88\x4d\x33\x24\x57\xa1\xd2\x66\x4f\x16\x8c\x76\xf0'
    ),
    # 更多 AES 测试数据...
]

# 测试用例 1
print('********************** Test-1: ivlen=12, ptlen=0, aadlen=0 ******************')
print('GCM Encrypt......')
crypto = ucryptolib.aes(aes[0].key, 0, aes[0].iv, aes[0].aad)
inbuf = aes[0].pt
outbuf = bytearray(16)
val = crypto.encrypt(inbuf, outbuf)
val0 = aes[0].ct + aes[0].tag
print(val0 == val)

print('GCM Decrypt......')
crypto = ucryptolib.aes(aes[0].key, 0, aes[0].iv, aes[0].aad)
inbuf = aes[0].ct + aes[0].tag
val = crypto.decrypt(inbuf)
print(val[:1] == b'\x00')

# 其他测试用例...
```

### 2.2 SM4 示例

该示例演示了 SM4 的 ECB、CFB、OFB、CBC 和 CTR 模式加解密计算。

```python
print('\n###################### SM4-ECB/CFB/OFB/CBC/CTR Test ##############################')
Sm4 = collections.namedtuple('Sm4', ['key', 'iv', 'pt', 'ct'])
sm4 = [
    Sm4(b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',
        None,
        b'\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb\xcc\xcc\xcc\xcc\xdd\xdd\xdd\xdd\xee\xee\xee\xee\xff\xff\xff\xff\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb',
        b'\x5e\xc8\x14\x3d\xe5\x09\xcf\xf7\xb5\x17\x9f\x8f\x47\x4b\x86\x19\x2f\x1d\x30\x5a\x7f\xb1\x7d\xf9\x85\xf8\x1c\x84\x82\x19\x23\x04'
    ),
    # 更多 SM4 测试数据...
]

# 测试用例 1
print('********************** Test-1: keybits=128, ptlen=32 ******************')
print('SM4-ECB Encrypt......')
crypto = ucryptolib.sm4(sm4[0].key, 1)
inbuf = sm4[0].pt
outbuf = bytearray(32)
val = crypto.encrypt(inbuf, outbuf)
val0 = sm4[0].ct
print(val0 == val)

print('SM4-ECB Decrypt......')
crypto = ucryptolib.sm4(sm4[0].key, 1)
inbuf = sm4[0].ct
outbuf = bytearray(32)
val = crypto.decrypt(inbuf, outbuf)
val0 = sm4[0].pt
print(val0 == val)

# 其他测试用例...
```

```{admonition} 提示
AES 模块具体接口请参考 [API 文档](../../api/cipher/K230_CanMV_Ucryptolib模块API手册.md)
```
