# 1.5 `uos` – Basic Operating System Services

This module provides a subset of the functionality of CPython's operating system modules. For more details, please refer to the original CPython documentation: [os](https://docs.python.org/3.5/library/os.html#module-os).

The `uos` module includes functions for file system access and mounting, terminal redirection and duplication, as well as system information and random number generation functions such as `uname` and `urandom`.

## 1. Functions

### Basic Functions

#### 1.1 `uname`

```python
uos.uname()
```

Returns a tuple containing information about the underlying machine and its operating system. The tuple contains the following five fields, each as a string:

- `sysname` – Name of the underlying operating system.
- `nodename` – Node name (may be the same as `sysname`).
- `release` – Version number of the operating system.
- `version` – MicroPython version and build date.
- `machine` – Hardware identifier (e.g., board model, CPU type, etc.).

#### 1.2 `urandom`

```python
uos.urandom(n)
```

Generates and returns a byte object containing `n` random bytes. The random bytes are provided by the hardware random number generator if available.

#### 1.3 `cpu_usage`

```python
uos.cpu_usage()
```

Returns the current CPU usage of the system, ranging from `0` to `100`.

### File System Operations

#### 1.4 `chdir`

```python
uos.chdir(path)
```

Changes the current working directory.

#### 1.5 `getcwd`

```python
uos.getcwd()
```

Gets the path of the current working directory.

#### 1.6 `ilistdir`

```python
uos.ilistdir([dir])
```

Returns information about the entries in the specified directory (or the current directory). This function generates an iterator of tuples, each in the form `(name, type, inode [, size])`.

- `name`: Entry name, string type.
- `type`: Entry type, `0x4000` for directories, `0x8000` for regular files.
- `inode`: Inode value in the file system, `0` for file systems that do not support inodes.
- `size` (optional): File size, `-1` if it cannot be obtained.

#### 1.7 `listdir`

```python
uos.listdir([dir])
```

Lists all entries in the specified directory. If no directory is specified, lists the entries in the current directory.

#### 1.8 `mkdir`

```python
uos.mkdir(path)
```

Creates a new directory at the specified path.

#### 1.9 `remove`

```python
uos.remove(path)
```

Deletes the file at the specified path.

#### 1.10 `rmdir`

```python
uos.rmdir(path)
```

Deletes the directory at the specified path.

#### 1.11 `rename`

```python
uos.rename(old_path, new_path)
```

Renames the file or directory at the specified path.

#### 1.12 `stat`

```python
uos.stat(path)
```

Returns the status information of the file or directory at the specified path.

#### 1.13 `statvfs`

```python
uos.statvfs(path)
```

Gets the status of the file system at the specified path, returning a tuple with the following fields:

- `f_bsize` – File system block size.
- `f_frsize` – Fragment size.
- `f_blocks` – Total size of the file system in `f_frsize` units.
- `f_bfree` – Number of free blocks.
- `f_bavail` – Number of free blocks available to non-privileged users.
- `f_files` – Total number of inodes.
- `f_ffree` – Number of free inodes.
- `f_favail` – Number of free inodes available to non-privileged users.
- `f_flag` – Mount flags.
- `f_namemax` – Maximum length of filenames.

#### 1.14 `sync`

```python
uos.sync()
```

Synchronizes all file systems, writing any pending write operations to the storage device.

#### 1.15 `dupterm`

```python
uos.dupterm(stream_object, index=0)
```

Duplicates or switches the MicroPython terminal (REPL) to the specified `stream` object. The `stream_object` must implement the `readinto()` and `write()` methods. The stream should operate in non-blocking mode, with `readinto()` returning `None` when no data is available.

After calling this function, all terminal output will be duplicated to the stream object, and any input provided on the stream will be passed to the terminal. The `index` parameter should be a non-negative integer specifying the duplication slot to set.

If `stream_object` is `None`, terminal duplication is canceled for the specified slot.

Returns the stream object previously in the specified slot.

## 2. Usage Examples

**Example 1**: Implementing a block device based on the FAT file system

The following example uses a `bytearray` to simulate a block device in RAM and operates based on the FAT32 file system:

```python
class RAMBlockDev:
    def __init__(self, block_size, num_blocks):
        self.block_size = block_size
        self.data = bytearray(block_size * num_blocks)

    def readblocks(self, block_num, buf):
        for i in range(len(buf)):
            buf[i] = self.data[block_num * self.block_size + i]

    def writeblocks(self, block_num, buf):
        for i in range(len(buf)):
            self.data[block_num * self.block_size + i] = buf[i]

    def ioctl(self, op, arg):
        if op == 4:  # Get number of blocks
            return len(self.data) // self.block_size
        if op == 5:  # Get block size
            return self.block_size
```

Or:

```python
import uos

bdev = RAMBlockDev(512, 50)
uos.VfsFat.mkfs(bdev)
vfs = uos.VfsFat(bdev)
uos.mount(vfs, '/ramdisk')
```

**Example 2**: Implementing a block device based on the SPIFFS file system

The following example simulates a block device for the SPIFFS file system in RAM:

```python
class RAMFlashDev:
    def __init__(self):
        self.fs_size = 256 * 1024
        self.fs_data = bytearray(256 * 1024)
        self.erase_block = 32 * 1024
        self.log_block_size = 64 * 1024
        self.log_page_size = 4 * 1024

    def read(self, buf, size, addr):
        for i in range(len(buf)):
            buf[i] = self.fs_data[addr + i]

    def write(self, buf, size, addr):
        for i in range(len(buf)):
            self.fs_data[addr + i] = buf[i]

    def erase(self, size, addr):
        for i in range(size):
            self.fs_data[addr + i] = 0xFF
```

Mount the block device using the SPIFFS file system:

```python
blkdev = RAMFlashDev()
vfs = uos.VfsSpiffs(blkdev)
vfs.mkfs(vfs)
uos.mount(vfs, '/ramdisk')
```
