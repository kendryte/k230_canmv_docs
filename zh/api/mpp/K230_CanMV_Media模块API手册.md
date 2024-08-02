# 3.4 Media模块API手册

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

本文档主要介绍K230 CanMV平台media模块 API使用说明及应用示例。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
|   |    |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 汪成根    | 2023-09-25 |
| V2.0       | 重构API         | xel           | 2024-06-11 |

```{attention}
该模块在固件版本V0.7之后有较大改变，若使用V0.7之前固件请参考旧版本的文档
```

## 1. 概述

​        K230 CanMV平台media模块是一个软件抽象模块，主要是针对K230 CanMV平台媒体数据链路以及媒体缓冲区相关操作的封装。

## 2. API描述

K230 CanMV平台media模块提供MediaManager静态类，该类提供以下章节描述的方法。

### 2.1 init

【描述】

用户[配置](#23-_config)完`buffer`之后，调用`init`进行初始化，必须在最后进行调用

【语法】

```python
MediaManager.init()
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| 无 | | |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 无 | |

【注意】

【举例】

无

【相关主题】

无

### 2.2 deinit

【描述】

销毁所有申请的`buffer`

【语法】

```python
MediaManager.deinit()
```

【参数】

| 参数名称 | 描述           | 输入/输出 |
| -------- | -------------- | --------- |
| 无 | | |

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| 无 | |

【注意】

【举例】

无

【相关主题】

无

### 2.3 _config

【描述】

配置媒体缓冲区

【语法】

```python
MediaManager._config(config)
```

【参数】

| 参数名称 | 描述               | 输入/输出 |
| -------- | ------------------ | --------- |
| config   | 媒体缓冲区配置参数 | 输入      |

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| 0      | 成功。                 |
| 非 0   | 失败，其值为\[错误码\] |

【注意】
该方法仅提供给K230 CanMV平台各媒体子模块（例如：camera，video encode等）封装本模块接口时内部使用。上层应用开发者无需关注！

【举例】

无

【相关主题】

无

### 2.4 link

【描述】

为不同模块的通道建立连接，数据自动流转，无需用户手动操作

`Display`可使用`bind_layer`自动创建`link`

【语法】

```python
MediaManager.link(src=(mod,dev,chn), dst = (mod,dev,chn))
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| 无 | | |

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| `MediaManager.linker`类 | |

【注意】
该方法仅提供给K230 CanMV平台各媒体子模块（例如：camera，video encode等）封装本模块接口时内部使用。上层应用开发者无需关注！

【举例】

无

【相关主题】

无

### 2.5 Buffer 管理

#### 2.5.1 get

【描述】

用户在[_config](#23-_config)之后，可通过`MediaManager.Buffer.get`获取`buffer`

**必须在[init](#21-init)执行之后才能获取**

【语法】

```python
MediaManager.Buffer.get(size)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| size | 想要获取的`buffer`大小，不能超过`_config`中配置的 | 输入 |

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| `MediaManager.Buffer` 类 | 成功 |

【举例】

无

【相关主题】

无

#### 2.5.2 释放内存

【描述】

用户手动释放获取到的`buffer`

【语法】

```python
buffer.__del__()
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| 无 | | |

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| 无 | |

【举例】

无

【相关主题】

无

## 3. 数据结构描述

K230 CanMV平台Meida模块包含如下描述的各个数据定义。

### 3.1 媒体模块ID

【说明】

K230 CanMV平台当前定义的各个媒体模块ID，用户创建媒体链路时需要设置对应的模块ID。

【定义】

```python
# K230 CanMV meida module define
AUDIO_IN_MOD_ID = K_ID_AI          # audio in device module
AUDIO_OUT_MOD_ID = K_ID_AO         # audio out device module
AUDIO_ENCODE_MOD_ID = K_ID_AENC    # audio encode device module
AUDIO_DECODE_MOD_ID = K_ID_ADEC    # audio decode device module
CAMERA_MOD_ID = K_ID_VI            # camera cdevice module
DISPLAY_MOD_ID = K_ID_VO           # display device module
DMA_MOD_ID = K_ID_DMA              # DMA device module
DPU_MOD_ID = K_ID_DPU              # DPU device module
VIDEO_ENCODE_MOD_ID = K_ID_VENC    # video encode device module
VIDEO_DECODE_MOD_ID = K_ID_VDEC    # video decode device module

```

【注意事项】

无

【相关数据类型及接口】

### 3.2 媒体设备ID

【说明】

K230 CanMV平台当前定义的各个媒体设备ID，用户创建媒体链路时需要设置对应的设备ID。

【定义】

```python
# audio device id definition
# TODO

# camera device id definition
CAM_DEV_ID_0 = VICAP_DEV_ID_0
CAM_DEV_ID_1 = VICAP_DEV_ID_1
CAM_DEV_ID_2 = VICAP_DEV_ID_2
CAM_DEV_ID_MAX = VICAP_DEV_ID_MAX

# display device id definition
DISPLAY_DEV_ID = K_VO_DISPLAY_DEV_ID

# DMA device id definition
# TODO

# DPU device id definition
# TODO

# video encode device id definition
# TODO

# video decode device id definition
# TODO
```

【注意事项】

无

【相关数据类型及接口】

### 3.3 媒体设备通道ID

【说明】

K230 CanMV平台当前定义的各个媒体设备通道ID，用户创建媒体链路时需要设置对应的设备通道ID。

【定义】

```python
# audio channel id definition
# TODO

# camera channel id definition
CAM_CHN_ID_0 = VICAP_CHN_ID_0
CAM_CHN_ID_1 = VICAP_CHN_ID_1
CAM_CHN_ID_2 = VICAP_CHN_ID_2
CAM_CHN_ID_MAX = VICAP_CHN_ID_MAX

# display channel id definition
DISPLAY_CHN_ID_0 = K_VO_DISPLAY_CHN_ID0
DISPLAY_CHN_ID_1 = K_VO_DISPLAY_CHN_ID1
DISPLAY_CHN_ID_2 = K_VO_DISPLAY_CHN_ID2
DISPLAY_CHN_ID_3 = K_VO_DISPLAY_CHN_ID3
DISPLAY_CHN_ID_4 = K_VO_DISPLAY_CHN_ID4
DISPLAY_CHN_ID_5 = K_VO_DISPLAY_CHN_ID5
DISPLAY_CHN_ID_6 = K_VO_DISPLAY_CHN_ID6

# DMA channel id definition
# TODO

# DPU channel id definition
# TODO

# video encode channel id definition
# TODO

# video decode channel id definition
# TODO

```

【注意事项】

无

【相关数据类型及接口】

无

## 4. 示例程序

### 例程

```python
from media.media import *

config = k_vb_config()
config.max_pool_cnt = 1
config.comm_pool[0].blk_size = 1024
config.comm_pool[0].blk_cnt = 1
config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

ret = MediaManager._config(config)
if not ret:
    raise RuntimeError(f"configure buffer failed.")

MediaManager.init()

buffer = MediaManager.Buffer.get(1024)

print(buffer)

buffer.__del__()

MediaManager.deinit()

'''
buffer pool :  1
MediaManager.Buffer: handle 0, size 1024, poolId 0, phyAddr 268439552, virtAddr 100424000
'''
```
