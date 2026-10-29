# Cloud Training Platform Model Deployment

## Cloud Training Platform Introduction

The Canaan Developer Community model training feature is a training platform opened up to simplify the development process and improve development efficiency. This platform enables users to focus on the implementation of visual scenarios, more quickly complete the process from data annotation to obtaining the KModel in the deployment package, and deploy on K230 and K230D chip development boards equipped with Canaan Technology's Kendryte® series AIoT chips. Users only need to upload datasets and simply configure parameters to start training.

![plat](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/04792fdbd787.png)

📌Platform URL: **[Canaan Cloud Training Platform](https://www.kendryte.com/zh/training/start)**

📌Platform usage documentation reference: **[Canaan Cloud Training Platform Documentation Tutorial](https://www.kendryte.com/web/CloudPlatDoc.html)**, please pay attention to the format of the dataset!

## Supported Tasks Introduction

The cloud training platform supports 7 visual tasks for the K230 series chips. The task introductions are shown in the table below:

💡 **Task Introduction**:

| Task Name | Task Description |
| ----- | --------------------------------------------------------------------------------------------------------------------- |
| Image Classification | Classify images and obtain the category result and score of the image. |
| Image Detection | Detect target objects in the image and provide position information, category information, and score of the object. |
| Semantic Segmentation | Segment the target area in the image and cut out different labeled areas in the image, which is a pixel-level task. |
| OCR Detection | Detect text areas in the image and provide the position information of the text areas. |
| OCR Recognition | Recognize text content in the image. |
| Metric Learning | Train a model that can characterize images, use this model to create a feature library, and classify new categories without retraining the model through feature comparison, also known as self-learning. |
| Multi-label Classification | Perform multi-category classification on images. Some images may not only belong to a single category, sky and sea can exist simultaneously, and obtain multi-label classification results of the image. |

## Deployment Steps

## Deployment Package Description

After training is completed, you can download the deployment package for the corresponding training task. After extracting the downloaded deployment zip package, the directory is as follows:

```shell
📦 task_name
├── 📁 **_result
│   ├── test_0.jpg
│   ├── test_1.jpg
│   └──...
├── cpp_deployment_source.zip
├── mp_deployment_source.zip
└── README.md
```

The content is shown in the figure:

![Deployment Package](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/1c2cef01a930.png)

Among them, `mp_deployment_source.zip` is the code package deployed on the K230 MicroPython image, which internally contains the deployment configuration file and the deployed KModel.

## File Copy

✅ **Firmware Selection**: Please download the latest [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) on `github` according to your development board type to ensure that the **latest features** are supported! Or compile the firmware yourself using the latest code. For the tutorial, see: [Firmware Compilation](../../userguide/how_to_build.md).

✅ **Firmware Burning**: Burn the firmware according to the development board type. For firmware burning reference: [Firmware Burning](../../userguide/how_to_burn_firmware.md).

✅ **Deployment Script**: After the firmware is successfully burned, power on and start up. You can find the `CanMV/sdcard` directory in the root directory of the file system. Extract `mp_deployment_source.zip` and copy it to the `CanMV/sdcard` directory.

## Script Running

Open CanMV IDE K230, select `File (F)`->`Open File`->Select different task scripts in `CanMV/sdcard/examples/19-CloudPlatScripts` to run.

💡 **Script Introduction**:

|Script Name|Script Description|
|--|--|
|deploy_cls_image.py|Image classification single image inference script. You need to add test images by yourself and modify the path of the image read in the script.|
|deploy_cls_video.py|Image classification video stream inference script. For script details, see the comments in the script.|
|deploy_det_image.py|Target detection single image inference script. You need to add test images by yourself and modify the path of the image read in the script.|
|deploy_det_video.py|Target detection video stream inference script. For script details, see the comments in the script.|
|deploy_seg_image.py|Semantic segmentation single image inference script. You need to add test images by yourself and modify the path of the image read in the script.|
|deploy_seg_video.py|Semantic segmentation video stream inference script. For script details, see the comments in the script.|
|deploy_ocrdet_image.py|OCR detection single image inference script. You need to add test images by yourself and modify the path of the image read in the script.|
|deploy_ocrdet_video.py|OCR detection video stream inference script. For script details, see the comments in the script.|
|deploy_ocrrec_image.py|OCR recognition single image inference script. You need to add test images by yourself and modify the path of the image read in the script. Considering that the data input for a single inference of the platform OCR recognition model is long strip text, **video stream inference is not supported**.|
|deploy_ocr_image.py|OCR single image inference script. You need to add test images by yourself and modify the path of the image read in the script. Dual model task requires adding deployment packages for OCR detection and OCR recognition at the same time, pay attention to modifying the directory path in the script.|
|deploy_ocr_video.py|OCR video stream inference script. For script details, see the comments in the script. Dual model task requires adding deployment packages for OCR detection and OCR recognition at the same time, pay attention to modifying the directory path in the script.|
|deploy_ml_image.py|Metric learning single image inference script. You need to add test images by yourself and modify the path of the image read in the script. The output is the feature of the corresponding dimension, and subsequent operations are modified according to the application scenario.|
|deploy_ml_video.py|Metric learning video stream inference script. For script details, see the comments in the script. The output is the feature of the corresponding dimension, and subsequent operations are modified according to the application scenario.|
|deploy_multl_image.py|Multi-label classification single image inference script. You need to add test images by yourself and modify the path of the image read in the script.|
|deploy_multl_video.py|Multi-label classification video stream inference script. For script details, see the comments in the script.|

## Deployment Notes

- 📢 If the effect is not ideal when deploying the model, first adjust the threshold of the corresponding task and the resolution of the inference image, and test whether the results can improve!

- 📢 Learn to locate the problem, such as checking the test images in the `**_results` directory of the deployment package. If the image is normal, the problem may be with the deployment code, model conversion, or threshold!

- 📢 Adjust the parameters of model training, such as `epoch`, `learning_rate`, etc., to prevent insufficient training!

- 📢 If the online training platform cannot meet your requirements, you can choose to use open source models such as YOLO to complete the training, and specify the appropriate model size and input resolution during training. For YOLO tutorial, see: **[K230 yolo_battle](./yolo_battle.md)**!
