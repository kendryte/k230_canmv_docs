# Sensor Example Explanation

## Overview

The K230 has 3 MIPI-CSI inputs (3x2 lane/1x4+1x2 lane), supporting up to 3 cameras. Each camera can output 3 channels, providing different resolutions and image formats.

## Examples

### Capturing 3 Channels from a Single Camera and Displaying on an HDMI Monitor

This example opens a camera, captures images from 3 channels, and displays them on an HDMI monitor. Channel 0 captures 1080P images, while channels 1 and 2 capture VGA resolution images overlaid on top of the channel 0 image.

```python
# Camera 示例
import time
import os
import sys

from media.sensor import *
from media.display import *
from media.media import *

sensor = None

try:
    print("camera_test")

    # 根据默认配置构建 Sensor 对象
    sensor = Sensor()
    # 复位 sensor
    sensor.reset()

    # 设置通道 0 分辨率为 1920x1080
    sensor.set_framesize(Sensor.FHD)
    # 设置通道 0 格式为 YUV420SP
    sensor.set_pixformat(Sensor.YUV420SP)
    # 绑定通道 0 到显示 VIDEO1 层
    bind_info = sensor.bind_info()
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1)

    # 设置通道 1 分辨率和格式
    sensor.set_framesize(width=640, height=480, chn=CAM_CHN_ID_1)
    sensor.set_pixformat(Sensor.RGB888, chn=CAM_CHN_ID_1)

    # 设置通道 2 分辨率和格式
    sensor.set_framesize(width=640, height=480, chn=CAM_CHN_ID_2)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_2)

    # 初始化 HDMI 和 IDE 输出显示，若屏幕无法点亮，请参考 API 文档中的 K230_CanMV_Display 模块 API 手册进行配置
    Display.init(Display.LT9611, to_ide=True, osd_num=2)
    # 初始化媒体管理器
    MediaManager.init()
    # 启动 sensor
    sensor.run()

    while True:
        os.exitpoint()

        img = sensor.snapshot(chn=CAM_CHN_ID_1)
        Display.show_image(img, alpha=128)

        img = sensor.snapshot(chn=CAM_CHN_ID_2)
        Display.show_image(img, x=1920 - 640, layer=Display.LAYER_OSD1)

except KeyboardInterrupt as e:
    print("用户停止: ", e)
except BaseException as e:
    print(f"异常: {e}")
finally:
    # 停止 sensor
    if isinstance(sensor, Sensor):
        sensor.stop()
    # 销毁显示
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()
```

### Capturing Dual Camera Images and Displaying on an HDMI Monitor

This example configures 2 cameras to each output 960x540 images and displays them side by side on an HDMI monitor.

```python
# Camera 双摄示例
import time
import os
import sys

from media.sensor import *
from media.display import *
from media.media import *

sensor0 = None
sensor1 = None

try:
    print("camera_test")

    # 构建 Sensor 对象 sensor0
    sensor0 = Sensor(id=0)
    sensor0.reset()
    # 设置通道 0 分辨率为 960x540
    sensor0.set_framesize(width=960, height=540)
    # 设置通道 0 格式为 YUV420
    sensor0.set_pixformat(Sensor.YUV420SP)
    # 绑定通道 0 到显示 VIDEO1 层
    bind_info = sensor0.bind_info(x=0, y=0)
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1)

    # 构建 Sensor 对象 sensor1
    sensor1 = Sensor(id=1)
    sensor1.reset()
    # 设置通道 0 分辨率为 960x540
    sensor1.set_framesize(width=960, height=540)
    # 设置通道 0 格式为 YUV420
    sensor1.set_pixformat(Sensor.YUV420SP)
    # 绑定通道 0 到显示 VIDEO2 层
    bind_info = sensor1.bind_info(x=960, y=0)
    Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO2)

    # 初始化 HDMI 和 IDE 输出显示，若屏幕无法点亮，请参考 API 文档中的 K230_CanMV_Display 模块 API 手册进行配置
    Display.init(Display.LT9611, to_ide=True)
    # 初始化媒体管理器
    MediaManager.init()

    # 多摄场景仅需执行一次 run
    sensor0.run()

    while True:
        os.exitpoint()
        time.sleep(1)
except KeyboardInterrupt as e:
    print("用户停止")
except BaseException as e:
    print(f"异常: '{e}'")
finally:
    # 每个 sensor 都需要执行 stop
    if isinstance(sensor0, Sensor):
        sensor0.stop()
    if isinstance(sensor1, Sensor):
        sensor1.stop()
    # 销毁显示
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()
```

```{admonition} 提示
有关 Sensor 模块的详细接口，请参考 [API 文档](../../api/mpp/k230_canmv_sensor_module_api_manual.md)。
```
