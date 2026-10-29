# `PlatTasks` 模块API手册

## 概述

`libs/PlatTasks.py` 是为[嘉楠云训练平台](https://www.kendryte.com/zh/training/start)和 [AICube](../../ai_dev_doc.md#aicube) 离线训练工具产出的模型封装的部署库。平台训练出的每类任务都有固定的模型结构和后处理方式，本模块把这些细节封装成开箱即用的类，用户只需要传入部署包中的 kmodel 路径和配置，即可完成部署。

所有类都继承自 [`AIBase`](./aibase_module_api_manual.md)，因此都具备 `run`、`config_preprocess`、`deinit` 等基础能力，并统一实现了 `postprocess`、`draw_result`、`get_cur_result` 三个方法。

| 类 | 对应平台任务 | 后处理依赖 |
|----|--------------|------------|
| `ClassificationApp` | 图像分类 | softmax |
| `DetectionApp` | 图像检测 | `aicube` 原生模块 |
| `SegmentationApp` | 语义分割 | `aicube` 原生模块 |
| `OCRDetectionApp` | OCR 检测 | `aicube` 原生模块 |
| `OCRRecognitionApp` | OCR 识别 | CTC 贪心解码 |
| `MetricLearningApp` | 度量学习（自学习） | 余弦相似度比对 |
| `MultiLabelClassificationApp` | 多标签分类 | sigmoid |

```{admonition} 提示
:class: note
对应例程位于开发板 `CanMV/sdcard/examples/19-CloudPlatScripts` 目录，每类任务提供 `deploy_*_image.py`（单图推理）和 `deploy_*_video.py`（视频流推理）两个脚本。完整的部署流程见 [云训练平台模型部署](../../example/ai/cloudplat_deploy.md)。
```

## 公共说明

<a id="common-constructor-params"></a>

### 公共构造参数

除 `OCRDetectionApp` 和 `OCRRecognitionApp` 外，各类的构造函数都包含以下参数：

| 参数名称 | 描述 | 说明 | 类型 |
|----------|------|------|------|
| mode | 推理模式 | `'image'` 表示推理单张图片，`'video'` 表示推理摄像头实时视频流。该参数会影响 `draw_result` 的绘制目标 | str |
| kmodel_path | kmodel 路径 | 部署包中 kmodel 在开发板上的路径 | str |
| labels | 类别标签列表 | 来自部署包的配置文件 | list[str] |
| model_input_size | 模型输入分辨率 | 训练时指定的输入分辨率，来自部署包的配置文件 | list[int] |
| confidence_threshold | 置信度阈值 | 低于该值的结果被丢弃 | float [0~1] |
| rgb888p_size | 推理帧分辨率 | 送入 AI 的图像分辨率 | list[int] |
| display_size | 显示分辨率 | `mode='video'` 时设置，建议传 `PipeLine.get_display_size()` 的返回值 | list[int] |
| debug_mode | 调试模式 | 0 为不计时，1 为计时 | int [0/1] |

### 公共方法

| 方法 | 描述 |
|------|------|
| `config_preprocess(input_image_size=None)` | 配置 AI2D 预处理。`input_image_size` 为 `None` 时使用构造时的 `rgb888p_size` |
| `run(input_np)` | 继承自 `AIBase`，完成"预处理 → 推理 → 后处理"完整流程，返回后处理结果 |
| `postprocess(results)` | 后处理，返回值为 dict，各类的字段不同，详见下文 |
| `draw_result(draw_img, res)` | 把结果绘制到 `draw_img` 上。`mode='video'` 时传 `pl.osd_img`，`mode='image'` 时传 `read_image()` 返回的原图 |
| `get_cur_result()` | 获取最近一次 `postprocess` 的结果，内容与 `postprocess` 返回值一致。适合在绘制之外的地方（如上报、联动控制）取用结果 |
| `deinit()` | 释放 kmodel、AI2D 等原生资源，退出前必须调用 |

## API 介绍

### ClassificationApp

**描述**

图像分类任务。对整张图片做分类，输出概率最高的一个类别。

**语法**

```python
from libs.PlatTasks import ClassificationApp

app = ClassificationApp(mode="video", kmodel_path="best.kmodel", labels=labels,
                        model_input_size=[224,224], confidence_threshold=0.7,
                        rgb888p_size=[224,224], display_size=display_size, debug_mode=0)
```

**参数**

见[公共构造参数](#common-constructor-params)，其中 `confidence_threshold` 默认 0.7，`model_input_size` 默认 `[224,224]`。

**返回值**

构造函数返回 `ClassificationApp` 实例。`postprocess` 返回 dict：

| 键 | 类型 | 描述 |
|----|------|------|
| label | str | 分类结果的类别名称 |
| score | float | 对应的分数 |

```{admonition} 提示
:class: note
该类会根据 `labels` 的长度自动切换计算方式：

- **类别数 > 2**：对模型输出做 softmax 取最大值，只有分数**超过** `confidence_threshold` 时才返回结果，否则 `label` 为空字符串、`score` 为 `0.0`。
- **类别数 = 2**：按二分类处理，对模型输出做 sigmoid。分数超过阈值时返回 `labels[1]` 及该分数，否则返回 `labels[0]` 及 `1 - 分数`。因此二分类**总会**返回一个非空的 `label`。
```

### DetectionApp

**描述**

目标检测任务。平台会根据训练配置生成三种不同检测头的模型，本类通过 `model_type` 自动选择对应的 `aicube` 后处理接口。

**语法**

```python
from libs.PlatTasks import DetectionApp

app = DetectionApp(mode="video", kmodel_path="best.kmodel", labels=labels,
                   model_input_size=[640,640], anchors=anchors,
                   model_type="AnchorBaseDet", confidence_threshold=0.5,
                   nms_threshold=0.25, rgb888p_size=[1280,720],
                   display_size=display_size, debug_mode=0)
```

**参数**

除[公共构造参数](#common-constructor-params)外，还包括：

| 参数名称 | 描述 | 说明 | 类型 |
|----------|------|------|------|
| anchors | 锚框尺寸列表 | `model_type='AnchorBaseDet'` 时**必须为 18 个值**，否则抛出异常。取自部署包配置文件 | list |
| model_type | 检测头类型 | 可选 `'AnchorBaseDet'`、`'AnchorFreeDet'`、`'GFLDet'`，取自部署包配置文件，不要随意更改 | str |
| nms_threshold | NMS 阈值 | 非极大值抑制阈值，默认 0.25 | float [0~1] |

**返回值**

构造函数返回 `DetectionApp` 实例。`postprocess` 返回 dict：

| 键 | 类型 | 描述 |
|----|------|------|
| boxes | ndarray | 检测框列表，每个框为 `[x1, y1, x2, y2]`，坐标基于 `rgb888p_size` |
| scores | ndarray | 每个框对应的置信度 |
| idx | ndarray | 每个框对应的类别索引，可用于索引 `labels` |

### SegmentationApp

**描述**

语义分割任务。输出一张与 `display_size` 同分辨率的 mask 图像，可以直接叠加到 OSD 层显示。

**语法**

```python
from libs.PlatTasks import SegmentationApp

app = SegmentationApp(mode="video", kmodel_path="best.kmodel", labels=labels,
                      model_input_size=[320,320], rgb888p_size=[320,320],
                      display_size=display_size, debug_mode=0)
```

**参数**

全部为[公共构造参数](#common-constructor-params)，其中 `model_input_size` 默认 `[320,320]`。该类不使用 `confidence_threshold`。

**返回值**

构造函数返回 `SegmentationApp` 实例。`postprocess` 返回 dict：

| 键 | 类型 | 描述 |
|----|------|------|
| mask | image.Image | 与 `display_size` 同分辨率的 mask 图像。`mode='video'` 时为 ARGB8888 格式，可直接叠加到 OSD；`mode='image'` 时为 RGB888 格式 |

```{admonition} 注意
:class: warning
`postprocess` 的 `input_np` 参数仅为保持接口兼容而保留，实际不使用，方法内部读取的是上一步推理的输出。
```

### OCRDetectionApp

**描述**

OCR 检测任务。在图片中找出文本区域，返回四边形框坐标，同时把每个文本区域裁剪出来，可直接送给 `OCRRecognitionApp` 做识别。

**语法**

```python
from libs.PlatTasks import OCRDetectionApp

app = OCRDetectionApp(mode="video", kmodel_path="ocr_det.kmodel",
                      model_input_size=[640,640], mask_threshold=0.5,
                      box_threshold=0.5, rgb888p_size=[1280,720],
                      display_size=display_size, debug_mode=0)
```

**参数**

不含 `labels` 和 `confidence_threshold`，其余同[公共构造参数](#common-constructor-params)，另有：

| 参数名称 | 描述 | 说明 | 类型 |
|----------|------|------|------|
| mask_threshold | 文本区域二值化阈值 | 概率图二值化的阈值，默认 0.5 | float [0~1] |
| box_threshold | 文本框置信度阈值 | 低于该值的文本框被丢弃，默认 0.5 | float [0~1] |

**返回值**

构造函数返回 `OCRDetectionApp` 实例。`postprocess` 返回 dict：

| 键 | 类型 | 描述 |
|----|------|------|
| boxes | list | 每个元素是 8 个坐标值 `[p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y]`，依次为文本框的左上、右上、右下、左下角，坐标基于 `rgb888p_size` |
| crop_images | list | 与 `boxes` 一一对应的裁剪图像（HWC 排布数组），可直接送入 `OCRRecognitionApp` |

### OCRRecognitionApp

**描述**

OCR 识别任务。识别单张长条状文本图片中的文字内容，使用 CTC 贪心解码。

```{admonition} 注意
:class: warning
平台的 OCR 识别模型单次推理读入的是**长条状文本图片**，不能把摄像头整帧直接喂给它，必须先用 `OCRDetectionApp` 检测并裁剪出文本区域，再逐个送进来识别。

这与构造参数 `mode` 无关：`mode` 只影响 `draw_result`/`print_result` 的绘制目标。在"检测 + 识别"的视频流应用里（对应例程 `deploy_ocr_video.py`），本类同样使用 `mode="video"`，输入依然是 `OCRDetectionApp` 裁出的文本条。单图场景（`deploy_ocrrec_image.py`）则用 `mode="image"`。
```

**语法**

```python
from libs.PlatTasks import OCRRecognitionApp

app = OCRRecognitionApp(mode="video", kmodel_path="ocr_rec.kmodel",
                        model_input_size=[512,32], ocr_dict=ocr_dict,
                        rgb888p_size=[1280,720], display_size=display_size, debug_mode=0)
```

**参数**

不含 `labels` 和 `confidence_threshold`，其余同[公共构造参数](#common-constructor-params)，另有：

| 参数名称 | 描述 | 说明 | 类型 |
|----------|------|------|------|
| ocr_dict | 字符字典 | 来自部署包的字典文件，**最后一个元素被当作 CTC 的 blank 符号** | list[str] |

**返回值**

构造函数返回 `OCRRecognitionApp` 实例。`postprocess` 返回 dict：

| 键 | 类型 | 描述 |
|----|------|------|
| text | str | 识别出的文本内容 |

**专有方法**

| 方法 | 描述 |
|------|------|
| `print_result(osd_img, res)` | 打印识别文本，`mode='video'` 时同时清空 OSD |
| `draw_result(osd_img, det_boxes, ocr_texts)` | 与其它类签名不同，需要同时传入检测框和识别文本，用于把检测 + 识别的结果一起绘制 |

### MetricLearningApp

**描述**

度量学习任务，也称自学习。模型把图片映射成特征向量，通过与特征库中的向量做余弦相似度比对来分类。**不需要重新训练模型即可添加新类别**，只需要往特征库里加入新的参考图片。

**语法**

```python
from libs.PlatTasks import MetricLearningApp

app = MetricLearningApp(mode="video", kmodel_path="best.kmodel",
                        model_input_size=[224,224], confidence_threshold=0.5,
                        rgb888p_size=[224,224], display_size=display_size, debug_mode=0)
# 注册参考图片，建立特征库
app.load_image("/sdcard/examples/utils/db_img/apple.jpg", "apple")
app.load_image("/sdcard/examples/utils/db_img/banana.jpg", "banana")
```

**专有方法**

| 方法 | 描述 |
|------|------|
| `load_image(image_path, label)` | 从图片中提取特征并以 `label` 为标签存入特征库。内部会临时切换预处理配置，调用结束后自动恢复，因此可以在任意时刻调用 |
| `compute_similar(embedding)` | 在特征库中查找与 `embedding` 余弦相似度最高的向量，返回 `(索引, 相似度)`。特征库为空或无有效匹配时返回 `(-1, 0.0)` |

**参数**

不含 `labels`（类别来自特征库），其余为[公共构造参数](#common-constructor-params)，其中 `confidence_threshold` 为余弦相似度阈值，默认 0.5。

**返回值**

构造函数返回 `MetricLearningApp` 实例。`postprocess` 返回 dict：

| 键 | 类型 | 描述 |
|----|------|------|
| label | str | 匹配到的标签。特征库为空、无匹配或相似度低于阈值时为空字符串 |
| score | float | 余弦相似度 |

```{admonition} 注意
:class: warning
特征库保存在内存中，**不会持久化**，掉电或 `deinit()` 后丢失。库中条目数量没有上限，注册过多会占用大量内存，需要自行控制。
```

### MultiLabelClassificationApp

**描述**

多标签分类任务。一张图片可能同时属于多个类别（例如"天空"和"大海"），对每个类别独立做二分类，输出所有分数超过阈值的类别。

**语法**

```python
from libs.PlatTasks import MultiLabelClassificationApp

app = MultiLabelClassificationApp(mode="video", kmodel_path="best.kmodel", labels=labels,
                                  model_input_size=[224,224], confidence_threshold=0.5,
                                  rgb888p_size=[224,224], display_size=display_size, debug_mode=0)
```

**参数**

全部为[公共构造参数](#common-constructor-params)，其中 `confidence_threshold` 为每个类别独立二分类的判定阈值，默认 0.5。

**返回值**

构造函数返回 `MultiLabelClassificationApp` 实例。`postprocess` 返回 dict：

| 键 | 类型 | 描述 |
|----|------|------|
| labels | list[str] | 所有 sigmoid 分数超过 `confidence_threshold` 的类别名称 |
| scores | list[float] | 与 `labels` 一一对应的分数 |

## 示例程序

以下给出视频流推理的通用框架，以图像分类为例：

```python
from libs.PipeLine import PipeLine
from libs.PlatTasks import ClassificationApp
from libs.Utils import *
import os, ujson, gc

if __name__ == "__main__":
    # 从部署包的配置文件中读取参数
    deploy_conf = read_json("/sdcard/mp_deployment_source/deploy_config.json")
    kmodel_path = "/sdcard/mp_deployment_source/best.kmodel"
    labels = deploy_conf["categories"]
    model_input_size = [deploy_conf["img_size"][0], deploy_conf["img_size"][1]]

    rgb888p_size = [224, 224]
    pl = None
    app = None
    try:
        pl = PipeLine(rgb888p_size=rgb888p_size, display_mode="auto")
        pl.create()
        display_size = pl.get_display_size()

        app = ClassificationApp(mode="video", kmodel_path=kmodel_path, labels=labels,
                                model_input_size=model_input_size,
                                confidence_threshold=0.7, rgb888p_size=rgb888p_size,
                                display_size=display_size, debug_mode=0)
        app.config_preprocess()

        while True:
            img = pl.get_frame()
            res = app.run(img)
            app.draw_result(pl.osd_img, res)
            pl.show_image()
            gc.collect()
    finally:
        if app is not None:
            app.deinit()
        if pl is not None:
            pl.destroy()
        gc.collect()
```
