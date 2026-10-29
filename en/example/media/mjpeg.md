# MJPEG Encoding and Web Video Stream Example Explanation

## Overview

The MJPEG web video stream example obtains YUV420SP video frames from the Sensor, encodes them into JPEG via the `MJPEGEncoder` hardware, and continuously transmits them using HTTP `multipart/x-mixed-replace`. Once a phone or computer is connected to the same network as the development board, the live image can be viewed directly through a browser.

The complete example is located at:

- Development board firmware path: `/sdcard/examples/02-Media/mjpeg_web_server.py`
- SDK source path: `src/canmv/resources/examples/02-Media/mjpeg_web_server.py`

## Main Configuration

Before running, you need to modify the network parameters at the beginning of the example:

```python
NETWORK_TYPE = "wifi_sta"  # "default", "lan", "wifi_sta" or "wifi_ap"
WLAN_DEVICE = "auto"       # "auto", "usb", "sdio" or "spi"
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

| Configuration | Description |
|---|---|
| `NETWORK_TYPE` | Select default interface, LAN, Wi-Fi STA, or Wi-Fi AP |
| `WLAN_DEVICE` | Select auto, USB, SDIO, or SPI Wi-Fi |
| `NETWORK_TIMEOUT` | Timeout for waiting for a network address, in seconds |
| `FRAME_WIDTH`, `FRAME_HEIGHT` | Sensor output and JPEG encoding resolution |
| `FRAME_ALIGNMENT` | Sensor image plane alignment exponent; VENC input should be set to `12`, i.e., 4096 bytes |
| `JPEG_QUALITY` | JPEG quality, ranging from 1 to 99 |
| `STREAM_FPS` | Upper limit of sending frame rate; the actual frame rate is also limited by encoding speed and network bandwidth |
| `USE_VIDEO_FRAME` | `True` encodes the Sensor video frame directly; keep `True` for full-HD continuous video streams |

The script uses `libs.Network.connect_network()` to select the dynamically registered network interface, wait for a valid IP, and set the default uplink, without hardcoding the netdev name.

## Encoding Process

The Sensor output must use YUV420SP, and ensure that the physical address of each plane is aligned to 4096 bytes:

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

For continuous encoding, obtain `py_video_frame_info` directly:

```python
def capture_jpeg(sensor, encoder):
    frame = sensor.snapshot(dump_frame=True)
    jpeg = encoder.encode(frame, timeout_ms=1000)
    del frame
    return jpeg
```

This method submits the Sensor's VB frame directly to VENC, avoiding copying a 1920×1080 image to an intermediate buffer. If you need to demonstrate `image.Image` input, you can set `USE_VIDEO_FRAME` to `False` at a lower resolution.

## HTTP Interface

After the example starts, the access address will be printed on the serial port:

```text
Open http://192.168.2.60:8080/ in a browser
```

| Path | Content |
|---|---|
| `/` | Live video page |
| `/stream` | `multipart/x-mixed-replace` MJPEG data stream |
| `/snapshot.jpg` | Current single-frame JPEG image |

The JavaScript in the web page waits 1 second and reconnects to `/stream` after a video stream connection error, so there is no need to manually refresh the page.

## Large Frame Network Transmission

RT-Smart's blocking socket send timeout is limited to 500 ms. 1080P JPEG is relatively large, so calling `sendall()` once directly may timeout after TCP send buffer backpressure occurs, causing the browser to display only one frame before disconnecting.

The example keeps the client socket in non-blocking mode, sending JPEG in 16 KiB chunks; it continues to retry when encountering `EAGAIN` or temporary timeout. As long as sending still progresses, the connection is maintained. The client connection is closed only when there is no sending progress for 5 consecutive seconds.

## Running Steps

1. Modify `NETWORK_TYPE`, `WLAN_DEVICE`, and Wi-Fi credentials; set `NETWORK_TYPE` to `"lan"` when using wired network.
1. Run `/sdcard/examples/02-Media/mjpeg_web_server.py`.
1. Wait for the serial port to output `First JPEG size` and the browser access address.
1. Open that address on a phone or computer within the same LAN.

## Usage Limitations

- This example uses a synchronous single-client design. When one browser is accessing `/stream`, the server will not process another client's request simultaneously.
- `STREAM_FPS=30` is the target upper limit and does not guarantee that WLAN can continuously transmit 1080P 30 FPS. When noticeable lag occurs, reduce `JPEG_QUALITY`, `STREAM_FPS`, or resolution.
- When the browser consumes data at a rate lower than the generation rate, TCP backpressure will naturally reduce the actual frame rate, without caching JPEG frames indefinitely.
- When exiting the script, the socket, encoder, and Sensor will be closed in order, avoiding leftover VENC channels or VB buffer pools.

For the complete interface description, please refer to the [`MJPEGEncoder` API manual](../../api/mpp/media_mjpeg.md).
