# 12. TOUCH 例程

## 1. 概述

K230 的触摸模块基于 RT-Smart 的触摸框架封装，支持单点和多点电容触摸屏以及电阻触摸屏的操作。

## 2. 示例

以下示例展示了如何使用 TOUCH 模块读取触摸数据。

```python
from machine import TOUCH

# 实例化 TOUCH 设备 0
tp = TOUCH(0)
# 初始化触摸设备 0，坐标输出旋转 90 度
# tp = TOUCH(0, 1)

# 获取 TOUCH 数据
p = tp.read()
print(p)

# 输出触摸点的坐标和事件信息
# print(p[0].x)
# print(p[0].y)
# print(p[0].event)
```

## 3. 代码说明

1. **导入模块**：
   - 导入 `TOUCH` 模块。

1. **实例化触摸设备**：
   - 使用 `TOUCH(0)` 实例化触摸设备 0。如果需要旋转坐标，可以使用 `TOUCH(0, 1)`。

1. **读取触摸数据**：
   - 调用 `tp.read()` 获取触摸数据，返回的数据存储在 `p` 中。

1. **输出触摸信息**：
   - 可以通过 `print(p)` 打印出触摸数据的详细信息。可以注释掉的部分 `print(p[0].x)`、`print(p[0].y)` 和 `print(p[0].event)` 分别用于输出第一个触摸点的 x 和 y 坐标，以及触摸事件类型。

```{admonition} 提示
TOUCH 模块具体接口请参考 [API 文档](../../api/machine/K230_CanMV_TOUCH模块API手册.md)
```
