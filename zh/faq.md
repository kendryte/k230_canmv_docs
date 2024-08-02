# 常见问题解答

## 1.硬件类问题解答

## 2.SDK类问题解答

### 2.1 IDE无法连接Canmv-K230开发板

1、请确定开发板两个USB口都与电脑连接。
![CanMV-K230-poweron](images/CanMV-K230-poweron.png)

2、TF卡烧录的固件是“CanMV-K230_micropython”开头的固件，烧录其它的固件也无法连接。

3、查看电脑的设备管理器
![CanMV-K230-micropython-serial](userguide/images/CanMV-K230-micropython-serial.png)

是否有"USB串行设备(COMxx)的设备，如果没有请重新插拔USB。如果还没有，则请更换USB线。

### 2.2 虚拟U盘在哪？如何使用？

V0.5版本后的Canmv镜像支持虚拟U盘，即将板子的TF虚拟为U盘，可以像U盘一样对TF进行操作。系统正常启动后会在“我的电脑”或“此电脑”，在设备和驱动器中会出现“CanMV"设备。
![virtual_Udisk](userguide/images/virtual_Udisk.png)

将其做为普通的U盘即可。默认里面会存储micropython的示例，建议使用这里面的示例，可以保证镜像与示例版本一致。

## 3.nncase类问题解答

## 4.AI demo类问题解答

## 5.IDE 类问题解答

### 5.1 IDE 显示的图像帧率很低

IDE 显示图像默认来源是 VideoOutput 模块的回显，在使用HDMI时固定为1080P，由于USB传输速率限制，此时的帧率只能达到15~20FPS。

使用 image.compress_for_ide() 可以发送指定的图像，参考示例中的 camera_480p.py，使用硬件编码器发送 480P 图像时可以达到30FPS，需要注意硬件编码器对图像有一定要求，总的来说有一下几点

1. 图像来源必须是vb（通过 sensor.snapshot() 获得的图像满足这一要求）
1. 图像 buffer 的所有 planer 物理地址必须对齐 4096（通过 sensor.snapshot() 获得的图像满足这一要求）
1. 图像的格式必须为 YUV420SP/YUV422SP/ARGB8888/BGRA8888 这四种

如果图像不满足以上要求，那么 compress_for_ide 会使用 CPU 进行编码，此时帧率可能比较低。

### 5.2 Workaround

1. 显示输出设备选择`Displ.VIRT`，可以设置分辨率及帧率，可以获得较高的帧率
