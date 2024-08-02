# 5. 进阶-自定义固件

## 1. 概述

```{note}
本章节主要讲述如何进行如何进行K230 CanMV的开发，若无自定义需求可略过本章节
```

K230 CanMV是基于K230 SDK开发的一个运行micropython + OpenMV的应用，用户可通过python语言使用硬件的各种资源。

## 2. 开发环境搭建

| 主机环境 | 描述 |
| --- | --- |
| Docker编译环境 | 提供了dockerfile，可以生成docker镜像，用于编译 |
| Ubuntu 20.04.4 LTS (x86_64) | 可以在ubuntu 20.04环境下编译 |

K230 CanMV需要在linux环境下编译，支持docker环境编译，开发包中发布了docker file（`k230_sdk/tools/docker/Dockerfile`），可以生成docker镜像。具体dockerfile使用和编译步骤，详见4.3.1章节。

K230 CanMV没有在其他Linux版本的主机环境下验证过，不保证可以在其他环境下编译通过。

```{caution}
由于dockerhub无法访问，推荐使用wsl进行环境搭建
```

### 2.1 本地构建环境

- 更新APT源（可选）

```shell
sudo bash -c 'cp /etc/apt/sources.list /etc/apt/sources_bak.list && \
  sed -i "s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
  sed -i "s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list'
```

- 安装软件依赖

```shell
# 添加386 arch
sudo bash -c 'dpkg --add-architecture i386 && \
  apt-get clean all && \
  apt-get update && \
  apt-get install -y --fix-broken --fix-missing --no-install-recommends \
    sudo vim wget curl git git-lfs openssh-client net-tools sed tzdata expect mtd-utils inetutils-ping locales \
    sed make cmake binutils build-essential diffutils gcc g++ bash patch gzip bzip2 perl tar cpio unzip rsync \
    file bc findutils dosfstools mtools bison flex autoconf automake python3 python3-pip python3-dev python-is-python3 \
    lib32z1 scons libncurses5-dev kmod fakeroot pigz tree doxygen gawk pkg-config libyaml-dev libconfuse2 libconfuse-dev \
    libssl-dev libc6-dev-i386 libncurses5:i386'
```

- 更新PIP源（可选）

```shell
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
pip3 config set global.extra-index-url "https://mirrors.aliyun.com/pypi/simple https://mirrors.cloud.tencent.com/pypi/simple"
```

- 安装Python依赖

```shell
pip3 install -U pyyaml pycryptodome gmssl
```

- 编译genimage

```shell

sudo bash -c 'wget https://github.com/pengutronix/genimage/releases/download/v16/genimage-16.tar.xz -O /tmp/genimage-16.tar.xz && \
    tar -xf /tmp/genimage-16.tar.xz -C /tmp; cd /tmp/genimage-16 && \
    ./configure && \
    make -j && \
    make install && \
    cd -; rm -rf genimage*'

# 如果无法访问github,请使用gitee镜像
git clone https://gitee.com/ainiyaoyao/genimage.git -b v16 /tmp/genimage
sudo bash -c 'cd /tmp/genimage && \
    ./autogen.sh && \
    ./configure && \
    make -j && \
    make install && \
    cd -'
```

### 2.2 Docker环境

  在docker环境中编译K230 CanMV，可直接使用如下docker镜像：

- 拉取Docker镜像

  ```shell
  docker pull ghcr.io/kendryte/k230_sdk
  ```

  可使用如下命令确认docker镜像拉取成功：

  ```shell
  docker images | grep k230_sdk
  ```

- 本地构建Docker镜像

```shell
# 生成docker镜像（第一次编译需要，已经生成docker镜像后跳过此步骤，可选）
docker build -f k230_sdk/tools/docker/Dockerfile -t k230_docker k230_sdk/tools/docker
```

- 启动docker环境

```shell
# 启动docker环境(可选)
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/k230_sdk/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash
```

```{note}
docker镜像中默认不包含toolchain，下载源码后，使用命令'make prepare_sourcecode'命令会自动下载toolchain至当前编译目录中。
```

## 3. 编译流程

### 3.1 源码下载

```shell
# 从github下载
git clone https://github.com/kendryte/k230_canmv
# 从gitee下载
git clone https://gitee.com/kendryte/k230_canmv
```

### 3.2 代码准备

```shell
cd k230_canmv

# 推荐切换到dev分支
# git checkout dev

make prepare_sourcecode

# 创建工具链软链接
sudo bash -c 'ln -s `realpath k230_sdk/toolchain` /opt/toolchain'
```

### 3.3 编译

```shell
# 如果在编译过程中遇到git提示需要添加safe.directory按照提示执行指令之后再重新执行make即可

make CONF=k230_canmv_defconfig
```

编译完成后会在`k230_canmv/output/k230_xx_defconfig/images`目录下生成`sysimage-sdcard.img`镜像

## 4. 代码目录说明

```sh
k230_canmv
├── configs
├── fs_resource
├── images
├── k230_sdk
├── k230_sdk_overlay
├── micropython
├── output
└── scripts
```

目录介绍:

1. `configs`: 各种板级配置
1. `fs_resource`: 在编译时拷贝到镜像中的资源文件
1. `k230_sdk`: k230_sdk源码
1. `k230_sdk_overlay`: 基于k230源码的修改
1. `micropython`: micropython的移植
1. `output`: 编译产物结果，镜像文件
1. `scripts`: 各种辅助脚本

其中`k230_sdk`, `micropython`是git submodule, 子项目地址为:

- `k230_sdk`: <https://github.com/kendryte/k230_sdk.git>
- `micropython`: <https://github.com/micropython/micropython.git>

`k230_sdk_overlay`中的目录结构与`k230_sdk`相同, 编译时会将`k230_sdk_overlay`同步到`k230_sdk`
`output`为编译生成目录

`micropython`目录大体如下:

```sh
micropython
├── micropython
├── overlay
├── port
│   ├── 3d-party
│   ├── Kconfig
│   ├── Makefile
│   ├── ai_cube
│   ├── ai_demo
│   ├── boards
│   ├── builtin_py
│   ├── core
│   ├── include
│   ├── kpu
│   ├── lextab.py
│   ├── machine
│   ├── maix
│   ├── modules
│   ├── mpconfigport.h
│   ├── omv
│   ├── socket_network
│   └── yacctab.py
└── sync.mk
```

目录介绍:

1. `micropython`: micropython源码
1. `overlay`: 对micropython源码的一些修改patch
1. `port/boards`: 各种板级配置
1. `port/core`: micropython core模块
1. `port/machine`: machine模块, 包含GPIO, SPI, IIC, UART, PWM, WDT等
1. `port/kpu`: k230 kpu模块, 包含KPU, AI2D
1. `port/mpp`: k230 mpp模块, 包含VO, VI, AI, AO, MMZ, VPU, DPU等
1. `port/maix`: k230 其他模块, 包含IOMUX, PM等
1. `port/omv`: openmv模块
1. `port/include`: 各模块头文件

## 5. 定制固件指南

### 5.1 ramdisk定制

```{important}
K230D 系列不支持`ramdisk`功能
```

#### 5.1.1 ramdisk说明

canmv的rtt大核使用sd卡存储micopython程序，小核linux根文件系统使用initramfs格式。initramfs 是一种内存中的[文件系统](https://www.zhihu.com/search?q=文件系统&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2947632316})，用于在 Linux 内核启动时提供一个[轻量级](https://www.zhihu.com/search?q=轻量级&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2947632316})的临时[根文件系统](https://www.zhihu.com/search?q=根文件系统&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2947632316})，以便能够在根文件系统可用之前执行一些必要的操作。initramfs 通常使用 cpio 工具创建成一个 cpio [归档文件](https://www.zhihu.com/search?q=归档文件&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2947632316})，Linux 内核会读取该文件并将其解压缩到内存中。

ramdisk基本被initramfs取代，因为ramdisk需要ext2等文件系统支持，官方原因如下：

initrd usually functions as a block device, and compiling it into the kernel requires a file system driver such as ext2, ext3, or ext4.

For the kernel to successfully detect the file system of initrd, it must have at least one built-in module available.

All of the common operations of reading and writing on an initrd image are buffered inefficiently to our system’s main memory because the initrd disk has a fixed size.

NOTE: initrd was deprecated and replaced by initramfs.

#### 5.1.2 如何修改

##### 相关脚本修改

```bash
#详见tools/mkcpio-rootfs.sh  
cat tools/mkcpio-rootfs.sh 
#!/bin/bash

find . | cpio -o -H newc > ../rootfs-final.cpio
gzip -f ../rootfs-final.cpio
```

##### 设备树修改

```bash
#k230_sdk_overlay/board/common/gen_image_script/gen_image.sh
ROOTFS_BASE="${RAMDISK_ADDR}"
ROOTFS_SIZE=`ls -lt rootfs-final.cpio.gz | awk '{print $5}'`
((ROOTFS_END= $ROOTFS_BASE + $ROOTFS_SIZE))
ROOTFS_END=`printf "0x%x" $ROOTFS_END`
sed -i "s/linux,initrd-end = <0x0 .*/linux,initrd-end = <0x0 $ROOTFS_END>;/g" hw/k230.dts.txt
#linux,initrd-start = <0x0 0xa100000>;
sed -i "s/linux,initrd-start = <0x0 .*/linux,initrd-start = <0x0  $ROOTFS_BASE>;/g" hw/k230.dts.txt
```

```bash

chosen {
        bootargs = "console=ttyS0,115200  crashkernel=256M-:128M earlycon=sbi";
        stdout-path = "/soc/serial@91400000:115200";
        linux,initrd-start = <0x00 0xa100000>;
        linux,initrd-end = <0x00 0xaa8b186>;
};
```

#### 5.1.3 验证

```bash
#mount
 rootfs on / type rootfs (rw,size=48000k,nr_inodes=12000)
 devtmpfs on /dev type devtmpfs (rw,relatime,size=48000k,nr_inodes=12000,mode=755)
 proc on /proc type proc (rw,relatime)
 devpts on /dev/pts type devpts (rw,relatime,gid=5,mode=620,ptmxmode=666)
 tmpfs on /dev/shm type tmpfs (rw,relatime,mode=777)
 tmpfs on /tmp type tmpfs (rw,relatime)
 tmpfs on /run type tmpfs (rw,nosuid,nodev,relatime,mode=755)
 sysfs on /sys type sysfs (rw,relatime)
```

可以看出根文件系统不是ext4。

#### 5.1.4 参考资料

<https://www.zhihu.com/question/558974598/answer/2712616024>

<https://www.baeldung.com/linux/initrd-vs-initramfs>

### 5.2 其他定制

```{admonition} TODO
TODO
```
