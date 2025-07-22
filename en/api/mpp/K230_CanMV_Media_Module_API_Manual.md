# `Media` Module API Manual

```{attention}
This module has undergone significant changes since firmware version V0.7. If you are using firmware before V0.7, please refer to the old version documentation.
```

## Overview

The media module of the CanMV K230 platform is a software abstraction layer mainly used to encapsulate the media data link and media buffer operations of the CanMV K230 platform.

## API Introduction

The media module of the CanMV K230 platform provides a static class MediaManager, which contains the methods described in the following sections.

### init

**Description**
After the user completes the [configuration](#_config) of the `buffer`, call the `init` method to initialize. This method must be executed last.

**Syntax**

```python
MediaManager.init()
```

**Parameters**

| Parameter Name | Description | Input / Output |
|----------------|-------------|----------------|
| None           |             |                |

**Return Values**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### deinit

**Description**
This method is used to destroy all requested `buffers`.

**Syntax**

```python
MediaManager.deinit()
```

**Parameters**

| Parameter Name | Description | Input / Output |
|----------------|-------------|----------------|
| None           |             |                |

**Return Values**

| Return Value | Description |
|--------------|-------------|
| None         |             |

### _config

**Description**
Used to configure the media buffer.

**Syntax**

```python
MediaManager._config(config)
```

**Parameters**

| Parameter Name | Description             | Input / Output |
|----------------|-------------------------|----------------|
| config         | Media buffer config parameters | Input         |

**Return Values**

| Return Value | Description |
|--------------|-------------|
| 0            | Success     |
| Non-zero     | Failure, the value is [error code] |

**Notes**

This method is only for internal use when encapsulating this module interface by various media submodules (e.g., camera, video encoding, etc.) of the CanMV K230 platform. Upper-layer application developers do not need to pay attention to it.

### link

**Description**
This method is used to establish connections between channels of different modules to achieve automatic data flow, without manual operation by the user. The `Display` module can automatically create a `link` through `bind_layer`.

**Syntax**

```python
MediaManager.link(src=(mod,dev,chn), dst=(mod,dev,chn))
```

**Parameters**

| Parameter Name | Description | Input / Output |
|----------------|-------------|----------------|
| None           |             |                |

**Return Values**

| Return Value          | Description |
|-----------------------|-------------|
| `MediaManager.linker` |             |

**Notes**

This method is only for internal use when encapsulating this module interface by various media submodules (e.g., camera, video encoding, etc.) of the CanMV K230 platform. Upper-layer application developers do not need to pay attention to it.

### Buffer Management

#### get

**Description**
After [_config](#_config) is completed, the user can obtain the `buffer` through the `MediaManager.Buffer.get` method. This method must be called after [init](#init) is executed.

**Syntax**

```python
MediaManager.Buffer.get(size)
```

**Parameters**

| Parameter Name | Description                          | Input / Output |
|----------------|--------------------------------------|----------------|
| size           | Requested `buffer` size, not exceeding the size configured in `_config` | Input         |

**Return Values**

| Return Value              | Description |
|---------------------------|-------------|
| `MediaManager.Buffer` class | Success     |

#### Release Memory

**Description**

The user can manually release the obtained `buffer`.

**Syntax**

```python
buffer.__del__()
```

**Parameters**

| Parameter Name | Description | Input / Output |
|----------------|-------------|----------------|
| None           |             |                |

**Return Values**

| Return Value | Description |
|--------------|-------------|
| None         |             |

## Data Structure Description

The media module of the CanMV K230 platform includes the following data definitions.

### Media Module ID

**Description**

The currently defined media module IDs of the CanMV K230 platform. Users need to set the corresponding module ID when creating media links.

**Definition**

```python
# CanMV K230 Media Module Definitions
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
```

#### Related Data Types and Interfaces

### Media Device ID

**Description**

The currently defined media device IDs of the CanMV K230 platform. Users need to set the corresponding device ID when creating media links.

**Definition**

```python
# Audio Device ID Definitions
# TODO

# Camera Device ID Definitions
CAM_DEV_ID_0 = VICAP_DEV_ID_0
CAM_DEV_ID_1 = VICAP_DEV_ID_1
CAM_DEV_ID_2 = VICAP_DEV_ID_2
CAM_DEV_ID_MAX = VICAP_DEV_ID_MAX

# Display Device ID Definitions
DISPLAY_DEV_ID = K_VO_DISPLAY_DEV_ID

# DMA Device ID Definitions
# TODO

# DPU Device ID Definitions
# TODO

# Video Encoding Device ID Definitions
# TODO

# Video Decoding Device ID Definitions
# TODO
```

### Media Device Channel ID

**Description**

The currently defined media device channel IDs of the CanMV K230 platform. Users need to set the corresponding device channel ID when creating media links.

**Definition**

```python
# Audio Channel ID Definitions
# TODO

# Camera Channel ID Definitions
CAM_CHN_ID_0 = VICAP_CHN_ID_0
CAM_CHN_ID_1 = VICAP_CHN_ID_1
CAM_CHN_ID_2 = VICAP_CHN_ID_2
CAM_CHN_ID_MAX = VICAP_CHN_ID_MAX

# Display Channel ID Definitions
DISPLAY_CHN_ID_0 = K_VO_DISPLAY_CHN_ID0
DISPLAY_CHN_ID_1 = K_VO_DISPLAY_CHN_ID1
DISPLAY_CHN_ID_2 = K_VO_DISPLAY_CHN_ID2
DISPLAY_CHN_ID_3 = K_VO_DISPLAY_CHN_ID3
DISPLAY_CHN_ID_4 = K_VO_DISPLAY_CHN_ID4
DISPLAY_CHN_ID_5 = K_VO_DISPLAY_CHN_ID5
DISPLAY_CHN_ID_6 = K_VO_DISPLAY_CHN_ID6

# DMA Channel ID Definitions
# TODO

# DPU Channel ID Definitions
# TODO

# Video Encoding Channel ID Definitions
# TODO

# Video Decoding Channel ID Definitions
# TODO
```

#### Related Data Types and Interfaces

None

## Example Program

**Example**

```python
from media.media import *

config = k_vb_config()
config.max_pool_cnt = 1
config.comm_pool[0].blk_size = 1024
config.comm_pool[0].blk_cnt = 1
config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE

ret = MediaManager._config(config)
if not ret:
    raise RuntimeError("Buffer configuration failed.")

MediaManager.init()

buffer = MediaManager.Buffer.get(1024)

print(buffer)

buffer.__del__()

MediaManager.deinit()
```
