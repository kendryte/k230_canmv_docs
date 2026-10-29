# YOLOv8 Detection Example

## Overview

The K230 CanMV YOLOv8 detection is a simple application developed in MicroPython that acquires camera data, performs inference, detects targets, and draws bounding boxes. This example program uses multiple hardware modules of the K230 CanMV platform: AI2D, KPU, Sensor, Display, etc. The application mainly demonstrates how to implement AI inference under the K230 multimedia module!

📌 **This example is the detailed implementation of the PipeLine structure in the AI Demo. The PipeLine structure is a simplified application-layer encapsulation based on this application's code logic. When the PipeLine structure cannot meet user development needs, you can refer to this part of the code for development!**

```{admonition} Note
:class: warning
This example directly operates Sensor/Display/KPU to showcase the underlying flow, and differs from `PipeLine` in two aspects that need attention:

- This example uses **channel 1** (`CAM_CHN_ID_1`) for AI image output, while `PipeLine` uses **channel 2** (`CAM_CHN_ID_2`). Both work, but do not confuse the channel numbers when mixing the two sets of code.
- The main loop in this example is `while True:`, so the resource release code at the end will not actually be executed. When writing your own application, please wrap the main loop with `try/finally` according to [two main loop writing patterns](../../ai_dev_doc.md#main-loop-patterns).
```

## Hardware Environment

Running this example program requires the following hardware environment: K230 CanMV development board and the corresponding Sensor module.

## Example Code

```python
import os,sys
from media.sensor import *
from media.display import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc
from libs.Utils import *

#-----------------------------Other necessary methods---------------------------------------------
# Multi-object detection Non-Maximum Suppression method implementation
def nms(boxes,scores,thresh):
    """Pure Python NMS baseline."""
    x1,y1,x2,y2 = boxes[:, 0],boxes[:, 1],boxes[:, 2],boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = np.argsort(scores,axis = 0)[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        new_x1,new_y1,new_x2,new_y2,new_areas = [],[],[],[],[]
        for order_i in order:
            new_x1.append(x1[order_i])
            new_x2.append(x2[order_i])
            new_y1.append(y1[order_i])
            new_y2.append(y2[order_i])
            new_areas.append(areas[order_i])
        new_x1 = np.array(new_x1)
        new_x2 = np.array(new_x2)
        new_y1 = np.array(new_y1)
        new_y2 = np.array(new_y2)
        xx1 = np.maximum(x1[i], new_x1)
        yy1 = np.maximum(y1[i], new_y1)
        xx2 = np.minimum(x2[i], new_x2)
        yy2 = np.minimum(y2[i], new_y2)
        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        new_areas = np.array(new_areas)
        ovr = inter / (areas[i] + new_areas - inter)
        new_order = []
        for ovr_i,ind in enumerate(ovr):
            if ind < thresh:
                new_order.append(order[ovr_i])
        # What is stored here is the box index, use uint16 to avoid overflow when the number of boxes exceeds 255 (ulab supports uint8/int8/uint16/int16/float)
        order = np.array(new_order,dtype=np.uint16)
    return keep

# Note: letterbox_pad_param is provided by libs.Utils (imported at the beginning of the script via from libs.Utils import *),
#      so no need to redefine it here. If you want to understand the implementation details, check /sdcard/libs/Utils.py.


#-----------------------------Sensor/Display initialization part-------------------------------

# Define the screen display resolution
DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

# Define AI inference frame resolution
AI_RGB888P_WIDTH = ALIGN_UP(1280, 16)
AI_RGB888P_HEIGHT = 720

sensor = Sensor()
sensor.reset()
# Set horizontal mirror and vertical flip. Different boards have different orientations; configure these two parameters to make the image upright
#sensor.set_hmirror(False)
#sensor.set_vflip(False)

# Configure multi-channel image output of sensor. Each channel's output format and resolution can be different. Up to three channels can be output. Refer to the sensor API documentation
# Channel 0 directly feeds the display VO, in YUV420 format
sensor.set_framesize(width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT,chn=CAM_CHN_ID_0)
sensor.set_pixformat(Sensor.YUV420SP,chn=CAM_CHN_ID_0)
# Channel 1 feeds AI for algorithm processing, in RGB888P format
sensor.set_framesize(width = AI_RGB888P_WIDTH , height = AI_RGB888P_HEIGHT, chn=CAM_CHN_ID_1)
# Set the output format of channel 1
sensor.set_pixformat(Sensor.RGBP888, chn=CAM_CHN_ID_1)

# Bind the camera image of channel 0 to the screen to prevent the AI inference process of another channel from being too slow and affecting the display process, resulting in stuttering
sensor_bind_info = sensor.bind_info(x = 0, y = 0, chn = CAM_CHN_ID_0)
Display.bind_layer(**sensor_bind_info, layer = Display.LAYER_VIDEO1)

# OSD image initialization, create a transparent image with the same size as the screen resolution for drawing AI inference results
osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

# Set to LT9611 display, default 1920x1080
Display.init(Display.LT9611,width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1, to_ide = True)
## If using ST7701 LCD screen display, default 800*480, also supports 640*480, etc. Refer to the Display module API documentation for details
#Display.init(Display.ST7701, width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1, to_ide=True)

# Limit the frame rate of the bind channel to prevent the producer from being too fast
sensor._set_chn_fps(chn = CAM_CHN_ID_0, fps = Display.fps())


#-----------------------------AI model initialization part-------------------------------
# Kmodel path
kmodel_path="/sdcard/examples/kmodel/yolov8n_224.kmodel"
# Class labels
labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
# Model input resolution
model_input_size=[224,224]
# Other parameter settings, including threshold, maximum number of detection boxes, etc.
confidence_threshold = 0.3
nms_threshold = 0.4
max_boxes_num = 50
# Colors for different category boxes
colors=get_colors(len(labels))

# Initialize ai2d preprocessing, and configure ai2d padding+resize preprocessing. The input resolution of the preprocessing process is the image resolution, and the output resolution is the required resolution of the model input, implementing the image->preprocess->model process
ai2d=nn.ai2d()
# Configure the input and output data types and formats of the ai2d module
ai2d.set_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
# Set padding parameters: the size of top, bottom, left, right padding and the specific padding values for the three channels
top,bottom,left,right,ratio=letterbox_pad_param([AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT],model_input_size)
ai2d.set_pad_param(True,[0,0,0,0,top,bottom,left,right], 0, [128,128,128])
# Set resize parameters, configure interpolation method
ai2d.set_resize_param(True,nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
# Set the input and output dimensions of the ai2d module, and build the builder instance
ai2d_builder = ai2d.build([1,3,AI_RGB888P_HEIGHT,AI_RGB888P_WIDTH], [1,3,model_input_size[1],model_input_size[0]])
# Initialize an empty tensor for ai2d output and kpu input. Since the output of ai2d is generally directly fed to kpu, a shared variable is used here
input_init_data = np.ones((1,3,model_input_size[1],model_input_size[0]),dtype=np.uint8)
kpu_input_tensor = nn.from_numpy(input_init_data)


# Create kpu instance
kpu=nn.kpu()
# Load kmodel
kpu.load_kmodel(kmodel_path)

# media initialization
MediaManager.init()
# Start sensor
sensor.run()
# Test frame rate
fps = time.clock()
while True:
    fps.tick()
    #------------------------Dump a frame from the camera and process it----------------------------------
    # Dump a frame of RGB888P format Image from the camera channel 1
    img=sensor.snapshot(chn=CAM_CHN_ID_1)
    # Convert to ulab.numpy.ndarray format data, CHW
    img_np=img.to_numpy_ref()
    # Create nncase_runtime.tensor for ai2d preprocessing
    ai2d_input_tensor=nn.from_numpy(img_np)
    #------------------------Preprocessing steps before inference----------------------------------------
    # Execute preprocessing
    ai2d_builder.run(ai2d_input_tensor, kpu_input_tensor)
    #------------------------Use kpu to complete model inference--------------------------------------
    # Set the 0th input of kpu to the tensor after ai2d preprocessing. If there are multiple, you can set them in sequence
    kpu.set_input_tensor(0,kpu_input_tensor)
    # Execute model inference on kpu
    kpu.run()
    #------------------------Get the output after model inference----------------------------------------
    # Get the output tensor of model inference, and convert it to ulab.numpy.ndarray data for post-processing
    results=[]
    for i in range(kpu.outputs_size()):
        output_i_tensor = kpu.get_output_tensor(i)
        result_i = output_i_tensor.to_numpy()
        results.append(result_i)
        del output_i_tensor
    #------------------------Post-processing of inference output----------------------------------------
    # YOLOv8 detection model has only 1 output, that is, the shape of results[0] is [1,box_dim,box_num]. results[0][0] represents [box_dim,box_num], which is converted to [box_num,box_dim] for processing each box in turn
    output_data=results[0][0].transpose()
    # The first four data of each box are the center point coordinates and width and height
    boxes_ori = output_data[:,0:4]
    # The remaining data is the score for each category. Use argmax to find the category number and score with the highest score
    class_ori = output_data[:,4:]
    class_res=np.argmax(class_ori,axis=-1)
    scores_ = np.max(class_ori,axis=-1)
    # Filter boxes by confidence threshold (those below the confidence threshold are discarded), and process the coordinates to x1,y1,x2,y2, which are the top-left and bottom-right coordinates of the box. Note the ratio conversion, convert the input resolution coordinates (model_input_size) to the original image coordinates (AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT)
    boxes,inds,scores=[],[],[]
    for i in range(len(boxes_ori)):
        if scores_[i]>confidence_threshold:
            x,y,w,h=boxes_ori[i][0],boxes_ori[i][1],boxes_ori[i][2],boxes_ori[i][3]
            x1 = int((x - 0.5 * w)/ratio)
            y1 = int((y - 0.5 * h)/ratio)
            x2 = int((x + 0.5 * w)/ratio)
            y2 = int((y + 0.5 * h)/ratio)
            boxes.append([x1,y1,x2,y2])
            inds.append(class_res[i])
            scores.append(scores_[i])
    #If there are no boxes after the first round of filtering, continue processing the next frame
    if len(boxes)==0:
        continue
    # Convert list to ulab.numpy.ndarray for easier processing
    boxes = np.array(boxes)
    scores = np.array(scores)
    inds = np.array(inds)
    # NMS process to remove overlapping redundant boxes, keep is
    keep = nms(boxes,scores,nms_threshold)
    dets = np.concatenate((boxes, scores.reshape((len(boxes),1)), inds.reshape((len(boxes),1))), axis=1)
    # Get the final detection box results
    det_res = []
    for keep_i in keep:
        det_res.append(dets[keep_i])
    det_res = np.array(det_res)
    # Take the first max_box_num to prevent too many detection boxes
    det_res = det_res[:max_boxes_num, :]
    #------------------------Draw detection box results----------------------------------------
    osd_img.clear()
    # Process each box separately, convert the original image coordinates (AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT) to display screen coordinates (DISPLAY_WIDTH,DISPLAY_HEIGHT)
    for det in det_res:
        x_1, y_1, x_2, y_2 = map(lambda pos: int(round(pos, 0)), det[:4])
        draw_x= int(x_1 * DISPLAY_WIDTH // AI_RGB888P_WIDTH)
        draw_y= int(y_1 * DISPLAY_HEIGHT // AI_RGB888P_HEIGHT)
        draw_w = int((x_2 - x_1) * DISPLAY_WIDTH // AI_RGB888P_WIDTH)
        draw_h = int((y_2 - y_1) * DISPLAY_HEIGHT // AI_RGB888P_HEIGHT)
        osd_img.draw_rectangle(draw_x,draw_y, draw_w, draw_h, color=colors[int(det[5])],thickness=4)
        osd_img.draw_string_advanced( draw_x , max(0,draw_y-50), 24, labels[int(det[5])] + " {0:.3f}".format(det[4]), color=colors[int(det[5])])
    #------------------------Display detection box results on the screen----------------------------------------
    Display.show_image(osd_img)
    print("det fps:",fps.fps())
    gc.collect()

#Exit the loop and release resources
#Note: The while True above has no normal exit, so the release code here will not actually be executed.
#     When writing your own application, please put the main loop in try and the release code below in finally.
ai2d_builder.release()
ai2d.release()
kpu.release()
sensor.stop()
Display.deinit()
time.sleep_ms(50)
MediaManager.deinit()
gc.collect()
nn.shrink_memory_pool()
```

## Running the Example Code

It is recommended to use the CanMV Visual Studio Code extension to open the example program code, and run `CanMV: Run current Python script` to start running the YOLOv8 detection example program. For the use of the CanMV extension, please refer to: **[CanMV Extension Usage Instructions](../../userguide/how_to_use_ide.md)**

The running result is shown in the figure below:

![yolov8_det_result](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/4ce95b9cf643.png)
