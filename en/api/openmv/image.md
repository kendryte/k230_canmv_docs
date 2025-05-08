# 3.11 `Image` Processing API Manual

This module is ported from `openmv` with similar functionalities. For more details, please refer to the [official documentation](https://docs.openmv.io/library/omv.image.html). This document lists the differences from the official API and the newly added APIs, and includes references to some native APIs.

## 1. Class `Image`

The `Image` class is the fundamental object for machine vision processing. This class supports creating image objects from memory regions such as Micropython GC, MMZ, system heap, and VB area. Additionally, images can be created directly by referencing external memory (ALLOC_REF). Unused image objects are automatically released during garbage collection, but memory can also be manually released.

Supported image formats are:

- BINARY
- GRAYSCALE
- RGB565
- BAYER
- YUV422
- JPEG
- PNG
- ARGB8888 (new)
- RGB888 (new)
- RGBP888 (new)
- YUV420 (new)

Supported memory allocation regions:

- **ALLOC_MPGC**: Micropython managed memory
- **ALLOC_HEAP**: System heap memory
- **ALLOC_MMZ**: Multimedia memory
- **ALLOC_VB**: Video buffer
- **ALLOC_REF**: Memory using reference objects, no new memory allocation

### 1.1 Constructor

```python
image.Image(path, alloc=ALLOC_MMZ, cache=True, phyaddr=0, virtaddr=0, poolid=0, data=None)
```

Creates an image object from the file path `path`, supporting BMP, PGM, PPM, JPG, and JPEG formats.

```python
image.Image(w, h, format, alloc=ALLOC_MMZ, cache=True, phyaddr=0, virtaddr=0, poolid=0, data=None)
```

Creates an image object with specified size and format.

- **w**: Image width
- **h**: Image height
- **format**: Image format
- **alloc**: Memory allocation method (default is ALLOC_MMZ)
- **cache**: Whether to enable memory cache (default enabled)
- **phyaddr**: Physical memory address, only applicable for VB area
- **virtaddr**: Virtual memory address, only applicable for VB area
- **poolid**: Pool ID for VB area, only applicable for VB area
- **data**: Reference to external data object (optional)

Example:

```python
# Create a 640x480 image in ARGB8888 format in the MMZ area
img = image.Image(640, 480, image.ARGB8888)
 
# Create a 640x480 image in YUV420 format in the VB area
img = image.Image(640, 480, image.YUV420, alloc=image.ALLOC_VB, phyaddr=xxx, virtaddr=xxx, poolid=xxx)
 
# Create a 640x480 image in RGB888 format using external reference
img = image.Image(640, 480, image.RGB888, alloc=image.ALLOC_REF, data=buffer_obj)
```

Manually release image memory:

```python
del img
gc.collect()
```

### 1.2 `phyaddr`

Get the physical memory address of the image data.

```python
image.phyaddr()
```

### 1.3 `virtaddr`

Get the virtual memory address of the image data.

```python
image.virtaddr()
```

### 1.4 `poolid`

Get the VB pool ID of the image.

```python
image.poolid()
```

### 1.5 `to_rgb888`

Convert the image to RGB888 format and return a new image object.

```python
image.to_rgb888(x_scale=1.0, y_scale=1.0, roi=None, rgb_channel=-1, alpha=256, color_palette=None, alpha_palette=None, hint=0, alloc=ALLOC_MMZ, cache=True, phyaddr=0, virtaddr=0, poolid=0)
```

### 1.6 `copy_from`

Copy the content of `src_img` to the current image object.

```python
image.copy_from(src_img)
```

### 1.7 `copy_to`

Copy the content of the current image object to `dst_img`.

```python
image.copy_to(dst_img)
```

### 1.8 `to_numpy_ref`

Convert the image object to a NumPy array, with the returned NumPy array sharing memory with the original image object.

```python
image.to_numpy_ref()
```

Supported formats: GRAYSCALE, RGB565, ARGB8888, RGB888, RGBP888.

### 1.9 `draw_string_advanced`

Enhanced `draw_string`, supporting Chinese display and allowing custom fonts via the `font` parameter.

```python
image.draw_string_advanced(x, y, char_size, str, [color, font])
```

### 1.10 Methods with Differences

#### 1.10.1 Removed `crop` Parameter

The following APIs have the `crop` parameter removed, added memory allocation method parameter, and always return a new image object.

- `to_bitmap` method
- `to_grayscale` method
- `to_rgb565` method
- `to_rainbow` method
- `to_ironbow` method
- `to_jpeg` method
- `to_png` method
- `copy` method
- `crop` method
- `scale` method

#### 1.10.2 Drawing APIs

Added support for `ARGB8888` and `RGB888` formats, other formats are not supported.

#### 1.10.3 BINARY API

The `binary` method added a memory allocation method parameter, effective only when `copy=True`.

#### 1.10.4 POOL API

The `mean_pooled` and `midpoint_pooled` methods added a memory allocation method parameter.

#### 1.10.5 Other Image Algorithms

These algorithms only support native image formats, `RGB888` format needs to be converted before use.

### 1.11 `width`

```python
image.width()
```

Returns the width of the image in pixels.

### 1.12 `height`

```python
image.height()
```

Returns the height of the image in pixels.

### 1.13 `format`

```python
image.format()
```

Returns the format of the image, possible values include:

- `sensor.GRAYSCALE`: Grayscale image
- `sensor.RGB565`: RGB image
- `sensor.JPEG`: JPEG compressed image

### 1.14 `size`

```python
image.size()
```

Returns the size of the image in bytes.

### 1.15 `get_pixel`

```python
image.get_pixel(x, y[, rgbtuple])
```

Get the pixel value at the specified position `(x, y)` according to the image format:

- For grayscale images, returns the grayscale value.
- For RGB565 images, returns an RGB888 tuple `(r, g, b)`.
- For Bayer images, returns the pixel value at that position.

Compressed images are not supported.

> `get_pixel()` and `set_pixel()` are the only methods to operate on Bayer mode images. Bayer mode images are a special format where even rows contain `R/G/R/G/...` and odd rows contain `G/B/G/B/...` pixels, with each pixel occupying 8 bits.

### 1.16 `set_pixel`

```python
image.set_pixel(x, y, pixel)
```

Set the pixel value at the specified position `(x, y)`:

- For grayscale images, set the grayscale value.
- For RGB images, set an RGB888 tuple `(r, g, b)`.

Compressed images are not supported.

> `get_pixel()` and `set_pixel()` are the only methods to operate on Bayer mode images.

### 1.17 `mean_pool`

```python
image.mean_pool(x_div, y_div)
```

Divide the image into `x_div * y_div` rectangular regions and compute the average value for each region, returning a modified image containing these average values.

This method can be used to quickly downscale an image.

Compressed images and Bayer images are not supported.

### 1.18 `mean_pooled`

```python
image.mean_pooled(x_div, y_div)
```

Similar to `mean_pool()`, but returns a new image copy.

### 1.19 `midpoint_pool`

```python
image.midpoint_pool(x_div, y_div[, bias=0.5])
```

Divide the image into `x_div * y_div` regions and compute the midpoint value for each region, returning a modified image containing these midpoint values.

- When `bias=0.0`, returns the minimum value of the region, and when `bias=1.0`, returns the maximum value.

### 1.20 `midpoint_pooled`

```python
image.midpoint_pooled(x_div, y_div[, bias=0.5])
```

Similar to `midpoint_pool()`, but returns a new image copy.

### 1.21 `to_grayscale`

```python
image.to_grayscale([copy=False])
```

Convert the image to grayscale. If `copy=True`, a new image copy is created on the heap. Returns the image object.

### 1.22 `to_rgb565`

```python
image.to_rgb565([copy=False])
```

Convert the image to RGB565 format. If `copy=True`, a new image copy is created on the heap. Returns the image object.

### 1.23 `to_rainbow`

```python
image.to_rainbow([copy=False])
```

Convert the image to rainbow color. Returns the image object.

### 1.24 `compress`

```python
image.compress([quality=50])
```

JPEG compress the image with the specified quality `quality` (0-100).

### 1.25 `compress_for_ide`

```python
image.compress_for_ide([quality=50])
```

Compress the image and format it for display in OpenMV IDE.

### 1.26 `compressed`

```python
image.compressed([quality=50])
```

Return the JPEG compressed image.

### 1.27 `compressed_for_ide`

```python
image.compressed_for_ide([quality=50])
```

Return the JPEG compressed image, formatted for display in OpenMV IDE.

### 1.28 `copy`

```python
image.copy([roi[, copy_to_fb=False]])
```

Create a copy of the image object, supporting a region of interest `roi`.

### 1.29 `save`

```python
image.save(path[, roi[, quality=50]])
```

Save the image to the specified path `path`, supporting a region of interest `roi` and JPEG compression quality `quality`.

### 1.30 `clear`

```python
image.clear()
```

Quickly set all pixels in the image to zero. Returns the image object.

### 1.31 `draw_line`

```python
image.draw_line(x0, y0, x1, y1[, color[, thickness=1]])
```

Draw a line from `(x0, y0)` to `(x1, y1)` on the image. Parameters can be passed separately as `x0, y0, x1, y1` or as a tuple `(x0, y0, x1, y1)`.

- **color**: An RGB888 tuple representing the color, applicable for grayscale or RGB565 images, default is white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the line, default is 1.

This method returns the image object, allowing chaining other methods.

Compressed images and Bayer format images are not supported.

### 1.32 `draw_rectangle`

```python
image.draw_rectangle(x, y, w, h[, color[, thickness=1[, fill=False]]])
```

Draw a rectangle on the image. Parameters can be passed separately as `x, y, w, h` or as a tuple `(x, y, w, h)`.

- **color**: An RGB888 tuple representing the color, applicable for grayscale or RGB565 images, default is white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the rectangle border, default is 1.
- **fill**: When set to `True`, fills the interior of the rectangle, default is `False`.

This method returns the image object, allowing chaining other methods.

Compressed images and Bayer format images are not supported.

### 1.33 `draw_ellipse`

```python
image.draw_ellipse(cx, cy, rx, ry, rotation[, color[, thickness=1[, fill=False]]])
```

Draw an ellipse on the image. Parameters can be passed separately as `cx, cy, rx, ry, rotation` or as a tuple `(cx, cy, rx, ry, rotation)`.

- **color**: An RGB888 tuple representing the color, applicable for grayscale or RGB565 images, default is white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the ellipse border, default is 1.
- **fill**: When set to `True`, fills the interior of the ellipse, default is `False`.

This method returns the image object, allowing chaining other methods.

Compressed images and Bayer format images are not supported.

### 1.34 `draw_circle`

```python
image.draw_circle(x, y, radius[, color[, thickness=1[, fill=False]]])
```

Draw a circle on the image. Parameters can be passed separately as `x, y, radius` or as a tuple `(x, y, radius)`.

- **color**: An RGB888 tuple representing the color, applicable for grayscale or RGB565 images, default is white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the circle border, default is 1.
- **fill**: When set to `True`, fills the interior of the circle, default is `False`.

This method returns the image object, allowing chaining other methods.

Compressed images and Bayer format images are not supported.

Draw text of size 8x10 starting from position `(x, y)` on the image.

### 1.35 `draw_string`

```python
image.draw_string(x, y, text[, color[, scale=1[, x_spacing=0[, y_spacing=0[, mono_space=True]]]]])
```

Draw text starting from position `(x, y)` on the image. Parameters can be passed separately as `x, y` or as a tuple `(x, y)`.

- **text**: The string to be drawn. Newline characters `\n`, `\r`, or `\r\n` are used to move the cursor to the next line.
- **color**: An RGB888 tuple representing the color, applicable for grayscale or RGB565 images, default is white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **scale**: Controls the scaling factor of the text, default is 1. Must be an integer.
- **x_spacing**: Adjusts the horizontal spacing between characters. Positive values increase spacing, negative values decrease it.
- **y_spacing**: Adjusts the vertical spacing between lines. Positive values increase spacing, negative values decrease it.
- **mono_space**: Defaults to `True`, making characters have a fixed width. When set to `False`, character spacing is dynamically adjusted based on character width.

This method returns the image object, allowing chaining other methods.

Compressed images and Bayer format images are not supported.

### 1.36 `draw_cross`

```python
image.draw_cross(x, y[, color[, size=5[, thickness=1]]])
```

Draw a cross mark on the image. Parameters can be passed separately as `x, y` or as a tuple `(x, y)`.

- **color**: An RGB888 tuple representing the color, applicable for grayscale or RGB565 images, default is white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **size**: Controls the size of the cross mark, default is 5.
- **thickness**: Controls the pixel width of the cross lines, default is 1.

This method returns the image object, allowing chaining other methods.

Compressed images and Bayer format images are not supported.

### 1.37 `draw_arrow`

```python
image.draw_arrow(x0, y0, x1, y1[, color[, thickness=1]])
```

Draw an arrow from `(x0, y0)` to `(x1, y1)` on the image. Parameters can be passed separately as `x0, y0, x1, y1` or as a tuple `(x0, y0, x1, y1)`.

- **color**: An RGB888 tuple representing the color, applicable for grayscale or RGB565 images, default is white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the arrow lines, default is 1.

This method returns the image object, allowing chaining other methods.

Compressed images and Bayer format images are not supported.

### 1.38 `draw_image`

```python
image.draw_image(image, x, y[, x_scale=1.0[, y_scale=1.0[, mask=None[, alpha=256]]]])
```

This function is used to draw an image at the specified position `(x, y)`, aligning the top-left corner of the image with that position. Parameters `x` and `y` can be passed separately or as a tuple `(x, y)`.

- `x_scale`: Controls the horizontal scaling factor of the image (float).
- `y_scale`: Controls the vertical scaling factor of the image (float).
- `mask`: A pixel-level mask image applied to the drawing operation. The mask should be a binary image (black and white pixels) and the same size as the target image.
- `alpha`: Sets the transparency of the source image when drawing, ranging from 0 to 256. 256 means fully opaque, smaller values indicate the blend level between the source and target images, and 0 means no modification to the target image.

This method does not support compressed images and Bayer format images.

### 1.39 `draw_keypoints`

```python
image.draw_keypoints(keypoints[, color[, size=10[, thickness=1[, fill=False]]]])
```

Draw keypoints on the image.

- `color`: Specifies the color, applicable for grayscale or RGB565 images. Default is white. For grayscale images, a grayscale value (0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- `size`: Controls the size of the keypoints.
- `thickness`: Controls the thickness of the lines (in pixels).
- `fill`: If `True`, fills the keypoints.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.40 `flood_fill`

```python
image.flood_fill(x, y[, seed_threshold=0.05[, floating_threshold=0.05[, color[, invert=False[, clear_background=False[, mask=None]]]]]])
```

Perform a flood fill operation starting from position `(x, y)`. `x` and `y` can be passed separately or as a tuple `(x, y)`.

- `seed_threshold`: Controls the difference between pixels in the fill region and the seed pixel.
- `floating_threshold`: Controls the difference between adjacent pixels in the fill region.
- `color`: Fill color, applicable for grayscale or RGB565 images. Default is white. A grayscale value or a byte-swapped RGB565 value can also be passed.
- `invert`: If `True`, inverts the fill logic, filling the area outside the target region.
- `clear_background`: If `True`, sets unfilled pixels to zero.
- `mask`: A pixel-level mask image to limit the fill area. The mask should be a binary image (black and white pixels) and the same size as the target image.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.41 `binary`

```python
image.binary(thresholds[, invert=False[, zero=False[, mask=None]]])
```

Convert all pixels in the image to a black and white binary image based on the specified threshold list `thresholds`.

- `thresholds`: A list of tuples in the format `[(lo, hi), ...]`. For grayscale images, each tuple defines a range of grayscale values (low and high); for RGB565 images, each tuple contains six values representing the ranges of L, A, and B channels in LAB space.
- `invert`: If `True`, inverts the threshold operation, converting pixels outside the threshold to white.
- `zero`: If `True`, sets pixels matching the threshold to zero while preserving other pixels.
- `mask`: A mask image applied to the binarization operation. The mask should be a binary image and the same size as the target image.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.42 `invert`

```python
image.invert()
```

Quickly invert pixel values in a binary image, converting 0 (black) to 1 (white) and 1 (white) to 0 (black).

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.43 `b_and`

```python
image.b_and(image[, mask=None])
```

Perform a bitwise AND operation on two images.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. For scalar values, it can be an RGB888 tuple or a base pixel value for grayscale images (e.g., 8-bit grayscale value).
- `mask`: A mask image to limit the operation. The mask should be a binary image and the same size as the target image.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.44 `b_nand`

```python
image.b_nand(image[, mask=None])
```

Perform a bitwise NAND operation on two images.

Other parameters are the same as `b_and`.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.45 `b_or`

```python
image.b_or(image[, mask=None])
```

Perform a bitwise OR operation on two images.

Other parameters are the same as `b_and`.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.46 `b_nor`

```python
image.b_nor(image[, mask=None])
```

Perform a bitwise NOR operation on two images.

Other parameters are the same as `b_and`.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.47 `b_xor`

```python
image.b_xor(image[, mask=None])
```

Perform a bitwise XOR operation on two images.

Other parameters are the same as `b_and`.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.48 `b_xnor`

```python
image.b_xnor(image[, mask=None])
```

Perform a bitwise XNOR operation on two images.

Other parameters are the same as `b_and`.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.49 `erode`

```python
image.erode(size[, threshold[, mask=None]])
```

Perform an erosion operation by removing pixels along the edges of regions.

- `size`: Defines the kernel size for the erosion operation as `((size*2)+1)x((size*2)+1)`.
- `threshold`: If not specified, performs a standard erosion operation; if specified, determines erosion based on the sum of neighboring pixels being less than the threshold.

Returns the image object, allowing chaining other methods.

### 1.50 `dilate`

```python
image.dilate(size[, threshold[, mask=None]])
```

Perform a dilation operation by adding pixels along the edges of regions.

Other parameters are the same as `erode`.

Returns the image object, allowing chaining other methods.

### 1.51 `open`

```python
image.open(size[, threshold[, mask=None]])
```

Perform an erosion followed by a dilation operation on the image. For details, refer to the `erode()` and `dilate()` methods.

Returns the image object, allowing chaining other methods.

### 1.52 `close`

```python
image.close(size[, threshold[, mask=None]])
```

Perform a dilation followed by an erosion operation on the image. For details, refer to the `erode()` and `dilate()` methods.

Returns the image object, allowing chaining other methods.

### 1.53 `top_hat`

```python
image.top_hat(size[, threshold[, mask=None]])
```

This function returns the difference between the original image and the image after performing `image.open()`.

- `size`: Defines the kernel size for the operation as `((size*2)+1)x((size*2)+1)`.
- `threshold`: Controls the operation intensity, defaulting to standard operation if not specified.
- `mask`: A pixel-level mask image. The mask should be a binary image (black and white pixels) and the same size as the target image. Only pixels in the mask that are white will be operated on.

This method does not support compressed images and Bayer format images.

### 1.54 `black_hat`

```python
image.black_hat(size[, threshold[, mask=None]])
```

This function returns the difference between the original image and the image after performing `image.close()`.

- `size`: Defines the kernel size for the operation as `((size*2)+1)x((size*2)+1)`.
- `threshold`: Controls the operation intensity, defaulting to standard operation if not specified.
- `mask`: A pixel-level mask image. The mask should be a binary image and the same size as the target image. Only pixels in the mask that are white will be operated on.

This method does not support compressed images and Bayer format images.

### 1.55 `negate`

```python
image.negate()
```

Quickly invert all pixel values in the image, performing a numerical inversion on each color channel (e.g., `255 - pixel`).

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.56 `replace`

```python
image.replace(image[, hmirror=False[, vflip=False[, mask=None]]])
```

This function replaces the specified image onto the current image.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale value).
- `hmirror`: Horizontally mirror the replacement image if `True`.
- `vflip`: Vertically flip the replacement image if `True`.
- `mask`: A pixel-level mask image. The mask should be a binary image and the same size as the target image. Only pixels in the mask that are white will be modified.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.57 `add`

```python
image.add(image[, mask=None])
```

Perform pixel-wise addition of two images.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale value).
- `mask`: A pixel-level mask image. The mask should be a binary image and the same size as the target image. Only pixels in the mask that are white will be modified.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.
This method does not support compressed images and Bayer format images.

### 1.58 `sub`

```python
image.sub(image[, reverse=False[, mask=None]])
```

Perform pixel-wise subtraction of two images.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale value).
- `reverse`: When set to `True`, reverses the order of the subtraction operation from `this_image - image` to `image - this_image`.
- `mask`: A pixel-level mask image. The mask should be a binary image and the same size as the target image. Only pixels in the mask that are white will be modified.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.59 `mul`

```python
image.mul(image[, invert=False[, mask=None]])
```

Perform pixel-wise multiplication of two images.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale value).
- `invert`: When set to `True`, the multiplication changes from `a * b` to `1 / ((1 / a) * (1 / b))`, which brightens the image instead of darkening it (similar to a "screen blend" effect).
- `mask`: A pixel-level mask image. The mask should be a binary image and the same size as the target image. Only pixels in the mask that are white will be modified.

Returns the image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.60 `div`

```python
image.div(image[, invert=False[, mask=None]])
```

Perform pixel-wise division of the current image by another image.

The `image` parameter can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale value).

Setting `invert=True` changes the order of the division from `a/b` to `b/a`.

`mask` is a pixel-level mask image. The mask should be a binary image and the same size as the current image. Only pixels in the mask that are white will be modified.

Returns the modified image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.61 `min`

```python
image.min(image[, mask=None])
```

Replace the pixels in the current image with the minimum pixel values from two images at the pixel level.

The `image` parameter can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale value).

`mask` is a pixel-level mask image. The mask should be a binary image and the same size as the current image. Only pixels in the mask that are white will be modified.

Returns the new image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

This method is not available on OpenMV4.

### 1.62 `max`

```python
image.max(image[, mask=None])
```

Replace the pixels in the current image with the maximum pixel values from two images at the pixel level.

The `image` parameter can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale value).

`mask` is a pixel-level mask image. The mask should be a binary image and the same size as the current image. Only pixels in the mask that are white will be modified.

Returns the new image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.63 `difference`

```python
image.difference(image[, mask=None]])
```

Compute the absolute difference between the pixel values of two images. Each color channel's pixel values are updated as follows: `ABS(this.pixel - image.pixel)`.

The `image` parameter can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale value).

`mask` is a pixel-level mask image. The mask should be a binary image and the same size as the current image. Only pixels in the mask that are white will be modified.

Returns the modified image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.64 `blend`

```python
image.blend(image[, alpha=128[, mask=None]])
```

Blend another image with the current image.

The `image` parameter can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale value).

`alpha` controls the blending ratio, with values ranging from 0 to 256. The closer the value is to 0, the higher the blending degree; the closer to 256, the lower the blending degree.

`mask` is a pixel-level mask image. The mask should be a binary image and the same size as the current image. Only pixels in the mask that are white will be modified.

Returns the blended image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.65 `histeq`

```python
image.histeq([adaptive=False[, clip_limit=-1[, mask=None]]])
```

Perform histogram equalization on the image to standardize its contrast and brightness.

If `adaptive=True`, adaptive histogram equalization is enabled, which usually produces better results but is slower than non-adaptive methods.

`clip_limit` controls the contrast of adaptive histogram equalization; smaller values (e.g., 10) generate contrast-limited images.

`mask` is a pixel-level mask image. The mask should be a binary image and the same size as the current image. Only pixels in the mask that are white will be modified.

Returns the processed image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.66 `mean`

```python
image.mean(size[, threshold=False[, offset=0[, invert=False[, mask=None]]]])
```

Apply a standard mean blur filter to the image using a box filter.

`size` specifies the filter size, with values of 1 (corresponding to a 3x3 kernel), 2 (corresponding to a 5x5 kernel), or larger.

If you want to perform adaptive thresholding on the filter output, set `threshold=True` to binarize the target pixel based on the brightness of neighboring pixels. A negative `offset` parameter will cause more pixels to be set to 1, while a positive value will only set the highest contrast pixels to 1. Set `invert=True` to invert the output binary image.

`mask` is a pixel-level mask image. The mask should be a binary image and the same size as the current image. Only pixels in the mask that are white will be modified.

Returns the blurred image object, allowing chaining other methods.

This method does not support compressed images and Bayer format images.

### 1.67 `median`

```python
image.median(size, percentile=0.5[, threshold=False[, offset=0[, invert=False[, mask=None]]]])
```

Apply a median filter to the image, which smooths the image while preserving edge details, though it is slower.

`size` specifies the filter size, with values of 1 (corresponding to a 3x3 kernel), 2 (corresponding to a 5x5 kernel), or larger.

The `percentile` parameter controls the percentile of the selected pixel. By default, the middle value (50th percentile) is chosen. Setting `percentile` to 0 performs minimum filtering, while setting it to 1 performs maximum filtering.

If you want to perform adaptive thresholding on the filter output, set `threshold=True`. The `offset` and `invert` parameters control the output of the binarization.

`mask` is a pixel-level mask image. The mask should be a binary image and the same size as the current image. Only pixels in the mask that are white will be modified.

Returns the filtered image object.

This method does not support compressed images and Bayer format images.

### 1.68 `mode`

```python
image.mode(size[, threshold=False, offset=0, invert=False, mask])
```

Apply a mode filter to the image, replacing each pixel with the mode of neighboring pixels. This method works well in grayscale images but may produce artifacts at the edges of RGB images due to its non-linear nature.

**Parameters:**

- **size**: Kernel size, with values of 1 (3x3 kernel) or 2 (5x5 kernel).
- **threshold**: If set to `True`, enables adaptive thresholding, adjusting pixel values based on the brightness of neighboring pixels (setting them to 1 or 0).
- **offset**: Negative values increase the number of pixels set to 1, while positive values limit it to only the highest contrast pixels.
- **invert**: Set to `True` to invert the output binary image.
- **mask**: A pixel-level mask image used for drawing operations. The mask image should contain only black or white pixels and be the same size as the image to be processed. Only pixels set in the mask will be modified.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This method does not support compressed images and Bayer format images.

### 1.69 `midpoint`

```python
image.midpoint(size[, bias=0.5, threshold=False, offset=0, invert=False, mask])
```

Apply a midpoint filter to the image, computing the midpoint value ((max-min)/2) for each pixel neighborhood.

**Parameters:**

- **size**: Kernel size, with values of 1 (3x3 kernel), 2 (5x5 kernel), or larger.
- **bias**: Controls the extent of minimum/maximum blending, with 0 performing minimum filtering, 1 performing maximum filtering, and values between 0 and 1 performing blended filtering.
- **threshold**: If set to `True`, enables adaptive thresholding, adjusting pixel values based on the brightness of neighboring pixels (setting them to 1 or 0).
- **offset**: Negative values increase the number of pixels set to 1, while positive values limit it to only the highest contrast pixels.
- **invert**: Set to `True` to invert the output binary image.
- **mask**: A pixel-level mask image used for drawing operations. The mask image should contain only black or white pixels and be the same size as the image to be processed. Only pixels set in the mask will be modified.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This method does not support compressed images and Bayer format images.

### 1.70 `morph`

```python
image.morph(size, kernel, mul=Auto, add=0)
```

Perform convolution on the image using a specified convolution kernel for general convolution.

**Parameters:**

- **size**: Kernel size, controlling the kernel size as ((size*2)+1)x((size*2)+1) pixels.
- **kernel**: The kernel used for convolution, which can be a tuple or a list of values within the range [-128:127].
- **mul**: A number to multiply the convolution result with. If not set, a default value is used to prevent convolution output scaling.
- **add**: A number to add to each pixel's convolution result.

`mul` can be used for global contrast adjustment, and `add` can be used for global brightness adjustment.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This method does not support compressed images and Bayer format images.

### 1.71 `gaussian`

```python
image.gaussian(size[, unsharp=False[, mul[, add=0[, threshold=False[, offset=0[, invert=False[, mask=None]]]]]]])
```

Smooth the image using a Gaussian kernel for convolution.

**Parameters:**

- **size**: Kernel size, with values of 1 (3x3 kernel), 2 (5x5 kernel), or larger.
- **unsharp**: If set to `True`, performs an unsharp mask operation to enhance edge sharpness.
- **mul**: A number to multiply the convolution result with. If not set, a default value is used to prevent convolution output scaling.
- **add**: A number to add to each pixel's convolution result.

`mul` can be used for global contrast adjustment, and `add` can be used for global brightness adjustment.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This method does not support compressed images and Bayer format images.

### 1.72 `laplacian`

```python
image.laplacian(size[, sharpen=False[, mul[, add=0[, threshold=False[, offset=0[, invert=False[, mask=None]]]]]]])
```

Perform edge detection on the image using a Laplacian kernel for convolution.
**Parameter Description:**

- **size**: The size of the kernel, with values of 1 (3x3 kernel), 2 (5x5 kernel), or higher.
- **sharpen**: If set to `True`, sharpens the image instead of just outputting the thresholded edges.
- **mul**: A number to multiply the convolution result with. If not set, a default value is used to prevent convolution output scaling.
- **add**: A number to add to each pixel's convolution result.

`mul` can be used for global contrast adjustment, and `add` can be used for global brightness adjustment.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This method does not support compressed images and Bayer format images.

### 1.73 `bilateral`

```python
image.bilateral(size[, color_sigma=0.1[, space_sigma=1[, threshold=False[, offset=0[, invert=False[, mask=None]]]]]])
```

Perform convolution on the image using a bilateral filter, which smooths the image while preserving edge details.

**Parameter Description:**

- **size**: The size of the kernel, with values of 1 (3x3 kernel), 2 (5x5 kernel), or higher.
- **color_sigma**: Controls the extent to which the bilateral filter matches colors. Increasing this value will result in more color blurring.
- **space_sigma**: Controls the extent of spatial blurring. Increasing this value will result in more spatial blurring.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This method does not support compressed images and Bayer format images.

### 1.74 `cartoon`

```python
image.cartoon(size[, seed_threshold=0.05[, floating_threshold=0.05[, mask=None]]])
```

Process the image using a Flood-Fill algorithm to fill all pixel regions, effectively removing texture from the image.

**Parameter Description:**

- **size**: Controls the size of the fill regions.
- **seed_threshold**: Controls the difference between pixels within the fill region and the original seed pixel.
- **floating_threshold**: Controls the difference between pixels within the fill region and neighboring pixels.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This method does not support compressed images and Bayer format images.

### 1.75 `remove_shadows`

```python
image.remove_shadows([image])
```

Remove shadows from the current image.

**Function Description**:

- If the current image does not have a "shadow-free" version, this method will attempt to remove shadows from the image, suitable for removing shadows in flat, uniform backgrounds.
- If the current image has a "shadow-free" version, this method will remove shadows based on the "true source" background image while retaining non-shadow pixels, making it easier to add new objects.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This function only supports RGB565 images.

### 1.76 `chrominvar`

```python
image.chrominvar()
```

Remove lighting effects from the image, retaining only color gradients. This method is fast but somewhat sensitive to shadows.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This function only supports RGB565 images.

### 1.77 `illuminvar`

```python
image.illuminvar()
```

Remove lighting effects from the image, retaining only color gradients. This method is slower but less sensitive to shadows.

**Returns**: Returns the image object, allowing further method chaining.

**Note**: This function only supports RGB565 images.

### 1.78 `linpolar`

```python
image.linpolar([reverse=False])
```

Reproject the image from Cartesian coordinates to linear polar coordinates.

**Parameter Description**:

- `reverse`: Boolean, default is `False`. If set to `True`, performs the reprojection in the reverse direction.

Linear polar reprojection converts image rotation to translation in the x direction.

**Note**: This function does not support compressed images.

### 1.79 `logpolar`

```python
image.logpolar([reverse=False])
```

Reproject the image from Cartesian coordinates to logarithmic polar coordinates.

**Parameter Description**:

- `reverse`: Boolean, default is `False`. If set to `True`, performs the reprojection in the reverse direction.

Logarithmic polar reprojection converts image rotation to translation in the x direction and scaling in the y direction.

**Note**: This function does not support compressed images.

### 1.80 `lens_corr`

```python
image.lens_corr([strength=1.8[, zoom=1.0]])
```

Perform lens distortion correction to remove fisheye effects caused by the lens.

**Parameter Description**:

- `strength`: A float value that determines the extent of fisheye effect removal. The default value is 1.8, and users can adjust it based on the image effect.
- `zoom`: A float value used for image scaling, with a default value of 1.0.

This method returns the image object, allowing users to continue calling other methods.

**Note**: This function does not support compressed images and Bayer format images.

### 1.81 `rotation_corr`

```python
img.rotation_corr([x_rotation=0.0[, y_rotation=0.0[, z_rotation=0.0[, x_translation=0.0[, y_translation=0.0[, zoom=1.0[, fov=60.0[, corners]]]]]]]])
```

Correct perspective issues in the image by performing a 3D rotation on the frame buffer.

**Parameter Description**:

- `x_rotation`: The angle of rotation around the x-axis (up-down rotation).
- `y_rotation`: The angle of rotation around the y-axis (left-right rotation).
- `z_rotation`: The angle of rotation around the z-axis (image orientation adjustment).
- `x_translation`: The amount of movement along the x-axis after rotation, in units of 3D space.
- `y_translation`: The amount of movement along the y-axis after rotation, in units of 3D space.
- `zoom`: The zoom factor, with a default value of 1.0.
- `fov`: The field of view for the 2D->3D projection. When this value is close to 0, the image is at an infinite distance in the viewport; when close to 180, the image is in the viewport. It is generally not recommended to change this value, but it can be adjusted to change the 2D->3D mapping effect.
- `corners`: A list of four `(x, y)` tuples representing the four corner points used to create a four-point homography, mapping the first corner to (0,0), the second to (image_width-1, 0), the third to (image_width-1, image_height-1), and the fourth to (0, image_height-1). This parameter allows users to achieve a bird's-eye view transformation using `rotation_corr`.

This method returns the image object, allowing users to continue calling other methods.

**Note**: This function does not support compressed images and Bayer format images.

### 1.82 `get_similarity`

```python
image.get_similarity(image)
```

This method returns a "similarity" object that describes the similarity between two images using the SSIM algorithm, based on comparing 8x8 pixel blocks.

**Parameter Description**:

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be an RGB888 tuple or a base pixel value (e.g., an 8-bit grayscale value or a byte-reversed RGB565 value for RGB images).

**Note**: This function does not support compressed images and Bayer format images.

### 1.83 `get_histogram`

```python
image.get_histogram([thresholds[, invert=False[, roi[, bins[, l_bins[, a_bins[, b_bins]]]]]]])
```

This method performs a normalized histogram operation on all color channels in the ROI and returns a histogram object. For detailed information on the histogram object, refer to the corresponding documentation. Users can also call this method using `image.get_hist` or `image.histogram`.

**Parameter Description**:

- `thresholds`: A list of tuples defining the color ranges to track. For grayscale images, each tuple should contain two values (minimum and maximum grayscale values); for RGB565 images, each tuple should contain six values (l_lo, l_hi, a_lo, a_hi, b_lo, b_hi).
- `invert`: Boolean, default is `False`. If set to `True`, inverts the threshold operation, matching pixels outside the known color range.
- `roi`: A rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the entire image is used.
- `bins`: The number of bins for grayscale images or the number of bins for each channel in RGB565 images.

**Note**: This function does not support compressed images and Bayer format images.

### 1.84 `get_statistics`

```python
image.get_statistics([thresholds[, invert=False[, roi[, bins[, l_bins[, a_bins[, b_bins]]]]]]])
```

This method calculates the mean, median, mode, standard deviation, minimum value, maximum value, lower quartile, and upper quartile for each color channel within the ROI and returns a data object.

**Parameter Description**:

- `thresholds`: A list of tuples defining the color ranges to track. For grayscale images, each tuple should contain two values (minimum and maximum grayscale values); for RGB565 images, each tuple should contain six values (l_lo, l_hi, a_lo, a_hi, b_lo, b_hi).
- `invert`: Boolean, default is `False`. If set to `True`, inverts the threshold operation, matching pixels outside the known color range.
- `roi`: A rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the entire image is used.
- `bins`: The number of bins for grayscale images or the number of bins for each channel in RGB565 images.

**Note**: This function does not support compressed images and Bayer format images.

### 1.85 `get_regression`

```python
image.get_regression(thresholds[, invert=False[, roi[, x_stride=2[, y_stride=1[, area_threshold=10[, pixels_threshold=10[, robust=False]]]]]]])
```

This method performs linear regression on all pixels in the image that meet the threshold criteria. The calculation uses the least squares method, which is fast but cannot handle outliers. If `robust` is set to `True`, the Theil-Sen estimator will be used to calculate the median slope between pixels.

**Parameter Description**:

- `thresholds`: A list of tuples defining the color ranges to track.
- `invert`: Boolean, default is `False`. If set to `True`, inverts the threshold operation.
- `roi`: A rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the entire image is used.
- `x_stride`: The number of x pixels to skip when calling the function.
- `y_stride`: The number of y pixels to skip when calling the function.
- `area_threshold`: If the area of the bounding box after regression is less than this value, returns `None`.
- `pixels_threshold`: If the number of pixels after regression is less than this value, returns `None`.

This method returns an `image.line` object. For detailed usage, refer to the following blog post: [Linear Regression Line Following](https://openmv.io/blogs/news/linear-regression-line-following).

**Note**: This function does not support compressed images and Bayer format images.

### 1.86 `find_blobs`

```python
image.find_blobs(thresholds[, invert=False[, roi[, x_stride=2[, y_stride=1[, area_threshold=10[, pixels_threshold=10[, merge=False[, margin=0[, threshold_cb=None[, merge_cb=None]]]]]]]]]])
```

This function finds all color blobs in the image and returns a list of blob objects. For more information on `image.blob` objects, refer to the relevant documentation.

The `thresholds` parameter must be a list of tuples in the form `[(lo, hi), (lo, hi), ...]`, defining the color ranges to track. For grayscale images, each tuple should contain two values: the minimum and maximum grayscale values. The function will only consider pixel regions that fall within these thresholds. For RGB565 images, each tuple should contain six values `(l_lo, l_hi, a_lo, a_hi, b_lo, b_hi)`, corresponding to the minimum and maximum values of the L, A, and B channels in the LAB color space. The function will automatically correct for swapped minimum and maximum values. If a tuple contains more than six values, the extra values will be ignored; if a tuple is missing values, the missing thresholds will be assumed to be the maximum range.

**Notes**:

To obtain the thresholds for the target object, simply select (click and drag) the object to be tracked in the IDE frame buffer, and the histogram will update in real time. Then, record the start and end positions of the color distribution in each histogram channel, which will serve as the low and high values for the `thresholds`. It is recommended to manually determine the thresholds to avoid minor differences in the upper and lower quartiles.

You can also determine color thresholds by going to the "Tools" -> "Machine Vision" -> "Threshold Editor" in the OpenMV IDE and adjusting the sliders in the GUI.

- The `invert` parameter inverts the threshold operation so that only pixels outside the known color range are matched.
- The `roi` parameter is a rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the ROI defaults to the entire image rectangle. Operations are limited to pixels within this region.
- `x_stride` is the number of x pixels to skip when searching for blobs. Once a blob is found, the fill algorithm will accurately process the region. If the blobs are known to be large, increasing `x_stride` can speed up the search.
- `y_stride` is the number of y pixels to skip when searching for blobs. Once a blob is found, the fill algorithm will accurately process the region.
If the blobs are known to be large, you can increase `y_stride` to speed up the search.
- `area_threshold` is used to filter out blobs with a bounding box area smaller than this value.
- `pixels_threshold` is used to filter out blobs with fewer pixels than this value.
- `merge`, if set to `True`, merges all unfiltered blobs whose bounding rectangles overlap. The `margin` can be used to increase or decrease the size of the blob's bounding rectangle during the merge test. For example, two overlapping blobs with a margin of 1 will be merged.

Merging blobs allows for the tracking of color codes. Each blob object has a `code` value, which is a bit vector. For example, if you input two color thresholds in `image.find_blobs`, the code for the first threshold is 1, and the code for the second threshold is 2 (the third code is 4, the fourth code is 8, and so on). When blobs are merged, all `code` values are combined using a logical OR operation to indicate the colors that generated them. This makes it possible to track two colors simultaneously, and if the same blob object is obtained for two colors, it may correspond to a specific color code.

When using strict color ranges, it may not be possible to track all pixels of the target object completely. In this case, consider merging blobs. If you want to merge blobs but do not want blobs from different thresholds to be merged, you can call `image.find_blobs` twice separately.

- `threshold_cb` can be set to a callback function that is called after each blob is thresholded, to filter out specific blobs from the list of blobs about to be merged. The callback function will receive one argument: the blob object to be filtered. If you want to keep the blob, the callback function should return `True`; otherwise, return `False`.
- `merge_cb` can be set to a callback function that is called between two blobs about to be merged, to approve or disapprove the merge. The callback function will receive two arguments, the two blob objects to be merged. If you want to merge the blobs, return `True`; otherwise, return `False`.

**Note:** This function does not support compressed images and Bayer format images.

### 1.87 `find_lines`

```python
image.find_lines([roi[, x_stride=2[, y_stride=1[, threshold=1000[, theta_margin=25[, rho_margin=25]]]]]])
```

This function uses the Hough Transform to find all lines in the image and returns a list of `image.line` objects.

- `roi` is a rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the ROI defaults to the entire image rectangle. Operations are limited to pixels within this region.
- `x_stride` is the number of x pixels to skip during the Hough Transform process. If the lines are known to be long, you can increase `x_stride`.
- `y_stride` is the number of y pixels to skip during the Hough Transform process. If the lines are known to be long, you can increase `y_stride`.
- `threshold` controls the lines detected by the Hough Transform. Only lines greater than or equal to this threshold are returned. The appropriate threshold depends on the image content. Note that the magnitude of a line is the sum of all Sobel filter pixel magnitudes that make up the line.
- `theta_margin` controls the merging of detected lines if their angles are within `theta_margin`.
- `rho_margin` similarly controls the merging of detected lines if their rho values are within `rho_margin`.

This method applies a Sobel filter to the image and performs the Hough Transform using its magnitude and gradient response. No preprocessing of the image is needed, although cleaning and filtering the image will yield more stable results.

**Note:** This function does not support compressed images and Bayer format images.

### 1.88 `find_line_segments`

```python
image.find_line_segments([roi[, merge_distance=0[, max_theta_difference=15]]])
```

This function uses the Hough Transform to find line segments in the image and returns a list of `image.line` objects.

- `roi` is a rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the ROI defaults to the entire image rectangle. Operations are limited to pixels within this region.
- `merge_distance` specifies the maximum pixel distance between two line segments to be merged into one.
- `max_theta_difference` is the maximum angle difference between two line segments to be merged.

This method uses the LSD library (also adopted by OpenCV) to find line segments in the image. Although slower, it is highly accurate and line segments do not jump.

**Note:** This function does not support compressed images and Bayer format images.

### 1.89 `find_circles`

```python
image.find_circles([roi[, x_stride=2[, y_stride=1[, threshold=2000[, x_margin=10[, y_margin=10[, r_margin=10]]]]]]])
```

This function uses the Hough Transform to find circles in the image and returns a list of `image.circle` objects.

- `roi` is a rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the ROI defaults to the entire image rectangle. Operations are limited to pixels within this region.
- `x_stride` is the number of x pixels to skip during the Hough Transform process. If the circles are known to be large, you can increase `x_stride`.
- `y_stride` is the number of y pixels to skip during the Hough Transform process. If the circles are known to be large, you can increase `y_stride`.
- `threshold` controls the size of the detected circles, returning only circles greater than or equal to this threshold. The appropriate threshold depends on the image content. Note that the magnitude of a circle is the sum of all Sobel filter pixel magnitudes that make up the circle.
- `x_margin` is the maximum pixel deviation allowed when merging x coordinates.
- `y_margin` is the maximum pixel deviation allowed when merging y coordinates.
- `r_margin` is the maximum pixel deviation allowed when merging radii.

This method applies a Sobel filter to the image and performs the Hough Transform using its magnitude and gradient response. No preprocessing of the image is needed, although cleaning and filtering the image will yield more stable results.

**Note:** This function does not support compressed images and Bayer format images.

### 1.90 `find_rects`

```python
image.find_rects([roi=Auto, threshold=10000])
```

This function uses the same quadrilateral detection algorithm as AprilTag to find rectangles in the image. The algorithm is best suited for rectangles that contrast sharply with the background. AprilTag's quadrilateral detection can handle rectangles of any scale, rotation, and shear, and returns a list of `image.rect` objects.

- `roi` is a rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the ROI defaults to the entire image rectangle. Operations are limited to pixels within this region.

In the returned list of rectangles, those with a boundary size (calculated by sliding a Sobel operator over all pixels on the rectangle's edge and summing its values) smaller than `threshold` will be filtered out. The appropriate `threshold` value depends on the specific application.

**Note:** This function does not support compressed images and Bayer format images.

### 1.91 `find_qrcodes`

```python
image.find_qrcodes([roi])
```

This function finds all QR codes within the specified ROI and returns a list of `image.qrcode` objects. For more information, refer to the documentation on `image.qrcode` objects.

To ensure the method runs successfully, the QR code on the image should be as flat as possible. You can achieve this by zooming in on the lens center using the `sensor.set_windowing` function, removing lens barrel distortion using the `image.lens_corr` function, or using a lens with a narrower field of view to obtain a flat QR code unaffected by lens distortion. Some machine vision lenses do not produce barrel distortion but are more expensive than the standard lenses provided by OpenMV, which are distortion-free lenses.

- `roi` is a rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the ROI defaults to the entire image rectangle. Operations are limited to pixels within this region.

**Note:** This function does not support compressed images and Bayer format images.

### 1.92 `find_apriltags`

```python
image.find_apriltags([roi[, families=image.TAG36H11[, fx[, fy[, cx[, cy]]]]]])
```

This function finds all AprilTags within the specified ROI and returns a list of `image.apriltag` objects. For more information, refer to the documentation on `image.apriltag` objects.

Compared to QR codes, AprilTags can be effectively detected at greater distances, under poorer lighting conditions, and in more distorted image environments. AprilTags can handle various image distortion issues, whereas QR codes cannot. Therefore, AprilTags only encode a numeric ID as their payload.

Additionally, AprilTags can be used for localization. Each `image.apriltag` object will return its 3D position and rotation angle. The position information is determined by `fx`, `fy`, `cx`, and `cy`, which represent the focal lengths and center points in the X and Y directions of the image, respectively.

> You can create AprilTags using the built-in tag generator tool in the OpenMV IDE. This tool can generate printable AprilTags in 8.5"x11" format.

- `roi` is a rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the ROI defaults to the entire image rectangle. Operations are limited to pixels within this region.

- `families` is a bitmask of the tag families to decode, represented in logical OR form:
  - `image.TAG16H5`
  - `image.TAG25H7`
  - `image.TAG25H9`
  - `image.TAG36H10`
  - `image.TAG36H11`
  - `image.ARTOOLKIT`

The default setting is the most commonly used `image.TAG36H11` tag family. Note that enabling each tag family slightly reduces the speed of `find_apriltags`.

- `fx` is the camera focal length in the X direction in pixels. The standard OpenMV Cam value is \((2.8 / 3.984) \times 656\), calculated by dividing the focal length in millimeters by the length of the sensor in the X direction and then multiplying by the number of pixels in the X direction (for the OV7725 sensor).

- `fy` is the camera focal length in the Y direction in pixels. The standard OpenMV Cam value is \((2.8 / 2.952) \times 488\), calculated by dividing the focal length in millimeters by the length of the sensor in the Y direction and then multiplying by the number of pixels in the Y direction (for the OV7725 sensor).

- `cx` is the center of the image, i.e., `image.width()/2`, not `roi.w()/2`.

- `cy` is the center of the image, i.e., `image.height()/2`, not `roi.h()/2`.

**Note:** This function does not support compressed images and Bayer format images.

### 1.93 `find_datamatrices`

```python
image.find_datamatrices([roi[, effort=200]])
```

This function finds all Data Matrix codes within the specified ROI and returns a list of `image.datamatrix` objects. For more information, refer to the documentation on `image.datamatrix` objects.

To ensure the method runs successfully, the Data Matrix on the image should be as flat as possible. You can achieve this by zooming in on the lens center using the `sensor.set_windowing` function, removing lens barrel distortion using the `image.lens_corr` function, or using a lens with a narrower field of view to obtain a flat Data Matrix unaffected by lens distortion. Some machine vision lenses do not produce barrel distortion but are more expensive than the standard lenses provided by OpenMV, which are distortion-free lenses.

- `roi` is a rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the ROI defaults to the entire image rectangle. Operations are limited to pixels within this region.

- `effort` controls the computation time required to find a Data Matrix match. The default value is 200, suitable for all use cases. However, you can increase the frame rate at the cost of detection rate or improve the detection rate at the cost of frame rate. Note that when `effort` is set below approximately 160, no detection will occur; conversely, you can set it to any higher value, but if set above 240, the detection rate will not improve further.

**Note:** This function does not support compressed images and Bayer format images.

### 1.94 `find_barcodes`

```python
image.find_barcodes([roi])
```

This function finds all one-dimensional barcodes within the specified ROI and returns a list of `image.barcode` objects. For more information, refer to the documentation on `image.barcode` objects.

For best results, it is recommended to use a window that is 640 pixels long and 40/80/160 pixels wide. The less vertical the window, the faster it runs. Since barcodes are linear one-dimensional images, they need high resolution in one direction and can have lower resolution in the other direction. Note that this function will perform both horizontal and vertical scans, so you can use a window that is 40/80/160 pixels wide and 480 pixels long. Be sure to adjust the lens so that the barcode is in the clearest focus area. Blurry barcodes cannot be decoded.

This function supports the following one-dimensional barcodes:

- `image.EAN2`
- `image.EAN5`
- `image.EAN8`
- `image.UPCE`
- `image.ISBN10`
- `image.UPCA`
- `image.EAN13`
- `image.ISBN13`
- `image.I25`
- `image.DATABAR (RSS-14)`
- `image.DATABAR_EXP (RSS-Expanded)`
- `image.CODABAR`
- `image.CODE39`
- `image.PDF417`
- `image.CODE93`
- `image.CODE128`

- `roi` is a rectangular tuple `(x, y, w, h)` representing the region of interest. If not specified, the ROI defaults to the entire image rectangle. Operations are limited to pixels within this region.
**Note:** Not supported for compressed images and Bayer images.

### 1.95 `find_displacement`

```python
image.find_displacement(template[, roi[, template_roi[, logpolar=False]]])
```

This function finds the transformation offset of the image based on a template. It can be used for optical flow analysis. The result is an `image.displacement` object containing the displacement calculation results based on phase correlation.

- `roi` is the rectangular region `(x, y, w, h)` to be processed. If not specified, the default is the entire image.

- `template_roi` is the template region `(x, y, w, h)` to be processed. If not specified, the default is the entire image.

`roi` and `template_roi` must have the same width and height, but the `x` and `y` coordinates can be located anywhere in the image. You can slide a smaller ROI over a larger image to get an optical flow gradient image.

`image.find_displacement` is typically used to calculate X/Y translation between two images. However, if `logpolar=True` is set, changes in rotation and scale will also be found. The same `image.displacement` object can provide both results.

**Note:** Not supported for compressed images and Bayer images.

**Annotation:** Please use this method on images with consistent width and height (e.g., `sensor.B64X64`).

### 1.96 `find_number`

```python
image.find_number(roi)
```

This function uses the LENET-6 convolutional neural network (CNN) trained on the MNIST dataset to detect digits in any 28x28 ROI in the image. It returns a tuple containing the detected digit (0-9) and the corresponding confidence (0-1).

- `roi` is the rectangular region of interest `(x, y, w, h)`. If not specified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note:** This method only supports grayscale images and is experimental. It may be removed in future versions if running any CNNs trained on Caffe on PC. The latest firmware version (3.0.0) has removed this function.

### 1.97 `classify_object`

```python
image.classify_object(roi)
```

This function uses the CIFAR-10 convolutional neural network (CNN) to classify objects in the region of interest (ROI) in the image, capable of identifying categories such as airplanes, cars, birds, cats, deer, dogs, frogs, horses, ships, and trucks. The method internally scales the input image to 32x32 pixels for CNN processing.

- `roi` is the rectangular region of interest `(x, y, w, h)`. If not specified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note:** This method only supports RGB565 format images.

**Annotation:** This method is experimental and may be removed in the future if running CNNs trained on Caffe on PC.

### 1.98 `find_template`

```python
image.find_template(template, threshold[, roi[, step=2[, search=image.SEARCH_EX]]])
```

This function finds the first match of the template in the image using the Normalized Cross Correlation (NCC) algorithm and returns the bounding box tuple `(x, y, w, h)` of the match; if no match is found, it returns `None`.

- `template` is a small image object that needs to match the target image object. Note that both images should be grayscale images.

- `threshold` is a float (range 0.0 to 1.0). A smaller value increases the detection rate but may increase the false positive rate; conversely, a higher value reduces the detection rate while reducing the false positive rate.

- `roi` is the rectangular region of interest `(x, y, w, h)`. If not specified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

- `step` specifies the number of pixels to skip when searching for the template, which can significantly speed up the algorithm. This parameter is applicable to the `SEARCH_EX` mode algorithm.

- `search` can be `image.SEARCH_DS` or `image.SEARCH_EX`. `image.SEARCH_DS` is faster but may fail to find the template if it is near the image edge. `image.SEARCH_EX` performs a more thorough search but is slower.

**Note:** This method only supports grayscale images.

### 1.99 `find_features`

```python
image.find_features(cascade[, threshold=0.5[, scale=1.5[, roi]]])
```

This method searches the image for all regions matching the Haar Cascade model and returns a list of bounding box tuples `(x, y, w, h)` of these features. If no features are found, it returns an empty list.

- `cascade` is a Haar Cascade object. For more details, refer to `image.HaarCascade()`.

- `threshold` is a float (range 0.0 to 1.0). A smaller value increases the detection rate but may increase the false positive rate; conversely, a higher value reduces the detection rate while reducing the false positive rate.

- `scale` is a float greater than 1.0. A higher scale factor runs faster but with poorer image matching performance. The ideal value is between 1.35 and 1.5.

- `roi` is the rectangular region of interest `(x, y, w, h)`. If not specified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note:** This method only supports grayscale images.

### 1.100 `find_eye`

```python
image.find_eye(roi)
```

This function finds the pupil within the specified region of interest `(x, y, w, h)` and returns the position tuple `(x, y)` of the pupil in the image. If no pupil is found, it returns `(0, 0)`.

Before using this function, first search for a face using `image.find_features()` with the Haar cascade `frontalface`, then search for eyes on the face using `image.find_features()` with the Haar cascade `find_eye`. Finally, call this method on each eye ROI returned by `image.find_features()` to get the pupil coordinates.

- `roi` is the rectangular region of interest `(x, y, w, h)`. If not specified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note:** This method only supports grayscale images.

### 1.101 `find_lbp`

```python
image.find_lbp(roi)
```

This function extracts Local Binary Pattern (LBP) keypoints from the specified ROI tuple `(x, y, w, h)`. You can use the `image.match_descriptor` function to compare two sets of keypoints to get a matching distance.

- `roi` is the rectangular region of interest `(x, y, w, h)`. If not specified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note:** This method only supports grayscale images.

### 1.102 `find_keypoints`

```python
image.find_keypoints([roi[, threshold=20[, normalized=False[, scale_factor=1.5[, max_keypoints=100[, corner_detector=image.CORNER_AGAST]]]]]])
```

This function extracts ORB keypoints from the specified ROI tuple `(x, y, w, h)`. You can use the `image.match_descriptor` function to compare two sets of keypoints to get a matching region. If no keypoints are found, it returns `None`.

- `roi` is the rectangular region of interest `(x, y, w, h)`. If not specified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

- `threshold` controls the number of keypoints extracted (range 0-255). For the default AGAST corner detector, this value should be around 20; for the FAST corner detector, it should be around 60 to 80. The lower the threshold, the more corners are extracted.

- `normalized` is a boolean. If `True`, keypoint extraction is turned off at multiple resolutions. If you do not care about handling scale issues and want the algorithm to run faster, set it to `True`.

- `scale_factor` is a float greater than 1.0. A higher scale factor runs faster but with poorer image matching performance. The ideal value is between 1.35 and 1.5.

- `max_keypoints` is the maximum number of keypoints the keypoint object can hold. If the keypoint object is too large causing memory issues, reduce this value.

- `corner_detector` is the corner detector algorithm used to extract keypoints. Optional values are `image.CORNER_FAST` or `image.CORNER_AGAST`. The FAST corner detector is faster but less accurate.

**Note:** This method only supports grayscale images.

### 1.103 `find_edges`

```python
image.find_edges(edge_type[, threshold])
```

This function converts the image to a black-and-white image, retaining only the edges as white pixels.

- `edge_type` options include:
  - `image.EDGE_SIMPLE` - Simple threshold high-pass filter algorithm
  - `image.EDGE_CANNY` - Canny edge detection algorithm

- `threshold` is a binary tuple containing low and high thresholds. You can adjust this value to control the quality of the edges, with the default setting being `(100, 200)`.

**Note:** This method only supports grayscale images.

### 1.104 `find_hog`

```python
image.find_hog([roi[, size=8]])
```

This function replaces the pixels in the ROI with the Histogram of Oriented Gradients (HOG) algorithm.

- `roi` is the rectangular region of interest `(x, y, w, h)`. If not specified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note:** This method only supports grayscale images.

### 1.105 `draw_ellipse`

```python
image.draw_ellipse(cx, cy, rx, ry, color, thickness=1)
```

The `draw_ellipse` function is used to draw an ellipse on the image.

- `cx, cy`: Coordinates of the ellipse center.
- `rx, ry`: Radii of the ellipse along the x-axis and y-axis.

- `color`: The color of the ellipse.
- `thickness`: The thickness of the ellipse border (default is 1).

This function returns the image object so you can call other methods using the `.` notation.

**Note:** This method does not support compressed images and Bayer images.

**OpenMV Native API** is ported from `openmv`, maintaining consistent functionality. Users can refer to the native documentation for more API details.

## 2. image Module Functions

### 2.1 `rgb_to_lab`

Convert RGB888 to LAB color space.

```python
image.rgb_to_lab(rgb_tuple)
```

### 2.2 `lab_to_rgb`

Convert LAB color space to RGB888.

```python
image.lab_to_rgb(lab_tuple)
```

### 2.3 `rgb_to_grayscale`

Convert RGB888 to grayscale.

```python
image.rgb_to_grayscale(rgb_tuple)
```

### 2.4 `grayscale_to_rgb`

Convert grayscale to RGB888.

```python
image.grayscale_to_rgb(g_value)
```

### 2.5 `load_descriptor`

Load a descriptor object from a file.

```python
image.load_descriptor(path)
```

### 2.6 `save_descriptor`

Save a descriptor object to a file.

```python
image.save_descriptor(path, descriptor)
```

### 2.7 `match_descriptor`

Compare two descriptor objects and return the matching result.

```python
image.match_descriptor(descriptor0, descriptor1, threshold=70, filter_outliers=False)
```

## 5 Class `HaarCascade`

The `HaarCascade` feature descriptor is used for the `image.find_features()` method and does not provide methods for direct invocation.

### 5.1 Constructor

```python
class image.HaarCascade(path[, stages=Auto])
```

This constructor loads a Haar Cascade from a binary file (formatted for OpenMV Cam). If you pass the string "frontalface" instead of a path, the constructor will load the built-in frontal face Haar Cascade. Similarly, you can load the corresponding Haar Cascade by passing "eye". The method returns the loaded Haar Cascade object for subsequent use with `image.find_features()`.

The default value for `stages` is the number of stages in the Haar Cascade, but you can specify a lower value to speed up the feature detector, though this may increase the false positive rate.

> You can create custom Haar Cascades for OpenMV Cam. First, search for "Haar Cascade" on Google to see if someone has already made an OpenCV Haar Cascade for the object you want to detect. If not, you might need to create one yourself (a labor-intensive task). Refer to relevant materials for creating custom Haar Cascades and scripts to convert OpenCV Haar Cascades to a format readable by OpenMV Cam.

**Q: What is a Haar Cascade?**

**A:** A Haar Cascade is a series of contrast checks used to determine if an object exists in an image. These checks are divided into multiple stages, with each stage's execution depending on the results of the previous stage. Although the checks themselves are not complex, such as checking if the center of the image is darker than the edges, they are efficient feature detection tools. Initial stages perform broad checks, while subsequent stages focus on smaller areas.

**Q: How are Haar Cascades created?**

**A:** Haar Cascades are trained using images marked with positive and negative labels. For example, hundreds of images containing cats (marked as positive) and hundreds of images without cats (marked as negative) are used to train the algorithm. The final model generated is the Haar Cascade used to detect cats.

## 6 Class `Similarity`

The similarity object is returned by the `image.get_similarity` function.

### 6.1 Constructor

```python
class image.similarity
```

Create this object by calling the `image.get_similarity()` function.

### 6.2 `mean`

```python
similarity.mean()
```

This function returns the mean of the structural similarity differences in 8x8 pixel blocks, ranging from [-1, +1], where -1 indicates completely different and +1 indicates completely identical. You can also access this value using index [0].

### 6.3 `stdev`

```python
similarity.stdev()
```

This function returns the standard deviation of the structural similarity differences in 8x8 pixel blocks. You can also access this value using index [1].

### 6.4 `min`

```python
similarity.min()
```

This function returns the minimum value of the structural similarity differences in 8x8 pixel blocks, ranging from [-1, +1], where -1 indicates completely different and +1 indicates completely identical. You can also access this value using index [2].

> By looking at this value, you can quickly determine if any 8x8 pixel block between two images has a significant difference, i.e., a value much lower than +1.

### 6.5 `max`

```python
similarity.max()
```

This function returns the maximum value of the structural similarity differences in 8x8 pixel blocks, ranging from [-1, +1], where -1 indicates completely different and +1 indicates completely identical. You can also access this value using index [3].

> By looking at this value, you can quickly determine if any 8x8 pixel block between two images is completely identical, i.e., a value much higher than -1.

## 7 Class `Histogram`

The histogram object is returned by the `image.get_histogram` method. A grayscale histogram contains multiple normalized binary channels, totaling 1. An RGB565 format histogram has three binary channels, also normalized to ensure their sum is 1.

### 7.1 Constructor

```python
class image.histogram
```

Create this object by calling the `image.get_histogram()` function.

### 7.2 `bins`

```python
histogram.bins()
```

Returns a list of floating-point numbers for the grayscale histogram. You can also access this value using index [0].

### 7.3 `l_bins`

```python
histogram.l_bins()
```

Returns a list of floating-point numbers for the L channel of the LAB histogram in RGB565 format. You can access this value using index [0].

### 7.4 `a_bins`

```python
histogram.a_bins()
```

Returns a list of floating-point numbers for the A channel of the LAB histogram in RGB565 format. You can access this value using index [1].

### 7.5 `b_bins`

```python
histogram.b_bins()
```

Returns a list of floating-point numbers for the B channel of the LAB histogram in RGB565 format. You can access this value using index [2].

### 7.6 `get_percentile`

```python
histogram.get_percentile(percentile)
```

Calculates the cumulative distribution function (CDF) of the histogram channel and returns the histogram value corresponding to the specified percentile (0.0 - 1.0).

For example, if you pass in 0.1, this method will indicate which binary value causes the accumulator to exceed 0.1 during accumulation. This method is particularly effective for determining the minimum (0.1) and maximum (0.9) values of color distribution, assuming no abnormal utility interferes with adaptive color tracking results.

### 7.7 `get_threshold`

```python
histogram.get_threshold()
```

Calculates the optimal threshold using the Otsu method, splitting each channel of the histogram into two. This method returns an `image.threshold` object, especially useful for determining the best threshold for `image.binary()`.

### 7.8 `get_statistics`

```python
histogram.get_statistics()
```

Calculates the mean, median, mode, standard deviation, minimum value, maximum value, lower quartile, and upper quartile for each color channel in the histogram and returns a `statistics` object. You can also use `histogram.statistics()` and `histogram.get_stats()` as aliases for this method.

## 8 Class `Percentile`

The percentile object is returned by the `histogram.get_percentile` method. A grayscale percentile contains one channel and does not use the `l_*`, `a_*`, or `b_*` methods. An RGB565 format percentile contains three channels and requires the use of `l_*`, `a_*`, and `b_*` methods.

### 8.1 Constructor

```python
class image.percentile
```

Create this object by calling the `histogram.get_percentile()` function.

### 8.2 `value`

```python
percentile.value()
```

Returns the grayscale percentile value (range 0-255).

You can also access this value using index [0].

### 8.3 `l_value`

```python
percentile.l_value()
```

Returns the percentile value for the L channel of the LAB histogram in RGB565 format (range 0-100).

You can also access this value using index [0].

### 8.4 `a_value`

```python
percentile.a_value()
```

Returns the percentile value for the A channel of the LAB histogram in RGB565 format (range -128 to 127).

You can also access this value using index [1].

### 8.5 `b_value`

```python
percentile.b_value()
```

Returns the percentile value for the B channel of the LAB histogram in RGB565 format (range -128 to 127).

You can also access this value using index [2].

## 9 Class `Threshold`

The threshold object is returned by the `histogram.get_threshold` method.

A grayscale image contains one channel and does not include the `l_*`, `a_*`, and `b_*` methods.

An RGB565 format threshold contains three channels and requires the use of `l_*`, `a_*`, and `b_*` methods.

### 9.1 Constructor

```python
class image.threshold
```

Create this object by calling the `histogram.get_threshold()` function.

### 9.2 `value`

```python
threshold.value()
```

Returns the threshold value for the grayscale image (range 0-255).

You can also access this value using index [0].

### 9.3 `l_value`

```python
threshold.l_value()
```

Returns the threshold value for the L channel of the LAB histogram in RGB565 format (range 0-100).

You can also access this value using index [0].

### 9.4 `a_value`

```python
threshold.a_value()
```

Returns the threshold value for the A channel of the LAB histogram in RGB565 format (range -128 to 127).

You can also access this value using index [1].

### 9.5 `b_value`

```python
threshold.b_value()
```

Returns the threshold value for the B channel of the LAB histogram in RGB565 format (range -128 to 127).

You can also access this value using index [2].

## 10 Class `Statistics`

The statistics object is returned by the `histogram.get_statistics` or `image.get_statistics` methods.

Grayscale statistics contain one channel and do not use the `l_*`, `a_*`, or `b_*` methods.

RGB565 format statistics contain three channels and require the use of `l_*`, `a_*`, and `b_*` methods.

### 10.1 Constructor

```python
class image.statistics
```

Create this object by calling the `histogram.get_statistics()` or `image.get_statistics()` functions.

#### 10.2 `mean`

```python
statistics.mean()
```

Returns the mean value for the grayscale image (range 0-255, type int).

You can also access this value using index [0].

### 10.3 `median`

```python
statistics.median()
```

Returns the median value for the grayscale image (range 0-255, type int).

You can also access this value using index [1].

### 10.4 `mode`

```python
statistics.mode()
```

Returns the mode value for the grayscale image (range 0-255, type int).

You can also access this value using index [2].

### 10.5 `stdev`

```python
statistics.stdev()
```

Returns the standard deviation for the grayscale image (range 0-255, type int).

You can also access this value using index [3].

### 10.6 `min`

```python
statistics.min()
```

Returns the minimum value for the grayscale image (range 0-255, type int).

You can also access this value using index [4].

### 10.7 `max`

```python
statistics.max()
```

Returns the maximum value for the grayscale image (range 0-255, type int).

You can also access this value using index [5].

### 10.8 `lq`

```python
statistics.lq()
```

Returns the lower quartile for the grayscale image (range 0-255, type int).

You can also access this value using index [6].

### 10.9 `uq`

```python
statistics.uq()
```

Returns the upper quartile for the grayscale image (range 0-255, type int).

You can also access this value using index [7].

### 10.10 `l_mean`

```python
statistics.l_mean()
```

Returns the mean value for the L channel of the LAB histogram in RGB565 format (range 0-255, type int).

You can also access this value using index [0].

### 10.11 `l_median`

```python
statistics.l_median()
```

Returns the median value for the L channel of the LAB histogram in RGB565 format (range 0-255, type int).

You can also access this value using index [1].

### 10.12 `l_mode`

```python
statistics.l_mode()
```

Returns the mode value for the L channel of the LAB histogram in RGB565 format (range 0-255, type int).

You can also access this value using index [2].

### 10.13 `l_stdev`

```python
statistics.l_stdev()
```

Returns the standard deviation for the L channel of the LAB histogram in RGB565 format (range 0-255, type int).

You can also access this value using index [3].

### 10.14 `l_min`

```python
statistics.l_min()
```

Returns the minimum value for the L channel of the LAB histogram in RGB565 format (range 0-255, type int).

You can also access this value using index [4].

### 10.15 `l_max`

```python
statistics.l_max()
```

Returns the maximum value for the L channel of the LAB histogram in RGB565 format (range 0-255, type int).

You can also access this value using index [5].

### 10.16 `l_lq`

```python
statistics.l_lq()
```

Returns the lower quartile for the L channel of the LAB histogram in RGB565 format (range 0-255, type int). You can also access this value using index [6].

### 10.17 `l_uq`

```python
statistics.l_uq()
```

Returns the upper quartile for the L channel of the LAB histogram in RGB565 format (range 0-255, type int). You can also access this value using index [7].

### 10.18 `a_mean`

```python
statistics.a_mean()
```

Returns the mean value for the A channel of the LAB histogram in RGB565 format (range 0-255, type int). You can also access this value using index [8].

### 10.19 `a_median`

```python
statistics.a_median()
```

Returns the median value for the A channel of the LAB histogram in RGB565 format (range 0-255, type int). You can also access this value using index [9].

### 10.20 `a_mode`

```python
statistics.a_mode()
```

Returns the mode value for the A channel of the LAB histogram in RGB565 format (range 0-255, type int). You can also access this value using index [10].

### 10.21 `a_stdev`

```python
statistics.a_stdev()
```

Returns the standard deviation for the A channel of the LAB histogram in RGB565 format (range 0-255, type int).
You can also access this value using index [11].

### 10.22 `a_min`

```python
statistics.a_min()
```

Returns the minimum value for the A channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [12].

### 10.23 `a_max`

```python
statistics.a_max()
```

Returns the maximum value for the A channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [13].

### 10.24 `a_lq`

```python
statistics.a_lq()
```

Returns the lower quartile for the A channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [14].

### 10.25 `a_uq`

```python
statistics.a_uq()
```

Returns the upper quartile for the A channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [15].

### 10.26 `b_mean`

```python
statistics.b_mean()
```

Returns the mean value for the B channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [16].

### 10.27 `b_median`

```python
statistics.b_median()
```

Returns the median value for the B channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [17].

### 10.28 `b_mode`

```python
statistics.b_mode()
```

Returns the mode value for the B channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [18].

### 10.29 `b_stdev`

```python
statistics.b_stdev()
```

Returns the standard deviation for the B channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [19].

### 10.30 `b_min`

```python
statistics.b_min()
```

Returns the minimum value for the B channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [20].

### 10.31 `b_max`

```python
statistics.b_max()
```

Returns the maximum value for the B channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [21].

### 10.32 `b_lq`

```python
statistics.b_lq()
```

Returns the lower quartile for the B channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [22].

### 10.33 `b_uq`

```python
statistics.b_uq()
```

Returns the upper quartile for the B channel of the LAB histogram in RGB565 format, ranging from 0 to 255 (type int). You can also access this value using index [23].

## 11 Class `Blob`

The blob object is returned by the `image.find_blobs` method.

### 11.1 Constructor

```python
class image.blob
```

Create this object by calling the `image.find_blobs()` function.

### 11.2 `rect`

```python
blob.rect()
```

Returns a rectangle tuple (x, y, w, h) for the blob's bounding box, useful for drawing on the image and other image processing methods like `image.draw_rectangle`.

### 11.3 `x`

```python
blob.x()
```

Returns the x-coordinate of the blob's bounding box (type int). You can also access this value using index [0].

### 11.4 `y`

```python
blob.y()
```

Returns the y-coordinate of the blob's bounding box (type int). You can also access this value using index [1].

### 11.5 `w`

```python
blob.w()
```

Returns the width of the blob's bounding box (type int). You can also access this value using index [2].

### 11.6 `h`

```python
blob.h()
```

Returns the height of the blob's bounding box (type int). You can also access this value using index [3].

### 11.6 `pixels`

```python
blob.pixels()
```

Returns the number of pixels in the blob (type int). You can also access this value using index [4].

### 11.7 `cx`

```python
blob.cx()
```

Returns the x-coordinate of the blob's center (type int). You can also access this value using index [5].

### 11.8 `cy`

```python
blob.cy()
```

Returns the y-coordinate of the blob's center (type int). You can also access this value using index [6].

### 11.9 `rotation`

```python
blob.rotation()
```

Returns the rotation angle of the blob in radians. For pencil-like blobs, this value ranges from 0 to 180. If the blob is circular, this value is invalid; for completely asymmetric blobs, the rotation angle ranges from 0 to 360 degrees. You can also access this value using index [7].

### 11.10 `code`

```python
blob.code()
```

Returns a 16-bit binary number where each bit corresponds to a color threshold, indicating the properties of the blob. For example, if you search for three color thresholds using `image.find_blobs`, the blob can be set to the 0/1/2 bit. Note: Unless `merge=True` is set when calling `image.find_blobs`, each blob can only set one bit. Therefore, multiple blobs with different color thresholds can be merged. You can also use this method to track color codes by combining multiple thresholds. You can also access this value using index [8].

### 11.11 `count`

```python
blob.count()
```

Returns the number of blobs merged into this blob. This number will be greater than 1 only if `merge=True` is set when calling `image.find_blobs`. You can also access this value using index [9].

### 11.12 `area`

```python
blob.area()
```

Returns the area of the bounding box around the blob (calculated as w * h).

### 11.13 `density`

```python
blob.density()
```

Returns the density ratio of the blob, representing the number of pixels within the blob's bounding box. Generally, a lower density ratio indicates poor object locking.

## 12 Class `Line`

The line object is returned by the `image.find_lines`, `image.find_line_segments`, or `image.get_regression` methods.

### 12.1 Constructor

```python
class image.line
```

Create this object by calling the `image.find_lines()`, `image.find_line_segments()`, or `image.get_regression()` functions.

### 12.2 `line`

```python
line.line()
```

Returns a line tuple (x1, y1, x2, y2) for drawing on the image and other image processing methods like `image.draw_line`.

### 12.3 `x1`

```python
line.x1()
```

Returns the x-coordinate of the first vertex (p1) of the line. You can also access this value using index [0].

### 12.4 `y1`

```python
line.y1()
```

Returns the y-coordinate of the first vertex (p1) of the line. You can also access this value using index [1].

### 12.5 `x2`

```python
line.x2()
```

Returns the x-coordinate of the second vertex (p2) of the line. You can also access this value using index [2].

### 12.6 `y2`

```python
line.y2()
```

Returns the y-coordinate of the second vertex (p2) of the line. You can also access this value using index [3].

### 12.7 `length`

```python
line.length()
```

Returns the length of the line, calculated as \(\sqrt{((x2-x1)^2) + ((y2-y1)^2)}\). You can also access this value using index [4].

### 12.8 `magnitude`

```python
line.magnitude()
```

Returns the length of the line after the Hough transform. You can also access this value using index [5].

### 12.9 `theta`

```python
line.theta()
```

Returns the angle of the line after the Hough transform (range: 0-179 degrees). You can also access this value using index [7].

### 12.10 `rho`

```python
line.rho()
```

Returns the rho value of the line after the Hough transform. You can also access this value using index [8].

## 13 Class `Circle`

The circle object is returned by the `image.find_circles` method.

### 13.1 Constructor

```python
class image.circle
```

Create this object by calling the `image.find_circles()` function.

### 13.2 `x`

```python
circle.x()
```

Returns the x-coordinate of the circle's center. You can also access this value using index [0].

### 13.3 `y`

```python
circle.y()
```

Returns the y-coordinate of the circle's center. You can also access this value using index [1].

### 13.4 `r`

```python
circle.r()
```

Returns the radius of the circle. You can also access this value using index [2].

### 13.5 `magnitude`

```python
circle.magnitude()
```

Returns the magnitude of the circle. You can also access this value using index [3].

## 14 Class `Rect`

The rectangle object is returned by the `image.find_rects` function.

### 14.1 Constructor

```python
class image.rect
```

Create this object by using the `image.find_rects()` function.

### 14.2 `corners`

```python
rect.corners()
```

Returns a list of tuples containing the four corners of the rectangle object, each tuple in the format (x, y). The four corners are usually ordered clockwise starting from the top-left corner.

### 14.3 `rect`

```python
rect.rect()
```

Returns a rectangle tuple (x, y, w, h) for other image processing methods like the bounding box in `image.draw_rectangle`.

### 14.4 `x`

```python
rect.x()
```

Returns the x-coordinate of the top-left corner of the rectangle. You can also access this value using index [0].

### 14.5 `y`

```python
rect.y()
```

Returns the y-coordinate of the top-left corner of the rectangle. You can also access this value using index [1].

### 14.6 `w`

```python
rect.w()
```

Returns the width of the rectangle. You can also access this value using index [2].

### 14.7 `h`

```python
rect.h()
```

Returns the height of the rectangle. You can also access this value using index [3].

### 14.8 `magnitude`

```python
rect.magnitude()
```

Returns the magnitude of the rectangle. You can also access this value using index [4].

## 15 Class `QRCode`

The QR code object is returned by the `image.find_qrcodes` function.

### 15.1 Constructor

```python
class image.qrcode
```

Create this object by using the `image.find_qrcodes()` function.

### 15.2 `corners`

```python
qrcode.corners()
```

Returns a list of tuples containing the four corners of the QR code, each tuple in the format (x, y). The four corners are usually ordered clockwise starting from the top-left corner.

### 15.3 `rect`

```python
qrcode.rect()
```

Returns a rectangle tuple (x, y, w, h) for other image processing methods like the QR code bounding box in `image.draw_rectangle`.

### 15.4 `x`

```python
qrcode.x()
```

Returns the x-coordinate of the QR code's bounding box (int). You can also access this value using index [0].

### 15.5 `y`

```python
qrcode.y()
```

Returns the y-coordinate of the QR code's bounding box (int). You can also access this value using index [1].

### 15.6 `w`

```python
qrcode.w()
```

Returns the width of the QR code's bounding box (int). You can also access this value using index [2].

### 15.7 `h`

```python
qrcode.h()
```

Returns the height of the QR code's bounding box (int). You can also access this value using index [3].

### 15.8 `payload`

```python
qrcode.payload()
```

Returns the payload string of the QR code, such as a URL. You can also access this value using index [4].

### 15.9 `version`

```python
qrcode.version()
```

Returns the version number of the QR code (int). You can also access this value using index [5].

### 15.10 `ecc_level`

```python
qrcode.ecc_level()
```

Returns the error correction level of the QR code (int). You can also access this value using index [6].

### 15.11 `mask`

```python
qrcode.mask()
```

Returns the mask of the QR code (int). You can also access this value using index [7].

### 15.12 `data_type`

```python
qrcode.data_type()
```

Returns the data type of the QR code. You can also access this value using index [8].

### 15.13 `eci`

```python
qrcode.eci()
```

Returns the ECI (Extended Channel Interpretation) of the QR code, which is used to store encoding information for data bytes in the QR code. Check this value when dealing with QR codes containing non-standard ASCII text. You can also access this value using index [9].

### 15.14 `is_numeric`

```python
qrcode.is_numeric()
```

Returns True if the QR code's data type is numeric.

### 15.15 `is_alphanumeric`

```python
qrcode.is_alphanumeric()
```

Returns True if the QR code's data type is alphanumeric.

### 15.16 `is_binary`

```python
qrcode.is_binary()
```

Returns True if the QR code's data type is in binary format. To accurately handle all types of text, check if `eci` is True to determine the text encoding of the data. It is typically standard ASCII but may be UTF-8 containing two-byte characters.

### 15.17 `is_kanji`

```python
qrcode.is_kanji()
```

Returns True if the QR code's data type is in Kanji format. If the return value is True, you need to decode the string yourself, as each Kanji character is 10 bits, and MicroPython does not support parsing this type of text.

## 16 Class `AprilTag`

The AprilTag object is returned by the `image.find_apriltags` function.

### 16.1 Constructor

```python
class image.apriltag
```

Create this object by calling the `image.find_apriltags()` function.

### 16.2 `corners`

```python
apriltag.corners()
```

This method returns a list of tuples containing the four corners of the AprilTag, each tuple in the format (x, y). The four corners are usually ordered clockwise starting from the top-left corner.

### 16.3 `rect`

```python
apriltag.rect()
```

This method returns a rectangle tuple (x, y, w, h) for other image processing methods, such as the AprilTag bounding box in `image.draw_rectangle`.

### 16.4 `x`

```python
apriltag.x()
```

This method returns the x-coordinate of the AprilTag's bounding box (int). You can also access this value using index [0].

### 16.5 `y`

```python
apriltag.y()
```

This method returns the y-coordinate of the AprilTag's bounding box (int). You can also access this value using index [1].

### 16.6 `w`

```python
apriltag.w()
```

This method returns the width of the AprilTag's bounding box (int). You can also access this value using index [2].

### 16.7 `h`

```python
apriltag.h()
```

This method returns the height of the AprilTag's bounding box (int). You can also access this value using index [3].

### 16.8 `id`

```python
apriltag.id()
```

This method returns the numeric ID of the AprilTag.

- TAG16H5 -> 0 to 29
- TAG25H7 -> 0 to 241
- TAG25H9 -> 0 to 34
- TAG36H10 -> 0 to 2319
- TAG36H11 -> 0 to 586
- ARTOOLKIT -> 0 to 511

You can also access this value using index [4].

### 16.9 `family`

```python
apriltag.family()
```

This method returns the numeric family of the AprilTag.

- image.TAG16H5
- image.TAG25H7
- image.TAG25H9
- image.TAG36H10
- image.TAG36H11
- image.ARTOOLKIT

You can also access this value using index [5].

### 16.10 `cx`

```python
apriltag.cx()
```

This method returns the x-coordinate of the AprilTag's center (int). You can also access this value using index [6].

### 16.11 `cy`

```python
apriltag.cy()
```

This method returns the y-coordinate of the AprilTag's center (int). You can also access this value using index [7].

### 16.12 `rotation`

```python
apriltag.rotation()
```

This method returns the rotation angle of the AprilTag in radians (int). You can also access this value using index [8].

### 16.13 `decision_margin`

```python
apriltag.decision_margin()
```

This method returns the decision margin of the AprilTag, reflecting the confidence in the detection (float). You can also access this value using index [9].

### 16.14 `hamming`

```python
apriltag.hamming()
```

This method returns the maximum acceptable Hamming distance (i.e., the number of acceptable bit errors) for the AprilTag. Specifically:

- TAG16H5: up to 0 bit errors
- TAG25H7: up to 1 bit error
- TAG25H9: up to 3 bit errors
- TAG36H10: up to 3 bit errors
- TAG36H11: up to 4 bit errors
- ARTOOLKIT: up to 0 bit errors

You can also access this value using index [10].

### 16.15 `goodness`

```python
apriltag.goodness()
```

This method returns the color saturation of the AprilTag image, ranging from 0.0 to 1.0, with 1.0 indicating the best condition.

> Currently, this value is typically 0.0. In the future, we plan to enable a feature called "tag refinement" to support the detection of smaller AprilTags. However, this feature may currently reduce the frame rate to below 1 FPS.

You can also access this value using index [11].

### 16.16 `x_translation`

```python
apriltag.x_translation()
```

This method returns the camera's displacement in the x direction, with the unit unknown.

This method is useful for determining the position of an AprilTag relative to the camera. However, factors such as the size of the AprilTag and the lens you are using will affect the unit of x. For convenience, we recommend using a lookup table to convert the output of this method to information relevant to your application.

Note: The direction here is from left to right.

You can also access this value using index [12].

### 16.17 `y_translation`

```python
apriltag.y_translation()
```

This method returns the camera's displacement in the y direction, with the unit unknown.

This method is useful for determining the position of an AprilTag relative to the camera. However, factors such as the size of the AprilTag and the lens you are using will affect the unit of y. For convenience, we recommend using a lookup table to convert the output of this method to information relevant to your application.

Note: The direction here is from top to bottom.

You can also access this value using index [13].

### 16.18 `z_translation`

```python
apriltag.z_translation()
```

This method returns the camera's displacement in the z direction, with the unit unknown.

This method is useful for determining the position of an AprilTag relative to the camera. However, factors such as the size of the AprilTag and the lens you are using will affect the unit of z. For convenience, we recommend using a lookup table to convert the output of this method to information relevant to your application.

Note: The direction here is from front to back.

You can also access this value using index [14].

### 16.19 `x_rotation`

```python
apriltag.x_rotation()
```

This method returns the rotation angle of the AprilTag in the x plane, measured in radians. For example, this method can be applied when moving the camera from left to right to observe the AprilTag.

You can also access this value using index [15].

### 16.20 `y_rotation`

```python
apriltag.y_rotation()
```

This method returns the rotation angle of the AprilTag in the y plane, measured in radians. For example, this method can be applied when moving the camera from top to bottom to observe the AprilTag.

You can also access this value using index [16].

### 16.21 `z_rotation`

```python
apriltag.z_rotation()
```

This method returns the rotation angle of the AprilTag in the z plane, measured in radians. For example, this method can be applied when rotating the camera to observe the AprilTag.

Note: This method is a renamed version of `apriltag.rotation()`.

You can also access this value using index [17].

## 17 Class `DataMatrix`

The DataMatrix object is returned by the `image.find_datamatrices` function.

### 17.1 Constructor

```python
class image.datamatrix
```

Create this object by calling the `image.find_datamatrices()` function.

### 17.2 `corners`

```python
datamatrix.corners()
```

This method returns a list of tuples containing the four corners of the DataMatrix, each tuple in the format (x, y). The four corners are usually ordered clockwise starting from the top-left corner.

### 17.3 `rect`

```python
datamatrix.rect()
```

This method returns a rectangle tuple (x, y, w, h) for other image processing methods, such as the DataMatrix bounding box in `image.draw_rectangle`.

### 17.4 `x`

```python
datamatrix.x()
```

This method returns the x-coordinate of the DataMatrix's bounding box (int). You can also access this value using index [0].

### 17.5 `y`

```python
datamatrix.y()
```

This method returns the y-coordinate of the DataMatrix's bounding box (int). You can also access this value using index [1].

### 17.6 `w`

```python
datamatrix.w()
```

This method returns the width of the DataMatrix's bounding box (int). You can also access this value using index [2].

### 17.7 `h`

```python
datamatrix.h()
```

This method returns the height of the DataMatrix's bounding box (int). You can also access this value using index [3].

### 17.8 `payload`

```python
datamatrix.payload()
```

This method returns the payload string of the DataMatrix. For example: "string".

You can also access this value using index [4].

### 17.9 `rotation`

```python
datamatrix.rotation()
```

This method returns the rotation angle of the DataMatrix, measured in radians (float).

You can also access this value using index [5].

### 17.10 `rows`

```python
datamatrix.rows()
```

This method returns the number of rows in the DataMatrix (int).

You can also access this value using index [6].

### 17.11 `columns`

```python
datamatrix.columns()
```

This method returns the number of columns in the DataMatrix (int).

You can also access this value using index [7].

### 17.12 `capacity`

```python
datamatrix.capacity()
```

This method returns the number of characters that the DataMatrix can hold.

You can also access this value using index [8].

### 17.13 `padding`

```python
datamatrix.padding()
```

This method returns the number of unused characters in the DataMatrix.

You can also access this value using index [9].

## 18 Class `BarCode`

The BarCode object is returned by the `image.find_barcodes` function.

### 18.1 Constructor

```python
class image.barcode
```

Create this object by calling the `image.find_barcodes()` function.

### 18.2 `corners`

```python
barcode.corners()
```

This method returns a list of tuples containing the four corners of the barcode, each tuple in the format (x, y). The four corners are usually ordered clockwise starting from the top-left corner.

### 18.3 `rect`

```python
barcode.rect()
```

This method returns a rectangle tuple (x, y, w, h) for other image processing methods, such as the barcode bounding box in `image.draw_rectangle`.

### 18.4 `x`

```python
barcode.x()
```

This method returns the x-coordinate of the barcode's bounding box (int). You can also access this value using index [0].

### 18.5 `y`

```python
barcode.y()
```

This method returns the y-coordinate of the barcode's bounding box (int). You can also access this value using index [1].

### 18.6 `w`

```python
barcode.w()
```

This method returns the width of the barcode's bounding box (int). You can also access this value using index [2].

### 18.7 `h`

```python
barcode.h()
```

This method returns the height of the barcode's bounding box (int). You can also access this value using index [3].

### 18.8 `payload`

```python
barcode.payload()
```

This method returns the payload string of the barcode, for example: "quantity".

You can also access this value using index [4].

### 18.9 `type`

```python
barcode.type()
```

This method returns the type of the barcode (int). Possible types include:

- image.EAN2
- image.EAN5
- image.EAN8
- image.UPCE
- image.ISBN10
- image.UPCA
- image.EAN13
- image.ISBN13
- image.I25
- image.DATABAR
- image.DATABAR_EXP
- image.CODABAR
- image.CODE39
- image.PDF417 (future use, currently unavailable)
- image.CODE93
- image.CODE128

You can also access this value using index [5].

### 18.10 `rotation`

```python
barcode.rotation()
```

This method returns the rotation angle of the barcode, measured in radians (float).

You can also access this value using index [6].

### 18.11 `quality`

```python
barcode.quality()
```

This method returns the number of times the barcode has been detected in the image (int).

When scanning a barcode, each new scan line can decode the same barcode. Each time this process occurs, the value of the barcode increases.

You can also access this value using index [7].

## 19 Class `Displacement`

The Displacement object is returned by the `image.find_displacement` function.

### 19.1 Constructor

```python
class image.displacement
```

Create this object by calling the `image.find_displacement()` function.

### 19.2 `x_translation`

```python
displacement.x_translation()
```

This method returns the x-direction translation between two images, measured in pixels. The return value is a float, representing precise sub-pixel displacement.

You can also access this value using index [0].

### 19.3 `y_translation`

```python
displacement.y_translation()
```

This method returns the y-direction translation between two images, measured in pixels. The return value is a float, representing precise sub-pixel displacement.

You can also access this value using index [1].

### 19.4 `rotation`

```python
displacement.rotation()
```

This method returns the rotation between two images, measured in radians. The return value is a float, representing precise sub-pixel rotation.

You can also access this value using index [2].

### 19.5 `scale`

```python
displacement.scale()
```

This method returns the scale factor between two images, represented as a float.

You can also access this value using index [3].

### 19.6 `response`

```python
displacement.response()
```

This method returns the quality assessment of the displacement match between two images, with values ranging from 0 to 1. If the return value is less than 0.1, the displacement object may be considered noise.

You can also access this value using index [4].

## 20 Class `Kptmatch`

The keypoint object is returned by the `image.match_descriptor` function.

### 20.1 Constructor

```python
class image.kptmatch
```

Create this object by calling the `image.match_descriptor()` function.

### 20.2 `rect`

```python
kptmatch.rect()
```

This method returns a rectangle tuple (x, y, w, h) for other image processing methods, such as drawing the keypoint bounding box in `image.draw_rectangle`.

### 20.3 `cx`

```python
kptmatch.cx()
```

This method returns the x-coordinate of the keypoint's center as an integer.

You can also access this value using index [0].

### 20.4 `cy`

```python
kptmatch.cy()
```

This method returns the y-coordinate of the keypoint's center as an integer.

You can also access this value using index [1].

### 20.5 `x`

```python
kptmatch.x()
```

This method returns the x-coordinate of the keypoint's bounding box as an integer.

You can also access this value using index [2].

### 20.6 `y`

```python
kptmatch.y()
```

This method returns the y-coordinate of the keypoint's bounding box as an integer.

You can also access this value using index [3].

### 20.7 `w`

```python
kptmatch.w()
```

This method returns the width of the keypoint's bounding box as an integer.

You can also access this value using index [4].

### 20.8 `h`

```python
kptmatch.h()
```

This method returns the height of the keypoint's bounding box as an integer.

You can also access this value using index [5].

### 20.9 `count`

```python
kptmatch.count()
```

This method returns the number of matched keypoints as an integer.

You can also access this value using index [6].

### 20.10 `theta`

```python
kptmatch.theta()
```

This method returns the estimated rotation of the keypoints as an integer.

You can also access this value using index [7].

### 20.11 `match`

```python
kptmatch.match()
```

This method returns a list of (x, y) tuples of the matched keypoints.

You can also access this value using index [8].

## 21 Constants

### 21.1 `image.SEARCH_EX`

Used for exhaustive template matching search.

### 21.2 `image.SEARCH_DS`

Used for faster template matching search.

### 21.3 `image.EDGE_CANNY`

Applies the Canny edge detection algorithm to the image.

### 21.4 `image.EDGE_SIMPLE`

Applies a threshold high-pass filter algorithm for edge detection.

### 21.5 `image.CORNER_FAST`

High-speed, low-accuracy corner detection algorithm for ORB keypoints.

### 21.6 `image.CORNER_AGAST`

Low-speed, high-accuracy corner detection algorithm for ORB keypoints.

### 21.7 `image.TAG16H5`

Bitmask enumeration for the TAG16H5 family used in AprilTags.

### 21.8 `image.TAG25H7`

Bitmask enumeration for the TAG25H7 family used in AprilTags.

### 21.9 `image.TAG25H9`

Bitmask enumeration for the TAG25H9 family used in AprilTags.

### 21.10 `image.TAG36H10`

Bitmask enumeration for the TAG36H10 family used in AprilTags.

### 21.11 `image.TAG36H11`

Bitmask enumeration for the TAG36H11 family used in AprilTags.

### 21.12 `image.ARTOOLKIT`

Bitmask enumeration for the ARTOOLKIT family used in AprilTags.

### 21.13 `image.EAN2`

Enumeration for the EAN2 barcode type.

### 21.14 `image.EAN5`

Enumeration for the EAN5 barcode type.

### 21.15 `image.EAN8`

Enumeration for the EAN8 barcode type.

### 21.16 `image.UPCE`

Enumeration for the UPCE barcode type.

### 21.17 `image.ISBN10`

Enumeration for the ISBN10 barcode type.

### 21.18 `image.UPCA`

Enumeration for the UPCA barcode type.

### 21.19 `image.EAN13`

Enumeration for the EAN13 barcode type.

### 21.20 `image.ISBN13`

Enumeration for the ISBN13 barcode type.

### 21.21 `image.I25`

Enumeration for the I25 barcode type.

### 21.22 `image.DATABAR`

Enumeration for the DATABAR barcode type.

### 21.23 `image.DATABAR_EXP`

Enumeration for the DATABAR_EXP barcode type.

### 21.24 `image.CODABAR`

Enumeration for the CODABAR barcode type.

### 21.25 `image.CODE39`

Enumeration for the CODE39 barcode type.

### 21.26 `image.PDF417`

Enumeration for the PDF417 barcode type (currently unavailable).

### 21.27 `image.CODE93`

Enumeration for the CODE93 barcode type.

### 21.28 `image.CODE128`

Enumeration for the CODE128 barcode type.
