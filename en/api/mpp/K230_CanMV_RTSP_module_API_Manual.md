# 3.9 RTSP Module API Manual

## 1. Overview

This document aims to provide a detailed introduction to the usage and functions of the K230_CanMV RTSP module API. The RTSP module is specifically designed for creating and managing RTSP servers, supporting the transmission and reception of video and audio data.

## 2. API Introduction

The multimedia module provides the following RTSP interfaces:

1. `multimedia.rtspserver_create`: Create an RTSP server.
1. `multimedia.rtspserver_destroy`: Destroy an RTSP server.
1. `multimedia.rtspserver_init`: Initialize an RTSP server.
1. `multimedia.rtspserver_deinit`: Deinitialize an RTSP server.
1. `multimedia.rtspserver_createsession`: Create an RTSP session.
1. `multimedia.rtspserver_destroysession`: Destroy an RTSP session.
1. `multimedia.rtspserver_getrtspurl`: Get the RTSP URL.
1. `multimedia.rtspserver_start`: Start the RTSP server.
1. `multimedia.rtspserver_stop`: Stop the RTSP server.
1. `multimedia.rtspserver_sendvideodata`: Send video data to the RTSP server.
1. `multimedia.rtspserver_sendaudiodata`: Send audio data to the RTSP server.

These interfaces can be used to create and manage RTSP servers, create and destroy RTSP sessions, send video and audio data to the server, and obtain the RTSP URL for streaming.

### 2.1 multimedia.rtspserver_create

**Description**
Used to create an RTSP server.

**Syntax**

```python
rtspserver_create()
```

**Parameters**

None

**Return Value**

| Return Value | Description         |
|--------------|---------------------|
| 0            | Creation successful |
| Non-0        | Creation failed     |

### 2.2 multimedia.rtspserver_destroy

**Description**
Used to destroy an RTSP server.

**Syntax**

```python
rtspserver_destroy()
```

**Parameters**

None

**Return Value**

| Return Value | Description         |
|--------------|---------------------|
| 0            | Destruction successful |
| Non-0        | Destruction failed  |

### 2.3 multimedia.rtspserver_init

**Description**
Initialize an RTSP server.

**Syntax**

```python
rtspserver_init(port)
```

**Parameters**

| Parameter Name | Description               | Input / Output |
|----------------|---------------------------|----------------|
| port           | RTSP server listening port | Input          |

**Return Value**
None

**Example**

```python
rtspserver_init(8554)
```

### 2.4 multimedia.rtspserver_deinit

**Description**
Deinitialize an RTSP server.

**Syntax**

```python
rtspserver_deinit()
```

**Parameters**

None

**Return Value**
None

**Example**

```python
rtspserver_deinit()
```

### 2.5 multimedia.rtspserver_createsession

**Description**
Create an RTSP session.

**Syntax**

```python
rtspserver_createsession(session_name, video_type, enable_audio)
```

**Parameters**

| Parameter Name | Description            | Input / Output |
|----------------|------------------------|----------------|
| session_name   | Session name           | Input          |
| video_type     | Video encoding type    | Input          |
| enable_audio   | Whether to enable audio | Input          |

**Return Value**
None

**Example**

```python
rtspserver_createsession("session1", "h264", True)
```

### 2.6 multimedia.rtspserver_destroysession

**Description**
Destroy an RTSP session.

**Syntax**

```python
rtspserver_destroysession(session_name)
```

**Parameters**

- `session_name`: Session name.

**Return Value**
None

**Example**

```python
rtspserver_destroysession("session1")
```

### 2.7 multimedia.rtspserver_getrtspurl

**Description**
Get the RTSP URL.

**Syntax**

```python
rtspserver_getrtspurl()
```

**Parameters**

None

**Return Value**

| Parameter Name | Description | Input / Output |
|----------------|-------------|----------------|
| url            | RTSP URL    | Output         |

**Example**

```python
url = rtspserver_getrtspurl()
print(url)
```

### 2.8 multimedia.rtspserver_start

**Description**
Start the RTSP server.

**Syntax**

```python
rtspserver_start()
```

**Parameters**

None

**Return Value**
None

**Example**

```python
rtspserver_start()
```

### 2.9 multimedia.rtspserver_stop

**Description**
Stop the RTSP server.

**Syntax**

```python
rtspserver_stop()
```

**Parameters**

None

**Return Value**
None

**Example**

```python
rtspserver_stop()
```

### 2.10 multimedia.rtspserver_sendvideodata

**Description**
Send video data to the RTSP server.

**Syntax**

```python
rtspserver_sendvideodata(session_name, data, size, timestamp)
```

**Parameters**

| Parameter Name | Description   | Input / Output |
|----------------|---------------|----------------|
| session_name   | Session name  | Input          |
| data           | Video data    | Input          |
| size           | Data size     | Input          |
| timestamp      | Timestamp     | Input          |

**Return Value**
None

**Example**

```python
rtspserver_sendvideodata("session1", video_data, video_size, video_timestamp)
```

### 2.11 multimedia.rtspserver_sendaudiodata

**Description**
Send audio data to the RTSP server.

**Syntax**

```python
rtspserver_sendaudiodata(session_name, data, size, timestamp)
```

**Parameters**

| Parameter Name | Description   | Input / Output |
|----------------|---------------|----------------|
| session_name   | Session name  | Input          |
| data           | Audio data    | Input          |
| size           | Data size     | Input          |
| timestamp      | Timestamp     | Input          |

**Return Value**
None

**Example**

```python
rtspserver_sendaudiodata("session1", audio_data, audio_size, audio_timestamp)
```

## 3. Example Program

```python
# Example: Demonstrates how to send video and audio data to network streaming via RTSP server.
# Note: Running this example requires an SD card.
# You can start the RTSP server for video and audio streaming.

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
        self.video_type = video_type      # Video encoding type (H264/H265)
        self.enable_audio = enable_audio  # Whether to enable audio
        self.port = port                  # RTSP server port number
        self.rtspserver = mm.rtsp_server()  # Instantiate RTSP server
        self.venc_chn = VENC_CHN_ID_0     # Video encoding channel
        self.start_stream = False         # Whether to start streaming thread
        self.runthread_over = False       # Whether streaming thread has ended

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
        # Bind camera and venc
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
        # Unbind camera and venc
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
                # Streaming
                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = bytes(uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx]))
                    self.rtspserver.rtspserver_sendvideodata(self.session_name, stream_data, streamData.data_size[pack_idx], 1000)
                    #print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])
                # Release a frame of stream
                self.encoder.ReleaseStream(self.venc_chn, streamData)

        except BaseException as e:
            print(f"Exception {e}")
        finally:
            self.runthread_over = True
            # Stop rtsp server
            self.stop()

        self.runthread_over = True

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    # Create rtsp server object
    rtspserver = RtspServer()
    # Start rtsp server
    rtspserver.start()
    # Print rtsp url
    print("rtsp server start:", rtspserver.get_rtsp_url())
    # Stream for 60s
    sleep(60)
    # Stop rtsp server
    rtspserver.stop()
    print("done")
```
