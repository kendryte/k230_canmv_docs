# K230 控制 NeoPixel 灯带教程

## 一、简介：什么是 NeoPixel？

NeoPixel 是基于 **WS2812** 单总线 RGB 灯珠的商业名称，它具有以下特点：

* 每颗灯珠内部集成控制芯片，单线控制
* 支持 RGB 颜色设置
* 多颗可级联，支持逐个控制

K230 提供对 NeoPixel 的原生支持，适用于创意灯效、状态指示、视觉演示等项目。

## 二、硬件连接说明

| 项目     | 内容                |
| ------ | ----------------- |
| 控制引脚   | GPIO42（示例中使用）     |
| 灯珠电源   | 建议使用外接电源供电（5V）    |
| GND 接地 | 与 K230 开发板 GND 共地 |
| 灯珠数量限制 | 以实测为准  |

> ⚠️ 注意：每颗 WS2812 全亮时电流最高可达 60mA，多个灯珠务必使用外部电源。

## 三、示例代码：快速开始

```python
import time
from machine import Pin
import neopixel

# === 参数配置 ===
NEOPIXEL_PIN = 42     # 控制 WS2812 的 GPIO 引脚
NUM_PIXELS   = 10     # 灯珠个数

# === 初始化 NeoPixel ===
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

# === 函数：统一颜色设置 ===
def test_colors():
    print("[TEST] 全灯统一设置颜色")
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # 红绿蓝黄
    for color in colors:
        np.fill(color)
        np.write()
        print(f" → 颜色: {color}")
        time.sleep(0.5)

# === 函数：逐个点亮测试 ===
def test_pixels():
    print("[TEST] 依次点亮每个灯珠")
    for i in range(NUM_PIXELS):
        np.fill((0, 0, 0))
        np[i] = (0, 255, 128)
        np.write()
        print(f" → 灯珠 {i} 点亮")
        time.sleep(0.2)

# === 函数：关闭全部灯珠 ===
def clear():
    np.fill((0, 0, 0))
    np.write()
    print("[TEST] 全部灯珠熄灭")

# === 主测试流程 ===
def run_test():
    test_colors()
    test_pixels()
    clear()
    print("[完成] NeoPixel 测试结束")

run_test()
```

## 四、代码结构讲解

### 1️⃣ 初始化灯带对象

```python
np = neopixel.NeoPixel(Pin(42), 10)
```

* 第一个参数是 GPIO 控制引脚（如 42）
* 第二个参数是灯珠数量（如 10）

默认采用 RGB 格式，支持使用 `np[i] = (r, g, b)` 设置颜色。

### 2️⃣ 设置统一颜色

```python
np.fill((255, 0, 0))  # 全部红色
np.write()            # 写入更新
```

可以使用 `fill()` 一次性设置所有灯珠颜色，再通过 `write()` 发送到灯珠。

### 3️⃣ 逐个点亮测试

```python
for i in range(NUM_PIXELS):
    np.fill((0, 0, 0))   # 清空
    np[i] = (0, 255, 128)
    np.write()
```

逐个点亮某个灯珠用于 **灯珠编号确认**、**安装方向调试** 等。

### 4️⃣ 熄灭灯珠

```python
np.fill((0, 0, 0))
np.write()
```

设定为黑色 `(0, 0, 0)` 即可熄灭全部。

## 五、常见应用场景

| 场景     | 示例说明                |
| ------ | ------------------- |
| 状态指示灯  | 不同颜色代表不同状态          |
| 彩虹灯带   | 不同灯珠显示不同颜色          |
| 互动灯效   | 触控或传感器触发动态变化        |
| 编程教学演示 | 用于 Python 控制硬件的教学实践 |

## 六、使用建议与注意事项

| 项目   | 建议说明                   |
| ---- | ---------------------- |
| 灯珠数量 | 建议不超过 16 个，过多可能影响系统时序  |
| 电源   | 多颗灯珠需外部 5V 电源供电（注意电流）  |
| 性能   | 数据发送过程中关闭中断，不建议频繁刷新    |
| 稳定性  | 所有 GND 必须共地，否则可能导致通信失败 |

## 七、参考资料与进阶拓展

* 📘 [MicroPython 官方 NeoPixel 模块文档](https://docs.micropython.org/en/latest/library/neopixel.html)
