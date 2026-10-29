# `Ucryptolib` Module API Manual

## Overview

The `Ucryptolib` library provides the following encryption and decryption functionalities: AES-ECB, AES-CBC, AES-CTR.

***For related information, please refer to MicroPython's [cryptolib official documentation](https://docs.micropython.org/en/latest/library/cryptolib.html).***

## API Introduction

The `Ucryptolib` library provides the `aes` class, which implements encryption (`encrypt`) and decryption (`decrypt`) operations.

### Class `aes`

#### Constructor

**Description**

Initializes the encryption algorithm object, suitable for encryption/decryption.

***Note: After initialization, the encryption algorithm object can only be used for either encryption or decryption. Running a decryption operation after an encryption operation, or vice versa, is not supported.***

**Syntax**

```python
ucryptolib.aes(key, mode[, IV])
```

**Parameters**

- **key** : The encryption/decryption key (bytes-like object).
- **mode** :
  - `1` for Electronic Codebook (ECB).
  - `2` for Cipher Block Chaining (CBC).
  - `6` for Counter mode (CTR).
- **IV** : Initialization vector for `CBC` mode. For counter mode, `IV` is the initial value of the counter.

#### encrypt Method

**Description**

Encrypts `in_buf`. If `out_buf` is not given, the result is returned as a newly allocated `bytes object`. Otherwise, the result is written into the mutable buffer `out_buf`. `in_buf` and `out_buf` can also refer to the same mutable buffer, in which case the data is encrypted in place.

**Syntax**

```python
enc = aes.encrypt(in_buf[, out_buf])
```

#### decrypt Method

**Description**

Similar to `encrypt()`, but used for decryption.

**Syntax**

```python
dec = aes.decrypt(in_buf[, out_buf])
```

**Example**

```python
from ucryptolib import aes
# ECB mode
crypto = aes(b"1234" * 4, 1)
enc = crypto.encrypt(bytes(range(32)))
print(enc)
crypto = aes(b"1234" * 4, 1)
print(crypto.decrypt(enc))
```
