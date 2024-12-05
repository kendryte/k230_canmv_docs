# 1. FPIOA 例程

## 1. 概述

IOMUX 主要用于配置物理管脚（PAD）的功能。在 SoC 中，由于功能较多且管脚数量有限，多个功能可能会共享同一个 I/O 管脚。然而，同一时间一个管脚只能承载一个功能，因此需要通过 IOMUX（也称为 FPIOA、Pin multiplexing、管脚功能选择等）进行功能选择。

## 2. 示例

以下代码展示了如何使用 FPIOA 模块来设置和查询管脚的功能：

```python
from machine import FPIOA

# 实例化 FPIOA 对象
fpioa = FPIOA()

# 打印所有引脚的配置状态
fpioa.help()

# 打印指定引脚（Pin0）的详细配置
fpioa.help(0)

# 打印指定功能（如 IIC0_SDA）对应的所有可用引脚
fpioa.help(FPIOA.IIC0_SDA, func=True)

# 将 Pin0 设置为 GPIO0
fpioa.set_function(0, FPIOA.GPIO0)

# 将 Pin2 设置为 GPIO2，并同时配置其它选项
fpioa.set_function(2, FPIOA.GPIO2, ie=1, oe=1, pu=0, pd=0, st=1, sl=0, ds=7)

# 获取指定功能（如 UART0_TXD）当前所在的引脚编号
fpioa.get_pin_num(FPIOA.UART0_TXD)

# 获取指定引脚（Pin0）当前的功能配置
fpioa.get_pin_func(0)
```

```{admonition} 提示
有关 FPIOA 模块的具体接口说明，请参考 [API 文档](../../api/machine/K230_CanMV_FPIOA模块API手册.md)。
```
