# Timer - Timer例程

本示例程序用于对 CanMV 开发板进行一个定时器的功能展示。

```python
from machine import Timer
#定义定时器回调函数
def on_timer(arg):                                     
    print("time up: %d" % arg)
#构造定时器对象，时间为3s，默认开启定时器
tim = Timer(mode=Timer.MODE_ONE_SHOT,period=3, unit=Timer.UNIT_S, callback=on_timer, arg=1, start=True)     
```

具体接口定义请参考 [Timer](../../../api/machine/K230_CanMV_Timer模块API手册.md)
