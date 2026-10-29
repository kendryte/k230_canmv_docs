# `uart_periodic_tx` 模块 API 手册

## 概述

`uart_periodic_tx` 是一个可选的原生模块，用硬件定时器周期性发送已经准备好的完整 UART 帧，也可以在发布新帧时请求立即发送。定时器回调只执行原生 UART 写操作，不执行 Python 代码，也不在回调中分配 GC 内存。

适用于需要稳定周期发送不同长度数据帧的场景，例如每 50 ms 发送一次状态帧。应用程序在普通 Python 上下文中调用 `update()` 发布下一帧；每次发布的数据长度可以不同，但不能超过构造时设置的 `max_len`。

```{note}
该模块是 UART 周期发送器，不是通用硬件定时任务框架，不能在定时器中调度任意 Python 函数，也不能直接用于网络、SPI 或 I2C 传输。三组内部缓冲区用于避免更新与发送互相覆盖，不构成 FIFO 队列；模块只保证发送最近发布的数据，连续快速调用 `update()` 可能使尚未发送的旧数据被新数据取代。
```

## 启用模块

该功能默认关闭。编译固件前，在源码根目录执行构建环境对应的配置命令：

```bash
# 使用 k230-builder 时
k230 make menuconfig

# 直接本机编译时
make menuconfig
```

打开以下选项后重新编译固件：

```text
CanMV Micropython Components Configurations
    Enable UART periodic TX module
```

未启用该选项的固件中导入模块会报 `ImportError`。

## 导入模块

```python
from machine import FPIOA, UART
from uart_periodic_tx import UARTPeriodicTx
```

## 快速开始

以下示例将 UART3 的 TX 映射到 IO50，并每 50 ms 发送一帧。应根据开发板和板级配置选择未被 REPL 或其他系统功能占用的 UART 与引脚。

```python
from machine import FPIOA, UART
from uart_periodic_tx import UARTPeriodicTx
import time

fpioa = FPIOA()
fpioa.set_function(50, FPIOA.UART3_TXD)

tx = UARTPeriodicTx(
    UART.UART3,
    0,
    50,
    max_len=64,
    baudrate=115200,
    bits=UART.EIGHTBITS,
    parity=UART.PARITY_NONE,
    stop=UART.STOPBITS_ONE,
    repeat_last=True,
)

try:
    tx.update(b"\x01\x02\x03")
    tx.start()

    time.sleep_ms(1000)
    sent_now = tx.update(b"\x10\x20\x30\x40\x50", send_now=True)
    print("immediate submitted:", sent_now)
    print("latest packet submitted:", tx.is_sent())
    time.sleep_ms(1000)
finally:
    tx.deinit()
```

必须在调用 `start()` 前完成 FPIOA 的 UART TX 引脚映射。上例两次发布的数据长度分别为 3 字节和 5 字节。`update()` 会复制传入的缓冲区，因此调用返回后修改原始 `bytearray` 不会修改已经发布的帧。

## `UARTPeriodicTx` 类

### 构造函数

```python
UARTPeriodicTx(
    uart_id,
    timer_id,
    period=50,
    *,
    max_len=64,
    baudrate=115200,
    bits=UART.EIGHTBITS,
    parity=UART.PARITY_NONE,
    stop=UART.STOPBITS_ONE,
    repeat_last=True,
)
```

创建周期发送器。构造函数会分配三组发送缓冲区，但在调用 `start()` 前不会占用 UART 或硬件定时器。

| 参数 | 说明 |
| --- | --- |
| `uart_id` | UART 硬件编号，例如 `UART.UART3`。传入的是编号而不是 `machine.UART` 对象。UART 必须可用且 TX 引脚已正确复用。 |
| `timer_id` | 硬件定时器编号。不能使用软件定时器编号 `-1`。当前 K230 定时器编号为 `0` 到 `5`。 |
| `period` | 发送周期，单位为 ms，默认 `50`，最小值为 `1`。 |
| `max_len` | 单帧最大长度，默认 `64`，范围为 `1` 到 `4096` 字节。模块为该容量分配三组缓冲区。 |
| `baudrate` | UART 波特率，默认 `115200`。 |
| `bits` | 数据位，使用与 `machine.UART` 相同的常量，例如 `UART.EIGHTBITS`。支持 5 到 9 位。 |
| `parity` | 校验方式，例如 `UART.PARITY_NONE`、`UART.PARITY_ODD` 或 `UART.PARITY_EVEN`。 |
| `stop` | 停止位，例如 `UART.STOPBITS_ONE` 或 `UART.STOPBITS_TWO`。 |
| `repeat_last` | 是否在没有新的 `update()` 时重复发送最后一帧，默认 `True`。设为 `False` 时，每个成功 `update()` 的非空帧只在完整写入 UART 后发送一次；后续定时器触发会跳过，直到有新的 `update()`。 |

`period` 可以作为第三个位置参数传入，其余 UART 配置参数必须使用关键字参数。

### `update` 方法

```python
tx.update(data, send_now=False)
```

复制并发布一帧完整数据。默认由硬件定时器在后续触发时发送；设置 `send_now=True` 时，发布后还会立即尝试发送该帧。

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | 缓冲区对象 | 例如 `bytes`、`bytearray` 或 `memoryview`。每次调用可以使用不同长度，长度不能超过 `max_len`。空数据可以发布，但不会发送。 |
| `send_now` | `bool` | 仅限关键字参数，表示是否在发布后立即尝试发送，默认 `False`。设为 `True` 时发送器必须已经通过 `start()` 启动。 |

**返回值：`bool`**

- `send_now=False` 时返回 `False`，表示没有执行立即发送；该返回值不代表后续定时器不会发送此帧。
- `send_now=True` 时，如果本次发布的帧已经完整写入 UART，则返回 `True`。如果 UART 忙、发生短写或写入错误，则返回 `False`，数据仍保留为最近发布的帧，后续定时器可以再次尝试发送。

**异常**

- `ValueError`：对象已释放，或数据长度超过 `max_len`。
- `RuntimeError`：设置了 `send_now=True`，但发送器尚未启动或已经停止。
- `OSError(EBUSY)`：三组缓冲区暂时都不可写。可在普通 Python 上下文中稍后重试；不要在 `machine.Timer` 回调中调用该方法。

`update()` 不会等待 UART 在线路上完成发送，也不保证新帧恰好在下一次硬件触发时出现。如果发送路径已经取走当前缓冲区，新帧会在其后的触发中生效。`repeat_last=True` 时，定时器持续发送最近一次成功发布的完整帧；`repeat_last=False` 时，该帧完整写入一次后等待下一次 `update()`。

当 `repeat_last=True` 且同时使用 `send_now=True` 时，新帧会立即发送，定时器仍会在每次周期触发时重复最近一帧。若希望每次更新只发送一次，并在立即发送失败时由定时器重试，请使用 `repeat_last=False`。

### `start` 方法

```python
tx.start()
```

申请硬件定时器和 UART，并开始周期发送。调用前至少应成功调用一次 `update()`，否则定时器触发会记为跳过发送。

同一个 `timer_id` 不能同时被 `machine.Timer` 或另一个 `UARTPeriodicTx` 使用。资源冲突会抛出 `OSError(EBUSY)`。

### `stop` 方法

```python
tx.stop()
```

停止周期发送并释放硬件定时器和 UART 的运行时资源，但保留对象和已分配的发送缓冲区。之后可以再次调用 `start()`。

### `deinit` 方法

```python
tx.deinit()
```

停止发送并释放全部原生资源和缓冲区。调用后对象不能再次使用。建议在 `try` / `finally` 中调用，确保异常路径也能释放硬件定时器。

### `active` 方法

```python
tx.active()
```

返回布尔值，表示硬件定时器是否正在运行。

### `is_sent` 方法

```python
tx.is_sent()
```

返回最近发布的非空帧是否至少成功完整写入 UART 一次：

- 创建对象后、首次成功发送前返回 `False`。
- 每次发布新帧后，该帧尚未发送时返回 `False`。
- 立即发送或定时器发送完整写入后返回 `True`。
- 发布空数据后返回 `False`。

该状态对应 UART 驱动的 `write()` 已接受完整帧，不表示最后一个比特已经离开发送引脚，也不表示接收端已经收到或确认。调用 `deinit()` 后再次调用此方法会抛出 `ValueError`。

### `last_error` 方法

```python
tx.last_error()
```

**返回值：`int`**

返回最近一次 UART `write()` 返回负值时保存的 `errno`。尚未发生写入错误时返回 `0`；后续写入成功不会清除已经记录的错误码。短写不是负值错误，不会更新该错误码，应通过 `stats()` 返回的 `short_write` 计数检查。

硬件定时器回调中不能安全地打印日志或抛出 Python 异常，因此模块以原子方式记录错误码，由普通 Python 代码调用此方法查询。

### `stats` 方法

```python
sent, short_write, errors, skipped = tx.stats()
```

返回累计统计元组：

| 返回值 | 说明 |
| --- | --- |
| `sent` | UART 写入返回完整帧长度的次数，包括定时发送、立即发送和 `repeat_last=True` 时的重复发送。 |
| `short_write` | UART 写入了部分帧的次数。 |
| `errors` | UART 写入返回负值的次数。可调用 `last_error()` 查询最近一次错误的 `errno`。 |
| `skipped` | 未执行 UART 写入的发送尝试次数，例如 UART 正忙、尚未发布可发送帧，或 `repeat_last=False` 时没有新数据。该值同时统计被跳过的定时器触发和因 UART 忙而未执行的立即发送尝试。 |

统计值在对象生命周期内累计，`stop()` 和再次 `start()` 不会清零。

## 资源与时序约束

- `UARTPeriodicTx` 持有用于发送的原生 UART 驱动。运行期间不要通过 `machine.UART.write()` 发送同一 UART，也不要重新配置或释放同一 UART。
- 多个 `UARTPeriodicTx` 可以使用同一 UART，但 UART 配置必须完全相同。两个发送时刻重叠时，其中一个触发会被跳过并计入 `skipped`。需要可预测时序时，应为一个 UART 只创建一个周期发送器。
- 定时器触发由硬件定时器驱动，避免了 Python VM、GC 和 Python 回调带来的发送触发延迟；实际在线路上完成一帧仍受波特率、帧长度和 UART 驱动状态影响。
- 帧的串行发送时间应明显小于 `period`。若帧过长、波特率过低或 UART 忙，可能出现 `short_write`、`errors` 或 `skipped`。
- `repeat_last=True` 时，逻辑分析仪会看到最近成功 `update()` 的帧被连续发送。`repeat_last=False` 时，每次成功 `update()` 最多产生一次完整帧发送；没有新数据的触发会计入 `skipped`。
- `send_now=True` 只发起一次立即写入尝试，不会暂停或重新对齐硬件定时器。立即发送时刻靠近定时器触发时，线路上可能连续出现两帧。

完整回环验证示例见 [UARTPeriodicTx 硬件定时发送](../../example/peripheral/uart_periodic_tx.md)。
