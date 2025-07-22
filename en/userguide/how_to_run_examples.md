# Running Example Programs

## Overview

Starting from version `V0.5` of K230 CanMV, the virtual USB drive feature is supported. The virtual USB drive comes preloaded with example scripts, allowing users to use them directly without downloading from the internet.

Once the firmware is correctly flashed and successfully started, users can see the virtual USB drive `CanMV` on their computers. Upon opening the virtual USB drive, navigate to the `tests` or `examples` directory (folder names may vary across versions) to find various example programs. Users can select the corresponding script in the IDE, click run, and experience the respective example program.

## Running Example Programs

```{note}
If the IDE is not yet installed, please refer to the [IDE User Guide](./how_to_use_ide.md) for installation instructions.
```

For users with versions prior to K230 CanMV `V0.5`, you can download the test programs from the following link and load them through the IDE: [Test Program Download Link](https://github.com/kendryte/k230_canmv/tree/main/fs_resource/tests).

![Open Script](../../zh/userguide/images/canmv_open_py.png)

Click the "Open" button in the IDE, select the downloaded test file, and open it. Then click the green "Run" button at the bottom left corner, and the program will start executing. After a short wait, the monitor will display images captured by the sensor. This example program is a face detection program, and you will see faces in the image being highlighted.

For versions K230 CanMV `V0.5` and later, it is recommended to use the example programs in the virtual USB drive. After plugging in the development board, open "My Computer" or "This PC" on your computer, and a virtual USB drive named `CanMV` will appear under devices and drives.

![Virtual USB Drive](../../zh/userguide/images/virtual_Udisk.png)

In the virtual USB drive, select and open the desired example script.

![Open Example in Virtual USB Drive](../../zh/userguide/images/open_Udisk.png)

For instance, to run the face detection example, you can find the corresponding script in the `tests` or `examples` directory.

![Face Detection File](../../zh/userguide/images/face_detect_file.png)

After running the program, the monitor will display the AI face detection demonstration results, with faces in the image automatically highlighted and marked.

![CanMV-K230 Face Detection Demo](../../zh/userguide/images/CanMV-K230-aidemo.png)
