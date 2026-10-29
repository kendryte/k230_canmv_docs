# `Player` Module API Manual

## Overview

This document provides a detailed introduction to the K230_CanMV Player module API, designed to support playback of MP4 format files. This module can simultaneously play audio and video, with audio format supporting G.711A/U and video format supporting H.264/H.265 encoding.

## API Introduction

This module provides the `Player` class, which includes the following methods:

### Constructor

**Description**

Constructs a `Player` object based on the specified `display_type`. Users need to first create a `Player` object for subsequent operations.

**Syntax**

```python
player = Player(display_type = Display.VIRT,display_to_ide = True)
```

**Parameters**  

| Parameter Name   | Description                       | Input/Output | Notes |
|------------------|-----------------------------------|--------------| --- |
| display_type     | Display device type               | Input        |     |
| display_to_ide   | Whether to also output to IDE virtual screen | Input        |     |

**Return Value**  

| Return Value     | Description           |
|------------------|-----------------------|
| Player Object    | The created Player instance |

**Example**  

```python
player = Player(Display.VIRT)
player = Player(Display.ST7701)
player = Player(Display.LT9611)
```

### Player.load

**Description**

Loads the specified file. The current version only supports MP4 format files.

**Syntax**  

```python
player = Player()
Player.load(filename = "test.mp4")
```

**Parameters**

| Parameter Name   | Description            | Input/Output |
|------------------|------------------------|--------------|
| filename         | File name              | Input        |

**Return Value**

| Return Value | Description |
|--------------|-------------|
| None         |             |

**Notes**  

The current version only supports playback of MP4 format files.

### Player.start

**Description**

Starts playing audio and video content.

**Syntax**  

```python
player = Player()
player.start()
```

**Parameters**

None

**Return Value**  

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Player.pause

**Description**

Pauses the current playback.

**Syntax**  

```python
player = Player()
player.pause()
```

**Parameters**

None

**Return Value**  

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Player.resume

**Description**

Resumes playback.

**Syntax**  

```python
player = Player()
player.resume()
```

**Parameters**

None

**Return Value**  

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Player.stop

**Description**

Stops playback.

**Syntax**  

```python
player = Player()
player.stop()
```

**Parameters**

None

**Return Value**  

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Player.destroy_mp4

**Description**

Destroys the mp4 player

**Syntax**  

```python
Player.destroy_mp4()
```

**Parameters**

None

**Return Value**  

| Return Value | Description |
|--------------|-------------|
| None         |             |

### Player.set_event_callback

**Description**

Sets the callback function for playback events.

**Syntax**  

```python
def player_event(event, data):
    pass

player = Player()
player.set_event_callback(callback=player_event)
```

**Parameters**  

| Parameter Name | Description            | Input/Output |
|----------------|------------------------|--------------|
| callback       | Callback function name | Input        |

**Return Value**  

| Return Value | Description |
|--------------|-------------|
| None         |             |

## Data Structure Description

### play_event_type

**Description**

Defines the type of playback event.

**Members**  

| Member Name                    | Description          |
|--------------------------------|----------------------|
| K_PLAYER_EVENT_EOF             | Playback ended       |
| K_PLAYER_EVENT_PROGRESS        | Playback progress    |

## Example Programs

### Example 1

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
