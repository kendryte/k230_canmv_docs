# Wireless Network Example Explanation

## Overview

This tutorial will guide you on how to perform basic wireless network (WiFi) operations using MicroPython's `network` module on CanMV. This includes connecting to a wireless access point (AP) as a station (STA) and creating your own access point (AP).

* **sta_test()**: Demonstrates how to connect to a wireless network as a station (STA), including checking the current connection status, scanning available networks, connecting to a specific AP, viewing IP configuration, and disconnecting.
* **ap_test()**: Shows how to configure and start a wireless access point (AP), including setting SSID, channel, and password, and checking the AP's configuration and status.

## Interface Calls and Function Descriptions

### sta_test

* **`network.WLAN(id)`**: Initializes a WLAN object. `id` is 0 for STA mode.
* **`sta.active(bool)`**: Activates or deactivates STA mode. Pass `True` to activate, `False` to deactivate. If called without arguments, it returns the current activation status.
* **`sta.status()`**: Returns the current status of the STA, such as whether it is connected to an AP.
* **`sta.connect(ssid, password)`**: Attempts to connect to an AP with the specified SSID and password. This method does not directly return whether the connection was successful, but you can check the connection status using `sta.status()` or `sta.isconnected()`.
* **`sta.ifconfig()`**: Returns the IP configuration of the STA, such as IP address, subnet mask, gateway, and DNS server.
* **`sta.isconnected()`**: Returns `True` if the STA is connected to an AP, otherwise returns `False`.
* **`sta.disconnect()`**: Disconnects the STA from the current AP.

#### Complete Example

```python
import network

def sta_test():
    sta = network.WLAN(0)
    if not sta.active():
        sta.active(True)
    # Check if STA is active
    print(sta.active())
    # Check STA status
    print(sta.status())
    # STA connects to AP
    print(sta.connect("Canaan", "Canaan314"))
    # Check status
    print(sta.status())
    # View IP configuration
    print(sta.ifconfig())
    # Check if connected
    print(sta.isconnected())
    # Disconnect
    print(sta.disconnect())
    # Connect to AP
    print(sta.connect("Canaan", "Canaan314"))
    # Check status
    print(sta.status())

sta_test()
```

### ap_test

* **`network.WLAN(network.AP_IF)`**: Initializes a WLAN object and sets it to AP mode.
* **`ap.active(bool)`**: Activates or deactivates AP mode. Pass `True` to activate, `False` to deactivate. If called without arguments, it returns the current activation status.
* **`ap.config(ssid=None, password=None, channel=None, ...)`**: Configures the AP parameters such as SSID, password, channel, etc. If called without any parameters, it returns the current configuration.
* **`ap.config(key)`**: If `key` is a string representation of a configuration item like `'ssid'`, `'channel'`, etc., it returns the value of that configuration item.
* **`ap.status()`**: Returns the current status of the AP.

#### Complete Example

```python
import network

def ap_test():
    ap = network.WLAN(network.AP_IF)
    if not ap.active():
        ap.active(True)
    # Check if AP is active
    print(ap.active())
    # Configure and create AP
    ap.config(ssid='k230_ap_wjx', channel=11, key='12345678')
    # View AP SSID
    print(ap.config('ssid'))
    # View AP channel
    print(ap.config('channel'))
    # View all AP configuration
    print(ap.config())
    # Check AP status
    print(ap.status())
    # Check if STA is connected to AP
    print(ap.isconnected())

ap_test()
```

For detailed interface definitions, please refer to the [network module API documentation](../../api/extmod/K230_CanMV_network_API_Manual.md).
