# `uart_periodic_tx` Module API Manual

## Overview

`uart_periodic_tx` is an optional native module that periodically sends prepared complete UART frames using a hardware timer, and can also request an immediate send when a new frame is published. The timer callback only performs native UART write operations, does not execute Python code, and does not allocate GC memory in the callback.

It is suitable for scenarios requiring stable periodic transmission of data frames of varying lengths, such as sending a status frame every 50 ms. The application calls `update()` in a normal Python context to publish the next frame; each publication can have a different data length, but must not exceed the `max_len` set at construction time.

```{note}
This module is a UART periodic transmitter, not a general-purpose hardware timer task framework. It cannot schedule arbitrary Python functions in the timer, nor can it be used directly for network, SPI, or I2C transmission. Three internal buffers are used to prevent updates and sends from overwriting each other; they do not form a FIFO queue. The module only guarantees sending the most recently published data; rapidly calling `update()` in succession may cause unsent old data to be replaced by new data.
```

## Enabling the Module

This feature is disabled by default. Before compiling the firmware, execute the configuration command corresponding to your build environment in the source root directory:

```bash
# When using k230-builder
k230 make menuconfig

# When compiling directly on the host
make menuconfig
```

Enable the following option and recompile the firmware:

```text
CanMV Micropython Components Configurations
    Enable UART periodic TX module
```

Importing the module in firmware where this option is not enabled will raise an `ImportError`.

## Importing the Module

```python
from machine import FPIOA, UART
from uart_periodic_tx import UARTPeriodicTx
```

## Quick Start

The following example maps UART3's TX to IO50 and sends one frame every 50 ms. Choose UART and pins not occupied by REPL or other system functions based on the development board and board-level configuration.

```python
from machine import FPIOA, UART
from uart_periodic_tx import UARTPeriodicTx
import time

fpioa = FPIOA()
fpioa.set_function(50, FPIOA.UART3_TXD)

tx = UARTPeriodicTx(
    UART.UART3,
    0,
    50,
    max_len=64,
    baudrate=115200,
    bits=UART.EIGHTBITS,
    parity=UART.PARITY_NONE,
    stop=UART.STOPBITS_ONE,
    repeat_last=True,
)

try:
    tx.update(b"\x01\x02\x03")
    tx.start()

    time.sleep_ms(1000)
    sent_now = tx.update(b"\x10\x20\x30\x40\x50", send_now=True)
    print("immediate submitted:", sent_now)
    print("latest packet submitted:", tx.is_sent())
    time.sleep_ms(1000)
finally:
    tx.deinit()
```

The FPIOA UART TX pin mapping must be completed before calling `start()`. In the example above, the two published frames have lengths of 3 bytes and 5 bytes respectively. `update()` copies the passed-in buffer, so modifying the original `bytearray` after the call returns will not modify the published frame.

## `UARTPeriodicTx` Class

### Constructor

```python
UARTPeriodicTx(
    uart_id,
    timer_id,
    period=50,
    *,
    max_len=64,
    baudrate=115200,
    bits=UART.EIGHTBITS,
    parity=UART.PARITY_NONE,
    stop=UART.STOPBITS_ONE,
    repeat_last=True,
)
```

Creates a periodic transmitter. The constructor allocates three sets of send buffers, but does not occupy a UART or hardware timer until `start()` is called.

| Parameter | Description |
| --- | --- |
| `uart_id` | UART hardware number, e.g., `UART.UART3`. A number is passed in, not a `machine.UART` object. The UART must be available and the TX pin must be correctly multiplexed. |
| `timer_id` | Hardware timer number. Software timer number `-1` cannot be used. The current K230 timer numbers are `0` to `5`. |
| `period` | Send period in ms, default `50`, minimum value `1`. |
| `max_len` | Maximum length of a single frame, default `64`, range `1` to `4096` bytes. The module allocates three sets of buffers for this capacity. |
| `baudrate` | UART baud rate, default `115200`. |
| `bits` | Data bits, using the same constants as `machine.UART`, e.g., `UART.EIGHTBITS`. Supports 5 to 9 bits. |
| `parity` | Parity mode, e.g., `UART.PARITY_NONE`, `UART.PARITY_ODD`, or `UART.PARITY_EVEN`. |
| `stop` | Stop bits, e.g., `UART.STOPBITS_ONE` or `UART.STOPBITS_TWO`. |
| `repeat_last` | Whether to repeat sending the last frame when there is no new `update()`, default `True`. When set to `False`, each non-empty frame successfully published via `update()` is sent only once after being completely written to UART; subsequent timer triggers will be skipped until a new `update()` occurs. |

`period` can be passed as the third positional argument; the remaining UART configuration parameters must be passed as keyword arguments.

### `update` Method

```python
tx.update(data, send_now=False)
```

Copies and publishes a complete frame of data. By default, it is sent by the hardware timer on subsequent triggers; when `send_now=True` is set, an immediate send of the frame will also be attempted after publication.

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| `data` | Buffer object | e.g., `bytes`, `bytearray`, or `memoryview`. Each call can use a different length, which must not exceed `max_len`. Empty data can be published but will not be sent. |
| `send_now` | `bool` | Keyword-only parameter, indicates whether to attempt an immediate send after publication, default `False`. When set to `True`, the transmitter must have already been started via `start()`. |

**Return Value: `bool`**

- When `send_now=False`, returns `False`, indicating no immediate send was performed; this return value does not indicate that subsequent timers will not send this frame.
- When `send_now=True`, returns `True` if the frame published in this call has been completely written to UART. Returns `False` if the UART is busy, a short write occurred, or a write error occurred; the data remains as the most recently published frame, and subsequent timers can retry sending it.

**Exceptions**

- `ValueError`: The object has been released, or the data length exceeds `max_len`.
- `RuntimeError`: `send_now=True` was set, but the transmitter has not been started or has already been stopped.
- `OSError(EBUSY)`: All three buffers are temporarily unwritable. You can retry later in a normal Python context; do not call this method in a `machine.Timer` callback.

`update()` does not wait for the UART to complete sending on the line, nor does it guarantee that the new frame will appear at the next hardware trigger. If the send path has already taken the current buffer, the new frame will take effect on subsequent triggers. When `repeat_last=True`, the timer continuously sends the most recently successfully published complete frame; when `repeat_last=False`, the frame is sent once after being completely written, then waits for the next `update()`.

When `repeat_last=True` and `send_now=True` are used simultaneously, the new frame is sent immediately, and the timer will still repeat the most recent frame on each periodic trigger. To send each update only once and have the timer retry if the immediate send fails, use `repeat_last=False`.

### `start` Method

```python
tx.start()
```

Requests the hardware timer and UART, and begins periodic sending. At least one successful `update()` call should be made before calling this, otherwise timer triggers will be counted as skipped sends.

The same `timer_id` cannot be used simultaneously by `machine.Timer` or another `UARTPeriodicTx`. Resource conflicts will raise `OSError(EBUSY)`.

### `stop` Method

```python
tx.stop()
```

Stops periodic sending and releases the runtime resources of the hardware timer and UART, but retains the object and the allocated send buffers. `start()` can be called again afterward.

### `deinit` Method

```python
tx.deinit()
```

Stops sending and releases all native resources and buffers. The object cannot be used again after this call. It is recommended to call this in a `try` / `finally` block to ensure hardware timers are released even on exception paths.

### `active` Method

```python
tx.active()
```

Returns a boolean value indicating whether the hardware timer is running.

### `is_sent` Method

```python
tx.is_sent()
```

Returns whether the most recently published non-empty frame has been successfully and completely written to UART at least once:

- Returns `False` after object creation and before the first successful send.
- Returns `False` after each new frame is published but not yet sent.
- Returns `True` after an immediate send or a timer send completes a full write.
- Returns `False` after publishing empty data.

This status corresponds to the UART driver's `write()` having accepted the complete frame; it does not indicate that the last bit has left the transmit pin, nor that the receiver has received or acknowledged it. Calling this method again after `deinit()` raises `ValueError`.

### `last_error` Method

```python
tx.last_error()
```

**Return Value: `int`**

Returns the `errno` saved when the most recent UART `write()` returned a negative value. Returns `0` if no write error has occurred yet; subsequent successful writes do not clear the already recorded error code. Short writes are not negative errors and will not update this error code; check the `short_write` count returned by `stats()`.

Printing logs or raising Python exceptions in a hardware timer callback is not safe, so the module records the error code atomically and allows normal Python code to query it via this method.

### `stats` Method

```python
sent, short_write, errors, skipped = tx.stats()
```

Returns a cumulative statistics tuple:

| Return Value | Description |
| --- | --- |
| `sent` | Number of times the UART write returned the complete frame length, including timed sends, immediate sends, and repeated sends when `repeat_last=True`. |
| `short_write` | Number of times the UART wrote a partial frame. |
| `errors` | Number of times the UART write returned a negative value. Call `last_error()` to query the `errno` of the most recent error. |
| `skipped` | Number of send attempts that did not perform a UART write, e.g., UART was busy, no sendable frame has been published yet, or when `repeat_last=False` there is no new data. This value also counts skipped timer triggers and immediate send attempts that were not executed due to UART busy. |

Statistics are cumulative over the object's lifetime; `stop()` and subsequent `start()` do not reset them.

## Resources and Timing Constraints

- `UARTPeriodicTx` holds the native UART driver used for transmission. During operation, do not send data through the same UART using `machine.UART.write()`, nor reconfigure or release the same UART.
- Multiple `UARTPeriodicTx` instances may share the same UART, but the UART configuration must be exactly identical. When two transmission moments overlap, one of the triggers will be skipped and counted into `skipped`. When predictable timing is required, only one periodic transmitter should be created for a given UART.
- Timer triggers are driven by a hardware timer, avoiding the send-trigger latency caused by the Python VM, GC, and Python callbacks; the actual time to complete a frame on the wire is still affected by baud rate, frame length, and UART driver state.
- The serial transmission time of a frame should be significantly shorter than `period`. If the frame is too long, the baud rate is too low, or the UART is busy, `short_write`, `errors`, or `skipped` may occur.
- When `repeat_last=True`, the logic analyzer will see the most recently and successfully `update()`-ed frame being transmitted continuously. When `repeat_last=False`, each successful `update()` produces at most one complete frame transmission; triggers without new data are counted into `skipped`.
- `send_now=True` only initiates a single immediate write attempt and does not pause or re-align the hardware timer. When the immediate send time is close to a timer trigger, two frames may appear consecutively on the wire.

A complete loopback verification example is available at [UARTPeriodicTx Hardware Periodic Transmission](../../example/peripheral/uart_periodic_tx.md).
