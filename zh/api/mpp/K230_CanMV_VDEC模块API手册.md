# 3.5 VDEC 模块API手册

![cover](../images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍K230_CanMV VDEC模块API的使用。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
| VDEC | Video Decoder   |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 孙小朋      | 2023-10-27 |

## 1. 概述

此文档介绍K230_CanMV VDEC模块API，可支持264,265解码，并于vo模块绑定，将解码数据输出到vo显示。

## 2. API描述

提供Decoder类，该类提供如下方法：

### 2.1 Decoder.\_\_init__

【描述】

构造函数

【语法】

```python
decoder = Decoder(K_PT_H264)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| type  | 编码类型            | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【注意】

VDEC最多支持4路解码

【举例】

无

【相关主题】

无

### 2.2 Decoder.Create

【描述】

创建解码器

【语法】

```python
decoder = Decoder(K_PT_H264)
decoder.create()
```

【参数】

无

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功                          |
| 非 0    | 失败 |

【举例】

无

【相关主题】

无

### 2.3 Decoder.destroy

【描述】

销毁解码器

【语法】

```python
decoder = Decoder(K_PT_H264)
decoder.destroy()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.4 Decoder.Start

【描述】

开始编码

【语法】

```python
decoder = Decoder(K_PT_H264)
decoder.Start()
```

【参数】

【返回值】

| 返回值 | 描述 |
|--------|-----|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.5 Decoder.decode

【描述】

解码一帧数据

【语法】

```python
decoder = Decoder(K_PT_H264)
decoder.decode(stream_data)
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|----------|-----|----------|
| stream_data | 编码数据 | 输入 |

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

### 2.6 Decoder.stop

【描述】

释放一帧码流buffer

【语法】

```python
decoder = Decoder(K_PT_H264)
decoder.stop()
```

【参数】

无

【返回值】

| 返回值 | 描述 |
|--------|------|
| 0 | 成功 |
| 非0 | 失败 |

【注意】

无

【举例】

无

## 3. 数据结构描述

### 3.1 StreamData

【说明】

码流结构体

【定义】

```python
class StreamData:
    def __init__(self):
        self.data
        self.pts
```

【成员】

| 成员名称 | 描述 |
|---------|------|
| data | 码流数据 |
| pts | 时间戳 |

【注意事项】

无

## 4. 示例程序

### 4.1 例程1

```{admonition} 提示
无,具体接口使用可参考 [player](./K230_CanMV_播放器模块API手册.md)
```
