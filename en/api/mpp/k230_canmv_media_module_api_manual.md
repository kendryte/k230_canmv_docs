# `Media` Module API Manual

```{attention}
This module has undergone significant changes after firmware version V0.7. If you are using firmware prior to V0.7, please refer to the older version documentation.
```

## Overview

The media module of the CanMV K230 platform is a software abstraction layer, primarily used to encapsulate the media data link and media buffer-related operations of the CanMV K230 platform.

The VB buffer system of the media module is automatically initialized at system startup, and users do not need to manually call `init` / `deinit`.

## API Introduction

The media module of the CanMV K230 platform provides the `MediaManager` static class, which contains the methods described in the following sections.

### link

**Description**

This method is used to establish connections between channels of different modules, enabling automatic data flow. The `Display` module can automatically create a `link` through `bind_layer`.

**Syntax**  

```python
MediaManager.link(src=(mod, dev, chn), dst=(mod, dev, chn))
```

**Parameters**  

| Parameter Name | Description                                  | Input / Output |
|----------|---------------------------------------------|-----------|
| src      | Source channel triple `(mod_id, dev_id, chn_id)`      | Input      |
| dst      | Destination channel triple `(mod_id, dev_id, chn_id)`    | Input      |

**Return Value**  

| Return Value                | Description               |
|-----------------------|--------------------|
| `MediaManager.linker` | Link object, can be used for subsequent destruction |

**Example**  

```python
# Connect Sensor channel 0 to video encoder channel 0
link = MediaManager.link(
    src=(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0),
    dst=(VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, VENC_CHN_ID_0)
)
# Destroy the link
link.destroy()
```

> **Note**: To connect Sensor to Display, please use `Display.bind_layer()` instead of `MediaManager.link()`.

### Buffer Class

`MediaManager.Buffer` provides methods for acquiring and managing VB buffers.

#### Buffer.get

**Description**

Get a buffer of the specified size from the VB buffer pool.

**Syntax**  

```python
MediaManager.Buffer.get(size, poolid=VB_INVALID_POOLID)
```

**Parameters**  

| Parameter Name | Description                                                       | Input / Output |
|----------|------------------------------------------------------------|-----------|
| size     | Size of the buffer to request (in bytes)                                | Input      |
| poolid   | Buffer pool ID, `VB_INVALID_POOLID` indicates getting from any pool (optional)     | Input      |

**Return Value**  

| Return Value                    | Description |
|--------------------------|------|
| `MediaManager.Buffer` object | Success |

#### Buffer.alloc

**Description**

Directly allocate buffer through MMZ (not dependent on VB pool).

**Syntax**  

```python
MediaManager.Buffer.alloc(size)
```

**Parameters**  

| Parameter Name | Description                       | Input / Output |
|----------|----------------------------|-----------|
| size     | Size of the buffer to allocate (in bytes) | Input      |

**Return Value**  

| Return Value                    | Description |
|--------------------------|------|
| `MediaManager.Buffer` object | Success |

#### Buffer.destroy / Buffer.free

**Description**

Release the acquired or allocated `buffer` resource.

**Syntax**

```python
buffer.destroy()
# or
buffer.free()
```

**Parameters**

| Parameter Name | Description | Input / Output |
|----------|------|-----------|
| None       |      |           |

**Return Value**

| Return Value | Description |
|--------|------|
| `bool` | Returns `True` on success |

#### Buffer.flush_cache

**Description**

Flush the buffer's cache to ensure data consistency.

**Syntax**

```python
buffer.flush_cache()
```

**Return Value**

| Return Value | Description |
|--------|------|
| `bool` | Returns `True` on success |

#### Buffer Properties

| Property Name      | Type  | Description              |
|-------------|-------|-------------------|
| `handle`    | int   | VB block handle          |
| `pool_id`   | int   | VB pool ID it belongs to      |
| `phys_addr` | int   | Physical address           |
| `virt_addr` | int   | Virtual address           |
| `size`      | int   | Buffer size (in bytes)   |

### VBPool Class

`MediaManager.VBPool` is used to manually create and manage VB buffer pools.

#### VBPool.create

**Description**

Creates a VB buffer pool.

**Syntax**

```python
MediaManager.VBPool.create(blk_size, blk_cnt, mode=VB_REMAP_MODE_NOCACHE)
```

**Parameters**

| Parameter | Description                              | Input / Output |
|-----------|------------------------------------------|----------------|
| blk_size  | Size of each buffer block (bytes)        | Input          |
| blk_cnt   | Number of buffer blocks                  | Input          |
| mode      | Remap mode, default `VB_REMAP_MODE_NOCACHE` (optional) | Input          |

**Return Value**

| Return Value                | Description |
|-----------------------------|-------------|
| `MediaManager.VBPool` object | Success     |

#### VBPool.destroy

**Description**

Destroys the VB buffer pool and releases all associated resources.

**Syntax**

```python
pool.destroy()
```

**Return Value**

| Return Value | Description |
|--------------|-------------|
| `bool`       | Returns `True` on success |

#### VBPool Properties

| Property   | Type | Description          |
|------------|------|----------------------|
| `pool_id`  | int  | Pool ID              |
| `blk_size` | int  | Block size (bytes)   |
| `blk_cnt`  | int  | Number of blocks     |
| `mode`     | int  | Remap mode           |

### Deprecated Methods

The following methods are deprecated after firmware version V0.7. Calling them will print a deprecation notice or raise an exception:

| Method                            | Status                      |
|-----------------------------------|-----------------------------|
| `MediaManager.init()`             | Deprecated (prints notice)  |
| `MediaManager.deinit()`           | Deprecated (prints notice)  |
| `MediaManager._config()`          | Deprecated (raises exception) |
| `MediaManager.config_comm_pool()` | Deprecated (raises exception) |

## Data Structure Description

The media module of the CanMV K230 platform includes the following data definitions.

### Media Module ID

**Description**

The currently defined media module IDs of the CanMV K230 platform. Users need to set the corresponding module IDs when creating media links.

**Definition**

```python
# CanMV K230 media module definitions
AUDIO_IN_MOD_ID = K_ID_AI          # Audio input device module
AUDIO_OUT_MOD_ID = K_ID_AO         # Audio output device module
AUDIO_ENCODE_MOD_ID = K_ID_AENC    # Audio encoding device module
AUDIO_DECODE_MOD_ID = K_ID_ADEC    # Audio decoding device module
CAMERA_MOD_ID = K_ID_VI            # Camera device module
DISPLAY_MOD_ID = K_ID_VO           # Display device module
DMA_MOD_ID = K_ID_DMA              # DMA device module
DPU_MOD_ID = K_ID_DPU              # DPU device module
VIDEO_ENCODE_MOD_ID = K_ID_VENC    # Video encoding device module
VIDEO_DECODE_MOD_ID = K_ID_VDEC    # Video decoding device module
NONAI_2D_CSC_MOD_ID = K_ID_NONAI_2D  # Hardware color space conversion module
```

### Media Device ID

**Description**

The currently defined media device IDs of the CanMV K230 platform. Users need to set the corresponding device IDs when creating media links.

**Definition**

```python
# Audio device ID definitions
# TODO

# Camera device ID definitions
CAM_DEV_ID_0 = VICAP_DEV_ID_0
CAM_DEV_ID_1 = VICAP_DEV_ID_1
CAM_DEV_ID_2 = VICAP_DEV_ID_2
CAM_DEV_ID_MAX = VICAP_DEV_ID_MAX

# Display device ID definitions
DISPLAY_DEV_ID = 0

# DMA device ID definitions
# TODO

# DPU device ID definitions
# TODO

# Video encoding device ID definitions
VENC_DEV_ID = const(0)

# Video decoding device ID definitions
VDEC_DEV_ID = const(0)
```

### Media Device Channel ID

**Description**

The currently defined media device channel IDs of the CanMV K230 platform. Users need to set the corresponding device channel IDs when creating media links.

**Definition**

```python
# Audio channel ID definitions
# TODO

# Camera channel ID definitions
CAM_CHN_ID_0 = VICAP_CHN_ID_0
CAM_CHN_ID_1 = VICAP_CHN_ID_1
CAM_CHN_ID_2 = VICAP_CHN_ID_2
CAM_CHN_ID_MAX = VICAP_CHN_ID_MAX

# Video encoding channel ID definitions
VENC_CHN_ID_0 = const(0)
VENC_CHN_ID_1 = const(1)
VENC_CHN_ID_2 = const(2)
VENC_CHN_ID_3 = const(3)
VENC_CHN_ID_MAX = VENC_MAX_CHN_NUMS

# Video decoding channel ID definitions
VDEC_CHN_ID_0 = const(0)
VDEC_CHN_ID_1 = const(1)
VDEC_CHN_ID_2 = const(2)
VDEC_CHN_ID_3 = const(3)
VDEC_CHN_ID_MAX = VDEC_MAX_CHN_NUMS
```

### General Constants

| Constant Name             | Value         | Description                              |
|--------------------------|---------------|------------------------------------------|
| `MAX_MEDIA_BUFFER_POOLS` | `16`          | Maximum number of media buffer pools      |
| `MAX_MEDIA_LINK_COUNT`   | `8`           | Maximum number of media links             |
| `VENC_PACK_CNT_MAX`      | `const(12)`   | Maximum packets per frame for video encoding |
| `VB_INVALID_POOLID`      | `0xFFFFFFFF`  | Invalid VB pool ID                       |
| `VB_INVALID_HANDLE`      | `0xFFFFFFFF`  | Invalid VB block handle                  |
| `ALIGN_UP`               | (function)    | Address/size alignment utility function  |

## Example Programs

### Example 1: Using VBPool and Buffer

```python
from media.media import *

# Create VB buffer pool
pool = MediaManager.VBPool.create(blk_size=4096, blk_cnt=4, mode=VB_REMAP_MODE_NOCACHE)

# Get buffer from the specified pool
buffer = MediaManager.Buffer.get(1024, poolid=pool.pool_id)
print(buffer)

# View buffer properties
print(f"phys_addr: 0x{buffer.phys_addr:x}, size: {buffer.size}")

# Release buffer
buffer.destroy()

# Destroy buffer pool
pool.destroy()
```

### Example 2: Using Buffer.alloc for Direct Allocation

```python
from media.media import *

# Directly allocate buffer via MMZ
buffer = MediaManager.Buffer.alloc(4096)
print(buffer)

# Flush cache
buffer.flush_cache()

# Release
buffer.free()
```
