# Public Network Management Routine Explanation

## Routine Location

- Development board firmware path: `/sdcard/examples/14-Socket/network_manager.py`
- SDK source path: `src/canmv/resources/examples/14-Socket/network_manager.py`

The public library itself resides at `/sdcard/libs/Network.py`, corresponding to the SDK source
`src/canmv/resources/libs/Network.py`.

## Routine Purpose

This routine demonstrates the complete basic workflow of `libs.Network.NetworkManager`: viewing
registered NICs, selecting a network type, establishing a connection, displaying interface status,
and querying the current default uplink. The manager stores interface objects, so HTTP,
WebSocket, or media components within the same application can reuse the same connection.

## Configuration Parameters

```python
NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

| Configuration | Example Value | Purpose |
| :-- | :-- | :-- |
| `NETWORK_TYPE` | `"wifi_sta"` | Choose `default`, `lan`, `wifi_sta`, or `wifi_ap` |
| `WLAN_DEVICE` | `"auto"` | Auto-select Wi-Fi; can also be fixed to USB, SDIO, or SPI |
| `WIFI_SSID` | `"TEST"` | SSID used for STA connection or AP creation |
| `WIFI_PASSWORD` | `"12345678"` | Wi-Fi password |
| `NETWORK_TIMEOUT` | `20` | Wait up to 20 seconds to obtain a valid address |

`"default"` only reuses the default/auto interface that is already connected to the network; it
will not actively connect to a new Wi-Fi. If the device is not yet connected to the network, you
should explicitly choose `"lan"` or `"wifi_sta"`.

## Code Flow

### 1. Create the Manager

```python
manager = NetworkManager(
    network_type=NETWORK_TYPE,
    ssid=WIFI_SSID,
    password=WIFI_PASSWORD,
    wlan_device=WLAN_DEVICE,
    timeout=NETWORK_TIMEOUT,
    show=False,
)
```

The constructor only saves the configuration and does not connect immediately. `show=False`
means that information will not be repeatedly printed during the connection process; the routine
later explicitly calls `show_devices()` and `show_info()`.

### 2. View Dynamically Registered Devices

```python
manager.show_devices()
```

This call prints the complete device list returned by `network.get_dev_list()`, along with the
current default device. Device names are dynamically assigned by the driver, and the application
should not assume that names remain fixed based on hardware type.

### 3. Connect and Wait for IP

```python
netif, ip = manager.connect()
```

The behavior for different `NETWORK_TYPE` values is as follows:

- `lan`: obtain the LAN object, start DHCP if necessary, then wait for a valid IP;
- `wifi_sta`: select the WLAN device, connect to the SSID, then wait for successful association and a valid IP;
- `wifi_ap`: create a hotspot and wait for the AP address, without setting the AP as the default uplink;
- `default`: find an interface that is already connected and has a valid IP.

After the LAN and Wi-Fi STA connections succeed, the manager sets the interface as the preferred
default uplink. When the interface becomes invalid, the system can still automatically switch to
other ready uplink interfaces.

### 4. View Results

```python
manager.show_info()
print("Network ready:", ip)
print("Default network device:", get_default_device() or "auto")
```

`show_info()` prints the device name, activation status, connection status, IP configuration,
and MAC address. The returned `netif` is the actual `network.LAN` or `network.WLAN` object, which
can be passed directly to other modules.

## Interface Reuse

The manager saves the `netif` and `ip`. When `manager.connect()` is called again, if the original interface is still connected and has a valid address, the same object is returned directly. If called again after the network is disconnected, the recovery process is executed.

```python
netif, ip = manager.connect()
# Pass the same netif to multiple components of the application
netif, ip = manager.connect()  # Will not create a second interface if still available
```

`manager.disconnect()` is used to stop Wi-Fi and, by default, clears the manual preferred device and restores automatic route selection. LAN will not be hardware-disabled by calling `disconnect()`.

## Running and Verification

1. Open `/sdcard/examples/14-Socket/network_manager.py` in CanMV IDE.
1. Modify the network type and Wi-Fi credentials.
1. Run the script and check whether the target interface appears in `Network devices`.
1. Confirm that `Network ready` is not `0.0.0.0`.
1. For LAN/Wi-Fi STA, confirm that `Default network device` matches the selected interface.

If `network address timeout` occurs, check the network cable or Wi-Fi credentials, DHCP service, and whether `WLAN_DEVICE` selects an actually existing device in order.

For the complete interface description, see the [network module API manual](../../api/extmod/k230_canmv_network_api_manual.md).
