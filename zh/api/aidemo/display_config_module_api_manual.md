# `DisplayConfig` 模块API手册

## 概述

`libs/DisplayConfig.py` 用于解决同一份 AI 例程在不同开发板上显示适配的问题。K230/K230D 生态中的开发板搭载的屏幕各不相同（HDMI、ST7701、HX8399、ILI9806……），过去例程需要手动修改 `display_mode` 才能在另一块板子上跑起来。该模块把"板型 → 屏驱动"的对应关系集中维护，配合 `display_mode="auto"` 即可实现跨板运行。

模块提供三个函数和一个类：

| 名称 | 用途 |
|------|------|
| `get_default_display_mode` | 查询当前开发板的默认屏驱动名称 |
| `get_display_type` | 把驱动名称解析成 `Display.init()` 需要的驱动常量 |
| `init_display` | 初始化显示并返回**实际**显示分辨率，适合不使用 `PipeLine` 的场景 |
| `DisplayImage` | 用 AI2D 把任意分辨率的 RGB888 数据缩放到显示分辨率 |

```{admonition} 提示
:class: note
使用 [`PipeLine`](./pipeline_module_api_manual.md) 的 AI 程序不需要直接调用本模块，只要把 `display_mode` 设为 `"auto"`，`PipeLine` 内部会自动完成解析。本模块主要面向不走 `PipeLine` 的场景，例如 UVC 摄像头、MP4 解码播放、LVGL 应用等。
```

## API 介绍

### get_default_display_mode

**描述**

根据开发板型号返回该板的默认屏驱动名称。板型通过 `os.uname()[-1]` 获取。

```{admonition} 注意
:class: warning
返回的是该开发板**配套推荐**的驱动，而不是对实际插着哪块屏的硬件探测结果。如果您接的是非标配屏幕，请显式指定 `display_mode`。
```

**语法**

```python
from libs.DisplayConfig import get_default_display_mode

mode = get_default_display_mode()          # 查询当前开发板
mode = get_default_display_mode("k230_canmv_01studio")   # 查询指定板型
```

**参数**

| 参数名称 | 描述 | 输入 / 输出 | 说明 |
|----------|------|-----------|------|
| board_type | 开发板型号字符串 | 输入 | 可选，默认 `None` 表示查询当前运行的固件 |

**返回值**

| 返回值 | 描述 |
|--------|------|
| str | 屏驱动名称，如 `hdmi`、`st7701`、`hx8399` 等，可直接传给 `PipeLine` 的 `display_mode` |

已收录的开发板与默认屏驱动：

| 默认驱动 | 开发板 |
|----------|--------|
| `hdmi` | `k230_canmv`、`k230_canmv_v3p0` |
| `hx8399` | `k230_evb`、`k230d_evb` |
| `nt35516` | `k230_canmv_rtt_evb` |
| `st7701` | `k230_canmv_01studio`、`k230_canmv_lckfb`、`k230_canmv_yahboom`、`k230_canmv_mrt`、`k230_canmv_hiwonder`、`k230_labplus_1956`、`k230d_canmv_bpi_zero`、`k230d_canmv_atk_dnk230d`、`k230d_canmv_junroc_ai_cam`、`k230d_canmv_lushanpi_lite`、`k230d_canmv_mini`、`k230d_labplus_ai_camera`、`k230d_labplus_ai_camera_v2` |
| `ili9806` | `k230_canmv_dongshanpi` |
| `gc9503` | `k230_canmv_gt6700` |
| `jd9852` | `k230_canmv_wondermk` |

```{admonition} 注意
:class: warning
板型不在上表中时会抛出 `ValueError: No default display for board <型号>; set display_mode explicitly`。此时请显式指定屏驱动，不要使用 `auto`。
```

### get_display_type

**描述**

把屏驱动名称解析成 `Display.init()` 所需的驱动常量。

**语法**

```python
from libs.DisplayConfig import get_display_type
from media.display import Display

display_type = get_display_type("auto")
Display.init(display_type)
```

**参数**

| 参数名称 | 描述 | 输入 / 输出 | 说明 |
|----------|------|-----------|------|
| display_mode | 屏驱动名称或 `Display` 常量 | 输入 | 默认 `"auto"`。取值见 [PipeLine 手册的 display_mode 取值表](./pipeline_module_api_manual.md#init)。传入 int 类型（即 `Display.XXX` 常量）时原样返回 |

**返回值**

| 返回值 | 描述 |
|--------|------|
| int | `Display.init()` 接受的驱动常量 |

```{admonition} 注意
:class: warning
传入未收录的字符串不会报错，会回退到 `Display.ST7701`。该行为是为兼容旧代码保留的，新代码请使用规范取值。
```

### init_display

**描述**

初始化显示设备，并返回**实际生效的**显示分辨率。屏驱动可能不支持请求的分辨率而使用自己的默认值，因此后续布局计算必须以该函数的返回值为准，不能沿用传入的 `display_size`。

**语法**

```python
from libs.DisplayConfig import init_display

display_size = init_display(display_mode="auto", osd_num=1, to_ide=True)
width, height = display_size
```

**参数**

| 参数名称 | 描述 | 输入 / 输出 | 说明 |
|----------|------|-----------|------|
| display_mode | 屏驱动名称或 `Display` 常量 | 输入 | 默认 `"auto"` |
| display_size | 期望的显示分辨率 `[width, height]` | 输入 | 可选，默认 `None` 表示使用驱动默认分辨率。请使用该参数而不是 `width`/`height` 关键字 |
| **kwargs | 透传给 `Display.init()` 的其它参数 | 输入 | 如 `osd_num`、`to_ide` 等 |

**返回值**

| 返回值 | 描述 |
|--------|------|
| list[int] | 实际显示分辨率 `[width, height]` |

```{admonition} 注意
:class: warning
该函数只负责初始化显示，**调用方需要自行调用 `Display.deinit()`**。它也不会启动 sensor，更不会改变 AI 推理分辨率、解码分辨率或录像分辨率，这些需要各自单独配置。
```

### DisplayImage

**描述**

用 AI2D 硬件把任意分辨率的 RGB888 数据缩放到显示分辨率，并封装成 `image.Image` 供显示使用。典型场景是 UVC 摄像头或 MP4 解码出来的画面分辨率与屏幕不一致时的适配。

内部复用同一套 AI2D 管线，只有输入分辨率发生变化时才会重建，因此逐帧调用开销很低。

**语法**

```python
from libs.DisplayConfig import init_display, DisplayImage

display_size = init_display(display_mode="auto")
resizer = DisplayImage(display_size, planar=False)

while True:
    img = resizer.run(frame_np)     # frame_np 为 HWC 排布的 uint8 RGB 数据
    Display.show_image(img)

resizer.deinit()
```

**构造函数参数**

| 参数名称 | 描述 | 输入 / 输出 | 说明 |
|----------|------|-----------|------|
| display_size | 目标分辨率 `[width, height]` | 输入 | 必填，通常直接传 `init_display()` 的返回值 |
| planar | 输入数据是否为平面排布 | 输入 | `True` 表示输入为 CHW 排布，`False`（默认）表示 HWC 排布 |

**run 方法**

| 参数名称 | 描述 | 输入 / 输出 | 说明 |
|----------|------|-----------|------|
| input_np | 待缩放数据，`ulab.numpy.ndarray` 类型 | 输入 | 连续的 uint8 RGB 数据，排布需与构造时的 `planar` 一致 |

| 返回值 | 描述 |
|--------|------|
| image.Image | RGB888 格式的 Image 实例，分辨率为构造时指定的 `display_size` |

**deinit 方法**

释放 `DisplayImage` 持有的 AI2D 资源，无参数无返回值。程序退出前必须调用。

```{admonition} 注意
:class: warning
- `run()` 内部会对 AI2D 的输出做一次拷贝，返回的 Image 引用的是**独立的数据副本**，因此下一次 `run()` 不会覆盖它，可以安全跨帧保留。
- 传入的 `input_np` 在 `run()` 返回前必须保持有效（例如来自 `to_numpy_ref()` 的借用数据）。
- 只有当输入 shape 发生变化时才会重建底层 AI2D 管线，因此逐帧调用的开销很低。
```

## 示例程序

以下给出不使用 `PipeLine`、直接用本模块适配显示的框架代码：

```python
from media.display import Display
from libs.DisplayConfig import init_display, DisplayImage
import gc

resizer = None
try:
    # 按开发板型号自动选屏，返回实际分辨率
    display_size = init_display(display_mode="auto", osd_num=1, to_ide=True)
    print("display size:", display_size)

    # 源画面分辨率与屏幕不一致时，用 DisplayImage 缩放
    resizer = DisplayImage(display_size, planar=False)

    while True:
        frame_np = get_frame_from_somewhere()   # UVC / VDEC 等来源，HWC uint8 RGB
        img = resizer.run(frame_np)
        Display.show_image(img)
        gc.collect()
finally:
    if resizer is not None:
        resizer.deinit()
    Display.deinit()      # init_display 不负责反初始化，需自行调用
```
