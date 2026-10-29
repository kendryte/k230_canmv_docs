# `VENC` 模块 API 手册

## 概述

本手册详细介绍了 K230_CanMV VENC 模块的 API。开发者可以通过调用这些 API 进行视频编码，生成不同分辨率和编码格式的码流。VENC 模块需与相机模块结合使用以实现编码功能。

## API 介绍

VENC 模块提供了 `Encoder` 类，该类包含以下方法：

### Encoder.\_\_init__

**描述**

构造函数，用于初始化解码器实例。

**语法**

```python
encoder = Encoder()
```

**参数**

| 参数名称 | 描述         | 输入/输出 |
|----------|--------------|-----------|
| 无     |||

**返回值**

| 返回值 | 描述    |
|--------|---------|
| Encoder 对象 |  编码器对象   |

### `Encoder.SetOutBufs`

**描述**

配置编码器的输出缓冲区。

**语法**

```python
Encoder.SetOutBufs(buf_num, width, height)
```

**参数**

| 参数名称 | 描述           | 输入/输出 |
|----------|----------------|-----------|
| buf_num  | 输出缓冲区数量 | 输入      |
| width    | 编码图像宽度   | 输入      |
| height   | 编码图像高度   | 输入      |

**返回值**

| 返回值 | 描述    |
|--------|---------|
| 无 ||

**注意事项**

**`必须在 Encoder.Create() 之前调用`**

### `Encoder.Create`

**描述**

创建编码器实例。编码通道号由内部自动通过 `kd_mpi_venc_request_chn` 申请，无需外部传入。

**语法**

```python
Encoder.Create(chnAttr)
```

**参数**

| 参数名称  | 描述               | 输入/输出 |
|-----------|--------------------|-----------|
| chnAttr   | 编码通道属性结构   | 输入      |

**返回值**

| 返回值 | 描述    |
|--------|---------|
| 无 ||

**注意事项**

编码通道号在 `Create` 时自动申请，可通过 `encoder.chn` 获取。`Destroy` 时自动释放通道。

### `Encoder.Start`

**描述**

启动编码过程。

**语法**

```python
Encoder.Start()
```

**参数**

| 参数名称 | 描述         | 输入/输出 |
|----------|--------------|-----------|
| 无 |||

**返回值**

| 返回值 | 描述    |
|--------|---------|
| 无 ||

### `Encoder.RequestIDR`

**描述**

请求编码器将后续输入帧编码为 IDR 关键帧。该方法适用于已创建的 H.264/H.265 编码通道，常用于 RTSP/WebRTC 等场景中有新接收端接入时，减少等待下一个周期性 GOP 关键帧的时间。

**语法**

```python
Encoder.RequestIDR()
```

**参数**

无。

**返回值**

| 返回值 | 描述 |
|--------|------|
| 无 | 请求成功时不返回值；底层请求失败时抛出 `OSError`。 |

**注意事项**

- 需要先调用 `Create()` 创建 H.264 或 H.265 编码通道。
- 请求异步生效，调用本身不返回编码数据。
- 若接收端需要从关键帧开始解码，仍应一并发送 H.264 的 SPS/PPS 或 H.265 的 VPS/SPS/PPS。

### `Encoder.SendFrame`

**描述**

向编码器发送图像数据进行编码。

**语法**

```python
Encoder.SendFrame(frame_info)
```

**参数**

| 参数名称   | 描述               | 输入/输出 |
|------------|--------------------|-----------|
| frame_info | 原始图像信息结构   | 输入      |

**返回值**

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非0    | 失败   |

**注意事项**

可编码完整的一帧数据或不定长度的数据流。

### `Encoder.GetStream`

**描述**

获取一帧编码后的码流数据。

**语法**

```python
Encoder.GetStream(streamData, timeout=-1)
```

**参数**

| 参数名称   | 描述               | 输入/输出 |
|------------|--------------------|-----------|
| streamData | 编码码流结构体     | 输出      |
| timeout    | 获取码流超时时间. 取值范围： [-1, +∞ ) -1：阻塞。 0：非阻塞。 大于0：超时时间     | 输入      |

**返回值**

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非0    | 失败   |

### `Encoder.ReleaseStream`

**描述**

释放一帧码流缓冲区。

**语法**

```python
Encoder.ReleaseStream(streamData)
```

**参数**

| 参数名称   | 描述               | 输入/输出 |
|------------|--------------------|-----------|
| streamData | 编码码流结构体     | 输入      |

**返回值**

| 返回值 | 描述    |
|--------|---------|
| 无 ||

### `Encoder.Stop`

**描述**

停止编码过程。

**语法**

```python
Encoder.Stop()
```

**参数**

| 参数名称 | 描述         | 输入/输出 |
|----------|--------------|-----------|
| 无 |||

**返回值**

| 返回值 | 描述    |
|--------|---------|
| 无 ||

### `Encoder.Destroy`

**描述**

销毁编码器实例，自动释放编码通道。

**语法**

```python
Encoder.Destroy()
```

**参数**

| 参数名称 | 描述         | 输入/输出 |
|----------|--------------|-----------|
| 无 |||

**返回值**

| 返回值 | 描述    |
|--------|---------|
| 无 ||

**注意事项**

`Destroy` 会自动调用 `kd_mpi_venc_release_chn` 释放编码通道，并销毁 `SetOutBufs` 创建的 VB pool。若需要再次使用编码器，需重新调用 `SetOutBufs` 创建 VB pool。

## 数据结构描述

### `ChnAttrStr`

**说明**

编码通道属性结构。

**定义**

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

**成员**

| 成员名称       | 描述            |
|----------------|-----------------|
| payload_type   | 编码格式（h264/h265） |
| profile        | 编码 Profile         |
| pic_width      | 图像宽度             |
| pic_height     | 图像高度             |
| gop_len        | 编码 GOP 长度        |
| bit_rate       | 目标码率，单位为 Kbit/s，默认 `512` |
| src_frame_rate        | 输入帧率      |
| dst_frame_rate        | 输出帧率      |
| mjpeg_quality_factor  | MJPEG 编码质量因子（画质压缩比参数）   |

### `StreamData`

**说明**

码流结构体。

**定义**

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

**成员**

| 成员名称      | 描述             |
|---------------|-----------------|
| data          | 码流数据地址     |
| phy_addr      | 码流物理地址     |
| data_size     | 码流数据大小     |
| stream_type   | 帧类型           |
| pts           | 显示时间戳         |
| pack_cnt      | 码流中 pack 的个数 |

**注意事项**

`VENC_PACK_CNT_MAX` 表示码流结构体中 pack 的最大个数，当前设定为 12。

### `payload_type`

**描述**

编码格式类型。

**成员**

| 成员名称               | 描述           |
|-----------------------|----------------|
| PAYLOAD_TYPE_H264     | H.264 编码格式 |
| PAYLOAD_TYPE_H265     | H.265 编码格式 |

### `profile`

**描述**

编码 Profile。

**成员**

| 成员名称                | 描述                   |
|------------------------|------------------------|
| H264_PROFILE_BASELINE  | H.264 Baseline Profile  |
| H264_PROFILE_MAIN      | H.264 Main Profile      |
| H264_PROFILE_HIGH      | H.264 High Profile      |
| H265_PROFILE_MAIN      | H.265 Main Profile      |

### `stream_type`

**描述**

码流帧类型。

**成员**

| 成员名称            | 描述       |
|---------------------|------------|
| STREAM_TYPE_HEADER   | 码流 Header |
| STREAM_TYPE_I       | I 帧       |
| STREAM_TYPE_P       | P 帧       |

## 示例程序

### 例程 1

将 VENC 绑定到 VICAP，并将获取到的编码数据保存到文件。

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

### 例程2

venc编码数据流，并保存成文件。

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
