# 3.9 PM 模块API手册

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

本文档主要介绍mpp模块下的pm类API。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
|    |    |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 软件部      | 2023-09-17 |

## 1. 概述

PM模块是功耗管理模块，具体可参考SDK中关于PM框架的描述([K230_PM框架使用指南.md](https://github.com/kendryte/k230_docs/blob/main/zh/01_software/board/mpp/K230_PM%E6%A1%86%E6%9E%B6%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md))。micropython中封装了cpu和kpu两部分。

## 2. API描述

pm类位于mpp模块下，模块内部包含了两个实例化对象cpu, kpu

### 2.1 示例

```python
from mpp import pm
# get current cpu freq
pm.cpu.get_freq()
# get cpu support freq list
pm.cpu.list_profiles()
# set cpu freq
pm.cpu.set_profile(1)
```

### 2.2 get_freq

```python
pm.pm_domain.get_freq()
```

获取指定域频率

【参数】

无

【返回值】

指定域频率

### 2.3 list_profiles

```python
pm.pm_domain.list_profiles()
```

获取指定域支持的频率列表

【参数】

无

【返回值】

指定域支持的频率列表

### 2.4 set_profile

```python
pm.pm_domain.set_profile(index)
```

设置指定域的频率序号

【参数】

- index: 频率序号

【返回值】

无
