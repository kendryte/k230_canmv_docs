# Video Example Tutorial

## Overview

K230 supports H264 or H265 encoding for video streams. The APIs provided in CanMV enable users to record and play MP4 files, and also support RTSP streaming.

## Examples

### MP4 Recording

This example program demonstrates how to record MP4 files on the CanMV development board.
You can use the `Mp4Container` class to record camera audio and video data. For specific implementation, refer to the `mp4_muxer_test` function. This method is encapsulated in a relatively simple way and is suitable for quick start.
If you need more flexible control, you can use the `kd_mp4_*` series of functions to complete MP4 encapsulation of H264/H265 encoded video. These functions provide finer-grained control and are suitable for customized development by advanced users. For specific implementation, refer to the `vi_bind_venc_mp4_test` function.

```python
# Save MP4 file example
#
# Note: You will need an SD card to run this example.
#
# You can capture audio and video and save them as MP4.The current version only supports MP4 format, video supports 264/265, and audio supports g711a/g711u.

from media.mp4format import *
import os

def mp4_muxer_test():
    print("mp4_muxer_test start")
    width = 1280
    height = 720
    # Instantiate mp4 container
    mp4_muxer = Mp4Container()
    mp4_cfg = Mp4CfgStr(mp4_muxer.MP4_CONFIG_TYPE_MUXER)
    if mp4_cfg.type == mp4_muxer.MP4_CONFIG_TYPE_MUXER:
        file_name = "/sdcard/examples/test.mp4"
        mp4_cfg.SetMuxerCfg(file_name, mp4_muxer.MP4_CODEC_ID_H265, width, height, mp4_muxer.MP4_CODEC_ID_G711U)
    # Create mp4 muxer
    mp4_muxer.Create(mp4_cfg)
    # Start mp4 muxer
    mp4_muxer.Start()

    frame_count = 0
    try:
        while True:
            os.exitpoint()
            # Process audio and video data, write to file in MP4 format
            mp4_muxer.Process()
            frame_count += 1
            print("frame_count = ", frame_count)
            if frame_count >= 200:
                break
    except BaseException as e:
        print(e)
    # Stop mp4 muxer
    mp4_muxer.Stop()
    # Destroy mp4 muxer
    mp4_muxer.Destroy()
    print("mp4_muxer_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    mp4_muxer_test()
```

```python
# Save MP4 file example
#
# Note: You will need an SD card to run this example.
#
# You can capture audio and video and save them as MP4.
from media.mp4format import *
from mpp.mp4_format import *
from mpp.mp4_format_struct import *
from media.vencoder import *
from media.sensor import *
from media.media import *
import uctypes
import time
import os

def mp4_muxer_init(file_name,  fmp4_flag):
    mp4_cfg = k_mp4_config_s()
    mp4_cfg.config_type = K_MP4_CONFIG_MUXER
    mp4_cfg.muxer_config.file_name[:] = bytes(file_name, 'utf-8')
    mp4_cfg.muxer_config.fmp4_flag = fmp4_flag

    handle = k_u64_ptr()
    ret = kd_mp4_create(handle, mp4_cfg)
    if ret:
        raise OSError("kd_mp4_create failed.")
    return handle.value

def mp4_muxer_create_video_track(mp4_handle, width, height, video_payload_type):
    video_track_info = k_mp4_track_info_s()
    video_track_info.track_type = K_MP4_STREAM_VIDEO
    video_track_info.time_scale = 1000
    video_track_info.video_info.width = width
    video_track_info.video_info.height = height
    video_track_info.video_info.codec_id = video_payload_type
    video_track_handle = k_u64_ptr()
    ret = kd_mp4_create_track(mp4_handle, video_track_handle, video_track_info)
    if ret:
        raise OSError("kd_mp4_create_track failed.")
    return video_track_handle.value

def mp4_muxer_create_audio_track(mp4_handle,channel,sample_rate, bit_per_sample ,audio_payload_type):
    audio_track_info = k_mp4_track_info_s()
    audio_track_info.track_type = K_MP4_STREAM_AUDIO
    audio_track_info.time_scale = 1000
    audio_track_info.audio_info.channels = channel
    audio_track_info.audio_info.codec_id = audio_payload_type
    audio_track_info.audio_info.sample_rate = sample_rate
    audio_track_info.audio_info.bit_per_sample = bit_per_sample
    audio_track_handle = k_u64_ptr()
    ret = kd_mp4_create_track(mp4_handle, audio_track_handle, audio_track_info)
    if ret:
        raise OSError("kd_mp4_create_track failed.")
    return audio_track_handle.value

def vi_bind_venc_mp4_test(file_name,width=1280, height=720,venc_payload_type = K_PT_H264,fmp4_flag = False):
    print("venc_test start")
    width = ALIGN_UP(width, 16)

    frame_data = k_mp4_frame_data_s()
    save_idr = bytearray(width * height * 3 // 4)
    idr_index = 0

    # mp4 muxer init
    mp4_handle = mp4_muxer_init(file_name, fmp4_flag)

    # create video track
    if venc_payload_type == K_PT_H264:
        video_payload_type = K_MP4_CODEC_ID_H264
    elif venc_payload_type == K_PT_H265:
        video_payload_type = K_MP4_CODEC_ID_H265
    mp4_video_track_handle = mp4_muxer_create_video_track(mp4_handle, width, height, video_payload_type)

    # Initialize sensor
    sensor = Sensor()
    sensor.reset()
    # Set camera output buffer
    # set chn0 output size
    sensor.set_framesize(width = width, height = height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)

    # Instantiate video encoder
    encoder = Encoder()
    # Set video encoder output buffer
    encoder.SetOutBufs(8, width, height)

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # Create encoder
    encoder.Create(chnAttr)

    # Bind camera and venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, encoder.chn))

    # Start encoding
    encoder.Start()
    # Start camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    video_start_timestamp = 0
    get_first_I_frame = False

    try:
        while True:
            os.exitpoint()
            ret = encoder.GetStream(streamData,timeout = -1) # Get one or more stream frames
            if ret != 0:
                continue

            # Retrieve first IDR frame and write to MP4 file. Note: The first frame must be an IDR frame.
            if not get_first_I_frame:
                for pack_idx in range(0, streamData.pack_cnt):
                    stream_type = streamData.stream_type[pack_idx]
                    if stream_type == encoder.STREAM_TYPE_I:
                        get_first_I_frame = True
                        video_start_timestamp = streamData.pts[pack_idx]
                        save_idr[idr_index:idr_index+streamData.data_size[pack_idx]] = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                        idr_index += streamData.data_size[pack_idx]

                        frame_data.codec_id = video_payload_type
                        frame_data.data = uctypes.addressof(save_idr)
                        frame_data.data_length = idr_index
                        frame_data.time_stamp = streamData.pts[pack_idx] - video_start_timestamp

                        ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
                        if ret:
                            raise OSError("kd_mp4_write_frame failed.")

                        break

                    elif stream_type == encoder.STREAM_TYPE_HEADER:
                        save_idr[idr_index:idr_index+streamData.data_size[pack_idx]] = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                        idr_index += streamData.data_size[pack_idx]
                        continue
                    else:
                        continue

                encoder.ReleaseStream(streamData)
                continue

            # Write video stream to MP4 file (not first idr frame)
            for pack_idx in range(0, streamData.pack_cnt):
                frame_data.codec_id = video_payload_type
                frame_data.data = streamData.data[pack_idx]
                frame_data.data_length = streamData.data_size[pack_idx]
                frame_data.time_stamp = streamData.pts[pack_idx] - video_start_timestamp

                #print("video size: ", streamData.data_size[pack_idx], "video type: ", streamData.stream_type[pack_idx],"video timestamp:",frame_data.time_stamp)
                ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
                if ret:
                    raise OSError("kd_mp4_write_frame failed.")
                frame_count += 1

            encoder.ReleaseStream(streamData) # Release one stream frame

            print("frame_count = ", frame_count)
            if frame_count >= 200:
                break
    except KeyboardInterrupt as e:
        import sys
        sys.print_exception(e)
    except BaseException as e:
        import sys
        sys.print_exception(e)

    # Stop camera
    sensor.stop()
    # Destroy the binding between camera and venc
    link.destroy()
    # Stop encoding
    encoder.Stop()
    # Destroy encoder
    encoder.Destroy()

    # mp4 muxer destroy
    kd_mp4_destroy_tracks(mp4_handle)
    kd_mp4_destroy(mp4_handle)

    print("record mp4 done")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_mp4_test("/data/test.mp4", 1280, 720)
```

```{admonition} Note
For specific interface definitions, please refer to [mp4muxer](../../api/mpp/k230_canmv_mp4_module_api_manual.md)
```

### MP4 Demuxing

This example program demonstrates how to use the MP4 demuxer on the CanMV development board to parse MP4 files and extract the video and audio streams from them.

```python
# MP4 Demuxer Example
#
# This script demuxes an MP4 file, extracting video and audio streams.
# Supported video codecs: H.264, H.265
# Supported audio codecs: G.711A, G.711U

from media.media import *
from mpp.mp4_format import *
from mpp.mp4_format_struct import *
from media.pyaudio import *
import media.g711 as g711
from mpp.payload_struct import *
import media.vdecoder as vdecoder
from media.display import *
import uctypes
import time
import _thread
import os

def demuxer_mp4(filename):
    mp4_cfg = k_mp4_config_s()
    video_info = k_mp4_video_info_s()
    video_track = False
    audio_info = k_mp4_audio_info_s()
    audio_track = False
    mp4_handle = k_u64_ptr()

    mp4_cfg.config_type = K_MP4_CONFIG_DEMUXER
    mp4_cfg.muxer_config.file_name[:] = bytes(filename, 'utf-8')
    mp4_cfg.muxer_config.fmp4_flag = 0

    ret = kd_mp4_create(mp4_handle, mp4_cfg)
    if ret:
        raise OSError("kd_mp4_create failed:",filename)

    file_info = k_mp4_file_info_s()
    kd_mp4_get_file_info(mp4_handle.value, file_info)
    #print("=====file_info: track_num:",file_info.track_num,"duration:",file_info.duration)

    for i in range(file_info.track_num):
        track_info = k_mp4_track_info_s()
        ret = kd_mp4_get_track_by_index(mp4_handle.value, i, track_info)
        if (ret < 0):
            raise ValueError("kd_mp4_get_track_by_index failed")

        if (track_info.track_type == K_MP4_STREAM_VIDEO):
            if (track_info.video_info.codec_id == K_MP4_CODEC_ID_H264 or track_info.video_info.codec_id == K_MP4_CODEC_ID_H265):
                video_track = True
                video_info = track_info.video_info
                print("    codec_id: ", video_info.codec_id)
                print("    track_id: ", video_info.track_id)
                print("    width: ", video_info.width)
                print("    height: ", video_info.height)
            else:
                print("video not support codecid:",track_info.video_info.codec_id)
        elif (track_info.track_type == K_MP4_STREAM_AUDIO):
            if (track_info.audio_info.codec_id == K_MP4_CODEC_ID_G711A or track_info.audio_info.codec_id == K_MP4_CODEC_ID_G711U):
                audio_track = True
                audio_info = track_info.audio_info
                print("    codec_id: ", audio_info.codec_id)
                print("    track_id: ", audio_info.track_id)
                print("    channels: ", audio_info.channels)
                print("    sample_rate: ", audio_info.sample_rate)
                print("    bit_per_sample: ", audio_info.bit_per_sample)
                #audio_info.channels = 2
            else:
                print("audio not support codecid:",track_info.audio_info.codec_id)

    if (video_track == False):
        raise ValueError("video track not found")

    # Record initial system time
    start_system_time = time.ticks_ms()
    # Record initial video timestamp
    start_video_timestamp = 0

    while (True):
        frame_data =  k_mp4_frame_data_s()
        ret = kd_mp4_get_frame(mp4_handle.value, frame_data)
        if (ret < 0):
            raise OSError("get frame data failed")

        if (frame_data.eof):
            break

        if (frame_data.codec_id == K_MP4_CODEC_ID_H264 or frame_data.codec_id == K_MP4_CODEC_ID_H265):
            data = uctypes.bytes_at(frame_data.data,frame_data.data_length)
            print("video frame_data.codec_id:",frame_data.codec_id,"data_length:",frame_data.data_length,"timestamp:",frame_data.time_stamp)

            # Calculate elapsed video timestamp (time_stamp is in microseconds, convert to milliseconds)
            video_timestamp_elapsed = (frame_data.time_stamp - start_video_timestamp) // 1000
            # Calculate elapsed system time
            current_system_time = time.ticks_ms()
            system_time_elapsed = current_system_time - start_system_time

            # If the elapsed system time is less than the elapsed video timestamp, delay
            if system_time_elapsed < video_timestamp_elapsed:
                time.sleep_ms(video_timestamp_elapsed - system_time_elapsed)

        elif(frame_data.codec_id == K_MP4_CODEC_ID_G711A or frame_data.codec_id == K_MP4_CODEC_ID_G711U):
            data = uctypes.bytes_at(frame_data.data,frame_data.data_length)
            print("audio frame_data.codec_id:",frame_data.codec_id,"data_length:",frame_data.data_length,"timestamp:",frame_data.time_stamp)

    kd_mp4_destroy(mp4_handle.value)

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    demuxer_mp4("/sdcard/examples/test.mp4")
```

```{admonition} Note
For specific interface definitions, please refer to [mp4demuxer](../../api/mpp/k230_canmv_mp4_module_api_manual.md)
```

### MP4 Playback

This example program is used to demonstrate the functionality of an MP4 file player on the CanMV development board.

```python
# play mp4 file example
#
# Note: You will need an SD card to run this example.
#
# You can load local files to play. The current version only supports MP4 format, video supports 264/265, and audio supports g711a/g711u.

from media.player import * # Import player module, used to play mp4 files
import os

start_play = False # Playback finished flag
def player_event(event,data):
    global start_play
    if(event == K_PLAYER_EVENT_EOF): # Playback finished flag
        start_play = False # Set playback finished flag

def play_mp4_test(filename):
    global start_play
    # player=Player() # Create player object
    # Use IDE as output display, can set any resolution
    player=Player(Display.VIRT)
    # Use ST7701 LCD screen as output display, maximum resolution 800*480
    # player=Player(Display.ST7701)
    # Use HDMI as output display
    # player=Player(Display.LT9611)
    player.load(filename) # Load mp4 file
    player.set_event_callback(player_event) # Set player event callback
    player.start() # Start playback
    start_play = True

    # Wait for playback to finish
    try:
        while(start_play):
            time.sleep(0.1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)

    player.stop() # Stop playback
    print("play over")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    play_mp4_test("/sdcard/examples/test.mp4") # Play mp4 file
```

```{admonition} Note
For specific interface definitions, please refer to [player](../../api/mpp/k230_canmv_player_module_api_manual.md)
```

### H264/H265 Encoding

This example program is used to demonstrate the functionality of venc video encoding on the CanMV development board.

```python
# Video encode example
#
# Note: You will need an SD card to run this example.
#
# You can capture videos and encode them into 264/265 files

from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def vi_bind_venc_test(file_name,width=1280, height=720):
    print("venc_test start")
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # Determine file type
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # Initialize sensor
    sensor = Sensor()
    sensor.reset()
    # Set camera output buffer
    # set chn0 output size
    sensor.set_framesize(width = width, height = height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)


    # Instantiate video encoder
    encoder = Encoder()
    # Set video encoder output buffer
    encoder.SetOutBufs(8, width, height)

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # Create encoder
    encoder.Create(chnAttr)

    # Bind camera and venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, encoder.chn))

    # Start encoding
    encoder.Start()
    # Start camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                encoder.GetStream(streamData) # Get one stream frame

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # Write stream to file
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(streamData) # Release one stream frame

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # Stop camera
    sensor.stop()
    # Destroy the binding between camera and venc
    link.destroy()
    # Stop encoding
    encoder.Stop()
    # Destroy encoder
    encoder.Destroy()
    print("venc_test stop")

def stream_venc_test(file_name,width=1280, height=720):
    print("venc_test start")
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # Determine file type
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # Initialize sensor
    sensor = Sensor()
    sensor.reset()
    # Set camera output buffer
    # set chn0 output size
    sensor.set_framesize(width = width, height = height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)


    # Instantiate video encoder
    encoder = Encoder()
    # Set video encoder output buffer
    encoder.SetOutBufs(8, width, height)

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # Create encoder
    encoder.Create(chnAttr)

    # Start encoding
    encoder.Start()
    # Start camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    yuv420sp_img = None
    frame_info = k_video_frame_info()
    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                frame_info  = sensor.snapshot(chn=CAM_CHN_ID_0,dump_frame=True)
                #frame_info.v_frame.nv12_to_grayscale() # convert to grayscale
                encoder.SendFrame(frame_info)
                encoder.GetStream(streamData) # Get one stream frame

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # Write stream to file
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(streamData) # Release one stream frame

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # Stop camera
    sensor.stop()
    # Stop encoding
    encoder.Stop()
    # Destroy encoder
    encoder.Destroy()
    print("venc_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_test("/data/test.264",800,480)  # vi bind venc example
    #stream_venc_test("/data/test.264",800,480)  # venc encoding data stream example
```

```{admonition} Note
For specific interface definitions, please refer to [VENC](../../api/mpp/k230_canmv_venc_module_api_manual.md)
```

### H264/H265 Decoding

This example program is used to demonstrate the functionality of vdec video decoding on the CanMV development board.

```python
# Video encode example
#
# Note: You will need an SD card to run this example.
#
# You can decode 264/265 and display them on the screen

from media.media import *
from mpp.payload_struct import *
import media.vdecoder as vdecoder
from media.display import *

import time, os

STREAM_SIZE = 40960
def vdec_test(file_name,width=1280,height=720):
    print("vdec_test start")
    vdec_chn = VENC_CHN_ID_0
    vdec_width =  ALIGN_UP(width, 16)
    vdec_height = height
    vdec = None
    vdec_payload_type = K_PT_H264

    #display_type = Display.VIRT
    display_type = Display.ST7701 # Use ST7701 LCD screen as output display, maximum resolution 800*480
    #display_type = Display.LT9611 # Use HDMI as output display

    # Determine file type
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        vdec_payload_type = K_PT_H264
    elif suffix == '265':
        vdec_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # Instantiate video decoder
    #vdecoder.Decoder.vb_pool_config(4,6)
    vdec = vdecoder.Decoder(vdec_payload_type)

    # Initialize display
    if (display_type == Display.VIRT):
        Display.init(display_type,width = vdec_width, height = vdec_height,fps=30)
    else:
        Display.init(display_type,to_ide = True)

    #vb buffer initialization
    MediaManager.init()

    # Create video decoder
    vdec.create()

    # vdec bind display
    bind_info = vdec.bind_info(width=vdec_width,height=vdec_height,chn=vdec.get_vdec_channel())
    Display.bind_layer(**bind_info, layer = Display.LAYER_VIDEO1)

    vdec.start()
    # Open file
    with open(file_name, "rb") as fi:
        while True:
            os.exitpoint()
            # Read video data stream
            data = fi.read(STREAM_SIZE)
            if not data:
                break
            # Decode data stream
            vdec.decode(data)

    # Stop video decoder
    vdec.stop()
    # Destroy video decoder
    vdec.destroy()
    time.sleep(1)

    # Close display
    Display.deinit()
    # Release vb buffer
    MediaManager.deinit()

    print("vdec_test stop")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vdec_test("/sdcard/examples/test.264",800,480) # Decode 264/265 video file
```

```{admonition} Note
For specific interface definitions, please refer to [VDEC](../../api/mpp/k230_canmv_vdec_module_api_manual.md)
```

### RTSP Streaming

The example script path in the development board firmware is `/sdcard/examples/02-Media/rtsp_server.py`, and the SDK source code path is `src/canmv/resources/examples/02-Media/rtsp_server.py`. It establishes a `Sensor -> VENC -> RTSP` video pipeline through `RtspServer`. By default, it uses H.265, `1280 x 720`, `512 Kbit/s`, and does not enable audio to reduce encoding and network load.

The following items can be configured at the beginning of the script:

| Configuration | Description | Default Value |
| :-- | :-- | :-- |
| `NETWORK_TYPE` | `"default"`, `"lan"`, `"wifi_sta"`, or `"wifi_ap"` | `"wifi_sta"` |
| `WLAN_DEVICE` | `"auto"`, `"usb"`, `"sdio"`, or `"spi"` | `"auto"` |
| `NETWORK_TIMEOUT` | Timeout for waiting for a network address, in seconds | `15` |
| `VIDEO_TYPE` | H.265 or H.264 | H.265 |
| `ENABLE_AUDIO` | Whether to declare audio in the RTSP Session | `False` |
| `VIDEO_WIDTH` / `VIDEO_HEIGHT` | Encoding resolution | `1280` / `720` |
| `VIDEO_BIT_RATE` | VENC target bit rate, in Kbit/s | `512` |
| `VIDEO_GOP` | GOP frame count | `30` |

Modify the network type, Wi-Fi device type, and credentials, then run the script. The script selects the dynamically registered network interface through `libs.Network`, obtains the IP, and outputs a result similar to:

```text
RTSP server started: rtsp://192.168.1.108:8554/test (H265, 512 Kbit/s, audio disabled)
```

Use an RTSP client such as VLC to open this URL. H.265 typically saves more bandwidth at low bit rates; when the client does not support H.265, change `VIDEO_TYPE` to `mm.multi_media_type.media_h264`. Setting only `ENABLE_AUDIO` to `True` will not automatically establish an audio capture and encoding pipeline, and the example still only sends video.

Before closing the script, disconnect all RTSP clients first, then call `stop()` to release the encoder, camera, and RTSP service.

```{admonition} Note
For specific interfaces, network preparation, and performance configuration, please refer to [RTSP](../../api/mpp/k230_canmv_rtsp_module_api_manual.md).
```

### RTSP Streaming (Client Mode)

The example script path in the development board firmware is `/sdcard/examples/02-Media/rtsp_pusher.py`, and the SDK source code path is `src/canmv/resources/examples/02-Media/rtsp_pusher.py`. Unlike `rtsp_server.py` (which hosts an RTSP server and waits for clients to connect), `rtsp_pusher.py` acts as a client that actively connects to an external RTSP server (such as EasyDarwin, mediamtx, ZLMediaKit), and pushes the encoded H.264 video to it.

```python
# Description: This example demonstrates how to push encoded video to a remote RTSP server.
#
# Note: You will need an SD card to run this example.
#
# Unlike rtsp_server.py (which hosts the stream), the rtsp_pusher connects as a
# client to an external RTSP server URL and pushes H.264 video to it.
#
# Reference C++ sample: src/rtsmart/examples/mpp/sample_rtsppusher/main.cpp
#
# H.264 video at 512 Kbit/s is the default. Audio is not supported by the pusher.
#
# Flow (mirrors the C++ sample, which drives pushing from the encoder thread via
# OnVEncData; Python has no encoder callback, so we poll GetStream in the main
# thread instead of spawning a worker thread -- this avoids thread-creation
# failures on memory-constrained devices):
#   1. start the encoder so it begins producing SPS/PPS (K_VENC_HEADER)
#   2. on the first HEADER pack: rtsppusher_init() (deferred until the encoder is
#      producing so the pusher's frame queue does not starve the media pipeline on
#      startup); cache the SPS/PPS bytes, do not open yet
#   3. on every I frame: rtsppusher_pushvideoheader() with the latest cached SPS/PPS,
#      then (first time only) rtsppusher_open() -- pushing the header again before
#      each I frame keeps it in sync in case the encoder re-emits SPS/PPS mid-stream;
#      the underlying implementation prefixes this header to every subsequently
#      pushed frame (I and P) until it is updated again
#   4. push I/P frames with rtsppusher_pushvideodata(data, size, key_frame, timestamp)

from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os
import multimedia as mm
from libs.Network import connect_network

# Select "default", "lan", "wifi_sta", or "wifi_ap".
NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"  # "auto", "usb", "sdio", or "spi"
NETWORK_TIMEOUT = 15
WIFI_SSID = "Test"
WIFI_PASSWORD = "12345678"
# URL of the remote RTSP server that will receive the pushed stream.
# Replace the host with the address of your RTSP server (e.g. EasyDarwin/mediamtx/ZLMediaKit).
# The path needs a stream name after "live" (e.g. "/live/test"); some servers
# reject the push if the path stops at "/live" with no name.
RTSP_URL = "rtsp://192.168.1.100:8554/live/test"
# NOTE: the rtsp_pusher middleware hardcodes AV_CODEC_ID_H264 (see
# RtspPusherImpl.cpp), so it can only push H.264. H.265 is not supported.
VIDEO_TYPE = mm.multi_media_type.media_h264
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
VIDEO_BIT_RATE = 512  # Kbit/s
VIDEO_GOP = 30
VIDEO_FPS = 25
TRANSPORT = "tcp"  # "tcp" or "udp"


class RtspPusher:
    def __init__(self, url=RTSP_URL,
                 video_type=mm.multi_media_type.media_h264,
                 width=1280, height=720, bit_rate=512, gop_len=30,
                 fps=25, transport="tcp"):
        self.url = url                # Remote rtsp server url
        self.video_type = video_type  # Video type (pusher underlying only supports H.264)
        self.width = ALIGN_UP(width, 16)
        self.height = height
        self.bit_rate = bit_rate
        self.gop_len = gop_len
        self.fps = fps
        self.transport = transport
        self.rtsppusher = mm.rtsp_pusher()  # Instantiate rtsp pusher
        self.pusher_opened = False   # Whether pusher is opened (only init+open after first SPS/PPS is received)
        self.pusher_inited = False   # Whether pusher is inited
        self.started = False         # Whether encoding has started

        if bit_rate < 100 or bit_rate > 20000:
            raise ValueError("bit_rate must be between 100 and 20000 Kbit/s")
        if transport not in ("tcp", "udp"):
            raise ValueError("transport must be 'tcp' or 'udp'")
        # pusher middleware hardcodes AV_CODEC_ID_H264, does not support H.265
        if video_type != mm.multi_media_type.media_h264:
            raise ValueError("rtsp_pusher only supports media_h264 (middleware hardcodes H.264)")
        self.payload_type = Encoder.PAYLOAD_TYPE_H264
        self.profile = Encoder.H264_PROFILE_HIGH  # Consistent with C++ sample (VENC_PROFILE_H264_HIGH)

    def start(self):
        # Only initialize and start the encoder; pusher init is deferred until the first SPS/PPS is received (in run),
        # to avoid the pusher's 64MB queue allocation overwhelming the media pipeline before the encoder starts
        try:
            self._init_stream()
            self._start_stream()
            self.started = True
        except:
            if hasattr(self, 'encoder'):
                try:
                    self._stop_stream()
                except:
                    pass
            raise

    def run(self, duration=60):
        """Poll the encoder and push stream in the main thread for duration seconds.

        Does not create a worker thread: rtsppusher_open() internally blocks on RTSP handshake (up to ~5s),
        placing it in the main thread does not affect other threads; also avoids _thread.start_new_thread
        failing with EAGAIN when memory is tight.
        """
        streamData = StreamData()
        frame_count = 0
        last_header = None
        dropped_idr_count = 0
        end = time.ticks_add(time.ticks_ms(), duration * 1000)
        while time.ticks_diff(end, time.ticks_ms()) > 0:
            os.exitpoint()
            # Get one stream frame (finite timeout to avoid permanent blocking)
            if self.encoder.GetStream(streamData, 2000) != 0:
                continue
            # Push stream
            for pack_idx in range(0, streamData.pack_cnt):
                stream_type = streamData.stream_type[pack_idx]
                pack_data = bytes(uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx]))

                if stream_type == Encoder.STREAM_TYPE_HEADER:
                    last_header = pack_data
                    if not self.pusher_inited:
                        if self.rtsppusher.rtsppusher_init(self.width, self.height, self.url,
                                                           self.fps, self.transport) != 0:
                            raise RuntimeError("RTSP pusher init failed")
                        self.pusher_inited = True
                    continue

                is_idr = (stream_type == Encoder.STREAM_TYPE_I)
                if is_idr:
                    if last_header is None:
                        # Under normal startup timing, HEADER will arrive before the first I frame; this is only triggered in abnormal timing
                        dropped_idr_count += 1
                        if dropped_idr_count == 1 or dropped_idr_count % 30 == 0:
                            print("warning: I frame dropped, no SPS/PPS header yet (%d dropped)" % dropped_idr_count)
                        continue
                    # header is sent together with the I frame, ensuring they are back-to-back; pushvideoheader just updates
                    # the underlying cache, safe to call before or after open, and will be automatically prefixed to each subsequent frame (including P frames)
                    self.rtsppusher.rtsppusher_pushvideoheader(last_header, len(last_header))
                    if not self.pusher_opened:
                        print("opening pusher (rtsp handshake, may take ~5s)...")
                        if self.rtsppusher.rtsppusher_open() != 0:
                            raise RuntimeError("RTSP pusher open failed, check url: %s" % self.url)
                        self.pusher_opened = True
                        print("rtsp pusher opened: %s" % self.url)

                # Only push stream when there is video data and pusher is opened
                if self.pusher_opened:
                    timestamp = streamData.pts[pack_idx]
                    self.rtsppusher.rtsppusher_pushvideodata(pack_data, len(pack_data),
                                                             1 if is_idr else 0, timestamp)
                    frame_count += 1
                    if frame_count % 300 == 0:
                        print("pushed %d frames" % frame_count)
            # Release one stream frame
            self.encoder.ReleaseStream(streamData)

    def stop(self):
        if not self.started:
            return
        self.started = False
        # Stop encoding
        self._stop_stream()
        # Close pusher connection and deinitialize (pusher may not be init, need to check)
        if self.pusher_opened:
            self.rtsppusher.rtsppusher_close()
            self.pusher_opened = False
        if self.pusher_inited:
            self.rtsppusher.rtsppusher_deinit()
            self.pusher_inited = False

    def _init_stream(self):
        # Initialize sensor
        self.sensor = Sensor()
        self.sensor.reset()
        self.sensor.set_framesize(width=self.width, height=self.height, alignment=12)
        self.sensor.set_pixformat(Sensor.YUV420SP)
        # Instantiate video encoder
        self.encoder = Encoder()
        self.encoder.SetOutBufs(8, self.width, self.height)
        # Create encoder (without src/dst_frame_rate, use default 30, to avoid no frames due to mismatch with sensor actual frame rate)
        chnAttr = ChnAttrStr(self.payload_type, self.profile,
                             self.width, self.height,
                             bit_rate=self.bit_rate, gopLen=self.gop_len)
        self.encoder.Create(chnAttr)
        # Bind camera and venc
        self.link = MediaManager.link(self.sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, self.encoder.chn))

    def _start_stream(self):
        # Start encoding
        self.encoder.Start()
        # Start camera
        self.sensor.run()

    def _stop_stream(self):
        # Stop camera
        self.sensor.stop()
        # Unbind camera and venc
        self.link.destroy()
        # Stop encoding
        self.encoder.Stop()
        self.encoder.Destroy()


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    # Connect the selected network interface before opening the RTSP socket.
    nic, network_ip = connect_network(
        NETWORK_TYPE,
        ssid=WIFI_SSID,
        password=WIFI_PASSWORD,
        wlan_device=WLAN_DEVICE,
        timeout=NETWORK_TIMEOUT,
    )
    # Create rtsp pusher object
    rtsppusher = RtspPusher(url=RTSP_URL,
                            video_type=VIDEO_TYPE,
                            width=VIDEO_WIDTH,
                            height=VIDEO_HEIGHT,
                            bit_rate=VIDEO_BIT_RATE,
                            gop_len=VIDEO_GOP,
                            fps=VIDEO_FPS,
                            transport=TRANSPORT)
    # Start encoder (pusher will only init+open after receiving the first SPS/PPS)
    rtsppusher.start()
    # Print push stream information
    print("RTSP pusher started: %s (H264, %dx%d, %d Kbit/s, %s)" %
          (RTSP_URL, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_BIT_RATE, TRANSPORT))
    # Main thread pushes stream for 60s
    try:
        rtsppusher.run(60)
    finally:
        # Stop rtsp pusher
        rtsppusher.stop()
    print("done")
```

The following items can be configured at the beginning of the script:

| Configuration | Description | Default Value |
| :-- | :-- | :-- |
| `NETWORK_TYPE` | `"default"`, `"lan"`, `"wifi_sta"`, or `"wifi_ap"` | `"wifi_sta"` |
| `WLAN_DEVICE` | `"auto"`, `"usb"`, `"sdio"`, or `"spi"` | `"auto"` |
| `NETWORK_TIMEOUT` | Timeout for waiting for a network address, in seconds | `15` |
| `RTSP_URL` | Remote RTSP server address (a specific stream name is required after `live`, such as `/live/test`; some servers do not accept push requests whose path stops at `/live`) | `"rtsp://192.168.1.100:8554/live/test"` |
| `VIDEO_WIDTH` / `VIDEO_HEIGHT` | Encoding resolution | `1280` / `720` |
| `VIDEO_BIT_RATE` | VENC target bit rate, in Kbit/s | `512` |
| `VIDEO_GOP` | GOP frame count | `30` |
| `VIDEO_FPS` | Encoding frame rate | `25` |
| `TRANSPORT` | RTSP transport method, `"tcp"` or `"udp"` | `"tcp"` |

Modify `RTSP_URL` to the actual RTSP server address, along with the network type and Wi-Fi credentials, then run the script.
`RtspPusher.start()` first starts the camera and encoder; when polling the encoder output in the main thread `run()`, the first time a `STREAM_TYPE_HEADER` (SPS/PPS) is received, it triggers `rtsppusher_init()`;
After that, each time an I frame is received, the most recent SPS/PPS header is re-sent through `rtsppusher_pushvideoheader()`, then the I frame itself is pushed (the first time an I frame is received, `rtsppusher_open()` is also called to establish the connection with the server)——
This ensures that even if the encoder re-inserts SPS/PPS in the middle, the key frame and its corresponding header are paired and sent together, avoiding visual artifacts or stuttering such as "non-existing PPS" on the remote decoder.
The frame timestamp directly uses the `streamData.pts` output by VENC/vicap.

After the script runs, it outputs something similar to:

```text
RTSP pusher started: rtsp://192.168.1.100:8554/live/test (H264, 1280x720, 512 Kbit/s, tcp)
opening pusher (rtsp handshake, may take ~5s)...
rtsp pusher opened: rtsp://192.168.1.100:8554/live/test
```

By default, the script automatically calls `stop()` after running for 60 seconds to stop encoding, and close and deinitialize the RTSP push connection.

```{admonition} Note
For specific interfaces, network preparation, and performance configuration, please refer to [RTSP](../../api/mpp/k230_canmv_rtsp_module_api_manual.md).
```

### AI+RTSP Streaming

This example demonstrates how to use the AI module to implement face detection, and then output the image containing the detection results as an RTSP network stream for remote viewing or subsequent processing.
After the program starts, the relevant information will be displayed directly on the terminal interface, which will clearly give the RTSP stream access address in the following format: RTSP server started: rtsp://192.168.1.100:8554/test, users can use this address to obtain the image stream containing face detection results. Replace the example IP with your device's LAN IP.
Note:
If using a client to access the RTSP stream, before closing the program, please close all connected clients first, then perform the program closing operation.

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
from libs.WBCRtsp import WBCRtsp
import os,sys,ujson,gc,math
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import aidemo
from libs.Network import connect_network

NETWORK_TYPE = "wifi_sta"  # "default", "lan", "wifi_sta", or "wifi_ap"
WLAN_DEVICE = "auto"       # "auto", "usb", "sdio", or "spi"
NETWORK_TIMEOUT = 15
WIFI_SSID = "Test"
WIFI_PASSWORD = "12345678"

# Custom face detection class, inheriting from AIBase base class
class FaceDetectionApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, anchors, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)  # Call base class constructor
        self.kmodel_path = kmodel_path  # Model file path
        self.model_input_size = model_input_size  # Model input resolution
        self.confidence_threshold = confidence_threshold  # Confidence threshold
        self.nms_threshold = nms_threshold  # NMS (Non-Maximum Suppression) threshold
        self.anchors = anchors  # Anchor data, used for object detection
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]  # Resolution of image given by sensor to AI, and align width to 16
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]  # Display resolution, and align width to 16
        self.debug_mode = debug_mode  # Whether to enable debug mode
        self.ai2d = Ai2d(debug_mode)  # Instantiate Ai2d, used to implement model preprocessing
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)  # Set Ai2d input and output format and type

    # Configure preprocessing operation, here uses pad and resize, Ai2d supports crop/shift/pad/resize/affine, see specific code in /sdcard/app/libs/AI2D.py
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):  # Timer, enable if debug_mode is greater than 0
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size  # Initialize ai2d preprocessing configuration, default is the size given by sensor to AI, you can modify input size by setting input_image_size
            top, bottom, left, right,_ =letterbox_pad_param(self.rgb888p_size,self.model_input_size)
            self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])  # Pad edges
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)  # Resize image
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])  # Build preprocessing pipeline

    # Custom post-processing for current task, results is the list of model output arrays, here uses aidemo library's face_det_post_process interface
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
            post_ret = aidemo.face_det_post_process(self.confidence_threshold, self.nms_threshold, self.model_input_size[1], self.anchors, self.rgb888p_size, results)
            if len(post_ret) == 0:
                return post_ret
            else:
                return post_ret[0]

    # Draw detection results to the screen
    def draw_result(self, pl, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            if dets:
                pl.osd_img.clear()  # Clear OSD image
                for det in dets:
                    # Convert the coordinates of the detection box to coordinates at display resolution
                    x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                    x = x * self.display_size[0] // self.rgb888p_size[0]
                    y = y * self.display_size[1] // self.rgb888p_size[1]
                    w = w * self.display_size[0] // self.rgb888p_size[0]
                    h = h * self.display_size[1] // self.rgb888p_size[1]
                    pl.osd_img.draw_rectangle(x, y, w, h, color=(255, 255, 0, 255), thickness=2)  # Draw rectangle
            else:
                pl.osd_img.clear()

if __name__ == "__main__":
    # Add display mode, default hdmi, optional hdmi/lcd/lt9611/st7701/hx8399/nt35516, where hdmi defaults to lt9611, resolution 1920*1080; lcd defaults to st7701, resolution 800*480
    display_mode="lcd"
    # k230 remains unchanged, k230d can be adjusted to [640,360]
    rgb888p_size = [1280, 720]
    # Set model path and other parameters
    kmodel_path = "/sdcard/examples/kmodel/face_detection_320.kmodel"
    # Other parameters
    confidence_threshold = 0.5
    nms_threshold = 0.2
    anchor_len = 4200
    det_dim = 4
    anchors_path = "/sdcard/examples/utils/prior_data_320.bin"
    anchors = np.fromfile(anchors_path, dtype=np.float)
    anchors = anchors.reshape((anchor_len, det_dim))

    nic, network_ip = connect_network(
        NETWORK_TYPE,
        ssid=WIFI_SSID,
        password=WIFI_PASSWORD,
        wlan_device=WLAN_DEVICE,
        timeout=NETWORK_TIMEOUT,
    )

    # Initialize PipeLine, used for image processing pipeline
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode)
    # init wbc, wbc_width and wbc_height are the width and height of the original screen
    WBCRtsp.configure(wbc_width=480,wbc_height=800)
    pl.create(to_ide=False)  # Create PipeLine instance
    # Enable wbc encoding push stream
    WBCRtsp.start(network_ip)

    display_size=pl.get_display_size()
    # Initialize custom face detection instance
    face_det = FaceDetectionApp(kmodel_path, model_input_size=[320, 320], anchors=anchors, confidence_threshold=confidence_threshold, nms_threshold=nms_threshold, rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    face_det.config_preprocess()  # Configure preprocessing

    try:
        while True:
            img = pl.get_frame()            # Get current frame data
            res = face_det.run(img)         # Run inference on current frame
            face_det.draw_result(pl, res)   # Draw result
            pl.show_image()                 # Show result
            gc.collect()                    # Garbage collection
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        import sys
        sys.print_exception(e)

    face_det.deinit()                       # Deinitialize
    WBCRtsp.stop()                          # Stop WBC push stream
    pl.destroy()                            # Destroy PipeLine instance
```
