# UARTPeriodicTx Hardware Periodic Transmission

`UARTPeriodicTx` uses a hardware timer to periodically send prepared UART frames. It is suited for periodic status frames, control frames, and similar transmission tasks: Python code is responsible for preparing and updating data, while the hardware timer triggers the native send path at fixed intervals.

The development board firmware path for the corresponding example in this tutorial is
`/sdcard/examples/03-Machine/uart_periodic_tx.py`, and the SDK source path is
`src/canmv/resources/examples/03-Machine/uart_periodic_tx.py`. The example sends
variable-length frames of 7 to 22 bytes at a 50 ms period, requests an immediate send on each update, and uses UART3 local loopback to verify
receive results and the latest frame send state.

## Build Configuration

This module is not compiled into the firmware by default. Execute the following before building:

```bash
# When using k230-builder
k230 make menuconfig

# When building directly on the host
make menuconfig
```

Enable `Enable UART periodic TX module` in the following menu, then rebuild and flash the firmware:

```text
CanMV Micropython Components Configurations
    Enable UART periodic TX module
```

## Wiring

The example uses UART3:

```text
IO50 (UART3_TXD) ---- IO51 (UART3_RXD)
```

Power off before completing the loopback wiring, and confirm that the board's IO50 and IO51 levels and pin multiplexing are consistent with the example. UART levels must match; do not connect 5 V UART signals; for detailed requirements see [UART Levels and Adapter Module Safety](./uart.md). You may also connect a logic analyzer to IO50 to measure the transmission period.

```{warning}
UART3, IO50, and IO51 in the example are the current example's board-level mapping. Actual applications should select UART and FPIOA pins according to the development board schematic, REPL configuration, and other peripherals already in use.
```

## How the Example Works

The example first maps IO50/IO51 to UART3 TX/RX:

```python
from machine import FPIOA, UART

fpioa = FPIOA()
fpioa.set_function(50, FPIOA.UART3_TXD)
fpioa.set_function(51, FPIOA.UART3_RXD)
```

Then it creates and starts the transmitter:

```python
from uart_periodic_tx import UARTPeriodicTx

transmitter = UARTPeriodicTx(
    UART.UART3,
    0,
    50,
    max_len=22,
    baudrate=115200,
    bits=UART.EIGHTBITS,
    parity=UART.PARITY_NONE,
    stop=UART.STOPBITS_ONE,
    repeat_last=True,
)

transmitter.update(b"\xA5\x5A\x07\x00\x00\xF8\x0D")
transmitter.start()
```

The example uses `machine.UART` only to read data looped back to UART3 RX, so that the frame contents can be checked. In business code, a running `UARTPeriodicTx` already owns the send path for the same UART; do not call `machine.UART.write()`, `init()`, or `deinit()` on it.

`repeat_last` controls the behavior when data is not updated:

- `repeat_last=True` (default): each hardware timer trigger sends the most recent frame from `update()`.
- `repeat_last=False`: each non-empty frame from `update()` is sent only once; triggers without new data do not send and are counted in `skipped`.

The example calls `update()` every `UPDATE_PERIOD_MS`. The payload length for each frame is determined by the sequence number, so consecutive calls can publish data of different lengths:

```python
sent_now = transmitter.update(
    make_frame(sequence), send_now=SEND_NOW_ON_UPDATE
)
if sent_now:
    print(transmitter.is_sent())
```

`send_now=True` means an attempt to send immediately after publishing. Returning `True` means the frame has been completely written to the UART; returning `False` means the frame is still retained, and subsequent hardware timers can retry. `is_sent()` queries whether the most recently published non-empty frame has been successfully and completely written to the UART at least once. "Written" here means the UART driver has accepted the complete frame; it does not mean line transmission has finished, nor does it mean the receiver has acknowledged it.

The example frame format is as follows:

```text
A5 5A <total_length> <sequence> <payload...> <checksum> 0D
```

The payload length is between 1 and 16 bytes, so `total_length` is between 7 and 22. To verify the loopback data, the example defines the `n`-th payload byte as `(sequence + n) & 0xFF`, where `n` starts from 0; `valid_frame()` validates against this test pattern. Real applications may use any payload format, but the corresponding validation logic must be modified accordingly. The checksum byte is the XOR of all bytes preceding it. For example, when the sequence is `0x00`, the frame content is:

```text
A5 5A 07 00 00 F8 0D
```

When `repeat_last=True`, the hardware timer repeatedly sends the most recently successfully published frame, and does not generate sequence numbers on its own. The default example also sets `send_now=True`, so each update typically produces one immediate send, while the timer continues to send once every 50 ms, yielding a total of about 200 sends in 5 seconds. When an immediate send and a timer trigger occur very close together, the receive interval between the two frames may be very short; this is the expected result of the two send paths working together.

If business logic requires new data to be sent immediately, but each version of the data to be sent only once, set `repeat_last=False` and keep `send_now=True`. If the immediate send fails, the next timer trigger will still attempt to send that frame.

## Running and Results

Copy the example to the device and run `uart_periodic_tx.py`. The default configuration is:

| Item | Value |
| --- | --- |
| UART | UART3 |
| Baud rate | 115200, 8N1 |
| Hardware timer | 0 |
| Send period | 50 ms |
| Update period | 50 ms |
| Test duration | 5000 ms |
| Frame length | 7 to 22 bytes |
| Repeat latest frame | `True` |
| Immediate send on update | `True` |

The output gives send, receive, and error statistics, for example:

```text
UARTPeriodicTx loopback test: period=50 ms, duration=5000 ms, repeat_last=True, send_now=True
frames: sent=199, received=198, invalid=0
frame length: min=7, max=22
immediate: submitted=99, requested=99, state_errors=0
latest packet submitted=True
tx stats: short_write=0, errors=0, skipped=0, last_error=0
rx interval us: avg=24876, min=8, max=50172
PASS
```

The 199 sends in the output include 99 immediate sends and about 100 timer-triggered sends. When the test loop ends, the last frame may still be in the UART receive buffer, so having one fewer received than sent can still pass the test. `state_errors=0` means that after every successful immediate-send return, `is_sent()` confirmed the latest frame state; `min=7, max=22` indicates the variable-length frame path was exercised; `last_error=0` means no UART write error that returns a negative value has occurred.

The receive timestamp is used only for software loopback sanity checks. `send_now` and timer-triggered sends may cause two frames to be adjacent, so a very small minimum interval does not indicate hardware timer period jitter. To measure true on-wire period and jitter, use a logic analyzer on IO50 and decode at `115200`, 8 data bits, no parity, 1 stop bit.

## Frequently Asked Questions

| Symptom | Troubleshooting |
| --- | --- |
| `ImportError: no module named 'uart_periodic_tx'` | Enable `Enable UART periodic TX module` in `menuconfig` and rebuild the firmware. |
| `OSError: [Errno 16] EBUSY` | Check whether `timer_id` is already in use by `machine.Timer` or another `UARTPeriodicTx`; multiple periodic transmitters for the same UART must also use the same configuration. |
| `RuntimeError: transmitter is not running` | `update(..., send_now=True)` can only be used after `start()` is called; initial data before startup should be published with the default `send_now=False`. |
| The logic analyzer always shows the same sequence number | Confirm that the capture duration covers multiple `UPDATE_PERIOD_MS`, and check whether the application continuously calls `update()`. The timer repeating the last frame between updates is expected behavior. |
| The send count is close to twice the number of timer triggers | Both `repeat_last=True` and `send_now=True` are enabled; each update triggers an immediate send, and the timer still repeats the most recent frame. Set `repeat_last=False` when each frame should be sent only once. |
| No loopback data received, or `FAIL` is shown | Check the IO50 to IO51 connection, FPIOA mapping, whether UART3 is occupied by other functions, and whether both ends use 115200 8N1. |
| `short_write` or `errors` is non-zero | Reduce frame length or increase baud rate, lengthen the send period, and ensure no multiple overlapping send tasks are assigned to one UART. When `errors` is non-zero, call `last_error()` to get the `errno` of the most recent write failure. |
| `skipped` is non-zero | In `repeat_last=False` mode, timer triggers without an update are counted in `skipped`; immediate sends that are not executed because the UART is busy are also counted. For other situations, check UART busy, timer resources, and frame length. |

Release resources when finished:

```python
try:
    transmitter.start()
    # In business code, call transmitter.update(...) as needed
finally:
    transmitter.deinit()
```

For more API parameters and resource constraints, see the [`uart_periodic_tx` Module API Manual](../../api/machine/k230_canmv_uart_periodic_tx_api_manual.md).
