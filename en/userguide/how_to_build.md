# Advanced - Custom Firmware

```{note}
This chapter introduces how to develop on K230 CanMV. If you do not have custom requirements, you may skip this chapter.
```

## Overview

K230 CanMV is a Micropython + OpenMV application platform developed based on the K230 SDK, allowing users to call hardware resources through the Python language. This document provides two build methods:

- **Build with Docker** (recommended): No need to install any build dependencies, completes the build with a single command
- **Build directly on host**: Manually set up the environment on Ubuntu 20.04

## Build with Docker (recommended)

Use the preconfigured [k230-builder](https://github.com/huangzhenming/k230-builder) image, which includes the full toolchain, repo, genimage, and all build dependencies. The only prerequisite is to install Docker.

### Prerequisites

- **Install Docker**

  ```bash
  # Ubuntu/Debian
  sudo apt install docker.io
  sudo usermod -aG docker $USER && newgrp docker
  ```

  For other systems, refer to the [Docker official documentation](https://docs.docker.com/engine/install/).

- **Configure Gitee SSH key** (required for code download)
  Register an account on [Gitee](https://gitee.com) and [add an SSH public key](https://gitee.com/profile/sshkeys).

- **Configure Git user information**

  ```bash
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
  ```

### Install the k230 command

```bash
curl -fsSL https://www.kendryte.com/misc/install.sh | bash
source ~/.bashrc
```

After installation, run `k230 pull` to pull the Docker image (the first time depends on the network, about 1GB+).

### Quick Start

```bash
# 1) Create a working directory
mkdir -p ~/canmv_k230 && cd ~/canmv_k230

# 2) Pull the docker image
k230 pull

# 3) Download toolchains (only need to run once for the first time)
k230 download-toolchains TC1 TC3

# 4) Download code (repo is built into the container, host SSH key is auto-mounted)
# Download from Gitee (recommended for users in China, requires SSH key)
k230 repo init -u git@gitee.com:canmv-k230/manifest.git --repo-url=git@gitee.com:canmv-k230/git-repo.git

# Download from GitHub (international users)
# k230 repo init -u https://github.com/canmv-k230/manifest --repo-url=https://github.com/canmv-k230/git-repo.git --repo-branch stable

k230 repo sync -j$(nproc)

# 5) Select board configuration and build
k230 make list-def                      # View all board configurations
k230 make k230_canmv_01studio_defconfig # Select target board
k230 make

# 6) View output images
ls -lh output/k230_canmv_01studio_defconfig/images/
```

### Common Commands

```bash
k230 list-toolchains                  # View available toolchain list
k230 make                             # Build (incremental build)
k230 make list-def                    # View all board configurations
k230 make menuconfig                  # Interactive configuration
k230 bash                             # Enter container terminal
k230 repo sync -j$(nproc)             # Update code
k230 pull                             # Update k230-builder image
```

### Git and SSH

`k230` automatically mounts the host `~/.ssh` and `~/.gitconfig` into the container, so `repo init` / `git clone` can be used directly without additional configuration.

### Host Network Restricted

If ghcr.io is unreachable (common in China), `k230` automatically switches to the `registry.kendryte.com` mirror source. Specify the version manually:

```bash
K230_BUILDER_TAG=dev k230 make
```

---

## Direct Local Compilation

> It is recommended to use Docker for compilation. Only when Docker cannot be used, refer to the following manual setup process.

### System Requirements

- **Operating System**: Ubuntu 20.04 LTS (x86_64)
- **Memory**: ≥ 2GB
- **Disk**: ≥ 10GB

### Configure APT Sources (Optional, recommended for users in China)

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources_bak.list
sudo sed -i "s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list
sudo sed -i "s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list
sudo apt update
```

### Install System Dependencies

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

### Configure Python Environment

```bash
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install -U pyyaml pycryptodome gmssl jsonschema jinja2
```

### Install repo Tool

```bash
mkdir -p ~/.bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/.bin/repo
chmod a+rx ~/.bin/repo
echo 'export PATH="$HOME/.bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Download Code and Compile

```bash
mkdir -p ~/canmv_k230 && cd ~/canmv_k230

# Download from Gitee (recommended for users in China, requires SSH key)
repo init -u git@gitee.com:canmv-k230/manifest.git \
  --repo-url=git@gitee.com:canmv-k230/git-repo.git

# Download from GitHub (international users)
# repo init -u https://github.com/canmv-k230/manifest \
#   --repo-url=https://github.com/canmv-k230/git-repo.git --repo-branch stable

repo sync -j $(nproc)

# Download toolchain (only once for the first time)
make dl_toolchain

# Select board-level configuration and compile
make k230_canmv_01studio_defconfig
time make
```

---

## Build Output

After the build completes, the image files will be generated in the `output/<defconfig>/images/` directory.

Common files:

- `*.img`: SD card flashing or command-line flashing
- `*.kdimg`: K230BurningTool USB flashing or OTA upgrade

---

## Directory Structure

```text
canmv_k230/
├── boards/          # Board Support Package (BSP)
├── configs/         # defconfig configuration entries
├── output/          # Build output (organized by defconfig)
├── src/
│   ├── applications # User-defined applications
│   ├── canmv/       # CanMV components
│   ├── opensbi/     # OpenSBI (secondary bootloader)
│   ├── rtsmart/     # RT-Smart kernel, drivers, MPP
│   └── uboot/       # U-Boot
└── tools/           # Build scripts, kconfig, etc.
```

### Key Directories

| Directory | Description |
|------|------|
| `output/<defconfig>/images/` | Final flashable image |
| `configs/` | Default configuration templates (run `make list-def` to view all) |
| `src/canmv/` | CanMV component source code |
| `src/applications/` | User-defined application entry |

## Frequently Asked Questions

### `k230` command not found

Run `source ~/.bashrc` or re-login to the terminal. Make sure `~/.local/bin` is in `$PATH`.

### `repo sync` failed

1. Check the network connection; domestic users should use the Gitee mirror
2. Retry: `k230 repo sync -j4 --fail-fast`
3. Make sure the Gitee SSH key is configured and the corresponding private key exists under `~/.ssh`

### Toolchain download failed

The toolchain is stored in the Docker volume `k230_toolchains`. The first download is large; when the network is unstable, you can download in batches:

```bash
k230 download-toolchains TC1     # Download TC1 first
k230 download-toolchains TC3     # Then download TC3
```
