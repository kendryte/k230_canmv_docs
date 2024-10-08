# 1.3 `utime` Time-Related Functions API Manual

This module implements a subset of the functionality of the CPython module as described below. For more detailed information, please refer to the original CPython documentation: [time](https://docs.python.org/3.5/library/time.html#module-time).

The `utime` module provides functionalities for obtaining the current time and date, measuring time intervals, and delaying operations.

**Epoch Time**: The Unix port uses 1970-01-01 00:00:00 UTC as the standard epoch time for POSIX systems.

**Maintaining Actual Calendar Date/Time**: This requires using a real-time clock (RTC). On systems running an underlying operating system (including some real-time operating systems, RTOS), the RTC might be enabled by default. Setting and maintaining the actual calendar time is handled by the operating system or RTOS, and this is done outside of MicroPython. MicroPython queries the date and time via the operating system's API.

## Functions

### `ntp_sync`

```python
utime.ntp_sync()
```

When the system is connected to the network, calling this function can synchronize the current time from the internet. The function returns `True` or `False`, indicating whether the synchronization was successful. Some development boards do not support the RTC module, so this function always returns `False` on those boards.

### `localtime`

```python
utime.localtime([secs])
```

Converts time in seconds since the epoch to an 8-tuple containing the following information: (year, month, day, hour, minute, second, weekday, yearday). If no seconds are provided, it returns the current time from the RTC.

- Year includes the century (e.g., the year 2014)
- Month ranges from 1-12
- Day (mday) ranges from 1-31
- Hour ranges from 0-23
- Minute ranges from 0-59
- Second ranges from 0-59
- Weekday ranges from 0 (Monday) to 6 (Sunday)
- Yearday ranges from 1-366

### `mktime`

```python
utime.mktime(tuple)
```

This function is the inverse of `localtime()`. It accepts an 8-tuple representing local time and returns the number of seconds since 1970-01-01 00:00:00.

### `sleep`

```python
utime.sleep(seconds)
```

Delays execution for the specified number of seconds. Some development boards support passing floating-point numbers to achieve sub-second delays. However, to ensure compatibility, it is recommended to use `sleep_ms()` and `sleep_us()` functions for millisecond and microsecond delays.

### `sleep_ms`

```python
utime.sleep_ms(ms)
```

Delays execution for the specified number of milliseconds.

### `sleep_us`

```python
utime.sleep_us(us)
```

Delays execution for the specified number of microseconds.

### `ticks_ms`

```python
utime.ticks_ms()
```

Returns an increasing millisecond counter, referenced from an arbitrary point in the system's internal time. The counter will wrap around after a certain value.

### `ticks_us`

```python
utime.ticks_us()
```

Similar to `ticks_ms()`, but returns a microsecond-level counter.

### `ticks_cpu`

```python
utime.ticks_cpu()
```

Provides the highest resolution counter, usually related to the CPU clock, used for high-precision benchmarking or tight real-time loops.

### `ticks_add`

```python
utime.ticks_add(ticks, delta)
```

Calculates a new ticks value based on the specified time increment (`delta`, which can be positive or negative), useful for setting task deadlines.

### `ticks_diff`

```python
utime.ticks_diff(ticks1, ticks2)
```

Calculates the difference between two `ticks` values, handling counter wrap-around.

### `time`

```python
utime.time()
```

Returns the number of seconds since the epoch, provided the RTC is set. If the RTC is not set, it returns the number of seconds since the system was powered on or reset.

### `ticks`

```python
utime.ticks()
```

Equivalent to `utime.ticks_ms()`.

### `clock`

```python
utime.clock()
```

Returns a `clock` object for time measurement and FPS calculation.

## `clock` Class

### Constructor

```python
utime.clock()
```

### Methods

#### `tick`

```python
clock.tick()
```

Records the current time (in milliseconds), which can be used for FPS calculation.

#### `fps`

```python
clock.fps()
```

Calculates the frame rate (FPS) based on the time interval since the last `clock.tick()` call.

Example:

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

Resets all timing markers.

#### `avg`

```python
clock.avg()
```

Calculates the average time consumed per frame.
