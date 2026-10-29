# `VDEC`模块 API 手册

## 概述

本文件详细介绍了 K230_CanMV VDEC 模块的 API。该模块支持 H.264 和 H.265 解码，并能够与 VO 模块进行绑定，将解码后的数据输出至 VO 显示设备。

## API 介绍

本模块提供了 `Decoder` 类，该类包含以下方法：

### Decoder.\_\_init__

**描述**

构造函数，用于初始化解码器实例。

**语法**  

```python
decoder = Decoder(type)
```

**参数**  

| 参数名称 | 描述         | 输入/输出 |
|----------|--------------|-----------|
| type     | 编码类型     | 输入      |

**返回值**  

| 返回值 | 描述    |
|--------|---------|
| Decoder 对象 |  解码器对象   |

**注意事项**  

VDEC 模块最多支持四路并发解码。

### Decoder.create

**描述**

创建解码器实例。

**语法**  

```python
Decoder.create()
```

**参数**

无

**返回值**  

| 返回值 | 描述    |
|--------|---------|
| 无 ||

### Decoder.destroy

**描述**

销毁解码器实例。

**语法**  

```python
Decoder.destroy()
```

**参数**

无

**返回值**  

| 返回值 | 描述    |
|--------|---------|
| 无 ||

### Decoder.start

**描述**

启动解码器，开始解码过程。

**语法**  

```python
Decoder.start()
```

**参数**

无

**返回值**  

| 返回值 | 描述    |
|--------|---------|
| 无 ||

### Decoder.decode

**描述**

对一帧数据进行解码。

**语法**  

```python
Decoder.decode(stream_data)
```

**参数**  

| 参数名称   | 描述     | 输入/输出 |
|------------|----------|-----------|
| stream_data | 编码数据 | 输入      |

**返回值**  

| 返回值 | 描述    |
|--------|---------|
| 无 ||

### Decoder.stop

**描述**

释放当前解码帧的码流缓冲区。

**语法**  

```python
Decoder.stop()
```

**参数**

无

**返回值**  

| 返回值 | 描述    |
|--------|---------|
| 无 ||

### Decoder.get_vdec_channel

**描述**

返回解码输出通道号。

**语法**  

```python
Decoder.get_vdec_channel()
```

**参数**

无

**返回值**  

| 返回值 | 描述    |
|--------|---------|
| chn    | 解码输出通道号 |

### Decoder.bind_info

**描述**

在调用 `Display.bind_layer` 时使用，用于获取绑定信息。

**语法**  

```python
Decoder.bind_info(x = 0, y = 0, width = 1920,height = 1080,pix_format=PIXEL_FORMAT_YUV_SEMIPLANAR_420,chn = 0)
```

**参数**  

| 参数名称 | 描述               | 输入/输出 |
|----------|--------------------|-----------|
| x        | 绑定区域的水平起始坐标 | 输入      |
| y        | 绑定区域的垂直起始坐标 | 输入      |
| width    | 解码帧的宽度      | 输入      |
| height   | 解码帧的高度      | 输入      |
| pix_format | 图像像素格式    | 输入      |
| chn      | 解码输出通道号    | 输入      |

**返回值**  

| 返回值 | 描述    |
|--------|---------|
| dict 对象 | 包含通道的源信息、区域尺寸和像素格式 |

## 数据结构描述

### StreamData

**说明**  

码流结构体，包含解码数据及其时间戳信息。

**定义**  

```python
class StreamData:
    def __init__(self):
        self.data
        self.pts
```

**成员**  

| 成员名称 | 描述       |
|----------|------------|
| data     | 码流数据   |
| pts      | 时间戳信息 |

## 示例程序

### 示例 1

```python
from media.media import *
from mpp.payload_struct import *
import media.vdecoder as vdecoder
from media.display import *
import time
import os

STREAM_SIZE = 40960

def vdec_test(file_name, width=1280, height=720):
    print("vdec_test start")
    vdec_chn = VENC_CHN_ID_0
    vdec_width = ALIGN_UP(width, 16)
    vdec_height = height
    vdec = None
    vdec_payload_type = K_PT_H264

    # display_type = Display.VIRT
    display_type = Display.ST7701  # 使用 ST7701 LCD 屏幕作为输出，最大分辨率 800*480
    # display_type = Display.LT9611  # 使用 HDMI 作为输出

    # 判断文件类型
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        vdec_payload_type = K_PT_H264
    elif suffix == '265':
        vdec_payload_type = K_PT_H265
    else:
        print("未知的文件扩展名")
        return

    # 实例化视频解码器
    vdec = vdecoder.Decoder(vdec_payload_type)

    # 初始化显示设备
    if display_type == Display.VIRT:
        Display.init(display_type, width=vdec_width, height=vdec_height, fps=30)
    else:
        Display.init(display_type, to_ide=True)

    # 初始化缓冲区
    MediaManager.init()

    # 创建视频解码器
    vdec.create()

    # 绑定显示
    bind_info = vdec.bind_info(width=vdec_width, height=vdec_height, chn=vdec.get_vdec_channel())
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1)

    vdec.start()

    # 打开文件
    with open(file_name, "rb") as fi:
        while True:
            os.exitpoint()
            # 读取视频数据流
            data = fi.read(STREAM_SIZE)
            if not data:
                break
            # 解码数据流
            vdec.decode(data)

    # 停止视频解码器
    vdec.stop()
    # 销毁视频解码器
    vdec.destroy()
    time.sleep(1)

    # 关闭显示
    Display.deinit()
    # 释放缓冲区
    MediaManager.deinit()

    print("vdec_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vdec_test("/sdcard/examples/test.264", 800, 480)  # 解码 H.264/H.265 视频文件
```
