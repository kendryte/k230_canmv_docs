# 3.3 Audio Module API Manual

## 1. Overview

This manual aims to provide a detailed introduction to the CanMV audio module, guiding developers on how to achieve audio capture and playback functions by calling the Python API interface.

## 2. API Introduction

### 2.1 mpp.wave

The `wave` module provides a convenient way to read and process WAV files. Using the `wave.open` function, you can open a WAV file and return the corresponding class object.

- The `wave.Wave_read` class provides methods for obtaining metadata from a WAV file (such as sample rate, sample points, number of channels, and sampling precision) and reading WAV audio data from the file.
- The `wave.Wave_write` class provides methods for setting metadata for a WAV file (such as sample rate, sample points, number of channels, and sampling precision) and saving PCM audio data to a WAV file.

This module, when used in conjunction with the `pyaudio` module, can easily achieve the playback and capture of WAV file audio and save WAV audio files.

#### 2.1.1 open

**Description**

Open a WAVE file to read or write audio data.

**Syntax**

```python
def open(f, mode=None)
```

**Parameters**

| Parameter Name | Description                             | Input/Output |
|----------------|-----------------------------------------|--------------|
| f              | File name                               | Input        |
| mode           | Open mode ('r', 'rb', 'w', 'wb')        | Input        |

**Return Value**

| Return Value                  | Description                       |
|-------------------------------|-----------------------------------|
| Wave_read or Wave_write class object | Success                         |
| Others                        | Failure, raises an exception      |

#### 2.1.2 wave.Wave_read

The `Wave_read` class provides methods for obtaining metadata from a WAV file (such as sample rate, sample points, number of channels, and sampling precision) and reading WAV audio data from the file.

##### 2.1.2.1 get_channels

**Description**

Get the number of channels.

**Syntax**

```python
def get_channels(self)
```

**Parameters**

None

**Return Value**

| Return Value | Description |
|--------------|-------------|
| >0           | Success     |
| 0            | Failure     |

##### 2.1.2.2 get_sampwidth

**Description**

Get the sample byte length.

**Syntax**

```python
def get_sampwidth(self)
```

**Parameters**

None

**Return Value**

| Return Value                                     | Description |
|--------------------------------------------------|-------------|
| >0 (Valid range [1, 2, 3, 4] corresponding to sampling precision [8, 16, 24, 32]) | Success     |
| 0                                                | Failure     |

##### 2.1.2.3 get_framerate

**Description**

Get the sample rate.

**Syntax**

```python
def get_framerate(self)
```

**Parameters**

None

**Return Value**

| Return Value             | Description |
|--------------------------|-------------|
| >0 (Valid range (8000~192000)) | Success     |
| 0                        | Failure     |

##### 2.1.2.4 read_frames

**Description**

Read frame data.

**Syntax**

```python
def read_frames(self, nframes)
```

**Parameters**

| Parameter Name | Description                                        | Input/Output |
|----------------|----------------------------------------------------|--------------|
| nframes        | Length of frames to read (number of channels × sampling precision per sample point / 8) | Input        |

**Return Value**

| Return Value  | Description |
|---------------|-------------|
| bytes sequence |             |

#### 2.1.3 wave.Wave_write

The `Wave_write` class provides methods for setting metadata for a WAV file (such as sample rate, sample points, number of channels, and sampling precision) and saving PCM audio data to a WAV file.

##### 2.1.3.1 set_channels

**Description**

Set the number of channels.

**Syntax**

```python
def set_channels(self, nchannels)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| nchannels      | Number of channels | Input        |

**Return Value**

None

##### 2.1.3.2 set_sampwidth

**Description**

Set the sample byte length.

**Syntax**

```python
def set_sampwidth(self, sampwidth)
```

**Parameters**

| Parameter Name | Description                                                  | Input/Output |
|----------------|--------------------------------------------------------------|--------------|
| sampwidth      | Sample byte length, valid range [1, 2, 3, 4] corresponding to sampling precision [8, 16, 24, 32] | Input        |

**Return Value**

None

##### 2.1.3.3 set_framerate

**Description**

Set the sample rate.

**Syntax**

```python
def set_framerate(self, framerate)
```

**Parameters**

| Parameter Name | Description             | Input/Output |
|----------------|--------------------------|--------------|
| framerate      | Sample rate [8000~192000] | Input        |

**Return Value**

None

##### 2.1.3.4 write_frames

**Description**

Write audio data.

**Syntax**

```python
def write_frames(self, data)
```

**Parameters**

| Parameter Name | Description                      | Input/Output |
|----------------|-----------------------------------|--------------|
| data           | Audio data (bytes sequence)      | Input        |

**Return Value**

None

### 2.2 mpp.pyaudio

The `pyaudio` module is used for audio processing, responsible for capturing and playing binary PCM audio data. To play WAV format files or save captured data as WAV files, it needs to be used in conjunction with the `mpp.wave` library, as detailed in the [Example Programs](#3-example-programs) section.

#### 2.2.1 pyaudio.PyAudio

Responsible for managing multiple audio input and output channels, each channel is represented as a Stream class object.

##### 2.2.1.1 open

**Description**

Open a stream.

**Syntax**

```python
def open(self, *args, **kwargs)
```

**Parameters**

Variable parameters, refer to [`Stream.__init__`].

**Return Value**

| Return Value            | Description                       |
|-------------------------|-----------------------------------|
| py:class:`Stream`       | Success                           |
| Others                  | Failure, raises an exception      |

##### 2.2.1.2 close

**Description**

Close a stream.

**Syntax**

```python
def close(self, stream)
```

**Parameters**

None

**Return Value**

None

**Note**

This function will call the `close` method in the Stream object and remove the Stream object from the PyAudio object. Therefore, this function can be omitted, and the Stream.close method can be called directly.

##### 2.2.1.3 terminate

**Description**

Release audio resources. This function must be called to release audio resources when PyAudio is no longer in use. If a vb block is allocated in the default constructor, it should be released in this function.

**Syntax**

```python
def terminate(self)
```

**Parameters**

None

**Return Value**

None

**Note**

This function will call the `close` method in the Stream object and remove the Stream object from the PyAudio object. Therefore, this function can be omitted, and the Stream.close method can be called directly.

#### 2.2.2 pyaudio.Stream

The `Stream` class object is used to manage a single audio input or output channel.

##### 2.2.2.1 `__init__`

**Description**

Constructor.

**Syntax**

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

**Parameters**

| Parameter Name            | Description                                    | Input/Output |
|---------------------------|------------------------------------------------|--------------|
| PA_manager                | PyAudio class object                           | Input        |
| rate                      | Sample rate                                    | Input        |
| channels                  | Number of channels                             | Input        |
| format                    | Sample point byte length                       | Input        |
| input                     | Is it audio input, default is False            | Input        |
| output                    | Is it audio output, default is False           | Input        |
| input_device_index        | Input channel index [0,1], default is None (use default channel 0) | Input        |
| output_device_index       | Output channel index [0,1], default is None (use default channel 0) | Input        |
| enable_codec              | Enable codec, default is True                  | Input        |
| frames_per_buffer         | Frames per buffer                              | Input        |
| start                     | Start immediately, default is True             | Input        |
| stream_callback           | Input/Output callback function                 | Input        |

**Return Value**

None

##### 2.2.2.2 start_stream

**Description**

Start the stream.

**Syntax**

```python
def start_stream(self)
```

**Parameters**

None

**Return Value**

None

##### 2.2.2.3 stop_stream

**Description**

Stop the stream.

**Syntax**

```python
def stop_stream(self)
```

**Parameters**

None

**Return Value**

None

##### 2.2.2.4 read

**Description**

Read audio data.

**Syntax**

```python
def read(self, frames)
```

**Parameters**

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| frames         | Number of frames  | Input        |

**Return Value**

| Return Value  | Description       |
|---------------|-------------------|
| bytes         | Read audio data   |

##### 2.2.2.5 write

**Description**

Write audio data.

**Syntax**

```python
def write(self, data)
```

**Parameters**

| Parameter Name | Description                      | Input/Output |
|----------------|-----------------------------------|--------------|
| data           | Audio data (bytes sequence)      | Input        |

**Return Value**

None

### 3. Example Programs

#### 3.1 Example of Playing a WAV File

```python
import pyaudio
import wave

# Play a WAV file
def play_wav(file_path):
    # Open the WAV file
    wf = wave.open(file_path, 'rb')

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                     channels=wf.getnchannels(),
                     rate=wf.getframerate(),
                     output=True)

    # Read data and play
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
```

#### 3.2 Example of Capturing Audio and Saving as a WAV File

```python
import pyaudio
import wave

# Capture audio and save as a WAV file
def record_wav(file_path, duration):
    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=44100,
                     input=True,
                     frames_per_buffer=1024)

    frames = []

    # Capture audio data
    for _ in range(0, int(44100 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    # Stop the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save as a WAV file
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
```

### 4. Summary

Through this manual, developers can easily use the CanMV audio module to achieve audio playback and capture functions. This module combines the advantages of the `wave` and `pyaudio` libraries, providing convenient interfaces and clear API documentation, making it easy to quickly develop and apply audio-related projects.
