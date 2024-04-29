# K230 CanMV Lcd模块API手册

![cover](../images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

此文档介绍CanMV lcd模块，用以指导开发人员如何调用MicroPython API实现图像输出功能。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
|  VO  | Video Output |
|  DSI | Display Serial Interface |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 赵忠祥      | 2024-04-25 |

## 1. 概述

此文档介绍CanMV lcd模块，用以指导开发人员如何调用Micro Python API实现图像输出功能。

## 2. API描述

### 2.1 lcd.init

【描述】

初始化整个lcd通路，包括VO模块、DSI模块、LCD/HDMI

【语法】

```python
lcd.init(type)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| type | 输出接口参数 | 输入 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为\[错误码\] |

【注意】

无

【举例】

无

【相关主题】

无

### 2.2 lcd.set_backlight

【描述】

设置LCD背光

【语法】

```python
lcd.set_backlight(level)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| level | 0：关闭LCD背光；1：打开LCD背光 | 输入 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为\[错误码\] |

【注意】

set_backlight仅适用于LCD输出

【举例】

无

【相关主题】

无

### 2.3 lcd.set_plane

【描述】

设置VO通道参数，set_plane方法主要用来设置和Camera、vdec、DPU、AI2D绑定的VO通道

【语法】

```python
lcd.set_plane(x, y, width, height, pixelformat, rotate, chn, mirror)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| x | 起始坐标的x值 | 输入 |
| y | 起始坐标的y值 | 输入 |
| width | 宽度 | 输入 |
| height | 高度 | 输入 |
| pixelformat | 像素格式 | 输入 |
| rotate | 顺时针旋转功能 | 输入 |
| chn | VO通道 | 输入 |
| mirror | 翻转功能 | 输入 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为\[错误码\] |

【注意】

只有DISPLAY_CHN_VIDEO1通道支持rotate功能和mirror功能

【举例】

无

【相关主题】

无

### 2.4 lcd.display

【描述】

输出image到VO通道

【语法】

```python
lcd.display(image, x, y, chn)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| image | 待输出的图像 | 输入 |
| x | 起始坐标的x值 | 输入 |
| y | 起始坐标的y值 | 输入 |
| chn | VO通道 | 输入 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为\[错误码\] |

【注意】

无

【举例】

无

【相关主题】

无

### 2.5 lcd.disable_plane

【描述】

关闭VO通道

【语法】

```python
lcd.disable_plane(chn)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| chn | VO通道 | 输入 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为\[错误码\] |

【注意】

通过disable_plane方法关闭的VO通道，可以通过set_plane方法或者display方法重新打开

【举例】

无

【相关主题】

无

### 2.6 lcd.deinit

【描述】

执行反初始化，deinit方法会关闭整个lcd通路，包括VO模块、DSI模块、LCD/HDMI

【语法】

```python
lcd.deinit()
```

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为\[错误码\] |

【注意】

无

【举例】

无

【相关主题】

无

## 3. 数据结构描述

### 3.1 type

【说明】

输出接口参数

【定义】

【成员】

| 成员名称  | 描述                            |
|---------|---------------------------------|
| HX8377_1080X1920_30FPS | VO和DSI模块输出1080X1920 30FPS时序到LCD |
| ST7701_V1_MIPI_2LAN_480X800_30FPS | VO和DSI模块输出480x800 30FPS时序到LCD |
| LT9611_1920X1080_30FPS | VO和DSI模块输出1920X1080 30FPS时序到HDMI |
| LT9611_MIPI_4LAN_1920X1080_60FPS | VO和DSI模块输出1920X1080 60FPS时序到HDMI |
| LT9611_MIPI_4LAN_1280X720_60FPS | VO和DSI模块输出1280x720 60FPS时序到HDMI |
| LT9611_MIPI_4LAN_1280X720_50FPS | VO和DSI模块输出1280x720 50FPS时序到HDMI |
| LT9611_MIPI_4LAN_1280X720_30FPS | VO和DSI模块输出1280x720 30FPS时序到HDMI |
| LT9611_MIPI_4LAN_640X480_60FPS | VO和DSI模块输出640x480 30FPS时序到HDMI |

【注意事项】

无

### 3.2 chn

【说明】

VO通道

【定义】

【成员】

| 成员名称  | 描述                            |
|---------|---------------------------------|
| DISPLAY_CHN_VIDEO1 | VO模块video 1 通道，支持DISPLAY_OUT_NV12输出 |
| DISPLAY_CHN_VIDEO2 | VO模块video 2 通道，支持DISPLAY_OUT_NV12输出 |
| DISPLAY_CHN_OSD0 | VO模块OSD 0 通道，支持DISPLAY_OUT_ARGB8888、DISPLAY_OUT_RGB888、DISPLAY_OUT_RGB565输出 |
| DISPLAY_CHN_OSD1 | VO模块OSD 1 通道，支持DISPLAY_OUT_ARGB8888、DISPLAY_OUT_RGB888、DISPLAY_OUT_RGB565输出 |
| DISPLAY_CHN_OSD2 | VO模块OSD 2 通道，支持DISPLAY_OUT_ARGB8888、DISPLAY_OUT_RGB888、DISPLAY_OUT_RGB565输出 |
| DISPLAY_CHN_OSD3 | VO模块OSD 3 通道，支持DISPLAY_OUT_ARGB8888、DISPLAY_OUT_RGB888、DISPLAY_OUT_RGB565输出 |

【注意事项】

只有DISPLAY_CHN_VIDEO1通道支持rotate功能和mirror功能

### 3.3 pixelformat

【说明】

像素格式

【定义】

【成员】

| 成员名称  | 描述                            |
|---------|---------------------------------|
| DISPLAY_OUT_NV12 | 输出NV12  |
| DISPLAY_OUT_ARGB8888 | 输出ARGB8888 |
| DISPLAY_OUT_RGB888 | 输出RGB888 |
| DISPLAY_OUT_RGB565 | 输出RGB565 |

【注意事项】

无

### 3.4 mirror

【说明】

水平方向和垂直方向镜像翻转功能

【定义】

【成员】

| 成员名称  | 描述                            |
|---------|---------------------------------|
| DISPLAY_ROTATE_0 | 不进行旋转 |
| DISPLAY_ROTATE_90 | 顺时针旋转90度 |
| DISPLAY_ROTATE_180 | 顺时针旋转180度 |
| DISPLAY_ROTATE_270 | 顺时针旋转270度 |
| DISPLAY_MIRROR_NONE | 不进行翻转 |
| DISPLAY_MIRROR_HOR | 水平方向翻转180度 |
| DISPLAY_MIRROR_VER | 垂直方向翻转180度 |
| DISPLAY_MIRROR_BOTH | 水平方向和垂直方向都翻转180度 |

【注意事项】

无

## 4. 示例程序

例程

```python

from media.lcd import *
from media.media import *
import time, os, urandom, sys

DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

def lcd_test():
    print("lcd test")
    # use hdmi for lcd
    lcd.init(LT9611_1920X1080_30FPS)  // 实始化lcd
    # config vb for osd layer
    config = k_vb_config()            // 配置内存
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4*DISPLAY_WIDTH*DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE
    # meida buffer config
    media.buffer_config(config)
    # media buffer init
    media.buffer_init()
    # request media buffer for osd image
    globals()["buffer"] = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)

    # create image for drawing
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # create image for osd
    buffer = globals()["buffer"]
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888, alloc=image.ALLOC_VB, phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr, poolid=buffer.pool_id)
    osd_img.clear()
    lcd.display(osd_img, 0, 0, DISPLAY_CHN_OSD0) // 显示
    try:
        while True:
            img.clear()
            for i in range(10):
                x = (urandom.getrandbits(11) % img.width())
                y = (urandom.getrandbits(11) % img.height())
                r = (urandom.getrandbits(8))
                g = (urandom.getrandbits(8))
                b = (urandom.getrandbits(8))
                # If the first argument is a scaler then this method expects
                # to see x, y, and text. Otherwise, it expects a (x,y,text) tuple.
                # Character and string rotation can be done at 0, 90, 180, 270, and etc. degrees.
                img.draw_string(x, y, "Hello World!", color = (r, g, b), scale = 2, mono_space = False,
                                char_rotation = 0, char_hmirror = False, char_vflip = False,
                                string_rotation = 0, string_hmirror = False, string_vflip = False) // 绘图
            img.copy_to(osd_img)
            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)

    # deinit lcd
    lcd.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    media.release_buffer(globals()["buffer"])
    # deinit media buffer
    media.buffer_deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    lcd_test()

```
