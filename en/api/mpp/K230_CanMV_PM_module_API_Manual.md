# 3.10 PM Module API Manual

## 1. Overview

The PM module, also known as the Power Management module, is specifically designed to optimize and manage the power consumption of devices. For a detailed description of the PM framework, please refer to the relevant documentation in the SDK ([K230_PM Framework Usage Guide.md](https://github.com/kendryte/k230_docs/blob/main/zh/01_software/board/mpp/K230_PM%E6%A1%86%E6%9E%B6%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)). In the MicroPython environment, the PM module encapsulates power management functions for both the CPU and KPU.

## 2. API Introduction

The PM class is located under the `mpp` module, which contains two instantiated objects: `cpu` and `kpu`, used for managing the power consumption of the central processing unit and the neural network processor, respectively.

### 2.1 Example

The following code demonstrates how to use the PM module to get the current CPU frequency, list the supported frequency profiles, and set the CPU frequency:

```python
from mpp import pm

# Get the current CPU frequency
current_freq = pm.cpu.get_freq()

# Get the list of supported CPU frequency profiles
supported_freqs = pm.cpu.list_profiles()

# Set the CPU frequency to a specified profile
pm.cpu.set_profile(1)
```

### 2.2 get_freq

```python
pm.pm_domain.get_freq()
```

**Description**: Gets the current frequency of the specified power domain.

**Parameters**: None

**Return Value**: Returns the current frequency value of the specified domain.

### 2.3 list_profiles

```python
pm.pm_domain.list_profiles()
```

**Description**: Gets the list of supported frequency profiles for the specified power domain.

**Parameters**: None

**Return Value**: Returns a list containing all the supported frequency profiles of the domain.

### 2.4 set_profile

```python
pm.pm_domain.set_profile(index)
```

**Description**: Sets the frequency profile index for the specified power domain.

**Parameters**:

- `index`: The frequency profile index to be set.

**Return Value**: None

---

This API manual aims to provide developers with a clear and detailed guide to using the PM module, ensuring effective implementation and optimization of power management.
