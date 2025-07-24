# `Audio` Module API Manual

## Overview

This manual aims to provide a detailed introduction to the CanMV audio module, guiding developers on how to achieve audio capture and playback functions by calling the Python API interface.

## API Introduction

### wave

The `wave` module provides a convenient way to read and process WAV files.

- The `wave.open` function can open a WAV file and return the corresponding class object.
- The `wave.Wave_read` class provides methods for obtaining metadata from a WAV file (such as sample rate, sample points, number of channels, and sampling precision) and reading WAV audio data from the file.
- The `wave.Wave_write` class provides methods for setting metadata for a WAV file (such as sample rate, sample points, number of channels, and sampling precision) and saving PCM audio data to a WAV file.

This module, when used in conjunction with the `pyaudio` module, can easily achieve the playback and capture of WAV file audio and save WAV audio files.

#### open

**Description**

Open a WAVE file to read or write audio data.

**Syntax**

```python
open(f, mode=None)
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

#### wave.Wave_read

The `Wave_read` class provides methods for obtaining metadata from a WAV file (such as sample rate, sample points, number of channels, and sampling precision) and reading WAV audio data from the file.

##### get_channels

**Description**

Get the number of channels.

**Syntax**

```python
get_channels()
```

**Parameters**

None

**Return Value**

| Return Value | Description |
|--------------|-------------|
| >0           | Success     |
| 0            | Failure     |

##### get_sampwidth

**Description**

Get the sample byte length.

**Syntax**

```python
get_sampwidth()
```

**Parameters**

None

**Return Value**

| Return Value                                     | Description |
|--------------------------------------------------|-------------|
| >0 (Valid range [1, 2, 3, 4] corresponding to sampling precision [8, 16, 24, 32]) | Success     |
| 0                                                | Failure     |

##### get_framerate

**Description**

Get the sample rate.

**Syntax**

```python
get_framerate()
```

**Parameters**

None

**Return Value**

| Return Value             | Description |
|--------------------------|-------------|
| >0 (Valid range (8000~192000)) | Success     |
| 0                        | Failure     |

##### read_frames

**Description**

Read frame data.

**Syntax**

```python
read_frames(nframes)
```

**Parameters**

| Parameter Name | Description                                        | Input/Output |
|----------------|----------------------------------------------------|--------------|
| nframes        | Length of frames to read (number of channels × sampling precision per sample point / 8) | Input        |

**Return Value**

| Return Value  | Description |
|---------------|-------------|
| bytes sequence |             |

#### wave.Wave_write

The `Wave_write` class provides methods for setting metadata for a WAV file (such as sample rate, sample points, number of channels, and sampling precision) and saving PCM audio data to a WAV file.

##### set_channels

**Description**

Set the number of channels.

**Syntax**

```python
set_channels(nchannels)
```

**Parameters**

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| nchannels      | Number of channels | Input        |

**Return Value**

None

##### set_sampwidth

**Description**

Set the sample byte length.

**Syntax**

```python
set_sampwidth(sampwidth)
```

**Parameters**

| Parameter Name | Description                                                  | Input/Output |
|----------------|--------------------------------------------------------------|--------------|
| sampwidth      | Sample byte length, valid range [1, 2, 3, 4] corresponding to sampling precision [8, 16, 24, 32] | Input        |

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

| Parameter Name | Description             | Input/Output |
|----------------|--------------------------|--------------|
| framerate      | Sample rate [8000~192000] | Input        |

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

| Parameter Name | Description                      | Input/Output |
|----------------|-----------------------------------|--------------|
| data           | Audio data (bytes sequence)      | Input        |

**Return Value**

None

### pyaudio

The `pyaudio` module is used for audio processing, responsible for capturing and playing binary PCM audio data. To play WAV format files or save captured data as WAV files, it needs to be used in conjunction with the `wave` library, as detailed in the [Example Programs](#example-programs) section.

#### pyaudio.PyAudio

Responsible for managing multiple audio input and output channels, each channel is represented as a Stream class object.

##### open

**Description**

Open a stream.

**Syntax**

```python
open(*args, **kwargs)
```

**Parameters**

Variable parameters, refer to [`Stream.__init__`].

**Return Value**

| Return Value            | Description                       |
|-------------------------|-----------------------------------|
| py:class:`Stream`       | Success                           |
| Others                  | Failure, raises an exception      |

##### close

**Description**

Close a stream.

**Syntax**

```python
close(stream)
```

**Parameters**

None

**Return Value**

None

**Note**

This function will call the `close` method in the Stream object and remove the Stream object from the PyAudio object. Therefore, this function can be omitted, and the Stream.close method can be called directly.

##### terminate

**Description**

Release audio resources. This function must be called to release audio resources when PyAudio is no longer in use. If a vb block is allocated in the default constructor, it should be released in this function.

**Syntax**

```python
terminate()
```

**Parameters**

None

**Return Value**

None

**Note**

This function will call the `close` method in the Stream object and remove the Stream object from the PyAudio object. Therefore, this function can be omitted, and the Stream.close method can be called directly.

#### pyaudio.Stream

The `Stream` class object is used to manage a single audio input or output channel.

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

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| frames         | Number of frames  | Input        |

**Return Value**

| Return Value  | Description       |
|---------------|-------------------|
| bytes         | Read audio data   |

##### write

**Description**

Write audio data.

**Syntax**

```python
write(data)
```

**Parameters**

| Parameter Name | Description                      | Input/Output |
|----------------|-----------------------------------|--------------|
| data           | Audio data (bytes sequence)      | Input        |

**Return Value**

None

##### volume

**Description**

Get or set the volume.

**Syntax**

```python
volume(vol=None, channel=LEFT_RIGHT)
```

**Parameters**

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| vol            | Set volume value  | Input        |
| channel        | Channel selection: LEFT(left channel), RIGHT(right channel), LEFT_RIGHT(left and right channels) | Input        |

**Return Value**

When setting the volume, return value: None
When getting the volume, return value: tuple

##### enable_audio3a

**Description**

Enable audio 3A.

**Syntax**

```python
enable_audio3a(audio3a_value)
```

**Parameters**

| Parameter Name  | Description                                                                 | Input/Output |
|-----------------|-----------------------------------------------------------------------------|--------------|
| audio3a_value   | Audio 3A enable options: AUDIO_3A_ENABLE_ANS (noise suppression), AUDIO_3A_ENABLE_AGC (automatic gain control), AUDIO_3A_ENABLE_AEC (echo cancellation) | Input        |

**Return Value**

None

##### audio3a_send_far_echo_frame

**Description**

Send far-end reference audio (i.e., audio played by the near-end speaker), used only in the echo cancellation (AEC) scenario of audio 3A.

**Syntax**

```python
audio3a_send_far_echo_frame(frame_data, data_len)
```

**Parameters**

| Parameter Name | Description                          | Input/Output |
|----------------|--------------------------------------|--------------|
| frame_data     | Far-end reference audio data (bytes sequence) | Input        |
| data_len       | Data length                          | Input        |

**Return Value**

None

## Example Programs

### Example of Capturing Audio and Saving as a WAV File

```python
import os
from media.media import *   # Import media module for initializing vb buffer
from media.pyaudio import * # Import pyaudio module for audio capture and playback
import media.wave as wave   # Import wav module for saving and loading wav audio files

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
        return True
    return False

def play_audio(filename):
    try:
        wf = wave.open(filename, 'rb')  # Open wav file
        CHUNK = int(wf.get_framerate() / 25)  # Set audio chunk size

        p = PyAudio()
        p.initialize(CHUNK)  # Initialize PyAudio object
        MediaManager.init()  # Initialize vb buffer

        # Create audio output stream, set audio parameters from wav file
        stream = p.open(format=p.get_format_from_width(wf.get_sampwidth()),
                        channels=wf.get_channels(),
                        rate=wf.get_framerate(),
                        output=True, frames_per_buffer=CHUNK)

        # Set volume of audio output stream
        stream.volume(vol=85)

        data = wf.read_frames(CHUNK)  # Read one frame of data from wav file

        while data:
            stream.write(data)  # Write frame data to audio output stream
            data = wf.read_frames(CHUNK)  # Read one frame of data from wav file
            if exit_check():
                break
    except BaseException as e:
        print(f"Exception {e}")
    finally:
        stream.stop_stream()  # Stop audio output stream
        stream.close()        # Close audio output stream
        p.terminate()         # Release audio object
        wf.close()            # Close wav file

        MediaManager.deinit() # Release vb buffer

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("Audio example starts")
    play_audio('/sdcard/examples/test.wav')  # Play WAV file
    print("Audio example completed")
```

### Example of Playing a WAV File

```python
import os
from media.media import *   # Import media module for initializing vb buffer
from media.pyaudio import * # Import pyaudio module for audio capture and playback
import media.wave as wave   # Import wav module for saving and loading wav audio files

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
        return True
    return False

def record_audio(filename, duration):
    CHUNK = 44100 // 25  # Set audio chunk size
    FORMAT = paInt16     # Set sampling precision, supports 16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    CHANNELS = 2         # Set number of channels, supports mono(1)/stereo(2)
    RATE = 44100         # Set sampling rate

    try:
        p = PyAudio()
        p.initialize(CHUNK)    # Initialize PyAudio object
        MediaManager.init()    # Initialize vb buffer

        # Create audio input stream
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        stream.volume(vol=70, channel=LEFT)
        stream.volume(vol=85, channel=RIGHT)
        print("volume:", stream.volume())

        # Enable audio 3A feature: Automatic Noise Suppression (ANS)
        stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)

        frames = []
        # Capture audio data and store in list
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read()
            frames.append(data)
            if exit_check():
                break
        # Save data from list to wav file
        wf = wave.open(filename, 'wb')  # Create wav file
        wf.set_channels(CHANNELS)       # Set wav number of channels
        wf.set_sampwidth(p.get_sample_size(FORMAT))  # Set wav sampling precision
        wf.set_framerate(RATE)          # Set wav sampling rate
        wf.write_frames(b''.join(frames))  # Store wav audio data
        wf.close()  # Close wav file
    except BaseException as e:
        print(f"Exception {e}")
    finally:
        stream.stop_stream()  # Stop capturing audio data
        stream.close()        # Close audio input stream
        p.terminate()         # Release audio object
        MediaManager.deinit() # Release vb buffer


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("Audio example starts")
    record_audio('/sdcard/examples/test.wav', 5)  # Record WAV file
    print("Audio example completed")
```

## Summary

Through this manual, developers can easily use the CanMV audio module to achieve audio playback and capture functions. This module combines the advantages of the `wave` and `pyaudio` libraries, providing convenient interfaces and clear API documentation, making it easy to quickly develop and apply audio-related projects.
