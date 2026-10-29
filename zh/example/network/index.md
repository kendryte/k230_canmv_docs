# 网络例程讲解

```{warning}
K230D 目前不支持网络功能，因此网络通信、RTSP 推流等例程无法在 K230D 上运行。
```

## 例程路径说明

文档中的网络例程有两个对应位置：

- 开发板固件路径：`/sdcard/examples/14-Socket/`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/`

在 CanMV IDE 中打开并运行固件路径下的脚本。需要查看版本管理中的原始文件或
修改固件内置资源时，使用 SDK 源码路径。下列各页会同时列出这两个路径。

公共网络库位于：

- 开发板固件路径：`/sdcard/libs/Network.py`
- SDK 源码路径：`src/canmv/resources/libs/Network.py`

网络例程通过该库选择 LAN 或 WLAN、等待 IP 地址、设置默认上行，并避免写死
`eth0`、`wlan0` 等动态设备名。

Wi-Fi 硬件、Realtek/brcmfmac/RW007/AIC8800/ESP-Hosted 配置和各驱动限制见
[Wi-Fi 驱动与设备选择](../../userguide/wifi_drivers.md)。

## 通用网络参数

大部分例程在文件顶部提供以下参数：

| 参数 | 说明 |
| :-- | :-- |
| `NETWORK_TYPE` | `"default"` 复用已联网接口，`"lan"` 使用有线网，`"wifi_sta"` 连接热点，`"wifi_ap"` 创建热点 |
| `WLAN_DEVICE` | `"auto"` 自动选卡，也可固定为 `"usb"`、`"sdio"` 或 `"spi"` |
| `WIFI_SSID` | Wi-Fi STA 要连接的热点名，或 Wi-Fi AP 要创建的热点名 |
| `WIFI_PASSWORD` | Wi-Fi 密码；加密热点通常至少 8 个字符 |
| `NETWORK_TIMEOUT` | 等待连接和 IP 地址的超时时间，单位为秒 |

通常只需修改 `NETWORK_TYPE`、SSID 和密码。存在多块 Wi-Fi 设备且应用必须固定
其中一块时，才需要修改 `WLAN_DEVICE`。需要访问互联网的客户端例程通常使用
`"default"`、`"lan"` 或 `"wifi_sta"`；`"wifi_ap"` 更适合让本地终端连接开发板
上的服务。

## 推荐阅读顺序

1. 先运行公共网络管理例程，确认设备发现、IP 地址和默认上行正常。
1. 根据硬件阅读 LAN 或 WLAN 例程。
1. 再运行 TCP、UDP、HTTP、HTTPS 或组播例程验证具体协议。

```{toctree}
:maxdepth: 1

network_manager.md
lan.md
lte.md
wlan.md
tcp_client.md
tcp_server.md
udp_client.md
udp_server.md
udp_multicast.md
http_client.md
http_server.md
https_client.md
```
