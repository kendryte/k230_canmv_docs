# Wired Network Example Explanation

## Example Location

- Development board firmware path: `/sdcard/examples/14-Socket/network_lan.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/network_lan.py`

## Environment Preparation

Connect a USB Ethernet adapter or USB 4G ECM/NCM network card supported by the
development board to the board, and connect it to a router or network that
provides DHCP. The device name of the USB LAN is dynamically assigned. The
example selects the device through the logical LAN interface and does not depend
on a fixed name.

## Code Flow

### 1. Import Common Network Functions

```python
from libs.Network import configure_ip, connect_network, network_device_name
```

- `connect_network()`: Selects LAN, starts DHCP, waits for IP, and sets the default uplink;
- `configure_ip()`: Applies static address or DHCP, and waits for the address to take effect;
- `network_device_name()`: Reads the actual netdev name corresponding to the current LAN.

### 2. Connect to LAN Using DHCP

```python
a, ip = connect_network("lan")
print(a.active())
print(a.ifconfig())
```

`a` is the `network.LAN` object, and `ip` is the IPv4 address obtained after a
successful wait. On RT-Smart, `active()` is used to query whether the interface
is available, not to shut down the device. `ifconfig()` returns:

```text
(IP address, subnet mask, default gateway, DNS server)
```

### 3. Temporarily Switch to Static Address

```python
configure_ip(a, (
    "192.168.0.4",
    "255.255.255.0",
    "192.168.0.1",
    "8.8.8.8",
))
print(a.ifconfig())
```

The four values must match the actual network. The example address is for
demonstration only; if the network segment or gateway does not match, network
communication will be interrupted after switching.

### 4. Restore DHCP

```python
ip = configure_ip(a, "dhcp")
print("LAN device:", network_device_name(a))
print("LAN address:", ip)
```

`configure_ip()` not only initiates DHCP but also waits for a non-zero IP, so
subsequent Socket code does not need to poll `ifconfig()` by itself.

### 5. Query MAC Address

```python
print(a.config("mac"))
```

The return value is a 6-byte MAC. When a colon-separated string is needed, you
can use `libs.Network.mac_address(a)`.

## Run and Verify

1. Open `/sdcard/examples/14-Socket/network_lan.py` in CanMV IDE.
1. Make sure the network card and cable are connected before running the script.
1. The first `ifconfig()` should display the DHCP address.
1. The static address phase should display the example quadruple.
1. After restoring DHCP, `LAN address` should display the address assigned by the router again.

```{important}
The static address `192.168.0.4` may conflict with existing devices. It must be
modified according to the actual network segment before formal use, or remove
the static address test and keep only the DHCP part.
```

The Python usage of USB 4G ECM/NCM is the same as LAN. For supported modules and driver configurations, refer to
[EC200M-CN](./modules/ec200m.md). For complete interfaces, see
[network Module API Manual](../../api/extmod/k230_canmv_network_api_manual.md).
