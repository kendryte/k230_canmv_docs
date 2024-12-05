
# 2. GPIO 例程

## 1. 概述

K230 芯片内部集成了 64 个 GPIO 引脚（GPIO Pin），每个引脚都可以配置为输入或输出模式，并支持上下拉电阻配置和驱动能力设置。GPIO 引脚的灵活配置使得它在多种场景下具有广泛的应用。

## 2. 示例

以下代码示例展示了如何使用 GPIO 模块对管脚进行配置和控制：

```python
from machine import Pin

# 将 Pin2 实例化为输出模式，并配置为无上下拉（PULL_NONE），驱动能力为 7
pin = Pin(2, Pin.OUT, pull=Pin.PULL_NONE, drive=7)

# 设置 Pin2 输出高电平
pin.value(1)

# 设置 Pin2 输出低电平
pin.value(0)
```

```{admonition} 提示
关于 Pin 模块的详细接口和功能说明，请参考 [API 文档](../../api/machine/K230_CanMV_Pin模块API手册.md)。
```
