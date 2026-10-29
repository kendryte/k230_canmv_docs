# Audio Routine Explanation

## Overview

This routine demonstrates how to use the built-in codec link to implement I2S audio capture and output functions, while also supporting PDM audio capture. Users can complete audio capture in two ways: first, by using the onboard analog microphone (via the I2S path) to capture sound; second, by using a PDM audio daughter board with a PDM digital microphone (via the PDM path), which supports simultaneous capture from 8 channels. In addition, the I2S path also supports audio output functions, which can output audio signals through the relevant interfaces.

The CanMV K230 development board is equipped with an analog microphone and headphone output interface, while also supporting an external PDM audio daughter board to expand the PDM digital microphone access capability, which can meet the diverse testing requirements of I2S single-channel audio capture and output, as well as PDM 8-channel audio capture, making it convenient for users to complete the functional verification of recording and audio playback.

## Examples

### audio - Audio Capture and Playback Routine

This example program demonstrates the audio capture and output functions of the I2S path on the CanMV development board.

```python
# Audio input and output example
#
# Note: Running this example requires an SD card.
#
# You can play WAV files or capture audio and save it in WAV format.

import os
from media.media import *   #Import the media module, used to initialize the vb buffer
from media.pyaudio import * #Import the pyaudio module, used to capture and play audio
import media.wave as wave   #Import the wav module, used to save and load wav audio files

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
        return True
    return False

def record_audio(filename, duration):
    CHUNK = 44100//25  #Set the audio chunk value
    FORMAT = paInt16       #Set the sampling precision, supports 16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    CHANNELS = 2           #Set the number of channels, supports mono(1)/stereo(2)
    RATE = 44100           #Set the sampling rate

    try:
        p = PyAudio()
        MediaManager.init()    #vb buffer initialization

        #Create an audio input stream
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        stream.volume(vol=70, channel=LEFT)
        stream.volume(vol=85, channel=RIGHT)
        print("volume :",stream.volume())

        #Enable audio 3A function: Automatic Noise Suppression (ANS)
        stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)

        frames = []
        #Capture audio data and store it in a list
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read()
            frames.append(data)
            if exit_check():
                break
        #Save the data in the list to a wav file
        wf = wave.open(filename, 'wb') #Create a wav file
        wf.set_channels(CHANNELS) #Set the number of wav channels
        wf.set_sampwidth(p.get_sample_size(FORMAT))  #Set the wav sampling precision
        wf.set_framerate(RATE)  #Set the wav sampling rate
        wf.write_frames(b''.join(frames)) #Store wav audio data
        wf.close() #Close the wav file
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        stream.stop_stream() #Stop capturing audio data
        stream.close()#Close the audio input stream
        p.terminate()#Release the audio object
        MediaManager.deinit() #Release the vb buffer

def play_audio(filename):
    try:
        wf = wave.open(filename, 'rb')#Open the wav file
        CHUNK = int(wf.get_framerate()/25)#Set the audio chunk value

        p = PyAudio()
        MediaManager.init()    #vb buffer initialization

        #Create an audio output stream, the audio parameters set are all parameters obtained from wave
        stream = p.open(format=p.get_format_from_width(wf.get_sampwidth()),
                    channels=wf.get_channels(),
                    rate=wf.get_framerate(),
                    output=True,frames_per_buffer=CHUNK)

        #Set the volume of the audio output stream
        stream.volume(vol=85)

        data = wf.read_frames(CHUNK)#Read one frame of data from the wav file

        while data:
            stream.write(data)  #Write frame data to the audio output stream
            data = wf.read_frames(CHUNK) #Read one frame of data from the wav file
            if exit_check():
                break
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        stream.stop_stream() #Stop the audio output stream
        stream.close()#Close the audio output stream
        p.terminate()#Release the audio object
        wf.close()#Close the wav file

        MediaManager.deinit() #Release the vb buffer


def loop_audio(duration):
    CHUNK = 44100//25#Set the audio chunk
    FORMAT = paInt16 #Set the audio sampling precision, supports 16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    CHANNELS = 2 #Set the number of audio channels, supports mono(1)/stereo(2)
    RATE = 44100 #Set the audio sampling rate

    try:
        p = PyAudio()
        MediaManager.init()    #vb buffer initialization

        #Create an audio input stream
        input_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        #Set the volume of the audio input stream
        input_stream.volume(vol=70, channel=LEFT)
        input_stream.volume(vol=85, channel=RIGHT)
        print("input volume :",input_stream.volume())

        #Enable audio 3A function: Automatic Noise Suppression (ANS)
        input_stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)

        #Create an audio output stream
        output_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,frames_per_buffer=CHUNK)

        #Set the volume of the audio output stream
        output_stream.volume(vol=85)

        #Get data from the audio input stream and write it to the audio output stream
        for i in range(0, int(RATE / CHUNK * duration)):
            output_stream.write(input_stream.read())
            if exit_check():
                break
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        input_stream.stop_stream()#Stop the audio input stream
        output_stream.stop_stream()#Stop the audio output stream
        input_stream.close() #Close the audio input stream
        output_stream.close() #Close the audio output stream
        p.terminate() #Release the audio object

        MediaManager.deinit() #Release the vb buffer

def audio_recorder(filename, duration):
    CHUNK = 44100//25      #Set the audio chunk value
    FORMAT = paInt16       #Set the sampling precision, supports 16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    CHANNELS = 1           #Set the number of channels, supports mono(1)/stereo(2)
    RATE = 44100           #Set the sampling rate

    p = PyAudio()
    MediaManager.init()    #vb buffer initialization

    try:
        #Create an audio input stream
        input_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        input_stream.volume(vol=70, channel=LEFT)
        input_stream.volume(vol=85, channel=RIGHT)
        print("input volume :",input_stream.volume())

        #Enable audio 3A function: Automatic Noise Suppression (ANS)
        input_stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)
        print("enable audio 3a:ans")

        print("start record...")
        frames = []
        #Capture audio data and store it in a list
        for i in range(0, int(RATE / CHUNK * duration)):
            data = input_stream.read()
            frames.append(data)
            if exit_check():
                break
        print("stop record...")
        #Save the data in the list to a wav file
        wf = wave.open(filename, 'wb') #Create a wav file
        wf.set_channels(CHANNELS) #Set the number of wav channels
        wf.set_sampwidth(p.get_sample_size(FORMAT))  #Set the wav sampling precision
        wf.set_framerate(RATE)  #Set the wav sampling rate
        wf.write_frames(b''.join(frames)) #Store wav audio data
        wf.close() #Close the wav file
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        input_stream.stop_stream() #Stop capturing audio data
        input_stream.close()#Close the audio input stream

    try:
        wf = wave.open(filename, 'rb')#Open the wav file
        CHUNK = int(wf.get_framerate()/25)#Set the audio chunk value

        #Create an audio output stream, the audio parameters set are all parameters obtained from wave
        output_stream = p.open(format=p.get_format_from_width(wf.get_sampwidth()),
                    channels=wf.get_channels(),
                    rate=wf.get_framerate(),
                    output=True,frames_per_buffer=CHUNK)

        #Set the volume of the audio output stream
        output_stream.volume(vol=85)
        print("output volume :",output_stream.volume())

        print("start play...")
        data = wf.read_frames(CHUNK)#Read one frame of data from the wav file

        while data:
            output_stream.write(data)  #Write frame data to the audio output stream
            data = wf.read_frames(CHUNK) #Read one frame of data from the wav file
            if exit_check():
                break
        print("stop play...")
    except BaseException as e:
            print(f"Exception {e}")
    finally:
        output_stream.stop_stream() #Stop the audio output stream
        output_stream.close()#Close the audio output stream

    p.terminate() #Release the audio object
    MediaManager.deinit() #Release the vb buffer

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("Audio example start")
    # record_audio('/sdcard/examples/test.wav', 15)  # Record a WAV file
    # play_audio('/sdcard/examples/test.wav')  # Play the WAV file
    # loop_audio(15)  # Capture audio and output
    audio_recorder('/sdcard/examples/test.wav', 15) #Record 15 seconds of audio, save and play
    print("Audio example done")
```

```{admonition} Tip
For the specific interfaces of the audio i2s module, please refer to the [API Documentation](../../api/mpp/k230_canmv_audio_module_api_manual.md)
```

### pdm - Multi-channel Audio Capture Routine

This example program demonstrates the multi-channel audio capture function of the PDM digital microphone, supporting up to 8 channels of simultaneous capture and saving them as WAV files respectively.
The program uses the `init_audio_pdm_io()` function to specifically configure the GPIO pins of the Lichuang · Lushan Pai K230CanMV development board, mapping pin 26 as the PDM clock line, and pins 27/35/36/34 as 4 PDM data lines respectively, implementing multi-channel audio capture based on this development board, and saving the audio data of different channels as independent WAV files.

```python
# audio input and output example
#
# Note: You will need an SD card to run this example.
#
# Records audio from multiple channels and saves each to separate wav files

import os
from media.media import *   #Import the media module, used to initialize the vb buffer
from media.pyaudio import * #Import the pyaudio module, used to capture and play audio
import media.wave as wave   #Import the wav module, used to save and load wav audio files
from machine import FPIOA

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
        return True
    return False


def init_audio_pdm_io():
    """
    Initialize the IO configuration of the PDM audio interface (based on the Lushan Pai development board)

    Function: Configure the GPIO pin functions related to PDM audio capture on the Lushan Pai development board,
    map the PDM clock line and data line to the specified physical pins, and set the pins to input/output mode.
    The specific pin assignments are as follows:
    - Pin 26: PDM clock line (PDM_CLK), configured as output mode
    - Pin 27: PDM data line 0 (PDM_IN0), configured as input mode
    - Pin 35: PDM data line 1 (IIS_D_OUT0_PDM_IN1), configured as input mode
    - Pin 36: PDM data line 2 (IIS_D_IN1_PDM_IN2), configured as input mode
    - Pin 34: PDM data line 3 (IIS_D_IN0_PDM_IN3), configured as input mode
    """
    fpioa = FPIOA()
    fpioa.set_function(26, FPIOA.PDM_CLK,oe=0x1,ie=0x0)   #pdm clk
    fpioa.set_function(27, FPIOA.PDM_IN0,oe=0x0,ie=0x1)  #pdm data0
    fpioa.set_function(35, FPIOA.IIS_D_OUT0_PDM_IN1,oe=0x0,ie=0x1)  #pdm data1
    fpioa.set_function(36, FPIOA.IIS_D_IN1_PDM_IN2,oe=0x0,ie=0x1)  #pdm data2
    fpioa.set_function(34, FPIOA.IIS_D_IN0_PDM_IN3,oe=0x0,ie=0x1)  #pdm data3

def record_audio_pdm(base_filename, duration, num_channels):
    CHUNK = 44100//25  #Set the audio chunk value
    FORMAT = paInt16       #Set the sampling precision, supports 16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
    RATE = 44100           #Set the sampling rate
    pdm_chn_cnt = num_channels // 2

    init_audio_pdm_io()  #Initialize pdm audio IO ports

    try:
        p = PyAudio()
        MediaManager.init()    #vb buffer initialization

        #Create an audio input stream
        stream = p.open(format=FORMAT,
                        channels=num_channels,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=1) #Use the PDM device to capture audio


        # Initialize the audio frame storage array, each element corresponds to a channel's frame list
        channel_frames = [[] for _ in range(pdm_chn_cnt)]

        # Calculate the total number of frames
        total_frames = int(RATE / CHUNK * duration)

        #Capture audio data and store it in a list
        print(f"Start recording {pdm_chn_cnt} groups of {num_channels}-channel pdm audio, lasting {duration} seconds...")
        for i in range(total_frames):
            for ch in range(pdm_chn_cnt):
                data = stream.read(chn=ch)
                channel_frames[ch].append(data)

            # Print progress every 100 frames
            if i % 100 == 0:
                progress = (i / total_frames) * 100
                print(f"Recording progress: {progress:.1f}%", end='\r')

            if exit_check():
                print("\nUser interrupted recording")
                break

        # Create a separate WAV file for each pdm group
        for ch in range(pdm_chn_cnt):
            # Generate a filename with an index number, such as base_0.wav, base_1.wav
            filename = f"{base_filename}_ch{ch}.wav"

            # Save the data in the list to a wav file
            wf = wave.open(filename, 'wb') #Create a wav file
            wf.set_channels(2)  # Each file saves dual channels
            wf.set_sampwidth(p.get_sample_size(FORMAT))  #Set the wav sampling precision
            wf.set_framerate(RATE)  #Set the wav sampling rate
            wf.write_frames(b''.join(channel_frames[ch])) #Store the audio data of the corresponding channel
            wf.close() #Close the wav file
            print(f"Saved channel {ch*2},{ch*2+1} to {filename}")

    except BaseException as e:
            import sys
            sys.print_exception(e)
    finally:
        stream.stop_stream() #Stop capturing audio data
        stream.close()#Close the audio input stream
        p.terminate()#Release the audio object
        MediaManager.deinit() #Release the vb buffer
        print("Recording complete, resources released")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("pdm sample start")
    # Record 4 groups of 8-channel audio, saved as /sdcard/examples/test_ch0.wav to test_ch3.wav
    record_audio_pdm('/data/test', 15, 8)

    print("pdm sample done")
```

```{admonition} Tip
PDM audio capture requires an external PDM audio daughter board. For specific hardware connections and pin definitions, please refer to the development board hardware manual. When using it, pay attention to the correct configuration of the IO ports to ensure the normal operation of multi-channel capture.
For the specific interfaces of the audio pdm module, please refer to the [API Documentation](../../api/mpp/k230_canmv_audio_module_api_manual.md)
```

### audio3a - Audio 3A Processing Routine (AEC Echo Cancellation)

This example program demonstrates the audio 3A processing function of the CanMV development board. It implements simultaneous playback and recording of audio through multithreading, and enables AEC (Acoustic Echo Cancellation), AGC (Automatic Gain Control), and ANS (Automatic Noise Suppression) functions on the recording stream, effectively eliminating the echo interference of the played sound on the recording signal. It is suitable for scenarios such as intercom and voice interaction.

```python
# aec_playrec.py
# Multithreaded playback and recording of audio

import os
import _thread
from media.media import *
from media.pyaudio import *
import media.wave as wave
import time

# Global PyAudio instance
global_p = None
stop_flag = False        # Thread stop signal
play_complete = False    # Playback completion flag
play_thread_done = False # Whether the playback thread is finished
record_thread_done = False # Whether the recording thread is finished
DIV = 50

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("User stopped: ", e)
        return True
    return False

def init_global_pyaudio():
    """Initialize the global PyAudio instance"""
    global global_p
    if global_p is None:
        global_p = PyAudio()

def terminate_global_pyaudio():
    """Terminate the global PyAudio instance"""
    global global_p
    if global_p is not None:
        global_p.terminate()
        global_p = None

def get_wav_duration(wf):
    """Calculate the playback duration (in seconds) from the WAV file metadata"""
    nframes = wf.get_frames()
    framerate = wf.get_framerate()
    if framerate > 0:
        return nframes / framerate
    return 0

def play_thread_func(stream, wf):
    """Playback thread function"""
    global stop_flag, play_complete, play_thread_done
    try:
        CHUNK = int(wf.get_framerate() / DIV)
        data = wf.read_frames(CHUNK)

        while data and not stop_flag and not exit_check():
            stream.write(data)
            data = wf.read_frames(CHUNK)

        play_complete = True
        print("Playback completed (end of file)")

    except BaseException as e:
        import sys
        sys.print_exception(e)
        play_complete = True
    finally:
        # Release resources
        if stream:
            try: stream.stop_stream(); stream.close()
            except: pass
        if wf:
            try: wf.close()
            except: pass
        # Mark the playback thread as finished
        play_thread_done = True
        print("Playback thread finished")

def record_thread_func(stream, filename, duration, channels, rate):
    """Recording thread function - time-driven, precisely controls the recording duration"""
    global stop_flag, record_thread_done
    CHUNK = rate // DIV
    frames = []

    try:
        start_time = time.time()
        while (time.time() - start_time) < duration:
            if stop_flag or exit_check():
                break
            data = stream.read(block=False)
            if data:
                frames.append(data)
            else:
                time.sleep(0.01)

    except BaseException as e:
        import sys
        sys.print_exception(e)
    finally:
        # Release resources
        if stream:
            try: stream.stop_stream(); stream.close()
            except: pass
        # Save the recording file
        if frames:
            try:
                print("Saving file ...")
                wf = wave.open(filename, 'wb')
                wf.set_channels(channels)
                wf.set_sampwidth(global_p.get_sample_size(paInt16))
                wf.set_framerate(rate)
                wf.write_frames(b''.join(frames))
                wf.close()
                print(f"Recorded to {filename} (duration: {len(frames)*CHUNK/rate:.2f}s)")
            except Exception as e:
                print(f"Save failed: {e}")
        else:
            print("No audio recorded")
        # Mark the recording thread as finished
        record_thread_done = True
        print("Recording thread finished")

def play_and_record(play_filename, record_filename, duration):
    global stop_flag, play_complete, play_thread_done, record_thread_done
    stop_flag = False
    play_complete = False
    play_thread_done = False
    record_thread_done = False

    play_stream = None
    record_stream = None
    wf_play = None

    try:
        init_global_pyaudio()

        wf_play = wave.open(play_filename, 'rb')
        channels = wf_play.get_channels()
        rate = wf_play.get_framerate()
        wav_duration = get_wav_duration(wf_play)
        actual_duration = max(duration, wav_duration)
        print(f"WAV duration: {wav_duration:.2f}s, record duration: {actual_duration:.2f}s")

        play_stream = global_p.open(
            format=global_p.get_format_from_width(wf_play.get_sampwidth()),
            channels=channels,
            rate=rate,
            output=True,
            frames_per_buffer=int(rate/DIV)
        )
        play_stream.volume(vol=85)
        print(f"Play volume: {play_stream.volume()}")

        record_stream = global_p.open(
            format=paInt16,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=rate//DIV
        )
        record_stream.volume(70, LEFT)
        record_stream.volume(85, RIGHT)
        record_stream.enable_audio3a(AUDIO_3A_ENABLE_AEC | AUDIO_3A_ENABLE_AGC | AUDIO_3A_ENABLE_ANS)
        print(f"Record volume: {record_stream.volume()}")

        _thread.start_new_thread(play_thread_func, (play_stream, wf_play))
        _thread.start_new_thread(record_thread_func, (record_stream, record_filename, actual_duration, channels, rate))

        start_time = time.time()
        while True:
            if (time.time() - start_time >= actual_duration) or exit_check():
                stop_flag = True
                break
            time.sleep(0.1)

        print("Waiting for threads to exit...")
        timeout = time.time() + 10
        while not (play_thread_done and record_thread_done):
            if time.time() > timeout:
                print("Warning: Thread wait timeout!")
                break
            time.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
        stop_flag = True  # Stop the thread immediately on exception
    finally:
        if play_stream:
            try: play_stream.stop_stream(); play_stream.close()
            except: pass
        if record_stream:
            try: record_stream.stop_stream(); record_stream.close()
            except: pass
        if wf_play:
            try: wf_play.close()
            except: pass
        # Terminate PyAudio
        terminate_global_pyaudio()
        print("All resources released")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("AEC play and record start")
    PLAY_FILE = '/data/play.wav'
    RECORD_FILE = '/data/record.wav'
    DURATION = 30
    play_and_record(PLAY_FILE, RECORD_FILE, DURATION)
    print("AEC play and record done")
```

```{admonition} Tip
The audio 3A function is enabled through the `enable_audio3a()` interface, which supports the following function combinations:
- `AUDIO_3A_ENABLE_AEC`: Echo cancellation, which requires simultaneous playback and recording to take effect
- `AUDIO_3A_ENABLE_AGC`: Automatic Gain Control
- `AUDIO_3A_ENABLE_ANS`: Automatic Noise Suppression

It is recommended to use 8kHz or 16kHz mono audio. This sampling rate covers the voice frequency band, and the 3A algorithm is optimized for this frequency band to achieve the best processing effect; at the same time, it can reduce the data volume and computational overhead, which is more suitable for the real-time processing requirements of embedded platforms.

The AEC echo cancellation requires simultaneous playback and recording. The program uses multithreading to implement parallel processing of playback and recording. For the specific interfaces of the audio3a module, please refer to the [API Documentation](../../api/mpp/k230_canmv_audio_module_api_manual.md)
```

### acodec - G711 Codec Routine

This example program demonstrates the G711 codec function of the CanMV development board.

```python
# G711 encode/decode example
#
# Note: Running this example requires an SD card.
#
# You can collect raw data and encode it to G711, or decode it to raw data for output.

import os
from mpp.payload_struct import *  # Import the payload module, used to obtain audio and video codec types
from media.media import *         # Import the media module, used to initialize the vb buffer
from media.pyaudio import *       # Import the pyaudio module, used to capture and play audio
import media.g711 as g711         # Import the g711 module, used for G711 encoding and decoding

def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("User stopped: ", e)
        return True
    return False

def encode_audio(filename, duration):
    CHUNK = int(44100 / 25)  # Set the audio chunk size
    FORMAT = paInt16         # Set the sampling precision
    CHANNELS = 2             # Set the number of channels
    RATE = 44100             # Set the sampling rate

    try:
        p = PyAudio()
        enc = g711.Encoder(K_PT_G711A, CHUNK)  # Create a G711 encoder object
        MediaManager.init()   # Initialize the vb buffer

        enc.create()  # Create the encoder
        # Create an audio input stream
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        # Capture audio data, encode it, and store it in a list
        for i in range(0, int(RATE / CHUNK * duration)):
            frame_data = stream.read()  # Read audio data from the audio input stream
            data = enc.encode(frame_data)  # Encode the audio data to G711
            frames.append(data)  # Save the G711 encoded

data to the list
            if exit_check():
                break
        # Save the G711 encoded data to a file
        with open(filename, mode='wb') as wf:
            wf.write(b''.join(frames))
        stream.stop_stream()  # Stop the audio input stream
        stream.close()        # Close the audio input stream
        p.terminate()         # Release the audio object
        enc.destroy()         # Destroy the G711 encoder
    except BaseException as e:
        print(f"Exception: {e}")
    finally:
        MediaManager.deinit()  # Release the vb buffer

def decode_audio(filename):
    FORMAT = paInt16         # Set the audio chunk size
    CHANNELS = 2             # Set the number of channels
    RATE = 44100             # Set the sampling rate
    CHUNK = int(RATE / 25)   # Set the audio chunk size

    try:
        wf = open(filename, mode='rb')  # Open the G711 file
        p = PyAudio()
        dec = g711.Decoder(K_PT_G711A, CHUNK)  # Create a G711 decoder object
        MediaManager.init()   # Initialize the vb buffer

        dec.create()  # Create the decoder

        # Create an audio output stream
        stream = p.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         output=True,
                         frames_per_buffer=CHUNK)

        stream_len = CHUNK * CHANNELS * 2 // 2  # Set the length of G711 data stream to read each time
        stream_data = wf.read(stream_len)  # Read data from the G711 file

        # Decode the G711 file and play it
        while stream_data:
            frame_data = dec.decode(stream_data)  # Decode the G711 file
            stream.write(frame_data)  # Play the raw data
            stream_data = wf.read(stream_len)  # Continue to read data from the G711 file
            if exit_check():
                break
        stream.stop_stream()  # Stop the audio output stream
        stream.close()        # Close the audio output stream
        p.terminate()         # Release the audio object
        dec.destroy()         # Destroy the decoder
        wf.close()           # Close the G711 file

    except BaseException as e:
        print(f"Exception: {e}")
    finally:
        MediaManager.deinit()  # Release the vb buffer

def loop_codec(duration):
    CHUNK = int(44100 / 25)  # Set the audio chunk size
    FORMAT = paInt16         # Set the sampling precision
    CHANNELS = 2             # Set the number of channels
    RATE = 44100             # Set the sampling rate

    try:
        p = PyAudio()
        dec = g711.Decoder(K_PT_G711A, CHUNK)  # Create a G711 decoder object
        enc = g711.Encoder(K_PT_G711A, CHUNK)  # Create a G711 encoder object
        MediaManager.init()   # Initialize the vb buffer

        dec.create()  # Create the G711 decoder
        enc.create()  # Create the G711 encoder

        # Create an audio input stream
        input_stream = p.open(format=FORMAT,
                               channels=CHANNELS,
                               rate=RATE,
                               input=True,
                               frames_per_buffer=CHUNK)

        # Create an audio output stream
        output_stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                output=True,
                                frames_per_buffer=CHUNK)

        # Get data from the audio input stream, encode, decode, and write to the audio output stream
        for i in range(0, int(RATE / CHUNK * duration)):
            frame_data = input_stream.read()  # Get raw audio data from the audio input stream
            stream_data = enc.encode(frame_data)  # Encode the audio data to G711
            frame_data = dec.decode(stream_data)  # Decode the G711 data to raw data
            output_stream.write(frame_data)  # Play the raw data
            if exit_check():
                break
        input_stream.stop_stream()  # Stop the audio input stream
        output_stream.stop_stream()  # Stop the audio output stream
        input_stream.close()         # Close the audio input stream
        output_stream.close()        # Close the audio output stream
        p.terminate()                # Release the audio object
        dec.destroy()                # Destroy the G711 decoder
        enc.destroy()                # Destroy the G711 encoder
    except BaseException as e:
        print(f"Exception: {e}")
    finally:
        MediaManager.deinit()  # Release the vb buffer

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    print("Audio codec example start")
    # encode_audio('/sdcard/examples/test.g711a', 15) # Capture and encode a G711 file
    # decode_audio('/sdcard/examples/test.g711a')  # Decode the G711 file and output
    loop_codec(15)  # Capture audio data -> encode G711 -> decode G711 -> play audio
    print("Audio codec example done")
```

```{admonition} Tip
For the specific interfaces of the acodec module, please refer to the [API Documentation](../../api/mpp/k230_canmv_player_module_api_manual.md)
```
