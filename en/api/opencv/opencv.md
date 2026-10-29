# OpenCV API Manual

The `cv2` module provides MicroPython bindings for the OpenCV computer vision library, supporting classical computer vision functions such as image I/O, filtering, morphology, thresholding, color space conversion, geometric transformation, drawing, contour analysis, template matching, Hough transform, histogram, corner detection, and image segmentation.

Image data is represented using `ulab.numpy`'s `ndarray`, and can be converted to/from `image.Image` objects via the `image.Image.to_numpy_ref()` method.

```python
import cv2
from ulab import numpy as np
```

## Function List

### imgcodecs — Image Read/Write (4 functions)

| Function | Description |
|------|------|
| `imread` | Read image from file |
| `imwrite` | Save image to file |
| `imdecode` | Decode image from memory buffer |
| `imencode` | Encode image to memory buffer |

### core — Core Operations (23 functions)

| Function | Description |
|------|------|
| `add` | Element-wise addition |
| `subtract` | Element-wise subtraction |
| `multiply` | Element-wise multiplication |
| `divide` | Element-wise division |
| `addWeighted` | Weighted blending of two images: `alpha·src1 + beta·src2 + gamma` |
| `absdiff` | Element-wise absolute difference between two images |
| `bitwise_and` | Bitwise AND operation |
| `bitwise_or` | Bitwise OR operation |
| `bitwise_xor` | Bitwise XOR operation |
| `bitwise_not` | Bitwise NOT operation |
| `split` | Split multi-channel image into single-channel list |
| `merge` | Merge single-channel list into multi-channel image |
| `mean` | Calculate mean value of each channel |
| `normalize` | Normalize image value range |
| `compare` | Element-wise comparison of two images, returns binary mask |
| `inRange` | Color range filtering, returns binary mask |
| `convertScaleAbs` | Scale, take absolute value, then convert to 8-bit |
| `minMaxLoc` | Find min/max values and their positions |
| `LUT` | Lookup table mapping transformation |
| `countNonZero` | Count non-zero pixels |
| `flip` | Image flip (vertical/horizontal/diagonal) |
| `rotate` | Image rotation (90°/180°/270°) |
| `transpose` | Matrix transpose |

### imgproc — Image Processing (65 functions)

**Image Filtering**

| Function | Description |
|------|------|
| `Canny` | Canny edge detection |
| `GaussianBlur` | Gaussian blur |
| `blur` | Mean blur (box filter) |
| `medianBlur` | Median blur |
| `bilateralFilter` | Bilateral filter (edge-preserving denoising) |
| `boxFilter` | Box filter |
| `filter2D` | Custom kernel convolution filter |
| `Sobel` | Sobel edge detection (first-order derivative) |
| `Scharr` | Scharr edge detection (higher precision than Sobel) |
| `Laplacian` | Laplacian edge detection (second-order derivative) |

**Morphology**

| Function | Description |
|------|------|
| `erode` | Erosion operation |
| `dilate` | Dilation operation |
| `morphologyEx` | Advanced morphology (open/close/gradient/top hat/black hat) |
| `getStructuringElement` | Get structuring element (rectangle/cross/ellipse) |

**Thresholding**

| Function | Description |
|------|------|
| `threshold` | Global threshold segmentation (supports OTSU / Triangle) |
| `adaptiveThreshold` | Adaptive threshold segmentation (mean/Gaussian) |

**Color Conversion**

| Function | Description |
|------|------|
| `cvtColor` | Color space conversion (BGR↔GRAY/HSV/LAB/YUV and 22 others) |

**Geometric Transformation**

| Function | Description |
|------|------|
| `resize` | Image resizing |
| `warpAffine` | Affine transformation |
| `warpPerspective` | Perspective transformation |
| `getRotationMatrix2D` | Get 2D rotation matrix |
| `getAffineTransform` ⚠ | Compute affine transformation matrix from three point pairs |
| `getPerspectiveTransform` ⚠ | Compute perspective transformation matrix from four point pairs |
| `remap` | Pixel remapping |

**Pyramid**

| Function | Description |
|------|------|
| `pyrDown` | Gaussian pyramid downsampling (size halved) |
| `pyrUp` | Gaussian pyramid upsampling (size doubled) |

**Drawing**

| Function | Description |
|------|------|
| `line` | Draw line |
| `rectangle` | Draw rectangle |
| `circle` | Draw circle |
| `ellipse` | Draw ellipse/arc |
| `putText` | Draw text (supports 8 Hershey fonts) |
| `arrowedLine` | Draw line with arrow |
| `drawMarker` | Draw marker (cross/star/diamond and 4 others) |
| `fillPoly` | Fill polygon |
| `polylines` | Draw polygon outline |
| `getTextSize` | Get text rendering size and baseline |

**Contours**

| Function | Description |
|------|------|
| `findContours` | Find contours in binary image |
| `drawContours` | Draw contours |
| `contourArea` | Calculate contour area |
| `arcLength` | Calculate contour perimeter |
| `boundingRect` | Calculate bounding upright rectangle |
| `approxPolyDP` | Polygon approximation |
| `convexHull` | Calculate convex hull (supports returning point coordinates or indices) |
| `minAreaRect` | Minimum enclosing rotated rectangle |
| `minEnclosingCircle` | Minimum enclosing circle |
| `fitEllipse` | Fit ellipse (requires ≥5 points) |
| `fitLine` | Fit line |
| `pointPolygonTest` | Test point and contour position relationship |
| `convexityDefects` | Calculate convex hull defects |
| `matchShapes` | Shape matching (based on Hu moments) |
| `isContourConvex` | Check if contour is convex |

**Template Matching & Moments**

| Function | Description |
|------|------|
| `matchTemplate` | Template matching (6 matching methods) |
| `moments` | Calculate image moments (spatial/central/normalized moments) |

**Hough Transform**

| Function | Description |
|------|------|
| `HoughLines` | Standard Hough line detection |
| `HoughLinesP` | Probabilistic Hough line detection (returns line segment endpoints) |
| `HoughCircles` | Hough circle detection (gradient method) |

**Histogram**

| Function | Description |
|------|------|
| `calcHist` | Calculate image histogram |
| `calcBackProject` | Histogram back projection |
| `compareHist` | Histogram comparison (6 comparison methods) |
| `equalizeHist` | Histogram equalization |

**Corner Detection**

| Function | Description |
|------|------|
| `cornerHarris` | Harris corner detection |
| `goodFeaturesToTrack` | Shi-Tomasi corner detection |
| `cornerSubPix` ⚠ | Sub-pixel corner precise localization |

**Segmentation**

| Function | Description |
|------|------|
| `watershed` | Watershed segmentation |
| `distanceTransform` | Distance transform |
| `floodFill` | Flood fill |
| `grabCut` ⚠ | GrabCut foreground segmentation |
| `connectedComponents` | Connected components labeling |

### highgui — Interaction (2 functions)

| Function | Description |
|------|------|
| `waitKey` | Wait for key press (supports timeout) |
| `waitKeyEx` | Enhanced version of waitKey |

> **Total: 94 functions**. ⚠ indicates platform limitations: `getAffineTransform` / `getPerspectiveTransform` / `grabCut` may overflow with the default 128KB thread stack; `cornerSubPix` has an incompatible `InputOutputArray` wrapper path in this OpenCV port.

## imgcodecs — Image Read/Write

### `imread`

Read an image from a file.

```python
img = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
```

| Parameter | Type | Description |
|------|------|------|
| `filename` | `str` | Image file path, supports BMP, PNG, JPEG and other formats |
| `flags` | `int` | Read mode (see constants table), defaults to `IMREAD_COLOR` |

**Return value**: `ndarray`, returns `None` on failure.

Example:

```python
img = cv2.imread("/sdcard/photo.jpg")
gray = cv2.imread("/sdcard/photo.jpg", cv2.IMREAD_GRAYSCALE)
```

### `imwrite`

Save an image to a file.

```python
success = cv2.imwrite(filename, img)
```

| Parameter | Type | Description |
|------|------|------|
| `filename` | `str` | Save path, format is determined by extension (e.g. `.png`, `.jpg`) |
| `img` | `ndarray` | Image array |

**Return value**: `bool`, returns `True` on success.

Example:

```python
img = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.imwrite("/sdcard/output.png", img)
```

### `imdecode`

Decode an image from a memory buffer.

```python
img = cv2.imdecode(buf, flags=cv2.IMREAD_COLOR)
```

| Parameter | Type | Description |
|------|------|------|
| `buf` | `bytes` | Byte buffer containing image data |
| `flags` | `int` | Decode mode, same as `imread` |

**Return value**: `ndarray`, returns `None` on failure.

### `imencode`

Encode an image into a memory buffer.

```python
success, buf = cv2.imencode(ext, img, params=None)
```

| Parameter | Type | Description |
|------|------|------|
| `ext` | `str` | Image format extension, e.g. `".jpg"`, `".png"` |
| `img` | `ndarray` | Image to be encoded |
| `params` | `list` | Optional, encoding parameter list `[param_id, val, ...]`, e.g. `[1, 50]` for JPEG quality 50 |

**Return value**: `(bool, bytes)` tuple. `success` indicates whether encoding succeeded, `buf` is the encoded byte data.

Example:

```python
success, buf = cv2.imencode(".jpg", img, [1, 50])  # JPEG quality=50
decoded = cv2.imdecode(buf, cv2.IMREAD_COLOR)
```

### Image Read/Write Constants

| Constant | Value | Description |
|------|------|------|
| `IMREAD_UNCHANGED` | -1 | Keep original format |
| `IMREAD_GRAYSCALE` | 0 | Convert to grayscale |
| `IMREAD_COLOR` | 1 | Convert to BGR color image |
| `IMREAD_ANYDEPTH` | 2 | Preserve original bit depth |
| `IMREAD_ANYCOLOR` | 4 | Preserve original number of channels |
| `IMREAD_IGNORE_ORIENTATION` | 128 | Ignore EXIF orientation tag |

## core — Core Operations

### Arithmetic Operations

#### `add`

Element-wise addition of two images or an image and a scalar.

```python
dst = cv2.add(src1, src2, dst=None, mask=None, dtype=-1)
```

| Parameter | Type | Description |
|------|------|------|
| `src1` | `ndarray` | First input image |
| `src2` | `ndarray` | Second input image (or scalar ndarray) |
| `dst` | `ndarray` | Optional, output image |
| `mask` | `ndarray` | Optional, 8-bit single-channel mask |
| `dtype` | `int` | Optional, output depth (-1 means same as src1) |

**Return value**: `ndarray`.

#### `subtract`

Element-wise subtraction.

```python
dst = cv2.subtract(src1, src2, dst=None, mask=None, dtype=-1)
```

Parameters same as `add`.

#### `multiply`

Element-wise multiplication.

```python
dst = cv2.multiply(src1, src2, dst=None, scale=None, dtype=-1)
```

| Parameter | Type | Description |
|------|------|------|
| `scale` | `float` | Optional, scale factor, default is 1.0 |

#### `divide`

Element-wise division.

```python
dst = cv2.divide(src1, src2, dst=None, scale=None, dtype=-1)
```

#### `addWeighted`

Weighted blending of two images.

```python
dst = cv2.addWeighted(src1, alpha, src2, beta, gamma, dst=None, dtype=-1)
```

Formula: `dst = alpha * src1 + beta * src2 + gamma`

| Parameter | Type | Description |
|------|------|------|
| `src1` | `ndarray` | First input |
| `alpha` | `float` | Weight of the first input |
| `src2` | `ndarray` | Second input |
| `beta` | `float` | Weight of the second input |
| `gamma` | `float` | Scalar added to each sum |

```python
result = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)
```

#### `absdiff`

Computes the element-wise absolute difference between two images.

```python
dst = cv2.absdiff(src1, src2, dst=None)
```

### Bitwise Operations

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

### Channel Operations

#### `split`

Splits a multi-channel image into a list of single channels.

```python
channels = cv2.split(m)
```

| Parameter | Type | Description |
|------|------|------|
| `m` | `ndarray` | Multi-channel input image |

**Return value**: `list[ndarray]`, each element is one channel.

```python
b, g, r = cv2.split(img)  # Split into B, G, R three channels
```

#### `merge`

Merges a list of single channels into a multi-channel image.

```python
merged = cv2.merge(mv)
```

| Parameter | Type | Description |
|------|------|------|
| `mv` | `list[ndarray]` | List of single-channel ndarrays |

**Return value**: `ndarray`, the merged multi-channel image.

```python
merged = cv2.merge([b_channel, g_channel, r_channel])
```

### Statistics and Normalization

#### `mean`

Compute the image mean.

```python
mean_vals = cv2.mean(src, mask=None)
```

**Return value**: `list[float]`, mean of each channel.

#### `normalize`

Normalize the image value range.

```python
dst = cv2.normalize(src, dst=None, alpha=None, beta=None, norm_type=cv2.NORM_L2, dtype=-1, mask=None)
```

| Parameter | Type | Description |
|------|------|------|
| `alpha` | `float` | Minimum value for range normalization, or target value for norm normalization |
| `beta` | `float` | Maximum value for range normalization (effective when `NORM_MINMAX`) |
| `norm_type` | `int` | Normalization type (see constants table) |

```python
normed = cv2.normalize(src, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
```

#### `compare`

Compare two images element-wise.

```python
dst = cv2.compare(src1, src2, cmpop)
```

| Parameter | Type | Description |
|------|------|------|
| `cmpop` | `int` | Comparison operation type (see constants table) |

**Return value**: `ndarray` (dtype=`uint8`), matching positions are 255, non-matching are 0.

```python
mask = cv2.compare(img, threshold_val, cv2.CMP_GT)
```

### Other core functions

#### `inRange`

Color range filter.

```python
dst = cv2.inRange(src, lowerb, upperb, dst=None)
```

| Parameter | Type | Description |
|------|------|------|
| `lowerb` | `ndarray` | Lower bound value (consistent with src channel count) |
| `upperb` | `ndarray` | Upper bound value |

```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lo = np.array([0, 50, 50], dtype=np.uint8)
hi = np.array([10, 255, 255], dtype=np.uint8)
mask = cv2.inRange(hsv, lo, hi)
```

#### `convertScaleAbs`

Scale and take absolute value, then convert to 8-bit.

```python
dst = cv2.convertScaleAbs(src, dst=None, alpha=None, beta=None)
```

`dst = saturate_cast<uchar>(|alpha * src + beta|)`

#### `minMaxLoc`

Find the minimum value, maximum value, and their positions.

```python
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(src, mask=None)
```

**Return value**: `(float, float, (int,int), (int,int))`

#### `LUT`

Look-up table mapping transformation.

```python
dst = cv2.LUT(src, lut, dst=None)
```

#### `countNonZero`

Count the number of non-zero pixels.

```python
count = cv2.countNonZero(src)
```

#### `flip`

Image flipping.

```python
dst = cv2.flip(src, flipCode, dst=None)
```

| `flipCode` | Effect |
|-----------|------|
| 0 | Vertical flip |
| 1 | Horizontal flip |
| -1 | Diagonal flip |

#### `rotate`

Image rotation.

```python
dst = cv2.rotate(src, rotateCode, dst=None)
```

See the rotation constants table for `rotateCode` values.

#### `transpose`

Matrix transpose.

```python
dst = cv2.transpose(src, dst=None)
```

### core Constants

| Constant | Value | Description |
|------|------|------|
| `ROTATE_90_CLOCKWISE` | 0 | Rotate 90° clockwise |
| `ROTATE_180` | 1 | Rotate 180° |
| `ROTATE_90_COUNTERCLOCKWISE` | 2 | Rotate 90° counterclockwise |
| `CMP_EQ` | 0 | Equal |
| `CMP_GT` | 1 | Greater than |
| `CMP_GE` | 2 | Greater than or equal |
| `CMP_LT` | 3 | Less than |
| `CMP_LE` | 4 | Less than or equal |
| `CMP_NE` | 5 | Not equal |
| `NORM_INF` | 1 | Infinity norm |
| `NORM_L1` | 2 | L1 norm |
| `NORM_L2` | 4 | L2 norm |
| `NORM_MINMAX` | 32 | Min-max normalization |

## imgproc — Image Processing

### Image Filtering

#### `Canny`

Canny edge detection.

```python
edges = cv2.Canny(image, threshold1, threshold2, edges=None, apertureSize=3, L2gradient=False)
```

| Parameter | Type | Description |
|------|------|------|
| `image` | `ndarray` | Input (single-channel grayscale image) |
| `threshold1` | `float` | Low threshold |
| `threshold2` | `float` | High threshold |
| `apertureSize` | `int` | Sobel kernel size, default 3 |
| `L2gradient` | `bool` | Whether to use L2 norm |

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 80, 200)
```

#### `GaussianBlur`

Gaussian blur.

```python
dst = cv2.GaussianBlur(src, ksize, sigmaX, dst=None, sigmaY=None, borderType=cv2.BORDER_DEFAULT)
```

| Parameter | Type | Description |
|------|------|------|
| `ksize` | `tuple(int,int)` | Kernel size, e.g. `(5, 5)`, must be odd |
| `sigmaX` | `float` | Standard deviation in X direction |

#### `blur`

Mean blur (box filter).

```python
dst = cv2.blur(src, ksize, dst=None, anchor=None, borderType=cv2.BORDER_DEFAULT)
```

#### `medianBlur`

Median blur.

```python
dst = cv2.medianBlur(src, ksize, dst=None)
```

`ksize` must be odd, e.g. 5.

#### `bilateralFilter`

Bilateral filter (edge-preserving denoising).

```python
dst = cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace, dst=None, borderType=cv2.BORDER_DEFAULT)
```

| Parameter | Type | Description |
|------|------|------|
| `d` | `int` | Diameter of pixel neighborhood |
| `sigmaColor` | `float` | Standard deviation in color space |
| `sigmaSpace` | `float` | Standard deviation in coordinate space |

#### `boxFilter`

Box filter.

```python
dst = cv2.boxFilter(src, ddepth, ksize, dst=None, anchor=None, normalize=True, borderType=cv2.BORDER_DEFAULT)
```

#### `filter2D`

Custom convolution kernel filter.

```python
dst = cv2.filter2D(src, ddepth, kernel, dst=None, anchor=None, delta=None, borderType=cv2.BORDER_DEFAULT)
```

| Parameter | Type | Description |
|------|------|------|
| `ddepth` | `int` | Output depth (-1 means same as input) |
| `kernel` | `ndarray` | Convolution kernel |
| `delta` | `float` | Optional offset added to each pixel |

```python
kernel = np.ones((3, 3), dtype=np.float) / 9.0
result = cv2.filter2D(img, -1, kernel)
```

#### `Sobel`

Sobel edge detection.

```python
dst = cv2.Sobel(src, ddepth, dx, dy, dst=None, ksize=3, scale=None, delta=None, borderType=cv2.BORDER_DEFAULT)
```

| Parameter | Type | Description |
|------|------|------|
| `dx` | `int` | Order of the derivative in X direction |
| `dy` | `int` | Order of the derivative in Y direction |
| `ksize` | `int` | Kernel size (1/3/5/7) |

```python
grad_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
grad_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=3)
```

#### `Scharr`

Scharr edge detection (higher accuracy than Sobel).

```python
dst = cv2.Scharr(src, ddepth, dx, dy, dst=None, scale=None, delta=None, borderType=cv2.BORDER_DEFAULT)
```

#### `Laplacian`

Laplacian edge detection.

```python
dst = cv2.Laplacian(src, ddepth, dst=None, ksize=1, scale=None, delta=None, borderType=cv2.BORDER_DEFAULT)
```

### Morphological Operations

#### `erode`

Erosion operation.

```python
dst = cv2.erode(src, kernel, dst=None, anchor=None, iterations=1, borderType=cv2.BORDER_CONSTANT)
```

#### `dilate`

Dilation operation.

```python
dst = cv2.dilate(src, kernel, dst=None, anchor=None, iterations=1, borderType=cv2.BORDER_CONSTANT)
```

#### `morphologyEx`

Advanced morphological operation.

```python
dst = cv2.morphologyEx(src, op, kernel, dst=None, anchor=None, iterations=1, borderType=cv2.BORDER_CONSTANT)
```

See the morphological constants table for `op` values.

```python
kernel = np.ones((3, 3), dtype=np.uint8)
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
```

#### `getStructuringElement`

Get structuring element.

```python
kernel = cv2.getStructuringElement(shape, ksize, anchor=None)
```

| Parameter | Type | Description |
|------|------|------|
| `shape` | `int` | Shape (`MORPH_RECT`/`MORPH_CROSS`/`MORPH_ELLIPSE`) |
| `ksize` | `tuple` | Size, e.g. `(5, 5)` |

### Threshold Processing

#### `threshold`

Global threshold segmentation.

```python
retval, dst = cv2.threshold(src, thresh, maxval, type, dst=None)
```

**Return value**: `(float, ndarray)` — The actual threshold used and the output image.

```python
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
ret, otsu   = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
```

#### `adaptiveThreshold`

Adaptive threshold segmentation.

```python
dst = cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C, dst=None)
```

| Parameter | Type | Description |
|------|------|------|
| `adaptiveMethod` | `int` | `ADAPTIVE_THRESH_MEAN_C` or `ADAPTIVE_THRESH_GAUSSIAN_C` |
| `blockSize` | `int` | Neighborhood size (odd number) |
| `C` | `float` | Constant subtracted from the mean/weighted mean |

```python
result = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, 2)
```

### Color Space Conversion

#### `cvtColor`

Color space conversion.

```python
dst = cv2.cvtColor(src, code, dst=None, dstCn=0)
```

| Parameter | Type | Description |
|------|------|------|
| `code` | `int` | Conversion code (see color conversion constants table) |
| `dstCn` | `int` | Target number of channels (0 means automatic) |

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
rgb  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
lab  = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
```

### Geometric Transformations

#### `resize`

Image resizing.

```python
dst = cv2.resize(src, dsize, dst=None, fx=None, fy=None, interpolation=cv2.INTER_LINEAR)
```

| Parameter | Type | Description |
|------|------|------|
| `dsize` | `tuple(int,int)` | Target size `(w, h)` |
| `fx` | `float` | Optional, X-direction scaling factor |
| `fy` | `float` | Optional, Y-direction scaling factor |

```python
small = cv2.resize(img, (160, 120))
```

#### `warpAffine`

Affine transformation.

```python
dst = cv2.warpAffine(src, M, dsize, dst=None, flags=cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_CONSTANT, borderValue=None)
```

`M` is a 2x3 transformation matrix.

#### `warpPerspective`

Perspective transformation.

```python
dst = cv2.warpPerspective(src, M, dsize, dst=None, flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=None)
```

`M` is a 3x3 transformation matrix.

> **Note**: `getPerspectiveTransform` / `getAffineTransform` consume a significant amount of stack space during internal matrix solving, which may trigger stack overflow on the default 128KB thread stack. It is recommended to call them from the main REPL thread or increase the thread stack size.

#### `getRotationMatrix2D`

Get a 2D rotation matrix.

```python
M = cv2.getRotationMatrix2D(center, angle, scale)
```

| Parameter | Type | Description |
|------|------|------|
| `center` | `tuple(int,int)` | Rotation center |
| `angle` | `float` | Rotation angle (in degrees, positive is counterclockwise) |
| `scale` | `float` | Scaling factor |

```python
M = cv2.getRotationMatrix2D((160, 120), 45, 1.0)
rotated = cv2.warpAffine(img, M, (320, 240))
```

#### `getAffineTransform` ⚠

Computes a 2x3 affine transformation matrix from three pairs of points.

```python
M = cv2.getAffineTransform(src, dst)
```

`src` and `dst` are 3x2 point-set matrices.

#### `getPerspectiveTransform` ⚠

Computes a 3x3 perspective transformation matrix from four pairs of points.

```python
M = cv2.getPerspectiveTransform(src, dst, solveMethod=cv2.DECOMP_LU)
```

`src` and `dst` are 4x2 point-set matrices.

#### `remap`

Pixel remapping.

```python
dst = cv2.remap(src, map1, map2, interpolation, dst=None,
                borderMode=cv2.BORDER_CONSTANT, borderValue=None)
```

| Parameter | Type | Description |
|------|------|------|
| `map1` | `ndarray` | X coordinate mapping table |
| `map2` | `ndarray` | Y coordinate mapping table |
| `interpolation` | `int` | Interpolation method (see interpolation constants table) |

### Image Pyramid

#### `pyrDown`

Gaussian pyramid downsampling.

```python
dst = cv2.pyrDown(src, dst=None, dstsize=None, borderType=cv2.BORDER_DEFAULT)
```

Image size is halved.

#### `pyrUp`

Gaussian pyramid upsampling.

```python
dst = cv2.pyrUp(src, dst=None, dstsize=None, borderType=cv2.BORDER_DEFAULT)
```

Image size is doubled.

### Drawing Functions

All drawing functions modify the input image in-place and return it, supporting chained calls.

#### `line`

Draws a straight line.

```python
img = cv2.line(img, pt1, pt2, color, thickness=1, lineType=cv2.LINE_8, shift=0)
```

| Parameter | Type | Description |
|------|------|------|
| `pt1` | `tuple(int,int)` | Starting point |
| `pt2` | `tuple(int,int)` | Ending point |
| `color` | `tuple` | Color, BGR tuple such as `(0, 255, 0)` |

#### `rectangle`

Draws a rectangle.

```python
img = cv2.rectangle(img, pt1, pt2, color, thickness=1, lineType=cv2.LINE_8, shift=0)
```

When `thickness=-1`, the rectangle is filled.

```python
cv2.rectangle(img, (10, 10), (80, 60), (0, 0, 255), -1)  # Fill red rectangle
```

#### `circle`

Draws a circle.

```python
img = cv2.circle(img, center, radius, color, thickness=1, lineType=cv2.LINE_8, shift=0)
```

#### `ellipse`

Draws an ellipse/arc.

```python
img = cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color,
                  thickness=1, lineType=cv2.LINE_8, shift=0)
```

| Parameter | Type | Description |
|------|------|------|
| `center` | `tuple` | Center of the ellipse |
| `axes` | `tuple` | Half-axis lengths `(a, b)` |
| `angle` | `float` | Rotation angle |
| `startAngle` | `float` | Starting angle |
| `endAngle` | `float` | Ending angle |

#### `putText`

Draws text.

```python
img = cv2.putText(img, text, org, fontFace, fontScale, color,
                  thickness=1, lineType=cv2.LINE_8, bottomLeftOrigin=False)
```

| Parameter | Type | Description |
|------|------|------|
| `text` | `str` | Text content |
| `org` | `tuple` | Position of the bottom-left corner of the text |
| `fontFace` | `int` | Font (see font constants table) |
| `fontScale` | `float` | Font scale factor |

#### `arrowedLine`

Draws a line segment with an arrow.

```python
img = cv2.arrowedLine(img, pt1, pt2, color, thickness=1, line_type=cv2.LINE_8, shift=0, tipLength=None)
```

#### `drawMarker`

Draws a marker point.

```python
img = cv2.drawMarker(img, position, color, markerType=cv2.MARKER_CROSS,
                     markerSize=20, thickness=1, line_type=cv2.LINE_8)
```

See marker constants table for `markerType`.

#### `fillPoly`

Fills a polygon.

```python
img = cv2.fillPoly(img, pts, color, lineType=cv2.LINE_8, shift=0, offset=None)
```

`pts` is a list of contour points, where each contour is an Nx2 ndarray.

```python
tri = np.array([[20, 20], [80, 20], [50, 80]], dtype=np.float)
cv2.fillPoly(img, [tri], (0, 255, 0))
```

#### `polylines`

Draws polygon outlines.

```python
img = cv2.polylines(img, pts, isClosed, color, thickness=1, lineType=cv2.LINE_8, shift=0)
```

#### `getTextSize`

Gets the rendered text size.

```python
size, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
```

**Return value**: `((width, height), baseline)`

### Contour Analysis

#### `findContours`

Find contours in a binary image.

```python
contours, hierarchy = cv2.findContours(image, mode, method, contours=None, hierarchy=None, offset=None)
```

| Parameter | Type | Description |
|------|------|------|
| `mode` | `int` | Contour retrieval mode (`RETR_EXTERNAL`/`RETR_LIST`/`RETR_CCOMP`/`RETR_TREE`) |
| `method` | `int` | Contour approximation method (`CHAIN_APPROX_SIMPLE`/`CHAIN_APPROX_NONE` etc.) |

**Return value**: `(list[ndarray], ndarray)` — list of contours and hierarchy.

#### `drawContours`

Draw contours.

```python
img = cv2.drawContours(image, contours, contourIdx, color, thickness=1,
                       lineType=cv2.LINE_8, hierarchy=None, maxLevel=INT_MAX, offset=None)
```

When `contourIdx=-1`, all contours are drawn.

#### `contourArea`

Calculate the contour area.

```python
area = cv2.contourArea(contour, oriented=False)
```

#### `arcLength`

Calculate the contour perimeter.

```python
perimeter = cv2.arcLength(curve, closed)
```

#### `boundingRect`

Calculate the bounding upright rectangle.

```python
x, y, w, h = cv2.boundingRect(array)
```

#### `approxPolyDP`

Polygon approximation.

```python
approx = cv2.approxPolyDP(curve, epsilon, closed)
```

`epsilon` is usually set to `0.02 * cv2.arcLength(curve, True)`.

#### `convexHull`

Compute the convex hull.

```python
hull = cv2.convexHull(points, hull=None, clockwise=False, returnPoints=True)
```

| Parameter | Type | Description |
|------|------|------|
| `returnPoints` | `bool` | `True` returns point coordinates; `False` returns point indices of the contour (used for `convexityDefects`) |

#### `minAreaRect`

Minimum enclosing rotated rectangle.

```python
center, size, angle = cv2.minAreaRect(points)
```

**Return value**: `((cx, cy), (w, h), angle)` — center, size, rotation angle.

#### `minEnclosingCircle`

Minimum enclosing circle.

```python
center, radius = cv2.minEnclosingCircle(points)
```

#### `fitEllipse`

Fit an ellipse.

```python
center, size, angle = cv2.fitEllipse(points)
```

> At least 5 points are required as input.

#### `fitLine`

Fit a line.

```python
line = cv2.fitLine(points, distType, param, reps, aeps)
```

**Return value**: `(vx, vy, x0, y0)` — unit direction vector + a point on the line.

#### `pointPolygonTest`

Test the positional relationship between a point and a contour.

```python
dist = cv2.pointPolygonTest(contour, pt, measureDist)
```

| `measureDist` | Behavior |
|--------------|------|
| `True` | Returns signed shortest distance |
| `False` | Returns +1 (inside), 0 (on edge), -1 (outside) |

#### `convexityDefects`

Compute convexity defects.

```python
defects = cv2.convexityDefects(contour, convexhull)
```

`convexhull` must be a 1D index array (i.e., the output of `convexHull(..., returnPoints=False)`).

#### `matchShapes`

Shape matching (based on Hu moments).

```python
score = cv2.matchShapes(contour1, contour2, method, parameter)
```

#### `isContourConvex`

Determine whether a contour is convex.

```python
result = cv2.isContourConvex(contour)
```

Returns `bool`.

### Template Matching

#### `matchTemplate`

Template matching.

```python
result = cv2.matchTemplate(image, templ, method, result=None, mask=None)
```

See the `TM_*` constants table for optional values of `method`.

```python
result = cv2.matchTemplate(img, templ, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(result)
```

### Image Moments

#### `moments`

Computes image moments.

```python
m = cv2.moments(array, binaryImage=False)
```

Returns a `dict` containing spatial moments (`m00`, `m10`, ...), central moments (`mu20`, ...), and normalized central moments (`nu20`, ...).

```python
m = cv2.moments(binary)
cx = m['m10'] / m['m00']  # Centroid X
cy = m['m01'] / m['m00']  # Centroid Y
```

### Hough Transform

#### `HoughLines`

Standard Hough line detection.

```python
lines = cv2.HoughLines(image, rho, theta, threshold, lines=None,
                       srn=None, stn=None, min_theta=None, max_theta=None)
```

**Return value**: Nx2 ndarray, each row is `(rho, theta)`.

#### `HoughLinesP`

Probabilistic Hough line detection (line segments).

```python
lines = cv2.HoughLinesP(image, rho, theta, threshold, lines=None,
                        minLineLength=None, maxLineGap=None)
```

**Return value**: Nx4 ndarray, each row is `(x1, y1, x2, y2)`.

```python
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=30)
for i in range(lines.shape[0]):
    x1, y1, x2, y2 = lines[i, 0], lines[i, 1], lines[i, 2], lines[i, 3]
```

#### `HoughCircles`

Hough circle detection.

```python
circles = cv2.HoughCircles(image, method, dp, minDist, circles=None,
                           param1=None, param2=None, minRadius=0, maxRadius=0)
```

| Parameter | Type | Description |
|------|------|------|
| `method` | `int` | Detection method (3 = `HOUGH_GRADIENT`) |
| `dp` | `float` | Inverse ratio of accumulator resolution to image resolution |
| `minDist` | `float` | Minimum distance between circle centers |
| `param1` | `float` | Canny high threshold, default 100 |
| `param2` | `float` | Circle center accumulator threshold, default 100 |
| `minRadius` | `int` | Minimum radius |
| `maxRadius` | `int` | Maximum radius |

**Return value**: Nx3 ndarray, each row is `(cx, cy, r)`.

### Histogram

#### `calcHist`

Computes the image histogram.

```python
hist = cv2.calcHist(images, channels, mask, histSize, ranges)
```

| Parameter | Type | Description |
|------|------|------|
| `images` | `list[ndarray]` | Input image list |
| `channels` | `list[int]` | List of channel indices to compute |
| `mask` | `ndarray` or `None` | Optional 8-bit single-channel mask |
| `histSize` | `list[int]` | Number of bins for each dimension |
| `ranges` | `list[float]` | Value range for each dimension (flattened list) |

```python
hist = cv2.calcHist([img], [0], None, [32], [0, 256])
```

#### `calcBackProject`

Histogram back projection.

```python
dst = cv2.calcBackProject(images, channels, hist, dst=None, ranges, scale=None)
```

Used to find regions in an image that match a histogram.

#### `compareHist`

Histogram comparison.

```python
score = cv2.compareHist(H1, H2, method)
```

See the `HISTCMP_*` constants table for `method` values.

#### `equalizeHist`

Histogram equalization.

```python
dst = cv2.equalizeHist(src, dst=None)
```

### Corner Detection

#### `cornerHarris`

Harris corner detection.

```python
dst = cv2.cornerHarris(src, blockSize, ksize, k, dst=None, borderType=cv2.BORDER_DEFAULT)
```

| Parameter | Type | Description |
|------|------|------|
| `blockSize` | `int` | Neighborhood size for corner detection |
| `ksize` | `int` | Sobel aperture size |
| `k` | `float` | Harris detector free parameter (typically 0.04-0.06) |

#### `goodFeaturesToTrack`

Shi-Tomasi corner detection.

```python
corners = cv2.goodFeaturesToTrack(image, maxCorners, qualityLevel, minDistance,
                                  mask=None, blockSize=3, useHarrisDetector=False, k=None)
```

| Parameter | Type | Description |
|------|------|------|
| `maxCorners` | `int` | Maximum number of corners |
| `qualityLevel` | `float` | Quality threshold (0.01-0.1) |
| `minDistance` | `float` | Minimum Euclidean distance between corners |
| `blockSize` | `int` | Window size for gradient computation |

**Return value**: Nx2 ndarray, each row is `(x, y)` (float coordinates).

#### `cornerSubPix` ⚠

Sub-pixel accurate corner localization.

```python
refined = cv2.cornerSubPix(image, corners, winSize, zeroZone, criteria)
```

| Parameter | Type | Description |
|------|------|------|
| `corners` | `ndarray` | Initial corner coordinates (e.g., output of `goodFeaturesToTrack`) |
| `winSize` | `tuple` | Half-width of the search window |
| `zeroZone` | `tuple` | Half-width of the dead zone |
| `criteria` | `tuple` | Termination criteria `(type, maxCount, epsilon)`, e.g., `(3, 30, 0.001)` |

> **Platform limitation**: The `InputOutputArray(std::vector<Point2f>&)` wrapping path of this ported OpenCV is inconsistent with the standard version, and calls will trigger a `count >= 0` assertion failure. For real-time detection scenarios, please use `goodFeaturesToTrack` instead.

### Image Segmentation

#### `watershed`

Watershed segmentation.

```python
markers = cv2.watershed(image, markers)
```

| Parameter | Type | Description |
|------|------|------|
| `image` | `ndarray` | 3-channel 8-bit input image |
| `markers` | `ndarray` | int32 marker image (input/output parameter) |

#### `distanceTransform`

Distance transform.

```python
dst = cv2.distanceTransform(src, distanceType, maskSize, dst=None, dstType=cv2.CV_32F, labelType=cv2.DIST_LABEL_CCOMP)
```

| Parameter | Type | Description |
|------|------|------|
| `distanceType` | `int` | Distance type (`DIST_L1`/`DIST_L2`/`DIST_C`) |
| `maskSize` | `int` | Distance transform mask size (3 or 5) |

#### `floodFill`

Flood fill.

```python
filled, rect = cv2.floodFill(image, mask, seedPoint, newVal, loDiff=None, upDiff=None, flags=4)
```

**Return value**: `(ndarray, (x, y, w, h))` — filled image and filled region bounding box.

```python
filled, rect = cv2.floodFill(img, None, (50, 50), (0, 255, 0))
```

#### `grabCut` ⚠

GrabCut foreground segmentation.

```python
mask, bgd, fgd = cv2.grabCut(img, mask, rect, bgdModel, fgdModel, iterCount, mode=cv2.GC_INIT_WITH_RECT)
```

> **Note**: The internal GMM iteration stack consumption is relatively large, and may overflow under the default 128KB thread stack. It is recommended to increase the stack or call it from the main REPL thread.

#### `connectedComponents`

Connected components labeling.

```python
nlabels, labels = cv2.connectedComponents(image, labels=None, connectivity=8, ltype=cv2.CV_32S)
```

**Return value**: `(int, ndarray)` — number of labels and marker image.

## highgui — Interaction

### `waitKey`

Wait for a key press.

```python
key = cv2.waitKey(delay=0)
```

| `delay` | Behavior |
|--------|------|
| 0 | Wait indefinitely |
| >0 | Wait up to `delay` milliseconds, then return -1 on timeout |

On the K230 MicroPython, input is read from the serial REPL.

### `waitKeyEx`

Enhanced version of `waitKey`, behaves the same as `waitKey`.

```python
key = cv2.waitKeyEx(delay=0)
```

## Constant Reference

### Morphology Constants

| Constant | Value | Description |
|------|------|------|
| `MORPH_ERODE` | 0 | Erosion |
| `MORPH_DILATE` | 1 | Dilation |
| `MORPH_OPEN` | 2 | Opening |
| `MORPH_CLOSE` | 3 | Closing |
| `MORPH_GRADIENT` | 4 | Morphological Gradient |
| `MORPH_TOPHAT` | 5 | Top Hat |
| `MORPH_BLACKHAT` | 6 | Black Hat |
| `MORPH_HITMISS` | 7 | Hit-or-Miss |
| `MORPH_RECT` | 0 | Rectangular structuring element |
| `MORPH_CROSS` | 1 | Cross-shaped structuring element |
| `MORPH_ELLIPSE` | 2 | Elliptical structuring element |

### Threshold Constants

| Constant | Value | Description |
|------|------|------|
| `THRESH_BINARY` | 0 | Binary |
| `THRESH_BINARY_INV` | 1 | Inverse Binary |
| `THRESH_TRUNC` | 2 | Truncate |
| `THRESH_TOZERO` | 3 | To Zero |
| `THRESH_TOZERO_INV` | 4 | To Zero Inverted |
| `THRESH_OTSU` | 8 | OTSU (can be combined with the above) |
| `THRESH_TRIANGLE` | 16 | Triangle method |

### Adaptive Threshold Constants

| Constant | Value | Description |
|------|------|------|
| `ADAPTIVE_THRESH_MEAN_C` | 0 | Mean method |
| `ADAPTIVE_THRESH_GAUSSIAN_C` | 1 | Gaussian method |

### Border Constants

| Constant | Value |
|------|------|
| `BORDER_CONSTANT` | 0 |
| `BORDER_REPLICATE` | 1 |
| `BORDER_REFLECT` | 2 |
| `BORDER_WRAP` | 3 |
| `BORDER_REFLECT_101` | 4 |
| `BORDER_DEFAULT` | 4 |
| `BORDER_TRANSPARENT` | 5 |
| `BORDER_ISOLATED` | 16 |

### Interpolation Constants

| Constant | Value | Description |
|------|------|------|
| `INTER_NEAREST` | 0 | Nearest neighbor |
| `INTER_LINEAR` | 1 | Bilinear (default) |
| `INTER_CUBIC` | 2 | Bicubic |
| `INTER_AREA` | 3 | Area interpolation |
| `INTER_LANCZOS4` | 4 | Lanczos |
| `INTER_LINEAR_EXACT` | 5 | Exact bilinear |
| `INTER_MAX` | 7 | Interpolation mask |
| `WARP_FILL_OUTLIERS` | 8 | Fill outliers |
| `WARP_INVERSE_MAP` | 16 | Inverse mapping |

### Color Conversion Constants

| Constant | Value | Description |
|------|------|------|
| `COLOR_BGR2GRAY` | 6 | BGR → Grayscale |
| `COLOR_RGB2GRAY` | 7 | RGB → Grayscale |
| `COLOR_GRAY2BGR` | 8 | Grayscale → BGR |
| `COLOR_GRAY2RGB` | 8 | Grayscale → RGB |
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

### Font Constants

| Constant | Value |
|------|------|
| `FONT_HERSHEY_SIMPLEX` | 0 |
| `FONT_HERSHEY_PLAIN` | 1 |
| `FONT_HERSHEY_DUPLEX` | 2 |
| `FONT_HERSHEY_COMPLEX` | 3 |
| `FONT_HERSHEY_TRIPLEX` | 4 |
| `FONT_HERSHEY_COMPLEX_SMALL` | 5 |
| `FONT_HERSHEY_SCRIPT_SIMPLEX` | 6 |
| `FONT_HERSHEY_SCRIPT_COMPLEX` | 7 |
| `FONT_ITALIC` | 16 (can be combined with the above) |

### Line Constants

| Constant | Value | Description |
|------|------|------|
| `LINE_4` | 4 | 4-connected line |
| `LINE_8` | 8 | 8-connected line |
| `LINE_AA` | 16 | Anti-aliased line |
| `FILLED` | -1 | Filled (used for thickness parameter) |

### Contour Constants

| Constant | Value | Description |
|------|------|------|
| `RETR_EXTERNAL` | 0 | Only detect the outermost contours |
| `RETR_LIST` | 1 | Detect all contours |
| `RETR_CCOMP` | 2 | Two-level hierarchy |
| `RETR_TREE` | 3 | Full hierarchy tree |
| `RETR_FLOODFILL` | 4 | Flood fill |
| `CHAIN_APPROX_NONE` | 1 | Save all contour points |
| `CHAIN_APPROX_SIMPLE` | 2 | Compress and retain endpoints |
| `CHAIN_APPROX_TC89_L1` | 3 | Teh-Chin chain L1 |
| `CHAIN_APPROX_TC89_KCOS` | 4 | Teh-Chin chain kCos |

### Shape Matching Constants

| Constant | Value | Description |
|------|------|------|
| `CONTOURS_MATCH_I1` | 1 | Method 1 |
| `CONTOURS_MATCH_I2` | 2 | Method 2 |
| `CONTOURS_MATCH_I3` | 3 | Method 3 |

### Connected Components Constants

| Constant | Value | Description |
|------|------|------|
| `CONNECTED_4` | 4 | 4-connected |
| `CONNECTED_8` | 8 | 8-connected |
| `CCL_DEFAULT` | -1 | Default algorithm |
| `CCL_WU` | 0 | Wu |
| `CCL_GRANA` | 1 | Grana |
| `CCL_BOLELLI` | 2 | Bolelli |
| `CCL_SAUF` | 3 | SAUF |
| `CCL_BBDT` | 4 | BBDT |
| `CCL_SPAGHETTI` | 5 | Spaghetti |

### Distance Transform Constants

| Constant | Value | Description |
|------|------|------|
| `DIST_L1` | 1 | Manhattan distance |
| `DIST_L2` | 2 | Euclidean distance |
| `DIST_C` | 3 | Chebyshev distance |
| `DIST_L12` | 4 | L1-L2 hybrid |
| `DIST_FAIR` | 5 | Fair |
| `DIST_WELSCH` | 6 | Welsch |
| `DIST_HUBER` | 7 | Huber |
| `DIST_LABEL_CCOMP` | 0 | CComp labeling |
| `DIST_LABEL_PIXEL` | 1 | Pixel labeling |

### Template Matching Constants

| Constant | Value | Description |
|------|------|------|
| `TM_SQDIFF` | 0 | Squared difference |
| `TM_SQDIFF_NORMED` | 1 | Normalized squared difference |
| `TM_CCORR` | 2 | Correlation |
| `TM_CCORR_NORMED` | 3 | Normalized correlation |
| `TM_CCOEFF` | 4 | Correlation coefficient |
| `TM_CCOEFF_NORMED` | 5 | Normalized correlation coefficient |

### Marker Type Constants

| Constant | Value |
|------|------|
| `MARKER_CROSS` | 0 |
| `MARKER_TILTED_CROSS` | 1 |
| `MARKER_STAR` | 2 |
| `MARKER_DIAMOND` | 3 |
| `MARKER_SQUARE` | 4 |
| `MARKER_TRIANGLE_UP` | 5 |
| `MARKER_TRIANGLE_DOWN` | 6 |

### Histogram Comparison Constants

| Constant | Value | Description |
|------|------|------|
| `HISTCMP_CORREL` | 0 | Correlation |
| `HISTCMP_CHISQR` | 1 | Chi-square |
| `HISTCMP_INTERSECT` | 2 | Intersection |
| `HISTCMP_BHATTACHARYYA` | 3 | Bhattacharyya |
| `HISTCMP_HELLINGER` | 3 | Hellinger (same as Bhattacharyya) |
| `HISTCMP_CHISQR_ALT` | 4 | Alternative Chi-square |
| `HISTCMP_KL_DIV` | 5 | KL divergence |

### GrabCut Constants

| Constant | Value | Description |
|------|------|------|
| `GC_BGD` | 0 | Definite background |
| `GC_FGD` | 1 | Definite foreground |
| `GC_PR_BGD` | 2 | Probable background |
| `GC_PR_FGD` | 3 | Probable foreground |
| `GC_INIT_WITH_RECT` | 0 | Rectangle initialization |
| `GC_INIT_WITH_MASK` | 1 | Mask initialization |
| `GC_EVAL` | 2 | Evaluation mode |
| `GC_EVAL_FREEZE_MODEL` | 3 | Freeze model evaluation |

### Termination Criteria Constants

| Constant | Value | Description |
|------|------|------|
| `TERM_CRITERIA_COUNT` | 1 | Iteration count |
| `TERM_CRITERIA_EPS` | 2 | Precision |
| `TERM_CRITERIA_MAX_ITER` | 1 | Maximum iterations (same as COUNT) |

## Usage Examples

### Complete Workflow: Read, Process, Save

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

### Image Arithmetic Blending

```python
img1 = cv2.imread("/sdcard/img1.jpg")
img2 = cv2.imread("/sdcard/img2.jpg")
blended = cv2.addWeighted(img1, 0.6, img2, 0.4, 0)
cv2.imwrite("/sdcard/blended.jpg", blended)
```

### Color Segmentation (inRange)

```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
green_lo = np.array([35, 50, 50], dtype=np.uint8)
green_hi = np.array([85, 255, 255], dtype=np.uint8)
mask = cv2.inRange(hsv, green_lo, green_hi)
result = cv2.bitwise_and(img, img, mask=mask)
```

### Histogram Analysis

```python
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
score = cv2.compareHist(hist, hist2, cv2.HISTCMP_CORREL)
```

### Real-time Camera Detection

Capture frames from the camera, convert to numpy, and process in real-time with OpenCV. An image resolution of 320x240 is recommended for higher frame rates.

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

> More real-time detection examples are located in the development board firmware at `/sdcard/examples/24-OpenCV/`, corresponding to the SDK source directory `src/canmv/resources/examples/24-OpenCV/`, with the filename pattern `demo_camera_*.py`.
