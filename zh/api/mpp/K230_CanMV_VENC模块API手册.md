# 3.6 VENC 模块API手册

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

本文档主要介绍K230_CanMV VENC模块API的使用。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| VENC  | Video Encoder   |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 郭玉会      | 2023-09-19 |

## 1. 概述

此文档介绍K230_CanMV VENC模块API，开发者可以通过调用提供的API编码得到不同分辨率、不同编码格式的码流，VENC作为编码模块需要和camera模块绑定使用。

## 2. API描述

提供Encoder类，该类提供如下方法：

### 2.1 Encoder.Create

【描述】

创建编码器

【语法】

```python
Encoder.Create(chn, chnAttr)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| chn  | 编码通道号            | 输入      |
| chnAttr | 编码通道属性 | 输入 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】
VENC最多支持4路编码，编码通道号取值范围[0, 3]，其中第4路固定用于 IDE 图像传输，除非不调用 compress_for_ide ，不然建议只使用 [0, 2]

【举例】

无

【相关主题】

无

### 2.2 Encoder.SetOutBufs

【描述】

设置编码器输出buffer

【语法】

```python
Encoder.SetOutBufs(chn, buf_num, width, height)
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---------|------|---------|
| chn | 编码通道号 | 输入 |
| buf_num | 输出buffer个数 | 输入 |
| width | 编码图像宽 | 输入 |
| height | 编码图像高 | 输入 |

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.3 Encoder.Start

【描述】

开始编码

【语法】

```python
Encoder.Start(chn)
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|----------|------|---------|
| chn | 编码通道号 | 输入 |

【返回值】

| 返回值 | 描述 |
|--------|-----|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.4 Encoder.GetStream

【描述】

获取一帧码流数据

【语法】

```python
Encoder.GetStream(chn, streamData)
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|----------|-----|----------|
| chn | 编码通道号 | 输入 |
| streamData | 编码码流结构 | 输出 |

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.5 Encoder.ReleaseStream

【描述】

释放一帧码流buffer

【语法】

```python
Encoder.ReleaseStream(chn, streamData)
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|----------|-----|----------|
| chn | 编码通道号 | 输入 |
| streamData | 编码码流结构 | 输入 |

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.6 Encoder.Stop

【描述】

停止编码

【语法】

```python
Encoder.Stop(chn)
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---------|------|----------|
| chn | 编码通道号 | 输入 |

【注意】

无

【举例】

无

### 2.7 Encoder.Destroy

【描述】

销毁编码器

【语法】

```python
Encoder.Destroy(chn)
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|----------|-----|----------|
| chn | 编码通道号 | 输入 |

【注意】

无

【举例】

无

## 3. 数据结构描述

### 3.1 ChnAttrStr

【说明】

编码通道属性

【定义】

```python
class ChnAttrStr:
    def __init__(self, payloadType, profile, picWidth, picHeight, gopLen = 30):
        self.payload_type = payloadType
        self.profile = profile
        self.pic_width = picWidth
        self.pic_height = picHeight
        self.gop_len = gopLen
```

【成员】

| 成员名称 | 描述 |
|---------|------|
| payload_type | 编码格式：h264/h265 |
| profile | 编码profile |
| pic_width | 图像宽 |
| pic_height | 图像高 |
| gop_len | 编码gop长度 |

【注意事项】

无

【相关数据类型及接口】

Encoder.Create

### 3.2 StreamData

【说明】

码流结构体

【定义】

```python
class StreamData:
    def __init__(self):
        self.data = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.data_size = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.stream_type = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.pack_cnt = 0
```

【成员】

| 成员名称 | 描述 |
|---------|------|
| data | 码流地址 |
| data_size | 码流大小 |
| stream_type | 帧类型 |
| pack_cnt | 码流结构体中pack的个数 |

【注意事项】

VENC_PACK_CNT_MAX是码流结构体中pack的最大个数，目前设置为12

【相关数据类型及接口】

Encoder.GetStream
Encoder.ReleaseStream

### 3.3 payload_type

【描述】

编码格式类型

【成员】

| 成员名称 | 描述 |
|---------|------|
| PAYLOAD_TYPE_H264 | h264编码格式 |
| PAYLOAD_TYPE_H265| h265编码格式 |

### 3.4 profile

【描述】

编码profile

【成员】

| 成员名称 | 描述 |
|----------|------|
| H264_PROFILE_BASELINE | h264 baseline profile |
| H264_PROFILE_MAIN | h264 main profile |
| H264_PROFILE_HIGH | h264 high profile |
| H265_PROFILE_MAIN | h265 main profile |

### 3.5 stream_type

【描述】

码流帧类型

【成员】

| 成员名称 | 描述 |
|---------|------|
| STREAM_TYPE_HEADER | 码流header |
| STREAM_TYPE_I | i帧 |
| STREAM_TYPE_P | p帧 |

## 4. 示例程序

### 4.1 例程1

```python
from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def canmv_venc_test():
    print("venc_test start")
    width = 1280
    height = 720
    venc_chn = VENC_CHN_ID_0
    width = ALIGN_UP(width, 16)
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
    encoder.SetOutBufs(venc_chn, 15, width, height)

    # 绑定camera和venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, venc_chn))

    # init media manager
    MediaManager.init()

    chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)
    streamData = StreamData()

    # 创建编码器
    encoder.Create(venc_chn, chnAttr)

    # 开始编码
    encoder.Start(venc_chn)
    # 启动camera
    sensor.run()

    frame_count = 0
    if chnAttr.payload_type == encoder.PAYLOAD_TYPE_H265:
        suffix = "265"
    elif chnAttr.payload_type == encoder.PAYLOAD_TYPE_H264:
        suffix = "264"
    else:
        suffix = "unkown"
        print("cam_venc_test, venc payload_type unsupport")

    out_file = f"/sdcard/app/tests/venc_chn_{venc_chn:02d}.{suffix}"
    print("save stream to file: ", out_file)

    with open(out_file, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                encoder.GetStream(venc_chn, streamData) # 获取一帧码流

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # 码流写文件
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(venc_chn, streamData) # 释放一帧码流

                frame_count += 1
                if frame_count >= 100:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
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
    print("venc_test stop")

canmv_venc_test()

```
