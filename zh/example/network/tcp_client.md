# 3. TCP-Client 例程讲解

## 1. 环境准备

为了确保顺利进行 TCP 通信的演示，我们需要确认以下环境已正确配置：

### 1.1 硬件连接

- 请确保您的 CanMV 开发板和电脑通过网线连接至同一个路由器或交换机，形成局域网。
- 确保路由器或交换机正常工作，以保证网络连接的稳定性。

### 1.2 关闭防火墙

- 为了避免防火墙阻止 TCP 通信，建议暂时关闭电脑的防火墙。

```{image} ../images/network/image-20240722145319713.png
:scale: 50 %
```

### 1.3 工具准备

- 下载并安装 [NetAssist 网络调试助手](https://www.bing.com/search?q=netassist+cmsoft) 作为网络通信的测试工具，帮助实现网络数据的收发。

### 1.4 获取 IP 地址

- 打开命令提示符（CMD），输入 `ipconfig`，查询并记录电脑网卡的 IP 地址，供后续配置和测试使用。

```{image} ../images/network/image-20240722145500693.png
:scale: 50 %
```

## 2. 客户端代码解析

### 2.1 导入必要的库

```python
import network  
import socket  
import time
```

- **network**：用于网络接口操作，例如配置 IP 地址和检查网络状态。
- **socket**：提供网络通信的 Socket 接口。
- **time**：提供与时间相关的函数，比如延时（`sleep`）。

### 2.2 定义客户端函数

```python
def client():  
    # ...（后续代码）
```

- `client` 函数包含了 TCP 客户端的主要逻辑。

### 2.3 配置网络接口

```python
def network_use_wlan(is_wlan=True):
    if is_wlan:
        sta = network.WLAN(0)
        sta.connect("Canaan", "Canaan314")
        print(sta.status())
        while sta.ifconfig()[0] == '0.0.0.0':
            os.exitpoint()
        print(sta.ifconfig())
        ip = sta.ifconfig()[0]
        return ip
    else:
        a = network.LAN()
        if not a.active():
            raise RuntimeError("LAN interface is not active.")
        a.ifconfig("dhcp")
        print(a.ifconfig())
        ip = a.ifconfig()[0]
        return ip
```

根据参数配置网络接口，流程如下：

1. **WLAN 模式**：
   - 如果 `is_wlan=True`，则配置无线网络接口（WLAN），连接到 SSID 为 "Canaan"、密码为 "Canaan314" 的 Wi-Fi。
   - 等待并检查是否分配到有效 IP 地址，返回 IP。

1. **LAN 模式**：
   - 如果 `is_wlan=False`，配置有线网络接口（LAN），启用 DHCP 以自动获取 IP 地址，返回 IP。

### 2.4 创建 Socket

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

- 使用 IPv4（`AF_INET`）和 TCP（`SOCK_STREAM`）协议创建 Socket 对象。

### 2.5 获取服务器地址和端口

```python
ai = socket.getaddrinfo("172.16.1.174", 8080)  
addr = ai[0][-1]  # 提取地址和端口
```

- 使用 `getaddrinfo` 获取服务器的 IP 地址和端口号，并提取出地址信息。

### 2.6 连接到服务器

```python
try:  
    s.connect(addr)  
    print("Connected to server:", addr)  
except Exception as e:  
    s.close()  
    print("Connection error:", e)  
    return
```

- 尝试连接到服务器，如果连接失败则打印错误信息并关闭连接。

### 2.7 发送数据

```python
for i in range(10):  
    message = "K230 TCP client send test {0} \r\n".format(i)  
    print("Sending:", message)  
    s.sendall(message.encode())  
    time.sleep(0.2)
```

- 在循环中发送 10 条测试信息，并且使用 `sendall` 方法确保每条消息完全发送。

### 2.8 关闭 Socket

```python
s.close()  
print("Client ends connection.")
```

- 关闭 Socket 以释放资源，表示客户端结束连接。

### 2.9 完整代码示例

```python
import network
import socket
import os, time

def network_use_wlan(is_wlan=True):
    if is_wlan:
        sta = network.WLAN(0)
        sta.connect("Canaan", "Canaan314")
        print(sta.status())
        while sta.ifconfig()[0] == '0.0.0.0':
            os.exitpoint()
        print(sta.ifconfig())
        ip = sta.ifconfig()[0]
        return ip
    else:
        a = network.LAN()
        if not a.active():
            raise RuntimeError("LAN interface is not active.")
        a.ifconfig("dhcp")
        print(a.ifconfig())
        ip = a.ifconfig()[0]
        return ip

def client():
    network_use_wlan(True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ai = socket.getaddrinfo("192.168.1.110", 8080)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("Connecting to:", addr)
    try:
        s.connect(addr)
    except Exception as e:
        s.close()
        print("Connection error:", e)
        return

    for i in range(10):
        message = "K230 TCP client send test {0} \r\n".format(i)
        print("Sending:", message)
        s.sendall(message.encode())
        time.sleep(0.2)

    s.close()
    print("Connection closed.")

client()
```

## 3. 运行结果与操作说明

1. 打开 NetAssist 网络调试助手，配置为 TCP 服务器并等待连接：

```{image} ../images/network/image-20240722152102440.png
:scale: 50 %
```

1. 在代码中修改服务器的 IP 和端口号：

```python
ai = socket.getaddrinfo("172.16.1.174", 8080)
```

1. 运行客户端代码，NetAssist 将显示客户端发送的消息：

```{image} ../images/network/image-20240722151843380.png
:scale: 50 %
```
