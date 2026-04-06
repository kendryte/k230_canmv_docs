# USB HID 示例

## 概述

CanMV 提供 `usb` 模块下的 HID 输入封装，可直接读取 USB 键盘、鼠标和触摸输入。

当前固件内置了 3 个配套示例：

- `src/canmv/resources/examples/03-Machine/usb_hid_keyboard.py`
- `src/canmv/resources/examples/03-Machine/usb_hid_mouse.py`
- `src/canmv/resources/examples/03-Machine/usb_hid_touch.py`

这组示例具备以下特点：

- 设备未插入时循环等待并重试打开
- 设备断开后支持自动重连
- 键盘示例会输出按键事件以及解析后的字符
- 鼠标示例会输出按键边沿、相对位移和滚轮
- 触摸示例会输出按下状态、压力和坐标

## 使用前提

1. 开发板工作在 USB Host 模式
1. 已插入 USB HID 设备，例如键盘、鼠标或 USB 触摸设备
1. 固件中包含 `usb` 模块和 USB HID 主机支持

## 键盘示例

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

### 输出说明

- `events`：原始键盘事件帧，每个元素是 `(keycode, value)`
- `chars`：本帧解析出的字符编码列表
- `text`：本帧解析出的字节串，例如 `b"abc"`
- `ctrl` / `shift` / `alt` / `meta` / `caps_lock`：当前修饰键状态

### 键盘示例输出参考

```text
USB keyboard ready: {'kind': 'keyboard', 'name': 'Logitech USB Keyboard', 'path': '/dev/hidk0', ...}
keycode=34 state=pressed
parsed chars=(103,) text=b'g' ctrl=False shift=False alt=False meta=False caps_lock=False
keycode=34 state=released
```

## 鼠标示例

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

### 鼠标示例输出参考

```text
USB mouse ready: {'kind': 'mouse', 'name': 'USB Optical Mouse', 'path': '/dev/hidm0', ...}
button masks: 1 2 4
buttons=1 pressed=1 released=0 rel=(12,-3) abs=(0,0) wheel=(0,0)
```

## 触摸示例

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

## 常见用法建议

### 1. 使用自动重连

建议创建对象时启用：

```python
kbd = Keyboard(timeout_ms=1000, auto_reconnect=True)
```

这样在 USB HID 设备拔出后，后续 `poll()`、`read()`、`info()` 会尝试自动恢复。

### 2. 区分原始按键与解析字符

- 需要做快捷键、游戏控制、原始按键处理时，用 `events`
- 需要输入文本时，用 `chars` 和 `text`

### 3. 处理超时返回

- `poll(timeout_ms)`：超时返回 `False`
- `read(timeout_ms)`：超时返回 `None`

因此示例里通常先判断：

```python
frame = keyboard.read(1000)
if not frame:
    continue
```

## 常见问题

### 键盘按键字符和实际输入不一致怎么办？

请更新到包含最新 USB HID 修复的固件版本。当前实现已经按 Linux input keycode 映射修正了字母键解析，并支持 `Ctrl`、`Shift`、`Caps Lock` 的组合处理。

### 设备拔出后脚本会停止吗？

如果启用了 `auto_reconnect=True`，脚本会进入等待重连状态；重新插入同类设备后会自动恢复。

### 鼠标和触摸都使用相同返回结构吗？

两者都返回指针类帧结构，但鼠标主要使用相对坐标和按键位，触摸更常使用绝对坐标、压力和 `touch_down`。

## 相关文档

- [USB HID 模块 API 手册](../../api/extmod/usb_hid.md)
