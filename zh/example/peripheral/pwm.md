# 6. PWM 例程

## 1. 概述

K230内部包含两个PWM硬件模块，每个模块有3个输出通道，模块输出频率可调，但3通道共用，通道占空比独立可调。因此通道0、1、2共用频率，通道3、4、5共用频率。
通道输出IO配置参考IOMUX模块。

## 2. 示例

```python
from machine import PWM
# channel 0 output freq 1kHz duty 50%, enable
pwm0 = PWM(0, 1000, 50, enable = True)
# disable channel 0 output
pwm0.enable(False)
# set channel 0 output freq 2kHz
pwm0.freq(2000)
# set channel 0 output duty 10%
pwm0.duty(10)
# enable channel 0 output
pwm0.enable(True)
# release channel 0
pwm0.deinit()
```

```{admonition} 提示
PWM模块具体接口请参考[API文档](../../api/machine/K230_CanMV_PWM模块API手册.md)
```
