# Timer 使用教程

## 什么是 Timer？

`machine.Timer` 用于在超时后执行回调函数。K230 提供硬件定时器和软件定时器，适合单次延迟、周期采样、状态上报和超时控制等场景。

Timer 的两个概念需要区分：

- **定时器来源**由编号决定：`0` 至 `5` 是硬件定时器，`-1` 是软件定时器。
- **回调执行方式**由 `hard` 决定：`hard=True` 在中断上下文执行，`hard=False` 在普通 Python 上下文执行。

这两个选择相互独立。硬件定时器配合 `hard=False` 仍然由硬件计时，只是 Python 回调会延后执行。

## K230 Timer 特性

| 特性 | 描述 |
| --- | --- |
| 硬件定时器数量 | 6 个，编号为 `0` 至 `5` |
| 软件定时器 | 1 个，编号为 `-1`，不占用硬件定时器资源 |
| 最小 `period` | 5 ms |
| 支持模式 | 单次模式（`Timer.ONE_SHOT`）、周期模式（`Timer.PERIODIC`） |
| 回调方式 | 中断上下文（`hard=True`）或普通 Python 上下文（`hard=False`） |

## 推荐用法：普通 Python 回调

对于打印、传感器读取、文件或网络操作等普通 Python 逻辑，请使用 `hard=False`。下面的示例先执行一次单次回调，再等待周期回调执行 3 次后释放定时器。

```python
from machine import Timer
import time

count = 0


def one_shot_callback(timer):
    print("one-shot callback")


def periodic_callback(timer):
    global count
    count += 1
    print("periodic callback", count)


# -1 表示软件定时器；也可使用 0 至 5 选择硬件定时器
tim = Timer(-1)

# 100 ms 后触发一次
tim.init(
    period=100,
    mode=Timer.ONE_SHOT,
    callback=one_shot_callback,
    hard=False,
)
time.sleep_ms(150)

# 每秒触发一次，直到已经收到 3 次回调
tim.init(
    freq=1,
    mode=Timer.PERIODIC,
    callback=periodic_callback,
    hard=False,
)
while count < 3:
    # 让解释器处理已调度的回调，避免忙等。
    time.sleep_ms(10)

tim.deinit()
```

不要用 `time.sleep(3)` 后立即调用 `deinit()` 来断言 1 Hz 回调一定执行 3 次。第三次到期可能恰好与 `sleep()` 返回和 `deinit()` 竞争，尤其是软件定时器或 `hard=False` 回调还可能存在调度延迟。需要等待指定次数时，应像上例一样使用计数器、标志位或事件同步。

## 参数说明

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| `index` | 整数 | `-1` 为软件定时器；`0` 至 `5` 为硬件定时器。 |
| `period` | 整数（ms） | 定时时间，最小为 5 ms。 |
| `freq` | 整数（Hz） | 定时频率。设置后优先于 `period`，实际周期按 `1000 // freq` 毫秒计算。 |
| `mode` | 常量 | `Timer.ONE_SHOT`（单次）或 `Timer.PERIODIC`（周期）。 |
| `callback` | 函数 | 定时器到期时调用，接收一个 `Timer` 参数。 |
| `hard` | 布尔值 | 仅关键字参数，默认为 `True`。决定回调的 Python 执行上下文。 |

## 回调方式

### `hard=False`：普通 Python 上下文

到期事件先由定时器中断处理，再将 Python 回调安排到普通 Python 上下文执行。

- 可以使用 `print()`，并执行会分配内存的普通 Python 代码。
- 回调执行时间受系统调度和 Python 负载影响，不是硬实时。
- 同一个定时器在回调等待执行期间只保留一个待执行任务；定时器到期过快时，多个事件可能合并或丢失。

这是大多数 Python 应用的推荐选择。

### `hard=True`：中断上下文

这是默认值。Python 回调由定时器中断直接调用，延迟较低，但限制严格：

- 回调必须非常短。
- 不要调用 `print()`、`sleep()`、阻塞 I/O、网络或文件系统 API。
- 不要创建 Python 对象或执行可能分配内存的操作。

违反这些限制可能导致异常、回调丢失或系统不稳定。需要复杂处理时，可在 `hard=True` 回调中仅设置一个预先准备好的状态，再由主循环处理；通常直接使用 `hard=False` 更合适。

## 模式详解

### 单次模式 `Timer.ONE_SHOT`

```python
tim.init(period=100, mode=Timer.ONE_SHOT, callback=func, hard=False)
```

- 定时器只触发一次。
- 到期后自动停止。

### 周期模式 `Timer.PERIODIC`

```python
tim.init(freq=2, mode=Timer.PERIODIC, callback=func, hard=False)
```

- 以配置的周期持续触发，直到重新初始化或调用 `deinit()`。
- `freq=2` 对应约 500 ms 的周期。

## 资源和生命周期

- 每个硬件定时器编号只能被一个 `Timer` 使用。
- `Timer(-1)` 只有一个软件定时器实例；重复创建会获得同一个对象。
- 对运行中的定时器再次调用 `init()` 会替换原有配置。
- `deinit()` 会停止定时器并释放资源。释放后的对象不能再次调用 `init()`，需要重新创建 `Timer`。

## 应用场景举例

- 周期采样：读取传感器数据
- 超时控制：任务执行超时处理
- 系统心跳：周期更新状态或输出日志
- 低延迟的简单中断操作：使用 `hard=True`，并保持回调短小且不分配内存

```{admonition} 提示
Timer 模块完整参数说明请参考 [K230 Timer API 文档](../../api/machine/k230_canmv_timer_api_manual.md)
```
