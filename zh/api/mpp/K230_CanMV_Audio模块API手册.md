# 3.3 Audio 模块API手册

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

此文档介绍CanMV音频模块，用以指导开发人员如何调用python api接口实现音频采集及播放功能。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| media  | k230 media包,包含多媒体相关模块   |
| media.pyaudio  | 音频处理模块   |
| media.wave  | wav文件处理模块   |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 孙小朋      | 2023-09-18 |
| V1.1       | 修改audio模块内存分配方式:所有模块统一由media.media分配内存，详见[示例程序](#3-示例程序)中的修改:media.buffer_init()  | 孙小朋      | 2023/10/12 |

## 1. 概述

此文档介绍CanMV音频模块，用以指导开发人员如何调用python api接口实现音频采集及播放功能。

## 2. API描述

### 2.1 mpp.wave

wave模块提供了一种简单的方式来读取和处理WAV文件。使用wave.open函数可以打开wav文件并返回以下类对象。
wave.Wave_read类提供获取WAV文件的元数据（如采样率、采样点、声道和采样精度）及从文件读取wav音频数据方法。
wave.Wave_write类提供设置WAV文件的元数据（如采样率、采样点、声道和采样精度）及保存pcm音频数据到wav文件的方法。
该模块与pyaudio模块配合会很容易实现播放wav文件音频和采集并保存wav音频文件。

#### 2.1.1 open

【描述】

打开wave文件，用以读取或写入音频数据。

【语法】

```python
def open(f, mode=None)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| f  | 文件名称         | 输入      |
| mode  | 打开模式('r','rb','w','wb')         | 输入 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| Wave_read或Wave_write类对象 | 成功。                          |
| 其他    | 失败，抛出异常 |

#### 2.1.2 wave.Wave_read

Wave_read类提供获取WAV文件的元数据（如采样率、采样点、声道和采样精度）及从文件读取wav音频数据方法。

##### 2.1.2.1 get_channels

【描述】

获取声道数。

【语法】

```python
def get_channels(self)
```

【参数】

无

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| >0 | 成功。                          |
| 0  | 失败 |

##### 2.1.2.2 get_sampwidth

【描述】

获取采样字节长度。

【语法】

```python
def get_sampwidth(self)
```

【参数】

无

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| >0 有效范围[1,2,3,4]分别对应采样精度[8,16,24,32]| 成功。                          |
| 0  | 失败 |

##### 2.1.2.2 get_framerate

【描述】

获取采样频率。

【语法】

```python
def get_framerate(self)
```

【参数】

无

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| >0 有效范围(8000~192000)| 成功。                          |
| 0  | 失败 |

##### 2.1.2.3 read_frames

【描述】

读取帧数据。

【语法】

```python
def read_frames(self, nframes)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| nframes  | 读取的帧长度(声道数*每个采样点的采样精度/8)         | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| bytes字节序列 |                           |

#### 2.1.3 wave.Wave_write

Wave_write为类对象，提供设置WAV文件的元数据（如采样率、采样点、声道和采样精度）及保存pcm音频数据到wav文件的方法。

##### 2.1.3.1 set_channels

【描述】

设置声道数。

【语法】

```python
def set_channels(self, nchannels)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| nchannels  | 声道数         | 输入      |

【返回值】

无

##### 2.1.3.2 set_sampwidth

【描述】

设置采样字节长度。

【语法】

```python
def set_sampwidth(self, sampwidth)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| sampwidth  | 采样字节长度，有效范围[1,2,3,4]分别对应采样精度[8,16,24,32]        | 输入      |

【返回值】

无

##### 2.1.3.3 set_framerate

【描述】

设置采样频率。

【语法】

```python
def set_framerate(self, framerate)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| framerate  | 采样频率[8000~192000]      | 输入      |

【返回值】

无

##### 2.1.3.4 write_frames

【描述】

写入音频数据。

【语法】

```python
def write_frames(self, data)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| data  | 音频数据（bytes字节序列）      | 输入      |

【返回值】

无

### 2.2 mpp.pyaudio

pyaudio为音频处理模块，负责采集和播放二进制pcm音频数据。如想播放wav格式文件或将采集到的数据保存成wav文件，需与mpp.wave库配合使用，详见[示例程序](#3-示例程序)部分。

#### 2.2.1 pyaudio.PyAudio

负责管理多路音频输入和输出通路，每路通路均以流(Stream)类对象体现。

##### 2.2.1.1 open

【描述】

打开一路流（Stream）。

【语法】

```python
def open(self, *args, **kwargs)
```

【参数】

可变参数，参考[Stream.\_\_init__]。

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| py:class:`Stream` | 成功。                          |
| 其他    | 失败，抛出异常 |

##### 2.2.1.2 close

【描述】

关闭一路流（Stream）。

【语法】

```python
def close(self, stream)
```

【参数】

无

【返回值】

无

【注意】

该函数会调用Stream对象中的close,并把Stream对象从PyAudio对象中删除。因此该函数可以不调用，调用Stream.close即可。

##### 2.2.1.3 terminate

【描述】

释放音频资源，PyAudio不再使用时，一定要调用该函数释放音频资源。如在:默认构造函数中申请vb block，在该函数中释放vb block。

【语法】

```python
def terminate(self)
```

【参数】

无

【返回值】

无

【注意】

该函数会调用Stream对象中的close,并把Stream对象从PyAudio对象中删除。因此该函数可以不调用，调用Stream.close即可。

#### 2.2.2 pyaudio.Stream

Stream为音频流类对象，负责管理一路音频输入或输出通路。

##### 2.2.2.1 \_\_init__

【描述】

构造函数。

【语法】

```python
def __init__(self,
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

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| PA_manager  |       PyAudio类对象      | 输入  |
| rate  |       采样率      | 输入  |
| channels  |       声道数      | 输入  |
| format  |       采样点字节数      | 输入  |
| input  |       是否是音频输入，默认值为False        | 输入  |
| output  |       是否是音频输出，默认值为False      | 输入  |
| input_device_index  |       输入通路组号[0,1]，默认值为None：使用默认通路0     | 输入  |
| output_device_index  |       输出通路组号[0,1]，默认值为None：使用默认通路0     | 输入  |
| enable_codec  |     是否启用内置codec，默认使用内置codec| 输入  |
| frames_per_buffer  |      每次采集帧数| 输入  |
| start  |      是否启动数据流，默认启动| 输入  |
| stream_callback  | 以回调方式写入或读取数据，默认不启用回调方式| 输入  |

【返回值】

无

##### 2.2.2.2 start_stream

【描述】

启动数据流。如构造函数中设置参数start=True，则创建Stream对象后默认就启动数据流。

【语法】

```python
def start_stream(self)
```

【参数】

无

【返回值】

无

##### 2.2.2.3 stop_stream

【描述】

停止数据流。停止数据流后可再次重新启动数据流。

【语法】

```python
def stop_stream(self)
```

【参数】

无

【返回值】

无

##### 2.2.2.4 write

【描述】

写入数据流，用来播放音频。如以回调方式写入数据流，则该函数不需要调用。

【语法】

```python
def write(self, frames,num_frames=None)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| frames  |   音频数据（bytes字节序列）     | 输入      |
| num_frames  |  写入帧数量，默认值为None:会根绝frames自动计算帧长度      | 输入    |

【返回值】

无

##### 2.2.2.5 read

【描述】

读取数据流，用来采集音频。如以回调方式读取数据流，则该函数不需要调用。

【语法】

```python
def read(self, num_frames)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| num_frames  |  读取帧数量    |     输入  |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| bytes字节序列 长度>0 |        成功                   |
| bytes字节序列 长度=0 |        失败                   |

##### 2.2.2.6 close

【描述】

关闭数据流。会从PyAudio对象中删除该对象。

【语法】

```python
def close(self)
```

【参数】

无

【返回值】

无

## 3. 示例程序

### 3.1 采集wav音频

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

record_audio('/sdcard/app/output.wav', 15)
```

### 3.2 播放wav音频

```python
import os
from media.media import *   #导入media模块，用于初始化vb buffer
from media.pyaudio import * #导入pyaudio模块，用于采集和播放音频
import media.wave as wave   #导入wav模块，用于保存和加载wav音频文件

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

play_audio('/sdcard/app/input.wav')
```

### 3.3 采集播放回环

```python
import os
from media.media import *   #导入media模块，用于初始化vb buffer
from media.pyaudio import * #导入pyaudio模块，用于采集和播放音频
import media.wave as wave   #导入wav模块，用于保存和加载wav音频文件

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

loop_audio(15)
```
