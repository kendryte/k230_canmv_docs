# `VENC` Module API Manual

## Overview

This manual provides detailed information on the APIs of the K230_CanMV VENC module. Developers can use these APIs to perform video encoding and generate bitstreams at different resolutions and encoding formats. The VENC module needs to be used in conjunction with the camera module to implement encoding functionality.

## API Overview

The VENC module provides the `Encoder` class, which contains the following methods:

### Encoder.**init**

**Description**

Constructor used to initialize the encoder instance.

**Syntax**

```python
encoder = Encoder()
```

**Parameters**

| Parameter Name | Description    | Input/Output |
|----------|----------------|----------|
| None     |||

**Return Value**

| Return Value | Description    |
|--------|---------|
| Encoder object |  Encoder object   |

### `Encoder.SetOutBufs`

**Description**

Configures the output buffers of the encoder.

**Syntax**

```python
Encoder.SetOutBufs(buf_num, width, height)
```

**Parameters**

| Parameter Name | Description         | Input/Output |
|----------|----------------|-----------|
| buf_num  | Number of output buffers | Input      |
| width    | Width of encoded image   | Input      |
| height   | Height of encoded image  | Input      |

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

**Notes**

**`Must be called before Encoder.Create()`**

### `Encoder.Create`

**Description**

Creates an encoder instance. The encoding channel number is automatically requested internally via `kd_mpi_venc_request_chn`, and does not need to be passed in externally.

**Syntax**

```python
Encoder.Create(chnAttr)
```

**Parameters**

| Parameter Name | Description               | Input/Output |
|-----------|--------------------|-----------|
| chnAttr   | Encoding channel attribute structure | Input      |

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

**Notes**

The encoding channel number is automatically requested during `Create`, and can be obtained via `encoder.chn`. The channel is automatically released upon `Destroy`.

### `Encoder.Start`

**Description**

Starts the encoding process.

**Syntax**

```python
Encoder.Start()
```

**Parameters**

| Parameter Name | Description         | Input/Output |
|----------|--------------|-----------|
| None |||

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

### `Encoder.RequestIDR`

**Description**

Requests the encoder to encode subsequent input frames as IDR key frames. This method applies to already created H.264/H.265 encoding channels, and is commonly used in scenarios such as RTSP/WebRTC when a new receiving end joins, to reduce the wait time for the next periodic GOP key frame.

**Syntax**

```python
Encoder.RequestIDR()
```

**Parameters**

None.

**Return Value**

| Return Value | Description |
|--------|------|
| None | Returns no value on a successful request; throws `OSError` if the underlying request fails. |

**Notes**

- `Create()` must be called first to create an H.264 or H.265 encoding channel.
- The request takes effect asynchronously; the call itself does not return encoded data.
- If the receiving end needs to start decoding from a key frame, the H.264 SPS/PPS or H.265 VPS/SPS/PPS should also be sent.

### `Encoder.SendFrame`

**Description**

Sends image data to the encoder for encoding.

**Syntax**

```python
Encoder.SendFrame(frame_info)
```

**Parameters**

| Parameter Name   | Description               | Input/Output |
|------------|--------------------|-----------|
| frame_info | Raw image information structure   | Input      |

**Return Value**

| Return Value | Description   |
|--------|--------|
| 0      | Success   |
| Non-0    | Failure   |

**Notes**

It can encode a complete frame of data or a variable-length data stream.

### `Encoder.GetStream`

**Description**

Obtains a frame of encoded stream data.

**Syntax**

```python
Encoder.GetStream(streamData, timeout=-1)
```

**Parameters**

| Parameter Name   | Description               | Input/Output |
|------------|--------------------|-----------|
| streamData | Encoded stream structure     | Output      |
| timeout    | Timeout for obtaining the stream. Value range: [-1, +∞) -1: Blocking. 0: Non-blocking. Greater than 0: Timeout duration     | Input      |

**Return Value**

| Return Value | Description   |
|--------|--------|
| 0      | Success   |
| Non-0    | Failure   |

### `Encoder.ReleaseStream`

**Description**

Releases a frame's stream buffer.

**Syntax**

```python
Encoder.ReleaseStream(streamData)
```

**Parameters**

| Parameter Name   | Description               | Input/Output |
|------------|--------------------|-----------|
| streamData | Encoded stream structure     | Input      |

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

### `Encoder.Stop`

**Description**

Stops the encoding process.

**Syntax**

```python
Encoder.Stop()
```

**Parameters**

| Parameter Name | Description         | Input/Output |
|----------|--------------|-----------|
| None |||

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

### `Encoder.Destroy`

**Description**

Destroys the encoder instance and automatically releases the encoding channel.

**Syntax**

```python
Encoder.Destroy()
```

**Parameters**

| Parameter Name | Description         | Input/Output |
|----------|--------------|-----------|
| None |||

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

**Notes**

`Destroy` automatically calls `kd_mpi_venc_release_chn` to release the encoding channel, and destroys the VB pool created by `SetOutBufs`. To use the encoder again, `SetOutBufs` must be called again to create a VB pool.

## Data Structure Description

### `ChnAttrStr`

**Description**

Encoding channel attribute structure.

**Definition**

```python
class ChnAttrStr:
    def __init__(self, payloadType, profile, picWidth, picHeight,bit_rate = 512,gopLen = 30,src_frame_rate = 30,dst_frame_rate = 30,mjpeg_quality_factor = 45):
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

| Member Name       | Description            |
|----------------|-----------------|
| payload_type   | Encoding format (h264/h265) |
| profile        | Encoding Profile         |
| pic_width      | Image width             |
| pic_height     | Image height             |
| gop_len        | Encoding GOP length        |
| bit_rate       | Target bit rate, in Kbit/s, default `512` |
| src_frame_rate        | Input frame rate      |
| dst_frame_rate        | Output frame rate      |
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

| Member Name      | Description             |
|---------------|-----------------|
| data          | Stream data address     |
| phy_addr      | Stream physical address     |
| data_size     | Stream data size     |
| stream_type   | Frame type           |
| pts           | Presentation timestamp         |
| pack_cnt      | Number of packs in the stream |

**Notes**

`VENC_PACK_CNT_MAX` indicates the maximum number of packs in the stream structure, currently set to 12.

### `payload_type`

**Description**

Encoding format type.

**Members**

| Member Name               | Description           |
|-----------------------|----------------|
| PAYLOAD_TYPE_H264     | H.264 encoding format |
| PAYLOAD_TYPE_H265     | H.265 encoding format |

### `profile`

**Description**

Encoding Profile.

**Members**

| Member Name                | Description                   |
|------------------------|------------------------|
| H264_PROFILE_BASELINE  | H.264 Baseline Profile  |
| H264_PROFILE_MAIN      | H.264 Main Profile      |
| H264_PROFILE_HIGH      | H.264 High Profile      |
| H265_PROFILE_MAIN      | H.265 Main Profile      |

### `stream_type`

**Description**

Stream frame type.

**Members**

| Member Name            | Description       |
|---------------------|------------|
| STREAM_TYPE_HEADER   | Stream Header |
| STREAM_TYPE_I       | I frame       |
| STREAM_TYPE_P       | P frame       |

## Example Programs

### Example 1

Bind VENC to VICAP and save the obtained encoded data to a file.

```python
from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def vi_bind_venc_test(file_name,width=1280, height=720):
    print("venc_test start")
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # 判断文件类型
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # 初始化sensor
    sensor = Sensor()
    sensor.reset()
    # 设置camera 输出buffer
    # set chn0 output size
    sensor.set_framesize(width = width, height = height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)


    # 实例化video encoder
    encoder = Encoder()
    # 设置video encoder 输出buffer
    encoder.SetOutBufs(8, width, height)

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(chnAttr)

    # 绑定camera和venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, encoder.chn))

    # 开始编码
    encoder.Start()
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                encoder.GetStream(streamData) # 获取一帧码流

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # 码流写文件
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(streamData) # 释放一帧码流

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # 停止camera
    sensor.stop()
    # 销毁camera和venc的绑定
    link.destroy()
    # 停止编码
    encoder.Stop()
    # 销毁编码器
    encoder.Destroy()
    print("venc_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_test("/data/test.264",800,480)  # vi绑定venc示例

```

### Example 2

Encode data stream with venc and save it to a file.

```python
from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def stream_venc_test(file_name,width=1280, height=720):
    print("venc_test start")
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # 判断文件类型
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # 初始化sensor
    sensor = Sensor()
    sensor.reset()
    # 设置camera 输出buffer
    # set chn0 output size
    sensor.set_framesize(width = width, height = height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)


    # 实例化video encoder
    encoder = Encoder()
    # 设置video encoder 输出buffer
    encoder.SetOutBufs(8, width, height)

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(chnAttr)

    # 开始编码
    encoder.Start()
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    yuv420sp_img = None
    frame_info = k_video_frame_info()
    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                frame_info  = sensor.snapshot(chn=CAM_CHN_ID_0,dump_frame=True)
                #frame_info.v_frame.nv12_to_grayscale() # convert to grayscale
                encoder.SendFrame(frame_info)
                encoder.GetStream(streamData) # 获取一帧码流

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # 码流写文件
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(streamData) # 释放一帧码流

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # 停止camera
    sensor.stop()
    # 停止编码
    encoder.Stop()
    # 销毁编码器
    encoder.Destroy()
    print("venc_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    stream_venc_test("/data/test.264",800,480)  # venc编码数据流示例

```
