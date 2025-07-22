# GPIO Example

## Overview

The K230 chip integrates 64 GPIO pins, each of which can be configured as either input or output mode. It also supports pull-up and pull-down resistor configurations as well as drive strength settings. The flexible configuration of GPIO pins makes it widely applicable in various scenarios.

## Example

The following code example demonstrates how to configure and control GPIO pins using the GPIO module:

```python
from machine import Pin

# Instantiate Pin2 as output mode, configure it with no pull-up/pull-down (PULL_NONE), and set drive strength to 7
pin = Pin(2, Pin.OUT, pull=Pin.PULL_NONE, drive=7)

# Set Pin2 to output high level
pin.value(1)

# Set Pin2 to output low level
pin.value(0)
```

```{admonition} Note
For detailed interface and functionality descriptions of the Pin module, please refer to the [API documentation](../../api/machine/K230_CanMV_Pin_Module_API_Manual.md).
```
