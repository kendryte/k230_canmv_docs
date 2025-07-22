# HTTP-Client 例程讲解

## 环境准备

首先，确保 CanMV 开发板通过网口连接到路由器或交换机，并且路由器能够正常工作，具备访问互联网的能力。这是进行 HTTP 请求的基础环境设置。

## 例程详解

以下 Python 例程展示了如何在 CanMV 开发板上实现一个 HTTP 客户端，通过该客户端向指定服务器（此处为百度）发送 HTTP GET 请求，并接收响应内容。

### 导入必要的模块

```python
import network  
import socket
```

- `network` 模块用于管理网络接口
- `socket` 模块提供网络通信的底层接口。

### 定义主函数

```python
def main(use_stream=True):  
    # ...（后续代码）
```

函数 `main` 定义了是否使用流式接口读取响应数据的参数 `use_stream`，默认为 `True`，用来控制数据接收方式。

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

该函数根据输入配置网络接口：

1. **WLAN 模式**：通过无线网络接口（WLAN）连接指定的 Wi-Fi（SSID 为 "Canaan"）。
1. **LAN 模式**：通过有线网络接口（LAN）自动获取 IP 地址。

### 创建并配置 Socket

```python
# 创建 socket 对象  
s = socket.socket()  
# 获取目标地址和端口号  
ai = []  
for attempt in range(0, 3):  
    try:  
        ai = socket.getaddrinfo("www.baidu.com", 80)  
        break  
    except:  
        print("getaddrinfo again")  
  
if ai == []:  
    print("连接错误")  
    s.close()  
    return  
  
addr = ai[0][-1]  
print("连接地址:", addr)
```

创建一个 `socket` 对象，并通过 `getaddrinfo` 函数获取服务器（百度）的地址和端口号信息，使用重试机制以提高健壮性。

### 发送 HTTP 请求并接收响应

```python
# 连接到服务器  
s.connect(addr)  
  
if use_stream:  
    # 使用流式接口读取响应  
    s = s.makefile("rwb", 0)  
    s.write(b"GET /index.html HTTP/1.0\r\n\r\n")  
    print(s.read())  
else:  
    # 直接使用 socket 接口发送和接收数据  
    s.send(b"GET /index.html HTTP/1.0\r\n\r\n")  
    print(s.recv(4096))  
  
# 关闭 socket  
s.close()
```

代码根据 `use_stream` 参数选择使用流式接口或直接通过 `socket` 接口发送 HTTP 请求并读取响应数据。

### 函数调用

```python
# 分别测试流式接口和非流式接口  
main(use_stream=True)  
main(use_stream=False)
```

调用 `main` 函数，通过不同的 `use_stream` 参数测试流式和非流式读取 HTTP 响应的效果。如果 use_stream 为 True，则使用流式接口发送请求并读取整个响应；如果为 False，则直接发送请求并接收一定长度的响应数据（本例中为4096字节）。最后，关闭 socket 连接以释放资源。

### 完整例程

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

def main(use_stream=True):
    # 获取 LAN 接口
    network_use_wlan(True)
    # 创建 socket
    s = socket.socket()
    # 获取地址及端口号
    ai = []
    for attempt in range(0, 3):
        try:
            ai = socket.getaddrinfo("www.baidu.com", 80)
            break
        except:
            print("getaddrinfo again")
    
    if ai == []:
        print("连接错误")
        s.close()
        return

    addr = ai[0][-1]
    print("连接地址:", addr)
    # 连接
    s.connect(addr)

    if use_stream:
        s = s.makefile("rwb", 0)
        s.write(b"GET /index.html HTTP/1.0\r\n\r\n")
        print(s.read())
    else:
        s.send(b"GET /index.html HTTP/1.0\r\n\r\n")
        print(s.recv(4096))

    s.close()

# main()
main(use_stream=True)
main(use_stream=False)
```

具体接口定义请参考 [socket](../../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../../api/extmod/K230_CanMV_network 模块API手册.md)。
