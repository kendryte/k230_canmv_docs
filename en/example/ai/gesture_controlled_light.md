# Gesture-Controlled Light

## Introduction

Gesture-Controlled Light is a **contactless lighting control** example located in the development board's `CanMV/sdcard/examples/27-Gesture-controlled-light` directory. The camera is the only control input—no buttons, no remote, and no need to touch the screen: open your palm to brighten, make a fist to dim, and give a thumbs-up to confirm a selection.

The example chains together two models for palm detection and palm keypoints, and builds on top of that gesture parsing, intent recognition, and a state machine. It is a relatively complete AI application engineering example, not just a model inference demo.

Applicable scenarios: contactless lighting in hospitals and cleanrooms, hygiene-sensitive environments such as kitchens, conference room lighting control, industrial environments where gloves are worn, and accessibility control for users with limited mobility.

## Hardware Preparation

| Hardware | Description |
|------|------|
| K230 Development Board | — |
| Display | Example default LCD (800×480), HDMI is also supported |
| Camera | Connect to CSI interface |
| LED Module × 2 | Driven by hardware PWM to achieve true analog dimming rather than on/off switching |
| SD Card | — |

**Wiring**:

| LED | Signal | K230 Pin | PWM Channel |
|-----|------|-----------|----------|
| LED 1 | `IN` | IO42 | PWM0 |
| LED 2 | `IN` | IO43 | PWM1 |
| Both LEDs | `VCC` | 3V3 | — |
| Both LEDs | `GND` | GND | — |

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

When the wiring differs, modify `LED_PINS` in `config.py`; to control a third light, add one entry to this list.

## How to Run

Open CanMV IDE K230, select `File(F)` -> `Open File` in the upper left corner, choose **This PC->CanMV->sdcard->examples->27-Gesture-controlled-light->main.py**, and click the run button at the bottom left corner of the IDE.

The two models used by the example are already provided with the image:

| Model | Input Resolution | Function |
|------|-----------|------|
| `/sdcard/examples/kmodel/hand_det.kmodel` | 512×512 | Locate the palm in the frame |
| `/sdcard/examples/kmodel/handkp_det.kmodel` | 256×256 | Output 21 keypoints for each hand |

## Usage

### 1. Radial Menu

When started, a radial menu pops up first with four options. Point your finger toward a sector to hover-select it (turns cyan), and hold the **thumbs-up** gesture to confirm. A progress arc will sweep across the sector.

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

| Option | Effect |
|------|------|
| **LED1** | The entire frame controls LED 1 |
| **BOTH** | The entire frame controls both LEDs simultaneously |
| **LED2** | The entire frame controls LED 2 |
| **REGION** | Split the frame into 3 independent control zones |

### 2. Device Mode

After selecting a device, full-frame control is entered. Any position of the hand in the frame works, and the degree of opening/closing maps directly to brightness:

```text
  Fist          Half-Open         Open Palm
  0%      →      50%      →     100%
```

### 3. Region Mode

After selecting **REGION**, the frame is divided vertically into three regions. Place your hand in a region to control the device corresponding to that region:

```text
+-------------+-------------+-------------+
|    LEFT     |   CENTER    |    RIGHT    |
|    LED2     |    BOTH     |    LED1     |
+-------------+-------------+-------------+
```

### 4. Reopening the Menu

In any control mode, perform the **thumbs-up** gesture to reopen the menu.

## Implementation Highlights

### Processing Pipeline

```text
Camera → Palm detection (hand_det) → Palm keypoints (handkp_det, 21 points)
      → Gesture parsing (open/close + vertical thumb) → Intent recognition (PASS/SEEN/LOCK)
      → State machine (menu/device/zone) → Multi-person safety check → PWM brightness output
```

### Intent Recognition

This is the most noteworthy design in this example. The system tracks each hand across frames and computes movement speed; only hands that "slow down long enough" gain control:

| State | Color | Meaning |
|------|------|------|
| **PASS** | Gray | Moving fast — a passing hand, globally ignored |
| **SEEN** | Amber | Slowing down, intent accumulating |
| **LOCK** | Green | Confirmed as intentional, control permitted |

This way, passing pedestrians won't accidentally trigger the lights or menu. The speed unit is "screen width per second." In dense pedestrian scenarios, increase `INTENT_TIME_MS` to require a longer, more deliberate dwell. Setting `INTENT_ENABLED = False` disables this filter entirely.

### Multi-Person Safety

When two or more intentional operating hands appear on the same control target simultaneously, the control intent is ambiguous. In that case, the system **freezes control** and displays a pulsing red `SAFETY LOCK` banner. This protection applies in menu, device mode, and zone mode.

### Performance Panel

The bottom of the screen displays FPS and frame time, CPU load, inference latency, heap memory usage and remaining, real-time PWM duty cycle for each LED channel, and end-to-end latency from capture to display. When a metric exceeds its threshold, the corresponding bar turns amber.

## Code Structure

| File | Responsibility |
|------|------|
| `main.py` | Entry: capture → detect → gesture → state machine main loop |
| `config.py` | All adjustable parameters |
| `camera.py` | sensor and display initialization |
| `hand_keypoint.py` | Palm detection + 21-point keypoint two models |
| `gesture.py` | Palm open/close degree and thumbs-up recognition |
| `intent.py` | Passing hand filtering (cross-frame tracking) |
| `menu.py` | Radial gesture menu |
| `device.py` | Whole-frame single-device control |
| `zones.py` | Three-zone control |
| `led_control.py` | PWM LED driver |
| `perf.py` | Performance statistics |
| `ui.py` | On-screen dashboard |

## Parameter Configuration

All parameters are centralized in `config.py`.

**Display and Models**

```python
DISPLAY_MODE = "lcd"            # "lcd" / "hdmi" / ...
DISPLAY_SIZE = [800, 480]
HAND_DET_KMODEL = "/sdcard/examples/kmodel/hand_det.kmodel"
HAND_KP_KMODEL  = "/sdcard/examples/kmodel/handkp_det.kmodel"
```

```{admonition} Note
:class: warning
This example does **NOT** use the `display_mode="auto"` convention common in other AI examples. The reason is that `camera.py` returns `config.DISPLAY_SIZE` directly as the actual display resolution to the UI layout after `pl.create()`, **without calling `pl.get_display_size()`**. The radial menu, three-zone boundaries, and bottom performance panel are all computed based on this value.

Therefore, when changing the screen, you cannot only modify `DISPLAY_MODE`; you must **also** change `DISPLAY_SIZE` to the actual resolution of that screen, otherwise UI elements will be misaligned. For example, switching to HDMI:

    DISPLAY_MODE = "hdmi"
    DISPLAY_SIZE = [1920, 1080]

For the meaning of `display_mode="auto"` and how other examples handle it, see [PipeLine Module API Manual](../../api/aidemo/pipeline_module_api_manual.md#init).
```

**LED Hardware**

```python
LED_PINS = (("LED1", 42, 0),    # (name, IO pin, PWM channel)
            ("LED2", 43, 1))
PWM_FREQ = 1000
```

**Gesture-to-Brightness Mapping**

```python
CURL_CLOSED = 1.10              # Palm extension value mapped to 0% brightness
CURL_OPEN   = 1.95              # Palm extension value mapped to 100% brightness
SMOOTH      = 0.40              # 0~1, how fast brightness follows gesture
```

`CURL_CLOSED` / `CURL_OPEN` are used to calibrate according to your hand shape and distance from the camera. A smaller `SMOOTH` makes the transition slower and softer; a larger value makes it more responsive.

**Intent Recognition**

```python
INTENT_ENABLED = True
INTENT_TIME_MS = 400            # How many milliseconds the hand must remain "intentional" before LOCK
INTENT_SLOW    = 0.35           # Speed below this value is considered intentional
INTENT_FAST    = 1.00           # Speed above this value is considered passing by
```

**Common Parameters Overview**

| Parameter | Default | Function |
|------|--------|------|
| `CURL_CLOSED` / `CURL_OPEN` | `1.10` / `1.95` | Mapping of palm extension range to 0~100% |
| `SMOOTH` | `0.40` | How fast brightness follows gesture |
| `ENGAGE_FRAMES` | `3` | How many consecutive frames a zone must have only 1 hand before relinquishing control |
| `THUMB_CONFIRM_MS` | `400` | Hold duration required to confirm / reopen menu |
| `THUMB_RELEASE_MS` | `150` | How long the gesture must be released to count as a new trigger |
| `MENU_COOLDOWN_MS` | `700` | Dead-zone time after menu toggle |
| `INTENT_TIME_MS` | `400` | How long the hand remains intentional before LOCK |
| `CONFIDENCE_THRESHOLD` | `0.30` | Palm detection confidence threshold |
| `DET_INTERVAL` | `3` | Run full palm detection every N frames |
| `PWM_FREQ` | `1000` | LED PWM frequency, in Hz |

```{admonition} Tip
`DET_INTERVAL` is the main trade-off point between frame rate and response speed. The detection model (512×512) is much more expensive than the keypoint model. Skipping frames for detection and only running keypoints on intermediate frames can significantly improve frame rate; however, there will be a delay in the first response when a hand quickly enters the frame.
```

```{admonition} Note
:class: warning
The example defaults `DISPLAY_MODE = "lcd"`, `DISPLAY_SIZE = [800, 480]`. When using HDMI or other specifications of screens, these two items need to be modified accordingly. For values, refer to [PipeLine Module API Manual](../../api/aidemo/pipeline_module_api_manual.md#init).
```
