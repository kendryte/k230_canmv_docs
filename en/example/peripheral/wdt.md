# WDT Routines

## Overview

The K230 contains two WDT (Watchdog Timer) hardware modules, primarily used to restart the system when the application crashes or enters an unrecoverable state. Once the WDT is activated, if no "feed dog" operation is performed within the set timeout period, the system will automatically reset.

## Example

The following example demonstrates how to use the WDT interface for a simple watchdog functionality test.

```python
import time
from machine import WDT

# Instantiate WDT1 with a timeout of 3 seconds
wdt1 = WDT(1, 3)

# Wait for 2 seconds
time.sleep(2)

# Feed the dog operation, reset the WDT timer
wdt1.feed()

# Wait for another 2 seconds
time.sleep(2)
```

## Code Explanation

1. **Instantiate WDT**:
   - Create a `WDT` object with parameters for the WDT number and timeout period (in seconds). In this example, the timeout is set to 3 seconds.

1. **Delay Operation**:
   - `time.sleep(2)` pauses execution for 2 seconds. During this period, if no feed dog operation is performed, the WDT will count to 3 seconds and then restart the system.

1. **Feed Dog Operation**:
   - Call the `wdt1.feed()` method to reset the WDT timer to prevent a timeout restart.

1. **Second Delay**:
   - Pause for another 2 seconds. Since no `feed()` operation is called this time, the WDT will trigger a restart after the timeout.

```{admonition} Tip
For detailed WDT module interface, please refer to the [API documentation](../../api/machine/K230_CanMV_WDT_Module_API_Manual.md)
```
