# 3. TCP-Client Example Explanation

## 1. Environment Preparation

To ensure a smooth demonstration of TCP communication, we need to confirm that the following environment is correctly configured:

### 1.1 Hardware Connection

- Ensure that your CanMV development board and computer are connected to the same router or switch via an Ethernet cable to form a local area network.
- Ensure the router or switch is working properly to guarantee network connection stability.

### 1.2 Disable Firewall

- To avoid the firewall blocking TCP communication, it is recommended to temporarily disable the computer's firewall.

```{image} ../images/network/image-20240722145319713.png
:scale: 50 %
```

### 1.3 Tool Preparation

- Download and install [NetAssist Network Debugging Assistant](https://www.cmsoft.cn/resource/102.html) as a network communication testing tool to help send and receive network data.

### 1.4 Obtain IP Address

- Open the Command Prompt (CMD), enter `ipconfig`, and query and record the IP address of the computer's network card for subsequent configuration and testing.

```{image} ../images/network/image-20240722145500693.png
:scale: 50 %
```

## 2. Client Code Analysis

### 2.1 Import Necessary Libraries

```python
import network  
import socket  
import time
```

- **network**: Used for network interface operations, such as configuring IP addresses and checking network status.
- **socket**: Provides the Socket interface for network communication.
- **time**: Provides functions related to time, such as delay (`sleep`).

### 2.2 Define Client Function

```python
def client():  
    # ... (subsequent code)
```

- The `client` function contains the main logic of the TCP client.

### 2.3 Configure Network Interface

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

Configure the network interface based on the parameters, as follows:

1. **WLAN Mode**:
   - If `is_wlan=True`, configure the wireless network interface (WLAN) and connect to the Wi-Fi with SSID "Canaan" and password "Canaan314".
   - Wait and check if a valid IP address is assigned, then return the IP.

1. **LAN Mode**:
   - If `is_wlan=False`, configure the wired network interface (LAN), enable DHCP to automatically obtain an IP address, and return the IP.

### 2.4 Create Socket

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

- Create a Socket object using IPv4 (`AF_INET`) and TCP (`SOCK_STREAM`) protocol.

### 2.5 Obtain Server Address and Port

```python
ai = socket.getaddrinfo("172.16.1.174", 8080)  
addr = ai[0][-1]  # Extract address and port
```

- Use `getaddrinfo` to obtain the server's IP address and port number, and extract the address information.

### 2.6 Connect to Server

```python
try:  
    s.connect(addr)  
    print("Connected to server:", addr)  
except Exception as e:  
    s.close()  
    print("Connection error:", e)  
    return
```

- Try to connect to the server. If the connection fails, print the error message and close the connection.

### 2.7 Send Data

```python
for i in range(10):  
    message = "K230 TCP client send test {0} \r\n".format(i)  
    print("Sending:", message)  
    s.sendall(message.encode())  
    time.sleep(0.2)
```

- Send 10 test messages in a loop, using the `sendall` method to ensure each message is completely sent.

### 2.8 Close Socket

```python
s.close()  
print("Client ends connection.")
```

- Close the Socket to release resources, indicating the client has ended the connection.

### 2.9 Complete Code Example

```python
import network
import socket
import os, time

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

def client():
    network_use_wlan(True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ai = socket.getaddrinfo("192.168.1.110", 8080)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("Connecting to:", addr)
    try:
        s.connect(addr)
    except Exception as e:
        s.close()
        print("Connection error:", e)
        return

    for i in range(10):
        message = "K230 TCP client send test {0} \r\n".format(i)
        print("Sending:", message)
        s.sendall(message.encode())
        time.sleep(0.2)

    s.close()
    print("Connection closed.")

client()
```

## 3. Running Results and Operation Instructions

1. Open the NetAssist Network Debugging Assistant, configure it as a TCP server, and wait for the connection:

```{image} ../images/network/image-20240722152102440.png
:scale: 50 %
```

1. Modify the server's IP and port number in the code:

```python
ai = socket.getaddrinfo("172.16.1.174", 8080)
```

1. Run the client code, and NetAssist will display the messages sent by the client:

```{image} ../images/network/image-20240722151843380.png
:scale: 50 %
```
