# adc - adc例程

本示例程序用于对 CanMV 开发板进行一个adc的功能展示。

```python
from machine import ADC

adc = ADC(0,enable=True)                      #构造adc对象，通道0默认开启
value = adc.value()                           #获取通道0的数值
print("value = %d" % value)
adc.deinit()                                  #注销adc对象
```

具体接口定义请参考 [ADC](../../../api/machine/K230_CanMV_ADC模块API手册.md)
