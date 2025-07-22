# `socket` 模块 API 手册

## 概述

该模块封装了 `socket` 库，用户可以通过调用 `socket` 库进行网络应用程序开发。

## 示例

```python
# 配置 tcp/udp socket 调试工具
import socket
import time

PORT = 60000

def client():
    # 获取 IP 地址及端口号
    ai = socket.getaddrinfo("10.100.228.5", PORT)
    # ai = socket.getaddrinfo("10.10.1.94", PORT)
    print("地址信息:", ai)
    addr = ai[0][-1]

    print("连接地址:", addr)
    # 创建 socket 对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    # 连接到指定地址
    s.connect(addr)

    for i in range(10):
        msg = "K230 TCP 客户端发送测试 {0} \r\n".format(i)
        print(msg)
        # 发送字符串数据
        print(s.write(msg))
        time.sleep(0.2)

    # 延时 1 秒后关闭 socket
    time.sleep(1)
    s.close()
    print("结束")

# 运行客户端程序
client()
```

## API 定义

详见 [Micropython socket module](https://docs.micropython.org/en/latest/library/socket.html)

### 构造函数

- **class** socket.socket(*af=AF_INET*, *type=SOCK_STREAM*, *proto=IPPROTO_TCP*)  

  创建一个新的套接字对象，使用指定的地址族（`af`）、套接字类型（`type`）和协议（`proto`）。通常，**无需**显式指定 `proto` 参数，MicroPython 会根据 `type` 自动选择相应的协议类型。示例：
  - 创建一个 TCP 流套接字：`socket(AF_INET, SOCK_STREAM)`
  - 创建一个 UDP 数据报套接字：`socket(AF_INET, SOCK_DGRAM)`

### 方法

- **socket.close()**

  关闭套接字并释放其相关资源。关闭后，所有对该套接字对象的操作将会失败。协议支持时，远程端会收到 EOF 指示。尽管套接字在被垃圾回收时会自动关闭，但建议在使用完后显式调用 `close()` 方法。

- **socket.bind(address)**

  将套接字绑定到指定的 IP 地址和端口。调用前确保套接字未被绑定。

- **socket.listen([backlog])**

  使服务器套接字开始监听连接请求。`backlog` 指定等待连接的最大数目，最小为 0（小于 0 的值将视为 0），如果未指定，则使用系统默认值。

- **socket.accept()**

  接受客户端连接。此方法返回 `(conn, address)`，其中 `conn` 是一个新套接字对象，可用于在该连接上发送和接收数据，`address` 是客户端的地址。

- **socket.connect(address)**

  连接到指定的服务端套接字地址。

- **socket.send(bytes)**

  向套接字发送数据，套接字必须已连接。返回发送的字节数，这可能小于数据的总长度（即“短写”情况）。

- **socket.sendall(bytes)**

  向套接字发送完整数据，套接字必须已连接。与 `send()` 不同，此方法会尝试连续发送所有数据，直至传输完成。该方法在非阻塞套接字上行为未定义，因此建议在 MicroPython 中使用 `write()` 方法。

- **socket.recv(bufsize)**

  从套接字接收数据，返回接收到的数据字节对象。`bufsize` 指定单次接收的最大字节数。

- **socket.sendto(bytes, address)**

  向未连接的套接字发送数据，目标地址由 `address` 指定。

- **socket.recvfrom(bufsize)**

  从未连接的套接字接收数据，返回 `(bytes, address)`，其中 `bytes` 是接收到的数据，`address` 是发送数据的源地址。

- **socket.setsockopt(level, optname, value)**

  设置套接字选项。`value` 可以是整数或字节类对象。

- **socket.settimeout(value)**

  设置套接字操作的超时时间（以秒为单位）。`value` 可以是一个正数、零或 `None`。若超时，操作将引发 `OSError`。在非阻塞模式下，设置 `value` 为零；在阻塞模式下，设置为 `None`。

- **socket.setblocking(flag)**

  设置套接字的阻塞模式。`flag` 为 `False` 时为非阻塞模式，为 `True` 时为阻塞模式。

- **socket.makefile(mode='rb', buffering=0)**

  返回与套接字关联的文件对象。仅支持二进制模式（如 `rb`、`wb` 和 `rwb`），`buffering` 参数在 MicroPython 中被忽略。

- **socket.read([size])**

  从套接字读取数据，返回字节对象。若未指定 `size`，则读取所有可用数据，直至 EOF。

- **socket.readinto(buf[, nbytes])**

  将数据读取到 `buf` 中，若指定 `nbytes`，则读取最多 `nbytes` 字节，否则读取 `len(buf)` 字节。

- **socket.readline()**

  从套接字读取一行数据，返回字节对象。

- **socket.write(buf)**

  将 `buf` 中的数据写入套接字。尽量写入所有数据，但对于非阻塞套接字，可能只写入部分数据。

- **socket.error**

  在 MicroPython 中未定义 `socket.error` 异常，直接使用 `OSError`。
  