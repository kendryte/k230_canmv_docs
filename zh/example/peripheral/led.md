# 15. LED例程讲解

## 1. 概述

K230 开发板板载一颗 LED 灯，用户可以通过`machine.LED`模块方便地控制该灯珠的状态和亮度。此功能可用于指示状态或提供视觉反馈。

## 2. 示例

以下示例展示了如何使用 K230 的 LED 模块来控制 LED 灯的亮灭和亮度：

```python
from machine import LED
import time

# 初始化LED灯对象
red_led = LED("LED_RED")          # 或者使用red_led = LED(1)
green_led = LED("LED_GREEN")      # 或者使用green_led = LED(2)
blue_led = LED("LED_BLUE")        # 或者使用blue_led = LED(3)

# 关闭所有LED灯
blue_led.off()
green_led.off()
red_led.off()

while True:
    # 设置绿色LED的亮度，取值范围为0-255
    green_led.value(50)    
    red_led.on()           # 点亮红色LED
    time.sleep_ms(250)     # 暂停250毫秒

    green_led.value(200)   # 设置绿色LED的亮度
    red_led.off()          # 关闭红色LED
    time.sleep_ms(250)     # 暂停250毫秒
```

## 3. 代码说明

此例程展示了如何利用K230开发板的LED模块进行灯珠的控制。通过调整LED的状态和亮度，开发者可以实现多种视觉效果，增强交互体验。

- **导入模块**：首先导入`machine`和`time`模块，前者用于控制硬件，后者用于设置时间延迟。
  
- **初始化 LED 对象**：
  - `red_led = LED("LED_RED")`：创建一个红色LED对象。
  - `green_led = LED("LED_GREEN")`：创建一个绿色LED对象。
  - `blue_led = LED("LED_BLUE")`：创建一个蓝色LED对象。
  
- **关闭 LED**：通过调用`off()`方法关闭所有LED灯，确保初始状态为关闭。

- **主循环**：
  - 使用`while True:`开始无限循环。
  - 在循环内，先将绿色LED的亮度设置为50，然后点亮红色LED。
  - `time.sleep_ms(250)`暂停程序250毫秒，以保持红色LED亮起的状态。
  - 然后将绿色LED的亮度设置为200，并关闭红色LED。
  - 再次暂停250毫秒。

```{admonition} 提示
有关LED模块的详细接口信息，请参考[API文档](../../api/machine/K230_CanMV_LED模块API手册.md)。
```
