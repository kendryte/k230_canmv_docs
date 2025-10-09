# Rotary Encoder 使用教程

## 什么是 Rotary Encoder？

**Rotary Encoder（旋转编码器）** 是一种将旋转位置或旋转运动转换为数字信号的传感器。常见的增量式旋转编码器通过检测旋转方向和旋转量来提供位置反馈。常用于：

- 音量调节旋钮
- 菜单导航控制
- 精确位置控制
- 速度和方向检测
- 工业自动化设备

K230 支持连接增量式旋转编码器，通过 GPIO 引脚读取编码器的 CLK（时钟）、DT（数据）和 SW（按键）信号，实现：

- 旋转方向检测（顺时针/逆时针）
- 旋转量计数（增量值和总计数）
- 按键状态检测（编码器通常带有按压开关）

## 示例概览

以下示例演示了如何使用 K230 的 `ENCODER` 模块完成以下操作：

- 初始化旋转编码器
- 读取旋转数据和按键状态
- 重置编码器计数
- 释放编码器资源

### 1. 导入模块并初始化编码器

```python
from machine import ENCODER

# 初始化编码器 0，连接 CLK 到引脚 42，DT 到引脚 43，SW 到引脚 5
encoder = ENCODER(id=0, pin_clk=42, pin_dt=43, pin_sw=5)
```

- `id`：编码器实例编号（必需，不同的id用于区分多个encoder实例，如id=0,1,2,3...）
- `pin_clk`：时钟信号引脚（必需）
- `pin_dt`：数据信号引脚（必需）
- `pin_sw`：按键信号引脚（可选，不使用时可设为 -1）

### 2. 读取编码器数据

```python
# 阻塞读取，等待编码器事件
data = encoder.read()
if data:
    print(f"增量变化: {data.delta}")
    print(f"总计数: {data.total_count}")
    print(f"旋转方向: {data.direction}")
    print(f"按键状态: {data.button_state}")
    print(f"时间戳: {data.timestamp}")

# 带超时的读取（单位：毫秒）
data = encoder.read(timeout_ms=1000)
if data is None:
    print("1秒内没有编码器事件")
```

返回的数据对象包含以下属性：

- `delta`：本次事件的增量变化值
- `total_count`：从初始化开始的总计数值
- `direction`：旋转方向（DIR_CW 顺时针 / DIR_CCW 逆时针 / DIR_NONE 无）
- `button_state`：按键状态（0 释放 / 1 按下）
- `timestamp`：事件时间戳

### 3. 重置编码器计数

```python
# 重置编码器的总计数值为 0
encoder.reset()
```

### 4. 释放编码器资源

```python
# 释放编码器资源
del encoder
# 或者显式调用
encoder.__del__()
```

## 方向常量说明

ENCODER 类提供了以下方向常量：

| 常量 | 值 | 说明 |
|------|----|----|
| DIR_NONE | 0 | 无旋转 |
| DIR_CW | 1 | 顺时针旋转 |
| DIR_CCW | 2 | 逆时针旋转 |

使用示例：

```python
if data.direction == ENCODER.DIR_CW:
    print("顺时针旋转")
elif data.direction == ENCODER.DIR_CCW:
    print("逆时针旋转")
```

## 完整使用示例

```python
from machine import ENCODER
import time

# 初始化编码器
encoder = ENCODER(id=0, pin_clk=42, pin_dt=43, pin_sw=5)

# 菜单选择示例
menu_items = ["选项1", "选项2", "选项3", "选项4"]
current_index = 0

print("旋转选择菜单项，按下确认")

while True:
    # 读取编码器事件，100ms 超时
    data = encoder.read(100)
    
    if data:
        # 根据旋转方向更新菜单索引
        if data.direction == ENCODER.DIR_CW:
            current_index = (current_index + 1) % len(menu_items)
        elif data.direction == ENCODER.DIR_CCW:
            current_index = (current_index - 1) % len(menu_items)
        
        # 显示当前选中项
        print(f"当前选择: {menu_items[current_index]}")
        
        # 检测按键
        if data.button_state == 1:
            print(f"确认选择: {menu_items[current_index]}")
            break

# 清理资源
del encoder
```

## 应用场景

- **用户界面控制**（菜单导航、参数调节）
- **音量/亮度调节**（精确的数值调整）
- **位置控制**（步进电机控制、机械臂定位）
- **测量仪器**（角度测量、长度测量）
- **游戏控制器**（方向盘、旋钮控制）

## 注意事项

- CLK 和 DT 引脚是必需的，SW 引脚可选
- 建议在 CLK 和 DT 引脚连接上拉电阻（通常编码器模块已内置）
- 快速旋转时可能需要更频繁地读取以避免丢失事件

## 编译开关

- 旋转编码器默认关闭，如需要打开的话，需要执行`make menuconfig`，打开如下对应的编译选项：

``` c
> RT-Smart Configuration > RT-Thread Smart System Features
        [*] Enable Rotary Encoder Support
```
