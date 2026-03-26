# `UVC` 模块 API 手册

## 概述

`UVC` 模块用于在 CanMV Python 中访问 USB 摄像头。

模块使用 `FOURCC` 描述视频格式。支持的主机输入格式为：

- `UVC.FOURCC_YUY2`
- `UVC.FOURCC_UYVY`
- `UVC.FOURCC_NV12`
- `UVC.FOURCC_I420`
- `UVC.FOURCC_MJPEG`

默认只支持单个 UVC 摄像头。

## 推荐流程

1. `UVC.probe()` 检测摄像头
1. `UVC.list_video_mode()` 查看设备支持的模式
1. `UVC.video_mode(...)` 构造目标模式
1. `UVC.select_video_mode(...)` 选择并协商模式
1. `UVC.start(...)` 启动视频流
1. 循环调用 `UVC.snapshot()` 获取图像
1. `UVC.stop()` 停止视频流

建议在 `try/finally` 中调用 `UVC.stop()`，确保异常退出时也能正确停流。

## API 参考

### `UVC.probe()` - 检测摄像头

**功能**

检测系统当前是否接入 UVC 摄像头，并返回厂商/产品字符串。

**语法**

```python
from media.uvc import UVC

plugin, devname = UVC.probe()
```

**返回值**

| 返回值 | 类型 | 说明 |
|---|---|---|
| `plugin` | `bool` | 是否检测到 UVC 摄像头 |
| `devname` | `str` / `None` | 设备信息，格式为 `厂商#产品` |

**示例**

```python
plugin, devinfo = UVC.probe()
print(f"detect: {plugin}, devinfo: {devinfo}")
```

### `UVC.video_mode()` - 获取或构造视频模式

**功能**

- 无参数调用时：返回当前已协商的视频模式
- 带参数调用时：构造一个目标视频模式对象

**语法**

```python
# 获取当前模式
mode = UVC.video_mode()

# 构造目标模式
mode = UVC.video_mode(width, height, fourcc, fps)
```

**参数**

| 参数 | 类型 | 说明 |
|---|---|---|
| `width` | `int` | 图像宽度 |
| `height` | `int` | 图像高度 |
| `fourcc` | `int` | 像素格式，使用 `UVC.FOURCC_*` 常量 |
| `fps` | `int` | 目标帧率 |

**说明**

- `fourcc` 省略时默认使用 `UVC.FOURCC_MJPEG`
- `fps` 省略时会以 `frameinterval = 0` 传入底层，由驱动选择默认帧率
- `UVC.select_video_mode()` 成功后，返回的模式对象会被更新为协商后的实际值

### `UVC.list_video_mode()` - 列举设备支持模式

**功能**

枚举摄像头支持的全部模式列表。列表中的每一项都是一个 `uvc_video_mode` 对象，包含宽、高、`fourcc` 和 `fps`。

**语法**

```python
modes = UVC.list_video_mode()
```

**示例**

```python
for i, mode in enumerate(UVC.list_video_mode()):
    print(f"{i}: {mode}")
```

### `UVC.select_video_mode(mode)` - 选择视频模式

**功能**

根据用户给定的目标模式初始化 UVC 设备，并返回协商后的实际模式。

**语法**

```python
succ, actual_mode = UVC.select_video_mode(mode)
```

**参数**

| 参数 | 类型 | 说明 |
|---|---|---|
| `mode` | `uvc_video_mode` | 目标模式 |

**返回值**

| 返回值 | 类型 | 说明 |
|---|---|---|
| `succ` | `bool` | 是否初始化成功 |
| `actual_mode` | `uvc_video_mode` | 协商后的实际模式 |

**常用 `FOURCC`**

`UVC.select_video_mode()` 中传入的 `mode.fourcc` 通常使用以下常量：

| 常量 | 说明 |
|---|---|
| `UVC.FOURCC_YUY2` | YUY2 / YUYV 4:2:2 |
| `UVC.FOURCC_UYVY` | UYVY 4:2:2 |
| `UVC.FOURCC_NV12` | NV12 4:2:0 |
| `UVC.FOURCC_I420` | I420 4:2:0 |
| `UVC.FOURCC_MJPEG` | MJPEG 压缩格式 |

### `UVC.start()` - 启动视频流

**功能**

启动 UVC 视频流，并配置 `snapshot()` 的返回类型。

**语法**

```python
success = UVC.start(delay_ms=0, cvt=True)
```

**参数**

| 参数 | 类型 | 说明 |
|---|---|---|
| `delay_ms` | `int` | 启动后额外等待的毫秒数 |
| `cvt` | `bool` | 是否对 `snapshot()` 返回数据做格式转换 |

**`cvt` 语义**

| 输入格式 | `cvt=True` | `cvt=False` |
|---|---|---|
| `FOURCC_MJPEG` | `snapshot()` 返回 NV12 帧（内部走硬件 JPEG 解码） | 返回 JPEG 图像 |
| `FOURCC_YUY2` | 返回 RGB565 图像 | 返回 YUV422 图像 |
| `FOURCC_UYVY` | 返回 RGB565 图像 | 返回 YUV422 图像 |
| `FOURCC_NV12` | 不支持，会在 `snapshot()` 抛异常 | 返回 YUV420 图像 |
| `FOURCC_I420` | 不支持，会在 `snapshot()` 抛异常 | 返回 YUV420 图像 |

### `UVC.stop()` - 停止视频流

**功能**

停止 UVC 视频流并释放内部状态。

**语法**

```python
UVC.stop()
```

### `UVC.snapshot()` - 获取一帧图像

**功能**

从当前视频流中取出一帧图像。

**语法**

```python
frame = UVC.snapshot()
frame = UVC.snapshot(timeout_ms)
```

**参数**

| 参数 | 类型 | 说明 |
|---|---|---|
| `timeout_ms` | `int` | 获取一帧的超时时间，单位毫秒 |

**返回值**

返回类型与当前 `fourcc` 及 `UVC.start(cvt=...)` 配置有关：

| 当前模式 | 返回对象 |
|---|---|
| `MJPEG + cvt=True` | NV12 视频帧对象 |
| `MJPEG + cvt=False` | JPEG `Image` |
| `YUY2/UYVY + cvt=True` | RGB565 `Image` |
| `YUY2/UYVY + cvt=False` | YUV422 `Image` |
| `NV12/I420 + cvt=False` | YUV420 `Image` |

**说明**

- 超时或暂时没有新帧时，可能返回 `None`
- `NV12/I420` 在 `cvt=True` 时会抛出 `RuntimeError`

## `uvc_video_mode` 对象

### 字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `width` | `int` | 宽度 |
| `height` | `int` | 高度 |
| `fourcc` | `int` | 像素格式 |
| `fps` | `float` | 当前模式帧率 |

### 打印示例

```python
mode = UVC.video_mode(640, 480, UVC.FOURCC_MJPEG, 30)
print(mode)
```

输出示意：

```python
{"width":640, "height":480, "format":mjpeg, "fourcc":0x47504a4d, "fps":30.00}
```

注意：

- `format` 仅体现在打印字符串中
- 代码里真正用于判断格式的是 `mode.fourcc`

## 示例

### 示例 1：MJPEG 软解显示

对应工程示例：`src/canmv/resources/examples/02-Media/uvc.py`

```python
import time, gc

from media.display import *
from media.uvc import *

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

while True:
    plugin, dev = UVC.probe()
    if plugin:
        print(f"detect USB Camera {dev}")
        break

mode = UVC.video_mode(640, 480, UVC.FOURCC_MJPEG, 30)
succ, mode = UVC.select_video_mode(mode)
print(f"select mode success: {succ}, mode: {mode}")

UVC.start(cvt=False)
clock = time.clock()

try:
    while True:
        clock.tick()
        img = UVC.snapshot()
        if img is not None:
            img = img.to_rgb565()
            Display.show_image(img)
            img.__del__()
            gc.collect()
        print(f"fps: {clock.fps()}")
finally:
    UVC.stop()
    time.sleep_ms(100)
    Display.deinit()
```

### 示例 2：MJPEG 硬解后再做 CSC

对应工程示例：`src/canmv/resources/examples/02-Media/uvc_with_csc.py`

```python
import time, gc

from media.display import *
from media.uvc import *
from nonai2d import CSC

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

csc = CSC(CSC.PIXEL_FORMAT_RGB_565)
Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

while True:
    plugin, dev = UVC.probe()
    if plugin:
        print(f"detect USB Camera {dev}")
        break
    time.sleep_ms(100)

mode = UVC.video_mode(640, 480, UVC.FOURCC_MJPEG, 30)
succ, mode = UVC.select_video_mode(mode)
print(f"select mode success: {succ}, mode: {mode}")

UVC.start(cvt=True)
clock = time.clock()

try:
    while True:
        clock.tick()
        img = UVC.snapshot()
        if img is None:
            continue
        img = csc.convert(img)
        Display.show_image(img)
        img.__del__()
        gc.collect()
        print(f"fps: {clock.fps()}")
finally:
    UVC.stop()
    time.sleep_ms(100)
    csc.destroy()
    Display.deinit()
```

### 示例 3：YUY2 直接转换为 RGB565 显示

```python
import time, gc

from media.display import *
from media.uvc import *

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

while True:
    plugin, dev = UVC.probe()
    if plugin:
        print(f"detect USB Camera {dev}")
        break
    time.sleep_ms(100)

mode = UVC.video_mode(640, 480, UVC.FOURCC_YUY2, 30)
succ, mode = UVC.select_video_mode(mode)
print(f"select mode success: {succ}, mode: {mode}")

UVC.start(cvt=True)
clock = time.clock()

try:
    while True:
        clock.tick()
        img = UVC.snapshot()
        if img is None:
            continue
        Display.show_image(img)
        img.__del__()
        gc.collect()
        print(f"fps: {clock.fps()}")
finally:
    UVC.stop()
    time.sleep_ms(100)
    Display.deinit()
```

## 注意事项

1. `UVC.stop()` 建议始终放在 `finally` 中调用。
1. `UVC.start(cvt=True)` 只影响 `snapshot()` 返回内容，不改变 USB 侧实际协商到的 `fourcc`。
1. `NV12` / `I420` 当前不支持直接在 `snapshot(cvt=True)` 中转换。
1. 不建议通过 Hub 同时连接 UVC 摄像头和大量占用 USB 带宽的设备。
