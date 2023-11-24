# gpio - gpio例程

本示例程序用于对 CanMV 开发板进行一个GPIO的功能展示。

```python
from machine import GPIO
gpio = GPIO(8, GPIO.OUT, GPIO.PULL_UP, value=0)        #构造GPIO对象，gpio编号为8，设置为上拉输出低电平
value = gpio.value()                                   #获取gpio的值
print("value = %d" % value) 
gpio.value(1)                                          #设置gpio输出为高电平
value = gpio.value()
print("value = %d" % value)
```

具体接口定义请参考 [GPIO](../../../api/machine/K230_CanMV_GPIO模块API手册.md)
