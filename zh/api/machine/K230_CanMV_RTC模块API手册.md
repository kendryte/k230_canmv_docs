# 2.15 `RTC` 模块 API 手册

## 1. 概述

当前 CanMV K230 提供一个类 RTC（实时时钟）模块，用户可以用其设置和获取当前系统时间。

## 2. API 介绍

RTC 类位于 `machine` 模块下。

### 2.1 示例

```python
from machine import RTC

# 实例化 RTC
rtc = RTC()
# 获取当前时间
print(rtc.datetime())
# 设置当前时间
rtc.init((2024, 2, 28, 2, 23, 59, 0, 0))
```

### 2.2 构造函数

```python
rtc = RTC()
```

**参数**

无

### 2.3 `init` 方法

```python
rtc.init(year, month, day, weekday, hours, minutes, seconds, microsec)
```

**参数**

- `year`: 年
- `month`: 月
- `day`: 日
- `weekday`: 星期几，[1-7]
- `hours`: 时
- `minutes`: 分
- `seconds`: 秒
- `microsec`: 微秒

**返回值**

无

### 2.4 `datetime` 方法

```python
print(rtc.datetime())
```

**参数**

无

**返回值**

返回当前日期和时间信息，包括：

- `year`: 年
- `mon`: 月
- `day`: 日
- `wday`: 星期几
- `hour`: 时
- `min`: 分
- `sec`: 秒
- `microsec`: 微秒
