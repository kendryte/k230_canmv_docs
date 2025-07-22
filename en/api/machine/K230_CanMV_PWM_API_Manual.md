# `PWM` Module API Manual  

## Overview  

The K230 integrates two PWM hardware modules, each with three output channels. The output frequency of each module is adjustable, but the three channels share the same clock, while the duty cycle can be independently configured. Therefore, channels 0, 1, and 2 share the same output frequency, and channels 3, 4, and 5 also share the same output frequency. For the I/O configuration of the channel outputs, refer to the IOMUX module.  

## API Introduction  

The PWM class is located in the `machine` module.  

### Example Code  

```python  
import time  
from machine import PWM  
from machine import FPIOA  

# Instantiate FPIOA  
fpioa = FPIOA()  

# Set PIN42 as PWM channel 0  
fpioa.set_function(42, fpioa.PWM0)  

# Instantiate PWM channel 0 with a frequency of 1000Hz and a duty cycle of 50% (enabled by default)  
pwm0 = PWM(0)  

# Adjust the frequency of channel 0 to 2000Hz  
pwm0.freq(2000)  

# Adjust the duty cycle of channel 0 to 50% (32768 / 65535)  
pwm0.duty_u16(32768)  
print(pwm0.duty_u16())  

# Output for 1 second and then disable  
time.sleep(1)  
pwm0.deinit()  
time.sleep(1)  

# Adjust channel 0 frequency to 10KHz with a duty cycle of 30%  
pwm0.freq(10000)  
pwm0.duty(30)  
print(pwm0.duty())  

# Output for 1 second and then disable  
time.sleep(1)  
pwm0.deinit()  
```  

### Constructor  

```python  
pwm = PWM(channel, freq = -1, duty = -1, duty_u16 = -1, duty_ns = -1)  
```  

**Parameters**  

- `channel`: PWM channel number, range [0, 5]  
- `freq`: PWM channel output frequency  
- `duty`: PWM channel duty cycle, representing the percentage of high-level duration in the entire period, range [0, 100]  
- `duty_ns`: PWM channel high-level duration in nanoseconds (`ns`)  
- `duty_u16`: PWM channel high-level duration, range [0, 65535]  

> Only one of `duty`, `duty_ns`, or `duty_u16` can be set at a time.  

### `init` Method  

```python  
PWM.init(freq = -1, duty = -1, duty_u16 = -1, duty_ns = -1)  
```  

**Parameters**  

Refer to [Constructor](#constructor).  

### `deinit` Method  

```python  
PWM.deinit()  
```  

Release the resources of the PWM channel.  

**Parameters**  

None  

**Return Value**  

None  

### `freq` Method  

```python  
PWM.freq([freq])  
```  

Get or set the output frequency of the PWM channel.  

**Parameters**  

- `freq`: PWM channel output frequency (optional). If no argument is provided, returns the current frequency.  

**Return Value**  

Returns the current PWM channel output frequency or `None`.  

### `duty` Method  

```python  
PWM.duty([duty])  
```  

Get or set the duty cycle of the PWM channel.  

**Parameters**  

- `duty`: PWM channel duty cycle (optional). If no argument is provided, returns the current duty cycle.  

**Return Value**  

Returns the current PWM channel duty cycle or `None`.  

### `duty_u16` Method  

```python  
PWM.duty_u16([duty_u16])  
```  

Get or set the duty cycle of the PWM channel.  

**Parameters**  

- `duty_u16`: PWM channel duty cycle (optional). If no argument is provided, returns the current duty cycle.  

**Return Value**  

Returns the current PWM channel duty cycle or `None`.  

### `duty_ns` Method  

```python  
PWM.duty_ns([duty_ns])  
```  

Get or set the duty cycle of the PWM channel.  

**Parameters**  

- `duty_ns`: PWM channel duty cycle in nanoseconds (optional). If no argument is provided, returns the current duty cycle.  

**Return Value**  

Returns the current PWM channel duty cycle or `None`.
