# 4. TCP-Server 例程讲解

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

## 2. 服务端例程解析

### 2.1 导入必要的库

```python
import socket  
import network  
import time
```

- **socket**：提供创建套接字的功能，是网络通信的基础。
- **network**：用于配置网络接口（如 LAN 和 WLAN）。
- **time**：可用于处理延时操作或网络超时控制。

### 2.2 定义服务内容

```python
CONTENT = b"""  
Hello #%d from k230 canmv MicroPython!  
"""
```

- 定义了服务端将发送给客户端的内容。`%d` 用于插入当前的连接计数。

### 2.3 创建并配置服务器

```python
def server():  
    ip = network_use_wlan(True)  # 获取网络接口的 IP

    # 创建 socket 并绑定到指定地址和端口  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)  
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许地址重用
    ai = socket.getaddrinfo(ip, 8080)  # 获取地址信息  
    addr = ai[0][-1]  # 提取地址和端口号  
    s.bind(addr)  # 绑定 socket 到地址和端口  
    s.listen(5)  # 开始监听，最多允许 5 个客户端同时等待连接
  
    print("tcp server %s port:%d\n" % (ip, 8080))
```

- 该部分代码创建了一个 TCP 服务器，并将其绑定到开发板的 IP 地址和端口 8080。`listen(5)` 表示最多允许 5 个客户端等待连接。

### 2.4 处理客户端连接

```python
counter = 1  
while True:  
    # 接受客户端连接  
    res = s.accept()  
    client_sock, client_addr = res  # 获取客户端套接字和地址
    print("Client address:", client_addr)
  
    client_sock.setblocking(False)  # 设置非阻塞模式
  
    # 向客户端发送消息  
    client_sock.write(CONTENT % counter)  
  
    while True:  
        try:  
            h = client_sock.read()  # 尝试读取客户端数据
            if h:  
                print(h)  
                client_sock.write(b"recv: " + h)  # 回复客户端
  
            if b"end" in h:  # 如果收到 "end"，则关闭连接  
                client_sock.close()  
                break  
        except Exception as e:  
            print("Error:", e)  
            time.sleep(0.1)  # 遇到错误后稍作等待
          
    counter += 1  
    if counter > 10:  
        print("server exit!")  
        s.close()  # 关闭服务器
        break
```

- 该代码段处理每个客户端的连接，并在与客户端通信时循环监听数据。当接收到 "end" 字符时，服务器关闭与该客户端的连接。
- 为了应对非阻塞模式下的异常，`try-except` 用于处理读取数据时可能出现的错误。

### 2.5 完整代码

```python
import socket
import network
import time, os

CONTENT = b"""
Hello #%d from k230 canmv MicroPython!
"""

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

def server():
    ip = network_use_wlan(True)

    counter = 1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ai = socket.getaddrinfo(ip, 8080)
    addr = ai[0][-1]
    s.bind(addr)
    s.listen(5)
    print("tcp server %s port:%d\n" % (ip, 8080))

    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        client_sock.setblocking(False)

        client_stream = client_sock
        client_stream.write(CONTENT % counter)

        while True:
            h = client_stream.read()
            if h:
                print(h)
                client_stream.write(b"recv: " + h)
            if b"end" in h:
                client_stream.close()
                break
          
        counter += 1
        if counter > 10:
            print("server exit!")
            s.close()
            break

server()
```

## 3. 运行现象与操作说明

1. 运行上述服务端代码，观察串口终端会打印出服务器的 IP 地址和端口号。

```{image} ../images/network/image-20240722162100719.png
:scale: 50 %
```

1. 打开 NetAssist 网络调试助手，配置为 TCP 客户端，并输入服务端终端显示的 IP 地址和端口号，点击 "连接"：

```{image} ../images/network/image-20240722162513633.png
:scale: 50 %
```

1. 成功连接后，客户端将会收到服务端的消息。
