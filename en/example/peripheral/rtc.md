# RTC Real-Time Clock Usage Tutorial

## What is RTC?

**RTC (Real-Time Clock)**
is a clock module independent of the main processor, used to track the current date and time, retaining the set time even after a system restart (if battery-powered). It is widely used in:

- Data timestamp recording (e.g., logs)
- Scheduled trigger control
- Low-power wake-up scenarios

## K230 RTC Features

| Feature       | Description                                                |
| --------- | --------------------------------------------------- |
| Module Support | K230 has 1 built-in RTC module                          |
| Precision     | Second-level precision, supports setting to microseconds        |
| Typical Applications | Time synchronization, date display, event scheduling             |
| Time Format   | Returns tuple format `(year, month, day, weekday, hour, minute, second, microsecond)` |

## Application Example: Getting and Setting System Time

This example demonstrates how to use the `RTC` module to set and read the system time.

### Example Code

```python
from machine import RTC

# ========== Initialize RTC ==========
rtc = RTC()

# ========== Get Current Time ==========
print("Current time:", rtc.datetime())

# ========== Set Current Time ==========
# Set to: February 28, 2024 (Wednesday) 23:59:00.000000
rtc.init((2024, 2, 28, 2, 23, 59, 0, 0))
print("After new time set:", rtc.datetime())
```

## Interface Description

| Method Name         | Description                                                |
| ---------------- | ------------------------------------------------- |
| `RTC()`          | Create RTC instance                                         |
| `datetime()`     | Get the current RTC time, return a tuple                                  |
| `init(datetime)` | Set the RTC time, the parameter is an 8-element tuple `(year, month, day, weekday, hour, minute, second, microsecond)` |

## Example Analysis

1. **Initialize RTC Object**
   `rtc = RTC()` creates and binds a real-time clock instance.

1. **Get Current Time**
   `rtc.datetime()` returns the current set time tuple, e.g., `(2024, 2, 28, 2, 23, 59, 0, 0)` represents February 28, 2024, Wednesday 23:59:00.

1. **Set Current Time**
   `rtc.init(...)` can set a new time, usually used to synchronize an external time source at program startup.

## Time Tuple Description

| Index | Meaning | Example Value      |
| -- | -- | -------- |
| 0  | Year  | 2024     |
| 1  | Month  | 2        |
| 2  | Day  | 28       |
| 3  | Weekday | 2 (0=Sunday) |
| 4  | Hour | 23       |
| 5  | Minute | 59       |
| 6  | Second  | 0        |
| 7  | Microsecond | 0        |

## Further Reading

- [K230 RTC API Documentation](../../api/machine/k230_canmv_rtc_api_manual.md)
