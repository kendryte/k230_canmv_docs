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
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # 绑定camera和venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, venc_chn))

    # init media manager
    MediaManager.init()

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(venc_chn, chnAttr)

    # 开始编码
    encoder.Start(venc_chn)
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    video_start_timestamp = 0
    get_first_I_frame = False

    try:
        while True:
            os.exitpoint()
            encoder.GetStream(venc_chn, streamData) # 获取一帧码流
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
                    encoder.ReleaseStream(venc_chn, streamData) # 释放一帧码流
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

            encoder.ReleaseStream(venc_chn, streamData) # 释放一帧码流

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
    del link
    # 停止编码
    encoder.Stop(venc_chn)
    # 销毁编码器
    encoder.Destroy(venc_chn)
    # 清理buffer
    MediaManager.deinit()

    # mp4 muxer destroy
    kd_mp4_destroy_tracks(mp4_handle)
    kd_mp4_destroy(mp4_handle)

    print("venc_test stop")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_mp4_test("/sdcard/examples/test.mp4", 1280, 720)
```

```{admonition} 提示
具体接口定义请参考 [mp4muxer](../../api/mpp/K230_CanMV_MP4模块API手册.md)
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

```{admonition} 提示
具体接口定义请参考 [mp4demuxer](../../api/mpp/K230_CanMV_MP4解复用器模块API手册.md)
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
具体接口定义请参考 [player](../../api/mpp/K230_CanMV_播放器模块API手册.md)
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
    venc_chn = VENC_CHN_ID_0
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
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # 绑定camera和venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, venc_chn))

    # init media manager
    MediaManager.init()

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(venc_chn, chnAttr)

    # 开始编码
    encoder.Start(venc_chn)
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    with open(file_name, "wb") as fo:
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
    del link
    # 停止编码
    encoder.Stop(venc_chn)
    # 销毁编码器
    encoder.Destroy(venc_chn)
    # 清理buffer
    MediaManager.deinit()
    print("venc_test stop")

def stream_venc_test(file_name,width=1280, height=720):
    print("venc_test start")
    venc_chn = VENC_CHN_ID_0
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
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # init media manager
    MediaManager.init()

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(venc_chn, chnAttr)

    # 开始编码
    encoder.Start(venc_chn)
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
                yuv420sp_img = sensor.snapshot(chn=CAM_CHN_ID_0)
                if (yuv420sp_img == -1):
                    continue

                frame_info.v_frame.width = yuv420sp_img.width()
                frame_info.v_frame.height = yuv420sp_img.height()
                frame_info.v_frame.pixel_format = Sensor.YUV420SP
                frame_info.pool_id = yuv420sp_img.poolid()
                frame_info.v_frame.phys_addr[0] = yuv420sp_img.phyaddr()
                #frame_info.v_frame.phys_addr[1] = yuv420sp_img.phyaddr(1)
                if (yuv420sp_img.width() == 800 and yuv420sp_img.height() == 480):
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width*frame_info.v_frame.height + 1024
                elif (yuv420sp_img.width() == 1920 and yuv420sp_img.height() == 1080):
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width*frame_info.v_frame.height + 3072
                elif (yuv420sp_img.width() == 640 and yuv420sp_img.height() == 360):
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width*frame_info.v_frame.height + 3072
                else:
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width*frame_info.v_frame.height


                encoder.SendFrame(venc_chn,frame_info)
                encoder.GetStream(venc_chn, streamData) # 获取一帧码流

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # 码流写文件
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(venc_chn, streamData) # 释放一帧码流

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
    encoder.Stop(venc_chn)
    # 销毁编码器
    encoder.Destroy(venc_chn)
    # 清理buffer
    MediaManager.deinit()
    print("venc_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_test("/sdcard/examples/test.264",800,480)  # vi绑定venc示例
    #stream_venc_test("/sdcard/examples/test.264",800,480)  # venc编码数据流示例
```

```{admonition} 提示
具体接口定义请参考 [VENC](../../api/mpp/K230_CanMV_VENC模块API手册.md)
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
具体接口定义请参考 [VDEC](../../api/mpp/K230_CanMV_VDEC模块API手册.md)
```

### RTSP推流

这个示例演示了如何使用RTSP服务器将视频和音频流式传输到网络。
注意：
若使用客户端访问 RTSP 流，在关闭程序前，请先关闭所有连接的客户端，再执行程序关闭操作。

```python
# Description: This example demonstrates how to stream video and audio to the network using the RTSP server.
#
# Note: You will need an SD card to run this example.
#
# You can run the rtsp server to stream video and audio to the network

from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os
import _thread
import multimedia as mm
from time import *

class RtspServer:
    def __init__(self,session_name="test",port=8554,video_type = mm.multi_media_type.media_h264,enable_audio=False):
        self.session_name = session_name # session name
        self.video_type = video_type  # 视频类型264/265
        self.enable_audio = enable_audio # 是否启用音频
        self.port = port   #rtsp 端口号
        self.rtspserver = mm.rtsp_server() # 实例化rtsp server
        self.venc_chn = VENC_CHN_ID_0 #venc通道
        self.start_stream = False #是否启动推流线程
        self.runthread_over = False #推流线程是否结束

    def start(self):
        # 初始化推流
        self._init_stream()
        self.rtspserver.rtspserver_init(self.port)
        # 创建session
        self.rtspserver.rtspserver_createsession(self.session_name,self.video_type,self.enable_audio)
        # 启动rtsp server
        self.rtspserver.rtspserver_start()
        self._start_stream()

        # 启动推流线程
        self.start_stream = True
        _thread.start_new_thread(self._do_rtsp_stream,())


    def stop(self):
        if (self.start_stream == False):
            return
        # 等待推流线程退出
        self.start_stream = False
        while not self.runthread_over:
            sleep(0.1)
        self.runthread_over = False

        # 停止推流
        self._stop_stream()
        self.rtspserver.rtspserver_stop()
        #self.rtspserver.rtspserver_destroysession(self.session_name)
        self.rtspserver.rtspserver_deinit()

    def get_rtsp_url(self):
        return self.rtspserver.rtspserver_getrtspurl(self.session_name)

    def _init_stream(self):
        width = 1280
        height = 720
        width = ALIGN_UP(width, 16)
        # 初始化sensor
        self.sensor = Sensor()
        self.sensor.reset()
        self.sensor.set_framesize(width = width, height = height, alignment=12)
        self.sensor.set_pixformat(Sensor.YUV420SP)
        # 实例化video encoder
        self.encoder = Encoder()
        self.encoder.SetOutBufs(self.venc_chn, 8, width, height)
        # 绑定camera和venc
        self.link = MediaManager.link(self.sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, self.venc_chn))
        # init media manager
        MediaManager.init()
        # 创建编码器
        chnAttr = ChnAttrStr(self.encoder.PAYLOAD_TYPE_H264, self.encoder.H264_PROFILE_MAIN, width, height)
        self.encoder.Create(self.venc_chn, chnAttr)

    def _start_stream(self):
        # 开始编码
        self.encoder.Start(self.venc_chn)
        # 启动camera
        self.sensor.run()

    def _stop_stream(self):
        # 停止camera
        self.sensor.stop()
        # 接绑定camera和venc
        del self.link
        # 停止编码
        self.encoder.Stop(self.venc_chn)
        self.encoder.Destroy(self.venc_chn)
        # 清理buffer
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
            # 停止rtsp server
            self.stop()

        self.runthread_over = True

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    # 创建rtsp server对象
    rtspserver = RtspServer()
    # 启动rtsp server
    rtspserver.start()
    # 打印rtsp url
    print("rtsp server start:",rtspserver.get_rtsp_url())
    # 推流60s
    sleep(60)
    # 停止rtsp server
    rtspserver.stop()
    print("done")
```

```{admonition} 提示
具体接口定义请参考 [RTSP](../../api/mpp/K230_CanMV_RTSP模块API手册.md)
```

### AI+RTSP推流

该示例展示了如何通过调用 AI 模块实现人脸检测功能后，将包含检测结果的图像以 RTSP 网络流的形式输出，便于远程查看或后续处理。
程序启动后，相关信息会直接在终端界面显示，其中将明确给出 RTSP 流的访问地址，格式示例如下：RTSP server started: rtsp://10.100.228.20:8554/test，用户可通过该地址获取带有人脸检测结果的图像流。
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

    # 初始化PipeLine，用于图像处理流程
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    # init wbc,wbc_width和wbc_height为原始屏幕的宽高
    WBCRtsp.configure(wbc_width=480,wbc_height=800)
    pl.create(to_ide=False)  # 创建PipeLine实例
    # 启用wbc编码推流
    WBCRtsp.start()

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
