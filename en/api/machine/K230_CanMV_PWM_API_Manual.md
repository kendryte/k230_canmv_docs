# 2.9 PWM Module API Manual

## 1. Overview

The K230 contains two PWM hardware modules, each with three output channels. The output frequency of each module is adjustable, but the three channels share the same clock, while the duty cycle can be adjusted independently. Therefore, channels 0, 1, and 2 have the same output frequency, and channels 3, 4, and 5 also have the same output frequency. For I/O configuration of channel outputs, please refer to the IOMUX module.

## 2. API Introduction

The PWM class is located in the `machine` module.

### 2.1 Example Code

```python
from machine import PWM

# Initialize channel 0 with an output frequency of 1 kHz, 50% duty cycle, and enable output
pwm0 = PWM(0, 1000, 50, enable=True)

# Disable channel 0 output
pwm0.enable(False)

# Set channel 0 output frequency to 2 kHz
pwm0.freq(2000)

# Set channel 0 output duty cycle to 10%
pwm0.duty(10)

# Re-enable channel 0 output
pwm0.enable(True)

# Release channel 0
pwm0.deinit()
```

### 2.2 Constructor

```python
pwm = PWM(channel, freq, duty=50, enable=False)
```

**Parameters**

- `channel`: PWM channel number, ranging from [0, 5]
- `freq`: PWM channel output frequency
- `duty`: PWM channel output duty cycle, representing the percentage of the high level in the entire period, ranging from [0, 100], optional parameter, default value is 50
- `enable`: Whether to immediately enable PWM channel output, optional parameter, default value is False

### 2.3 `freq` Method

```python
PWM.freq([freq])
```

Get or set the output frequency of the PWM channel.

**Parameters**

- `freq`: PWM channel output frequency, optional parameter. If no parameter is passed, the current frequency is returned.

**Return Value**

Returns the current output frequency of the PWM channel or None.

### 2.4 `duty` Method

```python
PWM.duty([duty])
```

Get or set the duty cycle of the PWM channel.

**Parameters**

- `duty`: PWM channel output duty cycle, optional parameter. If no parameter is passed, the current duty cycle is returned.

**Return Value**

Returns the current output duty cycle of the PWM channel or None.

### 2.5 `enable` Method

```python
PWM.enable(enable)
```

Enable or disable the output of the PWM channel.

**Parameters**

- `enable`: Whether to enable PWM channel output.

**Return Value**

None

### 2.6 `deinit` Method

```python
PWM.deinit()
```

Release the resources of the PWM channel.

**Parameters**

None

**Return Value**

None
