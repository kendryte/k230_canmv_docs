# 3.7 `MP4` 模块 API 手册

## 1. 概述

本文详细介绍了 K230_CanMV MP4 模块 API 的功能与使用方法。MP4 模块主要用于生成 MP4 文件，开发者无需关注底层实现细节，只需调用所提供的 API 即可生成不同编码格式和视频分辨率的 MP4 文件。本文将分别介绍 MP4Container API 和 kd_mp4* API，帮助开发者快速上手并灵活运用这些接口。

## 2. MP4Container API 介绍

`MP4Container` 类提供了简便的方法来录制摄像头画面和采集声音，生成 MP4 文件。该模块简化了 MP4 文件的处理流程，适合不需要关注底层实现细节的应用场景。

### 2.1 MP4Container.Create

**描述**

用于创建 MP4Container 实例。

**语法**

```python
MP4Container.Create(mp4Cfg)
```

**参数**

| 参数名称  | 描述                      | 输入/输出 |
|-----------|---------------------------|-----------|
| mp4cfg    | MP4Container 配置        | 输入      |

**返回值**

| 返回值  | 描述       |
|---------|------------|
| 0       | 成功       |
| 非 0    | 失败       |

### 2.2 MP4Container.Start

**描述**

启动 MP4Container 开始处理数据。

**语法**

```python
MP4Container.Start()
```

**参数**

无

**返回值**

| 返回值 | 描述 |
|--------|------|
| 0      | 成功 |
| 非0    | 失败 |

### 2.3 MP4Container.Process

**描述**

将一帧音频/视频数据写入 MP4 文件。

**语法**

```python
MP4Container.Process()
```

**参数**

无

**返回值**

| 返回值 | 描述 |
|--------|------|
| 0      | 成功 |
| 非0    | 失败 |

### 2.4 MP4Container.Stop

**描述**

停止 MP4Container 的数据处理。

**语法**

```python
MP4Container.Stop()
```

**参数**

无

**返回值**

| 返回值 | 描述 |
|--------|------|
| 0      | 成功 |
| 非0    | 失败 |

### 2.5 MP4Container.Destroy

**描述**

销毁创建的 MP4Container 实例。

**语法**

```python
MP4Container.Destroy()
```

**参数**

无

**返回值**

| 返回值 | 描述 |
|--------|------|
| 0      | 成功 |
| 非0    | 失败 |

## 3. kd_mp4* API介绍

本节详细描述与 MP4 模块相关的底层函数接口，用于更灵活地控制 MP4 文件的创建、写入和读取。这些接口适用于需要更高灵活性和控制力的开发者，允许他们精细控制 MP4 文件的各个方面，包括容器的创建、轨道管理、数据写入和读取等操作，并与其他模块配合生成一个综合性的解决方案。

### 3.1 kd_mp4_create

**描述**
创建 MP4 容器实例并初始化配置。

**语法**

```python
handle = k_u64_ptr()
ret = kd_mp4_create(handle, mp4_cfg)
```

**参数**
| 参数名称  | 描述                  | 输入/输出 |
|-----------|-----------------------|-----------|
| handle    | 输出参数，返回 MP4 实例句柄 | 输出      |
| [config](#46-k_mp4_config_s)    | MP4 容器配置结构体指针 | 输入      |

**返回值**
| 返回值  | 描述       |
|---------|------------|
| 0       | 成功       |
| 非 0    | 失败，错误码见具体实现 |

### 3.2 kd_mp4_create_track

**描述**
在 MP4 容器中创建音视频轨道。

**语法**

```python
track_handle = k_u64_ptr()
ret = kd_mp4_create_track(handle, track_handle, track_info)
```

**参数**
| 参数名称     | 描述                  | 输入/输出 |
|--------------|-----------------------|-----------|
| handle       | MP4 实例句柄         | 输入      |
| [track_info](#47-k_mp4_track_info_s)   | 轨道信息结构体指针    | 输入      |

**返回值**
| 返回值  | 描述       |
|---------|------------|
| 0       | 成功       |
| 非 0    | 失败       |

### 3.3 kd_mp4_destroy_tracks

**描述**
销毁 MP4 容器中所有已创建的轨道。

**语法**

```python
ret = kd_mp4_destroy_tracks(handle)
```

**参数**
| 参数名称  | 描述          | 输入/输出 |
|-----------|---------------|-----------|
| handle    | MP4 实例句柄 | 输入      |

**返回值**
| 返回值  | 描述       |
|---------|------------|
| 0       | 成功       |
| 非 0    | 失败       |

---

### 3.4 kd_mp4_write_frame

**描述**
向 MP4 文件写入一帧音视频数据。

**语法**

```python
ret = kd_mp4_write_frame(handle, track_id, frame_data)
```

**参数**
| 参数名称     | 描述                  | 输入/输出 |
|--------------|-----------------------|-----------|
| handle       | MP4 实例句柄         | 输入      |
| track_id     | 目标轨道的 ID        | 输入      |
| [frame_data](#48-k_mp4_frame_data_s)   | 帧数据结构体指针      | 输入      |

**返回值**
| 返回值  | 描述       |
|---------|------------|
| 0       | 成功       |
| 非 0    | 失败       |

### 3.5 kd_mp4_get_file_info

**描述**
获取 MP4 文件的全局信息（如总时长、轨道数量）。

**语法**

```python
file_info = k_mp4_file_info_s()
ret = kd_mp4_get_file_info(handle, file_info)
```

**参数**
| 参数名称     | 描述                  | 输入/输出 |
|--------------|-----------------------|-----------|
| handle       | MP4 实例句柄         | 输入      |
| file_info    | 文件信息结构体指针    | 输出      |

**返回值**
| 返回值  | 描述       |
|---------|------------|
| 0       | 成功       |
| 非 0    | 失败       |

### 3.6 kd_mp4_get_track_by_index

**描述**
通过索引获取指定轨道的详细信息。

**语法**

```python
track_info = k_mp4_track_info_s()
ret = kd_mp4_get_track_by_index(handle, track_index, track_info)
```

**参数**
| 参数名称      | 描述                  | 输入/输出 |
|---------------|-----------------------|-----------|
| handle        | MP4 实例句柄         | 输入      |
| track_index   | 轨道索引（从 0 开始）| 输入      |
| track_info    | 轨道信息结构体指针    | 输出      |

**返回值**
| 返回值  | 描述       |
|---------|------------|
| 0       | 成功       |
| 非 0    | 失败       |

---

### 3.7 kd_mp4_get_frame

**描述**
从 MP4 文件中读取一帧音视频数据。

**语法**

```python
ret = kd_mp4_get_frame(handle, frame_data)
```

**参数**
| 参数名称     | 描述                  | 输入/输出 |
|--------------|-----------------------|-----------|
| handle       | MP4 实例句柄         | 输入      |
| frame_data   | 帧数据结构体指针      | 输出      |

**返回值**
| 返回值  | 描述       |
|---------|------------|
| 0       | 成功       |
| 非 0    | 失败       |

## 4. 数据结构描述

### 4.1 Mp4CfgStr

**说明**

MP4Container 的配置属性。

**定义**

```python
class Mp4CfgStr:
    def __init__(self, type):
        self.type = type
        self.muxerCfg = MuxerCfgStr()

    def SetMuxerCfg(self, fileName, videoPayloadType, picWidth, picHeight, audioPayloadType, fmp4Flag=0):
        self.muxerCfg.file_name = fileName
        self.muxerCfg.video_payload_type = videoPayloadType
        self.muxerCfg.pic_width = picWidth
        self.muxerCfg.pic_height = picHeight
        self.muxerCfg.audio_payload_type = audioPayloadType
        self.muxerCfg.fmp4_flag = fmp4Flag
```

**成员**

| 成员名称  | 描述                                 |
|-----------|--------------------------------------|
| type      | MP4Container 类型：muxer/demuxer，当前仅支持 muxer |
| muxerCfg  | muxer 配置                           |

#### 相关数据类型及接口

- MP4Container.Create

### 4.2 MuxerCfgStr

**说明**

MP4Container muxer 类型的配置属性。

**定义**

```python
class MuxerCfgStr:
    def __init__(self):
        self.file_name = 0
        self.video_payload_type = 0
        self.pic_width = 0
        self.pic_height = 0
        self.audio_payload_type = 0
```

**成员**

| 成员名称           | 描述                   |
|--------------------|------------------------|
| file_name          | 生成的 MP4 文件名     |
| video_payload_type | 视频编码格式           |
| pic_width          | 视频帧宽度             |
| pic_height         | 视频帧高度             |
| audio_payload_type | 音频编码格式           |

#### 相关数据类型及接口

- MP4Container.Create

### 4.3 MP4Container 类型

**说明**

MP4Container 类型枚举。

**成员**

| 成员名称                        | 描述                     |
|---------------------------------|--------------------------|
| MP4_CONFIG_TYPE_MUXER          | muxer 类型               |
| MP4_CONFIG_TYPE_DEMUXER        | demuxer 类型，目前不支持 |

### 4.4 video_payload_type

**说明**

视频编码类型。

**成员**

| 成员名称                     | 描述                       |
|------------------------------|----------------------------|
| MP4_CODEC_ID_H264            | H.264 视频编码类型        |
| MP4_CODEC_ID_H265            | H.265 视频编码类型        |

### 4.5 audio_payload_type

**说明**

音频编码类型。

**成员**

| 成员名称                     | 描述                       |
|------------------------------|----------------------------|
| MP4_CODEC_ID_G711U           | G.711U 音频编码类型       |
| MP4_CODEC_ID_G711A           | G.711A 音频编码类型       |

### 4.6 k_mp4_config_s

**说明**
MP4 容器的全局配置结构体。

**成员**
| 成员名称          | 描述                              |
|-------------------|-----------------------------------|
| config_type       | 容器类型（如 `K_MP4_CONFIG_MUXER`）|
| muxer_config      | Muxer 配置（文件名、编码格式等）  |
| demuxer_config    | Demuxer 配置（当前未支持）        |

---

### 4.7 k_mp4_track_info_s

**说明**
轨道信息结构体，用于创建音视频轨道。

**成员**
| 成员名称      | 描述                              |
|---------------|-----------------------------------|
| track_type    | 轨道类型（如 `K_MP4_STREAM_VIDEO`）|
| time_scale    | 时间基准（单位：Hz）              |
| video_info    | 视频参数（分辨率、编码格式等）    |
| audio_info    | 音频参数（采样率、声道数等）      |

---

### 4.8 k_mp4_frame_data_s

**说明**
帧数据结构体，用于读写音视频帧。

**成员**
| 成员名称      | 描述                              |
|---------------|-----------------------------------|
| codec_id      | 编码类型（如 `K_MP4_CODEC_ID_H264`）|
| time_stamp    | 时间戳（单位：毫秒）              |
| data          | 数据指针                          |
| data_length   | 数据长度（字节）                  |
| eof           | 结束标志（1 表示最后一帧）        |

## 5. 示例程序

### 5.1 例程 1

该实例用于演示如何调用 `Mp4Container` 类来生成 MP4 文件。通过该例程，开发者可以录制摄像头画面和采集声音，生成 MP4 文件。该示例展示了如何创建 `Mp4Container` 实例、配置 MP4 文件参数、启动和停止 MP4 录制过程。适合需要快速上手 MP4 文件生成的开发者。

```python
from media.mp4format import *
import os

def canmv_mp4_muxer_test():
    print("mp4_muxer_test 开始")
    width = 1280
    height = 720
    # BPI 开发板请设置宽高为640*360
    # width=640
    # height=360
    # 实例化 MP4 Container
    mp4_muxer = Mp4Container()
    mp4_cfg = Mp4CfgStr(mp4_muxer.MP4_CONFIG_TYPE_MUXER)
    if mp4_cfg.type == mp4_muxer.MP4_CONFIG_TYPE_MUXER:
        file_name = "/sdcard/examples/test.mp4"
        mp4_cfg.SetMuxerCfg(file_name, mp4_muxer.MP4_CODEC_ID_H265, width, height, mp4_muxer.MP4_CODEC_ID_G711U)
    # 创建 MP4 muxer
    mp4_muxer.Create(mp4_cfg)
    # 启动 MP4 muxer
    mp4_muxer.Start()

    frame_count = 0
    try:
        while True:
            os.exitpoint()
            # 处理音视频数据，按 MP4 格式写入文件
            mp4_muxer.Process()
            frame_count += 1
            print("frame_count = ", frame_count)
            if frame_count >= 200:
                break
    except BaseException as e:
        print(e)
    # 停止 MP4 muxer
    mp4_muxer.Stop()
    # 销毁 MP4 muxer
    mp4_muxer.Destroy()
    print("mp4_muxer_test 停止")

canmv_mp4_muxer_test()
```

### 5.2 例程 2

该实例用于演示如何调用 kd_mp4* API 来直接操作 MP4 模块。通过该例程，开发者可以了解如何创建 MP4 容器、创建音视频轨道、写入音视频帧数据以及销毁 MP4 容器。该例程展示了更底层的操作方式，适合需要精细控制 MP4 文件生成过程的开发者。

```python
# Save MP4 file example
#
# Note: You will need an SD card to run this example.
#
# You can capture audio and video and save them as MP4.The current version only supports MP4 format, video supports 264/265, and audio supports g711a/g711u.

from mpp.mp4_format import *
from mpp.mp4_format_struct import *
from media.vencoder import *
from media.sensor import *
from media.media import *
import uctypes
import time
import os

def mp4_muxer_init(file_name,  fmp4_flag):
    mp4_cfg = k_mp4_config_s()
    mp4_cfg.config_type = K_MP4_CONFIG_MUXER
    mp4_cfg.muxer_config.file_name[:] = bytes(file_name, 'utf-8')
    mp4_cfg.muxer_config.fmp4_flag = fmp4_flag

    handle = k_u64_ptr()
    ret = kd_mp4_create(handle, mp4_cfg)
    if ret:
        raise OSError("kd_mp4_create failed.")
    return handle.value

def mp4_muxer_create_video_track(mp4_handle, width, height, video_payload_type):
    video_track_info = k_mp4_track_info_s()
    video_track_info.track_type = K_MP4_STREAM_VIDEO
    video_track_info.time_scale = 1000
    video_track_info.video_info.width = width
    video_track_info.video_info.height = height
    video_track_info.video_info.codec_id = video_payload_type
    video_track_handle = k_u64_ptr()
    ret = kd_mp4_create_track(mp4_handle, video_track_handle, video_track_info)
    if ret:
        raise OSError("kd_mp4_create_track failed.")
    return video_track_handle.value

def mp4_muxer_create_audio_track(mp4_handle,channel,sample_rate, bit_per_sample ,audio_payload_type):
    audio_track_info = k_mp4_track_info_s()
    audio_track_info.track_type = K_MP4_STREAM_AUDIO
    audio_track_info.time_scale = 1000
    audio_track_info.audio_info.channels = channel
    audio_track_info.audio_info.codec_id = audio_payload_type
    audio_track_info.audio_info.sample_rate = sample_rate
    audio_track_info.audio_info.bit_per_sample = bit_per_sample
    audio_track_handle = k_u64_ptr()
    ret = kd_mp4_create_track(mp4_handle, audio_track_handle, audio_track_info)
    if ret:
        raise OSError("kd_mp4_create_track failed.")
    return audio_track_handle.value

def vi_bind_venc_mp4_test(file_name,width=1280, height=720,venc_payload_type = K_PT_H264):
    print("venc_test start")
    venc_chn = VENC_CHN_ID_0
    width = ALIGN_UP(width, 16)

    frame_data = k_mp4_frame_data_s()
    save_idr = bytearray(width * height * 3 // 4)
    idr_index = 0

    # mp4 muxer init
    mp4_handle = mp4_muxer_init(file_name, True)

    # create video track
    if venc_payload_type == K_PT_H264:
        video_payload_type = K_MP4_CODEC_ID_H264
    elif venc_payload_type == K_PT_H265:
        video_payload_type = K_MP4_CODEC_ID_H265
    mp4_video_track_handle = mp4_muxer_create_video_track(mp4_handle, width, height, video_payload_type)

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
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # 绑定camera和venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, venc_chn))

    # init media manager
    MediaManager.init()

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(venc_chn, chnAttr)

    # 开始编码
    encoder.Start(venc_chn)
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    video_start_timestamp = 0
    get_first_I_frame = False

    try:
        while True:
            os.exitpoint()
            encoder.GetStream(venc_chn, streamData) # 获取一帧码流
            stream_type = streamData.stream_type[0]

            # Retrieve first IDR frame and write to MP4 file. Note: The first frame must be an IDR frame.
            if not get_first_I_frame:
                if stream_type == encoder.STREAM_TYPE_I:
                    get_first_I_frame = True
                    video_start_timestamp = streamData.pts[0]
                    save_idr[idr_index:idr_index+streamData.data_size[0]] = uctypes.bytearray_at(streamData.data[0], streamData.data_size[0])
                    idr_index += streamData.data_size[0]

                    frame_data.codec_id = video_payload_type
                    frame_data.data = uctypes.addressof(save_idr)
                    frame_data.data_length = idr_index
                    frame_data.time_stamp = streamData.pts[0] - video_start_timestamp

                    ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
                    if ret:
                        raise OSError("kd_mp4_write_frame failed.")
                    encoder.ReleaseStream(venc_chn, streamData)
                    continue

                elif stream_type == encoder.STREAM_TYPE_HEADER:
                    save_idr[idr_index:idr_index+streamData.data_size[0]] = uctypes.bytearray_at(streamData.data[0], streamData.data_size[0])
                    idr_index += streamData.data_size[0]
                    encoder.ReleaseStream(venc_chn, streamData)
                    continue
                else:
                    encoder.ReleaseStream(venc_chn, streamData) # 释放一帧码流
                    continue

            # Write video stream to MP4 file （not first idr frame）
            frame_data.codec_id = video_payload_type
            frame_data.data = streamData.data[0]
            frame_data.data_length = streamData.data_size[0]
            frame_data.time_stamp = streamData.pts[0] - video_start_timestamp

            print("video size: ", streamData.data_size[0], "video type: ", streamData.stream_type[0],"video timestamp:",frame_data.time_stamp)
            ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
            if ret:
                raise OSError("kd_mp4_write_frame failed.")

            encoder.ReleaseStream(venc_chn, streamData) # 释放一帧码流

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
    del link
    # 停止编码
    encoder.Stop(venc_chn)
    # 销毁编码器
    encoder.Destroy(venc_chn)
    # 清理buffer
    MediaManager.deinit()

    # mp4 muxer destroy
    kd_mp4_destroy_tracks(mp4_handle)
    kd_mp4_destroy(mp4_handle)

    print("venc_test stop")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_mp4_test("/sdcard/examples/test.mp4", 1280, 720)
```

### 5.3 例程 3

该实例用于演示如何调用 kd_mp4* API 来直接操作 MP4 模块，通过该例程，开发者可以解复用 MP4 文件，提取视频和音频流。

```python
# MP4 Demuxer Example
#
# This script demuxes an MP4 file, extracting video and audio streams.
# Supported video codecs: H.264, H.265
# Supported audio codecs: G.711A, G.711U

from media.media import *
from mpp.mp4_format import *
from mpp.mp4_format_struct import *
from media.pyaudio import *
import media.g711 as g711
from mpp.payload_struct import *
import media.vdecoder as vdecoder
from media.display import *
import uctypes
import time
import _thread
import os

def demuxer_mp4(filename):
    mp4_cfg = k_mp4_config_s()
    video_info = k_mp4_video_info_s()
    video_track = False
    audio_info = k_mp4_audio_info_s()
    audio_track = False
    mp4_handle = k_u64_ptr()

    mp4_cfg.config_type = K_MP4_CONFIG_DEMUXER
    mp4_cfg.muxer_config.file_name[:] = bytes(filename, 'utf-8')
    mp4_cfg.muxer_config.fmp4_flag = 0

    ret = kd_mp4_create(mp4_handle, mp4_cfg)
    if ret:
        raise OSError("kd_mp4_create failed:",filename)

    file_info = k_mp4_file_info_s()
    kd_mp4_get_file_info(mp4_handle.value, file_info)
    #print("=====file_info: track_num:",file_info.track_num,"duration:",file_info.duration)

    for i in range(file_info.track_num):
        track_info = k_mp4_track_info_s()
        ret = kd_mp4_get_track_by_index(mp4_handle.value, i, track_info)
        if (ret < 0):
            raise ValueError("kd_mp4_get_track_by_index failed")

        if (track_info.track_type == K_MP4_STREAM_VIDEO):
            if (track_info.video_info.codec_id == K_MP4_CODEC_ID_H264 or track_info.video_info.codec_id == K_MP4_CODEC_ID_H265):
                video_track = True
                video_info = track_info.video_info
                print("    codec_id: ", video_info.codec_id)
                print("    track_id: ", video_info.track_id)
                print("    width: ", video_info.width)
                print("    height: ", video_info.height)
            else:
                print("video not support codecid:",track_info.video_info.codec_id)
        elif (track_info.track_type == K_MP4_STREAM_AUDIO):
            if (track_info.audio_info.codec_id == K_MP4_CODEC_ID_G711A or track_info.audio_info.codec_id == K_MP4_CODEC_ID_G711U):
                audio_track = True
                audio_info = track_info.audio_info
                print("    codec_id: ", audio_info.codec_id)
                print("    track_id: ", audio_info.track_id)
                print("    channels: ", audio_info.channels)
                print("    sample_rate: ", audio_info.sample_rate)
                print("    bit_per_sample: ", audio_info.bit_per_sample)
                #audio_info.channels = 2
            else:
                print("audio not support codecid:",track_info.audio_info.codec_id)

    if (video_track == False):
        raise ValueError("video track not found")

    # 记录初始系统时间
    start_system_time = time.ticks_ms()
    # 记录初始视频时间戳
    start_video_timestamp = 0

    while (True):
        frame_data =  k_mp4_frame_data_s()
        ret = kd_mp4_get_frame(mp4_handle.value, frame_data)
        if (ret < 0):
            raise OSError("get frame data failed")

        if (frame_data.eof):
            break

        if (frame_data.codec_id == K_MP4_CODEC_ID_H264 or frame_data.codec_id == K_MP4_CODEC_ID_H265):
            data = uctypes.bytes_at(frame_data.data,frame_data.data_length)
            print("video frame_data.codec_id:",frame_data.codec_id,"data_length:",frame_data.data_length,"timestamp:",frame_data.time_stamp)

            # 计算视频时间戳经历的时长
            video_timestamp_elapsed = frame_data.time_stamp - start_video_timestamp
            # 计算系统时间戳经历的时长
            current_system_time = time.ticks_ms()
            system_time_elapsed = current_system_time - start_system_time

            # 如果系统时间戳经历的时长小于视频时间戳经历的时长，进行延时
            if system_time_elapsed < video_timestamp_elapsed:
                time.sleep_ms(video_timestamp_elapsed - system_time_elapsed)

        elif(frame_data.codec_id == K_MP4_CODEC_ID_G711A or frame_data.codec_id == K_MP4_CODEC_ID_G711U):
            data = uctypes.bytes_at(frame_data.data,frame_data.data_length)
            print("audio frame_data.codec_id:",frame_data.codec_id,"data_length:",frame_data.data_length,"timestamp:",frame_data.time_stamp)

    kd_mp4_destroy(mp4_handle.value)

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    demuxer_mp4("/sdcard/examples/test.mp4")
```
