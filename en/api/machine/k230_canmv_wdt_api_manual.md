# `WDT` Module API Manual

## Overview

The K230 integrates two WDT (Watchdog Timer) hardware modules internally, designed to ensure that the system can restart when an application crashes and enters an unrecoverable state. After the WDT is started, if the "feed dog" operation is not performed periodically during hardware runtime, the system will automatically reset after a timeout.

## API Introduction

The WDT class is located in the `machine` module.

### Example Code

```python
from machine import WDT

# 实例化 WDT1，超时时间为 3 秒
wdt1 = WDT(1, 3)

# 执行喂狗操作
wdt1.feed()
```

### Constructor

```python
wdt = WDT(id=1, timeout=5, auto_close = True)
```

**Parameters**

- `id`: WDT module number, with a value range of [0, 1], default is 1.
- `timeout`: Timeout value, in seconds (s), default is 5.
- `auto_close`: Automatically stops the watchdog when the `python` interpreter stops running, to prevent the system from being restarted

**Note:** WDT0 is currently unavailable.

### `feed` Method

```python
WDT.feed()
```

Performs the feed dog operation.

**Parameters**

None

**Return Value**

None
