# OpenCV API 手册

`cv2` 模块提供了 OpenCV 计算机视觉库的 MicroPython 绑定，支持图像 I/O、滤波、形态学、阈值、颜色空间转换、几何变换、绘图、轮廓分析、模板匹配、霍夫变换、直方图、角点检测、图像分割等经典计算机视觉功能。

图像数据使用 `ulab.numpy` 的 `ndarray` 表示，与 `image.Image` 对象可通过 `image.Image.to_numpy_ref()` 方法互转。

```python
import cv2
from ulab import numpy as np
```

## 函数列表

### imgcodecs — 图像读写（4 个）

| 函数 | 说明 |
|------|------|
| `imread` | 从文件读取图像 |
| `imwrite` | 将图像保存到文件 |
| `imdecode` | 从内存缓冲区解码图像 |
| `imencode` | 将图像编码到内存缓冲区 |

### core — 核心运算（23 个）

| 函数 | 说明 |
|------|------|
| `add` | 逐元素加法 |
| `subtract` | 逐元素减法 |
| `multiply` | 逐元素乘法 |
| `divide` | 逐元素除法 |
| `addWeighted` | 两图像加权混合：`alpha·src1 + beta·src2 + gamma` |
| `absdiff` | 两图像逐元素绝对差 |
| `bitwise_and` | 逐位与运算 |
| `bitwise_or` | 逐位或运算 |
| `bitwise_xor` | 逐位异或运算 |
| `bitwise_not` | 逐位取反运算 |
| `split` | 拆分多通道图像为单通道列表 |
| `merge` | 合并单通道列表为多通道图像 |
| `mean` | 计算各通道均值 |
| `normalize` | 归一化图像数值范围 |
| `compare` | 逐元素比较两图像，返回二值掩码 |
| `inRange` | 颜色范围过滤，返回二值掩码 |
| `convertScaleAbs` | 缩放取绝对值后转为 8 位 |
| `minMaxLoc` | 查找最小/最大值及其位置 |
| `LUT` | 查找表映射变换 |
| `countNonZero` | 统计非零像素个数 |
| `flip` | 图像翻转（垂直/水平/对角线） |
| `rotate` | 图像旋转（90°/180°/270°） |
| `transpose` | 矩阵转置 |

### imgproc — 图像处理（65 个）

**图像滤波**

| 函数 | 说明 |
|------|------|
| `Canny` | Canny 边缘检测 |
| `GaussianBlur` | 高斯模糊 |
| `blur` | 均值模糊（盒式滤波） |
| `medianBlur` | 中值模糊 |
| `bilateralFilter` | 双边滤波（保边去噪） |
| `boxFilter` | 方框滤波 |
| `filter2D` | 自定义卷积核滤波 |
| `Sobel` | Sobel 边缘检测（一阶导数） |
| `Scharr` | Scharr 边缘检测（比 Sobel 精度更高） |
| `Laplacian` | 拉普拉斯边缘检测（二阶导数） |

**形态学**

| 函数 | 说明 |
|------|------|
| `erode` | 腐蚀操作 |
| `dilate` | 膨胀操作 |
| `morphologyEx` | 高级形态学（开/闭/梯度/顶帽/黑帽） |
| `getStructuringElement` | 获取结构元素（矩形/十字/椭圆） |

**阈值**

| 函数 | 说明 |
|------|------|
| `threshold` | 全局阈值分割（支持 OTSU / Triangle） |
| `adaptiveThreshold` | 自适应阈值分割（均值/高斯） |

**颜色转换**

| 函数 | 说明 |
|------|------|
| `cvtColor` | 颜色空间转换（BGR↔GRAY/HSV/LAB/YUV 等 23 种） |

**几何变换**

| 函数 | 说明 |
|------|------|
| `resize` | 图像缩放 |
| `warpAffine` | 仿射变换 |
| `warpPerspective` | 透视变换 |
| `getRotationMatrix2D` | 获取 2D 旋转矩阵 |
| `getAffineTransform` ⚠ | 从三对点计算仿射变换矩阵 |
| `getPerspectiveTransform` ⚠ | 从四对点计算透视变换矩阵 |
| `remap` | 像素重映射 |

**金字塔**

| 函数 | 说明 |
|------|------|
| `pyrDown` | 高斯金字塔降采样（尺寸减半） |
| `pyrUp` | 高斯金字塔升采样（尺寸加倍） |

**绘图**

| 函数 | 说明 |
|------|------|
| `line` | 绘制直线 |
| `rectangle` | 绘制矩形 |
| `circle` | 绘制圆形 |
| `ellipse` | 绘制椭圆/弧 |
| `putText` | 绘制文字（支持 8 种 Hershey 字体） |
| `arrowedLine` | 绘制带箭头的线段 |
| `drawMarker` | 绘制标记点（十字/星形/菱形等 7 种） |
| `fillPoly` | 填充多边形 |
| `polylines` | 绘制多边形边框 |
| `getTextSize` | 获取文字渲染尺寸及基线 |

**轮廓**

| 函数 | 说明 |
|------|------|
| `findContours` | 查找二值图像中的轮廓 |
| `drawContours` | 绘制轮廓 |
| `contourArea` | 计算轮廓面积 |
| `arcLength` | 计算轮廓周长 |
| `boundingRect` | 计算外接正矩形 |
| `approxPolyDP` | 多边形逼近 |
| `convexHull` | 计算凸包（支持返回点坐标或索引） |
| `minAreaRect` | 最小外接旋转矩形 |
| `minEnclosingCircle` | 最小外接圆 |
| `fitEllipse` | 拟合椭圆（需 ≥5 个点） |
| `fitLine` | 拟合直线 |
| `pointPolygonTest` | 点与轮廓位置关系测试 |
| `convexityDefects` | 计算凸包缺陷 |
| `matchShapes` | 形状匹配（基于 Hu 矩） |
| `isContourConvex` | 判断轮廓是否为凸 |

**模板匹配 & 矩**

| 函数 | 说明 |
|------|------|
| `matchTemplate` | 模板匹配（6 种匹配方法） |
| `moments` | 计算图像矩（空间矩/中心矩/归一化矩） |

**霍夫变换**

| 函数 | 说明 |
|------|------|
| `HoughLines` | 标准霍夫直线检测 |
| `HoughLinesP` | 概率霍夫直线检测（返回线段端点） |
| `HoughCircles` | 霍夫圆检测（梯度法） |

**直方图**

| 函数 | 说明 |
|------|------|
| `calcHist` | 计算图像直方图 |
| `calcBackProject` | 直方图反向投影 |
| `compareHist` | 直方图比较（6 种比较方法） |
| `equalizeHist` | 直方图均衡化 |

**角点检测**

| 函数 | 说明 |
|------|------|
| `cornerHarris` | Harris 角点检测 |
| `goodFeaturesToTrack` | Shi-Tomasi 角点检测 |
| `cornerSubPix` ⚠ | 亚像素角点精确定位 |

**分割**

| 函数 | 说明 |
|------|------|
| `watershed` | 分水岭分割 |
| `distanceTransform` | 距离变换 |
| `floodFill` | 漫水填充 |
| `grabCut` ⚠ | GrabCut 前景分割 |
| `connectedComponents` | 连通组件标记 |

### highgui — 交互（2 个）

| 函数 | 说明 |
|------|------|
| `waitKey` | 等待按键（支持超时） |
| `waitKeyEx` | 增强版 waitKey |

> **总计 94 个函数**。⚠ 表示平台限制：`getAffineTransform` / `getPerspectiveTransform` / `grabCut` 默认 128KB 线程栈下可能溢出；`cornerSubPix` 此移植版 OpenCV 的 `InputOutputArray` 包装路径不兼容。

## imgcodecs — 图像读写

### `imread`

从文件读取图像。

```python
img = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `filename` | `str` | 图像文件路径，支持 BMP、PNG、JPEG 等格式 |
| `flags` | `int` | 读取模式（见常量表），默认为 `IMREAD_COLOR` |

**返回值**: `ndarray`，读取失败返回 `None`。

示例：

```python
img = cv2.imread("/sdcard/photo.jpg")
gray = cv2.imread("/sdcard/photo.jpg", cv2.IMREAD_GRAYSCALE)
```

### `imwrite`

将图像保存到文件。

```python
success = cv2.imwrite(filename, img)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `filename` | `str` | 保存路径，扩展名决定格式（如 `.png`, `.jpg`） |
| `img` | `ndarray` | 图像数组 |

**返回值**: `bool`，成功返回 `True`。

示例：

```python
img = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.imwrite("/sdcard/output.png", img)
```

### `imdecode`

从内存缓冲区解码图像。

```python
img = cv2.imdecode(buf, flags=cv2.IMREAD_COLOR)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `buf` | `bytes` | 图像数据的字节缓冲区 |
| `flags` | `int` | 解码模式，同 `imread` |

**返回值**: `ndarray`，解码失败返回 `None`。

### `imencode`

将图像编码到内存缓冲区。

```python
success, buf = cv2.imencode(ext, img, params=None)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `ext` | `str` | 图像格式扩展名，如 `".jpg"`, `".png"` |
| `img` | `ndarray` | 待编码的图像 |
| `params` | `list` | 可选，编码参数列表 `[param_id, val, ...]`，如 `[1, 50]` 表示 JPEG 质量 50 |

**返回值**: `(bool, bytes)` 元组。`success` 表示是否编码成功，`buf` 为编码后的字节数据。

示例：

```python
success, buf = cv2.imencode(".jpg", img, [1, 50])  # JPEG quality=50
decoded = cv2.imdecode(buf, cv2.IMREAD_COLOR)
```

### 图像读写常量

| 常量 | 值 | 说明 |
|------|------|------|
| `IMREAD_UNCHANGED` | -1 | 保持原始格式 |
| `IMREAD_GRAYSCALE` | 0 | 转为灰度图 |
| `IMREAD_COLOR` | 1 | 转为 BGR 彩色图 |
| `IMREAD_ANYDEPTH` | 2 | 保留原始位深 |
| `IMREAD_ANYCOLOR` | 4 | 保留原始通道数 |
| `IMREAD_IGNORE_ORIENTATION` | 128 | 忽略 EXIF 方向标记 |

## core — 核心运算

### 算术运算

#### `add`

两图像或图像与标量的逐元素加法。

```python
dst = cv2.add(src1, src2, dst=None, mask=None, dtype=-1)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `src1` | `ndarray` | 第一个输入图像 |
| `src2` | `ndarray` | 第二个输入图像（或标量 ndarray） |
| `dst` | `ndarray` | 可选，输出图像 |
| `mask` | `ndarray` | 可选，8 位单通道掩码 |
| `dtype` | `int` | 可选，输出深度（-1 表示与 src1 相同） |

**返回值**: `ndarray`。

#### `subtract`

逐元素减法。

```python
dst = cv2.subtract(src1, src2, dst=None, mask=None, dtype=-1)
```

参数同 `add`。

#### `multiply`

逐元素乘法。

```python
dst = cv2.multiply(src1, src2, dst=None, scale=None, dtype=-1)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `scale` | `float` | 可选，缩放因子，默认为 1.0 |

#### `divide`

逐元素除法。

```python
dst = cv2.divide(src1, src2, dst=None, scale=None, dtype=-1)
```

#### `addWeighted`

两图像加权混合。

```python
dst = cv2.addWeighted(src1, alpha, src2, beta, gamma, dst=None, dtype=-1)
```

计算公式：`dst = alpha * src1 + beta * src2 + gamma`

| 参数 | 类型 | 说明 |
|------|------|------|
| `src1` | `ndarray` | 第一个输入 |
| `alpha` | `float` | 第一个输入的权重 |
| `src2` | `ndarray` | 第二个输入 |
| `beta` | `float` | 第二个输入的权重 |
| `gamma` | `float` | 加到每个和上的标量 |

```python
result = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)
```

#### `absdiff`

计算两图像逐元素绝对差。

```python
dst = cv2.absdiff(src1, src2, dst=None)
```

### 位运算

#### `bitwise_and`

```python
dst = cv2.bitwise_and(src1, src2, dst=None, mask=None)
```

#### `bitwise_or`

```python
dst = cv2.bitwise_or(src1, src2, dst=None, mask=None)
```

#### `bitwise_xor`

```python
dst = cv2.bitwise_xor(src1, src2, dst=None, mask=None)
```

#### `bitwise_not`

```python
dst = cv2.bitwise_not(src, dst=None, mask=None)
```

### 通道操作

#### `split`

将多通道图像拆分为单通道列表。

```python
channels = cv2.split(m)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `m` | `ndarray` | 多通道输入图像 |

**返回值**: `list[ndarray]`，每个元素为一个通道。

```python
b, g, r = cv2.split(img)  # 拆分为 B、G、R 三个通道
```

#### `merge`

将单通道列表合并为多通道图像。

```python
merged = cv2.merge(mv)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `mv` | `list[ndarray]` | 单通道 ndarray 列表 |

**返回值**: `ndarray`，合并后的多通道图像。

```python
merged = cv2.merge([b_channel, g_channel, r_channel])
```

### 统计与归一化

#### `mean`

计算图像均值。

```python
mean_vals = cv2.mean(src, mask=None)
```

**返回值**: `list[float]`，各通道均值。

#### `normalize`

归一化图像数值范围。

```python
dst = cv2.normalize(src, dst=None, alpha=None, beta=None, norm_type=cv2.NORM_L2, dtype=-1, mask=None)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `alpha` | `float` | 范围归一化时的最小值，或范数归一化时的目标值 |
| `beta` | `float` | 范围归一化时的最大值（`NORM_MINMAX` 时有效） |
| `norm_type` | `int` | 归一化类型（见常量表） |

```python
normed = cv2.normalize(src, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
```

#### `compare`

逐元素比较两图像。

```python
dst = cv2.compare(src1, src2, cmpop)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `cmpop` | `int` | 比较操作类型（见常量表） |

**返回值**: `ndarray` (dtype=`uint8`)，匹配位置为 255，不匹配为 0。

```python
mask = cv2.compare(img, threshold_val, cv2.CMP_GT)
```

### 其他 core 函数

#### `inRange`

颜色范围过滤。

```python
dst = cv2.inRange(src, lowerb, upperb, dst=None)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `lowerb` | `ndarray` | 下界值（与 src 通道数一致） |
| `upperb` | `ndarray` | 上界值 |

```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lo = np.array([0, 50, 50], dtype=np.uint8)
hi = np.array([10, 255, 255], dtype=np.uint8)
mask = cv2.inRange(hsv, lo, hi)
```

#### `convertScaleAbs`

缩放并取绝对值转换为 8 位。

```python
dst = cv2.convertScaleAbs(src, dst=None, alpha=None, beta=None)
```

`dst = saturate_cast<uchar>(|alpha * src + beta|)`

#### `minMaxLoc`

查找最小值、最大值及其位置。

```python
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(src, mask=None)
```

**返回值**: `(float, float, (int,int), (int,int))`

#### `LUT`

查找表映射变换。

```python
dst = cv2.LUT(src, lut, dst=None)
```

#### `countNonZero`

统计非零像素个数。

```python
count = cv2.countNonZero(src)
```

#### `flip`

图像翻转。

```python
dst = cv2.flip(src, flipCode, dst=None)
```

| `flipCode` | 效果 |
|-----------|------|
| 0 | 垂直翻转 |
| 1 | 水平翻转 |
| -1 | 对角线翻转 |

#### `rotate`

图像旋转。

```python
dst = cv2.rotate(src, rotateCode, dst=None)
```

`rotateCode` 取值见旋转常量表。

#### `transpose`

矩阵转置。

```python
dst = cv2.transpose(src, dst=None)
```

### core 常量

| 常量 | 值 | 说明 |
|------|------|------|
| `ROTATE_90_CLOCKWISE` | 0 | 顺时针旋转 90° |
| `ROTATE_180` | 1 | 旋转 180° |
| `ROTATE_90_COUNTERCLOCKWISE` | 2 | 逆时针旋转 90° |
| `CMP_EQ` | 0 | 等于 |
| `CMP_GT` | 1 | 大于 |
| `CMP_GE` | 2 | 大于等于 |
| `CMP_LT` | 3 | 小于 |
| `CMP_LE` | 4 | 小于等于 |
| `CMP_NE` | 5 | 不等于 |
| `NORM_INF` | 1 | 无穷范数 |
| `NORM_L1` | 2 | L1 范数 |
| `NORM_L2` | 4 | L2 范数 |
| `NORM_MINMAX` | 32 | 范围归一化 |

## imgproc — 图像处理

### 图像滤波

#### `Canny`

Canny 边缘检测。

```python
edges = cv2.Canny(image, threshold1, threshold2, edges=None, apertureSize=3, L2gradient=False)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `image` | `ndarray` | 输入（单通道灰度图） |
| `threshold1` | `float` | 低阈值 |
| `threshold2` | `float` | 高阈值 |
| `apertureSize` | `int` | Sobel 核大小，默认 3 |
| `L2gradient` | `bool` | 是否使用 L2 范数 |

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 80, 200)
```

#### `GaussianBlur`

高斯模糊。

```python
dst = cv2.GaussianBlur(src, ksize, sigmaX, dst=None, sigmaY=None, borderType=cv2.BORDER_DEFAULT)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `ksize` | `tuple(int,int)` | 核大小，如 `(5, 5)`，必须为奇数 |
| `sigmaX` | `float` | X 方向标准差 |

#### `blur`

均值模糊（盒式滤波）。

```python
dst = cv2.blur(src, ksize, dst=None, anchor=None, borderType=cv2.BORDER_DEFAULT)
```

#### `medianBlur`

中值模糊。

```python
dst = cv2.medianBlur(src, ksize, dst=None)
```

`ksize` 为奇数，如 5。

#### `bilateralFilter`

双边滤波（保边去噪）。

```python
dst = cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace, dst=None, borderType=cv2.BORDER_DEFAULT)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `d` | `int` | 像素邻域直径 |
| `sigmaColor` | `float` | 颜色空间标准差 |
| `sigmaSpace` | `float` | 坐标空间标准差 |

#### `boxFilter`

方框滤波。

```python
dst = cv2.boxFilter(src, ddepth, ksize, dst=None, anchor=None, normalize=True, borderType=cv2.BORDER_DEFAULT)
```

#### `filter2D`

自定义卷积核滤波。

```python
dst = cv2.filter2D(src, ddepth, kernel, dst=None, anchor=None, delta=None, borderType=cv2.BORDER_DEFAULT)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `ddepth` | `int` | 输出深度（-1 表示与输入相同） |
| `kernel` | `ndarray` | 卷积核 |
| `delta` | `float` | 加到每个像素的可选偏移 |

```python
kernel = np.ones((3, 3), dtype=np.float) / 9.0
result = cv2.filter2D(img, -1, kernel)
```

#### `Sobel`

Sobel 边缘检测。

```python
dst = cv2.Sobel(src, ddepth, dx, dy, dst=None, ksize=3, scale=None, delta=None, borderType=cv2.BORDER_DEFAULT)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `dx` | `int` | X 方向导数阶数 |
| `dy` | `int` | Y 方向导数阶数 |
| `ksize` | `int` | 核大小（1/3/5/7） |

```python
grad_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
grad_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=3)
```

#### `Scharr`

Scharr 边缘检测（比 Sobel 精度更高）。

```python
dst = cv2.Scharr(src, ddepth, dx, dy, dst=None, scale=None, delta=None, borderType=cv2.BORDER_DEFAULT)
```

#### `Laplacian`

拉普拉斯边缘检测。

```python
dst = cv2.Laplacian(src, ddepth, dst=None, ksize=1, scale=None, delta=None, borderType=cv2.BORDER_DEFAULT)
```

### 形态学操作

#### `erode`

腐蚀操作。

```python
dst = cv2.erode(src, kernel, dst=None, anchor=None, iterations=1, borderType=cv2.BORDER_CONSTANT)
```

#### `dilate`

膨胀操作。

```python
dst = cv2.dilate(src, kernel, dst=None, anchor=None, iterations=1, borderType=cv2.BORDER_CONSTANT)
```

#### `morphologyEx`

高级形态学操作。

```python
dst = cv2.morphologyEx(src, op, kernel, dst=None, anchor=None, iterations=1, borderType=cv2.BORDER_CONSTANT)
```

`op` 取值见形态学常量表。

```python
kernel = np.ones((3, 3), dtype=np.uint8)
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
```

#### `getStructuringElement`

获取结构元素。

```python
kernel = cv2.getStructuringElement(shape, ksize, anchor=None)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `shape` | `int` | 形状（`MORPH_RECT`/`MORPH_CROSS`/`MORPH_ELLIPSE`） |
| `ksize` | `tuple` | 大小，如 `(5, 5)` |

### 阈值处理

#### `threshold`

全局阈值分割。

```python
retval, dst = cv2.threshold(src, thresh, maxval, type, dst=None)
```

**返回值**: `(float, ndarray)` — 使用的实际阈值和输出图像。

```python
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
ret, otsu   = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
```

#### `adaptiveThreshold`

自适应阈值分割。

```python
dst = cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C, dst=None)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `adaptiveMethod` | `int` | `ADAPTIVE_THRESH_MEAN_C` 或 `ADAPTIVE_THRESH_GAUSSIAN_C` |
| `blockSize` | `int` | 邻域大小（奇数） |
| `C` | `float` | 从均值/加权均值中减去的常数 |

```python
result = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, 2)
```

### 颜色空间转换

#### `cvtColor`

颜色空间转换。

```python
dst = cv2.cvtColor(src, code, dst=None, dstCn=0)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `code` | `int` | 转换码（见颜色转换常量表） |
| `dstCn` | `int` | 目标通道数（0 表示自动） |

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
rgb  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
lab  = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
```

### 几何变换

#### `resize`

图像缩放。

```python
dst = cv2.resize(src, dsize, dst=None, fx=None, fy=None, interpolation=cv2.INTER_LINEAR)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `dsize` | `tuple(int,int)` | 目标大小 `(w, h)` |
| `fx` | `float` | 可选，X 方向缩放因子 |
| `fy` | `float` | 可选，Y 方向缩放因子 |

```python
small = cv2.resize(img, (160, 120))
```

#### `warpAffine`

仿射变换。

```python
dst = cv2.warpAffine(src, M, dsize, dst=None, flags=cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_CONSTANT, borderValue=None)
```

`M` 为 2x3 变换矩阵。

#### `warpPerspective`

透视变换。

```python
dst = cv2.warpPerspective(src, M, dsize, dst=None, flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=None)
```

`M` 为 3x3 变换矩阵。

> **注意**: `getPerspectiveTransform` / `getAffineTransform` 内部矩阵求解栈消耗较大，在默认 128KB 线程栈上可能触发栈溢出，建议从主 REPL 线程调用或增大线程栈。

#### `getRotationMatrix2D`

获取 2D 旋转矩阵。

```python
M = cv2.getRotationMatrix2D(center, angle, scale)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `center` | `tuple(int,int)` | 旋转中心 |
| `angle` | `float` | 旋转角度（度，逆时针为正） |
| `scale` | `float` | 缩放因子 |

```python
M = cv2.getRotationMatrix2D((160, 120), 45, 1.0)
rotated = cv2.warpAffine(img, M, (320, 240))
```

#### `getAffineTransform` ⚠

从三对点计算 2x3 仿射变换矩阵。

```python
M = cv2.getAffineTransform(src, dst)
```

`src` 和 `dst` 为 3x2 点集矩阵。

#### `getPerspectiveTransform` ⚠

从四对点计算 3x3 透视变换矩阵。

```python
M = cv2.getPerspectiveTransform(src, dst, solveMethod=cv2.DECOMP_LU)
```

`src` 和 `dst` 为 4x2 点集矩阵。

#### `remap`

像素重映射。

```python
dst = cv2.remap(src, map1, map2, interpolation, dst=None,
                borderMode=cv2.BORDER_CONSTANT, borderValue=None)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `map1` | `ndarray` | X 坐标映射表 |
| `map2` | `ndarray` | Y 坐标映射表 |
| `interpolation` | `int` | 插值方式（见插值常量表） |

### 图像金字塔

#### `pyrDown`

高斯金字塔降采样。

```python
dst = cv2.pyrDown(src, dst=None, dstsize=None, borderType=cv2.BORDER_DEFAULT)
```

图像尺寸减半。

#### `pyrUp`

高斯金字塔升采样。

```python
dst = cv2.pyrUp(src, dst=None, dstsize=None, borderType=cv2.BORDER_DEFAULT)
```

图像尺寸加倍。

### 绘图函数

所有绘图函数直接修改输入图像并返回，支持链式调用。

#### `line`

绘制直线。

```python
img = cv2.line(img, pt1, pt2, color, thickness=1, lineType=cv2.LINE_8, shift=0)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `pt1` | `tuple(int,int)` | 起点 |
| `pt2` | `tuple(int,int)` | 终点 |
| `color` | `tuple` | 颜色，BGR 元组如 `(0, 255, 0)` |

#### `rectangle`

绘制矩形。

```python
img = cv2.rectangle(img, pt1, pt2, color, thickness=1, lineType=cv2.LINE_8, shift=0)
```

`thickness=-1` 时填充矩形。

```python
cv2.rectangle(img, (10, 10), (80, 60), (0, 0, 255), -1)  # 填充红色矩形
```

#### `circle`

绘制圆形。

```python
img = cv2.circle(img, center, radius, color, thickness=1, lineType=cv2.LINE_8, shift=0)
```

#### `ellipse`

绘制椭圆/弧。

```python
img = cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color,
                  thickness=1, lineType=cv2.LINE_8, shift=0)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `center` | `tuple` | 椭圆中心 |
| `axes` | `tuple` | 半轴长度 `(a, b)` |
| `angle` | `float` | 旋转角度 |
| `startAngle` | `float` | 起始角度 |
| `endAngle` | `float` | 终止角度 |

#### `putText`

绘制文字。

```python
img = cv2.putText(img, text, org, fontFace, fontScale, color,
                  thickness=1, lineType=cv2.LINE_8, bottomLeftOrigin=False)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `text` | `str` | 文字内容 |
| `org` | `tuple` | 文字左下角位置 |
| `fontFace` | `int` | 字体（见字体常量表） |
| `fontScale` | `float` | 字体缩放因子 |

#### `arrowedLine`

绘制带箭头的线段。

```python
img = cv2.arrowedLine(img, pt1, pt2, color, thickness=1, line_type=cv2.LINE_8, shift=0, tipLength=None)
```

#### `drawMarker`

绘制标记点。

```python
img = cv2.drawMarker(img, position, color, markerType=cv2.MARKER_CROSS,
                     markerSize=20, thickness=1, line_type=cv2.LINE_8)
```

`markerType` 见标记常量表。

#### `fillPoly`

填充多边形。

```python
img = cv2.fillPoly(img, pts, color, lineType=cv2.LINE_8, shift=0, offset=None)
```

`pts` 为轮廓点列表，每个轮廓是 Nx2 ndarray。

```python
tri = np.array([[20, 20], [80, 20], [50, 80]], dtype=np.float)
cv2.fillPoly(img, [tri], (0, 255, 0))
```

#### `polylines`

绘制多边形边框。

```python
img = cv2.polylines(img, pts, isClosed, color, thickness=1, lineType=cv2.LINE_8, shift=0)
```

#### `getTextSize`

获取文字渲染尺寸。

```python
size, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
```

**返回值**: `((width, height), baseline)`

### 轮廓分析

#### `findContours`

查找二值图像中的轮廓。

```python
contours, hierarchy = cv2.findContours(image, mode, method, contours=None, hierarchy=None, offset=None)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `mode` | `int` | 轮廓检索模式（`RETR_EXTERNAL`/`RETR_LIST`/`RETR_CCOMP`/`RETR_TREE`） |
| `method` | `int` | 轮廓近似方法（`CHAIN_APPROX_SIMPLE`/`CHAIN_APPROX_NONE` 等） |

**返回值**: `(list[ndarray], ndarray)` — 轮廓列表和层次结构。

#### `drawContours`

绘制轮廓。

```python
img = cv2.drawContours(image, contours, contourIdx, color, thickness=1,
                       lineType=cv2.LINE_8, hierarchy=None, maxLevel=INT_MAX, offset=None)
```

`contourIdx=-1` 时绘制所有轮廓。

#### `contourArea`

计算轮廓面积。

```python
area = cv2.contourArea(contour, oriented=False)
```

#### `arcLength`

计算轮廓周长。

```python
perimeter = cv2.arcLength(curve, closed)
```

#### `boundingRect`

计算外接正矩形。

```python
x, y, w, h = cv2.boundingRect(array)
```

#### `approxPolyDP`

多边形逼近。

```python
approx = cv2.approxPolyDP(curve, epsilon, closed)
```

`epsilon` 通常设为 `0.02 * cv2.arcLength(curve, True)`。

#### `convexHull`

计算凸包。

```python
hull = cv2.convexHull(points, hull=None, clockwise=False, returnPoints=True)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `returnPoints` | `bool` | `True` 返回点坐标；`False` 返回轮廓的点索引（用于 `convexityDefects`） |

#### `minAreaRect`

最小外接旋转矩形。

```python
center, size, angle = cv2.minAreaRect(points)
```

**返回值**: `((cx, cy), (w, h), angle)` — 中心、尺寸、旋转角。

#### `minEnclosingCircle`

最小外接圆。

```python
center, radius = cv2.minEnclosingCircle(points)
```

#### `fitEllipse`

拟合椭圆。

```python
center, size, angle = cv2.fitEllipse(points)
```

> 输入至少需要 5 个点。

#### `fitLine`

拟合直线。

```python
line = cv2.fitLine(points, distType, param, reps, aeps)
```

**返回值**: `(vx, vy, x0, y0)` — 单位方向向量 + 直线上一点。

#### `pointPolygonTest`

点与轮廓位置关系测试。

```python
dist = cv2.pointPolygonTest(contour, pt, measureDist)
```

| `measureDist` | 行为 |
|--------------|------|
| `True` | 返回带符号最短距离 |
| `False` | 返回 +1（内部）、0（在边上）、-1（外部） |

#### `convexityDefects`

计算凸包缺陷。

```python
defects = cv2.convexityDefects(contour, convexhull)
```

`convexhull` 必须为 1D 索引数组（即 `convexHull(..., returnPoints=False)` 的输出）。

#### `matchShapes`

形状匹配（基于 Hu 矩）。

```python
score = cv2.matchShapes(contour1, contour2, method, parameter)
```

#### `isContourConvex`

判断轮廓是否为凸。

```python
result = cv2.isContourConvex(contour)
```

返回 `bool`。

### 模板匹配

#### `matchTemplate`

模板匹配。

```python
result = cv2.matchTemplate(image, templ, method, result=None, mask=None)
```

`method` 可选值见 `TM_*` 常量表。

```python
result = cv2.matchTemplate(img, templ, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(result)
```

### 图像矩

#### `moments`

计算图像矩。

```python
m = cv2.moments(array, binaryImage=False)
```

返回 `dict`，包含空间矩 (`m00`, `m10`, ...)、中心矩 (`mu20`, ...) 和归一化中心矩 (`nu20`, ...)。

```python
m = cv2.moments(binary)
cx = m['m10'] / m['m00']  # 质心 X
cy = m['m01'] / m['m00']  # 质心 Y
```

### 霍夫变换

#### `HoughLines`

标准霍夫直线检测。

```python
lines = cv2.HoughLines(image, rho, theta, threshold, lines=None,
                       srn=None, stn=None, min_theta=None, max_theta=None)
```

**返回值**: Nx2 ndarray，每行为 `(rho, theta)`。

#### `HoughLinesP`

概率霍夫直线检测（线段）。

```python
lines = cv2.HoughLinesP(image, rho, theta, threshold, lines=None,
                        minLineLength=None, maxLineGap=None)
```

**返回值**: Nx4 ndarray，每行为 `(x1, y1, x2, y2)`。

```python
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=30)
for i in range(lines.shape[0]):
    x1, y1, x2, y2 = lines[i, 0], lines[i, 1], lines[i, 2], lines[i, 3]
```

#### `HoughCircles`

霍夫圆检测。

```python
circles = cv2.HoughCircles(image, method, dp, minDist, circles=None,
                           param1=None, param2=None, minRadius=0, maxRadius=0)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `method` | `int` | 检测方法（3 = `HOUGH_GRADIENT`） |
| `dp` | `float` | 累加器分辨率与图像分辨率的反比 |
| `minDist` | `float` | 圆心间最小距离 |
| `param1` | `float` | Canny 高阈值，默认 100 |
| `param2` | `float` | 圆心累加器阈值，默认 100 |
| `minRadius` | `int` | 最小半径 |
| `maxRadius` | `int` | 最大半径 |

**返回值**: Nx3 ndarray，每行为 `(cx, cy, r)`。

### 直方图

#### `calcHist`

计算图像直方图。

```python
hist = cv2.calcHist(images, channels, mask, histSize, ranges)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `images` | `list[ndarray]` | 输入图像列表 |
| `channels` | `list[int]` | 要计算的通道索引列表 |
| `mask` | `ndarray` 或 `None` | 可选 8 位单通道掩码 |
| `histSize` | `list[int]` | 每个维度的 bin 数 |
| `ranges` | `list[float]` | 每个维度的取值范围（平铺列表） |

```python
hist = cv2.calcHist([img], [0], None, [32], [0, 256])
```

#### `calcBackProject`

直方图反向投影。

```python
dst = cv2.calcBackProject(images, channels, hist, dst=None, ranges, scale=None)
```

用于在图像中寻找与直方图匹配的区域。

#### `compareHist`

直方图比较。

```python
score = cv2.compareHist(H1, H2, method)
```

`method` 取值见 `HISTCMP_*` 常量表。

#### `equalizeHist`

直方图均衡化。

```python
dst = cv2.equalizeHist(src, dst=None)
```

### 角点检测

#### `cornerHarris`

Harris 角点检测。

```python
dst = cv2.cornerHarris(src, blockSize, ksize, k, dst=None, borderType=cv2.BORDER_DEFAULT)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `blockSize` | `int` | 角点检测邻域大小 |
| `ksize` | `int` | Sobel 孔径大小 |
| `k` | `float` | Harris 检测器自由参数（通常 0.04-0.06） |

#### `goodFeaturesToTrack`

Shi-Tomasi 角点检测。

```python
corners = cv2.goodFeaturesToTrack(image, maxCorners, qualityLevel, minDistance,
                                  mask=None, blockSize=3, useHarrisDetector=False, k=None)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `maxCorners` | `int` | 最大角点数 |
| `qualityLevel` | `float` | 质量阈值（0.01-0.1） |
| `minDistance` | `float` | 角点间最小欧氏距离 |
| `blockSize` | `int` | 梯度计算窗口大小 |

**返回值**: Nx2 ndarray，每行为 `(x, y)`（float 坐标）。

#### `cornerSubPix` ⚠

亚像素角点精确定位。

```python
refined = cv2.cornerSubPix(image, corners, winSize, zeroZone, criteria)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `corners` | `ndarray` | 初始角点坐标（如 `goodFeaturesToTrack` 的输出） |
| `winSize` | `tuple` | 搜索窗口半宽 |
| `zeroZone` | `tuple` | 死区半宽 |
| `criteria` | `tuple` | 终止条件 `(type, maxCount, epsilon)`，如 `(3, 30, 0.001)` |

> **平台限制**: 此移植版 OpenCV 的 `InputOutputArray(std::vector<Point2f>&)` 包装路径与标准版不一致，调用会触发 `count >= 0` 断言失败。实时检测场景请使用 `goodFeaturesToTrack` 代替。

### 图像分割

#### `watershed`

分水岭分割。

```python
markers = cv2.watershed(image, markers)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `image` | `ndarray` | 3 通道 8 位输入图像 |
| `markers` | `ndarray` | int32 标记图（输入输出参数） |

#### `distanceTransform`

距离变换。

```python
dst = cv2.distanceTransform(src, distanceType, maskSize, dst=None, dstType=cv2.CV_32F, labelType=cv2.DIST_LABEL_CCOMP)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `distanceType` | `int` | 距离类型（`DIST_L1`/`DIST_L2`/`DIST_C`） |
| `maskSize` | `int` | 距离变换掩码大小（3 或 5） |

#### `floodFill`

漫水填充。

```python
filled, rect = cv2.floodFill(image, mask, seedPoint, newVal, loDiff=None, upDiff=None, flags=4)
```

**返回值**: `(ndarray, (x, y, w, h))` — 填充后图像和填充区域边界框。

```python
filled, rect = cv2.floodFill(img, None, (50, 50), (0, 255, 0))
```

#### `grabCut` ⚠

GrabCut 前景分割。

```python
mask, bgd, fgd = cv2.grabCut(img, mask, rect, bgdModel, fgdModel, iterCount, mode=cv2.GC_INIT_WITH_RECT)
```

> **注意**: 内部 GMM 迭代栈消耗较大，默认 128KB 线程栈下可能溢出。建议加大栈或从主 REPL 线程调用。

#### `connectedComponents`

连通组件标记。

```python
nlabels, labels = cv2.connectedComponents(image, labels=None, connectivity=8, ltype=cv2.CV_32S)
```

**返回值**: `(int, ndarray)` — 标签数和标记图。

## highgui — 交互

### `waitKey`

等待按键。

```python
key = cv2.waitKey(delay=0)
```

| `delay` | 行为 |
|--------|------|
| 0 | 一直等待 |
| >0 | 等待 `delay` 毫秒后超时返回 -1 |

在 K230 MicroPython 上，从串口 REPL 读取输入。

### `waitKeyEx`

增强版 `waitKey`，行为与 `waitKey` 相同。

```python
key = cv2.waitKeyEx(delay=0)
```

## 常量参考

### 形态学常量

| 常量 | 值 | 说明 |
|------|------|------|
| `MORPH_ERODE` | 0 | 腐蚀 |
| `MORPH_DILATE` | 1 | 膨胀 |
| `MORPH_OPEN` | 2 | 开运算 |
| `MORPH_CLOSE` | 3 | 闭运算 |
| `MORPH_GRADIENT` | 4 | 形态学梯度 |
| `MORPH_TOPHAT` | 5 | 顶帽 |
| `MORPH_BLACKHAT` | 6 | 黑帽 |
| `MORPH_HITMISS` | 7 | 击中击不中 |
| `MORPH_RECT` | 0 | 矩形结构元素 |
| `MORPH_CROSS` | 1 | 十字形结构元素 |
| `MORPH_ELLIPSE` | 2 | 椭圆形结构元素 |

### 阈值常量

| 常量 | 值 | 说明 |
|------|------|------|
| `THRESH_BINARY` | 0 | 二值化 |
| `THRESH_BINARY_INV` | 1 | 反二值化 |
| `THRESH_TRUNC` | 2 | 截断 |
| `THRESH_TOZERO` | 3 | 置零 |
| `THRESH_TOZERO_INV` | 4 | 反置零 |
| `THRESH_OTSU` | 8 | OTSU（可与上述组合） |
| `THRESH_TRIANGLE` | 16 | Triangle 法 |

### 自适应阈值常量

| 常量 | 值 | 说明 |
|------|------|------|
| `ADAPTIVE_THRESH_MEAN_C` | 0 | 均值法 |
| `ADAPTIVE_THRESH_GAUSSIAN_C` | 1 | 高斯法 |

### 边界常量

| 常量 | 值 |
|------|------|
| `BORDER_CONSTANT` | 0 |
| `BORDER_REPLICATE` | 1 |
| `BORDER_REFLECT` | 2 |
| `BORDER_WRAP` | 3 |
| `BORDER_REFLECT_101` | 4 |
| `BORDER_DEFAULT` | 4 |
| `BORDER_TRANSPARENT` | 5 |
| `BORDER_ISOLATED` | 16 |

### 插值常量

| 常量 | 值 | 说明 |
|------|------|------|
| `INTER_NEAREST` | 0 | 最近邻 |
| `INTER_LINEAR` | 1 | 双线性（默认） |
| `INTER_CUBIC` | 2 | 双三次 |
| `INTER_AREA` | 3 | 区域插值 |
| `INTER_LANCZOS4` | 4 | Lanczos |
| `INTER_LINEAR_EXACT` | 5 | 精确双线性 |
| `INTER_MAX` | 7 | 插值掩码 |
| `WARP_FILL_OUTLIERS` | 8 | 填充异常值 |
| `WARP_INVERSE_MAP` | 16 | 逆向映射 |

### 颜色转换常量

| 常量 | 值 | 说明 |
|------|------|------|
| `COLOR_BGR2GRAY` | 6 | BGR → 灰度 |
| `COLOR_RGB2GRAY` | 7 | RGB → 灰度 |
| `COLOR_GRAY2BGR` | 8 | 灰度 → BGR |
| `COLOR_GRAY2RGB` | 8 | 灰度 → RGB |
| `COLOR_BGR2RGB` | 4 | BGR ↔ RGB |
| `COLOR_BGR2HSV` | 40 | BGR → HSV |
| `COLOR_HSV2BGR` | 54 | HSV → BGR |
| `COLOR_RGB2HSV` | 41 | RGB → HSV |
| `COLOR_HSV2RGB` | 55 | HSV → RGB |
| `COLOR_BGR2YUV` | 82 | BGR → YUV |
| `COLOR_YUV2BGR` | 84 | YUV → BGR |
| `COLOR_BGR2YCR_CB` | 36 | BGR → YCrCb |
| `COLOR_YCR_CB2BGR` | 38 | YCrCb → BGR |
| `COLOR_BGR2LAB` | 44 | BGR → LAB |
| `COLOR_LAB2BGR` | 56 | LAB → BGR |
| `COLOR_BGR2LUV` | 50 | BGR → LUV |
| `COLOR_LUV2BGR` | 58 | LUV → BGR |
| `COLOR_BGR2XYZ` | 32 | BGR → XYZ |
| `COLOR_XYZ2BGR` | 34 | XYZ → BGR |
| `COLOR_BGR2HLS` | 52 | BGR → HLS |
| `COLOR_HLS2BGR` | 60 | HLS → BGR |
| `COLOR_BGRA2BGR` | 45 | BGRA → BGR |
| `COLOR_BGR2BGRA` | 43 | BGR → BGRA |

### 字体常量

| 常量 | 值 |
|------|------|
| `FONT_HERSHEY_SIMPLEX` | 0 |
| `FONT_HERSHEY_PLAIN` | 1 |
| `FONT_HERSHEY_DUPLEX` | 2 |
| `FONT_HERSHEY_COMPLEX` | 3 |
| `FONT_HERSHEY_TRIPLEX` | 4 |
| `FONT_HERSHEY_COMPLEX_SMALL` | 5 |
| `FONT_HERSHEY_SCRIPT_SIMPLEX` | 6 |
| `FONT_HERSHEY_SCRIPT_COMPLEX` | 7 |
| `FONT_ITALIC` | 16（可与上述叠加） |

### 线条常量

| 常量 | 值 | 说明 |
|------|------|------|
| `LINE_4` | 4 | 4 连通线 |
| `LINE_8` | 8 | 8 连通线 |
| `LINE_AA` | 16 | 抗锯齿线 |
| `FILLED` | -1 | 填充（用于 thickness 参数） |

### 轮廓常量

| 常量 | 值 | 说明 |
|------|------|------|
| `RETR_EXTERNAL` | 0 | 只检测最外层轮廓 |
| `RETR_LIST` | 1 | 检测所有轮廓 |
| `RETR_CCOMP` | 2 | 两级层次 |
| `RETR_TREE` | 3 | 完整层次树 |
| `RETR_FLOODFILL` | 4 | 漫水填充 |
| `CHAIN_APPROX_NONE` | 1 | 保存所有轮廓点 |
| `CHAIN_APPROX_SIMPLE` | 2 | 压缩并保留端点 |
| `CHAIN_APPROX_TC89_L1` | 3 | Teh-Chin 链 L1 |
| `CHAIN_APPROX_TC89_KCOS` | 4 | Teh-Chin 链 kCos |

### 形状匹配常量

| 常量 | 值 | 说明 |
|------|------|------|
| `CONTOURS_MATCH_I1` | 1 | 方法 1 |
| `CONTOURS_MATCH_I2` | 2 | 方法 2 |
| `CONTOURS_MATCH_I3` | 3 | 方法 3 |

### 连通组件常量

| 常量 | 值 | 说明 |
|------|------|------|
| `CONNECTED_4` | 4 | 4 连通 |
| `CONNECTED_8` | 8 | 8 连通 |
| `CCL_DEFAULT` | -1 | 默认算法 |
| `CCL_WU` | 0 | Wu |
| `CCL_GRANA` | 1 | Grana |
| `CCL_BOLELLI` | 2 | Bolelli |
| `CCL_SAUF` | 3 | SAUF |
| `CCL_BBDT` | 4 | BBDT |
| `CCL_SPAGHETTI` | 5 | Spaghetti |

### 距离变换常量

| 常量 | 值 | 说明 |
|------|------|------|
| `DIST_L1` | 1 | 曼哈顿距离 |
| `DIST_L2` | 2 | 欧氏距离 |
| `DIST_C` | 3 | 棋盘距离 |
| `DIST_L12` | 4 | L1-L2 混合 |
| `DIST_FAIR` | 5 | Fair |
| `DIST_WELSCH` | 6 | Welsch |
| `DIST_HUBER` | 7 | Huber |
| `DIST_LABEL_CCOMP` | 0 | CComp 标记 |
| `DIST_LABEL_PIXEL` | 1 | 像素标记 |

### 模板匹配常量

| 常量 | 值 | 说明 |
|------|------|------|
| `TM_SQDIFF` | 0 | 平方差 |
| `TM_SQDIFF_NORMED` | 1 | 归一化平方差 |
| `TM_CCORR` | 2 | 相关性 |
| `TM_CCORR_NORMED` | 3 | 归一化相关性 |
| `TM_CCOEFF` | 4 | 相关系数 |
| `TM_CCOEFF_NORMED` | 5 | 归一化相关系数 |

### 标记类型常量

| 常量 | 值 |
|------|------|
| `MARKER_CROSS` | 0 |
| `MARKER_TILTED_CROSS` | 1 |
| `MARKER_STAR` | 2 |
| `MARKER_DIAMOND` | 3 |
| `MARKER_SQUARE` | 4 |
| `MARKER_TRIANGLE_UP` | 5 |
| `MARKER_TRIANGLE_DOWN` | 6 |

### 直方图比较常量

| 常量 | 值 | 说明 |
|------|------|------|
| `HISTCMP_CORREL` | 0 | 相关性 |
| `HISTCMP_CHISQR` | 1 | 卡方 |
| `HISTCMP_INTERSECT` | 2 | 相交 |
| `HISTCMP_BHATTACHARYYA` | 3 | Bhattacharyya |
| `HISTCMP_HELLINGER` | 3 | Hellinger（同 Bhattacharyya） |
| `HISTCMP_CHISQR_ALT` | 4 | 替代卡方 |
| `HISTCMP_KL_DIV` | 5 | KL 散度 |

### GrabCut 常量

| 常量 | 值 | 说明 |
|------|------|------|
| `GC_BGD` | 0 | 确定背景 |
| `GC_FGD` | 1 | 确定前景 |
| `GC_PR_BGD` | 2 | 可能背景 |
| `GC_PR_FGD` | 3 | 可能前景 |
| `GC_INIT_WITH_RECT` | 0 | 矩形初始化 |
| `GC_INIT_WITH_MASK` | 1 | 掩码初始化 |
| `GC_EVAL` | 2 | 评估模式 |
| `GC_EVAL_FREEZE_MODEL` | 3 | 冻结模型评估 |

### 终止条件常量

| 常量 | 值 | 说明 |
|------|------|------|
| `TERM_CRITERIA_COUNT` | 1 | 迭代次数 |
| `TERM_CRITERIA_EPS` | 2 | 精度 |
| `TERM_CRITERIA_MAX_ITER` | 1 | 最大迭代（同 COUNT） |

## 使用示例

### 完整流程：读取、处理、保存

```python
import cv2
from ulab import numpy as np

img = cv2.imread("/sdcard/input.jpg")
if img is None:
    img = np.zeros((240, 320, 3), dtype=np.uint8)
    cv2.circle(img, (160, 120), 80, (0, 255, 0), -1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imwrite("/sdcard/output.jpg", result)
```

### 图像算术混合

```python
img1 = cv2.imread("/sdcard/img1.jpg")
img2 = cv2.imread("/sdcard/img2.jpg")
blended = cv2.addWeighted(img1, 0.6, img2, 0.4, 0)
cv2.imwrite("/sdcard/blended.jpg", blended)
```

### 颜色分割（inRange）

```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
green_lo = np.array([35, 50, 50], dtype=np.uint8)
green_hi = np.array([85, 255, 255], dtype=np.uint8)
mask = cv2.inRange(hsv, green_lo, green_hi)
result = cv2.bitwise_and(img, img, mask=mask)
```

### 直方图分析

```python
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
score = cv2.compareHist(hist, hist2, cv2.HISTCMP_CORREL)
```

### 摄像头实时检测

从摄像头取帧，转为 numpy 后用 OpenCV 实时处理。图像分辨率建议 320x240 以获得较高帧率。

```python
import time, gc
from media.sensor import *
from media.display import *
from media.media import *
import cv2
from ulab import numpy as np

sensor = Sensor(width=1280, height=960, fps=90)
sensor.reset()
sensor.set_framesize(width=320, height=240)
sensor.set_pixformat(Sensor.RGB888)    # OpenCV 需 RGB888
sensor.run()

Display.init(Display.ST7701, width=800, height=480, to_ide=True)

try:
    while True:
        img = sensor.snapshot()            # image.Image
        img_np = img.to_numpy_ref()        # 共享内存转 ndarray

        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 60, 150)

        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 60,
                                minLineLength=40, maxLineGap=15)
        if lines is not None:
            for i in range(lines.shape[0]):
                x1, y1, x2, y2 = lines[i, 0], lines[i, 1], lines[i, 2], lines[i, 3]
                cv2.line(img_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        gc.collect()
        Display.show_image(img)  # 直接显示 (OpenCV 已修改共享内存)
finally:
    sensor.stop()
    Display.deinit()
```

> 更多实时检测示例位于开发板固件的 `/sdcard/examples/24-OpenCV/`，对应 SDK
> 源码目录为 `src/canmv/resources/examples/24-OpenCV/`，文件名为
> `demo_camera_*.py`。
