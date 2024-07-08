# 3.外设 例程讲解

## 1. Cipher - Cipher 例程

本示例程序用于对 CanMV 开发板进行一个 Cipher 输出的功能展示。

```python
import uhashlib

print('###################### SHA256 Test ##############################')
print('********************** Test-1: Only Call update() Once ******************')
# 初始化sha256对象
obj = uhashlib.sha256()
# 输入消息message
msg = b'\x45\x11\x01\x25\x0e\xc6\xf2\x66\x52\x24\x9d\x59\xdc\x97\x4b\x73\x61\xd5\x71\xa8\x10\x1c\xdf\xd3\x6a\xba\x3b\x58\x54\xd3\xae\x08\x6b\x5f\xdd\x45\x97\x72\x1b\x66\xe3\xc0\xdc\x5d\x8c\x60\x6d\x96\x57\xd0\xe3\x23\x28\x3a\x52\x17\xd1\xf5\x3f\x2f\x28\x4f\x57\xb8'
# 标准哈希值
dgst0 = b'\x1a\xaa\xf9\x28\x5a\xf9\x45\xb8\xa9\x7c\xf1\x4f\x86\x9b\x18\x90\x14\xc3\x84\xf3\xc7\xc2\xb7\xd2\xdf\x8a\x97\x13\xbf\xfe\x0b\xf1'
# 将消息更新到硬件IP中
obj.update(msg)
# 计算哈希值
dgst = obj.digest()
print(dgst0 == dgst)
# print(binascii.hexlify(dgst))
print('********************** Test-2: Call update() Twice ******************')
dgst0 = b'\x93\x6a\x18\x5c\xaa\xa2\x66\xbb\x9c\xbe\x98\x1e\x9e\x05\xcb\x78\xcd\x73\x2b\x0b\x32\x80\xeb\x94\x44\x12\xbb\x6f\x8f\x8f\x07\xaf'
obj = uhashlib.sha256()
# 向硬件多次更新消息
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
# dgst1 = obj.digest()
# print(dgst0 == dgst)
# print(dgst == dgst1)


print('\n###################### AES-GCM Test ##############################')
import ucryptolib
import collections
# 创建一个具名元组并返回具名元组子类
Aes = collections.namedtuple('Aes', ['key', 'iv', 'aad', 'pt', 'ct', 'tag'])
aes = [
    Aes(b'\xb5\x2c\x50\x5a\x37\xd7\x8e\xda\x5d\xd3\x4f\x20\xc2\x25\x40\xea\x1b\x58\x96\x3c\xf8\xe5\xbf\x8f\xfa\x85\xf9\xf2\x49\x25\x05\xb4',
        b'\x51\x6c\x33\x92\x9d\xf5\xa3\x28\x4f\xf4\x63\xd7',
        b'',
        b'',
        b'',
        b'\xbd\xc1\xac\x88\x4d\x33\x24\x57\xa1\xd2\x66\x4f\x16\x8c\x76\xf0'
        ),

    Aes(b'\x24\x50\x1a\xd3\x84\xe4\x73\x96\x3d\x47\x6e\xdc\xfe\x08\x20\x52\x37\xac\xfd\x49\xb5\xb8\xf3\x38\x57\xf8\x11\x4e\x86\x3f\xec\x7f',
        b'\x9f\xf1\x85\x63\xb9\x78\xec\x28\x1b\x3f\x27\x94',
        b'\xad\xb5\xec\x72\x0c\xcf\x98\x98\x50\x00\x28\xbf\x34\xaf\xcc\xbc\xac\xa1\x26\xef',
        b'\x27',
        b'\xeb',
        b'\x63\x35\xe1\xd4\x9e\x89\x88\xea\xc4\x8e\x42\x19\x4e\x5f\x56\xdb'
        ),
        
    Aes(b'\x1f\xde\xd3\x2d\x59\x99\xde\x4a\x76\xe0\xf8\x08\x21\x08\x82\x3a\xef\x60\x41\x7e\x18\x96\xcf\x42\x18\xa2\xfa\x90\xf6\x32\xec\x8a',
        b'\x1f\x3a\xfa\x47\x11\xe9\x47\x4f\x32\xe7\x04\x62',
        b'',
        b'\x06\xb2\xc7\x58\x53\xdf\x9a\xeb\x17\xbe\xfd\x33\xce\xa8\x1c\x63\x0b\x0f\xc5\x36\x67\xff\x45\x19\x9c\x62\x9c\x8e\x15\xdc\xe4\x1e\x53\x0a\xa7\x92\xf7\x96\xb8\x13\x8e\xea\xb2\xe8\x6c\x7b\x7b\xee\x1d\x40\xb0',
        b'\x91\xfb\xd0\x61\xdd\xc5\xa7\xfc\xc9\x51\x3f\xcd\xfd\xc9\xc3\xa7\xc5\xd4\xd6\x4c\xed\xf6\xa9\xc2\x4a\xb8\xa7\x7c\x36\xee\xfb\xf1\xc5\xdc\x00\xbc\x50\x12\x1b\x96\x45\x6c\x8c\xd8\xb6\xff\x1f\x8b\x3e\x48\x0f',
        b'\x30\x09\x6d\x34\x0f\x3d\x5c\x42\xd8\x2a\x6f\x47\x5d\xef\x23\xeb'
        ),
        
    Aes(b'\x24\x50\x1a\xd3\x84\xe4\x73\x96\x3d\x47\x6e\xdc\xfe\x08\x20\x52\x37\xac\xfd\x49\xb5\xb8\xf3\x38\x57\xf8\x11\x4e\x86\x3f\xec\x7f',
        b'\x9f\xf1\x85\x63\xb9\x78\xec\x28\x1b\x3f\x27\x94',
        b'\xad\xb5\xec\x72\x0c\xcf\x98\x98\x50\x00\x28\xbf\x34\xaf\xcc\xbc\xac\xa1\x26\xef',
        b'\x27\xf3\x48\xf9\xcd\xc0\xc5\xbd\x5e\x66\xb1\xcc\xb6\x3a\xd9\x20\xff\x22\x19\xd1\x4e\x8d\x63\x1b\x38\x72\x26\x5c\xf1\x17\xee\x86\x75\x7a\xcc\xb1\x58\xbd\x9a\xbb\x38\x68\xfd\xc0\xd0\xb0\x74\xb5\xf0\x1b\x2c',
        b'\xeb\x7c\xb7\x54\xc8\x24\xe8\xd9\x6f\x7c\x6d\x9b\x76\xc7\xd2\x6f\xb8\x74\xff\xbf\x1d\x65\xc6\xf6\x4a\x69\x8d\x83\x9b\x0b\x06\x14\x5d\xae\x82\x05\x7a\xd5\x59\x94\xcf\x59\xad\x7f\x67\xc0\xfa\x5e\x85\xfa\xb8',
        b'\xbc\x95\xc5\x32\xfe\xcc\x59\x4c\x36\xd1\x55\x02\x86\xa7\xa3\xf0'
        )
]

print('********************** Test-1: ivlen=12, ptlen=0, aadlen=0 ******************')
print('GCM Encrypt......')
# 初始化aes-gcm密码对象，参数包含密钥key、初始化向量iv以及附加数据aad
crypto = ucryptolib.aes(aes[0].key, 0, aes[0].iv, aes[0].aad)
# 输入明文数据
inbuf = aes[0].pt
outbuf = bytearray(16)
# 加密，输出格式为：密文 + tag
val = crypto.encrypt(inbuf, outbuf)
# 标准数据
val0 = aes[0].ct + aes[0].tag
print(val0 == val)
print('GCM Decrypt......')
crypto = ucryptolib.aes(aes[0].key, 0, aes[0].iv, aes[0].aad)
# 输入数据格式：密文 + tag
inbuf = aes[0].ct + aes[0].tag
# 解密，输出数据格式：明文
val = crypto.decrypt(inbuf)
print(val[:1] == b'\x00')
# val0 = aes[0].pt
# print(val0 == val)

print('********************** Test-2: ivlen=12, ptlen=1, aadlen=20 ******************')
print('GCM Encrypt......')
# 初始化
crypto = ucryptolib.aes(aes[1].key, 0, aes[1].iv, aes[1].aad)
# 输入明文
inbuf = aes[1].pt
outbuf = bytearray(17)
# 输出密文+tag
val = crypto.encrypt(inbuf, outbuf)
val0 = aes[1].ct + aes[1].tag
print(val0 == val)
print('GCM Decrypt......')
crypto = ucryptolib.aes(aes[1].key, 0, aes[1].iv, aes[1].aad)
# 输入密文+tag
inbuf = aes[1].ct + aes[1].tag
outbuf = bytearray(1)
# 输出明文
val = crypto.decrypt(inbuf, outbuf)
val0 = aes[1].pt
print(val0 == val)

print('********************** Test-3: ivlen=12, ptlen=51, aadlen=0 ******************')
print('GCM Encrypt......')
# 初始化
crypto = ucryptolib.aes(aes[2].key, 0, aes[2].iv, aes[2].aad)
# 输入明文
inbuf = aes[2].pt
outbuf = bytearray(67)
# 输出密文+tag
val = crypto.encrypt(inbuf, outbuf)
val0 = aes[2].ct + aes[2].tag
print(val0 == val)
print('GCM Decrypt......')
crypto = ucryptolib.aes(aes[2].key, 0, aes[2].iv, aes[2].aad)
# 输入密文+tag
inbuf = aes[2].ct + aes[2].tag
outbuf = bytearray(51)
# 输入明文
val = crypto.decrypt(inbuf, outbuf)
val0 = aes[2].pt
print(val0 == val)

print('********************** Test-4: ivlen=12, ptlen=51, aadlen=20 ******************')
print('GCM Encrypt......')
# 初始化
crypto = ucryptolib.aes(aes[3].key, 0, aes[3].iv, aes[3].aad)
# 输入明文
inbuf = aes[3].pt
outbuf = bytearray(67)
# 输出密文+tag
val = crypto.encrypt(inbuf, outbuf)
val0 = aes[3].ct + aes[3].tag
print(val0 == val)
print('GCM Decrypt......')
crypto = ucryptolib.aes(aes[3].key, 0, aes[3].iv, aes[3].aad)
# 输入密文+tag
inbuf = aes[3].ct + aes[3].tag
val = crypto.decrypt(inbuf)
val0 = aes[3].pt
print(val[:51] == val0)
# outbuf = bytearray(51)
# val = crypto.decrypt(inbuf, outbuf)
# val0 = aes[3].pt
# print(val0 == val)


print('\n###################### SM4-ECB/CFB/OFB/CBC/CTR Test ##############################')
Sm4 = collections.namedtuple('Sm4', ['key', 'iv', 'pt', 'ct'])
sm4 = [
    # ecb
    Sm4(b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',
        None,
        b'\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb\xcc\xcc\xcc\xcc\xdd\xdd\xdd\xdd\xee\xee\xee\xee\xff\xff\xff\xff\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb',
        b'\x5e\xc8\x14\x3d\xe5\x09\xcf\xf7\xb5\x17\x9f\x8f\x47\x4b\x86\x19\x2f\x1d\x30\x5a\x7f\xb1\x7d\xf9\x85\xf8\x1c\x84\x82\x19\x23\x04'
        ),

    # cbc
    Sm4(
        b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',
        b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f',
        b'\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb\xcc\xcc\xcc\xcc\xdd\xdd\xdd\xdd\xee\xee\xee\xee\xff\xff\xff\xff\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb',
        b'\x78\xeb\xb1\x1c\xc4\x0b\x0a\x48\x31\x2a\xae\xb2\x04\x02\x44\xcb\x4c\xb7\x01\x69\x51\x90\x92\x26\x97\x9b\x0d\x15\xdc\x6a\x8f\x6d'
        ),
    
    # cfb
    Sm4(
        b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',
        b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f',
        b'\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb\xcc\xcc\xcc\xcc\xdd\xdd\xdd\xdd\xee\xee\xee\xee\xff\xff\xff\xff\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb',
        b'\xac\x32\x36\xcb\x86\x1d\xd3\x16\xe6\x41\x3b\x4e\x3c\x75\x24\xb7\x69\xd4\xc5\x4e\xd4\x33\xb9\xa0\x34\x60\x09\xbe\xb3\x7b\x2b\x3f'
        ),

    # ofb
    Sm4(
        b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',
        b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f',
        b'\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb\xcc\xcc\xcc\xcc\xdd\xdd\xdd\xdd\xee\xee\xee\xee\xff\xff\xff\xff\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb',
        b'\xac\x32\x36\xcb\x86\x1d\xd3\x16\xe6\x41\x3b\x4e\x3c\x75\x24\xb7\x1d\x01\xac\xa2\x48\x7c\xa5\x82\xcb\xf5\x46\x3e\x66\x98\x53\x9b'
        ),

    # ctr
    Sm4(
        b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',
        b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f',
        b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xbb\xbb\xbb\xbb\xbb\xbb\xbb\xbb\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xdd\xdd\xdd\xdd\xdd\xdd\xdd\xdd\xee\xee\xee\xee\xee\xee\xee\xee\xff\xff\xff\xff\xff\xff\xff\xff\xee\xee\xee\xee\xee\xee\xee\xee\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa',
        b'\xac\x32\x36\xcb\x97\x0c\xc2\x07\x91\x36\x4c\x39\x5a\x13\x42\xd1\xa3\xcb\xc1\x87\x8c\x6f\x30\xcd\x07\x4c\xce\x38\x5c\xdd\x70\xc7\xf2\x34\xbc\x0e\x24\xc1\x19\x80\xfd\x12\x86\x31\x0c\xe3\x7b\x92\x2a\x46\xb8\x94\xbe\xe4\xfe\xb7\x9a\x38\x22\x94\x0c\x93\x54\x05'
        )
]

print('********************** Test-1: keybits=128, ptlen=32 ******************')
print('SM4-ECB Encrypt......')
# 初始化sm4密码对象，参数包含密钥key、加解密模式
crypto = ucryptolib.sm4(sm4[0].key, 1)
# 输入明文数据
inbuf = sm4[0].pt
outbuf = bytearray(32)
# 加密
val = crypto.encrypt(inbuf, outbuf)
# golden数据
val0 = sm4[0].ct
print(val0 == val)
print('SM4-ECB Decrypt......')
# 解密
crypto = ucryptolib.sm4(sm4[0].key, 1)
inbuf = sm4[0].ct
outbuf = bytearray(32)
val = crypto.decrypt(inbuf, outbuf)
val0 = sm4[0].pt
print(val0 == val)

print('********************** Test-2: keybits=128, ivlen=16, ptlen=32 ******************')
print('SM4-CBC Encrypt......')
# 初始化sm4密码对象
crypto = ucryptolib.sm4(sm4[1].key, 2, sm4[1].iv)
# 输入明文数据
inbuf = sm4[1].pt
outbuf = bytearray(32)
# 加密
val = crypto.encrypt(inbuf, outbuf)
val0 = sm4[1].ct
print(val0 == val)
print('SM4-CBC Decrypt......')
# 解密
crypto = ucryptolib.sm4(sm4[1].key, 2, sm4[1].iv)
inbuf = sm4[1].ct
val = crypto.decrypt(inbuf)
val0 = sm4[1].pt
print(val0 == val)
# outbuf = bytearray(32)
# val = crypto.decrypt(inbuf, outbuf)
# val0 = sm4[1].pt
# print(val0 == val)

print('********************** Test-3: keybits=128, ivlen=16, ptlen=32 ******************')
print('SM4-CFB Encrypt......')
# 初始化sm4密码对象
crypto = ucryptolib.sm4(sm4[2].key, 3, sm4[2].iv)
# 输入明文数据
inbuf = sm4[2].pt
outbuf = bytearray(32)
# 加密
val = crypto.encrypt(inbuf, outbuf)
val0 = sm4[2].ct
print(val0 == val)
print('SM4-CFB Decrypt......')
# 解密
crypto = ucryptolib.sm4(sm4[2].key, 3, sm4[2].iv)
inbuf = sm4[2].ct
outbuf = bytearray(32)
val = crypto.decrypt(inbuf, outbuf)
val0 = sm4[2].pt
print(val0 == val)

print('********************** Test-4: keybits=128, ivlen=16, ptlen=32 ******************')
print('SM4-OFB Encrypt......')
# 初始化sm4密码对象
crypto = ucryptolib.sm4(sm4[3].key, 5, sm4[3].iv)
# 输入明文数据
inbuf = sm4[3].pt
outbuf = bytearray(32)
# 加密
val = crypto.encrypt(inbuf, outbuf)
val0 = sm4[3].ct
print(val0 == val)
print('SM4-OFB Decrypt......')
# 解密
crypto = ucryptolib.sm4(sm4[3].key, 5, sm4[3].iv)
inbuf = sm4[3].ct
outbuf = bytearray(32)
val = crypto.decrypt(inbuf, outbuf)
val0 = sm4[3].pt
print(val0 == val)

print('********************** Test-5: keybits=128, ivlen=16, ptlen=64 ******************')
print('SM4-CTR Encrypt......')
# 初始化sm4密码对象
crypto = ucryptolib.sm4(sm4[4].key, 6, sm4[4].iv)
# 输入明文数据
inbuf = sm4[4].pt
outbuf = bytearray(64)
# 加密
val = crypto.encrypt(inbuf, outbuf)
val0 = sm4[4].ct
print(val0 == val)
print('SM4-CTR Decrypt......')
# 解密
crypto = ucryptolib.sm4(sm4[4].key, 6, sm4[4].iv)
inbuf = sm4[4].ct
outbuf = bytearray(64)
val = crypto.decrypt(inbuf, outbuf)
val0 = sm4[4].pt
print(val0 == val)
```

具体接口定义请参考 [Cipher](../api/cipher/K230_CanMV_Ucryptolib模块API手册.md)、[Hash](../api/cipher/K230_CanMV_Hashlib模块API手册.md)

## 2. ADC - ADC例程

本示例程序用于对 CanMV 开发板进行一个ADC的功能展示。

```python
from machine import ADC

# 实例化ADC通道0
adc = ADC(0)
# 获取ADC通道0采样值
print(adc.read_u16())
# 获取ADC通道0电压值
print(adc.read_uv(), "uV")
```

具体接口定义请参考 [ADC](../api/machine/K230_CanMV_ADC模块API手册.md)

## 3. FFT - FFT例程

本示例程序用于对 CanMV 开发板进行一个FFT的功能展示。

```python
from machine import FFT
import array
import math
from ulab import numpy as np
PI = 3.14159265358979323846264338327950288419716939937510

rx = []
def input_data():
    for i in range(64):
        data0 = 10 *math.cos(2* PI *i / 64)
        data1  = 20 * math.cos(2 * 2* PI *i / 64)
        data2  = 30* math.cos(3 *2* PI *i / 64)
        data3  = 0.2* math.cos(4 *2 * PI * i / 64)
        data4  = 1000* math.cos(5 *2* PI * i / 64)
        rx.append((int(data0 + data1 + data2 + data3 + data4)))
input_data()                                                            #初始化需要进行FFT的数据，列表类型
print(rx)
data = np.array(rx,dtype=np.uint16)                                     #把列表数据转换成数组
print(data)
fft1 = FFT(data, 64, 0x555)                                             #创建一个FFT对象,运算点数为64，偏移是0x555
res = fft1.run()                                                        #获取FFT转换后的数据
print(res)
res = fft1.amplitude(res)                                               #获取各个频率点的幅值
print(res)
res = fft1.freq(64,38400)                                               #获取所有频率点的频率值  
print(res)
```

具体接口定义请参考 [FFT](../api/machine/K230_CanMV_FFT模块API手册.md)

## 4. FPIOA - FPIOA例程

本示例程序用于对 CanMV 开发板进行一个FPIOA的功能展示。

```python
from machine import FPIOA

# 实例化FPIOA
fpioa = FPIOA()
# 打印所有引脚配置
fpioa.help()
# 打印指定引脚详细配置
fpioa.help(0)
# 打印指定功能所有可用的配置引脚
fpioa.help(FPIOA.IIC0_SDA, func=True)
# 设置Pin0为GPIO0
fpioa.set_function(0, FPIOA.GPIO0)
# 设置Pin2为GPIO2, 同时配置其它项
fpioa.set_function(2, FPIOA.GPIO2, ie=1, oe=1, pu=0, pd=0, st=1, sl=0, ds=7)
# 获取指定功能当前所在的引脚
fpioa.get_pin_num(FPIOA.UART0_TXD)
# 获取指定引脚当前功能
fpioa.get_pin_func(0)

```

具体接口定义请参考 [FPIOA](../api/machine/K230_CanMV_FPIOA模块API手册.md)

## 5. PWM - PWM例程

本示例程序用于对 CanMV 开发板进行一个PWM输出的功能展示。  

```python
from machine import PWM
# 实例化PWM通道0，频率为1000Hz，占空比为50%，默认使能输出
pwm0 = PWM(0, 1000, 50, enable = True)
# 关闭通道0输出
pwm0.enable(0)
# 调整通道0频率为2000Hz
pwm0.freq(2000)
# 调整通道0占空比为40%
pwm0.duty(40)
# 打开通道0输出
pwm0.enable(1)
```

具体接口定义请参考 [PWM](../api/machine/K230_CanMV_PWM模块API手册.md)

## 6. SPI - SPI例程

本示例程序用于对 CanMV 开发板进行spi读取flash id的功能展示。

```python
from machine import SPI
from machine import FPIOA

# 实例化SPI的gpio
a = FPIOA()

# 打印gpio14的属性
a.help(14)
# 设置gpio14为QSPI0_CS0功能
a.set_function(14,a.QSPI0_CS0)
a.help(14)

# 打印gpio15的属性
a.help(15)
# 设置gpio15为QSPI0_CLK功能
a.set_function(15,a.QSPI0_CLK)
a.help(15)

# 打印gpio16的属性
a.help(16)
# 设置gpio16为QSPI0_D0功能
a.set_function(16,a.QSPI0_D0)
a.help(16)

# 打印gpio17的属性
a.help(17)
# 设置gpio17为QSPI0_D1功能
a.set_function(17,a.QSPI0_D1)
a.help(17)

# 实例化SPI，使用5MHz时钟，极性为0，数据位宽为8bit
spi=SPI(1,baudrate=5000000, polarity=0, phase=0, bits=8)

# 使能 gd25lq128 复位
spi.write(bytes([0x66]))
# gd25lq128 复位
spi.write(bytes([0x99]))

# 读id命令（0x9f）
a=bytes([0x9f])
# 创建长度为3的接收buff
b=bytearray(3)
# 读id
spi.write_readinto(a,b)
# 打印为：bytearray(b'\xc8`\x18')
print(b)

# 读id命令（0x90,0,0,0）
a=bytes([0x90,0,0,0])
# 创建长度为2的接收buff
b=bytearray(2)
# 读id
spi.write_readinto(a,b)
# 打印为：bytearray(b'\xc8\x17')
print(b)
```

具体接口定义请参考 [SPI](../api/machine/K230_CanMV_SPI模块API手册.md)

## 7. Timer - Timer例程

本示例程序用于对 CanMV 开发板进行一个Timer的功能展示。

```python
from machine import Timer
import time

# 实例化一个软定时器
tim = Timer(-1)
# 初始化定时器为单次模式，周期100ms
tim.init(period=100, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
time.sleep(0.2)
# 初始化定时器为周期模式，频率为1Hz
tim.init(freq=1, mode=Timer.PERIODIC, callback=lambda t:print(2))
time.sleep(2)
# 释放定时器资源
tim.deinit()

```

具体接口定义请参考 [Timer](../api/machine/K230_CanMV_Timer模块API手册.md)

## 8. WDT - WDT例程

本示例程序用于对 CanMV 开发板进行一个WDT的功能展示。

```python
import time
from machine import WDT

# 实例化wdt1，timeout为3s
wdt1 = WDT(1,3)
time.sleep(2)
# 喂狗操作
wdt1.feed()
time.sleep(2)
```

具体接口定义请参考 [WDT](../api/machine/K230_CanMV_WDT模块API手册.md)
