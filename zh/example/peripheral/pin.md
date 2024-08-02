# 2. GPIO 例程

## 1. 概述

K230内部包含64个GPIO Pin，每个Pin可配置为输入或输出，可配置上下拉，可配置驱动能力。

## 2. 示例

```python
from machine import Pin
# 实例化Pin2为输出
pin = Pin(2, Pin.OUT, pull=Pin.PULL_NONE, drive=7)
# 设置输出为高
pin.value(1)
# 设置输出为低
pin.value(0)
```

```{admonition} 提示
Pin模块具体接口请参考[API文档](../../api/machine/K230_CanMV_Pin模块API手册.md)
```
