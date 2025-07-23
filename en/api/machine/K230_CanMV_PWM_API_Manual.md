# `PWM` Module API Manual  

## Overview  

The K230 integrates two PWM hardware modules, each with three output channels. The output frequency of each module is adjustable, but the three channels share the same clock, while the duty cycle can be independently configured. Therefore, channels 0, 1, and 2 share the same output frequency, and channels 3, 4, and 5 also share the same output frequency. For the I/O configuration of the channel outputs, refer to the IOMUX module.  

## API Introduction  

The PWM class is located in the `machine` module.  

### Example Code  

```python  
import time
from machine import PWM, FPIOA

CONSTRUCT_WITH_FPIOA = False

PWM_CHANNEL = 0

PWM_PIN = 42
TEST_FREQ = 1000  # Hz


# Initialize PWM with 50% duty
try:
    if CONSTRUCT_WITH_FPIOA:
        fpioa = FPIOA()
        fpioa.set_function(PWM_PIN, fpioa.PWM0 + PWM_CHANNEL)
        pwm = PWM(PWM_CHANNEL, freq=TEST_FREQ, duty=50)
    else:
        pwm = PWM(PWM_PIN, freq=TEST_FREQ, duty=50)
except Exception:
    print("FPIOA setup skipped or failed")

print("[INIT] freq: {}Hz, duty: {}%".format(pwm.freq(), pwm.duty()))
time.sleep(0.5)

# duty() getter and setter
print("[TEST] duty()")
pwm.duty(25)
print("Set duty to 25%, got:", pwm.duty(), "→ duty_u16:", pwm.duty_u16(), "→ duty_ns:", pwm.duty_ns())
time.sleep(0.2)

# duty_u16()
print("[TEST] duty_u16()")
pwm.duty_u16(32768)  # 50%
print("Set duty_u16 to 32768, got:", pwm.duty_u16(), "→ duty():", pwm.duty(), "→ duty_ns():", pwm.duty_ns())
time.sleep(0.2)

# duty_ns()
print("[TEST] duty_ns()")
period_ns = 1000000000 // pwm.freq()
duty_ns_val = (period_ns * 75) // 100  # 75%
pwm.duty_ns(duty_ns_val)
print("Set duty_ns to", duty_ns_val, "ns (≈75%), got:", pwm.duty_ns(), "→ duty():", pwm.duty(), "→ duty_u16():", pwm.duty_u16())
time.sleep(0.2)

# Change frequency and re-check duty values
print("[TEST] Change frequency to 500Hz")
pwm.freq(500)
print("New freq:", pwm.freq())
print("Duty after freq change → duty():", pwm.duty(), "→ duty_u16():", pwm.duty_u16(), "→ duty_ns():", pwm.duty_ns())
time.sleep(0.2)

# Clean up
pwm.deinit()
print("[DONE] PWM test completed")
```  

### Constructor  

```python  
pwm = PWM(channel_or_pin, freq = -1, duty = -1, duty_u16 = -1, duty_ns = -1)  
```  

**Parameters**  

- `channel_or_pin`: PWM channel number, range [0, 5], or Pin number, such as pin42 -> pwm0
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
