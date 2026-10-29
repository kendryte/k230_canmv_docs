# Video例程讲解

## 概述

K230 支持对视频流进行 H264 或 H265 编码，CanMV 中提供的 API 使用户能够进行 MP4 文件的录制与播放，同时支持 RTSP 推流。

## 示例

### MP4录制

本示例程序展示了如何在 CanMV 开发板上进行 MP4 文件的录制。
您可以使用 `Mp4Container` 类来实现摄像头音视频数据的录制，具体实现可以参考 `mp4_muxer_test` 函数。该方法封装较为简单，适合快速上手。
如果您需要更灵活的控制，可以使用 `kd_mp4_*` 系列函数来完成 H264/H265 编码视频的 MP4 封装。这些函数提供了更细粒度的控制，适合高级用户进行定制化开发，具体实现可以参考 `vi_bind_venc_mp4_test` 函数。

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
        file_name = "/sdcard/examples/test.mp4"
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

```python
# Save MP4 file example
#
# Note: You will need an SD card to run this example.
#
# You can capture audio and video and save them as MP4.
from media.mp4format import *
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

    # mp4 muxer init
    mp4_handle = mp4_muxer_init(file_name, fmp4_flag)

    # create video track
    if venc_payload_type == K_PT_H264:
        video_payload_type = K_MP4_CODEC_ID_H264
    elif venc_payload_type == K_PT_H265:
        video_payload_type = K_MP4_CODEC_ID_H265
    mp4_video_track_handle = mp4_muxer_create_video_track(mp4_handle, width, height, video_payload_type)

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
    encoder.SetOutBufs(8, width, height)

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(chnAttr)

    # 绑定camera和venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, encoder.chn))

    # 开始编码
    encoder.Start()
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    video_start_timestamp = 0
    get_first_I_frame = False

    try:
        while True:
            os.exitpoint()
            ret = encoder.GetStream(streamData,timeout = -1) # 获取一帧或多帧码流
            if ret != 0:
                continue

            # Retrieve first IDR frame and write to MP4 file. Note: The first frame must be an IDR frame.
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

            # Write video stream to MP4 file （not first idr frame）
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

            encoder.ReleaseStream(streamData) # 释放一帧码流

            print("frame_count = ", frame_count)
            if frame_count >= 200:
                break
    except KeyboardInterrupt as e:
        import sys
        sys.print_exception(e)
    except BaseException as e:
        import sys
        sys.print_exception(e)

    # 停止camera
    sensor.stop()
    # 销毁camera和venc的绑定
    link.destroy()
    # 停止编码
    encoder.Stop()
    # 销毁编码器
    encoder.Destroy()

    # mp4 muxer destroy
    kd_mp4_destroy_tracks(mp4_handle)
    kd_mp4_destroy(mp4_handle)

    print("record mp4 done")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_mp4_test("/data/test.mp4", 1280, 720)
```

```{admonition} 提示
具体接口定义请参考 [mp4muxer](../../api/mpp/k230_canmv_mp4_module_api_manual.md)
```

### MP4解复用

本示例程序展示了如何在 CanMV 开发板上使用 MP4 解复用器来解析 MP4 文件，并提取其中的视频和音频流。

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

            # 计算视频时间戳经历的时长(time_stamp 单位为微秒，转换为毫秒)
            video_timestamp_elapsed = (frame_data.time_stamp - start_video_timestamp) // 1000
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

```{admonition} 提示
具体接口定义请参考 [mp4demuxer](../../api/mpp/k230_canmv_mp4_module_api_manual.md)
```

### MP4播放

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
    # player=Player() #创建播放器对象
    # 使用IDE作为输出显示，可以设定任意分辨率
    player=Player(Display.VIRT)
    # 使用ST7701 LCD屏幕作为输出显示，最大分辨率800*480
    # player=Player(Display.ST7701)
    # 使用HDMI作为输出显示
    # player=Player(Display.LT9611)
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
    play_mp4_test("/sdcard/examples/test.mp4")#播放mp4文件
```

```{admonition} 提示
具体接口定义请参考 [player](../../api/mpp/k230_canmv_player_module_api_manual.md)
```

### H264/H265编码

本示例程序用于在 CanMV 开发板进行 venc 视频编码的功能展示。

```python
# Video encode example
#
# Note: You will need an SD card to run this example.
#
# You can capture videos and encode them into 264/265 files

from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def vi_bind_venc_test(file_name,width=1280, height=720):
    print("venc_test start")
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # 判断文件类型
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

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
    encoder.SetOutBufs(8, width, height)

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(chnAttr)

    # 绑定camera和venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, encoder.chn))

    # 开始编码
    encoder.Start()
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                encoder.GetStream(streamData) # 获取一帧码流

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # 码流写文件
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(streamData) # 释放一帧码流

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # 停止camera
    sensor.stop()
    # 销毁camera和venc的绑定
    link.destroy()
    # 停止编码
    encoder.Stop()
    # 销毁编码器
    encoder.Destroy()
    print("venc_test stop")

def stream_venc_test(file_name,width=1280, height=720):
    print("venc_test start")
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # 判断文件类型
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

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
    encoder.SetOutBufs(8, width, height)

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(chnAttr)

    # 开始编码
    encoder.Start()
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    yuv420sp_img = None
    frame_info = k_video_frame_info()
    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                frame_info  = sensor.snapshot(chn=CAM_CHN_ID_0,dump_frame=True)
                #frame_info.v_frame.nv12_to_grayscale() # convert to grayscale
                encoder.SendFrame(frame_info)
                encoder.GetStream(streamData) # 获取一帧码流

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # 码流写文件
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(streamData) # 释放一帧码流

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # 停止camera
    sensor.stop()
    # 停止编码
    encoder.Stop()
    # 销毁编码器
    encoder.Destroy()
    print("venc_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_test("/data/test.264",800,480)  # vi绑定venc示例
    #stream_venc_test("/data/test.264",800,480)  # venc编码数据流示例
```

```{admonition} 提示
具体接口定义请参考 [VENC](../../api/mpp/k230_canmv_venc_module_api_manual.md)
```

### H264/H265解码

本示例程序用于在 CanMV 开发板进行 vdec 视频解码的功能展示。

```python
# Video encode example
#
# Note: You will need an SD card to run this example.
#
# You can decode 264/265 and display them on the screen

from media.media import *
from mpp.payload_struct import *
import media.vdecoder as vdecoder
from media.display import *

import time, os

STREAM_SIZE = 40960
def vdec_test(file_name,width=1280,height=720):
    print("vdec_test start")
    vdec_chn = VENC_CHN_ID_0
    vdec_width =  ALIGN_UP(width, 16)
    vdec_height = height
    vdec = None
    vdec_payload_type = K_PT_H264

    #display_type = Display.VIRT
    display_type = Display.ST7701 #使用ST7701 LCD屏作为输出显示，最大分辨率800*480
    #display_type = Display.LT9611 #使用HDMI作为输出显示

    # 判断文件类型
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        vdec_payload_type = K_PT_H264
    elif suffix == '265':
        vdec_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # 实例化video decoder
    #vdecoder.Decoder.vb_pool_config(4,6)
    vdec = vdecoder.Decoder(vdec_payload_type)

    # 初始化display
    if (display_type == Display.VIRT):
        Display.init(display_type,width = vdec_width, height = vdec_height,fps=30)
    else:
        Display.init(display_type,to_ide = True)

    #vb buffer初始化
    MediaManager.init()

    # 创建video decoder
    vdec.create()

    # vdec bind display
    bind_info = vdec.bind_info(width=vdec_width,height=vdec_height,chn=vdec.get_vdec_channel())
    Display.bind_layer(**bind_info, layer = Display.LAYER_VIDEO1)

    vdec.start()
    # 打开文件
    with open(file_name, "rb") as fi:
        while True:
            os.exitpoint()
            # 读取视频数据流
            data = fi.read(STREAM_SIZE)
            if not data:
                break
            # 解码数据流
            vdec.decode(data)

    # 停止video decoder
    vdec.stop()
    # 销毁video decoder
    vdec.destroy()
    time.sleep(1)

    # 关闭display
    Display.deinit()
    # 释放vb buffer
    MediaManager.deinit()

    print("vdec_test stop")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vdec_test("/sdcard/examples/test.264",800,480) #解码264/265视频文件
```

```{admonition} 提示
具体接口定义请参考 [VDEC](../../api/mpp/k230_canmv_vdec_module_api_manual.md)
```

### RTSP推流

示例脚本在开发板固件中的路径为 `/sdcard/examples/02-Media/rtsp_server.py`，SDK
源码路径为 `src/canmv/resources/examples/02-Media/rtsp_server.py`。它通过
`RtspServer` 建立 `Sensor -> VENC -> RTSP` 视频链路。默认使用 H.265、
`1280 x 720`、`512 Kbit/s`，且不启用音频，以降低编码和网络负载。

在脚本开头可配置以下项目：

| 配置项 | 说明 | 默认值 |
| :-- | :-- | :-- |
| `NETWORK_TYPE` | `"default"`、`"lan"`、`"wifi_sta"` 或 `"wifi_ap"` | `"wifi_sta"` |
| `WLAN_DEVICE` | `"auto"`、`"usb"`、`"sdio"` 或 `"spi"` | `"auto"` |
| `NETWORK_TIMEOUT` | 等待网络地址的超时时间，单位秒 | `15` |
| `VIDEO_TYPE` | H.265 或 H.264 | H.265 |
| `ENABLE_AUDIO` | 是否在 RTSP Session 中声明音频 | `False` |
| `VIDEO_WIDTH` / `VIDEO_HEIGHT` | 编码分辨率 | `1280` / `720` |
| `VIDEO_BIT_RATE` | VENC 目标码率，单位 Kbit/s | `512` |
| `VIDEO_GOP` | GOP 帧数 | `30` |

修改网络类型、Wi-Fi 设备类型和凭据后运行脚本。脚本通过 `libs.Network` 选择
动态注册的网络接口、获取 IP 并输出类似结果：

```text
RTSP server started: rtsp://192.168.1.108:8554/test (H265, 512 Kbit/s, audio disabled)
```

使用 VLC 等 RTSP 客户端打开该 URL。H.265 在低码率下通常更省带宽；客户端不支持 H.265 时，将 `VIDEO_TYPE` 改为 `mm.multi_media_type.media_h264`。仅将 `ENABLE_AUDIO` 设为 `True` 不会自动建立音频采集和编码链路，示例仍只发送视频。

关闭脚本前应先断开所有 RTSP 客户端，然后调用 `stop()` 释放编码器、摄像头和 RTSP 服务。

```{admonition} 提示
具体接口、网络准备和性能配置请参考 [RTSP](../../api/mpp/k230_canmv_rtsp_module_api_manual.md)。
```

### RTSP推流（客户端模式）

示例脚本在开发板固件中的路径为 `/sdcard/examples/02-Media/rtsp_pusher.py`，SDK
源码路径为 `src/canmv/resources/examples/02-Media/rtsp_pusher.py`。与
`rtsp_server.py`（内置 RTSP 服务器，等待客户端连接）不同，`rtsp_pusher.py`
以客户端身份主动连接到外部 RTSP 服务器（如 EasyDarwin、mediamtx、ZLMediaKit），
并将编码后的 H.264 视频推送过去。

```python
# Description: This example demonstrates how to push encoded video to a remote RTSP server.
#
# Note: You will need an SD card to run this example.
#
# Unlike rtsp_server.py (which hosts the stream), the rtsp_pusher connects as a
# client to an external RTSP server URL and pushes H.264 video to it.
#
# Reference C++ sample: src/rtsmart/examples/mpp/sample_rtsppusher/main.cpp
#
# H.264 video at 512 Kbit/s is the default. Audio is not supported by the pusher.
#
# Flow (mirrors the C++ sample, which drives pushing from the encoder thread via
# OnVEncData; Python has no encoder callback, so we poll GetStream in the main
# thread instead of spawning a worker thread -- this avoids thread-creation
# failures on memory-constrained devices):
#   1. start the encoder so it begins producing SPS/PPS (K_VENC_HEADER)
#   2. on the first HEADER pack: rtsppusher_init() (deferred until the encoder is
#      producing so the pusher's frame queue does not starve the media pipeline on
#      startup); cache the SPS/PPS bytes, do not open yet
#   3. on every I frame: rtsppusher_pushvideoheader() with the latest cached SPS/PPS,
#      then (first time only) rtsppusher_open() -- pushing the header again before
#      each I frame keeps it in sync in case the encoder re-emits SPS/PPS mid-stream;
#      the underlying implementation prefixes this header to every subsequently
#      pushed frame (I and P) until it is updated again
#   4. push I/P frames with rtsppusher_pushvideodata(data, size, key_frame, timestamp)

from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os
import multimedia as mm
from libs.Network import connect_network

# Select "default", "lan", "wifi_sta", or "wifi_ap".
NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"  # "auto", "usb", "sdio", or "spi"
NETWORK_TIMEOUT = 15
WIFI_SSID = "Test"
WIFI_PASSWORD = "12345678"
# URL of the remote RTSP server that will receive the pushed stream.
# Replace the host with the address of your RTSP server (e.g. EasyDarwin/mediamtx/ZLMediaKit).
# The path needs a stream name after "live" (e.g. "/live/test"); some servers
# reject the push if the path stops at "/live" with no name.
RTSP_URL = "rtsp://192.168.1.100:8554/live/test"
# NOTE: the rtsp_pusher middleware hardcodes AV_CODEC_ID_H264 (see
# RtspPusherImpl.cpp), so it can only push H.264. H.265 is not supported.
VIDEO_TYPE = mm.multi_media_type.media_h264
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
VIDEO_BIT_RATE = 512  # Kbit/s
VIDEO_GOP = 30
VIDEO_FPS = 25
TRANSPORT = "tcp"  # "tcp" or "udp"


class RtspPusher:
    def __init__(self, url=RTSP_URL,
                 video_type=mm.multi_media_type.media_h264,
                 width=1280, height=720, bit_rate=512, gop_len=30,
                 fps=25, transport="tcp"):
        self.url = url                # 远端rtsp server url
        self.video_type = video_type  # 视频类型 (pusher底层仅支持H.264)
        self.width = ALIGN_UP(width, 16)
        self.height = height
        self.bit_rate = bit_rate
        self.gop_len = gop_len
        self.fps = fps
        self.transport = transport
        self.rtsppusher = mm.rtsp_pusher()  # 实例化rtsp pusher
        self.pusher_opened = False   # pusher是否已open(收到首个SPS/PPS后才init+open)
        self.pusher_inited = False   # pusher是否已init
        self.started = False         # 编码是否已启动

        if bit_rate < 100 or bit_rate > 20000:
            raise ValueError("bit_rate must be between 100 and 20000 Kbit/s")
        if transport not in ("tcp", "udp"):
            raise ValueError("transport must be 'tcp' or 'udp'")
        # pusher中间件硬编码 AV_CODEC_ID_H264, 不支持H.265
        if video_type != mm.multi_media_type.media_h264:
            raise ValueError("rtsp_pusher only supports media_h264 (middleware hardcodes H.264)")
        self.payload_type = Encoder.PAYLOAD_TYPE_H264
        self.profile = Encoder.H264_PROFILE_HIGH  # 与 C++ sample (VENC_PROFILE_H264_HIGH) 一致

    def start(self):
        # 仅初始化并启动编码器; pusher init 推迟到收到首个SPS/PPS后(run里),
        # 避免 pusher 64MB 队列分配在编码器启动前压垮 media pipeline
        try:
            self._init_stream()
            self._start_stream()
            self.started = True
        except:
            if hasattr(self, 'encoder'):
                try:
                    self._stop_stream()
                except:
                    pass
            raise

    def run(self, duration=60):
        """在主线程中轮询编码器并推流 duration 秒。

        不创建工作线程: rtsppusher_open() 内部会阻塞做 RTSP 握手 (最长约 5s),
        放在主线程不会影响其他线程; 同时避免在内存吃紧时 _thread.start_new_thread
        以 EAGAIN 失败。
        """
        streamData = StreamData()
        frame_count = 0
        last_header = None
        dropped_idr_count = 0
        end = time.ticks_add(time.ticks_ms(), duration * 1000)
        while time.ticks_diff(end, time.ticks_ms()) > 0:
            os.exitpoint()
            # 获取一帧码流 (有限超时, 避免永久阻塞)
            if self.encoder.GetStream(streamData, 2000) != 0:
                continue
            # 推流
            for pack_idx in range(0, streamData.pack_cnt):
                stream_type = streamData.stream_type[pack_idx]
                pack_data = bytes(uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx]))

                if stream_type == Encoder.STREAM_TYPE_HEADER:
                    last_header = pack_data
                    if not self.pusher_inited:
                        if self.rtsppusher.rtsppusher_init(self.width, self.height, self.url,
                                                           self.fps, self.transport) != 0:
                            raise RuntimeError("RTSP pusher init failed")
                        self.pusher_inited = True
                    continue

                is_idr = (stream_type == Encoder.STREAM_TYPE_I)
                if is_idr:
                    if last_header is None:
                        # 正常启动时序下 HEADER 会先于首个 I 帧到达, 这里只在异常时序下触发
                        dropped_idr_count += 1
                        if dropped_idr_count == 1 or dropped_idr_count % 30 == 0:
                            print("warning: I frame dropped, no SPS/PPS header yet (%d dropped)" % dropped_idr_count)
                        continue
                    # header 紧跟 I 帧一起下发, 保证二者背靠背; pushvideoheader 只是更新
                    # 底层缓存, open 前后调用均安全, 且会被自动前缀到之后每一帧(含P帧)
                    self.rtsppusher.rtsppusher_pushvideoheader(last_header, len(last_header))
                    if not self.pusher_opened:
                        print("opening pusher (rtsp handshake, may take ~5s)...")
                        if self.rtsppusher.rtsppusher_open() != 0:
                            raise RuntimeError("RTSP pusher open failed, check url: %s" % self.url)
                        self.pusher_opened = True
                        print("rtsp pusher opened: %s" % self.url)

                # 仅在有视频数据且 pusher 已开时推流
                if self.pusher_opened:
                    timestamp = streamData.pts[pack_idx]
                    self.rtsppusher.rtsppusher_pushvideodata(pack_data, len(pack_data),
                                                             1 if is_idr else 0, timestamp)
                    frame_count += 1
                    if frame_count % 300 == 0:
                        print("pushed %d frames" % frame_count)
            # 释放一帧码流
            self.encoder.ReleaseStream(streamData)

    def stop(self):
        if not self.started:
            return
        self.started = False
        # 停止编码
        self._stop_stream()
        # 关闭pusher连接并去初始化 (pusher可能未init, 需判断)
        if self.pusher_opened:
            self.rtsppusher.rtsppusher_close()
            self.pusher_opened = False
        if self.pusher_inited:
            self.rtsppusher.rtsppusher_deinit()
            self.pusher_inited = False

    def _init_stream(self):
        # 初始化sensor
        self.sensor = Sensor()
        self.sensor.reset()
        self.sensor.set_framesize(width=self.width, height=self.height, alignment=12)
        self.sensor.set_pixformat(Sensor.YUV420SP)
        # 实例化video encoder
        self.encoder = Encoder()
        self.encoder.SetOutBufs(8, self.width, self.height)
        # 创建编码器 (不传 src/dst_frame_rate, 用默认30, 避免与sensor实际帧率不匹配导致不出帧)
        chnAttr = ChnAttrStr(self.payload_type, self.profile,
                             self.width, self.height,
                             bit_rate=self.bit_rate, gopLen=self.gop_len)
        self.encoder.Create(chnAttr)
        # 绑定camera和venc
        self.link = MediaManager.link(self.sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, self.encoder.chn))

    def _start_stream(self):
        # 开始编码
        self.encoder.Start()
        # 启动camera
        self.sensor.run()

    def _stop_stream(self):
        # 停止camera
        self.sensor.stop()
        # 解除绑定camera和venc
        self.link.destroy()
        # 停止编码
        self.encoder.Stop()
        self.encoder.Destroy()


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    # Connect the selected network interface before opening the RTSP socket.
    nic, network_ip = connect_network(
        NETWORK_TYPE,
        ssid=WIFI_SSID,
        password=WIFI_PASSWORD,
        wlan_device=WLAN_DEVICE,
        timeout=NETWORK_TIMEOUT,
    )
    # 创建rtsp pusher对象
    rtsppusher = RtspPusher(url=RTSP_URL,
                            video_type=VIDEO_TYPE,
                            width=VIDEO_WIDTH,
                            height=VIDEO_HEIGHT,
                            bit_rate=VIDEO_BIT_RATE,
                            gop_len=VIDEO_GOP,
                            fps=VIDEO_FPS,
                            transport=TRANSPORT)
    # 启动编码器 (pusher将在收到首个SPS/PPS时才init+open)
    rtsppusher.start()
    # 打印推流信息
    print("RTSP pusher started: %s (H264, %dx%d, %d Kbit/s, %s)" %
          (RTSP_URL, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_BIT_RATE, TRANSPORT))
    # 主线程推流60s
    try:
        rtsppusher.run(60)
    finally:
        # 停止rtsp pusher
        rtsppusher.stop()
    print("done")
```

在脚本开头可配置以下项目：

| 配置项 | 说明 | 默认值 |
| :-- | :-- | :-- |
| `NETWORK_TYPE` | `"default"`、`"lan"`、`"wifi_sta"` 或 `"wifi_ap"` | `"wifi_sta"` |
| `WLAN_DEVICE` | `"auto"`、`"usb"`、`"sdio"` 或 `"spi"` | `"auto"` |
| `NETWORK_TIMEOUT` | 等待网络地址的超时时间，单位秒 | `15` |
| `RTSP_URL` | 远端 RTSP 服务器地址（`live` 后需带具体流名，如 `/live/test`；部分服务器不接受路径止步于 `/live` 的推流请求） | `"rtsp://192.168.1.100:8554/live/test"` |
| `VIDEO_WIDTH` / `VIDEO_HEIGHT` | 编码分辨率 | `1280` / `720` |
| `VIDEO_BIT_RATE` | VENC 目标码率，单位 Kbit/s | `512` |
| `VIDEO_GOP` | GOP 帧数 | `30` |
| `VIDEO_FPS` | 编码帧率 | `25` |
| `TRANSPORT` | RTSP 传输方式，`"tcp"` 或 `"udp"` | `"tcp"` |

修改 `RTSP_URL` 为实际 RTSP 服务器地址，以及网络类型、Wi-Fi 凭据后运行脚本。
`RtspPusher.start()` 先启动摄像头和编码器；在主线程 `run()` 轮询编码器输出时，
第一次拿到 `STREAM_TYPE_HEADER`（SPS/PPS）会触发 `rtsppusher_init()`；
之后每收到一个 I 帧，都会把最近一次的 SPS/PPS header 通过
`rtsppusher_pushvideoheader()` 重新下发一次，再推送该 I 帧本身
（首次收到 I 帧时还会调用 `rtsppusher_open()` 建立与服务器的连接）——
这样即使编码器中途重新插入 SPS/PPS，也能保证关键帧与其对应的 header
配对下发，避免远端解码器出现类似 “non-existing PPS” 的花屏或卡顿。
帧时间戳直接使用 VENC/vicap 输出的 `streamData.pts`。

脚本运行后输出类似：

```text
RTSP pusher started: rtsp://192.168.1.100:8554/live/test (H264, 1280x720, 512 Kbit/s, tcp)
opening pusher (rtsp handshake, may take ~5s)...
rtsp pusher opened: rtsp://192.168.1.100:8554/live/test
```

脚本默认运行 60 秒后自动调用 `stop()` 停止编码、关闭并去初始化 RTSP 推流连接。

```{admonition} 提示
具体接口、网络准备和性能配置请参考 [RTSP](../../api/mpp/k230_canmv_rtsp_module_api_manual.md)。
```

### AI+RTSP推流

该示例展示了如何通过调用 AI 模块实现人脸检测功能后，将包含检测结果的图像以 RTSP 网络流的形式输出，便于远程查看或后续处理。
程序启动后，相关信息会直接在终端界面显示，其中将明确给出 RTSP 流的访问地址，格式示例如下：RTSP server started: rtsp://192.168.1.100:8554/test，用户可通过该地址获取带有人脸检测结果的图像流。请将示例 IP 替换为设备实际的局域网 IP。
注意：
若使用客户端访问 RTSP 流，在关闭程序前，请先关闭所有连接的客户端，再执行程序关闭操作。

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
from libs.WBCRtsp import WBCRtsp
import os,sys,ujson,gc,math
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import aidemo
from libs.Network import connect_network

NETWORK_TYPE = "wifi_sta"  # "default"、"lan"、"wifi_sta" 或 "wifi_ap"
WLAN_DEVICE = "auto"       # "auto"、"usb"、"sdio" 或 "spi"
NETWORK_TIMEOUT = 15
WIFI_SSID = "Test"
WIFI_PASSWORD = "12345678"

# 自定义人脸检测类，继承自AIBase基类
class FaceDetectionApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, anchors, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)  # 调用基类的构造函数
        self.kmodel_path = kmodel_path  # 模型文件路径
        self.model_input_size = model_input_size  # 模型输入分辨率
        self.confidence_threshold = confidence_threshold  # 置信度阈值
        self.nms_threshold = nms_threshold  # NMS（非极大值抑制）阈值
        self.anchors = anchors  # 锚点数据，用于目标检测
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]  # sensor给到AI的图像分辨率，并对宽度进行16的对齐
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]  # 显示分辨率，并对宽度进行16的对齐
        self.debug_mode = debug_mode  # 是否开启调试模式
        self.ai2d = Ai2d(debug_mode)  # 实例化Ai2d，用于实现模型预处理
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)  # 设置Ai2d的输入输出格式和类型

    # 配置预处理操作，这里使用了pad和resize，Ai2d支持crop/shift/pad/resize/affine，具体代码请打开/sdcard/app/libs/AI2D.py查看
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):  # 计时器，如果debug_mode大于0则开启
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size  # 初始化ai2d预处理配置，默认为sensor给到AI的尺寸，可以通过设置input_image_size自行修改输入尺寸
            top, bottom, left, right,_ =letterbox_pad_param(self.rgb888p_size,self.model_input_size)
            self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])  # 填充边缘
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)  # 缩放图像
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])  # 构建预处理流程

    # 自定义当前任务的后处理，results是模型输出array列表，这里使用了aidemo库的face_det_post_process接口
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
            post_ret = aidemo.face_det_post_process(self.confidence_threshold, self.nms_threshold, self.model_input_size[1], self.anchors, self.rgb888p_size, results)
            if len(post_ret) == 0:
                return post_ret
            else:
                return post_ret[0]

    # 绘制检测结果到画面上
    def draw_result(self, pl, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            if dets:
                pl.osd_img.clear()  # 清除OSD图像
                for det in dets:
                    # 将检测框的坐标转换为显示分辨率下的坐标
                    x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                    x = x * self.display_size[0] // self.rgb888p_size[0]
                    y = y * self.display_size[1] // self.rgb888p_size[1]
                    w = w * self.display_size[0] // self.rgb888p_size[0]
                    h = h * self.display_size[1] // self.rgb888p_size[1]
                    pl.osd_img.draw_rectangle(x, y, w, h, color=(255, 255, 0, 255), thickness=2)  # 绘制矩形框
            else:
                pl.osd_img.clear()

if __name__ == "__main__":
    # 添加显示模式，默认hdmi，可选hdmi/lcd/lt9611/st7701/hx8399/nt35516,其中hdmi默认置为lt9611，分辨率1920*1080；lcd默认置为st7701，分辨率800*480
    display_mode="lcd"
    # k230保持不变，k230d可调整为[640,360]
    rgb888p_size = [1280, 720]
    # 设置模型路径和其他参数
    kmodel_path = "/sdcard/examples/kmodel/face_detection_320.kmodel"
    # 其它参数
    confidence_threshold = 0.5
    nms_threshold = 0.2
    anchor_len = 4200
    det_dim = 4
    anchors_path = "/sdcard/examples/utils/prior_data_320.bin"
    anchors = np.fromfile(anchors_path, dtype=np.float)
    anchors = anchors.reshape((anchor_len, det_dim))

    nic, network_ip = connect_network(
        NETWORK_TYPE,
        ssid=WIFI_SSID,
        password=WIFI_PASSWORD,
        wlan_device=WLAN_DEVICE,
        timeout=NETWORK_TIMEOUT,
    )

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    # init wbc,wbc_width和wbc_height为原始屏幕的宽高
    WBCRtsp.configure(wbc_width=480,wbc_height=800)
    pl.create(to_ide=False)  # 创建PipeLine实例
    # 启用wbc编码推流
    WBCRtsp.start(network_ip)

    display_size=pl.get_display_size()
    # 初始化自定义人脸检测实例
    face_det = FaceDetectionApp(kmodel_path, model_input_size=[320, 320], anchors=anchors, confidence_threshold=confidence_threshold, nms_threshold=nms_threshold, rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    face_det.config_preprocess()  # 配置预处理

    try:
        while True:
            img = pl.get_frame()            # 获取当前帧数据
            res = face_det.run(img)         # 推理当前帧
            face_det.draw_result(pl, res)   # 绘制结果
            pl.show_image()                 # 显示结果
            gc.collect()                    # 垃圾回收
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        import sys
        sys.print_exception(e)

    face_det.deinit()                       # 反初始化
    WBCRtsp.stop()                          # 停止WBC推流
    pl.destroy()                            # 销毁PipeLine实例
```
