# Explanation of Wireless Network Examples

## Example Locations

Wi-Fi STA example:

- Development board firmware path: `/sdcard/examples/14-Socket/network_wlan_sta.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/network_wlan_sta.py`

Wi-Fi AP example:

- Development board firmware path: `/sdcard/examples/14-Socket/network_wlan_ap.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/network_wlan_ap.py`

## WLAN Device Selection

Both examples use:

```python
WLAN_DEVICE = "auto"
```

Valid values are `"auto"`, `"usb"`, `"sdio"`, and `"spi"`. Typically keep `"auto"`
to let the system choose from registered devices. Only fix this parameter when
multiple Wi-Fi modules are installed simultaneously and the application must
use a specific transport type.

The current SDK supports RTL8189FTV/RTL8733BS and Broadcom brcmfmac SDIO, RW007
SPI, AIC8800 USB/SDIO, as well as ESP-Hosted SPI/SDIO solutions enabled per
firmware configuration. For details on specific drivers, default board
configuration, and security mode restrictions, see
[Wi-Fi Drivers and Device Selection](../../userguide/wifi_drivers.md). `WLAN_DEVICE`
only selects the transport type and cannot select between devices from
different vendors or models on the same bus.

## Wi-Fi STA Example

STA mode is used to connect to an existing wireless router or hotspot.

### 1. Configure Credentials

```python
SSID = "TEST"
PASSWORD = "12345678"
WLAN_DEVICE = "auto"
```

Modify the SSID and password to match the on-site hotspot information. SSID is
case-sensitive.

### 2. Connect and Wait for Address

```python
from libs.Network import connect_network

sta, ip = connect_network(
    "wifi_sta",
    ssid=SSID,
    password=PASSWORD,
    wlan_device=WLAN_DEVICE,
    timeout=10,
)
```

This step sequentially completes physical WLAN selection, device registration
waiting, hotspot connection, DHCP address waiting, and default uplink
configuration. An exception is thrown on failure or if no address is obtained
within 10 seconds, so the application does not need to poll indefinitely on its
own.

### 3. Check Status

```python
print(sta.ifconfig())
print(sta.status())
```

`ifconfig()` returns IP parameters, and `status()` returns the connection
status. To view the dynamic device name corresponding to the current Wi-Fi
STA, you can additionally call `sta.netdev_name()`.

### 4. Disconnection Test

```python
sta.disconnect()
print("Disconnect")
print(sta.status())
```

The active disconnection at the end of the example is only for demonstration.
Programs that need continuous network access should remove these lines. After
disconnection, the default route management will attempt to select another
ready LAN or Wi-Fi STA.

## Example LocationWi-Fi STA example

### 1. Create a Hotspot

```python
from libs.Network import connect_network

ap, ip = connect_network(
    "wifi_ap",
    ssid="k230_ap_wjx",
    password="12345678",
    wlan_device=WLAN_DEVICE,
)
```

The common network library selects the WLAN AP device, creates an encrypted hotspot, and waits for the AP address. The Wi-Fi AP is a local
access interface and will not be set as the default Internet uplink.

### 2. View hotspot information

```python
print(ap.info())
print(ap.status())
```

`info()` returns the hotspot configuration, and `status()` returns the AP status. To view the dynamic device name, call
`ap.netdev_name()`; to view connected terminals, use `ap.status("stations")`.

### 3. Stop Hotspot

The example keeps the hotspot running. If you need to stop it proactively before the application exits, call:

```python
ap.stop()
```

## Operation and Verification

STA test:

1. Open `/sdcard/examples/14-Socket/network_wlan_sta.py`.
1. Modify the SSID and password, then run it.
1. Confirm that the IP address in `ifconfig()` is not `0.0.0.0`.
1. The example will actively disconnect after execution reaches the end.

AP test:

1. Open `/sdcard/examples/14-Socket/network_wlan_ap.py` and run it.
1. Use a phone to search for and connect to `k230_ap_wjx`, using the password `12345678`.
1. Check the AP information and status printed to the serial port.

If the device is reported as unavailable after specifying `WLAN_DEVICE`, change it back to `"auto"` first. See the
[network module API manual](../../api/extmod/k230_canmv_network_api_manual.md) for the complete interface definitions.
