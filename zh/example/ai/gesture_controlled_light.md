# 手势控灯

## 简介

手势控灯是一个**无接触灯光控制**示例，位于开发板的 `CanMV/sdcard/examples/27-Gesture-controlled-light` 目录。摄像头是唯一的控制入口——没有按钮、没有遥控器、也不需要碰触摸屏：张开手掌调亮，握拳调暗，竖大拇指确认选择。

示例串联了手掌检测和手掌关键点两个模型，并在此之上做了手势解析、意图识别和状态机，是一个相对完整的 AI 应用工程范例，而不只是模型推理的演示。

适用场景：医院和洁净室的无接触照明、厨房等卫生要求高的环境、会议室灯光控制、戴手套作业的工业环境，以及行动不便用户的无障碍控制。

## 硬件准备

| 硬件 | 说明 |
|------|------|
| K230 开发板 | — |
| 显示屏 | 示例默认 LCD（800×480），也支持 HDMI |
| 摄像头 | 接 CSI 接口 |
| LED 模块 × 2 | 由硬件 PWM 驱动，实现真正的模拟调光而非开关 |
| SD 卡 | — |

**接线**：

| LED | 信号 | K230 引脚 | PWM 通道 |
|-----|------|-----------|----------|
| LED 1 | `IN` | IO42 | PWM0 |
| LED 2 | `IN` | IO43 | PWM1 |
| 两个 LED | `VCC` | 3V3 | — |
| 两个 LED | `GND` | GND | — |

```text
       K230                          LED 1
    +----------+                  +---------+
    |     IO42 |----------------->| IN      |
    |      3V3 |----------------->| VCC     |
    |      GND |----------------->| GND     |
    |          |                  +---------+
    |          |                     LED 2
    |     IO43 |----------------->| IN      |
    |      3V3 |----------------->| VCC     |
    |      GND |----------------->| GND     |
    +----------+                  +---------+
```

接线不同时，修改 `config.py` 中的 `LED_PINS` 即可；在该列表中增加一项就能控制第三盏灯。

## 运行方法

打开 CanMV IDE K230，选择左上角 `文件(F)` -> `打开文件`，选择 **此电脑->CanMV->sdcard->examples->27-Gesture-controlled-light->main.py**，点击 IDE 左下角运行按钮。

示例使用的两个模型已经随镜像提供：

| 模型 | 输入分辨率 | 作用 |
|------|-----------|------|
| `/sdcard/examples/kmodel/hand_det.kmodel` | 512×512 | 定位画面中的手掌 |
| `/sdcard/examples/kmodel/handkp_det.kmodel` | 256×256 | 输出每只手的 21 个关键点 |

## 使用方式

### 1. 径向菜单

启动后首先弹出径向菜单，共四个选项。把手指向某个扇区即可悬停选中（变为青色），保持**竖大拇指**手势确认，扇区上会有一段进度弧扫过。

```text
              LED1
        \      |      /
         \     |     /
   REGION  \   |   /   BOTH
   ---------  ( )  ---------
           /   |   \
          /    |    \
         /     |     \
              LED2
```

| 选项 | 效果 |
|------|------|
| **LED1** | 整个画面控制 LED 1 |
| **BOTH** | 整个画面同时控制两个 LED |
| **LED2** | 整个画面控制 LED 2 |
| **REGION** | 把画面分成 3 个独立控制区 |

### 2. 设备模式

选中某个设备后进入整画面控制，手放在画面任意位置都有效，张合程度直接映射为亮度：

```text
  握拳          半张开         张开手掌
  0%      →      50%      →     100%
```

### 3. 分区模式

选择 **REGION** 后，画面被竖向分成三个区域，把手放进某个区域即可控制该区域对应的设备：

```text
+-------------+-------------+-------------+
|    LEFT     |   CENTER    |    RIGHT    |
|    LED2     |    BOTH     |    LED1     |
+-------------+-------------+-------------+
```

### 4. 重新打开菜单

在任意控制模式下，做出**竖大拇指**手势即可重新打开菜单。

## 实现要点

### 处理流程

```text
摄像头 → 手掌检测(hand_det) → 手掌关键点(handkp_det, 21点)
      → 手势解析(张合度 + 竖大拇指) → 意图识别(PASS/SEEN/LOCK)
      → 状态机(菜单/设备/分区) → 多人安全检查 → PWM 亮度输出
```

### 意图识别

这是该示例最值得参考的设计。系统对每只手做跨帧跟踪并计算移动速度，只有"慢下来足够久"的手才获得控制权：

| 状态 | 颜色 | 含义 |
|------|------|------|
| **PASS** | 灰色 | 移动快——路过的手，全局忽略 |
| **SEEN** | 琥珀色 | 正在慢下来，意图累积中 |
| **LOCK** | 绿色 | 确认为有意操作，允许控制 |

这样路人走过不会误触灯光和菜单。速度单位是"屏幕宽度/秒"。在人流密集的场景，把 `INTENT_TIME_MS` 调大可以要求更长、更明确的停留。设 `INTENT_ENABLED = False` 可完全关闭该过滤。

### 多人安全

同一个控制目标上同时出现两只以上的有意操作手时，控制意图是有歧义的，此时系统会**冻结控制**并显示脉动的红色 `SAFETY LOCK` 横幅。菜单、设备模式和分区模式下均有该保护。

### 性能面板

画面底部实时显示 FPS 与帧耗时、CPU 负载、推理耗时、堆内存占用与剩余、每路 LED 的实时 PWM 占空比、采集到显示的延迟。指标超标时对应的条会变成琥珀色。

## 代码结构

| 文件 | 职责 |
|------|------|
| `main.py` | 入口：采集 → 检测 → 手势 → 状态机 主循环 |
| `config.py` | 全部可调参数 |
| `camera.py` | sensor 与显示初始化 |
| `hand_keypoint.py` | 手掌检测 + 21 点关键点两个模型 |
| `gesture.py` | 手掌张合度与竖大拇指识别 |
| `intent.py` | 路过手过滤（跨帧跟踪） |
| `menu.py` | 径向手势菜单 |
| `device.py` | 整画面单设备控制 |
| `zones.py` | 三分区控制 |
| `led_control.py` | PWM LED 驱动 |
| `perf.py` | 性能统计 |
| `ui.py` | 屏幕仪表盘 |

## 参数配置

全部参数集中在 `config.py`。

**显示与模型**

```python
DISPLAY_MODE = "lcd"            # "lcd" / "hdmi" / ...
DISPLAY_SIZE = [800, 480]
HAND_DET_KMODEL = "/sdcard/examples/kmodel/hand_det.kmodel"
HAND_KP_KMODEL  = "/sdcard/examples/kmodel/handkp_det.kmodel"
```

```{admonition} 注意
:class: warning
本示例**没有**采用其它 AI 例程通用的 `display_mode="auto"` 约定，原因是 `camera.py` 在 `pl.create()` 之后直接把 `config.DISPLAY_SIZE` 当作实际显示分辨率返回给 UI 布局，**没有调用 `pl.get_display_size()`**。径向菜单、三分区边界和底部性能面板都是按这个值计算的。

因此换屏时不能只改 `DISPLAY_MODE`，必须**同时**把 `DISPLAY_SIZE` 改成该屏的真实分辨率，否则界面元素会错位。例如换成 HDMI：

    DISPLAY_MODE = "hdmi"
    DISPLAY_SIZE = [1920, 1080]

`display_mode="auto"` 的含义与其它例程的做法见 [PipeLine 模块API手册](../../api/aidemo/pipeline_module_api_manual.md#init)。
```

**LED 硬件**

```python
LED_PINS = (("LED1", 42, 0),    # (名称, IO 引脚, PWM 通道)
            ("LED2", 43, 1))
PWM_FREQ = 1000
```

**手势到亮度的映射**

```python
CURL_CLOSED = 1.10              # 映射为 0% 亮度的手掌伸展值
CURL_OPEN   = 1.95              # 映射为 100% 亮度的手掌伸展值
SMOOTH      = 0.40              # 0~1，亮度跟随手势的快慢
```

`CURL_CLOSED` / `CURL_OPEN` 用于按您的手型和到摄像头的距离做标定。`SMOOTH` 调小则渐变更慢更柔和，调大则响应更跟手。

**意图识别**

```python
INTENT_ENABLED = True
INTENT_TIME_MS = 400            # 手需要保持"有意"多少毫秒才 LOCK
INTENT_SLOW    = 0.35           # 速度低于此值视为有意
INTENT_FAST    = 1.00           # 速度高于此值视为路过
```

**常用参数一览**

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `CURL_CLOSED` / `CURL_OPEN` | `1.10` / `1.95` | 手掌伸展范围到 0~100% 的映射 |
| `SMOOTH` | `0.40` | 亮度跟随手势的快慢 |
| `ENGAGE_FRAMES` | `3` | 一个区域需要连续多少帧只有 1 只手才交出控制权 |
| `THUMB_CONFIRM_MS` | `400` | 确认 / 重开菜单所需的保持时长 |
| `THUMB_RELEASE_MS` | `150` | 手势需要松开多久才算一次新的触发 |
| `MENU_COOLDOWN_MS` | `700` | 菜单开关后的死区时间 |
| `INTENT_TIME_MS` | `400` | 手保持有意多久后 LOCK |
| `CONFIDENCE_THRESHOLD` | `0.30` | 手掌检测置信度阈值 |
| `DET_INTERVAL` | `3` | 每 N 帧跑一次完整的手掌检测 |
| `PWM_FREQ` | `1000` | LED PWM 频率，单位 Hz |

```{admonition} 提示
`DET_INTERVAL` 是帧率和响应速度之间的主要权衡点。检测模型（512×512）比关键点模型贵得多，隔帧检测、中间帧只跑关键点可以显著提升帧率；但手快速进入画面时的首次响应会有延迟。
```

```{admonition} 注意
:class: warning
示例默认 `DISPLAY_MODE = "lcd"`、`DISPLAY_SIZE = [800, 480]`。使用 HDMI 或其它规格的屏幕时需要相应修改这两项，取值参考 [PipeLine 模块API手册](../../api/aidemo/pipeline_module_api_manual.md#init)。
```
