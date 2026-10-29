# CanMV-K230D-Zero Development Board

## Overview

The CanMV-K230D Zero development board is jointly designed and developed by Canaan Technology and the Banana Pi open-source community, aiming to explore cutting-edge applications of RISC-V Vector 1.0 technology. This development board integrates the high-performance K230D chip, featuring a dual-core Xuantie C908 RISC-V CPU, and is equipped with Canaan's self-developed third-generation KPU (Neural Network Processing Unit). With onboard 128MB LPDDR4 memory, it provides excellent local inference computing capability. With its compact design and rich development resources, the CanMV-K230D Zero is widely applicable to DIY projects, IoT devices, and embedded system development, making it an ideal choice for learning programming, developing edge AI audio/video products, and conducting performance evaluation.

![Development Board Interface Diagram](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/images/bpi-canmv-k230d-zero_interface.jpg)

## Technical Specifications

| Parameter        | Description                                                                                                                                                              |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **CPU**          | Xuantie C908 Dual-core RISC-V CPU <br> CPU1: 1.6GHz, supports RVV1.0 <br> CPU2: 800MHz                                                                                    |
| **KPU**          | Third-generation Neural Network Processing Unit, supports multiple data types such as INT8/INT16 <br> Typical performance: ResNet50 >= 85fps@INT8, MobileNet_v2 >= 670fps@INT8, YOLOv5s >= 38fps@INT8 |
| **DPU**          | Built-in 3D structured light depth engine, supports up to 1920×1080 resolution                                                                                            |
| **VPU**          | Built-in H.264/H.265 hardware codec                                                                                                                                     |
| **Image Input**  | 2-channel MIPI-CSI (2-lane and 4-lane)                                                                                                                                   |
| **Display Output** | MIPI DSI interface, supports up to 1080P resolution output                                                                                                              |
| **RAM**          | 128MB LPDDR4                                                                                                                                                             |
| **Storage Expansion** | Onboard TF card slot, supports up to 1TB expansion                                                                                                                   |
| **USB**          | 1 USB 2.0 interface, supports OTG function                                                                                                                               |
| **Network**      | Built-in 2.4GHz Wi-Fi module                                                                                                                                             |
| **Audio**        | Supports external audio input/output interface                                                                                                                           |
| **GPIO Expansion** | 40-pin GPIO expansion, supports I2C, UART, I2S, SPI, PWM, ADC, JTAG and other interfaces                                                                                |
| **Buttons**      | 1 function button, 1 reset button                                                                                                                                        |
| **Power**        | USB Type-C interface, input voltage 5V, current 2A                                                                                                                       |
| **Dimensions**   | Length 65mm, width 30mm, height 7mm                                                                                                                                     |

## Connection Diagram

When using the BPI-CanMV-K230D Zero development board, two USB data cables need to be connected simultaneously, one for power supply and the other for serial communication.

![Connection Diagram](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/images/BPI_K230D_Zero_Wire_Connection.jpg)
