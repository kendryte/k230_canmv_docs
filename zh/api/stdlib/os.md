# 1.5 `uos` – 基本操作系统服务

该模块提供了部分 CPython 操作系统模块的功能子集。有关详细信息，请参阅原始 CPython 文档：[os](https://docs.python.org/3.5/library/os.html#module-os)。

`uos` 模块包含用于文件系统的访问与挂载、终端重定向与复制，以及诸如 `uname` 和 `urandom` 等系统信息和随机数生成函数。

## 1. 函数

### 基础功能

#### 1.1 `uname`

```python
uos.uname()
```

返回一个包含有关底层机器及其操作系统信息的元组。该元组包含以下五个字段，每个字段均为字符串：

- `sysname`  – 底层操作系统名称。
- `nodename`  – 节点名称（可能与 `sysname` 相同）。
- `release`  – 操作系统的版本号。
- `version`  – MicroPython 版本及构建日期。
- `machine`  – 硬件标识符（如主板型号、CPU 类型等）。

#### 1.2 `urandom`

```python
uos.urandom(n)
```

生成并返回包含 `n` 个随机字节的字节对象。随机字节尽可能由硬件随机数生成器提供。

#### 1.3 `cpu_usage`

```python
uos.cpu_usage()
```

返回当前系统 CPU 的使用率，范围为 `0` 到 `100`。

### 文件系统操作

#### 1.4 `chdir`

```python
uos.chdir(path)
```

更改当前工作目录。

#### 1.5 `getcwd`

```python
uos.getcwd()
```

获取当前工作目录的路径。

#### 1.6 `ilistdir`

```python
uos.ilistdir([dir])
```

返回指定目录（或当前目录）的条目信息。该函数生成一个元组迭代器，其中每个元组的形式为 `(name, type, inode [, size])`。

- `name`：条目名称，字符串类型。
- `type`：条目类型，目录为 `0x4000`，普通文件为 `0x8000`。
- `inode`：文件系统的 inode 值，对于不支持 inode 的文件系统则为 `0`。
- `size`（可选）：文件大小，若无法获取则为 `-1`。

#### 1.7 `listdir`

```python
uos.listdir([dir])
```

列出指定目录中的所有条目。如果未指定目录，则列出当前目录。

#### 1.8 `mkdir`

```python
uos.mkdir(path)
```

在指定路径创建一个新目录。

#### 1.9 `remove`

```python
uos.remove(path)
```

删除指定路径的文件。

#### 1.10 `rmdir`

```python
uos.rmdir(path)
```

删除指定路径的目录。

#### 1.11 `rename`

```python
uos.rename(old_path, new_path)
```

重命名指定路径的文件或目录。

#### 1.12 `stat`

```python
uos.stat(path)
```

返回指定路径的文件或目录的状态信息。

#### 1.13 `statvfs`

```python
uos.statvfs(path)
```

获取指定路径文件系统的状态，返回一个元组，包含以下字段：

- `f_bsize` – 文件系统块大小。
- `f_frsize` – 片段大小。
- `f_blocks` – 文件系统总大小，以 `f_frsize` 为单位。
- `f_bfree` – 空闲块数。
- `f_bavail` – 非特权用户可用的空闲块数。
- `f_files` – inode 总数。
- `f_ffree` – 可用 inode 数量。
- `f_favail` – 非特权用户可用的 inode 数量。
- `f_flag` – 挂载标志。
- `f_namemax` – 最大文件名长度。

> 目前仅 `f_bsize`， `f_blocks` 和 `f_bfree` 有效

#### 1.14 `sync`

```python
uos.sync()
```

同步所有文件系统，将挂起的写操作写入存储设备。

#### 1.15 `dupterm`

```python
uos.dupterm(stream_object, index = 0)
```

在指定的 `stream` 对象上复制或切换 MicroPython 终端（REPL）。`stream_object` 必须实现 `readinto()` 和 `write()` 方法。`stream` 应以非阻塞模式运行，`readinto()` 在没有可读数据时应返回 `None`。

调用后，所有终端输出将被复制到该流对象，同时该流上提供的任何输入也将被传递到终端。`index` 参数应为非负整数，指定要设置的复制槽。

如果 `stream_object` 为 `None`，则取消指定槽的终端复制。

返回先前在指定槽中的流对象。
