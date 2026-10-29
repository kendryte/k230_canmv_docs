# `UVC` Module API Manual

## Overview

The `UVC` module is used to access USB cameras in CanMV Python.

The module uses `FOURCC` to describe video formats. The supported host input formats are:

- `UVC.FOURCC_YUY2`
- `UVC.FOURCC_UYVY`
- `UVC.FOURCC_NV12`
- `UVC.FOURCC_I420`
- `UVC.FOURCC_MJPEG`

Only a single UVC camera is supported by default.

## Recommended Workflow

1. `UVC.probe()` to detect the camera
1. `UVC.list_video_mode()` to view the modes supported by the device
1. `UVC.video_mode(...)` to construct the target mode
1. `UVC.select_video_mode(...)` to select and negotiate the mode
1. `UVC.start(...)` to start the video stream
1. Loop calling `UVC.snapshot()` to get images
1. `UVC.stop()` to stop the video stream

It is recommended to call `UVC.stop()` inside a `try/finally` block to ensure proper stream shutdown even on abnormal exit.

## API Reference

### `UVC.probe()` - Detect Camera

**Function**

Detects whether a UVC camera is currently connected to the system, and returns the vendor/product string.

**Syntax**

```python
from media.uvc import UVC

plugin, devname = UVC.probe()
```

**Return Values**

| Return Value | Type | Description |
|---|---|---|
| `plugin` | `bool` | Whether a UVC camera is detected |
| `devname` | `str` / `None` | Device information, in the format `vendor#product` |

**Example**

```python
plugin, devinfo = UVC.probe()
print(f"detect: {plugin}, devinfo: {devinfo}")
```

### `UVC.video_mode()` - Get or Construct Video Mode

**Function**

- When called without arguments: returns the currently negotiated video mode
- When called with arguments: constructs a target video mode object

**Syntax**

```python
# Get current mode
mode = UVC.video_mode()

# Construct target mode
mode = UVC.video_mode(width, height, fourcc, fps)
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `width` | `int` | Image width |
| `height` | `int` | Image height |
| `fourcc` | `int` | Pixel format, uses `UVC.FOURCC_*` constants |
| `fps` | `int` | Target frame rate |

**Description**

- When `fourcc` is omitted, `UVC.FOURCC_MJPEG` is used by default
- When `fps` is omitted, `frameinterval = 0` is passed to the lower layer, allowing the driver to select the default frame rate
- After `UVC.select_video_mode()` succeeds, the returned mode object will be updated to the actual negotiated values

### `UVC.list_video_mode()` - List Device Supported Modes

**Function**

Enumerates the full list of modes supported by the camera. Each item in the list is a `uvc_video_mode` object containing width, height, `fourcc`, and `fps`.

**Syntax**

```python
modes = UVC.list_video_mode()
```

**Example**

```python
for i, mode in enumerate(UVC.list_video_mode()):
    print(f"{i}: {mode}")
```

### `UVC.select_video_mode(mode)` - Select Video Mode

**Function**

Initializes the UVC device according to the user-specified target mode, and returns the actual negotiated mode.

**Syntax**

```python
succ, actual_mode = UVC.select_video_mode(mode)
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `mode` | `uvc_video_mode` | Target mode |

**Return Values**

| Return Value | Type | Description |
|---|---|---|
| `succ` | `bool` | Whether initialization succeeded |
| `actual_mode` | `uvc_video_mode` | The actual negotiated mode |

**Common `FOURCC`**

The `mode.fourcc` passed into `UVC.select_video_mode()` typically uses the following constants:

| Constant | Description |
|---|---|
| `UVC.FOURCC_YUY2` | YUY2 / YUYV 4:2:2 |
| `UVC.FOURCC_UYVY` | UYVY 4:2:2 |
| `UVC.FOURCC_NV12` | NV12 4:2:0 |
| `UVC.FOURCC_I420` | I420 4:2:0 |
| `UVC.FOURCC_MJPEG` | MJPEG compressed format |

### `UVC.start()` - Start Video Stream

**Function**

Starts the UVC video stream and configures the return type of `snapshot()`.

**Syntax**

```python
success = UVC.start(delay_ms=0, cvt=True)
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `delay_ms` | `int` | Additional wait time in milliseconds after starting |
| `cvt` | `bool` | Whether to perform format conversion on `snapshot()` returned data |

**`cvt` Semantics**

| Input Format | `cvt=True` | `cvt=False` |
|---|---|---|
| `FOURCC_MJPEG` | `snapshot()` returns NV12 frame (internally uses hardware JPEG decoding) | Returns JPEG image |
| `FOURCC_YUY2` | Returns RGB565 image | Returns YUV422 image |
| `FOURCC_UYVY` | Returns RGB565 image | Returns YUV422 image |
| `FOURCC_NV12` | Not supported, will raise exception in `snapshot()` | Returns YUV420 image |
| `FOURCC_I420` | Not supported, will raise exception in `snapshot()` | Returns YUV420 image |

### `UVC.stop()` - Stop Video Stream

**Function**

Stops the UVC video stream and releases internal state.

**Syntax**

```python
UVC.stop()
```

### `UVC.snapshot()` - Get One Frame Image

**Function**

Takes one frame image from the current video stream.

**Syntax**

```python
frame = UVC.snapshot()
frame = UVC.snapshot(timeout_ms)
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `timeout_ms` | `int` | Timeout for getting one frame, in milliseconds |

**Return Value**

The return type depends on the current `fourcc` and `UVC.start(cvt=...)` configuration:

| Current Mode | Returned Object |
|---|---|
| `MJPEG + cvt=True` | NV12 video frame object |
| `MJPEG + cvt=False` | JPEG `Image` |
| `YUY2/UYVY + cvt=True` | RGB565 `Image` |
| `YUY2/UYVY + cvt=False` | YUV422 `Image` |
| `NV12/I420 + cvt=False` | YUV420 `Image` |

**Description**

- May return `None` on timeout or when no new frame is temporarily available
- `NV12/I420` will raise a `RuntimeError` when `cvt=True`

## `uvc_video_mode` Object

### Fields

| Field | Type | Description |
|---|---|---|
| `width` | `int` | Width |
| `height` | `int` | Height |
| `fourcc` | `int` | Pixel format |
| `fps` | `float` | Current mode frame rate |

### Print Example

```python
mode = UVC.video_mode(640, 480, UVC.FOURCC_MJPEG, 30)
print(mode)
```

Output example:

```python
{"width":640, "height":480, "format":mjpeg, "fourcc":0x47504a4d, "fps":30.00}
```

Note:

- `format` is only reflected in the print string
- The field actually used in code to determine the format is `mode.fourcc`

## Example

### Example 1: MJPEG Software Decoding Display

Corresponding routine:

- Development board firmware path: `/sdcard/examples/02-Media/uvc.py`
- SDK source code path: `src/canmv/resources/examples/02-Media/uvc.py`

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

### Example 2: MJPEG Hardware Decoding Followed by CSC

Corresponding routine:

- Development board firmware path: `/sdcard/examples/02-Media/uvc_with_csc.py`
- SDK source code path: `src/canmv/resources/examples/02-Media/uvc_with_csc.py`

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

### Example 3: YUY2 Directly Converted to RGB565 for Display

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

## Notes

1. `UVC.stop()` is recommended to always be called in `finally`.
1. `UVC.start(cvt=True)` only affects the content returned by `snapshot()`; it does not change the `fourcc` actually negotiated on the USB side.
1. `NV12` / `I420` currently do not support direct conversion in `snapshot(cvt=True)`.
1. It is not recommended to connect UVC cameras and devices that heavily occupy USB bandwidth through a Hub at the same time.
