# NimBLE Bluetooth Low Energy

## Architecture and Support Scope

CanMV uses the MicroPython `bluetooth` module and the NimBLE host stack to implement
GAP, GATT, L2CAP, and SMP for BLE. NimBLE does not access USB or SPI directly; instead
it opens the first `/dev/hciN` H:4 controller auto-registered by RT-Smart.

The currently available controller backends are as follows:

| Backend | Transport | RT-Smart Configuration | Limitations |
| :-- | :-- | :-- | :-- |
| AIC8800 series combo device | USB | `AIC8800_WIFI_BLE=y` | USB transport only; does not implement SCO audio |
| ESP-Hosted-MCU | SPI Full/Half-Duplex | `ESP_HOSTED_BLE=y` | ESP firmware must also enable Bluetooth HCI |

Realtek RTL8189FTV/RTL8733BS, Broadcom brcmfmac, legacy CYW43xx, RW007,
AIC8800 SDIO, and ESP-Hosted-FG/NG do not register a BLE HCI controller. The current
integration targets BLE and does not support Bluetooth Classic or Bluetooth audio.

## Build Configuration

BLE requires enabling both the controller driver and the CanMV NimBLE host:

```text
# CanMV MicroPython Configuration
ENABLE_BLUETOOTH=y

# Choose one of the following controllers, or both may be compiled together
AIC8800_WIFI_TRANSPORT_USB=y
AIC8800_WIFI_BLE=y

# or
RT_USING_ESP_HOSTED_MCU=y
ESP_HOSTED_BLE=y
```

`AIC8800_WIFI_BLE` and `ESP_HOSTED_BLE` automatically select RT-Smart
`RT_USING_BT_HCI`. `ENABLE_BLUETOOTH` is disabled by default, so using firmware that
includes the related Wi-Fi drivers does not imply that the Python `bluetooth` module
has been enabled.

AIC8800DC additionally requires completing the Bluetooth patch before the controller
is available. ESP-Hosted-MCU requires ESP firmware matching the host driver; controller
start and stop are performed via the FeatureControl RPC. For detailed Wi-Fi transport
configuration, see [Wi-Fi Drivers and Device Selection](wifi_drivers.md).

## Initialization and Scanning

The following code enables the controller, actively scans for 5 seconds, and prints
the scan results:

```python
import bluetooth
import time

_IRQ_SCAN_RESULT = 5
_IRQ_SCAN_DONE = 6

ble = bluetooth.BLE()

def on_ble_irq(event, data):
    if event == _IRQ_SCAN_RESULT:
        addr_type, addr, adv_type, rssi, adv_data = data
        print("scan", addr_type, bytes(addr), adv_type, rssi, bytes(adv_data))
    elif event == _IRQ_SCAN_DONE:
        print("scan done")

ble.irq(on_ble_irq)
ble.active(True)
print("MAC:", ble.config("mac"))
ble.gap_scan(5000, 30000, 30000, True)
time.sleep_ms(5500)
```

`active(True)` opens the first available `/dev/hciN` and initializes the controller.
The current CanMV interface cannot select between `hci0`, `hci1` by name; when
multiple controllers are connected simultaneously, the actual one used is determined
by registration order.

## Advertising Test

The following payload contains the generic discoverable flag and the device name
`CanMV-K230`:

```python
import bluetooth

ble = bluetooth.BLE()
ble.active(True)

adv_data = b"\x02\x01\x06\x0b\x09CanMV-K230"
ble.gap_advertise(100_000, adv_data=adv_data)
```

The advertising interval is in microseconds. An actual GATT peripheral also needs to
register services/characteristics via `gatts_register_services()`, and handle connect,
write, and disconnect events in the IRQ callback. When used as a central, the IRQ
handles scanning, connection, service discovery, and characteristic read/write/notify.

## Shutdown

After finishing BLE operations, execute:

```python
# While scanning, use ble.gap_scan(None)
# While advertising, use ble.gap_advertise(None)
ble.active(False)
```

`active(False)` stops NimBLE and closes the HCI device. ESP-Hosted-MCU also
deactivates the remote controller; `active(True)` can be executed again afterwards.

## Troubleshooting

1. `import bluetooth` fails: confirm that the CanMV build has `ENABLE_BLUETOOTH`
   enabled.
1. `active(True)` reports it cannot open HCI: check whether `/dev/hciN` was registered
   in the startup log, and confirm that the controller's corresponding
   `AIC8800_WIFI_BLE` or `ESP_HOSTED_BLE` is enabled.
1. AIC USB has no HCI: verify the device USB ID, combo interface enumeration, and
   the Bluetooth patch log for the firmware and DC model; AIC SDIO does not provide
   this backend.
1. ESP controller does not appear: verify the ESP-Hosted-MCU firmware, transport,
   Reset, and FeatureControl support; FG/NG firmware cannot replace the MCU personality.
1. Multiple HCIs exist simultaneously but connect to the wrong device: currently CanMV
   automatically selects the first registered `/dev/hciN`; only the required controller
   backends should be enabled in the firmware.
