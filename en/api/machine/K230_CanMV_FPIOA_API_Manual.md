# 2.8 `FPIOA` Module API Manual

## 1. Overview

The FPIOA (Pin Multiplexer) module is primarily responsible for configuring the functions of physical pins (PAD). In an SoC, although multiple functions are available, due to the limited number of pins, multiple functions may share the same I/O pin. At this point, each pin can only activate one function at a time, so it is necessary to use IOMUX (i.e., FPIOA) to select the appropriate function.

## 2. API Introduction

The FPIOA class is located in the `machine` module.

**Example**

```python
from machine import FPIOA

# Instantiate an FPIOA object
fpioa = FPIOA()

# Print the configuration of all pins
fpioa.help()

# Print detailed configuration of a specified pin
fpioa.help(0)

# Print all available configuration pins for a specified function
fpioa.help(FPIOA.IIC0_SDA, func=True)

# Set Pin0 to GPIO0
fpioa.set_function(0, FPIOA.GPIO0)

# Set Pin2 to GPIO2, while configuring other parameters
fpioa.set_function(2, FPIOA.GPIO2, ie=1, oe=1, pu=0, pd=0, st=1, sl=0, ds=7)

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
FPIOA.set_function(pin, func, ie=-1, oe=-1, pu=-1, pd=-1, st=-1, sl=-1, ds=-1)
```

Set the function of a pin.

**Parameters**

- `pin`: Pin number, range: [0, 63]
- `func`: Function number
- `ie`: Input enable, optional parameter
- `oe`: Output enable, optional parameter
- `pu`: Pull-up enable, optional parameter
- `pd`: Pull-down enable, optional parameter
- `st`: St enable, optional parameter
- `ds`: Drive strength, optional parameter

More detail,  See [IO configuration instructions](#31-io-configuration-instructions)

**Return Value**

None

### `get_pin_num` Method

```python
fpioa.get_pin_num(func)
```

Get the pin currently used by the specified function.

**Parameters**

- `func`: Function number

**Return Value**

Returns the pin number, or `None` if the corresponding function is not found.

### `get_pin_func` Method

```python
fpioa.get_pin_func(pin)
```

Get the current function of the specified pin.

**Parameters**

- `pin`: Pin number

**Return Value**

Returns the current function number of the pin.

### `help` Method

```python
fpioa.help([number, func=False])
```

Print pin configuration help information.

**Parameters**

- `number`: Pin number or function number, optional parameter
- `func`: Whether to enable function number query, default is `False`

**Return Value**

May be one of the following three:

1. Configuration information of all pins (if `number` is not set)
1. Detailed configuration information of the specified pin (if `number` is set, `func` is not set or set to `False`)
1. All configurable pin numbers for the specified function (if `number` is set and `func` is set to `True`)

## 3. Appendix

### 3.1 IO configuration instructions

![io-ds](https://www.kendryte.com/api/post/attachment?id=436)
