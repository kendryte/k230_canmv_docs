# ADC - ADC例程

本示例程序用于对 CanMV 开发板进行一个ADC的功能展示。

```python
from machine import ADC

# 实例化ADC通道0
adc = ADC(0)
# 获取ADC通道0采样值
print(adc.read_u16())
# 获取ADC通道0电压值
print(adc.read_uv(), "uV")
```

具体接口定义请参考 [ADC](../../../api/machine/K230_CanMV_ADC模块API手册.md)
