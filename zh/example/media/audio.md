# 3. Audio例程讲解

## 1. 概述

本例程演示了如何使用内置的codec链路实现i2s音频的采集和播放功能。可以通过板载mic 采集声音并通过板载耳机插口输出声音。

CanMV K230开发板板载一颗模拟mic和耳机输出，用户可用来测试录音与音频播放

## 2. 示例

### 2.1 audio - 音频采集与播放例程

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

```{admonition} 提示
audio模块具体接口请参考[API文档](../../api/mpp/K230_CanMV_Audio模块API手册.md)
```

### 2.2 acodec - g711 编解码例程

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

```{admonition} 提示
acodec模块具体接口请参考[API文档](../../api/mpp/K230_CanMV_播放器模块API手册.md)
```
