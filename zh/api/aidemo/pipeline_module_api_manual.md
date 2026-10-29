# `Pipeline` 模块API手册

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
| display_mode | 显示模式，str类型，取值见下表 | 输入 | 默认`hdmi`。推荐使用`auto`，由开发板型号自动选择 |
| display_size | 显示分辨率，list类型，包括宽高，如[1920,1080]，如果为None，根据显示屏决定；否则按输入设置 | 输入 | 默认None，根据显示屏决定 |
| osd_layer_num| osd显示层数，用户程序在原画上叠加的层数| 输入 | 默认为1 |
| debug_mode   | 调试计时模式，int类型，0为不计时，1为计时 | 输入 | 默认为0 |

💡 **display_mode 取值**：

| 取值 | 对应显示驱动 | 说明 |
|------|--------------|------|
| `auto` | 由开发板型号决定 | **推荐**。根据 `os.uname()[-1]` 查表选择该开发板的默认屏驱动，无需修改代码即可跨板运行。若板型未收录会抛出 `ValueError`，此时请显式指定驱动 |
| `hdmi` / `lt9611` | LT9611 | HDMI 输出，默认 1920x1080 |
| `lcd` / `st7701` | ST7701 | 常见 MIPI LCD，默认 800x480 |
| `hx8399` | HX8399 | |
| `nt35516` | NT35516 | 该屏会强制把 sensor 帧率限制为 30fps |
| `nt35532` | NT35532 | |
| `gc9503` | GC9503 | |
| `aml020t` | AML020T | |
| `jd9852` | JD9852 | |
| `ili9806` | ILI9806 | |
| `virt` | VIRT | 虚拟显示，仅在 CanMV IDE 中显示，可通过 `display_size` 自定义分辨率 |

```{admonition} 注意
:class: note
传入未收录的字符串不会报错，会回退到 ST7701。该行为是为兼容旧代码保留的，新代码请使用上表中的取值或 `auto`。
```

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

```{admonition} 提示
:class: note
推荐配合 `display_mode="auto"` 使用，这样同一份脚本在不同开发板上都能正确出图：

    pl = PipeLine(rgb888p_size=[1280,720], display_mode="auto")
    pl.create()
    display_size = pl.get_display_size()   # create 之后再取实际显示分辨率
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| sensor   | Sensor实例，用户可以在外部创建sensor实例并传入  | 输入      |  可选，不同开发板有默认配置 |
| sensor_id| Sensor ID，用户可以配置该参数设置摄像头  | 输入      |  可选，不同开发板有默认配置 |
| hmirror  | 水平镜像参数                | 输入      | 可选，默认为 `None`,根据不同开发板默认配；设置时为bool类型，设为True或False |
| vflip    | 垂直翻转参数                | 输入      | 可选，默认为 `None`,根据不同开发板默认配置；设置时为bool类型，设为True或False     |
| fps      | sensor 帧率参数    | 输入      | 可选，默认60。部分开发板（`k230d_canmv_bpi_zero`、`k230_canmv_lckfb`、`k230d_canmv_atk_dnk230d`）和 `nt35516` 屏会强制使用 30fps，该参数不生效 |
| to_ide   | 是否将屏幕显示传输到 IDE 显示 | 输入      | 开启时占用更多内存 |
| crop_vertical   | 是否适配竖屏显示 | 输入      | sensor出图为横图，显示为竖屏时，通过裁剪实现竖屏显示 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

```{admonition} 注意
:class: warning
- **不可重复调用**。若 PipeLine 已经初始化，再次调用 `create()` 会抛出 `RuntimeError: PipeLine must be destroyed before create`。需要重新配置时，请先调用 [`destroy`](#destroy) 再 `create`。
- 传入的 `sensor` 实例会由 PipeLine 接管，`destroy()` 时一并停止。
- `create()` 成功后，构造函数里设置的 `display_size` 会被**显示驱动的实际分辨率覆盖**，因此请在 `create()` 之后再用 [`get_display_size`](#get_display_size) 获取显示分辨率，不要直接沿用构造时传入的值。
- 初始化过程中任一步失败，PipeLine 会自动回滚已申请的 sensor/display 资源后再抛出异常，无需手动清理。
```

### get_frame

**描述**

获取一帧图像给 AI 程序使用，获取图像分辨率为PipeLine构造函数设置的rgb888p_size，图像格式为Sensor.RGBP888，返回时转换成ulab.numpy.ndarray格式。

**语法**  

```python
img=pl.get_frame()
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| 无  |                   |       |   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| img     | `ulab.numpy.ndarray` 类型，**CHW 三维**数据，shape 为 `[3, height, width]`，其中宽高由构造时的 `rgb888p_size` 决定（宽度已按 16 对齐）。注意不是四维的 `[1,3,H,W]` |

```{admonition} 注意
:class: warning
返回的是当前帧的**引用**，不是拷贝。必须在下一次 `get_frame()` 或 `destroy()` 之前处理完；若需要跨帧保留，请先自行 `copy()`。
```

### show_image

**描述**

将在 `pl.osd_img` 上绘制的 AI 结果在 Display 上叠加显示。`pl.osd_img` 是 `create` 接口初始化的一帧格式为 `image.ARGB8888` 的空白图像，用于绘制 AI 结果。

**语法**  

```python
pl.show_image()
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| flag | 透传给 `Display.show_image()` 的标志位 | 输入 | 可选，默认 `None` 表示不传 |

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

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| 无  |                   |       |   |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| list    | 返回屏幕配置的显示宽高[display_width,display_height] |

### destroy

**描述**

反初始化PipeLine实例。

**语法**  

```python
pl.destroy()
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| 无  |                   |       |   |

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
    # 显示模式，推荐"auto"由开发板型号自动选择屏驱动，也可显式指定"hdmi"/"lcd"/"st7701"等
    display_mode="auto"
    # None表示使用屏驱动的默认分辨率；需要指定时填[宽, 高]
    display_size=None

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=[1920,1080], display_mode=display_mode, display_size=display_size)
    pl.create()  # 创建PipeLine实例
    display_size = pl.get_display_size()    # create之后再取实际显示分辨率
    while True:
        with ScopedTiming("total",1):
            img = pl.get_frame()            # 获取当前帧数据
            print(img.shape)                # CHW三维数据，shape为[3, height, width]
            gc.collect()                    # 垃圾回收
    pl.destroy()                            # 销毁PipeLine实例
```

上述代码中，通过`pl.get_frame()`接口获取一帧分辨率为rgb888p_size的图像，类型为ulab.numpy.ndarray，排布为CHW。基于这段代码，您可以专注于 AI 推理部分的操作。

完整的推荐写法（含 AI 模型的创建与释放）见 [两种主循环写法](../../ai_dev_doc.md#main-loop-patterns)。
