# 3.1 Sensor 模块API手册

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

本文档主要介绍K230 CanMV平台Sensor模块 API使用说明及应用示例。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称               | 说明                                                   |
|--------------------|--------------------------------------------------------|
|||

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 赵忠祥    | 2024-04-24 |
| V2.0       | 重构API     | xel    | 2024-06-11 |

```{attention}
该模块在固件版本V0.7之后有较大改变，若使用V0.7之前固件请参考旧版本的文档
```

## 1. 概述

K230 CanMV平台sensor模块负责图像采集处理任务。本模块提供了一系列Highe Levl的API，应用开发者可以不用关注底层硬件细节，仅通过该模块提供的API即可获取不同格式和尺寸的图像。

K230 CanMV平台sensor模块包括三个独立的能力完全相同的sensor设备，每个sensor设备均可独立完成图像数据采集捕获处理，并可以同时输出3路图像数据。如下图所示：

![cover](../images/k230-canmv-camera-top.png)

sensor 0，sensor 1，sensor 2表示三个图像传感器；Camera Device 0，Camera Device 1，Camera Device 2表示三个sensor设备；output channel 0，output channel 1，output channel 2表示sensor设备的三个输出通道。三个图像传感器可以通过软件配置映射到不同的sensor 设备。

## 2. API描述

### 构造函数

【描述】

根据`csi id`和摄像头类型构建`Sensor`对象

用户需要先构建`Sensor`对象再继续操作

目前已实现自动探测摄像头，用户可选择输出图像的最大分辨率和帧率，参考[摄像头列表](#4-摄像头列表)

用户设置目标分辨率和帧率之后，如果底层驱动不支持该设置，则会进行自动匹配出最佳配置

具体使用的配置可参考日志，如`use sensor 23, output 640x480@90`

【语法】

```python
sensor = Sensor(id, [width, height, fps])
```

【参数】

| 参数名称        | 描述                          | 输入/输出 | 说明 |
|-----------------|-------------------------------|-----------| --- |
| id | `csi` 端口, 支持`0-2` | 输入 | 必选 |
| width | `sensor`最大输出图像宽度 | 输入 | 可选，默认`1920` |
| height | `sensor`最大输出图像高度 | 输入 | 可选，默认`1080` |
| fps | `sensor`最大输出图像帧率 | 输入 | 可选，默认`30` |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| Sensor 对象       |  |

【举例】

```python
sensor = Sensor(id = 0)
sensor = Sensor(id = 0, witdh = 1280, height = 720, fps = 60)
sensor = Sensor(id = 0, witdh = 640, height = 480)
```

【相关主题】

无

### 2.1 sensor.reset

【描述】

复位`sensor`

在构造`Sensor`对象之后，必须调用本函数才能继续其他操作

【语法】

```python
sensor.reset()
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| 无 | | |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 无 | |

【举例】

```python
# 初始化sensor设备0以及sensor OV5647
sensor.reset()
```

【相关主题】

无

### 2.2 sensor.set_framesize

【描述】

设置指定通道的输出图像尺寸

用户可使用`framesize`或通过指定`width`&`height`来设置输出图像尺寸

***宽度会自动对齐到16像素宽***

【语法】

```python
sensor.set_framesize(framesize = FRAME_SIZE_INVAILD, chn = CAM_CHN_ID_0, alignment=0, **kwargs)
```

【参数】

| 参数名称 | 描述             | 输入/输出 |
| -------- | ---------------- | --------- |
| framesize  | sensor[输出图像尺寸](#31-frame_size)     | 输入      |
| chn  | sensor输出[通道号](#33-channel) | 输入      |
| width    | 输出图像宽度,*kw_arg*     | 输入      |
| height   | 输出图像高度,*kw_arg*     | 输入      |

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| 无 | |

【注意】

输出图像尺寸不能超过摄像头实际输出。

不同输出通道最大可输出图像尺寸由硬件限制。

【举例】

```python
# 配置sensor设备0,输出通道0, 输出图尺寸为640x480
sensor.set_framesize(chn = CAM_CHN_ID_0, width = 640, height = 480)

# 配置sensor设备0,输出通道1, 输出图尺寸为320x240
sensor.set_framesize(chn = CAM_CHN_ID_1, width = 320, height = 240)
```

【相关主题】

无

### 2.3 sensor.set_pixformat

【描述】

设置指定sensor设备和通道的输出图像格式

【语法】

```python
sensor.set_pixformat(pix_format, chn = CAM_CHN_ID_0)
```

【参数】

| 参数名称   | 描述             | 输入/输出 |
| ---------- | ---------------- | --------- |
| pix_format | [输出图像格式](#32-pixel_format)     | 输入      |
| chn_num    | sensor输出[通道号](#33-channel) | 输入      |

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| 无 | |

【举例】

```python
# 配置sensor设备0,输出通道0, 输出NV12格式
sensor.set_pixformat(sensor.YUV420SP, chn = CAM_CHN_ID_0)

# 配置sensor设备0,输出通道1, 输出RGB888格式
sensor.set_pixformat(sensor.RGB888, chn =  CAM_CHN_ID_1)
```

【相关主题】

无

### 2.4 sensor.set_hmirror

【描述】

设置摄像头水平镜像

【语法】

```python
sensor.set_hmirror(enable)
```

【参数】

| 参数名称   | 描述             | 输入/输出 |
| ---------- | ---------------- | --------- |
| enable    | `True` 表示开启水平镜像<br>`False`表示关闭水平镜像 | 输入      |

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| 无 | |

【注意】

【举例】

```python
sensor.set_hmirror(True)
```

【相关主题】

无

### 2.5 sensor.set_vflip

【描述】

设置摄像头垂直翻转

【语法】

```python
sensor.set_vflip(enable)
```

【参数】

| 参数名称   | 描述             | 输入/输出 |
| ---------- | ---------------- | --------- |
| enable    | `True` 表示开启垂直翻转<br>`False` 表示关闭垂直翻转 | 输入      |

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| 无 | |

【注意】

【举例】

```python
sensor.set_vflip(True)
```

【相关主题】

无

### 2.6 sensor.run

【描述】

摄像头开始输出

**`必须在MediaManager.init()之前调用`**

【语法】

```python
sensor.run()
```

【参数】

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| 无 | |

【注意】

如果同时使用多个摄像头(最多3个)，只需要其中一个执行`run`即可

【举例】

```python
# 启动sensor设备输出数据流
sensor.run()
```

【相关主题】

无

### 2.7 sensor.stop

【描述】

停止sensor输出

**`必须在MediaManager.deinit()之前调用`**

【语法】

```python
sensor.stop()
```

【参数】

【返回值】

| 返回值 | 描述                   |
| ------ | ---------------------- |
| 无 | |

【注意】

如果同时使用多个摄像头(最多3个)，**需要每一个都执行`stop`**

【举例】

```python
# 停止sensor设备0输出数据流
sensor.stop()
```

【相关主题】

无

### 2.8 sensor.snapshot

【描述】

从指定sensor设备的支持输出通道中捕获一帧图像数据

【语法】

```python
sensor.snapshot(chn = CAM_CHN_ID_0)
```

【参数】

| 参数名称 | 描述             | 输入/输出 |
| -------- | ---------------- | --------- |
| chn_num  | sensor输出[通道号](#33-channel) |           |

【返回值】

| 返回值    | 描述 |
| --------- | ---- |
| image对象 | 成功 |
| 其他      | 失败 |

【注意】

【举例】

```python
# 从sensor设备0的通道0输出捕获一帧图像数据
sensor.snapshot()
```

【相关主题】

无

### 2.9 sensor.bind_info

【描述】

在`Display.bind_layer`时使用，获取绑定信息

【语法】

```python
sensor.bind_info(x = 0, y = 0, chn = CAM_CHN_ID_0)
```

【参数】

| 参数名称 | 描述             | 输入/输出 |
| -------- | ---------------- | --------- |
| x | 将`sensor`指定通道输出图像绑定到`Display`或`Venc`模块的指定坐标 | |
| y | 将`sensor`指定通道输出图像绑定到`Display`或`Venc`模块的指定坐标 | |
| chn_num  | sensor输出[通道号](#33-channel) |           |

【返回值】

| 返回值    | 描述 |
| --------- | ---- |
| 无 | |

【注意】

【举例】

```python

```

【相关主题】

无

## 3. 数据结构描述

### 3.1 frame_size

| 图像帧尺寸 | 分辨率 |
| -- | -- |
| QQCIF       | 88x72 |
| QCIF        | 176x144 |
| CIF         | 352x288 |
| QSIF        | 176x120 |
| SIF         | 352x240 |
| QQVGA       | 160x120 |
| QVGA        | 320x240 |
| VGA         | 640x480 |
| HQQVGA      | 120x80 |
| HQVGA       | 240x160 |
| HVGA        | 480x320 |
| B64X64      | 64x64 |
| B128X64     | 128x64 |
| B128X128    | 128x128 |
| B160X160    | 160x160 |
| B320X320    | 320x320 |
| QQVGA2      | 128x160 |
| WVGA        | 720x480 |
| WVGA2       | 752x480 |
| SVGA        | 800x600 |
| XGA         | 1024x768 |
| WXGA        | 1280x768 |
| SXGA        | 1280x1024 |
| SXGAM       | 1280x960 |
| UXGA        | 1600x1200 |
| HD          | 1280x720 |
| FHD         | 1920x1080 |
| QHD         | 2560x1440 |
| QXGA        | 2048x1536 |
| WQXGA       | 2560x1600 |
| WQXGA2      | 2592x1944 |

### 3.2 pixel_format

| 像素格式 |  |
| -- | -- |
|   RGB565 | |
|   RGB888 | |
|   RGBP888 | |
|   YUV420SP | NV12 |
|   GRAYSCALE | |

### 3.3 channel

| 通道号 | |
| -- | -- |
| CAM_CHN_ID_0 | 通道0 |
| CAM_CHN_ID_1 | 通道1 |
| CAM_CHN_ID_2 | 通道2 |
| CAM_CHN_ID_MAX | 非法通道 |

## 4. 摄像头列表

| 摄像头型号 | 分辨率<br>Width x Height | 帧率 |
| -- | -- | -- |
| OV5647 | 1920x1080 | 30 |
| | 1280x960 | 60 |
| | 1280x720 | 60 |
| | 640x480 | 90 |

## 5. 示例程序

### 例程

```python
# Camera Example
import time, os, sys

from media.sensor import *
from media.display import *
from media.media import *

def camera_test():
    print("camera_test")

    # construct a Sensor object with default configure
    sensor = Sensor()
    # sensor reset
    sensor.reset()
    # set hmirror
    # sensor.set_hmirror(False)
    # sensor vflip
    # sensor.set_vflip(False)

    # set chn0 output size, 1920x1080
    sensor.set_framesize(Sensor.FHD)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)
    # bind sensor chn0 to display layer video 1
    bind_info = sensor.bind_info()
    Display.bind_layer(**bind_info, layer = Display.LAYER_VIDEO1)

    # set chn1 output format
    sensor.set_framesize(width = 640, height = 480, chn = CAM_CHN_ID_1)
    sensor.set_pixformat(Sensor.RGB888, chn = CAM_CHN_ID_1)

    # set chn2 output format
    sensor.set_framesize(width = 640, height = 480, chn = CAM_CHN_ID_2)
    sensor.set_pixformat(Sensor.RGB565, chn = CAM_CHN_ID_2)

    # use hdmi as display output
    Display.init(Display.LT9611, to_ide = True, osd_num = 2)
    # init media manager
    MediaManager.init()
    # sensor start run
    sensor.run()

    try:
        while True:
            os.exitpoint()

            img = sensor.snapshot(chn = CAM_CHN_ID_1)
            Display.show_image(img, alpha = 128)

            img = sensor.snapshot(chn = CAM_CHN_ID_2)
            Display.show_image(img, x = 1920 - 640, layer = Display.LAYER_OSD1)

    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        print(f"Exception {e}")
    # sensor stop run
    sensor.stop()
    # deinit display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    camera_test()
```
