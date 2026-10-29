# UARTPeriodicTx 硬件定时发送

`UARTPeriodicTx` 用硬件定时器周期性发送已经准备好的 UART 帧。它适合周期状态帧、控制帧等发送任务：Python 代码负责准备并更新数据，硬件定时器负责按周期触发原生发送路径。

本教程对应例程的开发板固件路径为
`/sdcard/examples/03-Machine/uart_periodic_tx.py`，SDK 源码路径为
`src/canmv/resources/examples/03-Machine/uart_periodic_tx.py`。示例以 50 ms 周期发送
7 到 22 字节的变长帧，在每次更新时请求立即发送，并使用 UART3 本地回环验证收发
结果和最新帧发送状态。

## 编译配置

该模块默认未编入固件。编译前执行：

```bash
# 使用 k230-builder 时
k230 make menuconfig

# 直接本机编译时
make menuconfig
```

在以下菜单打开 `Enable UART periodic TX module`，然后重新编译并烧录固件：

```text
CanMV Micropython Components Configurations
    Enable UART periodic TX module
```

## 接线

示例使用 UART3：

```text
IO50 (UART3_TXD) ---- IO51 (UART3_RXD)
```

运行前断电完成回环接线，并确认该板的 IO50 和 IO51 电平及引脚复用与示例一致。UART 电平必须匹配，不能接入 5 V UART 信号；详细要求见 [串口电平与转接模块安全](./uart.md)。也可以在 IO50 上连接逻辑分析仪测量发送周期。

```{warning}
示例中的 UART3、IO50 和 IO51 是当前示例的板级映射。实际应用应根据开发板原理图、REPL 配置及其他已使用外设选择 UART 和 FPIOA 引脚。
```

## 示例工作方式

示例首先将 IO50/IO51 映射为 UART3 TX/RX：

```python
from machine import FPIOA, UART

fpioa = FPIOA()
fpioa.set_function(50, FPIOA.UART3_TXD)
fpioa.set_function(51, FPIOA.UART3_RXD)
```

然后创建并启动发送器：

```python
from uart_periodic_tx import UARTPeriodicTx

transmitter = UARTPeriodicTx(
    UART.UART3,
    0,
    50,
    max_len=22,
    baudrate=115200,
    bits=UART.EIGHTBITS,
    parity=UART.PARITY_NONE,
    stop=UART.STOPBITS_ONE,
    repeat_last=True,
)

transmitter.update(b"\xA5\x5A\x07\x00\x00\xF8\x0D")
transmitter.start()
```

示例使用 `machine.UART` 只读取回环到 UART3 RX 的数据，以便检查帧内容。业务代码中，运行中的 `UARTPeriodicTx` 已拥有同一 UART 的发送路径，不要再对它调用 `machine.UART.write()`、`init()` 或 `deinit()`。

`repeat_last` 控制未更新数据时的行为：

- `repeat_last=True`（默认）：每次硬件定时器触发都发送最近一次 `update()` 的帧。
- `repeat_last=False`：每次 `update()` 的非空帧只发送一次；没有新数据的触发不发送，并计入 `skipped`。

示例每隔 `UPDATE_PERIOD_MS` 调用一次 `update()`。每帧的载荷长度由序号决定，因此连续调用可以发布不同长度的数据：

```python
sent_now = transmitter.update(
    make_frame(sequence), send_now=SEND_NOW_ON_UPDATE
)
if sent_now:
    print(transmitter.is_sent())
```

`send_now=True` 表示发布后立即尝试发送。返回 `True` 表示该帧已经完整写入 UART；返回 `False` 时帧仍然保留，后续硬件定时器可以重试。`is_sent()` 查询最近发布的非空帧是否至少成功完整写入 UART 一次。这里的“写入”表示 UART 驱动已接受完整帧，不表示线路发送已经结束，也不表示接收端确认。

示例帧格式如下：

```text
A5 5A <total_length> <sequence> <payload...> <checksum> 0D
```

载荷长度在 1 到 16 字节之间，`total_length` 因此在 7 到 22 之间。为了验证回环数据，示例约定第 `n` 个载荷字节为 `(sequence + n) & 0xFF`，其中 `n` 从 0 开始；`valid_frame()` 对该测试模式进行校验。实际应用可以使用任意载荷格式，但必须同步修改相应的校验逻辑。校验字节是它之前所有字节的异或值。例如序号为 `0x00` 时，帧内容为：

```text
A5 5A 07 00 00 F8 0D
```

当 `repeat_last=True` 时，硬件定时器会重复发送最近一次成功发布的帧，不会自行生成序号。默认示例又设置了 `send_now=True`，因此每次更新通常产生一次立即发送，同时定时器每 50 ms 继续发送一次，5 秒内的发送总数约为 200。立即发送和定时器触发靠得很近时，两帧的接收间隔可能很短，这是两条发送路径共同工作的预期结果。

若业务需要新数据立即发送，但每个版本的数据只发送一次，可以设置 `repeat_last=False` 并保留 `send_now=True`。立即发送失败时，下一次定时器触发仍会尝试发送该帧。

## 运行与结果

将示例复制到设备后运行 `uart_periodic_tx.py`。默认配置为：

| 项目 | 值 |
| --- | --- |
| UART | UART3 |
| 波特率 | 115200，8N1 |
| 硬件定时器 | 0 |
| 发送周期 | 50 ms |
| 更新周期 | 50 ms |
| 测试时长 | 5000 ms |
| 帧长度 | 7 到 22 字节 |
| 重复最近帧 | `True` |
| 更新时立即发送 | `True` |

输出会给出发送、接收和错误统计，例如：

```text
UARTPeriodicTx loopback test: period=50 ms, duration=5000 ms, repeat_last=True, send_now=True
frames: sent=199, received=198, invalid=0
frame length: min=7, max=22
immediate: submitted=99, requested=99, state_errors=0
latest packet submitted=True
tx stats: short_write=0, errors=0, skipped=0, last_error=0
rx interval us: avg=24876, min=8, max=50172
PASS
```

输出中的 199 次发送包括 99 次立即发送和约 100 次定时发送。测试循环结束时最后一帧可能仍在 UART 接收缓冲区中，因此接收数比发送数少 1 仍可通过测试。`state_errors=0` 表示每次立即发送返回成功后，`is_sent()` 都确认了最新帧状态；`min=7, max=22` 表示变长帧路径已被覆盖；`last_error=0` 表示尚未出现返回负值的 UART 写入错误。

接收时间戳仅用于软件回环健全性检查。`send_now` 和定时发送可能使两帧紧邻，因此很小的最短间隔不表示硬件定时周期抖动。若需要测量真实线上的周期和抖动，应使用 IO50 上的逻辑分析仪，并按 `115200`、8 数据位、无校验、1 停止位解码。

## 常见问题

| 现象 | 排查方式 |
| --- | --- |
| `ImportError: no module named 'uart_periodic_tx'` | 在 `menuconfig` 打开 `Enable UART periodic TX module` 后重新编译固件。 |
| `OSError: [Errno 16] EBUSY` | 检查 `timer_id` 是否已被 `machine.Timer` 或另一个 `UARTPeriodicTx` 使用；同一 UART 的多个周期发送器还必须使用相同配置。 |
| `RuntimeError: transmitter is not running` | 只有调用 `start()` 后才能使用 `update(..., send_now=True)`；启动前的初始数据应使用默认的 `send_now=False` 发布。 |
| 逻辑分析仪始终显示同一序号 | 确认捕获时长覆盖多个 `UPDATE_PERIOD_MS`，并检查应用是否持续调用 `update()`。定时器在两次更新之间重复上一帧是预期行为。 |
| 发送数接近定时触发次数的两倍 | 同时启用了 `repeat_last=True` 和 `send_now=True`，每次更新会立即发送，定时器仍会重复最近帧。需要每帧只发送一次时设置 `repeat_last=False`。 |
| 收不到回环数据或显示 `FAIL` | 检查 IO50 到 IO51 的连接、FPIOA 映射、UART3 是否被其他功能占用，以及两端是否均为 115200 8N1。 |
| `short_write` 或 `errors` 不为零 | 降低帧长度或提高波特率、增大发送周期，并确保一个 UART 没有多个重叠发送任务。`errors` 不为零时调用 `last_error()` 获取最近一次写入失败的 `errno`。 |
| `skipped` 不为零 | 在 `repeat_last=False` 模式下，未更新数据时的定时器触发会计入 `skipped`；立即发送因 UART 忙而未执行时也会计入。其他情况检查 UART 忙、定时器资源和帧长度。 |

结束时应释放资源：

```python
try:
    transmitter.start()
    # 业务代码中按需调用 transmitter.update(...)
finally:
    transmitter.deinit()
```

更多 API 参数和资源约束见 [`uart_periodic_tx` 模块 API 手册](../../api/machine/k230_canmv_uart_periodic_tx_api_manual.md)。
