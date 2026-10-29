# TCP Client Example Explanation

## Example Location

- Development board firmware path: `/sdcard/examples/14-Socket/tcp_client.py`
- SDK source code path: `src/canmv/resources/examples/14-Socket/tcp_client.py`

This example uses the development board as a TCP client, connects to a TCP service on the computer, and continuously sends 10 test
messages.

## Preparation Before Running

First, start a TCP debugging tool on the computer and listen on a port. Then modify the two types of configurations in the script:

```python
NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

```python
ai = socket.getaddrinfo("192.168.1.110", 8080)
```

Change `192.168.1.110` to the computer's IP address, and change `8080` to the TCP port that the debugging tool is listening on. The computer and the development board must be on the same network, and the computer's firewall must also allow inbound traffic on that port.

## Code Flow

### 1. Connect to the Network

```python
netif, _ = connect_network(
    NETWORK_TYPE,
    ssid=WIFI_SSID,
    password=WIFI_PASSWORD,
    wlan_device=WLAN_DEVICE,
    timeout=NETWORK_TIMEOUT,
)
```

The common network library is responsible for selecting the network interface, waiting for an IP address, and setting the default uplink, so applications do not need to hardcode the netdev name.

### 2. Create the TCP Socket and Resolve the Address

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
addr = socket.getaddrinfo("192.168.1.110", 8080)[0][-1]
```

`AF_INET` selects IPv4, and `SOCK_STREAM` selects a connection-oriented, reliable, and ordered TCP byte stream. `getaddrinfo()` works for both IPv4 strings and domain names.

### 3. Connect to the Server

```python
s.connect(addr)
```

TCP must complete the connection before data can be sent. A "connection refused" usually means the destination address is reachable, but no service is listening on the corresponding port; a "connection timeout" is typically related to the address, routing, or firewall.

### 4. Continuously Send Messages

```python
for i in range(10):
    message = "K230 tcp client send test {0} \r\n".format(i)
    s.write(message)
    time.sleep(0.2)
```

The example sends a message with a sequence number every `0.2` seconds. TCP is a byte stream and does not preserve message boundaries from individual `write()` calls; the example uses `\r\n` so the receiving end can conveniently display or split the data by line.

### 5. Close the Connection

After sending is complete, the script waits for 1 second, then calls `s.close()` to release the connection and prints `end`.

## Running and Verification

1. First, start the computer-side TCP service and confirm the listening address and port.
2. Run the script under the development board firmware path in CanMV IDE.
3. The computer side should receive 10 messages with sequence numbers `0` to `9`.
4. If the computer has multiple network cards, the target IP should be the one that communicates with the development board, not the loopback address.
