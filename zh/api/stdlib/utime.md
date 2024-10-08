# 1.3 `utime` 时间相关功能 API 手册

该模块实现了部分 CPython 模块的功能子集，具体如下所述。更多详细信息，请参考 CPython 原始文档：[time](https://docs.python.org/3.5/library/time.html#module-time)。

`utime` 模块提供获取当前时间与日期、测量时间间隔以及延迟操作的相关功能。

**纪元时间**：Unix 系统移植版本使用 1970-01-01 00:00:00 UTC 作为 POSIX 系统的标准纪元时间。

**维护实际日历日期/时间**：这需要使用实时时钟（RTC）。在运行底层操作系统（包括部分实时操作系统，RTOS）的系统上，RTC 可能默认启用。设置和维护实际日历时间的工作由操作系统或 RTOS 负责，并且是在 MicroPython 之外完成的，MicroPython 只通过操作系统的 API 查询日期和时间。

## 函数

### `ntp_sync`

```python
utime.ntp_sync()
```

当系统联网后，调用该函数可以从互联网同步当前时间。函数返回 `True` 或 `False`，表示同步是否成功。某些开发板不支持 RTC 模块，因此该函数在这些板上总是返回 `False`。

### `localtime`

```python
utime.localtime([secs])
```

将自纪元以来以秒为单位的时间转换为 8 元组，包含以下信息：(年，月，日，小时，分钟，秒，工作日，yearday)。如果未提供秒数，则返回来自 RTC 的当前时间。

- 年份包含世纪（如 2014 年）
- 月份范围为 1-12
- 日（mday）范围为 1-31
- 小时范围为 0-23
- 分钟范围为 0-59
- 秒范围为 0-59
- 工作日范围为 0（周一）至 6（周日）
- yearday 范围为 1-366

### `mktime`

```python
utime.mktime(tuple)
```

该函数是 `localtime()` 的逆函数。它接受一个 8 元组，表示本地时间，并返回自 1970-01-01 00:00:00 以来的秒数。

### `sleep`

```python
utime.sleep(seconds)
```

延迟执行指定的秒数。部分开发板支持以浮点数传入秒数，以实现亚秒级的延迟。不过，为确保兼容性，推荐使用 `sleep_ms()` 和 `sleep_us()` 函数来处理毫秒和微秒级的延迟。

### `sleep_ms`

```python
utime.sleep_ms(ms)
```

延迟指定的毫秒数。

### `sleep_us`

```python
utime.sleep_us(us)
```

延迟指定的微秒数。

### `ticks_ms`

```python
utime.ticks_ms()
```

返回一个递增的毫秒计数器，参考点为系统内部的任意时间点，该计数器会在某个值后回绕。

### `ticks_us`

```python
utime.ticks_us()
```

与 `ticks_ms()` 类似，但返回的是微秒级计数。

### `ticks_cpu`

```python
utime.ticks_cpu()
```

提供最高分辨率的计数器，通常与 CPU 时钟相关，用于高精度基准测试或紧凑的实时循环。

### `ticks_add`

```python
utime.ticks_add(ticks, delta)
```

根据指定的时间增量（`delta`，可以为正或负数）计算新的 ticks 值，用于设定任务的截止时间等。

### `ticks_diff`

```python
utime.ticks_diff(ticks1, ticks2)
```

计算两个 `ticks` 值之间的差异，支持处理计数器回绕。

### `time`

```python
utime.time()
```

返回自纪元以来的秒数，前提是已设置 RTC。如果未设置 RTC，则返回自系统上电或复位以来的秒数。

### `ticks`

```python
utime.ticks()
```

等同于 `utime.ticks_ms()`。

### `clock`

```python
utime.clock()
```

返回一个 `clock` 对象，用于时间测量和 FPS 计算。

## `clock` 类

### 构造函数

```python
utime.clock()
```

### 方法

#### `tick`

```python
clock.tick()
```

记录当前时间（毫秒），可用于 FPS 计算。

#### `fps`

```python
clock.fps()
```

根据上一次 `clock.tick()` 调用后的时间间隔，计算帧率（FPS）。

示例：

```python
import utime
clock = utime.clock()
while True:
    clock.tick()
    utime.sleep(0.1)
    print("fps = ", clock.fps())
```

#### `reset`

```python
clock.reset()
```

重置所有计时标记。

#### `avg`

```python
clock.avg()
```

计算每帧的平均时间消耗。
