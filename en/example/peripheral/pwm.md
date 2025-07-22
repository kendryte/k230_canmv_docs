# PWM Example

## Overview

The K230 integrates two PWM hardware modules, each providing 3 output channels. These channels share a clock, but the duty cycle can be adjusted independently. Therefore, channels 0, 1, and 2 share one clock, while channels 3, 4, and 5 share another clock. The configuration of the output IO can be set through the IOMUX module.

## Example

The following example demonstrates how to use the PWM interface for output control.

**Example**

```python
from machine import PWM

# Initialize channel 0, set output frequency to 1 kHz, duty cycle to 50%, and enable it
pwm0 = PWM(0, 1000, 50, enable=True)

# Disable channel 0 output
pwm0.enable(False)

# Set channel 0 output frequency to 2 kHz
pwm0.freq(2000)

# Set channel 0 output duty cycle to 10%
pwm0.duty(10)

# Enable channel 0 output
pwm0.enable(True)

# Release channel 0
pwm0.deinit()
```

## Code Explanation

1. **Initialize PWM Channel**:
   - Create a `PWM` object, specify the channel number (0 in this example), set the initial frequency to 1 kHz, the duty cycle to 50%, and immediately enable the output.

1. **Disable PWM Output**:
   - Call the `enable(False)` method to disable the output of channel 0, which might be necessary to temporarily stop signal output in some situations.

1. **Adjust Frequency and Duty Cycle**:
   - Use the `freq(2000)` method to change the output frequency of channel 0 to 2 kHz.
   - Use the `duty(10)` method to adjust the duty cycle to 10%.

1. **Enable PWM Output**:
   - Use the `enable(True)` method to re-enable the PWM output, starting to send signals with the new frequency and duty cycle.

1. **Release Channel Resources**:
   - Call the `deinit()` method to release the channel, which is usually done when the PWM functionality is no longer needed to free up resources.

```{admonition} Tip
For detailed interfaces and usage of the PWM module, please refer to the [API documentation](../../api/machine/K230_CanMV_PWM_Module_API_Manual.md).
```
