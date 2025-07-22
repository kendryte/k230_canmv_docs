# ADC Example

## Overview

The K230 integrates an internal ADC hardware module, providing 6 channels. It has a sampling resolution of 12 bits (range 0-4095) and a sampling rate of up to 1 MHz.

## Example

The following example demonstrates how to use the ADC interface to read sampling values and voltage.

```python
from machine import ADC

# Instantiate ADC channel 0
adc = ADC(0)

# Get the sampling value of ADC channel 0
print(adc.read_u16())

# Get the voltage value of ADC channel 0
print(adc.read_uv(), "uV")
```

## Code Explanation

1. **Instantiate ADC**:
   - Create an `ADC` object and specify the channel number (0 in this example) to access the ADC functionality of that channel.

1. **Read Sampling Value**:
   - Call the `read_u16()` method to get the current sampling value of ADC channel 0. The returned value ranges from 0 to 4095, representing the intensity of the analog signal.

1. **Read Voltage Value**:
   - Call the `read_uv()` method to get the voltage value of channel 0. The returned value is in microvolts (uV), providing a more intuitive voltage representation.

```{admonition} Tip
For detailed interfaces and usage of the ADC module, please refer to the [API documentation](../../api/machine/K230_CanMV_ADC_Module_API_Manual.md)
```
