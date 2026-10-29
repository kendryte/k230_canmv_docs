# `usb_hid` Module API Manual

## Overview

The `usb` module provides 3 USB HID input classes:

- `Keyboard`
- `Mouse`
- `Touch`

These classes are encapsulated based on the system input HAL and support:

- Automatically find and open HID nodes by device type
- Open specific nodes by specifying path
- Timeout read
- Automatic reconnection after device unplugging
- Keyboard character parsing and modifier key state tracking

## Import Method

```python
from usb import Keyboard, Mouse, Touch
```

## Common Constructor

### `Keyboard(path=None, timeout_ms=300, auto_reconnect=True)`

### `Mouse(path=None, timeout_ms=300, auto_reconnect=True)`

### `Touch(path=None, timeout_ms=300, auto_reconnect=True)`

Creates the corresponding USB HID object.

**Parameter Description:**

- `path`: Optional, device node path, e.g. `"/dev/hidk0"`
- `timeout_ms`: Default timeout in milliseconds
- `auto_reconnect`: Whether to automatically reconnect after the device is disconnected, default `True`

If `path` is not provided, the object will automatically find the first matching device by type.

## General Methods

### `open([path])`

Open the HID device.

**Parameters:**

- `path`: Optional, when provided overrides the current object path

**Return Value:**

- `True`: Opened successfully

**Exceptions:**

- Raises `OSError` on failure

### `close()`

Close the current device and release the handle.

After closing, the object can still call `open()` or `reconnect()` again.

### `is_open()`

Returns whether the device instance is currently held.

**Return Value:**

- `True`: Opened
- `False`: Not opened

### `poll([timeout_ms])`

Wait for a HID input event.

**Parameters:**

- `timeout_ms`: Optional, overrides the object's default timeout

**Return Value:**

- `True`: Data is available to read
- `False`: Timed out

If `auto_reconnect=True` is enabled, the device will attempt to automatically reconnect after disconnection instead of failing immediately.

### `info()`

Query current device information.

**Return Value:**

Returns a `dict` containing the following fields:

- `kind`: Device type, string, e.g. `"keyboard"`
- `name`: Device name
- `path`: Current device path
- `ev_bits`: Event type bitmap
- `key_bits`: Key capability bitmap
- `rel_bits`: Relative coordinate capability bitmap
- `abs_bits`: Absolute coordinate capability bitmap
- `auto_reconnect`: Whether auto-reconnect is currently enabled

**Example:**

```python
from usb import Keyboard

kbd = Keyboard(auto_reconnect=True)
kbd.open()
print(kbd.info())
```

### `reconnect()`

Immediately attempt to reconnect the current HID device.

If the object was created using automatic type matching, it will search again for a device of the same type; if the object was created with an explicit `path`, it will attempt to reopen the same path.

## Keyboard Class

### `read([timeout_ms])`

Reads one frame of keyboard events.

**Return Value:**

- Returns `dict` on success
- Returns `None` on timeout

The returned dictionary fields are as follows:

- `events`: event tuple, each element is `(keycode, value)`
- `count`: number of key-value pairs in this frame
- `complete`: whether the frame-end sync event was encountered
- `chars`: parsed character encoding tuple, e.g. `(97, 98)`
- `text`: parsed byte string, e.g. `b"ab"`
- `shift`: current Shift state
- `ctrl`: current Ctrl state
- `alt`: current Alt state
- `meta`: current Meta/Win state
- `caps_lock`: current Caps Lock state

**Event Value Constants:**

- `Keyboard.VALUE_RELEASED`
- `Keyboard.VALUE_PRESSED`
- `Keyboard.VALUE_REPEAT`

**Example:**

```python
from usb import Keyboard

kbd = Keyboard(timeout_ms=1000, auto_reconnect=True)
kbd.open()

while True:
    frame = kbd.read(1000)
    if not frame:
        continue

    print(frame["events"])
    print(frame["text"])
```

### Keyboard Character Parsing Notes

`Keyboard.read()` parses characters based on the current modifier key state, supporting:

- Regular letter and number keys
- `Shift` case switching
- `Caps Lock` case switching
- `Ctrl + A` through `Ctrl + Z`
- Common symbol keys, e.g. `-=[]\\;',./`

If you only care about raw key presses, use the `events` field.

## Mouse Class

### `read([timeout_ms])`

Read one frame of mouse data.

**Return Value:**

- Returns `dict` on success
- Returns `None` on timeout

The returned dictionary fields are as follows:

- `kind`
- `complete`
- `has_rel`
- `has_abs`
- `touch_seen`
- `touch_down`
- `rel_x`
- `rel_y`
- `wheel`
- `hwheel`
- `abs_x`
- `abs_y`
- `pressure`
- `buttons`
- `pressed_mask`
- `released_mask`

**Button Bit Constants:**

- `Mouse.BTN_LEFT_MASK`
- `Mouse.BTN_RIGHT_MASK`
- `Mouse.BTN_MIDDLE_MASK`
- `Mouse.BTN_TOUCH_MASK`

**Example:**

```python
from usb import Mouse

mouse = Mouse(timeout_ms=1000, auto_reconnect=True)
mouse.open()

while True:
    frame = mouse.read(1000)
    if frame:
        print(frame)
```

## Touch Class

### `read([timeout_ms])`

Reads one frame of USB touch input.

The return structure is similar to `Mouse.read()`, but more commonly uses the following fields:

- `has_abs`
- `abs_x`
- `abs_y`
- `pressure`
- `touch_seen`
- `touch_down`
- `buttons`

**Example:**

```python
from usb import Touch

tp = Touch(timeout_ms=1000, auto_reconnect=True)
tp.open()

while True:
    frame = tp.read(1000)
    if frame:
        print(frame["touch_down"], frame["abs_x"], frame["abs_y"])
```

## Properties

All HID objects support reading and writing the following properties:

- `path`
- `timeout_ms`
- `auto_reconnect`

**Example:**

```python
from usb import Keyboard

kbd = Keyboard()
print(kbd.timeout_ms)
kbd.timeout_ms = 1000
kbd.auto_reconnect = True
```

## Frequently Asked Questions

### 1. What happens to `read()` / `poll()` after the device is unplugged?

If `auto_reconnect=True`, the object checks the device status during timeout polling and attempts to automatically reconnect; after reinserting a device of the same type, it can continue to work.

### 2. Why is `text` of type `bytes` instead of `str`?

This field is used directly to represent raw ASCII results, making it more suitable for use in serial terminals, protocol handling, and low-level event streams; if a string is needed, you can manually `decode()` it.

### 3. Why is `chars` sometimes empty but `events` is not?

Because some events are modifier keys, function keys, or navigation keys, they appear in `events` but do not generate printable characters.

## Related Documents

- [USB HID Example](../../example/peripheral/usb_hid.md)
