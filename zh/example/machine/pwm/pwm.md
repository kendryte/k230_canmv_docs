# PWM - PWM例程

本示例程序用于对 CanMV 开发板进行一个PWM输出的功能展示。  

```python
from machine import PWM
# 实例化PWM通道0，频率为1000Hz，占空比为50%，默认使能输出
pwm0 = PWM(0, 1000, 50, enable = True)
# 关闭通道0输出
pwm0.enable(0)
# 调整通道0频率为2000Hz
pwm0.freq(2000)
# 调整通道0占空比为40%
pwm0.duty(40)
# 打开通道0输出
pwm0.enable(1)
```

具体接口定义请参考 [PWM](../../../api/machine/K230_CanMV_PWM模块API手册.md)
