# `Display` 模块 API 手册

```{attention}
该模块自固件版本 V0.7 起有较大更改，若您使用的是 V0.7 之前的固件，请参考旧版本文档。
```

## 概述

本手册旨在指导开发人员使用 Micro Python API 调用 CanMV Display 模块，实现图像显示功能。

如需增加自定义屏幕，可参考[Display Debugger](../../example/media/how_to_add_new_mipi_panel.md)

## API 介绍

### init

**描述**

初始化 Display 通路，包括 VO 模块、 DSI 模块和 LCD/HDMI。

**语法**  

```python
init(type, width=0, height=0, fps=0, flag=0, osd_num=1, to_ide=False, quality=90)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| type     | [显示设备类型](#type)     | 输入      | 必选 |
| width    | 分辨率宽度                   | 输入      | 可选参数，默认值根据 `type` 决定 |
| height   | 分辨率高度                   | 输入      | 可选参数，默认值根据 `type` 决定 |
| fps      | 显示帧率                     | 输入      | 仅部分显示设备类型支持指定帧率 |
| flag     | 显示[标志](#flag)           | 输入      |                   |
| osd_num  | 在 [show_image](#show_image) 时支持的 OSD 图层数量 | 输入 | 越大占用内存越多，默认值为1 |
| to_ide   | 是否将屏幕显示传输到 IDE 显示 | 输入      | 开启时占用更多内存，通过 WBC 功能实现 |
| quality  | 设置 JPEG 压缩质量          | 输入      | 仅在 `to_ide=True` 时有效，范围 [10-100]，默认90 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### deinit

**描述**

执行反初始化，deinit 方法会关闭整个 Display 通路，包括 VO 模块、DSI 模块和 LCD/HDMI。

**语法**  

```python
deinit()
```

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### inited

**描述**

查询 Display 模块是否已初始化。

**语法**  

```python
inited()
```

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| bool   | `True` 表示已初始化，`False` 表示未初始化 |

### config_layer

**描述**

配置显示层的属性。此方法通常在绑定层之前调用，用于设置图层的显示参数。

**语法**  

```python
config_layer(rect, pix_format, layer, alpha=255, flag=0)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| rect     | 显示区域 (x, y, w, h)          | 输入      | 必选，元组形式 |
| pix_format | 图像像素格式                | 输入      | 参见 [pix_format](#pix_format) |
| layer    | [显示层](#layer) ID           | 输入      | 必选，指定要配置的图层 |
| alpha    | 图层混合透明度                | 输入      | 范围 0-255，默认255（不透明） |
| flag     | 显示[标志](#flag)             | 输入      | 默认0 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| int    | 配置的图层 ID                   |

### bind_layer

**描述**

将 `sensor` 或 `vdec` 模块的输出绑定到屏幕显示。无需用户手动干预即可持续显示图像。

**语法**  

```python
bind_layer(src, rect, pix_format, layer, alpha=255, flag=0)
```

**参数**

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| src      | 源通道信息 (mod, dev, chn)    | 输入      | 可通过 `sensor.bind_info()` 获取，格式为元组 |
| rect     | 显示区域 (x, y, w, h)          | 输入      | 可通过 `sensor.bind_info()` 获取 |
| pix_format | 图像像素格式                | 输入      | 可通过 `sensor.bind_info()` 获取 |
| layer    | 绑定到 Display 的[显示层](#layer) | 输入      | 可绑定到 `video` 或 `osd` 层 |
| alpha    | 图层混合透明度                | 输入      | 范围 0-255，默认255 |
| flag     | 显示[标志](#flag)             | 输入      | 默认0 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### unbind_layer

**描述**

解绑指定图层的绑定关系。

**语法**  

```python
unbind_layer(layer)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| layer    | [显示层](#layer) ID           | 输入      | 必选 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| bool   | `True` 表示解绑成功，`False` 表示失败 |

### disable_layer

**描述**

禁用指定的显示层。

**语法**  

```python
disable_layer(layer)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| layer    | [显示层](#layer) ID           | 输入      | 必选 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### show_image

**描述**

在屏幕上显示图像。

**语法**  

```python
show_image(img, x=0, y=0, layer=Display.LAYER_OSD0, alpha=None, pixel_format=None, flag=0)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| img      | 要显示的图像对象             | 输入      | 必选 |
| x        | 起始坐标的 x 值              | 输入      | 默认0 |
| y        | 起始坐标的 y 值              | 输入      | 默认0 |
| layer    | 显示到[指定层](#layer)       | 输入      | 仅支持 OSD 层，默认 `LAYER_OSD0` |
| alpha    | 图层混合透明度               | 输入      | 范围 0-255，`None` 表示使用图层原有设置 |
| pixel_format | 图像像素格式             | 输入      | `None` 表示使用图像原有格式，参见 [pix_format](#pix_format) |
| flag     | 显示[标志](#flag)            | 输入      | 默认0 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| 无     |                                 |

### width

**描述**

获取屏幕或某一图层的显示宽度。

**语法**

```python
width(layer=None)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| layer    | 指定获取[显示层](#layer)的宽度 | 输入      | 可选，如果不传则表示获取屏幕的分辨率宽度 |

**返回值**  

| 返回值 | 描述                            |
|--------|---------------------------------|
| width  | 屏幕或显示层的宽度信息，单位像素 |

### height

**描述**

获取屏幕或某一图层的显示高度。

**语法**

```python
height(layer=None)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| layer    | 指定获取[显示层](#layer)的高度 | 输入      | 可选，如果不传则表示获取屏幕的分辨率高度 |

**返回值**

| 返回值 | 描述                            |
|--------|---------------------------------|
| height | 屏幕或显示层的高度信息，单位像素 |

### fps

**描述**

获取当前的显示帧率。

**语法**

```python
fps()
```

**返回值**

| 返回值 | 描述                            |
|--------|---------------------------------|
| int    | 当前的显示帧率，单位 fps        |

### writeback

**描述**

查询或设置 WriteBack (WBC) 功能状态。WBC 功能用于将屏幕显示内容回传，通常用于传输到 IDE 显示。

**语法**

```python
writeback(enable=None)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| enable   | 设置 WBC 功能状态             | 输入      | 可选，`True` 表示开启，`False` 表示关闭。不传参时表示查询当前状态 |

**返回值**

| 返回值 | 描述                            |
|--------|---------------------------------|
| bool   | 查询时返回当前 WBC 状态；设置时返回操作结果 |

### writeback_dump

**描述**

从 WBC 抓取一帧显示内容。需要在 [init](#init) 时设置 `to_ide=True` 且 WBC 功能已开启。

**语法**

```python
writeback_dump(timeout=1000)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 | 说明 |
|----------|-------------------------------|-----------|------|
| timeout  | 超时时间（毫秒）              | 输入      | 默认1000ms |

**返回值**

| 返回值 | 描述                            |
|--------|---------------------------------|
| object | 返回包含视频帧信息的对象        |

## 数据结构描述

### type

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
|         | Display.init(Display.ST7701, width = 368, height = 544) | 368x544 |
|         | Display.init(Display.ST7701, width = 544, height = 368) | 544x368 |
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
| ILI9881 | Display.init(Display.ILI9881, width = 1280, height = 800) | *默认值*<br>1280x800 |
|         | Display.init(Display.ILI9881, width = 800, height = 1280) | 800x1280 |
| NT35516 | Display.init(Display.NT35516, width=960, height=536) | *默认值*<br>960x536 |
|         | Display.init(Display.NT35516, width=536, height=960) | 536x960 |
| NT35532 | Display.init(Display.NT35532, width=1920, height=1080) | *默认值*<br>1920x1080 |
|         | Display.init(Display.NT35532, width=1080, height=1920) | 1080x1920 |
| GC9503  | Display.init(Display.GC9503, width=800, height=480) | *默认值*<br>800x480 |
|         | Display.init(Display.GC9503, width=480, height=800) | 480x800 |
| ST7102  | Display.init(Display.ST7102, width=640, height=480) | *默认值*<br>640x480 |
|         | Display.init(Display.ST7102, width=480, height=640) | 480x640 |
| AML020T | Display.init(Display.AML020T, width=480, height=360) | *默认值*<br>480x360 |
|         | Display.init(Display.AML020T, width=360, height=480) | 360x480 |
| JD9852  | Display.init(Display.JD9852, width=320, height=240) | *默认值*<br>320x240 |
|         | Display.init(Display.JD9852, width=240, height=320) | 240x320 |

### layer

K230 提供 3 层视频图层支持和 4 层 OSD 图层支持。分类如下：

| 显示层 | 常量名 | 说明 | 支持格式 |
|--------|--------|------|----------|
| 视频层1 | `Display.LAYER_VIDEO1` | 建议用来显示视频数据 | 仅支持 `YUV420SP` |
| 视频层2 | `Display.LAYER_VIDEO2` | 建议用来显示视频数据 | 仅支持 `YUV420SP` |
| 视频层3 | `Display.LAYER_VIDEO3` | 建议用来显示视频数据 | 仅支持 `YUV420SP` |
| OSD层0 | `Display.LAYER_OSD0` | 图形叠加层 | 仅支持 RGB 颜色空间 |
| OSD层1 | `Display.LAYER_OSD1` | 图形叠加层 | 仅支持 RGB 颜色空间 |
| OSD层2 | `Display.LAYER_OSD2` | 图形叠加层 | 仅支持 RGB 颜色空间 |
| OSD层3 | `Display.LAYER_OSD3` | 图形叠加层 | 仅支持 RGB 颜色空间 |

### flag

| 标志 | 常量名 | 说明 |
|------|--------|------|
| 不旋转 | `Display.FLAG_ROTATION_NONE` 或 `0` | 不进行旋转 |
| 旋转0度 | `Display.FLAG_ROTATION_0` | 旋转 0 度 |
| 旋转90度 | `Display.FLAG_ROTATION_90` | 旋转 90 度 |
| 旋转180度 | `Display.FLAG_ROTATION_180` | 旋转 180 度 |
| 旋转270度 | `Display.FLAG_ROTATION_270` | 旋转 270 度 |
| 无镜像 | `Display.FLAG_MIRROR_NONE` 或 `0` | 不进行镜像 |
| 水平镜像 | `Display.FLAG_MIRROR_HOR` | 水平镜像 |
| 垂直镜像 | `Display.FLAG_MIRROR_VER` | 垂直镜像 |
| 水平和垂直镜像 | `Display.FLAG_MIRROR_BOTH` | 同时进行水平和垂直镜像 |

### pix_format

| 颜色格式 | 常量名 | 说明 |
|---------|--------|------|
| 灰度图 | `image.GRAYSCALE` 或 `PIXFORMAT_GRAYSCALE` | 8位灰度格式，每个像素1字节 |
| RGB565 | `image.RGB565` 或 `PIXFORMAT_RGB565` | RGB格式，16位/像素 (5:6:5) |
| ARGB8888 | `image.ARGB8888` 或 `PIXFORMAT_ARGB8888` | ARGB格式，32位/像素 (A:R:G:B) |
| ABGR8888 | `image.ABGR8888` 或 `PIXFORMAT_ABGR8888` | ABGR格式，32位/像素 (A:B:G:R) |
| RGBA8888 | `image.RGBA8888` 或 `PIXFORMAT_RGBA8888` | RGBA格式，32位/像素 (R:G:B:A) |
| BGRA8888 | `image.BGRA8888` 或 `PIXFORMAT_BGRA8888` | BGRA格式，32位/像素 (B:G:R:A) |
| RGB888 | `image.RGB888` 或 `PIXFORMAT_RGB888` | RGB格式，24位/像素 (R:G:B) |
| BGR888 | `image.BGR888` 或 `PIXFORMAT_BGR888` | BGR格式，24位/像素 (B:G:R) |

## 注意事项

1. **图层支持**：`show_image` 仅支持 OSD 图层，如需使用多个 OSD 图层，请在 `init` 时设置 `osd_num` 参数。
1. **图像尺寸**：调用 `show_image` 时，图像的尺寸不能超过屏幕分辨率。
1. **旋转处理**：某些屏幕类型（如 ST7701 的 368x544 模式）存在硬件尺寸和应用尺寸的差异，API 会自动处理这种转换。
1. **WBC 功能**：如需使用 `writeback_dump` 抓取屏幕内容，必须在 `init` 时设置 `to_ide=True`。

## 示例程序

### 基础显示示例

```python
from media.display import *
from media.media import *
import os, time, image

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
    print("用户停止：", e)
except BaseException as e:
    print(f"异常：{e}")

Display.deinit()
MediaManager.deinit()
```

### 绑定 Sensor 示例

```python
from media.display import *
from media.sensor import *
from media.media import *
import time

# 初始化 sensor
sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=800, height=480)
sensor.set_pixformat(Sensor.RGB565)

# 获取 sensor 绑定信息
bind_info = sensor.bind_info()

# 配置并绑定显示层
Display.config_layer(rect=(0, 0, 800, 480), 
                     pix_format=bind_info[2], 
                     layer=Display.LAYER_VIDEO1)
Display.bind_layer(src=bind_info[0], 
                   rect=bind_info[1], 
                   pix_format=bind_info[2], 
                   layer=Display.LAYER_VIDEO1)

# 初始化显示
Display.init(Display.ST7701, width=800, height=480)
MediaManager.init()

# 启动 sensor
sensor.run()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("用户停止")
finally:
    sensor.stop()
    Display.deinit()
    MediaManager.deinit()
```
