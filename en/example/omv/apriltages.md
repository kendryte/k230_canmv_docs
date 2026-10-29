# AprilTags Recognition Example Explanation

## Overview

AprilTags is a visual marker system widely used in computer vision for localization, recognition, and tracking. Developed by April Robotics, AprilTags is an efficient binary identification tag system particularly suitable for applications such as robotics and augmented reality.

CanMV supports the OpenMV algorithm and can recognize AprilTags. The relevant interface is `find_apriltags`.

## Example

This example configures the camera output to a 320x240 grayscale image and uses `image.find_apriltags` to recognize AprilTags.

```{tip}
If the recognition success rate is low, try adjusting the camera's mirror and flip settings.
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
tag_families |= image.ARTOOLKIT # ARTOOLKit 标签

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

### Code Explanation

- **Import Modules**: Import the necessary libraries to use sensor, display, and media management functions.
- **Define Image Dimensions**: Set the width and height of the detection image to 320x240.
- **Define Tag Families**: Configure recognizable tag families, including TAG16H5, TAG25H7, TAG25H9, TAG36H10, TAG36H11, and ARToolkit. You can disable certain tag families by commenting out the relevant lines.
- **family_name Function**: Returns the name of the tag based on its type, facilitating subsequent processing and display.
- **Sensor Configuration**: Create and configure the sensor object, setting the output image size and format (grayscale image).
- **Display Initialization**: Configure the display output method, selecting IDE output.
- **Main Loop**:
  - Capture images and check exit conditions.
  - Recognize AprilTags in the image, and draw red rectangles and center crosses around the tags.
  - Print detailed information about the tags, including tag family, tag ID, and rotation angle.
- **Exception Handling**: Catch user interruptions or other exceptions to ensure the sensor stops normally and resources are released.

```{admonition} Tip
For specific interface definitions, please refer to [find_apriltags](../../api/openmv/image.md#find-apriltags).
```
