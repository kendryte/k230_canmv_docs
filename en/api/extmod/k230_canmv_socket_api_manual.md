# `socket` Module API Manual

## Overview

This module wraps the `socket` library, allowing users to develop network applications by calling the `socket` library.

## Example

```python
# Configure tcp/udp socket debugging tool
import socket
import time

PORT = 60000

def client():
    # Get IP address and port number
    ai = socket.getaddrinfo("192.168.1.100", PORT)  # Replace with your server's LAN IP
    print("Address Info:", ai)
    addr = ai[0][-1]

    print("Connect Address:", addr)
    # Create socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    # Connect to the specified address
    s.connect(addr)

    for i in range(10):
        msg = "K230 TCP client send test {0} \r\n".format(i)
        print(msg)
        # Send string data
        print(s.write(msg))
        time.sleep(0.2)

    # Close the socket after a 1-second delay
    time.sleep(1)
    s.close()
    print("End")

# Run the client program
client()
```

## API Definitions

See [Micropython socket module](https://docs.micropython.org/en/latest/library/socket.html)

### Constructor

- **class** socket.socket(*af=AF_INET*, *type=SOCK_STREAM*, *proto=IPPROTO_TCP*)  

  Creates a new socket object using the specified address family (`af`), socket type (`type`), and protocol (`proto`). Typically, there is **no need** to explicitly specify the `proto` parameter, as MicroPython will automatically select the corresponding protocol type based on `type`. Examples:
  - Create a TCP stream socket: `socket(AF_INET, SOCK_STREAM)`
  - Create a UDP datagram socket: `socket(AF_INET, SOCK_DGRAM)`

### Methods

- **socket.close()**

  Closes the socket and releases its associated resources. After closing, all operations on this socket object will fail. When supported by the protocol, the remote end will receive an EOF indication. Although the socket will be automatically closed when garbage collected, it is recommended to explicitly call the `close()` method after use.

- **socket.bind(address)**

  Binds the socket to the specified IP address and port. Ensure the socket is not already bound before calling.

- **socket.listen([backlog])**

  Causes the server socket to begin listening for connection requests. `backlog` specifies the maximum number of pending connections, with a minimum of 0 (values less than 0 will be treated as 0). If not specified, the system default value is used.

- **socket.accept()**

  Accepts a client connection. This method returns `(conn, address)`, where `conn` is a new socket object that can be used to send and receive data on that connection, and `address` is the client's address.

- **socket.connect(address)**

  Connects to the specified server socket address.

- **socket.send(bytes)**

  Sends data to the socket; the socket must be connected. Returns the number of bytes sent, which may be less than the total length of the data (i.e., a "short write" situation).

- **socket.sendall(bytes)**

  Sends complete data to the socket; the socket must be connected. Unlike `send()`, this method attempts to continuously send all data until transmission is complete. The behavior of this method on non-blocking sockets is undefined, so it is recommended to use the `write()` method in MicroPython.

- **socket.recv(bufsize)**

  Receives data from the socket, returning the received data as a bytes object. `bufsize` specifies the maximum number of bytes to receive in a single call.

- **socket.sendto(bytes, address)**

  Sends data to an unconnected socket, with the destination address specified by `address`.

- **socket.recvfrom(bufsize)**

  Receives data from an unconnected socket, returning `(bytes, address)`, where `bytes` is the received data and `address` is the source address of the data sender.

- **socket.setsockopt(level, optname, value)**

  Sets socket options. `value` can be an integer or a bytes-like object.

- **socket.settimeout(value)**

  Sets the timeout for socket operations (in seconds). `value` can be a positive number, zero, or `None`. If a timeout occurs, the operation will raise an `OSError`. In non-blocking mode, set `value` to zero; in blocking mode, set it to `None`.

- **socket.setblocking(flag)**

  Sets the blocking mode of the socket. When `flag` is `False`, it is in non-blocking mode; when `True`, it is in blocking mode.

- **socket.makefile(mode='rb', buffering=0)**

  Returns a file object associated with the socket. Only binary modes are supported (such as `rb`, `wb`, and `rwb`). The `buffering` parameter is ignored in MicroPython.

- **socket.read([size])**

  Reads data from the socket, returning a bytes object. If `size` is not specified, reads all available data until EOF.

- **socket.readinto(buf[, nbytes])**

  Reads data into `buf`. If `nbytes` is specified, reads at most `nbytes` bytes; otherwise, reads `len(buf)` bytes.

- **socket.readline()**

  Reads a line of data from the socket, returning a bytes object.

- **socket.write(buf)**

  Writes the data in `buf` to the socket. It will attempt to write all data, but for non-blocking sockets, only partial data may be written.

- **socket.error**

  The `socket.error` exception is not defined in MicroPython; use `OSError` directly.
  