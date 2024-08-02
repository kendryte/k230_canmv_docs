# 1. Sensor例程讲解

## 1. 概述

K230有3路MIPI-CSI（3x2 lane/1x4+1x2 lane）输入，最多可接3路摄像头，每路摄像头支持3个通道输出不同的分辨率及图像格式

## 2. 示例

### 2.1 获取单摄3个通道图像显示在HDMI显示器

打开摄像头，获取3个通道的图像显示在HDMI显示器

通道0采集1080P图像，通道1和通道2采集VGA分辨率图像并叠加在通道0图像上

```python
# Camera Example
import time, os, sys

from media.sensor import *
from media.display import *
from media.media import *

sensor = None

try:
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
finally:
    # sensor stop run
    if isinstance(sensor, Sensor):
        sensor.stop()
    # deinit display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()
```

### 2.2 获取双摄图像显示在HDMI显示器

分别配置2个摄像头输出960x540图像，并排显示在HDMI显示器

```python
# Camera Example
#
# Note: You will need an SD card to run this example.
#
# You can start 2 camera preview.
import time, os, sys

from media.sensor import *
from media.display import *
from media.media import *

sensor0 = None
sensor1 = None

try:
    print("camera_test")

    sensor0 = Sensor(id = 0)
    sensor0.reset()
    # set chn0 output size, 960x540
    sensor0.set_framesize(width = 960, height = 540)
    # set chn0 out format
    sensor0.set_pixformat(Sensor.YUV420SP)
    # bind sensor chn0 to display layer video 1
    bind_info = sensor0.bind_info(x = 0, y = 0)
    Display.bind_layer(**bind_info, layer = Display.LAYER_VIDEO1)

    sensor1 = Sensor(id = 1)
    sensor1.reset()
    # set chn0 output size, 960x540
    sensor1.set_framesize(width = 960, height = 540)
    # set chn0 out format
    sensor1.set_pixformat(Sensor.YUV420SP)

    bind_info = sensor1.bind_info(x = 960, y = 540)
    Display.bind_layer(**bind_info, layer = Display.LAYER_VIDEO2)

    # use hdmi as display output
    Display.init(Display.LT9611, to_ide = True)
    # init media manager
    MediaManager.init()

    # multiple sensor only need one excute run()
    sensor0.run()

    while True:
        os.exitpoint()
        time.sleep(1)
except KeyboardInterrupt as e:
    print("user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # multiple sensor all need excute stop()
    if isinstance(sensor0, Sensor):
        sensor0.stop()
    if isinstance(sensor1, Sensor):
        sensor1.stop()
    # or call Sensor.deinit()
    # Sensor.deinit()

    # deinit display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # deinit media buffer
    MediaManager.deinit()
```

```{admonition} 提示
Sensor模块具体接口请参考[API文档](../../api/mpp/K230_CanMV_Sensor模块API手册.md)
```
