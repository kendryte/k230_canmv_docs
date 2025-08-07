# `Ucryptolib` Module API Manual

## Overview

The `Ucryptolib` library provides the following encryption and decryption functionalities: AES-ECB, AES-CBC, AES-CTR.

***For related information, please refer to MicroPython's [official cryptolib documentation](https://docs.micropython.org/en/latest/library/cryptolib.html).***

## API Introduction

The `Ucryptolib` library provides the `aes` class, which implements encryption (`encrypt`) and decryption (`decrypt`) operations.

### Class `aes`

#### Constructor

**Description**

Initialize the encryption algorithm object, which is suitable for encryption/decryption.

***Note: After initialization, the encryption algorithm object can only be used for encryption or decryption. Running a decryption operation after an encryption operation, or vice versa, is not supported.***

**Syntax**

```python
ucryptolib.aes(key, mode[, IV])
```

**Parameters**

- **key** : An encryption/decryption key (bytes-like).
- **mode** :
  - `1` for Electronic Code Book (ECB) mode.
  - `2` for Cipher Block Chaining (CBC) mode.
  - `6` for Counter mode (CTR) mode.
- **IV** : an initialization vector for CBC mode.For Counter mode, IV is the initial value for the counter.

#### encrypt

**Description**

Encrypt `in_buf`. If no `out_buf` is given result is returned as a newly allocated `bytes object`. Otherwise, result is written into mutable buffer out_buf. `in_buf` and `out_buf` can also refer to the same mutable buffer, in which case data is encrypted in-place.

**Syntax**

```python
enc = aes.encrypt(in_buf[, out_buf])
```

#### decrypt

**Description**

Like `encrypt()`, but for decryption.

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
