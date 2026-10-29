# `FFT` Module API Manual

## Overview

The FFT (Fast Fourier Transform) module is used to perform Fourier transform on input time-domain data, converting it into frequency-domain data and returning the corresponding frequency amplitudes. Through FFT computation, time-domain signals can be effectively converted into frequency-domain signals, facilitating the analysis of signal frequency components.

## API Introduction

The FFT module provides an `FFT` class that supports three main functions: `run()`, `freq()`, and `amplitude()`, used for fast Fourier transform, frequency calculation, and amplitude calculation respectively.

### Class `machine.FFT`

**Description**

This class is used to create FFT objects and perform Fourier transform on input data.

**Syntax**

```python
from machine import FFT
import array

# Define time-domain data
data = array.array('i', [1, 2, 3, 4, 5, 6, 7, 8])

# Create an FFT object, perform 64-point FFT computation, offset is 0
fft1 = FFT(data, 64, 0)
```

**Parameters**

| Parameter Name | Description                                              | Type | Input/Output |
|----------------|----------------------------------------------------------|------|--------------|
| `data`         | Input time-domain data, `bytearray` type.                |      | Input        |
| `points`       | Number of points for FFT computation, supports 64, 128, 256, 512, 1024, 2048, and 4096 points. |      | Input        |
| `shift`        | Data offset, default is 0.                               |      | Input        |

**Return Value**

| Return Value | Description          |
|--------------|----------------------|
| 0            | Operation successful.|
| Non-0        | Operation failed.    |

### `run()` Method

**Description**

This function is used to obtain the frequency-domain data after Fourier transform.

**Syntax**

```python
res = FFT.run()
```

**Parameters**

None

**Return Value**

| Return Value | Description                                                  |
|--------------|--------------------------------------------------------------|
| `res`        | Returns a `list` containing frequency-domain data, which contains `points` tuples, each containing 2 elements: real part and imaginary part. |

### `freq()` Method

**Description**

This function is used to obtain the calculated frequency values.

**Syntax**

```python
res = FFT.freq(points, sample_rate)
```

**Parameters**

| Parameter Name | Description                                         | Input/Output |
|----------------|-----------------------------------------------------|--------------|
| `points`       | Number of points participating in FFT computation.  | Input        |
| `sample_rate`  | Data sampling rate.                                 | Input        |

**Return Value**

| Return Value | Description                                                  |
|--------------|--------------------------------------------------------------|
| `res`        | Returns a list containing the frequency values of each frequency point after computation. |

### `amplitude()` Method

**Description**

This function is used to calculate the amplitude of each frequency point, mainly for testing purposes. Users can write more complex amplitude processing functions in Python on their own.

**Syntax**

```python
amp = FFT.amplitude(FFT_res)
```

**Parameters**

| Parameter Name | Description                                       | Input/Output |
|----------------|---------------------------------------------------|--------------|
| `FFT_res`      | FFT computation result returned by the `run()` function. | Input        |

**Return Value**

| Return Value | Description                                                |
|--------------|------------------------------------------------------------|
| `amp`        | Returns a list containing the amplitudes of each frequency point. |
