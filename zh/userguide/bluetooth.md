# NimBLE 低功耗蓝牙

## 架构与支持范围

CanMV 使用 MicroPython `bluetooth` 模块和 NimBLE host stack 实现 BLE 的 GAP、
GATT、L2CAP 与 SMP。NimBLE 不直接访问 USB 或 SPI，而是打开 RT-Smart 自动注册的
第一个 `/dev/hciN` H:4 controller。

当前可用的 controller backend 如下：

| 后端 | 传输 | RT-Smart 配置 | 限制 |
| :-- | :-- | :-- | :-- |
| AIC8800 系列组合设备 | USB | `AIC8800_WIFI_BLE=y` | 仅 USB transport；不实现 SCO 音频 |
| ESP-Hosted-MCU | SPI Full/Half-Duplex | `ESP_HOSTED_BLE=y` | ESP 固件也必须启用 Bluetooth HCI |

Realtek RTL8189FTV/RTL8733BS、Broadcom brcmfmac、旧版 CYW43xx、RW007、
AIC8800 SDIO 以及 ESP-Hosted-FG/NG 不会注册 BLE HCI controller。当前集成面向
BLE，不支持 Bluetooth Classic 或蓝牙音频。

## 构建配置

BLE 需要同时启用 controller 驱动和 CanMV NimBLE host：

```text
# CanMV MicroPython Configuration
ENABLE_BLUETOOTH=y

# 以下 controller 二选一，也可以同时编译
AIC8800_WIFI_TRANSPORT_USB=y
AIC8800_WIFI_BLE=y

# 或
RT_USING_ESP_HOSTED_MCU=y
ESP_HOSTED_BLE=y
```

`AIC8800_WIFI_BLE` 和 `ESP_HOSTED_BLE` 会自动选择 RT-Smart
`RT_USING_BT_HCI`。`ENABLE_BLUETOOTH` 默认关闭，因此使用包含相关 Wi-Fi 驱动的
固件并不等于已启用 Python `bluetooth` 模块。

AIC8800DC 还需要在 controller 可用前完成 Bluetooth patch。ESP-Hosted-MCU
需要与主机驱动匹配的 ESP firmware；controller 启停通过 FeatureControl RPC
完成。详细 Wi-Fi transport 配置见 [Wi-Fi 驱动与设备选择](wifi_drivers.md)。

## 初始化和扫描

下面的代码启用 controller，主动扫描 5 秒，并打印扫描结果：

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

`active(True)` 会打开第一个可用的 `/dev/hciN` 并初始化 controller。当前 CanMV
接口不能按名称选择 `hci0`、`hci1`；同时接入多个 controller 时，实际使用对象由
注册顺序决定。

## 广播测试

以下 payload 包含通用 discoverable 标志和设备名 `CanMV-K230`：

```python
import bluetooth

ble = bluetooth.BLE()
ble.active(True)

adv_data = b"\x02\x01\x06\x0b\x09CanMV-K230"
ble.gap_advertise(100_000, adv_data=adv_data)
```

广播间隔单位为微秒。实际 GATT peripheral 还需要通过
`gatts_register_services()` 注册 service/characteristic，并在 IRQ 回调中处理连接、
写入和断开事件。作为 central 使用时，通过 IRQ 处理扫描、连接、service discovery
和 characteristic read/write/notify。

## 关闭

结束 BLE 业务后执行：

```python
# 正在扫描时使用 ble.gap_scan(None)
# 正在广播时使用 ble.gap_advertise(None)
ble.active(False)
```

`active(False)` 会停止 NimBLE 并关闭 HCI device。ESP-Hosted-MCU 会同时停用远端
controller；后续可以再次执行 `active(True)`。

## 排错

1. `import bluetooth` 失败：确认 CanMV 构建启用了 `ENABLE_BLUETOOTH`。
1. `active(True)` 报无法打开 HCI：检查启动日志中是否注册了 `/dev/hciN`，并确认
   controller 对应的 `AIC8800_WIFI_BLE` 或 `ESP_HOSTED_BLE` 已启用。
1. AIC USB 没有 HCI：核对设备 USB ID、组合接口枚举、firmware 与 DC 型号的
   Bluetooth patch 日志；SDIO AIC 不提供此 backend。
1. ESP controller 未出现：核对 ESP-Hosted-MCU firmware、transport、Reset 和
   FeatureControl 支持，FG/NG firmware 不能替代 MCU personality。
1. 多个 HCI 同时存在但连接到错误设备：当前 CanMV 自动选择第一个注册的
   `/dev/hciN`，应在固件中只启用需要的 controller backend。
