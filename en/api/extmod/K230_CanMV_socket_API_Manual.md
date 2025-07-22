# `Socket` Module API Manual

## Overview

This module encapsulates the `socket` library, allowing users to develop network applications by calling the `socket` library.

## Example

```python
# Configure TCP/UDP socket debugging tool
import socket
import time

PORT = 60000

def client():
    # Get IP address and port number
    ai = socket.getaddrinfo("10.100.228.5", PORT)
    # ai = socket.getaddrinfo("10.10.1.94", PORT)
    print("Address info:", ai)
    addr = ai[0][-1]

    print("Connecting to address:", addr)
    # Create socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    # Connect to the specified address
    s.connect(addr)

    for i in range(10):
        msg = "K230 TCP client test message {0} \r\n".format(i)
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

## API Definition

For more details, see [Micropython socket module](https://docs.micropython.org/en/latest/library/socket.html).

### Constructor

- **class** socket.socket(*af=AF_INET*, *type=SOCK_STREAM*, *proto=IPPROTO_TCP*)  

  Creates a new socket object using the specified address family (`af`), socket type (`type`), and protocol (`proto`). Typically, **there is no need** to explicitly specify the `proto` parameter, as MicroPython will automatically select the appropriate protocol type based on `type`. Examples:
  - Create a TCP stream socket: `socket(AF_INET, SOCK_STREAM)`
  - Create a UDP datagram socket: `socket(AF_INET, SOCK_DGRAM)`

### Methods

- **socket.close()**

  Closes the socket and releases its resources. After closing, all operations on the socket object will fail. If supported by the protocol, the remote end will receive an EOF indication. Although sockets are automatically closed when garbage collected, it is recommended to explicitly call the `close()` method after use.

- **socket.bind(address)**

  Binds the socket to the specified IP address and port. Ensure the socket is not already bound before calling.

- **socket.listen([backlog])**

  Makes the server socket start listening for incoming connection requests. `backlog` specifies the maximum number of queued connections, with a minimum of 0 (values less than 0 are treated as 0). If not specified, the system default is used.

- **socket.accept()**

  Accepts a client connection. This method returns `(conn, address)`, where `conn` is a new socket object for sending and receiving data on the connection, and `address` is the client's address.

- **socket.connect(address)**

  Connects to the specified server socket address.

- **socket.send(bytes)**

  Sends data to the socket, which must be connected. Returns the number of bytes sent, which may be less than the total length of the data (a "short write").

- **socket.sendall(bytes)**

  Sends all data to the socket, which must be connected. Unlike `send()`, this method attempts to send all data continuously until complete. This method's behavior is undefined for non-blocking sockets, so it is recommended to use the `write()` method in MicroPython.

- **socket.recv(bufsize)**

  Receives data from the socket, returning the received data as a bytes object. `bufsize` specifies the maximum number of bytes to receive at once.

- **socket.sendto(bytes, address)**

  Sends data to an unconnected socket, with the destination address specified by `address`.

- **socket.recvfrom(bufsize)**

  Receives data from an unconnected socket, returning `(bytes, address)`, where `bytes` is the received data and `address` is the source address.

- **socket.setsockopt(level, optname, value)**

  Sets a socket option. `value` can be an integer or a bytes-like object.

- **socket.settimeout(value)**

  Sets the timeout for socket operations (in seconds). `value` can be a positive number, zero, or `None`. If a timeout occurs, an `OSError` is raised. For non-blocking mode, set `value` to zero; for blocking mode, set to `None`.

- **socket.setblocking(flag)**

  Sets the socket's blocking mode. When `flag` is `False`, the socket is in non-blocking mode; when `True`, it is in blocking mode.

- **socket.makefile(mode='rb', buffering=0)**

  Returns a file object associated with the socket. Only binary modes (such as `rb`, `wb`, and `rwb`) are supported, and the `buffering` parameter is ignored in MicroPython.

- **socket.read([size])**

  Reads data from the socket, returning a bytes object. If `size` is not specified, reads all available data until EOF.

- **socket.readinto(buf[, nbytes])**

  Reads data into `buf`. If `nbytes` is specified, reads up to `nbytes` bytes; otherwise, reads up to `len(buf)` bytes.

- **socket.readline()**

  Reads a line of data from the socket, returning a bytes object.

- **socket.write(buf)**

  Writes the data in `buf` to the socket. Attempts to write all data, but for non-blocking sockets, may write only part of the data.

- **socket.error**

  In MicroPython, the `socket.error` exception is not defined; use `OSError` directly.
  