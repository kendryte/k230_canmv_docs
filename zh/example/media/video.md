# 4. Video例程讲解

## 1. 概述

K230支持对视频流进行H264或H265编码，CanMV中提供API供用户使用，可进行MP4文件的录制与播放，还可以进行rtsp推流

## 2. 示例

### 2.1 MP4录制

本示例程序用于在 CanMV 开发板进行 mp4 muxer 的功能展示。

```python
# Save MP4 file example
#
# Note: You will need an SD card to run this example.
#
# You can capture audio and video and save them as MP4.The current version only supports MP4 format, video supports 264/265, and audio supports g711a/g711u.

from media.mp4format import *
import os

def mp4_muxer_test():
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

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    mp4_muxer_test()
```

```{admonition} 提示
具体接口定义请参考 [player](../../api/mpp/K230_CanMV_播放器模块API手册.md)
```

### 2.2 MP4播放

本示例程序用于对 CanMV 开发板进行一个 mp4 文件播放器的功能展示。

```python
# play mp4 file example
#
# Note: You will need an SD card to run this example.
#
# You can load local files to play. The current version only supports MP4 format, video supports 264/265, and audio supports g711a/g711u.

from media.player import * #导入播放器模块，用于播放mp4文件
import os

start_play = False #播放结束flag
def player_event(event,data):
    global start_play
    if(event == K_PLAYER_EVENT_EOF): #播放结束标识
        start_play = False #设置播放结束标识

def play_mp4_test(filename):
    global start_play
    player=Player() #创建播放器对象
    player.load(filename) #加载mp4文件
    player.set_event_callback(player_event) #设置播放器事件回调
    player.start() #开始播放
    start_play = True

    #等待播放结束
    try:
        while(start_play):
            time.sleep(0.1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)

    player.stop() #停止播放
    print("play over")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    play_mp4_test("/sdcard/app/tests/test.mp4")#播放mp4文件
```

```{admonition} 提示
具体接口定义请参考 [player](../../api/mpp/K230_CanMV_播放器模块API手册.md)
```

### 2.3 H264/H265编码

本示例程序用于在 CanMV 开发板进行 venc 视频编码的功能展示。

```python
# Video encode example
#
# Note: You will need an SD card to run this example.
#
# You can capture videos and encode them into 264 files

from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def venc_test():
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

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    venc_test()
```

```{admonition} 提示
具体接口定义请参考 [VENC](../../api/mpp/K230_CanMV_VENC模块API手册.md)
```

### 2.4 RTSP推流

这个示例演示了如何使用RTSP服务器将视频和音频流式传输到网络。

```python
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

```{admonition} 提示
具体接口定义请参考 [RTSP](../../api/mpp/K230_CanMV_RTSP模块API手册.md)
```
