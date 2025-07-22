# Explanation of Using Wired Network Routine

## Environment Preparation

First, ensure that your CanMV development board is correctly connected to the router or switch so that the development board can access the network. Also, make sure that the router or switch is working properly to allow the development board to communicate normally.

## Analysis of Routine Content

The following Python routine will help you understand how to configure and use the network LAN interface on the CanMV development board.

### Import Modules

```python
import network
```

This line of code imports the `network` module, which is a library used to manage network interfaces.

### Main Function Definition

```python
def main():   
    # All subsequent network operations will be placed in this function
```

### Get the LAN Interface

```python
a = network.LAN()
```

This line of code creates an instance of the LAN interface and assigns it to the variable `a`. Through this instance, we can perform various operations on the LAN interface.

### Check Network Interface Status

```python
# Check if the network interface is active
print(a.active())  
```

Here, we first check if the network interface is activated (i.e., in use).

### View and Set Network Configuration

```python
# View the network interface IP, mask, gateway, DNS configuration
print(a.ifconfig())   
# Set the network interface IP, mask, gateway, DNS configuration
print(a.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8')))   
# View again to confirm the settings are successful
print(a.ifconfig())
```

This code first prints out the current network configuration (IP address, subnet mask, gateway, and DNS server), then sets a new network configuration, and prints it again to confirm the settings are successful.

### Use DHCP for Automatic Configuration

```python
# Set the network interface to DHCP mode
print(a.ifconfig("dhcp"))   
# View the automatically obtained network configuration
print(a.ifconfig())
```

In some cases, we may want the network configuration to be automatically obtained. In this case, we can use DHCP mode. By setting the parameter of the `ifconfig()` method to `"dhcp"`, we can let the development board automatically obtain IP address and other configuration information from the DHCP server.

### View MAC Address

```python
# View the network interface MAC address
print(a.config("mac"))  
```

The MAC address is the unique identifier of the network interface. You can get the MAC address through `config("mac")`.

### Full Execution

Finally, by calling the `main()` function, all the above operations will be executed.

```python
main()
```

This routine demonstrates how to perform basic network configuration and operations on the CanMV development board, including checking the network interface status, viewing and setting network configuration, using DHCP for automatic configuration, and viewing and setting the MAC address. Through these operations, you can better understand and control the behavior of your development board in the network.

### Complete Routine

```python
import network

def main():
    # Get the LAN interface
    a = network.LAN()
    # Check if the network interface is active
    print(a.active())
    # View the network interface IP, mask, gateway, DNS configuration
    print(a.ifconfig())
    # Set the network interface IP, mask, gateway, DNS configuration
    print(a.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8')))
    # View the network interface IP, mask, gateway, DNS configuration
    print(a.ifconfig())
    # Set the network interface to DHCP mode
    print(a.ifconfig("dhcp"))
    # View the network interface IP, mask, gateway, DNS configuration
    print(a.ifconfig())
    # View the network interface MAC address
    print(a.config("mac"))
    # Set the network interface to DHCP mode
    print(a.ifconfig("dhcp"))
    # View the network interface IP, mask, gateway, DNS configuration
    print(a.ifconfig())

main()
```

For specific interface definitions, please refer to [network](../../api/extmod/K230_CanMV_network_API_Manual.md).
