# Xiaozhi Voice Assistant Example Walkthrough

## Overview

This example implements the "Xiaozhi" voice assistant client on CanMV K230, communicating with the cloud-based Xiaozhi service via WebSocket to complete voice collection, upload, TTS playback, interface status display, and supports face detection/registration wake-up and MCP / IoT device control capabilities.

Example location:

- Development board firmware path: `/sdcard/examples/26-xiaozhi/`
- SDK source code path: `src/canmv/resources/examples/26-xiaozhi/`

## Environment Preparation

Before running this example, please confirm:

- **Hardware**: CanMV K230 development board, camera module, on-board microphone and speaker/headphone; the default conversation button is **GPIO21** (active low), and the status LED is **GPIO52**. These can be modified in `PROJECT_CONFIG` at the top of `run.py`.
- **Network**: The development board is connected to the internet via LAN or WLAN and can access the Xiaozhi OTA / WebSocket service (default `api.tenclass.net`).
- **Storage**: The SD card contains this example directory and related resources (fonts, emoji images, etc.).
- **Configuration**: All user configurations are uniformly located in `PROJECT_CONFIG` at the top of `run.py`. On the first run, `/data/xiaozhi.cfg` will be generated; this file only saves the auto-generated UUID and MAC, and does not need to be manually modified.

## How to Run

### First-Time Activation

The first time you start, you need to complete device activation; otherwise, you cannot connect to the Xiaozhi service normally.

- Open the Xiaozhi official website in your browser: [https://xiaozhi.me/](https://xiaozhi.me/), and follow the page instructions to complete device binding/activation.
- The activation code will be printed in the serial port log on the **first startup**, please pay attention to check, for example:

  ```text
  收到激活码: xxxxxx
  设备需要激活，激活码: xxxxxx
  ```

- Enter the activation code from the log into the corresponding location on the official website to complete activation. After successful activation, run the example again to establish a connection normally; subsequent starts generally do not require repeated activation.

### Startup

Open and run in CanMV IDE:

```text
/sdcard/examples/26-xiaozhi/run.py
```

Before running, you only need to modify `PROJECT_CONFIG` at the top of `run.py`; other project files do not need to be modified:

```python
PROJECT_CONFIG = {
    "hardware": {
        "key_pin": 21,
        "led_pin": 52,
    },
    "network": {
        "type": "wifi_sta",       # "default"、"lan" 或 "wifi_sta"
        "wlan_device": "auto",    # "auto"、"usb"、"sdio" 或 "spi"
        "timeout": 20,
        "ssid": "canaan",
        "password": "Canaan314",
    },
    "xiaozhi": {
        "ota_url": "https://api.tenclass.net/xiaozhi/ota/",
        "websocket_url": "wss://api.tenclass.net:443/xiaozhi/v1/",
    },
    "webtts": {
        "app_id": "",
        "api_key": "",
        "api_secret": "",
        "sample_rate": 16000,
        "voice_name": "xiaoyan",
        "speed": 50,
    },
}
```

When `network.type` is set to `"default"`, it will reuse the default interface that is already connected to the network; when set to `"lan"`, LAN is used; when set to `"wifi_sta"`, the SSID and password above are used to connect to Wi-Fi.

The program will complete in sequence: UI / camera initialization → device initialization → OTA activation → connecting to the Xiaozhi WebSocket service.

After successful startup, the serial port and interface status will prompt something like:

```text
小智语音助手已启动，按Ctrl+C退出
```

The interface status will eventually enter **"Waiting for Button Wake-up"**.

### Important Reminder: Wait for "Waiting for Button Wake-up" Before Pressing the Button to Talk

> **Please be sure to wait until the interface/status shows "Waiting for Button Wake-up" before pressing the button to start a conversation.**  
> If you press the button before network connection, device activation, or session establishment is complete, you may see a prompt like "Network connecting, please wait"; in this case, you need to wait for the connection to complete before trying again.

Recommended interaction flow:

- Wait for the status to change to **"Waiting for Button Wake-up"**.
- **Press and hold** the on-board conversation button (GPIO21): recording starts, the status changes to "Waiting for your command", and the LED (GPIO52) lights up.
- **Speak into the microphone**.
- **Release the button**: recording ends and is uploaded, waiting for the cloud response; the status is "Speaking" during TTS playback.
- After playback ends, return to **"Waiting for Button Wake-up"** and you can proceed with the next round of conversation.

Additional notes:

- This example uses **manual button** interaction mode by default (hold to speak, release to end).
- If a face has been registered, recognition of a registered user can also trigger face wake-up (sending wake-up text) without pressing the button.
- You can stop the script in the IDE or use Ctrl+C to exit; on exit, face detection and WebSocket / audio threads will be stopped first.

## Code Architecture

The routine is split into multiple layers by responsibility, with the entry point being `run.py`:

```text
run.py                 # Startup entry: UI + Client assembly, main loop, exit cleanup
├── xiaozhiclient.py   # Business hub: activation, session, button/face wakeup, message dispatch
├── websocket_client.py# WebSocket send/receive (including Opus audio frames)
├── http_client.py     # OTA / activation HTTP requests
├── audio_manager.py   # Recording / Opus codec / TTS playback queue
├── config.py          # Configuration loading, UUID/MAC, WS address and hello
├── state.py           # Protocol message types, session state, message construction/parsing
├── lvgl_ai.py         # LVGL UI + camera + face detection thread
├── face_reg_rec.py    # Face recognition / registration
└── iot/               # MCP / IoT device abstraction
    ├── thing.py
    ├── thing_manager.py
    └── things/speaker.py   # Example device: speaker volume control
```

### Module Description

| Module | Function |
|------|------|
| `run.py` | Creates `XiaoZhi_UI` and `XiaoZhiClient`, registers callbacks, refreshes LVGL and UI update queue in the main loop |
| `xiaozhiclient.py` | Device lifecycle, button recording, face wakeup, handles hello / STT / TTS / LLM / IoT / MCP messages |
| `websocket_client.py` | Maintains WSS connection, heartbeat, text/binary frame send/receive |
| `audio_manager.py` | AI/AO capture and playback, Opus encoding for upload and decoding for playback (pre-buffer queue used on playback side to reduce stuttering) |
| `lvgl_ai.py` | UI state, expressions, subtitles; face detection overlay; cross-thread UI updates via queue flushed in main loop |
| `iot/` | Abstracts board-side capabilities as Things, reports descriptors / states, executes control commands issued from the cloud |

### Data Flow (Schematic)

```text
Button pressed
  → AudioManager recording → Opus encoding
  → WebSocket binary upload
  → Cloud ASR / LLM / TTS
  → WebSocket sends Opus + text message
  → AudioManager playback + UI updates state/subtitle/expression

Cloud IoT / MCP control
  → ThingManager.invoke(...)
  → e.g. Speaker.setvolume to adjust volume
  → Send back states
```

### Startup Flow (Core Logic)

```python
xiaozhi_client = XiaoZhiClient.get_instance(PROJECT_CONFIG)
xiaozhi_gui = XiaoZhi_UI()
xiaozhi_gui.user_gui_init()

xiaozhi_client.init_device(audio_download_callback, tts_state_callback, ws_state_callback)
xiaozhi_client.active_device()
xiaozhi_client.connect_to_server()
xiaozhi_client.register_update_callback(text_callback, llm_callback, status_callback)
xiaozhi_client.start_key_trigle_thread()
xiaozhi_client.start_face_wakeup_thread()

while True:
    xiaozhi_gui.flush_ui_updates()
    time.sleep_ms(lv.task_handler())
    # ... face result sync, reconnect on demand, etc.
```

## MCP and IoT Features

This example declares MCP support in the `hello` message of the connection handshake:

```python
"features": {
    "mcp": True
}
```

Key implementation points:

- **Capability declaration**: Set `features.mcp = True` in `state.MessageBuilder.build_hello_message()` to inform the cloud client that MCP-related capabilities are supported.
- **IoT device model**: Register board-side devices (the current example is `Speaker`) through `ThingManager`. After the session is established, report `descriptors` (device and method descriptions, such as the volume property and the `setvolume` method) as well as `states` (current device state).
- **Command execution**: After receiving a `type: "iot"` message, it is dispatched and executed by `ThingManager.invoke()`, for example:

  ```json
  {
    "type": "iot",
    "commands": [
      {
        "name": "Speaker",
        "method": "setvolume",
        "parameters": { "volume": 50 }
      }
    ],
    "session_id": "..."
  }
  ```

  If the state changes after execution, `states` will be reported again.
- **MCP message channel**: The protocol side already supports parsing and dispatching entry points for `type: "mcp"` (`_hanle_mcp_message`), which can be extended for MCP tool invocation; the current example uses IoT Things (such as speaker volume) to demonstrate side-controllable capabilities.

When extending new devices, refer to `iot/things/speaker.py`:

- Inherit from `Thing` and define properties and methods;
- Register with `add_thing(...)` in `ThingManager.initialize_iot_devices()`.

## UI and Status Prompts

The meanings of common UI/status texts are as follows:

| Status Text | Meaning |
|----------|------|
| 网络连接中，请稍后。。。。 | WebSocket is not yet ready, please wait before pressing the button |
| 等待按键唤醒 | Ready, press and hold the button to start speaking |
| 等待您的指令 | Recording, please speak |
| 获取指令结束 | Button released, ending this round of recording |
| 说话中 / 说话结束 | TTS playback start / end |
| 网络已连接 / 网络连接中断 | WebSocket connection status change |

## Notes

- **Wait for "等待按键唤醒" before pressing the button to talk**, to avoid mistakenly triggering recording during activation or connection establishment.
- **For the first launch, please complete activation on the official website first** ([https://xiaozhi.me/](https://xiaozhi.me/)); the activation code can be found in the serial port log.
- A stable network is required; the first activation depends on the OTA interface, please confirm that the firewall/proxy will not block HTTPS / WSS.
- Face detection and TTS playback will simultaneously occupy computing power and memory. For long-running sessions, please ensure stable cooling and power supply.
- When stopping the script from the IDE, soft reboot related logs may appear (such as Display unbind, ISP stop), which are part of the resource recycling process and generally do not affect subsequent runs.

For specific multimedia and network related interfaces, please refer to the documentation: [audio](../media/audio.md), [display](../media/display.md), [sensor](../media/sensor.md), [lvgl](../media/lvgl.md), [network](../network/index.md), [socket](../../api/extmod/k230_canmv_socket_api_manual.md).
