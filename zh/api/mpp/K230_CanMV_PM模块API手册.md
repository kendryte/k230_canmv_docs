# 3.10 PM 模块API手册

## 1. 概述

PM模块，或称功耗管理模块，专门用于优化和管理设备的能耗。有关PM框架的详细描述，请参阅SDK中的相关文档（[K230_PM框架使用指南.md](https://github.com/kendryte/k230_docs/blob/main/zh/01_software/board/mpp/K230_PM%E6%A1%86%E6%9E%B6%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)）。在MicroPython环境中，PM模块封装了CPU和KPU两部分的功耗管理功能。

## 2. API 介绍

PM类位于`mpp`模块下，模块内部包含两个实例化对象：`cpu`和`kpu`，分别用于管理中央处理器和神经网络处理器的功耗。

### 2.1 示例

以下代码展示了如何使用PM模块获取当前CPU频率、列出支持的频率列表以及设置CPU频率：

```python
from mpp import pm

# 获取当前CPU频率
current_freq = pm.cpu.get_freq()

# 获取CPU支持的频率列表
supported_freqs = pm.cpu.list_profiles()

# 设置CPU频率为指定配置
pm.cpu.set_profile(1)
```

### 2.2 get_freq

```python
pm.pm_domain.get_freq()
```

**描述**
：获取指定功耗域的当前频率。

**参数**：无

**返回值**：返回当前指定域的频率值。

### 2.3 list_profiles

```python
pm.pm_domain.list_profiles()
```

**描述**
：获取指定功耗域支持的频率配置列表。

**参数**：无

**返回值**：返回一个列表，包含该域支持的所有频率配置。

### 2.4 set_profile

```python
pm.pm_domain.set_profile(index)
```

**描述**
：设置指定功耗域的频率配置索引。

**参数**：

- `index`：所要设置的频率配置索引。

**返回值**：无

---

此API手册旨在为开发者提供清晰、详尽的PM模块使用指南，确保功耗管理的有效实施与优化。
