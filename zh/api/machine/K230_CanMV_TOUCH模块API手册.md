# 2.16 `TOUCH` 模块 API 手册

## 1. 概述

触摸模块基于 RTT 的触摸框架，支持单点和多点电容触摸屏及电阻触摸屏。

## 2. API 介绍

TOUCH 类位于 `machine` 模块下。

**示例**

```python
from machine import TOUCH

# 实例化 TOUCH 设备 0
tp = TOUCH(0)
# 获取 TOUCH 数据
p = tp.read()
print(p)
# 打印触摸点坐标
# print(p[0].x)
# print(p[0].y)
# print(p[0].event)
```

### 构造函数

```python
# when index is 0
touch = TOUCH(index, type = TOUCH.TYPE_CST328, rotation = -1)

# when index is 1
touch = TOUCH(index, type = TOUCH.TYPE_CST328, rotation = -1, range_x = -1, range_y = -1, i2c : I2C = None, rst : Pin = None, int : Pin = None)
```

**参数**

- `index`: `TOUCH` 设备号，为 `0` 时，表示使用系统自带的触摸，为 `1` 时，表示使用 `CanMV` 专有的触摸驱动
- `type`: 触摸驱动类型，具体定义参考[触摸类型](#43-触摸类型)
- `rotation`: 面板输出坐标与屏幕坐标的旋转，取值范围为 [0-3]，具体定义参考[坐标旋转](#42-坐标旋转)。
- `range_x`: `index=1` 时有效，触摸输出坐标的宽度最大值
- `range_y`: `index=1` 时有效，触摸输出坐标的高度最大值
- `i2c`: `index=1` 时有效，触摸使用 `I2C` 总线对象
- `rst`: `index=1` 时有效，触摸复位引脚对象
- `int`: `index=1` 时有效，触摸中断引脚对象，当前不支持

### `read` 方法

```python
TOUCH.read([count])
```

获取触摸数据。

**参数**

- `count`: 最多读取的触摸点数量，取值范围为 [0:10]，默认为 0，表示读取所有触摸点。

**返回值**

返回触摸点数据，类型为元组 `([tp[, tp...]])`，其中每个 `tp` 是一个 `touch_info` 类实例。

### `deinit` 方法

```python
TOUCH.deinit()
```

释放 TOUCH 资源。

**参数**

无

**返回值**

无

## 3. TOUCH_INFO 类

TOUCH_INFO 类用于存储触摸点的信息，用户可通过相关只读属性访问。

- `event`: 事件码，具体参考[触摸事件](#41-触摸事件)。
- `track_id`: 触点 ID，用于多点触摸。
- `width`: 触点宽度。
- `x`: 触点的 x 坐标。
- `y`: 触点的 y 坐标。
- `timestamp`: 触点时间戳。

## 4. 常量

### 4.1 触摸事件

- `EVENT_NONE`: 无事件。
- `EVENT_UP`: 触摸按下后抬起。
- `EVENT_DOWN`: 触摸按下开始。
- `EVENT_MOVE`: 触摸按下后移动。

### 4.2 坐标旋转

- `ROTATE_0`: 坐标不旋转。
- `ROTATE_90`: 坐标旋转 90 度。
- `ROTATE_180`: 坐标旋转 180 度。
- `ROTATE_270`: 坐标旋转 270 度。

### 4.3 触摸类型

- `TYPE_CST128`: 系统自带触摸驱动
- `TYPE_CST328`: `CanMV` 专有触摸驱动
- `TYPE_FT5x16`: 系统自带触摸驱动
