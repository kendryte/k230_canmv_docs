# 1.4 `gc` – 内存管理 API 手册

该模块实现了部分 CPython 内存管理模块的功能子集。有关详细信息，请参阅 CPython 原始文档：[gc](https://docs.python.org/3.5/library/gc.html#module-gc)。

在 `K230` 上，新增了以下接口来获取 `RT-Smart` 系统的内存信息：

- `sys_heap`: 用于内核应用的内存管理。
- `sys_page`: 用于用户应用的内存管理。
- `sys_mmz`: 用于多媒体驱动内存管理，适用于 `Sensor`、`Display` 等模块。

## 1. 函数

### 1.1 `enable`

```python
gc.enable()
```

启用自动垃圾回收机制。

### 1.2 `disable`

```python
gc.disable()
```

禁用自动垃圾回收机制。在禁用状态下，仍可进行堆内存的分配，并且可以通过手动调用 `gc.collect()` 来执行垃圾回收。

### 1.3 `collect`

```python
gc.collect()
```

手动运行垃圾回收过程，回收不再使用的内存。

### 1.4 `mem_alloc`

```python
gc.mem_alloc()
```

返回当前已分配的堆内存字节数。

```{admonition} 与 CPython 的差异
此功能为 MicroPython 的扩展功能，CPython 并不包含此方法。
```

### 1.5 `mem_free`

```python
gc.mem_free()
```

返回当前可用的堆内存字节数。如果堆剩余的内存数量无法确定，则返回 `-1`。

```{admonition} 与 CPython 的差异
此功能为 MicroPython 的扩展功能，CPython 并不包含此方法。
```

### 1.6 `threshold`

```python
gc.threshold([amount])
```

设置或查询垃圾回收的分配阈值。当堆内存不足时，通常会触发垃圾回收。如果设置了阈值，则在总共分配了超过设定值的字节后，也会触发垃圾回收。`amount` 参数通常小于整个堆的大小，目的是在堆耗尽之前提前触发回收，减少内存碎片。此值的效果因应用而异，最佳值需要根据应用场景调整。

不传入参数时，此函数将返回当前的阈值设置。返回值为 `-1` 表示分配阈值已禁用。

```{admonition} 与 CPython 的差异
此函数为 MicroPython 的扩展。CPython 中有类似的 `set_threshold()` 函数，但由于垃圾回收机制的不同，其签名和语义有所差异。
```

### 1.7 `sys_heap`

```python
gc.sys_heap()
```

查询系统 `heap` 内存的使用情况，返回一个包含 3 个元素的元组，分别表示 `total`（总内存）、`free`（可用内存）和 `used`（已用内存），单位为字节（Byte）。

### 1.8 `sys_page`

```python
gc.sys_page()
```

查询系统 `page` 内存的使用情况，返回一个包含 3 个元素的元组，分别表示 `total`（总内存）、`free`（可用内存）和 `used`（已用内存），单位为字节（Byte）。

### 1.9 `sys_mmz`

```python
gc.sys_mmz()
```

查询系统 `mmz` 内存的使用情况，返回一个包含 3 个元素的元组，分别表示 `total`（总内存）、`free`（可用内存）和 `used`（已用内存），单位为字节（Byte）。
