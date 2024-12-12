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

> only `f_bsize`, `f_blocks` and `f_bfree` valid.

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
