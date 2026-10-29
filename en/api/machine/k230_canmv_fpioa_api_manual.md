# `FPIOA` Module API Manual

## Overview

The FPIOA (Pin Multiplexer) module is primarily responsible for configuring the functions of physical pins (PAD). In an SoC, although multiple functions are available, due to the limited number of pins, several functions may share the same I/O pin. In such cases, only one function can be activated on each pin at any given time, so the appropriate function needs to be selected through IOMUX (i.e., FPIOA).

## API Introduction

The FPIOA class is located in the `machine` module.

**Example**

```python
from machine import FPIOA

# Instantiate the FPIOA object
fpioa = FPIOA()

# Print the configuration of all pins
fpioa.help()

# Print the detailed configuration of the specified pin
fpioa.help(0)

# Print all configurable pins for the specified function
fpioa.help(FPIOA.IIC0_SDA, func=True)

# Set Pin0 to GPIO0
fpioa.set_function(0, FPIOA.GPIO0)

# Set Pin2 to GPIO2, and configure other parameters
fpioa.set_function(2, FPIOA.GPIO2, ie=1, oe=1, pu=0, pd=0, st=1, ds=7)

# Get the pin currently used by the specified function
fpioa.get_pin_num(FPIOA.UART0_TXD)

# Get the current function of the specified pin
fpioa.get_pin_func(0)
```

### Constructor

```python
fpioa = FPIOA()
```

**Parameters**

None

### `set_function` Method

```python
FPIOA.set_function(pin, func, ie=-1, oe=-1, pu=-1, pd=-1, st=-1, ds=-1)
```

Sets the function of a pin.

**Parameters**

- `pin`: Pin number, range: [0, 63]
- `func`: Function number
- `ie`: Input enable, optional parameter
- `oe`: Output enable, optional parameter
- `pu`: Pull-up enable, optional parameter
- `pd`: Pull-down enable, optional parameter
- `st`: Schmitt trigger enable, optional parameter
- `ds`: Drive strength, optional parameter

For more details, refer to [IO Drive Strength](#io-configuration)

**Return Value**

None

### `get_pin_num` Method

```python
fpioa.get_pin_num(func)
```

Gets the pin currently used by the specified function.

**Parameters**

- `func`: Function number

**Return Value**

Returns the pin number, or `None` if the corresponding function is not found.

### `get_pin_func` Method

```python
fpioa.get_pin_func(pin)
```

Gets the current function of the specified pin.

**Parameters**

- `pin`: Pin number

**Return Value**

Returns the current function number of the pin.

### `help` Method

```python
fpioa.help([number, func=False])
```

Prints pin configuration hints.

**Parameters**

- `number`: Pin number or function number, optional parameter
- `func`: Whether to enable function number query, defaults to `False`

**Return Value**

One of the following three:

1. Configuration information for all pins (`number` not set)
1. Detailed configuration information for the specified pin (`number` is set, `func` is not set or set to `False`)
1. All configurable pin numbers for the specified function (`number` is set, and `func` is set to `True`)

## Appendix

<a id="io-configuration"></a>

### IO Configuration Description

![io-ds](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/7d3661a9530f.jpg)
