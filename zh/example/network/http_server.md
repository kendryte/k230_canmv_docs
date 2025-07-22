# HTTP-Server 例程讲解

## 环境准备

首先，确保你的 CanMV 开发板通过网口与路由器或交换机相连，并且路由器能够正常工作并具备访问互联网的能力。此环境是实现 HTTP 请求的前提。

## 服务端例程详解

下面展示了一个基于 CanMV 开发板的简单 HTTP 服务器 Python 例程。该服务器监听端口 8081，能够响应客户端的 HTTP 请求。

### 导入必要的模块

```python
import socket  
import network  
import time
```

通过导入 `socket`、`network` 和 `time` 模块，`socket` 模块用于网络通信，`network` 管理网络接口（如 LAN），`time` 提供时间相关功能。

### 定义响应内容

```python
CONTENT = b"""\  
HTTP/1.0 200 OK  
Hello #%d from k230 canmv MicroPython!  
"""
```

定义一个字节字符串 `CONTENT`，作为 HTTP 响应主体。 `%d` 是计数器占位符，表示每次请求的序号。

### 定义主函数

```python
def main(micropython_optimize=True):  
    # ...（后续代码）
```

定义了 `main` 函数，参数 `micropython_optimize` 控制是否启用 MicroPython 的特定优化方式。

### 配置网络接口

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

这段代码依据 `is_wlan` 参数选择 WLAN 或 LAN 接口。WLAN 模式下连接到指定 Wi-Fi 网络，而 LAN 模式则通过 DHCP 获取 IP 地址。获取并打印网络配置后，返回 IP。

### 创建并配置 socket

```python
# 创建 socket 对象  
s = socket.socket()  
# 设置 socket 选项，允许地址重用  
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
# 绑定到所有网络接口，监听 8081 端口  
ai = socket.getaddrinfo("0.0.0.0", 8081)  
addr = ai[0][-1]  
s.bind(addr)  
# 开始监听，最大连接数为 5  
s.listen(5)  
print("监听中，请在浏览器中访问 http://%s:8081/" % (network.LAN().ifconfig()[0]))
```

代码创建 socket，并启用 `SO_REUSEADDR` 选项以允许端口重用。绑定地址并开始监听端口 8081，最多支持 5 个连接请求。

### 处理客户端请求

```python
counter = 0  
while True:  
    # 接受连接  
    res = s.accept()  
    client_sock = res[0]  
    client_addr = res[1]  
    print("客户端地址:", client_addr)  
  
    # 根据是否启用优化，选择不同的读取方式  
    if not micropython_optimize:  
        # 使用流式接口（适用于 CPython）  
        client_stream = client_sock.makefile("rwb")  
    else:  
        # 使用 MicroPython 特有接口  
        client_stream = client_sock  
  
    # 读取请求内容  
    # ...  
  
    # 发送响应  
    client_stream.write(CONTENT % counter)  
    # 关闭连接  
    client_stream.close()  
  
    counter += 1  
    time.sleep(2)  
    if counter > 0:  
        print("HTTP 服务器退出！")  
        s.close()  
        break
```

服务器主循环接受客户端连接，选择不同的读取方式处理请求，发送带有计数器的响应，并关闭连接。连接关闭后，等待 2 秒进入下次循环。

### 完整例程

```python
import socket
import network
import time, os

CONTENT = b"""\
HTTP/1.0 200 OK

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

def main(micropython_optimize=True):
    ip = network_use_wlan(True)
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8081)
    addr = ai[0][-1]
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://%s:8081/" % (ip))

    counter = 0
    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        client_sock.setblocking(True)
        client_stream = client_sock if micropython_optimize else client_sock.makefile("rwb")

        while True:
            h = client_stream.read()
            if h is None:
                continue
            print(h)
            if h.endswith(b'\r\n\r\n'):
                break
            os.exitpoint()

        client_stream.write(CONTENT % counter)
        client_stream.close()
        counter += 1
        time.sleep(2)
        if counter > 0:
            print("http server exit!")
            s.close()
            break

main()
```

具体接口定义请参考 [socket](../../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../../api/extmod/K230_CanMV_network模块API手册.md)。

## 例程现象与操作说明

在 CanMV IDE K230 中运行该例程后，IDE 串口终端会显示如下信息：

![image-20240722134617332](../images/network/image-20240722134617332.png)

复制终端中的网址并在浏览器中访问，即可查看服务器的响应内容：

![image-20240722134912486](../images/network/image-20240722134912486.png)
