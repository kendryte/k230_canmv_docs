# 7. HTTP-Client例程讲解

## 1. 环境准备

首先，确保你的CanMV开发板已经通过网口与路由器或交换机相连，并且路由器能够正常工作，具备访问互联网的能力。这是进行HTTP请求的基础环境设置。

## 2. 例程详解

下面的Python例程展示了如何在CanMV开发板上实现一个简单的HTTP客户端，用于向指定的服务器（本例中为百度）发送HTTP GET请求，并接收响应内容。

### 2.1 导入必要的模块

```python
import network  
import socket
```

这里导入了`network`和`socket`两个模块。`network`模块用于管理网络接口，而`socket`模块则提供了网络通信的底层接口。

### 2.2 定义主函数

```python
def main(use_stream=True):  
    # ...（后续代码）
```

定义了一个名为`main`的函数，它接受一个名为`use_stream`的参数，默认为`True`。这个参数用于控制是否使用流式接口来读取响应数据。

### 2.3 配置网络接口

```python
# 获取LAN接口  
a = network.LAN()  
# 如果网口已激活，则先关闭再激活  
if a.active():  
    a.active(0)  
a.active(1)  
# 设置网口为DHCP模式，自动获取IP地址  
a.ifconfig("dhcp")  
  
# 打印网络配置和MAC地址  
print(a.ifconfig())  
print(a.config("mac"))
```

这部分代码首先获取LAN接口实例，并检查其状态。如果网口已激活，则先关闭再激活（虽然这一步通常不是必需的，但这里展示了如何操作）。然后，设置网口为DHCP模式，以便自动从路由器获取IP地址等配置信息。最后，打印出网络配置和MAC地址以供检查。

### 2.4 创建并配置socket

```python
# 创建socket对象  
s = socket.socket()  
# 尝试获取目标地址和端口号  
ai = []  
for attempt in range(0, 3):  
    try:  
        ai = socket.getaddrinfo("www.baidu.com", 80)  
        break  
    except:  
        print("getaddrinfo again")  
  
# 检查是否成功获取地址信息  
if ai == []:  
    print("连接错误")  
    s.close()  
    return  
  
# 提取地址和端口号  
addr = ai[0][-1]  
print("连接地址:", addr)
```

这段代码首先创建了一个socket对象，然后尝试通过`getaddrinfo`函数获取目标服务器（百度）的地址和端口号信息。为了提高代码的健壮性，这里使用了重试机制，最多尝试3次。如果成功获取到地址信息，则提取出地址和端口号，并打印出来。

### 2.5 发送HTTP请求并接收响应

```python
# 连接到服务器  
s.connect(addr)  
  
if use_stream:  
    # 使用流式接口读取响应  
    s = s.makefile("rwb", 0)  
    s.write(b"GET /index.html HTTP/1.0\r\n\r\n")  
    print(s.read())  
else:  
    # 直接使用socket接口发送和接收数据  
    s.send(b"GET /index.html HTTP/1.0\r\n\r\n")  
    print(s.recv(4096))  
  
# 关闭socket  
s.close()
```

这部分代码首先连接到服务器，然后根据`use_stream`参数的值选择使用流式接口还是直接通过socket接口发送HTTP请求。如果`use_stream`为`True`，则使用流式接口发送请求并读取整个响应；如果为`False`，则直接发送请求并接收一定长度的响应数据（本例中为4096字节）。最后，关闭socket连接以释放资源。

### 2.6 函数调用

```python
# 调用主函数，分别测试流式接口和非流式接口  
main(use_stream=True)  
main(use_stream=False)
```

最后，通过调用`main`函数并传入不同的`use_stream`参数值，可以分别测试流式接口和非流式接口的效果。这样可以帮助你更好地理解这两种方式在读取HTTP响应时的差异。

### 2.7 完整例程

```python
import network
import socket


def main(use_stream=True):
  
    #获取lan接口
    a=network.LAN()
    if(a.active()):
        a.active(0)
    a.active(1)
    a.ifconfig("dhcp")
  
    print(a.ifconfig())
    print(a.config("mac"))
    #创建socket
    s = socket.socket()
    #获取地址及端口号 对应地址
    ai = []
  
    for attempt in range(0, 3):
        try:
            #获取地址及端口号 对应地址
            ai = socket.getaddrinfo("www.baidu.com", 80)
            break
        except:
            print("getaddrinfo again");
  
    if(ai == []):
        print("connet error")
        s.close()
        return

    print("Address infos:", ai)
    addr = ai[0][-1]
  
    print("Connect address:", addr)
    #连接
    s.connect(addr)

    if use_stream:
        # MicroPython socket objects support stream (aka file) interface
        # directly, but the line below is needed for CPython.
        s = s.makefile("rwb", 0)
        #发送http请求
        s.write(b"GET /index.html HTTP/1.0\r\n\r\n")
        #打印请求内容
        print(s.read())
    else:
        #发送http请求
        s.send(b"GET /index.html HTTP/1.0\r\n\r\n")
        #打印请求内容
        print(s.recv(4096))
        #print(s.read())
    #关闭socket
    s.close()


#main()
main(use_stream=True)
main(use_stream=False)
```

具体接口定义请参考 [socket](../../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../../api/extmod/K230_CanMV_network模块API手册.md)
