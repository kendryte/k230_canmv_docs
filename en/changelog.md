# Version Notes

## Version Information

| Product | Version | Release Date |
|----------|--------|----------|
| K230 CanMV | V0.2.0 | 2023-11-23 |
| K230 CanMV | V0.3.0 | 2023-12-28 |
| K230 CanMV | V0.4.0 | 2024-01-26 |
| K230 CanMV | V0.5.0 | 2024-03-15 |
| K230 CanMV | V0.6.0 | 2024-04-30 |
| K230 CanMV | V0.7.0 | 2024-07-05 |
| K230 CanMV | V1.0.0 | 2024-08-02 |
| K230 CanMV | V1.1.0 | 2024-09-14 |

## Supported Hardware

K230 platform supports CanMV-K230 and other boards

## Version Usage Restrictions

None

## CanMV, SDK, and nncase Version Relationship

When performing AI development, the version correspondence between k230_sdk and nncase is shown in the table below. Please pay attention to the version correspondence when compiling images and using nncase to convert kmodel.

| Canmv(micropython) Version | K230 SDK Version | nncase Version | Remarks |
| -------------| ------------- | ----------- |  ---- |
| 0.2.0        | 1.1.0         | 2.4.0       |  -    |
| 0.3.0        | 1.1.0         | 2.4.0       |  -    |
| 0.4.0        | 1.3.0         | 2.7.0       |  -    |
| 0.5.0        | 1.4.0         | 2.8.0       |  -    |
| 0.6.0        | 1.5.0         | 2.8.1       |  -    |
| 0.7.0        | 1.6.0         | 2.8.3       |  -    |
| 1.0.0        | 1.6.0         | 2.8.3       |  -    |
| 1.1.0        | -             | 2.9.0       |  -    |

## Version Feature Statistics

### Basic Features

| ID | Supported Version | Feature Summary | Feature Description | Remarks |
| --- | --- | --- | --- | --- |
| 1 | V0.2.0 | Camera | Supports acquiring sensor images | |
| 2 | V0.2.0 | Display | Supports HDMI display | |
| 3 | V0.2.0 | Encryption Module | Supports hardware SHA256, AES | |
| 4 | V0.2.0 | VPU | Supports encoding and decoding | |
| 5 | V0.2.0 | audio | Supports audio, built-in codec | |
| 6 | V0.2.0 | gpio | Supports GPIO | |
| 7 | V0.2.0 | adc | Supports analog-to-digital conversion | |
| 8 | V0.2.0 | fft | Supports Fourier transform | |
| 9 | V0.2.0 | i2c | Supports i2c communication | |
| 10 | V0.2.0 | pwm | Supports PWM output | |
| 11 | V0.2.0 | spi | Supports SPI communication | |
| 12 | V0.2.0 | timer | Supports timer | |
| 13 | V0.2.0 | wdt | Supports watchdog | |
| 14 | V0.3.0 | omv | Supports openmv-related algorithms | |
| 15 | V0.3.0 | Network | Supports wired network | |
| 16 | V0.3.0 | Stability | Improves micropython stability | |
| 17 | V0.3.0 | IDE Display | IDE can display images in real time | |
| 18 | V0.4.0 | SDK and nncase Upgrade | SDK upgraded to V1.3, nncase upgraded to v2.7 | |
| 19 | V0.4.0 | lvgl | Supports LVGL | |
| 20 | V0.4.0 | wifi | Supports WIFI | |
| 21 | V0.5.0 | Virtual USB Drive | Supports virtual USB drive function | |
| 22 | V0.5.0 | Peripheral Modules | Reorganized APIs for fpioa, adc, uart, spi, i2c, rtc, timer modules according to the official micropython | |
| 23 | V0.5.0 | MCM | Supports multiple cameras, adds 2sensors, 3sensors demos | |
| 24 | V0.6.0 | sensor | Added sensor class | |
| 25 | V0.6.0 | lcd | Added lcd class | |
| 25 | V0.6.0 | HDMI | Added 720P, 480P resolutions | |
| 26 | V0.7.0 | API | Modified Display, Sensor, and Media APIs | |
| 27 | V0.7.0 | Development Board | Supports 01Studio-CanMV and K230D-Zero development boards | |
| 28 | V1.0.0 | Feature Optimization | Optimized Chinese font rendering, optimized IDE preview image quality, supports GC2093 | |
| 29 | V1.1.0 | **Major Version Change** | No longer depends on specific SDK version, removed Linux code dependencies, large-scale code refactoring | |

### AI Demo

| ID | Supported Version | Feature Summary | Feature Description | Remarks |
| --- | --- | --- | --- | --- |
| 1 | V0.2.0 | Face Detection | Locate faces | |
| 2 | V0.2.0 | COCO Object Detection | Locate objects | |
| 3 | V0.2.0 | yolov8-seg | Segment objects | |
| 4 | V0.2.0 | License Plate Detection | Locate license plates | |
| 5 | V0.2.0 | OCR Recognition | Recognize text | |
| 6 | V0.2.0 | Palm Detection | Locate palms | |
| 7 | V0.2.0 | Human Detection | Locate human bodies | |
| 8 | V0.2.0 | Human Pose Estimation | Locate human body keypoints | |
| 9 | V0.2.0 | KWS | Keyword wake-up | |
| 10 | V0.2.0 | Face Keypoint Detection | Locate 106 face keypoints | |
| 11 | V0.2.0 | Face Parsing | Segmentation of different face parts | |
| 12 | V0.2.0 | Face Recognition | Recognize different faces | |
| 13 | V0.2.0 | OCR Detection | Locate text | |
| 14 | V0.2.0 | License Plate Recognition | Recognize license plate content | |
| 15 | V0.2.0 | Face Pose Angle | Infer face rotation angle | |
| 16 | V0.2.0 | Rock Paper Scissors | Rock paper scissors hand gesture game | |
| 17 | V0.2.0 | Palm Keypoint Detection | Locate palm keypoints | |
| 18 | V0.2.0 | Static Gesture Recognition | Recognize gestures | |
| 19 | V0.2.0 | Face Mesh | Locate 3D face keypoints | |
| 20 | V0.3.0 | Fall Detection | Determine whether a fall has occurred | |
| 21 | V0.3.0 | Gaze Estimation | Infer glasses gaze angle | |
| 22 | V0.3.0 | Dynamic Gesture Recognition | Recognize dynamic gestures | |
| 23 | V0.3.0 | Single Object Tracking | Track specified target | |
| 24 | V0.3.0 | Air Zoom | Zoom in and out of corresponding area image in the air | |
| 25 | V0.3.0 | Jigsaw Puzzle Game | Reproduce the digital Huarong Road puzzle game | |
| 26 | V0.3.0 | Keypoint-based Gesture Recognition | Keypoint-based gesture recognition | |
| 27 | V0.4.0 | Self-learning | Determine category based on image features | |
| 28 | V0.5.0 | TTS Chinese | Chinese text to speech | |

## Known Issues and Limitations

| ID | Feature Module | Issue/Limit Description | Notes |
| --- | --- | --- | --- |

## Detailed Change Log

For changes after `V1.1.0`, refer to the [CHANGELOG](https://github.com/kendryte/canmv_k230/blob/main/CHANGELOG.md) in the source code.
