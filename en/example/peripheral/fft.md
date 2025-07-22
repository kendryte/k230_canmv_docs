# FFT Example

## Overview

The FFT (Fast Fourier Transform) module can perform a Fourier transform on input data and return the corresponding frequency amplitudes. Through FFT operations, time-domain signals can be converted into frequency-domain signals, which helps in analyzing the frequency components of the signal.

## Example

The following example demonstrates how to use the FFT module to perform a Fourier transform.

```python
from machine import FFT
import array
import math
from ulab import numpy as np

PI = 3.14159265358979323846264338327950288419716939937510

rx = []

def input_data():
    for i in range(64):
        data0 = 10 * math.cos(2 * PI * i / 64)
        data1 = 20 * math.cos(2 * 2 * PI * i / 64)
        data2 = 30 * math.cos(3 * 2 * PI * i / 64)
        data3 = 0.2 * math.cos(4 * 2 * PI * i / 64)
        data4 = 1000 * math.cos(5 * 2 * PI * i / 64)
        rx.append(int(data0 + data1 + data2 + data3 + data4))

input_data()  # Initialize the data to be FFT'd, in list form
print(rx)

data = np.array(rx, dtype=np.uint16)  # Convert list data to an array
print(data)

fft1 = FFT(data, 64, 0x555)  # Create an FFT object with 64 points and offset 0x555
res = fft1.run()  # Perform FFT and get the transformed data
print(res)

res = fft1.amplitude(res)  # Get the amplitude of each frequency point
print(res)

res = fft1.freq(64, 38400)  # Get the frequency values of all frequency points
print(res)
```

## Code Explanation

1. **Import Modules**:
   - Import the necessary modules, including `FFT`, `array`, `math`, and `numpy`.

1. **Input Data Function**:
   - Define the `input_data()` function to generate 64 data points, simulating cosine waves of different frequencies and storing them in the `rx` list.

1. **Data Conversion**:
   - Convert the list `rx` into a NumPy array `data`, specifying the data type as unsigned 16-bit integers.

1. **Create FFT Object**:
   - Use `FFT(data, 64, 0x555)` to create an FFT object, setting the number of points to 64 and the offset to `0x555`.

1. **Run FFT**:
   - Call `fft1.run()` to perform the Fourier transform, storing the result in `res`.

1. **Get Amplitude**:
   - Use `fft1.amplitude(res)` to get the amplitude of each frequency point and print it.

1. **Get Frequency Values**:
   - Call `fft1.freq(64, 38400)` to get the frequency values of all frequency points and print them.

```{admonition} Note
For detailed API references of the FFT module, please refer to the [API Documentation](../../api/machine/K230_CanMV_FFT_Module_API_Manual.md)
```
