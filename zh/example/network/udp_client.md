# 5. UDP-Client例程讲解

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

## 2. 客户端例程解析

这个UDP客户端例程展示了如何在Python中创建一个简单的UDP客户端，包括连接到UDP服务器、发送数据和关闭socket。通过这个例程，你可以学习如何构建基本的UDP网络通信应用。

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

### 2.3 创建UDP套接字

```python
# 获取UDP服务器的地址和端口号  
    ai = socket.getaddrinfo('172.16.1.174', 8080)  
    print("Address infos:", ai)  
    addr = ai[0][-1]  # 提取地址和端口号对  
  
    print("Connecting to address:", addr)  
    # 建立UDP socket  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

这里，我们使用`socket.getaddrinfo`来获取UDP服务器的地址和端口号信息，并从中提取出我们需要的地址和端口号。然后，我们创建了一个UDP类型的socket。

### 2.4 发送数据

```python
# 发送测试消息  
    for i in range(10):  
        message = "K230 udp client send test {0} \r\n".format(i)  
        print("Sending:", message)  
        # 发送字符串  
        bytes_sent = s.sendto(message.encode(), addr)  # 注意：需要编码为字节串  
        print("Bytes sent:", bytes_sent)  
        # 延时  
        time.sleep(0.2)
```

在循环中，我们构造了一个包含当前迭代次数的测试消息，并使用`sendto`方法将其发送到UDP服务器。注意，`sendto`方法需要字节串作为参数，因此我们将字符串编码为字节串。然后，我们打印出发送的字节数，并暂停一段时间以等待下一次迭代。

### 2.5 关闭Socket

```python
# 关闭socket  
    s.close()  
    print("Client ended.")
```

最后，我们关闭了socket以释放资源，并打印出结束消息。

### 2.6 完整例程

```python
#配置 tcp/udp socket调试工具
import socket
import time
import network


def udpclient():
    #获取lan接口
    a=network.LAN()
    if(a.active()):
        a.active(0)
    a.active(1)
    a.ifconfig("dhcp")
    ip = a.ifconfig()[0]
    print(a.ifconfig())
  
    #获取地址和端口号 对应地址
    ai = socket.getaddrinfo('172.16.1.174', 8080)
    #ai = socket.getaddrinfo("10.10.1.94", 60000)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("Connect address:", addr)
    #建立socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



    for i in range(10):
        str="K230 udp client send test {0} \r\n".format(i)
        print(str)
        #发送字符串
        print(s.sendto(str,addr))
        #延时
        time.sleep(0.2)
        #time.sleep(1)
        #print(s.recv(4096))
        #print(s.read())
    #延时
    time.sleep(1)
    #关闭
    s.close()
    print("end")



#main()
udpclient()
```

具体接口定义请参考 [socket](../../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../../api/extmod/K230_CanMV_network模块API手册.md)

## 3. 例程现象与操作说明

打开NetAssist网络调试助手，建立UDP连接：

```{image} ../images/network/image-20240722171950467.png
:scale: 50 %
```

在例程源码中修改对应的IP，端口：

```python
ai = socket.getaddrinfo("172.16.1.174", 8080)
```

运行例程代码，NetAssist网络调试助手输出信息：

```{image} ../images/network/image-20240722172037608.png
:scale: 50 %
```
