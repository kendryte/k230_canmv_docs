# App Center

## Introduction

The App Center is a LVGL-based graphical demo launcher located at `CanMV/sdcard/examples/28-APP_CENTER` on the development board. It integrates more than 30 AI and CV examples into a touch-interactive interface: after booting, you land on the home page with an icon grid; tap an icon to launch the corresponding example, and tap stop to return to the home page—no need to repeatedly open and switch scripts in the IDE.

For developers, the App Center is also a **reference example for running multiple applications together**, demonstrating how to perform application switching, resource cleanup, and display adaptation under limited memory.

Key features:

- **Icon grid home page**, displayed in pages, with touch-based selection.
- **Chinese/English UI switching**, with the language selection persistently saved to `/sdcard/app_center_language.txt`.
- **Adaptive display**: cards, footer, and status bar are laid out according to the actual display resolution, so screens of different sizes all display correctly.
- **Runtime status bar**: shows current frame rate, detection count, and Wi-Fi connection status.
- **Model missing detection**: checks whether the kmodel and resource files exist before launching the app, and gives a clear prompt instead of crashing directly.
- **Strict resource cleanup**: every app fully releases model and media resources when stopped, ensuring the next app can load properly.

## How to Run

Open CanMV IDE K230, select `File(F)` -> `Open File` in the top-left corner, choose **This PC->CanMV->sdcard->examples->28-APP_CENTER->main.py**, and click the run button in the bottom-left corner of the IDE.

If you want the App Center to launch automatically at boot, copy `main.py` to the root of `/sdcard` (or refer to [How to set a debugged script to auto-start](../../ai_dev_doc.md#faq-script-autostart)).

```{admonition} Note
:class: warning
The App Center requires a **touch screen** for interaction. When using HDMI output without a touch device, the interface can be displayed but cannot be selected. The IDE's virtual touch is also supported—you can click directly on the IDE screen.
```

```{admonition} Tip
The App Center loads fonts from `/sdcard/examples/15-LVGL/data/font/` and icons from `/sdcard/examples/utils/icons/`. If these directories are missing, the interface will display abnormally—please make sure the image is complete.
```

## Built-in App List

| Category | Apps |
|------|------|
| Face | Face Detection, Face Registration, Face Recognition, Face Keypoints, Face Pose, Face Parsing, Face 3D Mesh, Face Liveness Detection |
| Person | Person Detection, Person Keypoint Detection, Person Segmentation, Fall Detection |
| Hand | Palm Detection, Palm Keypoint Classification, Dynamic Gesture Recognition |
| General Detection | YOLO Object Detection, YOLO Segmentation, YOLO Rotated Object Detection |
| License Plate & OCR | License Plate Recognition, YOLO License Plate Detection, OCR Recognition |
| Other AI | Single Object Tracking, Self-Learning, Gaze Estimation, Keyword Wakeup, Chinese Text-to-Speech |
| CV (cv_lite) | Edge Detection, Line Detection, Circle Detection, Rectangle Detection |
| CV (OpenMV) | Edge Detection, Line Detection, Circle Detection, Rectangle Detection |
| System | System Information, Wi-Fi Configuration |

See `DEMO_REGISTRY` in `runner.py` for the full registry.

## Code Structure

| File | Responsibility |
|------|------|
| `main.py` | Entry point and main loop. Initializes display, LVGL, touch; drives the home page and app switching |
| `config.py` | Global constants: display configuration, theme colors, resource paths. `DISPLAY_TYPE=None` means the screen is auto-selected based on the development board model; `main.py` backfills `DISPLAY_WIDTH/HEIGHT` with the actual resolution after `Display.init()` |
| `center.py` | Home page icon grid and pagination |
| `runner.py` | App registry `DEMO_REGISTRY`, app loading, run threads, resource file checks |
| `app_contract.py` | App protocol base class `Application`, defines the lifecycle |
| `app_display.py` / `app_visual.py` | Display and drawing wrappers |
| `ui_layout.py` / `lvgl_utils.py` / `overlay.py` / `splash.py` | Interface layout, LVGL helpers, runtime overlays, splash screen |
| `touch.py` | Touch input driver, supports both physical touch and IDE virtual touch |
| `i18n.py` | Chinese/English text and language persistence |
| `model_cleanup.py` | Model resource cleanup helper functions, see [AI Resource Management and Memory Optimization](../../ai_dev_doc.md#multi-model-switching) |
| `demo_common.py` | Model path and resource path constants shared by all apps |
| `demo_*.py` | Individual specific apps |

## App Protocol

Every app inherits `app_contract.Application` (AI apps usually also inherit `AIBase`), and implements the following methods to be schedulable by the App Center:

| Member | Description |
|------|------|
| `name` | App display name |
| `model_path` | kmodel path; the file's existence will be checked before launch |
| `required_files` | List of other required resource files (such as anchors, dictionaries); same existence check applies |
| `create(display)` | Class method, creates an instance and injects the display object |
| `open()` / `start()` | Initialize resources, start sensor |
| `run_once()` | Process one frame, return the number of results in this frame; interactive apps may return `None` during preview/pause, and those frames are not counted in the frame rate statistics |
| `request_stop()` | **Only sets a flag, does not release resources**. This method is called from the LVGL thread, while resources are created in the app's own thread—cross-thread release will cause problems |
| `should_run()` | Returns whether to continue running |
| `_release_owned_resources()` | Final cleanup hook, guaranteed to be called only once |

```{admonition} Note
:class: warning
The `Application` base class **deliberately does not involve** Sensor, Media, KPU, audio, image format, or resolution strategy—these are all decided and released by each app itself. The purpose of this design is to let pure CV apps, audio apps, and vision AI apps share the same scheduling framework.
```

### Adding Your Own App

1. Create a new `demo_myapp.py`, define a class that inherits `Application` (and `AIBase` if AI inference is needed), referring to `demo_face_detect.py`.
2. Add a line in `DEMO_REGISTRY` of `runner.py`: `"myapp": ("demo_myapp", "MyAppDemo")`.
3. In `SHORT_MAP` of `center.py`, add a two-letter abbreviation for it (used as a placeholder when no icon file is available).
4. Add Chinese and English names in `i18n.py`.

```{admonition} Tip
App modules are **imported on demand** (`runner._load_demo` uses `__import__`), so a broken optional app will not affect the App Center itself or the loading of other apps.
```

## Development Tips

- **Resource release is the first principle**. The core difficulty of the application center is not the interface, but rather repeatedly loading/unloading models under limited memory. When adding a new application, be sure to implement `_release_owned_resources()`, and refer to [AI Resource Management and Memory Optimization](../../ai_dev_doc.md#ai-resource-management).
- **Do not release resources in the LVGL thread**. `request_stop()` only sets a flag; the actual release occurs when the application thread detects the flag and exits the loop.
- **Use the actual resolution for layout**. `config.CAM_WIN_W/H` are only backfilled with real values after `Display.init()`; do not use them to calculate layouts during the import phase.
- **When frame rate is low, look at the model first, not the interface**. LVGL interface refresh is only triggered on state changes; the main loop overhead is concentrated on model inference.
