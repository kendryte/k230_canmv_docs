# Frequently Asked Questions

## Hardware Issues

### Computer Not Recognizing the Correct USB Device

#### Displaying `K230 USB Boot Device`

When `K230 USB Boot Device` appears, it may be due to the following reasons:

- The startup media has not been flashed with firmware, causing the chip to fail to start and automatically enter USB flashing mode.
- The Boot mode is set incorrectly, causing the chip to fail to read the correct firmware and thus fail to start.

You can force the K230 to enter USB flashing mode by holding down the BOOT button. At this point, `K230 USB Boot Device` will be displayed on the computer, and you can use the [K230 Burning Tool](https://kendryte-download.canaan-creative.com/k230/downloads/burn_tool/) to flash the firmware.

When using `K230 USB Boot Device`, you need to install the corresponding driver through [Zadig](https://zadig.akeo.ie/) to use the flashing tool properly.

#### Displaying Unknown USB Device (Device Descriptor Request Failed)

This situation is usually caused by flashing the wrong firmware, resulting in U-Boot failing to start. Please re-flash the correct firmware and restart the device to resolve this issue.

### How to light up the LED light (WS2812) on CanMV-K230 V1.1

The `CanmV-K230-V1.1` development board needs to modify the hardware to light up the onboard `LED` light

![how-to-fix](https://www.kendryte.com/api/post/attachment?id=435)

## SDK Issues

### IDE Cannot Connect to Canmv-K230 Development Board

1. Ensure that both USB ports of the development board are correctly connected to the computer.
1. Confirm that the firmware flashed on the TF card starts with "CanMV-K230_micropython"; other types of firmware will not connect.
1. Check if "USB Serial Device (COMxx)" is displayed in the computer's Device Manager. If not, try reconnecting the USB cable or using a different USB cable.

### Using the Virtual U Disk

Starting from version V0.5, CanMV supports the virtual U disk function, and the TF card of the development board will be virtualized as a U disk. After the system starts, you will see a device named "CanMV" in the "This PC" section under Devices and Drives. You can operate the TF card like a regular U disk. It stores sample codes for MicroPython, and it is recommended to use these samples first to ensure compatibility with the current image version.

## nncase Issues

(This section to be supplemented)

## AI Demo Issues

(This section to be supplemented)

## IDE Issues

### IDE Displays Low Image Frame Rate

The IDE by default displays 1080P HDMI images transmitted through the VideoOutput module. Due to the limitation of USB transmission speed, the frame rate is only 15-20 FPS.

You can use the `image.compress_for_ide()` function to send specified images. Refer to the camera_480p.py example; the hardware encoder can achieve 30 FPS when sending 480P images. Note that the images must meet the following conditions:

1. The image source must be the vb cache obtained through `sensor.snapshot()`.
1. The physical address of the image buffer must be aligned to 4096.
1. The image format must be YUV420SP, YUV422SP, ARGB8888, or BGRA8888.

If the image does not meet the above requirements, `compress_for_ide()` will use the CPU for encoding, and the frame rate will decrease.

### Methods to Improve Frame Rate

- Select `Displ.VIRT` as the display output device and set an appropriate resolution and frame rate to achieve a higher frame rate.
