# 7. ADC 例程

## 1. 概述

K230内部包含一个ADC硬件模块，有6个通道，采样分辨率为12bit(0-4095)，采样速率为1M。

## 2. 示例

```python
from machine import ADC
# 实例化ADC通道0
adc = ADC(0)
# 获取ADC通道0采样值
print(adc.read_u16())
# 获取ADC通道0电压值
print(adc.read_uv(), "uV")
```

```{admonition} 提示
ADC模块具体接口请参考[API文档](../../api/machine/K230_CanMV_ADC模块API手册.md)
```
