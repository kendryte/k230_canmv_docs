# 3.2 Display 模块 API 手册

```{attention}
该模块自固件版本 V0.7 起有显著更改，若您使用的是 V0.7 之前的固件，请参考旧版本文档。
```

## 1. 概述

本手册旨在指导开发人员使用 Micro Python API 调用 CanMV Display 模块，实现图像显示功能。

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
| width    | 分辨率宽度                   | 输入      | 默认值根据 `type` 决定 |
| height   | 分辨率高度                   | 输入      | 默认值根据 `type` 决定 |
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

## 3. 数据结构描述

### 3.1 type

| 类型    | 分辨率 <br>(width x height @ fps) | 备注                              |
|---------|-----------------------------------|-----------------------------------|
| LT9611  | 1920x1080@30                      | *默认值*                          |
|         | 1280x720@30                       |                                   |
|         | 640x480@60                        |                                   |
| HX8377  | 1080x1920@30                      | *默认值*                          |
| ST7701  | 800x480@30                        | *默认值*<br> 可设置为竖屏 480x800  |
|         | 854x480@30                        | 可设置为竖屏 480x854               |
| VIRT    | 640x480@90                        | *默认值*                          |
|         |                                   | `IDE` 调试专用，不在外接屏幕上显示内容 <br> 用户可自定义设置分辨率 (64x64)-(4096x4096) 和帧率 (1-200) |

### 3.2 layer

K230 提供 2 层视频图层支持和 4 层 OSD 图层支持。分列如下：

| 显示层     | 说明                                     | 备注          |
|------------|------------------------------------------|---------------|
| LAYER_VIDEO1 |                                          | 仅可在 [bind_layer](#24-bind_layer) 中使用 |
| LAYER_VIDEO2 |                                          | 仅可在 [bind_layer](#24-bind_layer) 中使用 |
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

以下为示例程序：

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
