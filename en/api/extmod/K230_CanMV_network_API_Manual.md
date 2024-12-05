# 2.2 `Network` Module API Manual

## 1. Overview

This module is primarily used to configure and view network parameters. Once configured, the `socket` module can be used for network communication.

## 2. `LAN` Class

Reference documentation: [Micropython LAN](https://docs.micropython.org/en/latest/library/network.LAN.html)

This class serves as the interface for configuring wired networks. Example code is as follows:

```python
import network
nic = network.LAN()
print(nic.ifconfig())

# Once configured, sockets can be used as usual
...
```

### 2.1 Constructor

- **class** `network.LAN()` [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN)

  Creates a wired Ethernet object.

### 2.2 Methods

- **LAN.active([state])** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.active)

  Activates or deactivates the network interface. Pass a boolean parameter `True` to activate, `False` to deactivate. If no parameter is passed, it returns the current state.

- **LAN.isconnected()** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.isconnected)

  Returns `True` if connected to the network, `False` otherwise.

- **LAN.ifconfig([(ip, subnet, gateway, dns)])** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.ifconfig)

  Gets or sets the network interface parameters at the IP level, including IP address, subnet mask, gateway, and DNS server. When called without parameters, it returns a tuple containing the above information; to set parameters, pass a tuple containing the IP address, subnet mask, gateway, and DNS. For example:

  ```python
  nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  ```

- **LAN.config(*config_parameters*)** [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN.config)

  Gets or sets network interface parameters. Currently, only the MAC address can be set or retrieved. For example:

  ```python
  import network
  lan = network.LAN()
  # Set MAC address
  lan.config(mac="42:EA:D0:C2:0D:83")
  # Get MAC address
  print(lan.config("mac"))
  ```

## 3. `WLAN` Class

Reference documentation: [Micropython WLAN](https://docs.micropython.org/en/latest/library/network.WLAN.html)

This class serves as the interface for configuring WiFi networks. Example code is as follows:

```python
import network
# Enable STA mode and connect to WiFi access point
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('your-ssid', 'your-password')
# Once configured, sockets can be used as usual
```

### 3.1 Constructor

- **class** `network.WLAN(*interface_id*)`

  Creates a WLAN network interface object. Supported interface types include `network.STA_IF` (station mode, connecting to an upstream WiFi access point) and `network.AP_IF` (access point mode, allowing other devices to connect). Methods differ based on the interface type; for example, only STA mode supports connecting to an access point using [`WLAN.connect()`](https://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.connect).

### 3.2 Methods

- **WLAN.active([is_active])**

  Activates (`True`) or deactivates (`False`) the network interface by passing a boolean parameter. If no parameter is passed, it returns the current state of the interface.

- **WLAN.connect(ssid=None, password=None, bssid=None)**

  Connects to a WiFi network using the specified SSID and password. If `bssid` is provided, it connects only to the access point with that MAC address (SSID must also be specified in this case).

- **WLAN.disconnect()**

  Disconnects from the current WiFi network.

- **WLAN.scan()**

  Scans for available WiFi networks. This method is only valid in STA mode and returns a list containing information about each network, such as:

  ```bash
  # print(sta.scan())
  bssid / frequency / signal strength / security protocol / ssid
  da:c5:47:12:80:ab       2462    -30     [WPA2-PSK-CCMP][ESS]    Redmi Note 11 Pro
  72:a8:d3:ab:c8:2c       2412    -42     [WPA2-PSK-CCMP][WPS][ESS]       wifi_test
  ```

- **WLAN.status([param])**

  Returns the current network connection status. When no parameter is passed, it returns detailed connection information, including BSSID, frequency, SSID, encryption type, IP address, etc. For example:

  ```bash
  # print(sta.status())
  bssid=c6:b5:b6:86:64:d7
  freq=2462
  ssid=wjx_pc
  ip_address=192.168.137.221
  ```

- **WLAN.isconnected()**

  In STA mode, returns `True` if connected to a WiFi access point and has a valid IP address, otherwise returns `False`. In AP mode, returns `True` if devices are connected to the access point.

- **WLAN.ifconfig([(ip, subnet, gateway, dns)])**

  Gets or sets the network interface parameters at the IP level. When called without parameters, it returns a tuple containing the IP address, subnet mask, gateway, and DNS server; passing parameters sets these values. For example:

  ```python
  nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  ```

- **WLAN.config(param)**

  Gets or sets the network interface configuration parameters. Supported parameters include MAC address, SSID, WiFi channel, whether to hide SSID, password, etc. Use keyword argument syntax to set parameters; to query a parameter, pass the parameter name. For example:

  ```python
  # Set access point SSID and channel
  ap.config(ssid='k230_ap_wjx', channel=11, key='12345678')
  # Query configuration parameters
  print(ap.config('ssid'))
  print(ap.config('channel'))
  ```

  Supported configuration parameters include:

  | Parameter | Description                  |
  | --------- | ---------------------------- |
  | mac       | MAC address (bytes)          |
  | ssid      | WiFi access point name (string) |
  | channel   | WiFi channel (integer)       |
  | hidden    | Whether to hide SSID (boolean) |
  | password  | WiFi connection password (string) |
  