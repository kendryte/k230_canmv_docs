# Audio例程讲解

## 概述

本例程演示了如何利用内置的 codec 链路实现 I2S 音频的采集与播放功能。用户可以通过板载麦克风采集声音，并通过耳机插口进行声音输出。

CanMV K230 开发板配备了一颗模拟麦克风和耳机输出接口，方便用户进行录音与音频播放的测试。

## 示例

### audio - 音频采集与播放例程

该示例程序展示了 CanMV 开发板的音频采集和输出功能。

```python
# 音频输入和输出示例
#
# 注意：运行此示例需要一个 SD 卡。
#
# 您可以播放WAV文件或捕获音频并保存为 WAV 格式。

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
    CHUNK = 44100//25  #设置音频chunk值
    FORMAT = paInt16       #设置采样精度,支持16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    CHANNELS = 2           #设置声道数,支持单声道(1)/立体声(2)
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

        stream.volume(LEFT,70)
        stream.volume(RIGHT,85)
        print("volume :",stream.volume())

        #启用音频3A功能：自动噪声抑制(ANS)
        stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)

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

        #设置音频输出流的音量
        stream.volume(vol=85)

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
    CHUNK = 44100//25#设置音频chunck
    FORMAT = paInt16 #设置音频采样精度,支持16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    CHANNELS = 2 #设置音频声道数，支持单声道(1)/立体声(2)
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

        #设置音频输入流的音量
        input_stream.volume(LEFT,70)
        input_stream.volume(RIGHT,85)
        print("input volume :",input_stream.volume())

        #启用音频3A功能：自动噪声抑制(ANS)
        input_stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)

        #创建音频输出流
        output_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,frames_per_buffer=CHUNK)

        #设置音频输出流的音量
        output_stream.volume(vol=85)

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

def audio_recorder(filename, duration):
    CHUNK = 44100//25      #设置音频chunk值
    FORMAT = paInt16       #设置采样精度,支持16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    CHANNELS = 1           #设置声道数,支持单声道(1)/立体声(2)
    RATE = 44100           #设置采样率

    p = PyAudio()
    p.initialize(CHUNK)    #初始化PyAudio对象
    MediaManager.init()    #vb buffer初始化

    try:
        #创建音频输入流
        input_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        input_stream.volume(LEFT,70)
        input_stream.volume(RIGHT,85)
        print("input volume :",input_stream.volume())

        #启用音频3A功能：自动噪声抑制(ANS)
        input_stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)
        print("enable audio 3a:ans")

        print("start record...")
        frames = []
        #采集音频数据并存入列表
        for i in range(0, int(RATE / CHUNK * duration)):
            data = input_stream.read()
            frames.append(data)
            if exit_check():
                break
        print("stop record...")
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
        input_stream.stop_stream() #停止采集音频数据
        input_stream.close()#关闭音频输入流

    try:
        wf = wave.open(filename, 'rb')#打开wav文件
        CHUNK = int(wf.get_framerate()/25)#设置音频chunk值

        #创建音频输出流，设置的音频参数均为wave中获取到的参数
        output_stream = p.open(format=p.get_format_from_width(wf.get_sampwidth()),
                    channels=wf.get_channels(),
                    rate=wf.get_framerate(),
                    output=True,frames_per_buffer=CHUNK)

        #设置音频输出流的音量
        output_stream.volume(vol=85)
        print("output volume :",output_stream.volume())

        print("start play...")
        data = wf.read_frames(CHUNK)#从wav文件中读取数一帧数据

        while data:
            output_stream.write(data)  #将帧数据写入到音频输出流中
            data = wf.read_frames(CHUNK) #从wav文件中读取数一帧数据
            if exit_check():
                break
        print("stop play...")
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        output_stream.stop_stream() #停止音频输出流
        output_stream.close()#关闭音频输出流

    p.terminate() #释放音频对象
    MediaManager.deinit() #释放vb buffer

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("音频示例开始")
    # record_audio('/sdcard/examples/test.wav', 15)  # 录制WAV文件
    # play_audio('/sdcard/examples/test.wav')  # 播放WAV文件
    # loop_audio(15)  # 采集音频并输出
    audio_recorder('/sdcard/examples/test.wav', 15) #录制15秒音频并播放
    print("音频示例完成")
```

```{admonition} 提示
有关audio模块的具体接口，请参考[API文档](../../api/mpp/K230_CanMV_Audio模块API手册.md)
```

### acodec - G711 编解码例程

该示例程序展示了 CanMV 开发板的 G711 编解码功能。

```python
# G711 编码/解码示例
#
# 注意：运行此示例需要一个SD卡。
#
# 您可以收集原始数据并编码为G711，或将其解码为原始数据输出。

import os
from mpp.payload_struct import *  # 导入payload模块，用于获取音视频编解码类型
from media.media import *         # 导入media模块，用于初始化vb buffer
from media.pyaudio import *       # 导入pyaudio模块，用于采集和播放音频
import media.g711 as g711         # 导入g711模块，用于G711编解码

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("用户停止：", e)
        return True
    return False

def encode_audio(filename, duration):
    CHUNK = int(44100 / 25)  # 设置音频块大小
    FORMAT = paInt16         # 设置采样精度
    CHANNELS = 2             # 设置声道数
    RATE = 44100             # 设置采样率

    try:
        p = PyAudio()
        p.initialize(CHUNK)  # 初始化PyAudio对象
        enc = g711.Encoder(K_PT_G711A, CHUNK)  # 创建G711编码器对象
        MediaManager.init()   # 初始化vb buffer

        enc.create()  # 创建编码器
        # 创建音频输入流
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        # 采集音频数据并编码，存入列表
        for i in range(0, int(RATE / CHUNK * duration)):
            frame_data = stream.read()  # 从音频输入流中读取音频数据
            data = enc.encode(frame_data)  # 编码音频数据为G711
            frames.append(data)  # 保存G711编码

数据到列表中
            if exit_check():
                break
        # 将G711编码数据存入文件
        with open(filename, mode='wb') as wf:
            wf.write(b''.join(frames))
        stream.stop_stream()  # 停止音频输入流
        stream.close()        # 关闭音频输入流
        p.terminate()         # 释放音频对象
        enc.destroy()         # 销毁G711编码器
    except BaseException as e:
        print(f"异常：{e}")
    finally:
        MediaManager.deinit()  # 释放vb buffer

def decode_audio(filename):
    FORMAT = paInt16         # 设置音频块大小
    CHANNELS = 2             # 设置声道数
    RATE = 44100             # 设置采样率
    CHUNK = int(RATE / 25)   # 设置音频块大小

    try:
        wf = open(filename, mode='rb')  # 打开G711文件
        p = PyAudio()
        p.initialize(CHUNK)  # 初始化PyAudio对象
        dec = g711.Decoder(K_PT_G711A, CHUNK)  # 创建G711解码器对象
        MediaManager.init()   # 初始化vb buffer

        dec.create()  # 创建解码器

        # 创建音频输出流
        stream = p.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         output=True,
                         frames_per_buffer=CHUNK)

        stream_len = CHUNK * CHANNELS * 2 // 2  # 设置每次读取的G711数据流长度
        stream_data = wf.read(stream_len)  # 从G711文件中读取数据

        # 解码G711文件并播放
        while stream_data:
            frame_data = dec.decode(stream_data)  # 解码G711文件
            stream.write(frame_data)  # 播放原始数据
            stream_data = wf.read(stream_len)  # 继续从G711文件中读取数据
            if exit_check():
                break
        stream.stop_stream()  # 停止音频输出流
        stream.close()        # 关闭音频输出流
        p.terminate()         # 释放音频对象
        dec.destroy()         # 销毁解码器
        wf.close()           # 关闭G711文件

    except BaseException as e:
        print(f"异常：{e}")
    finally:
        MediaManager.deinit()  # 释放vb buffer

def loop_codec(duration):
    CHUNK = int(44100 / 25)  # 设置音频块大小
    FORMAT = paInt16         # 设置采样精度
    CHANNELS = 2             # 设置声道数
    RATE = 44100             # 设置采样率

    try:
        p = PyAudio()
        p.initialize(CHUNK)  # 初始化PyAudio对象
        dec = g711.Decoder(K_PT_G711A, CHUNK)  # 创建G711解码器对象
        enc = g711.Encoder(K_PT_G711A, CHUNK)  # 创建G711编码器对象
        MediaManager.init()   # 初始化vb buffer

        dec.create()  # 创建G711解码器
        enc.create()  # 创建G711编码器

        # 创建音频输入流
        input_stream = p.open(format=FORMAT,
                               channels=CHANNELS,
                               rate=RATE,
                               input=True,
                               frames_per_buffer=CHUNK)

        # 创建音频输出流
        output_stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                output=True,
                                frames_per_buffer=CHUNK)

        # 从音频输入流获取数据，编码，解码并写入音频输出流
        for i in range(0, int(RATE / CHUNK * duration)):
            frame_data = input_stream.read()  # 从音频输入流获取原始音频数据
            stream_data = enc.encode(frame_data)  # 编码音频数据为G711
            frame_data = dec.decode(stream_data)  # 解码G711数据为原始数据
            output_stream.write(frame_data)  # 播放原始数据
            if exit_check():
                break
        input_stream.stop_stream()  # 停止音频输入流
        output_stream.stop_stream()  # 停止音频输出流
        input_stream.close()         # 关闭音频输入流
        output_stream.close()        # 关闭音频输出流
        p.terminate()                # 释放音频对象
        dec.destroy()                # 销毁G711解码器
        enc.destroy()                # 销毁G711编码器
    except BaseException as e:
        print(f"异常：{e}")
    finally:
        MediaManager.deinit()  # 释放vb buffer

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("音频编解码示例开始")
    # encode_audio('/sdcard/examples/test.g711a', 15) # 采集并编码G711文件
    # decode_audio('/sdcard/examples/test.g711a')  # 解码G711文件并输出
    loop_codec(15)  # 采集音频数据 -> 编码G711 -> 解码G711 -> 播放音频
    print("音频编解码示例完成")
```

```{admonition} 提示
有关 acodec 模块的具体接口，请参考[API文档](../../api/mpp/K230_CanMV_播放器模块API手册.md)
```
