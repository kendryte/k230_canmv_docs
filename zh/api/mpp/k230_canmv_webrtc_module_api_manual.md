# `webrtc` 模块 API 手册

## 概述

`webrtc` 是 CanMV 对 libpeer 的原生 MicroPython 封装。它提供后台协议工作线程，处理 ICE、DTLS-SRTP 和 RTP；Python 应用负责 HTTP/其他信令、视频编码以及媒体发送。

模块由 `CONFIG_ENABLE_MODULE_WEBRTC` 控制，默认启用并依赖 libpeer。每个 MicroPython 运行时最多只能同时创建一个 `PeerConnection`；已有连接未关闭时再次创建会抛出 `OSError(EBUSY)`。

随附的局域网摄像头示例见 [WebRTC Camera](../../example/media/webrtc.md)。

## 常量

### SDP 类型

| 常量 | 含义 |
| :-- | :-- |
| `SDP_TYPE_OFFER` | SDP Offer |
| `SDP_TYPE_ANSWER` | SDP Answer |

### 编码类型

| 常量 | 含义 |
| :-- | :-- |
| `CODEC_NONE` | 不启用对应媒体类型 |
| `CODEC_H264` | H.264 视频 |
| `CODEC_H265` | H.265 视频 |
| `CODEC_OPUS` | Opus 音频负载 |
| `CODEC_PCMA` | G.711 A-law 音频负载 |
| `CODEC_PCMU` | G.711 u-law 音频负载 |

设置音频编码类型不会把 PCM 自动编码为 Opus/PCMA/PCMU；`send_audio()` 的数据必须已经完成编码。

### 连接状态

| 常量 | 含义 |
| :-- | :-- |
| `STATE_CLOSED` | 已关闭 |
| `STATE_NEW` | 已创建，尚未完成 SDP 协商 |
| `STATE_CHECKING` | ICE 连通性检查中 |
| `STATE_CONNECTED` | ICE 已连接，DTLS 握手进行中 |
| `STATE_COMPLETED` | DTLS-SRTP 已完成，可发送媒体 |
| `STATE_FAILED` | ICE 或 DTLS 失败 |
| `STATE_DISCONNECTED` | 连接中断 |

## `PeerConnection`

### 构造函数

```python
import webrtc

peer = webrtc.PeerConnection(
    video_codec=webrtc.CODEC_H265,
    audio_codec=webrtc.CODEC_NONE,
    audio_sample_rate=48000,
    ice_server=None,
    ice_username=None,
    ice_credential=None,
)
```

| 参数 | 含义 | 默认值 |
| :-- | :-- | :-- |
| `video_codec` | `CODEC_NONE`、`CODEC_H264` 或 `CODEC_H265` | `CODEC_H265` |
| `audio_codec` | `CODEC_NONE`、`CODEC_OPUS`、`CODEC_PCMA` 或 `CODEC_PCMU` | `CODEC_NONE` |
| `audio_sample_rate` | 音频采样率，必须大于 0 | `48000` |
| `ice_server` | 可选 STUN/TURN 服务地址 | `None` |
| `ice_username` | 可选 ICE 服务用户名 | `None` |
| `ice_credential` | 可选 ICE 服务凭据 | `None` |

构造完成后，模块会启动后台协议线程。局域网视频通常不需要配置 `ice_server`。

### SDP 和 ICE

```python
offer = peer.create_offer()
answer = peer.create_answer()
peer.set_remote_description(answer_sdp, webrtc.SDP_TYPE_ANSWER)
result = peer.add_ice_candidate(candidate_sdp)
```

| 方法 | 说明 |
| :-- | :-- |
| `create_offer()` | 创建本地 SDP Offer，返回 `str`。再次调用会关闭当前连接并开始新的 Offer。 |
| `create_answer()` | 在已设置远端 Offer 后创建 SDP Answer，返回 `str`。 |
| `set_remote_description(sdp, type=SDP_TYPE_ANSWER)` | 设置远端 SDP；非 trickle 场景的候选地址可直接包含在 SDP 中。 |
| `add_ice_candidate(candidate)` | 解析并添加一个远端候选，成功返回 `0`。 |

### 媒体发送

```python
peer.send_video(venc_data, timestamp_us)
peer.send_audio(encoded_audio, timestamp_us)
```

| 方法 | 参数 | 说明 |
| :-- | :-- | :-- |
| `send_video(data, timestamp_us)` | 缓冲区、微秒时间戳 | 发送 Annex-B H.264/H.265 VENC 码流，返回底层发送结果。 |
| `send_audio(data, timestamp_us)` | 已编码缓冲区、微秒时间戳 | 发送与 `audio_codec` 对应的音频负载。 |

仅在 `is_connected()` 返回 `True` 后发送媒体。新接收端需要关键帧和编码参数集：H.264 发送 SPS/PPS，H.265 发送 VPS/SPS/PPS，然后发送 I 帧。

### 状态和关闭

```python
print(peer.state())       # 整数状态常量
print(peer.state_name())  # 例如 "COMPLETED"
if peer.is_connected():
    pass
peer.close()
```

| 方法 | 说明 |
| :-- | :-- |
| `state()` | 返回当前状态整数。 |
| `state_name()` | 返回当前状态名称。 |
| `is_connected()` | 仅在状态为 `STATE_COMPLETED` 时返回 `True`。 |
| `close()` | 停止后台线程、销毁 PeerConnection 并释放 libpeer 资源；可重复调用。 |

`PeerConnection` 被垃圾回收时也会关闭，但应用应在 `finally` 中显式调用 `close()`。

## 典型信令流程

下面展示最小的板端 Offer 流程。HTTP 服务器的实现由应用决定。

```python
peer = webrtc.PeerConnection(video_codec=webrtc.CODEC_H265)
try:
    offer_sdp = peer.create_offer()
    # 将 offer_sdp 返回给浏览器。
    # 接收浏览器 POST 的 answer_sdp 后：
    peer.set_remote_description(answer_sdp)

    while not peer.is_connected():
        time.sleep_ms(10)

    # 从 Encoder.GetStream() 取得 H.265 Annex-B 数据后发送。
finally:
    peer.close()
```

完整示例还会处理浏览器 mDNS 候选地址、HTTP 客户端提前断开、编码参数集缓存、连接建立时请求 IDR，以及网络接口选择。

## 注意事项

- WebRTC 摄像头示例默认 H.265、`512 Kbit/s`、无音频。浏览器不支持 H.265 时，将示例的 `VIDEO_CODEC` 改为 `"h264"`。
- 该模块不创建摄像头、VENC 或 HTTP 服务；应用必须自行管理这些资源。
- `send_video()` 发送时会与后台协议线程同步。不要在持有其他长时间锁的情况下调用它。
- 对于公网或复杂 NAT 场景，请配置 STUN/TURN，并实现带鉴权的信令服务；示例的 HTTP 服务只适合可信局域网。
