# USB 4G LTE Example Explanation

## Example Location

- Development board firmware path: `/sdcard/examples/14-Socket/network_lte.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/network_lte.py`

This example sends AT commands to an EC200M-class 4G module through a USB serial port. It first queries the module version, then initiates ECM data dialing. After the dialing is successful, the system network driver automatically registers the module's data interface as a LAN-type network device.

## Prerequisites

1. Install an antenna for the 4G module and insert a usable SIM card.
1. Connect the module to the development board's USB Host interface.
1. Confirm that the firmware has enabled the USB Serial and CDC ECM drivers required by the module.
1. Check the `/dev/ttyUSB*` devices enumerated by the module in the RT-Smart command line.

For specific driver options, SIM card checks, and AT debugging methods, see [EC200M-CN Module Description](./modules/ec200m.md).

## Code Flow

### 1. Open AT Serial Port

```python
from usb import Serial

ser = Serial("/dev/ttyUSB1", 200)

while True:
    if ser.open():
        break
    time.sleep(1)
```

The example uses `/dev/ttyUSB1` by default and retries every second when opening fails. Different modules, firmware, or USB enumeration order may produce different nodes; if there is no response, you should first confirm the actual AT command port and modify this path.

### 2. Query Module Firmware Version

```python
ser.write("AT+GMR\r\n")
time.sleep(0.1)
data = ser.read()
print(data)
```

`AT+GMR` is used to confirm that serial communication is normal and to read the module version. Under normal circumstances, the output should include version information and `OK`; garbled characters usually indicate incorrect serial port parameters or port, and no response indicates that power, USB enumeration, and port should be checked.

### 3. Initiate ECM Dial-up

```python
ser.write("AT+QNETDEVCTL=1,1,1\r\n")
time.sleep(0.1)
data = ser.read()
print(data)
```

This command asks the module to establish a data connection. The AT command returning `OK` only indicates that the command has been accepted; the module may still need some time to complete network registration, dialing, USB network interface registration, and address configuration.

### 4. Close AT Serial Port

```python
ser.close()
```

Closing the Python serial port object does not actively disconnect an already-established data connection. If you still need to query signal, registration status, or dialing status afterwards, you should keep the serial port in the application and manage it according to the module's AT manual.

## Verifying the Network Interface

After the script completes, you can use `ifconfig` on the RT-Smart command line to check the new interface and IP. In Python, you can also run the common network management routine to confirm the device has registered dynamically and obtained an address:

```python
import network
from libs.Network import connect_network

print(network.get_dev_list())
netif, ip = connect_network("lan")
print(netif.netdev_name(), ip)
```

`connect_network("lan")` will wait for a LAN-type interface to obtain a valid address and set the default uplink; it does not need to assume the 4G data interface is always named `eth0`.

If no network interface appears, check the SIM status, antenna, signal, APN, ECM mode, and CDC ECM driver in sequence. If the interface appears but has no IP, continue checking the dial-up status and carrier data services.
