# `utime` Time-related Functions API Manual

This module implements a subset of the functionality of the corresponding CPython module, as described below. For more information, refer to the original CPython documentation: [time](https://docs.python.org/3.5/library/time.html#module-time).

The `utime` module provides functions for getting the current time and date, measuring time intervals, and performing delays.

**Epoch Time**: The Unix port version uses 1970-01-01 00:00:00 UTC as the standard epoch time for POSIX systems.

**Maintaining Actual Calendar Date/Time**: This requires the use of a real-time clock (RTC). On systems running an underlying operating system (including some real-time operating systems, RTOS), the RTC may be enabled by default. The work of setting and maintaining the actual calendar time is handled by the operating system or RTOS and is performed outside of MicroPython. MicroPython only queries the date and time through the operating system's API.

## Functions

### `ntp_sync`

```python
utime.ntp_sync()
```

When the system is connected to the network, calling this function synchronizes the current time from the internet. The function returns `True` or `False`, indicating whether the synchronization was successful. Some development boards do not support the RTC module, so this function always returns `False` on those boards.

### `localtime`

```python
utime.localtime([secs])
```

Converts a time expressed in seconds since the epoch into an 8-tuple containing the following information: (year, month, day, hour, minute, second, weekday, yearday). If no seconds are provided, the current time from the RTC is returned.

- The year includes the century (e.g., 2014)
- The month ranges from 1-12
- The day (mday) ranges from 1-31
- The hour ranges from 0-23
- The minute ranges from 0-59
- The second ranges from 0-59
- The weekday ranges from 0 (Monday) to 6 (Sunday)
- The yearday ranges from 1-366

### `mktime`

```python
utime.mktime(tuple)
```

This function is the inverse of `localtime()`. It takes an 8-tuple representing local time and returns the number of seconds since 1970-01-01 00:00:00.

### `sleep`

```python
utime.sleep(seconds)
```

Delays execution for the specified number of seconds. Some development boards support passing seconds as a floating-point number to achieve sub-second delays. However, for compatibility, it is recommended to use the `sleep_ms()` and `sleep_us()` functions to handle millisecond and microsecond delays.

### `sleep_ms`

```python
utime.sleep_ms(ms)
```

Delays for the specified number of milliseconds.

### `sleep_us`

```python
utime.sleep_us(us)
```

Delays for the specified number of microseconds.

### `ticks_ms`

```python
utime.ticks_ms()
```

Returns an incrementing millisecond counter with an arbitrary reference point in the system's internal time, which will wrap around after a certain value.

### `ticks_us`

```python
utime.ticks_us()
```

Similar to `ticks_ms()`, but returns microsecond-level counts.

### `ticks_cpu`

```python
utime.ticks_cpu()
```

Provides the highest resolution counter, usually related to the CPU clock, used for high-precision benchmarking or tight real-time loops.

### `ticks_add`

```python
utime.ticks_add(ticks, delta)
```

Calculates a new ticks value based on the specified time increment (`delta`, which can be positive or negative), used to set task deadlines, etc.

### `ticks_diff`

```python
utime.ticks_diff(ticks1, ticks2)
```

Calculates the difference between two `ticks` values, supporting the handling of counter wraparound.

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

Returns a `clock` object, used for time measurement and FPS calculation.

## `clock` class

### Constructor

```python
utime.clock()
```

### Methods

#### `tick`

```python
clock.tick()
```

Records the current time (in milliseconds), can be used for FPS calculation.

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

Calculates the average time consumption per frame.
