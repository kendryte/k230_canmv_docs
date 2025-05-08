# 2.19 `USB Serial` 模块 API 手册

## 概述

USB Serial 模块提供了通过 USB 串口进行数据通信的功能。本模块实现了标准的流协议接口，支持读写操作。

该模块支持通过 AT 指令与 4G 模块通信。

## 构造函数

### `usb_serial(path="/dev/ttyUSB1", timeout_ms=300)`

创建一个 USB Serial 对象。

**参数：**

- `path` (str): 串口设备路径，默认为 "/dev/ttyUSB1"
- `timeout_ms` (int): 读写超时时间，单位为毫秒，默认为 300ms

**返回值：**

USB Serial 对象

**示例：**

```python
import usb_serial

# 创建 USB Serial 对象
serial = usb_serial.usb_serial("/dev/ttyUSB1", timeout_ms=300)
```

## 方法

### `open([path])`

打开 USB 串口设备。

**参数：**

- `path` (str, 可选): 如果提供，将使用此路径代替构造函数中指定的路径

**返回值：**

- `True`: 打开成功
- `False`: 打开失败

**示例：**

```python
serial.open()  # 使用构造函数中指定的路径
serial.open("/dev/ttyUSB2")  # 使用新路径
```

### `close()`

关闭 USB 串口设备。

**示例：**

```python
serial.close()
```

### `read(size)`

从串口读取数据。

**参数：**

- `size` (int): 要读取的字节数

**返回值：**
读取到的数据（bytes 类型）

### `readinto(buf)`

将数据读取到缓冲区中。

**参数：**

- `buf` (bytearray): 目标缓冲区

**返回值：**
实际读取的字节数

### `readline()`

读取一行数据，直到遇到换行符或超时。

**返回值：**
读取到的行数据（bytes 类型）

### `write(buf)`

向串口写入数据。

**参数：**

- `buf` (bytes/bytearray): 要写入的数据

**返回值：**
实际写入的字节数

## 属性

### `path`

获取或设置串口设备路径。

**示例：**

```python
print(serial.path)  # 获取当前路径
serial.path = "/dev/ttyUSB1"  # 设置新路径
```

### `timeout_ms`

获取或设置读写超时时间（毫秒）。

**示例：**

```python
print(serial.timeout_ms)  # 获取当前超时时间
serial.timeout_ms = 1000  # 设置超时时间为1秒
```

## 流协议支持

USB Serial 对象实现了标准的流协议，可以直接用于需要流对象的场合。

**示例：**

```python
# 使用 readline() 方法读取一行数据
line = serial.readline()

# 使用 write() 方法写入数据
serial.write(b"Hello World\n")
```

## 注意事项

1. 在对象销毁时会自动调用 `close()` 方法关闭串口
1. 所有读写操作都受 `timeout_ms` 参数控制
1. 如果串口未打开，调用读写方法会抛出 OSError 异常
1. 默认设备路径为 "/dev/ttyUSB1"，请根据实际设备修改
