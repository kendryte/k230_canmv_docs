# Timer Usage Tutorial

## What is Timer?

`machine.Timer` is used to execute a callback function after a timeout. The K230 provides hardware timers and a software timer, suitable for one-shot delays, periodic sampling, status reporting, timeout control, and other scenarios.

Two concepts of Timer need to be distinguished:

- **The timer source** is determined by the number: `0` to `5` are hardware timers, `-1` is the software timer.
- **The callback execution mode** is determined by `hard`: `hard=True` executes in interrupt context, `hard=False` executes in normal Python context.

These two choices are independent of each other. A hardware timer paired with `hard=False` is still timed by hardware, but the Python callback will be executed later.

## K230 Timer Features

| Feature | Description |
| --- | --- |
| Number of hardware timers | 6, numbered `0` to `5` |
| Software timer | 1, numbered `-1`, does not occupy hardware timer resources |
| Minimum `period` | 5 ms |
| Supported modes | One-shot mode (`Timer.ONE_SHOT`), periodic mode (`Timer.PERIODIC`) |
| Callback mode | Interrupt context (`hard=True`) or normal Python context (`hard=False`) |

## Recommended Usage: Normal Python Callback

For normal Python logic such as printing, sensor reading, file or network operations, please use `hard=False`. The following example first executes a one-shot callback, then waits for the periodic callback to be executed 3 times before releasing the timer.

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


# -1 indicates the software timer; you can also use 0 to 5 to select a hardware timer
tim = Timer(-1)

# Trigger once after 100 ms
tim.init(
    period=100,
    mode=Timer.ONE_SHOT,
    callback=one_shot_callback,
    hard=False,
)
time.sleep_ms(150)

# Trigger once every second, until 3 callbacks have been received
tim.init(
    freq=1,
    mode=Timer.PERIODIC,
    callback=periodic_callback,
    hard=False,
)
while count < 3:
    # Let the interpreter handle the scheduled callbacks to avoid busy waiting.
    time.sleep_ms(10)

tim.deinit()
```

Don't use `time.sleep(3)` followed immediately by `deinit()` to assert that a 1 Hz callback has run exactly 3 times. The third expiry may race against `sleep()` returning and `deinit()`, and software timers or `hard=False` callbacks may also incur scheduling delays. When you need to wait for a specific number of occurrences, use a counter, flag, or event synchronization as in the example above.

## Parameter Description

| Parameter | Type | Description |
| --- | --- | --- |
| `index` | Integer | `-1` for software timer; `0` to `5` for hardware timers. |
| `period` | Integer (ms) | Timer period, minimum 5 ms. |
| `freq` | Integer (Hz) | Timer frequency. When set, takes priority over `period`; the actual period is computed as `1000 // freq` milliseconds. |
| `mode` | Constant | `Timer.ONE_SHOT` (single shot) or `Timer.PERIODIC` (periodic). |
| `callback` | Function | Called when the timer expires; receives a `Timer` argument. |
| `hard` | Boolean | Keyword-only argument, defaults to `True`. Determines the Python execution context for the callback. |

## Callback Modes

### `hard=False`: Normal Python Context

Expiry events are first handled by the timer interrupt, then the Python callback is scheduled to run in the normal Python context.

- You can use `print()` and execute regular Python code that allocates memory.
- Callback execution time is affected by system scheduling and Python load, so it is not hard real-time.
- For the same timer, only one pending task is kept while the callback is awaiting execution; if the timer expires too quickly, multiple events may be coalesced or lost.

This is the recommended choice for most Python applications.

### `hard=True`: Interrupt Context

This is the default. The Python callback is invoked directly by the timer interrupt, giving lower latency but with strict limitations:

- The callback must be very short.
- Do not call `print()`, `sleep()`, blocking I/O, network, or filesystem APIs.
- Do not create Python objects or perform operations that may allocate memory.

Violating these restrictions may cause exceptions, lost callbacks, or system instability. When complex processing is needed, a `hard=True` callback may only set a pre-prepared state that the main loop handles; in most cases using `hard=False` directly is more appropriate.

## Mode Details

### One-Shot Mode `Timer.ONE_SHOT`

```python
tim.init(period=100, mode=Timer.ONE_SHOT, callback=func, hard=False)
```

- The timer fires only once.
- It stops automatically after expiring.

### Periodic Mode `Timer.PERIODIC`

```python
tim.init(freq=2, mode=Timer.PERIODIC, callback=func, hard=False)
```

- Fires continuously at the configured period until reinitialized or `deinit()` is called.
- `freq=2` corresponds to approximately 500 ms period.

## Resources and Lifecycle

- Each hardware timer number can only be used by one `Timer`.
- `Timer(-1)` has only one software timer instance; repeated creation will return the same object.
- Calling `init()` again on a running timer will replace the existing configuration.
- `deinit()` will stop the timer and release resources. The released object cannot call `init()` again; a new `Timer` needs to be created.

## Application Scenario Examples

- Periodic sampling: reading sensor data
- Timeout control: handling task execution timeouts
- System heartbeat: periodically updating status or outputting logs
- Low-latency simple interrupt operations: use `hard=True`, and keep callbacks short without allocating memory

```{admonition} Tip
For the complete parameter description of the Timer module, please refer to the [K230 Timer API Documentation](../../api/machine/k230_canmv_timer_api_manual.md)
```
