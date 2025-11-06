# K230 ADB使用指南

## ADB功能说明

K230支持Android Debug Bridge (ADB)功能，提供了设备调试和文件传输的能力。通过ADB，开发者可以在PC端与K230设备进行交互，包括执行shell命令、传输文件等。ADB功能特别适用于：

- 远程调试和日志查看
- 应用程序部署和测试
- 文件上传和下载

## ADB配置说明

### 板端功能配置

```bash
make rtsmart-menuconfig

# 找到对应的配置项
Components Configuration > Enable CherryUSB > Enable CherryUSB Device

# 选择打开功能
选择 CDC + ADB 或者 ADB
```

![ENABL ADB](https://www.kendryte.com/api/post/attachment?id=770)

### 主机环境配置

#### Windows环境

1. 下载Android SDK Platform Tools：
   - 访问Android开发者官网
   - 下载对应平台的platform-tools压缩包

1. 解压并配置环境变量：

```shell
   # 将platform-tools目录添加到系统PATH环境变量中
   C:\path\to\platform-tools
```

1. 验证安装：

```cmd
   adb version
```

#### Linux环境

```bash
# Ubuntu/Debian系统
sudo apt update
sudo apt install android-tools-adb

# 或者下载platform-tools
wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
unzip platform-tools-latest-linux.zip
export PATH=$PATH:$(pwd)/platform-tools
```

## ADB 命令说明

### 设备连接验证

连接设备后，在PC端执行以下命令验证连接：

```cmd
# 查看连接的设备列表
adb devices

# 预期输出：
# List of devices attached
# 001000000    device
```

### ADB Shell

#### 进入交互式shell

```cmd
adb shell
```

#### 在shell中执行单个命令

##### 基本语法

```cmd
adb shell <command>
```

##### 使用示例

```cmd
# 查看内存使用情况
adb shell free
```

### ADB文件传输

#### adb push - 上传文件到设备

##### 基本语法

```cmd
adb push <local_file_path> <remote_file_path>
```

##### 使用示例

```cmd
# 上传单个文件
adb push C:\Users\user\test.txt /tmp/test.txt

# 上传文件并重命名
adb push ./local_config.json /tmp/config.json

# 上传到特定目录
adb push ./app.bin /tmp
```

#### adb pull - 下载文件到PC

##### 基本语法

```cmd
adb pull <remote_file_path> [local_file_path]
```

##### 使用示例

```cmd
# 下载单个文件
adb pull /tmp/syslog ./logs/

# 下载并重命名
adb pull /tmp/debug.log ./debug_backup.log

# 下载到当前目录
adb pull /home/user/config.json ./
```

## 注意事项

1. 文件传输功能只支持单个文件，不支持传输目录。
1. 使用过程突然发现adb掉线了，可能是动到了 USB 线，需要晃动插紧 USB 线。
