# 8. HTTP-Server例程讲解

## 1. 环境准备

**首先，确保你的CanMV开发板已经通过网口与路由器或交换机相连，并且路由器能够正常工作，具备访问互联网的能力。这是进行HTTP请求的基础环境设置。**

### 2. 服务端例程详解

下面的Python例程展示了如何在CanMV开发板上实现一个简单的HTTP服务器，该服务器能够监听特定端口（本例中为8081），并响应来自客户端的HTTP请求。

### 2.1 导入必要的模块

```python
import socket  
import network  
import time
```

这里导入了`socket`、`network`和`time`三个模块。`socket`模块用于网络通信，`network`模块用于管理网络接口（如LAN），而`time`模块用于在处理请求时提供时间延迟等功能。

### 2.2 定义响应内容

```python
CONTENT = b"""\  
HTTP/1.0 200 OK  
Hello #%d from k230 canmv MicroPython!  
"""
```

定义了一个名为`CONTENT`的字节字符串，用于作为HTTP响应的主体发送给客户端。`%d`是一个占位符，用于在响应时插入一个动态的数字（计数器）。

### 2.3 定义主函数

```python
def main(micropython_optimize=True):  
    # ...（后续代码）
```

定义了一个名为`main`的函数，它接受一个名为`micropython_optimize`的参数，默认为`True`。这个参数用于控制是否使用MicroPython特有的优化方式读取socket数据。

### 2.4 配置网络接口

```python
# 获取LAN接口  
a = network.LAN()  
# 如果网口已激活，则先关闭再激活  
if a.active():  
    a.active(0)  
a.active(1)  
# 设置网口为DHCP模式，自动获取IP地址  
a.ifconfig("dhcp")
```

这部分代码首先获取LAN接口实例，并检查其状态。如果网口已激活，则先关闭再激活（这一步在大多数情况下不是必需的，但提供了操作接口的示例）。然后，设置网口为DHCP模式，以便自动从路由器获取IP地址等配置信息。

### 2.5 创建并配置socket

```python
# 创建socket对象  
s = socket.socket()  
# 设置socket选项，允许地址重用  
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
# 绑定到所有网络接口，监听8081端口  
ai = socket.getaddrinfo("0.0.0.0", 8081)  
addr = ai[0][-1]  
s.bind(addr)  
# 开始监听，最大连接数为5  
s.listen(5)  
print("监听中，请在浏览器中访问 http://%s:8081/" % (network.LAN().ifconfig()[0]))
```

这段代码首先创建了一个socket对象，并设置了`SO_REUSEADDR`选项，允许在同一端口上启动服务器的多个实例（在重启服务器时很有用）。然后，将socket绑定到所有网络接口上的8081端口，并开始监听连接。监听队列的大小设置为5，表示最多可以同时处理5个连接请求。

### 2.6 处理客户端请求

```python
counter = 0  
while True:  
    # 接受连接  
    res = s.accept()  
    client_sock = res[0]  
    client_addr = res[1]  
    print("客户端地址:", client_addr)  
    print("客户端socket:", client_sock)  
  
    # 根据是否使用MicroPython优化，选择不同的读取方式  
    if not micropython_optimize:  
        # 使用流式接口（适用于CPython）  
        client_stream = client_sock.makefile("rwb")  
    else:  
        # 直接使用socket对象（MicroPython特有）  
        client_stream = client_sock  
  
    # 读取请求内容（此处略过详细解析，仅作为示例）  
    # ...  
  
    # 发送响应内容  
    client_stream.write(CONTENT % counter)  
    # 关闭连接  
    client_stream.close()  
  
    counter += 1  
    time.sleep(2)  
    if counter > 0:  
        print("HTTP服务器退出！")  
        s.close()  
        break
```

这部分代码实现了服务器的主循环，用于不断接受来自客户端的连接请求，并发送响应。根据`micropython_optimize`参数的值，服务器会选择不同的方式读取socket数据。在发送完响应后，关闭与客户端的连接，并等待一段时间（本例中为2秒）后再次接受新的连接请求。

### 2.7 完整例程

```python
# port from micropython/examples/network/http_server.py
import socket
import network
import time
# print(network.LAN().ifconfig()[0])
# print("Listening, connect your browser to http://%s:8081/" % (network.LAN().ifconfig()[0]))

CONTENT = b"""\
HTTP/1.0 200 OK

Hello #%d from k230 canmv MicroPython!
"""


def main(micropython_optimize=True):
    #获取lan接口
    a=network.LAN()
    if(a.active()):
        a.active(0)
    a.active(1)
    a.ifconfig("dhcp")
  
    #建立socket
    s = socket.socket()
    #获取地址及端口号 对应地址
    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 8081)
    print("Bind address info:", ai)
    addr = ai[0][-1]
    #设置属性
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #绑定地址
    s.bind(addr)
    #开始监听
    s.listen(5)
    print("Listening, connect your browser to http://%s:8081/" % (network.LAN().ifconfig()[0]))

    counter = 0
    while True:
        #接受连接
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)
        #非阻塞模式
        client_sock.setblocking(False)
        if not micropython_optimize:
            # To read line-oriented protocol (like HTTP) from a socket (and
            # avoid short read problem), it must be wrapped in a stream (aka
            # file-like) object. That's how you do it in CPython:
            client_stream = client_sock.makefile("rwb")
        else:
            # .. but MicroPython socket objects support stream interface
            # directly, so calling .makefile() method is not required. If
            # you develop application which will run only on MicroPython,
            # especially on a resource-constrained embedded device, you
            # may take this shortcut to save resources.
            client_stream = client_sock

        print("Request:")
        #获取内容
        req = client_stream.read()
        print(req)
  
        while True:
            ##获取内容
            h = client_stream.read()      
            if h == b"" or h == b"\r\n":
                break
            print(h)
        #回复内容
        client_stream.write(CONTENT % counter)
        #time.sleep(0.5)
        #关闭
        client_stream.close()
        # if not micropython_optimize:
        #     client_sock.close()
        counter += 1
        #print("wjx", counter)
        time.sleep(2)
        if counter > 0 :
            print("http server exit!")
            #关闭 
            s.close()
            break

main()
```

具体接口定义请参考 [socket](../../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../../api/extmod/K230_CanMV_network模块API手册.md)

## 3. 例程现象与操作说明

在CanMV IDE K230中运行例程代码，在IDE串口终端会输出以下打印：
![image-20240722134617332](../images/network/image-20240722134617332.png)

复制打印输出的网址信息并在浏览器中访问打开：

![image-20240722134912486](../images/network/image-20240722134912486.png)
