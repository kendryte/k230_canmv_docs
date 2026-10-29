# `mot` 模块API手册

## 概述

`mot`（Multi-Object Tracking）是 CanMV 内置的多目标跟踪原生模块，用于给检测模型的输出结果分配**稳定的目标 ID**。检测模型每帧独立推理，同一个人在相邻两帧里没有任何关联；`mot` 在检测结果之上做数据关联和卡尔曼预测，让同一个目标在整段视频中保持同一个 `track_id`，从而可以实现计数、轨迹绘制、越界判断等应用。

模块提供四种跟踪算法：

| 类 | 算法 | 是否需要 ReID 特征 | 适用场景 |
|----|------|------|------|
| `mot.ByteTrack` | ByteTrack | 否 | **推荐的默认选择**。纯 IoU 关联，速度最快，额外开销极小；利用低分检测框找回被遮挡目标 |
| `mot.OCSort` | OC-SORT | 否 | 目标运动不规则、频繁加减速或转向的场景，对遮挡后的轨迹恢复更好 |
| `mot.DeepSort` | DeepSort | **是（必需）** | 目标外观差异明显、需要长时间遮挡后仍保持同一 ID 的场景。需额外跑一个 ReID 特征模型，帧率下降明显 |
| `mot.BoTSort` | BoT-SORT | 可选 | ByteTrack 的增强版，`reid_enabled=True` 时融合外观特征，精度最高，开销也最大 |

```{admonition} 提示
:class: note
`mot` 只做跟踪，不做检测。使用前需要先有一个目标检测模型（如 YOLOv8 行人检测）输出检测框。`DeepSort` 和开启 ReID 的 `BoTSort` 还需要额外的 ReID 特征提取模型。

对应例程位于开发板 `CanMV/sdcard/examples/05-AI-Demo` 目录：`bytetrack.py`、`ocsort.py`、`deepsort.py`、`botsort.py`。
```

## API 介绍

### 公共说明

四个类的构造函数**全部只接受关键字参数**，不支持位置参数。以下两个参数为四个类共有：

| 参数名称 | 描述 | 说明 | 类型 |
|----------|------|------|------|
| class_aware | 是否按类别跟踪 | `True` 时只有同类别的检测框才会与已有轨迹关联，多类别场景下避免 ID 串类；`False` 时忽略类别。默认 `True` | bool |
| bbox_format | 检测框格式 | `'xyxy'` 表示 `[x1,y1,x2,y2]`（左上、右下坐标），`'xywh'` 表示 `[x,y,w,h]`（左上坐标 + 宽高）。该设置同时作用于 `update()` 的入参和返回结果中的 `bbox`。默认 `'xyxy'`，取其它值会抛出 `ValueError` | str |

所有阈值类参数取值必须为 `[0, 1]` 区间内的有限浮点数，否则抛出 `ValueError`。

### mot.ByteTrack

**描述**

创建 ByteTrack 跟踪器。ByteTrack 的核心思路是"低分框也不浪费"：先用高分检测框与轨迹做第一轮匹配，再用低分检测框去找回那些因遮挡而置信度下降的轨迹。

**语法**

```python
import mot

tracker = mot.ByteTrack(track_thresh=0.5, high_thresh=0.6, match_thresh=0.8,
                        track_buffer=30, frame_rate=30, min_hits=1,
                        class_aware=True, bbox_format="xywh")
```

**参数**

| 参数名称 | 描述 | 说明 | 类型 | 默认值 |
|----------|------|------|------|--------|
| track_thresh | 高分框阈值 | 分数高于该值的检测框参与第一轮关联，低于该值的进入第二轮"找回"关联 | float [0~1] | 0.5 |
| high_thresh | 新建轨迹阈值 | 未匹配上的检测框分数高于该值时才会新建一条轨迹。必须 **≥ `track_thresh`** | float [0~1] | 0.6 |
| match_thresh | 匹配阈值 | 第一轮关联允许的最大 IoU 距离，值越大越容易匹配上 | float [0~1] | 0.8 |
| track_buffer | 轨迹保留帧数 | 目标消失后轨迹保留多少帧才删除，按 30fps 基准计 | int | 30 |
| frame_rate | 实际帧率 | 与 `track_buffer` 一起换算实际保留帧数，公式为 `track_buffer * frame_rate / 30` | int | 30 |
| min_hits | 确认所需命中数 | 轨迹连续命中该次数后才从 `tentative` 转为 `tracked` 并被输出 | int | 1 |

**返回值**

| 返回值 | 描述 |
|--------|------|
| ByteTrack | ByteTrack 跟踪器实例 |

```{admonition} 注意
:class: warning
若 `high_thresh < track_thresh`，或 `track_buffer`/`frame_rate`/`min_hits` 小于 1，构造时会抛出 `ValueError: invalid ByteTrack thresholds or lifetime`。
```

### mot.OCSort

**描述**

创建 OC-SORT（Observation-Centric SORT）跟踪器。相比 ByteTrack 更依赖运动建模，通过观测方向一致性（`inertia`）和虚拟轨迹补全，改善目标遮挡后重新出现时的 ID 保持。

**语法**

```python
import mot

tracker = mot.OCSort(det_thresh=0.3, max_age=30, min_hits=3, iou_threshold=0.3,
                     delta_t=3, inertia=0.2, use_byte=False,
                     class_aware=True, bbox_format="xywh")
```

**参数**

| 参数名称 | 描述 | 说明 | 类型 | 默认值 |
|----------|------|------|------|--------|
| det_thresh | 检测框阈值 | 分数低于该值的检测框不参与新建轨迹 | float [0~1] | 0.3 |
| max_age | 轨迹最大存活帧数 | 目标连续多少帧未匹配后删除轨迹 | int | 30 |
| min_hits | 确认所需命中数 | 轨迹累计命中该次数后才被输出 | int | 3 |
| iou_threshold | IoU 关联阈值 | 检测框与轨迹预测框的最小 IoU | float [0~1] | 0.3 |
| delta_t | 速度估计跨度 | 用前 `delta_t` 帧的位置估计目标运动方向，值越大方向越平滑但响应越慢 | int | 3 |
| inertia | 方向一致性权重 | 运动方向一致性在关联代价中的权重 | float [0~1] | 0.2 |
| use_byte | 是否启用低分框找回 | `True` 时借鉴 ByteTrack 的二轮关联策略 | bool | False |

**返回值**

| 返回值 | 描述 |
|--------|------|
| OCSort | OCSort 跟踪器实例 |

```{admonition} 注意
:class: warning
`max_age`、`min_hits`、`delta_t` 必须均 ≥ 1，否则抛出 `ValueError: age, hits, and delta_t must be positive`。
```

### mot.DeepSort

**描述**

创建 DeepSort 跟踪器。在运动关联之外增加**外观特征（ReID）关联**，每条轨迹维护一个特征库，用余弦距离匹配。**调用 `update()` 时必须传入 `features` 参数**。

**语法**

```python
import mot

tracker = mot.DeepSort(feature_dim=128, max_cosine_distance=0.2, nn_budget=100,
                       max_iou_distance=0.7, max_age=30, n_init=3,
                       class_aware=True, bbox_format="xywh")
```

**参数**

| 参数名称 | 描述 | 说明 | 类型 | 默认值 |
|----------|------|------|------|--------|
| feature_dim | 特征维度 | **必填**，ReID 模型输出的特征向量长度，必须 ≥ 1，且与实际传入 `update()` 的特征长度完全一致 | int | 无 |
| max_cosine_distance | 最大余弦距离 | 外观匹配允许的最大余弦距离，越小越严格 | float [0~1] | 0.2 |
| nn_budget | 特征库容量 | 每条轨迹最多保存多少个历史特征，超出后丢弃最旧的 | int | 100 |
| max_iou_distance | 最大 IoU 距离 | 外观匹配失败后，回退到 IoU 匹配时允许的最大距离 | float [0~1] | 0.7 |
| max_age | 轨迹最大存活帧数 | 目标连续多少帧未匹配后删除轨迹 | int | 30 |
| n_init | 确认所需命中数 | 轨迹连续命中该次数后才被输出 | int | 3 |

**返回值**

| 返回值 | 描述 |
|--------|------|
| DeepSort | DeepSort 跟踪器实例 |

```{admonition} 注意
:class: warning
`feature_dim`、`nn_budget`、`max_age`、`n_init` 必须均 ≥ 1，否则抛出 `ValueError: feature_dim, budget, age, and n_init must be positive`。
```

### mot.BoTSort

**描述**

创建 BoT-SORT 跟踪器。在 ByteTrack 的两轮关联基础上，可选叠加外观特征匹配。`reid_enabled=False` 时行为接近 ByteTrack，无需传入特征；`reid_enabled=True` 时必须传入特征。

**语法**

```python
import mot

# 纯运动模式，不需要 ReID 模型
tracker = mot.BoTSort(reid_enabled=False, track_high_thresh=0.6, track_buffer=30,
                      class_aware=True, bbox_format="xywh")

# 开启外观匹配
tracker = mot.BoTSort(feature_dim=128, reid_enabled=True,
                      track_high_thresh=0.6, track_low_thresh=0.1,
                      new_track_thresh=0.7, track_buffer=30, match_thresh=0.7,
                      proximity_thresh=0.5, appearance_thresh=0.25,
                      appearance_weight=0.985, frame_rate=30, min_hits=1,
                      class_aware=True, bbox_format="xywh")
```

**参数**

| 参数名称 | 描述 | 说明 | 类型 | 默认值 |
|----------|------|------|------|--------|
| feature_dim | 特征维度 | ReID 特征向量长度。`reid_enabled=False` 时该值被强制置 0 并忽略；`reid_enabled=True` 时必须 ≥ 1 | int | 0 |
| reid_enabled | 是否启用外观匹配 | 为 `True` 时 `update()` 必须传入 `features` | bool | False |
| track_high_thresh | 高分框阈值 | 高于该值的检测框参与第一轮关联 | float [0~1] | 0.6 |
| track_low_thresh | 低分框阈值 | 低于该值的检测框直接丢弃。必须 **≤ `track_high_thresh`** | float [0~1] | 0.1 |
| new_track_thresh | 新建轨迹阈值 | 未匹配的检测框分数高于该值才新建轨迹。必须 **≥ `track_high_thresh`** | float [0~1] | 0.7 |
| track_buffer | 轨迹保留帧数 | 与 `frame_rate` 一起换算实际保留帧数，公式为 `track_buffer * frame_rate / 30` | int | 30 |
| match_thresh | 匹配阈值 | 第一轮关联允许的最大距离 | float [0~1] | 0.7 |
| proximity_thresh | 空间邻近阈值 | 只有 IoU 足够大的检测框才允许参与外观匹配，防止远距离误配 | float [0~1] | 0.5 |
| appearance_thresh | 外观匹配阈值 | 外观匹配允许的最大余弦距离 | float [0~1] | 0.25 |
| appearance_weight | 外观权重 | 外观代价与运动代价的融合权重 | float [0~1] | 0.985 |
| frame_rate | 实际帧率 | 与 `track_buffer` 配合换算轨迹保留帧数 | int | 30 |
| min_hits | 确认所需命中数 | 轨迹命中该次数后才被输出 | int | 1 |

**返回值**

| 返回值 | 描述 |
|--------|------|
| BoTSort | BoTSort 跟踪器实例 |

```{admonition} 注意
:class: warning
若 `track_low_thresh > track_high_thresh`、`new_track_thresh < track_high_thresh`、`max_age < 1`、`min_hits < 1`，或开启 ReID 但 `feature_dim < 1`，构造时会抛出 `ValueError: invalid BoTSORT parameters`。
```

### update

**描述**

输入当前帧的检测结果，推进跟踪器一帧，返回本帧**活跃**的轨迹列表。四个跟踪器类的 `update` 接口完全一致。

**语法**

```python
tracks = tracker.update(boxes, scores, class_ids)
tracks = tracker.update(boxes, scores, class_ids, features)   # DeepSort / BoTSort(reid)
```

**参数**

| 参数名称 | 描述 | 输入 / 输出 | 说明 |
|----------|------|-----------|------|
| boxes | 检测框列表 | 输入 | 每个元素是长度为 4 的序列，格式由构造时的 `bbox_format` 决定 |
| scores | 分数列表 | 输入 | 与 `boxes` 等长，每个值须在 `[0, 1]` 区间内 |
| class_ids | 类别索引列表 | 输入 | 与 `boxes` 等长，每个值须为非负整数 |
| features | ReID 特征列表 | 输入 | 可选。与 `boxes` 等长，每行长度须等于 `feature_dim`。`DeepSort` 和开启 ReID 的 `BoTSort` **必填**；其它跟踪器传入会报错 |

**返回值**

| 返回值 | 描述 |
|--------|------|
| list[dict] | 本帧活跃轨迹列表，字段说明见 [轨迹结果格式](#track-result-format) |

```{admonition} 注意
:class: warning
当前帧没有检测到目标时，**仍然要调用** `tracker.update([], [], [])`，让跟踪器推进帧计数并按 `max_age` 淘汰过期轨迹。漏调会导致目标消失后轨迹一直不释放。

传入数据不合法时会抛出 `ValueError`，常见原因：三个列表长度不一致、检测框不是 4 个值、框的宽高不为正、分数超出 `[0,1]`、类别为负数、特征行数或维度不匹配、特征向量为全零。
```

### tracks

**描述**

查询跟踪器当前持有的轨迹，不推进帧。与 `update()` 的返回值不同，该接口可以额外返回处于 `lost` 状态的轨迹。

**语法**

```python
active = tracker.tracks()                     # 仅本帧可见的轨迹
all_tracks = tracker.tracks(include_lost=True)  # 包含暂时丢失的轨迹
```

**参数**

| 参数名称 | 描述 | 输入 / 输出 | 说明 |
|----------|------|-----------|------|
| include_lost | 是否包含丢失轨迹 | 输入 | 关键字参数。`False`（默认）只返回本帧更新过的轨迹，等价于最近一次 `update()` 的结果；`True` 时返回**全部未被删除的轨迹**，包括本帧未匹配上（`time_since_update > 0`）的活跃轨迹和处于 `lost` 状态的轨迹。两种情况下 `removed` 状态的轨迹都不会返回 |

**返回值**

| 返回值 | 描述 |
|--------|------|
| list[dict] | 轨迹列表，字段说明见 [轨迹结果格式](#track-result-format) |

### reset

**描述**

清空所有轨迹并把帧计数归零，跟踪器回到刚创建的状态。切换场景、切换视频源时使用，可以避免旧场景的 ID 延续到新场景。

**语法**

```python
tracker.reset()
```

**返回值**

| 返回值 | 描述 |
|--------|------|
| 无 | |

### frame_id

**描述**

获取跟踪器已处理的帧序号，即 `update()` 的累计调用次数。`reset()` 后归零。

**语法**

```python
n = tracker.frame_id()
```

**返回值**

| 返回值 | 描述 |
|--------|------|
| int | 已处理的帧数 |

### close

**描述**

释放跟踪器占用的原生资源。程序退出前必须调用，通常放在 `finally` 块里。等价于 `__del__`，但不必等待垃圾回收触发。

**语法**

```python
tracker.close()
```

**返回值**

| 返回值 | 描述 |
|--------|------|
| 无 | |

```{admonition} 注意
:class: warning
`close()` 之后再调用 `update()`、`tracks()`、`reset()`、`frame_id()` 会抛出 `ValueError: tracker is closed`。
```

<a id="track-result-format"></a>

## 轨迹结果格式

`update()` 和 `tracks()` 返回的列表中，每个元素是一个 dict：

| 键 | 类型 | 描述 |
|----|------|------|
| track_id | int | 轨迹唯一 ID。同一个目标在整段视频中保持不变，是实现计数和轨迹绘制的依据 |
| class_id | int | 目标类别索引，来自 `update()` 传入的 `class_ids` |
| bbox | tuple[float, float, float, float] | 轨迹当前框，格式与构造时的 `bbox_format` 一致。注意这是跟踪器**平滑/预测后**的框，与传入的检测框不完全相同 |
| score | float | 目标置信度 |
| state | str | 轨迹状态：`tentative`（新建待确认）、`tracked`（正常跟踪中）、`lost`（暂时丢失，等待找回）。`removed` 状态的轨迹不会被返回 |
| age | int | 轨迹自创建以来经过的总帧数 |
| hits | int | 轨迹累计匹配上检测框的次数 |
| time_since_update | int | 距离上次匹配上检测框过去了多少帧。`0` 表示本帧可见 |

## 示例程序

以下给出 YOLOv8 行人检测 + ByteTrack 的完整跟踪流程，完整代码参考开发板上的 `05-AI-Demo/bytetrack.py`：

```python
from libs.PipeLine import PipeLine
from libs.Utils import *
import os, gc
import mot

def update_tracker(tracker, dets):
    # dets 为检测结果，dets[0] 是框列表，dets[2] 是分数列表
    boxes = dets[0]
    if not boxes:
        # 没有检测到目标也必须调用 update，推进帧计数并淘汰过期轨迹
        return tracker.update([], [], [])
    scores = dets[2]
    class_ids = [0] * len(boxes)      # 单类别（行人），类别索引全为 0
    return tracker.update(boxes, scores, class_ids)

if __name__ == "__main__":
    rgb888p_size = [1280, 720]
    pl = None
    person_det = None
    tracker = None
    os.exitpoint(os.EXITPOINT_ENABLE)
    try:
        pl = PipeLine(rgb888p_size=rgb888p_size, display_mode="auto")
        pl.create()
        display_size = pl.get_display_size()
        # person_det 为自定义的 YOLOv8 行人检测类，继承自 AIBase
        person_det = PersonDetectionApp(...)
        person_det.config_preprocess()

        # 初始化多目标跟踪器，注意 bbox_format 要与检测结果的框格式一致
        tracker = mot.ByteTrack(track_thresh=0.5, high_thresh=0.6, match_thresh=0.8,
                                track_buffer=30, frame_rate=30, min_hits=1,
                                class_aware=True, bbox_format="xywh")

        while True:
            os.exitpoint()
            with ScopedTiming("total", 1):
                img = pl.get_frame()
                dets = person_det.run(img)
                tracks = update_tracker(tracker, dets)
                # tracks 中每个元素带有稳定的 track_id，可直接用于绘制或计数
                person_det.draw_result(pl, tracks)
                pl.show_image()
                gc.collect()
    except KeyboardInterrupt:
        print("ByteTrack stopped")
    finally:
        os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
        # 释放顺序：跟踪器 -> AI 模型 -> PipeLine
        if tracker is not None:
            tracker.close()
        if person_det is not None:
            person_det.deinit()
        if pl is not None:
            pl.destroy()
        gc.collect()
```

使用 `DeepSort` 时需要额外为每个检测框提取 ReID 特征再传入：

```python
tracker = mot.DeepSort(feature_dim=128, max_cosine_distance=0.2, nn_budget=100,
                       max_iou_distance=0.7, max_age=30, n_init=3,
                       class_aware=True, bbox_format="xywh")

features = []
for det_box in boxes:
    # feature_app 为自定义的 ReID 特征提取类，对每个框裁剪后送入特征模型
    features.append(feature_app.run_feature(img, det_box))
tracks = tracker.update(boxes, scores, class_ids, features)
```

<a id="mot-tips"></a>

## 开发Tips

- **先调检测，再调跟踪**。跟踪质量的上限由检测决定，检测框闪烁或漏检严重时，任何跟踪算法都救不回来。
- **ID 频繁跳变**：说明轨迹被过早删除，适当增大 `track_buffer`（ByteTrack/BoTSort）或 `max_age`（OCSort/DeepSort）；也可放宽 `match_thresh` / `iou_threshold`。
- **出现大量虚假轨迹**：提高新建轨迹的阈值（`high_thresh` / `new_track_thresh` / `det_thresh`），或增大 `min_hits` / `n_init` 让轨迹需要更多次确认才输出。
- **`frame_rate` 要填实际帧率**。ByteTrack 和 BoTSort 用 `track_buffer * frame_rate / 30` 换算轨迹存活帧数，帧率填错会让轨迹保留时间偏离预期。
- **多类别场景保持 `class_aware=True`**，否则不同类别的目标可能互相抢占 ID。
- **优先选 ByteTrack**。DeepSort 和开启 ReID 的 BoTSort 每帧要为每个检测框额外跑一次特征模型，目标较多时帧率下降非常明显，只有在确实需要长时遮挡后保持 ID 时才使用。
