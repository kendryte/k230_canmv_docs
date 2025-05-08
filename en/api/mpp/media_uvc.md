# 3.13 `UVC` API Manual

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
| plugin    | bool | True if camera is detected, False otherwise |  
| devname   | str  | Camera device information in "Manufacturer#Product" format |  

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
| width     | int  | Resolution width in pixels |  
| height    | int  | Resolution height in pixels |  
| format    | int  | Image format (see constant definitions) |  
| fps       | int  | Frame rate in fps |  

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
| mode      | uvc_video_mode | Video mode configuration to set |  

**Return Values**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| succ      | bool | True if setting was successful |  
| actual_mode | uvc_video_mode | The actual mode that was applied |  

### 2.5 UVC.start - Start Video Stream  

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
frame = UVC.snapshot(timeout_ms=1000)  
```  

**Parameters**  

| Parameter | Type | Description |  
|-----------|------|-------------|  
| timeout_ms | int  | Timeout in milliseconds for frame capture (default: 1000) |  

**Return Value**  
Returns image data in NV12 Frame format (if hardware decoding enabled) or JPEG/YUV422 format.  

## 3. Data Structures  

### uvc_video_mode Structure  

```python  
class uvc_video_mode:  
    width: int    # Resolution width in pixels  
    height: int   # Resolution height in pixels  
    format: int   # Image format (see constants)  
    fps: int      # Frame rate in fps  
```  

## 4. Constant Definitions  

| Constant | Value | Description |  
|----------|-------|-------------|  
| UVC.FORMAT_MJPEG | 1 | MJPG compressed format (recommended for low bandwidth) |  
| UVC.FORMAT_UNCOMPRESS | 2 | YUV422 uncompressed format (requires higher bandwidth) |  

## 5. Recommended Workflow  

1. Detect camera (`probe()`)  
1. List supported modes (`list_video_mode()`)  
1. Select an appropriate mode (`select_video_mode()`)  
1. Start video stream (`start()`)  
1. Capture images (`snapshot()`)  
1. Stop video stream (`stop()`)  

## 6. Best Practices  

### 6.1 Software Decoding Example  

```python  
import time  
from media.display import *  
from media.media import *  
from media.uvc import *  

DISPLAY_WIDTH = ALIGN_UP(800, 16)  
DISPLAY_HEIGHT = 480  

# Initialize LCD display  
Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)  
# Initialize media manager  
MediaManager.init()  

# Detect camera  
while True:  
    plugin, dev = UVC.probe()  
    if plugin:  
        print(f"Detected USB Camera: {dev}")  
        break  

# Set video mode  
mode = UVC.video_mode(640, 480, UVC.FORMAT_MJPEG, 30)  
succ, mode = UVC.select_video_mode(mode)  
print(f"Mode selection: {'Success' if succ else 'Failed'}, Actual mode: {mode}")  

# Start video stream  
UVC.start()  

try:  
    while True:  
        img = UVC.snapshot()  
        if img is not None:  
            img = img.to_rgb565()  # Convert to RGB565 format  
            Display.show_image(img)  # Display image  
finally:  
    # Cleanup resources  
    Display.deinit()  
    UVC.stop()  
    time.sleep_ms(100)  
    MediaManager.deinit()  
```  

### 6.2 Hardware Decoding Example  

```python  
import time  
from media.display import *  
from media.media import *  
from media.uvc import *  
from nonai2d import CSC  # Hardware Color Space Converter  

DISPLAY_WIDTH = ALIGN_UP(800, 16)  
DISPLAY_HEIGHT = 480  

# Initialize hardware color space converter  
csc = CSC(0, CSC.PIXEL_FORMAT_RGB_565)  

# Initialize LCD display  
Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)  
# Initialize media manager  
MediaManager.init()  

# Detect camera  
while True:  
    plugin, dev = UVC.probe()  
    if plugin:  
        print(f"Detected USB Camera: {dev}")  
        break  
    time.sleep_ms(100)  

# Set video mode  
mode = UVC.video_mode(640, 480, UVC.FORMAT_MJPEG, 30)  
succ, mode = UVC.select_video_mode(mode)  
print(f"Mode selection: {'Success' if succ else 'Failed'}, Actual mode: {mode}")  

# Start video stream with hardware decoding  
UVC.start(cvt=True)  

clock = time.clock()  # For FPS calculation  

try:  
    while True:  
        clock.tick()  
        
        img = UVC.snapshot()  
        if img is not None:  
            img = csc.convert(img)  # Hardware color space conversion  
            Display.show_image(img)  
        
        print(f"Current FPS: {clock.fps()}")  
finally:  
    # Cleanup resources  
    Display.deinit()  
    csc.destroy()  
    UVC.stop()  
    time.sleep_ms(100)  
    MediaManager.deinit()  
```  
