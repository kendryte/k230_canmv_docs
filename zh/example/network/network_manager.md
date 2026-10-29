# 公共网络管理例程讲解

## 例程位置

- 开发板固件路径：`/sdcard/examples/14-Socket/network_manager.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/network_manager.py`

公共库本身位于 `/sdcard/libs/Network.py`，对应 SDK 源码
`src/canmv/resources/libs/Network.py`。

## 例程作用

该例程演示 `libs.Network.NetworkManager` 的完整基础流程：查看已注册网卡、选择
网络类型、建立连接、显示接口状态，以及查询当前默认上行。管理器保存接口对象，
因此同一应用中的 HTTP、WebSocket 或媒体组件可以复用同一个连接。

## 配置参数

```python
NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

| 配置 | 示例值 | 作用 |
| :-- | :-- | :-- |
| `NETWORK_TYPE` | `"wifi_sta"` | 选择 `default`、`lan`、`wifi_sta` 或 `wifi_ap` |
| `WLAN_DEVICE` | `"auto"` | 自动选 Wi-Fi；也可固定 USB、SDIO 或 SPI |
| `WIFI_SSID` | `"TEST"` | STA 连接或 AP 创建时使用的 SSID |
| `WIFI_PASSWORD` | `"12345678"` | Wi-Fi 密码 |
| `NETWORK_TIMEOUT` | `20` | 最长等待 20 秒取得有效地址 |

`"default"` 只复用已经联网的默认/自动接口，不会主动连接新的 Wi-Fi。若设备
还未联网，应明确选择 `"lan"` 或 `"wifi_sta"`。

## 代码流程

### 1. 创建管理器

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

构造函数只保存配置，不会立即连接。`show=False` 表示连接过程中不重复打印信息，
例程稍后显式调用 `show_devices()` 和 `show_info()`。

### 2. 查看动态注册的设备

```python
manager.show_devices()
```

该调用打印 `network.get_dev_list()` 返回的完整设备列表，以及当前默认设备。设备
名称由驱动动态分配，应用不应根据硬件类型假设名称固定不变。

### 3. 连接并等待 IP

```python
netif, ip = manager.connect()
```

不同 `NETWORK_TYPE` 的行为如下：

- `lan`：取得 LAN 对象，必要时启动 DHCP，然后等待有效 IP；
- `wifi_sta`：选择 WLAN 设备、连接 SSID，然后等待关联成功和有效 IP；
- `wifi_ap`：创建热点并等待 AP 地址，不把 AP 设置为默认上行；
- `default`：查找已经连接且具有有效 IP 的接口。

LAN 和 Wi-Fi STA 连接成功后，管理器会把接口设置为首选默认上行。接口失效时，
系统仍可自动切换到其他已就绪的上行接口。

### 4. 查看结果

```python
manager.show_info()
print("Network ready:", ip)
print("Default network device:", get_default_device() or "auto")
```

`show_info()` 会打印设备名、激活状态、连接状态、IP 配置和 MAC 地址。返回的
`netif` 是实际的 `network.LAN` 或 `network.WLAN` 对象，可直接交给其他模块。

## 接口复用

管理器会保存 `netif` 和 `ip`。再次调用 `manager.connect()` 时，如果原接口仍然
连接并具有有效地址，就直接返回同一对象。网络断开后再次调用则执行恢复流程。

```python
netif, ip = manager.connect()
# 将同一个 netif 交给应用的多个组件
netif, ip = manager.connect()  # 仍可用时不会创建第二个接口
```

`manager.disconnect()` 用于停止 Wi-Fi，并默认清除人工首选设备、恢复自动路由
选择。LAN 不会因调用 `disconnect()` 而被硬件关闭。

## 运行与验证

1. 在 CanMV IDE 中打开 `/sdcard/examples/14-Socket/network_manager.py`。
1. 修改网络类型和 Wi-Fi 凭据。
1. 运行脚本并检查 `Network devices` 中是否出现目标接口。
1. 确认 `Network ready` 不是 `0.0.0.0`。
1. 对 LAN/Wi-Fi STA，确认 `Default network device` 与选中的接口一致。

若出现 `network address timeout`，依次检查网线或 Wi-Fi 凭据、DHCP 服务和
`WLAN_DEVICE` 是否选择了实际存在的设备。

完整接口说明见 [network 模块 API 手册](../../api/extmod/k230_canmv_network_api_manual.md)。
