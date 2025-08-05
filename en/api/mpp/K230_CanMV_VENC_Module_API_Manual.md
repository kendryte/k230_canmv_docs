# `VENC` Module API Manual

## Overview

This manual provides a detailed introduction to the API of the K230_CanMV VENC module. Developers can use these APIs to perform video encoding, generating streams of different resolutions and encoding formats. The VENC module needs to be used in conjunction with the camera module to achieve encoding functionality.

## API Introduction

The VENC module provides the `Encoder` class, which includes the following methods:

### Encoder.\_\_init__

**Description**

Constructor to initialize the encoder instance.

**Syntax**

```python
encoder = Encoder()
```

**Parameters**

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| None |||

**Return Value**

| Return Value | Description |
|--------------|-------------|
| Encoder Object | Encoder Object |

### `Encoder.SetOutBufs`

**Description**

Configures the output buffer of the encoder.

**Syntax**

```python
Encoder.SetOutBufs(chn, buf_num, width, height)
```

**Parameters**

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| chn            | Encoding channel number | Input       |
| buf_num        | Number of output buffers | Input       |
| width          | Width of the encoded image | Input      |
| height         | Height of the encoded image | Input      |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Notes**

**`Must be called before MediaManager.init()`**

### `Encoder.Create`

**Description**

Creates an encoder instance.

**Syntax**

```python
Encoder.Create(chn, chnAttr)
```

**Parameters**

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| chn            | Encoding channel number | Input       |
| chnAttr        | Encoding channel attribute structure | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Notes**

VENC supports up to 4 encoding channels, with channel numbers ranging from [0, 3]. The 4th channel is fixed for IDE image transmission. Unless calling `compress_for_ide`, it is recommended to use only [0, 2].

### `Encoder.Start`

**Description**

Starts the encoding process.

**Syntax**

```python
Encoder.Start(chn)
```

**Parameters**

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| chn            | Encoding channel number | Input       |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### `Encoder.SendFrame`

**Description**

Sends image data to the encoder for encoding.

**Syntax**

```python
Encoder.SendFrame(venc_chn, frame_info)
```

**Parameters**

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| chn            | Encoding channel number | Input       |
| frame_info     | Raw image information structure | Input |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-zero     | Failure     |

**Notes**

Can encode a full frame of data or a variable-length data stream.

### `Encoder.GetStream`

**Description**

Gets a frame of encoded stream data.

**Syntax**

```python
Encoder.GetStream(chn, streamData,timeout=-1)
```

**Parameters**

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| chn            | Encoding channel number | Input       |
| streamData     | Encoded stream structure | Output     |
| timeout        | Obtain the bitstream timeout. Value range:  [-1, +∞ ) -1：Blocking. 0: Non-blocking.Greater than 0: Timeout period. | Input     |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-zero     | Failure     |

### `Encoder.ReleaseStream`

**Description**

Releases a frame of stream buffer.

**Syntax**

```python
Encoder.ReleaseStream(chn, streamData)
```

**Parameters**

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| chn            | Encoding channel number | Input       |
| streamData     | Encoded stream structure | Input      |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### `Encoder.Stop`

**Description**

Stops the encoding process.

**Syntax**

```python
Encoder.Stop(chn)
```

**Parameters**

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| chn            | Encoding channel number | Input       |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### `Encoder.Destroy`

**Description**

Destroys the encoder instance.

**Syntax**

```python
Encoder.Destroy(chn)
```

**Parameters**

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| chn            | Encoding channel number | Input       |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

## Data Structure Description

### `ChnAttrStr`

**Description**

Encoding channel attribute structure.

**Definition**

```python
class ChnAttrStr:
    def __init__(self, payloadType, profile, picWidth, picHeight,bit_rate = 4000,gopLen = 30,src_frame_rate = 30,dst_frame_rate = 30,mjpeg_quality_factor = 45):
        self.payload_type = payloadType
        self.profile = profile
        self.pic_width = picWidth
        self.pic_height = picHeight
        self.gop_len = gopLen
        self.bit_rate = bit_rate
        self.src_frame_rate = src_frame_rate
        self.dst_frame_rate = dst_frame_rate
        self.mjpeg_quality_factor = mjpeg_quality_factor
```

**Members**

| Member Name    | Description            |
|----------------|------------------------|
| payload_type   | Encoding format (h264/h265) |
| profile        | Encoding Profile       |
| pic_width      | Image width            |
| pic_height     | Image height           |
| gop_len        | Encoding GOP length    |
| bit_rate       | Bitrate                |
| src_frame_rate        | Input frame rate      |
| dst_frame_rate        | Output frame rate     |
| mjpeg_quality_factor  | MJPEG encoding quality factor (image quality compression ratio parameter)   |

### `StreamData`

**Description**

Stream structure.

**Definition**

```python
class StreamData:
    def __init__(self):
        self.data = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.phy_addr = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.data_size = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.stream_type = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.pts = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.pack_cnt = 0
```

**Members**

| Member Name    | Description            |
|----------------|------------------------|
| data           | Stream data address    |
| phy_addr       | Physical address of the code stream     |
| data_size      | Stream data size       |
| stream_type    | Frame type             |
| pts            | Display the timestamp         |
| pack_cnt       | Number of packs in the stream |

**Notes**

`VENC_PACK_CNT_MAX` indicates the maximum number of packs in the stream structure, currently set to 12.

### `payload_type`

**Description**

Encoding format type.

**Members**

| Member Name           | Description       |
|-----------------------|-------------------|
| PAYLOAD_TYPE_H264     | H.264 encoding format |
| PAYLOAD_TYPE_H265     | H.265 encoding format |

### `profile`

**Description**

Encoding Profile.

**Members**

| Member Name          | Description            |
|----------------------|------------------------|
| H264_PROFILE_BASELINE | H.264 Baseline Profile |
| H264_PROFILE_MAIN     | H.264 Main Profile     |
| H264_PROFILE_HIGH     | H.264 High Profile     |
| H265_PROFILE_MAIN     | H.265 Main Profile     |

### `stream_type`

**Description**

Stream frame type.

**Members**

| Member Name          | Description       |
|----------------------|-------------------|
| STREAM_TYPE_HEADER   | Stream Header     |
| STREAM_TYPE_I        | I Frame           |
| STREAM_TYPE_P        | P Frame           |

## Example Programs

### Example 1

Bind VENC to VICAP and save the obtained encoded data to a file.

```python
from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def vi_bind_venc_test(file_name, width=1280, height=720):
    print("VENC test starts")
    venc_chn = VENC_CHN_ID_0
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # Determine file extension
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # Initialize sensor
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=width, height=height, alignment=12)
    sensor.set_pixformat(Sensor.YUV420SP)

    # Instantiate video encoder
    encoder = Encoder()
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # Bind camera and venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, venc_chn))

    # Initialize media manager
    MediaManager.init()

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # Create encoder
    encoder.Create(venc_chn, chnAttr)

    # Start encoding
    encoder.Start(venc_chn)
    # Start camera
    sensor.run()

    frame_count = 0
    print("Save stream to file: ", file_name)

    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                encoder.GetStream(venc_chn, streamData)  # Get a frame of stream

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data)  # Write stream to file
                    print("Stream size: ", streamData.data_size[pack_idx], "Stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(venc_chn, streamData)  # Release a frame of stream

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("User stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # Stop camera
    sensor.stop()
    # Destroy the binding of camera and venc
    del link
    # Stop encoding
    encoder.Stop(venc_chn)
    # Destroy encoder
    encoder.Destroy(venc_chn)
    # Clean buffer
    MediaManager.deinit()
    print("VENC test stops")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_test("/sdcard/examples/test.264", 800, 480)  # Example of binding vi to venc
```

### Example 2

Encode VENC data stream and save it as a file.
Here's the translated text to English:

```python
from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def stream_venc_test(file_name, width=1280, height=720):
    print("venc_test start")
    venc_chn = VENC_CHN_ID_0
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # Determine file type
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # Initialize sensor
    sensor = Sensor()
    sensor.reset()
    # Set camera output buffer
    # Set chn0 output size
    sensor.set_framesize(width=width, height=height, alignment=12)
    # Set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)

    # Instantiate video encoder
    encoder = Encoder()
    # Set video encoder output buffer
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # Initialize media manager
    MediaManager.init()

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # Create encoder
    encoder.Create(venc_chn, chnAttr)

    # Start encoding
    encoder.Start(venc_chn)
    # Start camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    yuv420sp_img = None
    frame_info = k_video_frame_info()
    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                yuv420sp_img = sensor.snapshot(chn=CAM_CHN_ID_0)
                if (yuv420sp_img == -1):
                    continue

                frame_info.v_frame.width = yuv420sp_img.width()
                frame_info.v_frame.height = yuv420sp_img.height()
                frame_info.v_frame.pixel_format = Sensor.YUV420SP
                frame_info.pool_id = yuv420sp_img.poolid()
                frame_info.v_frame.phys_addr[0] = yuv420sp_img.phyaddr()
                # frame_info.v_frame.phys_addr[1] = yuv420sp_img.phyaddr(1)
                if (yuv420sp_img.width() == 800 and yuv420sp_img.height() == 480):
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width * frame_info.v_frame.height + 1024
                elif (yuv420sp_img.width() == 1920 and yuv420sp_img.height() == 1080):
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width * frame_info.v_frame.height + 3072
                elif (yuv420sp_img.width() == 640 and yuv420sp_img.height() == 360):
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width * frame_info.v_frame.height + 3072
                else:
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width * frame_info.v_frame.height

                encoder.SendFrame(venc_chn, frame_info)
                encoder.GetStream(venc_chn, streamData)  # Get a frame of stream

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data)  # Write stream to file
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(venc_chn, streamData)  # Release a frame of stream

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # Stop camera
    sensor.stop()
    # Stop encoding
    encoder.Stop(venc_chn)
    # Destroy encoder
    encoder.Destroy(venc_chn)
    # Clean buffer
    MediaManager.deinit()
    print("venc_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    stream_venc_test("/sdcard/examples/test.264", 800, 480)  # VENC encoding data stream example
```
