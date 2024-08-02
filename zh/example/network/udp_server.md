# 6. UDP-Server例程讲解

## 1. 环境准备

为了顺利进行TCP通信的演示，我们需要确保以下环境已经配置妥当：

### 1.1 硬件连接

- 确保你的CanMV开发板和电脑都已经通过网线连接到同一个路由器或交换机上，形成一个局域网。
- 路由器或交换机需要正常工作，以确保网络通畅。

### 1.2 关闭防火墙

- 为了避免防火墙拦截TCP通信，建议暂时关闭电脑上的防火墙。

```{image} ../images/network/image-20240722145319713.png
:scale: 50 %
```

### 1.3 工具准备

- 下载并安装[NetAssist网络调试助手](https://www.cmsoft.cn/resource/102.html)工具，这将帮助我们进行网络数据的收发测试。

### 1.4 记录IP地址

- 打开CMD（命令提示符），输入`ipconfig`指令，查看并记录电脑网口所分配的IP地址。这将用于后续设置和测试。
  
```{image} ../images/network/image-20240722145500693.png
:scale: 50 %
```

## 2. 服务端例程解析

例程展示了如何在Python（或MicroPython）中创建一个简单的UDP服务器，包括配置网络接口、创建socket、绑定地址和端口、接收和发送数据以及关闭socket。通过这个例程，你可以学习如何构建基本的网络通信应用。

### 2.1 导入必要的库

```python
import socket  
import network  
import time
```

- `socket` 库用于创建套接字，它是网络通信的基础。
- `network` 库用于处理网络接口的配置，如启用和配置LAN接口。
- `time` 库在这个例程中虽然没有直接使用，但在处理网络请求时，它可能用于超时控制或延迟处理。

### 2.2 配置网络接口

```python
lan = network.LAN()  
    if lan.active():  
        lan.active(0)  # 如果已经激活，先关闭  
    lan.active(1)      # 重新激活以获取IP  
    lan.ifconfig("dhcp")  # 使用DHCP自动配置IP  
    print("LAN Interface Config:", lan.ifconfig())  # 打印配置信息
```

这部分代码首先获取LAN接口实例，并检查其状态。如果网口已激活，则先关闭再激活（这一步在大多数情况下不是必需的，但提供了操作接口的示例）。然后，设置网口为DHCP模式，以便自动从路由器获取IP地址等配置信息。

### 2.3 创建UDP Socket

```python
# 创建UDP socket  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    # 设置socket选项，允许地址重用  
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    # 获取地址及端口号对应地址，并绑定socket  
    ai = socket.getaddrinfo(ip, 8080)  
    addr = ai[0][-1]  
    s.bind(addr)
```

我们创建了一个UDP类型的socket，并通过`setsockopt`设置了`SO_REUSEADDR`选项，允许在同一地址和端口上重用socket。然后，我们使用`getaddrinfo`获取地址和端口号的详细信息，并绑定socket到该地址和端口上。

### 2.4 接收和发送数据

```python
# 延时1秒，确保socket绑定完成  
    time.sleep(1)  
  
    # 接收数据并回复  
    for j in range(10):  
        try:  
            data, addr = s.recvfrom(800)  # 接收数据，最多800字节  
            print("Received:", data, "from", addr)  
            # 回复数据，包含接收到的数据和接收次数  
            response = b"%s have recv count=%d " % (data, j)  
            s.sendto(response, addr)  
        except Exception as e:  
            print("Error:", e)  # 打印异常信息，便于调试  
  
    # 关闭socket  
    s.close()  
    print("UDP Server exited!!")
```

在socket绑定后，我们等待1秒以确保其准备就绪。然后，进入一个循环，尝试接收最多800字节的数据。如果接收到数据，则打印接收到的数据和发送方的地址，并构造一个回复消息发送回发送方。在循环中，我们还添加了异常处理来捕获并打印任何可能发生的错误，这有助于调试和错误追踪。

### 2.5 完整例程

```python
#配置 tcp/udp socket调试工具
import socket
import time
import network


def udpserver():
    #获取lan接口
    a=network.LAN()
    if(a.active()):
        a.active(0)
    a.active(1)
    a.ifconfig("dhcp")
    ip = a.ifconfig()[0]
    print(a.ifconfig())
    
    #获取地址及端口号对应地址
    ai = socket.getaddrinfo(ip, 8080)
    #ai = socket.getaddrinfo("10.10.1.94", 60000)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("udp server %s port:%d\n" % ((network.LAN().ifconfig()[0]),8080))
    #建立socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #设置属性
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #绑定
    s.bind(addr)
    print("a")
    #延时
    time.sleep(1)

    for j in range(10):
        try:
            #接受内容
            data, addr = s.recvfrom(800)
            print("b")
        except:
            continue
        #打印内容
        print("recv %d" % j,data,addr)
        #回复内容
        s.sendto(b"%s have recv count=%d " % (data,j), addr)
    #关闭
    s.close()
    print("udp server exit!!")




#main()
udpserver()
```

具体接口定义请参考 [socket](../../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../../api/extmod/K230_CanMV_network模块API手册.md)

## 3. 例程现象与操作说明

运行例程源码，记录串口终端打印输出的IP与端口号信息：

![image-20240722165929097](../images/network/image-20240722165929097.png)

在网络调试助手中，选择UDP，建立连接：

```{image} ../images/network/image-20240722170233348.png
:scale: 50 %
```

发生数据：

```{image} ../images/network/image-20240722170412175.png
:scale:  50 %
```
