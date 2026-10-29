# `VDEC` Module API Manual

## Overview

This document provides a detailed introduction to the K230_CanMV VDEC module's API. This module supports H.264 and H.265 decoding, and can be bound to the VO module to output the decoded data to the VO display device.

## API Introduction

This module provides the `Decoder` class, which contains the following methods:

### Decoder.\_\_init\_\_

**Description**

Constructor used to initialize a decoder instance.

**Syntax**  

```python
decoder = Decoder(type)
```

**Parameters**  

| Parameter Name | Description | Input/Output |
|----------|--------------|-----------|
| type     | Encoding type | Input      |

**Return Value**  

| Return Value | Description    |
|--------|---------|
| Decoder object |  Decoder object   |

**Notes**  

The VDEC module supports up to four concurrent decodings.

### Decoder.create

**Description**

Create a decoder instance.

**Syntax**  

```python
Decoder.create()
```

**Parameters**

None

**Return Value**  

| Return Value | Description    |
|--------|---------|
| None ||

### Decoder.destroy

**Description**

Destroy a decoder instance.

**Syntax**  

```python
Decoder.destroy()
```

**Parameters**

None

**Return Value**  

| Return Value | Description    |
|--------|---------|
| None ||

### Decoder.start

**Description**

Start the decoder and begin the decoding process.

**Syntax**  

```python
Decoder.start()
```

**Parameters**

None

**Return Value**  

| Return Value | Description    |
|--------|---------|
| None ||

### Decoder.decode

**Description**

Decode one frame of data.

**Syntax**  

```python
Decoder.decode(stream_data)
```

**Parameters**  

| Parameter Name   | Description     | Input/Output |
|------------|----------|-----------|
| stream_data | Encoded data | Input      |

**Return Value**  

| Return Value | Description    |
|--------|---------|
| None ||

### Decoder.stop

**Description**

Release the stream buffer of the current decoded frame.

**Syntax**  

```python
Decoder.stop()
```

**Parameters**

None

**Return Value**  

| Return Value | Description    |
|--------|---------|
| None ||

### Decoder.get_vdec_channel

**Description**

Return the decoder output channel number.

**Syntax**  

```python
Decoder.get_vdec_channel()
```

**Parameters**

None

**Return Value**  

| Return Value | Description    |
|--------|---------|
| chn    | Decoder output channel number |

### Decoder.bind_info

**Description**

Used when calling `Display.bind_layer`, to obtain binding information.

**Syntax**  

```python
Decoder.bind_info(x = 0, y = 0, width = 1920,height = 1080,pix_format=PIXEL_FORMAT_YUV_SEMIPLANAR_420,chn = 0)
```

**Parameters**  

| Parameter Name | Description               | Input/Output |
|----------|--------------------|-----------|
| x        | Horizontal starting coordinate of the binding area | Input      |
| y        | Vertical starting coordinate of the binding area | Input      |
| width    | Width of the decoded frame      | Input      |
| height   | Height of the decoded frame      | Input      |
| pix_format | Image pixel format    | Input      |
| chn      | Decoder output channel number    | Input      |

**Return Value**  

| Return Value | Description    |
|--------|---------|
| dict object | Contains the channel's source information, area size, and pixel format |

## Data Structure Description

### StreamData

**Description**

Stream structure containing decoded data and its timestamp information.

**Definition**

```python
class StreamData:
    def __init__(self):
        self.data
        self.pts
```

**Members**

| Member Name | Description       |
|----------|------------|
| data     | Stream data   |
| pts      | Timestamp information |

## Example Program

### Example 1

```python
from media.media import *
from mpp.payload_struct import *
import media.vdecoder as vdecoder
from media.display import *
import time
import os

STREAM_SIZE = 40960

def vdec_test(file_name, width=1280, height=720):
    print("vdec_test start")
    vdec_chn = VENC_CHN_ID_0
    vdec_width = ALIGN_UP(width, 16)
    vdec_height = height
    vdec = None
    vdec_payload_type = K_PT_H264

    # display_type = Display.VIRT
    display_type = Display.ST7701  # 使用 ST7701 LCD 屏幕作为输出，最大分辨率 800*480
    # display_type = Display.LT9611  # 使用 HDMI 作为输出

    # 判断文件类型
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        vdec_payload_type = K_PT_H264
    elif suffix == '265':
        vdec_payload_type = K_PT_H265
    else:
        print("未知的文件扩展名")
        return

    # 实例化视频解码器
    vdec = vdecoder.Decoder(vdec_payload_type)

    # 初始化显示设备
    if display_type == Display.VIRT:
        Display.init(display_type, width=vdec_width, height=vdec_height, fps=30)
    else:
        Display.init(display_type, to_ide=True)

    # 初始化缓冲区
    MediaManager.init()

    # 创建视频解码器
    vdec.create()

    # 绑定显示
    bind_info = vdec.bind_info(width=vdec_width, height=vdec_height, chn=vdec.get_vdec_channel())
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1)

    vdec.start()

    # 打开文件
    with open(file_name, "rb") as fi:
        while True:
            os.exitpoint()
            # 读取视频数据流
            data = fi.read(STREAM_SIZE)
            if not data:
                break
            # 解码数据流
            vdec.decode(data)

    # 停止视频解码器
    vdec.stop()
    # 销毁视频解码器
    vdec.destroy()
    time.sleep(1)

    # 关闭显示
    Display.deinit()
    # 释放缓冲区
    MediaManager.deinit()

    print("vdec_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vdec_test("/sdcard/examples/test.264", 800, 480)  # 解码 H.264/H.265 视频文件
```
