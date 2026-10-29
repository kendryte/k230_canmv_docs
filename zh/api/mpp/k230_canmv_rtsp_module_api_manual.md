# `RTSP` 模块 API 手册

## 概述

`media.rtspserver.RtspServer` 提供 `Sensor -> VENC -> RTSP` 的高层封装。当前默认配置为 H.265、`1280 x 720`、`512 Kbit/s`，音频关闭，以降低编码和网络资源占用。底层 `multimedia.rtsp_server` 对象也可用于由应用自行管理编码器和媒体发送。拉流解码使用固件类型 `multimedia.RtspClient`。显示仍由 `Display.bind_layer` 完成，见文末。

示例脚本在开发板固件中的路径为 `/sdcard/examples/02-Media/rtsp_server.py`，
SDK 源码路径为 `src/canmv/resources/examples/02-Media/rtsp_server.py`。它包含与
高层封装相同的摄像头推流模式，并增加了 LAN/Wi-Fi 配置、错误检查和可配置参数。

```{important}
RTSP 服务本身不负责联网。调用 `start()` 前，应用必须先连接 LAN、Wi-Fi STA 或 Wi-Fi AP。推荐使用 `libs.Network` 完成接口选择并设置默认上行。
```

## `RtspServer`

### 构造函数

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

| 参数 | 含义 | 默认值 |
| :-- | :-- | :-- |
| `session_name` | RTSP 会话名称，也是 URL 路径 | `"test"` |
| `port` | RTSP 监听端口 | `8554` |
| `video_type` | `mm.multi_media_type.media_h265` 或 `media_h264` | `media_h265` |
| `enable_audio` | 在 RTSP Session 中声明音频 | `False` |
| `width` | 编码宽度；内部自动向上按 16 对齐 | `1280` |
| `height` | 编码高度 | `720` |
| `bit_rate` | VENC CBR 目标码率，单位 Kbit/s，范围 `100` 到 `20000` | `512` |
| `gop_len` | GOP 帧数 | `30` |

当 `video_type` 不是 H.264/H.265，或 `bit_rate` 超出范围时，构造函数抛出 `ValueError`。

### `start()`

```python
server.start()
```

初始化 RTSP 服务和 Session，创建 Sensor/VENC 管道，启动编码并在后台线程中发送视频。需要直接检查端口绑定和 Session 创建的返回状态时，请使用下方的 `multimedia.rtsp_server` API，或使用随附示例的 `RtspServer` 类。

### `stop()`

```python
server.stop()
```

停止后台推流线程，停止 VENC 和 Sensor，销毁媒体链路并关闭 RTSP 服务。应用退出前应调用该方法释放硬件资源。

### `get_rtsp_url()`

```python
url = server.get_rtsp_url()
```

返回当前会话的 RTSP URL。例如，网络地址为 `192.168.1.108` 时，默认 URL 是：

```text
rtsp://192.168.1.108:8554/test
```

## 使用示例

以下示例使用低码率 H.265；如果客户端不支持 H.265，可切换为 H.264。

```python
import multimedia as mm
from libs.Network import connect_network
from media.rtspserver import RtspServer

# 仅展示 LAN 配置；Wi-Fi 连接方式见 /sdcard/examples/02-Media/rtsp_server.py。
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
    # 保持脚本运行，客户端即可连接。
finally:
    if started:
        server.stop()
```

## 音频和兼容性

默认 `enable_audio=False`。随附的 `RtspServer` 封装和示例只建立视频采集、编码和发送链路；仅把 `enable_audio` 设为 `True` 不会自动采集或发送音频。

H.265 在低码率下通常效率更高，但部分 RTSP 客户端的兼容性较弱。优先兼容 VLC、旧 NVR 或浏览器插件时，可使用：

```python
video_type=mm.multi_media_type.media_h264
```

## 性能建议

- `512 Kbit/s` 适合默认的预览和资源受限场景。更高画质应逐步增大 `bit_rate`，同时观察编码和 Wi-Fi 负载。
- 降低分辨率通常比只降低码率更有效；例如网络较弱时可选择 `640 x 360` 或 `800 x 480`。
- 较短的 `gop_len` 可以缩短新客户端等待关键帧的时间，但会增加关键帧开销。实时低码率场景通常保持 `30`；自行搭建 VENC 推流链路时，可结合 `Encoder.RequestIDR()` 缩短首帧等待。

## 底层 `multimedia.rtsp_server` API

需要自行管理摄像头、VENC 或音频时，可直接使用原生 RTSP 对象：

```python
import multimedia as mm

server = mm.rtsp_server()
```

构造函数已经创建对象；通常不需要再调用 `rtspserver_create()`。所有带 `session_name` 的方法都使用创建 Session 时指定的名称。

### 生命周期

| 方法 | 返回值 | 说明 |
| :-- | :-- | :-- |
| `rtspserver_init(port)` | 状态码 | 初始化并监听 RTSP 端口。`0` 表示成功。 |
| `rtspserver_createsession(name, video_type, enable_audio)` | 状态码 | 创建 RTSP Session；`video_type` 使用 `mm.multi_media_type.media_h264`、`media_h265` 或底层支持的类型。 |
| `rtspserver_getrtspurl(name)` | `str` | 返回 Session 的 RTSP URL；Session 不存在时抛出 `RuntimeError`。 |
| `rtspserver_start()` | 无 | 开始 RTSP 服务。 |
| `rtspserver_stop()` | 无 | 停止 RTSP 服务。 |
| `rtspserver_destroysession(name)` | 状态码 | 销毁指定 Session。 |
| `rtspserver_deinit()` | 无 | 反初始化服务。 |
| `rtspserver_destroy()` | 无 | 释放对象；重复调用安全。 |

典型的手动流程如下：

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
    # 从 VENC 取得已编码数据后调用 rtspserver_sendvideodata()。
finally:
    server.rtspserver_stop()
    server.rtspserver_deinit()
    server.rtspserver_destroy()
```

### 媒体发送

| 方法 | 返回值 | 说明 |
| :-- | :-- | :-- |
| `rtspserver_sendvideodata(name, data, size, timestamp)` | 状态码 | 发送内存中的已编码视频数据。 |
| `rtspserver_sendaudiodata(name, data, size, timestamp)` | 状态码 | 发送已编码音频数据。 |
| `rtspserver_sendvideodata_byphyaddr(name, phy_addr, size, timestamp)` | 状态码 | 从物理地址发送已编码视频数据。 |
| `rtspserver_sendaudiodata_byphyaddr(name, phy_addr, size, timestamp)` | 状态码 | 从物理地址发送已编码音频数据。 |

`data`/`phy_addr`、`size` 和 `timestamp` 必须与 VENC 或音频编码器输出匹配。原生 RTSP 服务不负责 PCM 或原始图像编码。视频新客户端通常需要收到参数集和关键帧才能开始解码；H.264 需要 SPS/PPS，H.265 需要 VPS/SPS/PPS。

高层 `RtspServer` 和随附 `rtsp_server.py` 示例仅建立视频采集、编码和发送链路。底层 API 虽支持 `rtspserver_sendaudiodata()`，但应用必须自行实现音频采集、编码和时间戳管理。

有关底层编码参数和 IDR 请求，请参阅 [VENC 模块 API](k230_canmv_venc_module_api_manual.md)。

## `RtspClient`

`multimedia.RtspClient` 从 RTSP 地址接收 H.264 或 H.265，在固件里解码，再把画面交给现有的 `Display`。类实现在固件里，用 `from multimedia import RtspClient` 调用。客户端不打开屏幕，也不做人脸检测或缩放成模型输入。检测需要的 RGB 用 `get_frame()` 另取，letterbox 由 AI 预处理完成。

显示接法和 Sensor 相同：`bind_info()` 给出绑定参数，调用方自己 `Display.bind_layer`。视频层只接受 NV12。检测框画在一块 ARGB 的 OSD 上，用 `Display.show_image` 叠到视频上面。

```{important}
拉流前必须先连上 LAN、Wi-Fi STA 或 Wi-Fi AP。推荐使用 `libs.Network`。客户端不负责联网。传输固定为 TCP 交织，不使用 UDP。音频会被丢掉。需要认证时，把账号写进地址，或传给 `username` 和 `password`。
```

只显示的示例在开发板固件中的路径为 `/sdcard/examples/02-Media/rtsp_client_display.py`，SDK 源码路径为 `src/canmv/resources/examples/02-Media/rtsp_client_display.py`。带人脸检测的示例为 `/sdcard/examples/21-AI-With-Others/rtsp_client_face_detect.py`，SDK 源码路径为 `src/canmv/resources/examples/21-AI-With-Others/rtsp_client_face_detect.py`。类在 CanMV 固件的 `multimedia` 模块里，需要烧录包含该模块的固件后才能 `import`。

### 构造函数

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

构造时连接服务器并完成 DESCRIBE，记下码流宽高，按参数分配缓存。此时还不解码、不出画面。连接失败，或输出尺寸大于码流时，抛出 `OSError`。同时最多 4 个还没有 `deinit()` 的客户端，第 5 个构造也抛出 `OSError`。这个上限和 VDEC 通道数一致。不绑定显示同样占一个名额。

需要认证时用下面任一写法。服务器返回 401 后，按 Digest 或 Basic 带上账号重发：

```python
client = RtspClient("rtsp://user:password@192.168.1.108:8554/test")
client = RtspClient("rtsp://192.168.1.108:8554/test", username="user", password="password")
```

`username` 和 `password` 里除字母、数字和 `-._~` 以外的字符会按 UTF-8 做百分号编码后再写入地址。只给 `password`、不给 `username` 时抛出 `ValueError`。地址里已经有 `user:password@` 时再传 `username` 也抛出 `ValueError`。

| 参数 | 含义 | 默认值 |
| :-- | :-- | :-- |
| `url` | `rtsp://host[:port]/path`，或以 `rtsp://user:password@host[:port]/path` 带上账号。必须以 `rtsp://` 开头 | 必填 |
| `username` | 用户名。与 `password` 一起拼进地址。地址里已有账号时不要再传 | 不填 |
| `password` | 密码。只在给出 `username` 时使用。可以是空字符串 | 不填 |
| `cache_count` | 收流线程和解码线程之间缓存的压缩访问单元个数，范围 `1` 到 `120`。压缩数据总量超过 4 MB 时也视为已满。队列满时丢掉后续帧，直到下一个关键帧 | `60` |
| `buffer_count` | 解码输出的 YUV 缓冲块数，范围 `3` 到 `8` | `6` |
| `width` | 解码输出宽度。与 `height` 同时为 `0` 时按码流原尺寸输出 | `0` |
| `height` | 解码输出高度 | `0` |

`width` 和 `height` 必须同时为 `0`，或同时为大于 0 的偶数。只写一个、奇数或负数会抛出 `ValueError`。`cache_count`、`buffer_count` 超出范围，或 `url` 不是 `rtsp://`，同样抛出 `ValueError`。

指定的宽高是缩小，不能放大。任一方向大于码流可见尺寸时构造函数抛出 `OSError`。与码流尺寸相同时不做缩放。这个尺寸是解码器的唯一输出：`get_frame()` 和送给显示的 NV12 都是它。缩放由 VDEC 完成，播放器不做 CPU 缩放。

`stop()` 之后用同样的参数再调用 `init(url, ...)` 重新连接。正在播放时调用 `init()` 抛出 `OSError`。`init()`、`start()`、`stop()` 失败时抛出 `OSError`，成功时返回 `0`。

### `video_size()`

```python
width, height = client.video_size()
```

返回 DESCRIBE 得到的码流画面大小，例如 `(1920, 1080)`。还不知道时返回 `(0, 0)`。这是码流尺寸，不是构造时指定的输出尺寸，也不是屏幕窗口大小。

### `bind_info(x=0, y=0, width=None, height=None)`

返回给 `Display.bind_layer` 的参数，字段和 `Sensor.bind_info` 相同。

```python
info = client.bind_info(x=0, y=0, width=800, height=480)
Display.bind_layer(**info, layer=Display.LAYER_VIDEO1)
```

| 字段 | 含义 |
| :-- | :-- |
| `src` | 播放器自己的显示通道 `(mod, dev, chn)`，不是 VDEC |
| `rect` | `(x, y, width, height)`。`x, y` 是图层位置，`width, height` 是送进图层的图像大小 |
| `pix_format` | 视频层使用的 NV12 |

`width`、`height` 省略时使用解码输出尺寸：`init()` 指定了输出大小就用那个，否则用 `video_size()`。窗口必须和解码输出一样大。尺寸不同时这一帧不会送去显示。

`x`、`y` 必须是非负偶数。`width`、`height` 可以省略；给出时必须是正偶数。未 `init()`，或还不知道画面大小时抛出 `OSError`。

在 `start()` 之前调用。顺序和摄像头显示示例一样：先 `bind_layer`，再 `Display.init`，再 `start()`。播放开始后要改位置或大小，先 `stop()`，再 `Display.disable_layer`，然后重新 `bind_info`。不调用 `bind_info()` 也可以 `start()`，此时只为 `get_frame()` 解码。

### `start()`

```python
ret = client.start()
```

开始收流、解码。已经绑定显示层时，同时把画面送进去。成功返回 `0`。未 `init()`，或上一次 `start()` 还没有 `stop()` 时，抛出 `OSError`。不绑定显示也可以 `start()`。编码由 SDP 决定，接受 H.264 和 H.265。

构造函数返回之后、第一次 `PLAY` 之前如果会话被关掉，接收线程不会重连。`start()` 会先关掉这条会话，再重新 DESCRIBE。这一步失败时抛出 `OSError`。初次 DESCRIBE 失败也不会重连，构造函数直接抛出 `OSError`。

`PLAY` 成功之后连接被拆掉，客户端保留解码器和显示绑定，由接收线程重连。间隔从 1 秒起每次加倍，最长 5 秒，最多 3 次。一次 `PLAY` 成功后，次数和间隔都恢复。3 次都失败则停止重连，之后 `get_frame()` 和 `check()` 抛出 `OSError`。

### `get_frame(timeout_ms=100)`

取一张给 AI 使用的图。`timeout_ms` 是等待毫秒数。返回 `image`，超时返回 `None`。未 `start()` 抛出 `OSError`。连接已关闭且重连已放弃时抛出 `OSError("rtsp connection closed")`。等待期间放开解释器锁。

图像借用解码器唯一的一块 RGB 缓冲，格式是解码输出分辨率的 RGB 平面。`to_numpy_ref()` 的形状为 `(3, out_h, out_w)`，`out_w` 和 `out_h` 是 `init()` 的输出尺寸；未指定输出尺寸时就是码流尺寸。下一次会等待的 `get_frame()`，以及 `stop()`、`deinit()`，都会释放这块缓冲。`image` 和由它得到的数组一起失效。在循环里用完就丢掉，不要留到下一次 `get_frame()`。

```python
frame = client.get_frame(timeout_ms=100)
if frame is not None:
    data = frame.to_numpy_ref()  # (3, out_h, out_w)
    # 在这里读 data
frame = None
```

客户端不做 letterbox，也不缩到模型输入。只有有人等待 `get_frame()` 时才做 RGB 转换。显示走 `bind_layer`，不把这张 RGB 送进视频层。不调用 `get_frame()` 时，已绑定的显示仍然出画面。

### `check()`

不取帧。重连还在进行时直接返回。重连已放弃时抛出 `OSError("rtsp connection closed")`。只绑定显示、循环里不调用 `get_frame()` 的程序，应周期性调用它，失败后退出。

### `stop()`

```python
ret = client.stop()
```

停止收流和解码，释放 VDEC。成功返回 `0`。未启动也返回 `0`。底层 `stop` 返回非 0 时抛出 `OSError`。不关闭 `Display`，也不解除视频层绑定。之后可以再 `start()`。

### `deinit()`

```python
client.deinit()
```

在 `stop()` 之后释放客户端，并空出一个名额。重复调用没有效果。释放后这个对象不能再 `init()` 或 `start()`。要换地址，在 `stop()` 之后调用 `init(url, ...)`，不要先 `deinit()`。不调用 `Display.deinit()`。对象被回收时也会释放。

### 退出顺序

先停播放器，再解除视频层绑定，然后释放客户端，最后关闭显示：

```python
client.stop()
Display.disable_layer(Display.LAYER_VIDEO1)
client.deinit()
Display.deinit()
```

### 使用示例

只显示、不取帧：

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

需要把解码画面送给检测时，在循环里调用 `get_frame()`。返回图的宽高就是上面的 `800 x 480`，再由 AI 自己缩到模型输入。框画到与窗口同样大小的 ARGB 图像上，用 `Display.show_image(..., layer=Display.LAYER_OSD0)` 显示。完整流程见 `src/canmv/resources/examples/21-AI-With-Others/rtsp_client_face_detect.py`。

### 多路

同时最多 4 个 `RtspClient`，和第 4 个 VDEC 通道对齐。第 5 个构造函数抛出 `OSError`。某个客户端 `deinit()` 之后，名额空出来，可以再创建一个。不调用 `bind_info()` 和 `Display.bind_layer` 也可以 `start()`，这时只解码，用 `get_frame()` 取图，不占用视频层，但仍然占一个客户端名额。

要上屏时，可用的视频层是 `Display.LAYER_VIDEO1`、`LAYER_VIDEO2`、`LAYER_VIDEO3`。`LAYER_VIDEO0` 不能用。层不够的那几路不要绑定，继续 `get_frame()`。每个窗口的 `x + width`、`y + height` 必须落在屏幕内，窗口宽高必须等于该路的解码输出。

每路单独分配输入和输出 VB。多路 1080p 占用很大，显示时把 `width`、`height` 设成窗口大小，由 VDEC 缩小。

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

`stop()`、`deinit()` 按对象分别调用。绑定过的层再 `Display.disable_layer`。

### 限制

- 同时最多 4 个客户端。第 5 个构造函数抛出 `OSError`。`deinit()` 之后才能再创建。显示绑定是可选的，不绑定也占一个名额。视频层只有 `LAYER_VIDEO1` 到 `LAYER_VIDEO3`。
- 不使用 UDP，也不播放音频。
- 账号写在地址里，或通过 `username`、`password` 传入。服务器返回 401 时按 Digest 或 Basic 重发。
- 构造时的 `width`、`height` 只能缩小或保持码流尺寸，不能放大。
- 显示窗口必须和解码输出一样大，否则画面不会送到视频层。
- `get_frame()` 不会把图缩成检测模型的输入尺寸。
- 播放中断开会自动重连，间隔从 1 秒起加倍，最长 5 秒，最多 3 次。一次 `PLAY` 成功后次数和间隔恢复。仍失败时 `get_frame()` 和 `check()` 抛出 `OSError`。初次 DESCRIBE 失败不重连，构造函数直接抛出 `OSError`。`PLAY` 之前断开时，由接下来的 `start()` 重新连接。
