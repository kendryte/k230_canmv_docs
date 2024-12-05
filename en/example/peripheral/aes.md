# 13. Explanation of AES Routines

## 1. Overview

The K230 comes with a built-in cryptographic algorithm accelerator that supports AES and SM4 national cryptographic algorithms for encryption and decryption operations.

## 2. Examples

### 2.1 AES-GCM Example

This example demonstrates AES-GCM encryption and decryption computations.

```python
print('\n###################### AES-GCM Test ##############################')
import ucryptolib
import collections

# Create a named tuple
Aes = collections.namedtuple('Aes', ['key', 'iv', 'aad', 'pt', 'ct', 'tag'])
aes = [
    Aes(b'\xb5\x2c\x50\x5a\x37\xd7\x8e\xda\x5d\xd3\x4f\x20\xc2\x25\x40\xea\x1b\x58\x96\x3c\xf8\xe5\xbf\x8f\xfa\x85\xf9\xf2\x49\x25\x05\xb4',
        b'\x51\x6c\x33\x92\x9d\xf5\xa3\x28\x4f\xf4\x63\xd7',
        b'',
        b'',
        b'',
        b'\xbd\xc1\xac\x88\x4d\x33\x24\x57\xa1\xd2\x66\x4f\x16\x8c\x76\xf0'
    ),
    # More AES test data...
]

# Test Case 1
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

# Other test cases...
```

### 2.2 SM4 Example

This example demonstrates encryption and decryption computations in SM4's ECB, CFB, OFB, CBC, and CTR modes.

```python
print('\n###################### SM4-ECB/CFB/OFB/CBC/CTR Test ##############################')
Sm4 = collections.namedtuple('Sm4', ['key', 'iv', 'pt', 'ct'])
sm4 = [
    Sm4(b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',
        None,
        b'\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb\xcc\xcc\xcc\xcc\xdd\xdd\xdd\xdd\xee\xee\xee\xee\xff\xff\xff\xff\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb',
        b'\x5e\xc8\x14\x3d\xe5\x09\xcf\xf7\xb5\x17\x9f\x8f\x47\x4b\x86\x19\x2f\x1d\x30\x5a\x7f\xb1\x7d\xf9\x85\xf8\x1c\x84\x82\x19\x23\x04'
    ),
    # More SM4 test data...
]

# Test Case 1
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

# Other test cases...
```

```{admonition} Tip
For specific interfaces of the AES module, please refer to the [API documentation](../../api/cipher/K230_CanMV_UcryptolibModuleAPI_manual.md)
```
