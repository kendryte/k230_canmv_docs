# Explanation of the UDP-Client Example

## Environment Preparation

To ensure a smooth demonstration of UDP communication, we need to confirm that the following environment is correctly configured:

### Hardware Connection

- Ensure that your CanMV development board and computer are connected to the same router or switch via Ethernet cable to form a local area network (LAN).
- Ensure that the router or switch is working properly to guarantee network stability.

### Disable Firewall

- To avoid the firewall blocking UDP communication, it is recommended to temporarily disable the computer's firewall.

```{image} ../../../zh/example/images/network/image-20240722145319713.png
:scale: 50 %
```

### Tools Preparation

- Download and install [NetAssist Network Debugging Assistant](https://www.bing.com/search?q=netassist+cmsoft) as a network communication testing tool to help with sending and receiving network data.

### Obtain IP Address

- Open the command prompt (CMD), enter `ipconfig`, and record the IP address of the computer's network card for subsequent configuration and testing.

```{image} ../../../zh/example/images/network/image-20240722145500693.png
:scale: 50 %
```

## Client Example Analysis

This UDP client example demonstrates how to create a simple UDP client, including connecting to a server, sending data, and closing the connection. You can learn the basic methods of building UDP communication applications through this example.

### Import Necessary Libraries

```python
import socket  
import network  
import time
```

- The `socket` library is responsible for creating network communication sockets.
- The `network` library is used to configure network interfaces, such as enabling LAN or WLAN.
- The `time` library provides delay operations, usually used to control data sending frequency or timeout handling.

### Configure Network Interface

```python
def network_use_wlan(is_wlan=True):
    if is_wlan:
        sta = network.WLAN(0)
        sta.connect("Canaan", "Canaan314")
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

This function configures the network interface based on whether a wireless network (WLAN) or a wired network (LAN) is chosen, with the following steps:

1. **WLAN Mode**: Attempts to connect to a Wi-Fi network and waits to obtain a valid IP address before returning.
1. **LAN Mode**: Activates the LAN interface and uses DHCP mode to obtain an IP address.

### Create UDP Socket

```python
# Get the server's IP and port number  
ai = socket.getaddrinfo('172.16.1.174', 8080)
print("Address infos:", ai)  
addr = ai[0][-1]  # Extract IP and port number

print("Connecting to address:", addr) 
# Create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

Here, the server's IP and port information is obtained through `socket.getaddrinfo`, and the address and port number are extracted. Then, a UDP socket is created.

### Send Data

```python
# Send test messages
for i in range(10):
    message = "K230 UDP client send test {0} \r\n".format(i)
    print("Sending:", message)
    # Encode the message into bytes and send
    bytes_sent = s.sendto(message.encode(), addr)
    print("Bytes sent:", bytes_sent)
    # Pause for a while before the next send
    time.sleep(0.2)
```

In the loop, the program generates test messages and sends them to the specified server address using the `sendto` function. The message needs to be converted into a byte string before sending. After sending successfully, the number of bytes sent is printed, and a short delay is set.

### Close Socket

```python
# Close the socket
s.close()
print("Client ended.")
```

After the data is sent, the socket is closed to release resources.

### Complete Example

```python
import socket
import os
import time
import network

def network_use_wlan(is_wlan=True):
    if is_wlan:
        sta = network.WLAN(0)
        sta.connect("Canaan", "Canaan314")
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

def udpclient():
    # Configure network interface
    network_use_wlan(True)
  
    # Get server address and port number
    ai = socket.getaddrinfo('192.168.1.110', 8080)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("Connect address:", addr)
    # Create UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for i in range(10):
        message = "K230 UDP client send test {0} \r\n".format(i)
        print("Sending:", message)
        # Send string
        bytes_sent = s.sendto(message.encode(), addr)
        print("Bytes sent:", bytes_sent)
        time.sleep(0.2)
    
    # Close the socket
    s.close()
    print("Client ended.")
 
# Start the client
udpclient()
```

## Run and Test

1. Use NetAssist Network Debugging Assistant to establish a UDP connection:

```{image} ../../../zh/example/images/network/image-20240722171950467.png
:scale: 50 %
```

1. Modify the server IP address in the code:

```python
ai = socket.getaddrinfo("172.16.1.174", 8080)
```

1. After running the example, NetAssist will display the received UDP packets:

```{image} ../../../zh/example/images/network/image-20240722172037608.png
:scale: 50 %
```
