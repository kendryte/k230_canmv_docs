# 2.14 machine 模块 API 手册

## 1. 概述

`machine` 模块包含与特定硬件板相关的功能。该模块中的大多数功能允许对系统上的硬件组件进行直接且不受限制的访问和控制。若不当使用，可能会导致主板故障、死机或崩溃，甚至在极端情况下造成硬件损坏。

## 2. API 介绍

### 2.1 `reset` 方法

```python
machine.reset()
```

立即复位 SoC（系统级芯片）。

**参数**

无

**返回值**

无

### 2.2 `mem_copy` 方法

```python
machine.mem_copy(dst, src, size)
```

将指定数量的数据从源内存地址复制到目标内存地址。

**参数**

- `dst`: 目标地址。
- `src`: 源地址。
- `size`: 要复制的字节数。

**返回值**

无
