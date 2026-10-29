# `Timer` Module API Manual

## Overview

`machine.Timer` provides 6 hardware timers and 1 software timer:

- `Timer(0)` through `Timer(5)` use K230 hardware timers and occupy the corresponding hardware resources.
- `Timer(-1)` uses the system software timer and does not occupy hardware timer resources.

The timer source and the execution context of the Python callback are controlled by different parameters. `index` determines whether a hardware timer or the software timer is used; `hard` determines whether the callback is executed directly in the timer interrupt context, or deferred and executed in the normal Python context.

The unit of `period` is milliseconds, with a minimum value of 5 ms.

## Example Code

The following example uses `hard=False`, so the callback can safely execute `print()`. The periodic callback uses a counter to determine whether it has been executed 3 times, rather than calling `deinit()` immediately after exactly 3 seconds.

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


# -1 indicates the software timer
tim = Timer(-1)

# Execute once after 100 ms
tim.init(period=100, mode=Timer.ONE_SHOT, callback=on_one_shot, hard=False)
time.sleep_ms(150)

# Execute every second, wait for 3 callbacks to complete
tim.init(freq=1, mode=Timer.PERIODIC, callback=on_periodic, hard=False)
while ticks < 3:
    time.sleep_ms(10)

tim.deinit()
```

## Constructor

```python
timer = Timer(index, mode=Timer.PERIODIC, freq=-1, period=-1, callback=None, *, hard=True)
```

Creates a timer object. Parameters other than `index` can also be set in [`init`](#timer-init).

**Parameters**

| Parameter | Description |
| --- | --- |
| `index` | Timer number. `-1` is the software timer; `0` through `5` are hardware timers. |
| `mode` | Operating mode: `Timer.ONE_SHOT` for one-shot mode, `Timer.PERIODIC` for periodic mode. The default value is `Timer.PERIODIC`. |
| `freq` | Timer frequency, a positive integer, in Hz. When set, this parameter takes precedence over `period`; the actual period is calculated as `1000 // freq` milliseconds. |
| `period` | Timer duration, a positive integer, in milliseconds. Used when `freq` is not set, and must not be less than 5 ms. |
| `callback` | Timeout callback function. Must be a callable object that accepts one `Timer` parameter. |
| `hard` | Keyword-only parameter, boolean, default `True`. Controls the execution context of the Python callback; see [Callback Execution Mode](#timer-callback-context) for details. |

A timer number can only be used by one `Timer` object at a time. `Timer(-1)` has only one software timer instance; creating another `Timer` with the same number returns the existing object.

<a id="timer-init"></a>

## `init` Method

```python
Timer.init(mode=Timer.PERIODIC, freq=-1, period=-1, callback=None, *, hard=True)
```

Configures and starts the timer. Calling `init()` again on a running timer stops the previous configuration and applies the new one.

**Parameters**

The parameter meanings are the same as `mode`, `freq`, `period`, `callback`, and `hard` in the constructor.

**Return Value**

None.

<a id="timer-callback-context"></a>

## Callback Execution Mode

`hard` and `index` are independent of each other. For example, `Timer(-1, ..., hard=True)` still invokes the Python callback in the timer interrupt context; for `Timer(0, ..., hard=False)`, although it is triggered by a hardware timer expiry, the Python callback is deferred and executed in the normal Python context.

| `hard` | Callback Execution Mode | Applicable Scenarios and Limitations |
| --- | --- | --- |
| `True` (default) | The Python callback is invoked directly in the timer interrupt context. | Only for very short interrupt-safe operations that do not allocate memory. Do not use `print()`, `sleep()`, blocking I/O, network or file system operations in the callback, and do not create Python objects; these operations may fail or cause system instability. |
| `False` | The expiry event is captured by the interrupt, and the Python callback is subsequently executed in the normal Python context. | Recommended for `print()`, general Python logic, and operations that may allocate memory. The callback is affected by interpreter load and is not suitable for hard real-time tasks. |

When `hard=False`, at most one pending callback is kept for the same timer while a callback is already waiting to execute. If the timer expires faster than Python can process it, multiple expiry events may be coalesced, or dropped because the scheduling queue is full. Therefore, do not use the number of callbacks from `hard=False` as a strict hard real-time count.

## Timer Precision and Waiting Methods

Software timers are affected by system scheduling, and the Python callbacks of hardware timers are also affected by the choice of `hard` and the interpreter load. `time.sleep()` only guarantees that the main program waits at least the corresponding duration; it does not guarantee that the callback at the boundary moment has been executed.

For example, with a period of 1 Hz, if `deinit()` is called immediately after `time.sleep(3)`, the third expiry event may still be waiting to be scheduled or may not have been delivered yet, and therefore will not execute. When you need to accurately wait for a specific number of callbacks, use a counter, flag, or event synchronization; when only used for observing output, leave a small margin after the expected duration.

## `deinit` Method

```python
Timer.deinit()
```

Stops the timer and releases its resources. After calling, the object cannot call `init()` again; a new `Timer` object with the corresponding number needs to be created.

**Parameters**

None.

**Return Value**

None.
