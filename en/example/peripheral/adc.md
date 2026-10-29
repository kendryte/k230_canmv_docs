# ADC Usage Tutorial

## What is ADC?

**ADC (Analog-to-Digital Converter)** is a hardware module that converts **analog signals** (such as voltage) into **digital signals**.
In embedded systems, the ADC serves as a bridge between sensors and microprocessors, used to collect voltage signals and convert them into computable numerical data.

The K230 chip integrates a high-performance ADC module internally, with the following features:

- Supports **6 independent channels**
- Resolution: **12-bit** (i.e., output value range is 0\~4095)
- Sampling rate up to **1 MHz**
- Output format: raw value (`read_u16()`) or voltage (`read_uv()`, unit: microvolts)

## Example Overview

The following example demonstrates how to read the **sample value** and **voltage value** of the ADC channel through the interface provided by K230, for subsequent signal processing or sensor data acquisition.

### 1. Import module and initialize ADC

```python
from machine import ADC

# Instantiate ADC channel 0
adc = ADC(0)
```

### 2. Read raw sample value (unit: dimensionless)

```python
# Read the raw sample value of channel 0 (0 ~ 4095)
value = adc.read_u16()
print("ADC raw value:", value)
```

- Return value range: **0\~4095**
- Represents the ratio of the input voltage to the reference voltage
- Can be used for digital signal processing, threshold judgment, and other scenarios

### 3. Read voltage value (unit: microvolts)

```python
# Read the voltage value of channel 0, unit is uV
voltage = adc.read_uv()
print("ADC voltage value:", voltage, "uV")
```

- Return unit: **microvolts (μV)**
- Provides more intuitive actual voltage information, convenient for corresponding with circuit or sensor parameters
- If volts (V) are needed as the unit, divide by `1_000_000`

### 4. Example output (assuming input is 1.65V)

```text
ADC raw value: 2047
ADC voltage value: 1650000 uV
```

## Resolution and Voltage Mapping

The K230 ADC has a 12-bit resolution, and the relationship between the sampled value and the actual voltage is linear:

$$
V_{in} = \frac{\text{ADC\_Value}}{4095} \times V_{\text{ref}}
$$

⚠️ The default reference voltage is generally 3.3V, depending on the chip configuration

## Notes

| Item | Description |
| - | -- |
| **Channel Number** | Supports 6 channels (numbered 0\~5), please ensure that the pin corresponding to the connected channel has the analog input function |
| **Input Voltage Range** | The maximum input must not exceed the reference voltage (e.g., 3.3V), otherwise the chip may be damaged |
| **Unit Conversion** | `read_u16()` returns the raw sampled value; `read_uv()` returns the actual voltage (μV) |
| **Sampling Noise** | It is recommended to average multiple readings to reduce the transient jitter of ADC sampling and the impact of external interference |

## Application Scenarios

- Voltage detection (e.g., battery voltage, power status)
- Analog sensor reading (e.g., temperature, potentiometer, photoresistor)
- Sampling of analog signals such as audio and vibration
- Analog signal monitoring in feedback control systems

## Further Reading & Tool Resources

- 📘 [K230 ADC Module API Documentation](../../api/machine/k230_canmv_adc_api_manual.md)
- 📘 [K230 FPIOA Module API Manual](../../api/machine/k230_canmv_fpioa_api_manual.md)
- 📥 [K230 Pin Function Reference Table (Excel)](https://download.kendryte.com/developer/k230/HDK/K230%E7%A1%AC%E4%BB%B6%E6%96%87%E6%A1%A3/K230_PINOUT_V1.2_20240822.xlsx)
- 🛠️ [K230 IOMUX Configuration Tool](https://www.kendryte.com/zh/tools/dts_config_generation_tool)
