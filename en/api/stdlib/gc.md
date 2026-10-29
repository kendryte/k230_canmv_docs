# `gc` – Memory Management API Manual

This module implements a subset of the functionality of the CPython memory management module. For detailed information, please refer to the original CPython documentation: [gc](https://docs.python.org/3.5/library/gc.html#module-gc).

On `K230`, the following interfaces have been added to retrieve memory information of the `RT-Smart` system:

- `sys_totoal`: System memory size
- `sys_heap`: Used for memory management of kernel applications.
- `sys_page`: Used for memory management of user applications.
- `sys_mmz`: Used for multimedia driver memory management, applicable to modules such as `Sensor` and `Display`.

## Functions

### `enable`

```python
gc.enable()
```

Enables automatic garbage collection.

### `disable`

```python
gc.disable()
```

Disables automatic garbage collection. When disabled, heap memory allocation is still possible, and garbage collection can be performed by manually calling `gc.collect()`.

### `collect`

```python
gc.collect()
```

Manually runs the garbage collection process to reclaim memory that is no longer in use.

### `mem_alloc`

```python
gc.mem_alloc()
```

Returns the number of bytes of heap memory currently allocated.

```{admonition} Difference from CPython
This feature is an extension of MicroPython and is not included in CPython.
```

### `mem_free`

```python
gc.mem_free()
```

Returns the number of bytes of heap memory currently available. If the amount of remaining heap memory cannot be determined, it returns `-1`.

```{admonition} Difference from CPython
This feature is an extension of MicroPython and is not included in CPython.
```

### `threshold`

```python
gc.threshold([amount])
```

Sets or queries the allocation threshold for garbage collection. Garbage collection is typically triggered when heap memory is low. If a threshold is set, garbage collection will also be triggered after a total of more than the specified number of bytes have been allocated. The `amount` parameter is typically smaller than the entire heap size, with the purpose of triggering collection before the heap is exhausted to reduce memory fragmentation. The effect of this value varies by application, and the optimal value needs to be adjusted based on the application scenario.

When called without arguments, this function returns the current threshold setting. A return value of `-1` indicates that the allocation threshold is disabled.

```{admonition} Difference from CPython
This function is a MicroPython extension. CPython has a similar `set_threshold()` function, but due to differences in garbage collection mechanisms, its signature and semantics differ.
```

### `sys_total`

```python
gc.sys_total()
```

Queries the system memory size, in bytes.

### `sys_heap`

```python
gc.sys_heap()
```

Queries the usage of the system `heap` memory, returning a tuple containing 3 elements representing `total` (total memory), `used` (used memory), and `free` (available memory), in bytes (Byte).

### `sys_page`

```python
gc.sys_page()
```

Queries the usage of the system `page` memory, returning a tuple containing 3 elements representing `total` (total memory), `used` (used memory), and `free` (available memory), in bytes (Byte).

### `sys_mmz`

```python
gc.sys_mmz()
```

Queries the usage of the system `mmz` memory, returning a tuple containing 3 elements representing `total` (total memory), `used` (used memory), and `free` (available memory), in bytes (Byte).
