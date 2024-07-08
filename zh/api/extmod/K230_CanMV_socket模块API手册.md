# 2.3 socket 模块API手册

![cover](../images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍soccket模块API。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |

### 修订记录

| 文档版本号 | 修改说明 | 修改者 | 日期       |
| ---------- | -------- | ------ | ---------- |
| V1.0       | 初版     | 软件部 | 2023-11-09 |

## 1. 概述

封装socket库，需要通过核间通信调用小核的socket接口。

## 2.示例

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

## 3. api定义

详见`https://docs.micropython.org/en/latest/library/socket.html`

### 3.1 定义

- *class*socket.socket(*af=AF_INET*, *type=SOCK_STREAM*, *proto=IPPROTO_TCP*, */*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket)

  Create a new socket using the given address family, socket type and protocol number. Note that specifying *proto* in most cases is not required (and not recommended, as some MicroPython ports may omit `IPPROTO_*` constants). Instead, *type* argument will select needed protocol automatically:`# Create STREAM TCP socket socket(AF_INET, SOCK_STREAM) # Create DGRAM UDP socket socket(AF_INET, SOCK_DGRAM)`

### 3.2 函数

- socket.close()[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.close)

  Mark the socket closed and release all resources. Once that happens, all future operations on the socket object will fail. The remote end will receive EOF indication if supported by protocol.Sockets are automatically closed when they are garbage-collected, but it is recommended to [`close()`](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.close) them explicitly as soon you finished working with them.

- socket.bind(*address*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.bind)

  Bind the socket to *address*. The socket must not already be bound.

- socket.listen(**[***backlog***]**)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.listen)

  Enable a server to accept connections. If *backlog* is specified, it must be at least 0 (if it’s lower, it will be set to 0); and specifies the number of unaccepted connections that the system will allow before refusing new connections. If not specified, a default reasonable value is chosen.

- socket.accept()[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.accept)

  Accept a connection. The socket must be bound to an address and listening for connections. The return value is a pair (conn, address) where conn is a new socket object usable to send and receive data on the connection, and address is the address bound to the socket on the other end of the connection.

- socket.connect(*address*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.connect)

  Connect to a remote socket at *address*.

- socket.send(*bytes*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.send)

  Send data to the socket. The socket must be connected to a remote socket. Returns number of bytes sent, which may be smaller than the length of data (“short write”).

- socket.sendall(*bytes*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.sendall)

  Send all data to the socket. The socket must be connected to a remote socket. Unlike [`send()`](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.send), this method will try to send all of data, by sending data chunk by chunk consecutively.The behaviour of this method on non-blocking sockets is undefined. Due to this, on MicroPython, it’s recommended to use [`write()`](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.write) method instead, which has the same “no short writes” policy for blocking sockets, and will return number of bytes sent on non-blocking sockets.

- socket.recv(*bufsize*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.recv)

  Receive data from the socket. The return value is a bytes object representing the data received. The maximum amount of data to be received at once is specified by bufsize.

- socket.sendto(*bytes*, *address*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.sendto)

  Send data to the socket. The socket should not be connected to a remote socket, since the destination socket is specified by *address*.

- socket.recvfrom(*bufsize*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.recvfrom)

  Receive data from the socket. The return value is a pair *(bytes, address)* where *bytes* is a bytes object representing the data received and *address* is the address of the socket sending the data.

- socket.setsockopt(*level*, *optname*, *value*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.setsockopt)

  Set the value of the given socket option. The needed symbolic constants are defined in the socket module (SO_* etc.). The *value* can be an integer or a bytes-like object representing a buffer.

- socket.settimeout(*value*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.settimeout)

  **Note**: Not every port supports this method, see below.Set a timeout on blocking socket operations. The value argument can be a nonnegative floating point number expressing seconds, or None. If a non-zero value is given, subsequent socket operations will raise an [`OSError`](https://docs.micropython.org/en/latest/library/builtins.html#OSError) exception if the timeout period value has elapsed before the operation has completed. If zero is given, the socket is put in non-blocking mode. If None is given, the socket is put in blocking mode.Not every [MicroPython port](https://docs.micropython.org/en/latest/reference/glossary.html#term-MicroPython-port) supports this method. A more portable and generic solution is to use [`select.poll`](https://docs.micropython.org/en/latest/library/select.html#select.poll) object. This allows to wait on multiple objects at the same time (and not just on sockets, but on generic [`stream`](https://docs.micropython.org/en/latest/reference/glossary.html#term-stream) objects which support polling). Example:`# Instead of: s.settimeout(1.0)  # time in seconds s.read(10)  # may timeout # Use: poller = select.poll() poller.register(s, select.POLLIN) res = poller.poll(1000)  # time in milliseconds if not res:    # s is still not ready for input, i.e. operation timed out`Difference to CPythonCPython raises a `socket.timeout` exception in case of timeout, which is an [`OSError`](https://docs.micropython.org/en/latest/library/builtins.html#OSError) subclass. MicroPython raises an OSError directly instead. If you use `except OSError:` to catch the exception, your code will work both in MicroPython and CPython.

- socket.setblocking(*flag*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.setblocking)

  Set blocking or non-blocking mode of the socket: if flag is false, the socket is set to non-blocking, else to blocking mode.This method is a shorthand for certain [`settimeout()`](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.settimeout) calls:`sock.setblocking(True)` is equivalent to `sock.settimeout(None)``sock.setblocking(False)` is equivalent to `sock.settimeout(0)`

- socket.makefile(*mode='rb'*, *buffering=0*, */*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.makefile)

  Return a file object associated with the socket. The exact returned type depends on the arguments given to makefile(). The support is limited to binary modes only (‘rb’, ‘wb’, and ‘rwb’). CPython’s arguments: *encoding*, *errors* and *newline* are not supported.Difference to CPythonAs MicroPython doesn’t support buffered streams, values of *buffering* parameter is ignored and treated as if it was 0 (unbuffered).Difference to CPythonClosing the file object returned by makefile() WILL close the original socket as well.

- socket.read(**[***size***]**)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.read)

  Read up to size bytes from the socket. Return a bytes object. If *size* is not given, it reads all data available from the socket until EOF; as such the method will not return until the socket is closed. This function tries to read as much data as requested (no “short reads”). This may be not possible with non-blocking socket though, and then less data will be returned.

- socket.readinto(*buf***[**, *nbytes***]**)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.readinto)

  Read bytes into the *buf*. If *nbytes* is specified then read at most that many bytes. Otherwise, read at most *len(buf)* bytes. Just as [`read()`](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.read), this method follows “no short reads” policy.Return value: number of bytes read and stored into *buf*.

- socket.readline()[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.readline)

  Read a line, ending in a newline character.Return value: the line read.

- socket.write(*buf*)[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.write)

  Write the buffer of bytes to the socket. This function will try to write all data to a socket (no “short writes”). This may be not possible with a non-blocking socket though, and returned value will be less than the length of *buf*.Return value: number of bytes written.

- *exception*socket.error[¶](https://docs.micropython.org/en/latest/library/socket.html#socket.socket.error)

  MicroPython does NOT have this exception.Difference to CPythonCPython used to have a `socket.error` exception which is now deprecated, and is an alias of [`OSError`](https://docs.micropython.org/en/latest/library/builtins.html#OSError). In MicroPython, use [`OSError`](https://docs.micropython.org/en/latest/library/builtins.html#OSError) directly.
  