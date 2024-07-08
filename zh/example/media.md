# 4.多媒体 例程讲解

## 1.acodec - g711 编解码例程

本示例程序用于对 CanMV 开发板进行一个 g711 编解码的功能展示。

```python
# g711 encode/decode example
#
# Note: You will need an SD card to run this example.
#
# You can collect raw data and encode it into g711 or decode it into raw data output.

import os
from mpp.payload_struct import * #导入payload模块，用于获取音视频编解码类型
from media.media import * #导入media模块，用于初始化vb buffer
from media.pyaudio import * #导入pyaudio模块，用于采集和播放音频
import media.g711 as g711 #导入g711模块，用于g711编解码

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
        return True
    return False

def encode_audio(filename, duration):
    CHUNK = int(44100/25) #设置音频chunk值
    FORMAT = paInt16 #设置采样精度
    CHANNELS = 2 #设置声道数
    RATE = 44100 #设置采样率

    try:
        p = PyAudio()
        p.initialize(CHUNK) #初始化PyAudio对象
        enc = g711.Encoder(K_PT_G711A,CHUNK) #创建g711编码器对象
        MediaManager.init()    #vb buffer初始化

        enc.create() #创建编码器
        #创建音频输入流
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        #采集音频数据编码并存入列表
        for i in range(0, int(RATE / CHUNK * duration)):
            frame_data = stream.read() #从音频输入流中读取音频数据
            data = enc.encode(frame_data) #编码音频数据为g711
            frames.append(data)  #将g711编码数据保存到列表中
            if exit_check():
                break
        #将g711编码数据存入文件中
        with open(filename,mode='w') as wf:
            wf.write(b''.join(frames))
        stream.stop_stream() #停止音频输入流
        stream.close() #关闭音频输入流
        p.terminate() #释放音频对象
        enc.destroy() #销毁g711音频编码器
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        MediaManager.deinit() #释放vb buffer

def decode_audio(filename):
    FORMAT = paInt16 #设置音频chunk值
    CHANNELS = 2 #设置声道数
    RATE = 44100 #设置采样率
    CHUNK = int(RATE/25) #设置音频chunk值

    try:
        wf = open(filename,mode='rb') #打开g711文件
        p = PyAudio()
        p.initialize(CHUNK) #初始化PyAudio对象
        dec = g711.Decoder(K_PT_G711A,CHUNK) #创建g711解码器对象
        MediaManager.init()    #vb buffer初始化

        dec.create() #创建解码器

        #创建音频输出流
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

        stream_len = CHUNK*CHANNELS*2//2  #设置每次读取的g711数据流长度
        stream_data = wf.read(stream_len) #从g711文件中读取数据

        #解码g711文件并播放
        while stream_data:
            frame_data = dec.decode(stream_data) #解码g711文件
            stream.write(frame_data) #播放raw数据
            stream_data = wf.read(stream_len) #从g711文件中读取数据
            if exit_check():
                break
        stream.stop_stream() #停止音频输入流
        stream.close() #关闭音频输入流
        p.terminate() #释放音频对象
        dec.destroy() #销毁解码器
        wf.close() #关闭g711文件

    except BaseException as e:
            print(f"Exception {e}")
    finally:
        MediaManager.deinit() #释放vb buffer

def loop_codec(duration):
    CHUNK = int(44100/25) #设置音频chunk值
    FORMAT = paInt16 #设置采样精度
    CHANNELS = 2 #设置声道数
    RATE = 44100 #设置采样率

    try:
        p = PyAudio()
        p.initialize(CHUNK) #初始化PyAudio对象
        dec = g711.Decoder(K_PT_G711A,CHUNK) #创建g711解码器对象
        enc = g711.Encoder(K_PT_G711A,CHUNK) #创建g711编码器对象
        MediaManager.init()    #vb buffer初始化

        dec.create() #创建g711解码器
        enc.create() #创建g711编码器

        #创建音频输入流
        input_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        #创建音频输出流
        output_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

        #从音频输入流中获取数据->编码->解码->写入到音频输出流中
        for i in range(0, int(RATE / CHUNK * duration)):
            frame_data = input_stream.read() #从音频输入流中获取raw音频数据
            stream_data = enc.encode(frame_data) #编码音频数据为g711
            frame_data = dec.decode(stream_data) #解码g711数据为raw数据
            output_stream.write(frame_data) #播放raw数据
            if exit_check():
                break
        input_stream.stop_stream() #停止音频输入流
        output_stream.stop_stream() #停止音频输出流
        input_stream.close() #关闭音频输入流
        output_stream.close() #关闭音频输出流
        p.terminate() #释放音频对象
        dec.destroy() #销毁g711解码器
        enc.destroy() #销毁g711编码器
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        MediaManager.deinit() #释放vb buffer

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("audio codec sample start")
    #encode_audio('/sdcard/app/test.g711a', 15) #采集并编码g711文件
    #decode_audio('/sdcard/app/test.g711a') #解码g711文件并输出
    loop_codec(15) #采集音频数据->编码g711->解码g711->播放音频
    print("audio codec sample done")
```

具体接口定义请参考 [acodec](../api/mpp/K230_CanMV_播放器模块API手册.md)

## 2.audio - 音频采集输出例程

本示例程序用于对 CanMV 开发板进行一个音频采集和输出的功能展示。

```python
# audio input and output example
#
# Note: You will need an SD card to run this example.
#
# You can play wav files or capture audio to save as wav

import os
from media.media import *   #导入media模块，用于初始化vb buffer
from media.pyaudio import * #导入pyaudio模块，用于采集和播放音频
import media.wave as wave   #导入wav模块，用于保存和加载wav音频文件

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
        return True
    return False

def record_audio(filename, duration):
    CHUNK = int(44100/25)  #设置音频chunk值
    FORMAT = paInt16       #设置采样精度
    CHANNELS = 2           #设置声道数
    RATE = 44100           #设置采样率

    try:
        p = PyAudio()
        p.initialize(CHUNK)    #初始化PyAudio对象
        MediaManager.init()    #vb buffer初始化

        #创建音频输入流
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        #采集音频数据并存入列表
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read()
            frames.append(data)
            if exit_check():
                break
        #将列表中的数据保存到wav文件中
        wf = wave.open(filename, 'wb') #创建wav 文件
        wf.set_channels(CHANNELS) #设置wav 声道数
        wf.set_sampwidth(p.get_sample_size(FORMAT))  #设置wav 采样精度
        wf.set_framerate(RATE)  #设置wav 采样率
        wf.write_frames(b''.join(frames)) #存储wav音频数据
        wf.close() #关闭wav文件
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        stream.stop_stream() #停止采集音频数据
        stream.close()#关闭音频输入流
        p.terminate()#释放音频对象
        MediaManager.deinit() #释放vb buffer

def play_audio(filename):
    try:
        wf = wave.open(filename, 'rb')#打开wav文件
        CHUNK = int(wf.get_framerate()/25)#设置音频chunk值

        p = PyAudio()
        p.initialize(CHUNK) #初始化PyAudio对象
        MediaManager.init()    #vb buffer初始化

        #创建音频输出流，设置的音频参数均为wave中获取到的参数
        stream = p.open(format=p.get_format_from_width(wf.get_sampwidth()),
                    channels=wf.get_channels(),
                    rate=wf.get_framerate(),
                    output=True,frames_per_buffer=CHUNK)

        data = wf.read_frames(CHUNK)#从wav文件中读取数一帧数据

        while data:
            stream.write(data)  #将帧数据写入到音频输出流中
            data = wf.read_frames(CHUNK) #从wav文件中读取数一帧数据
            if exit_check():
                break
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        stream.stop_stream() #停止音频输出流
        stream.close()#关闭音频输出流
        p.terminate()#释放音频对象
        wf.close()#关闭wav文件

        MediaManager.deinit() #释放vb buffer


def loop_audio(duration):
    CHUNK = int(44100/25)#设置音频chunck
    FORMAT = paInt16 #设置音频采样精度
    CHANNELS = 2 #设置音频声道数
    RATE = 44100 #设置音频采样率

    try:
        p = PyAudio()
        p.initialize(CHUNK)#初始化PyAudio对象
        MediaManager.init()    #vb buffer初始化

        #创建音频输入流
        input_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        #创建音频输出流
        output_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,frames_per_buffer=CHUNK)

        #从音频输入流中获取数据写入到音频输出流中
        for i in range(0, int(RATE / CHUNK * duration)):
            output_stream.write(input_stream.read())
            if exit_check():
                break
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        input_stream.stop_stream()#停止音频输入流
        output_stream.stop_stream()#停止音频输出流
        input_stream.close() #关闭音频输入流
        output_stream.close() #关闭音频输出流
        p.terminate() #释放音频对象

        MediaManager.deinit() #释放vb buffer

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("audio sample start")
    #play_audio('/sdcard/app/input.wav') #播放wav文件
    #record_audio('/sdcard/app/output.wav', 15)  #录制wav文件
    loop_audio(15) #采集音频并输出
    print("audio sample done")
```

具体接口定义请参考 [audio](../api/mpp/K230_CanMV_Audio模块API手册.md)

## 3.Camera - 摄像头预览及图像采集示例

```python
# Camera Example
import time, os, sys

from media.sensor import *
from media.display import *
from media.media import *

sensor = None

try:
    print("camera_test")

    # construct a Sensor object with default configure
    sensor = Sensor()
    # sensor reset
    sensor.reset()
    # set hmirror
    # sensor.set_hmirror(False)
    # sensor vflip
    # sensor.set_vflip(False)

    # set chn0 output size, 1920x1080
    sensor.set_framesize(Sensor.FHD)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)
    # bind sensor chn0 to display layer video 1
    bind_info = sensor.bind_info()
    Display.bind_layer(**bind_info, layer = Display.LAYER_VIDEO1)

    # set chn1 output format
    sensor.set_framesize(width = 640, height = 480, chn = CAM_CHN_ID_1)
    sensor.set_pixformat(Sensor.RGB888, chn = CAM_CHN_ID_1)

    # set chn2 output format
    sensor.set_framesize(width = 640, height = 480, chn = CAM_CHN_ID_2)
    sensor.set_pixformat(Sensor.RGB565, chn = CAM_CHN_ID_2)

    # use hdmi as display output
    Display.init(Display.LT9611, to_ide = True, osd_num = 2)
    # init media manager
    MediaManager.init()
    # sensor start run
    sensor.run()

    while True:
        os.exitpoint()

        img = sensor.snapshot(chn = CAM_CHN_ID_1)
        Display.show_image(img, alpha = 128)

        img = sensor.snapshot(chn = CAM_CHN_ID_2)
        Display.show_image(img, x = 1920 - 640, layer = Display.LAYER_OSD1)

except KeyboardInterrupt as e:
    print("user stop: ", e)
except BaseException as e:
    print(f"Exception {e}")
finally:
    # sensor stop run
    if isinstance(sensor, Sensor):
        sensor.stop()
    # deinit display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()
```

具体接口定义请参考 [camera](../api/mpp/K230_CanMV_Sensor模块API手册.md)

## 4. Camera - 多摄像头预览及图像采集示例

```python
# Camera Example
#
# Note: You will need an SD card to run this example.
#
# You can start 2 camera preview.
import time, os, sys

from media.sensor import *
from media.display import *
from media.media import *

sensor0 = None
sensor1 = None

try:
    print("camera_test")

    sensor0 = Sensor(id = 0)
    sensor0.reset()
    # set chn0 output size, 960x540
    sensor0.set_framesize(width = 960, height = 540)
    # set chn0 out format
    sensor0.set_pixformat(Sensor.YUV420SP)
    # bind sensor chn0 to display layer video 1
    bind_info = sensor0.bind_info(x = 0, y = 0)
    Display.bind_layer(**bind_info, layer = Display.LAYER_VIDEO1)

    sensor1 = Sensor(id = 1)
    sensor1.reset()
    # set chn0 output size, 960x540
    sensor1.set_framesize(width = 960, height = 540)
    # set chn0 out format
    sensor1.set_pixformat(Sensor.YUV420SP)

    bind_info = sensor1.bind_info(x = 960, y = 540)
    Display.bind_layer(**bind_info, layer = Display.LAYER_VIDEO2)

    # use hdmi as display output
    Display.init(Display.LT9611, to_ide = True)
    # init media manager
    MediaManager.init()

    # multiple sensor only need one excute run()
    sensor0.run()

    while True:
        os.exitpoint()
        time.sleep(1)
except KeyboardInterrupt as e:
    print("user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # multiple sensor all need excute stop()
    if isinstance(sensor0, Sensor):
        sensor0.stop()
    if isinstance(sensor1, Sensor):
        sensor1.stop()
    # or call Sensor.deinit()
    # Sensor.deinit()

    # deinit display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # deinit media buffer
    MediaManager.deinit()

```

具体接口定义请参考 [camera](../api/mpp/K230_CanMV_Sensor模块API手册.md)

## 5. Display - 图像采集显示实例

```python
import time, os, urandom, sys

from media.display import *
from media.media import *

DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

def display_test():
    print("display test")

    # create image for drawing
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    # use hdmi as display output
    Display.init(Display.LT9611, to_ide = True)
    # init media manager
    MediaManager.init()

    try:
        while True:
            img.clear()
            for i in range(10):
                x = (urandom.getrandbits(11) % img.width())
                y = (urandom.getrandbits(11) % img.height())
                r = (urandom.getrandbits(8))
                g = (urandom.getrandbits(8))
                b = (urandom.getrandbits(8))
                size = (urandom.getrandbits(30) % 64) + 32
                # If the first argument is a scaler then this method expects
                # to see x, y, and text. Otherwise, it expects a (x,y,text) tuple.
                # Character and string rotation can be done at 0, 90, 180, 270, and etc. degrees.
                img.draw_string_advanced(x,y,size, "Hello World!，你好世界！！！", color = (r, g, b),)

            # draw result to screen
            Display.show_image(img)

            time.sleep(1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        print(f"Exception {e}")

    # deinit display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()


```

具体接口定义请参考 [display](../api/mpp/K230_CanMV_Display模块API手册.md)

## 6. mp4 muxer 例程

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

具体接口定义请参考 [VENC](../api/mpp/K230_CanMV_MP4模块API手册.md)

## 8. player - mp4 文件播放器例程

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

具体接口定义请参考 [player](../api/mpp/K230_CanMV_播放器模块API手册.md)

## 9. venc - venc 例程

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

具体接口定义请参考 [VENC](../api/mpp/K230_CanMV_VENC模块API手册.md)

## 10. lvgl - lvgl 例程

本示例程序用于对 CanMV 开发板进行一个 lvgl 的功能展示。

```python
from media.display import *
from media.media import *
import time, os, sys, gc
import lvgl as lv

DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

def display_init():
    # use hdmi for display
    Display.init(Display.LT9611, to_ide = False)
    # init media manager
    MediaManager.init()

def display_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(50)
    # deinit display
    Display.deinit()
    # release media buffer
    MediaManager.deinit()

def disp_drv_flush_cb(disp_drv, area, color):
    global disp_img1, disp_img2

    if disp_drv.flush_is_last() == True:
        if disp_img1.virtaddr() == uctypes.addressof(color.__dereference__()):
            Display.show_image(disp_img1)
        else:
            Display.show_image(disp_img2)
    disp_drv.flush_ready()

def lvgl_init():
    global disp_img1, disp_img2

    lv.init()
    disp_drv = lv.disp_create(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    disp_drv.set_flush_cb(disp_drv_flush_cb)
    disp_img1 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    disp_img2 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    disp_drv.set_draw_buffers(disp_img1.bytearray(), disp_img2.bytearray(), disp_img1.size(), lv.DISP_RENDER_MODE.DIRECT)

def lvgl_deinit():
    global disp_img1, disp_img2

    lv.deinit()
    del disp_img1
    del disp_img2

def user_gui_init():
    res_path = "/sdcard/app/tests/lvgl/data/"

    font_montserrat_16 = lv.font_load("A:" + res_path + "font/montserrat-16.fnt")
    ltr_label = lv.label(lv.scr_act())
    ltr_label.set_text("In modern terminology, a microcontroller is similar to a system on a chip (SoC).")
    ltr_label.set_style_text_font(font_montserrat_16,0)
    ltr_label.set_width(310)
    ltr_label.align(lv.ALIGN.TOP_MID, 0, 0)

    font_simsun_16_cjk = lv.font_load("A:" + res_path + "font/lv_font_simsun_16_cjk.fnt")
    cz_label = lv.label(lv.scr_act())
    cz_label.set_style_text_font(font_simsun_16_cjk, 0)
    cz_label.set_text("嵌入式系统（Embedded System），\n是一种嵌入机械或电气系统内部、具有专一功能和实时计算性能的计算机系统。")
    cz_label.set_width(310)
    cz_label.align(lv.ALIGN.BOTTOM_MID, 0, 0)

    anim_imgs = [None]*4
    with open(res_path + 'img/animimg001.png','rb') as f:
        anim001_data = f.read()

    anim_imgs[0] = lv.img_dsc_t({
    'data_size': len(anim001_data),
    'data': anim001_data
    })
    anim_imgs[-1] = anim_imgs[0]

    with open(res_path + 'img/animimg002.png','rb') as f:
        anim002_data = f.read()

    anim_imgs[1] = lv.img_dsc_t({
    'data_size': len(anim002_data),
    'data': anim002_data
    })

    with open(res_path + 'img/animimg003.png','rb') as f:
        anim003_data = f.read()

    anim_imgs[2] = lv.img_dsc_t({
    'data_size': len(anim003_data),
    'data': anim003_data
    })

    animimg0 = lv.animimg(lv.scr_act())
    animimg0.center()
    animimg0.set_src(anim_imgs, 4)
    animimg0.set_duration(2000)
    animimg0.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    animimg0.start()

def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    try:
        display_init()
        lvgl_init()
        user_gui_init()
        while True:
            time.sleep_ms(lv.task_handler())
    except BaseException as e:
        print(f"Exception {e}")
    lvgl_deinit()
    display_deinit()
    gc.collect()

if __name__ == "__main__":
    main()
```

具体接口定义请参考 [lvgl](../api/lvgl/lvgl.md)
