# 2. 识别条形码例程讲解

## 1. 概述

条形码（Barcode）是一种用来表示数据的视觉模式，通过不同宽度和间隔的条纹或图案来编码信息。条形码广泛应用于各种行业，用于自动识别、存储和管理数据。

CanMV 支持 OpenMV 算法，可以识别条形码，相关接口为 `find_barcodes`，支持多种条形码格式。

## 2. 示例

本示例设置摄像头输出为 640x480 的灰度图像，并使用 `image.find_barcodes` 来识别条形码。

```{tip}
如果识别成功率低，可尝试调整摄像头的镜像和翻转设置，并注意条形码两边留出白色区域。
```

```python
# 条形码检测示例
import time
import math
import os
import gc
import sys

from media.sensor import *
from media.display import *
from media.media import *

# 函数: 获取条形码类型的名称
def barcode_name(code):
    barcode_types = {
        image.EAN2: "EAN2",
        image.EAN5: "EAN5",
        image.EAN8: "EAN8",
        image.UPCE: "UPCE",
        image.ISBN10: "ISBN10",
        image.UPCA: "UPCA",
        image.EAN13: "EAN13",
        image.ISBN13: "ISBN13",
        image.I25: "I25",
        image.DATABAR: "DATABAR",
        image.DATABAR_EXP: "DATABAR_EXP",
        image.CODABAR: "CODABAR",
        image.CODE39: "CODE39",
        image.PDF417: "PDF417",
        image.CODE93: "CODE93",
        image.CODE128: "CODE128",
    }
    return barcode_types.get(code.type(), "未知条形码")

# 定义图像检测宽高
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

        # 识别图像中的条形码
        for code in img.find_barcodes():
            img.draw_rectangle([v for v in code.rect()], color=(255, 0, 0))  # 在识别到的条形码周围绘制矩形
            print_args = (
                barcode_name(code), 
                code.payload(), 
                (180 * code.rotation()) / math.pi, 
                code.quality(), 
                fps.fps()
            )
            print("条形码 %s, 内容 \"%s\", 旋转 %f (度), 质量 %d, FPS %f" % print_args)

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
- **barcode_name 函数**：根据条形码的类型返回其名称，便于后续处理和显示。
- **Sensor 配置**：创建并配置传感器对象，包括设置图像输出的宽度、高度和格式（灰度图像）。
- **显示初始化**：配置显示输出方式，可以选择 HDMI、LCD 或 IDE。
- **主循环**：
  - 捕捉图像并检查退出条件。
  - 识别图像中的条形码，并在条形码周围绘制红色矩形框。
  - 打印条形码的详细信息，包括类型、内容、旋转角度、质量和当前帧率。
- **异常处理**：捕获用户中断或其他异常，确保传感器正常停止并释放资源。

```{admonition} 提示
具体接口定义请参考 [find_barcodes](../../api/openmv/image.md#2284-find_barcodes)。
```
