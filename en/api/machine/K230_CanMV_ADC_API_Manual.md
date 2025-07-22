# `ADC` Module API Manual

## Overview

The K230 processor integrates an internal ADC (Analog-to-Digital Converter) hardware module, providing 6 independent channels. The module has a sampling resolution of 12 bits, meaning the output range is 0-4095, with a sampling rate of 1 MHz.

## API Introduction

The ADC class belongs to the `machine` module.

### Example

```python
from machine import ADC

# Instantiate ADC channel 0
adc = ADC(0)

# Get the sampling value of ADC channel 0
print(adc.read_u16())

# Get the voltage value of ADC channel 0 (in microvolts)
print(adc.read_uv(), "uV")
```

### Constructor

```python
adc = ADC(channel)
```

**Parameters**

- `channel`: Indicates the ADC channel number to use, ranging from [0, 5].

### `read_u16`

```python
ADC.read_u16()
```

#### Function

Gets the current sampling value of the specified channel.

**Parameters**

None

**Return Value**

Returns the sampling value of the ADC channel, ranging from [0, 4095].

### `read_uv`

```python
ADC.read_uv()
```

#### Function

Gets the current voltage value (in microvolts) of the specified channel.

**Parameters**

None

**Return Value**

Returns the voltage value of the ADC channel, in microvolts (uV), ranging from [0, 1800000] microvolts.
