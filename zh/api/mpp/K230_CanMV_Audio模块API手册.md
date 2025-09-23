# `音频`模块 API 手册

## 概述

本手册旨在详细介绍 CanMV 音频模块，指导开发人员如何通过调用 Python API 接口实现音频的采集与播放功能。

## API 介绍

### wave

`wave` 模块提供了一种简便的方法来读取和处理 WAV 文件。

- `wave.open` 函数可以打开 WAV 文件并返回相应的类对象。
- `wave.Wave_read` 类提供获取 WAV 文件的元数据（如采样率、采样点、声道数和采样精度）以及从文件读取 WAV 音频数据的方法。
- `wave.Wave_write` 类提供设置 WAV 文件的元数据（如采样率、采样点、声道数和采样精度）以及保存 PCM 音频数据到 WAV 文件的方法。

该模块与 `pyaudio` 模块结合使用，可以轻松实现 WAV 文件音频的播放与采集及保存 WAV 音频文件。

#### open

**描述**

打开 WAVE 文件，以读取或写入音频数据。

**语法**

```python
open(f, mode=None)
```

**参数**

| 参数名称 | 描述             | 输入 / 输出 |
|----------|------------------|-----------|
| f        | 文件名称         | 输入      |
| mode     | 打开模式 ('r', 'rb', 'w', 'wb') | 输入 |

**返回值**

| 返回值                         | 描述       |
|--------------------------------|------------|
| Wave_read 或 Wave_write 类对象   | 成功       |
| 其他                           | 失败，抛出异常 |

#### wave.Wave_read

`Wave_read` 类提供获取 WAV 文件的元数据（如采样率、采样点、声道数和采样精度）以及从文件读取 WAV 音频数据的方法。

##### get_channels

**描述**

获取声道数。

**语法**

```python
get_channels()
```

**参数**

无

**返回值**

| 返回值 | 描述       |
|--------|------------|
| >0     | 成功       |
| 0      | 失败       |

##### get_sampwidth

**描述**

获取采样字节长度。

**语法**

```python
get_sampwidth()
```

**参数**

无

**返回值**

| 返回值                                     | 描述       |
|--------------------------------------------|------------|
| >0 （有效范围 [1, 2, 3, 4] 分别对应采样精度 [8, 16, 24, 32]） | 成功       |
| 0                                          | 失败       |

##### get_framerate

**描述**

获取采样频率。

**语法**

```python
get_framerate()
```

**参数**

无

**返回值**

| 返回值             | 描述       |
|--------------------|------------|
| >0 （有效范围 (8000~192000)） | 成功       |
| 0                  | 失败       |

##### read_frames

**描述**

读取帧数据。

**语法**

```python
read_frames(nframes)
```

**参数**

| 参数名称 | 描述                                        | 输入 / 输出 |
|----------|---------------------------------------------|-----------|
| nframes  | 读取的帧长度（声道数 × 每个采样点的采样精度 / 8 ） | 输入      |

**返回值**

| 返回值         | 描述       |
|----------------|------------|
| bytes 字节序列  |            |

#### wave.Wave_write

`Wave_write` 类提供设置 WAV 文件的元数据（如采样率、采样点、声道数和采样精度）以及保存 PCM 音频数据到 WAV 文件的方法。

##### set_channels

**描述**

设置声道数。

**语法**

```python
set_channels(nchannels)
```

**参数**

| 参数名称   | 描述    | 输入 / 输出 |
|------------|---------|-----------|
| nchannels  | 声道数  | 输入      |

**返回值**

无

##### set_sampwidth

**描述**

设置采样字节长度。

**语法**

```python
set_sampwidth(sampwidth)
```

**参数**

| 参数名称  | 描述                                                  | 输入 / 输出 |
|-----------|-------------------------------------------------------|-----------|
| sampwidth | 采样字节长度，有效范围 [1, 2, 3, 4] 分别对应采样精度 [8, 16, 24, 32] | 输入      |

**返回值**

无

##### set_framerate

**描述**

设置采样频率。

**语法**

```python
set_framerate(framerate)
```

**参数**

| 参数名称   | 描述             | 输入 / 输出 |
|------------|------------------|-----------|
| framerate  | 采样频率 [8000~192000] | 输入      |

**返回值**

无

##### write_frames

**描述**

写入音频数据。

**语法**

```python
write_frames(data)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| data     | 音频数据（ bytes 字节序列） | 输入      |

**返回值**

无

### pyaudio

`pyaudio` 模块用于音频处理，负责采集和播放二进制 PCM 音频数据。如需播放 WAV 格式文件或将采集到的数据保存为 WAV 文件，需与 `wave` 库结合使用，详见 [示例程序](#示例程序) 部分。

#### pyaudio.PyAudio

负责管理多路音频输入和输出通路，每路通路均以流（ Stream）类对象体现。

##### open

**描述**

打开一路流（ Stream）。

**语法**

```python
open(*args, **kwargs)
```

**参数**

可变参数，参考 [`Stream.__init__`]。

**返回值**

| 返回值               | 描述       |
|----------------------|------------|
| py:class:`Stream`    | 成功       |
| 其他                 | 失败，抛出异常 |

##### close

**描述**

关闭一路流（ Stream）。

**语法**

```python
close(stream)
```

**参数**

无

**返回值**

无

**注意**

该函数会调用 Stream 对象中的 `close` 方法，并将 Stream 对象从 PyAudio 对象中删除。因此，该函数可以不调用，直接调用 Stream.close 方法即可。

##### terminate

**描述**

释放音频资源。在 PyAudio 不再使用时，一定要调用该函数以释放音频资源。如在默认构造函数中申请了 vb block，则应在该函数中释放 vb block。

**语法**

```python
terminate()
```

**参数**

无

**返回值**

无

**注意**

该函数会调用 Stream 对象中的 `close` 方法，并将 Stream 对象从 PyAudio 对象中删除。因此，该函数可以不调用，直接调用 Stream.close 方法即可。

#### pyaudio.Stream

`Stream` 类对象用于管理一路音频输入或输出通路。

##### `__init__`

**描述**

构造函数。

**语法**

```python
__init__(
            PA_manager,
            rate,
            channels,
            format,
            input=False,
            output=False,
            input_device_index=None,
            output_device_index=None,
            enable_codec=True,
            frames_per_buffer=1024,
            start=True,
            stream_callback=None)
```

**参数**

| 参数名称                | 描述                                    | 输入 / 输出 |
|-------------------------|-----------------------------------------|-----------|
| PA_manager              | PyAudio 类对象                          | 输入      |
| rate                    | 采样率                                  | 输入      |
| channels                | 声道数                                  | 输入      |
| format                  | 采样点字节数                            | 输入      |
| input                   | 是否为音频输入，默认值为 False         | 输入      |
| output                  | 是否为音频输出，默认值为 False        | 输入      |
| input_device_index      | 输入通路索引 [0,1]，默认值为 None（使用默认通路 0）。0：I2S 通路（由 enable_codec 决定具体链路：启用时为内置音频 codec 的模拟通路，禁用时为 I2S 数字通路）；1：PDM 数字通路 | 输入      |
| output_device_index     | 输出通路索引 [0,1]，默认值为 None（使用默认通路 0）。0：I2S 通路（由 enable_codec 决定具体链路：启用时为内置音频 codec 的模拟通路，禁用时为 I2S 数字通路）；1：固定为 I2S 数字通路 | 输入      |
| enable_codec            | 是否启用内置音频codec，默认值为 True            | 输入      |
| frames_per_buffer       | 每个缓冲区的帧数                        | 输入      |
| start                   | 是否立即启动，默认值为 True            | 输入      |
| stream_callback         | 输入 / 输出回调函数                       | 输入      |

**返回值**

无

##### start_stream

**描述**

启动流。

**语法**

```python
start_stream()
```

**参数**

无

**返回值**

无

##### stop_stream

**描述**

停止流。

**语法**

```python
stop_stream()
```

**参数**

无

**返回值**

无

##### read

**描述**

读取音频数据。

**语法**

```python
read(frames)
```

**参数**

| 参数名称 | 描述       | 输入 / 输出 |
|----------|------------|-----------|
| frames   | 帧数       | 输入      |

**返回值**

| 返回值         | 描述       |
|----------------|------------|
| bytes          | 读取的音频数据 |

##### write

**描述**

写入音频数据。

**语法**

```python
write(data)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| data     | 音频数据（ bytes 字节序列） | 输入      |

**返回值**

无

##### volume

**描述**

获取或设置音量。

**语法**

```python
volume(vol = None, channel = LEFT_RIGHT)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| vol     | 设置音量值 | 输入      |
| channel     | 声道选择：LEFT(左声道)，RIGHT(右声道)，LEFT_RIGHT(左右声道) | 输入      |

**返回值**

设置音量时，返回值：无
获取音量时，返回值：‌tuple

##### enable_audio3a

**描述**

使能音频3a。

**语法**

```python
enable_audio3a(audio3a_value)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| audio3a_value     | 音频3a使能项：AUDIO_3A_ENABLE_ANS（音频降噪），UDIO_3A_ENABLE_AGC（自动增益），AUDIO_3A_ENABLE_AEC（回声抑制） | 输入      |

**返回值**

无

##### audio3a_send_far_echo_frame

**描述**

发送远端参考语音（即近端扬声器播放的语音），仅在音频3a中回声抑制（AEC）场景使用。

**语法**

```python
audio3a_send_far_echo_frame(frame_data,data_len)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| frame_data     | 远端参考语音数据（ bytes 字节序列） | 输入      |
| data_len     | 数据长度 | 输入      |

**返回值**

无

## 示例程序

### 采集音频并保存为 WAV 文件示例

```python
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

        stream.volume(vol=70, channel=LEFT)
        stream.volume(vol=85, channel=RIGHT)
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

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("音频示例开始")
    record_audio('/sdcard/examples/test.wav', 5)  # 录制WAV文件
```

### 播放 WAV 文件示例

```python
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

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("音频示例开始")
    play_audio('/sdcard/examples/test.wav')  # 播放WAV文件
```

## 总结

通过本手册，开发者可以轻松地利用 CanMV 音频模块实现音频的播放与采集功能。该模块结合了 `wave` 和 `pyaudio` 库的优势，提供了便捷的接口和清晰的 API 文档，便于快速开发和应用音频相关项目。
