# 3.13 UVC API 手册

## 1. 概述

UVC模块提供了USB摄像头的检测、配置和图像采集功能，支持单摄像头操作。

## 2. API参考

### 2.1 UVC.probe - 检测摄像头

**功能**  

检测系统是否连接了USB摄像头（当前仅支持单个摄像头检测）。

**语法**

```python
from media.uvc import UVC
plugin, devname = UVC.probe()
```

**返回值**

| 参数 | 类型 | 说明 |
|------|------|------|
| plugin | bool | 是否检测到摄像头 |
| devname | str | 摄像头设备信息（厂家#产品） |

**示例**

```python
plugin, devinfo = UVC.probe()
print(f"摄像头检测: {'已连接' if plugin else '未连接'}, 设备信息: {devinfo}")
```

### 2.2 UVC.video_mode - 视频模式操作

**功能**  

构造或获取当前视频模式配置。

**语法**

```python
# 获取当前模式
mode = UVC.video_mode()

# 创建新配置
mode = UVC.video_mode(width, height, format, fps)
```

**参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| width | int | 分辨率宽度（像素） |
| height | int | 分辨率高度（像素） |
| format | int | 图像格式（见常量定义） |
| fps | int | 帧率（fps） |

**返回值**  

返回`uvc_video_mode`对象

### 2.3 UVC.list_video_mode - 列举支持模式

**功能**  

获取摄像头支持的所有视频模式。

**语法**

```python
modes = UVC.list_video_mode()
```

**返回值**  

返回支持的`uvc_video_mode`列表

**示例**

```python
for i, mode in enumerate(UVC.list_video_mode()):
    print(f"模式{i}: {mode.width}x{mode.height} {mode.format}@{mode.fps}fps")
```

### 2.4 UVC.select_video_mode - 选择视频模式

**功能**  

设置摄像头输出模式。

**语法**

```python
succ, actual_mode = UVC.select_video_mode(mode)
```

**参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| mode | uvc_video_mode | 要设置的视频模式 |

**返回值**

| 参数 | 类型 | 说明 |
|------|------|------|
| succ | bool | 是否设置成功 |
| actual_mode | uvc_video_mode | 实际生效的模式 |

### 2.5 UVC.start - 启动视频流

**功能**  

开始摄像头视频流输出。

**语法**

```python
success = UVC.start()
```

**返回值**  

返回bool表示是否启动成功

### 2.6 UVC.stop - 停止视频流

**功能**  

停止视频流并释放资源。

**语法**

```python
UVC.stop()
```

### 2.7 UVC.snapshot - 捕获帧

**功能**  

从视频流中捕获一帧图像。

**语法**

```python
frame = UVC.snapshot()
```

**返回值**  
返回YUV422或JPEG格式的图像数据

## 3. 数据结构

### uvc_video_mode结构

```python
class uvc_video_mode:
    width: int    # 分辨率宽度
    height: int   # 分辨率高度
    format: int   # 图像格式
    fps: int      # 帧率(fps)
```

## 4. 常量定义

| 常量 | 值 | 说明 |
|------|----|------|
| UVC.FORMAT_MJPEG | 1 | MJPG压缩格式（推荐，带宽低） |
| UVC.FORMAT_UNCOMPRESS | 2 | YUV422未压缩格式（带宽高） |

## 5. 使用流程建议

1. 检测摄像头 (`probe()`)
1. 列举支持模式 (`list_video_mode()`)
1. 选择合适模式 (`select_video_mode()`)
1. 启动视频流 (`start()`)
1. 捕获图像 (`snapshot()`)
1. 停止视频流 (`stop()`)

## 6. 最佳实践

```python
import time, os, urandom, sys

from media.display import *
from media.media import *
from media.uvc import *

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# use lcd as display output
Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)
# init media manager
MediaManager.init()

while True:
    plugin, dev = UVC.probe()
    if plugin:
        print(f"detect USB Camera {dev}")
        break

mode = UVC.video_mode(640, 480, UVC.FORMAT_MJPEG, 30)

succ, mode = UVC.select_video_mode(mode)
print(f"select mode success: {succ}, mode: {mode}")

UVC.start()

while True:
    img = UVC.snapshot()
    if img is not None:
        img = img.to_rgb565()
        Display.show_image(img)

# deinit display
Display.deinit()
UVC.stop()
time.sleep_ms(100)
# release media buffer
MediaManager.deinit()
```
