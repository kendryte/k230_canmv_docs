# 3.7 `MP4` Module API Manual

## 1. Overview

This document provides a detailed introduction to the K230_CanMV MP4 module API's functionality and usage. The MP4 module is primarily used for generating MP4 files. Developers do not need to focus on the underlying implementation details; they can simply call the provided APIs to generate MP4 files with different encoding formats and video resolutions. This document will introduce both the MP4Container API and the kd_mp4* API, helping developers quickly get started and flexibly use these interfaces.

## 2. MP4Container API Introduction

The `MP4Container` class provides a convenient way to record camera footage and capture audio to generate MP4 files. This module simplifies the MP4 file processing workflow, making it suitable for application scenarios where there is no need to focus on the underlying implementation details.

### 2.1 MP4Container.Create

**Description**

Creates an instance of MP4Container.

**Syntax**

```python
MP4Container.Create(mp4Cfg)
```

**Parameters**

| Parameter Name | Description               | Input/Output |
|----------------|---------------------------|--------------|
| mp4Cfg         | Configuration for MP4Container | Input       |

**Return Values**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-0        | Failure     |

### 2.2 MP4Container.Start

**Description**

Starts the MP4Container to begin processing data.

**Syntax**

```python
MP4Container.Start()
```

**Parameters**

None

**Return Values**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-0        | Failure     |

### 2.3 MP4Container.Process

**Description**

Writes a frame of audio/video data to the MP4 file.

**Syntax**

```python
MP4Container.Process()
```

**Parameters**

None

**Return Values**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-0        | Failure     |

### 2.4 MP4Container.Stop

**Description**

Stops the MP4Container from processing data.

**Syntax**

```python
MP4Container.Stop()
```

**Parameters**

None

**Return Values**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-0        | Failure     |

### 2.5 MP4Container.Destroy

**Description**

Destroys the created MP4Container instance.

**Syntax**

```python
MP4Container.Destroy()
```

**Parameters**

None

**Return Values**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-0        | Failure     |

## 3. kd_mp4* API Introduction

This section provides a detailed description of the low-level function interfaces related to the MP4 module, which are used for more flexible control over the creation, writing, and reading of MP4 files. These interfaces are suitable for developers who need higher flexibility and control, allowing them to finely manage various aspects of MP4 files, including container creation, track management, data writing, and reading, and integrate with other modules to create a comprehensive solution.

### 3.1 kd_mp4_create

**Description**
Creates an MP4 container instance and initializes the configuration.

**Syntax**

```python
handle = k_u64_ptr()
ret = kd_mp4_create(handle, mp4_cfg)
```

**Parameters**
| Parameter Name | Description                        | Input/Output |
|----------------|------------------------------------|--------------|
| handle         | Output parameter, returns MP4 instance handle | Output       |
| config         | Pointer to MP4 container configuration structure | Input       |

**Return Values**
| Return Value | Description       |
|--------------|-------------------|
| 0            | Success           |
| Non-0        | Failure, see specific implementation for error codes |

### 3.2 kd_mp4_create_track

**Description**
Creates an audio/video track in the MP4 container.

**Syntax**

```python
track_handle = k_u64_ptr()
ret = kd_mp4_create_track(handle, track_handle, track_info)
```

**Parameters**
| Parameter Name | Description                        | Input/Output |
|----------------|------------------------------------|--------------|
| handle         | MP4 instance handle                | Input        |
| track_info     | Pointer to track information structure | Input        |

**Return Values**
| Return Value | Description       |
|--------------|-------------------|
| 0            | Success           |
| Non-0        | Failure           |

### 3.3 kd_mp4_destroy_tracks

**Description**
Destroys all created tracks in the MP4 container.

**Syntax**

```python
ret = kd_mp4_destroy_tracks(handle)
```

**Parameters**
| Parameter Name | Description          | Input/Output |
|----------------|----------------------|--------------|
| handle         | MP4 instance handle  | Input        |

**Return Values**
| Return Value | Description       |
|--------------|-------------------|
| 0            | Success           |
| Non-0        | Failure           |

### 3.4 kd_mp4_write_frame

**Description**
Writes a frame of audio/video data to the MP4 file.

**Syntax**

```python
ret = kd_mp4_write_frame(handle, track_id, frame_data)
```

**Parameters**
| Parameter Name | Description                        | Input/Output |
|----------------|------------------------------------|--------------|
| handle         | MP4 instance handle                | Input        |
| track_id       | ID of the target track             | Input        |
| frame_data     | Pointer to frame data structure    | Input        |

**Return Values**
| Return Value | Description       |
|--------------|-------------------|
| 0            | Success           |
| Non-0        | Failure           |

### 3.5 kd_mp4_get_file_info

**Description**
Gets global information of the MP4 file (e.g., total duration, number of tracks).

**Syntax**

```python
file_info = k_mp4_file_info_s()
ret = kd_mp4_get_file_info(handle, file_info)
```

**Parameters**
| Parameter Name | Description                        | Input/Output |
|----------------|------------------------------------|--------------|
| handle         | MP4 instance handle                | Input        |
| file_info      | Pointer to file information structure | Output       |

**Return Values**
| Return Value | Description       |
|--------------|-------------------|
| 0            | Success           |
| Non-0        | Failure           |

### 3.6 kd_mp4_get_track_by_index

**Description**
Gets detailed information of a specified track by index.

**Syntax**

```python
track_info = k_mp4_track_info_s()
ret = kd_mp4_get_track_by_index(handle, track_index, track_info)
```

**Parameters**
| Parameter Name | Description                        | Input/Output |
|----------------|------------------------------------|--------------|
| handle         | MP4 instance handle                | Input        |
| track_index    | Track index (starting from 0)      | Input        |
| track_info     | Pointer to track information structure | Output       |

**Return Values**
| Return Value | Description       |
|--------------|-------------------|
| 0            | Success           |
| Non-0        | Failure           |

### 3.7 kd_mp4_get_frame

**Description**
Reads a frame of audio/video data from the MP4 file.

**Syntax**

```python
ret = kd_mp4_get_frame(handle, frame_data)
```

**Parameters**
| Parameter Name | Description                        | Input/Output |
|----------------|------------------------------------|--------------|
| handle         | MP4 instance handle                | Input        |
| frame_data     | Pointer to frame data structure    | Output       |

**Return Values**
| Return Value | Description       |
|--------------|-------------------|
| 0            | Success           |
| Non-0        | Failure           |

- MP4Container.Create

### 4.3 MP4Container Type

**Description**

Enumeration of MP4Container types.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| MP4_CONFIG_TYPE_MUXER      | Muxer type                 |
| MP4_CONFIG_TYPE_DEMUXER    | Demuxer type, currently unsupported |

### 4.4 video_payload_type

**Description**

Video encoding types.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| MP4_CODEC_ID_H264          | H.264 video encoding type  |
| MP4_CODEC_ID_H265          | H.265 video encoding type  |

### 4.5 audio_payload_type

**Description**

Audio encoding types.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| MP4_CODEC_ID_G711U         | G.711U audio encoding type |
| MP4_CODEC_ID_G711A         | G.711A audio encoding type |

### 4.6 k_mp4_config_s

**Description**

Global configuration structure for MP4 container.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| config_type                | Container type (e.g., `K_MP4_CONFIG_MUXER`) |
| muxer_config               | Muxer configuration (file name, encoding format, etc.) |
| demuxer_config             | Demuxer configuration (currently unsupported) |

### 4.7 k_mp4_track_info_s

**Description**

Track information structure for creating audio/video tracks.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| track_type                 | Track type (e.g., `K_MP4_STREAM_VIDEO`) |
| time_scale                 | Time scale (unit: Hz)      |
| video_info                 | Video parameters (resolution, encoding format, etc.) |
| audio_info                 | Audio parameters (sampling rate, number of channels, etc.) |

### 4.8 k_mp4_frame_data_s

**Description**

Frame data structure for reading/writing audio/video frames.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| codec_id                   | Encoding type (e.g., `K_MP4_CODEC_ID_H264`) |
| time_stamp                 | Timestamp (unit: milliseconds) |
| data                       | Data pointer               |
| data_length                | Data length (bytes)        |
| eof                        | End-of-file flag (1 indicates the last frame) |

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
