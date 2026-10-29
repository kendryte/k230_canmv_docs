# Wi-Fi Driver and Device Selection

## Overview

CanMV's `network.WLAN` is built on top of RT-Smart WLAN and NetMgmt. The current SDK includes
Realtek RTL8189FTV/RTL8733BS, Broadcom brcmfmac, RW007, AIC8800 series, and
ESP-Hosted drivers. The Python API does not directly call vendor drivers, but selects
registered physical radios by USB, SDIO, or SPI transport type.

Whether a solution can be used directly depends on the target board firmware's defconfig,
interface wiring, module model, and coprocessor firmware. Drivers not enabled in the
standard firmware require custom builds.

```{warning}
The currently released K230D standard firmware does not support network functionality.
The K230D-related usage scenarios on this page fall within the scope of custom
board-level and driver adaptation and cannot be directly applied to the standard firmware.
```

## Supported Solutions

| Solution | Transport | CanMV Capability | Registered Model |
| :-- | :-- | :-- | :-- |
| RTL8189FTV | SDIO | 2.4 GHz Wi-Fi 4, STA, SoftAP | `rtl8189ftv` |
| RTL8733BS | SDIO | Wi-Fi 4 with 5 GHz support, STA, SoftAP | `rtl8733bs` |
| Broadcom BCM43430A1 | SDIO | 2.4 GHz Wi-Fi 4, STA, SoftAP, single-channel concurrency | `BCM43430A1` |
| RW007 | SPI Mode 0 | STA, SoftAP | `rw007` |
| AIC8800/AIC8801, D80/D40/D80X2/DC/DW/DL | USB; AIC8801, D80, DC/DW/DL support SDIO | STA, SoftAP; USB composite device can optionally have BLE HCI | AIC specific model |
| ESP-Hosted-FG | SPI Full-Duplex, SDIO | ESP firmware manages connection and WPA | `esp-hosted-fg` |
| ESP-Hosted-NG | SPI Full-Duplex, SDIO | Host authentication path, can provide WLAN offload control device | `esp-hosted-ng` |
| ESP-Hosted-MCU | SPI Full-Duplex, Dual/Quad SPI Half-Duplex | RPC Wi-Fi, optional BLE HCI | `esp-hosted-mcu` |

The wire protocols of ESP-Hosted-FG, NG, and MCU are not compatible. The host driver
must match the firmware personality burned on the ESP side. ESP-Hosted-MCU currently
does not have an RT-Smart SDIO backend.

The current brcmfmac port only ports Wi-Fi FullMAC functionality and does not provide
Bluetooth HCI transport, so it cannot serve as a CanMV NimBLE controller. The retained
legacy CYW43xx port similarly has Bluetooth disabled. For BLE configuration and usage,
see [NimBLE Bluetooth Low Energy](bluetooth.md).

## Default Board-Level Configuration

In the current source code:

- `k230_canmv_defconfig` has brcmfmac and Realtek SDIO enabled;
- Most CanMV defconfigs with on-board SDIO Wi-Fi have Realtek enabled, with
  RTL8189FTV selected by default; when using RTL8733BS, the Realtek module option
  must be changed;
- `k230_canmv_rtt_evb_defconfig` has RW007 enabled;
- `k230_canmv_01studio_defconfig` has AIC8800 USB and SDIO enabled;
- `k230_canmv_01studio_emmc_defconfig` has AIC8800 USB enabled;
- `k230_canmv_lckfb_defconfig` has AIC8800 USB enabled;
- `k230_canmv_v3p0_defconfig` has AIC8800 SDIO enabled, with SDIO host 0 selected;
- ESP-Hosted must be enabled in custom firmware according to actual wiring.

Board-level defaults only describe build configuration and cannot replace hardware
verification. The same SDIO slot can compile drivers from multiple vendors at the
same time, matched at runtime by SDIO manufacturer/product ID; however, the Realtek
driver can only select either RTL8189FTV or RTL8733BS at a time internally.

AIC firmware is provided by a separate sub-repository in the manifest. After running
`repo sync`, the following should exist:

```text
src/rtsmart/rtsmart/kernel/bsp/maix3/drivers/extdrv/aic8800/firmware/
```

The build system installs the required files to `/bin/firmware` in the image. These
binaries have independent vendor license terms. The current firmware is synced from
AIC `aic8800d_linux_sdk_V5.0_2026_0123_5f7be68d`, corresponding to vendor repository
commit `df4c783b663eba1956579c681acd5e45f25c671d`; the authoritative source is the
`README.md` of the firmware sub-repository.

## Custom Firmware Configuration

First select the board-level configuration following [Custom Firmware](how_to_build.md),
then run `make rtsmart-menuconfig` or the corresponding container command.

### SDIO Common Board-Level Configuration

Realtek, brcmfmac, CYW43xx, AIC8800 SDIO, and ESP-Hosted SDIO share the following
board-level settings:

```text
BSP_WIFI_SDIO_HOST_0=y              # or BSP_WIFI_SDIO_HOST_1
BSP_WIFI_SDIO_REG_ON_PIN=<gpio>     # -1 means use board-level fixed wiring
BSP_WIFI_SDIO_RESET_ACTIVE_LOW=y
BSP_WIFI_SDIO_RESET_PULSE_MS=200
BSP_WIFI_SDIO_POWER_UP_DELAY_MS=50
```

The selected host must have the corresponding `RT_USING_SDIO0` or `RT_USING_SDIO1`
enabled. REG_ON, reset active level, and power-up delay must be set according to
the schematic and module manual.

### Realtek RTL8189FTV/RTL8733BS

Enable `RT_USING_REALTEK`, and choose one of the two in the Realtek module options:

```text
REALTEK_SDIO_RTL8189FTV=y
# REALTEK_SDIO_RTL8733BS=y
```

The SDIO ID of RTL8189FTV is `024c:f179`, and RTL8733BS is `024c:b733`. The driver
binds devices by ID; if the wrong module is selected, WLAN will not be registered even
if the SDIO bus discovers the card. Debug commands and driver logs can be enabled via
`REALTEK_INTERACTIVE_CMD` and `REALTEK_ENABLE_DEBUG` respectively.

### Broadcom brcmfmac

Enable:

```text
RT_USING_BRCMFMAC=y
BRCMFMAC_COUNTRY_CODE="CN"
BRCMFMAC_COUNTRY_REVISION=0
BRCMFMAC_BCM43430A1_NVRAM="nvram.txt"
```

The currently provided and verified target in the SDK is SDIO ID `02d0:a9a6`, chip
revision A1, with registered model `BCM43430A1`. The driver supports STA, SoftAP,
and single-channel STA + SoftAP concurrency. During concurrent operation, SoftAP may
briefly stop while STA is connected, and resumes on the STA's channel after the
connection is complete.

The build system installs firmware and NVRAM to `/bin/firmware/brcmfmac` in the image.
The default `nvram.txt` is the K016-CW43 board-level calibration used by the K230
CanMV Linux SDK; only when the module and radio design match the AP6212A V1.0.2
calibration should `BRCMFMAC_BCM43430A1_NVRAM` be changed to `nvram_ap6212.txt`.
NVRAM is board-level radio calibration data and cannot be swapped based solely on
SDIO ID or chip model.

The driver mapping table also lists other Broadcom/Cypress chips, but the SDK currently
does not include firmware, NVRAM, and optional CLM blobs for these targets. When adapting
new modules, the corresponding Linux brcmfmac files must be provided and installed to
the directory specified by `BRCMFMAC_FIRMWARE_PATH`.

The legacy `RT_USING_CYW43XX` is still available for existing custom configurations,
but it is mutually exclusive with `RT_USING_BRCMFMAC` because both match the same
Broadcom SDIO ID. New configurations should use brcmfmac.

### RW007

Enable `RT_USING_RW007`, and configure according to board-level wiring:

```text
RW007_SPI_BUS_NAME="spi0"
RW007_SPI_MAX_HZ=25000000
RW007_RST_PIN=20
RW007_CS_PIN=63
RW007_INT_BUSY_PIN=62
```

The driver uses SPI Mode 0, 8-bit, single data line, and mounts the slave as `wspi`.
The GPIOs above are only Kconfig defaults; when porting to other boards, the Reset,
CS, and INT/BUSY pins must be verified.

### AIC8800

Enable:

```text
RT_USING_AIC8800_WIFI=y
AIC8800_WIFI_TRANSPORT_USB=y        # USB network card
AIC8800_WIFI_TRANSPORT_SDIO=y       # SDIO module, can be enabled simultaneously with USB
```

2.4 GHz-only modules should disable `AIC8800_WIFI_5GHZ`. AIC8800D40L and D80 may use
the same USB ID; D40L must enable `AIC8800_WIFI_USB_LIMIT_40MHZ`. USB BLE requires
`AIC8800_WIFI_BLE`, and `ENABLE_BLUETOOTH` must also be enabled at the CanMV top level.

Firmware can be trimmed by series: `AIC8800_WIFI_FIRMWARE_AIC8800`,
`AIC8800_WIFI_FIRMWARE_D80`, `AIC8800_WIFI_FIRMWARE_D80X2`, and
`AIC8800_WIFI_FIRMWARE_DC_DW`. D80X2 currently only supports USB; DC/DW/DL share
the `aic8800DC` directory, and DL does not have a separate device ID or firmware
filename. The newly synced USB D80X2 firmware includes U03 and U05 revision files,
and the driver automatically selects based on silicon revision.

The current SDIO driver matches the following devices:

| Chip Series | SDIO Function and ID | Description |
| :-- | :-- | :-- |
| AIC8801 | function 1: `5449:0145` | Wi-Fi data and control share function 1 |
| AIC8800D80 | function 1: `c8a1:0082` | Currently only Wi-Fi function is used |
| AIC8800DC/DW/DL | function 1: `c8a1:c08d`; function 2: `c8a1:c18d` | Both functions must be enumerated simultaneously; function 2 is used for control/message transport, not Bluetooth HCI |

The SDIO Wi-Fi slot of `k230_canmv_01studio_defconfig` uses host 1, REG_ON GPIO is 53,
and AIC USB and SDIO transport are enabled; `k230_canmv_v3p0_defconfig` uses SDIO
host 0. AIC8800DC is a 2.4 GHz-only module; custom configurations using this card
should disable `AIC8800_WIFI_5GHZ`.

When building USB and SDIO transport simultaneously, the DC/DW/DL SDIO firmware is
installed at `/bin/firmware/sdio/aic8800DC`; when only building SDIO, it is installed
at `/bin/firmware/aic8800DC`. After the driver reads the chip ID and U02 revision,
it automatically selects the normal or H version patch, patch table, and calibration
firmware; do not use same-named USB firmware to overwrite these files. Both USB and
SDIO perform matching DPD calibration according to vendor procedures; calibration
failure terminates initialization, and there is no Kconfig option to skip calibration.

The default value changes after DC/DW/DL transport update are: `AIC8800_WIFI_POWER_SAVE`
changed from enabled to disabled; `AIC8800_WIFI_DATA_RX_URBS` changed from 5 to 4 for
descriptor DMA, and 20 for other modes; the previously implicitly enabled
`AIC8800_WIFI_USB_TX_AGGREGATION` is now disabled;
`AIC8800_WIFI_SDIO_TX_AGGREGATE_WAIT_MS` changed from 1 ms to 0 ms. Board-level
defconfigs that depend on old power or throughput configurations should explicitly
set the corresponding options. `AIC8800_WIFI_DATA_TX_URBS` remains 2 by default and
should not be blindly increased just for throughput.

`clock=50000 kHz` in SDIO logs is the host bus clock, not the Wi-Fi radio bandwidth.
`ME capabilities ... max-bw=80 MHz` only indicates capability; the
`association channel ... width=80 MHz` after association indicates that 80 MHz is
actually used for this connection. Throughput testing should cover 30~60 seconds
and record results per second or in segments, to avoid mistaking the short-term
rate ramp-up after association for DPD or bus failure.

### ESP-Hosted-FG/NG

Enable `RT_USING_ESP_HOSTED_WIFI`, select FG or NG, then select SPI Full-Duplex or
SDIO. SPI mode, frequency, checksum, Handshake/Data Ready levels, and pins must match
the ESP firmware. SDIO also requires the manufacturer/product ID actually published
by the slave. The current FG/NG ports do not register a BLE HCI controller with CanMV.

### ESP-Hosted-MCU

Enable `RT_USING_ESP_HOSTED_MCU`, and select SPI Full-Duplex or SPI Half-Duplex.
Half-Duplex uses 2/4 bidirectional data lines and does not support 1-line mode. After
enabling `ESP_HOSTED_BLE`, then enable CanMV `ENABLE_BLUETOOTH`, and MicroPython NimBLE
can use the dynamically registered `/dev/hciN` controller.

For all ESP-Hosted solutions, a controllable Reset should be connected preferentially.
When Reset is not connected, restarting only the K230 or ESP side may cause the
transport session to become out of sync.

## Python Device Selection

The second parameter of `network.WLAN` selects the transport:

```python
import network

auto_sta = network.WLAN(network.STA_IF, network.WLAN_AUTO)
usb_sta = network.WLAN(network.STA_IF, network.WLAN_USB)
sdio_sta = network.WLAN(network.STA_IF, network.WLAN_SDIO)
spi_ap = network.WLAN(network.AP_IF, network.WLAN_SPI)
```

Corresponding constants:

| Constant | Transport and Applicable Driver |
| :-- | :-- |
| `network.WLAN_AUTO` | Keep the currently available radio, otherwise select in the order SDIO, SPI, USB |
| `network.WLAN_USB` | AIC8800 USB |
| `network.WLAN_SDIO` | RTL8189FTV, RTL8733BS, Broadcom BCM43430A1, AIC8800, ESP-Hosted-FG/NG |
| `network.WLAN_SPI` | RW007, ESP-Hosted-FG/NG/MCU |

This parameter selects the transport type, not the vendor model. Typically use `WLAN_AUTO`; only fix the type when multiple Wi-Fi devices coexist and the application genuinely depends on a specific bus. The current Python API cannot distinguish between two different models present on the same transport.

Connect and query the dynamic netdev:

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

The network interface name is usually `wlanN`/`wlanNap`, but `N` is determined by probe order. Do not hardcode `wlan0` in scripts.

## Security Mode Limitations

- brcmfmac supports open networks and WPA/WPA2 Personal; WPA3-SAE is supported only when the firmware reports SAE capability. After switching Broadcom/Cypress modules or firmware, re-verify scanning, STA encrypted connection, SoftAP, and concurrent mode.
- Realtek, legacy CYW43xx, and RW007 security modes depend on the vendor driver and module firmware; re-verify scanning, STA encrypted connection, and SoftAP when switching modules.
- AIC8800 STA ordinary WPA/WPA2 Personal can be completed by the built-in authentication path; restricted WPA3-SAE uses group 19, and does not support SAE H2E and Enterprise/802.1X.
- AIC8800 SoftAP supports open networks and WPA2-PSK/CCMP, and does not support WPA3, Enterprise, WPS, DFS/CAC, or dynamic VLAN.
- The actual security capabilities of ESP-Hosted-FG are provided by the ESP firmware.
- ESP-Hosted-NG can use the built-in ordinary WPA/WPA2 STA and open/WPA2 SoftAP paths; other security modes require a full user-space supplicant.
- The actual capabilities of ESP-Hosted-MCU depend on the ESP chip, ESP-IDF, and slave compilation configuration.

## Verification and Troubleshooting

1. `network.get_dev_list()` has no WLAN: check whether the firmware enables the corresponding driver, interface power, SDIO host/REG_ON, RW007 SPI pins, AIC firmware files, or ESP transport ready logs.
1. Realtek not registered: verify the SDIO ID, and confirm whether RTL8189FTV or RTL8733BS is selected.
1. brcmfmac reports firmware or NVRAM missing: confirm `/bin/firmware/brcmfmac` exists in the image, and verify `BRCMFMAC_BCM43430A1_NVRAM` matches the actual board.
1. RW007 not registered: verify SPI bus, Mode 0, maximum frequency, CS, Reset, and INT/BUSY.
1. `active(True)` returns `False`: no device is currently available for the specified transport; first change to `network.WLAN_AUTO`.
1. AIC8800DC/DW/DL shows `no driver for SDIO function`: confirm the image contains the new AIC SDIO driver, and confirm that both functions `c8a1:c08d` and `c8a1:c18d` are enumerated.
1. AIC8800DC/DW/DL firmware initialization fails: check whether `/bin/firmware/sdio/aic8800DC` (when both USB and SDIO are enabled) or `/bin/firmware/aic8800DC` (SDIO only) is complete; if logs clearly show DPD calibration failure, also check power supply, reset timing, and the actual silicon revision.
1. AIC D40 connection rate is abnormal: check `AIC8800_WIFI_USB_LIMIT_40MHZ`.
1. ESP cannot initialize: prioritize checking firmware personality, SPI mode, checksum, pins, and HS/DR active level.
1. Associated but cannot access the network: first check whether `ifconfig()` has obtained a non-zero IP and gateway, then test the LAN gateway, and finally troubleshoot DNS and the public network.

The Python interface and complete examples are in [network module API](../api/extmod/k230_canmv_network_api_manual.md) and [wireless network examples](../example/network/wlan.md).
