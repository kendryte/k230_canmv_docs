# `MJPEGEncoder` 模块 API 手册

## 概述

`MJPEGEncoder` 使用 K230 的 VENC 硬件编码器，将一帧 `image.Image`、`py_video_frame` 或 `py_video_frame_info` 编码为 JPEG 字节数据。该接口适用于抓拍保存、HTTP MJPEG 视频流以及需要逐帧 JPEG 数据的应用。

推荐通过以下方式导入：

```python
from media.mjpeg import MJPEGEncoder
```

编码器在第一次调用 `encode()` 时申请 VENC 通道和 VB 缓冲区，并在输入尺寸或像素格式改变时自动重新配置。使用结束后应调用 `close()` 释放硬件资源。

## 快速开始

下面的例程直接编码 Sensor 输出的视频帧，避免额外的图像复制：

```python
from media.mjpeg import MJPEGEncoder
from media.sensor import Sensor

sensor = Sensor()
encoder = None

try:
    sensor.reset()
    sensor.set_framesize(width=1920, height=1080, alignment=12)
    sensor.set_pixformat(Sensor.YUV420SP)
    sensor.run()

    encoder = MJPEGEncoder(quality=50)
    frame = sensor.snapshot(dump_frame=True)
    jpeg = encoder.encode(frame, timeout_ms=1000)

    with open("/sdcard/snapshot.jpg", "wb") as file:
        file.write(jpeg)
finally:
    if encoder is not None:
        encoder.close()
    sensor.stop()
```

`alignment=12` 表示 Sensor 将各个图像平面按 $2^{12}=4096$ 字节对齐。VENC 输入平面的物理地址必须满足该要求，尤其是在 1920×1080 等图像平面大小不是 4096 整数倍的分辨率下。

## API 参考

### `MJPEGEncoder()`

创建一个 MJPEG 编码器对象。构造时不立即占用 VENC 通道，硬件资源在第一次编码时按需创建。

```python
encoder = MJPEGEncoder(quality=90)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `quality` | `int` | `90` | JPEG 编码质量，取值范围为 1～99；值越大，画质和输出数据量通常越高 |

当 `quality` 超出有效范围时抛出 `ValueError`。

### `MJPEGEncoder.encode()`

将一帧图像编码为完整的 JPEG 文件数据。

```python
jpeg = encoder.encode(input, timeout_ms=1000)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `input` | `image.Image`、`py_video_frame` 或 `py_video_frame_info` | 无 | 待编码的图像或视频帧 |
| `timeout_ms` | `int` | `1000` | VENC 发送帧和获取码流的超时时间，单位为毫秒；`-1` 表示阻塞等待 |

**返回值**

返回 `bytes` 对象，内容为单张完整 JPEG 图像，可直接写入 `.jpg` 文件、通过 socket 发送或嵌入 HTTP MJPEG multipart 数据流。

#### 支持的 `image.Image` 格式

| 图像格式 | 编码前处理 |
|---|---|
| `BINARY`、`GRAYSCALE`、`RGB565` | 转换为 RGB888 平面格式 |
| `RGB888`、`BGR888`、`RGBP888`、`BGRP888` | 转换或整理为 RGB888 平面格式 |
| `ARGB8888`、`ABGR8888`、`RGBA8888`、`BGRA8888` | 按 VENC 支持的 32 位像素顺序整理 |
| `YUV422`、`YVU422` | 整理为 YUYV 4:2:2 打包格式 |
| `YUV420`、`YVU420` | 整理为 4:2:0 半平面格式 |

`image.Image` 输入会复制到编码器内部的页对齐 VB 缓冲区。该方式通用，但在高分辨率连续编码时会产生额外的内存带宽开销。

下面的例程编码一张 `image.Image`：

```python
import image

from media.mjpeg import MJPEGEncoder

img = image.Image("/sdcard/input.bmp")
encoder = MJPEGEncoder(quality=85)

try:
    jpeg = encoder.encode(img)
    with open("/sdcard/output.jpg", "wb") as file:
        file.write(jpeg)
finally:
    encoder.close()
```

#### 支持的视频帧格式

视频帧输入支持以下 `k_pixel_format`：

- `PIXEL_FORMAT_ARGB_8888`
- `PIXEL_FORMAT_ABGR_8888`
- `PIXEL_FORMAT_BGRA_8888`
- `PIXEL_FORMAT_BGR_888_PLANAR`
- `PIXEL_FORMAT_RGB_888_PLANAR`
- `PIXEL_FORMAT_YUV_SEMIPLANAR_420`
- `PIXEL_FORMAT_YVU_PLANAR_420`
- `PIXEL_FORMAT_YVU_SEMIPLANAR_420`
- `PIXEL_FORMAT_UYVY_PACKAGE_422`
- `PIXEL_FORMAT_YUYV_PACKAGE_422`

视频帧必须来自 VB 缓冲池，并且每个有效平面的物理地址必须按 4096 字节对齐。对于 Sensor 输出，应使用：

```python
sensor.set_framesize(width=width, height=height, alignment=12)
frame = sensor.snapshot(dump_frame=True)
```

编码必须在该帧被 Sensor 回收前完成。通常应在获取下一帧之前立即调用 `encoder.encode(frame)`。

### `MJPEGEncoder.close()`

停止并销毁 VENC 通道，同时释放编码器创建的 VB 缓冲池。

```python
encoder.close()
```

该方法可以重复调用。关闭后不能再次使用该对象执行编码。

### `MJPEGEncoder.is_closed()`

返回编码器是否已经关闭。

```python
closed = encoder.is_closed()
```

返回类型为 `bool`。

## 只读属性

| 属性 | 类型 | 说明 |
|---|---|---|
| `quality` | `int` | 构造编码器时设置的 JPEG 质量 |
| `width` | `int` | 当前 VENC 通道的图像宽度；首次编码前为 0 |
| `height` | `int` | 当前 VENC 通道的图像高度；首次编码前为 0 |
| `chn` | `int` | 自动申请的 VENC 通道号；未初始化或关闭后为 -1 |

## 性能建议

- 对 Sensor 连续采集、高分辨率或高帧率场景，优先使用 `snapshot(dump_frame=True)` 返回的视频帧，避免 `image.Image` 输入的整帧复制。
- 1920×1080 等多平面格式应配置 `alignment=12`，否则编码器会拒绝未按 4096 字节对齐的物理地址。
- `quality` 会影响 JPEG 大小和网络带宽。网页视频流可从 `quality=50` 开始调整。
- `timeout_ms` 只控制 VENC 操作，不控制后续文件写入或网络发送时间。
- 一个 `MJPEGEncoder` 对象同一时刻只应编码一帧。对象内部会串行化并发调用。

## 异常

| 异常 | 常见原因 |
|---|---|
| `ValueError` | 质量或超时参数无效、输入格式不支持、图像尺寸无效、视频帧不是 VB 缓冲区或平面地址未对齐 |
| `MemoryError` | 无法为 JPEG 返回数据分配内存 |
| `RuntimeError` | VENC 通道、VB 缓冲池、发送帧或获取码流失败 |

发生 VENC 运行错误后，编码器会清理当前硬件资源。下一次调用 `encode()` 时会重新申请硬件资源；应用也可以调用 `close()` 结束任务。
