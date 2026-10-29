# `DisplayConfig` Module API Manual

## Overview

`libs/DisplayConfig.py` is used to solve the display adaptation issue when running the same AI example on different development boards. The development boards in the K230/K230D ecosystem are equipped with different screens (HDMI, ST7701, HX8399, ILI9806…), and previously examples required manually modifying `display_mode` to run on another board. This module centrally maintains the "board type → screen driver" mapping, and combined with `display_mode="auto"`, it enables cross-board operation.

The module provides three functions and one class:

| Name | Purpose |
|------|------|
| `get_default_display_mode` | Queries the default screen driver name for the current development board |
| `get_display_type` | Resolves the driver name into the driver constant required by `Display.init()` |
| `init_display` | Initializes the display and returns the **actual** display resolution, suitable for scenarios that do not use `PipeLine` |
| `DisplayImage` | Uses AI2D to scale RGB888 data of any resolution to the display resolution |

```{admonition} Tip
:class: note
AI programs that use [`PipeLine`](./pipeline_module_api_manual.md) do not need to call this module directly; just set `display_mode` to `"auto"`, and `PipeLine` will automatically handle the resolution internally. This module is mainly intended for scenarios that do not use `PipeLine`, such as UVC cameras, MP4 decoding playback, LVGL applications, etc.
```

## API Introduction

### get_default_display_mode

**Description**

Returns the default screen driver name for the development board based on the board model. The board type is obtained through `os.uname()[-1]`.

```{admonition} Note
:class: warning
The return value is the **recommended** driver that comes with the development board, not a hardware detection result of which screen is actually connected. If you are using a non-standard screen, please explicitly specify `display_mode`.
```

**Syntax**

```python
from libs.DisplayConfig import get_default_display_mode

mode = get_default_display_mode()          # Query the current development board
mode = get_default_display_mode("k230_canmv_01studio")   # Query a specific board type
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|------|-----------|------|
| board_type | Development board model string | Input | Optional, default `None` means querying the currently running firmware |

**Return Value**

| Return Value | Description |
|--------|------|
| str | Screen driver name, such as `hdmi`, `st7701`, `hx8399`, etc., which can be passed directly to `PipeLine`'s `display_mode` |

Supported development boards and their default screen drivers:

| Default Driver | Development Board |
|----------|--------|
| `hdmi` | `k230_canmv`、`k230_canmv_v3p0` |
| `hx8399` | `k230_evb`、`k230d_evb` |
| `nt35516` | `k230_canmv_rtt_evb` |
| `st7701` | `k230_canmv_01studio`、`k230_canmv_lckfb`、`k230_canmv_yahboom`、`k230_canmv_mrt`、`k230_canmv_hiwonder`、`k230_labplus_1956`、`k230d_canmv_bpi_zero`、`k230d_canmv_atk_dnk230d`、`k230d_canmv_junroc_ai_cam`、`k230d_canmv_lushanpi_lite`、`k230d_canmv_mini`、`k230d_labplus_ai_camera`、`k230d_labplus_ai_camera_v2` |
| `ili9806` | `k230_canmv_dongshanpi` |
| `gc9503` | `k230_canmv_gt6700` |
| `jd9852` | `k230_canmv_wondermk` |

```{admonition} Note
:class: warning
When the board type is not in the table above, `ValueError: No default display for board <model>; set display_mode explicitly` will be raised. In this case, please explicitly specify the screen driver instead of using `auto`.
```

### get_display_type

**Description**

Resolves the screen driver name into the driver constant required by `Display.init()`.

**Syntax**

```python
from libs.DisplayConfig import get_display_type
from media.display import Display

display_type = get_display_type("auto")
Display.init(display_type)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|------|-----------|------|
| display_mode | Screen driver name or `Display` constant | Input | Default `"auto"`. See the [display_mode value table in the PipeLine manual](./pipeline_module_api_manual.md#init) for valid values. When an int type (i.e., `Display.XXX` constant) is passed, it is returned as-is |

**Return Value**

| Return Value | Description |
|--------|------|
| int | Driver constant accepted by `Display.init()` |

```{admonition} Note
:class: warning
Passing an unsupported string will not raise an error; it will fall back to `Display.ST7701`. This behavior is retained for compatibility with old code; new code should use the standard values.
```

### init_display

**Description**

Initializes the display device and returns the **actually effective** display resolution. The screen driver may not support the requested resolution and will use its own default instead, so subsequent layout calculations must use the return value of this function as the source of truth, not the passed-in `display_size`.

**Syntax**

```python
from libs.DisplayConfig import init_display

display_size = init_display(display_mode="auto", osd_num=1, to_ide=True)
width, height = display_size
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|------|-----------|------|
| display_mode | Screen driver name or `Display` constant | Input | Default `"auto"` |
| display_size | Expected display resolution `[width, height]` | Input | Optional, default `None` means using the driver's default resolution. Please use this parameter instead of the `width`/`height` keyword arguments |
| **kwargs | Other parameters passed through to `Display.init()` | Input | Such as `osd_num`, `to_ide`, etc. |

**Return Value**

| Return Value | Description |
|--------|------|
| list[int] | Actual display resolution `[width, height]` |

```{admonition} Note
:class: warning
This function is only responsible for initializing the display; **the caller needs to call `Display.deinit()` on its own**. It also does not start the sensor, nor does it change the AI inference resolution, decoding resolution, or recording resolution; these need to be configured separately.
```

### DisplayImage

**Description**

Uses AI2D hardware to scale RGB888 data of any resolution to the display resolution, and wraps it into an `image.Image` for display use. A typical scenario is adapting when the resolution of images output from a UVC camera or MP4 decoding does not match the screen.

Internally, the same AI2D pipeline is reused, and it is only rebuilt when the input resolution changes, so the overhead of per-frame calls is very low.

**Syntax**

```python
from libs.DisplayConfig import init_display, DisplayImage

display_size = init_display(display_mode="auto")
resizer = DisplayImage(display_size, planar=False)

while True:
    img = resizer.run(frame_np)     # frame_np is HWC-layout uint8 RGB data
    Display.show_image(img)

resizer.deinit()
```

**Constructor Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|------|-----------|------|
| display_size | Target resolution `[width, height]` | Input | Required, usually pass the return value of `init_display()` directly |
| planar | Whether the input data is in planar layout | Input | `True` means the input is in CHW layout, `False` (default) means HWC layout |

**run Method**

| Parameter Name | Description | Input / Output | Notes |
|----------|------|-----------|------|
| input_np | Data to be scaled, of type `ulab.numpy.ndarray` | Input | Contiguous uint8 RGB data; the layout must match the `planar` setting during construction |

| Return Value | Description |
|--------|------|
| image.Image | An Image instance in RGB888 format, with the resolution specified during construction |

**deinit Method**

Releases the AI2D resources held by `DisplayImage`; no parameters and no return value. Must be called before the program exits.

```{admonition} Note
:class: warning
- `run()` internally makes a copy of the AI2D output; the returned Image references an **independent data copy**, so the next `run()` will not overwrite it, and it is safe to retain across frames.
- The passed-in `input_np` must remain valid until `run()` returns (e.g., borrowed data from `to_numpy_ref()`).
- The underlying AI2D pipeline is only rebuilt when the input shape changes, so the overhead of per-frame calls is very low.
```

## Example Program

Below is the framework code that does not use `PipeLine` and directly uses this module to adapt the display:

```python
from media.display import Display
from libs.DisplayConfig import init_display, DisplayImage
import gc

resizer = None
try:
    # Automatically select the screen according to the development board model, return the actual resolution
    display_size = init_display(display_mode="auto", osd_num=1, to_ide=True)
    print("display size:", display_size)

    # When the source frame resolution does not match the screen, use DisplayImage to scale
    resizer = DisplayImage(display_size, planar=False)

    while True:
        frame_np = get_frame_from_somewhere()   # UVC / VDEC and other sources, HWC uint8 RGB
        img = resizer.run(frame_np)
        Display.show_image(img)
        gc.collect()
finally:
    if resizer is not None:
        resizer.deinit()
    Display.deinit()      # init_display is not responsible for deinitialization, you need to call it yourself
```
