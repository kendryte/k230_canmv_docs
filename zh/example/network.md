# 5.网络 例程讲解

## 1. network - wlan 例程

本示例程序用于对 CanMV 开发板进行一个 network wlan 的功能展示。

```python
import network

def sta_test():
    sta=network.WLAN(0)
    #查看sta是否激活
    print(sta.active())
    #查看sta状态
    print(sta.status())
    #扫描并打印结果
    print(sta.scan())
    #sta连接ap
    print(sta.connect("wjx_pc","12345678"))
    #状态
    print(sta.status())
    #查看ip配置
    print(sta.ifconfig())
    #查看是否连接
    print(sta.isconnected())
    #断开连接
    print(sta.disconnect())
    #连接ap
    print(sta.connect("wjx_pc","12345678"))
    #查看状态
    print(sta.status())


def ap_test():
    ap=network.WLAN(network.AP_IF)
    #查看ap是否激活
    print(ap.active())
    #配置并创建ap
    ap.config(ssid='k230_ap_wjx', channel=11, key='12345678')
    #查看ap的ssid号
    print(ap.config('ssid'))
    #查看ap的channel
    print(ap.config('channel'))
    #查看ap的所有配置
    print(ap.config())
    #查看ap的状态
    print(ap.status())
    #sta是否连接ap
    print(ap.isconnected())

sta_test()
ap_test()
```

具体接口定义请参考 [socket](../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../api/extmod/K230_CanMV_network模块API手册.md)

---

## 2. tcp - client 例程

本示例程序用于对 CanMV 开发板进行一个 tcp client 的功能展示。

```python
#配置 tcp/udp socket调试工具
import socket
import time

PORT=60000

def client():
    #获取地址及端口号 对应地址
    ai = socket.getaddrinfo("10.100.228.5", PORT)
    #ai = socket.getaddrinfo("10.10.1.94", PORT)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("Connect address:", addr)
    #建立socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    #连接地址
    s.connect(addr)

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

具体接口定义请参考 [socket](../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../api/extmod/K230_CanMV_network模块API手册.md)

---

## 3. udp - server 例程

本示例程序用于对 CanMV 开发板进行一个 udp server 的功能展示。

```python
#配置 tcp/udp socket调试工具
import socket
import time
import network
PORT=60000


def udpserver():
    #获取地址及端口号对应地址
    ai = socket.getaddrinfo("0.0.0.0", PORT)
    #ai = socket.getaddrinfo("10.10.1.94", 60000)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("udp server %s port:%d\n" % ((network.LAN().ifconfig()[0]),PORT))
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

具体接口定义请参考 [socket](../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../api/extmod/K230_CanMV_network模块API手册.md)

---

## 4. http - client 例程

本示例程序用于对 CanMV 开发板进行一个 http client 的功能展示。

```python
import socket


def main(use_stream=True):
    #创建socket
    s = socket.socket()
    #获取地址及端口号 对应地址
    ai = socket.getaddrinfo("www.baidu.com", 80)
    #ai = socket.getaddrinfo("10.100.228.5", 8080)

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

具体接口定义请参考 [socket](../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../api/extmod/K230_CanMV_network模块API手册.md)

---

## 5. udp - client 例程

本示例程序用于对 CanMV 开发板进行一个 udp client 的功能展示。

```python
#配置 tcp/udp socket调试工具
import socket
import time


def udpclient():
    #获取地址和端口号 对应地址
    ai = socket.getaddrinfo("10.100.228.5", 60000)
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

具体接口定义请参考 [socket](../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../api/extmod/K230_CanMV_network模块API手册.md)

---

## 6. http - server 例程

本示例程序用于对 CanMV 开发板进行一个 http server 的功能展示。

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
        if counter > 20 :
            print("http server exit!")
            #关闭
            s.close()
            break


main()

```

具体接口定义请参考 [socket](../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../api/extmod/K230_CanMV_network模块API手册.md)

---

---

## 7. tcp - server 例程

本示例程序用于对 CanMV 开发板进行一个 tcp server 的功能展示。

```python
#配置 tcp/udp socket调试工具
import socket
import network
import time
PORT=60000


CONTENT = b"""
Hello #%d from k230 canmv MicroPython!
"""



def server():
    counter=1
    #获取地址及端口号 对应地址
    #ai = socket.getaddrinfo("10.100.228.5", 8000)
    ai = socket.getaddrinfo("0.0.0.0", PORT)
    print("Address infos:", ai,PORT)
    addr = ai[0][-1]

    print("Connect address:", addr)
    #建立socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    #设置属性
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #绑定
    s.bind(addr)
    #监听
    s.listen(5)
    print("tcp server %s port:%d\n" % ((network.LAN().ifconfig()[0]),PORT))


    while True:
        #接受连接
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)
        client_sock.setblocking(False)

        client_stream = client_sock
        #发送字符传
        client_stream.write(CONTENT % counter)

        while True:
            #读取内容
            h = client_stream.read()
            if h != b"" :
                print(h)
                #回复内容
                client_stream.write("recv :%s" % h)

            if "end" in h :
                #关闭socket
                client_stream.close()
                break

        counter += 1
        if counter > 10 :
            print("server exit!")
            #关闭
            s.close()
            break

#main()
server()

```

具体接口定义请参考 [socket](../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../api/extmod/K230_CanMV_network模块API手册.md)

---

## 8. network - lan 例程

本示例程序用于对 CanMV 开发板进行一个 network lan 的功能展示。

```python
import network


def main():
    #获取lan接口
    a=network.LAN()
    #获取网口是否在使用
    print(a.active())
    #关闭网口
    print(a.active(0))
    #使能网口
    print(a.active(1))
    #查看网口 ip，掩码，网关，dns配置
    print(a.ifconfig())
    #设置网口 ip，掩码，网关，dns配置
    print(a.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8')))
    #查看网口 ip，掩码，网关，dns配置
    print(a.ifconfig())
    #设置网口为dhcp模式
    print(a.ifconfig("dhcp"))
    #查看网口 ip，掩码，网关，dns配置
    print(a.ifconfig())
    #查看网口mac地址
    print(a.config("mac"))
    #设置网口mac地址
    print(a.config(mac="42:EA:D0:C2:0D:83"))
    #查看网口mac地址
    print(a.config("mac"))
    #设置网口为dhcp模式
    print(a.ifconfig("dhcp"))
    #查看网口 ip，掩码，网关，dns配置
    print(a.ifconfig())




main()


```

具体接口定义请参考 [socket](../api/extmod/K230_CanMV_socket模块API手册.md)、[network](../api/extmod/K230_CanMV_network模块API手册.md)

---
