# 3.13 UVC API Manual  

## 1. Overview  

The UVC module provides USB camera detection, configuration, and image capture functionality, supporting single-camera operation.  

## 2. API Reference  

### 2.1 UVC.probe - Detect Camera  

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
| plugin    | bool | Whether a camera is detected |  
| devname   | str  | Camera device information (Manufacturer#Product) |  

**Example**  

```python  
plugin, devinfo = UVC.probe()  
print(f"Camera detection: {'Connected' if plugin else 'Not connected'}, Device info: {devinfo}")  
```  

### 2.2 UVC.video_mode - Video Mode Operations  

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
| width     | int  | Resolution width (pixels) |  
| height    | int  | Resolution height (pixels) |  
| format    | int  | Image format (see constant definitions) |  
| fps       | int  | Frame rate (fps) |  

**Return Value**  
Returns a `uvc_video_mode` object.  

### 2.3 UVC.list_video_mode - List Supported Modes  

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

### 2.4 UVC.select_video_mode - Select Video Mode  

**Function**  
Sets the camera output mode.  

**Syntax**  

```python  
succ, actual_mode = UVC.select_video_mode(mode)  
```  

**Parameters**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| mode      | uvc_video_mode | Video mode to set |  

**Return Values**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| succ      | bool | Whether the setting was successful |  
| actual_mode | uvc_video_mode | The actual mode applied |  

### 2.5 UVC.start - Start Video Stream  

**Function**  
Starts the camera video stream output.  

**Syntax**  

```python  
success = UVC.start()  
```  

**Return Value**  
Returns a boolean indicating whether the stream started successfully.  

### 2.6 UVC.stop - Stop Video Stream  

**Function**  
Stops the video stream and releases resources.  

**Syntax**  

```python  
UVC.stop()  
```  

### 2.7 UVC.snapshot - Capture Frame  

**Function**  
Captures a single frame from the video stream.  

**Syntax**  

```python  
frame = UVC.snapshot()  
```  

**Return Value**  
Returns image data in YUV422 or JPEG format.  

## 3. Data Structures  

### uvc_video_mode Structure  

```python  
class uvc_video_mode:  
    width: int    # Resolution width  
    height: int   # Resolution height  
    format: int   # Image format  
    fps: int      # Frame rate (fps)  
```  

## 4. Constant Definitions  

| Constant | Value | Description |  
|----------|-------|-------------|  
| UVC.FORMAT_MJPEG | 1 | MJPG compressed format (recommended, low bandwidth) |  
| UVC.FORMAT_UNCOMPRESS | 2 | YUV422 uncompressed format (high bandwidth) |  

## 5. Recommended Workflow  

1. Detect camera (`probe()`)  
1. List supported modes (`list_video_mode()`)  
1. Select an appropriate mode (`select_video_mode()`)  
1. Start video stream (`start()`)  
1. Capture images (`snapshot()`)  
1. Stop video stream (`stop()`)  

## 6. Best Practices  

```python  
import time, os, urandom, sys  

from media.display import *  
from media.media import *  
from media.uvc import *  

DISPLAY_WIDTH = ALIGN_UP(800, 16)  
DISPLAY_HEIGHT = 480  

# Use LCD as display output  
Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)  
# Initialize media manager  
MediaManager.init()  

while True:  
    plugin, dev = UVC.probe()  
    if plugin:  
        print(f"Detected USB Camera {dev}")  
        break  

mode = UVC.video_mode(640, 480, UVC.FORMAT_MJPEG, 30)  

succ, mode = UVC.select_video_mode(mode)  
print(f"Select mode success: {succ}, mode: {mode}")  

UVC.start()  

while True:  
    img = UVC.snapshot()  
    if img is not None:  
        img = img.to_rgb565()  
        Display.show_image(img)  

# Deinitialize display  
Display.deinit()  
UVC.stop()  
time.sleep_ms(100)  
# Release media buffer  
MediaManager.deinit()  
```
