# `Timer` 模块 API 手册

## 概述

`machine.Timer` 提供 6 个硬件定时器和 1 个软件定时器：

- `Timer(0)` 至 `Timer(5)` 使用 K230 硬件定时器，并占用对应的硬件资源。
- `Timer(-1)` 使用系统软件定时器，不占用硬件定时器资源。

定时器来源和 Python 回调的执行上下文由不同参数控制。`index` 决定使用硬件定时器还是软件定时器；`hard` 决定回调是在定时器中断上下文直接执行，还是在普通 Python 上下文中延后执行。

`period` 的单位为毫秒，最小值为 5 ms。

## 示例代码

以下示例使用 `hard=False`，因此回调可以安全地执行 `print()`。周期回调通过计数器判断是否已经执行 3 次，而不是在恰好 3 秒后立即调用 `deinit()`。

```python
from machine import Timer
import time

ticks = 0


def on_one_shot(timer):
    print("one-shot")


def on_periodic(timer):
    global ticks
    ticks += 1
    print("periodic", ticks)


# -1 表示软件定时器
tim = Timer(-1)

# 100 ms 后执行一次
tim.init(period=100, mode=Timer.ONE_SHOT, callback=on_one_shot, hard=False)
time.sleep_ms(150)

# 每秒执行一次，等待 3 次回调完成
tim.init(freq=1, mode=Timer.PERIODIC, callback=on_periodic, hard=False)
while ticks < 3:
    time.sleep_ms(10)

tim.deinit()
```

## 构造函数

```python
timer = Timer(index, mode=Timer.PERIODIC, freq=-1, period=-1, callback=None, *, hard=True)
```

创建定时器对象。除 `index` 外的参数也可在 [`init`](#timer-init) 中设置。

**参数**

| 参数 | 说明 |
| --- | --- |
| `index` | 定时器编号。`-1` 为软件定时器；`0` 至 `5` 为硬件定时器。 |
| `mode` | 运行模式：`Timer.ONE_SHOT` 为单次模式，`Timer.PERIODIC` 为周期模式。默认值为 `Timer.PERIODIC`。 |
| `freq` | 定时频率，正整数，单位为 Hz。设置该参数时优先于 `period`；实际周期按 `1000 // freq` 毫秒计算。 |
| `period` | 定时时间，正整数，单位为毫秒。当未设置 `freq` 时使用，且必须不小于 5 ms。 |
| `callback` | 超时回调函数。必须是可调用对象，接收一个 `Timer` 参数。 |
| `hard` | 仅关键字参数，布尔值，默认 `True`。控制 Python 回调的执行上下文，详见[回调执行方式](#timer-callback-context)。 |

一个定时器编号同一时刻只能由一个 `Timer` 对象使用。`Timer(-1)` 只有一个软件定时器实例；再次创建相同编号的 `Timer` 会返回已有对象。

<a id="timer-init"></a>

## `init` 方法

```python
Timer.init(mode=Timer.PERIODIC, freq=-1, period=-1, callback=None, *, hard=True)
```

配置并启动定时器。对正在运行的定时器再次调用 `init()` 会停止原来的配置并应用新配置。

**参数**

参数含义与构造函数中的 `mode`、`freq`、`period`、`callback`、`hard` 相同。

**返回值**

无。

<a id="timer-callback-context"></a>

## 回调执行方式

`hard` 与 `index` 相互独立。例如，`Timer(-1, ..., hard=True)` 仍在定时器中断上下文调用 Python 回调；`Timer(0, ..., hard=False)` 虽由硬件定时器到期，但 Python 回调会被延后到普通 Python 上下文执行。

| `hard` | 回调执行方式 | 适用场景与限制 |
| --- | --- | --- |
| `True`（默认） | 在定时器中断上下文直接调用 Python 回调。 | 仅用于非常短且不会分配内存的中断安全操作。不要在回调中使用 `print()`、`sleep()`、阻塞 I/O、网络或文件系统操作，也不要创建 Python 对象；这些操作可能失败或导致系统不稳定。 |
| `False` | 到期事件由中断捕获，Python 回调随后在普通 Python 上下文中执行。 | 推荐用于 `print()`、一般 Python 逻辑和可能分配内存的操作。回调会受解释器负载影响，不适合硬实时任务。 |

当 `hard=False` 时，同一个定时器在已有回调等待执行期间最多保留一个待执行回调。若定时器到期速度高于 Python 处理速度，多个到期事件可能合并，或因调度队列已满而丢失。因此不要用 `hard=False` 的回调次数作为严格的硬实时计数。

## 定时精度和等待方式

软件定时器受系统调度影响，硬件定时器的 Python 回调也会受 `hard` 选择和解释器负载影响。`time.sleep()` 只保证主程序至少等待相应时长，不保证边界时刻的回调已经执行。

例如，周期为 1 Hz 时，在 `time.sleep(3)` 后立即调用 `deinit()`，第三个到期事件可能正处于等待调度或尚未送达的状态，因而不会执行。需要准确等待回调次数时，应使用计数器、标志位或事件同步；仅用于观察输出时，可在预期时长后留出少量余量。

## `deinit` 方法

```python
Timer.deinit()
```

停止定时器并释放其资源。调用后，该对象不能再次调用 `init()`；需要重新创建对应编号的 `Timer` 对象。

**参数**

无。

**返回值**

无。
