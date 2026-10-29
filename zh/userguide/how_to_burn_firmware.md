# 烧录固件

<a id="introduction"></a>

## 概述

本章节将介绍如何将 CanMV 固件烧录到开发板上。

## 固件获取

您可以通过以下链接获取 CanMV-K230 固件：[Github](https://github.com/kendryte/k230_canmv/releases) 或 [嘉楠开发者社区](https://www.kendryte.com/resource)。

请下载文件名以 “CanMV-K230_micropython” 开头的 `.gz` 压缩包，解压后会得到 `xxxxx.img` 文件，该文件即为 CanMV-K230 的固件镜像。

```{admonition} 注意
下载的固件文件通常为 gz 压缩格式，需要解压后才能获得可用于烧录的 img 文件。
```

<a id="how-to-flash-firmware"></a>

## 固件烧录

CanMV/MicroPython 固件与 K230 RTOS 固件使用相同的 USB 烧录流程。烧录模式、USB 驱动、图形界面工具、命令行工具及常见问题，请参考：

[K230 固件烧录指南](https://www.kendryte.com/k230_rtos/zh/main/userguide/how_to_flash.html)

该指南适用于 Windows、Linux 和 macOS，并提供以下三种 K230 专用工具的使用方法：

- `K230BurningTool`（推荐）
- `k230_flash` C++ 命令行工具
- `k230_flash_py` Python 命令行工具和 API

烧录前请先解压下载的 `*.gz` 固件，并根据开发板硬件选择正确的目标介质。使用 TF 卡启动的开发板通常选择 `SDCARD`，具体以开发板说明为准。

## 启动设备

固件成功烧录后，将开发板连接至电脑，系统会自动识别一个名为 `CanMV` 的虚拟 U 盘以及一个虚拟串口。

```{note}
部分开发板需要同时连接 2 条 USB 线。如果没有看到相应的虚拟 U 盘和虚拟串口，请检查连接是否正确。
```

### 在 Windows 系统下查看设备

打开设备管理器，您将看到如下设备：

![conn_succ_windows](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/userguide/images/canmv_connect_succ_windows.png)

- USB 串行设备（COM3）为 MicroPython 的 REPL 串口，也是 CanMV Visual Studio Code 扩展连接开发板时使用的接口。请确保您烧录的固件文件名以 “CanMV-K230_micropython” 开头。

### 在 Linux 系统下查看设备

在 Linux 系统中，串口设备会显示为：

![conn_succ_linux](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/userguide/images/canmv_connect_succ_linux.png)

- `/dev/ttyACM0` 为 MicroPython 的 REPL 串口，也是 CanMV Visual Studio Code 扩展连接开发板时使用的接口。请确保您烧录的固件文件名以 “CanMV-K230_micropython” 开头。
