# 2.12 WDT Module API Manual

## 1. Overview

The K230 integrates two WDT (Watchdog Timer) hardware modules internally, designed to ensure the system can reboot when the application crashes and enters an unrecoverable state. Once the WDT is started, if the hardware is not periodically "fed" during operation, it will automatically reset the system after a timeout.

## 2. API Introduction

The WDT class is located in the `machine` module.

### 2.1 Example Code

```python
from machine import WDT

# Instantiate WDT1 with a timeout of 3 seconds
wdt1 = WDT(1, 3)

# Perform the feed operation
wdt1.feed()
```

### 2.2 Constructor

```python
wdt = WDT(id=1, timeout=5)
```

**Parameters**

- `id`: WDT module number, range is [0, 1], default is 1.
- `timeout`: Timeout value in seconds (s), default is 5.

**Note:** WDT0 is currently unavailable.

### 2.3 `feed` Method

```python
WDT.feed()
```

Performs the feed operation.

**Parameters**

None

**Return Value**

None
