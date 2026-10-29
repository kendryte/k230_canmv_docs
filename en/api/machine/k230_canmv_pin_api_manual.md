# `Pin` Module API Manual

## Overview

The K230 chip contains 64 GPIO (General Purpose Input/Output) pins internally, each of which can be configured as input or output mode, and supports pull-up/pull-down resistor configuration and drive capability settings. These pins can be flexibly used in various digital input and output scenarios.

## API Introduction

The `Pin` class is located in the `machine` module and is used to control the GPIO pins of the K230 chip.

**Example**

```python
from machine import Pin

# Configure pin 2 as output mode, no pull-up/pull-down, drive capability of 7
pin = Pin(2, Pin.OUT, pull=Pin.PULL_NONE, drive=7)

# Set pin 2 to output high level
pin.value(1)

# Set pin 2 to output low level
pin.value(0)
```

### Constructor

```python
pin = Pin(index, mode, pull=Pin.PULL_NONE, value = -1, drive=7, alt = -1)
```

**Parameters**

- `index`: Pin number, range is [0, 63].
- `mode`: Pin mode, supports input mode or output mode.
- `pull`: Pull-up/pull-down configuration (optional), default is `Pin.PULL_NONE`.
- `drive`: Drive capability configuration (optional), default value is 7.
- `value`: Sets the default output value of the pin
- `alt`: Currently not used

### `init` Method

```python
Pin.init(mode, pull=Pin.PULL_NONE, drive=7)
```

Used to initialize the pin's mode, pull-up/pull-down configuration, and drive capability.

**Parameters**

- `mode`: Pin mode (input or output).
- `pull`: Pull-up/pull-down configuration (optional), default value is `Pin.PULL_NONE`.
- `drive`: Drive capability (optional), default value is 7.

**Return Value**

None

### `value` Method

```python
Pin.value([value])
```

Get the input level value of the pin or set the output level of the pin.

**Parameters**

- `value`: Output value (optional). If this parameter is passed, the pin output is set to the specified value. If no parameter is passed, the current input level value of the pin is returned.

**Return Value**

Returns empty or the current input level value of the pin.

### `mode` Method

```python
Pin.mode([mode])
```

Get or set the pin mode.

**Parameters**

- `mode`: Pin mode (input or output). If no parameter is passed, the current pin mode is returned.

**Return Value**

Returns empty or the current pin mode.

### `pull` Method

```python
Pin.pull([pull])
```

Get or set the pin's pull-up/pull-down configuration.

**Parameters**

- `pull`: Pull-up/pull-down configuration (optional). If no parameter is passed, the current pull-up/pull-down configuration is returned.

**Return Value**

Returns empty or the current pull-up/pull-down configuration of the pin.

### `drive` Method

```python
Pin.drive([drive])
```

Get or set the pin's drive capability.

**Parameters**

- `drive`: Drive capability (optional). If no parameter is passed, the current drive capability is returned.

**Return Value**

Returns empty or the current drive capability of the pin.

### `on` Method

```python
Pin.on()
```

Set the pin output to high level.

**Parameters**

None

**Return Value**

None

### `off` Method

```python
Pin.off()
```

Set the pin output to low level.

**Parameters**

None

**Return Value**

None

### `high` Method

```python
Pin.high()
```

Set the pin output to high level.

**Parameters**

None

**Return Value**

None

### `low` Method

```python
Pin.low()
```

Set the pin output to low level.

**Parameters**

None

**Return Value**

None

### `irq` Method

```python
Pin.irq(handler=None, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, *, priority=1, wake=None, hard=False, debounce = 10)
```

Enable the IO interrupt function

- `handler`: Callback function, must be set
- `trigger`: Trigger mode
- `priority`: Not supported
- `wake`: Not supported
- `hard`: Not supported
- `debounce`: For high level and low level triggers, the minimum trigger interval, in `ms`, minimum value is `5`

**Return Value**

mq_irq object

## Constant Definitions

### Mode

- Pin.IN: Input mode
- Pin.OUT: Output mode

### Pull-up/Pull-down Mode

- PULL_NONE: Disable pull-up/pull-down
- PULL_UP: Enable pull-up
- PULL_DOWN: Enable pull-down

### Interrupt Trigger Mode

- IRQ_FALLING: Falling edge trigger
- IRQ_RISING: Rising edge trigger
- IRQ_LOW_LEVEL: Low level trigger
- IRQ_HIGH_LEVEL: High level trigger
- IRQ_BOTH: Edge trigger

### Drive Strength

For the specific current output capability corresponding to each configuration, refer to [fpioa](./k230_canmv_fpioa_api_manual.md#io-configuration)

- DRIVE_0
- DRIVE_1
- DRIVE_2
- DRIVE_3
- DRIVE_4
- DRIVE_5
- DRIVE_6
- DRIVE_7
- DRIVE_8
- DRIVE_9
- DRIVE_10
- DRIVE_11
- DRIVE_12
- DRIVE_13
- DRIVE_14
- DRIVE_15
