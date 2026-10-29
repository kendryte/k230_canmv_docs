# 进阶 - 自定义固件

```{note}
本章节介绍如何在 K230 CanMV 上进行开发。如果您没有自定义需求，可跳过此章节。
```

## 概述

K230 CanMV 是基于 K230 SDK 开发的 Micropython + OpenMV 应用平台，用户可通过 Python 语言调用硬件资源。本文档提供两种构建方式：

- **使用 Docker 编译**（推荐）：无需安装任何编译依赖，一条命令即可完成编译
- **直接本机编译**：在 Ubuntu 20.04 上手动搭建环境

## 使用 Docker 编译（推荐）

使用预配置的 [k230-builder](https://github.com/huangzhenming/k230-builder) 镜像，内置全部工具链、repo、genimage 及所有编译依赖。前提条件仅需安装 Docker。

### 前提条件

- **安装 Docker**

  ```bash
  # Ubuntu/Debian
  sudo apt install docker.io
  sudo usermod -aG docker $USER && newgrp docker
  ```

  其他系统参考 [Docker 官方文档](https://docs.docker.com/engine/install/)。

- **配置 Gitee SSH 密钥**（代码下载需要）
  在 [Gitee](https://gitee.com) 注册账号并[添加 SSH 公钥](https://gitee.com/profile/sshkeys)。

- **配置 Git 用户信息**

  ```bash
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
  ```

### 安装 k230 命令

```bash
curl -fsSL https://www.kendryte.com/misc/install.sh | bash
source ~/.bashrc
```

安装后执行 `k230 pull` 拉取 Docker 镜像（首次耗时取决于网络，约 1GB+）。

### 快速开始

```bash
# 1) 创建工作目录
mkdir -p ~/canmv_k230 && cd ~/canmv_k230

# 2) 拉取 docker 镜像
k230 pull

# 3) 下载工具链（仅需首次执行一次）
k230 download-toolchains TC1 TC3

# 4) 下载代码（容器内置 repo，自动挂载宿主 SSH 密钥）
# 从 Gitee 下载（推荐国内用户，需 SSH 密钥）
k230 repo init -u git@gitee.com:canmv-k230/manifest.git --repo-url=git@gitee.com:canmv-k230/git-repo.git

# 从 GitHub 下载（国际用户）
# k230 repo init -u https://github.com/canmv-k230/manifest --repo-url=https://github.com/canmv-k230/git-repo.git --repo-branch stable

k230 repo sync -j$(nproc)

# 5) 选择板级配置并编译
k230 make list-def                      # 查看所有板级配置
k230 make k230_canmv_01studio_defconfig # 选择目标板子
k230 make

# 6) 查看输出镜像
ls -lh output/k230_canmv_01studio_defconfig/images/
```

### 常用命令

```bash
k230 list-toolchains                  # 查看可用工具链列表
k230 make                             # 编译（增量构建）
k230 make list-def                    # 查看所有板级配置
k230 make menuconfig                  # 交互式配置
k230 bash                             # 进入容器终端
k230 repo sync -j$(nproc)             # 更新代码
k230 pull                             # 更新 k230-builder 镜像
```

### Git 与 SSH

`k230` 自动挂载宿主 `~/.ssh` 和 `~/.gitconfig` 到容器，`repo init` / `git clone` 直接可用，无需额外配置。

### 宿主机网络受限

如果 ghcr.io 不可达（国内常见），`k230` 自动切换 `registry.kendryte.com` 镜像源。手动指定版本：

```bash
K230_BUILDER_TAG=dev k230 make
```

---

## 直接本机编译

> 推荐使用 Docker 编译。仅在无法使用 Docker 时，参考以下手动搭建流程。

### 系统要求

- **操作系统**：Ubuntu 20.04 LTS (x86_64)
- **内存**：≥ 2GB
- **磁盘**：≥ 10GB

### 配置 APT 源（可选，推荐国内用户）

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources_bak.list
sudo sed -i "s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list
sudo sed -i "s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list
sudo apt update
```

### 安装系统依赖

```bash
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install -y --no-install-recommends \
    sudo vim wget curl git git-lfs openssh-client net-tools sed tzdata expect \
    mtd-utils inetutils-ping locales \
    make cmake binutils build-essential gcc g++ bash patch perl tar cpio unzip \
    rsync file bc dosfstools mtools bison flex autoconf automake \
    python3 python3-pip python3-dev python-is-python3 \
    lib32z1 scons libncurses5-dev fakeroot pigz tree doxygen gawk pkg-config \
    libyaml-dev libconfuse-dev libssl-dev libc6-dev-i386 libncurses5:i386
sudo apt clean
```

### 配置 Python 环境

```bash
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install -U pyyaml pycryptodome gmssl jsonschema jinja2
```

### 安装 repo 工具

```bash
mkdir -p ~/.bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/.bin/repo
chmod a+rx ~/.bin/repo
echo 'export PATH="$HOME/.bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 下载代码与编译

```bash
mkdir -p ~/canmv_k230 && cd ~/canmv_k230

# 从 Gitee 下载（推荐国内用户，需 SSH 密钥）
repo init -u git@gitee.com:canmv-k230/manifest.git \
  --repo-url=git@gitee.com:canmv-k230/git-repo.git

# 从 GitHub 下载（国际用户）
# repo init -u https://github.com/canmv-k230/manifest \
#   --repo-url=https://github.com/canmv-k230/git-repo.git --repo-branch stable

repo sync -j $(nproc)

# 下载工具链（首次一次）
make dl_toolchain

# 选择板级配置并编译
make k230_canmv_01studio_defconfig
time make
```

---

## 编译输出

编译完成后，镜像文件将生成在 `output/<defconfig>/images/` 目录下。

常见文件：

- `*.img`：SD 卡烧录或命令行烧录
- `*.kdimg`：K230BurningTool USB 烧录或 OTA 升级

---

## 目录结构

```text
canmv_k230/
├── boards/          # 板级支持包（BSP）
├── configs/         # defconfig 配置入口
├── output/          # 编译输出（按 defconfig 分目录）
├── src/
│   ├── applications # 用户自定义应用
│   ├── canmv/       # CanMV 组件
│   ├── opensbi/     # OpenSBI（二级引导）
│   ├── rtsmart/     # RT-Smart 内核、驱动、MPP
│   └── uboot/       # U-Boot
└── tools/           # 构建脚本、kconfig 等
```

### 关键目录

| 目录 | 说明 |
|------|------|
| `output/<defconfig>/images/` | 最终可烧录镜像 |
| `configs/` | 默认配置模板（`make list-def` 查看全部） |
| `src/canmv/` | CanMV 组件源码 |
| `src/applications/` | 用户自定义应用入口 |

---

## 常见问题

### `k230` 命令未找到

执行 `source ~/.bashrc` 或重新登录终端。确认 `~/.local/bin` 在 `$PATH` 中。

### `repo sync` 失败

1. 检查网络连接，国内用户使用 Gitee 仓库
2. 重试：`k230 repo sync -j4 --fail-fast`
3. 确认 Gitee SSH 密钥已配置，`~/.ssh` 下存在对应私钥

### 工具链下载失败

工具链存储在 Docker Volume `k230_toolchains` 中，首次下载量较大，网络不稳定时可分批下载：

```bash
k230 download-toolchains TC1     # 先下 TC1
k230 download-toolchains TC3     # 再下 TC3
```
