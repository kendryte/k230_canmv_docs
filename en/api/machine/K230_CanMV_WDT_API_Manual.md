# 2.12 `WDT` Module API Manual  

## 1. Overview  

The K230 integrates two WDT (Watchdog Timer) hardware modules internally, designed to ensure the system can reboot when an application crashes and enters an unrecoverable state. Once activated, if the hardware does not receive periodic "feeding" operations during runtime, the WDT will automatically reset the system upon timeout.  

## 2. API Introduction  

The `WDT` class is located in the `machine` module.  

### 2.1 Example Code  

```python  
from machine import WDT  

# Instantiate WDT1 with a timeout of 3 seconds  
wdt1 = WDT(1, 3)  

# Perform a feed operation  
wdt1.feed()  
```  

### 2.2 Constructor  

```python  
wdt = WDT(id=1, timeout=5, auto_close=True)  
```  

**Parameters**  

- `id`: WDT module ID, valid range [0, 1], defaults to 1.  
- `timeout`: Timeout value in seconds (s), defaults to 5.  
- `auto_close`: Automatically stops the watchdog when the Python interpreter terminates to prevent unintended system reboots.  

**Note:** WDT0 is currently unavailable.  

### 2.3 `feed` Method  

```python  
WDT.feed()  
```  

Performs a feed operation.  

**Parameters**  

None  

**Return Value**  

None
