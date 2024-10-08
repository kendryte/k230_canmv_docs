# 1.1 Ucryptolib Module API Manual

## 1. Overview

The `Ucryptolib` library provides the following encryption and decryption functionalities: AES-ECB, AES-CBC, AES-CTR, AES-GCM, and SM4. Among these, AES-ECB, AES-CBC, and AES-CTR modes are natively implemented by MicroPython's software library, while AES-GCM and SM4 are accelerated through underlying hardware accelerators.

***Note: This document does not detail the encryption and decryption steps for AES-ECB, AES-CBC, and AES-CTR modes. For related information, please refer to MicroPython's [official cryptolib documentation](https://docs.micropython.org/en/latest/library/cryptolib.html).***

## 2. API Introduction

The `Ucryptolib` library provides two main classes: `aes` and `sm4`, which implement encryption (`encrypt`) and decryption (`decrypt`) operations respectively.

### 2.1 Class `aes`

**Description**

The `aes` class is used to initialize an AES-GCM encryption/decryption object, supporting encryption and decryption operations. In the AES-GCM encryption/decryption algorithm, you must specify the key (`key`), mode (`mode`), initialization vector (`IV`), and additional authenticated data (`AAD`) during initialization.

***Note: Once initialized, the encryption or decryption object can only be used for a single operation, either encryption or decryption, and cannot be used for both simultaneously.***

**Syntax**

```python
ucryptolib.aes((key, mode, IV, AAD))
```

**Parameters**

| Parameter Name | Description                                                      | Input/Output |
| -------------- | ---------------------------------------------------------------- | ------------ |
| key            | Encryption/decryption key, supports a key length of 256 bits     | Input        |
| mode           | Encryption/decryption mode, supported mode is AES-GCM, set `mode=0` | Input        |
| IV             | Initialization vector, length of 12 bytes                        | Input        |
| AAD            | Additional authenticated data for data integrity verification, supports any length | Input        |

**Example**

```python
import ucryptolib

# Initialize AES-GCM object
cipher = ucryptolib.aes(key, mode=0, IV=iv, AAD=aad)

# Perform encryption operation
ciphertext = cipher.encrypt(plaintext)

# Perform decryption operation
decrypted_text = cipher.decrypt(ciphertext)
```

### 2.2 Class `sm4`

**Description**

The `sm4` class is used to initialize an SM4 encryption/decryption object, supporting encryption and decryption operations according to the Chinese national cryptographic standard SM4. Similar to AES-GCM, SM4 requires a key (`key`), mode (`mode`), and initialization vector (`IV`) during initialization.

**Syntax**

```python
ucryptolib.sm4((key, mode, IV))
```

**Parameters**

| Parameter Name | Description                                                      | Input/Output |
| -------------- | ---------------------------------------------------------------- | ------------ |
| key            | SM4 encryption/decryption key, supports a key length of 128 bits | Input        |
| mode           | Encryption/decryption mode, supports ECB (Electronic Codebook) and CBC (Cipher Block Chaining) modes | Input        |
| IV             | Initialization vector, length of 16 bytes, must be provided in CBC mode | Input        |

**Example**

```python
import ucryptolib

# Initialize SM4 object
cipher = ucryptolib.sm4(key, mode=1, IV=iv)

# Perform encryption operation
ciphertext = cipher.encrypt(plaintext)

# Perform decryption operation
decrypted_text = cipher.decrypt(ciphertext)
```
