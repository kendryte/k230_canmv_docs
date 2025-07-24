# `UVC` API Manual

## Overview  

The UVC module provides USB camera detection, configuration, and image capture functionality, supporting single-camera operation.

## API Reference  

### UVC.probe - Detect Camera  

**Function**  
Checks whether a USB camera is connected to the system (currently supports single-camera detection only).  

**Syntax**  

```python  
from media.uvc import UVC  
plugin, devname = UVC.probe()  
```  

**Return Values**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| plugin    | bool | True if camera is detected, False otherwise |  
| devname   | str  | Camera device information in "Manufacturer#Product" format |  

**Example**  

```python  
plugin, devinfo = UVC.probe()  
print(f"Camera detection: {'Connected' if plugin else 'Not connected'}, Device info: {devinfo}")  
```  

### UVC.video_mode - Video Mode Operations  

**Function**  
Constructs or retrieves the current video mode configuration.  

**Syntax**  

```python  
# Get current mode  
mode = UVC.video_mode()  

# Create new configuration  
mode = UVC.video_mode(width, height, format, fps)  
```  

**Parameters**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| width     | int  | Resolution width in pixels |  
| height    | int  | Resolution height in pixels |  
| format    | int  | Image format (see constant definitions) |  
| fps       | int  | Frame rate in fps |  

**Return Value**  
Returns a `uvc_video_mode` object.  

### UVC.list_video_mode - List Supported Modes  

**Function**  
Retrieves all video modes supported by the camera.  

**Syntax**  

```python  
modes = UVC.list_video_mode()  
```  

**Return Value**  
Returns a list of supported `uvc_video_mode` objects.  

**Example**  

```python  
for i, mode in enumerate(UVC.list_video_mode()):  
    print(f"Mode {i}: {mode.width}x{mode.height} {mode.format}@{mode.fps}fps")  
```  

### UVC.select_video_mode - Select Video Mode  

**Function**  
Sets the camera output mode.  

**Syntax**  

```python  
succ, actual_mode = UVC.select_video_mode(mode)  
```  

**Parameters**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| mode      | uvc_video_mode | Video mode configuration to set |  

**Return Values**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| succ      | bool | True if setting was successful |  
| actual_mode | uvc_video_mode | The actual mode that was applied |  

### UVC.start - Start Video Stream  

**Function**  
Starts the camera video stream output.  

**Syntax**  

```python  
success = UVC.start(delay_ms=0, cvt=True)  
```  

**Parameters**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| delay_ms  | int  | Delay in milliseconds to wait for UVC camera data output (default: 0) |  
| cvt       | bool | Whether to hardware-decode snapshot images to NV12 format (default: True) |  

**Return Value**  
Returns True if the stream started successfully.  

### UVC.stop - Stop Video Stream  

**Function**  
Stops the video stream and releases resources.  

**Syntax**  

```python  
UVC.stop()  
```  

### UVC.snapshot - Capture Frame  

**Function**  
Captures a single frame from the video stream.  

**Syntax**  

```python  
frame = UVC.snapshot(timeout_ms=1000)  
```  

**Parameters**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| timeout_ms | int  | Timeout in milliseconds for frame capture (default: 1000) |  

**Return Value**  
Returns image data in NV12 Frame format (if hardware decoding enabled) or JPEG/YUV422 format.  

## Data Structures  

### uvc_video_mode Structure  

```python  
class uvc_video_mode:  
    width: int    # Resolution width in pixels  
    height: int   # Resolution height in pixels  
    format: int   # Image format (see constants)  
    fps: int      # Frame rate in fps  
```  

## Constant Definitions  

| Constant | Value | Description |  
|----------|-------|-------------|  
| UVC.FORMAT_MJPEG | 1 | MJPG compressed format (recommended for low bandwidth) |  
| UVC.FORMAT_UNCOMPRESS | 2 | YUV422 uncompressed format (requires higher bandwidth) |  

## Recommended Workflow  

1. Detect camera (`probe()`)  
1. List supported modes (`list_video_mode()`)  
1. Select an appropriate mode (`select_video_mode()`)  
1. Start video stream (`start()`)  
1. Capture images (`snapshot()`)  
1. Stop video stream (`stop()`)  

## Best Practices  

### Software Decoding Example  

```python  
import time, os, urandom, sys, gc

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

UVC.start(cvt = False)

fps = time.clock()

while True:
    fps.tick()
    img = UVC.snapshot()
    if img is not None:
        try:
            img = img.to_rgb565()
            Display.show_image(img)
            img.__del__()
            gc.collect()
        except OSError as e:
            pass

    print(f"fps: {fps.fps()}")

# deinit display
Display.deinit()
UVC.stop()
time.sleep_ms(100)
# release media buffer
MediaManager.deinit()
```  

### Hardware Decoding Example  

```python  
import time, os, urandom, sys, gc

from media.display import *
from media.media import *
from media.uvc import *

from nonai2d import CSC

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

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

    img = None
    while img is None:
        try:
            img = UVC.snapshot()
        except:
            print("drop frame")
            continue

    img = csc.convert(img)
    Display.show_image(img)
    img.__del__()
    gc.collect()

    print(f"fps: {clock.fps()}")

# deinit display
Display.deinit()
csc.destroy()
UVC.stop()
time.sleep_ms(100)
# release media buffer
MediaManager.deinit()
```  
