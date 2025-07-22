# RTC Example

## Overview

The K230 provides an RTC (Real-Time Clock) module that allows users to set and get the current system time, suitable for applications that require time tracking.

## Example

The following example demonstrates how to use the RTC interface to get and set the system time.

```python
from machine import RTC

# Instantiate RTC
rtc = RTC()

# Get current time
print(rtc.datetime())

# Set current time
rtc.init((2024, 2, 28, 2, 23, 59, 0, 0))
```

## Code Explanation

1. **Instantiate RTC**:
   - Create an `RTC` object to access RTC functionalities.

1. **Get current time**:
   - Call the `datetime()` method to get the current system time, which returns in the format `(year, month, day, weekday, hour, minute, second, microsecond)`.

1. **Set current time**:
   - Call the `init()` method to set the current time. The tuple parameter includes the year, month, day, weekday, hour, minute, second, and microsecond.

```{admonition} Tip
For detailed interfaces and usage of the RTC module, please refer to the [API documentation](../../api/machine/K230_CanMV_RTC_Module_API_Manual.md)
```
