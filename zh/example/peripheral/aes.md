# K230 AES 加解密教程

## 什么是 AES？

**AES（Advanced Encryption Standard，高级加密标准）** 是一种对称加密算法，被广泛应用于文件保护、网络通信、嵌入式设备加密等场景。

K230 芯片内置硬件加速模块，可通过 `ucryptolib.aes` 快速实现 AES 加密和解密操作。

## 支持的 AES 模式

| 模式      | 特性描述              |
| ------- | ----------------- |
| ECB     | 电码本模式，最基本但不安全     |
| CBC     | 密码块链接模式，安全性更强     |
| CTR     | 计数器模式，适合流式数据      |

## 本示例内容

本教程使用 **AES-CBC（密码块链接）模式**，展示如何对一段任意长度的数据进行：

* 数据填充（Pad）
* 加密（Encrypt）
* 解密（Decrypt）
* 验证原始明文一致性

## 示例代码

```python
import urandom
from ucryptolib import aes

# ========== 辅助函数：填充与去填充 ==========
def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# ========== 加密函数 ==========
def aes_encrypt(plaintext: bytes, key: bytes) -> bytes:
    iv = bytes([urandom.getrandbits(8) for _ in range(16)])  # 生成随机 IV
    cipher = aes(key, 2, iv)  # 模式 2 = CBC
    padded = pad(plaintext)
    ciphertext = cipher.encrypt(padded)
    return iv + ciphertext  # 返回 IV + 密文

# ========== 解密函数 ==========
def aes_decrypt(data: bytes, key: bytes) -> bytes:
    iv = data[:16]
    ciphertext = data[16:]
    cipher = aes(key, 2, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    return unpad(padded_plaintext)

# ========== 示例使用 ==========
key = b"0123456789abcdef"              # 16字节密钥
plaintext = b"This is a raw data"      # 明文（不一定是16的倍数）

encrypted_data = aes_encrypt(plaintext, key)
print("密文 (IV + Ciphertext):", encrypted_data)

decrypted_data = aes_decrypt(encrypted_data, key)
print("解密后明文:", decrypted_data)

assert decrypted_data == plaintext, "明文解密不一致！"
```

## 核心流程解析

### 1. 补齐明文（Padding）

由于 AES 加密块大小为 16 字节，需对明文进行 PKCS#7 填充：

```python
pad_len = 16 - len(data) % 16
data + bytes([pad_len] * pad_len)
```

### 2. 随机生成 IV

在 CBC 模式中，每次加密都需新的随机初始向量（IV）：

```python
iv = bytes([urandom.getrandbits(8) for _ in range(16)])
```

### 3. CBC 模式加密 & 解密

```python
cipher = aes(key, 2, iv)   # 模式 2：CBC
cipher.encrypt()           # 加密
cipher.decrypt()           # 解密
```

注意：CBC 模式无法验证数据完整性，若需认证请考虑 GCM 模式。

## 模块接口说明

| 函数/类名                | 功能说明                          |
| -------------------- | ----------------------------- |
| `aes(key, mode, iv)` | 创建 AES 加解密器，`mode=2` 为 CBC 模式 |
| `.encrypt(data)`     | 加密字节串（长度必须为 16 的倍数）           |
| `.decrypt(data)`     | 解密字节串（同上）                     |

## 参数说明

| 参数     | 类型    | 描述                        |
| ------ | ----- | ------------------------- |
| `key`  | bytes | 16 字节密钥（支持 128 位）         |
| `iv`   | bytes | 16 字节初始向量，用于 CBC 加密       |
| `data` | bytes | 原始明文 / 密文（需 pad/unpad 处理） |

## 应用建议

| 应用场景   | 推荐说明                           |
| ------ | ------------------------------ |
| 数据存储加密 | 使用 AES-CBC 加密配置文件或日志           |
| 串口传输加密 | 加密传输数据，配合 IV 实现安全通信            |
| 简单认证通信 | 推荐结合 HMAC 使用，否则 CBC 不具备数据完整性校验 |

## 延伸阅读

* 📘 [K230 Ucryptolib 模块 API 文档](../../api/cipher/k230_canmv_ucryptolib_api_manual.md)
