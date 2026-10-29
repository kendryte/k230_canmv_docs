# `Utils` Module API Manual

## Overview

This manual is intended to provide developers with some common processing methods used when developing AI Demo with MicroPython.

## API Introduction

### Timing Module ScopedTiming

**Description**

The ScopedTiming class is a context manager used to measure the execution time of a code block. A context manager is created by defining a class that contains the `__enter__` and `__exit__` methods. When an instance of this class is used in a with statement, `__enter__` is called when entering the with block, and `__exit__` is called when leaving.

```python
from libs.Utils import ScopedTiming

def test_time():
    with ScopedTiming("test",1):
        #####code#####
        # ...
        ##############
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| info   | Description of the timed section | Input | Default "" |
| enable_profile   | Whether to enable debug printing of timing information | Input | Default True |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| - | No return value |

### read_json

**Description**

Reads fields from a JSON file based on the file path, mainly used for reading configuration files of scripts deployed on the online training platform.

**Syntax**

```python
from libs.Utils import read_json

json_path="/sdcard/examples/test.json"
json_data=read_json(json_path)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| json_path | Path of the JSON file on the development board | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| dict  |       JSON field content       |

### read_image

**Description**

Reads image data based on the image path, used during AI inference to read static images and feed them to the model to complete inference.

**Syntax**

```python
from libs.Utils import read_image

img_path="/sdcard/examples/test.jpg"
img_chw,img_rgb888=read_image(img_path)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| img_path | Path of the image file on the development board | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| img_chw  |       Image data in CHW layout in `ulab.numpy.ndarray` format, which can be used to create `nncase_runtime.tensor` for AI model inference       |
| img_rgb888  |       Image instance in rgb888 format, which can be used for drawing results      |

### get_colors

**Description**

Gets an ARGB color array based on the number of labels, e.g., [255,191,162,208]. 80 colors are preset; when the number exceeds 80, the modulo operation is applied.

**Syntax**

```python
from libs.Utils import get_colors

classes_num=30
colors=get_colors(classes_num)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| classes_num | Number of labels | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| list[tuple]  |  A list of ARGB colors, where each element is an `(A, R, G, B)` quadruple, e.g., `(255, 220, 20, 60)`. The built-in palette contains 80 colors; when `classes_num` exceeds 80, colors are cycled |

### center_crop_param

**Description**

`center_crop_param` is a square center-cropping function that takes an input parameter `input_size` representing the image size, which is usually a list containing two elements representing the image width and height respectively. The function calculates the coordinates of the top-left corner (top and left) of the cropping area based on the image center, as well as the side length m of the cropping area, and ultimately returns these parameters.

**Syntax**

```python
from libs.Utils import center_crop_param

input_size=[640,320]
top,left,m=center_crop_param(input_size)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| input_size | Input width and height list | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| top     | Distance from the top-left corner of the crop to the top boundary                   |
| left    | Distance from the top-left corner of the crop to the left boundary                   |
| m       | Crop side length                   |

### letterbox_pad_param

**Description**

The `letterbox_pad_param` function is used to calculate the parameters required for padding the input image. This padding is a technique that scales the image to the specified output size while maintaining the aspect ratio, and adds padding around it. It is commonly used in computer vision tasks such as object detection to ensure that the input image fits the model's input size. The function performs single-side padding, i.e., only padding on the bottom and right sides, and returns the top, bottom, left, and right boundary widths of the padding area, as well as the scale ratio. The result calculated by this method is generally used together with resize.

**Syntax**

```python
from libs.Utils import letterbox_pad_param

input_size=[1920,1080]
output_size=[640,640]
top,bottom,left,right,scale=letterbox_pad_param(input_size,output_size)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| input_size| Input resolution before scaling and padding | Input | Required |
| output_size| Output resolution after scaling and padding | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| top     |  Top padding value                     |
| bottom  |  Bottom padding value                     |
| left    |  Left padding value                     |
| right   |  Right padding value                     |
| scale   |  Scale ratio                       |

### center_pad_param

**Description**

The main purpose of the `center_pad_param` function is to calculate the parameters required for padding the input image in a centered manner and scaling it to the specified output size. When processing images, in order to fit a specific output size while maintaining the original aspect ratio, a scaling operation is usually performed, and then padding is added around the image so that the image is centered in the output area. The function returns the top, bottom, left, and right boundary widths of the padding area, as well as the scale ratio. The result calculated by this method is generally used together with resize.

**Syntax**

```python
from libs.Utils import center_pad_param

input_size=[1920,1080]
output_size=[640,640]
top,bottom,left,right,scale=center_pad_param(input_size,output_size)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| input_size| Input resolution before scaling and padding | Input | Required |
| output_size| Output resolution after scaling and padding | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| top     |  Top padding value                     |
| bottom  |  Bottom padding value                     |
| left    |  Left padding value                     |
| right   |  Right padding value                     |
| scale   |  Scale ratio                       |

### softmax

**Description**

The softmax function is widely used in classification problems. Its main purpose is to convert a real-valued vector into a probability distribution, making each element in the vector fall within the [0, 1] interval and the sum of all elements equal to 1. In this way, the model's output can be interpreted as the probability corresponding to each category.

**Syntax**

```python
from libs.Utils import softmax

input_data=[1,2,3]
output_data=softmax(input_data)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| x | One-dimensional data returned by the classification model | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| softmax_res    |       Probability distribution of categories      |

### sigmoid

**Description**

The sigmoid function is widely used in binary classification models. Its purpose is to map any real number to the (0, 1) interval, which is commonly used to convert model output into probability values for probability judgment or classification decisions.

**Syntax**

```python
from libs.Utils import sigmoid

input_data = 0.5
output_data = sigmoid(input_data)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| input_data | Any real number | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| sigmoid_res| A value or array mapped to the (0, 1) interval |

### chw2hwc

**Description**

Converts `ulab.numpy.ndarray` data in CHW layout to HWC layout. Only applicable to 3-dimensional data.

**Syntax**

```python
from libs.Utils import chw2hwc

# chw_np is ulab.numpy.ndarray data in CHW layout
hwc_np = chw2hwc(chw_np)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| chw_np | 3-dimensional `ulab.numpy.ndarray` data | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| hwc_np| 3-dimensional `ulab.numpy.ndarray` data in HWC layout |

### hwc2chw

**Description**

Converts `ulab.numpy.ndarray` data in HWC layout to CHW layout. Only applicable to 3-dimensional data, commonly used to convert Image instance data before feeding it to AI models.

**Syntax**

```python
from libs.Utils import hwc2chw

# hwc_np is ulab.numpy.ndarray data in CHW layout
chw_np = hwc2chw(hwc_np)
```

**Parameters**

| Parameter Name | Description | Input / Output | Notes |
|----------|-------------------------------|-----------|------|
| hwc_np | 3-dimensional `ulab.numpy.ndarray` data | Input | Required |

**Return Value**

| Return Value | Description |
|--------|---------------------------------|
| chw_np| 3-dimensional `ulab.numpy.ndarray` data in CHW layout |
