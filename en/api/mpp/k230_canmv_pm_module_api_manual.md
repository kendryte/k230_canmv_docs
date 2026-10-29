# `PM` Module API Manual

## Overview

The PM module, also known as the Power Management module, is specifically designed to optimize and manage device energy consumption. For a detailed description of the PM framework, please refer to the relevant documentation in the SDK ([K230_PM Framework User Guide.md](https://github.com/kendryte/k230_docs/blob/main/zh/01_software/board/mpp/K230_PM%E6%A1%86%E6%9E%B6%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)). In the MicroPython environment, the PM module encapsulates the power management functions of both the CPU and KPU.

## API Introduction

The PM class is located under the `mpp` module, and the module internally contains two instantiated objects: `cpu` and `kpu`, which are used to manage the power consumption of the central processing unit and the neural network processor, respectively.

### Example

The following code demonstrates how to use the PM module to get the current CPU frequency, list the supported frequency list, and set the CPU frequency:

```python
from mpp import pm

# Get the current CPU frequency
current_freq = pm.cpu.get_freq()

# Get the list of supported CPU frequencies
supported_freqs = pm.cpu.list_profiles()

# Set the CPU frequency to the specified configuration
pm.cpu.set_profile(1)
```

### get_freq

```python
pm.pm_domain.get_freq()
```

**Description**
: Gets the current frequency of the specified power domain.

**Parameters**: None

**Return Value**: Returns the current frequency value of the specified domain.

### list_profiles

```python
pm.pm_domain.list_profiles()
```

**Description**
: Gets the list of frequency configurations supported by the specified power domain.

**Parameters**: None

**Return Value**: Returns a list containing all frequency configurations supported by the domain.

### set_profile

```python
pm.pm_domain.set_profile(index)
```

**Description**
: Sets the frequency configuration index of the specified power domain.

**Parameters**:

- `index`: The frequency configuration index to be set.

**Return Value**: None

---

This API manual aims to provide developers with a clear and detailed PM module usage guide, ensuring the effective implementation and optimization of power management.
