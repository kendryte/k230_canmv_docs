# TOUCH - TOUCH例程

本示例程序用于对 CanMV 开发板进行一个TOUCH的功能展示。

```python
from machine import TOUCH

# 实例化TOUCH设备0
tp = TOUCH(0)
# 获取TOUCH数据
p = tp.read()
print(p)
# print(p[0].x)
# print(p[0].y)
# print(p[0].event)
```

具体接口定义请参考 [TOUCH](../../../api/machine/K230_CanMV_TOUCH模块API手册.md)
