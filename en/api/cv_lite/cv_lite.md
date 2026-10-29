# `cv_lite` Module API Manual

## Overview

The `cv_lite` module is a lightweight image processing module implemented at the underlying level based on `OpenCV` for certain specific tasks, providing accelerated versions of methods for common tasks as a **supplement** to the methods in the `image` module of `openmv`. It should be noted that **it is not the `opencv` library, but only provides accelerated versions of certain tasks**.

For common formats in the `cv_lite` module, the following notes are provided:

- Input data format: `ulab.numpy.ndarray` type, generally obtained through `image.to_numpy_ref()`.
- To convert `ulab.numpy.ndarray` type back to `image` instance type, generally use `img = image.Image(image_width, image_height, image.GRAYSCALE,alloc=image.ALLOC_REF, data=np_data)`, noting whether the image type and data size meet the requirements.
- The above two items do not reallocate memory, they use the same block of memory, and take little time.
- rgb888 format data and openmv's `image` module can be mixed by using `to_rgb565()` to convert.

```{admonition} Note
Please flash the daily_build firmware to enable cv_lite support: https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/
```

## API Description

### grayscale_find_blobs

**Description**

Finds blobs (connected regions) in a grayscale image, returning the position information of the blobs.

**Syntax**  

Please ensure that the Sensor is configured to output a grayscale image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480,640]  # height, width

threshold = [230, 255]   # 二值化阈值范围（亮区域）/ Threshold range for binarization
min_area = 10            # 最小目标面积 / Minimum area to keep
kernel_size = 1          # 腐蚀核大小（可用于降噪）/ Erosion kernel size

img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取图像数据引用 

# 执行灰度图二值连通域检测
blobs = cv_lite.grayscale_find_blobs(image_shape, img_np,threshold[0], threshold[1],min_area, kernel_size)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| threshold_min | Minimum binarization threshold, int type | Input |  |
| threshold_max | Maximum binarization threshold, int type | Input |  |
| min_area | Minimum region area, int type | Input |  |
| kernel_size | Kernel size, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| blobs | List of blob position information, every 4 elements represent the position information of a blob, including position x, y, w, h|

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/grayscale_find_blobs.py`, please open and run it in K230 CanMV IDE.

### rgb888_find_blobs

**Description**

Finds blobs (connected regions) in an RGB888 image, returning the position information of the blobs.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480,640]  # height, width

threshold = [120, 255, 0, 50, 0, 50]

min_area = 100    # 最小色块面积 / Minimum blob area
kernel_size = 1   # 腐蚀膨胀核大小（用于预处理）/ Kernel size for morphological ops

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用

# 调用 cv_lite 扩展进行色块检测，返回 [x, y, w, h, ...] 列表
blobs = cv_lite.rgb888_find_blobs(image_shape, img_np, threshold, min_area, kernel_size)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| threshold | Binarization threshold range, list type, including threshold ranges for R, G, B channels | Input |  |
| min_area | Minimum region area, int type | Input |  |
| kernel_size | Kernel size, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| blobs | List of blob position information, every 4 elements represent the position information of a blob, including position x, y, w, h|

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_find_blobs.py`, please open and run it in K230 CanMV IDE.

### grayscale_find_circles

**Description**

Finds circles in a grayscale image, returning the position information of the circles.

**Syntax**  

Please ensure that the Sensor is configured to output a grayscale image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480,640]  # height, width

# -------------------------------
# 霍夫圆检测参数 / Hough circle detection parameters
# -------------------------------
dp = 1            # 累加器分辨率比 / Inverse ratio of resolution
minDist = 20      # 圆心最小距离 / Minimum distance between centers
param1 = 80       # Canny 高阈值 / Upper threshold for Canny edge detector
param2 = 20       # 累加器阈值 / Accumulator threshold for center detection
minRadius = 10    # 最小圆半径 / Minimum radius to detect
maxRadius = 50    # 最大圆半径 / Maximum radius to detect

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取图像的 ndarray 引用 / Get image data reference

# 检测圆形 / Detect circles using Hough Transform
# 返回格式：[x1, y1, r1, x2, y2, r2, ...]
circles = cv_lite.grayscale_find_circles(image_shape, img_np,dp, minDist,param1, param2,
minRadius, maxRadius)

```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| dp | Inverse ratio of accumulator resolution, float type | Input |  |
| minDist | Minimum distance between centers, int type | Input |  |
| param1 | Canny high threshold, int type | Input |  |
| param2 | Accumulator threshold, int type | Input |  |
| minRadius | Minimum circle radius, int type | Input |  |
| maxRadius | Maximum circle radius, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| circles | List of circle information, every 3 elements represent information of a circle, including position x, y, r|

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/grayscale_find_circles.py`, please open and run it in K230 CanMV IDE.

### rgb888_find_circles

**Description**

Finds circles in an RGB888 image, returning the position information of the circles.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480,640]  # height, width

# -------------------------------
# 霍夫圆检测参数 / Hough Circle parameters
# -------------------------------
dp = 1           # 累加器分辨率与图像分辨率的反比 / Inverse ratio of accumulator resolution
minDist = 30     # 检测到的圆心最小距离 / Minimum distance between detected centers
param1 = 80      # Canny边缘检测高阈值 / Higher threshold for Canny edge detection
param2 = 20      # 霍夫变换圆心检测阈值 / Threshold for center detection in accumulator
minRadius = 10   # 检测圆最小半径 / Minimum circle radius
maxRadius = 50   # 检测圆最大半径 / Maximum circle radius

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用

# 调用 cv_lite 扩展的霍夫圆检测函数，返回圆参数列表 [x, y, r, ...]
circles = cv_lite.rgb888_find_circles(image_shape, img_np, dp, minDist, param1, param2, minRadius, maxRadius)

```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| dp | Inverse ratio of accumulator resolution to image resolution, float type | Input |  |
| minDist | Minimum distance between detected centers, int type | Input |  |
| param1 | Higher threshold for Canny edge detection, int type | Input |  |
| param2 | Threshold for center detection in Hough transform, int type | Input |  |
| minRadius | Minimum circle radius to detect, int type | Input |  |
| maxRadius | Maximum circle radius to detect, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| circles | List of circle information, every 3 elements represent information of a circle, including position x, y, r|

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_find_circles.py`, please open and run it in K230 CanMV IDE.

### grayscale_find_rectangles

**Description**

Finds rectangles in a grayscale image, returning the position information of the rectangles.

**Syntax**  

Please ensure that the Sensor is configured to output a grayscale image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480,640]  # height, width

# -------------------------------
# 矩形检测可调参数 / Adjustable rectangle detection parameters
# -------------------------------
canny_thresh1      = 50        # Canny 边缘检测低阈值 / Canny low threshold
canny_thresh2      = 150       # Canny 边缘检测高阈值 / Canny high threshold
approx_epsilon     = 0.04      # 多边形拟合精度比例（越小拟合越精确）/ Polygon approximation accuracy
area_min_ratio     = 0.001     # 最小面积比例（相对于图像总面积）/ Min area ratio
max_angle_cos      = 0.3       # 最大角度余弦（越小越接近矩形）/ Max cosine of angle between edges
gaussian_blur_size = 5         # 高斯模糊核尺寸（奇数）/ Gaussian blur kernel size

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()

# 调用底层矩形检测函数
# 返回格式：[x0, y0, w0, h0, x1, y1, w1, h1, ...]
rects = cv_lite.grayscale_find_rectangles(
    image_shape, img_np,
    canny_thresh1, canny_thresh2,
    approx_epsilon,
    area_min_ratio,
    max_angle_cos,
    gaussian_blur_size
)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| canny_thresh1 | Canny edge detection low threshold, int type | Input |  |
| canny_thresh2 | Canny edge detection high threshold, int type | Input |  |
| approx_epsilon | Polygon approximation accuracy ratio, float type | Input |  |
| area_min_ratio | Minimum area ratio, float type | Input |  |
| max_angle_cos | Maximum cosine of angle, float type | Input |  |
| gaussian_blur_size | Gaussian blur kernel size, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| rects | List of rectangle position information, every 4 elements represent the position information of a rectangle, including position x, y, w, h|

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/grayscale_find_rectangles.py`, please open and run it in K230 CanMV IDE.

### grayscale_find_rectangles_with_corners

**Description**

Finds rectangles in a grayscale image, returning the position and corner coordinates of the rectangles.

**Syntax**  

Please ensure that the Sensor is configured to output a grayscale image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480,640]  # height, width

# -------------------------------
# 矩形检测可调参数 / Adjustable rectangle detection parameters
# -------------------------------
canny_thresh1      = 50        # Canny 边缘检测低阈值 / Canny low threshold
canny_thresh2      = 150       # Canny 边缘检测高阈值 / Canny high threshold
approx_epsilon     = 0.04      # 多边形拟合精度比例（越小拟合越精确）/ Polygon approximation accuracy
area_min_ratio     = 0.001     # 最小面积比例（相对于图像总面积）/ Min area ratio
max_angle_cos      = 0.3       # 最大角度余弦（越小越接近矩形）/ Max cosine of angle between edges
gaussian_blur_size = 5         # 高斯模糊核尺寸（奇数）/ Gaussian blur kernel size

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()

# 调用底层矩形检测函数
# 返回格式：[[x0, y0, w0, h0, c1.x, c1.y, c2.x, c2.y, c3.x, c3.y, c4,x, c4.y], [x1, y1, w1, h1,c1.x, c1.y, c2.x, c2.y, c3.x, c3.y, c4,x, c4.y], ...]
rects = cv_lite.grayscale_find_rectangles_with_corners(
    image_shape, img_np,
    canny_thresh1, canny_thresh2,
    approx_epsilon,
    area_min_ratio,
    max_angle_cos,
    gaussian_blur_size
)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| canny_thresh1 | Canny edge detection low threshold, int type | Input |  |
| canny_thresh2 | Canny edge detection high threshold, int type | Input |  |
| approx_epsilon | Polygon approximation accuracy ratio, float type | Input |  |
| area_min_ratio | Minimum area ratio, float type | Input |  |
| max_angle_cos | Maximum cosine of angle, float type | Input |  |
| gaussian_blur_size | Gaussian blur kernel size, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| rects | List of rectangle position information, each element is a list containing a rectangle's position coordinates and corner coordinates, totaling 12 values|

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/grayscale_find_rectangles_with_corners.py`, please open and run it in K230 CanMV IDE.

### rgb888_find_rectangles

**Description**

Finds rectangles in an RGB888 image, returning the position information of the rectangles.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480,640]  # height, width

# -------------------------------
# 可调参数（建议调试时调整）/ Adjustable parameters (recommended for tuning)
# -------------------------------
canny_thresh1       = 50        # Canny 边缘检测低阈值 / Canny edge low threshold
canny_thresh2       = 150       # Canny 边缘检测高阈值 / Canny edge high threshold
approx_epsilon      = 0.04      # 多边形拟合精度（比例） / Polygon approximation precision (ratio)
area_min_ratio      = 0.001     # 最小面积比例（0~1） / Minimum area ratio (0~1)
max_angle_cos       = 0.5       # 最大角余弦（值越小越接近矩形） / Max cosine of angle (smaller closer to rectangle)
gaussian_blur_size  = 5         # 高斯模糊核大小（奇数） / Gaussian blur kernel size (odd number)

# 拍摄当前帧图像 / Capture current frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用 / Get RGB888 ndarray reference

# 调用底层矩形检测函数，返回矩形列表 [x0, y0, w0, h0, x1, y1, w1, h1, ...]
# Call underlying rectangle detection function, returns list of rectangles [x, y, w, h, ...]
rects = cv_lite.rgb888_find_rectangles(
    image_shape, img_np,
    canny_thresh1, canny_thresh2,
    approx_epsilon,
    area_min_ratio,
    max_angle_cos,
    gaussian_blur_size
)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| canny_thresh1 | Canny edge detection low threshold, int type | Input |  |
| canny_thresh2 | Canny edge detection high threshold, int type | Input |  |
| approx_epsilon | Polygon approximation accuracy ratio, float type | Input |  |
| area_min_ratio | Minimum area ratio, float type | Input |  |
| max_angle_cos | Maximum cosine of angle, float type | Input |  |
| gaussian_blur_size | Gaussian blur kernel size, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| rects | List of rectangle position information, every 4 elements represent the position information of a rectangle, including position x, y, w, h|

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_find_rectangles.py`, please open and run it in K230 CanMV IDE.

### rgb888_find_rectangles_with_corners

**Description**

Finds rectangles in an RGB888 image, returning the position information and corner coordinates of the rectangles.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480,640]  # height, width

# -------------------------------
# 可调参数（建议调试时调整）/ Adjustable parameters (recommended for tuning)
# -------------------------------
canny_thresh1       = 50        # Canny 边缘检测低阈值 / Canny edge low threshold
canny_thresh2       = 150       # Canny 边缘检测高阈值 / Canny edge high threshold
approx_epsilon      = 0.04      # 多边形拟合精度（比例） / Polygon approximation precision (ratio)
area_min_ratio      = 0.001     # 最小面积比例（0~1） / Minimum area ratio (0~1)
max_angle_cos       = 0.5       # 最大角余弦（值越小越接近矩形） / Max cosine of angle (smaller closer to rectangle)
gaussian_blur_size  = 5         # 高斯模糊核大小（奇数） / Gaussian blur kernel size (odd number)

# 拍摄当前帧图像 / Capture current frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用 / Get RGB888 ndarray reference

# 调用底层矩形检测函数，
# 返回矩形列表 [[x0, y0, w0, h0, c1.x, c1.y, c2.x, c2.y, c3.x, c3.y, c4,x, c4.y], [x1, y1, w1, h1,c1.x, c1.y, c2.x, c2.y, c3.x, c3.y, c4,x, c4.y], ...]
rects = cv_lite.rgb888_find_rectangles_with_corners(
    image_shape, img_np,
    canny_thresh1, canny_thresh2,
    approx_epsilon,
    area_min_ratio,
    max_angle_cos,
    gaussian_blur_size
)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| canny_thresh1 | Canny edge detection low threshold, int type | Input |  |
| canny_thresh2 | Canny edge detection high threshold, int type | Input |  |
| approx_epsilon | Polygon approximation accuracy ratio, float type | Input |  |
| area_min_ratio | Minimum area ratio, float type | Input |  |
| max_angle_cos | Maximum cosine of angle, float type | Input |  |
| gaussian_blur_size | Gaussian blur kernel size, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| rects | List of rectangle position information, each element is a list containing a rectangle's position coordinates and corner coordinates, totaling 12 values|

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_find_rectangles_with_corners.py`, please open and run it in K230 CanMV IDE.

### grayscale_find_edges

**Description**

Finds edges in a grayscale image, returning ulab.numpy.ndarray image data of edge detection, which can be used to create an image instance on top of the returned data.

**Syntax**  

Please ensure that the Sensor is configured to output a grayscale image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# -------------------------------
# 边缘检测参数 / Canny edge detection thresholds
# -------------------------------
threshold1 = 50  # 低阈值 / Lower threshold
threshold2 = 80  # 高阈值 / Upper threshold

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 ndarray 引用 / Get ndarray reference

# 调用 cv_lite 扩展执行边缘检测 / Perform edge detection
# 返回灰度边缘图像 ndarray / Returns edge image ndarray
edge_np = cv_lite.grayscale_find_edges(
    image_shape, img_np, threshold1, threshold2)

# 包装边缘图像用于显示 / Wrap ndarray as image for display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=edge_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| threshold1 | Low threshold, int type | Input |  |
| threshold2 | High threshold, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| edge_np | Image data after edge detection, ulab.numpy.ndarray type, create image instance on this data |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/grayscale_find_edges.py`, please open and run it in K230 CanMV IDE.

### rgb888_find_edges

**Description**

Finds edges in an RGB888 image, returning ulab.numpy.ndarray image data of edge detection, which can be used to create an image instance on top of the returned data.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# -------------------------------
# 边缘检测参数 / Canny edge detection thresholds
# -------------------------------
threshold1 = 50  # 低阈值 / Lower threshold
threshold2 = 80  # 高阈值 / Upper threshold

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用

# 调用 cv_lite 扩展的边缘检测函数，返回灰度边缘图 ndarray
edge_np = cv_lite.rgb888_find_edges(image_shape, img_np, threshold1, threshold2)

# 构造灰度图像对象用于显示
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE, alloc=image.ALLOC_REF, data=edge_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| threshold1 | Low threshold, int type | Input |  |
| threshold2 | High threshold, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| edge_np | Image data after edge detection, ulab.numpy.ndarray type, create image instance on this data |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_find_edges.py`, please open and run it in K230 CanMV IDE.

### grayscale_threshold_binary

**Description**

Performs binarization on a grayscale image, returning the ulab.numpy.ndarray image data after binarization, which can be used to create an image instance on top of the returned data.

**Syntax**  

Please ensure that the Sensor is configured to output a grayscale image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# -------------------------------
# 二值化参数设置 / Binary threshold parameters
# -------------------------------
thresh = 130   # 阈值 / Threshold value
maxval = 255   # 最大值，二值化后白色像素值 / Max value for white pixels

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 ndarray 引用 / Get ndarray reference

# 调用 cv_lite 扩展进行二值化处理
# 返回二值化后的灰度图 ndarray / Returns binary image ndarray
binary_np = cv_lite.grayscale_threshold_binary(image_shape, img_np, thresh, maxval)

# 构造用于显示的灰度图像对象 / Wrap ndarray as grayscale image for display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=binary_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| thresh | Threshold, int type | Input |  |
| maxval | Maximum value, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| binary_np | Image data after binarization, ulab.numpy.ndarray type, create image instance on this data |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/grayscale_threshold_binary.py`, please open and run it in K230 CanMV IDE.

### rgb888_threshold_binary

**Description**

Performs binarization on an RGB888 image, returning the ulab.numpy.ndarray image data after binarization, which can be used to create an image instance on top of the returned data.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# -------------------------------
# 二值化参数设置 / Binary threshold parameters
# -------------------------------
thresh = 130   # 阈值 / Threshold value
maxval = 255   # 最大值，二值化后白色像素值 / Max value for white pixels

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 ndarray 引用 / Get ndarray reference

# 调用二值化接口（返回 ndarray）/ Call binary threshold function (returns ndarray)
binary_np = cv_lite.rgb888_threshold_binary(image_shape, img_np, thresh, maxval)

# 构造灰度图像用于显示 / Construct grayscale image for display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=binary_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| thresh | Threshold, int type | Input |  |
| maxval | Maximum value, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| binary_np | Image data after binarization, ulab.numpy.ndarray type, create image instance on this data |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_threshold_binary.py`, please open and run it in K230 CanMV IDE.

### rgb888_adjust_exposure

**Description**

Adjusts exposure on an RGB888 image, returning the ulab.numpy.ndarray image data after adjustment, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# -------------------------------
# 曝光增益因子（<1 降低亮度，>1 增加亮度）/ Exposure gain factor
# -------------------------------
exposure_gain = 2.5          # 推荐范围 0.2 ~ 3.0；1.0 表示无增益 / Recommended range: 0.2~3.0, 1.0 = no gain

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 图像数据引用 / Get RGB888 ndarray reference (HWC)

# 调用 cv_lite 模块进行曝光调节 / Apply exposure adjustment using cv_lite module
exposed_np = cv_lite.rgb888_adjust_exposure(image_shape, img_np, exposure_gain)

# 包装图像用于显示 / Wrap processed image for display
img_out = image.Image(image_shape[1], image_shape[0], image.RGB888,
                        alloc=image.ALLOC_REF, data=exposed_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| exposure_gain | Exposure gain factor, float type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| exposed_np | Image data after exposure adjustment, ulab.numpy.ndarray type, create image instance on this data |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_adjust_exposure.py`, please open and run it in K230 CanMV IDE.

### rgb888_adjust_exposure_fast

**Description**

Quickly adjusts exposure on an RGB888 image, returning the ulab.numpy.ndarray image data after adjustment, which can be used to create an image instance for display. This method is an accelerated version of the software exposure used above.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# -------------------------------
# 曝光调节参数 / Exposure gain parameter
# exposure_gain: 曝光增益因子，范围建议 0.2 ~ 3.0
# 小于 1.0 为减弱曝光（变暗），大于 1.0 为增强曝光（变亮）
# exposure_gain < 1.0: darker, > 1.0: brighter
# -------------------------------
exposure_gain = 2.5  # 示例：增强亮度 1.5 倍 / Example: brighten image by 1.5x

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 图像引用 / Get RGB888 ndarray (HWC)

# 使用 cv_lite 模块进行曝光调整 / Apply exposure gain using cv_lite
exposed_np = cv_lite.rgb888_adjust_exposure_fast(
    image_shape,
    img_np,
    exposure_gain
)

# 构造图像用于显示 / Wrap processed image for display
img_out = image.Image(image_shape[1], image_shape[0], image.RGB888,
                        alloc=image.ALLOC_REF, data=exposed_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| exposure_gain | Exposure gain factor, float type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| exposed_np | Image data after exposure adjustment, ulab.numpy.ndarray type, create image instance on this data |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_adjust_exposure_fast.py`, please open and run it in K230 CanMV IDE.

### rgb888_white_balance_gray_world_fast

**Description**

Performs fast white balance using the gray world algorithm on an RGB888 image, returning the ulab.numpy.ndarray image data after white balance, which can be used to create an image instance for display. This method is an accelerated version of the software white balance used above.

**Syntax**

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 图像引用 / Get RGB888 ndarray reference (HWC)

# 使用 cv_lite 进行加速灰度世界白平衡处理
# Apply fast gray world white balance
balanced_np = cv_lite.rgb888_white_balance_gray_world_fast(image_shape, img_np)

# 包装图像用于显示 / Wrap processed image for display
img_out = image.Image(image_shape[1], image_shape[0], image.RGB888,alloc=image.ALLOC_REF, data=balanced_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| balanced_np | Image data after white balance, ulab.numpy.ndarray type, create image instance on this data |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_white_balance_gray_world_fast.py`, please open and run it in K230 CanMV IDE.

### rgb888_white_balance_gray_world_fast_ex

**Description**

Performs fast white balance using the gray world algorithm on an RGB888 image, returning the ulab.numpy.ndarray image data after white balance, which can be used to create an image instance for display. This method is a parameter-tunable version of the above method.

**Syntax**

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# -------------------------------
# 设置白平衡参数 / White balance parameters
# -------------------------------
gain_clip = 2.5             # 增益限制系数，防止偏色 / Gain limit to prevent color blowout
brightness_boost = 1.25     # 亮度增强系数 / Global brightness boost

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 图像引用 / Get RGB888 ndarray reference (HWC)

# 使用 cv_lite 进行加速灰度世界白平衡处理（可调参数）
# Apply fast gray world white balance with tunable parameters
balanced_np = cv_lite.rgb888_white_balance_gray_world_fast_ex(
    image_shape,
    img_np,
    gain_clip,
    brightness_boost
)

# 包装图像用于显示 / Wrap processed image for display
img_out = image.Image(image_shape[1], image_shape[0], image.RGB888,
                        alloc=image.ALLOC_REF, data=balanced_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| gain_clip | Gain limit factor, float type | Input |  |
| brightness_boost | Brightness boost factor, float type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| balanced_np | Image data after white balance, ulab.numpy.ndarray type, can create image instance on this data for display |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_white_balance_gray_world_fast_ex.py`, please open and run it in K230 CanMV IDE.

### rgb888_white_balance_white_patch

**Description**

Performs white balance using the white patch algorithm on an RGB888 image, returning the ulab.numpy.ndarray image data after white balance, which can be used to create an image instance for display.

**Syntax**

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# 拍摄一帧图像
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # RGB888 原始图像（ulab ndarray）

# 调用 cv_lite 扩展模块进行白色补丁白平衡
balanced_np = cv_lite.rgb888_white_balance_white_patch(image_shape, img_np)

# 构造 RGB888 显示图像
img_out = image.Image(image_shape[1], image_shape[0], image.RGB888,
                        alloc=image.ALLOC_REF, data=balanced_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| balanced_np | Image data after white balance, ulab.numpy.ndarray type, create image instance on this data|

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_white_balance_white_patch.py`, please open and run it in K230 CanMV IDE.

### rgb888_white_balance_white_patch_ex

**Description**

Performs white balance using the white patch algorithm on an RGB888 image, returning the ulab.numpy.ndarray image data after white balance, which can be used to create an image instance for display. This method is a parameter-tunable version of the above method.

**Syntax**

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640]  # height, width

# -------------------------------
# 白平衡参数 / White balance config
# -------------------------------
top_percent = 5.0          # 用于白点估计的最亮像素百分比 / Top N% brightest pixels used for white patch
gain_clip = 2.5            # 最大增益限制 / Limit gain to avoid over-brightening
brightness_boost = 1.1     # 提亮因子 / Global brightness scaling

# 拍摄一帧图像 / Capture one frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取图像数据引用（ulab ndarray）

# 执行白点白平衡处理 / Apply white patch white balance with parameters
balanced_np = cv_lite.rgb888_white_balance_white_patch_ex(
    image_shape, img_np,
    top_percent,
    gain_clip,
    brightness_boost
)

# 包装图像用于显示 / Wrap balanced image as displayable image object
img_out = image.Image(image_shape[1], image_shape[0], image.RGB888,
                        alloc=image.ALLOC_REF, data=balanced_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| top_percent | Top percentage of brightest pixels used for white point estimation, float type | Input |  |
| gain_clip | Maximum gain limit, float type | Input |  |
| brightness_boost | Brightness boost factor, float type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| balanced_np | Image data after white balance, ulab.numpy.ndarray type, create image instance on this data for display |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_white_balance_white_patch_ex.py`, please open and run it in K230 CanMV IDE.

### rgb888_erode

**Description**

Performs erosion operation on an RGB888 image, returning single-channel ulab.numpy.ndarray image data after erosion, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite

# -------------------------------
# 腐蚀算法参数设置 / Erosion parameters
# -------------------------------
kernel_size = 3         # 卷积核尺寸（必须为奇数，如 3, 5, 7）/ Kernel size (must be odd)
iterations = 1          # 腐蚀迭代次数 / Number of erosion passes
threshold_value = 100   # 二值化阈值（0=使用 Otsu 自动阈值）/ Threshold for binarization (0 = Otsu)

# 获取一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用 / Get RGB888 ndarray reference (HWC)

# 应用腐蚀操作（自动转换为灰度后进行） / Apply erosion (converts RGB to gray internally)
eroded_np = cv_lite.rgb888_erode(
    image_shape,
    img_np,
    kernel_size,
    iterations,
    threshold_value
)

# 构造图像用于显示（灰度格式） / Wrap eroded grayscale image for display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=eroded_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| kernel_size | Kernel size, int type | Input |  |
| iterations | Number of erosion iterations, int type | Input |  |
| threshold_value | Binarization threshold, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| eroded_np | Image data after erosion, ulab.numpy.ndarray type |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_erode.py`, please open and run it in K230 CanMV IDE.

### rgb888_dilate

**Description**

Performs dilation operation on an RGB888 image, returning single-channel ulab.numpy.ndarray image data after dilation, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640] # height, width

# -------------------------------
# 膨胀算法参数设置 / Dilation parameters
# -------------------------------
kernel_size = 3         # 卷积核尺寸 / Kernel size (推荐为奇数，但部分实现支持偶数)
iterations = 1          # 膨胀迭代次数 / Number of dilation passes
threshold_value = 100   # 二值化阈值（0=使用 Otsu 自动阈值）/ Threshold for binarization (0 = Otsu)

# 获取一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用 / Get RGB888 ndarray reference

# 应用膨胀操作（内部先转换为灰度再膨胀）/ Apply dilation (converts RGB to gray internally)
result_np = cv_lite.rgb888_dilate(
    image_shape,
    img_np,
    kernel_size,
    iterations,
    threshold_value
)

# 构造图像用于显示（灰度格式） / Wrap dilated grayscale image for display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=result_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| kernel_size | Kernel size, int type | Input |  |
| iterations | Number of dilation iterations, int type | Input |  |
| threshold_value | Binarization threshold, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| dilated_np | Image data after dilation, ulab.numpy.ndarray type |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_dilate.py`, please open and run it in K230 CanMV IDE.

### rgb888_open

**Description**

Performs opening operation on an RGB888 image, returning single-channel ulab.numpy.ndarray image data after opening, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640] # height, width

# -------------------------------
# 开操作参数设置 / Opening parameters
# -------------------------------
kernel_size = 3         # 卷积核尺寸（应为奇数）/ Kernel size (should be odd)
iterations = 1          # 操作迭代次数 / Number of morphological passes
threshold_value = 100   # 二值化阈值（0=使用 Otsu 自动阈值）/ Threshold for binarization (0 = Otsu)

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用 / Get RGB888 ndarray reference (HWC)

# 执行开操作（先腐蚀再膨胀）/ Apply opening (erode then dilate)
open_np = cv_lite.rgb888_open(
    image_shape,
    img_np,
    kernel_size,
    iterations,
    threshold_value
)

# 构造灰度图像对象用于显示 / Wrap processed grayscale image for display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=open_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| kernel_size | Kernel size, int type | Input |  |
| iterations | Number of opening iterations, int type | Input |  |
| threshold_value | Binarization threshold, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| opened_np | Image data after opening operation, ulab.numpy.ndarray type |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_open.py`, please open and run it in K230 CanMV IDE.

### rgb888_close

**Description**

Performs closing operation on an RGB888 image, returning single-channel ulab.numpy.ndarray image data after closing, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640] # height, width

# -------------------------------
# 闭操作参数设置 / Closing parameters
# -------------------------------
kernel_size = 3         # 卷积核尺寸（建议为奇数）/ Kernel size (recommended odd)
iterations = 1          # 操作迭代次数 / Number of morphological passes
threshold_value = 100   # 二值化阈值（0=使用 Otsu 自动阈值）/ Threshold for binarization (0 = Otsu)

# 获取图像帧 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用 / Get RGB888 ndarray reference (HWC)

# 应用闭操作（先膨胀后腐蚀）/ Apply closing (dilate then erode)
closed_np = cv_lite.rgb888_close(
    image_shape,
    img_np,
    kernel_size,
    iterations,
    threshold_value
)

# 构造图像对象（灰度图）用于显示 / Wrap processed grayscale image for display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=closed_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| kernel_size | Kernel size, int type | Input |  |
| iterations | Number of closing iterations, int type | Input |  |
| threshold_value | Binarization threshold, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| closed_np | Image data after closing operation, ulab.numpy.ndarray type |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_close.py`, please open and run it in K230 CanMV IDE.

### rgb888_tophat

**Description**

Performs top-hat operation on an RGB888 image, returning single-channel ulab.numpy.ndarray image data after top-hat operation, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640] # height, width

# -------------------------------
# 顶帽运算参数设置 / Top-Hat parameters
# -------------------------------
kernel_size = 3         # 卷积核尺寸（建议为奇数）/ Kernel size (recommended odd)
iterations = 1          # 运算迭代次数 / Number of morphological passes
threshold_value = 100   # 二值化阈值（0=使用 Otsu 自动阈值）/ Threshold for binarization (0 = Otsu)

# 获取一帧图像并转换为 ndarray / Capture a frame and convert to ndarray
img = sensor.snapshot()
img_np = img.to_numpy_ref()

# 执行顶帽运算 / Apply Top-Hat operation
# 顶帽 = 原图 - 开运算结果 / Top-Hat = Original - Opening
tophat_np = cv_lite.rgb888_tophat(
    image_shape,
    img_np,
    kernel_size,
    iterations,
    threshold_value
)

# 构造图像对象并显示 / Wrap result as image and display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=tophat_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| kernel_size | Kernel size, int type | Input |  |
| iterations | Number of top-hat iterations, int type | Input |  |
| threshold_value | Binarization threshold, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| tophat_np | Image data after top-hat operation, ulab.numpy.ndarray type |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_tophat.py`, please open and run it in K230 CanMV IDE.

### rgb888_blackhat

**Description**

Performs black-hat operation on an RGB888 image, returning single-channel ulab.numpy.ndarray image data after black-hat operation, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640] # height, width

# -------------------------------
# 黑帽运算参数设置 / Black-Hat parameters
# -------------------------------
kernel_size = 3         # 卷积核尺寸（建议为奇数）/ Kernel size (recommended odd)
iterations = 1          # 运算迭代次数 / Number of morphological passes
threshold_value = 100   # 二值化阈值（0=使用 Otsu 自动阈值）/ Threshold for binarization (0 = Otsu)

# 获取一帧图像并转换为 ndarray / Capture a frame and convert to ndarray
img = sensor.snapshot()
img_np = img.to_numpy_ref()

# 执行黑帽运算 / Apply Black-Hat operation
# 黑帽 = 闭运算 - 原图 / Black-Hat = Closing - Original
blackhat_np = cv_lite.rgb888_blackhat(
    image_shape,
    img_np,
    kernel_size,
    iterations,
    threshold_value
)

# 构造图像对象并显示 / Wrap result as image and display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=blackhat_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| kernel_size | Kernel size, int type | Input |  |
| iterations | Number of black-hat iterations, int type | Input |  |
| threshold_value | Binarization threshold, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| blackhat_np | Image data after black-hat operation, ulab.numpy.ndarray type |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_blackhat.py`, please open and run it in K230 CanMV IDE.

### rgb888_gradient

**Description**

Performs morphological gradient operation on an RGB888 image, returning single-channel ulab.numpy.ndarray image data after morphological gradient, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640] # height, width

# ================================
# 梯度操作参数 / Morphological Gradient parameters
# ================================
kernel_size = 3        # 卷积核尺寸（建议奇数）/ Kernel size (recommended odd)
iterations = 1         # 形态学迭代次数 / Morphology iterations
threshold_value = 100  # 二值化阈值（0=使用 Otsu 自动阈值）/ Threshold value (0=use Otsu)

# 获取图像并转为 ndarray / Capture image and convert to ndarray
img = sensor.snapshot()
img_np = img.to_numpy_ref()

# 调用梯度操作（Gradient = 膨胀 - 腐蚀）/ Call morphological gradient (dilate - erode)
gradient_np = cv_lite.rgb888_gradient(image_shape, img_np, kernel_size, iterations, threshold_value)

# 构造灰度图像用于显示 / Construct grayscale image for display
img_out = image.Image(image_shape[1], image_shape[0], image.GRAYSCALE,
                        alloc=image.ALLOC_REF, data=gradient_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| kernel_size | Kernel size, int type | Input |  |
| iterations | Number of morphological iterations, int type | Input |  |
| threshold_value | Binarization threshold, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| gradient_np | Image data after morphological gradient, ulab.numpy.ndarray type |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_gradient.py`, please open and run it in K230 CanMV IDE.

### rgb888_mean_blur

**Description**

Performs mean blur on an RGB888 image, returning the ulab.numpy.ndarray image data after blurring, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640] # height, width

# -------------------------------
# 均值模糊核大小 / Mean blur kernel size
# 必须为奇数，例如 3 / 5 / 7 / Must be odd: 3, 5, 7, etc.
# -------------------------------
kernel_size = 3

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 图像引用 / Get RGB888 ndarray (HWC)

# 应用均值模糊滤波 / Apply mean blur using cv_lite
mean_blur_np = cv_lite.rgb888_mean_blur_fast(
    image_shape,
    img_np,
    kernel_size
)

# 构造图像用于显示 / Wrap processed image for display
img_out = image.Image(image_shape[1], image_shape[0], image.RGB888,
                        alloc=image.ALLOC_REF, data=mean_blur_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| kernel_size | Kernel size, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| mean_blur_np | Image data after mean blur, ulab.numpy.ndarray type |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_mean_blur.py`, please open and run it in K230 CanMV IDE.

### rgb888_gaussian_blur

**Description**

Performs Gaussian blur on an RGB888 image, returning the ulab.numpy.ndarray image data after blurring, which can be used to create an image instance for display.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite
import image

image_shape = [480,640] # height, width

# -------------------------------
# 高斯滤波核大小 / Gaussian blur kernel size
# 必须为奇数，例如 3 / 5 / 7 / Must be odd: 3, 5, 7, etc.
# -------------------------------
kernel_size = 3

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 图像引用 / Get RGB888 ndarray (HWC)

# 应用高斯模糊滤波 / Apply gaussian blur using cv_lite
gaussian_blur_np = cv_lite.rgb888_gaussian_blur_fast(
    image_shape,
    img_np,
    kernel_size
)

# 构造图像用于显示 / Wrap processed image for display
img_out = image.Image(image_shape[1], image_shape[0], image.RGB888,
                        alloc=image.ALLOC_REF, data=gaussian_blur_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, in the order of [height, width], e.g., [480,640] | Input |  |
| img_np | Image data reference, ulab.numpy.ndarray type | Input |  |
| kernel_size | Kernel size, int type | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| gaussian_blur_np | Image data after Gaussian blur, ulab.numpy.ndarray type |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_gaussian_blur.py`, please open and run it in K230 CanMV IDE.

### rgb888_calc_histogram

**Description**

Calculates the histogram of an RGB888 image, returning the histogram data.

**Syntax**  

```python
import cv_lite

# 拍摄一帧图像 / Capture a frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 图像引用 / Get RGB888 ndarray reference (HWC)

# 使用 cv_lite 计算 RGB 直方图（返回 shape 为 3x256 的数组）
# Calculate RGB888 histogram using cv_lite (3x256 array)
hist = cv_lite.rgb888_calc_histogram(image_shape, img_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, including width and height, e.g., [1920,1080] | Input |  |
| img_np | Image data reference | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| hist | Histogram data |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_calc_histogram.py`, please open and run it in K230 CanMV IDE.

### rgb888_find_corners

**Description**

Finds corners in an RGB888 image, returning the coordinates of the corners.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite

image_shape = [240,320] # height, width

# -------------------------------
# 可调参数（建议调试时调整）/ Adjustable parameters (recommended for tuning)
# -------------------------------
max_corners       = 20        # 最大角点数 / Maximum number of corners
quality_level     = 0.01      # Shi-Tomasi质量因子 / Corner quality factor (0.01 ~ 0.1)
min_distance      = 20.0      # 最小角点距离 / Minimum distance between corners

# 拍摄当前帧图像 / Capture current frame
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 ndarray 引用 / Get RGB888 ndarray reference

# 调用角点检测函数，返回角点数组 [x0, y0, x1, y1, ...]
corners = cv_lite.rgb888_find_corners(
    image_shape, img_np,
    max_corners,
    quality_level,
    min_distance
)

# 遍历角点数组，绘制角点 / Draw detected corners
for i in range(0, len(corners), 2):
    x = corners[i]
    y = corners[i + 1]
    img.draw_circle(x, y, 3, color=(0, 255, 0), fill=True)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, including width and height, e.g., [240,320] | Input |  |
| img_np | Image data reference | Input |  |
| max_corners | Maximum number of corners | Input |  |
| quality_level | Shi-Tomasi quality factor | Input |  |
| min_distance | Minimum distance | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| corners | Array of corner coordinates, every two numbers represent the coordinates of a corner, e.g., [x0,y0,x1,y1,...] |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_find_corners.py`, please open and run it in K230 CanMV IDE.

### rgb888_undistort

**Description**

Performs distortion correction on an RGB888 image using camera calibration parameters and distortion coefficients. Three methods are provided, including default distortion correction, fast distortion correction, and optimized camera matrix distortion correction.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480,640] # height, width

# -------------------------------
# 相机内参与畸变系数 / Camera intrinsics & distortion
# -------------------------------
camera_matrix = [1601.79998, 0.0, 960.2537,0.0, 1600.6784, 496.5050,0.0, 0.0, 1.0]
dist_coeffs = [0.16096, -0.73425, -0.01634, -0.00896, 0.41294]
dist_len=len(dist_coeffs)

# 获取图像帧
img = sensor.snapshot()
img_np = img.to_numpy_ref()  # 获取 RGB888 图像 ndarray 引用 (HWC)

# 畸变校正
result_np = cv_lite.rgb888_undistort(image_shape,img_np,camera_matrix,dist_coeffs,dist_len)
# 快速畸变校正
# result_np = cv_lite.rgb888_undistort_fast(image_shape,img_np,camera_matrix,dist_coeffs,dist_len)
# 带优化相机矩阵畸变校正
# result_np = cv_lite.rgb888_undistort_new_cam_mat(image_shape,img_np,camera_matrix,dist_coeffs,dist_len)

# 构造图像对象用于显示
img_out = image.Image(image_shape[1], image_shape[0], image.RGB888,
                        alloc=image.ALLOC_REF, data=result_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, including width and height, e.g., [480,640] | Input |  |
| img_np | Image data reference | Input |  |
| camera_matrix | Camera intrinsic matrix | Input |  |
| dist_coeffs | Distortion coefficients | Input |  |
| dist_len | Length of distortion coefficients | Input |  |

**Return Value**  

| Return Value | Description                            |
|--------|---------------------------------|
| result_np | Image data after distortion correction, ulab.numpy.ndarray format, can create image instance on this data |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_undistort.py`, please open and run it in K230 CanMV IDE.

### rgb888_pnp_distance

**Description**

Given the real-world dimensions of the ROI region and its corresponding projected position in the image, combined with the camera intrinsics, the relative position between the camera and the object can be estimated, especially the distance Z.

**Syntax**  

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480, 640]  # 图像高 x 宽 / Height x Width

# -------------------------------
# 相机内参与畸变系数 / Camera intrinsics and distortion
# -------------------------------
camera_matrix = [
    1601.79998, 0.0, 960.2537,
    0.0, 1600.6784, 496.5050,
    0.0, 0.0, 1.0
]
dist_coeffs = [0.16096, -0.73425, -0.01634, -0.00896, 0.41294]
dist_len = len(dist_coeffs)
# 实际 ROI 尺寸（单位：厘米）/ Real-world size of detected ROI (cm)
roi_width_real = 3.0     # 例如：色块宽 3cm / Blob width in real world
roi_height_real = 3.0    # 例如：色块高 3cm / Blob height in real world
roi = [200, 200, 300, 300] # xywh，可以换成检测到的区域

img = sensor.snapshot()          # 拍摄一帧 / Capture one frame
img_np = img.to_numpy_ref()      # 获取图像 NumPy 引用 / Get NumPy reference to RGB data

# 色块检测：返回多个色块 [x, y, w, h, ...] / Detect color blobs
blobs = cv_lite.rgb888_find_blobs(image_shape, img_np, threshold, min_area, kernel_size)

# 使用 PnP 估算距离 / Estimate distance via PnP
distance = cv_lite.rgb888_pnp_distance(
    image_shape, img_np, roi,
    camera_matrix, dist_coeffs, dist_len,
    roi_width_real, roi_height_real
)

# 绘制矩形与距离文字 / Draw bounding box and distance text
img.draw_rectangle(roi[0], roi[1], roi[2], roi[3], color=(255, 0, 0), thickness=2)
img.draw_string_advanced(roi[0], roi[1] - 30, 32, str(distance), color=(255, 0, 0))

```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, including width and height, e.g., [480,640] | Input |  |
| img_np | Image data reference | Input |  |
| roi | ROI region for distance estimation, list type, including xywh | Input |  |
| camera_matrix | Camera intrinsic matrix | Input |  |
| dist_coeffs | Distortion coefficients | Input |  |
| dist_len | Length of distortion coefficients | Input |  |
| roi_width_real | Actual ROI width, unit cm | Input |  |
| roi_height_real | Actual ROI height, unit cm | Input |  |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| distance | Estimated distance, unit cm |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_pnp_distance.py`, please open and run it in K230 CanMV IDE.

### rgb888_pnp_distance_from_corners

**Description**

The method rgb888_pnp_distance_from_corners implements automatic recognition and distance estimation of rectangular targets based on RGB888 images: it first performs distortion correction and edge detection on the image, extracts the largest rectangular contour and calculates its four corner points, then combines the actual target size and camera calibration parameters to solve the 3D distance from the target to the camera through the PnP algorithm, and finally returns the straight-line distance (in cm) between the target and the camera, the minimum bounding rectangle and corner information.

**Syntax**

Please ensure that the Sensor is configured to output an RGB888 image, otherwise errors will occur.

```python
import cv_lite

image_shape = [480, 640]  # 图像高 x 宽 / Height x Width

# -------------------------------
# 相机参数
# -------------------------------
camera_matrix = [
    789.1207591978101,0.0,308.8211709453399,
    0.0,784.6402477892891,220.80604393744628,
    0.0,0.0,1.0
]
dist_coeffs = [-0.0032975761115662697,-0.009984467065645562,-0.01301691382446514,-0.00805834837844004,-1.063818733754765]
dist_len = len(dist_coeffs)

# -------------------------------
# 目标实际尺寸（单位 cm）
# -------------------------------
obj_width_real = 20.1
obj_height_real = 28.9

# 获取一帧RGB888图像
img = sensor.snapshot()
# 处理成ulab.numpy.ndarray格式
img_np = img.to_numpy_ref()

# 距离估计（通过轮廓+PnP）返回格式[distance,[x,y,w,h],[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]]
res = cv_lite.rgb888_pnp_distance_from_corners(
    image_shape, img_np,
    camera_matrix, dist_coeffs, dist_len,
    obj_width_real, obj_height_real
)
# 距离
distance=res[0]
# 最小外接矩形xywh
rect=res[1]
# 矩形角点坐标
corners=res[2]

# 如果距离估计成功
if distance > 0:
    img.draw_string_advanced(10, 10, 32, "Dist: %.2fcm" % distance, color=(0, 255, 0))
    img.draw_rectangle(rect[0], rect[1], rect[2], rect[3], color=(255, 0, 0), thickness=2)
    img.draw_cross(corners[0][0],corners[0][1],color=(255,255,255),size=5,thickness=2)
    img.draw_cross(corners[1][0],corners[1][1],color=(255,255,255),size=5,thickness=2)
    img.draw_cross(corners[2][0],corners[2][1],color=(255,255,255),size=5,thickness=2)
    img.draw_cross(corners[3][0],corners[3][1],color=(255,255,255),size=5,thickness=2)
else:
    img.draw_string_advanced(10, 10, 32, "No Rect Found", color=(255, 0, 0))

```

**Parameters**

| Parameter Name | Description                          | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| image_shape | Image shape, list type, including width and height, e.g., [480,640] | Input |  |
| img_np | Image data reference | Input |  |
| camera_matrix | Camera intrinsic matrix | Input |  |
| dist_coeffs | Distortion coefficients | Input |  |
| dist_len | Length of distortion coefficients | Input |  |
| roi_width_real | Actual width, unit cm | Input |  |
| roi_height_real | Actual height, unit cm | Input |  |

**Return Value**

| Return Value | Description                            |
|--------|---------------------------------|
| res | res[0] estimated distance, unit cm, res[1] minimum bounding rectangle xywh, res[2] rectangle corner coordinates |

**Example**

The provided example is located at `/sdcard/examples/23-CV_Lite/rgb888_pnp_distance_from_corners.py`, please open and run it in K230 CanMV IDE.

### grayscale_find_lines

**Description**

Grayscale image line detection. First performs Gaussian blurring and Canny edge detection, then extracts line segments using the probabilistic Hough transform.

**Syntax**

```python
lines = cv_lite.grayscale_find_lines(image_shape, img_np, canny_thresh1, canny_thresh2,
                                     gaussian_blur_size, rho, theta, hough_thresh,
                                     min_line_length, max_line_gap)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | image_shape | Image resolution `[height, width]` | list[int] |
| 2 | img_np | Grayscale image data | ndarray(uint8) |
| 3 | canny_thresh1 | Canny low threshold | int |
| 4 | canny_thresh2 | Canny high threshold | int |
| 5 | gaussian_blur_size | Gaussian blur kernel size; must be a positive odd number | int |
| 6 | rho | Hough transform distance resolution, in pixels; typically set to 1.0 | float |
| 7 | theta | Hough transform angle resolution, in radians; typically set to `math.pi/180` | float |
| 8 | hough_thresh | Hough accumulator threshold; a larger value detects fewer and more reliable lines | int |
| 9 | min_line_length | Minimum line segment length; segments shorter than this value are discarded | float |
| 10 | max_line_gap | Maximum allowed gap between two segments on the same line | float |

**Return Value**

| Return Value | Description |
|--------|------|
| list[int] | Line segment endpoints stored in a flat list, with every 4 values forming a group `[x1, y1, x2, y2]`. Returns an empty list when no lines are detected |

### rgb888_find_lines

**Description**

Line detection in RGB888 images. The image is first converted to grayscale internally; the remaining process is identical to `grayscale_find_lines`.

**Syntax**

```python
lines = cv_lite.rgb888_find_lines(image_shape, img_np, canny_thresh1, canny_thresh2,
                                  gaussian_blur_size, rho, theta, hough_thresh,
                                  min_line_length, max_line_gap)
```

**Parameters**: Exactly the same as `grayscale_find_lines`, except that the second parameter is changed to RGB888 data (HWC layout).

**Return Value**: The same as `grayscale_find_lines`.

### grayscale_find_lines_sobel

**Description**

The Sobel version of grayscale line detection. It uses the Sobel operator instead of Canny to generate an edge map, followed by a probabilistic Hough transform. Compared with Canny, it requires only one threshold, making the parameters easier to tune, and it is also faster in scenarios with uniform lighting.

**Syntax**

```python
lines = cv_lite.grayscale_find_lines_sobel(image_shape, img_np, sobel_thresh,
                                           gaussian_blur_size, rho, theta,
                                           hough_thresh, min_line_length, max_line_gap)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | image_shape | Image resolution `[height, width]` | list[int] |
| 2 | img_np | Grayscale image data | ndarray(uint8) |
| 3 | sobel_thresh | Binarization threshold for the Sobel edge map | int |
| 4 | gaussian_blur_size | Gaussian blur kernel size; must be a positive odd number | int |
| 5 | rho | Distance resolution, in pixels | float |
| 6 | theta | Angular resolution, in radians | float |
| 7 | hough_thresh | Hough accumulator threshold | int |
| 8 | min_line_length | Minimum line segment length | float |
| 9 | max_line_gap | Maximum allowed gap between two segments on the same line | float |

**Return Value**: The same as `grayscale_find_lines`.

### grayscale_find_lines_raw

**Description**

The raw Hough transform version of grayscale line detection. It performs a standard Hough transform directly on the Sobel edge map and uses `x_stride` / `y_stride` to subsample pixels to reduce computational cost, making it suitable for scenarios with high speed requirements and distinct lines.

**Syntax**

```python
lines = cv_lite.grayscale_find_lines_raw(image_shape, img_np, x_stride, y_stride,
                                         sobel_thresh, rho_step, theta_step, hough_thresh)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | image_shape | Image resolution `[height, width]` | list[int] |
| 2 | img_np | Grayscale image data | ndarray(uint8) |
| 3 | x_stride | Horizontal pixel sampling stride; a larger value is faster but less accurate | int |
| 4 | y_stride | Vertical pixel sampling stride | int |
| 5 | sobel_thresh | Binarization threshold for the Sobel edge map | int |
| 6 | rho_step | Distance step, in pixels | float |
| 7 | theta_step | Angular step, in radians | float |
| 8 | hough_thresh | Hough accumulator threshold | int |

**Return Value**: The same as `grayscale_find_lines`.

### grayscale_find_lines_no_hough

**Description**

Line detection without using the Hough transform. First, Canny edge detection is performed, then contours are extracted and line fitting is applied to sufficiently long contours. The Hough transform is expensive when there are many edge points. This interface is significantly faster in scenarios with sparse edges, but is less robust than the Hough transform for broken lines.

**Syntax**

```python
lines = cv_lite.grayscale_find_lines_no_hough(image_shape, img_np, canny_thresh1,
                                              canny_thresh2, gaussian_blur_size,
                                              min_contour_len)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | image_shape | Image resolution `[height, width]` | list[int] |
| 2 | img_np | Grayscale image data | ndarray(uint8) |
| 3 | canny_thresh1 | Canny low threshold | int |
| 4 | canny_thresh2 | Canny high threshold | int |
| 5 | gaussian_blur_size | Gaussian blur kernel size; must be a positive odd number | int |
| 6 | min_contour_len | Minimum contour length included in line fitting | float |

**Return value**: The same as `grayscale_find_lines`.

### grayscale_find_corners

**Description**

Corner detection in grayscale images (Shi-Tomasi).

**Syntax**

```python
corners = cv_lite.grayscale_find_corners(image_shape, img_np, max_corners,
                                         quality_level, min_distance)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | image_shape | Image resolution `[height, width]` | list[int] |
| 2 | img_np | Grayscale image data | ndarray(uint8) |
| 3 | max_corners | Maximum number of corners to return | int |
| 4 | quality_level | Lower bound on corner quality, relative to the strongest corner, typically 0.01~0.1 | float |
| 5 | min_distance | Minimum pixel distance between two corners | float |

**Return Value**

| Return Value | Description |
|--------|------|
| list[int] | Flattened corner coordinates, with every 2 values forming a group `[x, y]` |

### rgb888_find_corners_fast

**Description**

An accelerated version of RGB888 image corner detection. Its parameters are consistent with [`rgb888_find_corners`](#rgb888_find_corners). It uses a faster implementation internally, with slightly reduced accuracy.

**Syntax**

```python
corners = cv_lite.rgb888_find_corners_fast(image_shape, img_np, max_corners,
                                           quality_level, min_distance)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | image_shape | Image resolution `[height, width]` | list[int] |
| 2 | img_np | RGB888 data in HWC layout | ndarray(uint8) |
| 3 | max_corners | Maximum number of corners to return | int |
| 4 | quality_level | Lower limit for corner quality | float |
| 5 | min_distance | Minimum pixel distance between two corners | float |

**Return Value**

| Return Value | Description |
|--------|------|
| list[int] | Flattened corner coordinates, with every 2 values forming a group `[x, y]` |

### rgb888_denoise

**Description**

RGB888 image denoising, providing four algorithms.

**Syntax**

```python
out = cv_lite.rgb888_denoise(image_shape, img_np, method, strength)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | image_shape | Image resolution `[height, width]` | list[int] |
| 2 | img_np | RGB888 data in HWC layout | ndarray(uint8) |
| 3 | method | Denoising algorithm; see the table below for available values | int |
| 4 | strength | Denoising strength, corresponding to the filter kernel size; must be a positive odd number | int |

| method | Algorithm | Characteristics |
|--------|------|------|
| 0 | Mean blur | Fastest, with average results |
| 1 | Gaussian blur | Softer edges |
| 2 | Median filter | Particularly effective against salt-and-pepper noise |
| 3 | Bilateral filter | Best edge preservation, slowest |

**Return Value**

| Return Value | Description |
|--------|------|
| ndarray(uint8) | Denoised RGB888 data |

### rgb888_denoise_fast

**Description**

An accelerated version of `rgb888_denoise`. The meaning of the `method` values remains the same. It replaces OpenCV with custom fixed-point arithmetic, making it faster with slightly different results.

**Syntax**

```python
out = cv_lite.rgb888_denoise_fast(image_shape, img_np, method, strength)
```

**Parameters**: The same as `rgb888_denoise`.

**Return Value**

| Return Value | Description |
|--------|------|
| ndarray(uint8) | Denoised RGB888 data |

### rgb888_white_balance_gray_world_adjustable

**Description**

Intensity-adjustable gray-world white balance. Unlike the full correction of `rgb888_white_balance_gray_world_fast`, this interface uses `alpha` to control the correction strength, making it easier to strike a balance between "color cast" and "overcorrection".

**Syntax**

```python
out = cv_lite.rgb888_white_balance_gray_world_adjustable(image_shape, img_np, alpha)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | image_shape | Image resolution `[height, width]` | list[int] |
| 2 | img_np | RGB888 data in HWC layout | ndarray(uint8) |
| 3 | alpha | Correction strength; 0 means no correction, and 1 means full correction according to the gray-world assumption | float [0~1] |

**Return Value**

| Return Value | Description |
|--------|------|
| ndarray(uint8) | White-balanced RGB888 data |

### rgb888_perspective_transform

**Description**

Perspective transform. Rectifies a quadrilateral region in an image into a rectangular output, commonly used to straighten documents, license plates, or signs captured at an angle.

**Syntax**

```python
out = cv_lite.rgb888_perspective_transform(image_shape, img_np, roi, dst_pts,
                                           out_width, out_height)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | image_shape | Image resolution `[height, width]` | list[int] |
| 2 | img_np | RGB888 data in HWC layout | ndarray(uint8) |
| 3 | roi | Region of interest `[x, y, width, height]` | list[int] |
| 4 | dst_pts | Four vertices of the source quadrilateral `[x1, y1, x2, y2, x3, y3, x4, y4]` | list[int] |
| 5 | out_width | Output image width; must be positive | int |
| 6 | out_height | Output image height; must be positive | int |

**Return Value**

| Return Value | Description |
|--------|------|
| ndarray(uint8) | Rectified result with shape `[1, out_height, out_width, 3]` |

```{admonition} Note
:class: warning
A `ValueError: output shape must be positive` is raised when `out_width` or `out_height` is not positive; an `OverflowError: output image too large` is raised when the output size is too large.
```

### save_image

**Description**

Save RGB888 data as an image file, with the format determined by the file extension (such as `.jpg` and `.png`).

**Syntax**

```python
cv_lite.save_image("/sdcard/out.jpg", image_shape, img_np)
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | save_path | Save path | str |
| 2 | image_shape | Image resolution `[height, width]` | list[int] |
| 3 | img_np | RGB888 data in HWC layout | ndarray(uint8) |

**Return value**: None.

### load_image

**Description**

Reads an image from a file and returns a `ulab.numpy.ndarray`, which can be passed directly to other `cv_lite` interfaces or AI preprocessing.

**Syntax**

```python
img_np = cv_lite.load_image("/sdcard/test.jpg")
```

**Parameters**

| No. | Parameter Name | Description | Type |
|------|----------|------|------|
| 1 | file_path | Image file path | str |

**Return Value**

| Return Value | Description |
|--------|------|
| ndarray(uint8) | Image data with shape `[1, height, width, channel]`. The returned data is an independent copy and is not associated with the file |

## Optimization Comparison

On the premise that the input is at the same resolution, the above-mentioned methods and the openmv method are compared: openmv processes RGB565 color images, while cv_lite processes RGB888 color images. The processing efficiency comparison yields the frame rate results shown in the table below. The frame rates below are only compared when processing a fixed scene. The actual frame rate will be affected by the complexity of the scene, such as the number of circles, etc. Please test with your specific scene as the reference.

| Task | Input Resolution | cv_lite Processing Frame Rate (fps) | openmv Processing Frame Rate (fps) |
|------|------------|----------------|----------------|
| Grayscale find_blobs | 480x640 | 90 |57|
| Color find_blobs | 480x640 | 80  |44|
| Grayscale find_circles | 480x640 | 24 | 1.2 |
| Color find_circles | 480x640 | 24 | 1.2 |
| Grayscale find_rectangles | 480x640 | 40 | 8 |
| Color find_rectangles | 480x640 | 38 | 4.6 |
| Grayscale find_edges | 480x640 | 57 | 11 |
| Color find_edges | 480x640 | 53 | Only supports grayscale |
| Grayscale binarization | 480x640 | 90 | 90 |
| Color binarization | 480x640 | 90 | 40 |
| Color mean filtering | 480x640 | 26 | 19 |
| Color Gaussian filtering | 480x640 | 12 | 4 |

In addition to the above optimizations, cv_lite also adds interfaces implemented using software processing for morphological operations on RGB888 images, white balance, exposure adjustment, and RGB888 image histogram statistics:

| Task | Input Resolution | cv_lite Processing Frame Rate (fps) |
|------|------------|----------------|
| Erosion | 480x640 | 90 |
| Dilation | 480x640 | 32 |
| Opening operation | 480x640 | 31 |
| Closing operation | 480x640 | 32 |
| Morphological gradient | 480x640 | 12 |
| Top-hat transform | 480x640 | 12 |
| Black-hat transform | 480x640 | 12 |
| Gray world white balance | 480x640 | 47 |
| White patch white balance| 480x640 | 22 |
| Exposure adjustment | 480x640 | 65 |
| RGB888 image histogram statistics | 480x640 | 77 |

```{admonition} Note
The above methods serve as a supplement to openmv, optimizing some common image processing tasks as much as possible. However, these modules cannot replace the openmv image module. You can combine the two modules based on your specific task.
```
