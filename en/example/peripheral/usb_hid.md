# USB HID Examples

## Overview

CanMV provides HID input wrappers under the `usb` module, which can directly read input from USB keyboards, mice, and touch devices.

The current firmware includes 3 companion examples. The firmware paths on the development board are:

- `/sdcard/examples/03-Machine/usb_hid_keyboard.py`
- `/sdcard/examples/03-Machine/usb_hid_mouse.py`
- `/sdcard/examples/03-Machine/usb_hid_touch.py`

The corresponding SDK source paths are:

- `src/canmv/resources/examples/03-Machine/usb_hid_keyboard.py`
- `src/canmv/resources/examples/03-Machine/usb_hid_mouse.py`
- `src/canmv/resources/examples/03-Machine/usb_hid_touch.py`

This set of examples has the following characteristics:

- Waits in a loop and retries opening when no device is connected
- Supports automatic reconnection after the device is disconnected
- The keyboard example outputs key events and parsed characters
- The mouse example outputs key edges, relative displacement, and scroll wheel
- The touch example outputs press status, pressure, and coordinates

## Prerequisites

1. The development board works in USB Host mode
1. A USB HID device has been connected, such as a keyboard, mouse, or USB touch device
1. The firmware includes the `usb` module and USB HID host support

## Keyboard Example

```python
import time
from usb import Keyboard

def open_keyboard():
    keyboard = Keyboard(timeout_ms=1000, auto_reconnect=True)

    while True:
        try:
            keyboard.open()
            info = keyboard.info()
            print("USB keyboard ready:", info)
            return keyboard
        except OSError as err:
            print("waiting for USB keyboard:", err)
            time.sleep_ms(500)

keyboard = open_keyboard()

while True:
    frame = keyboard.read(1000)
    if not frame:
        continue

    events = frame["events"]
    if not events:
        continue

    text = frame["text"]
    chars = frame["chars"]

    for keycode, value in events:
        if value == Keyboard.VALUE_PRESSED:
            state = "pressed"
        elif value == Keyboard.VALUE_REPEAT:
            state = "repeat"
        else:
            state = "released"

        print("keycode=%d state=%s" % (keycode, state))

    if chars:
        print(
            "parsed chars=%s text=%r ctrl=%s shift=%s alt=%s meta=%s caps_lock=%s"
            % (
                chars,
                text,
                frame["ctrl"],
                frame["shift"],
                frame["alt"],
                frame["meta"],
                frame["caps_lock"],
            )
        )
```

### Output Description

- `events`: raw keyboard event frame, each element is `(keycode, value)`
- `chars`: list of character codes parsed in this frame
- `text`: byte string parsed in this frame, e.g. `b"abc"`
- `ctrl` / `shift` / `alt` / `meta` / `caps_lock`: current modifier key status

### Keyboard Example Output Reference

```text
USB keyboard ready: {'kind': 'keyboard', 'name': 'Logitech USB Keyboard', 'path': '/dev/hidk0', ...}
keycode=34 state=pressed
parsed chars=(103,) text=b'g' ctrl=False shift=False alt=False meta=False caps_lock=False
keycode=34 state=released
```

## Mouse Example

```python
import time
from usb import Mouse

def open_mouse():
    mouse = Mouse(timeout_ms=1000, auto_reconnect=True)

    while True:
        try:
            mouse.open()
            info = mouse.info()
            print("USB mouse ready:", info)
            print("button masks:", Mouse.BTN_LEFT_MASK, Mouse.BTN_RIGHT_MASK, Mouse.BTN_MIDDLE_MASK)
            return mouse
        except OSError as err:
            print("waiting for USB mouse:", err)
            time.sleep_ms(500)

mouse = open_mouse()

while True:
    frame = mouse.read(1000)
    if not frame:
        continue

    moved = frame["has_rel"] or frame["has_abs"]
    button_edge = frame["pressed_mask"] or frame["released_mask"]
    wheel_move = frame["wheel"] or frame["hwheel"]

    if not moved and not button_edge and not wheel_move:
        continue

    print(
        "buttons=%d pressed=%d released=%d rel=(%d,%d) abs=(%d,%d) wheel=(%d,%d)" % (
            frame["buttons"],
            frame["pressed_mask"],
            frame["released_mask"],
            frame["rel_x"],
            frame["rel_y"],
            frame["abs_x"],
            frame["abs_y"],
            frame["wheel"],
            frame["hwheel"],
        )
    )
```

### Mouse Example Output Reference

```text
USB mouse ready: {'kind': 'mouse', 'name': 'USB Optical Mouse', 'path': '/dev/hidm0', ...}
button masks: 1 2 4
buttons=1 pressed=1 released=0 rel=(12,-3) abs=(0,0) wheel=(0,0)
```

## Touch Example

```python
import time
from usb import Touch

def open_touch():
    touch = Touch(timeout_ms=1000, auto_reconnect=True)

    while True:
        try:
            touch.open()
            info = touch.info()
            print("USB touch ready:", info)
            return touch
        except OSError as err:
            print("waiting for USB touch device:", err)
            time.sleep_ms(500)

touch = open_touch()

while True:
    frame = touch.read(1000)
    if not frame:
        continue

    active = frame["touch_seen"] or frame["buttons"] or frame["pressure"]
    moved = frame["has_abs"] or frame["has_rel"]

    if not active and not moved:
        continue

    print(
        "down=%s pressure=%d buttons=%d abs=(%d,%d) rel=(%d,%d)" % (
            frame["touch_down"],
            frame["pressure"],
            frame["buttons"],
            frame["abs_x"],
            frame["abs_y"],
            frame["rel_x"],
            frame["rel_y"],
        )
    )
```

## Common Usage Suggestions

### 1. Use Auto-Reconnect

It is recommended to enable this when creating the object:

```python
kbd = Keyboard(timeout_ms=1000, auto_reconnect=True)
```

This way, after the USB HID device is unplugged, subsequent `poll()`, `read()`, `info()` calls will attempt to automatically recover.

### 2. Distinguish Between Raw Keys and Parsed Characters

- For shortcut keys, game controls, or raw key handling, use `events`
- For text input, use `chars` and `text`

### 3. Handle Timeout Returns

- `poll(timeout_ms)`: returns `False` on timeout
- `read(timeout_ms)`: returns `None` on timeout

So in the example, it is common to check first:

```python
frame = keyboard.read(1000)
if not frame:
    continue
```

## Frequently Asked Questions

### What to do when keyboard key characters don't match the actual input?

Please update to the firmware version that includes the latest USB HID fixes. The current implementation has corrected letter key parsing based on Linux input keycode mapping, and supports combination handling of `Ctrl`, `Shift`, and `Caps Lock`.

### Will the script stop after the device is unplugged?

If `auto_reconnect=True` is enabled, the script will enter a waiting-for-reconnection state; it will automatically resume after reinserting a device of the same type.

### Do mouse and touch use the same return structure?

Both return pointer-type frame structures, but the mouse mainly uses relative coordinates and button bits, while touch more commonly uses absolute coordinates, pressure, and `touch_down`.

## Related Documentation

- [USB HID Module API Manual](../../api/extmod/usb_hid.md)
