# `uhashlib` Module API Documentation

## Overview

`uhashlib` module implements binary data hashing algorithms. The exact inventory of available algorithms depends on a board. Among the algorithms which may be implemented:

- `SHA256` - The current generation, modern hashing algorithm (of SHA2 series). It is suitable for cryptographically-secure purposes. Included in the MicroPython core and any board is recommended to provide this, unless it has particular code size constraints.
- `SHA1` - A previous generation algorithm. Not recommended for new usages, but SHA1 is a part of number of Internet standards and existing applications, so boards targeting network connectivity and interoperability will try to provide this.
- `MD5` - A legacy algorithm, not considered cryptographically secure. Only selected boards, targeting interoperability with legacy applications, will offer this.

***For specifics, please refer to the MicroPython [hash official documentation](https://docs.micropython.org/en/latest/library/hashlib.html)***

### Constructor

#### sha256

**Description**

Create an SHA256 hasher object and optionally feed `data` into it.

**Syntax**

```python
obj = uhashlib.sha256([data])
```

**Parameters**  

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| data (optional) | Binary data       | Input        |

**Return Value**  

Return the sha256 hasher object.

#### sha1

**Description**

Create an SHA1 hasher object and optionally feed `data` into it.

**Syntax**

```python
obj = uhashlib.sha1([data])
```

**Parameters**  

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| data (optional) | Binary data       | Input        |

**Return Value**  

Return the sha1 hasher object.

#### md5

**Description**

Create an md5 hasher object and optionally feed `data` into it.

**Syntax**

```python
obj = uhashlib.md5([data])
```

**Parameters**  

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| data (optional) | Binary data       | Input        |

**Return Value**  

Return the md5 hasher object.

### Hasher Object Functions

#### Data Update Function `update()`

**Description**

If you need to input binary data multiple times, you can call the `update()` function to update the data.

**Syntax**

```python
hash.update(data)
```

**Parameters**

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| data           | Input binary data | Input        |

**Return Value**

None.

#### Message Digest Function `digest()`

**Description**

Return hash for all data passed through hash, as a bytes object.

***Note:After this method is called, more data cannot be fed into the hash any longer.***

**Syntax**  

```python
dgst = hash.digest()
```

**Parameters**

None.

**Return Value**  

Return the hash values of all the data passed through the hash.

#### Hexadecimal Message Digest Function `hexdigest()`

This method is not implemented. You can use `binascii.hexlify(hash.digest())` to achieve a similar effect.

## Example Program

```python
import uhashlib

print('###################### SHA256 Test ##############################')
print('********************** Test-1: Only Call update() Once ******************')
# Initialize the sha256 object
obj = uhashlib.sha256()
# Enter the message
msg = b'\x45\x11\x01\x25\x0e\xc6\xf2\x66\x52\x24\x9d\x59\xdc\x97\x4b\x73\x61\xd5\x71\xa8\x10\x1c\xdf\xd3\x6a\xba\x3b\x58\x54\xd3\xae\x08\x6b\x5f\xdd\x45\x97\x72\x1b\x66\xe3\xc0\xdc\x5d\x8c\x60\x6d\x96\x57\xd0\xe3\x23\x28\x3a\x52\x17\xd1\xf5\x3f\x2f\x28\x4f\x57\xb8'
# The expected hash value
dgst0 = b'\x1a\xaa\xf9\x28\x5a\xf9\x45\xb8\xa9\x7c\xf1\x4f\x86\x9b\x18\x90\x14\xc3\x84\xf3\xc7\xc2\xb7\xd2\xdf\x8a\x97\x13\xbf\xfe\x0b\xf1'
# update the message
obj.update(msg)
# calculate the hash value
dgst = obj.digest()
print(dgst0 == dgst)
# print(binascii.hexlify(dgst))
print('********************** Test-2: Call update() Twice ******************')
dgst0 = b'\x93\x6a\x18\x5c\xaa\xa2\x66\xbb\x9c\xbe\x98\x1e\x9e\x05\xcb\x78\xcd\x73\x2b\x0b\x32\x80\xeb\x94\x44\x12\xbb\x6f\x8f\x8f\x07\xaf'
obj = uhashlib.sha256()
# Update the message to the hardware multiple times
obj.update(b'hello')
obj.update(b'world')
dgst = obj.digest()
print(dgst0 == dgst)
# print('********************** Test-3: Call digest() Twice ******************')
# dgst0 = b'\x93\x6a\x18\x5c\xaa\xa2\x66\xbb\x9c\xbe\x98\x1e\x9e\x05\xcb\x78\xcd\x73\x2b\x0b\x32\x80\xeb\x94\x44\x12\xbb\x6f\x8f\x8f\x07\xaf'
# obj = uhashlib.sha256()
# obj.update(b'hello')
# obj.update(b'world')
# dgst = obj.digest()
# dgst1 = obj.digest() # Error: digest() can only be called once
# print(dgst0 == dgst)
# print(dgst == dgst1)
```
