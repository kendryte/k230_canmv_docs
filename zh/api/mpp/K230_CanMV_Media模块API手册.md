# 3.4 `媒体`模块 API 手册`

```{attention}
该模块在固件版本 V0.7 之后发生了较大变化，若使用 V0.7 之前的固件，请参考旧版本文档。
```

## 1. 概述

CanMV K230 平台的媒体模块是一个软件抽象层，主要用于封装 CanMV K230 平台的媒体数据链路及媒体缓冲区相关操作。

## 2. API 介绍

CanMV K230 平台的媒体模块提供了 MediaManager 静态类，该类包含以下章节所描述的方法。

### 2.1 init

**描述**
在用户完成 `buffer` 的 [配置](#23-_config) 后，调用 `init` 方法进行初始化。该方法必须在最后执行。

**语法**  

```python
MediaManager.init()
```

**参数**  

| 参数名称 | 描述 | 输入 / 输出 |
|----------|------|-----------|
| 无       |      |           |

**返回值**  

| 返回值 | 描述 |
|--------|------|
| 无     |      |

### 2.2 deinit

**描述**
该方法用于销毁所有申请的 `buffer`。

**语法**  

```python
MediaManager.deinit()
```

**参数**  

| 参数名称 | 描述 | 输入 / 输出 |
|----------|------|-----------|
| 无       |      |           |

**返回值**  

| 返回值 | 描述 |
|--------|------|
| 无     |      |

### 2.3 _config

**描述**
用于配置媒体缓冲区。

**语法**  

```python
MediaManager._config(config)
```

**参数**  

| 参数名称 | 描述               | 输入 / 输出 |
|----------|-------------------|-----------|
| config   | 媒体缓冲区配置参数 | 输入      |

**返回值**  

| 返回值 | 描述                   |
|--------|------------------------|
| 0      | 成功                   |
| 非 0   | 失败，其值为 [ 错误码 ] |

**注意事项**  

此方法仅供 CanMV K230 平台的各媒体子模块（例如：相机、视频编码等）在封装本模块接口时内部使用，上层应用开发者无需关注。

### 2.4 link

**描述**
该方法用于为不同模块的通道建立连接，实现数据自动流转，用户无需手动操作。`Display` 模块可以通过 `bind_layer` 自动创建 `link`。

**语法**  

```python
MediaManager.link(src=(mod,dev,chn), dst=(mod,dev,chn))
```

**参数**  

| 参数名称 | 描述 | 输入 / 输出 |
|----------|------|-----------|
| 无       |      |           |

**返回值**  

| 返回值                | 描述 |
|-----------------------|------|
| `MediaManager.linker` |      |

**注意事项**  

此方法仅供 CanMV K230 平台的各媒体子模块（例如：相机、视频编码等）在封装本模块接口时内部使用，上层应用开发者无需关注。

### 2.5 缓冲区管理

#### 2.5.1 get

**描述**
在 [_config](#23-_config) 完成后，用户可以通过 `MediaManager.Buffer.get` 方法获取 `buffer`。#### 必须在[init](#21-init)执行之后才能调用该方法  。

**语法**  

```python
MediaManager.Buffer.get(size)
```

**参数**  

| 参数名称 | 描述                          | 输入 / 输出 |
|----------|-------------------------------|-----------|
| size     | 请求获取的 `buffer` 大小，不能超过 `_config` 中配置的大小 | 输入      |

**返回值**  

| 返回值                    | 描述   |
|--------------------------|--------|
| `MediaManager.Buffer` 类 | 成功   |

#### 2.5.2 释放内存

**描述**

用户可以手动释放已获取的 `buffer`。

**语法**

```python
buffer.__del__()
```

**参数**

| 参数名称 | 描述 | 输入 / 输出 |
|----------|------|-----------|
| 无       |      |           |

**返回值**

| 返回值 | 描述 |
|--------|------|
| 无     |      |

## 3. 数据结构描述

CanMV K230 平台的媒体模块包含以下各个数据定义。

### 3.1 媒体模块 ID

**说明**  

CanMV K230 平台当前定义的各个媒体模块 ID，用户在创建媒体链路时需要设置对应的模块 ID。

**定义**  

```python
# CanMV K230 媒体模块定义
AUDIO_IN_MOD_ID = K_ID_AI          # 音频输入设备模块
AUDIO_OUT_MOD_ID = K_ID_AO         # 音频输出设备模块
AUDIO_ENCODE_MOD_ID = K_ID_AENC    # 音频编码设备模块
AUDIO_DECODE_MOD_ID = K_ID_ADEC    # 音频解码设备模块
CAMERA_MOD_ID = K_ID_VI            # 摄像头设备模块
DISPLAY_MOD_ID = K_ID_VO           # 显示设备模块
DMA_MOD_ID = K_ID_DMA              # DMA 设备模块
DPU_MOD_ID = K_ID_DPU              # DPU 设备模块
VIDEO_ENCODE_MOD_ID = K_ID_VENC    # 视频编码设备模块
VIDEO_DECODE_MOD_ID = K_ID_VDEC    # 视频解码设备模块
```

#### 相关数据类型及接口  

### 3.2 媒体设备 ID

**说明**  

CanMV K230 平台当前定义的各个媒体设备 ID，用户在创建媒体链路时需要设置对应的设备 ID。

**定义**  

```python
# 音频设备 ID 定义
# TODO

# 摄像头设备 ID 定义
CAM_DEV_ID_0 = VICAP_DEV_ID_0
CAM_DEV_ID_1 = VICAP_DEV_ID_1
CAM_DEV_ID_2 = VICAP_DEV_ID_2
CAM_DEV_ID_MAX = VICAP_DEV_ID_MAX

# 显示设备 ID 定义
DISPLAY_DEV_ID = K_VO_DISPLAY_DEV_ID

# DMA 设备 ID 定义
# TODO

# DPU 设备 ID 定义
# TODO

# 视频编码设备 ID 定义
# TODO

# 视频解码设备 ID 定义
# TODO
```

### 3.3 媒体设备通道 ID

**说明**  

CanMV K230 平台当前定义的各个媒体设备通道 ID，用户在创建媒体链路时需要设置对应的设备通道 ID。

**定义**  

```python
# 音频通道 ID 定义
# TODO

# 摄像头通道 ID 定义
CAM_CHN_ID_0 = VICAP_CHN_ID_0
CAM_CHN_ID_1 = VICAP_CHN_ID_1
CAM_CHN_ID_2 = VICAP_CHN_ID_2
CAM_CHN_ID_MAX = VICAP_CHN_ID_MAX

# 显示通道 ID 定义
DISPLAY_CHN_ID_0 = K_VO_DISPLAY_CHN_ID0
DISPLAY_CHN_ID_1 = K_VO_DISPLAY_CHN_ID1
DISPLAY_CHN_ID_2 = K_VO_DISPLAY_CHN_ID2
DISPLAY_CHN_ID_3 = K_VO_DISPLAY_CHN_ID3
DISPLAY_CHN_ID_4 = K_VO_DISPLAY_CHN_ID4
DISPLAY_CHN_ID_5 = K_VO_DISPLAY_CHN_ID5
DISPLAY_CHN_ID_6 = K_VO_DISPLAY_CHN_ID6

# DMA 通道 ID 定义
# TODO

# DPU 通道 ID 定义
# TODO

# 视频编码通道 ID 定义
# TODO

# 视频解码通道 ID 定义
# TODO
```

#### 相关数据类型及接口  

无

## 4. 示例程序

**示例**

```python
from media.media import *

config = k_vb_config()
config.max_pool_cnt = 1
config.comm_pool[0].blk_size = 1024
config.comm_pool[0].blk_cnt = 1
config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

ret = MediaManager._config(config)
if not ret:
    raise RuntimeError(" 缓冲区配置失败。")

MediaManager.init()

buffer = MediaManager.Buffer.get(1024)

print(buffer)

buffer.__del__()

MediaManager.deinit()

```
