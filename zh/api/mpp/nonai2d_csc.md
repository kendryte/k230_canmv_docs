# 3.13 NONAI2D CSC API 手册

## 1. 概述

K230芯片内置24个硬件色彩空间转换(CSC)通道，能够高效地进行图像色彩空间转换处理。该模块支持多种图像格式转换，包括RGB/YUV等常见格式，适用于视频处理、图像显示等场景。

## 2. API 参考

### 2.1 构造函数

**功能**  
初始化CSC转换通道

**语法**  

```python
from nonai2d import CSC
csc = CSC(chn, fmt, max_width=1920, max_height=1080, buf_num=2)
```

**参数说明**  

| 参数       | 类型  | 说明                                                                 | 默认值   |
|------------|-------|--------------------------------------------------------------------|----------|
| chn        | int   | CSC通道号，取值范围0-23                                            | 无       |
| fmt        | int   | 目标图像格式(见常量定义)                                            | 无       |
| max_width  | int   | 支持处理的最大图像宽度(像素)                                        | 1920     |
| max_height | int   | 支持处理的最大图像高度(像素)                                        | 1080     |
| buf_num    | int   | 分配的VB缓冲区数量，影响处理性能                                    | 2        |

**返回值**  
成功返回CSC对象，失败抛出异常

> **重要说明**  
>
> 1. 必须在调用`MediaManager.init()`之前初始化CSC对象  
> 1. 通道号0-23不可重复使用  
> 1. 建议根据实际图像尺寸设置max_width/max_height以节省内存

### 2.2 convert方法

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

### 2.3 destroy方法

**功能**  
释放CSC通道资源

**语法**  

```python
csc.destroy()
```

**说明**  
调用后将释放该CSC通道占用的所有资源，不可再使用该对象

## 3. 常量定义

### 图像格式常量

| 常量名称                     | 说明                          | 典型应用场景              |
|------------------------------|-----------------------------|-------------------------|
| PIXEL_FORMAT_GRAYSCALE       | 灰度图像格式                  | 黑白图像处理             |
| PIXEL_FORMAT_RGB_565         | RGB565格式(大端)              | LCD显示                 |
| PIXEL_FORMAT_RGB_565_LE      | RGB565格式(小端)              | 特殊显示设备             |
| PIXEL_FORMAT_BGR_565         | BGR565格式(大端)              | OpenCV兼容处理          |
| PIXEL_FORMAT_BGR_565_LE      | BGR565格式(小端)              | 特殊显示设备             |
| PIXEL_FORMAT_RGB_888         | RGB888格式                   | 高质量图像处理           |
| PIXEL_FORMAT_BGR_888         | BGR888格式                   | OpenCV兼容处理          |
| PIXEL_FORMAT_ARGB_8888       | ARGB8888格式(带透明度)        | 图形界面合成             |
| PIXEL_FORMAT_YVU_PLANAR_420  | YVU420平面格式               | 视频解码输出             |
| PIXEL_FORMAT_YUV_SEMIPLANAR_420 | YUV420半平面格式            | 视频编码输入             |

## 4. 最佳实践

```python
import time, os, urandom, sys

from media.display import *
from media.media import *
from media.uvc import *

from nonai2d import CSC

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# hardware Color Space Converter
csc = CSC(0, CSC.PIXEL_FORMAT_RGB_565)

# use lcd as display output
Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)
# init media manager
MediaManager.init()

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
# release media buffer
MediaManager.deinit()
```
