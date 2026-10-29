# `Image Processing` API Manual

This module is ported from `openmv` and has basically the same functionality. For details, please refer to the [official documentation](https://docs.openmv.io/v5.0.0/library/omv.image.html). This article lists the differences from the official API and the newly added APIs, and also includes references to some native APIs.

## Class `Image`

The `Image` class is the fundamental object in machine vision processing. This class supports creating image objects from memory regions such as Micropython GC, MMZ, system heap, and VB areas. In addition, images can be created directly by referencing external memory (ALLOC_REF). Unused image objects are automatically released during garbage collection, and memory can also be manually released.

Supported image formats are as follows:

- BINARY
- GRAYSCALE
- RGB565
- BAYER
- YUV422
- JPEG
- PNG
- ARGB8888 (newly added)
- RGB888 (newly added)
- RGBP888 (newly added)
- YUV420 (newly added)

Supported memory allocation regions:

- **ALLOC_MPGC**: Memory managed by Micropython
- **ALLOC_HEAP**: System heap memory
- **ALLOC_MMZ**: Multimedia memory
- **ALLOC_VB**: Video buffer
- **ALLOC_REF**: Memory that uses referenced objects without allocating new memory

### Constructor

```python
image.Image(path, alloc=ALLOC_MMZ, cache=True, phyaddr=0, virtaddr=0, poolid=0, data=None)
```

Create an image object from the file path `path`, supporting BMP, PGM, PPM, JPG, JPEG formats.

```python
image.Image(w, h, format, alloc=ALLOC_MMZ, cache=True, phyaddr=0, virtaddr=0, poolid=0, data=None)
```

Create an image object with the specified size and format.

- **w**: image width
- **h**: image height
- **format**: image format
- **alloc**: memory allocation method (default ALLOC_MMZ)
- **cache**: whether to enable memory cache (enabled by default)
- **phyaddr**: physical memory address, only applicable to the VB area
- **virtaddr**: virtual memory address, only applicable to the VB area
- **poolid**: pool ID of the VB area, only applicable to the VB area
- **data**: reference to an external data object (optional)

Example:

```python
# Create a 640x480 image in ARGB8888 format in the MMZ area
img = image.Image(640, 480, image.ARGB8888)

# Create a 640x480 image in YUV420 format in the VB area
img = image.Image(640, 480, image.YUV420, alloc=image.ALLOC_VB, phyaddr=xxx, virtaddr=xxx, poolid=xxx)

# Create a 640x480 image in RGB888 format using an external reference
img = image.Image(640, 480, image.RGB888, alloc=image.ALLOC_REF, data=buffer_obj)
```

Manually release image memory:

```python
del img
gc.collect()
```

### `phyaddr`

Get the physical memory address of the image data.

```python
image.phyaddr()
```

### `virtaddr`

Get the virtual memory address of the image data.

```python
image.virtaddr()
```

### `poolid`

Get the VB pool ID of the image.

```python
image.poolid()
```

### `to_rgb888`

Convert the image to RGB888 format and return a new image object.

```python
image.to_rgb888(x_scale=1.0, y_scale=1.0, roi=None, rgb_channel=-1, alpha=256, color_palette=None, alpha_palette=None, hint=0, alloc=ALLOC_MMZ, cache=True, phyaddr=0, virtaddr=0, poolid=0)
```

### `copy_from`

Copy the content of `src_img` into the current image object.

```python
image.copy_from(src_img)
```

### `copy_to`

Copy the content of the current image object to `dst_img`.

```python
image.copy_to(dst_img)
```

### `to_numpy_ref`

Convert the image object to a NumPy array. The returned NumPy array shares memory with the original image object.

```python
image.to_numpy_ref()
```

Supported formats: GRAYSCALE, RGB565, ARGB8888, RGB888, RGBP888.

<a id="draw_string_advanced"></a>

### `draw_string_advanced`

An enhanced version of `draw_string` that supports Chinese display and allows users to customize the font through the `font` parameter.

```python
image.draw_string_advanced(x, y, char_size, str, [color, font])
```

### `as_lvgl_img_src`

This method is an **LVGL helper tool** used to quickly connect the `image_t` object from the image processing library to the **LVGL** graphics library. It automatically sets the image as the data source of the LVGL image object (`lv.img`).

#### **Function Description**

This function creates an LVGL image descriptor (`lv_img_dsc_t`) and points it directly to the raw pixel buffer of the current image. It automatically handles format mapping and performs an **in-place color conversion** for **RGB888** images to match the BGR byte order required by LVGL.

#### **Syntax**

```python
image.as_lvgl_img_src(lv_img_obj)
```

#### **Parameters**

- **`lv_img_obj`**: Pointer to an already created LVGL image object (created via `lv.img(parent)`).

#### **Return Value**

- Returns the reference of the passed-in `lv_img_obj`, supporting chained calls.

#### **Important Limitations and Notes**

1. **Supported Formats**: Currently only `PIXFORMAT_RGB565` and `PIXFORMAT_RGB888` are supported.
1. **In-place Modification**: For **RGB888** images, this function will **directly modify the original image buffer** (performing RGB to BGR conversion). If you still need the original RGB data afterwards, please make an image copy first (`img.copy()`).
1. **Memory Management**: This operation **does not copy image pixel data**. The LVGL descriptor directly references the existing image memory. Therefore, during the display of the LVGL object, you must ensure that the `image` object is not released.
1. **Hardware Acceleration**: On supported hardware, the color conversion is implemented using **RISC-V Vector (vector extension) instructions**, which is approximately **2 times faster** than the standard C language loop (for example, only about 500us is needed at 640x480 resolution).

#### **Usage Example**

```python
import lvgl as lv

# 1. Capture an image
img = sensor.snapshot()

# 2. Create an LVGL image component
ui_img = lv.img(lv.scr_act())

# 3. Use the helper method to set the data source
# This method automatically handles dsc_t allocation and BGR vector conversion
img.as_lvgl_img_src(ui_img)

# 4. Standard LVGL layout settings
ui_img.align(lv.ALIGN.CENTER, 0, 0)
```

### Methods with Implementation Differences

#### APIs with the `crop` Parameter Removed

The `crop` parameter in the following APIs is invalid. A memory allocation method parameter has been added, and they always return new image objects.

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

#### Drawing API

Added support for `ARGB8888` and `RGB888` formats; other formats are not supported.

#### BINARY API

`binary` has added a memory allocation method parameter, which only takes effect when `copy=True`.

#### POOL API

The `mean_pooled` and `midpoint_pooled` methods have added a memory allocation method parameter.

#### Other Image Algorithms

These algorithms only support native image formats; the `RGB888` format must be converted before use.

### `width`

```python
image.width()
```

Returns the width of the image in pixels.

### `height`

```python
image.height()
```

Returns the height of the image in pixels.

### `format`

```python
image.format()
```

Returns the format of the image. Possible values include:

- `sensor.GRAYSCALE`: Grayscale image
- `sensor.RGB565`: RGB image
- `sensor.JPEG`: JPEG compressed image

### `size`

```python
image.size()
```

Returns the size of the image in bytes.

### `get_pixel`

```python
image.get_pixel(x, y[, rgbtuple])
```

Gets the pixel value at the specified position `(x, y)` based on the image format:

- For grayscale images, returns the grayscale value.
- For RGB565 images, returns the tuple `(r, g, b)` in RGB888 format.
- For Bayer images, returns the pixel value at that position.

Compressed images are not supported.

> `get_pixel()` and `set_pixel()` are the only methods to operate on Bayer pattern images. A Bayer pattern image is a special format that contains `R/G/R/G/...` on even rows and `G/B/G/B/...` on odd rows, with each pixel occupying 8 bits.

### `set_pixel`

```python
image.set_pixel(x, y, pixel)
```

Sets the pixel value at the specified position `(x, y)` of the image:

- For grayscale images, sets the grayscale value.
- For RGB images, sets the tuple `(r, g, b)` in RGB888 format.

Compressed images are not supported.

> `get_pixel()` and `set_pixel()` are the only methods to operate on Bayer pattern images.

### `mean_pool`

```python
image.mean_pool(x_div, y_div)
```

Divides the image into `x_div * y_div` rectangular regions, computes the average value of each region, and returns a modified image containing these averages.

This method can be used to quickly downsize an image.

Compressed images and Bayer images are not supported.

### `mean_pooled`

```python
image.mean_pooled(x_div, y_div)
```

Similar to `mean_pool()`, but returns a new copy of the image.

### `midpoint_pool`

```python
image.midpoint_pool(x_div, y_div[, bias=0.5])
```

Divides the image into `x_div * y_div` regions, computes the midpoint value of each region, and returns a modified image containing these midpoints.

- With `bias=0.0`, returns the minimum value of the region; with `bias=1.0`, returns the maximum value of the region.

### `midpoint_pooled`

```python
image.midpoint_pooled(x_div, y_div[, bias=0.5])
```

Similar to `midpoint_pool()`, but returns a new copy of the image.

### `to_grayscale`

```python
image.to_grayscale([copy=False])
```

Converts the image to a grayscale image. If `copy=True`, creates a new image copy on the heap. Returns the image object.

### `to_rgb565`

```python
image.to_rgb565([copy=False])
```

Converts the image to an RGB565 format color image. If `copy=True`, creates a new image copy on the heap. Returns the image object.

### `to_rainbow`

```python
image.to_rainbow([copy=False])
```

Converts the image to a rainbow-colored image. Returns the image object.

### `compress`

```python
image.compress([quality=50])
```

Performs JPEG compression on the image with the specified quality `quality` (0-100).

### `compress_for_ide`

```python
image.compress_for_ide([quality=50])
```

Compresses the image and formats it for display in the OpenMV IDE.

### `compressed`

```python
image.compressed([quality=50])
```

Returns the JPEG-compressed image.

### `compressed_for_ide`

```python
image.compressed_for_ide([quality=50])
```

Returns the JPEG-compressed image formatted for display in the OpenMV IDE.

### `copy`

```python
image.copy([roi[, copy_to_fb=False]])
```

Creates a copy of the image object, with optional specification of a region of interest `roi`.

### `save`

```python
image.save(path[, roi[, quality=50]])
```

Saves the image to the specified path `path`, with optional specification of a region of interest `roi` and JPEG compression quality `quality`.

### `clear`

```python
image.clear()
```

Quickly sets all pixels in the image to zero. Returns the image object.

### `draw_line`

```python
image.draw_line(x0, y0, x1, y1[, color[, thickness=1]])
```

Draws a line on the image from `(x0, y0)` to `(x1, y1)`. Arguments can be passed individually as `x0, y0, x1, y1`, or as a tuple `(x0, y0, x1, y1)`.

- **color**: An RGB888 tuple representing the color, applicable to grayscale or RGB565 images, defaulting to white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the line, defaulting to 1.

The method returns the image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `draw_rectangle`

```python
image.draw_rectangle(x, y, w, h[, color[, thickness=1[, fill=False]]])
```

Draws a rectangle on the image. Arguments can be passed individually as `x, y, w, h`, or as a tuple `(x, y, w, h)`.

- **color**: An RGB888 tuple representing the color, applicable to grayscale or RGB565 images, defaulting to white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the rectangle's border, defaulting to 1.
- **fill**: When set to `True`, fills the interior of the rectangle, defaulting to `False`.

The method returns the image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `draw_ellipse-1`

```python
image.draw_ellipse(cx, cy, rx, ry, rotation[, color[, thickness=1[, fill=False]]])
```

Draws an ellipse on the image. Arguments can be passed individually as `cx, cy, rx, ry, rotation`, or as a tuple `(cx, cy, rx, ry, rotation)`.

- **color**: An RGB888 tuple representing the color, applicable to grayscale or RGB565 images, defaulting to white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the ellipse's border, defaulting to 1.
- **fill**: When set to `True`, fills the interior of the ellipse, defaulting to `False`.

The method returns the image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `draw_circle`

```python
image.draw_circle(x, y, radius[, color[, thickness=1[, fill=False]]])
```

Draws a circle on the image. Arguments can be passed individually as `x, y, radius`, or as a tuple `(x, y, radius)`.

- **color**: An RGB888 tuple representing the color, applicable to grayscale or RGB565 images, defaulting to white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the circle's border, defaulting to 1.
- **fill**: When set to `True`, fills the interior of the circle, defaulting to `False`.

The method returns the image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `draw_string`

```python
image.draw_string(x, y, text[, color[, scale=1[, x_spacing=0[, y_spacing=0[, mono_space=True]]]]])
```

Draws 8x10 sized text starting at the `(x, y)` position of the image. Arguments can be passed individually as `x, y`, or as a tuple `(x, y)`.

- **text**: The string to draw. Newline characters `\n`, `\r`, or `\r\n` are used to move the cursor to the next line.
- **color**: An RGB888 tuple representing the color, applicable to grayscale or RGB565 images, defaulting to white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **scale**: Controls the scaling factor of the text, defaulting to 1. Must be an integer.
- **x_spacing**: Adjusts the horizontal spacing between characters. Positive values increase the spacing, negative values decrease it.
- **y_spacing**: Adjusts the vertical spacing between lines. Positive values increase the spacing, negative values decrease it.
- **mono_space**: Defaults to `True`, making characters have fixed width. When set to `False`, character spacing is dynamically adjusted based on character width.

The method returns the image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `draw_cross`

```python
image.draw_cross(x, y[, color[, size=5[, thickness=1]]])
```

Draws a cross marker on the image. Arguments can be passed individually as `x, y`, or as a tuple `(x, y)`.

- **color**: An RGB888 tuple representing the color, applicable to grayscale or RGB565 images, defaulting to white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **size**: Controls the size of the cross marker, defaulting to 5.
- **thickness**: Controls the pixel width of the cross lines, defaulting to 1.

The method returns the image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `draw_arrow`

```python
image.draw_arrow(x0, y0, x1, y1[, color[, thickness=1]])
```

Draws an arrow on the image from `(x0, y0)` to `(x1, y1)`. Arguments can be passed individually as `x0, y0, x1, y1`, or as a tuple `(x0, y0, x1, y1)`.

- **color**: An RGB888 tuple representing the color, applicable to grayscale or RGB565 images, defaulting to white. For grayscale images, a pixel value (range 0-255) can also be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- **thickness**: Controls the pixel width of the arrow lines, defaulting to 1.

The method returns the image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `draw_image`

```python
image.draw_image(image, x, y[, x_scale=1.0[, y_scale=1.0[, mask=None[, alpha=256]]]])
```

This function is used to draw an image at the specified position (x, y), where the top-left corner of the image aligns with that position. Arguments x and y can be passed individually, or as a tuple (x, y).

- `x_scale`: Controls the horizontal scaling factor of the image (float).
- `y_scale`: Controls the vertical scaling factor of the image (float).
- `mask`: A pixel-level mask image applied to the drawing operation. The mask should be a binary image (black and white pixels) with the same dimensions as the target image.
- `alpha`: Sets the transparency when drawing the source image, with a range of 0-256. 256 means fully opaque; smaller values indicate the degree of blending between the source and target images; 0 means the target image is not modified at all.

This method does not support compressed images and Bayer format images.

### `draw_keypoints`

```python
image.draw_keypoints(keypoints[, color[, size=10[, thickness=1[, fill=False]]]])
```

Draws feature points on the image.

- `color`: Specifies the color, applicable to grayscale or RGB565 images. Defaults to white. For grayscale images, a grayscale value (0-255) can be passed; for RGB565 images, a byte-swapped RGB565 value can be passed.
- `size`: Controls the size of the feature points.
- `thickness`: Controls the line thickness (in pixels).
- `fill`: If True, fills the feature points.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `flood_fill`

```python
image.flood_fill(x, y[, seed_threshold=0.05[, floating_threshold=0.05[, color[, invert=False[, clear_background=False[, mask=None]]]]]])
```

Fills an area of the image starting from the position (x, y). `x` and `y` can be passed individually, or as a tuple (x, y).

- `seed_threshold`: Controls the difference between pixels in the fill area and the seed pixel.
- `floating_threshold`: Controls the difference between adjacent pixels in the fill area.
- `color`: The fill color, applicable to grayscale or RGB565 images. Defaults to white; a grayscale value or a byte-swapped RGB565 value can also be passed.
- `invert`: If set to True, inverts the fill logic, i.e., fills the area outside the target region.
- `clear_background`: If set to True, zeros out the unfilled pixels.
- `mask`: A pixel-level mask image used to limit the fill area. The mask should be a binary image (black and white pixels) with the same dimensions as the target image.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `binary`

```python
image.binary(thresholds[, invert=False[, zero=False[, mask=None]]])
```

Converts all pixels in the image to a black-and-white binary image based on the specified threshold list `thresholds`.

- `thresholds`: A list of tuples in the format `[(lo, hi), ...]`. For grayscale images, each tuple defines a grayscale value range (lowest and highest); for RGB565 images, each tuple contains six values representing the ranges of the L, A, and B channels in LAB space.
- `invert`: If set to True, inverts the threshold operation, converting pixels outside the thresholds to white.
- `zero`: If set to True, sets pixels matching the thresholds to zero while preserving the rest.
- `mask`: A mask image applied to the binarization operation. The mask should be a binary image with the same dimensions as the target image.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `invert`

```python
image.invert()
```

Quickly inverts the pixel values in a binary image, turning 0 (black) into 1 (white) and 1 (white) into 0 (black).

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `b_and`

```python
image.b_and(image[, mask=None])
```

Performs a bitwise AND operation on two images.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. For scalar values, it can be an RGB888 tuple or a base pixel value for grayscale images (e.g., an 8-bit grayscale value).
- `mask`: A mask image used to limit the operation. The mask should be a binary image with the same dimensions as the target image.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `b_nand`

```python
image.b_nand(image[, mask=None])
```

Performs a bitwise NAND operation on two images.

Other parameter descriptions are the same as `b_and`.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `b_or`

```python
image.b_or(image[, mask=None])
```

Performs a bitwise OR operation on two images.

Other parameter descriptions are the same as `b_and`.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `b_nor`

```python
image.b_nor(image[, mask=None])
```

Performs a bitwise NOR operation on two images.

Other parameter descriptions are the same as `b_and`.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `b_xor`

```python
image.b_xor(image[, mask=None])
```

Performs a bitwise XOR operation on two images.

Other parameter descriptions are the same as `b_and`.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `b_xnor`

```python
image.b_xnor(image[, mask=None])
```

Performs a bitwise XNOR operation on two images.

Other parameter descriptions are the same as `b_and`.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `erode`

```python
image.erode(size[, threshold[, mask=None]])
```

Performs an erosion operation by removing pixels from the edges of segmented regions.

- `size`: Defines the convolution kernel size of the erosion operation as `((size*2)+1)x((size*2)+1)`.
- `threshold`: If unspecified, performs a standard erosion operation; if specified, decides whether to erode a pixel based on whether the sum of neighboring pixels is less than the threshold.

Returns the image object, allowing chained calls to other methods.

### `dilate`

```python
image.dilate(size[, threshold[, mask=None]])
```

Performs a dilation operation by adding pixels to the edges of segmented regions.

Other parameter descriptions are the same as `erode`.

Returns the image object, allowing chained calls to other methods.

### `open`

```python
image.open(size[, threshold[, mask=None]])
```

Performs erosion followed by dilation on the image sequentially. For details, see the `erode()` and `dilate()` methods.

Returns the image object, allowing chained calls to other methods.

### `close`

```python
image.close(size[, threshold[, mask=None]])
```

Performs dilation followed by erosion on the image sequentially. For details, see the `erode()` and `dilate()` methods.

Returns the image object, allowing chained calls to other methods.

### `top_hat`

```python
image.top_hat(size[, threshold[, mask=None]])
```

This function returns the difference between the original image and the image resulting from performing `image.open()`.

- `size`: Defines the convolution kernel size of the operation as `((size*2)+1)x((size*2)+1)`.
- `threshold`: Used to control the intensity of the operation. If unspecified, the standard operation is performed by default.
- `mask`: A pixel-level mask image. The mask should be a binary image (black and white pixels) with dimensions matching the target image. Only pixels set to white in the mask are operated on.

This method does not support compressed images and Bayer format images.

### `black_hat`

```python
image.black_hat(size[, threshold[, mask=None]])
```

This function returns the difference between the original image and the image resulting from performing `image.close()`.

- `size`: Defines the convolution kernel size of the operation as `((size*2)+1)x((size*2)+1)`.
- `threshold`: Used to control the intensity of the operation. If unspecified, the standard operation is performed by default.
- `mask`: A pixel-level mask image. The mask should be a binary image with dimensions matching the target image. Only pixels set to white in the mask are operated on.

This method does not support compressed images and Bayer format images.

### `negate`

```python
image.negate()
```

Quickly inverts all pixel values in the image, i.e., flips the numerical value of each color channel pixel (e.g., `255 - pixel`).

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `replace`

```python
image.replace(image[, hmirror=False[, vflip=False[, mask=None]]])
```

This function replaces the current image with the specified image.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be RGB888 tuples or base pixel values (e.g., 8-bit grayscale values for grayscale images).
- `hmirror`: When True, the replacement image is horizontally mirrored.
- `vflip`: When True, the replacement image is vertically flipped.
- `mask`: A pixel-level mask image. The mask should be a binary image with dimensions matching the target image. Only pixels set to white in the mask are modified.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `add`

```python
image.add(image[, mask=None])
```

Performs pixel-wise addition on two images.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be RGB888 tuples or base pixel values (e.g., 8-bit grayscale values for grayscale images).
- `mask`: A pixel-level mask image. The mask should be a binary image with dimensions matching the target image. Only pixels set to white in the mask are modified.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `sub`

```python
image.sub(image[, reverse=False[, mask=None]])
```

Performs pixel-wise subtraction on two images.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be RGB888 tuples or base pixel values (e.g., 8-bit grayscale values for grayscale images).
- `reverse`: When True, reverses the subtraction order, i.e., from `this_image - image` to `image - this_image`.
- `mask`: A pixel-level mask image. The mask should be a binary image with dimensions matching the target image. Only pixels set to white in the mask are modified.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `mul`

```python
image.mul(image[, invert=False[, mask=None]])
```

Performs pixel-wise multiplication on two images.

- `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. Scalar values can be RGB888 tuples or base pixel values (e.g., 8-bit grayscale values for grayscale images).
- `invert`: When True, the multiplication changes from `a * b` to `1 / ((1 / a) * (1 / b))`, which brightens the image rather than darkening it (similar to a "screen blend" effect).
- `mask`: A pixel-level mask image. The mask should be a binary image with dimensions matching the target image. Only pixels set to white in the mask are modified.

Returns the image object, allowing chained calls to other methods.

This method does not support compressed images and Bayer format images.

### `div`

```python
image.div(image[, invert=False[, mask=None]])
```

Performs pixel-wise division of the current image by another image.

The `image` parameter can be an image object, a path to an uncompressed image file (supporting bmp/pgm/ppm formats), or a scalar value. For scalar values, RGB888 tuples or base pixel values are supported (e.g., grayscale values for 8-bit grayscale images, or byte-swapped RGB565 values for RGB images).

Setting `invert=True` changes the division order from `a/b` to `b/a`.

`mask` is a pixel-level mask image used for the operation. The mask image should be a black-and-white image with dimensions matching the current image. Only pixels set to white in the mask are modified.

Returns the modified image object, allowing chained calls to other methods using the dot operator.

Compressed images and Bayer format images are not supported.

### `min`

```python
image.min(image[, mask=None])
```

Replaces the pixels in the current image with the pixel-wise minimum of two images.

The `image` parameter can be an image object, a path to an uncompressed image file (supporting bmp/pgm/ppm formats), or a scalar value. For scalar values, RGB888 tuples or base pixel values are supported (e.g., grayscale values for 8-bit grayscale images, or byte-swapped RGB565 values for RGB images).

`mask` is a pixel-level mask image used for drawing operations. It must be a black-and-white image with dimensions matching the current image. Only areas corresponding to white pixels in the mask are modified.

Returns the new image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

This method is not available on OpenMV4.

### `max`

```python
image.max(image[, mask=None])
```

Replaces the pixels in the current image with the pixel-wise maximum of two images.

The `image` parameter can be an image object, a path to an uncompressed image file (supporting bmp/pgm/ppm formats), or a scalar value. For scalar values, RGB888 tuples or base pixel values are supported (e.g., grayscale values for 8-bit grayscale images, or byte-swapped RGB565 values for RGB images).

`mask` is a pixel-level mask image used for drawing operations. It must be a black-and-white image with dimensions matching the current image. Only areas corresponding to white pixels in the mask are modified.

Returns the new image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `difference`

```python
image.difference(image[, mask=None])
```

Takes the absolute difference of the pixel values of two images. Each color channel's pixel value is updated as follows: `ABS(this.pixel - image.pixel)`.

The `image` parameter can be an image object, a path to an uncompressed image file (supporting bmp/pgm/ppm formats), or a scalar value. For scalar values, RGB888 tuples or base pixel values are supported (e.g., grayscale values for 8-bit grayscale images, or byte-swapped RGB565 values for RGB images).

`mask` is a pixel-level mask image used for drawing operations. It must be a black-and-white image with dimensions matching the current image. Only areas corresponding to white pixels in the mask are modified.

Returns the modified image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `blend`

```python
image.blend(image[, alpha=128[, mask=None]])
```

Blends another image with the current image.

The `image` parameter can be an image object, a path to an uncompressed image file (supporting bmp/pgm/ppm formats), or a scalar value. For scalar values, RGB888 tuples or base pixel values are supported (e.g., grayscale values for 8-bit grayscale images, or byte-swapped RGB565 values for RGB images).

`alpha` controls the blend ratio, with a range of 0 to 256. Values closer to 0 result in a stronger blend; values closer to 256 do the opposite.

`mask` is a pixel-level mask image used for the operation. It must be a black-and-white image with dimensions matching the current image. Only areas corresponding to white pixels in the mask are modified.

Returns the blended image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `histeq`

```python
image.histeq([adaptive=False[, clip_limit=-1[, mask=None]]])
```

Performs histogram equalization on the image to normalize its contrast and brightness.

If `adaptive=True`, the adaptive histogram equalization method is enabled, which generally produces better results than the non-adaptive method but is slower.

`clip_limit` controls the contrast of the adaptive histogram equalization; smaller values (e.g., 10) can produce contrast-limited images.

`mask` is a pixel-level mask image used for the operation. It must be a black-and-white image with dimensions matching the current image. Only areas corresponding to white pixels in the mask are modified.

Returns the processed image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `mean`

```python
image.mean(size[, threshold=False[, offset=0[, invert=False[, mask=None]]]])
```

Performs standard mean blur on the image using a box filter.

`size` specifies the filter size, with values of 1 (corresponding to a 3x3 kernel), 2 (corresponding to a 5x5 kernel), or larger.

To apply adaptive thresholding to the filter output, set `threshold=True`, which binarizes the target pixel based on the brightness of neighboring pixels. Negative values of the `offset` parameter cause more pixels to be set to 1, while positive values only set the pixels with the strongest contrast to 1. Set `invert=True` to invert the output binary image.

`mask` is a pixel-level mask image used for the operation. It must be a black-and-white image with dimensions matching the current image. Only areas corresponding to white pixels in the mask are modified.

Returns the blurred image object, allowing chained calls to other methods.

Compressed images and Bayer format images are not supported.

### `median`

```python
image.median(size, percentile=0.5[, threshold=False[, offset=0[, invert=False[, mask=None]]]])
```

Applies a median filter to the image, which smooths the image while preserving edge details but is slower.

`size` specifies the filter size, with values of 1 (corresponding to a 3x3 kernel), 2 (corresponding to a 5x5 kernel), or larger.

The `percentile` parameter controls the percentile of the selected pixels. By default, the middle value (50th percentile) is selected. Setting `percentile` to 0 implements minimum filtering, and setting it to 1 implements maximum filtering.

If you want to apply adaptive thresholding to the filter result, pass `threshold=True`. The `offset` and `invert` parameters control the binarization output.

`mask` is a pixel-level mask image used for the operation. It must be a black-and-white image with dimensions matching the current image. Only areas corresponding to white pixels in the mask are modified.

Returns the filtered image object.

Compressed images and Bayer format images are not supported.

### `mode`

```python
image.mode(size[, threshold=False, offset=0, invert=False, mask])
```

Applies mode filtering on the image, replacing each pixel with the mode of its neighboring pixels. This method works well on grayscale images, but due to its non-linear nature, may produce artifacts at the edges of RGB images.

**Parameter Description:**

- **size**: The kernel size, with values of 1 (3x3 kernel) or 2 (5x5 kernel).
- **threshold**: If set to `True`, enables adaptive thresholding, adjusting pixel values (set to 1 or 0) based on the brightness of surrounding pixels.
- **offset**: Negative values can increase the number of pixels set to 1; positive values limit the setting to only the pixels with the strongest contrast.
- **invert**: Set to `True` to invert the output binary image result.
- **mask**: A pixel-level mask image used for drawing operations. The mask image should contain only black or white pixels, with dimensions matching the image to be processed. Only pixels set in the mask are modified.

**Return Value**: Returns the image object for further method chaining.

**Note**: Compressed images and Bayer images are not supported.

### `midpoint`

```python
image.midpoint(size[, bias=0.5, threshold=False, offset=0, invert=False, mask])
```

Applies midpoint filtering on the image, computing the midpoint value ((max-min)/2) for each pixel's neighborhood.

**Parameter Description:**

- **size**: The kernel size, with values of 1 (3x3 kernel), 2 (5x5 kernel), or higher.
- **bias**: Controls the degree of min/max blending in the image. 0 performs only minimum filtering, 1 performs only maximum filtering, and values between 0 and 1 enable blended filtering.
- **threshold**: If set to `True`, enables adaptive thresholding, adjusting pixel values (set to 1 or 0) based on the brightness of surrounding pixels.
- **offset**: Negative values can increase the number of pixels set to 1; positive values limit the setting to only the pixels with the strongest contrast.
- **invert**: Set to `True` to invert the output binary image result.
- **mask**: A pixel-level mask image used for drawing operations. The mask image should contain only black or white pixels, with dimensions matching the image to be processed. Only pixels set in the mask are modified.

**Return Value**: Returns the image object for further method chaining.

**Note**: Compressed images and Bayer images are not supported.

### `morph`

```python
image.morph(size, kernel, mul=Auto, add=0)
```

Convolves the image with the specified convolution kernel, implementing general convolution.

**Parameter Description:**

- **size**: The kernel size, controlled as `((size*2)+1)x((size*2)+1)` pixels.
- **kernel**: The kernel used for convolution, can be a tuple or a list with values in the range [-128:127].
- **mul**: A number used to multiply the convolution result. If not set, the default value is used to prevent scaling of the convolution output.
- **add**: A value added to the convolution result of each pixel.

`mul` can be used for global contrast adjustment, and `add` can be used for global brightness adjustment.

**Return Value**: Returns the image object for further method chaining.

**Note**: Compressed images and Bayer images are not supported.

### `gaussian`

```python
image.gaussian(size[, unsharp=False[, mul[, add=0[, threshold=False[, offset=0[, invert=False[, mask=None]]]]]]])
```

Convolves the image with a Gaussian kernel to smooth it.

**Parameter Description:**

- **size**: The kernel size, with values of 1 (3x3 kernel), 2 (5x5 kernel), or higher.
- **unsharp**: If set to `True`, performs an unsharp mask operation, enhancing the clarity of image edges.
- **mul**: A number used to multiply the convolution result. If not set, the default value is used to prevent scaling of the convolution output.
- **add**: A value added to the convolution result of each pixel.

`mul` can be used for global contrast adjustment, and `add` can be used for global brightness adjustment.

**Return Value**: Returns the image object for further method chaining.

**Note**: Compressed images and Bayer images are not supported.

### `laplacian`

```python
image.laplacian(size[, sharpen=False[, mul[, add=0[, threshold=False[, offset=0[, invert=False[, mask=None]]]]]]])
```

Convolves the image with a Laplacian kernel for edge detection.

**Parameter Description:**

- **size**: The kernel size, with values of 1 (3x3 kernel), 2 (5x5 kernel), or higher.
- **sharpen**: If set to `True`, sharpens the image instead of outputting the un-thresholded edge image.
- **mul**: A number used to multiply the convolution result. If not set, the default value is used to prevent scaling of the convolution output.
- **add**: A value added to the convolution result of each pixel.

`mul` can be used for global contrast adjustment, and `add` can be used for global brightness adjustment.

**Return Value**: Returns the image object for further method chaining.

**Note**: Compressed images and Bayer images are not supported.

### `bilateral`

```python
image.bilateral(size[, color_sigma=0.1[, space_sigma=1[, threshold=False[, offset=0[, invert=False[, mask=None]]]]]])
```

Convolves the image with a bilateral filter, smoothing the image while preserving edge features.

**Parameter Description:**

- **size**: The kernel size, with values of 1 (3x3 kernel), 2 (5x5 kernel), or higher.
- **color_sigma**: Controls how closely colors match in the bilateral filter. Increasing this value will result in increased color blurring.
- **space_sigma**: Controls the degree of spatial blurring of pixels. Increasing this value will result in enhanced pixel blurring.

**Return Value**: Returns the image object for further method chaining.

**Note**: Compressed images and Bayer images are not supported.

### `cartoon`

```python
image.cartoon(size[, seed_threshold=0.05[, floating_threshold=0.05[, mask=None]]])
```

Processes the image using the Flood-Fill algorithm, filling all pixel regions in the image, effectively removing textures.

**Parameter Description:**

- **size**: Controls the size of the fill regions.
- **seed_threshold**: Controls the difference between pixels in the fill region and the original starting pixel.
- **floating_threshold**: Controls the difference between pixels in the fill region and adjacent pixels.

**Return Value**: Returns the image object for further method chaining.

**Note**: Compressed images and Bayer images are not supported.

### `remove_shadows`

```python
image.remove_shadows([image])
```

Removes shadows from the current image.

**Function Description**:

- If the current image has no "shadowless" version, this method will attempt to remove shadows from the image, suitable for shadow removal in flat, uniform backgrounds.
- If the current image has a "shadowless" version, this method will remove shadows based on the "true source" background image while preserving non-shadow pixels, facilitating the addition of new objects.

**Return Value**: Returns the image object for further method chaining.

**Note**: Only RGB565 images are supported.

### `chrominvar`

```python
image.chrominvar()
```

Removes lighting effects from the image, retaining only color gradients. This method is fast but has some sensitivity to shadows.

**Return Value**: Returns the image object for further method chaining.

**Note**: Only RGB565 images are supported.

### `illuminvar`

```python
image.illuminvar()
```

Removes lighting effects from the image, retaining only color gradients. This method is slow but is not sensitive to shadows.

**Return Value**: Returns the image object for further method chaining.

**Note**: Only RGB565 images are supported.

### `linpolar`

```python
image.linpolar([reverse=False])
```

This method is used to reproject the image from the Cartesian coordinate system to the linear polar coordinate system.

- **Parameter Description**:
  - `reverse`: A boolean value, defaulting to `False`. If set to `True`, the reprojection is performed in the opposite direction.

The linear polar reprojection process converts the rotation of the image into a translation in the x direction.

**Note**: This function does not support compressed images.

### `logpolar`

```python
image.logpolar([reverse=False])
```

This method is used to reproject the image from the Cartesian coordinate system to the log-polar coordinate system.

- **Parameter Description**:
  - `reverse`: A boolean value, defaulting to `False`. If set to `True`, the reprojection is performed in the opposite direction.

The log-polar reprojection process converts the rotation of the image into a translation in the x direction and a scaling in the y direction.

**Note**: This function does not support compressed images.

### `lens_corr`

```python
image.lens_corr([strength=1.8[, zoom=1.0]])
```

This method is used for lens distortion correction to eliminate the fisheye effect caused by the lens.

- **Parameter Description**:
  - `strength`: A float that determines the degree of fisheye effect removal. The default value is 1.8, and users can adjust it based on the image effect.
  - `zoom`: A float used for image scaling, with a default value of 1.0.

The method returns the image object, allowing users to continue calling other methods.

**Note**: This function does not support compressed images and Bayer images.

### `rotation_corr`

```python
img.rotation_corr([x_rotation=0.0[, y_rotation=0.0[, z_rotation=0.0[, x_translation=0.0[, y_translation=0.0[, zoom=1.0[, fov=60.0[, corners]]]]]]]])
```

Corrects perspective issues in the image by performing 3D rotation on the frame buffer.

- **Parameter Description**:
  - `x_rotation`: The angle to rotate the image around the x-axis (up/down rotation).
  - `y_rotation`: The angle to rotate the image around the y-axis (left/right rotation).
  - `z_rotation`: The angle to rotate the image around the z-axis (image orientation adjustment).
  - `x_translation`: The number of units to move the image along the x-axis after rotation, in units of 3D space.
  - `y_translation`: The number of units to move the image along the y-axis after rotation, in units of 3D space.
  - `zoom`: The image scaling factor, defaulting to 1.0.
  - `fov`: The field of view used for 2D->3D projection. When this value is close to 0, the image is at infinity in the viewport; when it is close to 180, the image is in the viewport. It is generally not recommended to change this value, but you can adjust it to change the 2D->3D mapping effect.
  - `corners`: A list containing four `(x, y)` tuples representing the four corner points, used to create a four-point correspondence homography that maps the first corner to (0,0), the second corner to (image_width-1, 0), the third corner to (image_width-1, image_height-1), and the fourth corner to (0, image_height-1). This parameter allows users to use `rotation_corr` to implement bird's-eye view conversion.

The method returns the image object, allowing users to continue calling other methods.

**Note**: This function does not support compressed images or Bayer images.

### `get_similarity`

```python
image.get_similarity(image)
```

This method returns a "similarity" object that uses the SSIM algorithm to describe the similarity between two images, based on 8x8 pixel blocks comparison.

- **Parameter Description**:
  - `image`: Can be an image object, a path to an uncompressed image file (bmp/pgm/ppm), or a scalar value. For scalar values, it can be an RGB888 tuple or a base pixel value (e.g., 8-bit grayscale values for grayscale images, or byte-swapped RGB565 values for RGB images).

**Note**: This function does not support compressed images and Bayer images.

### `get_histogram`

```python
image.get_histogram([thresholds[, invert=False[, roi[, bins[, l_bins[, a_bins[, b_bins]]]]]]])
```

This method performs normalized histogram operations on all color channels within the ROI and returns a histogram object. For details about the histogram object, please refer to the corresponding documentation. Users can also call this method using `image.get_hist` or `image.histogram`.

- **Parameter Description**:
  - `thresholds`: A list of tuples defining the color ranges to track. For grayscale images, each tuple should contain two values (minimum and maximum grayscale values); for RGB565 images, each tuple should contain six values (l_lo, l_hi, a_lo, a_hi, b_lo, b_hi).
  - `invert`: A boolean value, defaulting to `False`. If set to `True`, the threshold operation is inverted, and pixels will be matched outside the known color ranges.
  - `roi`: A rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, it defaults to the entire image.
  - `bins`: The number of bins for grayscale images, or the number of bins for each channel in RGB565 images.

**Note**: This function does not support compressed images and Bayer images.

### `get_statistics`

```python
image.get_statistics([thresholds[, invert=False[, roi[, bins[, l_bins[, a_bins[, b_bins]]]]]]])
```

This method calculates the mean, median, mode, standard deviation, minimum, maximum, lower quartile, and upper quartile for each color channel within the ROI, and returns a data object.

- **Parameter Description**:
  - `thresholds`: A list of tuples defining the color ranges to track. For grayscale images, each tuple should contain two values (minimum and maximum grayscale values); for RGB565 images, each tuple should contain six values (l_lo, l_hi, a_lo, a_hi, b_lo, b_hi).
  - `invert`: A boolean value, defaulting to `False`. If set to `True`, the threshold operation is inverted, and pixels will be matched outside the known color ranges.
  - `roi`: A rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, it defaults to the entire image.
  - `bins`: The number of bins for grayscale images, or the number of bins for each channel in RGB565 images.

**Note**: This function does not support compressed images and Bayer images.

### `get_regression`

```python
image.get_regression(thresholds[, invert=False[, roi[, x_stride=2[, y_stride=1[, area_threshold=10[, pixels_threshold=10[, robust=False]]]]]]])
```

This method performs linear regression calculation on all pixels in the image that match the thresholds. The calculation uses the least squares method, which is fast but cannot handle outliers. If `robust` is set to `True`, the Theil-Sen estimator will be used to compute the median of the slopes between pixels.

- **Parameter Description**:
  - `thresholds`: A list of tuples defining the color ranges to track.
  - `invert`: A boolean value, defaulting to `False`. If set to `True`, the threshold operation is inverted.
  - `roi`: A rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, it defaults to the entire image.
  - `x_stride`: The number of x pixels to skip when calling the function.
  - `y_stride`: The number of y pixels to skip when calling the function.
  - `area_threshold`: If the bounding box area after regression is less than this value, returns `None`.
  - `pixels_threshold`: If the number of pixels after regression is less than this value, returns `None`.

This method returns an `image.line` object. For detailed usage, see the following blog post: [Linear Regression Line Following](https://openmv.io/blogs/news/linear-regression-line-following).

**Note**: This function does not support compressed images and Bayer images.

### `find_blobs`

```python
image.find_blobs(thresholds[, invert=False[, roi[, x_stride=2[, y_stride=1[, area_threshold=10[, pixels_threshold=10[, merge=False[, margin=0[, threshold_cb=None[, merge_cb=None]]]]]]]]]])
```

This function finds all color blobs in the image and returns a list of blob objects. For more information about the `image.blob` object, please refer to the relevant documentation.

The `thresholds` parameter must be a list of tuples in the form `[(lo, hi), (lo, hi), ...]`, used to define the color ranges to track. For grayscale images, each tuple should contain two values: minimum grayscale value and maximum grayscale value. The function will only consider pixel regions falling within these thresholds. For RGB565 images, each tuple should contain six values `(l_lo, l_hi, a_lo, a_hi, b_lo, b_hi)`, corresponding to the minimum and maximum values of the L, A, and B channels in LAB color space, respectively. The function automatically corrects for swapped minimum and maximum values. If a tuple contains more than six values, the extra values are ignored; if a tuple has fewer, the missing thresholds are assumed to be the maximum range.

**Notes:**

To get the threshold for the target object, simply select (click and drag) the object to track in the IDE frame buffer, and the histogram will update in real time. Then, record the start and end positions of the color distribution in each histogram channel; these values will be used as the low and high values for `thresholds`. It is recommended to manually determine the thresholds to avoid minor differences in the upper and lower quartiles.

You can also go to OpenMV IDE's "Tools" -> "Machine Vision" -> "Threshold Editor" and use the GUI interface to drag the sliders to determine color thresholds.

- The `invert` parameter is used to invert the threshold operation, so that only pixels outside the known color ranges are matched.
- The `roi` parameter is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the rectangle of the entire image. Operations are limited to pixels within this region.
- `x_stride` is the number of x pixels to skip when finding blobs. After a blob is found, the line-filling algorithm will precisely process that region. If you know the blobs are large, you can increase `x_stride` to improve the search speed.
- `y_stride` is the number of y pixels to skip when finding blobs. After a blob is found, the line-filling algorithm will precisely process that region. If you know the blobs are large, you can increase `y_stride` to improve the search speed.
- `area_threshold` is used to filter out blobs whose bounding box area is less than this value.
- `pixels_threshold` is used to filter out blobs whose pixel count is less than this value.
- If `merge` is `True`, all unfiltered blobs whose bounding rectangles overlap with each other are merged. `margin` can be used to increase or decrease the size of the blob bounding rectangles in the merge test. For example, two overlapping blobs with a margin of 1 will be merged.
  
Merged blobs enable color code tracking. Each blob object has a `code` value, which is a bit vector. For example, if two color thresholds are entered in `image.find_blobs`, the code for the first threshold is 1, and the second is 2 (the third code is 4, the fourth is 8, and so on). When blobs are merged, all `code` values are combined with a logical OR to indicate the colors that produced them. This makes it possible to track two colors simultaneously; if two colors yield the same blob object, it may correspond to a certain color code.

When using strict color ranges, it may not be possible to fully track all pixels of the target object, in which case blob merging can be considered. If you want to merge blobs but do not want blobs from different thresholds to be merged, you can call `image.find_blobs` twice separately.

- `threshold_cb` can be set as a callback function called after each blob has been threshold-filtered, to filter out specific blobs from the list of blobs about to be merged. The callback function will receive one argument: the blob object to be filtered. If you want to keep the blob, the callback function should return `True`; otherwise, return `False`.
- `merge_cb` can be set as a callback function called between two blobs about to be merged, to control the approval or prohibition of merging. The callback function will receive two arguments, i.e., the two blob objects to be merged. If you want to merge the blobs, return `True`; otherwise, return `False`.

**Note**: This function does not support compressed images and Bayer images.

### `find_lines`

```python
image.find_lines([roi[, x_stride=2[, y_stride=1[, threshold=1000[, theta_margin=25[, rho_margin=25]]]]]])
```

This function uses the Hough transform to find all straight lines in the image and returns a list of `image.line` objects.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the rectangle of the entire image. Operations are limited to pixels within this region.
- `x_stride` is the number of x pixels to skip during the Hough transform. If you know the lines are long, you can increase `x_stride`.
- `y_stride` is the number of y pixels to skip during the Hough transform. If you know the lines are long, you can increase `y_stride`.
- `threshold` controls the lines detected from the Hough transform. Only lines greater than or equal to this threshold are returned. The appropriate threshold depends on the image content. Note that the magnitude of a line is the sum of the magnitudes of all Sobel-filtered pixels that make up the line.
- `theta_margin` controls the merging of detected lines; lines with angles within the `theta_margin` range are merged.
- `rho_margin` also controls the merging of detected lines; lines with rho values within the `rho_margin` range are merged.

The method applies a Sobel filter to the image and uses its magnitude and gradient response to perform the Hough transform. No image preprocessing is required, although image cleanup and filtering will produce more stable results.

**Note**: This function does not support compressed images and Bayer images.

### `find_line_segments`

```python
image.find_line_segments([roi[, merge_distance=0[, max_theta_difference=15]]])
```

This function uses the Hough transform to find line segments in the image and returns a list of `image.line` objects.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the rectangle of the entire image. Operations are limited to pixels within this region.
- `merge_distance` specifies the maximum pixel distance between two line segments; if less than this value, they are merged into one line segment.
- `max_theta_difference` is the maximum angle difference between two line segments to be merged.

This method uses the LSD library (also used by OpenCV) to find line segments in the image. Although it is slower, it is highly accurate, and the line segments do not exhibit jumping.

**Note**: This function does not support compressed images and Bayer images.

### `find_circles`

```python
image.find_circles([roi[, x_stride=2[, y_stride=1[, threshold=2000[, x_margin=10[, y_margin=10[, r_margin=10]]]]]]])
```

This function uses the Hough transform to find circles in the image and returns a list of `image.circle` objects.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the rectangle of the entire image. Operations are limited to pixels within this region.
- `x_stride` is the number of x pixels to skip during the Hough transform. If you know the circles are large, you can increase `x_stride`.
- `y_stride` is the number of y pixels to skip during the Hough transform. If you know the circles are large, you can increase `y_stride`.
- `threshold` controls the size of detected circles; only circles greater than or equal to this threshold are returned. The appropriate threshold depends on the image content. Note that the magnitude of a circle is the sum of the magnitudes of all Sobel-filtered pixels that make up the circle.

- `x_margin` is the maximum pixel deviation allowed when merging on the x coordinate.
- `y_margin` is the maximum pixel deviation allowed when merging on the y coordinate.
- `r_margin` is the maximum pixel deviation allowed when merging on the radius.

The method applies a Sobel filter to the image and uses its magnitude and gradient response to perform the Hough transform. No image preprocessing is required, although image cleanup and filtering will produce more stable results.

**Note**: This function does not support compressed images and Bayer images.

### `find_rects`

```python
image.find_rects([roi=Auto, threshold=10000])
```

This function uses the same quadrilateral detection algorithm as AprilTag to find rectangles in the image. The algorithm works best with rectangles that form a sharp contrast with the background. The AprilTag quadrilateral detection can handle rectangles with arbitrary scaling, rotation, and shearing, and returns a list of `image.rect` objects.

- `roi` is a rectangle tuple `(x, y, w, h)` for specifying the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

In the returned list of rectangles, rectangles whose boundary size (obtained by sliding a Sobel operator over all pixels on the rectangle's edges and accumulating their values) is less than `threshold` will be filtered out. The appropriate `threshold` value depends on the specific application scenario.

**Note**: Compressed images and Bayer images are not supported.

### `find_qrcodes`

```python
image.find_qrcodes([roi])
```

This function finds all QR codes within the specified ROI and returns a list of `image.qrcode` objects. For more information, please refer to the relevant documentation for the `image.qrcode` object.

For this method to work successfully, the QR codes on the image should be as flat as possible. You can zoom in on the center of the lens by using the `sensor.set_windowing` function, use the `image.lens_corr` function to eliminate barrel distortion from the lens, or replace the lens with a narrower field of view lens to obtain flat QR codes unaffected by lens distortion. Some machine vision lenses do not produce barrel distortion, but they cost more than the standard lenses provided by OpenMV; these lenses are distortion-free lenses.

- `roi` is a rectangle tuple `(x, y, w, h)` for specifying the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note**: Compressed images and Bayer images are not supported.

### `find_apriltags`

```python
image.find_apriltags([roi[, families=image.TAG36H11[, fx[, fy[, cx[, cy]]]]]])
```

This function finds all AprilTags within the specified ROI and returns a list of `image.apriltag` objects. For more information, please refer to the relevant documentation for the `image.apriltag` object.

Compared to QR codes, AprilTags can be effectively detected at longer distances, in poor lighting conditions, and in more distorted image environments. AprilTags can handle various image distortion issues, while QR codes cannot. Therefore, AprilTags only encode a numeric ID as their payload.

In addition, AprilTags can also be used for localization. Each `image.apriltag` object will return its 3D position information and rotation angle. The position information is determined by `fx`, `fy`, `cx`, and `cy`, representing the focal length and center point of the image in the X and Y directions, respectively.

> You can use the tag generator tool built into the OpenMV IDE to create AprilTags. This tool can generate printable AprilTags in 8.5"x11" format.

- `roi` is a rectangle tuple `(x, y, w, h)` for specifying the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

- `families` is a bitmask of the tag families to decode, expressed as a logical OR:
  - `image.TAG16H5`
  - `image.TAG25H7`
  - `image.TAG25H9`
  - `image.TAG36H10`
  - `image.TAG36H11`
  - `image.ARTOOLKIT`

The default is set to the most commonly used `image.TAG36H11` tag family. Note that enabling each tag family will slightly reduce the speed of `find_apriltags`.

- `fx` is the focal length of the camera in the X direction in pixels. The value for a standard OpenMV Cam is \((2.8 / 3.984) \times 656\), which is calculated by dividing the focal length in millimeters by the length of the sensor in the X direction, then multiplying by the number of pixels of the sensor in the X direction (for the OV7725 sensor).

- `fy` is the focal length of the camera in the Y direction in pixels. The value for a standard OpenMV Cam is \((2.8 / 2.952) \times 488\), which is calculated by dividing the focal length in millimeters by the length of the sensor in the Y direction, then multiplying by the number of pixels of the sensor in the Y direction (for the OV7725 sensor).

- `cx` is the center of the image, i.e., `image.width()/2`, not `roi.w()/2`.

- `cy` is the center of the image, i.e., `image.height()/2`, not `roi.h()/2`.

**Note**: Compressed images and Bayer images are not supported.

### `find_datamatrices`

```python
image.find_datamatrices([roi[, effort=200]])
```

This function finds all data matrices within the specified ROI and returns a list of `image.datamatrix` objects. For more information, please refer to the relevant documentation for the `image.datamatrix` object.

For this method to work successfully, the rectangular codes on the image should be as flat as possible. You can zoom in on the center of the lens by using the `sensor.set_windowing` function, use the `image.lens_corr` function to eliminate barrel distortion from the lens, or replace the lens with a narrower field of view lens to obtain flat rectangular codes unaffected by lens distortion. Some machine vision lenses do not produce barrel distortion, but they cost more than the standard lenses provided by OpenMV; these lenses are distortion-free lenses.

- `roi` is a rectangle tuple `(x, y, w, h)` for specifying the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

- `effort` controls the computation time required to find a rectangular code match. The default value is 200, suitable for all use cases. However, you can increase the frame rate at the cost of detection rate, or increase the detection rate at the cost of frame rate. Note that when `effort` is set below approximately 160, no detection can be performed; conversely, you can set it to any higher value, but if it is set above 240, the detection rate will not improve further.

**Note**: Compressed images and Bayer images are not supported.

### `find_barcodes`

```python
image.find_barcodes([roi])
```

This function finds all 1D barcodes within the specified ROI and returns a list of `image.barcode` objects. For more information, please refer to the relevant documentation for the `image.barcode` object.

For best results, it is recommended to use a window that is 640 pixels long and 40/80/160 pixels wide. The less vertical the window is, the faster it runs. Since barcodes are linear 1D images, they require high resolution in one direction and can have lower resolution in the other. Note that this function performs both horizontal and vertical scanning, so you can use a window that is 40/80/160 pixels wide and 480 pixels long. Be sure to adjust the lens so that the barcode is in the area of clearest focus. Blurry barcodes cannot be decoded.

This function supports all of the following 1D barcodes:

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

- `roi` is a rectangle tuple `(x, y, w, h)` for specifying the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note**: Compressed images and Bayer images are not supported.

### `find_displacement`

```python
image.find_displacement(template[, roi[, template_roi[, logpolar=False]]])
```

This function finds the transformation offset of the image based on a template. This method can be used to implement optical flow analysis. The return result is an `image.displacement`

 object, containing the displacement calculation result based on phase correlation.

- `roi` is the rectangular region `(x, y, w, h)` to be processed. If unspecified, it defaults to the entire image.

- `template_roi` is the template region `(x, y, w, h)` to be processed. If unspecified, it defaults to the entire image.

`roi` and `template_roi` must have the same width and height, but the `x` and `y` coordinates can be at any position in the image. You can slide a smaller ROI over a larger image to obtain an optical flow gradient image.

`image.find_displacement` is typically used to compute X/Y translation between two images. However, if `logpolar=True` is set, changes in rotation and scale will also be found. The same `image.displacement` object can provide both results.

**Note**: Compressed images and Bayer images are not supported.

**Note**: Please use this method on images with consistent aspect ratios (e.g., `sensor.B64X64`).

### `find_number`

```python
image.find_number(roi)
```

This function uses the LENET-6 Convolutional Neural Network (CNN) trained on the MINST dataset to detect numbers in any 28x28 ROI in the image. Returns a tuple containing the detected number (0-9) and the corresponding confidence (0-1).

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note**: This method only supports grayscale images and is experimental. If any CNN trained based on Caffe on a PC is run in the future, this method may be removed. The latest version (3.0.0) firmware has removed this function.

### `classify_object`

```python
image.classify_object(roi)
```

This function uses the CIFAR-10 Convolutional Neural Network (CNN) to classify objects in a region of interest (ROI) in the image, capable of recognizing categories such as airplanes, cars, birds, cats, deer, dogs, frogs, horses, ships, and trucks. The method internally automatically scales the input image to 32x32 pixels for CNN processing.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note**: This method only supports images in RGB565 format.

**Note**: This method is experimental and may be removed in the future if a CNN trained based on Caffe on a PC is implemented.

### `find_template`

```python
image.find_template(template, threshold[, roi[, step=2[, search=image.SEARCH_EX]]])
```

This function uses the Normalized Cross-Correlation (NCC) algorithm to find the first position in the image that matches the template, and returns the bounding box tuple `(x, y, w, h)` of the matching position; if no match is found, returns `None`.

- `template` is a small image object that needs to match the target image object. Note that both images should be grayscale images.

- `threshold` is a float (range 0.0 to 1.0). Smaller values can increase the detection rate but may increase the false positive rate; conversely, higher values will decrease the detection rate and reduce the false positive rate.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

- `step` refers to the number of pixels to skip when looking for the template. Skipping pixels can significantly increase the algorithm's running speed. This parameter applies to the algorithm in `SEARCH_EX` mode.

- `search` can be `image.SEARCH_DS` or `image.SEARCH_EX`. The algorithm used by `image.SEARCH_DS` to search for templates is faster than `image.SEARCH_EX`, but it may not successfully search when the template is at the edge of the image. `image.SEARCH_EX` can perform a more thorough search of the image, but its running speed is lower than `image.SEARCH_DS`.

**Note**: This method only supports grayscale images.

### `find_features`

```python
image.find_features(cascade[, threshold=0.5[, scale=1.5[, roi]]])
```

This method searches the image for all regions that match the Haar Cascade model and returns a list of bounding box rectangle tuples `(x, y, w, h)` of these features. If no features are found, returns an empty list.

- `cascade` is a Haar Cascade object. For details, please refer to `image.HaarCascade()`.

- `threshold` is a float (range 0.0 to 1.0). Smaller values can increase the detection rate but may increase the false positive rate; conversely, higher values will decrease the detection rate and reduce the false positive rate.

- `scale` is a float greater than 1.0. A higher scale factor runs faster, but the image matching effect is relatively worse. The ideal value is between 1.35 and 1.5.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note**: This method only supports grayscale images.

### `find_eye`

```python
image.find_eye(roi)
```

This function finds the pupil within the specified region of interest `(x, y, w, h)` and returns the position tuple `(x, y)` of the pupil in the image. If no pupil is found, returns `(0, 0)`.

Before using this function, you need to first search for a face using `image.find_features()` and the Haar operator `frontalface`, then search for eyes on the face using `image.find_features()` and the Haar operator `find_eye`. Finally, call this method on each eye ROI returned by `image.find_features()` to get the coordinates of the pupil.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note**: This method only supports grayscale images.

### `find_lbp`

```python
image.find_lbp(roi)
```

This function extracts Local Binary Pattern (LBP) keypoints from the specified ROI tuple `(x, y, w, h)`. You can use the `image.match_descriptor` function to compare two sets of keypoints to obtain the matching distance.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note**: This method only supports grayscale images.

### `find_keypoints`

```python
image.find_keypoints([roi[, threshold=20[, normalized=False[, scale_factor=1.5[, max_keypoints=100[, corner_detector=image.CORNER_AGAST]]]]]])
```

This function extracts ORB keypoints from the specified ROI tuple `(x, y, w, h)`. You can use the `image.match_descriptor` function to compare two sets of keypoints to obtain matching regions. If no keypoints are found, returns `None`.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

- `threshold` controls the number of keypoints extracted (range 0-255). For the default AGAST corner detector, this value should be set to about 20; for the FAST corner detector, this value should be set to about 60 to 80. The lower the threshold, the more corners are extracted.

- `normalized` is a boolean. If `True`, keypoint extraction is turned off at multi-resolution. If you do not care about handling scaling issues and want the algorithm to run faster, set it to `True`.

- `scale_factor` is a float greater than 1.0. A higher scale factor runs faster, but the image matching effect is relatively worse. The ideal value is between 1.35 and 1.5.

- `max_keypoints` is the maximum number of keypoints that the keypoint object can hold. If the keypoint object is too large causing memory issues, please reduce this value appropriately.

- `corner_detector` is the corner detector algorithm used to extract keypoints. Optional values are `image.CORNER_FAST` or `image.CORNER_AGAST`. The FAST corner detector is faster but less accurate.

**Note**: This method only supports grayscale images.

### `find_edges`

```python
image.find_edges(edge_type[, threshold])
```

This function converts the image to a black-and-white image, retaining only the edges as white pixels.

- `edge_type` optional values include:
  - `image.EDGE_SIMPLE` - Simple threshold high-pass filtering algorithm
  - `image.EDGE_CANNY` - Canny edge detection algorithm

- `threshold` is a two-tuple containing the low threshold and high threshold. You can control the edge quality by adjusting this value, with the default set to `(100, 200)`.

**Note**: This method only supports grayscale images.

### `find_hog`

```python
image.find_hog([roi[, size=8]])
```

This function uses the HOG (Histogram of Oriented Gradients) algorithm to replace pixels in the ROI.

- `roi` is a rectangle tuple `(x, y, w, h)` for the region of interest. If unspecified, the ROI defaults to the entire image. Operations are limited to pixels within this region.

**Note**: This method only supports grayscale images.

### `draw_ellipse-2`

```python
image.draw_ellipse(cx, cy, rx, ry, color, thickness=1)
```

The `draw_ellipse` function is used to draw an ellipse on the image.

- `cx, cy`: The coordinates of the ellipse's center.
- `rx, ry`: The radii of the ellipse along the x and y axes

directions.

- `color`: The color of the ellipse.
- `thickness`: The thickness of the ellipse's border (defaulting to 1).

The function returns the image object, allowing you to use the `.` notation to call other methods.

**Note**: This method does not support compressed images and Bayer images.

**OpenMV Native API** is ported from `openmv` with consistent functionality. Users can refer to the native documentation for more API details.

## image Module Functions

### `rgb_to_lab`

Converts RGB888 to LAB color space.

```python
image.rgb_to_lab(rgb_tuple)
```

### `lab_to_rgb`

Converts LAB color space to RGB888.

```python
image.lab_to_rgb(lab_tuple)
```

### `rgb_to_grayscale`

Converts RGB888 to grayscale value.

```python
image.rgb_to_grayscale(rgb_tuple)
```

### `grayscale_to_rgb`

Converts grayscale value to RGB888.

```python
image.grayscale_to_rgb(g_value)
```

### `load_descriptor`

Loads a descriptor object from a file.

```python
image.load_descriptor(path)
```

### `save_descriptor`

Saves a descriptor object to a file.

```python
image.save_descriptor(path, descriptor)
```

### `match_descriptor`

Compares two descriptor objects and returns the match result.

```python
image.match_descriptor(descriptor0, descriptor1, threshold=70, filter_outliers=False)
```

## Class `HaarCascade`

The `HaarCascade` feature descriptor is used by the `image.find_features()` method and does not provide directly callable methods.

### Constructor

```python
class image.HaarCascade(path[, stages=Auto])
```

This constructor loads a Haar Cascade from a Haar Cascade binary file (in a format suitable for OpenMV Cam). If you pass the string "frontalface" instead of a path, the constructor will load the built-in frontalface Haar Cascade. Similarly, you can load the corresponding Haar Cascade by passing "eye". This method returns the loaded Haar Cascade object for subsequent use with `image.find_features()`.

The default value of `stages` is the number of stages in the Haar Cascade, but you can specify a lower value to speed up the feature detector, although this may increase the false positive rate.

> You can create custom Haar Cascades suitable for OpenMV Cam. First, Google "Haar Cascade" to find out if someone has already made an OpenCV Haar Cascade for the object you want to detect. If not, you may need to make one yourself (which is a significant workload). For information on how to create a custom Haar Cascade, please refer to relevant materials; for information on how to convert OpenCV Haar Cascades into a format readable by OpenMV Cam, please refer to the corresponding script.

**Q: What is a Haar Cascade?**

**A:** A Haar Cascade is a series of contrast checks used to determine whether an object exists in an image. These contrast checks are divided into multiple stages, with the execution of later stages depending on the results of earlier stages. Although the contrast checks themselves are not complex—for example, checking whether the brightness in the center of an image is lower than the brightness at the edges—they are efficient feature detection tools. The initial stages perform broad checks, while subsequent stages focus on smaller regions.

**Q: How are Haar Cascades made?**

**A:** Haar Cascades are trained by an algorithm using images labeled with positive and negative examples. For example, hundreds of images containing cats (labeled as positive examples) and hundreds of images not containing cats (labeled as negative examples) are used to train the algorithm. The resulting model is the Haar Cascade used to detect cats.

## Class `Similarity`

The similarity object is returned by the `image.get_similarity` function.

### Constructor

```python
class image.similarity
```

Please create this object by calling the `image.get_similarity()` function.

### `mean`

```python
similarity.mean()
```

This function returns the mean of the 8x8 pixel block structural similarity difference, ranging from [-1, +1], where -1 indicates completely different and +1 indicates exactly the same. You can also obtain this value directly through index [0].

### `stdev`

```python
similarity.stdev()
```

This function returns the standard deviation of the 8x8 pixel block structural similarity difference. You can also obtain this value through index [1].

### `min`

```python
similarity.min()
```

This function returns the minimum of the 8x8 pixel block structural similarity difference, ranging from [-1, +1], where -1 indicates completely different and +1 indicates exactly the same. You can also obtain this value through index [2].

> By looking at this value, you can quickly determine whether there is a significant difference in any 8x8 pixel block between the two images, that is, the value is much lower than +1.

### `max`

```python
similarity.max()
```

This function returns the maximum of the 8x8 pixel block structural similarity difference, ranging from [-1, +1], where -1 indicates completely different and +1 indicates exactly the same. You can also obtain this value through index [3].

> By looking at this value, you can quickly determine whether any 8x8 pixel block between the two images is exactly the same, that is, the value is much greater than -1.

## Class `Histogram`

A histogram object is returned by the `image.get_histogram` method. A grayscale histogram has multiple normalized binary channels that sum to 1. An RGB565 histogram has three binary channels, also normalized to sum to 1.

### Constructor

```python
class image.histogram
```

Please create this object by calling the `image.get_histogram()` function.

### `bins`

```python
histogram.bins()
```

Returns the float list of the grayscale histogram. You can also access this value via the index [0].

### `l_bins`

```python
histogram.l_bins()
```

Returns the float list of the L channel of LAB in the RGB565 histogram. You can access this value via the index [0].

### `a_bins`

```python
histogram.a_bins()
```

Returns the float list of the A channel of LAB in the RGB565 histogram. You can access this value via the index [1].

### `b_bins`

```python
histogram.b_bins()
```

Returns the float list of the B channel of LAB in the RGB565 histogram. You can access this value via the index [2].

### `get_percentile`

```python
histogram.get_percentile(percentile)
```

Computes the cumulative distribution function (CDF) of the histogram channels and returns the histogram value at the specified percentile (0.0 - 1.0).

For example, if you pass in 0.1, the method will indicate which binary value caused the accumulator to exceed 0.1 during the accumulation process. In the absence of anomalous utility interference with adaptive color tracking results, this method is particularly effective for determining the minimum (0.1) and maximum (0.9) values of the color distribution.

### `get_threshold`

```python
histogram.get_threshold()
```

Uses the Otsu method to compute the optimal threshold, dividing each channel of the histogram in two. This method returns an `image.threshold` object, which is particularly suitable for determining the optimal `image.binary()` threshold.

### `get_statistics`

```python
histogram.get_statistics()
```

Calculates the mean, median, mode, standard deviation, minimum, maximum, lower quartile, and upper quartile of each color channel in the histogram, and returns a `statistics` object. You can also use `histogram.statistics()` and `histogram.get_stats()` as aliases for this method.

## Class `Percentile`

The percentile value object is returned by the `histogram.get_percentile` method. The grayscale percentile value contains one channel and does not use the `l_*`, `a_*`, or `b_*` methods. The percentile value in RGB565 format contains three channels and requires the `l_*`, `a_*`, and `b_*` methods.

### Constructor

```python
class image.percentile
```

Please create this object by calling the `histogram.get_percentile()` function.

### `value`

```python
percentile.value()
```

Returns the grayscale percentile value (range 0-255).

You can also access this value via index [0].

### `l_value`

```python
percentile.l_value()
```

Returns the percentile value of the L channel of LAB in RGB565 format (range 0-100).

You can also access this value via index [0].

### `a_value`

```python
percentile.a_value()
```

Returns the percentile value of the A channel of LAB in RGB565 format (range -128 to 127).

You can also access this value via index [1].

### `b_value`

```python
percentile.b_value()
```

Returns the percentile value of the B channel of LAB in RGB565 format (range -128 to 127).

You can also access this value via index [2].

## Class `Threshold`

The threshold object is returned by the `histogram.get_threshold` method.

Grayscale images contain one channel and do not include `l_*`, `a_*`, and `b_*` methods.

The threshold in RGB565 format contains three channels and requires the use of `l_*`, `a_*`, and `b_*` methods.

### Constructor

```python
class image.threshold
```

Please create this object by calling the `histogram.get_threshold()` function.

### `value`

```python
threshold.value()
```

Returns the threshold of the grayscale image (range between 0 and 255).

You can also obtain this value via the index [0].

### `l_value`

```python
threshold.l_value()
```

Returns the threshold of the L channel in LAB in RGB565 format (range between 0 and 100).

You can also obtain this value via the index [0].

### `a_value`

```python
threshold.a_value()
```

Returns the threshold of the A channel in LAB in RGB565 format (range between -128 and 127).

You can also obtain this value via the index [1].

### `b_value`

```python
threshold.b_value()
```

Returns the threshold of the B channel in LAB in RGB565 format (range between -128 and 127).

You can also obtain this value via the index [2].

## Class `Statistics`

The statistics data object is returned by the `histogram.get_statistics` or `image.get_statistics` method.

Grayscale statistics contain one channel and do not use the `l_*`, `a_*`, or `b_*` methods.

RGB565 format statistics contain three channels and require the use of `l_*`, `a_*`, and `b_*` methods.

### Constructor

```python
class image.statistics
```

Please create this object by calling the `histogram.get_statistics()` or `image.get_statistics()` function.

#### `mean`

```python
statistics.mean()
```

Returns the grayscale mean value (range 0-255, type int).

You can also obtain this value through index [0].

### `median`

```python
statistics.median()
```

Returns the grayscale median (range 0-255, type int).

You can also get this value through index [1].

### `mode`

```python
statistics.mode()
```

Returns the grayscale mode (range 0-255, type int).

You can also get this value through index [2].

### `stdev`

```python
statistics.stdev()
```

Returns the grayscale standard deviation (range 0-255, type int).

You can also get this value through index [3].

### `min`

```python
statistics.min()
```

Returns the grayscale minimum (range 0-255, type int).

You can also get this value through index [4].

### `max`

```python
statistics.max()
```

Returns the grayscale maximum (range 0-255, type int).

You can also get this value through index [5].

### `lq`

```python
statistics.lq()
```

Returns the grayscale lower quartile (range 0-255, type int).

You can also get this value through index [6].

### `uq`

```python
statistics.uq()
```

Returns the grayscale upper quartile (range 0-255, type int).

You can also get this value through index [7].

### `l_mean`

```python
statistics.l_mean()
```

Returns the mean of the L channel of LAB in RGB565 format (range 0-255, type int).

You can also get this value through index [0].

### `l_median`

```python
statistics.l_median()
```

Returns the median of the L channel of LAB in RGB565 format (range 0-255, type int).

You can also get this value through index [1].

### `l_mode`

```python
statistics.l_mode()
```

Returns the mode of the L channel of LAB in RGB565 format (range 0-255, type int).

You can also get this value through index [2].

### `l_stdev`

```python
statistics.l_stdev()
```

Returns the standard deviation of the L channel of LAB in RGB565 format (range 0-255, type int).

You can also get this value through index [3].

### `l_min`

```python
statistics.l_min()
```

Returns the minimum of the L channel of LAB in RGB565 format (range 0-255, type int).

You can also get this value through index [4].

### `l_max`

```python
statistics.l_max()
```

Returns the maximum of the L channel of LAB in RGB565 format (range 0-255, type int).

You can also get this value through index [5].

### `l_lq`

```python
statistics.l_lq()
```

Returns the lower quartile of the L channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [6].

### `l_uq`

```python
statistics.l_uq()
```

Returns the upper quartile of the L channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [7].

### `a_mean`

```python
statistics.a_mean()
```

Returns the mean of the A channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [8].

### `a_median`

```python
statistics.a_median()
```

Returns the median of the A channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [9].

### `a_mode`

```python
statistics.a_mode()
```

Returns the mode of the A channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [10].

### `a_stdev`

```python
statistics.a_stdev()
```

Returns the standard deviation of the A channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [11].

### `a_min`

```python
statistics.a_min()
```

Returns the minimum of the A channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [12].

### `a_max`

```python
statistics.a_max()
```

Returns the maximum of the A channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [13].

### `a_lq`

```python
statistics.a_lq()
```

Returns the lower quartile of the A channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [14].

### `a_uq`

```python
statistics.a_uq()
```

Returns the upper quartile of the A channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [15].

### `b_mean`

```python
statistics.b_mean()
```

Returns the mean of the B channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [16].

### `b_median`

```python
statistics.b_median()
```

Returns the median of the B channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [17].

### `b_mode`

```python
statistics.b_mode()
```

Returns the mode of the B channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [18].

### `b_stdev`

```python
statistics.b_stdev()
```

Returns the standard deviation of the B channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [19].

### `b_min`

```python
statistics.b_min()
```

Returns the minimum of the B channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [20].

### `b_max`

```python
statistics.b_max()
```

Returns the maximum of the B channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [21].

### `b_lq`

```python
statistics.b_lq()
```

Returns the lower quartile of the B channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [22].

### `b_uq`

```python
statistics.b_uq()
```

Returns the upper quartile of the B channel of LAB in RGB565 format, with a value range of 0 to 255 (type int). You can also get this value through index [23].

## Class `Blob`

The blob object is returned by `image.find_blobs`.

### Constructor

```python
class image.blob
```

Please create this object by calling the `image.find_blobs()` function.

### `rect`

```python
blob.rect()
```

Returns a rectangle tuple (x, y, w, h) for use in other image processing methods such as `image.draw_rectangle` to draw the bounding box of the blob on the image.

### `x`

```python
blob.x()
```

Returns the x coordinate of the blob's bounding box (type: int). You can also get this value via index [0].

### `y`

```python
blob.y()
```

Returns the y coordinate of the blob's bounding box (type: int). You can also get this value via index [1].

### `w`

```python
blob.w()
```

Returns the width of the blob's bounding box (type: int). You can also get this value via index [2].

### `h`

```python
blob.h()
```

Returns the height of the blob's bounding box (type: int). You can also get this value via index [3].

### `pixels`

```python
blob.pixels()
```

Returns the number of pixels that belong to the blob (type: int). You can also get this value via index [4].

### `cx`

```python
blob.cx()
```

Returns the x coordinate of the blob's center (type: int). You can also get this value via index [5].

### `cy`

```python
blob.cy()
```

Returns the y coordinate of the blob's center (type: int). You can also get this value via index [6].

### `rotation`

```python
blob.rotation()
```

Returns the rotation angle of the blob (unit: radians). For blobs resembling a pencil or pen, this value ranges from 0 to 180. If the blob is circular, this value is invalid; if the blob has perfect asymmetry, the rotation angle ranges from 0 to 360 degrees. You can also get this value via index [7].

### `code`

```python
blob.code()
```

Returns a 16-bit binary number in which each bit corresponds to a color threshold, representing the attributes of the blob. For example, if three color thresholds are looked up via `image.find_blobs`, then this blob may have bits 0, 1, or 2 set. Note that unless `merge=True` is set when calling `image.find_blobs`, each blob will only have one bit set. Thus, multiple blobs of different color thresholds can be merged together. You can also use this method in conjunction with multiple thresholds to implement color code tracking. You can also get this value via index [8].

### `count`

```python
blob.count()
```

Returns the number of blobs merged into this blob. This number will only be greater than 1 if `merge=True` is set when calling `image.find_blobs`. You can also get this value via index [9].

### `area`

```python
blob.area()
```

Returns the area of the bounding box around the blob (calculated as w * h).

### `density`

```python
blob.density()
```

Returns the density ratio of the blob, representing the number of pixels within the blob's bounding box area. Generally, a lower density ratio indicates that the object is not locked onto well.

## Class `Line`

Line objects are returned by `image.find_lines`, `image.find_line_segments`, or `image.get_regression` methods.

### Constructor

```python
class image.line
```

Please create this object by calling the `image.find_lines()`, `image.find_line_segments()`, or `image.get_regression()` functions.

### `line`

```python
line.line()
```

Returns a line tuple (x1, y1, x2, y2), used by other image processing methods such as `image.draw_line` for image drawing.

### `x1`

```python
line.x1()
```

Returns the x-coordinate component of the first vertex (p1) of the line. You can also obtain this value through index [0].

### `y1`

```python
line.y1()
```

Returns the y-coordinate component of the first vertex (p1) of the line. You can also obtain this value through index [1].

### `x2`

```python
line.x2()
```

Returns the x-coordinate component of the second vertex (p2) of the line. You can also obtain this value through index [2].

### `y2`

```python
line.y2()
```

Returns the y-coordinate component of the second vertex (p2) of the line. You can also obtain this value through index [3].

### `length`

```python
line.length()
```

Returns the length of the line, calculated as \(\sqrt{((x2-x1)^2) + ((y2-y1)^2)}\). You can also obtain this value through index [4].

### `magnitude`

```python
line.magnitude()
```

Returns the length of the line after the Hough transform. You can also obtain this value through index [5].

### `theta`

```python
line.theta()
```

Returns the angle of the line after the Hough transform (range: 0–179 degrees). You can also obtain this value through index [7].

### `rho`

```python
line.rho()
```

Returns the ρ value of the line after the Hough transform. You can also obtain this value through index [8].

## Class `Circle`

Circle objects are returned by the `image.find_circles` method.

### Constructor

```python
class image.circle
```

Please create this object by calling the `image.find_circles()` function.

### `x`

```python
circle.x()
```

Returns the x-coordinate of the circle's center. You can also get this value through index [0].

### `y`

```python
circle.y()
```

Returns the y-coordinate of the circle's center. You can also get this value through index [1].

### `r`

```python
circle.r()
```

Returns the radius of the circle. You can also get this value through index [2].

### `magnitude`

```python
circle.magnitude()
```

Returns the magnitude of the circle. You can also get this value through index [3].

## Class `Rect`

The rectangle object is returned by the `image.find_rects` function.

### Constructor

```python
class image.rect
```

Please use the `image.find_rects()` function to create this object.

### `corners`

```python
rect.corners()
```

This method returns a list of tuples containing the four corners of the rectangle object, with each tuple in the format (x, y). The four corners are typically arranged starting from the lower-left corner and proceeding counterclockwise.

### `rect`

```python
rect.rect()
```

This method returns a rectangle tuple (x, y, w, h) that can be used in other image processing methods, such as the bounding box in `image.draw_rectangle`.

### `x`

```python
rect.x()
```

This method returns the x-coordinate of the upper-left corner of the rectangle. You can also access this value via the index [0].

### `y`

```python
rect.y()
```

This method returns the y-coordinate of the upper-left corner of the rectangle. You can also access this value via the index [1].

### `w`

```python
rect.w()
```

This method returns the width of the rectangle. You can also access this value via the index [2].

### `h`

```python
rect.h()
```

This method returns the height of the rectangle. You can also access this value via the index [3].

### `magnitude`

```python
rect.magnitude()
```

This method returns the magnitude of the rectangle. You can also access this value via the index [4].

## Class `QRCode`

The QRCode object is returned by the `image.find_qrcodes` function.

### Constructor

```python
class image.qrcode
```

Please use the `image.find_qrcodes()` function to create this object.

### `corners`

```python
qrcode.corners()
```

This method returns a list of tuples containing the four corners of the QR code, with each tuple in the format (x, y). The four corners are typically ordered starting from the top-left corner and proceeding clockwise.

### `rect`

```python
qrcode.rect()
```

This method returns a rectangle tuple (x, y, w, h) that can be used in other image processing methods, such as the QR code bounding box in `image.draw_rectangle`.

### `x`

```python
qrcode.x()
```

This method returns the x-coordinate of the QR code bounding box (int). You can also obtain this value through index [0].

### `y`

```python
qrcode.y()
```

This method returns the y-coordinate of the QR code bounding box (int). You can also obtain this value through index [1].

### `w`

```python
qrcode.w()
```

This method returns the width of the QR code bounding box (int). You can also obtain this value through index [2].

### `h`

```python
qrcode.h()
```

This method returns the height of the QR code bounding box (int). You can also obtain this value through index [3].

### `payload`

```python
qrcode.payload()
```

This method returns the payload string of the QR code, such as a URL. You can also obtain this value through index [4].

### `version`

```python
qrcode.version()
```

This method returns the version number of the QR code (int). You can also obtain this value through index [5].

### `ecc_level`

```python
qrcode.ecc_level()
```

This method returns the error correction level of the QR code (int). You can also obtain this value through index [6].

### `mask`

```python
qrcode.mask()
```

This method returns the mask of the QR code (int). You can also obtain this value through index [7].

### `data_type`

```python
qrcode.data_type()
```

This method returns the data type of the QR code. You can also obtain this value through index [8].

### `eci`

```python
qrcode.eci()
```

This method returns the ECI (Extended Channel Interpretation) of the QR code, which is used to store the encoding of data bytes in the QR code. When processing QR codes containing non-standard ASCII text, check this value. You can also obtain this value through index [9].

### `is_numeric`

```python
qrcode.is_numeric()
```

Returns True if the data type of the QR code is numeric format.

### `is_alphanumeric`

```python
qrcode.is_alphanumeric()
```

Returns True if the data type of the QR code is alphanumeric format.

### `is_binary`

```python
qrcode.is_binary()
```

Returns True if the data type of the QR code is binary format. To accurately process all types of text, check whether `eci` is True to determine the text encoding of the data. Typically it is standard ASCII, but it may be UTF-8 containing two-byte characters.

### `is_kanji`

```python
qrcode.is_kanji()
```

Returns True if the data type of the QR code is Japanese Kanji format. If the return value is True, you will need to decode the string yourself, because Japanese Kanji characters are 10 bits each, and MicroPython does not support parsing this type of text.

## Class `AprilTag`

The AprilTag object is returned by the `image.find_apriltags` function.

### Constructor

```python
class image.apriltag
```

Please use the `image.find_apriltags()` function to create this object.

### `corners`

```python
apriltag.corners()
```

This method returns a list of tuples containing the four corners of the AprilTag, each in the format (x, y). The four corners are typically ordered starting from the top-left corner and proceeding clockwise.

### `rect`

```python
apriltag.rect()
```

This method returns a rectangle tuple (x, y, w, h) that can be used with other image processing methods, such as the AprilTag bounding box in `image.draw_rectangle`.

### `x`

```python
apriltag.x()
```

This method returns the x coordinate (int) of the AprilTag bounding box. You can also obtain this value by indexing [0].

### `y`

```python
apriltag.y()
```

This method returns the y coordinate (int) of the AprilTag bounding box. You can also obtain this value by indexing [1].

### `w`

```python
apriltag.w()
```

This method returns the width (int) of the AprilTag bounding box. You can also obtain this value by indexing [2].

### `h`

```python
apriltag.h()
```

This method returns the height (int) of the AprilTag bounding box. You can also obtain this value by indexing [3].

### `id`

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

You can also obtain this value by indexing [4].

### `family`

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

You can also obtain this value by indexing [5].

### `cx`

```python
apriltag.cx()
```

This method returns the center x coordinate (int) of the AprilTag. You can also obtain this value by indexing [6].

### `cy`

```python
apriltag.cy()
```

This method returns the center y coordinate (int) of the AprilTag. You can also obtain this value by indexing [7].

### `rotation`

```python
apriltag.rotation()
```

This method returns the rotation angle of the AprilTag, measured in radians (int). You can also obtain this value by indexing [8].

### `decision_margin`

```python
aprilt

ag.decision_margin()
```

This method returns the decision margin of the AprilTag, reflecting the confidence in the detection (float). You can also obtain this value by indexing [9].

### `hamming`

```python
apriltag.hamming()
```

This method returns the maximum acceptable Hamming distance of the AprilTag (i.e., the number of bit errors that can be tolerated). Specifically:

- TAG16H5: Accepts up to 0 bit errors
- TAG25H7: Accepts up to 1 bit error
- TAG25H9: Accepts up to 3 bit errors
- TAG36H10: Accepts up to 3 bit errors
- TAG36H11: Accepts up to 4 bit errors
- ARTOOLKIT: Accepts up to 0 bit errors

You can obtain this value by indexing [10].

### `goodness`

```python
apriltag.goodness()
```

This method returns the color saturation of the AprilTag image, with a value range from 0.0 to 1.0, where 1.0 represents the best state.

> Currently, this value is typically 0.0. In the future, we plan to enable a feature called "tag refinement" to support the detection of smaller AprilTags. However, at present, this feature may cause the frame rate to drop below 1 FPS.

You can obtain this value by indexing [11].

### `x_translation`

```python
apriltag.x_translation()
```

This method returns the displacement of the camera in the x direction, in unknown units.

This method is very useful for determining the position of an AprilTag that is far from the camera. However, factors such as the size of the AprilTag and the lens you are using will affect what the x unit represents. For convenience, we recommend that you use a lookup table to convert the output of this method into information suitable for your application.

Note: The direction here is from left to right.

You can obtain this value by indexing [12].

### `y_translation`

```python
apriltag.y_translation()
```

This method returns the displacement of the camera in the y direction, in unknown units.

This method is very useful for determining the position of an AprilTag that is far from the camera. However, factors such as the size of the AprilTag and the lens you are using will affect what the y unit represents. For convenience, we recommend that you use a lookup table to convert the output of this method into information suitable for your application.

Note: The direction here is from top to bottom.

You can obtain this value by indexing [13].

### `z_translation`

```python
apriltag.z_translation()
```

This method returns the displacement of the camera in the z direction, in unknown units.

This method is very useful for determining the position of an AprilTag that is far from the camera. However, factors such as the size of the AprilTag and the lens you are using will affect what the z unit represents. For convenience, we recommend that you use a lookup table to convert the output of this method into information suitable for your application.

Note: The direction here is from front to back.

You can obtain this value by indexing [14].

### `x_rotation`

```python
apriltag.x_rotation()
```

This method returns the rotation angle of the AprilTag in the x plane, measured in radians. For example, this method can be applied if you move the camera from left to right to observe the AprilTag.

You can obtain this value by indexing [15].

### `y_rotation`

```python
apriltag.y_rotation()
```

This method returns the rotation angle of the AprilTag in the y plane, measured in radians. For example, this method can be applied if you move the camera from top to bottom to observe the AprilTag.

You can obtain this value by indexing [16].

### `z_rotation`

```python
apriltag.z_rotation()
```

This method returns the rotation angle of the AprilTag in the z plane, measured in radians. For example, this method can be applied if you rotate the camera to observe the AprilTag.

Note: This method is a renamed version of `apriltag.rotation()`.

You can obtain this value by indexing [17].

## Class `DataMatrix`

Data Matrix objects are returned by the `image.find_datamatrices` function.

### Constructor

```python
class image.datamatrix
```

Please call the `image.find_datamatrices()` function to create this object.

### `corners`

```python
datamatrix.corners()
```

This method returns a list of tuples containing the four corners of the data matrix, each tuple formatted as (x, y). The four corners are typically arranged starting from the top-left corner and proceeding clockwise.

### `rect`

```python
datamatrix.rect()
```

This method returns a rectangle tuple (x, y, w, h), which can be used in other image processing methods, such as the data matrix bounding box in `image.draw_rectangle`.

### `x`

```python
datamatrix.x()
```

This method returns the x-coordinate of the data matrix's bounding box (integer). You can also obtain this value via index [0].

### `y`

```python
datamatrix.y()
```

This method returns the y-coordinate of the data matrix's bounding box (integer). You can also obtain this value via index [1].

### `w`

```python
datamatrix.w()
```

This method returns the width of the data matrix's bounding box (integer). You can also obtain this value via index [2].

### `h`

```python
datamatrix.h()
```

This method returns the height of the data matrix's bounding box (integer). You can also obtain this value via index [3].

### `payload`

```python
datamatrix.payload()
```

This method returns the payload string of the data matrix. For example: "string".

You can also obtain this value via index [4].

### `rotation`

```python
datamatrix.rotation()
```

This method returns the rotation angle of the data matrix (measured in radians, as a float).

You can also obtain this value via index [5].

### `rows`

```python
datamatrix.rows()
```

This method returns the number of rows in the data matrix (integer).

You can also obtain this value via index [6].

### `columns`

```python
datamatrix.columns()
```

This method returns the number of columns in the data matrix (integer).

You can also obtain this value via index [7].

### `capacity`

```python
datamatrix.capacity()
```

This method returns the number of characters that the data matrix can hold.

You can also obtain this value via index [8].

### `padding`

```python
datamatrix.padding()
```

This method returns the number of unused characters in the data matrix.

You can also obtain this value via index [9].

## Class `BarCode`

The barcode object is returned by the `image.find_barcodes` function.

### Constructor

```python
class image.barcode
```

Please call the `image.find_barcodes()` function to create this object.

### `corners`

```python
barcode.corners()
```

This method returns a list of tuples containing the four corners of the barcode, with each tuple in the format (x, y). The four corners are typically arranged starting from the top-left corner and proceeding clockwise.

### `rect`

```python
barcode.rect()
```

This method returns a rectangle tuple (x, y, w, h), which can be used in other image processing methods, such as the barcode bounding box in `image.draw_rectangle`.

### `x`

```python
barcode.x()
```

This method returns the x-coordinate of the barcode bounding box (integer). You can also obtain this value through the index [0].

### `y`

```python
barcode.y()
```

This method returns the y-coordinate of the barcode bounding box (integer). You can also obtain this value through the index [1].

### `w`

```python
barcode.w()
```

This method returns the width of the barcode bounding box (integer). You can also obtain this value through the index [2].

### `h`

```python
barcode.h()
```

This method returns the height of the barcode bounding box (integer). You can also obtain this value through the index [3].

### `payload`

```python
barcode.payload()
```

This method returns the payload string of the barcode, for example: "Quantity".

You can also obtain this value through the index [4].

### `type`

```python
barcode.type()
```

This method returns the type of the barcode (integer). Possible types include:

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
- image.PDF417 (enabled in the future, currently unavailable)
- image.CODE93
- image.CODE128

You can also obtain this value through the index [5].

### `rotation`

```python
barcode.rotation()
```

This method returns the rotation angle of the barcode (in radians, float).

You can also obtain this value through the index [6].

### `quality`

```python
barcode.quality()
```

This method returns the number of times the barcode has been detected in the image (integer).

When scanning a barcode, each new scan line can decode the same barcode. Each time this process is performed, the barcode value increments.

You can also obtain this value through the index [7].

## Class `Displacement`

The displacement object is returned by the `image.find_displacement` function.

### Constructor

```python
class image.displacement
```

Please create this object by calling the `image.find_displacement()` function.

### `x_translation`

```python
displacement.x_translation()
```

This method returns the x-direction translation between two images, in pixels. The return value is a floating-point number representing the precise sub-pixel displacement.

You can also get this value through index [0].

### `y_translation`

```python
displacement.y_translation()
```

This method returns the y-direction translation between two images, in pixels. The return value is a floating-point number representing the precise sub-pixel displacement.

You can also get this value through index [1].

### `rotation`

```python
displacement.rotation()
```

This method returns the rotation between two images, in radians. The return value is a floating-point number representing the precise sub-pixel rotation.

You can also get this value through index [2].

### `scale`

```python
displacement.scale()
```

This method returns the scaling factor between two images, expressed as a floating-point number.

You can also get this value through index [3].

### `response`

```python
displacement.response()
```

This method returns the quality assessment of the displacement matching result between two images, with a value range from 0 to 1. If the return value is less than 0.1, the displacement object may be considered as noise.

You can also get this value through index [4].

## Class `Kptmatch`

Feature point objects are returned by the `image.match_descriptor` function.

### Constructor

```python
class image.kptmatch
```

Please create this object by calling the `image.match_descriptor()` function.

### `rect`

```python
kptmatch.rect()
```

This method returns a rectangle tuple (x, y, w, h), which can be used by other image processing methods that draw feature point bounding boxes, such as `image.draw_rectangle`.

### `cx`

```python
kptmatch.cx()
```

This method returns the x coordinate of the feature point's center, as an integer.

You can also access this value through index [0].

### `cy`

```python
kptmatch.cy()
```

This method returns the y coordinate of the feature point's center, as an integer.

You can also access this value through index [1].

### `x`

```python
kptmatch.x()
```

This method returns the x coordinate of the feature point's bounding box, as an integer.

You can also access this value through index [2].

### `y`

```python
kptmatch.y()
```

This method returns the y coordinate of the feature point's bounding box, as an integer.

You can also access this value through index [3].

### `w`

```python
kptmatch.w()
```

This method returns the width of the feature point's bounding box, as an integer.

You can also access this value through index [4].

### `h`

```python
kptmatch.h()
```

This method returns the height of the feature point's bounding box, as an integer.

You can also access this value through index [5].

### `count`

```python
kptmatch.count()
```

This method returns the number of matching feature points, as an integer.

You can also access this value through index [6].

### `theta`

```python
kptmatch.theta()
```

This method returns the estimated rotation of the feature point, as an integer.

You can also access this value through index [7].

### `match`

```python
kptmatch.match()
```

This method returns a list of (x, y) tuples for matching key points.

You can also access this value through index [8].

## Constants

### `image.SEARCH_EX`

Used to perform exhaustive template matching search.

### `image.SEARCH_DS`

Used to perform faster template matching search.

### `image.EDGE_CANNY`

Applies the Canny edge detection algorithm for edge detection on the image.

### `image.EDGE_SIMPLE`

Uses a threshold high-pass filtering algorithm for edge detection on the image.

### `image.CORNER_FAST`

Used for ORB feature points with high-speed, low-accuracy corner detection algorithm.

### `image.CORNER_AGAST`

Used for ORB feature points with low-speed, high-accuracy corner detection algorithm.

### `image.TAG16H5`

Bitmask enumeration of the TAG16H5 tag family for AprilTags.

### `image.TAG25H7`

Bitmask enumeration of the TAG25H7 tag family for AprilTags.

### `image.TAG25H9`

Bitmask enumeration of the TAG25H9 tag family for AprilTags.

### `image.TAG36H10`

Bitmask enumeration of the TAG36H10 tag family for AprilTags.

### `image.TAG36H11`

Bitmask enumeration of the TAG36H11 tag family for AprilTags.

### `image.ARTOOLKIT`

Bitmask enumeration of the ARTOLKIT tag family for AprilTags.

### `image.EAN2`

Enumeration of the EAN2 barcode type.

### `image.EAN5`

Enumeration of the EAN5 barcode type.

### `image.EAN8`

Enumeration of the EAN8 barcode type.

### `image.UPCE`

Enumeration of the UPCE barcode type.

### `image.ISBN10`

Enumeration of the ISBN10 barcode type.

### `image.UPCA`

Enumeration of the UPCA barcode type.

### `image.EAN13`

Enumeration of the EAN13 barcode type.

### `image.ISBN13`

Enumeration of the ISBN13 barcode type.

### `image.I25`

Enumeration of the I25 barcode type.

### `image.DATABAR`

Enumeration of the DATABAR barcode type.

### `image.DATABAR_EXP`

Enumeration of the DATABAR_EXP barcode type.

### `image.CODABAR`

Enumeration of the CODABAR barcode type.

### `image.CODE39`

Enumeration of the CODE39 barcode type.

### `image.PDF417`

Enumeration of the PDF417 barcode type (not yet implemented).

### `image.CODE93`

Enumeration of the CODE93 barcode type.

### `image.CODE128`

Enumeration of the CODE128 barcode type.
