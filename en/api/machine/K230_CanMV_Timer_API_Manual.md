# `Timer` Module API Manual

## Overview

The K230 integrates 6 Timer hardware modules internally, with a minimum timing period of 1 millisecond (ms).

## API Introduction

The Timer class is located in the `machine` module.

### Example Code

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

### Constructor

```python
timer = Timer(index, mode=Timer.PERIODIC, freq=-1, period=-1, callback=None)
```

**Parameters**

- `index`: Timer module number, range is [-1, 5], where -1 represents a software timer.
- `mode`: Timer operating mode, can be one-shot or periodic (optional parameter).
- `freq`: Timer operating frequency, supports floating-point numbers, unit is Hertz (Hz), this parameter has a higher priority than `period` (optional parameter).
- `period`: Timer operating period, unit is milliseconds (ms) (optional parameter).
- `callback`: Timeout callback function, must be set and should have one parameter.

### `init` Method

```python
Timer.init(mode=Timer.PERIODIC, freq=-1, period=-1, callback=None)
```

Initialize timer parameters.

**Parameters**

- `mode`: Timer operating mode, can be one-shot or periodic (optional parameter).
- `freq`: Timer operating frequency, supports floating-point numbers, unit is Hertz (Hz), this parameter has a higher priority than `period` (optional parameter).
- `period`: Timer operating period, unit is milliseconds (ms) (optional parameter).
- `callback`: Timeout callback function, must be set and should have one parameter.
- `arg`: Argument for the timeout callback function (optional parameter).

**Return Value**

None

### `deinit` Method

```python
Timer.deinit()
```

Release timer resources.

**Parameters**

None

**Return Value**

None
