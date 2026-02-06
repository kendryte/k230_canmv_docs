# K230 触摸屏（TOUCH）使用教程

## 概述

K230 支持 **电容屏** 和 **电阻屏** 的触摸输入，提供了基于 RT-Smart 封装的 `TOUCH` 类接口。开发者可使用它读取触点坐标、事件类型等信息，广泛应用于 HMI、交互终端等场景。

## 快速上手示例

以下示例展示了如何读取触摸屏上的触点数据：

```python
from machine import TOUCH

# 实例化触摸设备 0（系统默认触摸）
tp = TOUCH(0)

# 读取当前触摸点数据（返回元组，每个元素为 TOUCH_INFO 对象）
p = tp.read()
print(p)

# 如有触摸点，可访问第一个触点的坐标与事件类型
# print(p[0].x)       # X 坐标
# print(p[0].y)       # Y 坐标
# print(p[0].event)   # 事件类型（如 EVENT_DOWN、EVENT_MOVE、EVENT_UP）
```

## 接口说明

| 接口名 | 说明 |
| --- | --- |
| `TOUCH(dev, *, rotate=-1, range_x=-1, range_y=-1, i2c=None, rst=None, int=None)` | 创建触摸屏实例，`dev=0` 表示系统默认，`dev!=0` 为自定义设备，详见下文参数 |
| `read([count])` | 返回当前触摸点信息，返回元组，每个元素为 TOUCH_INFO 对象，`count` 为最多读取的触点数（默认1） |
| `deinit()` | 释放触摸资源 |

### 构造函数参数说明

- `dev`: 触摸设备号，0为系统默认，非0为自定义设备。
- `rotate`: 坐标旋转，见[常量](#常量)，默认-1（使用设备默认）。
- `range_x`, `range_y`: 仅自定义设备有效，指定触摸屏分辨率。
- `i2c`: 仅自定义设备有效，I2C总线对象，必填。
- `rst`, `int`: 仅自定义设备有效，复位/中断引脚对象，选填。
- 其余参数已废弃。

### TOUCH_INFO 对象属性

- `event`: 事件码，见[常量](#常量)
- `track_id`: 触点ID
- `width`: 触点宽度
- `x`: X坐标
- `y`: Y坐标
- `timestamp`: 时间戳

## 示例详解

### 1. 实例化设备

```python
# 系统默认触摸
tp = TOUCH(0)

# 自定义触摸设备（需指定i2c，分辨率等）
# tp = TOUCH(1, i2c=my_i2c, range_x=800, range_y=480)
```

### 2. 读取触摸数据

```python
p = tp.read()
print(p)
```

返回的 `p` 是一个元组，每个元素为 TOUCH_INFO 对象。每个对象包含：

- `x`: X 坐标
- `y`: Y 坐标
- `event`: 触摸事件（如 EVENT_DOWN、EVENT_MOVE、EVENT_UP）
- `track_id`, `width`, `timestamp` 等

### 3. 示例输出参考

```text
(<TOUCH_INFO x=120 y=65 event=0 ...>,)
```

如果有多个触点，例如支持多指操作：

```text
(<TOUCH_INFO x=120 y=65 event=0 ...>, <TOUCH_INFO x=250 y=130 event=0 ...>)
```

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

## 应用场景

| 场景 | 示例 |
| --- | --- |
| 图形界面交互 | 基于触摸点驱动按钮点击、滑动切换 |
| 自定义手势识别 | 多点滑动、旋转等操作识别 |
| 简单绘图板或签名板 | 基于触点轨迹做线条绘制 |

## 常见问题

**Q：没有读取到触摸点，返回是空元组？**
A：此时说明屏幕未被触摸。`tp.read()` 只在屏幕被按下时返回触点。

**Q：如何处理多点触控？**
A：读取到的是一个包含多个 `TOUCH_INFO` 的元组，使用 `for` 循环逐个读取即可。

**Q：是否支持旋转坐标系？**
A：支持，通过 `rotate` 参数（如 `TOUCH.ROTATE_90`）可开启坐标旋转。

## 延伸阅读

- 📄 [TOUCH 模块 API 文档](../../api/machine/K230_CanMV_TOUCH模块API手册.md)
