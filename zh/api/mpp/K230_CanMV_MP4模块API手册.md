# 3.7 MP4 模块API手册

![cover](../images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍K230_CanMV MP4模块API的使用

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| xxx  | xx   |
| XXX  | xx   |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 郭玉会      | 2023-09-19 |

## 1. 概述

此文档介绍K230_CanMV MP4模块API，MP4模块用来生成MP4文件，开发者不需要关注底层细节，只需要调用提供的API即可生成不同编码格式、不同视频分辨率的MP4文件。

## 2. API描述

提供MP4Container类，该类提供如下方法：

### 2.1 MP4Container.Create

【描述】

创建MP4Container

【语法】

```python
MP4Container.Create(mp4Cfg)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| mp4cfg  | MP4Contianer配置            | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】
无

【举例】

无

【相关主题】

无

### 2.2 MP4Container.Start

【描述】

MP4Container开始处理数据

【语法】

```python
MP4Container.Start()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|-------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.3 MP4Container.Process

【描述】

写入一帧音/视频数据到MP4

【语法】

```python
MP4Container.Process()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|-----|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.4 MP4Container.Stop

【描述】

MP4Container停止处理数据

【语法】

```python
MP4Container.Stop()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.5 MP4Container.Destroy

【描述】

销毁创建的MP4Container

【语法】

```python
MP4Container.Destroy()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

## 3. 数据结构描述

### 3.1 Mp4CfgStr

【说明】

MP4Container配置属性

【定义】

```python
class Mp4CfgStr:
    def __init__(self, type):
        self.type = type
        self.muxerCfg = MuxerCfgStr()

    def SetMuxerCfg(self, fileName, videoPayloadType, picWidth, picHeight, audioPayloadType, fmp4Flag = 0):
        self.muxerCfg.file_name = fileName
        self.muxerCfg.video_payload_type = videoPayloadType
        self.muxerCfg.pic_width = picWidth
        self.muxerCfg.pic_height = picHeight
        self.muxerCfg.audio_payload_type = audioPayloadType
        self.muxerCfg.fmp4_flag = fmp4Flag
```

【成员】

| 成员名称 | 描述 |
|---------|------|
| type | MP4Container类型：muxer/demuxer,目前只支持muxer |
| muxerCfg | muxer配置 |

【注意事项】

无

【相关数据类型及接口】

MP4Container.Create

### 3.2 MuxerCfgStr

【说明】

MP4Container Muxer类型配置属性

【定义】

```python
class MuxerCfgStr:
    def __init__(self):
        self.file_name = 0
        self.video_payload_type = 0
        self.pic_width = 0
        self.pic_height = 0
        self.audio_payload_type = 0
```

【成员】

| 成员名称 | 描述 |
|---------|------|
| filename | 生成的MP4文件名 |
| video_payload_type | 视频编码格式 |
| pic_width | 视频帧宽 |
| pic_height | 视频帧高 |
| audio_payload_type | 音频编码格式 |

【注意事项】

无

【相关数据类型及接口】

MP4Container.Create

### 3.3 MP4Container类型

【说明】

MP4Container类型枚举

【成员】

| 成员名称 | 描述 |
|---------|----|
| MP4_CONFIG_TYPE_MUXER | muxer类型 |
| MP4_CONFIG_TYPE_DEMUXER | demuxer类型，目前不支持 |

### 3.4 video_payload_type

【说明】

视频编码类型

【成员】

| 成员名称 | 描述 |
|--|--|
| MP4_CODEC_ID_H264 | h264视频编码类型 |
| MP4_CODEC_ID_H265 | h265视频编码类型 |

### 3.5 audio_payload_type

【说明】

音频编码类型

【成员】

| 成员名称 | 描述 |
|--|--|
| MP4_CODEC_ID_G711U | g711u音频编码类型 |
| MP4_CODEC_ID_G711A | g711a音频编码类型 |

## 4. 示例程序

### 4.1 例程1

```python

from media.mp4format import *
import os

def canmv_mp4_muxer_test():
    print("mp4_muxer_test start")
    width = 1280
    height = 720
    # 实例化mp4 container
    mp4_muxer = Mp4Container()
    mp4_cfg = Mp4CfgStr(mp4_muxer.MP4_CONFIG_TYPE_MUXER)
    if mp4_cfg.type == mp4_muxer.MP4_CONFIG_TYPE_MUXER:
        file_name = "/sdcard/app/tests/test.mp4"
        mp4_cfg.SetMuxerCfg(file_name, mp4_muxer.MP4_CODEC_ID_H265, width, height, mp4_muxer.MP4_CODEC_ID_G711U)
    # 创建mp4 muxer
    mp4_muxer.Create(mp4_cfg)
    # 启动mp4 muxer
    mp4_muxer.Start()

    frame_count = 0
    try:
        while True:
            os.exitpoint()
            # 处理音视频数据，按MP4格式写入文件
            mp4_muxer.Process()
            frame_count += 1
            print("frame_count = ", frame_count)
            if frame_count >= 200:
                break
    except BaseException as e:
        print(e)
    # 停止mp4 muxer
    mp4_muxer.Stop()
    # 销毁mp4 muxer
    mp4_muxer.Destroy()
    print("mp4_muxer_test stop")

canmv_mp4_muxer_test()
```
