# `RTC` Module API Manual

## Overview

The current CanMV K230 provides an RTC (Real-Time Clock) module, which users can use to set and get the current system time.

## API Introduction

The RTC class is located under the `machine` module.

### Example

```python
from machine import RTC

# Instantiate RTC
rtc = RTC()
# Get current time
print(rtc.datetime())
# Set current time
rtc.init((2024, 2, 28, 2, 23, 59, 0, 0))
```

### Constructor

```python
rtc = RTC()
```

**Parameters**

None

### `init` Method

```python
rtc.init(year, month, day, hour, minute, second, microsecond, tzinfo)
```

**Parameters**

- `year`: Year
- `month`: Month
- `day`: Day
- `hour`: Hour
- `minute`: Minute
- `second`: Second
- `microsecond`: Microsecond, this parameter is ignored
- `tzinfo`: Timezone, value range [-12 ~ 12]

**Return Value**

None

### `datetime` Method

```python
print(rtc.datetime())
```

**Parameters**

None

**Return Value**

Returns the current date and time information, including:

- `year`: Year
- `mon`: Month
- `day`: Day
- `wday`: Day of the week
- `hour`: Hour
- `min`: Minute
- `sec`: Second
- `microsec`: Microsecond
