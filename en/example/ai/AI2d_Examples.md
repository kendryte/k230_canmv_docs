# 4. Ai2d Preprocessing Examples

## 1. Overview

Based on the interfaces provided by the `nncase_runtime` module, the AIDemo part has performed secondary encapsulation on `nncase_runtime.ai2d`. The encapsulation file is in the `/sdcard/libs/AI2D.py` module. The provided interfaces can be found in: [Ai2d Module API Manual](../../api/aidemo/Ai2d Module API Manual.md). For the 5 preprocessing methods provided by Ai2d, this document provides examples, visualizing the results of preprocessing to help users better understand and use the Ai2d preprocessing process. The unencapsulated `nncase_runtime.ai2d` interfaces can be found in: [nncase_usage](./nncase_usage.md).

## 2. resize Method

The resize method is an operation widely used in image preprocessing. It is mainly used to change the size of an image. Whether it is to enlarge or reduce an image, this method can be used to achieve it. Here is the sample code for implementing the resize process using `Ai2d`.

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os

if __name__ == "__main__":
    # Display mode, default is "hdmi", you can choose "hdmi" or "lcd"
    display_mode="hdmi"
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]

    # Initialize PipeLine for image processing flow
    pl = PipeLine(rgb888p_size=[512,512], display_size=display_size, display_mode=display_mode)
    pl.create()  # Create a PipeLine instance
    my_ai2d=Ai2d(debug_mode=0) # Initialize an Ai2d instance
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # Configure the resize preprocessing method
    my_ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
    # Build the preprocessing process
    my_ai2d.build([1,3,512,512],[1,3,640,640])
    try:
        while True:
            os.exitpoint()                      # Check for exit signals
            with ScopedTiming("total",1):
                img = pl.get_frame()            # Get the current frame data
                print(img.shape)                # The shape of the original image is [3,512,512]
                ai2d_output_tensor=my_ai2d.run(img) # Perform resize preprocessing
                ai2d_output_np=ai2d_output_tensor.to_numpy() # Type conversion
                print(ai2d_output_np.shape)        # The shape after preprocessing is [1,3,640,640]
                gc.collect()                    # Garbage collection
    except Exception as e:
        sys.print_exception(e)                  # Print exception information
    finally:
        pl.destroy()                            # Destroy the PipeLine instance
```

## 3. crop Method

The crop method is an operation used to extract (crop) the region of interest (ROI) from the original image. It can select a part of the image as a new image according to the specified coordinates and size. Here is the sample code for implementing the crop process using `Ai2d`.

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os
import image

if __name__ == "__main__":
    # Display mode, default is "hdmi", you can choose "hdmi" or "lcd"
    display_mode="hdmi"
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]

    # Initialize PipeLine for image processing flow
    pl = PipeLine(rgb888p_size=[512,512], display_size=display_size, display_mode=display_mode)
    pl.create()  # Create a PipeLine instance
    my_ai2d=Ai2d(debug_mode=0) # Initialize an Ai2d instance
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # Configure the crop preprocessing method
    my_ai2d.crop(100,100,300,300)
    # Build the preprocessing process
    my_ai2d.build([1,3,512,512],[1,3,200,200])
    try:
        while True:
            os.exitpoint()                      # Check for exit signals
            with ScopedTiming("total",1):
                img = pl.get_frame()            # Get the current frame data
                print(img.shape)                # The shape of the original image is [1,3,512,512]
                ai2d_output_tensor=my_ai2d.run(img) # Perform crop preprocessing, cropping the data within the range of 100~300px in both the H/W dimensions
                ai2d_output_np=ai2d_output_tensor.to_numpy() # Type conversion
                print(ai2d_output_np.shape)        # The shape after preprocessing is [1,3,200,200]
                # Use transpose to process the output into np data arranged in HWC, and then create an Image instance in RGB888 format on the np data for display effects in the IDE
                shape=ai2d_output_np.shape
                ai2d_output_tmp = ai2d_output_np.reshape((shape[0] * shape[1], shape[2]*shape[3]))
                ai2d_output_tmp_trans = ai2d_output_tmp.transpose()
                ai2d_output_hwc=ai2d_output_tmp_trans.copy().reshape((shape[2],shape[3],shape[1]))
                out_img=image.Image(200, 200, image.RGB888,alloc=image.ALLOC_REF,data=ai2d_output_hwc)
                out_img.compress_for_ide()
                gc.collect()                    # Garbage collection
    except Exception as e:
        sys.print_exception(e)                  # Print exception information
    finally:
        pl.destroy()                            # Destroy the PipeLine instance
```

## 4. pad Method

The pad (padding) method is a technique for padding the edges of an image in the image preprocessing stage. It changes the size of the image by adding pixel values around the image (top, bottom, left, and right). These added pixel values can be customized. Here is the sample code for implementing the pad process using `Ai2d`.

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os
import image

if __name__ == "__main__":
    # Display mode, default is "hdmi", you can choose "hdmi" or "lcd"
    display_mode="hdmi"
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]

    # Initialize PipeLine for image processing flow
    pl = PipeLine(rgb888p_size=[512,512], display_size=display_size, display_mode=display_mode)
    pl.create()  # Create a PipeLine instance
    my_ai2d=Ai2d(debug_mode=0) # Initialize an Ai2d instance
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # Configure the pad preprocessing method
    my_ai2d.pad(paddings=[0,0,0,0,15,15,30,30],pad_mode=0,pad_val=[114,114,114])
    # Build the preprocessing process
    my_ai2d.build([1,3,512,512],[1,3,512+15+15,512+30+30])
    try:
        while True:
            os.exitpoint()                      # Check for exit signals
            with ScopedTiming("total",1):
                img = pl.get_frame()            # Get the current frame data
                print(img.shape)                # The shape of the original image is [1,3,512,512]
                ai2d_output_tensor=my_ai2d.run(img) # Perform pad preprocessing, padding 15px up and down in the H dimension and 30px left and right in the W dimension
                ai2d_output_np=ai2d_output_tensor.to_numpy() # Type conversion
                print(ai2d_output_np.shape)        # The shape after preprocessing is [1,3,542,572]
                # Use transpose to process the output into np data arranged in HWC, and then create an Image instance in RGB888 format on the np data for display effects in the IDE
                shape=ai2d_output_np.shape
                ai2d_output_tmp = ai2d_output_np.reshape((shape[0] * shape[1], shape[2]*shape[3]))
                ai2d_output_tmp_trans = ai2d_output_tmp.transpose()
                ai2d_output_hwc=ai2d_output_tmp_trans.copy().reshape((shape[2],shape[3],shape[1]))
                out_img=image.Image(512+30+30, 512+15+15, image.RGB888,alloc=image.ALLOC_REF,data=ai2d_output_hwc)
                out_img.compress_for_ide()
                gc.collect()                    # Garbage collection
    except Exception as e:
        sys.print_exception(e)                  # Print exception information
    finally:
        pl.destroy()                            # Destroy the PipeLine instance
```

## 5. affine Method

The affine (affine transformation) method is a technique used for geometric transformation of images in image preprocessing. It can implement various geometric transformation operations such as rotation, translation, and scaling of images, and can maintain the "straightness" of the image (i.e., a straight line remains a straight line after transformation) and "parallelism" (i.e., parallel lines remain parallel after transformation). Here is the sample code for implementing the affine process using `Ai2d`.

```python
from libs.PipeLine import PipeLine, ScopedTiming
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import gc
import sys,os
import image

if __name__ == "__main__":
    # Display mode, default is "hdmi", you can choose "hdmi" or "lcd"
    display_mode="hdmi"
    if display_mode=="hdmi":
        display_size=[1920,1080]
    else:
        display_size=[800,480]

    # Initialize PipeLine for image processing flow
    pl = PipeLine(rgb888p_size=[512,512], display_size=display_size, display_mode=display_mode)
    pl.create()  # Create a PipeLine instance
    my_ai2d=Ai2d(debug_mode=0) # Initialize an Ai2d instance
    my_ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # Create an affine transformation matrix, scale by 0.5 times, and translate 50px in both the X and Y directions
    affine_matrix = [0.5,0,50,
                     0,0.5,50]
    # Set the affine transformation preprocessing
    my_ai2d.affine(nn.interp_method.cv2_bilinear,0, 0, 127, 1,affine_matrix)
    # Build the preprocessing process
    my_ai2d.build([1,3,512,512],[1,3,256,256])
    try:
        while True:
            os.exitpoint()                      # Check for exit signals
            with ScopedTiming("total",1):
                img = pl.get_frame()            # Get the current frame data
                print(img.shape)                # The shape of the original image is [1,3,512,512]
```
