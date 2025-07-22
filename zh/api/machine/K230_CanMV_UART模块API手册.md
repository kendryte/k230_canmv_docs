# `UART` 模块 API 手册

## 概述

K230 内部集成了五个 UART（通用异步收发传输器）硬件模块，其中 UART0 被小核 SH 占用，UART3 被大核 SH 占用，剩余的 UART1、UART2 和 UART4 可供用户使用。UART 的 I/O 配置可参考 IOMUX 模块。

## API 介绍

UART 类位于 `machine` 模块中。

### 示例代码

```python
from machine import UART

# 配置 UART1: 波特率 115200, 8 位数据位, 无奇偶校验, 1 个停止位
u1 = UART(UART.UART1, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

# 写入数据到 UART
u1.write("UART1 test")

# 从 UART 读取数据
r = u1.read()

# 读取一行数据
r = u1.readline()

# 将数据读入字节缓冲区
b = bytearray(8)
r = u1.readinto(b)

# 释放 UART 资源
u1.deinit()
```

### 构造函数

```python
uart = UART(id, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE, timeout = 0)
```

**参数**

- `id`: UART 模块编号，有效值为 `UART1`、`UART2`、`UART4`。
- `baudrate`: UART 波特率，可选参数，默认值为 115200。
- `bits`: 每个字符的数据位数，有效值为 `FIVEBITS`、`SIXBITS`、`SEVENBITS`、`EIGHTBITS`，可选参数，默认值为 `EIGHTBITS`。
- `parity`: 奇偶校验，有效值为 `PARITY_NONE`、`PARITY_ODD`、`PARITY_EVEN`，可选参数，默认值为 `PARITY_NONE`。
- `stop`: 停止位数，有效值为 `STOPBITS_ONE`、`STOPBITS_TWO`，可选参数，默认值为 `STOPBITS_ONE`。
- `timeout`: 读数据超时，单位为 `ms`

### `init` 方法

```python
UART.init(baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
```

配置 UART 参数。

**参数**

参考构造函数。

**返回值**

无

### `read` 方法

```python
UART.read([nbytes])
```

读取字符。如果指定了 `nbytes`，则最多读取该数量的字节；否则，将尽可能多地读取数据。

**参数**

- `nbytes`: 最多读取的字节数，可选参数。

**返回值**

返回一个包含读取字节的字节对象。

### `readline` 方法

```python
UART.readline()
```

读取一行数据，并以换行符结束。

**参数**

无

**返回值**

返回一个包含读取字节的字节对象。

### `readinto` 方法

```python
UART.readinto(buf[, nbytes])
```

将字节读取到 `buf` 中。如果指定了 `nbytes`，则最多读取该数量的字节；否则，最多读取 `len(buf)` 数量的字节。

**参数**

- `buf`: 一个缓冲区对象。
- `nbytes`: 最多读取的字节数，可选参数。

**返回值**

返回读取并存入 `buf` 的字节数。

### `write` 方法

```python
UART.write(buf)
```

将字节缓冲区写入 UART。

**参数**

- `buf`: 一个缓冲区对象。

**返回值**

返回写入的字节数。

### `deinit` 方法

```python
UART.deinit()
```

释放 UART 资源。

**参数**

无

**返回值**

无
