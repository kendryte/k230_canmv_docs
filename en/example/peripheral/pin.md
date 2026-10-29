# GPIO Usage Tutorial

## What is GPIO?

**GPIO (General Purpose Input/Output) pins** are one of the most fundamental peripherals of a microcontroller. They can be configured as:

* **Input mode**: used to read external signals (such as buttons)
* **Output mode**: used to control external devices (such as LEDs)
* **With pull-up/pull-down resistors and drive capability**: adapts to different electrical connection scenarios

## K230 GPIO Features Overview

| Feature    | Description                                             |
| ----- | ---------------------------------------------- |
| Number of pins  | Total of 64 GPIO pins                                 |
| Mode support  | Input, Output                                          |
| Drive capability  | 0~7 adjustable (the larger the value, the stronger the drive capability)                            |
| Pull-up/pull-down configuration | Supports pull-up (PULL\_UP), pull-down (PULL\_DOWN), no pull-up/pull-down (PULL\_NONE) |

## Application Example: Controlling Output Pin High/Low Level

This example demonstrates how to configure Pin2 as output mode and control its output level.

### Example Code

```python
from machine import Pin

# ========== 初始化 GPIO ========== 
# 将 Pin2 设置为输出，关闭上下拉，设置驱动能力为 7（最大）
pin = Pin(2, Pin.OUT, pull=Pin.PULL_NONE, drive=7)

# ========== 控制电平输出 ==========
# 设置为高电平
pin.value(1)

# 设置为低电平
pin.value(0)
```

## Interface Description

| Method                              | Description                                                        |
| --------------------------------- | ----------------------------------------------------------- |
| `Pin(pin_num, mode, pull, drive)` | Initialize GPIO pin                                         |
| `pin.value(val)`                  | Set output level (0 low, 1 high), or get the current pin level state |
| `pin.init(...)`                   | Reinitialize or modify pin settings                          |

## Parameter Description

| Parameter   | Type    | Example Value   | Description                                                  |
| --------- | ----- | --------------- | ----------------------------------------------------- |
| `pin_num` | `int` | `2`             | Pin number (e.g., Pin2)                                |
| `mode`    | Enum    | `Pin.OUT`       | Mode: `Pin.IN` (input), `Pin.OUT` (output)            |
| `pull`    | Enum    | `Pin.PULL_NONE` | Pull-up/pull-down configuration: none, pull-up, pull-down |
| `drive`   | `int` | `0` \~ `7`      | Drive capability level, the larger the value, the stronger the drive capability     |

## Application Scenario Examples

| Scenario           | Example Description                          |
| -------------- | ------------------------------------- |
| Control LED lights | GPIO output high level to light up LED      |
| Read button state | Configure as input mode to read button signal   |
| Control relay or buzzer | Control peripherals through GPIO output level |
| General logic control | As high/low level logic output control signal |

## Special Notes

* The actual GPIO output current capability is limited by the drive level, supply voltage, and load, and direct driving of high-power devices should be avoided.
* All pins need to be configured for multi-function multiplexing through the **IOMUX/FPIOA tool** before use to ensure the corresponding function mapping.

## Further Reading

* 📘 [K230 Pin Module API Manual](../../api/machine/k230_canmv_pin_api_manual.md)
* 📘 [K230 FPIOA Module API Manual](../../api/machine/k230_canmv_fpioa_api_manual.md)
* 📥 [K230 Pin Function Comparison Table (Excel)](https://download.kendryte.com/developer/k230/HDK/K230%E7%A1%AC%E4%BB%B6%E6%96%87%E6%A1%A3/K230_PINOUT_V1.2_20240822.xlsx)
* 🛠️ [K230 IOMUX Configuration Tool](https://www.kendryte.com/zh/tools/dts_config_generation_tool)
