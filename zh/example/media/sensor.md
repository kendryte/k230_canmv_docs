# Sensor 示例讲解

## 概述

K230 具备 3 路 MIPI-CSI 输入（3x2 lane/1x4+1x2 lane），最多可连接 3 路摄像头，每路摄像头支持输出 3 个通道，提供不同的分辨率和图像格式。

## 示例

### 获取单摄像头的 3 个通道图像并显示在 HDMI 显示器上

本示例打开摄像头，获取 3 个通道的图像并显示在 HDMI 显示器上。通道 0 采集 1080P 图像，通道 1 和通道 2 采集 VGA 分辨率的图像并叠加在通道 0 的图像上。

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

### 获取双摄像头图像并显示在 HDMI 显示器上

本示例分别配置 2 个摄像头输出 960x540 图像，并并排显示在 HDMI 显示器上。

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
有关 Sensor 模块的详细接口，请参考 [API 文档](../../api/mpp/K230_CanMV_Sensor模块API手册.md)。
```
