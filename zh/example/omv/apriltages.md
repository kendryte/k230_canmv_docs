# 识别 AprilTags 例程讲解

## 概述

AprilTags 是一种视觉标记系统，广泛应用于计算机视觉领域，用于定位、识别和跟踪。由 April Robotics 开发，AprilTags 是一种高效的二进制识别标签系统，特别适合机器人技术和增强现实等应用。

CanMV 支持 OpenMV 算法，可以识别 AprilTags，相关接口为 `find_apriltags`。

## 示例

本示例设置摄像头输出为 320x240 的灰度图像，并使用 `image.find_apriltags` 来识别 AprilTags。

```{tip}
如果识别成功率低，可尝试调整摄像头的镜像和翻转设置。
```

```python
# AprilTags 示例
# 这个示例展示了 CanMV 检测 April Tags 的强大功能。

import time
import math
import os
import gc
import sys

from media.sensor import *
from media.display import *
from media.media import *

# 定义检测图像的宽度和高度
DETECT_WIDTH = 320
DETECT_HEIGHT = 240

# 定义可用的标签族
tag_families = 0
tag_families |= image.TAG16H5  # 4x4 方形标签
tag_families |= image.TAG25H7   # 5x7 方形标签
tag_families |= image.TAG25H9   # 5x9 方形标签
tag_families |= image.TAG36H10  # 6x10 方形标签
tag_families |= image.TAG36H11  # 6x11 方形标签（默认）
tag_families |= image.ARTOOLKIT # ARToolKit 标签

# 函数: 获取标签族的名称
def family_name(tag):
    family_dict = {
        image.TAG16H5: "TAG16H5",
        image.TAG25H7: "TAG25H7",
        image.TAG25H9: "TAG25H9",
        image.TAG36H10: "TAG36H10",
        image.TAG36H11: "TAG36H11",
        image.ARTOOLKIT: "ARTOOLKIT",
    }
    return family_dict.get(tag.family(), "未知标签族")

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
        for tag in img.find_apriltags(families=tag_families):
            # 绘制识别到的标签的矩形框和中心十字
            img.draw_rectangle([v for v in tag.rect()], color=(255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))
            print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
            print("标签族 %s, 标签 ID %d, 旋转 %f (度)" % print_args)

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
- **定义图像尺寸**：设置检测图像的宽度和高度为 320x240。
- **定义标签族**：配置可识别的标签族，包括 TAG16H5、TAG25H7、TAG25H9、TAG36H10、TAG36H11 和 ARToolkit。可以通过注释掉相关行来禁用某些标签族。
- **family_name 函数**：根据标签的类型返回其名称，便于后续处理和显示。
- **Sensor 配置**：创建并配置传感器对象，设置图像输出的大小和格式（灰度图像）。
- **显示初始化**：配置显示输出方式，选择 IDE 输出。
- **主循环**：
  - 捕捉图像并检查退出条件。
  - 识别图像中的 AprilTags，并在标签周围绘制红色矩形框和中心十字。
  - 打印标签的详细信息，包括标签族、标签 ID 和旋转角度。
- **异常处理**：捕获用户中断或其他异常，确保传感器正常停止并释放资源。

```{admonition} 提示
具体接口定义请参考 [find_apriltags](../../api/openmv/image.md#2282-find_apriltags)。
```
