# `FFT` Module API Manual

## Overview

The FFT (Fast Fourier Transform) module is used to perform a Fourier transform on input time-domain data, converting it into frequency-domain data and returning the corresponding frequency magnitudes. Through FFT operations, time-domain signals can be effectively transformed into frequency-domain signals, facilitating the analysis of the signal's frequency components.

## API Introduction

The FFT module provides an `FFT` class, supporting three main functions: `run()`, `freq()`, and `amplitude()`, which are used for performing Fast Fourier Transform, frequency calculation, and amplitude calculation, respectively.

### Class `machine.FFT`

**Description**

This class is used to create an FFT object and perform the Fourier transform on the input data.

**Syntax**

```python
from machine import FFT
import array

# Define time-domain data
data = array.array('i', [1, 2, 3, 4, 5, 6, 7, 8])

# Create an FFT object, perform a 64-point FFT operation, with an offset of 0
fft1 = FFT(data, 64, 0)
```

**Parameters**

| Parameter Name | Description                                          | Type   | Input/Output |
|----------------|------------------------------------------------------|--------|--------------|
| `data`         | Input time-domain data, of type `bytearray`.         |        | Input        |
| `points`       | Number of points for the FFT operation, supports 64, 128, 256, 512, 1024, 2048, and 4096 points. |        | Input        |
| `shift`        | Data offset, default is 0.                           |        | Input        |

**Return Values**

| Return Value | Description           |
|--------------|-----------------------|
| 0            | Operation successful. |
| Non-zero     | Operation failed.     |

### `run()` Method

**Description**

This function is used to obtain the frequency-domain data after the Fourier transform.

**Syntax**

```python
res = fft1.run()
```

**Parameters**

None

**Return Values**

| Return Value | Description                                               |
|--------------|-----------------------------------------------------------|
| `res`        | Returns a `list` containing the frequency-domain data, which includes `points` tuples, each containing 2 elements: the real part and the imaginary part. |

### `freq()` Method

**Description**

This function is used to obtain the calculated frequency values.

**Syntax**

```python
res = FFT.freq(points, sample_rate)
```

**Parameters**

| Parameter Name | Description             | Input/Output |
|----------------|-------------------------|--------------|
| `points`       | Number of points involved in the FFT operation. | Input        |
| `sample_rate`  | Data sampling rate.     | Input        |

**Return Values**

| Return Value | Description                          |
|--------------|--------------------------------------|
| `res`        | Returns a list containing the frequency values for each frequency point. |

### `amplitude()` Method

**Description**

This function is used to calculate the amplitude of each frequency point. It is mainly used for testing purposes, and users can write more complex amplitude processing functions in Python.

**Syntax**

```python
amp = FFT.amplitude(FFT_res)
```

**Parameters**

| Parameter Name | Description                         | Input/Output |
|----------------|-------------------------------------|--------------|
| `FFT_res`      | The FFT calculation result returned by the `run()` function. | Input        |

**Return Values**

| Return Value | Description                          |
|--------------|--------------------------------------|
| `amp`        | Returns a list containing the amplitude of each frequency point. |
