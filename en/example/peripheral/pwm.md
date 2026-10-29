# PWM Usage Tutorial

## What is PWM?

**PWM (Pulse Width Modulation)**
is a method of simulating analog signals by controlling the **high/low level ratio (duty cycle)** of a digital signal. It is commonly used for:

- Controlling LED brightness
- Driving motor speed
- Adjusting audio volume
- Generating tones/square wave signals

The K230 integrates two PWM hardware modules internally, each supporting 3 channels (6 channels in total):

- Channels **0\~2** share the same clock source (same frequency, with separate duty cycle settings)
- Channels **3\~5** use another independent clock source
- Each channel can be configured to different output pins via `IOMUX`

## Example Overview

The following example demonstrates how to use the K230's `PWM` module to perform the following operations:

- Initialize and start PWM output
- Dynamically adjust frequency and duty cycle
- Release PWM channel resources

### 1. Import Module and Initialize PWM

```python
from machine import PWM, Pin

# Initialize PWM channel 0, set frequency to 1kHz, duty cycle to 50%
pwm0 = PWM(Pin(42), freq=1000, duty=50)
```

- `PWM(channel number, frequency Hz, duty cycle %)`
  Creates a PWM output for the specified channel, outputting a 1kHz square wave with a 50% duty cycle

### 2. Dynamically Adjust Frequency and Duty Cycle

```python
# Modify channel 0's output frequency to 2kHz
pwm0.freq(2000)

# Modify duty cycle to 10%
pwm0.duty(10)
```

- `freq(x)`: Set output frequency (unit: Hz)
- `duty(x)`: Set duty cycle (unit: %, range 0\~100)

### 3. Release Channel Resources

```python
# Completely release channel 0, turn off output and free underlying resources
pwm0.deinit()
```

- `deinit()`: Close the channel, free resources, suitable for exit scenarios or switching functions

### 4. Example Output Waveform Description

Assume we set channel 0 to output a 1kHz, 50% duty cycle PWM waveform. The waveform is:

```text
Period T = 1ms
High level time = 0.5ms, Low level time = 0.5ms
```

```python
|‾‾‾‾‾     ‾‾‾‾‾     ‾‾‾‾‾
|     ‾‾‾‾‾     ‾‾‾‾‾     
```

If the duty cycle is adjusted to 10%, the waveform is as follows:

```text
|‾     ‾     ‾     ‾
|                         
```

## PWM Channel Description

| Channel Number | Module | Clock Sharing Group |
|-  | - | - |
| 0   | PWM0 | Group A |
| 1   | PWM0 | Group A |
| 2   | PWM0 | Group A |
| 3   | PWM1 | Group B |
| 4   | PWM1 | Group B |
| 5   | PWM1 | Group B |

> ⚠ Note: Channels in the same group share one frequency, but **the duty cycle can be set independently**

## Application Scenarios

- **LED Brightness Control** (control brightness through duty cycle)
- **Buzzer Sound** (control pitch through frequency)
- **Servo Control** (specific duty cycle controls rotation angle)
- **DC Motor Speed Control** (control average voltage through PWM)
- **Signal Waveform Generator** (square wave, PWM modulated wave, etc.)

## Further Reading

- [K230 PWM API Documentation](../../api/machine/k230_canmv_pwm_api_manual.md)
- [FPIOA Module Complete API Manual](../../api/machine/k230_canmv_fpioa_api_manual.md)
