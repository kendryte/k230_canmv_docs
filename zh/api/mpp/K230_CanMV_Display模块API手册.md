# 3.2 `Display` 模块 API 手册

```{attention}
该模块自固件版本 V0.7 起有显著更改，若您使用的是 V0.7 之前的固件，请参考旧版本文档。
```

## 1. 概述

本手册旨在指导开发人员使用 Micro Python API 调用 CanMV Display 模块，实现图像显示功能。

如需增加自定义屏幕，可参考[Display Debugger](../../example/media/how_to_add_new_mipi_panel.md)

## 2. API 介绍

### 2.1 init

**描述**

初始化 Display 通路，包括 VO 模块、 DSI 模块和 LCD/HDMI。  
**`必须在 MediaManager.init()之前调用`**

**语法**  

```python
init(type=None, width=None, height=None, osd_num=1, to_ide=False, fps=None, quality=90)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| type     | [显示设备类型](#31-type)     | 输入      | 必选 |
| width    | 分辨率宽度                   | 输入      | 可选参数,默认值根据 `type` 决定 |
| height   | 分辨率高度                   | 输入      | 可选参数,默认值根据 `type` 决定 |
| osd_num  | 在 [show_image](#22-show_image) 时支持的 LAYER 数量 | 输入 | 越大占用内存越多 |
| to_ide   | 是否将屏幕显示传输到 IDE 显示 | 输入      | 开启时占用更多内存 |
| fps      | 显示帧率                     | 输入      | 仅支持 `VIRT` 类型 |
| quality  | 设置 `Jpeg` 压缩质量          | 输入      | 仅在 `to_ide=True` 时有效，范围 [10-100] |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.2 show_image

**描述**

在屏幕上显示图像。

**语法**  

```python
show_image(img, x=0, y=0, layer=None, alpha=255, flag=0)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| img      | 显示的图像                   | 输入      |      |
| x        | 起始坐标的 x 值                | 输入      |      |
| y        | 起始坐标的 y 值                | 输入      |      |
| layer    | 显示到 [指定层](#32-layer)    | 输入      | 仅支持 `OSD` 层，若需要多层请在 [init](#21-init) 中设置 `osd_num` |
| alpha    | 图层混合 alpha                | 输入      |      |
| flag     | 显示 [标志](#33-flag)         | 输入      |      |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.3 deinit

**描述**

执行反初始化， deinit 方法会关闭整个 Display 通路，包括 VO 模块、 DSI 模块和 LCD/HDMI。  
**`必须在 MediaManager.deinit()之前调用`**  
**`必须在 sensor.stop()之后调用`**

**语法**  

```python
deinit()
```

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.4 bind_layer

**描述**

将 `sensor` 或 `vdec` 模块的输出绑定到屏幕显示。无需用户手动干预即可持续显示图像。  
**`必须在 init 之前调用`**

**语法**  

```python
bind_layer(src=(mod, dev, layer), dstlayer, rect=(x, y, w, h), pix_format, alpha, flag)
```

**参数**

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| src      | `sensor` 或 `vdec` 的输出信息   | 输入      | 可通过 `sensor.bind_info()` 获取 |
| dstlayer | 绑定到 Display 的 [显示层](#32-layer) | 输入      | 可绑定到 `video` 或 `osd` 层 |
| rect     | 显示区域                      | 输入      | 可通过 `sensor.bind_info()` 获取 |
| pix_format | 图像像素格式                | 输入      | 可通过 `sensor.bind_info()` 获取 |
| alpha    | 图层混合 alpha                | 输入      |      |
| flag     | 显示 [标志](#33-flag)         | 输入      | `LAYER_VIDEO1` 不支持 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### 2.5 width

**描述**

获取屏幕或某一图层的显示宽度

**语法**

```python
width(layer = None):
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| layer | 指定获取 [显示层](#32-layer) 的宽度,如果不传则表示获取屏幕的分辨率宽度 | | |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| width  | 屏幕或显示层的宽度信息 |

### 2.6 height

**描述**

获取屏幕或某一图层的显示高度

**语法**

```python
height(layer = None):
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| layer | 指定获取 [显示层](#32-layer) 的高度,如果不传则表示获取屏幕的分辨率高度 | | |

**返回值**

| 返回值 | 描述                            |
|--------|---------------------------------|
| height  | 屏幕或显示层的高度信息 |

## 3. 数据结构描述

### 3.1 type

| 类型    | 参数取值 | 备注                              |
|---------|-----------------------------------|-----------------------------------|
| VIRT    | 640x480@90                        | *默认值* <br> `IDE` 调试专用，不在外接屏幕上显示内容 <br> 用户可自定义设置分辨率 (64x64)-(4096x4096) 和帧率 (1-200) |
| DEBUGGER | | 调试屏幕专用 |
| ST7701  | Display.init(Display.ST7701, width = 800, height = 480) | *默认值*<br>800x480 |
|         | Display.init(Display.ST7701, width = 480, height = 800) | 480x800 |
|         | Display.init(Display.ST7701, width = 854, height = 480) | 854x480 |
|         | Display.init(Display.ST7701, width = 480, height = 854) | 480x854 |
|         | Display.init(Display.ST7701, width = 640, height = 480) | 640x480 |
|         | Display.init(Display.ST7701, width = 480, height = 640) | 480x640 |
|         | Display.init(Display.ST7701, width = 368, height = 552) | 368x552 |
|         | Display.init(Display.ST7701, width = 552, height = 368) | 552x368 |
| HX8399  | Display.init(Display.HX8399, width = 1920, height = 1080) | *默认值*<br>1920x1080 |
|         | Display.init(Display.HX8399, width = 1080, height = 1920) | 1920x1080 |
| ILI9806 | Display.init(Display.ILI9806, width = 800, height = 480) | *默认值*<br>800x480 |
|         | Display.init(Display.ILI9806, width = 480, height = 800) | 480x800 |
| LT9611  | Display.init(Display.LT9611, width = 1920, height = 1080, fps = 30) | *默认值*<br>1920x1080@30 |
|         | Display.init(Display.LT9611, width = 1920, height = 1080, fps = 60) | 1920x1080@60 |
|         | Display.init(Display.LT9611, width = 1280, height = 720, fps = 60) | 1280x720@60 |
|         | Display.init(Display.LT9611, width = 1280, height = 720, fps = 50) | 1280x720@50 |
|         | Display.init(Display.LT9611, width = 1280, height = 720, fps = 30) | 1280x720@30 |
|         | Display.init(Display.LT9611, width = 640, height = 480, fps = 60) | 640x480@60 |

### 3.2 layer

K230 提供 2 层视频图层支持和 4 层 OSD 图层支持。分列如下：

| 显示层     | 说明                                     | 备注          |
|------------|------------------------------------------|---------------|
| LAYER_VIDEO1 |                                          | 仅可在 [bind_layer](#24-bind_layer) 中使用,支持硬件旋转 |
| LAYER_VIDEO2 |                                          | 仅可在 [bind_layer](#24-bind_layer) 中使用,不支持硬件旋转 |
| LAYER_OSD0  |                                          | 支持 [show_image](#22-show_image) 和 [bind_layer](#24-bind_layer) 使用 |
| LAYER_OSD1  |                                          | 支持 [show_image](#22-show_image) 和 [bind_layer](#24-bind_layer) 使用 |
| LAYER_OSD2  |                                          | 支持 [show_image](#22-show_image) 和 [bind_layer](#24-bind_layer) 使用 |
| LAYER_OSD3  |                                          | 支持 [show_image](#22-show_image) 和 [bind_layer](#24-bind_layer) 使用 |

### 3.3 flag

| 标志               | 说明            | 备注 |
|-------------------|-----------------|------|
| FLAG_ROTATION_0   | 旋转 `0` 度      |      |
| FLAG_ROTATION_90  | 旋转 `90` 度     |      |
| FLAG_ROTATION_180 | 旋转 `180` 度    |      |
| FLAG_ROTATION_270 | 旋转 `270` 度    |      |
| FLAG_MIRROR_NONE  | 不镜像          |      |
| FLAG_MIRROR_HOR   | 水平镜像        |      |
| FLAG_MIRROR_VER   | 垂直镜像        |      |
| FLAG_MIRROR_BOTH  | 水平与垂直镜像  |      |

## 4. 示例程序

```python
from media.display import *  # 导入 display 模块，使用 display 相关接口
from media.media import *    # 导入 media 模块，使用 media 相关接口
import os, time, image       # 导入 image 模块，使用 image 相关接口

# 使用 LCD 作为显示输出
Display.init(Display.ST7701, width=800, height=480, to_ide=True)
# 初始化媒体管理器
MediaManager.init()

# 创建用于绘图的图像
img = image.Image(800, 480, image.RGB565)
img.clear()
img.draw_string_advanced(0, 0, 32, "Hello World!，你好世界！！！", color=(255, 0, 0))

Display.show_image(img)

try:
    while True:
        time.sleep(1)
        os.exitpoint()
except KeyboardInterrupt as e:
    print(" 用户停止：", e)
except BaseException as e:
    print(f" 异常：{e}")

Display.deinit()
MediaManager.deinit()
```
