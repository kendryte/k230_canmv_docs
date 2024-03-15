# WDT - WDT例程

本示例程序用于对 CanMV 开发板进行一个WDT的功能展示。

```python
import time
from machine import WDT

# 实例化wdt1，timeout为3s
wdt1 = WDT(1,3)
time.sleep(2)
# 喂狗操作
wdt1.feed()
time.sleep(2)
```

具体接口定义请参考 [WDT](../../../api/machine/K230_CanMV_WDT模块API手册.md)
