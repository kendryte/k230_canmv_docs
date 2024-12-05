# 3.3 `音频`模块 API 手册

## 1. 概述

本手册旨在详细介绍 CanMV 音频模块，指导开发人员如何通过调用 Python API 接口实现音频的采集与播放功能。

## 2. API 介绍

### 2.1 mpp.wave

`wave` 模块提供了一种简便的方法来读取和处理 WAV 文件。使用 `wave.open` 函数可以打开 WAV 文件并返回相应的类对象。

- `wave.Wave_read` 类提供获取 WAV 文件的元数据（如采样率、采样点、声道数和采样精度）以及从文件读取 WAV 音频数据的方法。
- `wave.Wave_write` 类提供设置 WAV 文件的元数据（如采样率、采样点、声道数和采样精度）以及保存 PCM 音频数据到 WAV 文件的方法。

该模块与 `pyaudio` 模块结合使用，可以轻松实现 WAV 文件音频的播放与采集及保存 WAV 音频文件。

#### 2.1.1 open

**描述**

打开 WAVE 文件，以读取或写入音频数据。

**语法**

```python
def open(f, mode=None)
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

#### 2.1.2 wave.Wave_read

`Wave_read` 类提供获取 WAV 文件的元数据（如采样率、采样点、声道数和采样精度）以及从文件读取 WAV 音频数据的方法。

##### 2.1.2.1 get_channels

**描述**

获取声道数。

**语法**

```python
def get_channels(self)
```

**参数**

无

**返回值**

| 返回值 | 描述       |
|--------|------------|
| >0     | 成功       |
| 0      | 失败       |

##### 2.1.2.2 get_sampwidth

**描述**

获取采样字节长度。

**语法**

```python
def get_sampwidth(self)
```

**参数**

无

**返回值**

| 返回值                                     | 描述       |
|--------------------------------------------|------------|
| >0 （有效范围 [1, 2, 3, 4] 分别对应采样精度 [8, 16, 24, 32]） | 成功       |
| 0                                          | 失败       |

##### 2.1.2.3 get_framerate

**描述**

获取采样频率。

**语法**

```python
def get_framerate(self)
```

**参数**

无

**返回值**

| 返回值             | 描述       |
|--------------------|------------|
| >0 （有效范围 (8000~192000)） | 成功       |
| 0                  | 失败       |

##### 2.1.2.4 read_frames

**描述**

读取帧数据。

**语法**

```python
def read_frames(self, nframes)
```

**参数**

| 参数名称 | 描述                                        | 输入 / 输出 |
|----------|---------------------------------------------|-----------|
| nframes  | 读取的帧长度（声道数 × 每个采样点的采样精度 / 8 ） | 输入      |

**返回值**

| 返回值         | 描述       |
|----------------|------------|
| bytes 字节序列  |            |

#### 2.1.3 wave.Wave_write

`Wave_write` 类提供设置 WAV 文件的元数据（如采样率、采样点、声道数和采样精度）以及保存 PCM 音频数据到 WAV 文件的方法。

##### 2.1.3.1 set_channels

**描述**

设置声道数。

**语法**

```python
def set_channels(self, nchannels)
```

**参数**

| 参数名称   | 描述    | 输入 / 输出 |
|------------|---------|-----------|
| nchannels  | 声道数  | 输入      |

**返回值**

无

##### 2.1.3.2 set_sampwidth

**描述**

设置采样字节长度。

**语法**

```python
def set_sampwidth(self, sampwidth)
```

**参数**

| 参数名称  | 描述                                                  | 输入 / 输出 |
|-----------|-------------------------------------------------------|-----------|
| sampwidth | 采样字节长度，有效范围 [1, 2, 3, 4] 分别对应采样精度 [8, 16, 24, 32] | 输入      |

**返回值**

无

##### 2.1.3.3 set_framerate

**描述**

设置采样频率。

**语法**

```python
def set_framerate(self, framerate)
```

**参数**

| 参数名称   | 描述             | 输入 / 输出 |
|------------|------------------|-----------|
| framerate  | 采样频率 [8000~192000] | 输入      |

**返回值**

无

##### 2.1.3.4 write_frames

**描述**

写入音频数据。

**语法**

```python
def write_frames(self, data)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| data     | 音频数据（ bytes 字节序列） | 输入      |

**返回值**

无

### 2.2 mpp.pyaudio

`pyaudio` 模块用于音频处理，负责采集和播放二进制 PCM 音频数据。如需播放 WAV 格式文件或将采集到的数据保存为 WAV 文件，需与 `mpp.wave` 库结合使用，详见 [示例程序](#3-示例程序) 部分。

#### 2.2.1 pyaudio.PyAudio

负责管理多路音频输入和输出通路，每路通路均以流（ Stream）类对象体现。

##### 2.2.1.1 open

**描述**

打开一路流（ Stream）。

**语法**

```python
def open(self, *args, **kwargs)
```

**参数**

可变参数，参考 [`Stream.__init__`]。

**返回值**

| 返回值               | 描述       |
|----------------------|------------|
| py:class:`Stream`    | 成功       |
| 其他                 | 失败，抛出异常 |

##### 2.2.1.2 close

**描述**

关闭一路流（ Stream）。

**语法**

```python
def close(self, stream)
```

**参数**

无

**返回值**

无

**注意**

该函数会调用 Stream 对象中的 `close` 方法，并将 Stream 对象从 PyAudio 对象中删除。因此，该函数可以不调用，直接调用 Stream.close 方法即可。

##### 2.2.1.3 terminate

**描述**

释放音频资源。在 PyAudio 不再使用时，一定要调用该函数以释放音频资源。如在默认构造函数中申请了 vb block，则应在该函数中释放 vb block。

**语法**

```python
def terminate(self)
```

**参数**

无

**返回值**

无

**注意**

该函数会调用 Stream 对象中的 `close` 方法，并将 Stream 对象从 PyAudio 对象中删除。因此，该函数可以不调用，直接调用 Stream.close 方法即可。

#### 2.2.2 pyaudio.Stream

`Stream` 类对象用于管理一路音频输入或输出通路。

##### 2.2.2.1 `__init__`

**描述**

构造函数。

**语法**

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

**参数**

| 参数名称                | 描述                                    | 输入 / 输出 |
|-------------------------|-----------------------------------------|-----------|
| PA_manager              | PyAudio 类对象                          | 输入      |
| rate                    | 采样率                                  | 输入      |
| channels                | 声道数                                  | 输入      |
| format                  | 采样点字节数                            | 输入      |
| input                   | 是否为音频输入，默认值为 False         | 输入      |
| output                  | 是否为音频输出，默认值为 False        | 输入      |
| input_device_index      | 输入通路索引 [0,1]，默认值为 None（使用默认通路 0 ） | 输入      |
| output_device_index     | 输出通路索引 [0,1]，默认值为 None（使用默认通路 0 ） | 输入      |
| enable_codec            | 是否启用 | |

编码，默认值为 True            | 输入      |
| frames_per_buffer       | 每个缓冲区的帧数                        | 输入      |
| start                   | 是否立即启动，默认值为 True            | 输入      |
| stream_callback         | 输入 / 输出回调函数                       | 输入      |

**返回值**

无

##### 2.2.2.2 start_stream

**描述**

启动流。

**语法**

```python
def start_stream(self)
```

**参数**

无

**返回值**

无

##### 2.2.2.3 stop_stream

**描述**

停止流。

**语法**

```python
def stop_stream(self)
```

**参数**

无

**返回值**

无

##### 2.2.2.4 read

**描述**

读取音频数据。

**语法**

```python
def read(self, frames)
```

**参数**

| 参数名称 | 描述       | 输入 / 输出 |
|----------|------------|-----------|
| frames   | 帧数       | 输入      |

**返回值**

| 返回值         | 描述       |
|----------------|------------|
| bytes          | 读取的音频数据 |

##### 2.2.2.5 write

**描述**

写入音频数据。

**语法**

```python
def write(self, data)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| data     | 音频数据（ bytes 字节序列） | 输入      |

**返回值**

无

##### 2.2.2.6 volume

**描述**

获取或设置音量。

**语法**

```python
def volume(self,vol = None, channel = LEFT_RIGHT)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| vol     | 设置音量值 | 输入      |
| channel     | 声道选择 | 输入      |

**返回值**

设置音量时，返回值：无
获取音量时，返回值：‌tuple

##### 2.2.2.7 enable_audio3a

**描述**

使能音频3a。

**语法**

```python
def enable_audio3a(self, audio3a_value)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| audio3a_value     | 音频3a使能项：AUDIO_3A_ENABLE_ANS（音频降噪），UDIO_3A_ENABLE_AGC（自动增益），AUDIO_3A_ENABLE_AEC（回声抑制） | 输入      |

**返回值**

无

##### 2.2.2.8 audio3a_send_far_echo_frame

**描述**

发送远端参考语音（即近端扬声器播放的语音），仅在音频3a中回声抑制（AEC）场景使用。

**语法**

```python
audio3a_send_far_echo_frame(self, frame_data,data_len)
```

**参数**

| 参数名称 | 描述                      | 输入 / 输出 |
|----------|---------------------------|-----------|
| frame_data     | 远端参考语音数据（ bytes 字节序列） | 输入      |
| data_len     | 数据长度 | 输入      |

**返回值**

无

### 3. 示例程序

#### 3.1 播放 WAV 文件示例

```python
import pyaudio
import wave

# 播放 WAV 文件
def play_wav(file_path):
    # 打开 WAV 文件
    wf = wave.open(file_path, 'rb')

    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()

    # 打开流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                     channels=wf.getnchannels(),
                     rate=wf.getframerate(),
                     output=True)

    # 读取数据并播放
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # 关闭流
    stream.stop_stream()
    stream.close()
    p.terminate()
```

#### 3.2 采集音频并保存为 WAV 文件示例

```python
import pyaudio
import wave

# 采集音频并保存为 WAV 文件
def record_wav(file_path, duration):
    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()

    # 打开流
    stream = p.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=44100,
                     input=True,
                     frames_per_buffer=1024)

    frames = []

    # 采集音频数据
    for _ in range(0, int(44100 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    # 停止流
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存为 WAV 文件
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
```

### 4. 总结

通过本手册，开发者可以轻松地利用 CanMV 音频模块实现音频的播放与采集功能。该模块结合了 `wave` 和 `pyaudio` 库的优势，提供了便捷的接口和清晰的 API 文档，便于快速开发和应用音频相关项目。
