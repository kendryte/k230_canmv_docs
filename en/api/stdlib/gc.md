# `gc` – Memory Management API Manual

This module implements a subset of the CPython memory management module's functionality. For more details, please refer to the original CPython documentation: [gc](https://docs.python.org/3.5/library/gc.html#module-gc).

On the `K230`, the following interfaces have been added to obtain memory information for the `RT-Smart` system:

- `sys_total`: System total memory size.
- `sys_heap`: Used for kernel application memory management.
- `sys_page`: Used for user application memory management.
- `sys_mmz`: Used for multimedia driver memory management, suitable for modules like `Sensor`, `Display`, etc.

## Functions

### `enable`

```python
gc.enable()
```

Enables the automatic garbage collection mechanism.

### `disable`

```python
gc.disable()
```

Disables the automatic garbage collection mechanism. While disabled, heap memory allocation is still possible, and garbage collection can be performed manually by calling `gc.collect()`.

### `collect`

```python
gc.collect()
```

Manually runs the garbage collection process to reclaim unused memory.

### `mem_alloc`

```python
gc.mem_alloc()
```

Returns the number of bytes of currently allocated heap memory.

```{admonition} Difference from CPython
This feature is an extension of MicroPython and is not included in CPython.
```

### `mem_free`

```python
gc.mem_free()
```

Returns the number of bytes of currently available heap memory. If the remaining heap memory cannot be determined, it returns `-1`.

```{admonition} Difference from CPython
This feature is an extension of MicroPython and is not included in CPython.
```

### `threshold`

```python
gc.threshold([amount])
```

Sets or queries the allocation threshold for garbage collection. Garbage collection is usually triggered when heap memory is low. If a threshold is set, garbage collection will also be triggered after allocating more than the set amount of bytes. The `amount` parameter is usually less than the total heap size to trigger collection before the heap is exhausted, reducing memory fragmentation. The effectiveness of this value varies by application, and the optimal value needs to be adjusted according to the application scenario.

Without parameters, this function returns the current threshold setting. A return value of `-1` indicates that the allocation threshold is disabled.

```{admonition} Difference from CPython
This function is an extension of MicroPython. CPython has a similar `set_threshold()` function, but due to differences in the garbage collection mechanism, its signature and semantics are different.
```

### `sys_total`

```python
gc.sys_total()
```

Queries the system `total` memory size, in bytes.

### `sys_heap`

```python
gc.sys_heap()
```

Queries the system `heap` memory usage, returning a tuple containing 3 elements representing `total` (total memory), `free` (available memory), and `used` (used memory), in bytes.

### `sys_page`

```python
gc.sys_page()
```

Queries the system `page` memory usage, returning a tuple containing 3 elements representing `total` (total memory), `free` (available memory), and `used` (used memory), in bytes.

### `sys_mmz`

```python
gc.sys_mmz()
```

Queries the system `mmz` memory usage, returning a tuple containing 3 elements representing `total` (total memory), `free` (available memory), and `used` (used memory), in bytes.
