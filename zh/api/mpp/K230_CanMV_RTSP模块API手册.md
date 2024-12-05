# 3.9 `RTSP` 模块 API 手册

## 1. 概述

本文档旨在详细介绍 K230_CanMV RTSP 模块 API 的使用方法和功能。 RTSP 模块专用于创建和管理 RTSP 服务器，支持视频和音频数据的发送与接收。

## 2. API 介绍

多媒体模块提供以下 RTSP 接口：

1. `multimedia.rtspserver_create`：创建 RTSP 服务器。
1. `multimedia.rtspserver_destroy`：销毁 RTSP 服务器。
1. `multimedia.rtspserver_init`：初始化 RTSP 服务器。
1. `multimedia.rtspserver_deinit`：反初始化 RTSP 服务器。
1. `multimedia.rtspserver_createsession`：创建 RTSP 会话。
1. `multimedia.rtspserver_destroysession`：销毁 RTSP 会话。
1. `multimedia.rtspserver_getrtspurl`：获取 RTSP URL。
1. `multimedia.rtspserver_start`：启动 RTSP 服务器。
1. `multimedia.rtspserver_stop`：停止 RTSP 服务器。
1. `multimedia.rtspserver_sendvideodata`：向 RTSP 服务器发送视频数据。
1. `multimedia.rtspserver_sendaudiodata`：向 RTSP 服务器发送音频数据。

这些接口可以用于创建和管理 RTSP 服务器、创建和销毁 RTSP 会话、向服务器发送视频和音频数据，以及获取用于流媒体的 RTSP URL。

### 2.1 multimedia.rtspserver_create

**描述**
用于创建 RTSP 服务器。

**语法**  

```python
rtspserver_create()
```

**参数**

无

**返回值**  

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 创建成功                        |
| 非 0    | 创建失败                        |

### 2.2 multimedia.rtspserver_destroy

**描述**
用于销毁 RTSP 服务器。

**语法**  

```python
rtspserver_destroy()
```

**参数**

无

**返回值**  

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 销毁成功                        |
| 非 0    | 销毁失败                        |

### 2.3 multimedia.rtspserver_init

**描述**
初始化 RTSP 服务器。

**语法**  

```python
rtspserver_init(port)
```

**参数**  

| 参数名称        | 描述                          | 输入 / 输出 |
|-----------------|-------------------------------|-----------|
| port            | RTSP 服务器监听端口号        | 输入      |

**返回值**
无

**示例**  

```python
rtspserver_init(8554)
```

### 2.4 multimedia.rtspserver_deinit

**描述**
反初始化 RTSP 服务器。

**语法**  

```python
rtspserver_deinit()
```

**参数**

无

**返回值**
无

**示例**  

```python
rtspserver_deinit()
```

### 2.5 multimedia.rtspserver_createsession

**描述**
创建 RTSP 会话。

**语法**  

```python
rtspserver_createsession(session_name, video_type, enable_audio)
```

**参数**  

| 参数名称        | 描述                          | 输入 / 输出 |
|-----------------|-------------------------------|-----------|
| session_name    | 会话名称                      | 输入      |
| video_type      | 视频编码类型                  | 输入      |
| enable_audio    | 是否启用音频                  | 输入      |

**返回值**
无

**示例**  

```python
rtspserver_createsession("session1", "h264", True)
```

### 2.6 multimedia.rtspserver_destroysession

**描述**
销毁 RTSP 会话。

**语法**  

```python
rtspserver_destroysession(session_name)
```

**参数**  

- `session_name`：会话名称。

**返回值**
无

**示例**  

```python
rtspserver_destroysession("session1")
```

### 2.7 multimedia.rtspserver_getrtspurl

**描述**
获取 RTSP URL。

**语法**  

```python
rtspserver_getrtspurl()
```

**参数**

无

**返回值**  

| 参数名称 | 描述     | 输入 / 输出 |
|----------|----------|-----------|
| url      | RTSP URL | 输出      |

**示例**  

```python
url = rtspserver_getrtspurl()
print(url)
```

### 2.8 multimedia.rtspserver_start

**描述**
启动 RTSP 服务器。

**语法**  

```python
rtspserver_start()
```

**参数**

无

**返回值**
无

**示例**  

```python
rtspserver_start()
```

### 2.9 multimedia.rtspserver_stop

**描述**
停止 RTSP 服务器。

**语法**  

```python
rtspserver_stop()
```

**参数**

无

**返回值**
无

**示例**  

```python
rtspserver_stop()
```

### 2.10 multimedia.rtspserver_sendvideodata

**描述**
向 RTSP 服务器发送视频数据。

**语法**  

```python
rtspserver_sendvideodata(session_name, data, size, timestamp)
```

**参数**  

| 参数名称        | 描述                          | 输入 / 输出 |
|-----------------|-------------------------------|-----------|
| session_name    | 会话名称                      | 输入      |
| data            | 视频数据                      | 输入      |
| size            | 数据大小                      | 输入      |
| timestamp       | 时间戳                        | 输入      |

**返回值**
无

**示例**  

```python
rtspserver_sendvideodata("session1", video_data, video_size, video_timestamp)
```

### 2.11 multimedia.rtspserver_sendaudiodata

**描述**
向 RTSP 服务器发送音频数据。

**语法**  

```python
rtspserver_sendaudiodata(session_name, data, size, timestamp)
```

**参数**  

| 参数名称        | 描述                          | 输入 / 输出 |
|-----------------|-------------------------------|-----------|
| session_name    | 会话名称                      | 输入      |
| data            | 音频数据                      | 输入      |
| size            | 数据大小                      | 输入      |
| timestamp       | 时间戳                        | 输入      |

**返回值**
无

**示例**  

```python
rtspserver_sendaudiodata("session1", audio_data, audio_size, audio_timestamp)
```

## 3. 示例程序

```python
# 示例：演示如何通过 RTSP 服务器向网络流媒体发送视频和音频数据。
# 注意：运行该示例需要 SD 卡。
# 可以启动 RTSP 服务器以进行视频和音频流媒体传输。

from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os
import _thread
import multimedia as mm
from time import *

class RtspServer:
    def __init__(self, session_name="test", port=8554, video_type=mm.multi_media_type.media_h264, enable_audio=False):
        self.session_name = session_name  # 会话名称
        self.video_type = video_type        # 视频编码类型（ H264/H265 ）
        self.enable_audio = enable_audio    # 是否启用音频
        self.port = port                    # RTSP 服务器端口号
        self.rtspserver = mm.rtsp_server()  # 实例化 RTSP 服务器
        self.venc_chn = VENC_CHN_ID_0       # 视频编码通道
        self.start_stream = False            # 是否启动推流线程
        self.runthread_over = False          # 推流线程是否结束

    def start(self):
        # 初始化推流
        self._init_stream()
        self.rtspserver.rtspserver_init(self.port)
        # 创建会话
        self.rtspserver.rtspserver_createsession(self.session_name, self.video_type, self.enable_audio)
        # 启动 RTSP 服务器
        self.rtspserver.rtspserver_start()
        self._start_stream()

        # 启动推流线程
        self.start_stream = True
        _thread.start_new_thread(self._do_rtsp_stream, ())

    def stop(self):
        if not self.start_stream:
            return
        # 等待推流线程退出
        self.start_stream = False
        while not self.runthread_over:
            sleep(0.1)
        self.runthread_over = False

        # 停止推流
        self._stop_stream()
        self.rtspserver.rtspserver_stop()
        self.rtspserver.rtspserver_deinit()

    def get_rtsp_url(self):
        return self.rtspserver.rtspserver_getrtspurl(self.session_name)

    def _init_stream(self):
        width = 1280
        height = 720
        width = ALIGN_UP(width, 16)
        # 初始化传感器
        self.sensor = Sensor()
        self.sensor.reset()
        self.sensor.set_framesize(width=width, height=height, alignment=12)
        self.sensor.set_pixformat(Sensor.YUV420SP)
        # 实例化 video encoder
        self.encoder = Encoder()
        self.encoder.SetOutBufs(self.venc_chn, 8, width, height)
        # 绑定 camera 和 venc
        self.link = MediaManager.link(self.sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, self.venc_chn))
        # init media manager
        MediaManager.init()
        # 创建编码器
        chnAttr = ChnAttrStr(self.encoder.PAYLOAD_TYPE_H264, self.encoder.H264_PROFILE_MAIN, width, height)
        self.encoder.Create(self.venc_chn, chnAttr)

    def _start_stream(self):
        # 开始编码
        self.encoder.Start(self.venc_chn)
        # 启动 camera
        self.sensor.run()

    def _stop_stream(self):
        # 停止 camera
        self.sensor.stop()
        # 接绑定 camera 和 venc
        del self.link
        # 停止编码
        self.encoder.Stop(self.venc_chn)
        self.encoder.Destroy(self.venc_chn)
        # 清理 buffer
        MediaManager.deinit()

    def _do_rtsp_stream(self):
        try:
            streamData = StreamData()
            while self.start_stream:
                os.exitpoint()
                # 获取一帧码流
                self.encoder.GetStream(self.venc_chn, streamData)
                # 推流
                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = bytes(uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx]))
                    self.rtspserver.rtspserver_sendvideodata(self.session_name,stream_data, streamData.data_size[pack_idx],1000)
                    #print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])
                # 释放一帧码流
                self.encoder.ReleaseStream(self.venc_chn, streamData)

        except BaseException as e:
            print(f"Exception {e}")
        finally:
            self.runthread_over = True
            # 停止 rtsp server
            self.stop()

        self.runthread_over = True

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    # 创建 rtsp server 对象
    rtspserver = RtspServer()
    # 启动 rtsp server
    rtspserver.start()
    # 打印 rtsp url
    print("rtsp server start:",rtspserver.get_rtsp_url())
    # 推流 60s
    sleep(60)
    # 停止 rtsp server
    rtspserver.stop()
    print("done")

```
