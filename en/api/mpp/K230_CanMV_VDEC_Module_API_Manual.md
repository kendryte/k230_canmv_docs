# `VDEC` Module API Manual

## Overview

This document provides a detailed introduction to the K230_CanMV VDEC module's API. This module supports H.264 and H.265 decoding and can be bound to the VO module to output decoded data to VO display devices.

## API Introduction

This module provides the `Decoder` class, which includes the following methods:

### Decoder.\_\_init\_\_

**Description**

Constructor to initialize the decoder instance.

**Syntax**

```python
decoder = Decoder(type)
```

**Parameters**

| Parameter Name | Description    | Input/Output |
|----------------|----------------|--------------|
| type           | Encoding type  | Input        |

**Return Values**

| Return Value | Description |
|--------------|-------------|
| Decoder object  | Decoder object |

**Notes**

The VDEC module supports up to four concurrent decodings.

### Decoder.create

**Description**

Creates a decoder instance.

**Syntax**

```python
Decoder.create()
```

**Parameters**

None

**Return Values**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Decoder.destroy

**Description**

Destroys the decoder instance.

**Syntax**

```python
Decoder.destroy()
```

**Parameters**

None

**Return Values**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Decoder.start

**Description**

Starts the decoder and begins the decoding process.

**Syntax**

```python
Decoder.start()
```

**Parameters**

None

**Return Values**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Decoder.decode

**Description**

Decodes a frame of data.

**Syntax**

```python
Decoder.decode(stream_data)
```

**Parameters**

| Parameter Name | Description  | Input/Output |
|----------------|--------------|--------------|
| stream_data    | Encoded data | Input        |

**Return Values**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Decoder.stop

**Description**

Releases the current decoded frame's stream buffer.

**Syntax**

```python
Decoder.stop()
```

**Parameters**

None

**Return Values**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Decoder.get_vdec_channel

**Description**

Return the output channel number of the decoder.

**Syntax**  

```python
Decoder.get_vdec_channel()
```

**Parameters**

None

**Return Values**  

| Return Value | Description |
|--------------|-------------|
| chn          | The output channel number |

### Decoder.bind_info

**Description**

Used to get binding information when calling `Display.bind_layer`.

**Syntax**

```python
Decoder.bind_info(x = 0, y = 0, width = 1920,height = 1080,pix_format=PIXEL_FORMAT_YUV_SEMIPLANAR_420,chn = 0)
```

**Parameters**

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| x              | The horizontal starting coordinates of the binding area | Input |
| y              | The vertical starting coordinate of the binding area | Input |
| width          | Width of the decoded frame | Input |
| height         | Height of the decoded frame | Input |
| pix_format     | The pixel format of image     | Input |
| chn            | Decoding output channel number | Input |

**Return Values**

| Return Value | Description |
|--------------|-------------|
| dict object  | It includes the source information of the channel, the area size and the pixel format |

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

| Member Name | Description    |
|-------------|----------------|
| data        | Stream data    |
| pts         | Timestamp info |

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
    display_type = Display.ST7701  # Use ST7701 LCD screen for output, max resolution 800*480
    # display_type = Display.LT9611  # Use HDMI for output

    # Determine file type
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        vdec_payload_type = K_PT_H264
    elif suffix == '265':
        vdec_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # Instantiate video decoder
    vdec = vdecoder.Decoder(vdec_payload_type)

    # Initialize display device
    if display_type == Display.VIRT:
        Display.init(display_type, width=vdec_width, height=vdec_height, fps=30)
    else:
        Display.init(display_type, to_ide=True)

    # Initialize buffer
    MediaManager.init()

    # Create video decoder
    vdec.create()

    # Bind display
    bind_info = vdec.bind_info(width=vdec_width, height=vdec_height, chn=vdec.get_vdec_channel())
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1)

    vdec.start()

    # Open file
    with open(file_name, "rb") as fi:
        while True:
            os.exitpoint()
            # Read video data stream
            data = fi.read(STREAM_SIZE)
            if not data:
                break
            # Decode data stream
            vdec.decode(data)

    # Stop video decoder
    vdec.stop()
    # Destroy video decoder
    vdec.destroy()
    time.sleep(1)

    # Close display
    Display.deinit()
    # Release buffer
    MediaManager.deinit()

    print("vdec_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vdec_test("/sdcard/examples/test.264", 800, 480)  # Decode H.264/H.265 video file
```
