# wdt - wdt例程

本示例程序用于对 CanMV 开发板进行一个wdt的功能展示。

```python
import time
from machine import WDT

wdt1 = WDT(1,3)                         #构造wdt对象，/dev/watchdog1,timeout为3s
print('into', wdt1)
time.sleep(2)                           #延时2s
print(time.ticks_ms())                  
## 1.test wdt feed
wdt1.feed()                             #喂狗操作
time.sleep(2)                           #延时2s
print(time.ticks_ms())
## 2.test wdt stop
wdt1.stop()                             #停止喂狗
```

具体接口定义请参考 [WDT](../../../api/machine/K230_CanMV_WDT模块API手册.md)
