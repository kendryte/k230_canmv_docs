# 1. FPIOA Example

## 1. Overview

IOMUX is mainly used to configure the functions of physical pins (PAD). In a SoC, due to the large number of functions and limited number of pins, multiple functions may share the same I/O pin. However, at any given time, a pin can only carry one function, so it is necessary to select the function through IOMUX (also known as FPIOA, Pin multiplexing, pin function selection, etc.).

## 2. Example

The following code demonstrates how to use the FPIOA module to set and query the functions of pins:

```python
from machine import FPIOA

# Instantiate FPIOA object
fpioa = FPIOA()

# Print the configuration status of all pins
fpioa.help()

# Print the detailed configuration of a specific pin (Pin0)
fpioa.help(0)

# Print all available pins corresponding to a specific function (e.g., IIC0_SDA)
fpioa.help(FPIOA.IIC0_SDA, func=True)

# Set Pin0 to GPIO0
fpioa.set_function(0, FPIOA.GPIO0)

# Set Pin2 to GPIO2 and configure other options simultaneously
fpioa.set_function(2, FPIOA.GPIO2, ie=1, oe=1, pu=0, pd=0, st=1, sl=0, ds=7)

# Get the current pin number for a specific function (e.g., UART0_TXD)
fpioa.get_pin_num(FPIOA.UART0_TXD)

# Get the current function configuration of a specific pin (Pin0)
fpioa.get_pin_func(0)
```

```{admonition} Tip
For specific interface descriptions of the FPIOA module, please refer to the [API documentation](../../api/machine/K230_CanMV_FPIOA_Module_API_Manual.md).
```
