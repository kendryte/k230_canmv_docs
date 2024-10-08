# 3.7 MP4 模块 API 手册

## 1. 概述

本文详细介绍了 K230_CanMV MP4 模块 API 的功能与使用方法。MP4 模块主要用于生成 MP4 文件，开发者无需关注底层实现细节，只需调用所提供的 API 即可生成不同编码格式和视频分辨率的 MP4 文件。

## 2. API 介绍

该模块提供了 `MP4Container` 类，包含以下方法：

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

## 3. 数据结构描述

### 3.1 Mp4CfgStr

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

### 3.2 MuxerCfgStr

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

### 3.3 MP4Container 类型

**说明**  

MP4Container 类型枚举。

**成员**  

| 成员名称                        | 描述                     |
|---------------------------------|--------------------------|
| MP4_CONFIG_TYPE_MUXER          | muxer 类型               |
| MP4_CONFIG_TYPE_DEMUXER        | demuxer 类型，目前不支持 |

### 3.4 video_payload_type

**说明**  

视频编码类型。

**成员**  

| 成员名称                     | 描述                       |
|------------------------------|----------------------------|
| MP4_CODEC_ID_H264            | H.264 视频编码类型        |
| MP4_CODEC_ID_H265            | H.265 视频编码类型        |

### 3.5 audio_payload_type

**说明**  

音频编码类型。

**成员**  

| 成员名称                     | 描述                       |
|------------------------------|----------------------------|
| MP4_CODEC_ID_G711U           | G.711U 音频编码类型       |
| MP4_CODEC_ID_G711A           | G.711A 音频编码类型       |

## 4. 示例程序

### 4.1 例程 1

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
