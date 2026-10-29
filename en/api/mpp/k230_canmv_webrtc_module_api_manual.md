# `webrtc` Module API Manual

## Overview

`webrtc` is CanMV's native MicroPython wrapper for libpeer. It provides background protocol worker threads that handle ICE, DTLS-SRTP, and RTP; the Python application is responsible for HTTP/other signaling, video encoding, and media sending.

The module is controlled by `CONFIG_ENABLE_MODULE_WEBRTC`, enabled by default and depends on libpeer. Each MicroPython runtime can create at most one `PeerConnection` at a time; creating another one while an existing connection has not been closed will raise `OSError(EBUSY)`.

An accompanying LAN camera example can be found at [WebRTC Camera](../../example/media/webrtc.md).

## Constants

### SDP Types

| Constant | Meaning |
| :-- | :-- |
| `SDP_TYPE_OFFER` | SDP Offer |
| `SDP_TYPE_ANSWER` | SDP Answer |

### Codec Types

| Constant | Meaning |
| :-- | :-- |
| `CODEC_NONE` | Do not enable the corresponding media type |
| `CODEC_H264` | H.264 video |
| `CODEC_H265` | H.265 video |
| `CODEC_OPUS` | Opus audio payload |
| `CODEC_PCMA` | G.711 A-law audio payload |
| `CODEC_PCMU` | G.711 u-law audio payload |

Setting the audio codec type does not automatically encode PCM to Opus/PCMA/PCMU; the data passed to `send_audio()` must already be encoded.

### Connection States

| Constant | Meaning |
| :-- | :-- |
| `STATE_CLOSED` | Closed |
| `STATE_NEW` | Created, SDP negotiation not yet completed |
| `STATE_CHECKING` | ICE connectivity checks in progress |
| `STATE_CONNECTED` | ICE connected, DTLS handshake in progress |
| `STATE_COMPLETED` | DTLS-SRTP completed, ready to send media |
| `STATE_FAILED` | ICE or DTLS failed |
| `STATE_DISCONNECTED` | Connection interrupted |

## `PeerConnection`

### Constructor

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

| Parameter | Meaning | Default |
| :-- | :-- | :-- |
| `video_codec` | `CODEC_NONE`, `CODEC_H264`, or `CODEC_H265` | `CODEC_H265` |
| `audio_codec` | `CODEC_NONE`, `CODEC_OPUS`, `CODEC_PCMA`, or `CODEC_PCMU` | `CODEC_NONE` |
| `audio_sample_rate` | Audio sample rate, must be greater than 0 | `48000` |
| `ice_server` | Optional STUN/TURN server address | `None` |
| `ice_username` | Optional ICE server username | `None` |
| `ice_credential` | Optional ICE server credential | `None` |

After construction completes, the module starts a background protocol thread. LAN video typically does not need to configure `ice_server`.

### SDP and ICE

```python
offer = peer.create_offer()
answer = peer.create_answer()
peer.set_remote_description(answer_sdp, webrtc.SDP_TYPE_ANSWER)
result = peer.add_ice_candidate(candidate_sdp)
```

| Method | Description |
| :-- | :-- |
| `create_offer()` | Creates a local SDP Offer, returns `str`. Calling again will close the current connection and start a new Offer. |
| `create_answer()` | Creates an SDP Answer after the remote Offer has been set, returns `str`. |
| `set_remote_description(sdp, type=SDP_TYPE_ANSWER)` | Sets the remote SDP; candidate addresses in non-trickle scenarios can be included directly in the SDP. |
| `add_ice_candidate(candidate)` | Parses and adds a remote candidate, returns `0` on success. |

### Media Sending

```python
peer.send_video(venc_data, timestamp_us)
peer.send_audio(encoded_audio, timestamp_us)
```

| Method | Parameter | Description |
| :-- | :-- | :-- |
| `send_video(data, timestamp_us)` | Buffer, microsecond timestamp | Sends Annex-B H.264/H.265 VENC stream, returns the underlying send result. |
| `send_audio(data, timestamp_us)` | Encoded buffer, microsecond timestamp | Sends the audio payload corresponding to `audio_codec`. |

Only send media after `is_connected()` returns `True`. New receivers need keyframes and encoding parameter sets: H.264 sends SPS/PPS, H.265 sends VPS/SPS/PPS, then sends I-frames.

### State and Closing

```python
print(peer.state())       # integer state constant
print(peer.state_name())  # e.g. "COMPLETED"
if peer.is_connected():
    pass
peer.close()
```

| Method | Description |
| :-- | :-- |
| `state()` | Returns the current state integer. |
| `state_name()` | Returns the current state name. |
| `is_connected()` | Returns `True` only when the state is `STATE_COMPLETED`. |
| `close()` | Stops the background thread, destroys the PeerConnection and releases libpeer resources; can be called repeatedly. |

`PeerConnection` is also closed when garbage collected, but the application should explicitly call `close()` in `finally`.

## Typical Signaling Flow

Below shows the minimal board-side Offer flow. The HTTP server implementation is up to the application.

```python
peer = webrtc.PeerConnection(video_codec=webrtc.CODEC_H265)
try:
    offer_sdp = peer.create_offer()
    # Return offer_sdp to the browser.
    # After receiving answer_sdp POSTed by the browser:
    peer.set_remote_description(answer_sdp)

    while not peer.is_connected():
        time.sleep_ms(10)

    # Send H.265 Annex-B data obtained from Encoder.GetStream().
finally:
    peer.close()
```

A complete example also handles browser mDNS candidate addresses, early disconnection of HTTP clients, encoding parameter set caching, requesting IDR when connection is established, and network interface selection.

## Notes

- The WebRTC camera example defaults to H.265, `512 Kbit/s`, and no audio. When the browser does not support H.265, change the example's `VIDEO_CODEC` to `"h264"`.
- This module does not create the camera, VENC, or HTTP service; the application must manage these resources itself.
- `send_video()` will synchronize with the background protocol thread when sending. Do not call it while holding other long-running locks.
- For public network or complex NAT scenarios, please configure STUN/TURN and implement a signaling service with authentication; the example HTTP service is only suitable for trusted LANs.
