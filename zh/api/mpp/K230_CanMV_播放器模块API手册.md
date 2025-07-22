# `播放器`模块 API 手册

## 概述

本文件详细介绍 K230_CanMV 播放器模块 API，旨在支持 MP4 格式文件的播放。该模块能够同时播放音频与视频，音频格式支持 G.711A/U，视频格式支持 H.264/H.265 编码。

## API 介绍

该模块提供了 `Player` 类，包含以下方法：

### 构造函数

**描述**

根据指定的 `display_type` 构造 `Player` 对象。用户需先创建 `Player` 对象以进行后续操作。

**语法**

```python
player = Player(Display.VIRT, [display_to_ide])
```

**参数**  

| 参数名称        | 描述                          | 输入/输出 | 说明 |
|-----------------|-------------------------------|-----------| --- |
| display_type     | 显示设备类型                 | 输入      |     |
| display_to_ide   | 是否同时输出到 IDE 虚拟屏    | 输入      |     |

**返回值**  

| 返回值        | 描述                |
|---------------|---------------------|
| Player 对象   | 创建的 Player 实例  |

**示例**  

```python
player = Player(Display.VIRT)
player = Player(Display.ST7701)
player = Player(Display.LT9611)
```

### Player.load

**描述**

加载指定文件，目前版本仅支持 MP4 格式文件。

**语法**  

```python
player = Player()
player.load("test.mp4")
```

**参数**

| 参数名称        | 描述                     | 输入/输出 |
|-----------------|--------------------------|-----------|
| filename        | 文件名称                 | 输入      |

**返回值**

| 返回值  | 描述        |
|---------|-------------|
| 0       | 成功        |
| 非 0    | 失败        |

**注意事项**  
当前版本仅支持播放 MP4 格式文件。

### Player.start

**描述**

开始播放音视频内容。

**语法**  

```python
player = Player()
player.start()
```

**参数**

无

**返回值**  

| 返回值 | 描述 |
|--------|------|
| 0      | 成功 |
| 非0    | 失败 |

### Player.pause

**描述**

暂停当前播放。

**语法**  

```python
player = Player()
player.pause()
```

**参数**

无

**返回值**  

| 返回值 | 描述 |
|--------|------|
| 0      | 成功 |
| 非0    | 失败 |

### Player.resume

**描述**

恢复播放。

**语法**  

```python
player = Player()
player.resume()
```

**参数**

无

**返回值**  

| 返回值 | 描述 |
|--------|------|
| 0      | 成功 |
| 非0    | 失败 |

### Player.stop

**描述**

停止播放。

**语法**  

```python
player = Player()
player.stop()
```

**参数**

无

**返回值**  

| 返回值 | 描述 |
|--------|------|
| 0      | 成功 |
| 非0    | 失败 |

### Player.set_event_callback

**描述**

设置播放事件的回调函数。

**参数**  

| 参数名称 | 描述            | 输入/输出 |
|----------|-----------------|-----------|
| callback | 回调函数名称    | 输入      |

**语法**  

```python
def player_event(event, data):
    pass

player = Player()
player.set_event_callback(callback=player_event)
```

**返回值**  

| 返回值 | 描述 |
|--------|------|
| 0      | 成功 |
| 非0    | 失败 |

## 数据结构描述

### play_event_type

**描述**

定义了播放事件的类型。

**成员**  

| 成员名称                      | 描述     |
|-------------------------------|----------|
| K_PLAYER_EVENT_EOF            | 播放结束 |
| K_PLAYER_EVENT_PROGRESS        | 播放进度 |

## 示例程序

### 例程 1

```python
from media.player import *
import os
import time

start_play = False

def player_event(event, data):
    global start_play
    if event == K_PLAYER_EVENT_EOF:
        start_play = False

def play_mp4_test(filename):
    global start_play
    # 使用 IDE 作为输出显示，支持任意分辨率；适用于 BPI 开发板
    player = Player(Display.VIRT)
    # 使用 ST7701 LCD 屏幕作为输出显示，最大分辨率为 800x480
    # player = Player(Display.ST7701)
    # 使用 HDMI 作为输出显示
    # player = Player(Display.LT9611)
    
    player.load(filename)
    player.set_event_callback(player_event)
    player.start()
    start_play = True

    while start_play:
        time.sleep(0.1)

    player.stop()
    print("播放结束")

play_mp4_test("/sdcard/examples/test.mp4")
```
