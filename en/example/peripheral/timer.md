# TIMER Example

## Overview

The K230 contains 6 Timer hardware modules with a minimum timing period of 1 microsecond. These timers enable precise timing and periodic tasks.

## Example

The following example demonstrates how to use the Timer module for timing operations.

```python
from machine import Timer
import time

# Instantiate a software timer
tim = Timer(-1)

# Initialize the timer in one-shot mode with a period of 100ms
tim.init(period=100, mode=Timer.ONE_SHOT, callback=lambda t: print(1))
time.sleep(0.2)

# Initialize the timer in periodic mode with a frequency of 1Hz
tim.init(freq=1, mode=Timer.PERIODIC, callback=lambda t: print(2))
time.sleep(2)

# Release timer resources
tim.deinit()
```

## Code Explanation

1. **Instantiate Timer**:
   - Create a `Timer` object, `-1` indicates using a software timer.

1. **One-shot Mode Timer**:
   - Use `tim.init(period=100, mode=Timer.ONE_SHOT, callback=lambda t: print(1))` to initialize the timer with a period of 100 milliseconds. The callback function will output `1` when the timer expires.

1. **Delay**:
   - `time.sleep(0.2)` pauses for 200 milliseconds to ensure the timer callback output can be observed.

1. **Periodic Mode Timer**:
   - Use `tim.init(freq=1, mode=Timer.PERIODIC, callback=lambda t: print(2))` to initialize the timer with a frequency of 1Hz. The timer triggers the callback every second, outputting `2`.

1. **Another Delay**:
   - `time.sleep(2)` pauses for 2 seconds to observe the output of the periodic mode timer.

1. **Release Resources**:
   - Call `tim.deinit()` to release timer resources and stop all timer operations.

```{admonition} Note
For detailed Timer module interfaces, please refer to the [API Documentation](../../api/machine/K230_CanMV_Timer_Module_API_Manual.md)
```
