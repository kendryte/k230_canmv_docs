# Timer - Timer例程

本示例程序用于对 CanMV 开发板进行一个Timer的功能展示。

```python
from machine import Timer
import time

# 实例化一个软定时器
tim = Timer(-1)
# 初始化定时器为单次模式，周期100ms
tim.init(period=100, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
time.sleep(0.2)
# 初始化定时器为周期模式，频率为1Hz
tim.init(freq=1, mode=Timer.PERIODIC, callback=lambda t:print(2))
time.sleep(2)
# 释放定时器资源
tim.deinit()

```

具体接口定义请参考 [Timer](../../../api/machine/K230_CanMV_Timer模块API手册.md)
