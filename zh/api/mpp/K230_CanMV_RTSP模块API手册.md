# 3.9 RTSP 模块API手册

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

本文档主要介绍K230_CanMV RTSP模块API的使用。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 孙小朋      | 2024-07-16 |

## 1. 概述

本文档旨在介绍K230_CanMV RTSP模块API的使用方法和功能。RTSP模块是用于创建和管理RTSP服务器以及发送视频和音频数据的模块。

## 2. API描述

多媒体模块提供以下RTSP接口：

1. `multimedia.rtspserver_create`：创建RTSP服务器。
1. `multimedia.rtspserver_destroy`：销毁RTSP服务器。
1. `multimedia.rtspserver_init`：初始化RTSP服务器。
1. `multimedia.rtspserver_deinit`：反初始化RTSP服务器。
1. `multimedia.rtspserver_createsession`：创建RTSP会话。
1. `multimedia.rtspserver_destroysession`：销毁RTSP会话。
1. `multimedia.rtspserver_getrtspurl`：获取RTSP URL。
1. `multimedia.rtspserver_start`：启动RTSP服务器。
1. `multimedia.rtspserver_stop`：停止RTSP服务器。
1. `multimedia.rtspserver_sendvideodata`：向RTSP服务器发送视频数据。
1. `multimedia.rtspserver_sendaudiodata`：向RTSP服务器发送音频数据。

media.rtspserver模块提供以下RTSP接口：

1. `media.rtspserver.__init__`：初始化RTSP服务器。
1. `media.rtspserver.start`：启动RTSP服务器。
1. `media.rtspserver.stop`：停止RTSP服务器。
1. `media.rtspserver.get_rtsp_url`：获取RTSP URL。

这些接口可用于创建和管理RTSP服务器，创建和销毁RTSP会话，向服务器发送视频和音频数据，并获取用于流媒体的RTSP URL。

### 2.1 multimedia.rtspserver_create

【描述】

创建rtsp server.

【语法】

```python
rtspserver_create()
```

【参数】

无

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【举例】

无

【相关主题】

无

### 2.2 multimedia.rtspserver_destroy

【描述】

销毁rtsp server.

【语法】

```python
rtspserver_destroy()
```

【参数】

无

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【举例】

无

【相关主题】

无

### 2.3 multimedia.rtspserver_init

【描述】

初始化RTSP服务器。

【语法】

```python
rtspserver_init(port)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| port    | RTSP服务器端口号                      | 输入      |

【返回值】
无

【举例】

```python
rtspserver_init(8554)
```

【相关主题】

无

### 2.4 multimedia.rtspserver_deinit

【描述】

反初始化RTSP服务器。

【语法】

```python
rtspserver_deinit()
```

【参数】

无

【返回值】

无

【举例】

```python
rtspserver_deinit()
```

【相关主题】

无

### 2.5 multimedia.rtspserver_createsession

【描述】

创建RTSP会话。

【语法】

```python
rtspserver_createsession(session_name, video_type, enable_audio)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| session_name    | 会话名称                      | 输入      |
| video_type      | 视频类型                      | 输入      |
| enable_audio    | 是否启用音频                  | 输入      |

【返回值】

无

【举例】

```python
rtspserver_createsession("session1", "h264", True)
```

【相关主题】

无

### 2.6 multimedia.rtspserver_destroysession

【描述】

销毁RTSP会话。

【语法】

```python
rtspserver_destroysession(session_name)
```

【参数】

- `session_name`：会话名称。

【返回值】

无

【举例】

```python
rtspserver_destroysession("session1")
```

【相关主题】

无

### 2.7 multimedia.rtspserver_getrtspurl

【描述】

获取RTSP URL。

【语法】

```python
rtspserver_getrtspurl()
```

【参数】

无

【返回值】

| 参数名称 | 描述     | 输入/输出 |
| -------- | -------- | --------- |
| url      | RTSP URL | 输出    |

【举例】

```python
url = rtspserver_getrtspurl()
print(url)
```

【相关主题】

无

### 2.8 multimedia.rtspserver_start

【描述】

启动RTSP服务器。

【语法】

```python
rtspserver_start()
```

【参数】

无

【返回值】

无

【举例】

```python
rtspserver_start()
```

【相关主题】

无

### 2.9 multimedia.rtspserver_stop

【描述】

停止RTSP服务器。

【语法】

```python
rtspserver_stop()
```

【参数】

无

【返回值】

无

【举例】

```python
rtspserver_stop()
```

【相关主题】

无

### 2.10 multimedia.rtspserver_sendvideodata

【描述】

发送视频数据到RTSP服务器。

【语法】

```python
rtspserver_sendvideodata(session_name, data, size, timestamp)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| session_name    | 会话名称                      | 输入      |
| data            | 视频数据                      | 输入      |
| size            | 数据大小                      | 输入      |
| timestamp       | 时间戳                        | 输入      |

【返回值】

无

【举例】

```python
rtspserver_sendvideodata("session1", video_data, video_size, video_timestamp)
```

【相关主题】

无

### 2.11 multimedia.rtspserver_sendaudiodata

【描述】

发送音频数据到RTSP服务器。

【语法】

```python
rtspserver_sendaudiodata(session_name, data, size, timestamp)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| session_name    | 会话名称                      | 输入      |
| data            | 视频数据                      | 输入      |
| size            | 数据大小                      | 输入      |
| timestamp       | 时间戳                        | 输入      |

【返回值】

无

【举例】

```python
rtspserver_sendaudiodata("session1", audio_data, audio_size, audio_timestamp)
```

【相关主题】

无

### 2.12 media.rtspserver.\_\_init__

【描述】

初始化RTSP服务器。

【语法】

```python
rtspserver.__init__(session_name, port, enable_audio)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| session_name    | 会话名称                      | 输入      |
| port            | RTSP服务器端口号              | 输入      |
| enable_audio    | 是否启用音频                  | 输入      |

【返回值】

无

【举例】

```python
rtspserver = media.rtspserver(session_name="test", port=8554, enable_audio=False)
```

【相关主题】

无

### 2.13 media.rtspserver.start

【描述】

启动RTSP服务器。

【语法】

```python
rtspserver.start()
```

【参数】

无

【返回值】

无

【举例】

```python
rtspserver.start()
```

【相关主题】

无

### 2.14 media.rtspserver.stop

【描述】

停止RTSP服务器。

【语法】

```python
rtspserver.stop()
```

【参数】

无

【返回值】

无

【举例】

```python
rtspserver.stop()
```

【相关主题】

无

### 2.15 media.rtspserver.get_rtsp_url

【描述】

获取RTSP URL。

【语法】

```python
url = rtspserver.get_rtsp_url()
```

【参数】

无

【返回值】

| 参数名称 | 描述     | 输入/输出 |
| -------- | -------- | --------- |
| url      | RTSP URL | 输出    |

【举例】

```python
url = rtspserver.get_rtsp_url()
print(url)
```

【相关主题】

无

## 3. 示例程序

```python
# Description: This example demonstrates how to stream video and audio to the network using the RTSP server.
#
# Note: You will need an SD card to run this example.
#
# You can run the rtsp server to stream video and audio to the network

from time import *
from media.rtspserver import *   #导入rtsp server 模块
import os
import time

def rtsp_server_test():
    rtspserver = RtspServer(session_name="test",port=8554,enable_audio=False) #创建rtsp server对象
    rtspserver.start() #启动rtsp server
    print("rtsp server start:",rtspserver.get_rtsp_url()) #打印rtsp server start

    #运行30s
    time_start = time.time() #获取当前时间
    try:
        while(time.time() - time_start < 30):
            time.sleep(0.1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)

    rtspserver.stop() #停止rtsp server
    print("rtsp server stop") #打印rtsp server stop

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    rtsp_server_test()
    print("rtsp server done")
```
