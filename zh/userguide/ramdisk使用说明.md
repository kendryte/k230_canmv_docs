# 4.ramdisk使用说明

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

