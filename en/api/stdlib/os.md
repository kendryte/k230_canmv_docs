# `uos` – Basic Operating System Services

This module provides a subset of the functionality of the CPython `os` module. For more information, refer to the original CPython documentation: [os](https://docs.python.org/3.5/library/os.html#module-os).

The `uos` module contains functions for filesystem access and mounting, terminal redirection and copying, as well as system information and random number generation functions such as `uname` and `urandom`.

## Functions

### Basic Functions

#### `uname`

```python
uos.uname()
```

Returns a tuple containing information about the underlying machine and its operating system. The tuple contains the following five fields, each of which is a string:

- `sysname`  – The name of the underlying operating system.
- `nodename`  – The node name (may be the same as `sysname`).
- `release`  – The version number of the operating system.
- `version`  – The MicroPython version and build date.
- `machine`  – The hardware identifier (e.g., board model, CPU type, etc.).

#### `urandom`

```python
uos.urandom(n)
```

Generates and returns a bytes object containing `n` random bytes. The random bytes are provided by the hardware random number generator whenever possible.

#### `cpu_usage`

```python
uos.cpu_usage()
```

Returns the current system CPU usage, ranging from `0` to `100`.

### File System Operations

#### `chdir`

```python
uos.chdir(path)
```

Changes the current working directory.

#### `getcwd`

```python
uos.getcwd()
```

Gets the path of the current working directory.

#### `ilistdir`

```python
uos.ilistdir([dir])
```

Returns entry information for the specified directory (or the current directory). This function generates an iterator of tuples, where each tuple is of the form `(name, type, inode [, size])`.

- `name`: Entry name, string type.
- `type`: Entry type, `0x4000` for directories, `0x8000` for regular files.
- `inode`: The inode value of the file system, or `0` for file systems that do not support inodes.
- `size` (optional): File size, or `-1` if it cannot be obtained.

#### `listdir`

```python
uos.listdir([dir])
```

Lists all entries in the specified directory. If no directory is specified, lists the current directory.

#### `mkdir`

```python
uos.mkdir(path)
```

Creates a new directory at the specified path.

#### `mkfs`

```python
uos.mkfs(mount_path)
```

Formats the file system at the specified mount point. Currently only `/data` which has already been mounted is supported.

This operation will delete all directories and files in the file system. Please close any files opened on `/data` before formatting; it is recommended to restart the device after formatting is complete. This operation only rebuilds the file system metadata and does not guarantee overwriting all data in the partition, so it cannot be used for secure erasure.

Returns `None` on success. If the mount point is not mounted, the parameter is not `/data`, or the underlying formatting fails, the function will raise `OSError` (e.g., `EIO`).

```python
try:
    uos.mkfs("/data")
except OSError as e:
    print("Formatting failed:", e)
```

#### `remove`

```python
uos.remove(path)
```

Deletes the file at the specified path.

#### `rmdir`

```python
uos.rmdir(path)
```

Deletes the directory at the specified path.

#### `rename`

```python
uos.rename(old_path, new_path)
```

Renames the file or directory at the specified path.

#### `stat`

```python
uos.stat(path)
```

Returns status information for the file or directory at the specified path.

#### `statvfs`

```python
uos.statvfs(path)
```

Gets the status of the file system at the specified path, returning a tuple containing the following fields:

- `f_bsize` – File system block size.
- `f_frsize` – Fragment size.
- `f_blocks` – Total size of the file system, in units of `f_frsize`.
- `f_bfree` – Number of free blocks.
- `f_bavail` – Number of free blocks available to unprivileged users.
- `f_files` – Total number of inodes.
- `f_ffree` – Number of available inodes.
- `f_favail` – Number of inodes available to unprivileged users.
- `f_flag` – Mount flags.
- `f_namemax` – Maximum file name length.

> Currently only `f_bsize`, `f_blocks`, and `f_bfree` are valid

#### `sync`

```python
uos.sync()
```

Synchronizes all file systems, flushing pending write operations to the storage device.

#### `dupterm`

```python
uos.dupterm(stream_object, index = 0)
```

Duplicates or switches the MicroPython terminal (REPL) on the specified `stream` object. The `stream_object` must implement `readinto()` and `write()` methods. The `stream` should operate in non-blocking mode, and `readinto()` should return `None` when there is no data available to read.

After calling, all terminal output will be duplicated to this stream object, and any input provided on this stream will also be passed to the terminal. The `index` parameter should be a non-negative integer specifying the duplication slot to set.

If `stream_object` is `None`, the terminal duplication for the specified slot is canceled.

Returns the stream object previously in the specified slot.
