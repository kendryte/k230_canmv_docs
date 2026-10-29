# `network` Module API Manual

## Overview

This module is primarily used to configure and view network parameters. After configuration is complete, the `socket` module can be used for network communication.

The system automatically registers network devices when the network card driver is loaded. Device names are dynamically assigned by the system, for example, USB Ethernet is typically `eth0`, Wi-Fi STA/AP is typically `wlan0`/`wlan0ap`. Applications should not hardcode device names; instead, they should obtain the current name through this module's device query interface or `libs.Network`. The path of the public network library in the development board firmware is `/sdcard/libs/Network.py`, and the SDK source code path is `src/canmv/resources/libs/Network.py`.

For supported Wi-Fi vendor drivers, firmware configuration, and security mode restrictions, see
[Wi-Fi Drivers and Device Selection](../../userguide/wifi_drivers.md).

## Network Device Management

### `network.get_dev_list()`

Returns a list of currently registered network device names. The list will change accordingly after devices are hot-plugged.

```python
import network

print(network.get_dev_list())
```

### `network.get_default_dev()`

Returns the name of the current default uplink network device. Returns `None` when no device satisfies the routing condition.

### `network.set_default_dev(device)`

Sets the preferred default uplink device. `device` can be a LAN/WLAN object, a device name returned by `get_dev_list()`, or a logical interface constant. Wi-Fi AP cannot be used as the default uplink device.

When the preferred device is unavailable, the system automatically switches to another available uplink device; when the preferred device recovers, it automatically switches back. Passing `None` clears the preferred device and restores fully automatic selection:

```python
import network

lan = network.LAN()
network.set_default_dev(lan)
print(network.get_default_dev())

# Restore automatic selection instead of disabling the default route
network.set_default_dev(None)
```

Automatic selection only considers LAN and Wi-Fi STA interfaces that are enabled, have their link connected, and have obtained a non-zero IP and gateway. When multiple interfaces are available simultaneously, LAN is preferred by default.

### `network.get_netdev_name(interface_id)`

Resolves a logical interface to the current device name. `interface_id` can use `network.STA_IF`, `network.AP_IF`, or `network.LAN_IF`; returns `None` when the interface is not yet available.

## `LAN` Class

Reference documentation: [Micropython LAN](https://docs.micropython.org/en/latest/library/network.LAN.html)

This class is the configuration interface for wired networks. Example code is as follows:

```python
import network
nic = network.LAN()
print(nic.ifconfig())

# After configuration is complete, you can use socket as usual
...
```

### Constructor

- **class** `network.LAN([interface_id])` [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN)

  Creates a wired Ethernet object. It is recommended to omit `interface_id`, or pass in `network.LAN_IF`. `LAN_RTL8152`, `LAN_NCM`, and `LAN_ECM` are retained for compatibility with legacy code; new code should not select a LAN through chip model.

### Methods

- **LAN.active([state])** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.active)

  Queries whether the interface is available when no argument is passed. Passing in `True` confirms that the interface is ready; RT-Smart does not support disabling the network interface through this method, and passing in `False` will not shut down the device.

- **LAN.isconnected()** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.isconnected)

  Returns `True` if connected to the network, `False` if not connected.

- **LAN.ifconfig([(ip, subnet, gateway, dns)])** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.ifconfig)

  Gets or sets IP-level network interface parameters, including IP address, subnet mask, gateway, and DNS server. When called without arguments, returns a 4-tuple containing the above information; to set parameters, pass in a 4-tuple containing IP address, subnet mask, gateway, and DNS. For example:

  ```python
  nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  ```

- **LAN.config(*config_parameters*)** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.config)

  Gets or sets network interface parameters. Currently only supports setting or getting the MAC address. For example:

  ```python
  import network
  lan = network.LAN()
  # Set MAC address
  lan.config(mac="42:EA:D0:C2:0D:83")
  # Get MAC address
  print(lan.config("mac"))
  ```

- **LAN.netdev_name()**

  Returns the dynamic network device name currently corresponding to this object; returns `None` when the device is unavailable.

## `WLAN` Class

Reference documentation: [Micropython WLAN](https://docs.micropython.org/en/latest/library/network.WLAN.html)

This class is the WiFi network configuration interface. Example code is as follows:

```python
import network
import time

SSID = "TEST"
PASSWORD = "12345678"

sta = network.WLAN(network.STA_IF)

sta.connect(SSID, PASSWORD)

timeout = 10  # Unit: seconds
start_time = time.time()

while not sta.isconnected():
    if time.time() - start_time > timeout:
        print("Connection timed out")
        break
    time.sleep(1)  # Please wait a moment before connecting

print(sta.ifconfig())

print(sta.status())

# Disconnecting here is just a test. In actual applications, you may not need to disconnect
sta.disconnect()
print("Network disconnected")
print(sta.status())

```

### Constructor

- **class** `network.WLAN([interface_id[, wlan_device]])`

  Creates a WLAN network interface object. When `interface_id` is omitted, STA is used by default. This parameter supports
  `network.STA_IF` (station mode, connecting
  to an upstream Wi-Fi access point) and `network.AP_IF` (access point mode). The optional
  `wlan_device` is used to select the physical transport type among multiple Wi-Fi devices:

  - `network.WLAN_AUTO`: automatic selection, recommended;
  - `network.WLAN_USB`: USB Wi-Fi;
  - `network.WLAN_SDIO`: SDIO Wi-Fi;
  - `network.WLAN_SPI`: SPI Wi-Fi.

  Automatic selection prefers a device that is already working in the current role; otherwise it searches in the order of SDIO, SPI, USB.
  This parameter selects the transport type, not the vendor model; only pass the second argument when you really need to fix a specific hardware
  connection method.

  ```python
  # Automatically select available Wi-Fi
  sta = network.WLAN(network.STA_IF, network.WLAN_AUTO)

  # Explicitly select USB Wi-Fi
  usb_sta = network.WLAN(network.STA_IF, network.WLAN_USB)
  ```

### Methods

- **WLAN.active()**

  When called without arguments, queries whether the interface is available. When called with `True`, waits for the selected WLAN device to complete registration;
  RT-Smart does not support deactivating the interface through this method; passing `False` will not turn off the device.

- **WLAN.connect(ssid=None, key=None, [info = None])**

  Connects to the specified `ssid` or `info`, where `info` is the result returned by `scan`.

  > Only available in `Sta` mode

- **WLAN.disconnect()**

  In `Sta` mode, disconnects the current WiFi network connection.
  In `Ap` mode, you can pass a specific `mac` to disconnect a device.

- **WLAN.scan()**

  Scans for available WiFi networks. This method is only valid in STA mode, and the returned list contains information for each network, for example:

  ```bash
  # print(sta.scan())
  [{"ssid":"XCTech", "bssid":xxxxxxxxx, "channel":3, "rssi":-76, "security":"SECURITY_WPA_WPA2_MIXED_PSK", "band":"2.4G", "hidden":0},...]
  ```
  
- **WLAN.status([param])**

  Returns information about the current network connection. When called without arguments, returns the current connection status. For example:

  ```python
  # Check connection status, equivalent to sta.isconnected()
  print(sta.status())

  # Check the signal quality of the connection
  print(sta.status("rssi"))
  ```

  Supported configuration parameters include:

  - In `Sta` mode
    - `rssi`: connection signal quality
    - `ap`: name of the connected hotspot
  - In `Ap` mode
    - `stations`: returns information about connected devices
  
- **WLAN.isconnected()**

  Returns whether it is connected to a hotspot

  > Only available in `Sta` mode

- **WLAN.ifconfig([(ip, subnet, gateway, dns)])**

  Gets or sets IP-level network interface parameters. When called without arguments, returns a tuple containing IP address, subnet mask, gateway, and DNS server; when arguments are passed, sets these values. For example:

  ```python
  sta.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  ```

- **WLAN.config(param)**

  Gets or sets configuration parameters for the network interface. Use keyword argument syntax when setting parameters; to query a parameter, just pass the parameter name. For example:

  ```python
  # Check auto_reconnect configuration
  print(sta.config('auto_reconnect'))

  # Set auto-reconnect
  sta.config(auto_reconnect = True)
  ```

  Supported configuration parameters include:

  - In `Sta` mode
    - `mac`: `mac` address
    - `auto_reconnect`: whether to auto-reconnect
  - In `Ap` mode
    - `ssid`: hotspot name. Passing this parameter will configure and start the hotspot; `key` and `security` can be used together to specify the password and security type
    - `key`: hotspot password, length should be 8 to 64 characters in encrypted mode; omit this parameter in open mode
    - `security`: hotspot security type. `ssid` must also be passed during configuration; the current value can also be queried via `ap.config('security')`
    - `info`: current hotspot information, can only be queried
    - `country`: country code

  Common security types in AP mode are as follows. The specific available types depend on the WiFi driver used by the development board; unsupported types will cause configuration to fail and return `False`.

  - `SECURITY_OPEN`: open hotspot, no password used
  - `SECURITY_WPA_TKIP_PSK`: WPA-PSK (TKIP)
  - `SECURITY_WPA2_AES_PSK`: WPA2-PSK (AES), recommended
  - `SECURITY_WPA2_MIXED_PSK`: WPA2-PSK (AES/TKIP mixed mode)

  Create a WPA2 encrypted hotspot:

  ```python
  import network

  ap = network.WLAN(network.AP_IF)
  result = ap.config(
      ssid='CanMV_AP',
      key='12345678',
      security=ap.SECURITY_WPA2_AES_PSK,
  )
  print(result)
  print(ap.config('security'))
  ```

  When creating an open hotspot, omit `key` and set the security type to `SECURITY_OPEN`:

  ```python
  ap.config(ssid='CanMV_Open', security=ap.SECURITY_OPEN)
  ```

  When `security` is not specified, passing `key` defaults to using `SECURITY_WPA2_AES_PSK`; when `key` is not passed, `SECURITY_OPEN` is used by default.
  
- **WLAN.stop()**

  Stops the hotspot

  > Only available in `Ap` mode

- **WLAN.info()**

  Queries current hotspot information

  > Only available in `Ap` mode

- **WLAN.netdev_name()**

  Returns the dynamic network device name of the physical device selected by this WLAN object in the current role; returns `None` when the device is unavailable.

## `libs.Network` Common Network Library

CanMV examples uniformly use `/sdcard/libs/Network.py` to manage networks. This library is responsible for selecting interfaces, waiting for IP, setting the default uplink, displaying device information, and allowing various components of an application to share the same interface object.

### Network Types and Wi-Fi Devices

`network_type` supports:

- `"default"`: reuses the default/auto interface that is already connected to the network;
- `"lan"`: uses LAN;
- `"wifi_sta"`: connects to a Wi-Fi AP;
- `"wifi_ap"`: creates a Wi-Fi AP.

`wlan_device` supports `"auto"`, `"usb"`, `"sdio"`, and `"spi"`, defaulting to `"auto"`.

### `connect_network()`

Connects to the specified network and returns `(netif, ip)`:

```python
from libs.Network import connect_network

netif, ip = connect_network(
    "wifi_sta",
    ssid="TEST",
    password="12345678",
    wlan_device="auto",
    timeout=20,
)
print(ip)
```

Common parameters include `ip_config` (`"dhcp"` or a static `ifconfig` tuple), `channel`, `set_default`, and `show`. LAN and Wi-Fi STA are set as the preferred uplink by default; Wi-Fi AP will not be set as the default uplink.

### `NetworkManager`

`NetworkManager` saves and reuses interfaces, suitable for applications where multiple components such as HTTP, WebSocket, and media streaming share the network. When `connect()` is called repeatedly, if the original interface is still available, a second interface will not be created.

```python
from libs.Network import NetworkManager

manager = NetworkManager(
    network_type="wifi_sta",
    ssid="TEST",
    password="12345678",
    wlan_device="auto",
    timeout=20,
)
netif, ip = manager.connect()
manager.show_info()
```

Main methods:

- `connect(**kwargs)`: connects or reuses the interface, returns `(netif, ip)`;
- `disconnect(restore_default=True)`: stops Wi-Fi, and restores automatic route selection as needed;
- `info()` / `show_info()`: returns or prints current interface information;
- `show_devices()`: prints and returns the list of registered devices;
- `wait_for_ip()`: waits for the current interface to obtain an IP;
- `set_default()`: sets the current interface as the preferred uplink;
- `scan()`: uses the selected Wi-Fi device to scan for hotspots.

### Other Helper Functions

- `get_interface()`: gets the interface object, but does not connect or modify the default route;
- `get_devices()` / `get_default_device()` / `set_default_device()`: device list and default
  uplink management;
- `configure_ip()` / `wait_for_ip()` / `has_ip()`: IP configuration and readiness check;
- `network_device_name()` / `network_info()` / `show_network_info()`: queries interface runtime
  information;
- `mac_address()`: returns the MAC address in lowercase colon-separated format;
- `scan_wifi()`: scans for hotspots on the specified Wi-Fi device.
