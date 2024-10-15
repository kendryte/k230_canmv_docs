# 常见问题解答

## 1. 硬件问题

### 1.1 电脑未识别正确的 USB 设备

#### 1.1.1 显示 `K230 USB Boot Device`

当出现 `K230 USB Boot Device` 时，可能是由以下原因造成的：

- 启动介质中未烧录固件，导致芯片启动失败，自动进入 USB 烧录模式。
- Boot 模式设置不正确，导致芯片无法读取到正确的固件，从而启动失败。

您可以通过按住 BOOT 按键强制 K230 进入 USB 烧录模式，此时电脑上将显示 `K230 USB Boot Device`，您可以使用 [K230 Burning Tool](https://kendryte-download.canaan-creative.com/k230/downloads/burn_tool/) 烧录固件。

在使用 `K230 USB Boot Device` 时，需要通过 [Zadig](https://zadig.akeo.ie/) 安装相应的驱动，以便正常使用烧录工具。

#### 1.1.2 显示未知 USB 设备（设备描述符请求失败）

这种情况通常是由于烧录了错误的固件，导致 U-Boot 启动失败。请重新烧录正确的固件并重启设备，以解决该问题。

### 1.2 CanMV-K230 V1.1 如何点亮LED灯(WS2812)

`CanmV-K230-V1.1` 开发板需要修改硬件才可以点亮板载`LED`灯

![how-to-fix](https://developer.canaan-creative.com/api/post/attachment?id=435)

## 2. SDK 问题

### 2.1 IDE 无法连接 Canmv-K230 开发板

1. 确保开发板的两个 USB 接口均与电脑正确连接。
1. 确认 TF 卡中烧录的固件以 “CanMV-K230_micropython” 开头，其他类型的固件将无法连接。
1. 检查电脑的设备管理器中是否显示 “USB 串行设备 (COMxx)” ，若未显示，请尝试重新插拔 USB 线或更换 USB 线。

### 2.2 虚拟 U 盘的使用

自 V0.5 版本起，CanMV 支持虚拟 U 盘功能，开发板的 TF 卡将被虚拟为 U 盘。在系统启动后，您将在“此电脑”的设备与驱动器中看到名为“CanMV”的设备。您可以像使用普通 U 盘一样操作 TF 卡，其中存储了 MicroPython 的示例代码，建议优先使用这些示例以确保与当前镜像版本匹配。

## 3. nncase 问题

（此部分待补充）

## 4. AI demo 问题

（此部分待补充）

## 5. IDE 问题

### 5.1 IDE 显示图像帧率低

IDE 默认显示通过 VideoOutput 模块回传的 1080P HDMI 图像，由于 USB 传输速率的限制，帧率仅为 15-20 FPS。

您可以使用 `image.compress_for_ide()` 函数发送指定图像。参见 camera_480p.py 示例，硬件编码器在发送 480P 图像时可达 30 FPS。需注意，图像必须满足以下条件：

1. 图像来源必须通过 `sensor.snapshot()` 获取的 vb 缓存。
1. 图像 buffer 的物理地址需对齐到 4096。
1. 图像格式必须为 YUV420SP、YUV422SP、ARGB8888 或 BGRA8888。

若图像不满足上述要求，`compress_for_ide()` 将使用 CPU 进行编码，帧率将会降低。

### 5.2 提高帧率的方法

- 选择 `Displ.VIRT` 作为显示输出设备，并设置合适的分辨率和帧率，以获得更高的帧率。
