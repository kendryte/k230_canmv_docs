# `Audio` Module API Manual

## Overview

This manual aims to provide a detailed introduction to the CanMV audio module, guiding developers on how to implement audio capture and playback functionality by calling Python API interfaces.

## API Introduction

### wave

The `wave` module provides a simple way to read and process WAV files.

- The `wave.open` function can open a WAV file and return the corresponding class object.
- The `wave.Wave_read` class provides methods to obtain metadata of a WAV file (such as sample rate, sample points, number of channels, and sample precision) and to read WAV audio data from the file.
- The `wave.Wave_write` class provides methods to set metadata of a WAV file (such as sample rate, sample points, number of channels, and sample precision) and to save PCM audio data to a WAV file.

When used in combination with the `pyaudio` module, this module can easily implement playback and capture of WAV file audio, as well as saving WAV audio files.

#### open

**Description**

Opens a WAVE file for reading or writing audio data.

**Syntax**

```python
open(f, mode=None)
```

**Parameters**

| Parameter Name | Description                              | Input / Output |
|----------|------------------------------------------|-----------|
| f        | File name                                | Input     |
| mode     | Open mode ('r', 'rb', 'w', 'wb')        | Input     |

**Return Value**

| Return Value                          | Description        |
|---------------------------------------|--------------------|
| Wave_read or Wave_write class object  | Success            |
| Other                                 | Failure, raises exception |

#### wave.Wave_read

The `Wave_read` class provides methods to obtain metadata of a WAV file (such as sample rate, sample points, number of channels, and sample precision) and to read WAV audio data from the file.

##### get_channels

**Description**

Gets the number of channels.

**Syntax**

```python
get_channels()
```

**Parameters**

None

**Return Value**

| Return Value | Description |
|--------|------------|
| >0     | Success     |
| 0      | Failure     |

##### get_sampwidth

**Description**

Gets the sample width in bytes.

**Syntax**

```python
get_sampwidth()
```

**Parameters**

None

**Return Value**

| Return Value                                     | Description |
|-------------------------------------------------|------------|
| >0 (valid range [1, 2, 3, 4] corresponding to sample precision [8, 16, 24, 32]) | Success     |
| 0                                               | Failure     |

##### get_framerate

**Description**

Gets the sample rate.

**Syntax**

```python
get_framerate()
```

**Parameters**

None

**Return Value**

| Return Value             | Description |
|--------------------------|------------|
| >0 (valid range (8000~192000)) | Success     |
| 0                        | Failure     |

##### read_frames

**Description**

Reads frame data.

**Syntax**

```python
read_frames(nframes)
```

**Parameters**

| Parameter Name | Description                                        | Input / Output |
|----------|---------------------------------------------|-----------|
| nframes  | Number of frames to read (number of channels × sample precision per sample point / 8 ) | Input     |

**Return Value**

| Return Value         | Description |
|----------------------|-------------|
| bytes byte sequence  |             |

#### wave.Wave_write

The `Wave_write` class provides methods to set metadata for WAV files (such as sample rate, sample points, number of channels, and sample precision) and to save PCM audio data to WAV files.

##### set_channels

**Description**

Set the number of channels.

**Syntax**

```python
set_channels(nchannels)
```

**Parameters**

| Parameter Name | Description       | Input / Output |
|----------------|-------------------|----------------|
| nchannels      | Number of channels | Input         |

**Return Value**

None

##### set_sampwidth

**Description**

Set the sample byte width.

**Syntax**

```python
set_sampwidth(sampwidth)
```

**Parameters**

| Parameter Name | Description                                                              | Input / Output |
|----------------|--------------------------------------------------------------------------|----------------|
| sampwidth      | Sample byte width, valid range [1, 2, 3, 4] corresponding to sample precision [8, 16, 24, 32] | Input         |

**Return Value**

None

##### set_framerate

**Description**

Set the sample rate.

**Syntax**

```python
set_framerate(framerate)
```

**Parameters**

| Parameter Name | Description                | Input / Output |
|----------------|----------------------------|----------------|
| framerate      | Sample rate [8000~192000]  | Input          |

**Return Value**

None

##### write_frames

**Description**

Write audio data.

**Syntax**

```python
write_frames(data)
```

**Parameters**

| Parameter Name | Description                        | Input / Output |
|----------------|------------------------------------|----------------|
| data           | Audio data (bytes byte sequence)   | Input          |

**Return Value**

None

### pyaudio

The `pyaudio` module is used for audio processing, responsible for capturing and playing binary PCM audio data. To play WAV format files or save captured data as WAV files, it needs to be used in combination with the `wave` library. See the [Examples](#examples) section for details.

#### pyaudio.PyAudio

Responsible for managing multiple audio input and output channels, each channel is represented as a Stream object.

##### open

**Description**

Open a Stream.

**Syntax**

```python
open(*args, **kwargs)
```

**Parameters**

Variable parameters, refer to [`Stream.__init__`].

**Return Value**

| Return Value          | Description |
|----------------------|-------------|
| py:class:`Stream`    | Success     |
| Other                | Failure, throws an exception |

##### close

**Description**

Close a Stream.

**Syntax**

```python
close(stream)
```

**Parameters**

None

**Return Value**

None

**Note**

This function will call the `close` method in the Stream object and remove the Stream object from the PyAudio object. Therefore, this function does not need to be called, you can directly call the Stream.close method.

##### terminate

**Description**

Release audio resources. When PyAudio is no longer used, this function must be called to release audio resources. If a vb block is applied for in the default constructor, the vb block should be released in this function.

**Syntax**

```python
terminate()
```

**Parameters**

None

**Return Value**

None

**Note**

This function will call the `close` method in the Stream object and remove the Stream object from the PyAudio object. Therefore, this function does not need to be called, you can directly call the Stream.close method.

#### pyaudio.Stream

The `Stream` class object is used to manage an audio input or output path.

##### `__init__`

**Description**

Constructor.

**Syntax**

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

**Parameters**

| Parameter Name          | Description                                                                                                                                                                                                                                                                                          | Input / Output |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| PA_manager              | PyAudio class object                                                                                                                                                                                                                                                                                 | Input          |
| rate                    | Sampling rate                                                                                                                                                                                                                                                                                        | Input          |
| channels                | Number of channels                                                                                                                                                                                                                                                                                   | Input          |
| format                  | Sample size in bytes                                                                                                                                                                                                                                                                                 | Input          |
| input                   | Whether it is an audio input, default value is False                                                                                                                                                                                                                                                | Input          |
| output                  | Whether it is an audio output, default value is False                                                                                                                                                                                                                                               | Input          |
| input_device_index      | Input path index [0,1], default value is None (use the default path 0). 0: I2S path (the specific link is determined by enable_codec: when enabled, it is the analog path of the built-in audio codec; when disabled, it is the I2S digital path); 1: PDM digital path                       | Input          |
| output_device_index     | Output path index [0,1], default value is None (use the default path 0). 0: I2S path (the specific link is determined by enable_codec: when enabled, it is the analog path of the built-in audio codec; when disabled, it is the I2S digital path); 1: fixed as I2S digital path                | Input          |
| enable_codec            | Whether to enable the built-in audio codec, default value is True                                                                                                                                                                                                                                    | Input          |
| frames_per_buffer       | Number of frames per buffer                                                                                                                                                                                                                                                                          | Input          |
| start                   | Whether to start immediately, default value is True                                                                                                                                                                                                                                                 | Input          |
| stream_callback         | Input / output callback function                                                                                                                                                                                                                                                                     | Input          |

**Return Value**

None

##### start_stream

**Description**

Start the stream.

**Syntax**

```python
start_stream()
```

**Parameters**

None

**Return Value**

None

##### stop_stream

**Description**

Stop the stream.

**Syntax**

```python
stop_stream()
```

**Parameters**

None

**Return Value**

None

##### read

**Description**

Read audio data.

**Syntax**

```python
read(frames)
```

**Parameters**

| Parameter Name | Description | Input / Output |
|----------------|-------------|----------------|
| frames         | Number of frames | Input      |

**Return Value**

| Return Value  | Description      |
|---------------|------------------|
| bytes         | The read audio data |

##### write

**Description**

Write audio data.

**Syntax**

```python
write(data)
```

**Parameters**

| Parameter Name | Description                          | Input / Output |
|----------------|--------------------------------------|----------------|
| data           | Audio data (bytes byte sequence)     | Input          |

**Return Value**

None

##### volume

**Description**

Get or set the volume.

**Syntax**

```python
volume(vol = None, channel = LEFT_RIGHT)
```

**Parameters**

| Parameter Name | Description                                                                                            | Input / Output |
|----------------|--------------------------------------------------------------------------------------------------------|----------------|
| vol            | Volume value to set                                                                                    | Input          |
| channel        | Channel selection: LEFT (left channel), RIGHT (right channel), LEFT_RIGHT (left and right channels)     | Input          |

**Return Value**

When setting the volume, return value: None
When getting the volume, return value: tuple

##### enable_audio3a

**Description**

Enable audio 3a.

**Syntax**

```python
enable_audio3a(audio3a_value)
```

**Parameters**

| Parameter Name | Description                                                                                                                                                                        | Input / Output |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| audio3a_value  | Audio 3a enable items: AUDIO_3A_ENABLE_ANS (audio noise suppression), UDIO_3A_ENABLE_AGC (automatic gain control), AUDIO_3A_ENABLE_AEC (echo cancellation)                            | Input          |

**Return Value**

None

##### audio3a_send_far_echo_frame

**Description**

Send the far-end reference audio (i.e., the audio played by the near-end speaker), only used in the echo cancellation (AEC) scenario in audio 3a.

**Syntax**

```python
audio3a_send_far_echo_frame(frame_data,data_len)
```

**Parameters**

| Parameter Name | Description                                       | Input / Output |
|----------------|---------------------------------------------------|----------------|
| frame_data     | Far-end reference audio data (bytes byte sequence) | Input          |
| data_len       | Data length                                       | Input          |

**Return Value**

None

<a id="examples"></a>

## Example Programs

### Audio Capture and Save as WAV File Example

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

### Play WAV File Example

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

## Summary

Through this manual, developers can easily utilize the CanMV audio module to implement audio playback and capture functionality. This module combines the advantages of the `wave` and `pyaudio` libraries, providing convenient interfaces and clear API documentation, facilitating rapid development and application of audio-related projects.
