# 3.7 `MP4` Module API Manual

## 1. Overview

This document provides a detailed introduction to the functions and usage of the K230_CanMV MP4 module API. The MP4 module is mainly used for generating MP4 files. Developers do not need to focus on the underlying implementation details; they only need to call the provided APIs to generate MP4 files in different encoding formats and video resolutions.

## 2. API Introduction

This module provides the `MP4Container` class, which includes the following methods:

### 2.1 MP4Container.Create

**Description**

Used to create an instance of MP4Container.

**Syntax**

```python
MP4Container.Create(mp4Cfg)
```

**Parameters**

| Parameter Name | Description                  | Input/Output |
|----------------|------------------------------|--------------|
| mp4cfg         | MP4Container configuration   | Input        |

**Return Values**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-zero     | Failure     |

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
| Non-zero     | Failure     |

### 2.3 MP4Container.Process

**Description**

Writes a frame of audio/video data into the MP4 file.

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
| Non-zero     | Failure     |

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
| Non-zero     | Failure     |

### 2.5 MP4Container.Destroy

**Description**

Destroys the created instance of MP4Container.

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
| Non-zero     | Failure     |

## 3. Data Structure Description

### 3.1 Mp4CfgStr

**Description**

Configuration properties for MP4Container.

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

| Member Name | Description                                      |
|-------------|--------------------------------------------------|
| type        | MP4Container type: muxer/demuxer, currently only supports muxer |
| muxerCfg    | Muxer configuration                              |

#### Related Data Types and Interfaces

- MP4Container.Create

### 3.2 MuxerCfgStr

**Description**

Configuration properties for MP4Container of muxer type.

**Definition**

```python
class MuxerCfgStr:
    def __init__(self):
        self.file_name = 0
        self.video_payload_type = 0
        self.pic_width = 0
        self.pic_height = 0
        self.audio_payload_type = 0
```

**Members**

| Member Name         | Description             |
|---------------------|-------------------------|
| file_name           | Generated MP4 file name |
| video_payload_type  | Video encoding format   |
| pic_width           | Video frame width       |
| pic_height          | Video frame height      |
| audio_payload_type  | Audio encoding format   |

#### Related Data Types and Interfaces

- MP4Container.Create

### 3.3 MP4Container Types

**Description**

Enumeration of MP4Container types.

**Members**

| Member Name               | Description                |
|---------------------------|----------------------------|
| MP4_CONFIG_TYPE_MUXER     | Muxer type                 |
| MP4_CONFIG_TYPE_DEMUXER   | Demuxer type, currently unsupported |

### 3.4 video_payload_type

**Description**

Video encoding types.

**Members**

| Member Name               | Description              |
|---------------------------|--------------------------|
| MP4_CODEC_ID_H264         | H.264 video encoding type|
| MP4_CODEC_ID_H265         | H.265 video encoding type|

### 3.5 audio_payload_type

**Description**

Audio encoding types.

**Members**

| Member Name               | Description              |
|---------------------------|--------------------------|
| MP4_CODEC_ID_G711U        | G.711U audio encoding type|
| MP4_CODEC_ID_G711A        | G.711A audio encoding type|

## 4. Example Program

### 4.1 Example 1

```python
from media.mp4format import *
import os

def canmv_mp4_muxer_test():
    print("mp4_muxer_test starts")
    width = 1280
    height = 720
    # For BPI development boards, set the width and height to 640*360
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
            # Process audio-video data and write to file in MP4 format
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
    print("mp4_muxer_test stops")

canmv_mp4_muxer_test()
```
