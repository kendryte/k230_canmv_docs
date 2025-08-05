# PipeLine 模块 API 手册

## 概述

本手册旨在指导开发人员使用 MicroPython 开发 AI Demo 时，构建完整的 Media 流程，实现从 Camera 获取图像和显示 AI 推理结果的功能。该模块封装了单摄双通道默认配置，一路将 Camera 的图像直接送给 Display 模块显示；另一路使用 `get_frame` 接口获取一帧图像供 AI 程序使用。

## API 介绍

### init

**描述**

PipeLine 构造函数，初始化 AI 程序获取图像的分辨率和显示相关的参数。

**语法**  

```python
from libs.PipeLine import PipeLine

pl=PipeLine(rgb888p_size=[1920,1080],display_mode='hdmi',display_size=None,osd_layer_num=1,debug_mode=0)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| rgb888p_size | AI 程序的输入图像分辨率，list类型，包括宽高，如[1920,1080] | 输入 | 默认[224,224]，根据 AI 程序决定|
| display_mode | 显示模式，支持 `hdmi` 和 `lcd`，str类型 | 输入 | 默认`hdmi`,根据显示配置|
| display_size | 显示分辨率，list类型，包括宽高，如[1920,1080]，如果为None，根据显示屏决定；否则按输入设置 | 输入 | 默认None，根据显示屏决定 |
| osd_layer_num| osd显示层数，用户程序在原画上叠加的层数| 输入 | 默认为1 |
| debug_mode   | 调试计时模式，0计时，1不计时，int类型 | 输入 | 默认为0 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| PipeLine | PipeLine实例                  |

### create

**描述**

PipeLine 初始化函数，初始化 Media 流程中的 Sensor/Display/OSD配置。

**语法**  

```python
# 默认配置
pl.create()
# 用户也可以自行创建实例传入
from media.sensor import *
sensor=Sensor()
pl.create(sensor=sensor)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| sensor   | Sensor实例，用户可以在外部创建sensor实例并传入  | 输入      |  可选，不同开发板有默认配置 |
| hmirror  | 水平镜像参数                | 输入      | 可选，默认为 `None`,根据不同开发板默认配；设置时为bool类型，设为True或False |
| vflip    | 垂直翻转参数                | 输入      | 可选，默认为 `None`,根据不同开发板默认配置；设置时为bool类型，设为True或False     |
| fps      | sensor 帧率参数    | 输入      | 可选，默认60，设置Sensor的帧率 |
| to_ide   | 是否将屏幕显示传输到 IDE 显示 | 输入      | 开启时占用更多内存 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### get_frame

**描述**

获取一帧图像给 AI 程序使用，获取图像分辨率为PipeLine构造函数设置的rgb888p_size，图像格式为Sensor.RGBP888，返回时转换成ulab.numpy.ndarray格式。

**语法**  

```python
img=pl.get_frame()
```

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| img     | 格式为ulab.numpy.ndarray，分辨率为rgb888p_size的图像数据 |

### show_image

**描述**

将在 `pl.osd_img` 上绘制的 AI 结果在 Display 上叠加显示。`pl.osd_img` 是 `create` 接口初始化的一帧格式为 `image.ARGB8888` 的空白图像，用于绘制 AI 结果。

**语法**  

```python
pl.show_image()
```

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### get_display_size

**描述**

获取当前屏幕配置的宽高。

**语法**  

```python
display_size=pl.get_display_size()
```

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| list    | 返回屏幕配置的显示宽高[display_width,display_height] |

### destroy

**描述**

反初始化PipeLine实例。

**语法**  

```python
img=pl.destroy()
```

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无    |                                  |

## 示例程序

以下为示例程序：

```python
from libs.PipeLine import PipeLine
from libs.Utils import ScopedTiming
from media.media import *
import gc
import sys,os

if __name__ == "__main__":
    # 显示模式，默认"hdmi",可以选择"hdmi"和"lcd"
    display_mode="hdmi"
    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=[1920,1080], display_mode=display_mode)
    pl.create()  # 创建PipeLine实例
    display_size = pl.get_display_size()
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)
            gc.collect()                    # 垃圾回收
    pl.destroy()                            # 销毁PipeLine实例
```

上述代码中，通过`pl.get_frame()`接口获取一帧分辨率为rgb888p_size的图像，类型为ulab.numpy.ndarray，排布为CHW。基于这段代码，您可以专注于 AI 推理部分的操作。
