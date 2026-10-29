# `mot` Module API Manual

## Overview

`mot` (Multi-Object Tracking) is a built-in multi-object tracking native module in CanMV, used to assign **stable target IDs** to detection model outputs. Detection models perform inference independently for each frame, with no correlation between the same person in two adjacent frames; `mot` performs data association and Kalman prediction on top of detection results, allowing the same target to maintain the same `track_id` throughout the video, enabling applications such as counting, trajectory drawing, and boundary-crossing detection.

The module provides four tracking algorithms:

| Class | Algorithm | Requires ReID Features | Use Case |
|----|------|------|------|
| `mot.ByteTrack` | ByteTrack | No | **Recommended default choice**. Pure IoU association, fastest speed, minimal overhead; uses low-score detection boxes to recover occluded targets |
| `mot.OCSort` | OC-SORT | No | Scenarios where target motion is irregular, with frequent acceleration/deceleration or turning; better trajectory recovery after occlusion |
| `mot.DeepSort` | DeepSort | **Yes (required)** | Scenarios where targets have distinct appearances and need to maintain the same ID after long-term occlusion. Requires an additional ReID feature model, with a significant drop in frame rate |
| `mot.BoTSort` | BoT-SORT | Optional | Enhanced version of ByteTrack. When `reid_enabled=True`, fuses appearance features, with the highest accuracy and the largest overhead |

```{admonition} Tip
:class: note
`mot` only does tracking, not detection. Before use, you need an object detection model (such as YOLOv8 pedestrian detection) to output detection boxes. `DeepSort` and `BoTSort` with ReID enabled also require an additional ReID feature extraction model.

Corresponding examples are located in the `CanMV/sdcard/examples/05-AI-Demo` directory on the development board: `bytetrack.py`, `ocsort.py`, `deepsort.py`, `botsort.py`.
```

## API Introduction

### Common Description

The constructors of all four classes **only accept keyword arguments**, positional arguments are not supported. The following two parameters are common to all four classes:

| Parameter Name | Description | Explanation | Type |
|----------|------|------|------|
| class_aware | Whether to track by class | When `True`, only detection boxes of the same class can be associated with existing tracks, avoiding ID class mixing in multi-class scenarios; when `False`, class is ignored. Default `True` | bool |
| bbox_format | Detection box format | `'xyxy'` means `[x1,y1,x2,y2]` (top-left and bottom-right coordinates), `'xywh'` means `[x,y,w,h]` (top-left coordinates + width and height). This setting applies to both the `update()` input and the `bbox` in the returned results. Default `'xyxy'`, other values will raise `ValueError` | str |

All threshold-type parameters must be finite floating-point numbers within the interval `[0, 1]`, otherwise `ValueError` is raised.

### mot.ByteTrack

**Description**

Creates a ByteTrack tracker. The core idea of ByteTrack is "don't waste low-score boxes": first match high-score detection boxes with tracks in the first round, then use low-score detection boxes to recover tracks whose confidence has dropped due to occlusion.

**Syntax**

```python
import mot

tracker = mot.ByteTrack(track_thresh=0.5, high_thresh=0.6, match_thresh=0.8,
                        track_buffer=30, frame_rate=30, min_hits=1,
                        class_aware=True, bbox_format="xywh")
```

**Parameters**

| Parameter Name | Description | Explanation | Type | Default |
|----------|------|------|------|--------|
| track_thresh | High-score box threshold | Detection boxes with scores above this value participate in the first round of association; those below enter the second round of "recovery" association | float [0~1] | 0.5 |
| high_thresh | New track threshold | A new track is only created when an unmatched detection box has a score higher than this value. Must be **≥ `track_thresh`** | float [0~1] | 0.6 |
| match_thresh | Match threshold | Maximum IoU distance allowed for the first round of association; the larger the value, the easier it is to match | float [0~1] | 0.8 |
| track_buffer | Track retention frames | How many frames a track is retained after the target disappears, based on 30fps | int | 30 |
| frame_rate | Actual frame rate | Used together with `track_buffer` to convert the actual number of retained frames, formula is `track_buffer * frame_rate / 30` | int | 30 |
| min_hits | Number of hits required for confirmation | Only after a track has been hit this many consecutive times does it transition from `tentative` to `tracked` and get output | int | 1 |

**Return Value**

| Return Value | Description |
|--------|------|
| ByteTrack | ByteTrack tracker instance |

```{admonition} Note
:class: warning
If `high_thresh < track_thresh`, or `track_buffer`/`frame_rate`/`min_hits` is less than 1, the constructor raises `ValueError: invalid ByteTrack thresholds or lifetime`.
```

### mot.OCSort

**Description**

Creates an OC-SORT (Observation-Centric SORT) tracker. Compared to ByteTrack, it relies more on motion modeling, improving ID retention when targets reappear after occlusion through observation direction consistency (`inertia`) and virtual trajectory completion.

**Syntax**

```python
import mot

tracker = mot.OCSort(det_thresh=0.3, max_age=30, min_hits=3, iou_threshold=0.3,
                     delta_t=3, inertia=0.2, use_byte=False,
                     class_aware=True, bbox_format="xywh")
```

**Parameters**

| Parameter Name | Description | Explanation | Type | Default |
|----------|------|------|------|--------|
| det_thresh | Detection box threshold | Detection boxes with scores below this value do not participate in creating new tracks | float [0~1] | 0.3 |
| max_age | Maximum track survival frames | How many consecutive frames without matching before the target's track is deleted | int | 30 |
| min_hits | Number of hits required for confirmation | Only after a track accumulates this many hits does it get output | int | 3 |
| iou_threshold | IoU association threshold | Minimum IoU between detection boxes and track predicted boxes | float [0~1] | 0.3 |
| delta_t | Velocity estimation span | Use the positions of the previous `delta_t` frames to estimate target motion direction; the larger the value, the smoother the direction but the slower the response | int | 3 |
| inertia | Direction consistency weight | Weight of motion direction consistency in the association cost | float [0~1] | 0.2 |
| use_byte | Whether to enable low-score box recovery | When `True`, borrows ByteTrack's two-round association strategy | bool | False |

**Return Value**

| Return Value | Description |
|--------|------|
| OCSort | OCSort tracker instance |

```{admonition} Note
:class: warning
`max_age`, `min_hits`, `delta_t` must all be ≥ 1, otherwise `ValueError: age, hits, and delta_t must be positive` is raised.
```

### mot.DeepSort

**Description**

Creates a DeepSort tracker. In addition to motion association, it adds **appearance feature (ReID) association**, maintaining a feature library for each track and using cosine distance for matching. **The `features` parameter must be passed when calling `update()`**.

**Syntax**

```python
import mot

tracker = mot.DeepSort(feature_dim=128, max_cosine_distance=0.2, nn_budget=100,
                       max_iou_distance=0.7, max_age=30, n_init=3,
                       class_aware=True, bbox_format="xywh")
```

**Parameters**

| Parameter Name | Description | Explanation | Type | Default |
|----------|------|------|------|--------|
| feature_dim | Feature dimension | **Required**, the length of the feature vector output by the ReID model, must be ≥ 1, and must exactly match the feature length actually passed to `update()` | int | None |
| max_cosine_distance | Maximum cosine distance | Maximum cosine distance allowed for appearance matching; the smaller the value, the stricter | float [0~1] | 0.2 |
| nn_budget | Feature library capacity | Maximum number of historical features saved per track; the oldest are discarded when exceeded | int | 100 |
| max_iou_distance | Maximum IoU distance | Maximum distance allowed for IoU matching as a fallback after appearance matching fails | float [0~1] | 0.7 |
| max_age | Maximum track survival frames | How many consecutive frames without matching before the target's track is deleted | int | 30 |
| n_init | Number of hits required for confirmation | Only after a track has been hit this many consecutive times does it get output | int | 3 |

**Return Value**

| Return Value | Description |
|--------|------|
| DeepSort | DeepSort tracker instance |

```{admonition} Note
:class: warning
`feature_dim`, `nn_budget`, `max_age`, `n_init` must all be ≥ 1, otherwise `ValueError: feature_dim, budget, age, and n_init must be positive` is raised.
```

### mot.BoTSort

**Description**

Creates a BoT-SORT tracker. Based on ByteTrack's two-round association, it optionally adds appearance feature matching. When `reid_enabled=False`, behavior is similar to ByteTrack and no features need to be passed; when `reid_enabled=True`, features must be passed.

**Syntax**

```python
import mot

# Pure motion mode, no ReID model required
tracker = mot.BoTSort(reid_enabled=False, track_high_thresh=0.6, track_buffer=30,
                      class_aware=True, bbox_format="xywh")

# Enable appearance matching
tracker = mot.BoTSort(feature_dim=128, reid_enabled=True,
                      track_high_thresh=0.6, track_low_thresh=0.1,
                      new_track_thresh=0.7, track_buffer=30, match_thresh=0.7,
                      proximity_thresh=0.5, appearance_thresh=0.25,
                      appearance_weight=0.985, frame_rate=30, min_hits=1,
                      class_aware=True, bbox_format="xywh")
```

**Parameters**

| Parameter Name | Description | Explanation | Type | Default |
|----------|------|------|------|--------|
| feature_dim | Feature dimension | Length of the ReID feature vector. When `reid_enabled=False`, this value is forced to 0 and ignored; when `reid_enabled=True`, it must be ≥ 1 | int | 0 |
| reid_enabled | Whether to enable appearance matching | When `True`, `features` must be passed to `update()` | bool | False |
| track_high_thresh | High-score box threshold | Detection boxes with scores above this value participate in the first round of association | float [0~1] | 0.6 |
| track_low_thresh | Low-score box threshold | Detection boxes with scores below this value are discarded directly. Must be **≤ `track_high_thresh`** | float [0~1] | 0.1 |
| new_track_thresh | New track threshold | A new track is only created when an unmatched detection box has a score higher than this value. Must be **≥ `track_high_thresh`** | float [0~1] | 0.7 |
| track_buffer | Track retention frames | Used together with `frame_rate` to convert the actual number of retained frames, formula is `track_buffer * frame_rate / 30` | int | 30 |
| match_thresh | Match threshold | Maximum distance allowed for the first round of association | float [0~1] | 0.7 |
| proximity_thresh | Spatial proximity threshold | Only detection boxes with sufficiently large IoU are allowed to participate in appearance matching, preventing false matches at long distances | float [0~1] | 0.5 |
| appearance_thresh | Appearance match threshold | Maximum cosine distance allowed for appearance matching | float [0~1] | 0.25 |
| appearance_weight | Appearance weight | Fusion weight of appearance cost and motion cost | float [0~1] | 0.985 |
| frame_rate | Actual frame rate | Used together with `track_buffer` to convert track retention frames | int | 30 |
| min_hits | Number of hits required for confirmation | Only after a track has been hit this many times does it get output | int | 1 |

**Return Value**

| Return Value | Description |
|--------|------|
| BoTSort | BoTSort tracker instance |

```{admonition} Note
:class: warning
If `track_low_thresh > track_high_thresh`, `new_track_thresh < track_high_thresh`, `max_age < 1`, `min_hits < 1`, or ReID is enabled but `feature_dim < 1`, the constructor raises `ValueError: invalid BoTSORT parameters`.
```

### update

**Description**

Inputs the detection results of the current frame, advances the tracker by one frame, and returns the list of **active** tracks for this frame. The `update` interface is identical for all four tracker classes.

**Syntax**

```python
tracks = tracker.update(boxes, scores, class_ids)
tracks = tracker.update(boxes, scores, class_ids, features)   # DeepSort / BoTSort(reid)
```

**Parameters**

| Parameter Name | Description | Input / Output | Explanation |
|----------|------|-----------|------|
| boxes | Detection box list | Input | Each element is a sequence of length 4, the format is determined by `bbox_format` at construction time |
| scores | Score list | Input | Same length as `boxes`, each value must be within the interval `[0, 1]` |
| class_ids | Class index list | Input | Same length as `boxes`, each value must be a non-negative integer |
| features | ReID feature list | Input | Optional. Same length as `boxes`, each row's length must equal `feature_dim`. **Required** for `DeepSort` and `BoTSort` with ReID enabled; passing it to other trackers will raise an error |

**Return Value**

| Return Value | Description |
|--------|------|
| list[dict] | List of active tracks for this frame, see [Track Result Format](#track-result-format) for field descriptions |

```{admonition} Note
:class: warning
When no targets are detected in the current frame, **`tracker.update([], [], [])` must still be called** to let the tracker advance the frame count and eliminate expired tracks according to `max_age`. Missing calls will cause tracks to never be released after targets disappear.

`ValueError` is raised when the input data is invalid; common reasons: the three lists have inconsistent lengths, detection boxes do not have 4 values, box width and height are not positive, scores are outside `[0,1]`, class is negative, feature rows or dimensions do not match, or feature vector is all zeros.
```

### tracks

**Description**

Queries the tracks currently held by the tracker without advancing the frame count. Unlike the return value of `update()`, this interface can additionally return tracks in the `lost` state.

**Syntax**

```python
active = tracker.tracks()                     # Tracks visible only in this frame
all_tracks = tracker.tracks(include_lost=True)  # Includes temporarily lost tracks
```

**Parameters**

| Parameter Name | Description | Input / Output | Explanation |
|----------|------|-----------|------|
| include_lost | Whether to include lost tracks | Input | Keyword parameter. `False` (default) returns only tracks updated in this frame, equivalent to the result of the most recent `update()`; when `True`, returns **all tracks that have not been deleted**, including active tracks that did not match in this frame (`time_since_update > 0`) and tracks in the `lost` state. Tracks in the `removed` state are not returned in either case |

**Return Value**

| Return Value | Description |
|--------|------|
| list[dict] | Track list, see [Track Result Format](#track-result-format) for field descriptions |

### reset

**Description**

Clears all tracks and resets the frame count to zero, returning the tracker to its just-created state. Used when switching scenes or video sources, to prevent old scene IDs from continuing into new scenes.

**Syntax**

```python
tracker.reset()
```

**Return Value**

| Return Value | Description |
|--------|------|
| None | |

### frame_id

**Description**

Gets the frame sequence number processed by the tracker, i.e., the cumulative number of `update()` calls. Reset to zero after `reset()`.

**Syntax**

```python
n = tracker.frame_id()
```

**Return Value**

| Return Value | Description |
|--------|------|
| int | Number of frames processed |

### close

**Description**

Releases the native resources occupied by the tracker. Must be called before program exit, usually placed in a `finally` block. Equivalent to `__del__`, but does not need to wait for garbage collection to trigger.

**Syntax**

```python
tracker.close()
```

**Return Value**

| Return Value | Description |
|--------|------|
| None | |

```{admonition} Note
:class: warning
Calling `update()`, `tracks()`, `reset()`, `frame_id()` after `close()` raises `ValueError: tracker is closed`.
```

<a id="track-result-format"></a>

## Track Result Format

Each element in the list returned by `update()` and `tracks()` is a dict:

| Key | Type | Description |
|----|------|------|
| track_id | int | Unique track ID. Remains unchanged for the same target throughout the video; this is the basis for counting and track drawing |
| class_id | int | Target class index, from the `class_ids` passed to `update()` |
| bbox | tuple[float, float, float, float] | Current track bounding box, in the same format as the `bbox_format` during construction. Note that this is the box after the tracker's **smoothing/prediction**, and is not exactly identical to the input detection box |
| score | float | Target confidence score |
| state | str | Track state: `tentative` (newly created, awaiting confirmation), `tracked` (normally tracking), `lost` (temporarily lost, awaiting recovery). Tracks in the `removed` state will not be returned |
| age | int | Total number of frames since the track was created |
| hits | int | Cumulative number of times the track has matched a detection box |
| time_since_update | int | Number of frames since the last match with a detection box. `0` means visible in the current frame |

## Example Program

Below is a complete tracking workflow for YOLOv8 pedestrian detection + ByteTrack. For the full code, refer to `05-AI-Demo/bytetrack.py` on the development board:

```python
from libs.PipeLine import PipeLine
from libs.Utils import *
import os, gc
import mot

def update_tracker(tracker, dets):
    # dets is the detection result, dets[0] is the box list, dets[2] is the score list
    boxes = dets[0]
    if not boxes:
        # update() must be called even when no targets are detected, to advance the frame count and remove expired tracks
        return tracker.update([], [], [])
    scores = dets[2]
    class_ids = [0] * len(boxes)      # single class (pedestrian), all class indices are 0
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
        # person_det is a custom YOLOv8 pedestrian detection class, inheriting from AIBase
        person_det = PersonDetectionApp(...)
        person_det.config_preprocess()

        # Initialize the multi-object tracker; note that bbox_format must match the box format of the detection result
        tracker = mot.ByteTrack(track_thresh=0.5, high_thresh=0.6, match_thresh=0.8,
                                track_buffer=30, frame_rate=30, min_hits=1,
                                class_aware=True, bbox_format="xywh")

        while True:
            os.exitpoint()
            with ScopedTiming("total", 1):
                img = pl.get_frame()
                dets = person_det.run(img)
                tracks = update_tracker(tracker, dets)
                # each element in tracks carries a stable track_id, which can be directly used for drawing or counting
                person_det.draw_result(pl, tracks)
                pl.show_image()
                gc.collect()
    except KeyboardInterrupt:
        print("ByteTrack stopped")
    finally:
        os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
        # release order: tracker -> AI model -> PipeLine
        if tracker is not None:
            tracker.close()
        if person_det is not None:
            person_det.deinit()
        if pl is not None:
            pl.destroy()
        gc.collect()
```

When using `DeepSort`, ReID features need to be extracted for each detection box before being passed in:

```python
tracker = mot.DeepSort(feature_dim=128, max_cosine_distance=0.2, nn_budget=100,
                       max_iou_distance=0.7, max_age=30, n_init=3,
                       class_aware=True, bbox_format="xywh")

features = []
for det_box in boxes:
    # feature_app is a custom ReID feature extraction class that crops each box and feeds it into the feature model
    features.append(feature_app.run_feature(img, det_box))
tracks = tracker.update(boxes, scores, class_ids, features)
```

<a id="mot-tips"></a>

## Development Tips

- **Tune detection first, then tracking.** The upper bound of tracking quality is determined by detection; when detection boxes flicker or have severe misses, no tracking algorithm can save it.
- **Frequent ID switches**: indicates tracks are being removed too early. Appropriately increase `track_buffer` (ByteTrack/BoTSort) or `max_age` (OCSort/DeepSort); you can also relax `match_thresh` / `iou_threshold`.
- **Many false tracks appearing**: raise the threshold for creating new tracks (`high_thresh` / `new_track_thresh` / `det_thresh`), or increase `min_hits` / `n_init` so that tracks require more confirmations before being output.
- **`frame_rate` should be the actual frame rate.** ByteTrack and BoTSort use `track_buffer * frame_rate / 30` to convert track survival frame count; an incorrect frame rate will cause the track retention time to deviate from expectations.
- **Keep `class_aware=True` in multi-class scenarios**, otherwise targets of different classes may compete for IDs.
- **Prefer ByteTrack.** DeepSort and BoTSort with ReID enabled require an additional feature model run for each detection box every frame; with many targets, the frame rate drops significantly. Only use them when you really need to maintain IDs after long-term occlusion.
