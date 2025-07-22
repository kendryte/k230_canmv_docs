# `Pin` Module API Manual

## Overview

The K230 chip contains 64 GPIO (General Purpose Input/Output) pins, each of which can be configured as either input or output mode, supporting pull-up and pull-down resistor configurations and drive capability settings. These pins can be flexibly used for various digital input/output scenarios.

## API Introduction

The `Pin` class is located in the `machine` module and is used to control the GPIO pins of the K230 chip.

**Example**

```python
from machine import Pin

# Configure pin 2 as output mode, no pull-up/down, drive capability set to 7
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

- `index`: Pin number, range [0, 63].
- `mode`: Pin mode, supports input or output mode.
- `pull`: Pull-up/down configuration (optional), defaults to `Pin.PULL_NONE`.
- `drive`: Drive capability configuration (optional), default value is 7.
- `value`: Default output value
- `alt`: not used

### `init` Method

```python
Pin.init(mode, pull=Pin.PULL_NONE, drive=7)
```

Used to initialize the pin's mode, pull-up/down configuration, and drive capability.

**Parameters**

- `mode`: Pin mode (input or output).
- `pull`: Pull-up/down configuration (optional), default value is `Pin.PULL_NONE`.
- `drive`: Drive capability (optional), default value is 7.

**Return Value**

None

### `value` Method

```python
Pin.value([value])
```

Get the pin's input level or set the pin's output level.

**Parameters**

- `value`: Output value (optional). If this parameter is passed, it sets the pin output to the specified value. If not passed, it returns the current input level of the pin.

**Return Value**

Returns nothing or the current pin input level.

### `mode` Method

```python
Pin.mode([mode])
```

Get or set the pin's mode.

**Parameters**

- `mode`: Pin mode (input or output). If not passed, it returns the current pin mode.

**Return Value**

Returns nothing or the current pin mode.

### `pull` Method

```python
Pin.pull([pull])
```

Get or set the pin's pull-up/down configuration.

**Parameters**

- `pull`: Pull-up/down configuration (optional). If not passed, it returns the current pull-up/down configuration.

**Return Value**

Returns nothing or the current pin pull-up/down configuration.

### `drive` Method

```python
Pin.drive([drive])
```

Get or set the pin's drive capability.

**Parameters**

- `drive`: Drive capability (optional). If not passed, it returns the current drive capability.

**Return Value**

Returns nothing or the current pin drive capability.

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
Pin.irq(handler=None, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, *, priority=1, wake=None, hard=False, debounce=10)
```

Enables IO interrupt functionality.

- `handler`: Callback function (must be specified)
- `trigger`: Trigger mode
- `priority`: Not supported
- `wake`: Not supported
- `hard`: Not supported
- `debounce`: Minimum trigger interval (in milliseconds) for high/low level triggering. Minimum value is `5`.

**Return Value**  
mq_irq object

## Constant Definitions

### Modes

- `Pin.IN`: Input mode  
- `Pin.OUT`: Output mode  

### Pull-up/Pull-down Modes

- `PULL_NONE`: Disable pull-up/pull-down  
- `PULL_UP`: Enable pull-up  
- `PULL_DOWN`: Enable pull-down  

### Interrupt Trigger Modes

- `IRQ_FALLING`: Falling edge trigger  
- `IRQ_RISING`: Rising edge trigger  
- `IRQ_LOW_LEVEL`: Low-level trigger  
- `IRQ_HIGH_LEVEL`: High-level trigger  
- `IRQ_BOTH`: Edge trigger (both rising and falling)  

### Drive Strength  

(Refer to [fpioa](./K230_CanMV_FPIOA_API_Manual.md#31-io-configuration-instructions) for corresponding current output capabilities)  

- `DRIVE_0`  
- `DRIVE_1`  
- `DRIVE_2`  
- `DRIVE_3`  
- `DRIVE_4`  
- `DRIVE_5`  
- `DRIVE_6`  
- `DRIVE_7`  
- `DRIVE_8`  
- `DRIVE_9`  
- `DRIVE_10`  
- `DRIVE_11`  
- `DRIVE_12`  
- `DRIVE_13`  
- `DRIVE_14`  
- `DRIVE_15`
