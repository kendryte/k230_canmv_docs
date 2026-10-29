# Wi-Fi 驱动与设备选择

## 概述

CanMV 的 `network.WLAN` 建立在 RT-Smart WLAN 和 NetMgmt 之上。当前 SDK 包含
Realtek RTL8189FTV/RTL8733BS、Broadcom brcmfmac、RW007、AIC8800 系列以及
ESP-Hosted 驱动。Python API 不直接调用厂商驱动，而是按 USB、SDIO 或 SPI
传输类型选择已注册的物理射频。

是否能直接使用某个方案取决于目标板固件的 defconfig、接口接线、模组型号和
协处理器固件。标准固件未启用的驱动需要自定义构建。

```{warning}
当前发布的 K230D 标准固件不支持网络功能。本页的 K230D 相关使用场景属于自定义
板级和驱动适配范围，不能直接套用标准固件。
```

## 支持方案

| 方案 | 传输 | CanMV 能力 | 注册型号 |
| :-- | :-- | :-- | :-- |
| RTL8189FTV | SDIO | 2.4 GHz Wi-Fi 4，STA、SoftAP | `rtl8189ftv` |
| RTL8733BS | SDIO | 支持 5 GHz 的 Wi-Fi 4，STA、SoftAP | `rtl8733bs` |
| Broadcom BCM43430A1 | SDIO | 2.4 GHz Wi-Fi 4，STA、SoftAP、单信道并发 | `BCM43430A1` |
| RW007 | SPI Mode 0 | STA、SoftAP | `rw007` |
| AIC8800/AIC8801、D80/D40/D80X2/DC/DW/DL | USB；AIC8801、D80、DC/DW/DL 支持 SDIO | STA、SoftAP；USB 组合设备可选 BLE HCI | AIC 具体型号 |
| ESP-Hosted-FG | SPI Full-Duplex、SDIO | ESP 固件管理连接和 WPA | `esp-hosted-fg` |
| ESP-Hosted-NG | SPI Full-Duplex、SDIO | 主机认证路径，可提供 WLAN offload 控制设备 | `esp-hosted-ng` |
| ESP-Hosted-MCU | SPI Full-Duplex、Dual/Quad SPI Half-Duplex | RPC Wi-Fi，可选 BLE HCI | `esp-hosted-mcu` |

ESP-Hosted-FG、NG 和 MCU 的 wire protocol 不兼容。主机驱动必须与 ESP 端烧录
的 firmware personality 一致。ESP-Hosted-MCU 当前没有 RT-Smart SDIO backend。

当前 brcmfmac 端口只移植 Wi-Fi FullMAC 功能，不提供 Bluetooth HCI transport，
不能作为 CanMV NimBLE controller。保留的旧版 CYW43xx 端口同样关闭 Bluetooth。
BLE 的配置和使用见 [NimBLE 低功耗蓝牙](bluetooth.md)。

## 默认板级配置

当前源码中：

- `k230_canmv_defconfig` 已启用 brcmfmac 和 Realtek SDIO；
- 多数带板载 SDIO Wi-Fi 的 CanMV defconfig 已启用 Realtek，默认选择
  RTL8189FTV；使用 RTL8733BS 时需要更改 Realtek module 选项；
- `k230_canmv_rtt_evb_defconfig` 已启用 RW007；
- `k230_canmv_01studio_defconfig` 已启用 AIC8800 USB 和 SDIO；
- `k230_canmv_01studio_emmc_defconfig` 已启用 AIC8800 USB；
- `k230_canmv_lckfb_defconfig` 已启用 AIC8800 USB；
- `k230_canmv_v3p0_defconfig` 已启用 AIC8800 SDIO，并选择 SDIO host 0；
- ESP-Hosted 需要按实际接线在自定义固件中启用。

板级默认值只说明构建配置，不能替代硬件核对。同一 SDIO 插槽可以同时编译多个
厂商驱动，运行时按 SDIO manufacturer/product ID 匹配；但 Realtek 驱动内部一次
只能选择 RTL8189FTV 或 RTL8733BS 中的一种。

AIC 固件由 manifest 中的独立子仓库提供。执行 `repo sync` 后，应存在：

```text
src/rtsmart/rtsmart/kernel/bsp/maix3/drivers/extdrv/aic8800/firmware/
```

构建系统会把所需文件安装到镜像的 `/bin/firmware`。这些二进制具有独立的
vendor 许可条款。当前固件同步自 AIC
`aic8800d_linux_sdk_V5.0_2026_0123_5f7be68d`，对应 vendor 仓库提交
`df4c783b663eba1956579c681acd5e45f25c671d`；准确来源以 firmware 子仓库的
`README.md` 为准。

## 自定义固件配置

先按 [自定义固件](how_to_build.md) 选择板级配置，再运行 `make rtsmart-menuconfig`
或对应的容器命令。

### SDIO 公共板级配置

Realtek、brcmfmac、CYW43xx、AIC8800 SDIO 和 ESP-Hosted SDIO 共用以下板级设置：

```text
BSP_WIFI_SDIO_HOST_0=y              # 或 BSP_WIFI_SDIO_HOST_1
BSP_WIFI_SDIO_REG_ON_PIN=<gpio>     # -1 表示使用板级固定接线
BSP_WIFI_SDIO_RESET_ACTIVE_LOW=y
BSP_WIFI_SDIO_RESET_PULSE_MS=200
BSP_WIFI_SDIO_POWER_UP_DELAY_MS=50
```

选择的 host 必须已启用对应的 `RT_USING_SDIO0` 或 `RT_USING_SDIO1`。REG_ON、复位
有效电平和上电延时必须按原理图及模组手册设置。

### Realtek RTL8189FTV/RTL8733BS

启用 `RT_USING_REALTEK`，并且在 Realtek module 选项中二选一：

```text
REALTEK_SDIO_RTL8189FTV=y
# REALTEK_SDIO_RTL8733BS=y
```

RTL8189FTV 的 SDIO ID 为 `024c:f179`，RTL8733BS 为 `024c:b733`。驱动按 ID
绑定设备；选错模块时即使 SDIO 总线发现了卡也不会注册 WLAN。调试命令和驱动
日志可分别通过 `REALTEK_INTERACTIVE_CMD` 和 `REALTEK_ENABLE_DEBUG` 启用。

### Broadcom brcmfmac

启用：

```text
RT_USING_BRCMFMAC=y
BRCMFMAC_COUNTRY_CODE="CN"
BRCMFMAC_COUNTRY_REVISION=0
BRCMFMAC_BCM43430A1_NVRAM="nvram.txt"
```

当前随 SDK 提供并验证的目标为 SDIO ID `02d0:a9a6`、芯片版本 A1，注册型号为
`BCM43430A1`。驱动支持 STA、SoftAP 和单信道 STA + SoftAP 并发。并发运行时，
STA 连接期间 SoftAP 可能短暂停止，连接完成后在 STA 所在信道恢复。

构建系统会把 firmware 和 NVRAM 安装到镜像的 `/bin/firmware/brcmfmac`。默认
`nvram.txt` 是 K230 CanMV Linux SDK 使用的 K016-CW43 板级校准；只有模组和射频
设计与 AP6212A V1.0.2 校准匹配时，才将 `BRCMFMAC_BCM43430A1_NVRAM` 改为
`nvram_ap6212.txt`。NVRAM 是板级射频校准数据，不能只按 SDIO ID 或芯片型号互换。

驱动映射表还列出其他 Broadcom/Cypress 芯片，但 SDK 当前没有随附这些目标的
firmware、NVRAM 和可选 CLM blob。适配新模组时，必须提供 Linux brcmfmac 对应
文件并安装到 `BRCMFMAC_FIRMWARE_PATH` 指定的目录。

旧版 `RT_USING_CYW43XX` 仍可用于现有自定义配置，但它与 `RT_USING_BRCMFMAC`
互斥，因为两者匹配相同的 Broadcom SDIO ID。新配置应使用 brcmfmac。

### RW007

启用 `RT_USING_RW007`，并按板级接线配置：

```text
RW007_SPI_BUS_NAME="spi0"
RW007_SPI_MAX_HZ=25000000
RW007_RST_PIN=20
RW007_CS_PIN=63
RW007_INT_BUSY_PIN=62
```

驱动使用 SPI Mode 0、8-bit、单数据线，并把从设备挂载为 `wspi`。上面的 GPIO
只是 Kconfig 默认值，移植到其他板卡时必须核对 Reset、CS 和 INT/BUSY 引脚。

### AIC8800

启用：

```text
RT_USING_AIC8800_WIFI=y
AIC8800_WIFI_TRANSPORT_USB=y        # USB 网卡
AIC8800_WIFI_TRANSPORT_SDIO=y       # SDIO 模组，可与 USB 同时启用
```

2.4 GHz-only 模组应关闭 `AIC8800_WIFI_5GHZ`。AIC8800D40L 与 D80 可能使用相同
USB ID，D40L 必须启用 `AIC8800_WIFI_USB_LIMIT_40MHZ`。USB BLE 需要
`AIC8800_WIFI_BLE`，同时 CanMV 顶层还需启用 `ENABLE_BLUETOOTH`。

固件可按系列裁剪：`AIC8800_WIFI_FIRMWARE_AIC8800`、
`AIC8800_WIFI_FIRMWARE_D80`、`AIC8800_WIFI_FIRMWARE_D80X2` 和
`AIC8800_WIFI_FIRMWARE_DC_DW`。D80X2 当前只支持 USB；DC/DW/DL 共用
`aic8800DC` 目录，DL 没有单独的设备 ID 或固件文件名。新同步的 USB D80X2
固件包含 U03 和 U05 revision 文件，驱动根据 silicon revision 自动选择。

当前 SDIO 驱动匹配以下设备：

| 芯片系列 | SDIO function 和 ID | 说明 |
| :-- | :-- | :-- |
| AIC8801 | function 1：`5449:0145` | Wi-Fi 数据和控制共用 function 1 |
| AIC8800D80 | function 1：`c8a1:0082` | 当前只使用 Wi-Fi function |
| AIC8800DC/DW/DL | function 1：`c8a1:c08d`；function 2：`c8a1:c18d` | 两个 function 必须同时枚举；function 2 用于控制/消息传输，不是 Bluetooth HCI |

`k230_canmv_01studio_defconfig` 的 SDIO Wi-Fi 插槽使用 host 1，REG_ON GPIO 为 53，
并已启用 AIC USB 和 SDIO transport；`k230_canmv_v3p0_defconfig` 使用 SDIO
host 0。AIC8800DC 是 2.4 GHz-only 模组，使用该卡的自定义配置应关闭
`AIC8800_WIFI_5GHZ`。

同时构建 USB 和 SDIO transport 时，DC/DW/DL 的 SDIO 固件安装在
`/bin/firmware/sdio/aic8800DC`；只构建 SDIO 时安装在
`/bin/firmware/aic8800DC`。驱动读取芯片 ID 和 U02 revision 后自动选择普通版或
H 版 patch、patch table 和校准固件，不要使用同名 USB 固件覆盖这些文件。
USB 和 SDIO 均按 vendor 流程执行匹配的 DPD 校准；校准失败会终止初始化，不提供
跳过校准的 Kconfig 选项。

DC/DW/DL transport 更新后的默认值变化为：`AIC8800_WIFI_POWER_SAVE` 从开启改为
关闭；`AIC8800_WIFI_DATA_RX_URBS` 从 5 改为 descriptor DMA 使用 4、其他模式使用
20；原先隐式开启的 `AIC8800_WIFI_USB_TX_AGGREGATION` 改为关闭；
`AIC8800_WIFI_SDIO_TX_AGGREGATE_WAIT_MS` 从 1 ms 改为 0 ms。依赖旧功耗或吞吐
配置的板级 defconfig 应显式设置对应选项。`AIC8800_WIFI_DATA_TX_URBS` 默认仍为
2，不应仅为追求吞吐量而盲目增大。

SDIO 日志中的 `clock=50000 kHz` 是主机总线时钟，不是 Wi-Fi 射频带宽。
`ME capabilities ... max-bw=80 MHz` 只表示能力；关联后的
`association channel ... width=80 MHz` 才表示本次连接实际使用 80 MHz。
吞吐测试应覆盖 30～60 秒，并按秒或分段记录结果，避免把关联后的短时速率爬升
误判为 DPD 或总线故障。

### ESP-Hosted-FG/NG

启用 `RT_USING_ESP_HOSTED_WIFI`，选择 FG 或 NG，再选择 SPI Full-Duplex 或
SDIO。SPI mode、频率、checksum、Handshake/Data Ready 电平及引脚必须与 ESP
固件一致。SDIO 还需填写从机实际发布的 manufacturer/product ID。当前 FG/NG
端口不向 CanMV 注册 BLE HCI controller。

### ESP-Hosted-MCU

启用 `RT_USING_ESP_HOSTED_MCU`，选择 SPI Full-Duplex 或 SPI Half-Duplex。
Half-Duplex 使用 2/4 条双向数据线，不支持 1-line 模式。启用
`ESP_HOSTED_BLE` 后，再启用 CanMV `ENABLE_BLUETOOTH`，MicroPython NimBLE 才能
使用动态注册的 `/dev/hciN` controller。

所有 ESP-Hosted 方案都应优先连接可控 Reset。Reset 未连接时，只重启 K230 或
ESP 一端可能使 transport session 不同步。

## Python 设备选择

构造 `network.WLAN` 时第二个参数选择传输：

```python
import network

auto_sta = network.WLAN(network.STA_IF, network.WLAN_AUTO)
usb_sta = network.WLAN(network.STA_IF, network.WLAN_USB)
sdio_sta = network.WLAN(network.STA_IF, network.WLAN_SDIO)
spi_ap = network.WLAN(network.AP_IF, network.WLAN_SPI)
```

对应常量：

| 常量 | 传输和适用驱动 |
| :-- | :-- |
| `network.WLAN_AUTO` | 保持当前可用射频，否则按 SDIO、SPI、USB 选择 |
| `network.WLAN_USB` | AIC8800 USB |
| `network.WLAN_SDIO` | RTL8189FTV、RTL8733BS、Broadcom BCM43430A1、AIC8800、ESP-Hosted-FG/NG |
| `network.WLAN_SPI` | RW007、ESP-Hosted-FG/NG/MCU |

该参数选择传输类型，不选择 vendor model。通常使用 `WLAN_AUTO`；只有多块 Wi-Fi
同时存在且应用确实依赖某条总线时才固定类型。当前 Python API 不能区分同一传输
上同时存在的两个不同型号。

连接并查询动态 netdev：

```python
import network
import time

sta = network.WLAN(network.STA_IF, network.WLAN_AUTO)
if not sta.active(True):
    raise RuntimeError("Wi-Fi device unavailable")

sta.connect("TEST", "12345678")
deadline = time.time() + 20
while not sta.isconnected() and time.time() < deadline:
    time.sleep_ms(200)

print(network.get_dev_list())
print(sta.netdev_name())
print(sta.ifconfig())
```

网卡名通常是 `wlanN`/`wlanNap`，但 `N` 由探测顺序决定。不要在脚本中写死
`wlan0`。

## 安全模式限制

- brcmfmac 支持开放网络及 WPA/WPA2 Personal；只有 firmware 报告 SAE 能力时才
  支持 WPA3-SAE。切换 Broadcom/Cypress 模组或 firmware 后，应重新验证扫描、
  STA 加密连接、SoftAP 和并发模式。
- Realtek、旧版 CYW43xx 和 RW007 的安全模式取决于厂商驱动及模组 firmware；
  切换模组时应重新验证扫描、STA 加密连接和 SoftAP。
- AIC8800 STA 的普通 WPA/WPA2 Personal 可由内置认证路径完成；受限 WPA3-SAE
  使用 group 19，不支持 SAE H2E 和 Enterprise/802.1X。
- AIC8800 SoftAP 支持开放网络和 WPA2-PSK/CCMP，不支持 WPA3、Enterprise、WPS、
  DFS/CAC 或动态 VLAN。
- ESP-Hosted-FG 的实际安全能力由 ESP firmware 提供。
- ESP-Hosted-NG 可使用内置普通 WPA/WPA2 STA 和开放/WPA2 SoftAP 路径；其他
  安全模式需要完整用户态 supplicant。
- ESP-Hosted-MCU 的实际能力取决于 ESP 芯片、ESP-IDF 和从机编译配置。

## 验证与排错

1. `network.get_dev_list()` 没有 WLAN：检查固件是否启用对应驱动、接口供电、
   SDIO host/REG_ON、RW007 SPI 引脚、AIC firmware 文件或 ESP transport ready 日志。
1. Realtek 未注册：核对 SDIO ID，并确认选择的是 RTL8189FTV 还是 RTL8733BS。
1. brcmfmac 报告 firmware 或 NVRAM 不存在：确认镜像中存在
   `/bin/firmware/brcmfmac`，并核对 `BRCMFMAC_BCM43430A1_NVRAM` 与实际板卡。
1. RW007 未注册：核对 SPI bus、Mode 0、最大频率、CS、Reset 和 INT/BUSY。
1. `active(True)` 返回 `False`：指定传输当前没有可用设备，先改为
   `network.WLAN_AUTO`。
1. AIC8800DC/DW/DL 显示 `no driver for SDIO function`：确认镜像已包含新版 AIC SDIO
   驱动，并确认 `c8a1:c08d` 和 `c8a1:c18d` 两个 function 均已枚举。
1. AIC8800DC/DW/DL 固件初始化失败：检查 `/bin/firmware/sdio/aic8800DC`（USB
   和 SDIO 同时启用）或 `/bin/firmware/aic8800DC`（仅 SDIO）是否完整；若日志
   明确显示 DPD 校准失败，还应检查供电、复位时序和实际 silicon revision。
1. AIC D40 连接速率异常：检查 `AIC8800_WIFI_USB_LIMIT_40MHZ`。
1. ESP 无法初始化：优先核对 firmware personality、SPI mode、checksum、引脚和
   HS/DR 有效电平。
1. 已关联但不能访问网络：先检查 `ifconfig()` 是否取得非零 IP 和网关，再测试
   局域网网关，最后排查 DNS 和公网。

Python 接口和完整示例分别见 [network 模块 API](../api/extmod/k230_canmv_network_api_manual.md)
和 [无线网例程](../example/network/wlan.md)。
