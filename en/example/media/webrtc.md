# WebRTC Camera Example

## Introduction

`webrtc_camera.py` feeds Sensor output into VENC, then pushes it to a browser via `webrtc.PeerConnection`. The example includes a lightweight HTTP signaling service and web page; when the development board and browser are on the same network, open the address in the browser and click **Connect** to view the video.

The default configuration is H.265, `1280 x 720`, `512 Kbit/s`, no audio. This configuration prioritizes controlling encoding, memory, and Wi-Fi load; H.264 can be used for compatibility-priority browsers.

## File Location

- Development board firmware path: `/sdcard/examples/02-Media/webrtc_camera.py`
- SDK source code path: `src/canmv/resources/examples/02-Media/webrtc_camera.py`

The firmware requires `CONFIG_ENABLE_MODULE_WEBRTC` to be enabled. This option is enabled by default and automatically depends on libpeer.

## Configuration Items

Modify the following constants at the beginning of the script:

| Configuration Item | Description | Default Value |
| :-- | :-- | :-- |
| `NETWORK_TYPE` | `"default"`, `"lan"`, `"wifi_sta"` or `"wifi_ap"` | `"lan"` |
| `WLAN_DEVICE` | `"auto"`, `"usb"`, `"sdio"` or `"spi"` | `"auto"` |
| `WIFI_SSID` / `WIFI_PASSWORD` | Credentials used by Wi-Fi STA/AP | Example value |
| `NETWORK_TIMEOUT` | Timeout for waiting for a network address, in seconds | `15` |
| `HTTP_PORT` | Web page and HTTP signaling port | `8080` |
| `WIDTH` / `HEIGHT` | Video encoding resolution | `1280` / `720` |
| `VIDEO_CODEC` | `"h265"` or `"h264"` | `"h265"` |
| `BIT_RATE` | VENC target bit rate, in Kbit/s | `512` |
| `AUDIO_CODEC` | WebRTC audio encoding type | `webrtc.CODEC_NONE` |

The example uses `libs.Network.connect_network()` to select the interface, wait for an IP, and set the default uplink, without hardcoding dynamic network device names. When multiple Wi-Fi interfaces exist simultaneously, `WLAN_DEVICE` can be used to fix the transport type; usually keep it as `"auto"`.

## How to Run

1. Modify `NETWORK_TYPE`, `WLAN_DEVICE`, and Wi-Fi credentials according to the network environment.
1. Run the script in CanMV IDE, or place the script on the development board and run it.
1. The serial port will output information similar to:

```text
WebRTC camera: http://192.168.1.108:8080 (H265, 512 Kbit/s, audio disabled)
```

1. Open this address in a browser on the same interconnectable network and click **Connect**.

The web page displays SDP negotiation, browser candidate collection, ICE/DTLS connection, and first frame waiting status in sequence. When the video actually starts playing, the overlay prompt will disappear; the page will not falsely report that it has started playing just because a video track has been received.

## Encoding and First Frame Behavior

The script continuously caches the `STREAM_TYPE_HEADER` parameter set output by VENC. When each I frame arrives, it first sends the cached H.264 SPS/PPS or H.265 VPS/SPS/PPS, then sends the I frame.

When WebRTC enters the `COMPLETED` state, the script calls `Encoder.RequestIDR()` to request an immediate key frame. Therefore, after the connection is complete, there is no need to wait for a complete GOP cycle before having the opportunity to decode the first frame. The VENC fetch timeout is 100 ms, allowing the main loop to promptly detect connection state changes.

## Performance and Compatibility Recommendations

- `512 Kbit/s` is the low-load default. When image detail is insufficient, try `768` or `1024` Kbit/s first, and observe CPU, encoding, and network stability.
- When the network is weak, prioritize reducing `WIDTH`/`HEIGHT`, for example using `800 x 480`; only reducing the bit rate may cause excessive compression artifacts.
- H.265 has higher bandwidth efficiency, but some browsers or systems do not have H.265 WebRTC decoding support. When there is no picture, change to:

```python
VIDEO_CODEC = "h264"
```

- Audio is disabled by default. Enabling audio also requires creating your own audio capture/encoding chain and calling `peer.send_audio()`; only modifying `AUDIO_CODEC` will not automatically generate audio.

## Frequently Asked Questions

| Symptom | Cause and Handling |
| :-- | :-- |
| `RuntimeError: libpeer initialization failed` | Firmware has not enabled WebRTC/libpeer, or there is an unclosed WebRTC object. Update the firmware and ensure the previous script has exited. |
| `network address timeout` | The selected interface did not connect and obtain an IP within `NETWORK_TIMEOUT`. Check `NETWORK_TYPE`, Wi-Fi credentials, network cable, and DHCP service. |
| Page stays on Connecting for a long time | Confirm that the browser and development board can communicate with each other, disable AP client isolation, and check whether UDP is blocked by a firewall. |
| Connected but no picture | Retry with H.264; also confirm that the browser supports H.265, and that the page has received a new key frame. |
| Web page still shows old status | The browser may have cached the old embedded web page. Reload or force refresh the page; the script has already sent the `Cache-Control: no-store` response header. |
| HTTP output `ECONNRESET` | It is normal for the browser to close the short connection after the request is completed; the example ignores common `ECONNRESET`/`EPIPE`. |

## Security Scope

This example is only intended for trusted LAN development and verification. HTTP signaling has no access control and does not enable TLS; it should not be exposed directly to the public network. Public network deployment requires at least adding authentication, HTTPS/WSS signaling, and STUN/TURN services.

For related APIs, please refer to the [`webrtc` module API](../../api/mpp/k230_canmv_webrtc_module_api_manual.md) and [VENC module API](../../api/mpp/k230_canmv_venc_module_api_manual.md).
