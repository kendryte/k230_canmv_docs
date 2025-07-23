# `PWM` Module API Manual  

## Overview  

The K230 integrates two PWM hardware modules, each with three output channels. The output frequency of each module is adjustable, but the three channels share the same clock, while the duty cycle can be independently configured. Thus, channels 0, 1, and 2 share the same output frequency, and channels 3, 4, and 5 also share the same output frequency. For the I/O configuration of the channel outputs, refer to the IOMUX module.  

## API Introduction  

The `PWM` class is located in the `machine` module.  

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
        # Use FPIOA to configure pin multiplexing for PWM, then pass the channel  
        fpioa = FPIOA()  
        fpioa.set_function(PWM_PIN, fpioa.PWM0 + PWM_CHANNEL)  
        pwm = PWM(PWM_CHANNEL, freq=TEST_FREQ, duty=50)  
    else:  
        # Directly pass the pin number  
        pwm = PWM(PWM_PIN, freq=TEST_FREQ, duty=50)  
except Exception:  
    print("FPIOA setup skipped or failed")  

print("[INIT] freq: {}Hz, duty: {}%".format(pwm.freq(), pwm.duty()))  
time.sleep(0.5)  

# Test duty() getter and setter  
print("[TEST] duty()")  
pwm.duty(25)  
print("Set duty to 25%, got:", pwm.duty(), "→ duty_u16:", pwm.duty_u16(), "→ duty_ns:", pwm.duty_ns())  
time.sleep(0.2)  

# Test duty_u16()  
print("[TEST] duty_u16()")  
pwm.duty_u16(32768)  # 50%  
print("Set duty_u16 to 32768, got:", pwm.duty_u16(), "→ duty():", pwm.duty(), "→ duty_ns():", pwm.duty_ns())  
time.sleep(0.2)  

# Test duty_ns()  
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
pwm = PWM(channel_or_pin, freq=-1, duty=-1, duty_u16=-1, duty_ns=-1)  
```  

**Parameters**  

- **`channel_or_pin`**:  
  - **`channel`**: PWM channel number, range `[0, 5]`. Requires configuring the corresponding pin for PWM multiplexing using FPIOA.  
  - **`pin`**: Pin object or pin number. The driver automatically sets the pin to PWM multiplexing. For pin mappings, refer to [PWM Pin Multiplexing](#pwm-pin-multiplexing).  
- **`freq`**: PWM output frequency (Hz). Default: `-1` (no change).  
- **`duty`**: Duty cycle as a percentage of the period, range `[0, 100]`. Default: `-1` (no change).  
- **`duty_ns`**: High-level duration in nanoseconds (`ns`). Default: `-1` (no change).  
- **`duty_u16`**: High-level duration, range `[0, 65535]`. Default: `-1` (no change).  

> Only one of `duty`, `duty_ns`, or `duty_u16` can be set at a time.  

### `init` Method  

```python  
PWM.init(freq=-1, duty=-1, duty_u16=-1, duty_ns=-1)  
```  

**Parameters**  

Same as [Constructor](#constructor).  

### `deinit` Method  

```python  
PWM.deinit()  
```  

Release the PWM channel resources.  

**Parameters**  

None.  

**Returns**  

None.  

### `freq` Method  

```python  
PWM.freq([freq])  
```  

Get or set the PWM output frequency.  

**Parameters**

- **`freq`**: Optional. If provided, sets the frequency; otherwise, returns the current frequency.  

**Returns**

Current frequency (if no argument) or `None`.  

### `duty` Method  

```python  
PWM.duty([duty])  
```  

Get or set the duty cycle (percentage).  

**Parameters**

- **`duty`**: Optional. If provided, sets the duty cycle; otherwise, returns the current value.  

**Returns**  

Current duty cycle (if no argument) or `None`.  

### `duty_u16` Method  

```python  
PWM.duty_u16([duty_u16])  
```  

Get or set the duty cycle (16-bit value).  

**Parameters**

- **`duty_u16`**: Optional. If provided, sets the duty cycle; otherwise, returns the current value.  

**Returns**  

Current duty cycle (if no argument) or `None`.  

### `duty_ns` Method  

```python  
PWM.duty_ns([duty_ns])  
```  

Get or set the duty cycle (nanoseconds).  

**Parameters**

- **`duty_ns`**: Optional. If provided, sets the duty cycle; otherwise, returns the current value.  

**Returns**  

Current duty cycle (if no argument) or `None`.  

## PWM Pin Multiplexing  

| PWM Channel | Available Pins          |  
|-------------|-------------------------|  
| PWM0        | GPIO42, GPIO54, GPIO60  |  
| PWM1        | GPIO43, GPIO55, GPIO61  |  
| PWM2        | GPIO7, GPIO46, GPIO56   |  
| PWM3        | GPIO8, GPIO47, GPIO57   |  
| PWM4        | GPIO9, GPIO52, GPIO58   |  
| PWM5        | GPIO25, GPIO53, GPIO59  |  
