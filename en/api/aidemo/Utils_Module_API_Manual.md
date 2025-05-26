# 5.5 Utils Module API Manual

## 1. Overview

This manual is intended to provide developers with some common processing methods for developing AI demos using MicroPython.

## 2. API Introduction

### 2.1 Timing Module ScopedTiming

**Description**

The ScopedTiming class is a context manager used to measure the execution time of a code block. A context manager is created by defining a class that contains the `__enter__` and `__exit__` methods. When an instance of this class is used in a `with` statement, the `__enter__` method is called when entering the `with` block, and the `__exit__` method is called when leaving.

```python
from libs.Utils import ScopedTiming

def test_time():
    with ScopedTiming("test",1):
        ##### Code #####
        # ...
        ##############
```

**Parameters**  

| Parameter Name | Description | Input / Output | Remarks |
|----------|-------------------------------|-----------|------|
| info   | Description of the timed part | Input | Default is "" |
| enable_profile   | Whether to debug and print timing information | Input | Default is True |

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| - | No return value |

### 2.2 read_json

**Description**

Reads fields from a JSON file based on the JSON file path, primarily used for reading configuration files for deploying online training platform scripts.

**Syntax**  

```python
import libs.Utils import read_json

json_path="/sdcard/examples/test.json"
json_data=read_json(json_path)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| json_path      | Path of the JSON file on the development board   | Input          | Required |

**Return Value**  

| Return Value | Description                            |
|--------------|-----------------------------------------|
| dict         | Content of JSON fields                  |

### 2.3 read_image

**Description**

Reads image data based on the image path, used for reading static images during AI inference and providing them to the model for completion of inference.

**Syntax**  

```python
import libs.Utils import read_image

img_path="/sdcard/examples/test.jpg"
img_chw,img_rgb888=read_image(img_path)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| img_path       | Path of the image file on the development board   | Input          | Required |

**Return Value**  

| Return Value | Description                            |
|--------------|-----------------------------------------|
| img_chw      | Image data in CHW arrangement in ulab.numpy.ndarray format, which can be used to create an nncase_runtime.tensor for AI model inference |
| img_rgb888   | Image instance in rgb888 format, which can be used for drawing results |

### 2.4 get_colors

**Description**

Get the ARGB color array according to the number of labels, such as [255,191,162,208]. There are 80 preset colors. When the number is greater than 80, the remainder is taken.

**Syntax**  

```python
from libs.Utils import get_colors

classes_num = 30
colors = get_colors(classes_num)
```

**Parameters**  

| Parameter Name | Description | Input / Output | Remarks |
|----------|-------------------------------|-----------|------|
| classes_num | Number of labels | Input | Required |

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| list[list]  | ARGB color array |

### 2.5 center_crop_param

**Description**

The `center_crop_param` is a square center cropping function that receives an input parameter `input_size` representing the image size. It is usually a list containing two elements, representing the width and height of the image respectively. The function will calculate the top-left coordinates (`top` and `left`) of the cropping area and the side length `m` of the cropping area based on the center of the image, and finally return these parameters.

**Syntax**  

```python
from libs.Utils import center_crop_param

input_size = [640,320]
top, left, m = center_crop_param(input_size)
```

**Parameters**  

| Parameter Name | Description | Input / Output | Remarks |
|----------|-------------------------------|-----------|------|
| input_size | Input width and height list | Input | Required |

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| left    | Distance from the top-left corner of the cropping area to the left border |
| top     | Distance from the top-left corner of the cropping area to the top border |
| m       | Side length of the cropping area |

### 2.6 letterbox_pad_param

**Description**

The `letterbox_pad_param` function is used to calculate the parameters required for padding the input image. This padding is a technique that scales the image to the specified output size while maintaining the aspect ratio of the image and adds padding around it. It is commonly used in computer vision tasks such as object detection to ensure that the input image can fit the input size of the model. This function performs one-sided padding, that is, only padding on the bottom and right sides, and returns the widths of the top, bottom, left, and right padding areas and the scaling ratio. The calculation results of this method are generally used together with `resize`.

**Syntax**  

```python
from libs.Utils import letterbox_pad_param

input_size = [1920,1080]
output_size = [640,640]
left, right, top, bottom, scale = letterbox_pad_param(input_size, output_size)
```

**Parameters**  

| Parameter Name | Description | Input / Output | Remarks |
|----------|-------------------------------|-----------|------|
| input_size | Input resolution before scaling and padding | Input | Required |
| output_size | Output resolution after scaling and padding | Input | Required |

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| left    | Left padding value |
| right   | Right padding value |
| top     | Top padding value |
| bottom  | Bottom padding value |
| scale   | Scaling ratio |

### 2.7 center_pad_param

**Description**

The main purpose of the `center_pad_param` function is to calculate the parameters required to center-pad the input image and scale it to the specified output size. When processing an image, in order to make the image fit a specific output size while maintaining its original aspect ratio, a scaling operation is usually performed, and then padding is added around the image to center the image in the output area. This function will return the widths of the top, bottom, left, and right padding areas and the scaling ratio. The calculation results of this method are generally used together with `resize`.

**Syntax**  

```python
from libs.Utils import center_pad_param

input_size = [1920,1080]
output_size = [640,640]
left, right, top, bottom, scale = center_pad_param(input_size, output_size)
```

**Parameters**  

| Parameter Name | Description | Input / Output | Remarks |
|----------|-------------------------------|-----------|------|
| input_size | Input resolution before scaling and padding | Input | Required |
| output_size | Output resolution after scaling and padding | Input | Required |

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| left    | Left padding value |
| right   | Right padding value |
| top     | Top padding value |
| bottom  | Bottom padding value |
| scale   | Scaling ratio |

### 2.8 softmax

**Description**

The `softmax` function is widely used in classification problems. Its main function is to convert a real-valued vector into a probability distribution, so that each element in the vector is in the interval [0, 1], and the sum of all elements is 1. In this way, the output of the model can be interpreted as the probability corresponding to each class.

**Syntax**  

```python
from libs.Utils import softmax

input_data = [1,2,3]
output_data = softmax(input_data)
```

**Parameters**  

| Parameter Name | Description | Input / Output | Remarks |
|----------|-------------------------------|-----------|------|
| x | One-dimensional data returned by the classification model | Input | Required |

**Return Value**  

| Return Value | Description |
|--------|---------------------------------|
| softmax_res    | Probability distribution of classes |

### 2.9 sigmoid

**Description**

The sigmoid function is widely used in binary classification models. Its role is to map any real number to the interval (0, 1), commonly used to convert model outputs into probability values for probability judgment or classification decision-making.

**Syntax**  

```python
from libs.Utils import sigmoid

input_data = 0.5
output_data = sigmoid(input_data)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| input_data     | Any real number                      | Input          | Required |

**Return Value**  

| Return Value | Description                            |
|--------------|-----------------------------------------|
| sigmoid_res  | Value or array mapped to the interval (0, 1) |

### 2.10 chw2hwc

**Description**

Converts `ulab.numpy.ndarray` data arranged in CHW format to HWC format, applicable only to 3-dimensional data.

**Syntax**  

```python
from libs.Utils import chw2hwc

# chw_np is 3D ulab.numpy.ndarray data arranged in CHW format
hwc_np = chw2hwc(chw_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| chw_np         | 3D ulab.numpy.ndarray data           | Input          | Required |

**Return Value**  

| Return Value | Description                            |
|--------------|-----------------------------------------|
| hwc_np       | 3D ulab.numpy.ndarray data arranged in HWC format |

### 2.11 hwc2chw

**Description**

Converts `ulab.numpy.ndarray` data arranged in HWC format to CHW format, applicable only to 3-dimensional data, often used to convert Image instance data for use with AI models.

**Syntax**  

```python
from libs.Utils import hwc2chw

# hwc_np is 3D ulab.numpy.ndarray data arranged in HWC format
chw_np = hwc2chw(hwc_np)
```

**Parameters**  

| Parameter Name | Description                          | Input / Output | Notes |
|----------------|--------------------------------------|----------------|-------|
| hwc_np         | 3D ulab.numpy.ndarray data           | Input          | Required |

**Return Value**  

| Return Value | Description                            |
|--------------|-----------------------------------------|
| chw_np       | 3D ulab.numpy.ndarray data arranged in CHW format |
