# 图像处理例程讲解

## 概述

在 OpenMV 中，有许多图像处理函数用于不同的图像操作和特征处理。这些函数可以帮助你实现各种视觉任务，如图像增强、降噪、二值化、边缘检测等。

CanMV支持OpenMV算法，同样可以使用这些函数

## 图像处理函数说明

### 图像增强与校正

- **`histeq`**: 直方图均衡化
  - 用于增强图像的对比度，使图像的直方图分布更均匀。

  ```python
  img = sensor.snapshot()
  img.histeq()
  ```

- **`gamma_corr`**: Gamma 校正
  - 调整图像的亮度和对比度。Gamma 值大于 1 可以增加对比度，Gamma 值小于 1 可以减小对比度。

  ```python
  img = sensor.snapshot()
  img.gamma_corr(1.5)  # Gamma 值为 1.5
  ```

- **`rotation_corr`**: 旋转校正
  - 校正图像中的旋转误差。

  ```python
  img = sensor.snapshot()
  img.rotation_corr(0.5)  # 校正旋转误差，校正角度为 0.5 弧度
  ```

- **`lens_corr`**: 镜头畸变校正
  - 校正镜头的几何畸变，通常用于纠正鱼眼镜头的畸变。

  ```python
  img = sensor.snapshot()
  img.lens_corr(1.0)  # 校正畸变，校正系数为 1.0
  ```

### 滤波与降噪

- **`gaussian`**: 高斯滤波
  - 用于平滑图像，减少噪声。高斯滤波通过均值滤波的方式进行加权平均。

  ```python
  img = sensor.snapshot()
  img.gaussian(2)  # 高斯滤波，滤波核大小为 2
  ```

- **`bilateral`**: 双边滤波
  - 旨在平滑图像同时保留边缘。双边滤波结合了空间域和颜色域的平滑。

  ```python
  img = sensor.snapshot()
  img.bilateral(5, 75, 75)  # 双边滤波，空间域、颜色域的标准差分别为 5、75
  ```

- **`median`**: 中值滤波
  - 去除图像中的噪声，特别是椒盐噪声。

  ```python
  img = sensor.snapshot()
  img.median(3)  # 中值滤波，窗口大小为 3x3
  ```

- **`mean`**: 均值滤波
  - 平滑图像，通过计算邻域像素的均值来降低噪声。

  ```python
  img = sensor.snapshot()
  img.mean(3)  # 均值滤波，窗口大小为 3x3
  ```

### 二值化与形态学操作

- **`binary`**: 二值化
  - 将图像转换为二值图像，根据阈值将像素分为黑白两种颜色。

  ```python
  img = sensor.snapshot()
  img.binary([(100, 255)])  # 二值化，阈值范围为 (100, 255)
  ```

- **`dilate`**: 膨胀
  - 形态学操作，扩展图像中的白色区域，通常用于填补孔洞。

  ```python
  img = sensor.snapshot()
  img.dilate(2)  # 膨胀操作，膨胀次数为 2
  ```

- **`erode`**: 腐蚀
  - 形态学操作，收缩图像中的白色区域，通常用于去除小的噪声。

  ```python
  img = sensor.snapshot()
  img.erode(2)  # 腐蚀操作，腐蚀次数为 2
  ```

- **`morph`**: 形态学操作
  - 进行复杂的形态学操作，如开运算、闭运算等。

  ```python
  img = sensor.snapshot()
  img.morph(2, morph.MORPH_CLOSE)  # 形态学操作，闭运算
  ```

### 边缘检测

- **`laplacian`**: 拉普拉斯边缘检测
  - 用于检测图像中的边缘。

  ```python
  img = sensor.snapshot()
  img.laplacian(3)  # 拉普拉斯边缘检测，窗口大小为 3
  ```

- **`sobel`**: Sobel 边缘检测
  - 另一种用于边缘检测的滤波器。

  ```python
  img = sensor.snapshot()
  img.sobel(3)  # Sobel 边缘检测，窗口大小为 3
  ```

### 极坐标转换

- **`linpolar`**: 线性极坐标转换
  - 将图像从笛卡尔坐标系转换到极坐标系。

  ```python
  img = sensor.snapshot()
  img.linpolar(10)  # 线性极坐标转换，半径步长为 10
  ```

- **`logpolar`**: 对数极坐标转换
  - 将图像从笛卡尔坐标系转换到对数极坐标系。

  ```python
  img = sensor.snapshot()
  img.logpolar(10)  # 对数极坐标转换，半径步长为 10
  ```

### 图像反转与模式

- **`negate`**: 反转图像
  - 将图像中的所有像素值取反。

  ```python
  img = sensor.snapshot()
  img.negate()  # 反转图像
  ```

- **`midpoint`**: 中值模式
  - 返回图像中值的像素。

  ```python
  img = sensor.snapshot()
  img.midpoint()
  ```

- **`mode`**: 模式值
  - 返回图像中最常见的像素值。

  ```python
  img = sensor.snapshot()
  img.mode()
  ```

### 总结

这些函数可以用来执行各种图像处理任务：

- **图像增强与校正**: `histeq`, `gamma_corr`, `rotation_corr`, `lens_corr`
- **滤波与降噪**: `gaussian`, `bilateral`, `median`, `mean`
- **二值化与形态学操作**: `binary`, `dilate`, `erode`, `morph`
- **边缘检测**: `laplacian`, `sobel`
- **极坐标转换**: `linpolar`, `logpolar`
- **图像反转与模式**: `negate`, `midpoint`, `mode`

可以根据实际需要选择合适的图像处理函数来处理和分析图像。

## 示例

这里只列举一个图像二值化demo，具体demo还请查看固件自带虚拟U盘中的例程

```python
# 颜色二值化滤波示例
#
# 这个脚本展示了二值化图像滤波。您可以传递任意数量的阈值来对图像进行分割。
import time, os, gc, sys

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = ALIGN_UP(640, 16)
DETECT_HEIGHT = 480

# 使用工具 -> 机器视觉 -> 阈值编辑器来选择更好的阈值。
red_threshold = (0,100,   0,127,   0,127) # L A B
green_threshold = (0,100,   -128,0,   0,127) # L A B
blue_threshold = (0,100,   -128,127,   -128,0) # L A B

sensor = None

def camera_init():
    global sensor

    # 使用默认配置构造一个Sensor对象
    sensor = Sensor(width=DETECT_WIDTH,height=DETECT_HEIGHT)
    # sensor复位
    sensor.reset()
    # 设置水平镜像
    # sensor.set_hmirror(False)
    # 设置垂直翻转
    # sensor.set_vflip(False)

    # 设置通道 0 输出大小
    sensor.set_framesize(width=DETECT_WIDTH,height=DETECT_HEIGHT)
    # 设置通道 0 输出格式
    sensor.set_pixformat(Sensor.RGB565)

    # 使用 IDE 作为显示输出，如果您选择的屏幕无法点亮，请参考API文档中的K230_CanMV_Display模块API手册自行配置
    Display.init(Display.VIRT, width= DETECT_WIDTH, height = DETECT_HEIGHT,fps=100,to_ide = True)
    # 初始化媒体管理器
    MediaManager.init()
    # sensor开始运行
    sensor.run()

def camera_deinit():
    global sensor

    # sensor停止运行
    sensor.stop()
    # 销毁display
    Display.deinit()
    # 休眠
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()

def capture_picture():

    frame_count = 0
    fps = time.clock()
    while True:
        fps.tick()
        try:
            os.exitpoint()

            global sensor
            img = sensor.snapshot()

            # 测试红色阈值
            if frame_count < 100:
                img.binary([red_threshold])
            # 测试绿色阈值
            elif frame_count < 200:
                img.binary([green_threshold])
            # 测试蓝色阈值
            elif frame_count < 300:
                img.binary([blue_threshold])
            # 测试非红色阈值
            elif frame_count < 400:
                img.binary([red_threshold], invert = 1)
            # 测试非绿色阈值
            elif frame_count < 500:
                img.binary([green_threshold], invert = 1)
            # 测试非蓝色阈值
            elif frame_count < 600:
                img.binary([blue_threshold], invert = 1)
            else:
                frame_count = 0
            frame_count = frame_count + 1
            # 将结果绘制到屏幕上
            Display.show_image(img)
            img = None
            gc.collect()
            #print(fps.fps())
        except KeyboardInterrupt as e:
            print("user stop: ", e)
            break
        except BaseException as e:
            print(f"Exception {e}")
            break

def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    camera_is_init = False
    try:
        print("camera init")
        camera_init()
        camera_is_init = True
        print("camera capture")
        capture_picture()
    except Exception as e:
        print(f"Exception {e}")
    finally:
        if camera_is_init:
            print("camera deinit")
            camera_deinit()

if __name__ == "__main__":
    main()
```

```{admonition} 提示
具体接口定义请参考 [image](../../api/openmv/image.md)
```
