# `媒体`模块 API 手册`

```{attention}
该模块在固件版本 V0.7 之后发生了较大变化，若使用 V0.7 之前的固件，请参考旧版本文档。
```

## 概述

CanMV K230 平台的媒体模块是一个软件抽象层，主要用于封装 CanMV K230 平台的媒体数据链路及媒体缓冲区相关操作。

媒体模块的 VB 缓冲系统在系统启动时自动初始化，用户无需手动调用 `init` / `deinit`。

## API 介绍

CanMV K230 平台的媒体模块提供了 `MediaManager` 静态类，该类包含以下章节所描述的方法。

### link

**描述**

该方法用于为不同模块的通道建立连接，实现数据自动流转。`Display` 模块可以通过 `bind_layer` 自动创建 `link`。

**语法**  

```python
MediaManager.link(src=(mod, dev, chn), dst=(mod, dev, chn))
```

**参数**  

| 参数名称 | 描述                                        | 输入 / 输出 |
|----------|---------------------------------------------|-----------|
| src      | 源通道三元组 `(mod_id, dev_id, chn_id)`      | 输入      |
| dst      | 目标通道三元组 `(mod_id, dev_id, chn_id)`    | 输入      |

**返回值**  

| 返回值                | 描述               |
|-----------------------|--------------------|
| `MediaManager.linker` | 链路对象，可用于后续销毁 |

**示例**  

```python
# 将 Sensor 通道 0 连接到视频编码器通道 0
link = MediaManager.link(
    src=(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0),
    dst=(VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, VENC_CHN_ID_0)
)
# 销毁链路
link.destroy()
```

> **注意**：连接 Sensor 到 Display 请使用 `Display.bind_layer()` 而非 `MediaManager.link()`。

### Buffer 类

`MediaManager.Buffer` 提供 VB 缓冲区的获取与管理方法。

#### Buffer.get

**描述**

从 VB 缓冲池中获取指定大小的缓冲区。

**语法**  

```python
MediaManager.Buffer.get(size, poolid=VB_INVALID_POOLID)
```

**参数**  

| 参数名称 | 描述                                                       | 输入 / 输出 |
|----------|------------------------------------------------------------|-----------|
| size     | 请求获取的 buffer 大小（字节）                                | 输入      |
| poolid   | 缓冲池 ID，`VB_INVALID_POOLID` 表示从任意池中获取（可选）     | 输入      |

**返回值**  

| 返回值                    | 描述 |
|--------------------------|------|
| `MediaManager.Buffer` 对象 | 成功 |

#### Buffer.alloc

**描述**

通过 MMZ 直接分配缓冲区（不依赖 VB 池）。

**语法**  

```python
MediaManager.Buffer.alloc(size)
```

**参数**  

| 参数名称 | 描述                       | 输入 / 输出 |
|----------|----------------------------|-----------|
| size     | 请求分配的 buffer 大小（字节） | 输入      |

**返回值**  

| 返回值                    | 描述 |
|--------------------------|------|
| `MediaManager.Buffer` 对象 | 成功 |

#### Buffer.destroy / Buffer.free

**描述**

释放已获取或已分配的 `buffer` 资源。

**语法**

```python
buffer.destroy()
# 或
buffer.free()
```

**参数**

| 参数名称 | 描述 | 输入 / 输出 |
|----------|------|-----------|
| 无       |      |           |

**返回值**

| 返回值 | 描述 |
|--------|------|
| `bool` | 成功返回 `True` |

#### Buffer.flush_cache

**描述**

刷新 buffer 的 cache，确保数据一致性。

**语法**

```python
buffer.flush_cache()
```

**返回值**

| 返回值 | 描述 |
|--------|------|
| `bool` | 成功返回 `True` |

#### Buffer 属性

| 属性名      | 类型  | 描述              |
|-------------|-------|-------------------|
| `handle`    | int   | VB 块句柄          |
| `pool_id`   | int   | 所属 VB 池 ID      |
| `phys_addr` | int   | 物理地址           |
| `virt_addr` | int   | 虚拟地址           |
| `size`      | int   | 缓冲区大小（字节）   |

### VBPool 类

`MediaManager.VBPool` 用于手动创建和管理 VB 缓冲池。

#### VBPool.create

**描述**

创建一个 VB 缓冲池。

**语法**

```python
MediaManager.VBPool.create(blk_size, blk_cnt, mode=VB_REMAP_MODE_NOCACHE)
```

**参数**

| 参数名称  | 描述                                    | 输入 / 输出 |
|-----------|-----------------------------------------|-----------|
| blk_size  | 每个缓冲块的大小（字节）                  | 输入      |
| blk_cnt   | 缓冲块数量                               | 输入      |
| mode      | 重映射模式，默认 `VB_REMAP_MODE_NOCACHE`（可选） | 输入      |

**返回值**

| 返回值                  | 描述 |
|-------------------------|------|
| `MediaManager.VBPool` 对象 | 成功 |

#### VBPool.destroy

**描述**

销毁 VB 缓冲池并释放所有关联资源。

**语法**

```python
pool.destroy()
```

**返回值**

| 返回值 | 描述 |
|--------|------|
| `bool` | 成功返回 `True` |

#### VBPool 属性

| 属性名     | 类型  | 描述            |
|------------|-------|-----------------|
| `pool_id`  | int   | 池 ID           |
| `blk_size` | int   | 块大小（字节）   |
| `blk_cnt`  | int   | 块数量          |
| `mode`     | int   | 重映射模式       |

### 已废弃的方法

以下方法在固件版本 V0.7 之后已废弃，调用会打印弃用提示或抛出异常：

| 方法                         | 状态              |
|------------------------------|-------------------|
| `MediaManager.init()`        | 废弃（打印提示）    |
| `MediaManager.deinit()`      | 废弃（打印提示）    |
| `MediaManager._config()`     | 废弃（抛出异常）    |
| `MediaManager.config_comm_pool()` | 废弃（抛出异常） |

## 数据结构描述

CanMV K230 平台的媒体模块包含以下各个数据定义。

### 媒体模块 ID

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
NONAI_2D_CSC_MOD_ID = K_ID_NONAI_2D  # 硬件色彩空间转换模块
```

### 媒体设备 ID

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
DISPLAY_DEV_ID = 0

# DMA 设备 ID 定义
# TODO

# DPU 设备 ID 定义
# TODO

# 视频编码设备 ID 定义
VENC_DEV_ID = const(0)

# 视频解码设备 ID 定义
VDEC_DEV_ID = const(0)
```

### 媒体设备通道 ID

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

# 视频编码通道 ID 定义
VENC_CHN_ID_0 = const(0)
VENC_CHN_ID_1 = const(1)
VENC_CHN_ID_2 = const(2)
VENC_CHN_ID_3 = const(3)
VENC_CHN_ID_MAX = VENC_MAX_CHN_NUMS

# 视频解码通道 ID 定义
VDEC_CHN_ID_0 = const(0)
VDEC_CHN_ID_1 = const(1)
VDEC_CHN_ID_2 = const(2)
VDEC_CHN_ID_3 = const(3)
VDEC_CHN_ID_MAX = VDEC_MAX_CHN_NUMS
```

### 通用常量

| 常量名称               | 值            | 说明                              |
|------------------------|---------------|-----------------------------------|
| `MAX_MEDIA_BUFFER_POOLS` | `16`        | 最大媒体缓冲池数量                  |
| `MAX_MEDIA_LINK_COUNT`   | `8`         | 最大媒体链路数量                    |
| `VENC_PACK_CNT_MAX`      | `const(12)` | 视频编码单帧最大包数                |
| `VB_INVALID_POOLID`      | `0xFFFFFFFF` | 无效 VB 池 ID                     |
| `VB_INVALID_HANDLE`      | `0xFFFFFFFF` | 无效 VB 块句柄                     |
| `ALIGN_UP`               | (函数)       | 地址/尺寸对齐工具函数               |

## 示例程序

### 示例1：使用 VBPool 和 Buffer

```python
from media.media import *

# 创建 VB 缓冲池
pool = MediaManager.VBPool.create(blk_size=4096, blk_cnt=4, mode=VB_REMAP_MODE_NOCACHE)

# 从指定池中获取 buffer
buffer = MediaManager.Buffer.get(1024, poolid=pool.pool_id)
print(buffer)

# 查看 buffer 属性
print(f"phys_addr: 0x{buffer.phys_addr:x}, size: {buffer.size}")

# 释放 buffer
buffer.destroy()

# 销毁缓冲池
pool.destroy()
```

### 示例2：使用 Buffer.alloc 直接分配

```python
from media.media import *

# 直接通过 MMZ 分配缓冲区
buffer = MediaManager.Buffer.alloc(4096)
print(buffer)

# 刷新缓存
buffer.flush_cache()

# 释放
buffer.free()
```
