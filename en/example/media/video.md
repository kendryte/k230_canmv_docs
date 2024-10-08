# 4. Video Tutorial Explanation

## 1. Overview

The K230 supports H264 or H265 encoding for video streams. The API provided in CanMV allows users to record and play MP4 files and also supports RTSP streaming.

## 2. Examples

### 2.1 MP4 Recording

This example program demonstrates the mp4 muxer functionality on the CanMV development board.

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

```{admonition} Tip
For specific interface definitions, please refer to [player](../../api/mpp/K230_CanMV_Player_Module_API_Manual.md)
```

### 2.2 MP4 Playback

This example program demonstrates the functionality of an mp4 file player on the CanMV development board.

```python
# Play MP4 file example
#
# Note: You will need an SD card to run this example.
#
# You can load local files to play. The current version only supports MP4 format, video supports 264/265, and audio supports g711a/g711u.

from media.player import *  # Import player module for playing mp4 files
import os

start_play = False  # Playback end flag

def player_event(event, data):
    global start_play
    if event == K_PLAYER_EVENT_EOF:  # Playback end marker
        start_play = False  # Set playback end marker

def play_mp4_test(filename):
    global start_play
    # player = Player()  # Create player object
    # Use IDE as output display, can set any resolution
    player = Player(Display.VIRT)
    # Use ST7701 LCD screen as output display, max resolution 800*480
    # player = Player(Display.ST7701)
    # Use HDMI as output display
    # player = Player(Display.LT9611)
    player.load(filename)  # Load mp4 file
    player.set_event_callback(player_event)  # Set player event callback
    player.start()  # Start playback
    start_play = True

    # Wait for playback to end
    try:
        while start_play:
            time.sleep(0.1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)

    player.stop()  # Stop playback
    print("play over")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    play_mp4_test("/sdcard/examples/test.mp4")  # Play mp4 file
```

```{admonition} Tip
For specific interface definitions, please refer to [player](../../api/mpp/K230_CanMV_Player_Module_API_Manual.md)
```

### 2.3 H264/H265 Encoding

This example program demonstrates the video encoding functionality on the CanMV development board.

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

def vi_bind_venc_test(file_name, width=1280, height=720):
    print("venc_test start")
    venc_chn = VENC_CHN_ID_0
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
    sensor.set_framesize(width=width, height=height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)

    # Instantiate video encoder
    encoder = Encoder()
    # Set video encoder output buffer
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

    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                encoder.GetStream(venc_chn, streamData)  # Get a frame stream

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data)  # Stream write to file
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(venc_chn, streamData)  # Release a frame stream

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
    print("venc_test stop")

def stream_venc_test(file_name, width=1280, height=720):
    print("venc_test start")
    venc_chn = VENC_CHN_ID_0
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
    sensor.set_framesize(width=width, height=height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)

    # Instantiate video encoder
    encoder = Encoder()
    # Set video encoder output buffer
    encoder.SetOutBufs(venc_chn, 8, width, height)

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

    yuv420sp_img = None
    frame_info = k_video_frame_info()
    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                yuv420sp_img = sensor.snapshot(chn=CAM_CHN_ID_0)
                if yuv420sp_img == -1:
                    continue

                frame_info.v_frame.width = yuv420sp_img.width()
                frame_info.v_frame.height = yuv420sp_img.height()
                frame_info.v_frame.pixel_format = Sensor.YUV420SP
                frame_info.pool_id = yuv420sp_img.poolid()
                frame_info.v_frame.phys_addr[0] = yuv420sp_img.phyaddr()
                if yuv420sp_img.width() == 800 and yuv420sp_img.height() == 480:
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width * frame_info.v_frame.height + 1024
                elif yuv420sp_img.width() == 1920 and yuv420sp_img.height() == 1080:
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width * frame_info.v_frame.height + 3072
                elif yuv420sp_img.width() == 640 and yuv420sp_img.height() == 360:
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width * frame_info.v_frame.height + 3072
                else:
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width * frame_info.v_frame.height

                encoder.SendFrame(venc_chn, frame_info)
                encoder.GetStream(venc_chn, streamData)  # Get a frame stream

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data)  # Stream write to file
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(venc_chn, streamData)  # Release a frame stream

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
    encoder.Stop(venc_chn)
    # Destroy encoder
    encoder.Destroy(venc_chn)
    # Clean buffer
    MediaManager.deinit()
    print("venc_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_test("/sdcard/examples/test.264", 800, 480)  # vi bind venc example
    # stream_venc_test("/sdcard/examples/test.264", 800, 480)  # venc encode data stream example
```

```{admonition} Tip
For specific interface definitions, please refer to [VENC](../../api/mpp/K230_CanMV_VENC_Module_API_Manual.md)
```

### 2.4 H264/H265 Decoding

This example program demonstrates the video decoding functionality on the CanMV development board.

```python
# Video encode example
#
# Note: You will need an SD card to run this example.
# (The rest of the code for decoding would follow a similar pattern to the encoding example.)
# You can decode 264/265 and display them on the screen

from media.media import *
from mpp.payload_struct import*
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
    # vdecoder.Decoder.vb_pool_config(4, 6)
    vdec = vdecoder.Decoder(vdec_payload_type)

    # Initialize display
    if display_type == Display.VIRT:
        Display.init(display_type, width=vdec_width, height=vdec_height, fps=30)
    else:
        Display.init(display_type, to_ide=True)

    # vb buffer initialization
    MediaManager.init()

    # Create video decoder
    vdec.create()

    # vdec bind display
    bind_info = vdec.bind_info(width=vdec_width, height=vdec_height, chn=vdec.get_vdec_channel())
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1)

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

if **name** == "**main**":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vdec_test("/sdcard/examples/test.264", 800, 480)  # Decode 264/265 video file

```{admonition} Tip
For specific interface definitions, please refer to [VDEC](../../api/mpp/K230_CanMV_VDEC_Module_API_Manual.md)
```

### 2.5 RTSP Streaming

This example demonstrates how to use the RTSP server to stream video and audio to the network.

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
        self.session_name = session_name  # session name
        self.video_type = video_type  # Video type 264/265
        self.enable_audio = enable_audio  # Enable audio
        self.port = port  # RTSP port number
        self.rtspserver = mm.rtsp_server()  # Instantiate RTSP server
        self.venc_chn = VENC_CHN_ID_0  # VENC channel
        self.start_stream = False  # Whether to start streaming thread
        self.runthread_over = False  # Whether streaming thread is over

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
        # self.rtspserver.rtspserver_destroysession(self.session_name)
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
        # Init media manager
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
                # Get a frame stream
                self.encoder.GetStream(self.venc_chn, streamData)
                # Stream
                for pack_idx in range(streamData.pack_cnt):
                    stream_data = bytes(uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx]))
                    self.rtspserver.rtspserver_sendvideodata(self.session_name, stream_data, streamData.data_size[pack_idx], 1000)
                    # print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])
                # Release a frame stream
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
    # Stream for 60s
    sleep(60)
    # Stop RTSP server
    rtspserver.stop()
    print("done")
```

```{admonition} Tip
For specific interface definitions, please refer to [RTSP](../../api/mpp/K230_CanMV_RTSP_Module_API_Manual.md)
```
