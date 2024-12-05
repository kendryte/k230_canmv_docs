# 1. 使用有线网例程讲解

## 1. 环境准备

首先，确保你的 CanMV 开发板已经正确连接到路由器或交换机上，这样开发板就能接入到网络中。同时，请确认路由器或交换机能够正常工作，以便开发板能够正常通信。

## 2. 例程内容解析

下面的 Python 例程将帮助你理解如何在 CanMV 开发板上配置和使用网络 LAN 接口。

### 2.1 导入模块

```python
import network
```

这一行代码导入了 `network` 模块，它是用于管理网络接口的库。

### 2.2 主函数定义

```python
def main():  
# 后续的网络操作都将放在这个函数内
```

### 2.3 获取 LAN 接口

```python
a = network.LAN()
```

这行代码创建了一个 LAN 接口的实例，并赋值给变量 `a`。通过这个实例，我们可以对 LAN 接口进行各种操作。

### 2.4 检查网口状态

```python
# 获取网口是否在使用  
print(a.active())  
```

这里，我们首先检查网口是否激活（即是否在使用中）。

### 2.5 查看和设置网络配置

```python
# 查看网口 IP、掩码、网关、 DNS 配置  
print(a.ifconfig())  
# 设置网口 IP、掩码、网关、 DNS 配置  
print(a.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8')))  
# 再次查看以确认设置成功  
print(a.ifconfig())
```

这段代码首先打印出当前的网络配置（ IP 地址、子网掩码、网关和 DNS 服务器），然后设置新的网络配置，并再次打印出来以确认设置成功。

### 2.6 使用 DHCP 自动配置

```python
# 设置网口为 DHCP 模式  
print(a.ifconfig("dhcp"))  
# 查看自动获取的网络配置  
print(a.ifconfig())
```

在某些情况下，我们可能希望网络配置能够自动获取，这时就可以使用 DHCP 模式。通过将 `ifconfig()` 方法的参数设置为 `"dhcp"`，我们可以让开发板自动从 DHCP 服务器获取 IP 地址等配置信息。

### 2.7 查看 MAC 地址

```python
# 查看网口 MAC 地址  
print(a.config("mac"))  
```

MAC 地址是网络接口的唯一标识符。可通过 config("mac") 获取 MAC 地址。

### 2.8 完整执行

最后，通过调用 `main()` 函数，上述所有操作将被执行。

```python
main()
```

这个例程展示了如何在 CanMV 开发板上进行基本的网络配置和操作，包括检查网口状态、查看和设置网络配置、使用 DHCP 自动配置以及查看和设置 MAC 地址等。通过这些操作，你可以更好地理解和控制你的开发板在网络中的行为。

### 2.9 完整例程

```python
import network

def main():
    # 获取 lan 接口
    a=network.LAN()
    # 获取网口是否在使用
    print(a.active())
    # 查看网口 ip，掩码，网关， dns 配置
    print(a.ifconfig())
    # 设置网口 ip，掩码，网关， dns 配置
    print(a.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8')))
    # 查看网口 ip，掩码，网关， dns 配置
    print(a.ifconfig())
    # 设置网口为 dhcp 模式
    print(a.ifconfig("dhcp"))
    # 查看网口 ip，掩码，网关， dns 配置
    print(a.ifconfig())
    # 查看网口 mac 地址
    print(a.config("mac"))
    # 设置网口为 dhcp 模式
    print(a.ifconfig("dhcp"))
    # 查看网口 ip，掩码，网关， dns 配置
    print(a.ifconfig())

main()
```

具体接口定义请参考 [network](../../api/extmod/K230_CanMV_network模块API手册.md)

## 3. 使用USB 4G Ethernet 网卡

CanMV 同时也支持通过 USB 接入 4G 网卡上网，使用类似 USB 以太网

目前支持了以下 4G 网卡模组，用户需要自行编译固件使能对应模块的驱动。

1. [EC200M-CN](./modules/ec200m.md)
