# 8. RTC 例程

## 1. 概述

当前CanMV K230提供了一个类RTC模块，用户可以设置和获取当前系统时间

## 2. 示例

```python
from machine import RTC

# 实例化RTC
rtc = RTC()
# 获取当前时间
print(rtc.datetime())
# 设置当前时间
rtc.init((2024,2,28,2,23,59,0,0))
```

```{admonition} 提示
RTC模块具体接口请参考[API文档](../../api/machine/K230_CanMV_RTC模块API手册.md)
```
