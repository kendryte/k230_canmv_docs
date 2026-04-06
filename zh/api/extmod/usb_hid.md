# `usb_hid` 模块 API 手册

## 概述

`usb` 模块提供了 3 个 USB HID 输入类：

- `Keyboard`
- `Mouse`
- `Touch`

这些类基于系统输入 HAL 封装，支持：

- 按设备类型自动查找并打开 HID 节点
- 指定路径打开特定节点
- 超时读
- 设备拔出后的自动重连
- 键盘字符解析与修饰键状态跟踪

## 导入方式

```python
from usb import Keyboard, Mouse, Touch
```

## 通用构造函数

### `Keyboard(path=None, timeout_ms=300, auto_reconnect=True)`

### `Mouse(path=None, timeout_ms=300, auto_reconnect=True)`

### `Touch(path=None, timeout_ms=300, auto_reconnect=True)`

创建对应的 USB HID 对象。

**参数说明：**

- `path`：可选，设备节点路径，例如 `"/dev/hidk0"`
- `timeout_ms`：默认超时时间，单位毫秒
- `auto_reconnect`：设备断开后是否自动重连，默认 `True`

如果未提供 `path`，对象会按类型自动查找第一个匹配设备。

## 通用方法

### `open([path])`

打开 HID 设备。

**参数：**

- `path`：可选，传入后覆盖当前对象路径

**返回值：**

- `True`：打开成功

**异常：**

- 失败时抛出 `OSError`

### `close()`

关闭当前设备并释放句柄。

关闭后对象仍可再次调用 `open()` 或 `reconnect()`。

### `is_open()`

返回当前是否已持有设备实例。

**返回值：**

- `True`：已打开
- `False`：未打开

### `poll([timeout_ms])`

等待 HID 输入事件。

**参数：**

- `timeout_ms`：可选，覆盖对象默认超时时间

**返回值：**

- `True`：有数据可读
- `False`：超时

若启用了 `auto_reconnect=True`，设备断开后会尝试自动重连，而不是立即失败。

### `info()`

查询当前设备信息。

**返回值：**

返回 `dict`，包含以下字段：

- `kind`：设备类型，字符串，例如 `"keyboard"`
- `name`：设备名称
- `path`：当前设备路径
- `ev_bits`：事件类型位图
- `key_bits`：按键能力位图
- `rel_bits`：相对坐标能力位图
- `abs_bits`：绝对坐标能力位图
- `auto_reconnect`：当前是否启用自动重连

**示例：**

```python
from usb import Keyboard

kbd = Keyboard(auto_reconnect=True)
kbd.open()
print(kbd.info())
```

### `reconnect()`

立即尝试重连当前 HID 设备。

如果对象使用自动类型匹配方式创建，则会重新查找同类设备；如果对象使用显式 `path` 创建，则会尝试重新打开同一路径。

## Keyboard 类

### `read([timeout_ms])`

读取一帧键盘事件。

**返回值：**

- 成功时返回 `dict`
- 超时返回 `None`

返回字典字段如下：

- `events`：事件元组，每个元素为 `(keycode, value)`
- `count`：本帧键值对数量
- `complete`：是否遇到帧结束同步事件
- `chars`：解析出的字符编码元组，例如 `(97, 98)`
- `text`：解析出的字节串，例如 `b"ab"`
- `shift`：Shift 当前状态
- `ctrl`：Ctrl 当前状态
- `alt`：Alt 当前状态
- `meta`：Meta/Win 当前状态
- `caps_lock`：Caps Lock 当前状态

**事件值常量：**

- `Keyboard.VALUE_RELEASED`
- `Keyboard.VALUE_PRESSED`
- `Keyboard.VALUE_REPEAT`

**示例：**

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

### 键盘字符解析说明

`Keyboard.read()` 会根据当前修饰键状态解析字符，支持：

- 普通字母和数字键
- `Shift` 大小写切换
- `Caps Lock` 大小写切换
- `Ctrl + A` 到 `Ctrl + Z`
- 常见符号键，例如 `-=[]\\;',./`

如果你只关心原始按键，请使用 `events` 字段。

## Mouse 类

### `read([timeout_ms])`

读取一帧鼠标数据。

**返回值：**

- 成功时返回 `dict`
- 超时返回 `None`

返回字典字段如下：

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

**按钮位常量：**

- `Mouse.BTN_LEFT_MASK`
- `Mouse.BTN_RIGHT_MASK`
- `Mouse.BTN_MIDDLE_MASK`
- `Mouse.BTN_TOUCH_MASK`

**示例：**

```python
from usb import Mouse

mouse = Mouse(timeout_ms=1000, auto_reconnect=True)
mouse.open()

while True:
    frame = mouse.read(1000)
    if frame:
        print(frame)
```

## Touch 类

### `read([timeout_ms])`

读取一帧 USB 触摸输入。

返回结构与 `Mouse.read()` 类似，但更常使用以下字段：

- `has_abs`
- `abs_x`
- `abs_y`
- `pressure`
- `touch_seen`
- `touch_down`
- `buttons`

**示例：**

```python
from usb import Touch

tp = Touch(timeout_ms=1000, auto_reconnect=True)
tp.open()

while True:
    frame = tp.read(1000)
    if frame:
        print(frame["touch_down"], frame["abs_x"], frame["abs_y"])
```

## 属性

所有 HID 对象都支持以下属性读写：

- `path`
- `timeout_ms`
- `auto_reconnect`

**示例：**

```python
from usb import Keyboard

kbd = Keyboard()
print(kbd.timeout_ms)
kbd.timeout_ms = 1000
kbd.auto_reconnect = True
```

## 常见问题

### 1. 拔出设备后 `read()` / `poll()` 会怎样？

若 `auto_reconnect=True`，对象会在超时轮询中检查设备状态并尝试自动重连；重新插入同类设备后可继续工作。

### 2. `text` 为什么是 `bytes` 而不是 `str`？

该字段直接用于表达原始 ASCII 结果，更适合在串口终端、协议处理和底层事件流中使用；如需字符串可手动 `decode()`。

### 3. 为什么有时 `chars` 为空但 `events` 不为空？

因为某些事件是修饰键、功能键或导航键，它们会出现在 `events` 中，但不会生成可打印字符。

## 相关文档

- [USB HID 示例](../../example/peripheral/usb_hid.md)
