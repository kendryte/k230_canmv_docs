# 小智语音助手例程讲解

## 概述

本例程在 CanMV K230 上实现「小智」语音助手客户端，通过 WebSocket 与云端小智服务通信，完成语音采集、上传、TTS 播放、界面状态显示，并支持人脸检测/注册唤醒与 MCP / IoT 设备控制能力。

例程位置：

- 开发板固件路径：`/sdcard/examples/26-xiaozhi/`
- SDK 源码路径：`src/canmv/resources/examples/26-xiaozhi/`

## 环境准备

运行本例程前，请确认：

- **硬件**：CanMV K230 开发板、摄像头模组、板载麦克风与扬声器/耳机；默认对话按键为 **GPIO21**（低电平有效），状态灯为 **GPIO52**。可在 `run.py` 顶部的 `PROJECT_CONFIG` 中修改。
- **网络**：开发板已通过 LAN 或 WLAN 接入互联网，可访问小智 OTA / WebSocket 服务（默认 `api.tenclass.net`）。
- **存储**：SD 卡中已包含本例程目录及相关资源（字体、表情图等）。
- **配置**：所有用户配置统一位于 `run.py` 顶部的 `PROJECT_CONFIG`。首次运行会生成 `/data/xiaozhi.cfg`，该文件只保存自动生成的 UUID 和 MAC，不需要手动修改。

## 运行方式

### 首次激活

第一次启动时需要先完成设备激活，否则无法正常连接小智服务。

- 在浏览器打开小智官网：[https://xiaozhi.me/](https://xiaozhi.me/)，按页面指引完成设备绑定/激活。
- 激活码会在**第一次启动**时打印在串口 log 中，请注意查看，例如：

  ```text
  收到激活码: xxxxxx
  设备需要激活，激活码: xxxxxx
  ```

- 将 log 中的激活码填入官网对应位置完成激活。激活成功后，再次运行例程即可正常建连；后续启动一般无需重复激活。

### 启动

在 CanMV IDE 中打开并运行：

```text
/sdcard/examples/26-xiaozhi/run.py
```

运行前只需修改 `run.py` 顶部的 `PROJECT_CONFIG`，其他项目文件无需修改：

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

`network.type` 设为 `"default"` 时会复用已经联网的默认接口；设为 `"lan"`
时使用 LAN；设为 `"wifi_sta"` 时使用上面的 SSID 和密码连接 Wi-Fi。

程序会依次完成：UI / 摄像头初始化 → 设备初始化 → OTA 激活 → 连接小智 WebSocket 服务。

启动成功后，串口与界面状态会提示类似：

```text
小智语音助手已启动，按Ctrl+C退出
```

界面状态最终会进入 **「等待按键唤醒」**。

### 重要提醒：先等「等待按键唤醒」，再按键对话

> **请务必先等到界面/状态显示「等待按键唤醒」之后，再按下按键开始对话。**  
> 若在网络连接、设备激活或会话建立完成前就按键，可能出现「网络连接中，请稍后」等提示，此时需等待连接完成后再试。

推荐交互流程：

- 等待状态变为 **「等待按键唤醒」**。
- **按下并按住** 板载对话按键（GPIO21）：开始录音，状态变为「等待您的指令」，LED（GPIO52）点亮。
- **对着麦克风说话**。
- **松开按键**：结束录音并上传，等待云端回复；TTS 播放时状态为「说话中」。
- 播放结束后再次回到 **「等待按键唤醒」**，可进行下一轮对话。

补充说明：

- 本例程默认使用 **手动按键** 交互模式（按住说话、松开结束）。
- 若已注册人脸，识别到已注册用户时，也可触发人脸唤醒（发送唤醒文本），无需按键。
- 在 IDE 中停止脚本或 Ctrl+C 可退出；退出时会先停人脸检测与 WebSocket / 音频线程。

## 代码架构

例程按职责拆分为多层，入口为 `run.py`：

```text
run.py                 # 启动入口：UI + Client 组装、主循环、退出清理
├── xiaozhiclient.py   # 业务中枢：激活、会话、按键/人脸唤醒、消息分发
├── websocket_client.py# WebSocket 收发（含 Opus 音频帧）
├── http_client.py     # OTA / 激活 HTTP 请求
├── audio_manager.py   # 录音 / Opus 编解码 / TTS 播放队列
├── config.py          # 配置加载、UUID/MAC、WS 地址与 hello
├── state.py           # 协议消息类型、会话状态、消息构建/解析
├── lvgl_ai.py         # LVGL UI + 摄像头 + 人脸检测线程
├── face_reg_rec.py    # 人脸识别 / 注册
└── iot/               # MCP / IoT 设备抽象
    ├── thing.py
    ├── thing_manager.py
    └── things/speaker.py   # 示例设备：扬声器音量控制
```

### 模块说明

| 模块 | 作用 |
|------|------|
| `run.py` | 创建 `XiaoZhi_UI` 与 `XiaoZhiClient`，注册回调，主循环中刷新 LVGL 与 UI 更新队列 |
| `xiaozhiclient.py` | 设备生命周期、按键录音、人脸唤醒、处理 hello / STT / TTS / LLM / IoT / MCP 消息 |
| `websocket_client.py` | 维护 WSS 连接、心跳、文本/二进制帧收发 |
| `audio_manager.py` | AI/AO 采集播放，Opus 编码上传与解码播放（播放侧使用预缓冲队列减轻卡顿） |
| `lvgl_ai.py` | 界面状态、表情、字幕；人脸检测叠加；跨线程 UI 更新通过队列在主循环 `flush` |
| `iot/` | 将板端能力抽象为 Thing，上报 descriptors / states，执行云端下发的控制命令 |

### 数据流（简图）

```text
按键按下
  → AudioManager 录音 → Opus 编码
  → WebSocket 二进制上传
  → 云端 ASR / LLM / TTS
  → WebSocket 下发 Opus + 文本消息
  → AudioManager 播放 + UI 更新状态/字幕/表情

云端 IoT / MCP 控制
  → ThingManager.invoke(...)
  → 如 Speaker.setvolume 调节音量
  → 回传 states
```

### 启动流程（核心逻辑）

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
    # ... 人脸结果同步、按需重连等
```

## MCP 与 IoT 功能

本例程在连接握手的 `hello` 消息中声明支持 MCP：

```python
"features": {
    "mcp": True
}
```

对应实现要点：

- **能力声明**：`state.MessageBuilder.build_hello_message()` 中设置 `features.mcp = True`，告知云端客户端支持 MCP 相关能力。
- **IoT 设备模型**：通过 `ThingManager` 注册板端设备（当前示例为 `Speaker`），会话建立后上报 `descriptors`（设备与方法描述，如音量属性、`setvolume` 方法）以及 `states`（当前设备状态）。
- **命令执行**：收到 `type: "iot"` 消息后，由 `ThingManager.invoke()` 分发执行，例如：

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

  执行后若状态变化，会再次上报 `states`。
- **MCP 消息通道**：协议侧已支持 `type: "mcp"` 的解析与分发入口（`_hanle_mcp_message`），可在此基础上扩展 MCP 工具调用；当前示例以 IoT Thing（如扬声器音量）演示端侧可控能力。

扩展新设备时，可参考 `iot/things/speaker.py`：

- 继承 `Thing`，定义属性与方法；
- 在 `ThingManager.initialize_iot_devices()` 中 `add_thing(...)` 注册。

## 界面与状态提示

常见界面/状态文案含义如下：

| 状态文案 | 含义 |
|----------|------|
| 网络连接中，请稍后。。。。 | WebSocket 尚未就绪，请稍候再按键 |
| 等待按键唤醒 | 已就绪，可按住按键开始说话 |
| 等待您的指令 | 正在录音，请说话 |
| 获取指令结束 | 已松键，结束本轮录音 |
| 说话中 / 说话结束 | TTS 播放开始 / 结束 |
| 网络已连接 / 网络连接中断 | WebSocket 连接状态变化 |

## 注意事项

- **先等「等待按键唤醒」，再按键对话**，避免在激活或建连过程中误触发录音。
- **首次启动请先完成官网激活**（[https://xiaozhi.me/](https://xiaozhi.me/)），激活码见串口 log。
- 需要稳定网络；首次激活依赖 OTA 接口，请确认防火墙/代理不会拦截 HTTPS / WSS。
- 人脸检测与 TTS 播放会同时占用算力与内存，长时间运行请保证散热与电源稳定。
- 从 IDE 停止脚本时可能出现 soft reboot 相关日志（如 Display unbind、ISP stop），属资源回收过程，一般不影响再次运行。

具体多媒体、网络相关接口可参考文档：[audio](../media/audio.md)、[display](../media/display.md)、[sensor](../media/sensor.md)、[lvgl](../media/lvgl.md)、[network](../network/index.md)、[socket](../../api/extmod/k230_canmv_socket_api_manual.md)。
