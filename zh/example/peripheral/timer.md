# TIMER 例程

## 概述

K230 内部包含 6 个 Timer 硬件模块，最小定时周期为 1 微秒。通过这些定时器，可以实现精确的定时和周期性任务。

## 示例

以下示例展示了如何使用 Timer 模块进行定时操作。

```python
from machine import Timer
import time

# 实例化一个软定时器
tim = Timer(-1)

# 初始化定时器为单次模式，周期 100ms
tim.init(period=100, mode=Timer.ONE_SHOT, callback=lambda t: print(1))
time.sleep(0.2)

# 初始化定时器为周期模式，频率为 1Hz
tim.init(freq=1, mode=Timer.PERIODIC, callback=lambda t: print(2))
time.sleep(2)

# 释放定时器资源
tim.deinit()
```

## 代码说明

1. **实例化 Timer**：
   - 创建 `Timer` 对象，`-1` 表示使用软件定时器。

1. **单次模式定时器**：
   - 使用 `tim.init(period=100, mode=Timer.ONE_SHOT, callback=lambda t: print(1))` 初始化定时器，设置周期为 100 毫秒，并在定时到达时执行回调函数，输出 `1`。

1. **延迟**：
   - `time.sleep(0.2)` 暂停 200 毫秒，确保能够看到定时器回调的输出。

1. **周期模式定时器**：
   - 使用 `tim.init(freq=1, mode=Timer.PERIODIC, callback=lambda t: print(2))` 初始化定时器，设置频率为 1Hz，定时器每秒触发一次回调，输出 `2`。

1. **再次延迟**：
   - `time.sleep(2)` 暂停 2 秒，以便观察周期模式定时器的输出。

1. **释放资源**：
   - 调用 `tim.deinit()` 释放定时器资源，停止所有定时器操作。

```{admonition} 提示
Timer 模块具体接口请参考 [API 文档](../../api/machine/K230_CanMV_Timer模块API手册.md)
```
