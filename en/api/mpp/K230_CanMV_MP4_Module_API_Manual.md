# `MP4` Module API Manual

## Overview

This document provides a detailed introduction to the K230_CanMV MP4 module API's functionality and usage. The MP4 module is primarily used for generating MP4 files. Developers do not need to focus on the underlying implementation details; they can simply call the provided APIs to generate MP4 files with different encoding formats and video resolutions. This document will introduce both the MP4Container API and the kd_mp4* API, helping developers quickly get started and flexibly use these interfaces.

## MP4Container API Introduction

The `MP4Container` class provides a convenient way to record camera footage and capture audio to generate MP4 files. This module simplifies the MP4 file processing workflow, making it suitable for application scenarios where there is no need to focus on the underlying implementation details.

### MP4Container.Create

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
| None         |             |

### MP4Container.Start

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
| None         |             |

### MP4Container.Process

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
| None         |             |

### MP4Container.Stop

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
| None         |             |

### MP4Container.Destroy

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
| None         |             |

## kd_mp4* API Introduction

This section provides a detailed description of the low-level function interfaces related to the MP4 module, which are used for more flexible control over the creation, writing, and reading of MP4 files. These interfaces are suitable for developers who need higher flexibility and control, allowing them to finely manage various aspects of MP4 files, including container creation, track management, data writing, and reading, and integrate with other modules to create a comprehensive solution.

### kd_mp4_create

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
| handle         | Output parameter, return the pointer of the MP4 instance handle | Output       |
| config         | Pointer to MP4 container configuration structure | Input       |

**Return Values**

| Return Value | Description       |
|--------------|-------------------|
| 0            | Success           |
| Non-0        | Failure, see specific implementation for error codes |

### kd_mp4_create_track

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
|track_handle    | Output parameter, the handle pointer of the audio and video track instance | Output        |
| track_info     | Pointer to track information structure | Input        |

**Return Values**

| Return Value | Description       |
|--------------|-------------------|
| 0            | Success           |
| Non-0        | Failure           |

### kd_mp4_destroy_tracks

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

### kd_mp4_write_frame

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

### kd_mp4_get_file_info

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

### kd_mp4_get_track_by_index

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

### kd_mp4_get_frame

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

## Data Structure Description

### Mp4CfgStr

**Description**

The configuration properties of MP4Container.

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

| Member Name                | Description                |
|----------------------------|----------------------------|
| type      | Muxer type                 |
| muxerCfg    | Demuxer type, currently unsupported |

#### Relevant data types and interfaces

- MP4Container.Create

### MuxerCfgStr

**Description**

Configuration properties of the MP4Container muxer type.

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

| Member Name                | Description                |
|----------------------------|----------------------------|
| file_name             | The file name of the generated MP4     |
| video_payload_type    | Video coding format           |
| pic_width             | Video frame width             |
| pic_height            | Video frame height             |
| audio_payload_type    | Audio coding format           |
| video_start_timestamp | The timestamp of the video's start       |
| fmp4_flag             | The flag bit of fMP4 format       |

#### Relevant data types and interfaces

- MP4Container.Create

### MP4Container Type

**Description**

Enumeration of MP4Container types.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| MP4_CONFIG_TYPE_MUXER      | MP4Container type: muxer/demuxer,only muxer is supported   |
| MP4_CONFIG_TYPE_DEMUXER    | Demuxer type, currently unsupported |

### video_payload_type

**Description**

Video encoding types.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| MP4_CODEC_ID_H264          | H.264 video encoding type  |
| MP4_CODEC_ID_H265          | H.265 video encoding type  |

### audio_payload_type

**Description**

Audio encoding types.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| MP4_CODEC_ID_G711U         | G.711U audio encoding type |
| MP4_CODEC_ID_G711A         | G.711A audio encoding type |

### k_mp4_config_s

**Description**

Global configuration structure for MP4 container.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| config_type                | Container type (e.g., `K_MP4_CONFIG_MUXER`) |
| muxer_config               | Muxer configuration (file name, encoding format, etc.) |
| demuxer_config             | Demuxer configuration (currently unsupported) |

### k_mp4_track_info_s

**Description**

Track information structure for creating audio/video tracks.

**Members**

| Member Name                | Description                |
|----------------------------|----------------------------|
| track_type                 | Track type (e.g., `K_MP4_STREAM_VIDEO`) |
| time_scale                 | Time scale (unit: Hz)      |
| video_info                 | Video parameters (resolution, encoding format, etc.) |
| audio_info                 | Audio parameters (sampling rate, number of channels, etc.) |

### k_mp4_frame_data_s

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

## Example Programs

### Example 1

This example is used to demonstrate how to call the 'Mp4Container' class to generate an MP4 file. Through this routine, developers can record camera footage and capture sound to generate MP4 files. This example demonstrates how to create an 'Mp4Container' instance, configure MP4 file parameters, and start and stop the MP4 recording process. Suitable for developers who need to quickly get started with generating MP4 files.

```python
from media.mp4format import *
import os

def canmv_mp4_muxer_test():
    print("mp4_muxer_test start")
    width = 1280
    height = 720
    # Please set the width and height of the BPI development board to 640*360
    # width=640
    # height=360
    # Instantiate MP4 Container
    mp4_muxer = Mp4Container()
    mp4_cfg = Mp4CfgStr(mp4_muxer.MP4_CONFIG_TYPE_MUXER)
    if mp4_cfg.type == mp4_muxer.MP4_CONFIG_TYPE_MUXER:
        file_name = "/sdcard/examples/test.mp4"
        mp4_cfg.SetMuxerCfg(file_name, mp4_muxer.MP4_CODEC_ID_H265, width, height, mp4_muxer.MP4_CODEC_ID_G711U)
    # creat MP4 muxer
    mp4_muxer.Create(mp4_cfg)
    # start MP4 muxer
    mp4_muxer.Start()

    frame_count = 0
    try:
        while True:
            os.exitpoint()
            # Process audio and video data and write it into files in MP4 format
            mp4_muxer.Process()
            frame_count += 1
            print("frame_count = ", frame_count)
            if frame_count >= 200:
                break
    except BaseException as e:
        print(e)
    # stop MP4 muxer
    mp4_muxer.Stop()
    # destory MP4 muxer
    mp4_muxer.Destroy()
    print("mp4_muxer_test stop")

canmv_mp4_muxer_test()
```

### Example 2

This example is used to demonstrate how to call the kd_mp4* API to directly operate the MP4 module. Through this routine, developers can learn how to create MP4 containers, create audio and video tracks, write audio and video frame data, and destroy MP4 containers. This routine demonstrates a more low-level operation method and is suitable for developers who need to precisely control the MP4 file generation process.

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

    # sensor init
    sensor = Sensor()
    sensor.reset()
    # Set the camera output buffer
    # set chn0 output size
    sensor.set_framesize(width = width, height = height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)

    # Instantiate the video encoder
    encoder = Encoder()
    # Set the video encoder output buffer
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # Bind the camera and venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, venc_chn))

    # init media manager
    MediaManager.init()

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # Create an encoder
    encoder.Create(venc_chn, chnAttr)

    # Start encoder
    encoder.Start(venc_chn)
    # camera enable
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    video_start_timestamp = 0
    get_first_I_frame = False

    try:
        while True:
            os.exitpoint()
            encoder.GetStream(venc_chn, streamData) # Obtain a frame of code stream
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
                    encoder.ReleaseStream(venc_chn, streamData) # Release a frame of code stream
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

            encoder.ReleaseStream(venc_chn, streamData) # Release a frame of code stream

            frame_count += 1
            if frame_count >= 200:
                break
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        import sys
        sys.print_exception(e)

    # camera stop
    sensor.stop()
    # Destroy the binding between camera and venc
    del link
    # Stop coding
    encoder.Stop(venc_chn)
    # Destroy the encoder
    encoder.Destroy(venc_chn)
    # Clean the buffer
    MediaManager.deinit()

    # mp4 muxer destroy
    kd_mp4_destroy_tracks(mp4_handle)
    kd_mp4_destroy(mp4_handle)

    print("venc_test stop")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_mp4_test("/sdcard/examples/test.mp4", 1280, 720)
```

### Example 3

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

    # Record the initial system time
    start_system_time = time.ticks_ms()
    # Record the initial video timestamp
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

            # Calculate the duration of the video timestamp
            video_timestamp_elapsed = frame_data.time_stamp - start_video_timestamp
            # Calculate the duration experienced by the system timestamp
            current_system_time = time.ticks_ms()
            system_time_elapsed = current_system_time - start_system_time

            # If the duration experienced by the system timestamp is less than that experienced by the video timestamp, delay it
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
