# `MJPEGEncoder` Module API Manual

## Overview

`MJPEGEncoder` uses the K230 VENC hardware encoder to encode a frame of `image.Image`, `py_video_frame`, or `py_video_frame_info` into JPEG byte data. This interface is suitable for snapshot saving, HTTP MJPEG video streaming, and applications that require per-frame JPEG data.

The recommended way to import is:

```python
from media.mjpeg import MJPEGEncoder
```

The encoder allocates VENC channels and VB buffers on the first call to `encode()`, and automatically reconfigures when the input size or pixel format changes. Call `close()` after use to release hardware resources.

## Quick Start

The following example directly encodes video frames output by the Sensor, avoiding extra image copying:

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

`alignment=12` means the Sensor aligns each image plane to $2^{12}=4096$ bytes. The physical address of the VENC input plane must satisfy this requirement, especially at resolutions such as 1920×1080 where the image plane size is not a multiple of 4096.

## API Reference

### `MJPEGEncoder()`

Creates an MJPEG encoder object. The VENC channel is not occupied during construction; hardware resources are created on demand during the first encoding.

```python
encoder = MJPEGEncoder(quality=90)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `quality` | `int` | `90` | JPEG encoding quality, ranging from 1 to 99; larger values typically produce higher image quality and larger output data size |

A `ValueError` is raised when `quality` is outside the valid range.

### `MJPEGEncoder.encode()`

Encodes a frame of image into complete JPEG file data.

```python
jpeg = encoder.encode(input, timeout_ms=1000)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `input` | `image.Image`, `py_video_frame`, or `py_video_frame_info` | None | The image or video frame to be encoded |
| `timeout_ms` | `int` | `1000` | Timeout for VENC sending frame and retrieving encoded stream, in milliseconds; `-1` means blocking wait |

**Return Value**

Returns a `bytes` object containing a single complete JPEG image, which can be directly written to a `.jpg` file, sent via socket, or embedded into an HTTP MJPEG multipart data stream.

#### Supported `image.Image` Formats

| Image Format | Pre-encoding Processing |
|---|---|
| `BINARY`, `GRAYSCALE`, `RGB565` | Convert to RGB888 planar format |
| `RGB888`, `BGR888`, `RGBP888`, `BGRP888` | Convert or arrange to RGB888 planar format |
| `ARGB8888`, `ABGR8888`, `RGBA8888`, `BGRA8888` | Arrange in the 32-bit pixel order supported by VENC |
| `YUV422`, `YVU422` | Arrange to YUYV 4:2:2 packed format |
| `YUV420`, `YVU420` | Arrange to 4:2:0 semi-planar format |

The `image.Image` input is copied to the encoder's internal page-aligned VB buffer. This approach is universal, but introduces additional memory bandwidth overhead during continuous encoding at high resolutions.

The following example encodes an `image.Image`:

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

#### Supported Video Frame Formats

Video frame input supports the following `k_pixel_format`:

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

Video frames must come from the VB buffer pool, and the physical address of each valid plane must be aligned to 4096 bytes. For Sensor output, use:

```python
sensor.set_framesize(width=width, height=height, alignment=12)
frame = sensor.snapshot(dump_frame=True)
```

Encoding must complete before the frame is recycled by the Sensor. Typically, `encoder.encode(frame)` should be called immediately before obtaining the next frame.

### `MJPEGEncoder.close()`

Stops and destroys the VENC channel, and releases the VB buffer pool created by the encoder.

```python
encoder.close()
```

This method can be called repeatedly. After being closed, the object cannot be used again to perform encoding.

### `MJPEGEncoder.is_closed()`

Returns whether the encoder has been closed.

```python
closed = encoder.is_closed()
```

The return type is `bool`.

## Read-only Properties

| Property | Type | Description |
|---|---|---|
| `quality` | `int` | JPEG quality set when the encoder was constructed |
| `width` | `int` | Image width of the current VENC channel; 0 before the first encoding |
| `height` | `int` | Image height of the current VENC channel; 0 before the first encoding |
| `chn` | `int` | Automatically allocated VENC channel number; -1 when not initialized or after closing |

## Performance Recommendations

- For continuous Sensor capture, high-resolution, or high-frame-rate scenarios, prefer using the video frame returned by `snapshot(dump_frame=True)` to avoid full-frame copying from `image.Image` input.
- For multi-plane formats like 1920×1080, configure `alignment=12`; otherwise the encoder will reject physical addresses that are not aligned to 4096 bytes.
- `quality` affects JPEG size and network bandwidth. For web video streaming, start adjusting from `quality=50`.
- `timeout_ms` only controls VENC operations, not subsequent file writing or network sending time.
- A `MJPEGEncoder` object should only encode one frame at a time. The object serializes concurrent calls internally.

## Exceptions

| Exception | Common Cause |
|---|---|
| `ValueError` | Invalid quality or timeout parameters, unsupported input format, invalid image dimensions, video frame is not a VB buffer, or unaligned plane address |
| `MemoryError` | Unable to allocate memory for JPEG return data |
| `RuntimeError` | VENC channel, VB buffer pool, sending frame, or obtaining stream failure |

After a VENC runtime error occurs, the encoder will clean up the current hardware resources. The next call to `encode()` will re-allocate hardware resources; the application can also call `close()` to end the task.
