# 2.15 `RTC` Module API Manual

## 1. Overview

The current CanMV K230 provides a class RTC (Real-Time Clock) module, which allows users to set and get the current system time.

## 2. API Introduction

The RTC class is located under the `machine` module.

### 2.1 Example

```python
from machine import RTC

# Instantiate RTC
rtc = RTC()
# Get the current time
print(rtc.datetime())
# Set the current time
rtc.init((2024, 2, 28, 23, 59, 0, 0))
```

### 2.2 Constructor

```python
rtc = RTC()
```

**Parameters**

None

### 2.3 `init` Method

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
- `microsecond`: Microsecond, now ignore this argument
- `tzinfo`: Timezone, value is [-12 ~ 12]

**Return Value**

None

### 2.4 `datetime` Method

```python
print(rtc.datetime())
```

**Parameters**

None

**Return Value**

Returns the current date and time information, including:

- `year`: Year
- `month`: Month
- `day`: Day
- `weekday`: weekday, 1-7
- `hour`: Hour
- `minute`: Minute
- `second`: Second
- `microsecond`: Microsecond
