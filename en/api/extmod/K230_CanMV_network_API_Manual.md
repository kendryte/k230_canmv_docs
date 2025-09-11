# `Network` Module API Manual

## Overview

This module is primarily used to configure and view network parameters. Once configured, the `socket` module can be used for network communication.

## `LAN` Class

Reference documentation: [Micropython LAN](https://docs.micropython.org/en/latest/library/network.LAN.html)

This class serves as the interface for configuring wired networks. Example code is as follows:

```python
import network
nic = network.LAN()
print(nic.ifconfig())

# Once configured, sockets can be used as usual
...
```

### Constructor

- **class** `network.LAN()` [¶](https://docs.micropython.org/en/latest/library/network.LAN.html#network.LAN)

  Creates a wired Ethernet object.

### Methods

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

## `WLAN` Class

Reference documentation: [Micropython WLAN](https://docs.micropython.org/en/latest/library/network.WLAN.html)

This class serves as the interface for configuring WiFi networks. Example code is as follows:

```python
import network
import time

SSID = "TEST"
PASSWORD = "12345678"

sta = network.WLAN(network.STA_IF)

sta.connect(SSID, PASSWORD)

timeout = 10  # seconds
start_time = time.time()

while not sta.isconnected():
    if time.time() - start_time > timeout:
        print("Connection timed out")
        break
    time.sleep(1)  # wait for a second before checking again

print(sta.ifconfig())

print(sta.status())

# Disconnect from the network, not necessary, just a test.
sta.disconnect()
print("Disconnected from the network")
print(sta.status())

```

### Constructor

- **class** `network.WLAN(*interface_id*)`

  Creates a WLAN network interface object. Supported interface types include `network.STA_IF` (station mode, connecting to an upstream WiFi access point) and `network.AP_IF` (access point mode, allowing other devices to connect). Methods differ based on the interface type; for example, only STA mode supports connecting to an access point using [`WLAN.connect()`](https://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.connect).

### Methods

- **WLAN.active()**

  Queries whether the current interface is active.

- **WLAN.connect(ssid=None, key=None, [info=None])**

  Connects to the specified `ssid` or `info`, where `info` is the result returned by `scan`.

  > Only available in `STA` mode.

- **WLAN.disconnect()**

  In `STA` mode, disconnects from the current WiFi network.
  In `AP` mode, a specific `mac` can be passed to disconnect a device.

- **WLAN.scan()**

  Scans for available WiFi networks. This method is only valid in STA mode and returns a list containing information about each network, such as:

  ```bash
  # print(sta.scan())
  [{"ssid":"XCTech", "bssid":xxxxxxxxx, "channel":3, "rssi":-76, "security":"SECURITY_WPA_WPA2_MIXED_PSK", "band":"2.4G", "hidden":0},...]
  ```

- **WLAN.status([param])**

  Returns the current network connection status. When no parameters are passed, return the current connection status. For example:

  ```python
  # Check connection status. Equivalent to sta.isconnected()
  print(sta.status())

  # Check the signal quality of the connection
  print(sta.status("rssi"))
  ```

  Supported configuration parameters include:

  - In `STA` mode:
    - `rssi`: Signal strength of the connection.
    - `ap`: Name of the connected hotspot.
  - In `AP` mode:
    - `stations`: Returns information about connected devices.

- **WLAN.isconnected()**

  Returns whether the device is connected to a hotspot.

  > Only available in `STA` mode.

- **WLAN.ifconfig([(ip, subnet, gateway, dns)])**

  Gets or sets the network interface parameters at the IP level. When called without parameters, it returns a tuple containing the IP address, subnet mask, gateway, and DNS server; passing parameters sets these values. For example:

  ```python
  sta.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  ```

- **WLAN.config(param)**

  Gets or sets the network interface configuration parameters. Supported parameters include MAC address, SSID, WiFi channel, whether to hide SSID, password, etc. Use keyword argument syntax to set parameters; to query a parameter, pass the parameter name. For example:

  ```python
  # View 'auto_reconnect' configuration
  print(sta.config('auto_reconnect'))

  # Set up automatic reconnection
  sta.config(auto_reconnect = True)
  ```

  Supported configuration parameters include:

  - In `STA` mode:
    - `mac`: MAC address.
    - `auto_reconnect`: Whether to automatically reconnect.
  - In `AP` mode:
    - `info`: Current hotspot information (read-only).
    - `country`: Country code.

- **WLAN.stop()**

  Stops the hotspot.

  > Only available in `AP` mode.

- **WLAN.info()**

  Queries current hotspot information.

  > Only available in `AP` mode.
