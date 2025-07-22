# `FPIOA` 模块 API 手册

## 概述

FPIOA（Pin Multiplexer）模块主要负责配置物理引脚（PAD）的功能。在 SoC 中，虽然有多种功能可用，但由于引脚数量有限，多个功能可能会共享同一个 I/O 引脚。此时，每个引脚在同一时刻只能激活一种功能，因此需要通过 IOMUX（即 FPIOA）来选择合适的功能。

## API 介绍

FPIOA 类位于 `machine` 模块中。

**示例**

```python
from machine import FPIOA

# 实例化 FPIOA 对象
fpioa = FPIOA()

# 打印所有引脚的配置
fpioa.help()

# 打印指定引脚的详细配置
fpioa.help(0)

# 打印指定功能的所有可用配置引脚
fpioa.help(FPIOA.IIC0_SDA, func=True)

# 设置 Pin0 为 GPIO0
fpioa.set_function(0, FPIOA.GPIO0)

# 设置 Pin2 为 GPIO2，同时配置其它参数
fpioa.set_function(2, FPIOA.GPIO2, ie=1, oe=1, pu=0, pd=0, st=1, ds=7)

# 获取指定功能当前所用的引脚
fpioa.get_pin_num(FPIOA.UART0_TXD)

# 获取指定引脚当前的功能
fpioa.get_pin_func(0)
```

### 构造函数

```python
fpioa = FPIOA()
```

**参数**

无

### `set_function` 方法

```python
FPIOA.set_function(pin, func, ie=-1, oe=-1, pu=-1, pd=-1, st=-1, ds=-1)
```

设置引脚的功能。

**参数**

- `pin`: 引脚号，范围：[0, 63]
- `func`: 功能号
- `ie`: 输入使能，可选参数
- `oe`: 输出使能，可选参数
- `pu`: 上拉使能，可选参数
- `pd`: 下拉使能，可选参数
- `st`: 施密特触发器使能，可选参数
- `ds`: 驱动能力，可选参数

更多详细信息，参考[IO 驱动能力](#io-配置说明)

**返回值**

无

### `get_pin_num` 方法

```python
fpioa.get_pin_num(func)
```

获取指定功能当前所在的引脚。

**参数**

- `func`: 功能号

**返回值**

返回引脚号，或 `None` 如果未找到相应功能。

### `get_pin_func` 方法

```python
fpioa.get_pin_func(pin)
```

获取指定引脚当前的功能。

**参数**

- `pin`: 引脚号

**返回值**

返回引脚当前的功能号。

### `help` 方法

```python
fpioa.help([number, func=False])
```

打印引脚配置提示信息。

**参数**

- `number`: 引脚号或功能号， 可选参数
- `func`: 是否启用功能号查询，默认为 `False`

**返回值**

可能为以下三种：

1. 所有引脚的配置信息（未设置 `number`）
1. 指定引脚的详细配置信息（设置了 `number`，未设置 `func` 或设置为 `False`）
1. 指定功能的所有可配置引脚号（设置了 `number`，并将 `func` 设置为 `True`）

## 附录

### IO 配置说明

![io-ds](https://www.kendryte.com/api/post/attachment?id=436)
