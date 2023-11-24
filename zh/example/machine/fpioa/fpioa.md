# fpioa - iomux fpioa例程

本示例程序用于对 CanMV 开发板进行iomux功能展示。

```python
from machine import FPIOA
a = FPIOA()  

help(a) #查看本模块所有帮助；

for i in range(63):
    a.help(i)  #查看第i个管脚的帮助

for i in range(221):
    a.get_Pin_num(i) #获取某个功能对应的管脚号

a.help(60)   #查看第60个管脚的当前配置和可配置功能
a.set_function(60,a.GPIO60)  #把第60个管脚设置为gpio60功能。
a.help(60)  #查看第60个管脚的帮助

a.set_function(60,set_pd=1) #使能第60个管脚的下拉 其他可配选项为(set_sl=1,set_ie=0,set_oe=0,set_pd=1,set_pu=0,set_ds=6,set_st=0,set_di=1) 
a.help(60)
```

具体接口定义请参考 [IOMUX_FPIOA](../../../api/machine/K230_CanMV_IOMUX_API手册.md)
