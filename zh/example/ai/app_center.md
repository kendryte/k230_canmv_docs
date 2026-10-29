# 应用中心（APP Center）

## 简介

应用中心是一个基于 LVGL 的图形化 Demo 启动器，位于开发板的 `CanMV/sdcard/examples/28-APP_CENTER` 目录。它把 30 多个 AI 和 CV 示例整合到一个带触摸交互的界面里：开机进入首页图标网格，点击图标即可启动对应示例，再点击停止返回首页，不需要在 IDE 里反复打开和切换脚本。

对开发者而言，应用中心同时也是一份**多应用共存的工程范例**，展示了如何在有限内存下做应用切换、资源回收和显示适配。

主要特性：

- **图标网格首页**，分页展示，支持触摸点选。
- **中英文界面切换**，语言选择持久化保存在 `/sdcard/app_center_language.txt`。
- **自适应显示**：卡片、页脚、状态栏均按实际显示分辨率布局，不同尺寸的屏幕都能正常显示。
- **运行时状态栏**：显示当前帧率、检测数量、Wi-Fi 连接状态。
- **模型缺失检测**：启动应用前先检查 kmodel 和资源文件是否存在，缺失时给出明确提示而不是直接崩溃。
- **严格的资源回收**：每个应用停止时彻底释放模型和 media 资源，保证下一个应用能正常加载。

## 运行方法

打开 CanMV IDE K230，选择左上角 `文件(F)` -> `打开文件`，选择 **此电脑->CanMV->sdcard->examples->28-APP_CENTER->main.py**，点击 IDE 左下角运行按钮。

若希望开机自动进入应用中心，把 `main.py` 复制到 `/sdcard` 根目录（或参考 [如何将调试好的脚本设置为自启动](../../ai_dev_doc.md#faq-script-autostart)）。

```{admonition} 注意
:class: warning
应用中心需要**触摸屏**才能交互。使用 HDMI 输出且没有触摸设备时，界面可以显示但无法点选。IDE 的虚拟触摸也被支持，可在 IDE 画面上直接点击。
```

```{admonition} 提示
应用中心会加载 `/sdcard/examples/15-LVGL/data/font/` 下的字体文件和 `/sdcard/examples/utils/icons/` 下的图标。若这些目录缺失，界面会显示异常，请确认镜像完整。
```

## 内置应用列表

| 分类 | 应用 |
|------|------|
| 人脸 | 人脸检测、人脸注册、人脸识别、人脸关键部位、人脸姿态、人脸解析、人脸3D网格、人脸活体检测 |
| 人体 | 人体检测、人体关键点检测、人体分割、跌倒检测 |
| 手部 | 手掌检测、手掌关键点分类、动态手势识别 |
| 通用检测 | YOLO 目标检测、YOLO 分割、YOLO 旋转目标检测 |
| 车牌与 OCR | 车牌识别、YOLO 车牌检测、OCR 识别 |
| 其它 AI | 单目标跟踪、自学习、注视估计、关键词唤醒、中文文本转语音 |
| CV（cv_lite） | 边缘检测、直线检测、圆检测、矩形检测 |
| CV（OpenMV） | 边缘检测、直线检测、圆检测、矩形检测 |
| 系统 | 系统信息、Wi-Fi 配置 |

完整注册表见 `runner.py` 中的 `DEMO_REGISTRY`。

## 代码结构

| 文件 | 职责 |
|------|------|
| `main.py` | 入口与主循环。初始化显示、LVGL、触摸，驱动首页与应用切换 |
| `config.py` | 全局常量：显示配置、主题配色、资源路径。`DISPLAY_TYPE=None` 表示按开发板型号自动选屏；`main.py` 在 `Display.init()` 之后用实际分辨率回填 `DISPLAY_WIDTH/HEIGHT` |
| `center.py` | 首页图标网格与分页 |
| `runner.py` | 应用注册表 `DEMO_REGISTRY`、应用加载、运行线程、资源文件检查 |
| `app_contract.py` | 应用协议基类 `Application`，定义生命周期 |
| `app_display.py` / `app_visual.py` | 显示与绘制封装 |
| `ui_layout.py` / `lvgl_utils.py` / `overlay.py` / `splash.py` | 界面布局、LVGL 辅助、运行时叠加层、启动画面 |
| `touch.py` | 触摸输入驱动，同时支持物理触摸和 IDE 虚拟触摸 |
| `i18n.py` | 中英文文案与语言持久化 |
| `model_cleanup.py` | 模型资源回收辅助函数，见 [AI资源管理与内存优化](../../ai_dev_doc.md#multi-model-switching) |
| `demo_common.py` | 各应用共用的模型路径和资源路径常量 |
| `demo_*.py` | 各个具体应用 |

## 应用协议

每个应用继承 `app_contract.Application`（AI 应用通常同时继承 `AIBase`），实现下面几个方法即可被应用中心调度：

| 成员 | 说明 |
|------|------|
| `name` | 应用显示名称 |
| `model_path` | kmodel 路径，启动前会检查文件是否存在 |
| `required_files` | 其它必需资源文件列表（如 anchors、字典），同样会做存在性检查 |
| `create(display)` | 类方法，创建实例并注入显示对象 |
| `open()` / `start()` | 初始化资源、启动 sensor |
| `run_once()` | 处理一帧，返回本帧结果数量；交互式应用在预览/暂停时可返回 `None`，这些帧不计入帧率统计 |
| `request_stop()` | **只置标志位，不释放资源**。该方法从 LVGL 线程调用，而资源在应用自己的线程中创建，跨线程释放会出问题 |
| `should_run()` | 返回是否应继续运行 |
| `_release_owned_resources()` | 最终清理钩子，保证只被调用一次 |

```{admonition} 注意
:class: warning
`Application` 基类**刻意不涉及** Sensor、Media、KPU、音频、图像格式和分辨率策略——这些都由各应用自己决定和释放。这样设计的目的是让纯 CV 应用、音频应用和视觉 AI 应用能共用同一套调度框架。
```

### 添加自己的应用

1. 新建 `demo_myapp.py`，定义一个继承 `Application`（需要 AI 推理时再继承 `AIBase`）的类，参考 `demo_face_detect.py`。
2. 在 `runner.py` 的 `DEMO_REGISTRY` 中加一行：`"myapp": ("demo_myapp", "MyAppDemo")`。
3. 在 `center.py` 的 `SHORT_MAP` 中为它加一个两字母缩写（没有图标文件时用于占位）。
4. 在 `i18n.py` 中补充中英文名称。

```{admonition} 提示
应用模块是**按需导入**的（`runner._load_demo` 用 `__import__`），某个可选应用写坏了不会影响应用中心本身和其它应用的加载。
```

## 开发Tips

- **资源释放是第一原则**。应用中心的核心难点不是界面，而是在有限内存下反复加载/卸载模型。新增应用时务必实现 `_release_owned_resources()`，并参考 [AI资源管理与内存优化](../../ai_dev_doc.md#ai-resource-management)。
- **不要在 LVGL 线程里释放资源**。`request_stop()` 只置标志，真正的释放发生在应用线程发现标志后退出循环时。
- **布局要用实际分辨率**。`config.CAM_WIN_W/H` 在 `Display.init()` 之后才被回填成真实值，不要在导入期就用它们计算布局。
- **帧率低时先看模型而不是界面**。LVGL 界面刷新只在状态变化时触发，主循环的开销集中在模型推理上。
