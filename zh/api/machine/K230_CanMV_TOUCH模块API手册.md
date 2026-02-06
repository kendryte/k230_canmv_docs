# `TOUCH` 模块 API 手册

## 概述

触摸模块基于 RTT 的触摸框架，支持单点和多点电容触摸屏及电阻触摸屏。

## API 介绍

TOUCH 类位于 `machine` 模块下。

**示例**

```python
from machine import TOUCH

# 实例化 TOUCH 设备 0（系统默认触摸）
tp = TOUCH(0)
# 获取 TOUCH 数据（返回元组，每个元素为 TOUCH_INFO 对象）
p = tp.read()
print(p)
# 打印触摸点坐标
# print(p[0].x)
# print(p[0].y)
# print(p[0].event)
```

### 构造函数

```python
# 系统默认触摸
touch = TOUCH(dev)

# 自定义触摸设备（dev != 0，需指定i2c，分辨率等）
touch = TOUCH(dev, i2c=my_i2c, range_x=800, range_y=480, rotate=TOUCH.ROTATE_0)
```

**参数**

- `dev`: 触摸设备号，0为系统默认，非0为自定义设备。
- `rotate`: 坐标旋转，见[常量](#常量)，默认-1（使用设备默认）。
- `range_x`, `range_y`: 仅自定义设备有效，指定触摸屏分辨率。
- `i2c`: 仅自定义设备有效，I2C总线对象，必填。
- `rst`, `int`: 仅自定义设备有效，复位/中断引脚对象，选填。
- 其余参数（如 type, slave_addr）已废弃。

### `read` 方法

```python
TOUCH.read([count])
```

获取触摸数据。

**参数**

- `count`: 最多读取的触摸点数量，范围[1, 最大支持数]，默认1。

**返回值**

返回触摸点数据，类型为元组 `(<TOUCH_INFO 对象>, ...)`，每个元素为 `TOUCH_INFO` 实例。

### `deinit` 方法

```python
TOUCH.deinit()
```

释放 TOUCH 资源。

**参数**

无

**返回值**

无

## TOUCH_INFO 类

TOUCH_INFO 类用于存储触摸点的信息，用户可通过相关只读属性访问：

- `event`: 事件码，见[常量](#常量)
- `track_id`: 触点 ID，用于多点触摸。
- `width`: 触点宽度。
- `x`: 触点的 x 坐标。
- `y`: 触点的 y 坐标。
- `timestamp`: 触点时间戳。

## 常量

### 触摸事件

- `TOUCH.EVENT_NONE`：无事件
- `TOUCH.EVENT_UP`：抬起
- `TOUCH.EVENT_DOWN`：按下
- `TOUCH.EVENT_MOVE`：移动

### 坐标旋转

- `TOUCH.ROTATE_0`：不旋转
- `TOUCH.ROTATE_90`：旋转90度
- `TOUCH.ROTATE_180`：旋转180度
- `TOUCH.ROTATE_270`：旋转270度
- `TOUCH.ROTATE_SWAP_XY`：XY互换

### 触摸类型（兼容保留，实际值均为0）

- `TOUCH.TYPE_CST226SE`
- `TOUCH.TYPE_CST328`
- `TOUCH.TYPE_GT911`
