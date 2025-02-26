# 4. Video Examples Explanation

## 1. Overview

The K230 supports H264 or H265 encoding for video streams. The CanMV provides APIs that allow users to record and play MP4 files, as well as support RTSP streaming.

## 2. Examples

### 2.1 MP4 Recording

This example demonstrates how to record MP4 files on the CanMV development board.
You can use the `Mp4Container` class to record audio and video data from the camera. The `mp4_muxer_test` function provides a simple implementation for quick start.
For more flexible control, you can use the `kd_mp4_*` series of functions to encapsulate H264/H265 encoded video into MP4. These functions offer finer control, suitable for advanced users who need custom development. Refer to the `vi_bind_venc_mp4_test` function for detailed implementation.

```python
# Save MP4 file example
#
# Note: You will need an SD card to run this example.
#
# You can capture audio and video and save them as MP4. The current version only supports MP4 format, video supports 264/265, and audio supports g711a/g711u.

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

from mpp.mp4_format import *
from mpp.mp4_format_struct import *
from media.vencoder import *
from media.sensor import *
from media.media import *
import uctypes
import time
import os

def mp4_muxer_init(file_name, fmp4_flag):
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

def mp4_muxer_create_audio_track(mp4_handle, channel, sample_rate, bit_per_sample, audio_payload_type):
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

def vi_bind_venc_mp4_test(file_name, width=1280, height=720, venc_payload_type=K_PT_H264):
    print("venc_test start")
    venc_chn = VENC_CHN_ID_0
    width = ALIGN_UP(width, 16)

    frame_data = k_mp4_frame_data_s()
    save_idr = bytearray(width * height * 3 // 4)
    idr_index = 0

    # mp4 muxer init
    mp4_handle = mp4_muxer_init(file_name, True)

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
    sensor.set_framesize(width=width, height=height, alignment=12)
    sensor.set_pixformat(Sensor.YUV420SP)

    # Instantiate video encoder
    encoder = Encoder()
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # Bind camera and venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, venc_chn))

    # Initialize media manager
    MediaManager.init()

    if venc_payload_type == K_PT_H264:
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif venc_payload_type == K_PT_H265:
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # Create encoder
    encoder.Create(venc_chn, chnAttr)

    # Start encoding
    encoder.Start(venc_chn)
    # Start camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    video_start_timestamp = 0
    get_first_I_frame = False

    try:
        while True:
            os.exitpoint()
            encoder.GetStream(venc_chn, streamData)  # Get a frame of stream
            stream_type = streamData.stream_type[0]

            # Retrieve first IDR frame and write to MP4 file. Note: The first frame must be an IDR frame.
            if not get_first_I_frame:
                if stream_type == encoder.STREAM_TYPE_I:
                    get_first_I_frame = True
                    video_start_timestamp = streamData.pts[0]
                    save_idr[idr_index:idr_index+streamData.data_size[0]] = uctypes.bytearray_at(streamData.data[0], streamData.data_size[0])
                    idr_index += streamData.data_size[0]

                    frame_data.codec_id = video_payload_type
                    frame_data.data = uctypes.addressof(save_idr)
                    frame_data.data_length = idr_index
                    frame_data.time_stamp = streamData.pts[0] - video_start_timestamp

                    ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
                    if ret:
                        raise OSError("kd_mp4_write_frame failed.")
                    encoder.ReleaseStream(venc_chn, streamData)
                    continue

                elif stream_type == encoder.STREAM_TYPE_HEADER:
                    save_idr[idr_index:idr_index+streamData.data_size[0]] = uctypes.bytearray_at(streamData.data[0], streamData.data_size[0])
                    idr_index += streamData.data_size[0]
                    encoder.ReleaseStream(venc_chn, streamData)
                    continue
                else:
                    encoder.ReleaseStream(venc_chn, streamData)  # Release a frame of stream
                    continue

            # Write video stream to MP4 file (not first IDR frame)
            frame_data.codec_id = video_payload_type
            frame_data.data = streamData.data[0]
            frame_data.data_length = streamData.data_size[0]
            frame_data.time_stamp = streamData.pts[0] - video_start_timestamp

            print("video size: ", streamData.data_size[0], "video type: ", streamData.stream_type[0], "video timestamp:", frame_data.time_stamp)
            ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
            if ret:
                raise OSError("kd_mp4_write_frame failed.")

            encoder.ReleaseStream(venc_chn, streamData)  # Release a frame of stream

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
    # Destroy camera and venc binding
    del link
    # Stop encoding
    encoder.Stop(venc_chn)
    # Destroy encoder
    encoder.Destroy(venc_chn)
    # Clean buffer
    MediaManager.deinit()

    # Destroy mp4 muxer
    kd_mp4_destroy_tracks(mp4_handle)
    kd_mp4_destroy(mp4_handle)

    print("venc_test stop")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_mp4_test("/sdcard/examples/test.mp4", 1280, 720)
```

```{admonition} Note
For detailed interface definitions, please refer to [mp4muxer](../../api/mpp/K230_CanMV_MP4模块API手册.md)
```

### 2.2 MP4 Demuxing

This example demonstrates how to use the MP4 demuxer on the CanMV development board to parse MP4 files and extract video and audio streams.

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
        raise OSError("kd_mp4_create failed:", filename)

    file_info = k_mp4_file_info_s()
    kd_mp4_get_file_info(mp4_handle.value, file_info)

    for i in range(file_info.track_num):
        track_info = k_mp4_track_info_s()
        ret = kd_mp4_get_track_by_index(mp4_handle.value, i, track_info)
        if ret < 0:
            raise ValueError("kd_mp4_get_track_by_index failed")

        if track_info.track_type == K_MP4_STREAM_VIDEO:
            if track_info.video_info.codec_id in [K_MP4_CODEC_ID_H264, K_MP4_CODEC_ID_H265]:
                video_track = True
                video_info = track_info.video_info
                print("    codec_id: ", video_info.codec_id)
                print("    track_id: ", video_info.track_id)
                print("    width: ", video_info.width)
                print("    height: ", video_info.height)
            else:
                print("video not support codec id:", track_info.video_info.codec_id)
        elif track_info.track_type == K_MP4_STREAM_AUDIO:
            if track_info.audio_info.codec_id in [K_MP4_CODEC_ID_G711A, K_MP4_CODEC_ID_G711U]:
                audio_track = True
                audio_info = track_info.audio_info
                print("    codec_id: ", audio_info.codec_id)
                print("    track_id: ", audio_info.track_id)
                print("    channels: ", audio_info.channels)
                print("    sample_rate: ", audio_info.sample_rate)
                print("    bit_per_sample: ", audio_info.bit_per_sample)
            else:
                print("audio not support codec id:", track_info.audio_info.codec_id)

    if not video_track:
        raise ValueError("video track not found")

    start_system_time = time.ticks_ms()
    start_video_timestamp = 0

    while True:
        frame_data = k_mp4_frame_data_s()
        ret = kd_mp4_get_frame(mp4_handle.value, frame_data)
        if ret < 0:
            raise OSError("get frame data failed")

        if frame_data.eof:
            break

        if frame_data.codec_id in [K_MP4_CODEC_ID_H264, K_MP4_CODEC_ID_H265]:
            data = uctypes.bytes_at(frame_data.data, frame_data.data_length)
            print("video frame_data.codec_id:", frame_data.codec_id, "data_length:", frame_data.data_length, "timestamp:", frame_data.time_stamp)

            video_timestamp_elapsed = frame_data.time_stamp - start_video_timestamp
            current_system_time = time.ticks_ms()
            system_time_elapsed = current_system_time - start_system_time

            if system_time_elapsed < video_timestamp_elapsed:
                time.sleep_ms(video_timestamp_elapsed - system_time_elapsed)

        elif frame_data.codec_id in [K_MP4_CODEC_ID_G711A, K_MP4_CODEC_ID_G711U]:
            data = uctypes.bytes_at(frame_data.data, frame_data.data_length)
            print("audio frame_data.codec_id:", frame_data.codec_id, "data_length:", frame_data.data_length, "timestamp:", frame_data.time_stamp)

    kd_mp4_destroy(mp4_handle.value)

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    demuxer_mp4("/sdcard/examples/test.mp4")
```

```{admonition} Note
For detailed interface definitions, please refer to [mp4demuxer](../../api/mpp/K230_CanMV_MP4解复用器模块API手册.md)
```

### 2.5 H264/H265 Decoding

This example demonstrates how to perform video decoding on the CanMV development board.

```python
# Video decode example
#
# Note: You will need an SD card to run this example.
#
# You can decode H264/H265 and display them on the screen

from media.media import *
from mpp.payload_struct import *
import media.vdecoder as vdecoder
from media.display import *

import time, os

STREAM_SIZE = 40960
def vdec_test(file_name, width=1280, height=720):
    print("vdec_test start")
    vdec_chn = VENC_CHN_ID_0
    vdec_width = ALIGN_UP(width, 16)
    vdec_height = height
    vdec = None
    vdec_payload_type = K_PT_H264

    # display_type = Display.VIRT
    display_type = Display.ST7701  # Use ST7701 LCD screen as output display, max resolution 800*480
    # display_type = Display.LT9611  # Use HDMI as output display

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
    vdec = vdecoder.Decoder(vdec_payload_type)

    # Initialize display
    if display_type == Display.VIRT:
        Display.init(display_type, width=vdec_width, height=vdec_height, fps=30)
    else:
        Display.init(display_type, to_ide=True)

    # Initialize vb buffer
    MediaManager.init()

    # Create video decoder
    vdec.create()

    # Bind video decoder to display
    bind_info = vdec.bind_info(width=vdec_width, height=vdec_height, chn=vdec.get_vdec_channel())
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1)

    vdec.start()
    # Open file
    with open(file_name, "rb") as fi:
        while True:
            os.exitpoint()
            # Read video stream data
            data = fi.read(STREAM_SIZE)
            if not data:
                break
            # Decode stream data
            vdec.decode(data)

    # Stop video decoder
    vdec.stop()
    # Destroy video decoder
    vdec.destroy()
    time.sleep(1)

    # Deinitialize display
    Display.deinit()
    # Release vb buffer
    MediaManager.deinit()

    print("vdec_test stop")


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vdec_test("/sdcard/examples/test.264", 800, 480)  # Decode H264/H265 video file
```

```{admonition} Note
For detailed interface definitions, please refer to [VDEC](../../api/mpp/K230_CanMV_VDEC_Module_API_Manual.md)
```

### 2.6 RTSP Streaming

This example demonstrates how to stream video and audio to the network using the RTSP server.

```python
# Description: This example demonstrates how to stream video and audio to the network using the RTSP server.
#
# Note: You will need an SD card to run this example.
#
# You can run the RTSP server to stream video and audio to the network

from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os
import _thread
import multimedia as mm
from time import *

class RtspServer:
    def __init__(self, session_name="test", port=8554, video_type=mm.multi_media_type.media_h264, enable_audio=False):
        self.session_name = session_name  # Session name
        self.video_type = video_type  # Video type H264/H265
        self.enable_audio = enable_audio  # Enable audio
        self.port = port  # RTSP port number
        self.rtspserver = mm.rtsp_server()  # Instantiate RTSP server
        self.venc_chn = VENC_CHN_ID_0  # VENC channel
        self.start_stream = False  # Start streaming thread
        self.runthread_over = False  # Streaming thread finished

    def start(self):
        # Initialize streaming
        self._init_stream()
        self.rtspserver.rtspserver_init(self.port)
        # Create session
        self.rtspserver.rtspserver_createsession(self.session_name, self.video_type, self.enable_audio)
        # Start RTSP server
        self.rtspserver.rtspserver_start()
        self._start_stream()

        # Start streaming thread
        self.start_stream = True
        _thread.start_new_thread(self._do_rtsp_stream, ())

    def stop(self):
        if not self.start_stream:
            return
        # Wait for streaming thread to exit
        self.start_stream = False
        while not self.runthread_over:
            sleep(0.1)
        self.runthread_over = False

        # Stop streaming
        self._stop_stream()
        self.rtspserver.rtspserver_stop()
        self.rtspserver.rtspserver_deinit()

    def get_rtsp_url(self):
        return self.rtspserver.rtspserver_getrtspurl(self.session_name)

    def _init_stream(self):
        width = 1280
        height = 720
        width = ALIGN_UP(width, 16)
        # Initialize sensor
        self.sensor = Sensor()
        self.sensor.reset()
        self.sensor.set_framesize(width=width, height=height, alignment=12)
        self.sensor.set_pixformat(Sensor.YUV420SP)
        # Instantiate video encoder
        self.encoder = Encoder()
        self.encoder.SetOutBufs(self.venc_chn, 8, width, height)
        # Bind camera and VENC
        self.link = MediaManager.link(self.sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, self.venc_chn))
        # Initialize media manager
        MediaManager.init()
        # Create encoder
        chnAttr = ChnAttrStr(self.encoder.PAYLOAD_TYPE_H264, self.encoder.H264_PROFILE_MAIN, width, height)
        self.encoder.Create(self.venc_chn, chnAttr)

    def _start_stream(self):
        # Start encoding
        self.encoder.Start(self.venc_chn)
        # Start camera
        self.sensor.run()

    def _stop_stream(self):
        # Stop camera
        self.sensor.stop()
        # Unbind camera and VENC
        del self.link
        # Stop encoding
        self.encoder.Stop(self.venc_chn)
        self.encoder.Destroy(self.venc_chn)
        # Clean buffer
        MediaManager.deinit()

    def _do_rtsp_stream(self):
        try:
            streamData = StreamData()
            while self.start_stream:
                os.exitpoint()
                # Get a frame of stream
                self.encoder.GetStream(self.venc_chn, streamData)
                # Stream data
                for pack_idx in range(streamData.pack_cnt):
                    stream_data = bytes(uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx]))
                    self.rtspserver.rtspserver_sendvideodata(self.session_name, stream_data, streamData.data_size[pack_idx], 1000)
                # Release a frame of stream
                self.encoder.ReleaseStream(self.venc_chn, streamData)

        except BaseException as e:
            print(f"Exception {e}")
        finally:
            self.runthread_over = True
            # Stop RTSP server
            self.stop()

        self.runthread_over = True

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    # Create RTSP server object
    rtspserver = RtspServer()
    # Start RTSP server
    rtspserver.start()
    # Print RTSP URL
    print("RTSP server start:", rtspserver.get_rtsp_url())
    # Stream for 60 seconds
    sleep(60)
    # Stop RTSP server
    rtspserver.stop()
    print("done")
```

```{admonition} Note
For detailed interface definitions, please refer to [RTSP](../../api/mpp/K230_CanMV_RTSP_Module_API_Manual.md)
```
