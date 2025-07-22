# Version Description

## Version Information

| Product       | Version | Release Date |
|---------------|---------|--------------|
| K230 CanMV    | V0.2.0  | 2023-11-23   |
| K230 CanMV    | V0.3.0  | 2023-12-28   |
| K230 CanMV    | V0.4.0  | 2024-01-26   |
| K230 CanMV    | V0.5.0  | 2024-03-15   |
| K230 CanMV    | V0.6.0  | 2024-04-30   |
| K230 CanMV    | V0.7.0  | 2024-07-05   |
| K230 CanMV    | V1.0.0  | 2024-08-02   |
| K230 CanMV    | V1.1.0  | 2024-09-14   |

## Supported Hardware

The K230 platform supports CanMV-K230 and other mainboards.

## Version Usage Restrictions

None

## Relationship Between CanMV, SDK, and nncase Versions

When developing AI, the corresponding versions of k230_sdk and nncase are as follows. Please pay attention to the version correspondence when compiling images and using nncase to convert kmodels.

| CanMV (micropython) Version | K230 SDK Version | nncase Version | Notes |
|-----------------------------|------------------|----------------|-------|
| 0.2.0                       | 1.1.0            | 2.4.0          | -     |
| 0.3.0                       | 1.1.0            | 2.4.0          | -     |
| 0.4.0                       | 1.3.0            | 2.7.0          | -     |
| 0.5.0                       | 1.4.0            | 2.8.0          | -     |
| 0.6.0                       | 1.5.0            | 2.8.1          | -     |
| 0.7.0                       | 1.6.0            | 2.8.3          | -     |
| 1.0.0                       | 1.6.0            | 2.8.3          | -     |
| 1.1.0                       | -                | 2.9.0          | -     |

## Version Functionality Statistics

### Basic Functions

| ID  | Supported Version | Function Summary | Function Description                | Notes |
|-----|-------------------|------------------|-------------------------------------|-------|
| 1   | V0.2.0            | Camera           | Supports capturing sensor images    |       |
| 2   | V0.2.0            | Display          | Supports HDMI display               |       |
| 3   | V0.2.0            | Encryption Module| Supports hardware SHA256, AES       |       |
| 4   | V0.2.0            | VPU              | Supports encoding and decoding      |       |
| 5   | V0.2.0            | Audio            | Supports audio, built-in codec      |       |
| 6   | V0.2.0            | GPIO             | Supports GPIO                       |       |
| 7   | V0.2.0            | ADC              | Supports analog-to-digital conversion|      |
| 8   | V0.2.0            | FFT              | Supports Fourier transform          |       |
| 9   | V0.2.0            | I2C              | Supports I2C communication          |       |
| 10  | V0.2.0            | PWM              | Supports PWM output                 |       |
| 11  | V0.2.0            | SPI              | Supports SPI communication          |       |
| 12  | V0.2.0            | Timer            | Supports timers                     |       |
| 13  | V0.2.0            | WDT              | Supports watchdog timer             |       |
| 14  | V0.3.0            | OMV              | Supports OpenMV related algorithms  |       |
| 15  | V0.3.0            | Network          | Supports wired network              |       |
| 16  | V0.3.0            | Stability        | Enhances micropython stability      |       |
| 17  | V0.3.0            | IDE Display      | IDE can display images in real-time |       |
| 18  | V0.4.0            | SDK and nncase Upgrade | Upgrades SDK to V1.3, nncase to V2.7 |  |
| 19  | V0.4.0            | LVGL             | Supports LVGL                       |       |
| 20  | V0.4.0            | WiFi             | Supports WiFi                       |       |
| 21  | V0.5.0            | Virtual U-Disk   | Supports virtual U-disk functionality|       |
| 22  | V0.5.0            | Peripheral Modules| Reorganizes API for fpioa, adc, uart, spi, i2c, rtc, timer based on official micropython | |
| 23  | V0.5.0            | MCM              | Supports multi-camera, adds 2sensors, 3sensors demo | |
| 24  | V0.6.0            | Sensor           | Adds sensor class                   |       |
| 25  | V0.6.0            | LCD              | Adds LCD class                      |       |
| 25  | V0.6.0            | HDMI             | Adds 720P, 480P resolutions         |       |
| 26  | V0.7.0            | API              | Modifies Display, Sensor, and Media API | |
| 27  | V0.7.0            | Development Boards| Supports 01Studio-CanMV and K230D-Zero development boards | |
| 28  | V1.0.0            | Function Optimization | Optimizes Chinese font rendering, IDE preview image quality, supports GC2093 | |
| 29  | V1.1.0            | **Major Version Change** | No longer depends on specific SDK version, removes Linux code dependency, large-scale code refactoring | |

### AI Demos

| ID  | Supported Version | Function Summary | Function Description                 | Notes |
|-----|-------------------|------------------|--------------------------------------|-------|
| 1   | V0.2.0            | Face Detection   | Locates faces                        |       |
| 2   | V0.2.0            | COCO Object Detection | Locates objects                   |       |
| 3   | V0.2.0            | yolov8-seg       | Segments objects                     |       |
| 4   | V0.2.0            | License Plate Detection | Locates license plates          |       |
| 5   | V0.2.0            | OCR Recognition  | Recognizes text                      |       |
| 6   | V0.2.0            | Palm Detection   | Locates palms                        |       |
| 7   | V0.2.0            | Human Detection  | Locates humans                       |       |
| 8   | V0.2.0            | Human Pose Estimation | Locates human key points         |       |
| 9   | V0.2.0            | KWS              | Keyword wake-up                      |       |
| 10  | V0.2.0            | Face Keypoint Detection | Locates 106 face key points    |       |
| 11  | V0.2.0            | Face Parsing     | Segments different parts of the face |       |
| 12  | V0.2.0            | Face Recognition | Recognizes different faces           |       |
| 13  | V0.2.0            | OCR Detection    | Locates text                         |       |
| 14  | V0.2.0            | License Plate Recognition | Recognizes license plate content | |
| 15  | V0.2.0            | Face Pose Angle  | Infers face rotation angle           |       |
| 16  | V0.2.0            | Rock-Paper-Scissors | Rock-paper-scissors hand gesture game | |
| 17  | V0.2.0            | Palm Keypoint Detection | Locates palm key points         |       |
| 18  | V0.2.0            | Static Gesture Recognition | Recognizes gestures             |       |
| 19  | V0.2.0            | Face Mesh        | Locates 3D face key points            |       |
| 20  | V0.3.0            | Fall Detection   | Determines if a fall has occurred     |       |
| 21  | V0.3.0            | Gaze Estimation  | Infers gaze angle                     |       |
| 22  | V0.3.0            | Dynamic Gesture Recognition | Recognizes dynamic gestures     |       |
| 23  | V0.3.0            | Single Object Tracking | Tracks specified object           |       |
| 24  | V0.3.0            | Air Zoom         | Zooms in and out of specific area images | |
| 25  | V0.3.0            | Puzzle Game      | Recreates the number sliding puzzle game | |
| 26  | V0.3.0            | Keypoint-based Gesture Recognition | Recognizes gestures based on key points | |
| 27  | V0.4.0            | Self-learning    | Determines category based on image features | |
| 28  | V0.5.0            | TTS Chinese      | Converts Chinese text to speech       |       |

## Known Issues and Limitations

| ID  | Functional Module | Issue/Limitations Description | Notes |
|-----|-------------------|-------------------------------|-------|

## Detailed Change Log

For versions after `V1.1.0`, please refer to the [CHANGELOG](https://github.com/kendryte/canmv_k230/blob/main/CHANGELOG.md) in the code.
