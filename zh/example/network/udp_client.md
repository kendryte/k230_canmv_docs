# 5. UDP-Client 例程讲解

## 1. 环境准备

为了确保顺利进行 UDP 通信的演示，我们需要确认以下环境已正确配置：

### 1.1 硬件连接

- 请确保您的 CanMV 开发板和电脑通过网线连接至同一个路由器或交换机，形成局域网。
- 确保路由器或交换机正常工作，以保证网络连接的稳定性。

### 1.2 关闭防火墙

- 为了避免防火墙阻止 UDP 通信，建议暂时关闭电脑的防火墙。

```{image} ../images/network/image-20240722145319713.png
:scale: 50 %
```

### 1.3 工具准备

- 下载并安装 [NetAssist 网络调试助手](https://www.cmsoft.cn/resource/102.html) 作为网络通信的测试工具，帮助实现网络数据的收发。

### 1.4 获取 IP 地址

- 打开命令提示符（CMD），输入 `ipconfig`，查询并记录电脑网卡的 IP 地址，供后续配置和测试使用。

```{image} ../images/network/image-20240722145500693.png
:scale: 50 %
```

## 2. 客户端例程解析

这个 UDP 客户端例程展示了如何创建一个简单的 UDP 客户端，包括连接到服务器、发送数据和关闭连接。你可以通过此例程学习构建 UDP 通信应用的基本方法。

### 2.1 导入必要库

```python
import socket  
import network  
import time
```

- `socket` 库负责创建网络通信的套接字。
- `network` 库用于配置网络接口，比如启用 LAN 或 WLAN。
- `time` 库提供延时操作，通常用于控制数据发送频率或超时处理。

### 2.2 配置网络接口

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

这个函数根据是否选择无线网络（WLAN）或有线网络（LAN）来配置网络接口，具体步骤如下：

1. **WLAN 模式**：尝试连接到 Wi-Fi 网络，等待获得有效的 IP 地址后返回。
1. **LAN 模式**：激活 LAN 接口，并使用 DHCP 模式获取 IP 地址。

### 2.3 创建 UDP 套接字

```python
# 获取服务器的 IP 和端口号  
ai = socket.getaddrinfo('172.16.1.174', 8080)
print("Address infos:", ai)  
addr = ai[0][-1]  # 提取 IP 和端口号

print("Connecting to address:", addr)
# 创建 UDP 套接字
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

这里通过 `socket.getaddrinfo` 获取服务器的 IP 和端口信息，并提取出地址和端口号，然后创建 UDP 套接字。

### 2.4 发送数据

```python
# 发送测试消息
for i in range(10):
    message = "K230 UDP client send test {0} \r\n".format(i)
    print("Sending:", message)
    # 将消息编码成字节并发送
    bytes_sent = s.sendto(message.encode(), addr)
    print("Bytes sent:", bytes_sent)
    # 暂停一段时间以等待下次发送
    time.sleep(0.2)
```

在循环中，程序生成测试消息，并将其通过 `sendto` 函数发送到指定的服务器地址。消息在发送之前需要转换成字节串。发送成功后，打印已发送的字节数，并设置一个小的延时。

### 2.5 关闭套接字

```python
# 关闭套接字
s.close()
print("Client ended.")
```

在数据发送完成后，关闭套接字以释放资源。

### 2.6 完整例程

```python
import socket
import os
import time
import network

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

def udpclient():
    # 配置网络接口
    network_use_wlan(True)
  
    # 获取服务器地址和端口号
    ai = socket.getaddrinfo('192.168.1.110', 8080)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("Connect address:", addr)
    # 创建 UDP 套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for i in range(10):
        message = "K230 UDP client send test {0} \r\n".format(i)
        print("Sending:", message)
        # 发送字符串
        bytes_sent = s.sendto(message.encode(), addr)
        print("Bytes sent:", bytes_sent)
        time.sleep(0.2)
    
    # 关闭套接字
    s.close()
    print("Client ended.")

# 启动客户端
udpclient()
```

## 3. 运行与测试

1. 使用 NetAssist 网络调试助手建立 UDP 连接：

```{image} ../images/network/image-20240722171950467.png
:scale: 50 %
```

1. 修改代码中的服务器 IP 地址：

```python
ai = socket.getaddrinfo("172.16.1.174", 8080)
```

1. 运行例程后，NetAssist 将显示接收到的 UDP 数据包：

```{image} ../images/network/image-20240722172037608.png
:scale: 50 %
```
