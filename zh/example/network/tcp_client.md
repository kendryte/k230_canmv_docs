# 3. TCP-Client例程讲解

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

### 2.1 导入库

```python
import network  
import socket  
import time
```

- **network**：这个库用于操作网络接口，如配置IP地址、检查网络状态等。
- **socket**：这个库提供了socket接口，用于网络通信。
- **time**：这个库提供了与时间相关的函数，如延时（sleep）。

### 2.2 定义客户端函数

```python
def client():  
    # ...（后续代码）
```

- 定义了一个名为`client`的函数，这个函数包含了TCP客户端的所有逻辑。

### 2.3 配置网络接口

```python
lan = network.LAN()  
    if lan.active():  
        lan.active(0)  # 如果已经激活，先关闭  
    lan.active(1)      # 重新激活以获取IP  
    lan.ifconfig("dhcp")  # 使用DHCP自动配置IP  
    print("LAN Interface Config:", lan.ifconfig())  # 打印配置信息
```

这部分代码首先获取LAN接口实例，并检查其状态。如果网口已激活，则先关闭再激活（这一步在大多数情况下不是必需的，但提供了操作接口的示例）。然后，设置网口为DHCP模式，以便自动从路由器获取IP地址等配置信息。

### 2.4 创建Socket

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
```

- 创建一个新的socket对象，使用IPv4（`AF_INET`）和TCP（`SOCK_STREAM`）协议。第三个参数（通常为0）用于指定socket的类型或其他选项，但在大多数情况下可以保持为0。

### 2.5 获取服务器地址和端口

```python
ai = socket.getaddrinfo("172.16.1.174", 8080)  
    addr = ai[0][-1]  # 提取地址和端口
```

- **地址解析**：使用`getaddrinfo`函数根据提供的服务器地址（`"172.16.1.174"`）和端口号（`8080`）获取地址信息。这个函数返回一个列表，其中每个元素都是一个包含多个元素的元组，第一个元素是地址族（如IPv4或IPv6），最后一个元素是一个包含地址和端口的元组。
- **提取地址和端口**：从`getaddrinfo`返回的结果中选择第一个元素（通常是首选的协议和地址），并提取出地址和端口。

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

- 尝试使用`connect`方法连接到服务器。如果连接成功，则打印连接信息。
- 如果在连接过程中发生异常（如网络不可达、服务器未运行等），则捕获异常并打印错误信息，然后关闭socket并退出函数。

### 2.7 发送数据

```python
for i in range(10):  
        message = "K230 tcp client send test {0} \r\n".format(i)  
        print("Sending:", message)  
        s.sendall(message.encode())  # 发送数据前需要编码为字节串  
        time.sleep(0.2)  # 稍作延时
```

- 在一个循环中发送10条消息。
- 构造每条消息，并使用`format`方法将循环变量`i`插入到消息中。
- 在发送之前，使用`encode`方法将消息编码为字节串，因为`sendall`方法需要字节串作为参数。
- 使用`sendall`方法发送数据，这个方法会尝试发送所有数据，直到所有数据都被发送完毕或发生错误。
- 在每次发送后使用`time.sleep`方法稍作延时，以模拟发送间隔。

### 2.8 关闭Socket

```python
s.close()  
    print("Client ends connection.")
```

- 在完成所有通信后，使用`close`方法关闭socket，以释放资源。
- 打印一条消息表示客户端已结束连接。

### 2.9 完整例程

```python
#配置 tcp/udp socket调试工具
import network
import socket
import time

def client():
    #获取lan接口
    a=network.LAN()
    if(a.active()):
        a.active(0)
    a.active(1)
    a.ifconfig("dhcp")
    print(a.ifconfig())
  
    #建立socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    #获取地址及端口号 对应地址。（地址根据实际情况填写）
    ai = socket.getaddrinfo("172.16.1.174", 8080)
    #ai = socket.getaddrinfo("10.10.1.94", PORT)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("Connect address:", addr)
    #连接地址
    if(s.connect(addr) == False):
        s.close()
        print("conner err")
        return

    for i in range(10):
        str="K230 tcp client send test {0} \r\n".format(i)
        print(str)
        #print(s.send(str))
        #发送字符串
        print(s.write(str))
        time.sleep(0.2)
        #time.sleep(1)
        #print(s.recv(4096))
        #print(s.read())
    #延时1秒
    time.sleep(1)
    #关闭socket
    s.close()
    print("end")



#main()
client()
```

## 3. 例程现象与操作说明

打开NetAssist网络调试助手，建立TCP server连接：

```{image} ../images/network/image-20240722152102440.png
:scale: 50 %
```

在例程源码中修改对应的IP，端口：

```python
ai = socket.getaddrinfo("172.16.1.174", 8080)
```

运行例程代码，NetAssist网络调试助手输出信息：

```{image} ../images/network/image-20240722151843380.png
:scale: 50 %
```
