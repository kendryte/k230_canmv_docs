# `RTSP` Module API Manual

## Overview

`media.rtspserver.RtspServer` provides a high-level wrapper for `Sensor -> VENC -> RTSP`. The current default configuration is H.265, `1280 x 720`, and `512 Kbit/s`, with audio disabled to reduce encoding and network resource consumption. The underlying `multimedia.rtsp_server` object can also be used when the application manages the encoder and media transmission itself. Stream pulling and decoding use the firmware type `multimedia.RtspClient`. Display is still handled by `Display.bind_layer`, as described at the end.

The example script is located at `/sdcard/examples/02-Media/rtsp_server.py` in the development board firmware,
and at `src/canmv/resources/examples/02-Media/rtsp_server.py` in the SDK source code. It includes the same
camera streaming mode as the high-level wrapper, and adds LAN/Wi-Fi configuration, error checking, and configurable parameters.

```{important}
RTSP 服务本身不负责联网。调用 `start()` 前，应用必须先连接 LAN、Wi-Fi STA 或 Wi-Fi AP。推荐使用 `libs.Network` 完成接口选择并设置默认上行。
```

## `RtspServer`

### Constructor

```python
from media.rtspserver import RtspServer
import multimedia as mm

server = RtspServer(
    session_name="test",
    port=8554,
    video_type=mm.multi_media_type.media_h265,
    enable_audio=False,
    width=1280,
    height=720,
    bit_rate=512,
    gop_len=30,
)
```

| Parameter | Description | Default |
| :-- | :-- | :-- |
| `session_name` | RTSP session name and URL path | `"test"` |
| `port` | RTSP listening port | `8554` |
| `video_type` | `mm.multi_media_type.media_h265` or `media_h264` | `media_h265` |
| `enable_audio` | Declares audio in the RTSP Session | `False` |
| `width` | Encoding width; automatically aligned up to a multiple of 16 internally | `1280` |
| `height` | Encoding height | `720` |
| `bit_rate` | VENC CBR target bitrate, in Kbit/s, ranging from `100` to `20000` | `512` |
| `gop_len` | Number of frames in the GOP | `30` |

When `video_type` is not H.264/H.265, or `bit_rate` is outside the supported range, the constructor raises `ValueError`.

### `start()`

```python
server.start()
```

Initializes the RTSP service and Session, creates the Sensor/VENC pipeline, starts encoding, and sends video in a background thread. To directly inspect the port binding and Session creation return status, use the `multimedia.rtsp_server` API below, or use the `RtspServer` class from the accompanying example.

### `stop()`

```python
server.stop()
```

Stops the background streaming thread, stops VENC and Sensor, destroys the media link, and closes the RTSP service. The application should call this method before exiting to release hardware resources.

### `get_rtsp_url()`

```python
url = server.get_rtsp_url()
```

Returns the RTSP URL of the current session. For example, when the network address is `192.168.1.108`, the default URL is:

```text
rtsp://192.168.1.108:8554/test
```

## Usage Example

The following example uses a low bitrate H.265. If the client does not support H.265, switch to H.264.

```python
import multimedia as mm
from libs.Network import connect_network
from media.rtspserver import RtspServer

# Only LAN configuration is shown; see /sdcard/examples/02-Media/rtsp_server.py for the Wi-Fi connection method.
lan, ip = connect_network("lan")

server = RtspServer(
    session_name="camera",
    video_type=mm.multi_media_type.media_h265,
    width=1280,
    height=720,
    bit_rate=512,
    gop_len=30,
)

started = False
try:
    server.start()
    started = True
    print(server.get_rtsp_url())
    # Keep the script running so that clients can connect.
finally:
    if started:
        server.stop()
```

## Audio and Compatibility

`enable_audio=False` is used by default. The accompanying `RtspServer` wrapper and example only establish the video capture, encoding, and transmission chain; setting `enable_audio` to `True` alone does not automatically capture or transmit audio.

H.265 is generally more efficient at low bitrates, but compatibility with some RTSP clients is weaker. When prioritizing compatibility with VLC, older NVRs, or browser plugins, use the following:

```python
video_type=mm.multi_media_type.media_h264
```

## Performance Recommendations

- `512 Kbit/s` is suitable for the default preview and resource-constrained scenarios. For higher quality, gradually increase `bit_rate` while monitoring the encoding and Wi-Fi load.
- Reducing the resolution is usually more effective than reducing only the bitrate; for example, you can choose `640 x 360` or `800 x 480` when the network is weak.
- A shorter `gop_len` can reduce the time new clients wait for a keyframe, but it increases keyframe overhead. In real-time low-bitrate scenarios, it is usually kept at `30`; when building a custom VENC streaming chain, you can use `Encoder.RequestIDR()` in combination with this to reduce the wait time for the first frame.

## Low-Level `multimedia.rtsp_server` API

When you need to manage the camera, VENC, or audio yourself, you can use the native RTSP object directly:

```python
import multimedia as mm

server = mm.rtsp_server()
```

The constructor already creates the object; usually, there is no need to call `rtspserver_create()` again. All methods with `session_name` use the name specified when the Session was created.

### Lifecycle

| Method | Return Value | Description |
| :-- | :-- | :-- |
| `rtspserver_init(port)` | Status code | Initializes the service and listens on the RTSP port. `0` indicates success. |
| `rtspserver_createsession(name, video_type, enable_audio)` | Status code | Creates an RTSP Session; `video_type` uses `mm.multi_media_type.media_h264`, `media_h265`, or a type supported by the low-level API. |
| `rtspserver_getrtspurl(name)` | `str` | Returns the RTSP URL of the Session; throws a `RuntimeError` when the Session does not exist. |
| `rtspserver_start()` | None | Starts the RTSP service. |
| `rtspserver_stop()` | None | Stops the RTSP service. |
| `rtspserver_destroysession(name)` | Status code | Destroys the specified Session. |
| `rtspserver_deinit()` | None | Deinitializes the service. |
| `rtspserver_destroy()` | None | Releases the object; safe to call repeatedly. |

A typical manual workflow is as follows:

```python
import multimedia as mm

session = "camera"
server = mm.rtsp_server()
if server.rtspserver_init(8554) != 0:
    raise RuntimeError("RTSP port bind failed")
if server.rtspserver_createsession(
        session, mm.multi_media_type.media_h265, False) != 0:
    server.rtspserver_deinit()
    raise RuntimeError("RTSP session creation failed")

try:
    server.rtspserver_start()
    print(server.rtspserver_getrtspurl(session))
    # Call rtspserver_sendvideodata() after obtaining encoded data from VENC.
finally:
    server.rtspserver_stop()
    server.rtspserver_deinit()
    server.rtspserver_destroy()
```

### Media Transmission

| Method | Return Value | Description |
| :-- | :-- | :-- |
| `rtspserver_sendvideodata(name, data, size, timestamp)` | Status code | Sends encoded video data in memory. |
| `rtspserver_sendaudiodata(name, data, size, timestamp)` | Status code | Sends encoded audio data. |
| `rtspserver_sendvideodata_byphyaddr(name, phy_addr, size, timestamp)` | Status code | Sends encoded video data from a physical address. |
| `rtspserver_sendaudiodata_byphyaddr(name, phy_addr, size, timestamp)` | Status code | Sends encoded audio data from a physical address. |

`data`/`phy_addr`, `size`, and `timestamp` must match the output of the VENC or audio encoder. The native RTSP service is not responsible for PCM or raw image encoding. New video clients usually need to receive the parameter sets and a keyframe before they can start decoding; H.264 requires SPS/PPS, and H.265 requires VPS/SPS/PPS.

The high-level `RtspServer` and the accompanying `rtsp_server.py` example only establish the video capture, encoding, and transmission chain. Although the low-level API supports `rtspserver_sendaudiodata()`, the application must implement audio capture, encoding, and timestamp management itself.

For information about low-level encoding parameters and IDR requests, see the [VENC Module API](k230_canmv_venc_module_api_manual.md).

## `RtspClient`

`multimedia.RtspClient` receives H.264 or H.265 from an RTSP address, decodes it in the firmware, and then passes the frames to the existing `Display`. The class is implemented in the firmware and is imported using `from multimedia import RtspClient`. The client does not open the screen, perform face detection, or scale the image to the model input size. The RGB data required for detection is obtained separately using `get_frame()`, and letterboxing is performed by the AI preprocessing.

The display connection method is the same as for the Sensor: `bind_info()` provides the binding parameters, and the caller calls `Display.bind_layer` itself. The video layer only accepts NV12. Detection boxes are drawn on an ARGB OSD and overlaid on the video using `Display.show_image`.

```{important}
Before pulling the stream, the LAN, Wi-Fi STA, or Wi-Fi AP must be connected first. Using `libs.Network` is recommended. The client is not responsible for networking. Transmission is fixed to interleaved TCP and does not use UDP. Audio is discarded. When authentication is required, include the account in the address, or pass it through `username` and `password`.
```

The path to the display-only example in the development board firmware is `/sdcard/examples/02-Media/rtsp_client_display.py`, and the SDK source path is `src/canmv/resources/examples/02-Media/rtsp_client_display.py`. The example with face detection is located at `/sdcard/examples/21-AI-With-Others/rtsp_client_face_detect.py`, and its SDK source path is `src/canmv/resources/examples/21-AI-With-Others/rtsp_client_face_detect.py`. The class is in the `multimedia` module of the CanMV firmware, so firmware containing this module must be flashed before it can be imported.

### Constructor

```python
from multimedia import RtspClient

client = RtspClient(
    "rtsp://192.168.1.108:8554/test",
    cache_count=60,
    buffer_count=6,
    width=800,
    height=480,
)
```

The constructor connects to the server and completes DESCRIBE, records the stream dimensions, and allocates buffers according to the parameters. At this point, it does not decode or display anything. If the connection fails, or the output dimensions exceed the stream dimensions, `OSError` is raised. There can be at most 4 clients that have not yet called `deinit()` simultaneously; constructing the 5th client also raises `OSError`. This limit corresponds to the number of VDEC channels. A client that is not bound for display still occupies a slot.

When authentication is required, use either of the following forms. After the server returns 401, the request is resent with the account using either Digest or Basic authentication:

```python
client = RtspClient("rtsp://user:password@192.168.1.108:8554/test")
client = RtspClient("rtsp://192.168.1.108:8554/test", username="user", password="password")
```

Characters other than letters, digits, and `-._~` in `username` and `password` are percent-encoded as UTF-8 before being written into the address. Providing `password` without providing `username` raises `ValueError`. Providing `username` when the address already contains `user:password@` also raises `ValueError`.

| Parameter | Description | Default |
| :-- | :-- | :-- |
| `url` | `rtsp://host[:port]/path`, or with an account as `rtsp://user:password@host[:port]/path`. Must start with `rtsp://` | Required |
| `username` | Username. Concatenated into the address together with `password`. Do not provide it when the address already contains an account | Not specified |
| `password` | Password. Used only when `username` is provided. May be an empty string | Not specified |
| `cache_count` | Number of compressed access units cached between the stream reception thread and the decoding thread, ranging from `1` to `120`. The cache is also considered full when the total compressed data exceeds 4 MB. When the queue is full, subsequent frames are discarded until the next keyframe | `60` |
| `buffer_count` | Number of YUV output buffer blocks from the decoder, ranging from `3` to `8` | `6` |
| `width` | Decoded output width. When both `width` and `height` are `0`, the original stream dimensions are used for output | `0` |
| `height` | Decoded output height | `0` |

`width` and `height` must either both be `0` or both be even numbers greater than `0`. Specifying only one, an odd number, or a negative number raises `ValueError`. Values of `cache_count` or `buffer_count` outside their permitted ranges, or a `url` that does not begin with `rtsp://`, also raise `ValueError`.

The specified dimensions are used for downscaling and cannot be used for upscaling. If either dimension is greater than the visible stream dimensions, the constructor raises `OSError`. No scaling is performed when the dimensions match the stream dimensions. These dimensions are the decoder's only output dimensions: both the NV12 data returned by `get_frame()` and the data sent for display use them. Scaling is performed by the VDEC, and the player does not perform CPU-based scaling.

After `stop()`, call `init(url, ...)` with the same parameters to reconnect. Calling `init()` while playback is in progress raises `OSError`. A failure in `init()`, `start()`, or `stop()` raises `OSError`; on success, `0` is returned.

### `video_size()`

```python
width, height = client.video_size()
```

Returns the stream frame dimensions obtained through DESCRIBE, such as `(1920, 1080)`. If they are not yet known, `(0, 0)` is returned. These are the stream dimensions, not the output dimensions specified during construction or the screen window dimensions.

### `bind_info(x=0, y=0, width=None, height=None)`

Returns the parameters for `Display.bind_layer`. The fields are the same as those of `Sensor.bind_info`.

```python
info = client.bind_info(x=0, y=0, width=800, height=480)
Display.bind_layer(**info, layer=Display.LAYER_VIDEO1)
```

| Field | Description |
| :-- | :-- |
| `src` | The player's own display channel `(mod, dev, chn)`, not the VDEC |
| `rect` | `(x, y, width, height)`. `x, y` are the layer position, and `width, height` are the image dimensions sent into the layer |
| `pix_format` | NV12 used by the video layer |

When `width` and `height` are omitted, the decoded output dimensions are used: the output size specified by `init()` if one was provided, or `video_size()` otherwise. The window must be the same size as the decoded output. If the dimensions differ, the frame is not sent for display.

`x` and `y` must be non-negative even numbers. `width` and `height` may be omitted; when provided, they must be positive even numbers. Calling it before `init()`, or before the frame dimensions are known, raises `OSError`.

Call this before `start()`. The order is the same as in the camera display example: first call `bind_layer`, then `Display.init`, and then `start()`. To change the position or size after playback starts, first call `stop()`, then call `Display.disable_layer`, and then call `bind_info` again. `start()` can also be called without calling `bind_info()`, in which case frames are decoded only for `get_frame()`.

### `start()`

```python
ret = client.start()
```

Starts stream reception and decoding. If a display layer has been bound, the frames are also sent to it. Returns `0` on success. Calling it before `init()`, or when the previous `start()` has not yet been followed by `stop()`, raises `OSError`. `start()` can also be called without binding the display. The encoding is determined by the SDP, and both H.264 and H.265 are accepted.

If the session is closed after the constructor returns but before the first PLAY, the reception thread will not reconnect. `start()` first closes this session and then performs DESCRIBE again. If this step fails, `OSError` is raised. A failure during the initial DESCRIBE also does not trigger a reconnect; the constructor directly raises `OSError`.

If the connection is broken after PLAY succeeds, the client retains the decoder and display binding, and the reception thread reconnects. The interval starts at 1 second and doubles each time, up to a maximum of 5 seconds, for a maximum of 3 attempts. After a PLAY succeeds, both the attempt count and the interval are reset. If all 3 attempts fail, reconnection stops, after which `get_frame()` and `check()` raise `OSError`.

### `get_frame(timeout_ms=100)`

Obtains one image for use by the AI. `timeout_ms` is the wait time in milliseconds. It returns an `image`, or `None` on timeout. Calling it before `start()` raises `OSError`. If the connection has closed and reconnection has been abandoned, it raises `OSError("rtsp connection closed")`. The interpreter lock is released while waiting.

The image borrows the decoder's sole RGB buffer, which uses the RGB planar format at the decoded output resolution. The shape returned by `to_numpy_ref()` is `(3, out_h, out_w)`, where `out_w` and `out_h` are the output dimensions specified by `init()`; if no output dimensions were specified, they are the stream dimensions. The next `get_frame()` call that waits for a frame, as well as `stop()` and `deinit()`, releases this buffer. The `image` and any arrays obtained from it become invalid. After using it in a loop, discard it rather than retaining it until the next `get_frame()` call.

```python
frame = client.get_frame(timeout_ms=100)
if frame is not None:
    data = frame.to_numpy_ref()  # (3, out_h, out_w)
    # Read data here
frame = None
```

The client does not perform letterboxing or scale the image to the model input size. RGB conversion is performed only when someone is waiting for `get_frame()`. Display uses `bind_layer`, and this RGB image is not sent to the video layer. If `get_frame()` is not called, the bound display continues to show frames.

### `check()`

Does not retrieve a frame. It returns immediately while reconnection is still in progress. If reconnection has been abandoned, it raises `OSError("rtsp connection closed")`. Programs that only bind the display and do not call `get_frame()` in their loop should call it periodically and exit after a failure.

### `stop()`

```python
ret = client.stop()
```

Stops stream reception and decoding and releases the VDEC. Returns `0` on success. It also returns `0` if the client was not started. If the underlying `stop` returns a nonzero value, `OSError` is raised. It does not close `Display` or unbind the video layer. `start()` can be called again afterward.

### `deinit()`

```python
client.deinit()
```

Releases the client after `stop()` and frees a slot. Repeated calls have no effect. After release, this object cannot call `init()` or `start()` again. To change the address, call `init(url, ...)` after `stop()`; do not call `deinit()` first. It does not call `Display.deinit()`. The client is also released when the object is garbage collected.

### Exit Sequence

First stop the player, then unbind the video layer, then release the client, and finally close the display:

```python
client.stop()
Display.disable_layer(Display.LAYER_VIDEO1)
client.deinit()
Display.deinit()
```

### Usage Example

Display only, without retrieving frames:

```python
import time
from media.display import Display
from multimedia import RtspClient
from libs.Network import connect_network

_, ip = connect_network("lan")

client = None
started = False
display_inited = False
try:
    client = RtspClient(
        "rtsp://192.168.1.108:8554/test",
        cache_count=60,
        buffer_count=6,
        width=800,
        height=480)

    Display.bind_layer(
        **client.bind_info(x=0, y=0, width=800, height=480),
        layer=Display.LAYER_VIDEO1)
    Display.init(Display.ST7701, width=800, height=480, to_ide=False, osd_num=1)
    display_inited = True

    client.start()
    started = True
    while True:
        time.sleep(1)
        client.check()
except OSError as exc:
    print("rtsp failed:", exc)
finally:
    if started:
        client.stop()
    if display_inited:
        Display.disable_layer(Display.LAYER_VIDEO1)
    if client is not None:
        client.deinit()
    if display_inited:
        Display.deinit()
```

When the decoded frames need to be sent to detection, call `get_frame()` in the loop. The returned image dimensions are the `800 x 480` shown above, and the AI then scales them to the model input size. The boxes are drawn on an ARGB image of the same size as the window and displayed using `Display.show_image(..., layer=Display.LAYER_OSD0)`. See `src/canmv/resources/examples/21-AI-With-Others/rtsp_client_face_detect.py` for the complete procedure.

### Multiple Streams

There can be at most 4 `RtspClient` instances simultaneously, aligned with the 4 VDEC channels. Constructing the 5th client raises `OSError`. After one client calls `deinit()`, its slot becomes available and another client can be created. `start()` can be called without calling `bind_info()` and `Display.bind_layer`. In this case, frames are only decoded and obtained using `get_frame()`. The video layer is not occupied, but a client slot is still used.

When displayed, the available video layers are `Display.LAYER_VIDEO1`, `LAYER_VIDEO2`, and `LAYER_VIDEO3`. `LAYER_VIDEO0` cannot be used. Streams without a sufficient number of layers should not be bound and should continue using `get_frame()`. For each window, `x + width` and `y + height` must be within the screen, and the window dimensions must equal the decoded output dimensions of that stream.

Input and output VB memory is allocated separately for each stream. Multiple 1080p streams consume substantial memory. When displaying them, set `width` and `height` to the window dimensions and allow the VDEC to downscale.

```python
left = RtspClient("rtsp://192.168.1.108:8554/cam0", width=400, height=480)
right = RtspClient("rtsp://192.168.1.108:8554/cam1", width=400, height=480)
detect = RtspClient("rtsp://192.168.1.108:8554/cam2", width=320, height=320)
Display.bind_layer(**left.bind_info(x=0, y=0, width=400, height=480), layer=Display.LAYER_VIDEO1)
Display.bind_layer(**right.bind_info(x=400, y=0, width=400, height=480), layer=Display.LAYER_VIDEO2)
Display.init(Display.ST7701, width=800, height=480, to_ide=False, osd_num=1)
left.start()
right.start()
detect.start()
frame = detect.get_frame(timeout_ms=100)
```

Call `stop()` and `deinit()` separately for each object. Call `Display.disable_layer` for each bound layer.

### Limitations

- There can be at most 4 clients simultaneously. Constructing the 5th client raises `OSError`. Another client can be created only after `deinit()` is called. Display binding is optional, but even an unbound client occupies a slot. The video layers are only `LAYER_VIDEO1` through `LAYER_VIDEO3`.
- UDP is not used, and audio is not played.
- Specify the account in the address or pass it through `username` and `password`. If the server returns 401, the request is resent using Digest or Basic authentication.
- The `width` and `height` specified during construction can only downscale or preserve the stream dimensions; they cannot upscale.
- The display window must be the same size as the decoded output; otherwise, the frames are not sent to the video layer.
- `get_frame()` does not scale the image to the detection model's input dimensions.
- A playback interruption triggers automatic reconnection. The interval starts at 1 second and doubles, up to a maximum of 5 seconds, for a maximum of 3 attempts. After a PLAY succeeds, the attempt count and interval are reset. If the attempts still fail, `get_frame()` and `check()` raise `OSError`. A failure during the initial DESCRIBE does not trigger a reconnect, and the constructor directly raises `OSError`. If the connection is broken before PLAY, the subsequent `start()` call reconnects.
