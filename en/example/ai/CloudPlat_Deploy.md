# Cloud training platform model deployment

> Warning: This page is translated by MACHINE, which may lead to POOR QUALITY or INCORRECT INFORMATION, please read with CAUTION!

## Introduction to the cloud training platform

The Canaan developer community model training function is an open training platform to simplify the development process and improve development efficiency. The platform allows users to pay attention to the implementation of visual scenes, and complete the process from data annotation to obtaining the KModel model in the deployment package more quickly, and deploy it on the K230 and K230D chip development boards equipped with Canaan Technology Kendryte® series AIoT chips. Users only need to upload the data set and simply configure the parameters to start training.

 ![plat](https://www.kendryte.com/api/post/attachment?id=600)

📌Platform address:**[Canaan Cloud Training Platform](https://www.kendryte.com/zh/training/start)**

📌Platform usage documentation reference:**[Canaan Cloud Training Platform Document Tutorial](https://www.kendryte.com/web/CloudPlatDoc.html)**, please pay attention to the format of the dataset!

## Support task introduction

There are 7 visual tasks supported by the K230 series chips in the cloud training platform, and the task introduction is as follows:

💡 **Task introduction**:

| Task name                  | Task description                                                                                                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Image classification       | Classify the pictures and get the category results and scores of the pictures.                                                                                                                                            |
| Image detection            | The target object is detected in the picture, and the position information, category information and score of the object are given.                                                                                       |
| Semantic segmentation      | The target area in the picture is segmented and the different label areas in the picture are cut out, which is a pixel-level task.                                                                                        |
| OCR detection              | The text area is detected in the picture and the location information of the text area is given.                                                                                                                          |
| OCR recognition            | Recognize text content in the picture.                                                                                                                                                                                    |
| Metric learning            | Training a model that characterizes the image, uses the model to create a feature library, and classifies new categories without retraining the model through feature comparison, which can also be called self-learning. |
| Multi-label classification | Classify pictures in multiple categories. Some pictures may not just belong to a single category. The sky and the sea can exist at the same time to obtain the multi-label classification results of the pictures.        |

## Deployment steps

## Deployment Package Description

After training, you can download the deployment package corresponding to the training task. After the downloaded deployment zip package is decompressed, the directory is as follows:

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

The content is shown in the picture:

 ![Deployment package](https://www.kendryte.com/api/post/attachment?id=597)

in `mp_deployment_source.zip` that is, the code package deployed on the K230 MicroPython image, which internally contains the deployed configuration files and the deployed KModel model.

## File copy

✅ **Firmware selection**: Please `github` download the latest ones according to your development board type [PreRelease firmware](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) to ensure **Latest features** being supported! Or use the latest code to compile the firmware yourself. See the tutorial:[Firmware Compilation](../../userguide/how_to_build.md).

✅ **Firmware burn**: Burn firmware according to the development board type, firmware burn reference:[Firmware burn](../../userguide/how_to_burn_firmware.md).

✅ **Deploy the script**: After the firmware is successfully burned, power on and power on. You can find it in the root directory of the file system `CanMV/sdcard` directory,`mp_deployment_source.zip` copy to decompress `CanMV/sdcard` in the directory.

## Script running

Open CanMV IDE K230 and select the upper left corner `File (F)`->`Open the file`->`Select CanMV/sdcard/examples/19-CloudPlatScripts` scripts in different tasks run.

💡 **Script introduction**:

| Script name            | Script Description                                                                                                                                                                                                                                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| deploy_cls_image.py    | For image classification single image inference script, you need to add test images yourself and modify the path to read the image in the script.                                                                                                                                                                        |
| deploy_cls_video.py    | Image classification video stream inference script, please refer to the comments in the script for details.                                                                                                                                                                                                              |
| deploy_det_image.py    | In an object detection single-image inference script, you need to add test images yourself and modify the path to read the image in the script.                                                                                                                                                                          |
| deploy_det_video.py    | Object detection video stream inference script, please refer to the comments in the script for details.                                                                                                                                                                                                                  |
| deploy_seg_image.py    | In a semantic segmentation single-graphic inference script, you need to add test images yourself and modify the path to read the image in the script.                                                                                                                                                                    |
| deploy_seg_video.py    | Semantic segmentation video stream inference script, see the comments in the script for details.                                                                                                                                                                                                                         |
| deploy_ocrdet_image.py | OCR detects single-image inference scripts, you need to add test images yourself and modify the path to read them into the image.                                                                                                                                                                                        |
| deploy_ocrdet_video.py | OCR detects video stream inference scripts, see the comments in the script for details.                                                                                                                                                                                                                                  |
| deploy_ocrrec_image.py | OCR recognizes single-picture inference scripts. You need to add test images yourself and modify the path to read them into the image. Considering that the data read in a single inference by the platform OCR recognition model is long strip text, therefore **Not supported** video stream reasoning.                |
| deploy_ocr_image.py    | For OCR single-picture inference script, you need to add test images yourself and modify the path to read them into the image. For dual-model tasks, it is necessary to add deployment packages for OCR detection and OCR recognition at the same time, and pay attention to modifying the directory path in the script. |
| deploy_ocr_video.py    | OCR video stream inference script, please refer to the comments in the script for details. For dual-model tasks, it is necessary to add deployment packages for OCR detection and OCR recognition at the same time, and pay attention to modifying the directory path in the script.                                     |
| deploy_ml_image.py     | To measure learning single-graphic inference scripts, you need to add test images yourself and modify the path to read them into the image. The output is the features of the corresponding dimension, and subsequent operations are modified according to the application scenario.                                     |
| deploy_ml_video.py     | Measuring learning video stream inference scripts, please refer to the comments in the script for details. The output is the features of the corresponding dimension, and subsequent operations are modified according to the application scenario.                                                                      |
| deploy_multl_image.py  | For multi-label classification single-picture inference script, you need to add test images yourself and modify the path to read them into the image.                                                                                                                                                                    |
| deploy_multl_video.py  | Multi-label classified video stream inference scripts, please refer to the comments in the script for details.                                                                                                                                                                                                           |

## Deployment Instructions

- 📢 If the effect is not ideal when deploying the model, first adjust the threshold of the corresponding task and the resolution of the inference image to see if the test results can improve!

- 📢 Learn to locate problems, such as viewing and deploying packages `**_results` if the test picture in the directory is normal, it may be a problem with the deployment code, model conversion or threshold!

- 📢 Adjust the parameters of model training, such as `epoch`,`learning_rate` wait to prevent insufficient training!

- 📢 If the online training platform cannot meet your requirements, you can choose to use open source models such as YOLO to complete the training, and specify the appropriate model size and input resolution during training. For the YOLO tutorial, see: **[K230 YOLO Battle](./YOLO_Battle.md)**!
