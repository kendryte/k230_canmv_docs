# HTTP-Client Example Explanation

## Environment Setup

First, ensure that the CanMV development board is connected to a router or switch via an Ethernet port, and that the router is functioning properly with internet access. This is the basic setup for making HTTP requests.

## Detailed Example

The following Python example demonstrates how to implement an HTTP client on the CanMV development board. This client sends an HTTP GET request to a specified server (in this case, Baidu) and receives the response content.

### Import Necessary Modules

```python
import network  
import socket
```

- The `network` module is used to manage network interfaces.
- The `socket` module provides the underlying interface for network communication.

### Define the Main Function

```python
def main(use_stream=True):  
    # ... (subsequent code)
```

The `main` function defines a parameter `use_stream` which determines whether to use a stream interface to read the response data. The default value is `True`, which controls the data reception method.

### Configure Network Interface

```python
def network_use_wlan(is_wlan=True):
    if is_wlan:
        sta = network.WLAN(0)
        sta.connect("TEST", "12345678")
        print(sta.status())
        while sta.ifconfig()[0] == '0.0.0.0':
            os.exitpoint()
        print(sta.ifconfig())
        ip = sta.ifconfig()[0]
        return ip
    else:
        a = network.LAN()
        if not a.active():
            raise RuntimeError("LAN interface is not active.")
        a.ifconfig("dhcp")
        print(a.ifconfig())
        ip = a.ifconfig()[0]
        return ip
```

This function configures the network interface based on the input:

1. **WLAN Mode**: Connects to a specified Wi-Fi network (SSID is "TEST") using the wireless network interface (WLAN).
1. **LAN Mode**: Automatically obtains an IP address using the wired network interface (LAN).

### Create and Configure Socket

```python
# Create socket object  
s = socket.socket()   
# Get target address and port number  
ai = []  
for attempt in range(0, 3):  
    try:  
        ai = socket.getaddrinfo("www.baidu.com", 80)  
        break  
    except:  
        print("getaddrinfo again")  
  
if ai == []:  
    print("Connection error")  
    s.close()  
    return  
  
addr = ai[0][-1]  
print("Connection address:", addr)
```

This code creates a `socket` object and uses the `getaddrinfo` function to obtain the server's (Baidu) address and port information. It employs a retry mechanism to enhance robustness.

### Send HTTP Request and Receive Response

```python
# Connect to the server  
s.connect(addr)  
  
if use_stream:  
    # Use stream interface to read response  
    s = s.makefile("rwb", 0)  
    s.write(b"GET /index.html HTTP/1.0\r\n\r\n")  
    print(s.read())  
else:  
    # Directly use socket interface to send and receive data  
    s.send(b"GET /index.html HTTP/1.0\r\n\r\n")  
    print(s.recv(4096))  
   
# Close socket  
s.close()
```

The code selects whether to use the stream interface or directly use the socket interface to send an HTTP request and read the response data based on the `use_stream` parameter.

### Function Invocation

```python
# Test both stream and non-stream interfaces  
main(use_stream=True)  
main(use_stream=False)
```

The `main` function is called with different `use_stream` parameters to test the effects of reading the HTTP response using stream and non-stream methods. If `use_stream` is `True`, it uses the stream interface to send the request and read the entire response; if `False`, it directly sends the request and receives a fixed length of response data (4096 bytes in this example). Finally, the socket connection is closed to release resources.

### Complete Example

```python
import network
import socket
import os, time

def network_use_wlan(is_wlan=True):
    if is_wlan:
        sta = network.WLAN(0)
        sta.connect("TEST", "12345678")
        print(sta.status())
        while sta.ifconfig()[0] == '0.0.0.0':
            os.exitpoint()
        print(sta.ifconfig())
        ip = sta.ifconfig()[0]
        return ip
    else:
        a = network.LAN()
        if not a.active():
            raise RuntimeError("LAN interface is not active.")
        a.ifconfig("dhcp")
        print(a.ifconfig())
        ip = a.ifconfig()[0]
        return ip

def main(use_stream=True):
    # Get LAN interface
    network_use_wlan(True)
    # Create socket
    s = socket.socket()
    # Get address and port number
    ai = []
    for attempt in range(0, 3):
        try:
            ai = socket.getaddrinfo("www.baidu.com", 80)
            break
        except:
            print("getaddrinfo again")
    
    if ai == []:
        print("Connection error")
        s.close()
        return

    addr = ai[0][-1]
    print("Connection address:", addr)
    # Connect
    s.connect(addr)

    if use_stream:
        s = s.makefile("rwb", 0)
        s.write(b"GET /index.html HTTP/1.0\r\n\r\n")
        print(s.read())
    else:
        s.send(b"GET /index.html HTTP/1.0\r\n\r\n")
        print(s.recv(4096))

    s.close()
 
# main()
main(use_stream=True)
main(use_stream=False)
```

For specific interface definitions, please refer to [socket](../../api/extmod/K230_CanMV_socket_API_Manual.md) and [network](../../api/extmod/K230_CanMV_network_API_Manual.md).
