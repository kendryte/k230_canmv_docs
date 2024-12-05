# 3.6 `VENC` 模块 API 手册

## 1. 概述

本手册详细介绍了 K230_CanMV VENC 模块的 API。开发者可以通过调用这些 API 进行视频编码，生成不同分辨率和编码格式的码流。VENC 模块需与相机模块结合使用以实现编码功能。

## 2. API 介绍

VENC 模块提供了 `Encoder` 类，该类包含以下方法：

### 2.1 `Encoder.SetOutBufs`

**描述**

配置编码器的输出缓冲区。

**语法**

```python
Encoder.SetOutBufs(chn, buf_num, width, height)
```

**参数**  

| 参数名称 | 描述           | 输入/输出 |
|----------|----------------|-----------|
| chn      | 编码通道号     | 输入      |
| buf_num  | 输出缓冲区数量 | 输入      |
| width    | 编码图像宽度   | 输入      |
| height   | 编码图像高度   | 输入      |

**返回值**  

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非0    | 失败   |

**注意事项**

**`必须在 MediaManager.init() 之前调用`**

### 2.2 `Encoder.Create`

**描述**

创建编码器实例。

**语法**

```python
Encoder.Create(chn, chnAttr)
```

**参数**  

| 参数名称  | 描述               | 输入/输出 |
|-----------|--------------------|-----------|
| chn       | 编码通道号         | 输入      |
| chnAttr   | 编码通道属性结构   | 输入      |

**返回值**  

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非0    | 失败   |

**注意事项**

VENC 最多支持 4 路编码，编码通道号取值范围为 [0, 3]，第 4 路固定用于 IDE 图像传输。除非调用 `compress_for_ide`，建议仅使用 [0, 2]。

### 2.3 `Encoder.Start`

**描述**

启动编码过程。

**语法**

```python
Encoder.Start(chn)
```

**参数**  

| 参数名称 | 描述         | 输入/输出 |
|----------|--------------|-----------|
| chn      | 编码通道号   | 输入      |

**返回值**  

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非0    | 失败   |

### 2.4 `Encoder.SendFrame`

**描述**

向编码器发送图像数据进行编码。

**语法**

```python
Encoder.SendFrame(venc_chn, frame_info)
```

**参数**  

| 参数名称   | 描述               | 输入/输出 |
|------------|--------------------|-----------|
| chn        | 编码通道号         | 输入      |
| frame_info | 原始图像信息结构   | 输入      |

**返回值**  

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非0    | 失败   |

**注意事项**

可编码完整的一帧数据或不定长度的数据流。

### 2.5 `Encoder.GetStream`

**描述**

获取一帧编码后的码流数据。

**语法**

```python
Encoder.GetStream(chn, streamData)
```

**参数**  

| 参数名称   | 描述               | 输入/输出 |
|------------|--------------------|-----------|
| chn        | 编码通道号         | 输入      |
| streamData | 编码码流结构体     | 输出      |

**返回值**  

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非0    | 失败   |

### 2.6 `Encoder.ReleaseStream`

**描述**

释放一帧码流缓冲区。

**语法**

```python
Encoder.ReleaseStream(chn, streamData)
```

**参数**  

| 参数名称   | 描述               | 输入/输出 |
|------------|--------------------|-----------|
| chn        | 编码通道号         | 输入      |
| streamData | 编码码流结构体     | 输入      |

**返回值**  

| 返回值 | 描述   |
|--------|--------|
| 0      | 成功   |
| 非0    | 失败   |

### 2.7 `Encoder.Stop`

**描述**

停止编码过程。

**语法**

```python
Encoder.Stop(chn)
```

**参数**  

| 参数名称 | 描述         | 输入/输出 |
|----------|--------------|-----------|
| chn      | 编码通道号   | 输入      |

### 2.8 `Encoder.Destroy`

**描述**

销毁编码器实例。

**语法**

```python
Encoder.Destroy(chn)
```

**参数**  

| 参数名称 | 描述         | 输入/输出 |
|----------|--------------|-----------|
| chn      | 编码通道号   | 输入      |

## 3. 数据结构描述

### 3.1 `ChnAttrStr`

**说明**

编码通道属性结构。

**定义**

```python
class ChnAttrStr:
    def __init__(self, payloadType, profile, picWidth, picHeight, gopLen=30):
        self.payload_type = payloadType
        self.profile = profile
        self.pic_width = picWidth
        self.pic_height = picHeight
        self.gop_len = gopLen
```

**成员**  

| 成员名称       | 描述            |
|----------------|-----------------|
| payload_type   | 编码格式（h264/h265） |
| profile        | 编码 Profile     |
| pic_width      | 图像宽度        |
| pic_height     | 图像高度        |
| gop_len        | 编码 GOP 长度    |

### 3.2 `StreamData`

**说明**

码流结构体。

**定义**

```python
class StreamData:
    def __init__(self):
        self.data = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.data_size = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.stream_type = [0 for i in range(0, VENC_PACK_CNT_MAX)]
        self.pack_cnt = 0
```

**成员**  

| 成员名称      | 描述             |
|---------------|------------------|
| data          | 码流数据地址     |
| data_size     | 码流数据大小     |
| stream_type   | 帧类型           |
| pack_cnt      | 码流中 pack 的个数 |

**注意事项**

`VENC_PACK_CNT_MAX` 表示码流结构体中 pack 的最大个数，当前设定为 12。

### 3.3 `payload_type`

**描述**

编码格式类型。

**成员**  

| 成员名称               | 描述           |
|-----------------------|----------------|
| PAYLOAD_TYPE_H264     | H.264 编码格式 |
| PAYLOAD_TYPE_H265     | H.265 编码格式 |

### 3.4 `profile`

**描述**

编码 Profile。

**成员**  

| 成员名称                | 描述                   |
|------------------------|------------------------|
| H264_PROFILE_BASELINE  | H.264 Baseline Profile  |
| H264_PROFILE_MAIN      | H.264 Main Profile      |
| H264_PROFILE_HIGH      | H.264 High Profile      |
| H265_PROFILE_MAIN      | H.265 Main Profile      |

### 3.5 `stream_type`

**描述**

码流帧类型。

**成员**  

| 成员名称            | 描述       |
|---------------------|------------|
| STREAM_TYPE_HEADER   | 码流 Header |
| STREAM_TYPE_I       | I 帧       |
| STREAM_TYPE_P       | P 帧       |

## 4. 示例程序

### 4.1 例程 1

将 VENC 绑定到 VICAP，并将获取到的编码数据保存到文件。

```python
from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def vi_bind_venc_test(file_name, width=1280, height=720):
    print("VENC 测试开始")
    venc_chn = VENC_CHN_ID_0
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # 判断文件扩展名
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("未知文件扩展名")
        return

    # 初始化传感器
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=width, height=height, alignment=12)
    sensor.set_pixformat(Sensor.YUV420SP)

    # 实例化视频编码器
    encoder = Encoder()
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # 绑定camera和venc
    link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, venc_chn))

    # init media manager
    MediaManager.init()

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(venc_chn, chnAttr)

    # 开始编码
    encoder.Start(venc_chn)
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                encoder.GetStream(venc_chn, streamData) # 获取一帧码流

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # 码流写文件
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(venc_chn, streamData) # 释放一帧码流

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # 停止camera
    sensor.stop()
    # 销毁camera和venc的绑定
    del link
    # 停止编码
    encoder.Stop(venc_chn)
    # 销毁编码器
    encoder.Destroy(venc_chn)
    # 清理buffer
    MediaManager.deinit()
    print("venc_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    vi_bind_venc_test("/sdcard/examples/test.264",800,480)  # vi绑定venc示例

```

### 4.2 例程2

venc编码数据流，并保存成文件。

```python
from media.vencoder import *
from media.sensor import *
from media.media import *
import time, os

def stream_venc_test(file_name,width=1280, height=720):
    print("venc_test start")
    venc_chn = VENC_CHN_ID_0
    width = ALIGN_UP(width, 16)
    venc_payload_type = K_PT_H264

    # 判断文件类型
    suffix = file_name.split('.')[-1]
    if suffix == '264':
        venc_payload_type = K_PT_H264
    elif suffix == '265':
        venc_payload_type = K_PT_H265
    else:
        print("Unknown file extension")
        return

    # 初始化sensor
    sensor = Sensor()
    sensor.reset()
    # 设置camera 输出buffer
    # set chn0 output size
    sensor.set_framesize(width = width, height = height, alignment=12)
    # set chn0 output format
    sensor.set_pixformat(Sensor.YUV420SP)


    # 实例化video encoder
    encoder = Encoder()
    # 设置video encoder 输出buffer
    encoder.SetOutBufs(venc_chn, 8, width, height)

    # init media manager
    MediaManager.init()

    if (venc_payload_type == K_PT_H264):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
    elif (venc_payload_type == K_PT_H265):
        chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

    streamData = StreamData()

    # 创建编码器
    encoder.Create(venc_chn, chnAttr)

    # 开始编码
    encoder.Start(venc_chn)
    # 启动camera
    sensor.run()

    frame_count = 0
    print("save stream to file: ", file_name)

    yuv420sp_img = None
    frame_info = k_video_frame_info()
    with open(file_name, "wb") as fo:
        try:
            while True:
                os.exitpoint()
                yuv420sp_img = sensor.snapshot(chn=CAM_CHN_ID_0)
                if (yuv420sp_img == -1):
                    continue

                frame_info.v_frame.width = yuv420sp_img.width()
                frame_info.v_frame.height = yuv420sp_img.height()
                frame_info.v_frame.pixel_format = Sensor.YUV420SP
                frame_info.pool_id = yuv420sp_img.poolid()
                frame_info.v_frame.phys_addr[0] = yuv420sp_img.phyaddr()
                #frame_info.v_frame.phys_addr[1] = yuv420sp_img.phyaddr(1)
                if (yuv420sp_img.width() == 800 and yuv420sp_img.height() == 480):
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width*frame_info.v_frame.height + 1024
                elif (yuv420sp_img.width() == 1920 and yuv420sp_img.height() == 1080):
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width*frame_info.v_frame.height + 3072
                elif (yuv420sp_img.width() == 640 and yuv420sp_img.height() == 360):
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width*frame_info.v_frame.height + 3072
                else:
                    frame_info.v_frame.phys_addr[1] = frame_info.v_frame.phys_addr[0] + frame_info.v_frame.width*frame_info.v_frame.height


                encoder.SendFrame(venc_chn,frame_info)
                encoder.GetStream(venc_chn, streamData) # 获取一帧码流

                for pack_idx in range(0, streamData.pack_cnt):
                    stream_data = uctypes.bytearray_at(streamData.data[pack_idx], streamData.data_size[pack_idx])
                    fo.write(stream_data) # 码流写文件
                    print("stream size: ", streamData.data_size[pack_idx], "stream type: ", streamData.stream_type[pack_idx])

                encoder.ReleaseStream(venc_chn, streamData) # 释放一帧码流

                frame_count += 1
                if frame_count >= 200:
                    break
        except KeyboardInterrupt as e:
            print("user stop: ", e)
        except BaseException as e:
            import sys
            sys.print_exception(e)

    # 停止camera
    sensor.stop()
    # 停止编码
    encoder.Stop(venc_chn)
    # 销毁编码器
    encoder.Destroy(venc_chn)
    # 清理buffer
    MediaManager.deinit()
    print("venc_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    stream_venc_test("/sdcard/examples/test.264",800,480)  # venc编码数据流示例

```
