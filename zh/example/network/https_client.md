# HTTPS Client 例程讲解

## 例程位置

底层 Socket 与 TLS 版本：

- 开发板固件路径：`/sdcard/examples/14-Socket/https_client.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/https_client.py`

`requests` 高层接口版本：

- 开发板固件路径：`/sdcard/examples/14-Socket/https_client2.py`
- SDK 源码路径：`src/canmv/resources/examples/14-Socket/https_client2.py`

两个例程都访问 `https://www.baidu.com`，用于对比手动建立 TLS 连接和使用高层 HTTP
客户端库的差异。

## 运行前准备

两个脚本使用相同的公共网络配置。修改 Wi-Fi 凭据，或将 `NETWORK_TYPE` 改为
`"lan"`、`"default"`：

```python
NETWORK_TYPE = "wifi_sta"
WLAN_DEVICE = "auto"
WIFI_SSID = "TEST"
WIFI_PASSWORD = "12345678"
NETWORK_TIMEOUT = 20
```

开发板必须能够访问互联网并解析 DNS。实际应用若在 TLS 配置中启用证书有效期
校验，还应先确保设备时间正确。

## 底层 TLS 版本

### 1. 解析并连接 HTTPS 端口

```python
addr = usocket.getaddrinfo("www.baidu.com", 443)[0][-1]
sock = usocket.socket()
sock.connect(addr)
```

HTTPS 默认使用 TCP `443` 端口。此时只完成了 TCP 连接，尚未建立加密通道。

### 2. 包装 TLS Socket

```python
ssl_sock = ussl.wrap_socket(sock, server_hostname="www.baidu.com")
```

`server_hostname` 会在 TLS 握手中提供 SNI。多个网站共享同一 IP 时，服务器依靠
SNI 选择对应证书和站点。

### 3. 发送 HTTP 请求并循环读取

```python
ssl_sock.write(
    b"GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: close\r\n\r\n"
)

while True:
    data = ssl_sock.read()
    if not data:
        break
    print(data.decode(), end="")
```

请求使用 `Connection: close`，服务器关闭连接时读取循环结束。最后调用
`ssl_sock.close()` 释放 TLS 和 TCP 资源。

## requests 高层版本

```python
response = requests.get("https://www.baidu.com")
print(response.text)
response.close()
```

`requests.get()` 内部完成 DNS、TCP、TLS 和 HTTP 处理，适合普通业务请求。读取完
响应后仍应显式调用 `response.close()`，及时释放 Socket 和内存。

## 运行与排查

1. 初次学习时先运行 `https_client2.py`，确认联网和 HTTPS 基础环境正常。
2. 再运行 `https_client.py`，观察原始 HTTP 状态行、响应头和正文。
3. DNS 错误应检查网络、网关和 DNS；连接超时应检查默认上行和防火墙。
4. TLS 握手失败时检查系统时间、目标域名、SNI 以及固件支持的 TLS 算法。
