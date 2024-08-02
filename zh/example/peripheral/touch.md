# 12. TOUCH 例程

## 1. 概述

基于RT-Smart的触摸框架封装，支持单点多点电容触摸屏、电阻触摸屏。

## 2. 示例

```python
from machine import TOUCH
# 实例化TOUCH设备0
tp = TOUCH(0)
# 初始化触摸设备0，坐标输出旋转90度
# tp = TOUCH(0,1)
# 获取TOUCH数据
p = tp.read()
print(p)
# print(p[0].x)
# print(p[0].y)
# print(p[0].event)
```

```{admonition} 提示
TOUCH模块具体接口请参考[API文档](../../api/machine/K230_CanMV_TOUCH模块API手册.md)
```
