# 9. WDT 例程

## 1. 概述

K230内部包含两个WDT硬件模块，用于在应用程序崩溃且最终进入不可恢复状态时重启系统。一旦开始，当硬件运行期间没有定期进行喂狗（feed）就会在超时后自动复位。

## 2. 示例

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

```{admonition} 提示
WDT模块具体接口请参考[API文档](../../api/machine/K230_CanMV_WDT模块API手册.md)
```
