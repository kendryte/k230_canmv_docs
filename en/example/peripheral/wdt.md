# WDT Watchdog Tutorial

## What is WDT?

**WDT (Watchdog Timer)**
is a defensive mechanism for system stability, ensuring that when a program encounters an exception (such as an infinite loop or freeze), the system can automatically restart to resume operation.

Typical uses include:

- Preventing embedded devices from being stuck for long periods
- Ensuring programs respond in a timely manner in mission-critical tasks
- A core component of the system self-recovery mechanism

## K230 WDT Features

| Feature | Description |
| ------ | --------------------------- |
| Supported channels | Built-in **2 WDT channels** (WDT0 / WDT1) |
| Minimum timeout | Second-level precision, timeout is usually 1 second or more |
| Reset mechanism | Automatically triggers **system reset** upon timeout |
| Manual feeding | Call the `feed()` method to reset the timer before the timeout |

## Application Example: Basic Watchdog Test

The following example sets a 3-second timeout through WDT1, and simulates a "feed the dog" operation in the program to prevent the system from restarting.

### Example Code

```python
import time
from machine import WDT

# ========== Initialize WDT1 ==========
wdt1 = WDT(1, 3)  # Channel 1, timeout 3 seconds

# ========== Wait 2 seconds ==========
time.sleep(2)

# ========== Feed the dog operation ==========
wdt1.feed()       # Reset the watchdog counter to avoid triggering a system reset

# ========== Wait another 2 seconds ==========
time.sleep(2)

# If feed() is not called again, the system will automatically restart after 3 seconds
```

## Interface Description

| Method Name                | Description                                              |
| ----------------------- | -------------------------------------------------- |
| `WDT(channel, timeout)` | Create a watchdog object, with parameters being the channel number and timeout duration (in seconds) |
| `feed()`                | Feed the watchdog operation, resets the countdown counter               |

## Usage Recommendations

| Scenario                  | Recommended Operation                          |
| --------------------- | ---------------------------------------- |
| System task deadlock prevention | Call `feed()` in each main loop to feed the watchdog       |
| Serial/Network stall detection | Feed the watchdog only after successfully receiving data     |
| Multi-threaded applications    | Use a message queue to notify the main thread to feed the watchdog periodically |

## Frequently Asked Questions and Troubleshooting

| Issue                           | Cause and Solution                                |
| ---------------------------- | ----------------------------------------- |
| Program auto-restarts after running for a while | The watchdog was not fed, and the timeout reset has been triggered         |
| Still restarts after feeding the watchdog        | Feed frequency is lower than the timeout, or the call location is not in the main loop |
| Want to disable the watchdog                     | K230 currently has no disable interface; it is recommended to adapt and avoid it at the logic level |

## Further Reading

- [K230 WDT API Documentation](../../api/machine/k230_canmv_wdt_api_manual.md)
