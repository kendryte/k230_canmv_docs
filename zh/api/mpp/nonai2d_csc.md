# `NONAI2D CSC` 模块 API 手册

## 概述

K230芯片内置24个硬件色彩空间转换(CSC)通道，能够高效地进行图像色彩空间转换处理。该模块支持多种图像格式转换，包括RGB/YUV等常见格式，适用于视频处理、图像显示等场景。

## API 参考

### 构造函数

**功能**  
初始化CSC转换通道。通道号由系统自动分配，无需用户指定。

**语法**  

```python
from nonai2d import CSC
csc = CSC(fmt, max_width=1920, max_height=1080, buf_num=2)
```

**参数说明**  

| 参数       | 类型  | 说明                                                                 | 默认值   |
|------------|-------|--------------------------------------------------------------------|----------|
| fmt        | int   | 目标图像格式(见常量定义)                                            | 无       |
| max_width  | int   | 支持处理的最大图像宽度(像素)                                        | 1920     |
| max_height | int   | 支持处理的最大图像高度(像素)                                        | 1080     |
| buf_num    | int   | 分配的VB缓冲区数量，影响处理性能                                    | 2        |

**返回值**  
成功返回CSC对象，失败抛出异常

> **重要说明**  
>
> 1. 通道号由系统自动分配（0-23范围内），用户无需也无法指定  
> 1. 建议根据实际图像尺寸设置max_width/max_height以节省内存  
> 1. 当 `fmt=PIXEL_FORMAT_GRAYSCALE` 时，内部会先转换为 YUV420SP 再提取灰度通道

**属性**  

| 属性名   | 类型 | 描述                   |
|----------|------|-----------------------|
| `chn`    | int  | 系统分配的 CSC 通道号   |
| `dst_fmt`| int  | 目标图像格式            |

### convert方法

**功能**  
执行图像色彩空间转换

**语法**  

```python
result = csc.convert(frame, timeout_ms=1000, cvt=True)
```

**参数说明**  

| 参数          | 类型                  | 说明                                                                 | 默认值   |
|---------------|-----------------------|--------------------------------------------------------------------|----------|
| frame         | py_video_frame_info   | 输入图像帧(Sensor.snapshot获取)                                     | 无       |
| timeout_ms    | int                   | 转换超时时间(毫秒)                                                  | 1000     |
| cvt           | bool                  | True返回Image对象，False返回py_video_frame_info                     | True     |

**返回值**  
根据cvt参数返回转换后的Image对象或py_video_frame_info

### get_frame方法

**功能**  
从CSC通道获取转换后的帧（低级别接口，不自动转换为Image）。

**语法**  

```python
frame = csc.get_frame(timeout_ms=1000)
```

**参数说明**  

| 参数          | 类型  | 说明                | 默认值   |
|---------------|-------|-------------------|----------|
| timeout_ms    | int   | 超时时间(毫秒)      | 1000     |

**返回值**  
成功返回 `py_video_frame_info` 对象，超时返回 `None`

> **注意**：使用 `get_frame` 获取的帧需要手动调用 `release_frame` 释放。

### release_frame方法

**功能**  
释放通过 `get_frame` 获取的帧。

**语法**  

```python
csc.release_frame(frame)
```

**参数说明**  

| 参数          | 类型                  | 说明                |
|---------------|-----------------------|-------------------|
| frame         | py_video_frame_info   | 需要释放的帧对象     |

### destroy方法

**功能**  
释放CSC通道资源

**语法**  

```python
csc.destroy()
```

**说明**  
调用后将释放该CSC通道占用的所有资源，不可再使用该对象

## 常量定义

### 图像格式常量

| 常量名称                          | 说明                          | 典型应用场景              |
|-----------------------------------|-----------------------------|-------------------------|
| PIXEL_FORMAT_GRAYSCALE            | 灰度图像格式                  | 黑白图像处理             |
| PIXEL_FORMAT_RGB_565              | RGB565格式(大端)              | LCD显示                 |
| PIXEL_FORMAT_RGB_565_LE           | RGB565格式(小端)              | 特殊显示设备             |
| PIXEL_FORMAT_BGR_565              | BGR565格式(大端)              | OpenCV兼容处理          |
| PIXEL_FORMAT_BGR_565_LE           | BGR565格式(小端)              | 特殊显示设备             |
| PIXEL_FORMAT_RGB_888              | RGB888格式                   | 高质量图像处理           |
| PIXEL_FORMAT_BGR_888              | BGR888格式                   | OpenCV兼容处理          |
| PIXEL_FORMAT_ARGB_8888            | ARGB8888格式(带透明度)        | 图形界面合成             |
| PIXEL_FORMAT_ARGB_1555            | ARGB1555格式(带透明度)        | 低色彩深度UI             |
| PIXEL_FORMAT_ARGB_4444            | ARGB4444格式(带透明度)        | 低色彩深度UI             |
| PIXEL_FORMAT_BGR_888_PLANAR       | BGR888平面格式               | 专业图像处理             |
| PIXEL_FORMAT_RGB_888_PLANAR       | RGB888平面格式               | 专业图像处理             |
| PIXEL_FORMAT_YVU_PLANAR_420       | YVU420平面格式               | 视频解码输出             |
| PIXEL_FORMAT_YUV_SEMIPLANAR_420   | YUV420半平面格式             | 视频编码输入             |
| PIXEL_FORMAT_YVU_SEMIPLANAR_420   | YVU420半平面格式             | 视频处理                 |
| PIXEL_FORMAT_YVU_PLANAR_444       | YVU444平面格式               | 高质量视频处理           |
| PIXEL_FORMAT_YUV_PACKAGE_444      | YUV444打包格式               | 高质量视频处理           |
| PIXEL_FORMAT_YUV_SEMIPLANAR_444   | YUV444半平面格式             | 高质量视频处理           |
| PIXEL_FORMAT_YVU_SEMIPLANAR_444   | YVU444半平面格式             | 高质量视频处理           |

## 最佳实践

```python
import time, os, urandom, sys

from media.display import *
from media.media import *
from media.uvc import *

from nonai2d import CSC

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# hardware Color Space Converter (通道号自动分配)
csc = CSC(CSC.PIXEL_FORMAT_RGB_565)

# use lcd as display output
Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)

while True:
    plugin, dev = UVC.probe()
    if plugin:
        print(f"detect USB Camera {dev}")
        break
    time.sleep_ms(100)

mode = UVC.video_mode(640, 480, UVC.FORMAT_MJPEG, 30)

succ, mode = UVC.select_video_mode(mode)
print(f"select mode success: {succ}, mode: {mode}")

UVC.start(cvt = True)

clock = time.clock()

while True:
    clock.tick()

    img = UVC.snapshot()
    if img is not None:
        img = csc.convert(img)
        Display.show_image(img)

    print(clock.fps())

# deinit display
Display.deinit()
csc.destroy()
UVC.stop()

time.sleep_ms(100)
```
