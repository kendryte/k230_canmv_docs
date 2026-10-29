# MJPEG 编码与网页视频流例程讲解

## 概述

MJPEG 网页视频流例程从 Sensor 获取 YUV420SP 视频帧，通过 `MJPEGEncoder` 硬件编码为 JPEG，然后使用 HTTP `multipart/x-mixed-replace` 连续发送。手机或计算机与开发板连接到同一网络后，可以直接通过浏览器查看实时画面。

完整例程位于：

- 开发板固件路径：`/sdcard/examples/02-Media/mjpeg_web_server.py`
- SDK 源码路径：`src/canmv/resources/examples/02-Media/mjpeg_web_server.py`

## 主要配置

运行前需要修改例程开头的网络参数：

```python
NETWORK_TYPE = "wifi_sta"  # "default"、"lan"、"wifi_sta" 或 "wifi_ap"
WLAN_DEVICE = "auto"       # "auto"、"usb"、"sdio" 或 "spi"
WIFI_SSID = "Test"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20

SERVER_PORT = 8080
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080
FRAME_ALIGNMENT = 12
JPEG_QUALITY = 50
STREAM_FPS = 30
USE_VIDEO_FRAME = True
```

| 配置 | 说明 |
|---|---|
| `NETWORK_TYPE` | 选择默认接口、LAN、Wi-Fi STA 或 Wi-Fi AP |
| `WLAN_DEVICE` | 选择自动、USB、SDIO 或 SPI Wi-Fi |
| `NETWORK_TIMEOUT` | 等待网络地址的超时时间，单位秒 |
| `FRAME_WIDTH`、`FRAME_HEIGHT` | Sensor 输出和 JPEG 编码分辨率 |
| `FRAME_ALIGNMENT` | Sensor 图像平面对齐指数；VENC 输入应设置为 `12`，即 4096 字节 |
| `JPEG_QUALITY` | JPEG 质量，范围为 1～99 |
| `STREAM_FPS` | 发送帧率上限；实际帧率还受编码速度和网络带宽限制 |
| `USE_VIDEO_FRAME` | `True` 直接编码 Sensor 视频帧；全高清连续视频流应保持为 `True` |

脚本通过 `libs.Network.connect_network()` 选择动态注册的网卡、等待有效 IP 并
设置默认上行，不需要写死 netdev 名称。

## 编码流程

Sensor 输出需要采用 YUV420SP，并保证每个平面的物理地址按 4096 字节对齐：

```python
sensor = Sensor()
sensor.reset()
sensor.set_framesize(
    width=FRAME_WIDTH,
    height=FRAME_HEIGHT,
    alignment=FRAME_ALIGNMENT,
)
sensor.set_pixformat(Sensor.YUV420SP)
sensor.run()

encoder = MJPEGEncoder(quality=JPEG_QUALITY)
```

连续编码时直接获取 `py_video_frame_info`：

```python
def capture_jpeg(sensor, encoder):
    frame = sensor.snapshot(dump_frame=True)
    jpeg = encoder.encode(frame, timeout_ms=1000)
    del frame
    return jpeg
```

这种方式将 Sensor 的 VB 帧直接提交给 VENC，避免将 1920×1080 图像复制到中间缓冲区。若需要演示 `image.Image` 输入，可在较低分辨率下将 `USE_VIDEO_FRAME` 改为 `False`。

## HTTP 接口

例程启动后会在串口输出访问地址：

```text
Open http://192.168.2.60:8080/ in a browser
```

| 路径 | 内容 |
|---|---|
| `/` | 实时视频页面 |
| `/stream` | `multipart/x-mixed-replace` MJPEG 数据流 |
| `/snapshot.jpg` | 当前单帧 JPEG 图像 |

网页中的 JavaScript 会在视频流连接出错后等待 1 秒并重新连接 `/stream`，不需要手动刷新页面。

## 大帧网络发送

RT-Smart 的阻塞 socket 发送超时会限制为 500 ms。1080P JPEG 较大，直接调用一次 `sendall()` 可能在 TCP 发送缓冲区产生回压后超时，表现为浏览器只显示一帧便断开。

例程保持客户端 socket 为非阻塞模式，将 JPEG 按 16 KiB 分块发送；遇到 `EAGAIN` 或暂时超时时继续重试。只要发送仍有进展，连接就会保持。连续 5 秒没有发送进展时才关闭该客户端连接。

## 运行步骤

1. 修改 `NETWORK_TYPE`、`WLAN_DEVICE` 和 Wi-Fi 凭据；使用有线网络时将
   `NETWORK_TYPE` 设为 `"lan"`。
1. 运行 `/sdcard/examples/02-Media/mjpeg_web_server.py`。
1. 等待串口输出 `First JPEG size` 和浏览器访问地址。
1. 在同一局域网内的手机或计算机上打开该地址。

## 使用限制

- 该例程采用同步单客户端设计。一个浏览器正在访问 `/stream` 时，服务器不会同时处理另一个客户端请求。
- `STREAM_FPS=30` 是目标上限，并不保证 WLAN 能持续传输 1080P 30 FPS。出现明显延迟时应降低 `JPEG_QUALITY`、`STREAM_FPS` 或分辨率。
- 浏览器消费数据的速度低于生成速度时，TCP 回压会自然降低实际帧率，不会无限缓存 JPEG 帧。
- 退出脚本时会依次关闭 socket、编码器和 Sensor，避免遗留 VENC 通道或 VB 缓冲池。

接口的完整说明请参考 [`MJPEGEncoder` API 手册](../../api/mpp/media_mjpeg.md)。
