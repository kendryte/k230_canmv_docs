# 3.1 `Sensor` Module API Manual

```{attention}
This module has undergone significant changes since firmware version V0.7. If you are using firmware prior to V0.7, please refer to the old version of the documentation.
```

## 1. Overview

The `sensor` module on the CanMV K230 platform is responsible for image acquisition and data processing. This module provides a set of advanced APIs, allowing developers to easily obtain images in different formats and sizes without needing to understand the specifics of the underlying hardware implementation. The architecture is shown in the diagram below:

![camera-block-diagram](../../../zh/api/images/k230-canmv-camera-top.png)

In the diagram, sensor 0, sensor 1, and sensor 2 represent three image input sensor devices; Camera Device 0, Camera Device 1, and Camera Device 2 correspond to the respective image processing units; output channel 0, output channel 1, and output channel 2 indicate that each image processing unit supports up to three output channels. Through software configuration, different sensor devices can be flexibly mapped to the corresponding image processing units.

The `sensor` module of the CanMV K230 supports simultaneous access of up to three image sensors, each of which can independently complete image data acquisition, capture, and processing. Additionally, each video channel can output three image data streams in parallel for further processing by backend modules. In practical applications, the number of supported sensors, input resolution, and the number of output channels are limited by the hardware configuration and memory size of the development board, so a comprehensive evaluation based on project requirements is necessary.

## 2. API Introduction

### Constructor

**Description**

Construct a `Sensor` object using `csi id` and image sensor type.

In image processing applications, users typically need to first create a `Sensor` object. The CanMV K230 software can automatically detect built-in image sensors without users needing to specify the exact model; they only need to set the sensor's maximum output resolution and frame rate. For information on supported image sensors, please refer to the [Image Sensor Support List](#4-image-sensor-support-list). If the set resolution or frame rate does not match the current sensor's default configuration, the system will automatically adjust to the optimal configuration, and the final configuration can be viewed in the log, e.g., `use sensor 23, output 640x480@90`.

**Syntax**

```python
sensor = Sensor(id, [width, height, fps])
```

**Parameters**

| Parameter Name | Description | Input/Output | Notes |
|----------------|-------------|--------------|-------|
| id             | `csi` port, supports `0-2`, refer to hardware schematic for specific ports | Input | Optional, default values vary for different development boards |
| width          | Maximum output image width of the `sensor` | Input | Optional, default `1920` |
| height         | Maximum output image height of the `sensor` | Input | Optional, default `1080` |
| fps            | Maximum output frame rate of the `sensor` | Input | Optional, default `30` |

**Return Value**

| Return Value  | Description |
|---------------|-------------|
| Sensor Object | Sensor object |

**Examples**

```python
sensor = Sensor(id=0)
sensor = Sensor(id=0, width=1280, height=720, fps=60)
sensor = Sensor(id=0, width=640, height=480)
```

### 2.1 sensor.reset

**Description**

Reset the `sensor` object. After constructing the `Sensor` object, this function must be called to continue with other operations.

**Syntax**

```python
sensor.reset()
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| None           |             |              |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Examples**

```python
# Initialize sensor device 0 and sensor OV5647
sensor.reset()
```

### 2.2 sensor.set_framesize

**Description**

Set the output image size for the specified channel. Users can configure the output image size through the `framesize` parameter or by directly specifying `width` and `height`. **Width will automatically align to 16 pixels wide**.

**Syntax**

```python
sensor.set_framesize(framesize=FRAME_SIZE_INVALID, chn=CAM_CHN_ID_0, alignment=0, **kwargs)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| framesize      | Output image size of the sensor | Input |
| chn            | Sensor output channel number | Input |
| width          | Output image width, *kw_arg* | Input |
| height         | Output image height, *kw_arg* | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Notes**

- The output image size must not exceed the actual output capability of the image sensor.
- The maximum output image size of each channel is limited by hardware.

**Examples**

```python
# Configure sensor device 0, output channel 0, output image size 640x480
sensor.set_framesize(chn=CAM_CHN_ID_0, width=640, height=480)

# Configure sensor device 0, output channel 1, output image size 320x240
sensor.set_framesize(chn=CAM_CHN_ID_1, width=320, height=240)
```

### 2.3 sensor.set_pixformat

**Description**

Configure the image format output by the image sensor for the specified channel.

**Syntax**

```python
sensor.set_pixformat(pix_format, chn=CAM_CHN_ID_0)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| pix_format     | Output image format | Input |
| chn            | Sensor output channel number | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Examples**

```python
# Configure sensor device 0, output channel 0, output format NV12
sensor.set_pixformat(sensor.YUV420SP, chn=CAM_CHN_ID_0)

# Configure sensor device 0, output channel 1, output format RGB888
sensor.set_pixformat(sensor.RGB888, chn=CAM_CHN_ID_1)
```

### 2.4 sensor.set_hmirror

**Description**

Configure whether the image sensor performs horizontal mirroring.

**Syntax**

```python
sensor.set_hmirror(enable)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| enable         | `True` to enable horizontal mirroring<br>`False` to disable horizontal mirroring | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Examples**

```python
sensor.set_hmirror(True)
```

### 2.5 sensor.set_vflip

**Description**

Configure whether the image sensor performs vertical flipping.

**Syntax**

```python
sensor.set_vflip(enable)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| enable         | `True` to enable vertical flipping<br>`False` to disable vertical flipping | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Examples**

```python
sensor.set_vflip(True)
```

### 2.6 sensor.run

**Description**

Start the output of the image sensor. **This must be done after calling `MediaManager.init()`**.

**Syntax**

```python
sensor.run()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Notes**

- When using multiple sensors simultaneously (up to 3), only one of them needs to execute `run`.

**Examples**

```python
# Start the sensor device output data stream
sensor.run()
```

### 2.7 sensor.stop

**Description**

Stop the output of the image sensor. **This must be done before calling `MediaManager.deinit()`**.

**Syntax**

```python
sensor.stop()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Notes**

- If multiple image sensors are used simultaneously (up to 3), **each sensor must call `stop` individually**.

**Examples**

```python
# Stop the data stream output of sensor device 0
sensor.stop()
```

### 2.8 sensor.snapshot

**Description**

Capture a frame of image data from the specified output channel.

**Syntax**

```python
sensor.snapshot(chn=CAM_CHN_ID_0, timeout = 1000, dump_frame = False)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| chn            | Sensor output channel number | Input |
| timeout        | Sensor dump one frame timeout, Default 1000 ms | Input |
| dump_frame     | If set True return py_video_frame_info else return Image | Input |

**Return Value**

| Return Value  | Description          |
|---------------|----------------------|
| image object or py_video_frame_info object | Captured image data  |
| other         | Capture failed       |

**Examples**

```python
# Capture a frame of image data from channel 0 of sensor device 0
sensor.snapshot()
```

### 2.9 sensor.bind_info

**Description**

Get the binding information of the sensor channel for integration with other modules (e.g., display module).

**Syntax**

```python
sensor.bind_info(x=0, y=0, chn=CAM_CHN_ID_0)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| x              | Horizontal start coordinate of the binding area | Input |
| y              | Vertical start coordinate of the binding area | Input |
| chn            | Sensor output channel number | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| dict         | Contains source information, region size, and pixel format of the channel |

**Examples**

```python
# Get binding information of channel 0
info = sensor.bind_info(chn=CAM_CHN_ID_0)
print(info)  # Output: {'src': (0, 0, 0), 'rect': (0, 0, 640, 480), 'pix_format': 2}
```

### 2.10 sensor.get_hmirror

**Description**

Get the current status of horizontal mirroring.

**Syntax**

```python
sensor.get_hmirror()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| bool         | `True` if enabled, `False` otherwise |

**Examples**

```python
hmirror_enabled = sensor.get_hmirror()
print("Horizontal mirror enabled:", hmirror_enabled)
```

### 2.11 sensor.get_vflip

**Description**

Get the current status of vertical flipping.

**Syntax**

```python
sensor.get_vflip()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| bool         | `True` if enabled, `False` otherwise |

**Examples**

```python
vflip_enabled = sensor.get_vflip()
print("Vertical flip enabled:", vflip_enabled)
```

### 2.12 sensor.width

**Description**

Get the current output image width of the specified channel.

**Syntax**

```python
sensor.width(chn=CAM_CHN_ID_0)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| chn            | Sensor output channel number | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| int          | Image width in pixels |

**Examples**

```python
current_width = sensor.width(chn=CAM_CHN_ID_0)
print("Current width:", current_width)
```

### 2.13 sensor.height

**Description**

Get the current output image height of the specified channel.

**Syntax**

```python
sensor.height(chn=CAM_CHN_ID_0)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| chn            | Sensor output channel number | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| int          | Image height in pixels |

**Examples**

```python
current_height = sensor.height(chn=CAM_CHN_ID_0)
print("Current height:", current_height)
```

### 2.14 sensor.get_pixformat

**Description**

Get the current pixel format of the specified channel.

**Syntax**

```python
sensor.get_pixformat(chn=CAM_CHN_ID_0)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| chn            | Sensor output channel number | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| int          | Pixel format enum value (e.g., `sensor.RGB888`) |

**Examples**

```python
current_format = sensor.get_pixformat(chn=CAM_CHN_ID_0)
print("Current pixel format:", current_format)
```

### 2.15 sensor.get_type

**Description**

Get the type identifier of the current sensor.

**Syntax**

```python
sensor.get_type()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| int          | Sensor type enum value |

**Examples**

```python
sensor_type = sensor.get_type()
print("Sensor type:", sensor_type)
```

### 2.16 sensor.again

**Description**

Get or set the analog gain value of the sensor (unit: dB).

**Syntax**

```python
# Get gain
gain = sensor.again()

# Set gain
sensor.again(desired_gain)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| desired_gain   | Target gain value (for setting) | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| k_sensor_gain | Current gain object (when getting) |
| int          | Operation result (when setting) |

**Notes**

- Only supported by specific sensors (e.g., `sc132gs`).
- Ensure the sensor is initialized and running before setting gain.

**Examples**

```python
# Get current gain
current_gain = sensor.again()
print("Current gain:", current_gain)

# Set gain to 10 dB
result = sensor.again(10)
if result == 0:
    print("Gain set successfully")
```

## 3. Data Structure Description

### 3.1 frame_size

| Image Frame Size | Resolution    |
|------------------|---------------|
| QQCIF            | 88x72         |
| QCIF             | 176x144       |
| CIF              | 352x288       |
| QSIF             | 176x120       |
| SIF              | 352x240       |
| QQVGA            | 160x120       |
| QVGA             | 320x240       |
| VGA              | 640x480       |
| HQQVGA           | 120x80        |
| HQVGA            | 240x160       |
| HVGA             | 480x320       |
| B64X64           | 64x64         |
| B128X64          | 128x64        |
| B128X128         | 128x128       |
| B160X160         | 160x160       |
| B320X320         | 320x320       |
| QQVGA2           | 128x160       |
| WVGA             | 720x480       |
| WVGA2            | 752x480       |
| SVGA             | 800x600       |
| XGA              | 1024x768      |
| WXGA             | 1280x768      |
| SXGA             | 1280x1024     |
| SXGAM            | 1280x960      |
| UXGA             | 1600x1200     |
| HD               | 1280x720      |
| FHD              | 1920x1080     |
| QHD              | 2560x1440     |
| QXGA             | 2048x1536     |
| WQXGA            | 2560x1600     |
| WQXGA2           | 2592x1944     |

### 3.2 pixel_format

| Pixel Format | Description       |
|--------------|-------------------|
| RGB565       | 16-bit RGB format |
| RGB888       | 24-bit RGB format |
| RGBP888      | Separated 24-bit RGB |
| YUV420SP     | Semi-planar YUV   |
| GRAYSCALE    | Grayscale image   |

### 3.3 channel

| Channel Number | Description |
|----------------|-------------|
| CAM_CHN_ID_0   | Channel 0   |
| CAM_CHN_ID_1   | Channel 1   |
| CAM_CHN_ID_2   | Channel 2   |
| CAM_CHN_ID_MAX | Invalid channel |

## 4. Image Sensor Support List

| Image Sensor Model | Resolution<br>Width x Height | Frame Rate |
|--------------------|------------------------------|------------|
| OV5647             | 2592x1944                    | 10 FPS     |
|                    | 1920x1080                    | 30 FPS     |
|                    | 1280x960                     | 45 FPS     |
|                    | 1280x720                     | 60 FPS     |
|                    | 640x480                      | 90 FPS     |
| GC2093             | 1920x1080                    | 30 FPS     |
|                    | 1920x1080                    | 60 FPS     |
|                    | 1280x960                     | 60 FPS     |
|                    | 1280x720                     | 90 FPS     |
| IMX335             | 1920x1080                    | 30 FPS     |
|                    | 2592x1944                    | 30 FPS     |
