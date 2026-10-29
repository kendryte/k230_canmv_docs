# K230 AES Encryption/Decryption Tutorial

## What is AES?

**AES (Advanced Encryption Standard)** is a symmetric encryption algorithm widely used in file protection, network communication, embedded device encryption, and other scenarios.

The K230 chip has a built-in hardware acceleration module that can quickly implement AES encryption and decryption operations via `ucryptolib.aes`.

## Supported AES Modes

| Mode     | Feature Description                |
| -------- | ---------------------------------- |
| ECB      | Electronic Codebook mode, basic but insecure |
| CBC      | Cipher Block Chaining mode, stronger security |
| CTR      | Counter mode, suitable for streaming data      |

## Contents of This Example

This tutorial uses **AES-CBC (Cipher Block Chaining) mode** to demonstrate how to perform the following on a piece of arbitrary-length data:

* Padding (Pad)
* Encryption (Encrypt)
* Decryption (Decrypt)
* Verification of original plaintext consistency

## Example Code

```python
import urandom
from ucryptolib import aes

# ========== Helper Functions: Padding and Unpadding ==========
def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# ========== Encryption Function ==========
def aes_encrypt(plaintext: bytes, key: bytes) -> bytes:
    iv = bytes([urandom.getrandbits(8) for _ in range(16)])  # Generate random IV
    cipher = aes(key, 2, iv)  # Mode 2 = CBC
    padded = pad(plaintext)
    ciphertext = cipher.encrypt(padded)
    return iv + ciphertext  # Return IV + ciphertext

# ========== Decryption Function ==========
def aes_decrypt(data: bytes, key: bytes) -> bytes:
    iv = data[:16]
    ciphertext = data[16:]
    cipher = aes(key, 2, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    return unpad(padded_plaintext)

# ========== Example Usage ==========
key = b"0123456789abcdef"              # 16-byte key
plaintext = b"This is a raw data"      # Plaintext (not necessarily a multiple of 16)

encrypted_data = aes_encrypt(plaintext, key)
print("Ciphertext (IV + Ciphertext):", encrypted_data)

decrypted_data = aes_decrypt(encrypted_data, key)
print("Decrypted plaintext:", decrypted_data)

assert decrypted_data == plaintext, "Plaintext decryption mismatch!"
```

## Core Workflow Analysis

### 1. Padding the Plaintext

Since the AES encryption block size is 16 bytes, the plaintext needs to be padded using PKCS#7:

```python
pad_len = 16 - len(data) % 16
data + bytes([pad_len] * pad_len)
```

### 2. Random IV Generation

In CBC mode, a new random initialization vector (IV) is required for each encryption:

```python
iv = bytes([urandom.getrandbits(8) for _ in range(16)])
```

### 3. CBC Mode Encryption & Decryption

```python
cipher = aes(key, 2, iv)   # Mode 2: CBC
cipher.encrypt()           # Encrypt
cipher.decrypt()           # Decrypt
```

Note: CBC mode cannot verify data integrity; consider GCM mode if authentication is required.

## Module Interface Description

| Function/Class Name       | Description                              |
| --------------------- | ---------------------------------------- |
| `aes(key, mode, iv)` | Create an AES encryptor/decryptor, `mode=2` is CBC mode |
| `.encrypt(data)`     | Encrypt byte string (length must be a multiple of 16) |
| `.decrypt(data)`     | Decrypt byte string (same as above)              |

## Parameter Description

| Parameter | Type    | Description                                |
| ------ | ----- | ------------------------------------------ |
| `key`  | bytes | 16-byte key (supports 128-bit)               |
| `iv`   | bytes | 16-byte initialization vector, used for CBC encryption |
| `data` | bytes | Original plaintext / ciphertext (requires pad/unpad handling) |

## Application Recommendations

| Application Scenario   | Recommended Description                          |
| ------ | ---------------------------------------------- |
| Data storage encryption | Use AES-CBC to encrypt configuration files or logs      |
| Serial transmission encryption | Encrypt transmitted data, combined with IV for secure communication |
| Simple authenticated communication | Recommended to use with HMAC, otherwise CBC does not provide data integrity verification |

## Further Reading

* 📘 [K230 Ucryptolib Module API Documentation](../../api/cipher/k230_canmv_ucryptolib_api_manual.md)
