# 4. 识别 DM 码例程讲解

## 1. 概述

Data Matrix 码是一种二维条码，广泛用于小型产品的标识和跟踪。它由小黑白方块组成，这些方块在矩形或正方形的网格中排列。

CanMV 支持 OpenMV 算法，能够识别 Data Matrix 码，相关接口为 `find_datamatrices`。

## 2. 示例

本示例设置摄像头输出为 640x480 的灰度图像，并使用 `image.find_datamatrices` 来识别 Data Matrix 码。

```{tip}
如果识别成功率低，可尝试调整摄像头的镜像和翻转设置。
```

```python
# 数据矩阵示例
import time
import math
import os
import gc
import sys

from media.sensor import *
from media.display import *
from media.media import *

# 定义检测图像的宽度和高度
DETECT_WIDTH = 640
DETECT_HEIGHT = 480

sensor = None

try:
    # 使用默认配置构造 Sensor 对象
    sensor = Sensor(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    # 重置 sensor
    sensor.reset()

    # 设置输出大小和格式
    sensor.set_framesize(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    sensor.set_pixformat(Sensor.GRAYSCALE)

    # 初始化显示
    Display.init(Display.VIRT, width=DETECT_WIDTH, height=DETECT_HEIGHT, fps=100)

    # 初始化媒体管理器
    MediaManager.init()
    # 启动 sensor
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()

        # 检查是否应该退出
        os.exitpoint()
        
        img = sensor.snapshot()
        for matrix in img.find_datamatrices():
            # 绘制识别到的 Data Matrix 码的矩形框
            img.draw_rectangle([v for v in matrix.rect()], color=(255, 0, 0))
            print_args = (matrix.rows(), matrix.columns(), matrix.payload(), (180 * matrix.rotation()) / math.pi, fps.fps())
            print("矩阵 [%d:%d], 内容 \"%s\", 旋转 %f (度), FPS %f" % print_args)

        # 将结果绘制到屏幕上
        Display.show_image(img)
        gc.collect()

except KeyboardInterrupt:
    print("用户停止")
except BaseException as e:
    print(f"异常 '{e}'")
finally:
    # 停止 sensor
    if isinstance(sensor, Sensor):
        sensor.stop()
    # 销毁 display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # 释放媒体缓冲区
    MediaManager.deinit()
```

### 代码说明

- **导入模块**：导入必要的库以便使用传感器、显示和媒体管理功能。
- **定义图像尺寸**：设置检测图像的宽度和高度为 640x480。
- **Sensor 配置**：创建并配置传感器对象，设置图像输出的大小和格式（灰度图像）。
- **显示初始化**：配置显示输出方式，选择 IDE 输出。
- **主循环**：
  - 捕捉图像并检查退出条件。
  - 识别图像中的 Data Matrix 码，并在码周围绘制红色矩形框。
  - 打印 Data Matrix 码的详细信息，包括行数、列数、内容、旋转角度和帧率。
- **异常处理**：捕获用户中断或其他异常，确保传感器正常停止并释放资源。

```{admonition} 提示
具体接口定义请参考 [find_datamatrices](../../api/openmv/image.md#2283-find_datamatrices)。
```
