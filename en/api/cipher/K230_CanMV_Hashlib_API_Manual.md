# `Hashlib` Module API Documentation

## Overview

The `uhashlib` library provides binary data hashing functionality based on MD5, SHA1, and SHA2 algorithms.

## API Introduction

The `uhashlib` library provides three classes: `md5`, `sha1`, and `sha256`. These classes each implement two functions: the data update function `update()` and the message digest function `digest()`. Among them, `md5` and `sha1` are software implementations in MicroPython; `sha256` is accelerated by the underlying hardware accelerator.

***Note: This document does not detail the usage steps for `md5` and `sha1`. For specifics, please refer to the MicroPython [hash official documentation](https://docs.micropython.org/en/latest/library/hashlib.html)***

### Class `sha256`

**Description**

The `sha256` class is used to create a SHA256 hash object and optionally send data to it.

**Syntax**  

```python
uhashlib.sha256([data])
```

**Parameters**  

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| data (optional) | Binary data       | Input        |

**Return Value**  

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-0        | Failure     |

**Example**  

```python
data = bytes([0]*64)
hash_obj = uhashlib.sha256(data)
hash_obj.update(data)
dgst = hash_obj.digest()
print(dgst)
```

#### Data Update Function `update()`

**Description**

If you need to input binary data multiple times, you can call the `update()` function to update the data.

**Syntax**

```python
obj.update(data)
```

**Parameters**

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| data           | Input binary data | Input        |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-0        | Failure     |

#### Message Digest Function `digest()`

**Description**
Returns the hash value of all input data.

***Note: In MicroPython, using this function completes the final calculation, not just displaying the result. Therefore, it can only be called once. If you need to use the value multiple times, please save it to a variable.***

**Syntax**  

```python
dgst = hash.digest()
print(dgst)

/*********** Note ***********/
a = hash.digest()
b = hash.digest() # Error
```

**Parameters**

None

**Return Value**  

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-0        | Failure     |

#### Hexadecimal Message Digest Function `hexdigest()`

This method is not implemented. You can use `binascii.hexlify(hash.digest())` to achieve a similar effect.

## Example Program

### Calculate Hash Value

```python
import uhashlib
import binascii

# Initialize sha256 object
obj = uhashlib.sha256()
# Input data1
obj.update(b'hello')
# Input data2
obj.update(b'world')
# Compute digest
dgst = obj.digest()
print(binascii.hexlify(dgst))
# b'936a185caaa266bb9cbe981e9e05cb78cd732b0b3280eb944412bb6f8f8f07af'
```
