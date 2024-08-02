# 3.8 播放器 模块API手册

![cover](../images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍K230_CanMV 播放器模块API的使用。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 孙小朋      | 2023-10-27 |

## 1. 概述

此文档介绍K230_CanMV 播放器模块API，可播放mp4格式文件。支持音视频同时播放，音频支持g711a/u，视频支持H264/H265。

## 2. API描述

提供Player类，该类提供如下方法：

### 2.1 Player.load

【描述】

加载文件，当前版本只支持mp4格式文件

【语法】

```python
player=Player()
player.load("test.mp4")
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| filename  | 文件名称            | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

当前版本只支持播放mp4格式文件

【举例】

无

【相关主题】

无

### 2.2 Player.start

【描述】

开始播放

【语法】

```python
player=Player()
player.start()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.3 Player.pause

【描述】

暂停播放

【语法】

```python
player=Player()
player.pause()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|-----|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.4 Player.resume

【描述】

继续播放

【语法】

```python
player=Player()
player.resume()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.5 Player.stop

【描述】

停止播放

【语法】

```python
player=Player()
player.stop()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.6 Player.set_event_callback

【描述】

设置播放事件回调函数

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| callback  | 回调函数名            | 输入      |

【语法】

```python

def player_event(event,data):
    pass

player=Player()
player.set_event_callback(callback=player_event)
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

## 3. 数据结构描述

### 3.1 playe_event_type

【描述】

编码格式类型

【成员】

| 成员名称 | 描述 |
|---------|------|
| K_PLAYER_EVENT_EOF | 播放结束 |
| K_PLAYER_EVENT_PROGRESS| 播放进度 |

## 4. 示例程序

### 4.1 例程1

```python
from media.player import *
import os

start_play = False
def player_event(event,data):
    global start_play
    if(event == K_PLAYER_EVENT_EOF):
        start_play = False

def play_mp4_test(filename):
    global start_play
    player=Player()
    player.load(filename)
    player.set_event_callback(player_event)
    player.start()
    start_play = True

    while(start_play):
        time.sleep(0.1)

    player.stop()
    print("play over")

play_mp4_test("/sdcard/app/tests/test.mp4")
```
