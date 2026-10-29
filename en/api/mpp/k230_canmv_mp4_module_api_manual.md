# `MP4` Module API Manual

## Overview

This document provides a detailed introduction to the functionality and usage of the K230_CanMV MP4 module API. The MP4 module is primarily used to generate MP4 files. Developers do not need to focus on the underlying implementation details; they only need to call the provided APIs to generate MP4 files in different encoding formats and video resolutions. This document will introduce the MP4Container API and kd_mp4* API separately, helping developers get started quickly and flexibly use these interfaces.

## MP4Container API Introduction

The `MP4Container` class provides convenient methods to record camera footage and capture audio, generating MP4 files. This module simplifies the MP4 file processing workflow and is suitable for application scenarios that do not require attention to underlying implementation details.

### MP4Container.Create

**Description**

Used to create an MP4Container instance.

**Syntax**

```python
MP4Container.Create(mp4Cfg)
```

**Parameters**

| Parameter Name | Description              | Input/Output |
|-----------|---------------------------|-----------|
| mp4cfg    | MP4Container configuration | Input      |

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

### MP4Container.Start

**Description**

Starts MP4Container to begin processing data.

**Syntax**

```python
MP4Container.Start()
```

**Parameters**

None

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

### MP4Container.Process

**Description**

Writes a frame of audio/video data to the MP4 file.

**Syntax**

```python
MP4Container.Process()
```

**Parameters**

None

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

### MP4Container.Stop

**Description**

Stops the data processing of MP4Container.

**Syntax**

```python
MP4Container.Stop()
```

**Parameters**

None

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

### MP4Container.Destroy

**Description**

Destroys the created MP4Container instance.

**Syntax**

```python
MP4Container.Destroy()
```

**Parameters**

None

**Return Value**

| Return Value | Description    |
|--------|---------|
| None ||

## kd_mp4* API Introduction

This section describes in detail the low-level function interfaces related to the MP4 module, used for more flexible control over the creation, writing, and reading of MP4 files. These interfaces are suitable for developers who need higher flexibility and control, allowing them to finely control various aspects of MP4 files, including container creation, track management, data writing and reading, and other operations, and can be combined with other modules to generate a comprehensive solution.

### kd_mp4_create

**Description**
Creates an MP4 container instance and initializes the configuration.

**Syntax**

```python
handle = k_u64_ptr()
ret = kd_mp4_create(handle, mp4_cfg)
```

**Parameters**

| Parameter Name | Description              | Input/Output |
|-----------|-----------------------|-----------|
| handle    | Output parameter, returns a pointer to the MP4 instance handle | Output      |
| [config](#k_mp4_config_s)    | MP4 container configuration structure pointer | Input      |

**Return Value**

| Return Value  | Description       |
|---------|------------|
| 0       | Success       |
| Non-0    | Failure, see specific implementation for error codes |

### kd_mp4_create_track

**Description**
Creates an audio/video track in the MP4 container.

**Syntax**

```python
track_handle = k_u64_ptr()
ret = kd_mp4_create_track(handle, track_handle, track_info)
```

**Parameters**

| Parameter Name     | Description                  | Input/Output |
|--------------|-----------------------|-----------|
| handle       | MP4 instance handle         | Input      |
| track_handle       | Output parameter, pointer to the audio/video track instance handle         | Output      |
| [track_info](#k_mp4_track_info_s)   | Track information structure pointer    | Input      |

**Return Value**

| Return Value  | Description       |
|---------|------------|
| 0       | Success       |
| Non-0    | Failure       |

### kd_mp4_destroy_tracks

**Description**
Destroys all created tracks in the MP4 container.

**Syntax**

```python
ret = kd_mp4_destroy_tracks(handle)
```

**Parameters**

| Parameter Name  | Description          | Input/Output |
|-----------|---------------|-----------|
| handle    | MP4 instance handle | Input      |

**Return Value**

| Return Value  | Description       |
|---------|------------|
| 0       | Success       |
| Non-0    | Failure       |

---

### kd_mp4_write_frame

**Description**
Writes a frame of audio/video data to the MP4 file.

**Syntax**

```python
ret = kd_mp4_write_frame(handle, track_id, frame_data)
```

**Parameters**

| Parameter Name     | Description                  | Input/Output |
|--------------|-----------------------|-----------|
| handle       | MP4 instance handle         | Input      |
| track_id     | ID of the target track        | Input      |
| [frame_data](#k_mp4_frame_data_s)   | Frame data structure pointer      | Input      |

**Return Value**

| Return Value  | Description       |
|---------|------------|
| 0       | Success       |
| Non-0    | Failure       |

### kd_mp4_get_file_info

**Description**
Retrieves global information of the MP4 file (such as total duration, number of tracks).

**Syntax**

```python
file_info = k_mp4_file_info_s()
ret = kd_mp4_get_file_info(handle, file_info)
```

**Parameters**

| Parameter Name     | Description                  | Input/Output |
|--------------|-----------------------|-----------|
| handle       | MP4 instance handle         | Input      |
| file_info    | File information structure pointer    | Output      |

**Return Value**

| Return Value  | Description       |
|---------|------------|
| 0       | Success       |
| Non-0    | Failure       |

### kd_mp4_get_track_by_index

**Description**
Retrieves detailed information of a specified track by index.

**Syntax**

```python
track_info = k_mp4_track_info_s()
ret = kd_mp4_get_track_by_index(handle, track_index, track_info)
```

**Parameters**

| Parameter Name      | Description                  | Input/Output |
|---------------|-----------------------|-----------|
| handle        | MP4 instance handle         | Input      |
| track_index   | Track index (starting from 0)| Input      |
| track_info    | Track information structure pointer    | Output      |

**Return Value**

| Return Value  | Description       |
|---------|------------|
| 0       | Success       |
| Non-0    | Failure       |

---

### kd_mp4_get_frame

**Description**
Reads a frame of audio/video data from the MP4 file.

**Syntax**

```python
ret = kd_mp4_get_frame(handle, frame_data)
```

**Parameters**

| Parameter Name     | Description                  | Input/Output |
|--------------|-----------------------|-----------|
| handle       | MP4 instance handle         | Input      |
| frame_data   | Frame data structure pointer      | Output      |

**Return Value**

| Return Value  | Description       |
|---------|------------|
| 0       | Success       |
| Non-0    | Failure       |

## Data Structure Description

### Mp4CfgStr

**Description**

Configuration properties of MP4Container.

**Definition**

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

**Members**

| Member Name | Description                                                  |
|-------------|--------------------------------------------------------------|
| type        | MP4Container type: muxer/demuxer, currently only muxer is supported |
| muxerCfg    | muxer configuration                                          |

#### Related Data Types and Interfaces

- MP4Container.Create

### MuxerCfgStr

**Description**

Configuration properties for the MP4Container muxer type.

**Definition**

```python
class MuxerCfgStr:
    def __init__(self):
        self.file_name = 0
        self.video_payload_type = 0
        self.pic_width = 0
        self.pic_height = 0
        self.audio_payload_type = 0
        self.video_start_timestamp = 0
        self.fmp4_flag = 0
```

**Members**

| Member Name           | Description            |
|-----------------------|------------------------|
| file_name             | Generated MP4 file name |
| video_payload_type    | Video encoding format   |
| pic_width             | Video frame width       |
| pic_height            | Video frame height      |
| audio_payload_type    | Audio encoding format   |
| video_start_timestamp | Video start timestamp   |
| fmp4_flag             | fMP4 format flag        |

#### Related Data Types and Interfaces

- MP4Container.Create

### MP4Container Type

**Description**

MP4Container type enumeration.

**Members**

| Member Name                     | Description                                  |
|---------------------------------|----------------------------------------------|
| MP4_CONFIG_TYPE_MUXER           | muxer type                                   |
| MP4_CONFIG_TYPE_DEMUXER         | demuxer type, currently not supported        |

### video_payload_type

**Description**

Video encoding type.

**Members**

| Member Name                     | Description                                  |
|---------------------------------|----------------------------------------------|
| MP4_CODEC_ID_H264               | H.264 video encoding type                    |
| MP4_CODEC_ID_H265               | H.265 video encoding type                    |

### audio_payload_type

**Description**

Audio encoding type.

**Members**

| Member Name                     | Description                                  |
|---------------------------------|----------------------------------------------|
| MP4_CODEC_ID_G711U              | G.711U audio encoding type                   |
| MP4_CODEC_ID_G711A              | G.711A audio encoding type                   |

### k_mp4_config_s

**Description**
Global configuration structure for the MP4 container.

**Members**

| Member Name      | Description                                                  |
|------------------|--------------------------------------------------------------|
| config_type      | Container type (e.g., `K_MP4_CONFIG_MUXER`)                  |
| muxer_config     | Muxer configuration (file name, encoding format, etc.)       |
| demuxer_config   | Demuxer configuration (currently not supported)              |

---

### k_mp4_track_info_s

**Description**
Track information structure, used to create audio and video tracks.

**Members**

| Member Name      | Description                                                  |
|------------------|--------------------------------------------------------------|
| track_type       | Track type (e.g., `K_MP4_STREAM_VIDEO`)                      |
| time_scale       | Time base (unit: Hz)                                         |
| video_info       | Video parameters (resolution, encoding format, etc.)         |
| audio_info       | Audio parameters (sample rate, number of channels, etc.)     |

---

### k_mp4_frame_data_s

**Description**
Frame data structure, used to read and write audio and video frames.

**Members**

| Member Name      | Description                                                  |
|------------------|--------------------------------------------------------------|
| codec_id         | Encoding type (e.g., `K_MP4_CODEC_ID_H264`)                  |
| time_stamp       | Timestamp (unit: millisecond)                                |
| data             | Data pointer                                                 |
| data_length      | Data length (bytes)                                          |
| eof              | End flag (1 indicates the last frame)                        |

## Example Programs

### Example 1

This example demonstrates how to call the `Mp4Container` class to generate MP4 files. Through this example, developers can record camera footage and capture audio to generate MP4 files. The example shows how to create an `Mp4Container` instance, configure MP4 file parameters, and start and stop the MP4 recording process. It is suitable for developers who need to quickly get started with MP4 file generation.

```python
from media.mp4format import *
import os

def canmv_mp4_muxer_test():
    print("mp4_muxer_test start")
    width = 1280
    height = 720
    # For BPI development board, set width and height to 640*360
    # width=640
    # height=360
    # Instantiate MP4 Container
    mp4_muxer = Mp4Container()
    mp4_cfg = Mp4CfgStr(mp4_muxer.MP4_CONFIG_TYPE_MUXER)
    if mp4_cfg.type == mp4_muxer.MP4_CONFIG_TYPE_MUXER:
        file_name = "/sdcard/examples/test.mp4"
        mp4_cfg.SetMuxerCfg(file_name, mp4_muxer.MP4_CODEC_ID_H265, width, height, mp4_muxer.MP4_CODEC_ID_G711U)
    # Create MP4 muxer
    mp4_muxer.Create(mp4_cfg)
    # Start MP4 muxer
    mp4_muxer.Start()

    frame_count = 0
    try:
        while True:
            os.exitpoint()
            # Process audio and video data and write to file in MP4 format
            mp4_muxer.Process()
            frame_count += 1
            print("frame_count = ", frame_count)
            if frame_count >= 200:
                break
    except BaseException as e:
        print(e)
    # Stop MP4 muxer
    mp4_muxer.Stop()
    # Destroy MP4 muxer
    mp4_muxer.Destroy()
    print("mp4_muxer_test stop")

canmv_mp4_muxer_test()
```

### Example 2

This example demonstrates how to call the kd_mp4* API to directly operate the MP4 module. Through this example, developers can learn how to create an MP4 container, create audio and video tracks, write audio and video frame data, and destroy the MP4 container. This example shows a more low-level operation method and is suitable for developers who need fine-grained control over the MP4 file generation process.

```python
# Save MP4 file example
#
# Note: You need an SD card to run this example.
#
# You can capture audio and video and save it as MP4. The current version only supports MP4 format, with video supporting 264/265 and audio supporting g711a/g711u.

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

def vi_bind_venc_mp4_test(file_name,width=1280, height=720,venc_payload_type = K_PT_H264,fmp4_flag = False):
    print("venc_test start")
    width = ALIGN_UP(width, 16)

    frame_data = k_mp4_frame_data_s()
    save_idr = bytearray(width * height * 3 // 4)
    idr_index = 0

    # Initialize mp4 muxer
    mp4_handle = mp4_muxer_init(file_name, fmp4_flag)

    # Create video track
    if venc_payload_type == K_PT_H264:
        video_payload_type = K_MP4_CODEC_ID_H264
    elif venc_payload_type == K_PT_H265:
        video_payload_type = K_MP4_CODEC_ID_H265
    mp4_video_track_handle = mp4_muxer_create_video_track(mp4_handle, width, height, video_payload_type)

    # Initialize sensor
    sensor = Sensor()
    sensor.reset()
    # Set camera output buffer
    # set chn0 output size
    sensor.set_framesize(width = width, height = height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)

    # Instantiate video encoder
    encoder = Encoder()
    # Set video encoder output buffer
    encoder.SetOutBufs(8, width, height)

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # Create encoder
    encoder.Create(chnAttr)

    # Bind camera and venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, encoder.chn))

    # Start encoding
    encoder.Start()
    # Start camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    video_start_timestamp = 0
    get_first_I_frame = False

    try:
        while True:
            os.exitpoint()
            ret = encoder.GetStream(streamData,timeout = -1) # Get one or more frames of stream
            if ret != 0:
                continue

            # Retrieve the first IDR frame and write it to the MP4 file. Note: The first frame must be an IDR frame.
            if not get_first_I_frame:
                for pack_idx in range(0, streamData.pack_cnt):
                    stream_type = streamData.stream_type[pack_idx]
                    if stream_type == encoder.STREAM_TYPE_I:
                        get_first_I_frame = True
                        video_start_timestamp = streamData.pts[pack_idx]
                        save_idr[idr_index:idr_index+streamData.data_size[pack_idx]] = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                        idr_index += streamData.data_size[pack_idx]

                        frame_data.codec_id = video_payload_type
                        frame_data.data = uctypes.addressof(save_idr)
                        frame_data.data_length = idr_index
                        frame_data.time_stamp = streamData.pts[pack_idx] - video_start_timestamp

                        ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
                        if ret:
                            raise OSError("kd_mp4_write_frame failed.")

                        break

                    elif stream_type == encoder.STREAM_TYPE_HEADER:
                        save_idr[idr_index:idr_index+streamData.data_size[pack_idx]] = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                        idr_index += streamData.data_size[pack_idx]
                        continue
                    else:
                        continue

                encoder.ReleaseStream(streamData)
                continue

            # Write video stream to MP4 file (not the first IDR frame)
            for pack_idx in range(0, streamData.pack_cnt):
                frame_data.codec_id = video_payload_type
                frame_data.data = streamData.data[pack_idx]
                frame_data.data_length = streamData.data_size[pack_idx]
                frame_data.time_stamp = streamData.pts[pack_idx] - video_start_timestamp

                #print("video size: ", streamData.data_size[pack_idx], "video type: ", streamData.stream_type[pack_idx],"video timestamp:",frame_data.time_stamp)
                ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
                if ret:
                    raise OSError("kd_mp4_write_frame failed.")
                frame_count += 1

            encoder.ReleaseStream(streamData) # Release a frame of stream

            print("frame_count = ", frame_count)
            if frame_count >= 200:
                break
    except KeyboardInterrupt as e:
        import sys
        sys.print_exception(e)
    except BaseException as e:
        import sys
        sys.print_exception(e)

    # Stop camera
    sensor.stop()
    # Destroy the binding between camera and venc
    link.destroy()
    # Stop encoding
    encoder.Stop()
    # Destroy encoder
    encoder.Destroy()

    # mp4 muxer destroy
    kd_mp4_destroy_tracks(mp4_handle)
    kd_mp4_destroy(mp4_handle)

    print("record mp4 done")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_mp4_test("/data/test.mp4", 1280, 720)
```

### Example 3

This example demonstrates how to call the kd_mp4* API to directly operate the MP4 module. Through this example, developers can demux MP4 files and extract video and audio streams.

```python
# MP4 Demuxer example
#
# This script demuxes an MP4 file and extracts video and audio streams.
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

    # Record initial system time
    start_system_time = time.ticks_ms()
    # Record initial video timestamp
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

            # Calculate elapsed duration of video timestamp
            video_timestamp_elapsed = frame_data.time_stamp - start_video_timestamp
            # Calculate elapsed duration of system timestamp
            current_system_time = time.ticks_ms()
            system_time_elapsed = current_system_time - start_system_time

            # If the elapsed system timestamp is less than the elapsed video timestamp, delay
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
