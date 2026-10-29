# Network Example Tutorials

```{warning}
K230D currently does not support network functionality, so network communication, RTSP streaming, and other examples cannot run on K230D.
```

## Example Path Description

The network examples in the documentation have two corresponding locations:

- Development board firmware path: `/sdcard/examples/14-Socket/`
- SDK source code path: `src/canmv/resources/examples/14-Socket/`

Open and run the scripts under the firmware path in CanMV IDE. When you need to view the original files in version management or modify the firmware built-in resources, use the SDK source code path. Each of the following pages will list both paths.

The common network library is located at:

- Development board firmware path: `/sdcard/libs/Network.py`
- SDK source code path: `src/canmv/resources/libs/Network.py`

Network examples use this library to select LAN or WLAN, wait for IP addresses, set the default uplink, and avoid hardcoding dynamic device names such as `eth0` and `wlan0`.

For Wi-Fi hardware, Realtek/brcmfmac/RW007/AIC8800/ESP-Hosted configuration, and various driver limitations, see [Wi-Fi Drivers and Device Selection](../../userguide/wifi_drivers.md).

## Common Network Parameters

Most examples provide the following parameters at the top of the file:

| Parameter | Description |
| :-- | :-- |
| `NETWORK_TYPE` | `"default"` reuses an already connected interface, `"lan"` uses wired network, `"wifi_sta"` connects to a hotspot, `"wifi_ap"` creates a hotspot |
| `WLAN_DEVICE` | `"auto"` automatically selects the card, can also be fixed as `"usb"`, `"sdio"`, or `"spi"` |
| `WIFI_SSID` | The hotspot name for Wi-Fi STA to connect to, or the hotspot name for Wi-Fi AP to create |
| `WIFI_PASSWORD` | Wi-Fi password; encrypted hotspots typically require at least 8 characters |
| `NETWORK_TIMEOUT` | Timeout for waiting for connection and IP address, in seconds |

Usually you only need to modify `NETWORK_TYPE`, SSID, and password. `WLAN_DEVICE` only needs to be modified when multiple Wi-Fi devices exist and the application must fix one of them. Client examples that need internet access typically use `"default"`, `"lan"`, or `"wifi_sta"`; `"wifi_ap"` is more suitable for letting local terminals connect to services on the development board.

## Recommended Reading Order

1. First run the common network management example to confirm that device discovery, IP address, and default uplink are working properly.
1. Read the LAN or WLAN examples based on the hardware.
1. Then run the TCP, UDP, HTTP, HTTPS, or multicast examples to verify specific protocols.

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
