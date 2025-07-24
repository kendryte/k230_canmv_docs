# NeoPixel 控制示例讲解（K230）

## 概述

本示例演示了如何在 K230 开发板上使用 `neopixel` 模块控制 **WS2812（NeoPixel）灯珠**。
通过该模块，用户可以灵活设置每颗 RGB 灯珠的颜色，实现动态灯效、颜色渐变、定位测试等功能。

NeoPixel（WS2812）使用单线串行通信，可以将多个 LED 串联连接，并统一控制。
此例程包含：

* 批量设置统一颜色
* 按序点亮每颗灯珠
* 关闭所有灯珠

---

## 示例代码

```python
import time
from machine import Pin
import neopixel

# === CONFIGURATION ===
NEOPIXEL_PIN = 42     # GPIO引脚号，可根据实际连接修改
NUM_PIXELS   = 10     # 控制的 WS2812 灯珠数量

# === INITIALIZE NEOPIXEL OBJECT ===
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

# === FUNCTION: Show solid colors ===
def test_colors():
    print("[TEST] Setting colors...")
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 0)]  # 红绿蓝和黄

    for i, color in enumerate(colors):
        for j in range(NUM_PIXELS):
            np[j] = color
        np.write()
        print(f"  → Color: {color}")
        time.sleep(0.5)

# === FUNCTION: Test individual pixel addressing ===
def test_pixels():
    print("[TEST] Lighting up pixels one by one...")
    for i in range(NUM_PIXELS):
        np.fill((0, 0, 0))         # 清空
        np[i] = (0, 255, 128)      # 点亮第 i 个为浅绿色
        np.write()
        print(f"  → Pixel {i} ON")
        time.sleep(0.2)

# === FUNCTION: Clear all pixels ===
def clear():
    np.fill((0, 0, 0))
    np.write()
    print("[TEST] Cleared all pixels.")

# === MAIN TEST SEQUENCE ===
def run_test():
    test_colors()
    test_pixels()
    clear()
    print("[DONE] NeoPixel test completed.")

run_test()
```

---

## 代码结构解读

### 1. **初始化 NeoPixel**

```python
np = neopixel.NeoPixel(Pin(42), 10)
```

* 使用 GPIO42 控制灯带
* 控制灯珠数量为 10 个
* 每颗灯珠为 RGB 格式（默认 bpp=3）

---

### 2. **统一设置颜色（test\_colors）**

```python
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 0)]
```

* 依次将所有灯珠设置为红色、绿色、蓝色、黄色
* 通过 `np.fill()` 或逐个赋值设置颜色
* `np.write()` 刷新数据

---

### 3. **逐个点亮灯珠（test\_pixels）**

```python
np[i] = (0, 255, 128)
```

* 每次只点亮第 `i` 颗灯珠，其余清零
* 有助于测试串联方向、定位灯珠编号

---

### 4. **关闭所有灯珠（clear）**

```python
np.fill((0, 0, 0)); np.write()
```

* 置零所有颜色值，达到熄灭效果

---

## 说明与建议

| 项目     | 内容说明                               |
| ------ | ---------------------------------- |
| GPIO选择 | 推荐使用未占用的 IO，比如 GPIO42、43 等         |
| 最大数量   | 根据中断/时序限制，一般建议不要超过 16 个灯珠         |
| 电源建议   | 每颗 WS2812 全亮时最大电流约 60mA，多个灯珠建议独立供电 |
| 性能影响   | 发送数据期间关闭中断，建议控制灯珠总长度/刷新频率以免影响其他任务  |

---

## 更多说明

如需实现 **彩虹跑马灯、渐变、亮度调整** 等效果，请查看 MicroPython 官方文档：
👉 [https://docs.micropython.org/en/latest/library/neopixel.html](https://docs.micropython.org/en/latest/library/neopixel.html)

---
