# K230 CanMV ramdisk使用说明

![cover](images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍小核ramdisk的使用。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| MV  | Machine Vision   |
| initrd | initial RAM disk |
| initramfs | initial RAM File System |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 王建新   | 2023-09-18 |

## 1. 说明

canmv的rtt大核使用sd卡存储micopython程序，小核linux根文件系统使用initramfs格式。initramfs 是一种内存中的[文件系统](https://www.zhihu.com/search?q=文件系统&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2947632316})，用于在 Linux 内核启动时提供一个[轻量级](https://www.zhihu.com/search?q=轻量级&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2947632316})的临时[根文件系统](https://www.zhihu.com/search?q=根文件系统&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2947632316})，以便能够在根文件系统可用之前执行一些必要的操作。initramfs 通常使用 cpio 工具创建成一个 cpio [归档文件](https://www.zhihu.com/search?q=归档文件&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2947632316})，Linux 内核会读取该文件并将其解压缩到内存中。

ramdisk基本被initramfs取代，因为ramdisk需要ext2等文件系统支持，官方原因如下：

initrd usually functions as a block device, and compiling it into the kernel requires a file system driver such as ext2, ext3, or ext4.

For the kernel to successfully detect the file system of initrd, it must have at least one built-in module available.

All of the common operations of reading and writing on an initrd image are buffered inefficiently to our system’s main memory because the initrd disk has a fixed size.

NOTE: initrd was deprecated and replaced by initramfs.

## 2. 主要脚本介绍

### 2.1initramfs生成脚本

```bash
#详见tools/mkcpio-rootfs.sh  
cat tools/mkcpio-rootfs.sh 
#!/bin/bash

find . | cpio -o -H newc > ../rootfs-final.cpio
gzip -f ../rootfs-final.cpio
```

### 2.2设备树关于initramfs修改

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

## 3.验证

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

## 4.参考资料

<https://www.zhihu.com/question/558974598/answer/2712616024>

<https://www.baeldung.com/linux/initrd-vs-initramfs>
