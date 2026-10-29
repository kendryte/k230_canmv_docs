# WebRTC Camera 示例

## 简介

`webrtc_camera.py` 将 Sensor 输出送入 VENC，再经 `webrtc.PeerConnection` 推送到
浏览器。示例内置一个轻量 HTTP 信令服务和网页；开发板与浏览器在同一网络中时，
浏览器打开地址并点击 **Connect** 即可查看视频。

默认配置为 H.265、`1280 x 720`、`512 Kbit/s`、无音频。该配置优先控制编码、内存和 Wi-Fi 负载；H.264 可用于兼容性优先的浏览器。

## 文件位置

- 开发板固件路径：`/sdcard/examples/02-Media/webrtc_camera.py`
- SDK 源码路径：`src/canmv/resources/examples/02-Media/webrtc_camera.py`

固件需要启用 `CONFIG_ENABLE_MODULE_WEBRTC`。该选项默认启用，并自动依赖 libpeer。

## 配置项

在脚本开头修改以下常量：

| 配置项 | 说明 | 默认值 |
| :-- | :-- | :-- |
| `NETWORK_TYPE` | `"default"`、`"lan"`、`"wifi_sta"` 或 `"wifi_ap"` | `"lan"` |
| `WLAN_DEVICE` | `"auto"`、`"usb"`、`"sdio"` 或 `"spi"` | `"auto"` |
| `WIFI_SSID` / `WIFI_PASSWORD` | Wi-Fi STA/AP 使用的凭据 | 示例值 |
| `NETWORK_TIMEOUT` | 等待网络地址的超时时间，单位秒 | `15` |
| `HTTP_PORT` | 网页和 HTTP 信令端口 | `8080` |
| `WIDTH` / `HEIGHT` | 视频编码分辨率 | `1280` / `720` |
| `VIDEO_CODEC` | `"h265"` 或 `"h264"` | `"h265"` |
| `BIT_RATE` | VENC 目标码率，单位 Kbit/s | `512` |
| `AUDIO_CODEC` | WebRTC 音频编码类型 | `webrtc.CODEC_NONE` |

示例通过 `libs.Network.connect_network()` 选择接口、等待 IP 并设置默认上行，
不会写死动态网络设备名。多块 Wi-Fi 同时存在时，可通过 `WLAN_DEVICE` 固定传输
类型；通常保留 `"auto"` 即可。

## 运行方法

1. 根据网络环境修改 `NETWORK_TYPE`、`WLAN_DEVICE` 和 Wi-Fi 凭据。
1. 在 CanMV IDE 中运行脚本，或将脚本放到开发板后运行。
1. 串口会输出类似信息：

```text
WebRTC camera: http://192.168.1.108:8080 (H265, 512 Kbit/s, audio disabled)
```

1. 在同一可互通网络的浏览器打开该地址，点击 **Connect**。

网页依次显示 SDP 协商、浏览器候选收集、ICE/DTLS 连接和首帧等待状态。视频实际开始播放时，覆盖提示才会消失；页面不会把仅收到视频轨道误报为已经播放。

## 编码和首帧行为

脚本持续缓存 VENC 输出的 `STREAM_TYPE_HEADER` 参数集。在每个 I 帧到来时，先发送缓存的 H.264 SPS/PPS 或 H.265 VPS/SPS/PPS，再发送 I 帧。

当 WebRTC 进入 `COMPLETED` 状态，脚本调用 `Encoder.RequestIDR()` 请求即时关键帧。因此连接完成后无需等待完整 GOP 周期才有机会解码首帧。VENC 获取超时为 100 ms，使主循环能及时发现连接状态变化。

## 性能和兼容性建议

- `512 Kbit/s` 是低负载默认值。画面细节不足时，先尝试 `768` 或 `1024` Kbit/s，并观察 CPU、编码和网络稳定性。
- 网络较弱时，优先降低 `WIDTH`/`HEIGHT`，例如使用 `800 x 480`；仅降低码率可能会造成过多压缩伪影。
- H.265 的带宽效率更高，但某些浏览器或系统没有 H.265 WebRTC 解码支持。没有画面时改为：

```python
VIDEO_CODEC = "h264"
```

- 音频默认关闭。启用音频还需要自行创建音频采集/编码链路并调用 `peer.send_audio()`；只修改 `AUDIO_CODEC` 不会自动产生音频。

## 常见问题

| 现象 | 原因和处理 |
| :-- | :-- |
| `RuntimeError: libpeer initialization failed` | 固件未启用 WebRTC/libpeer，或已有未关闭的 WebRTC 对象。更新固件并确保上一个脚本已退出。 |
| `network address timeout` | 所选接口未在 `NETWORK_TIMEOUT` 内连接并取得 IP。检查 `NETWORK_TYPE`、Wi-Fi 凭据、网线和 DHCP 服务。 |
| 页面长时间停在 Connecting | 确认浏览器和开发板可互通，关闭 AP 客户端隔离并检查 UDP 被防火墙拦截的情况。 |
| 已连接却无画面 | 用 H.264 重试；同时确认浏览器支持 H.265，且页面已收到新的关键帧。 |
| 网页仍显示旧状态 | 浏览器可能缓存了旧的内嵌网页。重新加载或强制刷新页面；脚本已经发送 `Cache-Control: no-store` 响应头。 |
| HTTP 输出 `ECONNRESET` | 浏览器在请求完成后关闭短连接是正常情况，示例会忽略常见的 `ECONNRESET`/`EPIPE`。 |

## 安全范围

该示例仅用于受信任的局域网开发和验证。HTTP 信令没有访问控制，也不启用 TLS；不应直接暴露到公网。公网部署需要至少增加鉴权、HTTPS/WSS 信令和 STUN/TURN 服务。

相关 API 请参阅 [`webrtc` 模块 API](../../api/mpp/k230_canmv_webrtc_module_api_manual.md) 和 [VENC 模块 API](../../api/mpp/k230_canmv_venc_module_api_manual.md)。
