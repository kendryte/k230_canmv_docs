# RTC 例程

## 概述

K230 提供了一个 RTC（实时时钟）模块，允许用户设置和获取当前系统时间，适用于需要时间跟踪的应用。

## 示例

以下示例展示了如何使用 RTC 接口获取和设置系统时间。

```python
from machine import RTC

# 实例化 RTC
rtc = RTC()

# 获取当前时间
print(rtc.datetime())

# 设置当前时间
rtc.init((2024, 2, 28, 2, 23, 59, 0, 0))
```

## 代码说明

1. **实例化 RTC**：
   - 创建 `RTC` 对象，以便访问 RTC 功能。

1. **获取当前时间**：
   - 调用 `datetime()` 方法获取当前的系统时间，返回格式为 `(年, 月, 日, 星期, 时, 分, 秒, 微秒)`。

1. **设置当前时间**：
   - 调用 `init()` 方法设置当前时间。传入的元组参数包括年份、月份、日期、星期几、小时、分钟、秒和微秒。

```{admonition} 提示
有关 RTC 模块的详细接口和使用方法，请参考[API文档](../../api/machine/K230_CanMV_RTC模块API手册.md)
```
