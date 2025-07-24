# Audio Routine Explanation

## Overview

This routine demonstrates how to use the built-in codec link to implement I2S audio capture and playback functions. Users can capture sound through the onboard microphone and output the sound through the headphone jack.

The CanMV K230 development board is equipped with an analog microphone and a headphone output interface, making it convenient for users to test recording and audio playback.

## Examples

### audio - Audio Capture and Playback Routine

This example program demonstrates the audio capture and output functions of the CanMV development board.

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

def loop_audio(duration):
    CHUNK = 44100 // 25  # Set audio chunk size
    FORMAT = paInt16     # Set audio sampling precision, supports 16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    CHANNELS = 2         # Set number of channels, supports mono(1)/stereo(2)
    RATE = 44100         # Set audio sampling rate

    try:
        p = PyAudio()
        p.initialize(CHUNK)  # Initialize PyAudio object
        MediaManager.init()  # Initialize vb buffer

        # Create audio input stream
        input_stream = p.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)

        # Set volume of audio input stream
        input_stream.volume(vol=70, channel=LEFT)
        input_stream.volume(vol=85, channel=RIGHT)
        print("input volume:", input_stream.volume())

        # Enable audio 3A feature: Automatic Noise Suppression (ANS)
        input_stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)

        # Create audio output stream
        output_stream = p.open(format=FORMAT,
                               channels=CHANNELS,
                               rate=RATE,
                               output=True, frames_per_buffer=CHUNK)

        # Set volume of audio output stream
        output_stream.volume(vol=85)

        # Get data from audio input stream and write to audio output stream
        for i in range(0, int(RATE / CHUNK * duration)):
            output_stream.write(input_stream.read())
            if exit_check():
                break
    except BaseException as e:
        print(f"Exception {e}")
    finally:
        input_stream.stop_stream()  # Stop audio input stream
        output_stream.stop_stream()  # Stop audio output stream
        input_stream.close()         # Close audio input stream
        output_stream.close()        # Close audio output stream
        p.terminate()                # Release audio object

        MediaManager.deinit()        # Release vb buffer

def audio_recorder(filename, duration):
    CHUNK = 44100 // 25  # Set audio chunk size
    FORMAT = paInt16     # Set sampling precision, supports 16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    CHANNELS = 1         # Set number of channels, supports mono(1)/stereo(2)
    RATE = 44100         # Set sampling rate

    p = PyAudio()
    p.initialize(CHUNK)  # Initialize PyAudio object
    MediaManager.init()  # Initialize vb buffer

    try:
        # Create audio input stream
        input_stream = p.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)

        input_stream.volume(vol=70, channel=LEFT)
        input_stream.volume(vol=85, channel=RIGHT)
        print("input volume:", input_stream.volume())

        # Enable audio 3A feature: Automatic Noise Suppression (ANS)
        input_stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)
        print("enable audio 3a: ans")

        print("start record...")
        frames = []
        # Capture audio data and store in list
        for i in range(0, int(RATE / CHUNK * duration)):
            data = input_stream.read()
            frames.append(data)
            if exit_check():
                break
        print("stop record...")
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
        input_stream.stop_stream()  # Stop capturing audio data
        input_stream.close()        # Close audio input stream

    try:
        wf = wave.open(filename, 'rb')  # Open wav file
        CHUNK = int(wf.get_framerate() / 25)  # Set audio chunk size

        # Create audio output stream, set audio parameters from wav file
        output_stream = p.open(format=p.get_format_from_width(wf.get_sampwidth()),
                               channels=wf.get_channels(),
                               rate=wf.get_framerate(),
                               output=True, frames_per_buffer=CHUNK)

        # Set volume of audio output stream
        output_stream.volume(vol=85)
        print("output volume:", output_stream.volume())

        print("start play...")
        data = wf.read_frames(CHUNK)  # Read one frame of data from wav file

        while data:
            output_stream.write(data)  # Write frame data to audio output stream
            data = wf.read_frames(CHUNK)  # Read one frame of data from wav file
            if exit_check():
                break
        print("stop play...")
    except BaseException as e:
        print(f"Exception {e}")
    finally:
        output_stream.stop_stream()  # Stop audio output stream
        output_stream.close()        # Close audio output stream

    p.terminate()  # Release audio object
    MediaManager.deinit()  # Release vb buffer

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("Audio example starts")
    # record_audio('/sdcard/examples/test.wav', 15)  # Record WAV file
    # play_audio('/sdcard/examples/test.wav')  # Play WAV file
    # loop_audio(15)  # Capture and output audio
    audio_recorder('/sdcard/examples/test.wav', 15)  # Record a 15-second audio file, save it and play it
    print("Audio example completed")

```

```{admonition} Tip
For detailed interfaces of the audio module, please refer to the [API documentation](../../api/mpp/K230_CanMV_Audio_Module_API_Manual.md).
```

### acodec - G711 Encoding and Decoding Routine

This example program demonstrates the G711 encoding and decoding functions of the CanMV development board.

```python
# G711 Encoding/Decoding Example
#
# Note: An SD card is required to run this example.
#
# You can collect raw data and encode it to G711, or decode it to raw data for output.

import os
from mpp.payload_struct import *  # Import payload module for getting audio and video codec types
from media.media import *         # Import media module for initializing vb buffer
from media.pyaudio import *       # Import pyaudio module for audio capture and playback
import media.g711 as g711         # Import g711 module for G711 encoding and decoding

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("User stopped:", e)
        return True
    return False

def encode_audio(filename, duration):
    CHUNK = int(44100 / 25)  # Set audio chunk size
    FORMAT = paInt16         # Set sampling precision
    CHANNELS = 2             # Set number of channels
    RATE = 44100             # Set sampling rate

    try:
        p = PyAudio()
        p.initialize(CHUNK)  # Initialize PyAudio object
        enc = g711.Encoder(K_PT_G711A, CHUNK)  # Create G711 encoder object
        MediaManager.init()   # Initialize vb buffer

        enc.create()  # Create encoder
        # Create audio input stream
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        # Capture audio data, encode it, and store in list
        for i in range(0, int(RATE / CHUNK * duration)):
            frame_data = stream.read()  # Read audio data from input stream
            data = enc.encode(frame_data)  # Encode audio data to G711
            frames.append(data)  # Save G711 encoded data to list
            if exit_check():
                break
        # Save G711 encoded data to file
        with open(filename, mode='wb') as wf:
            wf.write(b''.join(frames))
        stream.stop_stream()  # Stop audio input stream
        stream.close()        # Close audio input stream
        p.terminate()         # Release audio object
        enc.destroy()         # Destroy G711 encoder
    except BaseException as e:
        print(f"Exception: {e}")
    finally:
        MediaManager.deinit()  # Release vb buffer

def decode_audio(filename):
    FORMAT = paInt16         # Set audio chunk size
    CHANNELS = 2             # Set number of channels
    RATE = 44100             # Set sampling rate
    CHUNK = int(RATE / 25)   # Set audio chunk size

    try:
        wf = open(filename, mode='rb')  # Open G711 file
        p = PyAudio()
        p.initialize(CHUNK)  # Initialize PyAudio object
        dec = g711.Decoder(K_PT_G711A, CHUNK)  # Create G711 decoder object
        MediaManager.init()   # Initialize vb buffer

        dec.create()  # Create decoder

        # Create audio output stream
        stream = p.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         output=True,
                         frames_per_buffer=CHUNK)

        stream_len = CHUNK * CHANNELS * 2 // 2  # Set length of G711 data stream to read each time
        stream_data = wf.read(stream_len)  # Read data from G711 file

        # Decode G711 file and play
        while stream_data:
            frame_data = dec.decode(stream_data)  # Decode G711 file
            stream.write(frame_data)  # Play raw data
            stream_data = wf.read(stream_len)  # Continue reading data from G711 file
            if exit_check():
                break
        stream.stop_stream()  # Stop audio output stream
        stream.close()        # Close audio output stream
        p.terminate()         # Release audio object
        dec.destroy()         # Destroy decoder
        wf.close()           # Close G711 file

    except BaseException as e:
        print(f"Exception: {e}")
    finally:
        MediaManager.deinit()  # Release vb buffer

def loop_codec(duration):
    CHUNK = int(44100 / 25)  # Set audio chunk size
    FORMAT = paInt16         # Set sampling precision
    CHANNELS = 2             # Set number of channels
    RATE = 44100             # Set sampling rate

    try:
        p = PyAudio()
        p.initialize(CHUNK)  # Initialize PyAudio object
        dec = g711.Decoder(K_PT_G711A, CHUNK)  # Create G711 decoder object
        enc = g711.Encoder(K_PT_G711A, CHUNK)  # Create G711 encoder object
        MediaManager.init()   # Initialize vb buffer

        dec.create()  # Create G711 decoder
        enc.create()  # Create G711 encoder

        # Create audio input stream
        input_stream = p.open(format=FORMAT,
                               channels=CHANNELS,
                               rate=RATE,
                               input=True,
                               frames_per_buffer=CHUNK)

        # Create audio output stream
        output_stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                output=True,
                                frames_per_buffer=CHUNK)

        # Get data from audio input stream, encode, decode, and write to audio output stream
        for i in range(0, int(RATE / CHUNK * duration)):
            frame_data = input_stream.read()  # Get raw audio data from input stream
            stream_data = enc.encode(frame_data)  # Encode audio data to G711
            frame_data = dec.decode(stream_data)  # Decode G711 data to raw data
            output_stream.write(frame_data)  # Play raw data
            if exit_check():
                break
        input_stream.stop_stream()  # Stop audio input stream
        output_stream.stop_stream()  # Stop audio output stream
        input_stream.close()         # Close audio input stream
        output_stream.close()        # Close audio output stream
        p.terminate()                # Release audio object
        dec.destroy()                # Destroy G711 decoder
        enc.destroy()                # Destroy G711 encoder
    except BaseException as e:
        print(f"Exception: {e}")
    finally:
        MediaManager.deinit()  # Release vb buffer

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("Audio codec example starts")
    # encode_audio('/sdcard/examples/test.g711a', 15) # Capture and encode G711 file
    # decode_audio('/sdcard/examples/test.g711a')  # Decode G711 file and output
    loop_codec(15)  # Capture audio data -> Encode G711 -> Decode G711 -> Play audio
    print("Audio codec example completed")
```

```{admonition} Tip
For detailed interfaces of the acodec module, please refer to the [API documentation](../../api/mpp/K230_CanMV_Player_Module_API_Manual.md).
```
