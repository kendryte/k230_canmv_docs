# 使用 CanMV Visual Studio Code 扩展

<a id="introduction"></a>

## 概述

推荐使用 **CanMV for Visual Studio Code** 扩展进行 CanMV K230 开发。扩展将连接开发板、运行 MicroPython 脚本、预览图像、管理设备文件、查看终端输出和浏览示例等常用能力集成到 Visual Studio Code 中，适合作为 CanMV IDE / OpenMV IDE 的日常替代工具。

![CanMV for Visual Studio Code](https://raw.githubusercontent.com/kendryte/canmv-vscode-extension/main/extension/resources/demo.gif)

相比传统 IDE，CanMV 扩展提供：

1. 在 Visual Studio Code 中编辑、运行和停止脚本。
1. 通过 `CanMV Terminal` 查看输出，并在无脚本运行时使用 REPL。
1. 在 `Device` 视图中浏览 `/sdcard`、`/data`、`/udisk`，并上传、下载、编辑和同步文件。
1. 通过 `Preview` 查看 IDE 帧缓冲图像，支持截图、旋转、像素读取、ROI 直方图和录制。
1. 通过 `Examples` 视图下载并运行与固件资源匹配的官方示例。
1. 自动配置 K230 MicroPython stubs，为 Pylance 提供代码补全和类型提示。

```{note}
本文面向从 CanMV IDE / OpenMV IDE 迁移到 CanMV Visual Studio Code 扩展的用户。使用扩展连接开发板前，请关闭旧版 IDE，避免串口被其他程序占用。
```

## 安装扩展

1. 安装 Visual Studio Code `1.90.0` 或更高版本。
1. 在 Visual Studio Code 的扩展视图中搜索并安装 `CanMV` 扩展。
1. 如果使用离线 VSIX 包，可在命令面板运行 `Extensions: Install from VSIX...` 进行安装。
1. Pylance 会作为扩展依赖自动安装，用于 Python 代码分析。

扩展源码和更多说明可参考 [canmv-vscode-extension](https://github.com/kendryte/canmv-vscode-extension)。

## 连接开发板

将 CanMV K230 开发板通过 USB 连接到电脑，然后在 Visual Studio Code 中执行以下任一操作：

1. 打开命令面板，运行 `CanMV: 连接开发板`。
1. 点击侧边栏中的 CanMV 图标，在 `Controls` 视图中点击连接按钮。

扩展默认会通过 USB VID/PID `1209:abd1` 自动检测开发板。连接成功后，CanMV 活动栏会显示开发板状态，`Device` 视图会刷新设备文件，`CanMV Terminal` 面板会显示开发板输出。

如果自动检测失败，可在 Visual Studio Code 设置中配置：

```text
canmv.serialPath
```

例如 Linux 常见路径为 `/dev/ttyACM0`，macOS 常见路径为 `/dev/cu.usbmodem*`。手动设置串口后，扩展会使用 `canmv.baudRate` 连接开发板。

## 运行 Python 代码

打开一个 Python 文件后，可以通过以下方式运行：

1. 命令面板运行 `CanMV: 运行当前 Python 脚本`。
1. 使用编辑器右上角的运行按钮。
1. 在编辑器右键菜单中选择 `CanMV: 在 K230 上运行当前文件`。

脚本运行时，`CanMV Terminal` 会显示脚本输出，运行按钮会切换为停止状态。需要中断脚本时，可运行 `CanMV: 停止脚本`，或在 `CanMV Terminal` 中按 `Ctrl-C`。

## 预览图像

从 CanMV 活动栏的 `Toolbox` 打开 `Preview`，或在命令面板运行 `CanMV: 启用预览`。当脚本向 IDE 帧缓冲输出图像时，扩展会在预览窗口中显示实时画面。

原来在 CanMV IDE 中使用的图像预览代码可以继续使用，例如：

1. `Display.init(..., to_ide=True)` 将显示输出同步到 IDE 帧缓冲。
1. `image` 对象调用 `compress_for_ide()` 将指定图像发送到 IDE 帧缓冲。

`Preview` 工具支持适应窗口、原始尺寸、旋转、保存 PNG、像素 RGB 读取、FPS 显示、ROI 直方图、RGB/灰度/LAB/YUV 直方图、视频录制，以及固件支持时的虚拟触控。

## 管理开发板文件

连接开发板后，打开 CanMV 活动栏中的 `Device` 视图即可管理设备文件。常用操作包括：

1. 展开 `/sdcard`、`/data`、`/udisk` 等挂载目录。
1. 新建文件或文件夹。
1. 上传本地文件或文件夹。
1. 下载、重命名或删除设备文件。
1. 打开设备上的 Python 文件，编辑后保存会自动同步回开发板。

如果需要设置开机脚本，可在编辑器右键菜单中选择：

1. `CanMV: 另存为 main.py`，将当前文件写入 `/sdcard/main.py`。
1. `CanMV: 另存为 boot.py`，将当前文件写入 `/sdcard/boot.py`。

## 使用示例和代码提示

扩展会根据固件资源清单下载匹配的示例和 K230 MicroPython stubs。连接开发板后，可打开 CanMV 活动栏中的 `Examples` 视图浏览官方示例。

常用操作包括：

1. 运行 `CanMV: 刷新示例` 下载或更新示例缓存。
1. 从 `Examples` 视图打开示例，扩展会以可编辑的未保存文件打开，避免修改本地缓存。
1. 右键 Python 示例并选择运行，可直接在已连接开发板上执行。

示例缓存位于：

```text
~/.kendryte/k230_canmv_examples/<examples-id>
```

stubs 缓存位于：

```text
~/.kendryte/k230_canmv_stubs/<firmware-revision>
```

扩展会将当前 stubs 路径写入 `python.analysis.extraPaths`，使 Pylance 能够提供更准确的补全和诊断。

## 从 CanMV IDE 迁移

| CanMV IDE / OpenMV IDE 操作 | CanMV Visual Studio Code 扩展中的对应操作 |
| --- | --- |
| 点击左下角连接按钮 | 运行 `CanMV: 连接开发板`，或使用 CanMV `Controls` 视图 |
| 打开本地 Python 文件并运行 | 打开文件后运行 `CanMV: 运行当前 Python 脚本` |
| 点击停止按钮 | 运行 `CanMV: 停止脚本`，或在 `CanMV Terminal` 中按 `Ctrl-C` |
| 查看串口输出 | 打开 `CanMV Terminal` 面板 |
| 保存为 `main.py` | 右键编辑器并选择 `CanMV: 另存为 main.py` |
| 保存文件到开发板 | 在 `Device` 视图中上传文件，或打开远程文件后保存同步 |
| 浏览开发板文件 | 使用 `Device` 视图 |
| 打开示例程序 | 使用 `Examples` 视图，或从虚拟 U 盘/本地目录打开 Python 文件 |
| 查看 IDE 图像窗口 | 打开 `Preview` 工具 |
| 使用阈值编辑器 | 从 `Toolbox` 打开 `Threshold Editor` |

## 常见问题

### 无法连接开发板

确认 USB 线支持数据传输，开发板已正常上电，并关闭其他可能占用串口的软件。Linux 用户还需确认当前用户有串口访问权限。仍无法自动检测时，请手动设置 `canmv.serialPath`。

### 预览窗口没有图像

确认脚本正在运行，并且脚本会向 IDE 帧缓冲输出图像，例如使用 `Display.init(..., to_ide=True)` 或 `compress_for_ide()`。如果脚本已运行但仍无图像，请打开 `CanMV` 输出通道查看预览和后端日志。

### 设备文件无法显示

请先确认开发板已连接且状态为就绪，然后运行 `CanMV: 刷新资源管理器`。如果固件版本过旧或不支持远程文件能力，请更新到较新的 CanMV K230 固件。
