# AI开发文档

## KPU硬件基本原理介绍

在边缘计算场景中（如物联网设备、智能摄像头、工业检测终端、可穿戴设备等），设备通常部署在远离云端数据中心的现场，面临着**实时性要求高、网络带宽受限、数据隐私敏感以及功耗约束严格**的挑战。在这些场景下运行复杂的AI模型（如图像识别、目标检测、语音唤醒），如果仅依赖传统的通用CPU进行计算，往往会遇到**计算量过大、处理速度慢、功耗过高**的问题，难以满足实时响应和能效比的要求。

**KPU（Knowledge Processing Unit）** 是嘉楠科技专为应对边缘AI计算挑战而设计的硬件加速引擎。它本质上是一个高度优化的**深度学习协处理器/加速器**，其核心功能是**高效执行神经网络模型中的密集计算任务**（特别是卷积、矩阵乘法、激活函数等操作）。

**KPU的核心优势**：专精与高效, 与通用CPU相比，KPU的优势在于其**专用化架构**：

- **并行计算能力：** KPU内部包含大量专为神经网络计算设计的处理单元（PE），能够同时处理海量数据（如特征图、权重），显著加速模型推理过程。
- **优化的数据流与内存访问：** 针对神经网络计算模式（如数据复用）进行深度优化，减少不必要的数据搬运，最大化利用内存带宽，降低延迟。
- **高能效比：** 专用电路设计避免了CPU执行通用指令的开销，在执行相同的AI计算任务时，KPU通常能提供**数十倍甚至上百倍于CPU的计算效率（TOPS/W）**，在有限的边缘设备功耗预算内实现高性能AI处理。
- **降低CPU负载：** 将繁重的AI计算任务卸载（Offload）到KPU执行，释放宝贵的CPU资源去处理设备控制、通信、用户交互等其他关键任务，提升系统整体响应能力和稳定性。

KPU支持各种主流的神经网络模型结构，适用于广泛的边缘视觉AI应用场景，包括但不限于：

- **图像分类：** 识别图像中的物体类别（如识别水果种类、工业零件）。
- **目标检测：** 定位并识别图像中的多个目标及其位置（如检测行人、车辆、缺陷）。
- **语义分割：** 对图像中的每个像素进行分类（如区分道路、天空、建筑物；医疗图像分析）。
- **人脸检测与识别：** 设备端的人脸验证、门禁考勤。
- **姿态估计：** 分析人体关节位置（如健身动作指导）。

**KPU在系统中的定位：**

它通常作为SoC（System on Chip）中的一个独立IP核存在，与CPU、内存、外设等协同工作。CPU负责系统管理、任务调度和应用逻辑，而将计算密集型的AI模型推理任务高效地交给KPU执行。下图展示了KPU在典型边缘AI SoC中的位置。

![kpu_in_system](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/dc607bf20ffc.png)

## K230 AI 应用示例展示

为了帮助开发者快速上手并直观体验 K230 强大的边缘 AI 能力，CanMV K230 镜像内置了丰富多样的 AI 示例程序 (AI Demo)。

这些开箱即用的 Demo 涵盖了单模型应用（如人脸检测）和多模型应用（如手掌关键点）两大类别，用户无需从零搭建环境，即可通过零配置、一键运行的方式，体验主流 AI 功能，包括但不限于：

- 视觉应用： 物体识别、人脸检测、手势识别、人体识别、车牌识别、OCR 文字识别。
- 音频应用： 关键词识别 (KWS)、语音合成 (TTS) 等。

通过这些 Demo，开发者可以快速验证模型性能，熟悉 K230 的 AI 推理能力，为后续的定制化开发打下坚实基础。

**运行方式：**

所有 Demo 的源代码均开放、结构清晰、注释丰富，统一存放在 `/CanMV/sdcard/examples/05-AI-Demo` 目录下。用户可以通过 CanMV IDE 便捷地打开、运行、调试和深入研究这些代码，理解 API 调用、数据处理流程和模型集成方式，极大地加速自身应用的开发进程。

**注意事项：**

- 部分 Demo 因内存占用较高，在 K230D 芯片上可能无法正常运行，请参考下方链接中的适配表选择合适的示例进行测试。

- 关于K230和K230D的区别，请参考：**[产品中心](https://www.kendryte.com/zh/products)**

完整的 Demo 列表、K230/K230D 适配情况以及每个 Demo 的说明，统一维护在 **[AI Demo说明文档](./example/ai/ai_demo_user_manual.md#ai-demo-list)**，本文不再重复列出，避免两处数据不一致。

## AI模型推理的基本流程

把训练的AI模型部署在K230上的基本流程见下面的流程图：

![pipeline_model_deploy](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/587bcb799ab8.png)

🏷️ **数据采集**:

数据采集是指通过摄像头、麦克风等传感设备收集原始输入数据的过程。采集数据的质量与数量直接决定了模型训练与推理的效果。因此，选择合适的采集设备和策略至关重要。

为获得更好的部署效果，推荐使用 K230 本身采集图像数据，以确保数据分布更贴近实际部署环境。

🏷️ **数据标注**:

数据标注是为采集到的数据添加语义标签的过程，用于监督学习模型的训练。这一过程可以通过人工方式完成，也可以借助标注工具进行半自动化处理。

比如图像分类任务需要为每张图像分配正确的类别标签；目标检测任务要为图像中每个目标添加边界框及其类别标签。准确的标注对于训练出高性能、泛化能力强的模型至关重要。

🏷️ **模型训练**:

模型训练阶段是整个 AI 应用开发流程的重要步骤之一，其主要目标是利用已标注的数据集，通过深度学习方法训练出具有泛化能力的神经网络模型。在这一过程中，模型通过不断地调整内部参数，逐步拟合数据的分布特征，以便在面对未见过的输入数据时，仍能做出准确且稳定的预测结果。

模型训练通常需要依托大量高质量的样本数据，涵盖任务相关的多样性场景与类别。数据的充分性和标注的准确性直接影响模型的学习效果和应用表现。在训练过程中，神经网络模型会从输入数据中提取特征，计算预测输出，并通过与真实标签对比产生损失（Loss），再借助反向传播机制调整网络中的权重参数，不断优化模型的性能。

为了实现高效的训练，开发者需要选择一个适合当前任务的模型结构，如图像分类中的 MobileNet、ResNet，目标检测中的 YOLO 系列等。模型的选择不仅取决于精度要求，还需考虑推理速度、模型体积和部署平台的资源约束等因素，特别是在面向 K230 这样的边缘 AI 芯片时，轻量化模型更具实际价值。

此外，训练过程往往需要在具备一定算力支持的计算平台（如 GPU 服务器或本地高性能工作站）上进行，以保证模型在合理时间内完成优化。现代深度学习训练通常使用成熟的训练框架，如 **PyTorch** 和 **TensorFlow**，它们提供了丰富的神经网络构建模块、优化器、损失函数及数据处理工具，极大地简化了模型开发流程。您可以根据自身的技术背景和模型需求，选择合适的框架开展训练工作。

🏷️ **模型转换和验证**:

由于边缘设备计算资源有限，不能直接部署在高算力平台训练得到的模型。必须通过模型转换工具对模型进行优化与量化，生成适用于目标硬件的推理格式。

对于 K230 芯片：

- 使用 KPU（Knowledge Processing Unit） 作为神经网络加速单元；
- 支持的模型格式为 KModel；
- 使用 nncase 编译器 将训练好的 ONNX 或 TFLite 模型 转换为 KModel；
- 转换过程中会进行结构优化与量化，以减少模型体积和计算复杂度。

转换完成后，还需进行功能验证，确保模型在精度、延迟和资源使用方面满足应用需求。

🏷️ **模型部署**:

验证通过的 KModel 可以通过 K230 MicroPython SDK 提供的 API 加载到设备上运行。

部署流程通常包含以下几个步骤：

- 加载kmodel；
- 读取图像/音频等输入数据；
- 执行数据预处理（如缩放、归一化、通道排列等）；
- 运行模型推理；
- 执行结果后处理（如分类解码、边界框过滤等）；
- 绘制/输出推理结果。

不同模型的预处理和后处理流程可能不同，需根据具体模型手动适配相应代码逻辑。

🏷️ **模型调优**:

部署完成后，仍需对模型进行性能与效果上的调优，以适配边缘场景的实际需求。优化措施包括但不限于：

- 设置更合理的推理阈值或输出策略；
- 调整模型转换参数（如量化策略、输入分辨率）；
- 改进模型结构或训练超参数；
- 丰富并优化数据集；
- 优化推理流程（如线程调度、内存复用）。

模型调优是一个持续迭代的过程，有助于提升系统的稳定性、实时性与能效比。

以上六个步骤构成了在 K230 芯片 上完成 AI 模型部署与推理的完整流程。每一步均需精心设计与执行，以确保最终应用具备良好的性能、稳定性与用户体验。

## 训练模型

```{note}
🤖 **【场景定义】**：在 K230 开发板上实现“打印数字的识别与定位”。

📌 **任务背景**：
在很多 AI 应用中，我们经常会遇到“识别图片里的某些东西”的需求，比如识别图片中的人脸、物体，或者像本例中识别数字。为了更好地理解目标检测的基本流程，我们设计了一个简单的小任务————**识别打印纸上 “0”、“1”、“2”、“3” 这四种数字，并标出它们在图像中的位置**。

这个任务不复杂，但能完整地练习一遍从模型部署到图像处理、结果显示的整个过程。它作为一个入门教程，帮助大家快速掌握如何在 K230 平台上部署 AI 模型，进行目标检测，并将检测结果显示在屏幕上。

🎯 **项目目标**：
基于 Kendryte K230 AI SoC 平台，开发一个轻量级、高性能的视觉识别示例，实现以下功能：

* ✅ **识别类别**：仅识别“0”、“1”、“2”、“3”四类数字字符；
* ✅ **识别对象**：打印在纸张上的标准字体数字；
* ✅ **定位功能**：不仅识别数字类别，还能**准确获取每个数字在图像中的位置坐标**（框出检测框），为后续处理或操作提供基础；
* ✅ **运行平台**：应用部署在 K230 开发板，利用其**AI 硬件加速、摄像头输入、屏幕显示能力**，实现端侧推理、实时显示。

🖼 **预期效果图**：

![4_number_det](https://www.kendryte.com/api/post/attachment?id=635)
```

### 数据采集

```{note}
👉 采集训练数据其实很简单！你只需要先把 MicroPython 固件烧进开发板，然后找到那个脚本——/sdcard/examples/16-AI-Cube/DataCollectionCamera.py，把它改名为 main.py，放到 /sdcard 目录下。接着重新上电（也就是重启一下板子），运行起来后，按下板子上的key按键就可以开始采集啦！每按一下就拍一张照片，图像会自动保存到 /sdcard/examples/data/ 文件夹里，完全不用你管，超省心！
```

在训练模型之前，数据采集是整个流程中的第一步，也是至关重要的一步。高质量的数据不仅能提升模型的性能，还能增强模型在实际应用场景中的泛化能力。根据不同的应用需求，数据采集可以分为**通用场景**和**专用场景**两种情况，下面将分别进行详细说明。

📌 **通用场景下的数据采集**

在通用人工智能任务中，如图像分类、目标检测、语义分割等，通常可以借助已有的公开数据集来构建训练样本。这些数据集由学术机构、研究组织或大型企业整理发布，具有良好的标注质量和广泛的应用基础。

比如，常见图像类公开数据集包括：ImageNet、COCO、MNIST、Fashion-MNIST、CIFAR系列等，或者寻找网络上对应场景的开源数据集。

虽然公开数据集质量较高，但在实际使用前仍需进行适当的筛选与处理，以确保其符合项目需求：

- **质量保证处理**：去除模糊、错误标注或低质量样本。
- **类别平衡**：确保各类别样本数量均衡，避免模型偏向。
- **格式统一**：将数据转换为统一格式（如JPEG、PNG等）。
- **数据扩增**：通过旋转、裁剪、翻转、添加噪声等方式扩充数据量，提高模型鲁棒性。
- **构建定制化数据集**：有时单一数据集可能无法满足特定需求，可以通过组合多个数据集并进行重新标注和清洗，构建更符合业务场景的定制化数据集。

📌 **专用场景下的数据采集**

对于一些特殊行业或具体应用场景（如工业质检、农业监测、安防监控、医疗诊断等），往往需要采集专用于该场景的数据。这种情况下，公开数据集可能无法准确反映真实环境的数据分布，因此需要进行**定制化数据采集**。

在某些特定的AI部署场景中，有条件的情况下可以直接**使用K230设备**进行数据采集。这样**采集的数据更贴近实际部署环境，有助于提升模型在设备上的表现**。

⚠️ 这里给出一些数据采集流程建议：

- **明确采集目标**：定义采集对象（如物体类型、场景）、光照条件、角度、分辨率等。
- **明确数据任务**：不同的任务对数据集的要求不同，一方面要考虑实际部署场景，另一方面要考虑任务需求，比如分类任务可能需要物体占据较大的区域，大片的背景可能会影响分类效果；而目标检测可以有大小不同的多个物体。
- **使用合适工具**：使用K230开发板配合摄像头模块，可编写脚本自动采集。
- **同步标注信息**：在采集过程中尽量同步记录标签信息，便于后期标注。
- **初步质量检查**：剔除模糊、曝光过度、遮挡严重等无效样本。
  
### 数据标注

```{note}
👉 拿到采集好的图片之后，就可以开始给它们打标签啦！根据这个任务的要求，你可以用一些常见的标注工具，比如 LabelImg、Labelme 或 X-AnyLabeling，给图片里的数字加上对应的类别、画出目标框。你可以亲自采集图像、自己动手标注，整个过程也挺有趣的。当然啦，如果你不想从头做，我们也贴心准备了一份现成的“0/1/2/3四类打印数字识别”数据集，直接点这里就能下载：[0/1/2/3四类打印数字识别数据集](https://download.kendryte.com/developer/k230/yolo_dataset/number_det.zip)。省时又省力，直接上手训练也没问题！
```

数据标注是训练模型的关键步骤之一，它涉及到对原始数据进行标注，以便模型能够学习到数据的特征和模式。在进行数据标注时，需要考虑以下几个方面：

- **标注格式**：选择适合模型的标注格式，如XML、JSON、TXT等。
- **标注工具**：选择适合的标注工具，如LabelImg、Labelme、X-AnyLabeling、VIA等。
- **标注质量**：确保标注的准确性和一致性，避免标注错误。
- **标注策略**：根据任务需求和数据特点，选择合适的标注策略，如边界框标注、关键点标注等。

关于常见的视觉任务，这里推荐使用X-AnyLabeling进行标注。下载链接: [X-AnyLabeling-release](https://github.com/CVHub520/X-AnyLabeling/releases)。
  
### 模型训练

```{note}
👉 模型训练的方法有很多，其中 YOLO 系列是现在特别常用的选择，比如 YOLOv5、YOLOv8 或 YOLO11。我们推荐你用 YOLO 来进行训练，因为它效果好、速度快、社区也很活跃。更棒的是，我们提供的数据集已经整理好了，可以直接用来训练 YOLO 模型！你只需要跳转到这个示例：[YOLO检测示例](#yolov8-fall-detection)，按照里面的流程来做，把示例中的数据集部分换成我们准备的“0/1/2/3 四类打印数字识别数据集”就行啦。本节的目标是先把模型训练好，并导出为 ONNX 格式，后面还有更多有趣的内容等着你继续解锁！
```

模型训练是整个AI流程中最重要的一步，它涉及到模型的构建、训练和优化。在进行模型训练时，需要考虑以下几个方面：

- **模型选择**：根据任务需求和数据特点，选择适合的模型。
- **模型构建**：构建模型的网络结构，包括输入层、隐藏层和输出层。
- **模型训练**：使用标注好的数据进行模型训练，包括选择合适的损失函数和优化器。
- **模型评估**：使用测试集对模型进行评估，评估模型的性能和泛化能力。
- **模型优化**：根据模型评估结果，对模型进行优化，提高模型的性能和泛化能力。

训练好的模型需要转换成onnx模型或者tflite模型，准备后续使用nncase进行模型转换，得到可以在K230上推理的kmodel。

## 模型转换

当我们训练结束后，会得到一个 ONNX 模型文件。但这个模型还不能直接在 K230 上用 KPU 来跑，因为 KPU 只支持 Kmodel 格式。

所以接下来，我们要用一个叫 nncase 的编译器，把 ONNX 模型“翻译”成 Kmodel，这样 KPU 才能理解并运行它。

下面我们就来简单认识一下这个关键工具 —— nncase！

### 什么是 nncase

#### nncase 简介

`nncase` 是一款专为 AI 加速器设计的**神经网络编译器**，目前已支持的后端（target）包括：**CPU、K210、K510、K230** 等平台。

**nncase 提供的核心功能**

- 支持 **多输入多输出** 的网络结构，兼容常见的 **多分支模型拓扑**；
- 采用 **静态内存分配** 策略，无需依赖运行时堆内存，资源占用可控；
- 实现 **算子融合与图优化**，有效减少冗余计算，提升推理效率；
- 支持 **浮点（float）推理** 和 **定点量化推理（uint8/int8）**；
- 支持 **训练后量化（Post-Training Quantization, PTQ）**，可基于浮点模型和校准数据集生成高效的量化模型；
- 编译生成的模型为**平坦结构（Flat Model）**，具备 **零拷贝加载（Zero-Copy Loading）** 能力，适合资源受限的嵌入式场景。

**支持的模型格式**

nncase 支持从主流深度学习框架导出的以下模型格式：

- **TFLite（TensorFlow Lite）**
- **ONNX（Open Neural Network Exchange）**

您可以使用 PyTorch、TensorFlow 等训练框架导出模型至上述格式，再通过 nncase 转换为 KModel，以部署至 K230 等设备。

**架构概览**

![nncase架构](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/9e869eeb5b09.png)

nncase 的软件栈主要包括以下两大组成部分：

- **Compiler（编译器）**：将高层框架导出的 TFLite 或 ONNX 模型，转换为适用于目标硬件平台的 KModel 格式，并执行结构优化、算子调度与量化处理；
- **Runtime（运行时）**：在目标设备（如 K230）上加载并运行 KModel，结合硬件加速单元（如 KPU）实现高性能模型推理。

🏷️ **Compiler**: 用于在PC上编译神经网络模型，最终生成kmodel文件。主要包括importer, IR, Evaluator, Quantize, Transform优化, Tiling, Partition, Schedule, Codegen等模块。

- Importer: 将其它神经网络框架的模型导入到nncase中；
- IR: 中间表示, 分为importer导入的Neutral IR(设备无关)和Neutral IR经lowering转换生成的Target IR(设备相关)；
- Evaluator: Evaluator提供IR的解释执行能力，常被用于Constant Folding/PTQ Calibration等场景；
- Transform: 用于IR转换和图的遍历优化等；
- Quantize: 训练后量化, 对要量化的tensor加入量化标记, 根据输入的校正集, 调用 Evaluator进行解释执行, 收集tensor的数据范围, 插入量化/反量化结点, 最后优化消除不必要的量化/反量化结点等；
- Tiling: 受限于NPU较低的存储器容量，需要将大块计算进行拆分。另外，计算存在大量数据复用时选择Tiling参数会对时延和带宽产生影响；
- Partition: 将图按ModuleType进行切分, 切分后的每个子图会对应RuntimeModule, 不同类型的RuntimeModule对应不同的Device(CPU/K230)；
- Schedule: 根据优化后图中的数据依赖关系生成计算顺序并分配Buffer；
- Codegen: 对每个子图分别调用ModuleType对应的codegen，生成RuntimeModule；

🏷️ **Runtime**: 集成于用户应用程序（App）中，提供模型加载、输入设置、推理执行和输出读取等功能。Runtime 接口屏蔽了底层硬件差异，使开发者能更专注于模型推理逻辑的集成与应用开发。

模型转换章节主要介绍nncase compiler和simulator的使用方法。

#### 安装 nncase 环境

- **Linux 环境搭建 nncase**

首先，请安装 `.NET SDK 7.0` 并配置 `DOTNET_ROOT` 环境变量。**请注意，不建议在 Anaconda 虚拟环境中安装 `dotnet`，否则可能导致兼容性问题。**

```bash
sudo apt-get update
sudo apt-get install dotnet-sdk-7.0
export DOTNET_ROOT=/usr/share/dotnet
```

接下来，通过 pip 安装 `nncase` 和 `nncase-kpu`：

```bash
pip install nncase nncase-kpu
```

- **Windows 环境搭建 nncase**

首先安装 [.NET SDK 7.0](https://learn.microsoft.com/zh-cn/dotnet/core/install/windows)，请根据 Microsoft 官方文档完成安装流程。
安装 `nncase` 库。可通过 pip 在线安装主程序 `nncase`，并从 [GitHub Releases 页面](https://github.com/kendryte/nncase/releases) 下载对应版本的 `nncase_kpu`，再使用 pip 离线安装。

```bash
pip install nncase
# 请将 `2.x.x` 替换为实际下载版本号。
pip install nncase_kpu-2.x.x-py2.py3-none-win_amd64.whl
```

- **使用 Docker 搭建环境**

如果您未配置 Ubuntu 本地环境，可直接使用官方提供的 `nncase` Docker 镜像。该镜像基于 Ubuntu 20.04，预装了 Python 3.8 和 dotnet-sdk-7.0，方便快速启动。

```bash
cd /path/to/nncase_sdk
docker pull ghcr.io/kendryte/k230_sdk
docker run -it --rm -v `pwd`:/mnt -w /mnt ghcr.io/kendryte/k230_sdk /bin/bash
```

- **查看 nncase 版本信息**

进入 Python 交互环境后可通过如下命令确认当前安装的 `nncase` 版本：

```python
>>> import _nncase
>>> print(_nncase.__version__)
2.11.0
```

> 示例输出为 `2.11.0`，请以实际安装版本为准。

### 使用 nncase 编译器转换kmodel

![compile_kmodel](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/3a16288edfb5.jpg)

编译kmodel的流程主要包含以下关键步骤，每个步骤都有其特定的目的和技术考量：

**设置编译选项**：这一步的核心目的是为模型部署适配目标硬件平台。由于边缘计算设备需要明确指定运行平台以确保生成的kmodel是否需要利用硬件（kpu）加速。同时，配置预处理参数（如输入标准化参数）到kmodel内部可减少推理时的计算开销，提升整体效率。

**初始化编译器**：nncase编译器的初始化是为后续转换工作构建标准化环境。编译器根据前述配置的编译选项完成初始化过程。

**导入原始模型**：当前主流训练框架（如TensorFlow/PyTorch）生成的ONNX/TFLite模型包含通用运算符，但KPU作为专用加速器需要特定算子格式。此步骤通过模型解析和算子转换，将原始模型转化为编译器可优化的中间表示，为后续硬件相关优化奠定基础。

**量化处理**：这是提升边缘侧推理性能的关键环节。我们训练得到的FP32模型虽精度高但存在计算延迟大、内存占用高等问题。通过量化到INT8/INT16：显著减少模型体积，提升计算速度（利用硬件定点加速指令），降低功耗（减少内存带宽需求）。需注意的是，量化会引入精度损失，因此需要通过校准数据集帮助模型确定在量化过程中每一层权重和激活值应该被映射到的范围，以便保留更多的信息，减少量化误差。量化过程需要配置量化参数和校准数据，量化参数见[编译参数说明](#compilation-parameters)。

**编译生成kmodel**：在前述优化基础上，最终生成的kmodel是经过深度优化的可直接部署到K230设备执行高效推理。

#### 转换示例

我们就以**四类打印数字识别**场景为例，将上面得到的ONNX模型转换成Kmodel。这里给出编译示例脚本：

```python
# 导入所需库
import os
import argparse
import numpy as np
from PIL import Image  # 用于图像读取和处理
import onnxsim         # ONNX 模型简化工具
import onnx            # ONNX 模型处理工具
import nncase          # nncase 编译器 SDK
import shutil
import math

def parse_model_input_output(model_file, input_shape):
    # 加载ONNX模型
    onnx_model = onnx.load(model_file)
    
    # 获取模型中所有输入节点名称
    input_all = [node.name for node in onnx_model.graph.input]
    
    # 获取模型中已经被初始化的参数（如权重等），这些不属于输入数据
    input_initializer = [node.name for node in onnx_model.graph.initializer]
    
    # 真实输入 = 所有输入 - 初始化器
    input_names = list(set(input_all) - set(input_initializer))
    
    # 从图中提取真实输入张量
    input_tensors = [node for node in onnx_model.graph.input if node.name in input_names]

    # 提取输入张量的名称、数据类型、形状等信息
    inputs = []
    for _, e in enumerate(input_tensors):
        onnx_type = e.type.tensor_type
        input_dict = {}
        input_dict['name'] = e.name
        # 转换为NumPy数据类型
        input_dict['dtype'] = onnx.mapping.TENSOR_TYPE_TO_NP_TYPE[onnx_type.elem_type]
        # 如果某维为0，说明ONNX模型未固定shape，使用传入的input_shape代替
        input_dict['shape'] = [(i.dim_value if i.dim_value != 0 else d) for i, d in zip(onnx_type.shape.dim, input_shape)]
        inputs.append(input_dict)

    return onnx_model, inputs

def onnx_simplify(model_file, dump_dir, input_shape):
    # 获取模型和输入形状信息
    onnx_model, inputs = parse_model_input_output(model_file, input_shape)

    # 自动推断缺失的shape信息
    onnx_model = onnx.shape_inference.infer_shapes(onnx_model)

    # 构造用于onnxsim的输入shape映射
    input_shapes = {input['name']: input['shape'] for input in inputs}

    # 简化模型
    onnx_model, check = onnxsim.simplify(onnx_model, input_shapes=input_shapes)
    assert check, "模型简化校验失败"

    # 保存简化后的模型
    model_file = os.path.join(dump_dir, 'simplified.onnx')
    onnx.save_model(onnx_model, model_file)
    return model_file

def read_model_file(model_file):
    with open(model_file, 'rb') as f:
        model_content = f.read()
    return model_content

def generate_data(shape, batch, calib_dir):
    # 获取数据集中的所有图片路径
    img_paths = [os.path.join(calib_dir, p) for p in os.listdir(calib_dir)]
    data = []

    for i in range(batch):
        assert i < len(img_paths), "校准图片数量不足"

        # 加载图片，转换为RGB格式
        img_data = Image.open(img_paths[i]).convert('RGB')

        # 按模型输入尺寸进行缩放
        img_data = img_data.resize((shape[3], shape[2]), Image.BILINEAR)

        # 转换为NumPy数组
        img_data = np.asarray(img_data, dtype=np.uint8)

        # 转换为 NCHW 格式
        img_data = np.transpose(img_data, (2, 0, 1))

        # 增加batch维度
        data.append([img_data[np.newaxis, ...]])

    return np.array(data)

def main():
    # 命令行参数定义
    parser = argparse.ArgumentParser(prog="nncase")
    parser.add_argument("--target", default="k230", type=str, help='编译目标，例如k230或cpu')
    parser.add_argument("--model", type=str, help='输入ONNX模型路径')
    parser.add_argument("--dataset_path", type=str, help='PTQ校准数据集路径')
    parser.add_argument("--input_width", type=int, default=320, help='模型输入宽度')
    parser.add_argument("--input_height", type=int, default=320, help='模型输入高度')
    parser.add_argument("--ptq_option", type=int, default=0, help='PTQ选项：0-5')

    args = parser.parse_args()

    # 输入尺寸向上对齐到32的整数倍，符合硬件要求
    input_width = int(math.ceil(args.input_width / 32.0)) * 32
    input_height = int(math.ceil(args.input_height / 32.0)) * 32
    input_shape = [1, 3, input_height, input_width]  # NCHW格式

    # 创建临时目录保存中间模型
    dump_dir = 'tmp'
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    # 简化模型
    model_file = onnx_simplify(args.model, dump_dir, input_shape)

    # 编译选项设置
    compile_options = nncase.CompileOptions()
    compile_options.target = args.target                  # 指定目标平台
    compile_options.preprocess = True                     # 启用预处理
    compile_options.swapRB = False                        # 不交换RB通道
    compile_options.input_shape = input_shape             # 设置输入形状
    compile_options.input_type = 'uint8'                  # 输入图像数据类型
    compile_options.input_range = [0, 1]                  # 输入图像反量化范围
    compile_options.mean = [0, 0, 0]                      # 预处理均值
    compile_options.std = [1, 1, 1]                       # 标准差设为1，不进行归一化
    compile_options.input_layout = "NCHW"                 # 输入数据格式

    # 初始化编译器
    compiler = nncase.Compiler(compile_options)

    # 导入ONNX模型为IR
    model_content = read_model_file(model_file)
    import_options = nncase.ImportOptions()
    compiler.import_onnx(model_content, import_options)

    # PTQ选项设置（后训练量化）
    ptq_options = nncase.PTQTensorOptions()
    ptq_options.samples_count = 10  # 校准样本数量

    # 支持6种量化方案（根据精度与性能权衡选择）
    if args.ptq_option == 0:
        ptq_options.calibrate_method = 'NoClip'
        ptq_options.quant_type = 'uint8'
        ptq_options.w_quant_type = 'uint8'
    elif args.ptq_option == 1:
        ptq_options.calibrate_method = 'NoClip'
        ptq_options.quant_type = 'uint8'
        ptq_options.w_quant_type = 'int16'
    elif args.ptq_option == 2:
        ptq_options.calibrate_method = 'NoClip'
        ptq_options.quant_type = 'int16'
        ptq_options.w_quant_type = 'uint8'
    elif args.ptq_option == 3:
        ptq_options.calibrate_method = 'Kld'
        ptq_options.quant_type = 'uint8'
        ptq_options.w_quant_type = 'uint8'
    elif args.ptq_option == 4:
        ptq_options.calibrate_method = 'Kld'
        ptq_options.quant_type = 'uint8'
        ptq_options.w_quant_type = 'int16'
    elif args.ptq_option == 5:
        ptq_options.calibrate_method = 'Kld'
        ptq_options.quant_type = 'int16'
        ptq_options.w_quant_type = 'uint8'

    # 设置PTQ校准数据
    ptq_options.set_tensor_data(generate_data(input_shape, ptq_options.samples_count, args.dataset_path))

    # 应用PTQ
    compiler.use_ptq(ptq_options)

    # 编译模型
    compiler.compile()

    # 导出KModel文件
    base, ext = os.path.splitext(args.model)
    kmodel_name = base + ".kmodel"
    with open(kmodel_name, 'wb') as f:
        f.write(compiler.gencode_tobytes())

# Python程序主入口
if __name__ == '__main__':
    main()
```

将上述代码保存为`to_kmodel.py`脚本，使用如下转换命令完成编译：

```shell
# 你需要将onnx模型换成你训练好的模型
python to_kmodel.py --target k230 --model best.onnx --dataset_path test --input_width 320 --input_height 320 --ptq_option 0
```

通过上面的代码，我们已经成功拿到了用于识别四类数字的 Kmodel 模型。那么你可能会好奇：在把模型转换成 Kmodel 的过程中，里面用到的那些参数到底是啥意思？如果以后我想换个模型来转，是不是也要改参数呢？别着急，接下来的章节我们就会带你搞懂这些转换参数的具体含义，还会教你在转换其他模型时该怎么正确配置，一步步带你上手，不迷路！

<a id="compilation-parameters"></a>

#### 编译参数说明

使用 `nncase compiler` 将 `tflite/onnx` 模型转换成 `kmodel` ，模型转换代码的关键在于根据自身需求进行选项配置，主要是 `CompileOptions` 、 `PTQTensorOptions` 和 `ImportOptions`。

`nncase` 用户指南文档见：[github: user_guide](https://github.com/kendryte/nncase/tree/master/examples/user_guide) 或 [gitee: user_guide](https://gitee.com/kendryte/nncase/tree/master/examples/user_guide) 。

- **编译选项 CompileOptions**

`CompileOptions` 类, 用于配置 `nncase` 编译选项，各属性说明如下：

| 属性名称                    |         类型          | 是否必须 | 描述                                                                                                                   |
| :-------------------------- | :-------------------: | :------: | ---------------------------------------------------------------------------------------------------------------------- |
| target                      |        string         |    是    | 指定编译目标, 如'cpu', 'k230'                                                                                          |
| dump_ir                     |         bool          |    否    | 指定是否dump IR, 默认为False                                                                                           |
| dump_asm                    |         bool          |    否    | 指定是否dump asm汇编文件, 默认为False                                                                                  |
| dump_dir                    |        string         |    否    | 前面指定dump_ir等开关后, 这里指定dump的目录, 默认为""                                                                  |
| input_file                  |        string         |    否    | ONNX模型超过2GB时，用于指定参数文件路径，默认为""                                                                      |
| preprocess                  |         bool          |    否    | 是否开启前处理，默认为False。以下参数仅在 `preprocess=True`时生效                                                      |
| input_type                  |        string         |    否    | 开启前处理时指定输入数据类型，默认为"float"。当 `preprocess`为 `True`时，必须指定为"uint8"或者"float32"                |
| input_shape                 |       list[int]       |    否    | 开启前处理时指定输入数据的shape，默认为[]。当 `preprocess`为 `True`时，必须指定                                        |
| input_range                 |      list[float]      |    否    | 开启前处理时指定输入数据反量化后的浮点数范围，默认为[ ]。当 `preprocess`为 `True`且 `input_type`为 `uint8`时，必须指定 |
| input_layout                |        string         |    否    | 指定输入数据的layout，默认为""                                                                                         |
| swapRB                      |         bool          |    否    | 是否在 `channel`维度反转数据，默认为False                                                                              |
| mean                        |      list[float]      |    否    | 前处理标准化参数均值，默认为[0,0,0]                                                                                    |
| std                         |      list[float]      |    否    | 前处理标准化参数方差，默认为[1,1,1]                                                                                    |
| letterbox_value             |         float         |    否    | 指定前处理letterbox的填充值，默认为0                                                                                   |
| output_layout               |        string         |    否    | 指定输出数据的layout, 默认为""                                                                                         |
| shape_bucket_enable         |         bool          |    是    | 是否开启ShapeBucket功能，默认为False。在 `dump_ir=True`时生效                                                          |
| shape_bucket_range_info     | Dict[str, [int, int]] |    是    | 每个输入shape维度信息中的变量的范围，最小值必须大于等于1                                                               |
| shape_bucket_segments_count |          int          |    是    | 输入变量的范围划分为几段                                                                                               |
| shape_bucket_fix_var_map    |    Dict[str, int]     |    否    | 固定shape维度信息中的变量为特定的值|

关于前处理的配置说明，请参考 API 文档：[nncase 模型编译API手册前处理流程](https://www.kendryte.com/k230_rtos/zh/main/api_reference/nncase/nncase_compile.html#id2)。将部分前处理操作封装在模型内可以提高开发板推理时的前处理效率，支持的前处理包括：`swapRB`(RGB->BGR or BGR->RGB)、`Transpose`(NHWC->NCHW or NCHW->NHWC)、`Normalization`（减均值除方差）、`Dequantize`等。比如：onnx模型需要的输入是`RGB`的，我们使用`opencv`读取的图片是`BGR`，正常onnx模型推理的预处理我们需要先将`BGR`转成`RGB`给onnx模型使用。转kmodel的时候我们就可以设置 `swapRB` 为 `True` ，这样kmodel中自带交换`RB`通道的预处理步骤，在进行kmodel推理的预处理时，我们就可以忽略交换`RB`通道的步骤，将此步骤放到kmodel内部。

- **导入选项 ImportOptions**

ImportOptions类, 用于配置nncase导入选项，配置编译器的待转换模型。可以配置 `tflite/onnx`。使用示例如下：

```python
# 读取并导入tflite模型
model_content = read_model_file(model)
compiler.import_tflite(model_content, import_options)

# 读取并导入onnx模型
model_content = read_model_file(model)
compiler.import_onnx(model_content, import_options)
```

- **训练后量化选项 PTQTensorOptions**

`PTQTensorOptions` 类, 用于配置 `nncase PTQ` 选项：

| 名称                           | 类型   | 是否必须 | 描述 |
| ------------------------------ | ------ | -------- | ---- |
| samples_count                  | int    |    否    |  指定用于量化的校正集数量    |
| calibrate_method               | string |    否    |  指定量化方法，可选'NoClip'、'Kld'，默认为'Kld'   |
| finetune_weights_method        | string |    否    |  指定是否对权重进行微调，可选'NoFineTuneWeights'、'UseSquant'，默认为'NoFineTuneWeights'  |
| quant_type                     | string |    否    |  指定数据量化类型，可选'uint8'，'int8'，'int16'，`quant_type`和`w_quant_type`两种类型不可同时为'int16'  |
| w_quant_type                   | string |    否    |  指定权重量化类型，可选'uint8'，'int8'，'int16'，`quant_type`和`w_quant_type`两种类型不可同时为'int16' |
| quant_scheme                   | string |    否    |  导入量化参数配置文件的路径 |
| quant_scheme_strict_mode       | bool   |    否    |  是否严格按照quant_scheme执行量化  |
| export_quant_scheme            | bool   |    否    |  是否导出量化参数配置文件  |
| export_weight_range_by_channel | bool   |    否    |  是否导出 `bychannel`形式的weights量化参数，该参数建议设置为 `True`  |

混合量化具体使用流程见 [MixQuant说明](https://github.com/kendryte/nncase/blob/release/2.0/docs/MixQuant.md)。

关于量化的配置说明，请参考上表。如果转换的kmodel达不到效果，可以修改 `quant_type` 和 `w_quant_type` 参数，修改模型数据和权重的量化类型，但是这两个参数不能同时设置为 `int16`。

- **量化校正集设置**

| 名称 | 类型                  | 描述           |
| ---- | --------------------- | -------------- |
| data | List[List[np.ndarray]] | 读取的校准数据 |

量化过程中使用的校正数据通过 `set_tensor_data` 方法进行设置，接口参数类型为 `List[List[np.ndarray]]`，比如：模型有一个输入，校正数据量设置为10，传入的校正数据维度为 `[10,1,3,320,320]`；如果模型有两个输入，校正数据量设置为10，传入的校正数据维度为 `[[10,1,3,224,224],[10,1,3,320,320]]`。

### 使用 nncase 模拟器验证转换效果

前面我们说了怎么把模型转换成 Kmodel，现在我们要来“体检”一下这个模型，看它转得好不好！

因为 ONNX 和 Kmodel 在预处理的时候可能不太一样，所以我们得分别按它们各自的要求来准备输入数据。然后，用 ONNX 模型和 Kmodel 模型各跑一遍推理，把结果都保存下来，接着算一下它们之间的 **Cosine 相似度**——这就像是在对比它俩输出的“相似度”。

一句话总结就是：我们要看看转换后的 Kmodel 和原来的 ONNX 模型，输出差不多不？如果相差太大，说明转换过程中可能有问题，那就要回头检查参数设置～

模型转换成功后，可以使用`nncase.Simulator` 在本地PC上加载Kmodel进行推理，通过计算onnx模型和kmodel模型的余弦相似度判断kmodel输出是否正确。**这里需要注意的是，该过程是在本地计算机上运行的，而不是在k230开发板上运行的。**

首先需要在python环境下安装onnx相关的包：

```shell
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

执行模拟器推理脚本需要添加nncase插件环境变量：

- **linux**：

```shell
# 下述命令中的路径为安装 nncase 的 Python 环境的路径，请按照您的环境适配修改
export NNCASE_PLUGIN_PATH=$NNCASE_PLUGIN_PATH:/usr/local/lib/python3.9/site-packages/
export PATH=$PATH:/usr/local/lib/python3.9/site-packages/
source /etc/profile
```

- **windows**：

将安装 `nncase` 的 `Python` 环境下的 `Lib/site-packages` 路径添加到环境变量的系统变量 `Path` 中。

针对**4类打印数字识别**场景，验证输出相似度的示例代码：

```python
import os
import cv2
import numpy as np
import onnxruntime as ort
import nncase
import math

def get_onnx_input(img_path,mean,std,model_input_size):
    # 读取图片，图片数据一般是RGB三通道，颜色范围为[0, 255.0]
    image_fp32=cv2.imread(img_path)
    # 如果模型输入要求是RGB的，则转换为RGB格式，如果要求是BGR的，则不需要转换
    image_fp32=cv2.cvtColor(image_fp32, cv2.COLOR_BGR2RGB)
    # 缩放成模型输入大小
    image_fp32 = cv2.resize(image_fp32, (model_input_size[0], model_input_size[1]))
    # 数据类型为float32,
    image_fp32 = np.asarray(image_fp32, dtype=np.float32)
    # 数据标准化,先归一化到[0,1]范围内，然后减均值除方差
    image_fp32/=255.0
    for i in range(3):
        image_fp32[:, :, i] -= mean[i]
        image_fp32[:, :, i] /= std[i]
    # 按照模型输入要求处理成NCHW排布或者NHWC排布
    image_fp32 = np.transpose(image_fp32, (2, 0, 1))
    return image_fp32.copy()

def get_kmodel_input(img_path,mean,std,model_input_size):
    # 读取图片，图片数据一般是RGB三通道，颜色范围为[0, 255.0]
    image_uint8=cv2.imread(img_path)
    # 如果模型输入要求是RGB的，则转换为RGB格式，如果要求是BGR的，则不需要转换
    image_uint8=cv2.cvtColor(image_uint8, cv2.COLOR_BGR2RGB)
    # 缩放成模型输入大小
    image_uint8 = cv2.resize(image_uint8, (model_input_size[0], model_input_size[1]))
    # 数据类型为uint8,因为转换kmodel的时候开启了预处理，并且设定了标准化参数，因此这里的输入就不需要实现标准化了
    image_uint8 = np.asarray(image_uint8, dtype=np.uint8)
    # 按照模型输入要求处理成NCHW排布或者NHWC排布
    image_uint8 = np.transpose(image_uint8, (2, 0, 1))
    return image_uint8.copy()

def onnx_inference(onnx_path,onnx_input_data):
    # 创建 ONNX 推理会话（加载模型）
    ort_session = ort.InferenceSession(onnx_path)
    # 获取模型输出名称列表，用于后续调用推理
    output_names = []
    model_outputs = ort_session.get_outputs()
    for i in range(len(model_outputs)):
        output_names.append(model_outputs[i].name)

    # 获取模型的输入信息
    model_input = ort_session.get_inputs()[0]             # 第一个输入（通常只有一个）
    model_input_name = model_input.name                   # 输入的名称（键）
    model_input_type = np.float32                         # 输入数据类型，这里假设是 float32
    model_input_shape = model_input.shape                 # 输入张量的形状（维度）

    # 处理输入数据,需确保和模型输入形状一致
    model_input_data = onnx_input_data.astype(model_input_type).reshape(model_input_shape)

    # 执行推理，传入输入名称和数据，返回所有输出结果
    onnx_results = ort_session.run(output_names, { model_input_name : model_input_data })
    return onnx_results

def kmodel_inference(kmodel_path,kmodel_input_data,model_input_size):
    # 初始化nncase 模拟器
    sim = nncase.Simulator()
    # 读取kmodel
    with open(kmodel_path, 'rb') as f:
        kmodel = f.read()
    # 加载kmodel
    sim.load_model(kmodel)
    # 读取输入数据
    input_shape = [1, 3, model_input_size[1], model_input_size[0]]
    dtype = sim.get_input_desc(0).dtype
    # 处理输入数据,需确保和模型输入形状一致
    kmodel_input = kmodel_input_data.astype(dtype).reshape(input_shape)
    # 设置模拟器输入tensor,此处为单输入
    sim.set_input_tensor(0, nncase.RuntimeTensor.from_numpy(kmodel_input))
    # 模拟器推理kmodel模型
    sim.run()
    # 获取推理输出
    kmodel_results = []
    for i in range(sim.outputs_size):
        kmodel_result = sim.get_output_tensor(i).to_numpy()  # 转换为numpy数组
        kmodel_results.append(kmodel_result)  # 保存到列表中
    return kmodel_results

def cosine_similarity(onnx_results,kmodel_results):
    output_size=len(kmodel_results)
    # 将每个输出展成一维，然后计算余弦相似度
    for i in range(output_size):
        onnx_i=np.reshape(onnx_results[i], (-1))
        kmodel_i=np.reshape(kmodel_results[i], (-1))
        cos = (onnx_i @ kmodel_i) / (np.linalg.norm(onnx_i, 2) * np.linalg.norm(kmodel_i, 2))
        print('output {0} cosine similarity : {1}'.format(i, cos))
    return

if __name__ == '__main__':
    img_path="test.jpg"
    mean=[0,0,0]
    std=[1,1,1]
    model_input_size=[320,320]
    # ONNX 模型文件
    onnx_model = "best.onnx"
    # kmodel 模型文件
    kmodel_path="best.kmodel"
    # 生成onnx模型输入数据
    onnx_input_data = get_onnx_input(img_path,mean,std,model_input_size)
    # 生成kmodel模型输入数据
    kmodel_input_data = get_kmodel_input(img_path,mean,std,model_input_size)
    # onnx模型推理
    onnx_results = onnx_inference(onnx_model,onnx_input_data)
    # kmodel模型推理
    nncase_results = kmodel_inference(kmodel_path,kmodel_input_data,model_input_size)
    # 计算输出相似度
    cosine_similarity(onnx_results,nncase_results)
```

将上述代码保存成文件，并将代码内的模型换成您自己转换的模型后，运行脚本得到如下输出：

```shell
output 0 cosine similarity : 0.9995334148406982
```

一般我们认为当相似度大于0.99时，表示该模型转换成功，在实际部署场景下是可用的。

#### 生成输入数据

⚠️ **注意**：在使用 ONNX 模型和 KModel 进行推理时，**必须谨慎处理输入数据的预处理步骤**。若 KModel 中已封装了特定的预处理操作，则在推理前无需对其输入数据手动执行这些预处理；但在使用 ONNX 模型推理时，则需显式地在模型外部完成所有必要的预处理流程。

KModel 所支持并可封装的预处理操作包括：

- 通道顺序变换（如 RGB ↔ BGR），对应 `SwapRB` 参数；
- 布局转换（NCHW ↔ NHWC），对应 `input_shape` 与 `input_layout` 参数；
- 数据标准化处理，依赖 `mean` 和 `std` 参数；
- 输入反量化处理，依赖 `input_type` 和 `input_range` 参数；

关于 ONNX 与 KModel 推理流程的差异，可参考以下流程图：

![inference_diff_onnx_kmodel](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/682d145bc0d1.png)

在使用 ONNX 模型推理时，由于其本体不包含任何预处理逻辑，用户必须在输入前完成所需的全部预处理步骤。
而对于 KModel，如果在模型编译时启用了 `preprocess` 选项，则相关预处理操作将被自动封装进模型内部，推理时不再需要用户手动处理。
如果未启用 `preprocess`，其使用方式与 ONNX 模型相同，仍需在模型外部完成所有预处理过程。

根据上述流程，开发者可按照模型要求构造符合输入规范的推理数据，以便在推理过程中使用。
**请注意：数据生成过程必须严格符合模型要求，不同模型之间的输入处理流程可能存在显著差异，不能混用。**

以下为数据预处理的示例代码：

```python
def get_onnx_input(img_path,mean,std,model_input_size):
    # 读取图片，图片数据一般是RGB三通道，颜色范围为[0, 255.0]
    image_fp32=cv2.imread(img_path)
    # 如果模型输入要求是RGB的，则转换为RGB格式，如果要求是BGR的，则不需要转换
    image_fp32=cv2.cvtColor(image_fp32, cv2.COLOR_BGR2RGB)
    # 缩放成模型输入大小
    image_fp32 = cv2.resize(image_fp32, (model_input_size[0], model_input_size[1]))
    # 数据类型为float32,
    image_fp32 = np.asarray(image_fp32, dtype=np.float32)
    # 数据标准化,先归一化到[0,1]范围内，然后减均值除方差
    image_fp32/=255.0
    for i in range(3):
        image_fp32[:, :, i] -= mean[i]
        image_fp32[:, :, i] /= std[i]
    # 按照模型输入要求处理成NCHW排布或者NHWC排布
    image_fp32 = np.transpose(image_fp32, (2, 0, 1))
    return image_fp32.copy()

def get_kmodel_input(img_path,mean,std,model_input_size):
    # 读取图片，图片数据一般是RGB三通道，颜色范围为[0, 255.0]
    image_uint8=cv2.imread(img_path)
    # 如果模型输入要求是RGB的，则转换为RGB格式，如果要求是BGR的，则不需要转换
    image_uint8=cv2.cvtColor(image_uint8, cv2.COLOR_BGR2RGB)
    # 缩放成模型输入大小
    image_uint8 = cv2.resize(image_uint8, (model_input_size[0], model_input_size[1]))
    # 数据类型为uint8,因为转换kmodel的时候开启了预处理，并且设定了标准化参数，因此这里的输入就不需要实现标准化了
    image_uint8 = np.asarray(image_uint8, dtype=np.uint8)
    # 按照模型输入要求处理成NCHW排布或者NHWC排布
    image_uint8 = np.transpose(image_uint8, (2, 0, 1))
    return image_uint8.copy()
```

在使用 ONNX 模型和 KModel 进行推理时，输入数据的预处理存在若干关键差异，主要体现在以下几个方面：

- **标准化处理**：ONNX 模型本身不包含任何预处理逻辑，因此其输入数据必须在外部完成标准化（例如减均值除标准差）。而对于 KModel，如果在模型转换阶段已配置了归一化参数（如 `mean` 和 `std`），则这部分标准化操作会被封装进模型内部，**推理前无需重复处理**。

- **数据类型差异**：ONNX 模型的输入通常为 `float32` 类型，而 KModel 的输入类型则依赖模型转换时指定的 `input_type`（例如 `uint8`）及 `input_range`。KModel 会在推理内部进行反量化处理，将整数类型还原为近似的浮点表达。

- **通道顺序处理**：若在模型转换过程中未启用 `SwapRB`（即参数为 `False`），则需要在外部预处理阶段将输入图像的通道顺序从 BGR 转换为 RGB。若 `SwapRB=True`，该通道变换操作将自动由 KModel 内部处理，**无需在外部执行**。

综合来看，ONNX 模型所需的外部预处理操作等于 KModel 的外部预处理 **加上** 内部预处理，两者的关系可表示如下：

```shell
ONNX 模型外部预处理 = KModel 外部预处理 + KModel 内部预处理
```

#### 加载onnx模型并推理

首先需要使用onnx模型完成推理，获取onnx模型的推理结果。示例代码如下：

```python
def onnx_inference(onnx_path,onnx_input_data):
    # 创建 ONNX 推理会话（加载模型）
    ort_session = ort.InferenceSession(onnx_path)
    # 获取模型输出名称列表，用于后续调用推理
    output_names = []
    model_outputs = ort_session.get_outputs()
    for i in range(len(model_outputs)):
        output_names.append(model_outputs[i].name)

    # 获取模型的输入信息
    model_input = ort_session.get_inputs()[0]             # 第一个输入（通常只有一个）
    model_input_name = model_input.name                   # 输入的名称（键）
    model_input_type = np.float32                         # 输入数据类型，这里假设是 float32
    model_input_shape = model_input.shape                 # 输入张量的形状（维度）

    # 处理输入数据,需确保和模型输入形状一致
    model_input_data = onnx_input_data.astype(model_input_type).reshape(model_input_shape)

    # 执行推理，传入输入名称和数据，返回所有输出结果
    onnx_results = ort_session.run(output_names, { model_input_name : model_input_data })
    return onnx_results
```

#### 加载kmodel模型并推理

然后使用转换成功的kmodel进行推理，获得kmodel的推理结果。示例代码如下：

```python
def kmodel_inference(kmodel_path,kmodel_input_data,model_input_size):
    # 初始化nncase 模拟器
    sim = nncase.Simulator()
    # 读取kmodel
    with open(kmodel_path, 'rb') as f:
        kmodel = f.read()
    # 加载kmodel
    sim.load_model(kmodel)
    # 读取输入数据
    input_shape = [1, 3, model_input_size[1], model_input_size[0]]
    dtype = sim.get_input_desc(0).dtype
    # 处理输入数据,需确保和模型输入形状一致
    kmodel_input = kmodel_input_data.astype(dtype).reshape(input_shape)
    # 设置模拟器输入tensor,此处为单输入
    sim.set_input_tensor(0, nncase.RuntimeTensor.from_numpy(kmodel_input))
    # 模拟器推理kmodel模型
    sim.run()
    # 获取推理输出
    kmodel_results = []
    for i in range(sim.outputs_size):
        kmodel_result = sim.get_output_tensor(i).to_numpy()  # 转换为numpy数组
        kmodel_results.append(kmodel_result)  # 保存到列表中
    return kmodel_results
```

#### 计算输出的余弦相似度

得到onnx模型和kmodel模型的推理结果后，逐个计算每个输出的余弦相似度。一般相似度在0.99以上可以认为该模型转换成功，可部署使用。示例代码如下：

```python
def cosine_similarity(onnx_results,kmodel_results):
    output_size=len(kmodel_results)
    # 将每个输出展成一维，然后计算余弦相似度
    for i in range(output_size):
        onnx_i=np.reshape(onnx_results[i], (-1))
        kmodel_i=np.reshape(kmodel_results[i], (-1))
        cos = (onnx_i @ kmodel_i) / (np.linalg.norm(onnx_i, 2) * np.linalg.norm(kmodel_i, 2))
        print('output {0} cosine similarity : {1}'.format(i, cos))
    return
```

## 模型部署

```{note}
👉 前面我们把kmodel模型转好了、也验证过了，接下来当然就是———**上板子跑起来啦！** 这一章我们就来聊聊怎么在 K230 的 MicroPython 环境下，用提供的 nncase runtime API 把模型加载进来并实现推理。

那问题来了：模型是有了，那输入数据要怎么准备？我们要根据模型的“口味”对输入图像做一些处理，比如尺寸、格式、归一化等等，确保它能“吃得对”。然后把处理好的数据喂进去，让模型开始推理。推理完之后，模型会给我们一堆“输出结果”，这些结果是啥意思？我们还得做一番解析，比如拿出类别、坐标这些有用的信息。

最后嘛，当然不能藏着掖着！我们会把这些识别出来的内容显示在屏幕上，比如画框、标数字，让整个流程从图像采集、模型推理，到结果展示**一气呵成、全流程跑通**！

这一章就会带你把这个完整过程搞明白，让模型真的开始“动起来”～
```

对于一个实用的 AI 程序，不仅包括模型推理，还包括有图像输入、前后处理程序、结果显示等不同模块。下图展示了一个典型的AI应用程序的完整框图：

![deploy_pipeline](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/dd5383ab43ed.png)

🚀 部署流程讲解：部署其实可以理解为“让模型真正工作起来”的过程，下面我们按照流程，分步介绍。

**1️⃣ 获取图像数据（输入数据源）**
我们先得拿到一张图像，通常是从摄像头中实时采集，也可以从本地加载一张测试图片。拿到图像后，会得到一个 Image 对象。在 K230 开发板上，通常你会通过 sensor.snapshot() 来获取图像。

**2️⃣ 构造输入 Tensor（准备投喂模型的数据）**
有了图像之后，我们要把它“打包”成模型能处理的格式nncase_runtime.runtime_tensor。这一步，是为了喂给模型一个标准结构的数据。

**3️⃣ 预处理（ai2d 模块）**
模型对输入图像有特定要求，比如大小、格式、通道顺序等等。这一步我们就用 ai2d 模块把图像tensor处理成模型需要的“样子”。

**4️⃣ 模型推理（使用 KPU 推理模块）**
图像处理好后，喂进 KPU（K230 的神经网络加速模块）进行推理。KPU 会返回一个结果 tensor，这里面包含了模型的输出，比如检测框、分类概率等等。

**5️⃣ 后处理（提取有用信息）**
KPU 输出的是一堆数字，我们得把这些“干货”解析出来。比如识别到的数字是几？框在图像上的位置在哪？这些都需要用后处理算法来搞定。对 YOLO 模型来说，后处理包括置信度过滤、NMS 非极大值抑制等。

**6️⃣ 显示识别结果（可视化）**
最后一步，把识别到的内容“画”出来！我们可以在屏幕上画出检测框、数字标签等，让结果一目了然。一般会用两个图层来显示，一层是原始图像，另一层是识别结果（如框和数字），叠加显示可以保证效果更清晰也更灵活。

总结：部署的核心流程就是：拿图像 → 处理成输入 → 扔给模型 → 拿结果 → 解读结果 → 显示出来！这套流程跑通了，你的模型就等于真正“上线工作”了！🎉

💡 **固件介绍**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](./userguide/how_to_build.md)。

### 获取输入并创建tensor

前面我们说了，模型跑起来之后，需要输入数据才能开始推理对吧？那这些图像数据从哪儿来呢？这节我们就来聊聊——**图像是怎么来的，又是怎么一步步变成模型能“吃”的格式的！**

图像来源其实有三种方式：可以用板子上提前放好的本地图片（比如你事先拷进去的测试图），也可以用板载的 MIPI 摄像头拍摄实时画面，或者接个 UVC 摄像头来取图。不管你选哪种方式，最终我们都要拿到一个 **Image 对象**——这个就像是“原材料”。

拿到图像之后，我们还不能直接送给模型。中间还要“加工一下”！我们会用 `ulab.numpy.ndarray` 把图片转成一个数组格式，通过这个格式我们可以查看数据的通道顺序等信息。

最后，我们用 `nncase_runtime` 模块提供的 API，把这个数组转成 **tensor（张量）**。这时候数据就“打包”好了，可以安心送进模型做推理了！

那什么是 tensor 呢？你可以把它想象成是模型能听懂的“语言”——它就像一个装数据的盒子，模型吃进去的是 tensor，推理之后吐出来的结果也是 tensor。在 `nncase_runtime` 模块里，这个东西被封装成了 `runtime_tensor`，你只要按照要求构造好，就能直接用了，特别方便。

![image2tensor](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/159f6662a39b.png)

上图说明了在获取输入图像并创建tensor的过程。模型推理输入为`nncase_runtime runtime_tensor`类型，可以从`ulab.numpy.ndarray`数据创建，`ulab.numpy.ndarray`数据可以来自`Image`实例，`Image`实例可以来自以下三种：

- 图片文件
- MIPI摄像头
- UVC摄像头

本节就这三种输入数据来源进行详细介绍。
  
#### 图片文件输入

从开发板读入一张图片数据，创建`Image`实例，并将`Image`实例转换为`nncase_runtime tensor`类型。示例代码如下：

```python
import os,sys
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc

# 请自行将测试图片拷贝到开发板data目录下
img_path="/data/test.jpg"

# 使用图片创建Image实例，类型为jpeg
img_data = image.Image(img_path)
print(img_data)
# 将图片数据转换成rgb888格式的Image实例，该类型数据是RGB三通道，颜色范围为[0,255]
img_rgb888=img_data.to_rgb888()
print(img_rgb888)
# 将Image实例转换成ulab.numpy.ndarray类型,这是数据是HWC类型的
img_hwc=img_rgb888.to_numpy_ref()
print(img_hwc.shape)
# 获取hwc排布的shape,使用ulab.numpy的transpose方法将hwc转换为chw排布
shape=img_hwc.shape
img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
img_trans = img_tmp.transpose()
img_tmp=img_trans.copy()
img_chw=img_tmp.reshape((shape[2],shape[0],shape[1]))
print(img_chw.shape)
# 使用chw数据创建nncase_runtime runtime_tensor，可以给kmodel模型推理使用
input_tensor=nn.from_numpy(img_chw)
print(type(input_tensor))
```

上述代码的IDE打印信息如下：

```shell
{"w":1024, "h":1024, "type":"jpeg", "size":200610}
{"w":1024, "h":1024, "type":"rgb888", "size":3145728}
(1024, 1024, 3)
(3, 1024, 1024)
<class 'runtime_tensor'>
```
  
#### MIPI视频流输入

k230 Sensor模块负责图像采集和数据处理，支持MIPI接口摄像头。MIPI摄像头可以通过Sensor模块采集图像数据，Sensor模块支持多通道采图，可以将采集到的图像数据转换为`nncase_runtime runtime_tensor`类型，供kmodel模型推理使用。Sensor模块的配置和使用请参考 [Sensor API文档](./api/mpp/k230_canmv_sensor_module_api_manual.md)。

🏷️ **单通道采图**

每个MIPI摄像头最多可以出3路图像通道（各路通道可以具有不同分辨率或不同格式）。
这里我们采用一路通道输出作为示例，数据处理流程图下图所示：

![1_chn_process](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/928b6059eea3.png)

模型推理过程中的输入数据也可以来自MIPI摄像头的视频流，为了保证输出数据为CHW排布，我们一般指定摄像头流出数据格式为`Sensor.RGBP888`。代码如下：

```python
import os,sys
from media.sensor import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc

#-----------------------------Sensor初始化部分-------------------------------
# 定义AI推理帧分辨率
AI_RGB888P_WIDTH = ALIGN_UP(1280, 16)
AI_RGB888P_HEIGHT = 720

sensor = Sensor()
sensor.reset()
# 设置水平镜像和垂直翻转，不同开发板的方向不同，通过配置这两个参数使画面转正
#sensor.set_hmirror(False)
#sensor.set_vflip(False)

# 配置sensor的多通道出图，每个通道的出图格式和分辨率可以不同，最多可以出三路图，参考sensor API文档
# 通道1给到AI做算法处理，格式为RGB888P
sensor.set_framesize(width = AI_RGB888P_WIDTH , height = AI_RGB888P_HEIGHT, chn=CAM_CHN_ID_1)
# 设置1通道的出图格式
sensor.set_pixformat(Sensor.RGBP888, chn=CAM_CHN_ID_1)

# MediaManager初始化
MediaManager.init()
# 启动sensor
sensor.run()
while True:
    #------------------------从摄像头dump一帧图像并处理----------------------------------
    print("-----------------------------------")
    # 从摄像头1通道dump一帧RGB888P格式的Image图像
    img=sensor.snapshot(chn=CAM_CHN_ID_1)
    print(img)
    # 转换成ulab.numpy.ndarray格式的数据，CHW
    img_np=img.to_numpy_ref()
    print(img_np.shape)
    # 创建nncase_runtime.runtime_tensor用于进行后续的预处理
    runtime_tensor=nn.from_numpy(img_np)
    print(type(runtime_tensor))
    print("-----------------------------------")

sensor.stop()
time.sleep_ms(50)
MediaManager.deinit()
nn.shrink_memory_pool()
```

CanMV IDE的串口输出为：

```shell
-----------------------------------
{"w":1280, "h":720, "type":"rgbp888", "size":2764800}
(3, 720, 1280)
<class 'runtime_tensor'>
-----------------------------------
-----------------------------------
{"w":1280, "h":720, "type":"rgbp888", "size":2764800}
(3, 720, 1280)
<class 'runtime_tensor'>
-----------------------------------
```

🏷️ **双通道采图**

在边缘设备上执行 AI 模型推理时，由于模型计算量较大，**推理过程通常较耗时**，耗时范围从几毫秒到数百毫秒不等。若采用单通道处理流程：

```text
图像采集 → 格式转换 → 数据预处理 → 模型推理 → 结果后处理 → 原图绘制 → 图像显示
```

这种串行执行方式会导致图像显示延迟较高，尤其是当模型较大或系统资源有限时，画面更新明显变慢，影响用户体验。

为了解决这一问题，**推荐使用双通道处理架构**，即采用“**一通道用于实时显示，另一通道用于模型推理**”的异步处理策略。该架构通过并行处理图像采集与模型推理，有效减少了显示延迟，提升了画面流畅性。双通道处理机制如下：

- **显示通道**：直接采集图像并推送至屏幕，实现低延迟的实时画面显示。
- **推理通道**：独立采集图像并执行完整的 AI 推理流程（包括格式转换、预处理、模型推理与后处理）。
- **OSD 图层合成**：将模型推理结果（如检测框、关键点等）绘制为 OSD 图层，并通过硬件叠加与原始图像合成后再输出显示。

虽然推理结果在视觉上会存在一定延迟（即上一帧的检测框显示在当前帧图像上），但整体画面连续性更好，用户体验更加流畅。

![2_chn_process](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/9a6786d388a1.png)

代码如下：

```python
import os,sys
from media.sensor import *
from media.display import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc

#-----------------------------Sensor/Display初始化部分-------------------------------

# 定义屏幕显示分辨率
DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# 定义AI推理帧分辨率
AI_RGB888P_WIDTH = ALIGN_UP(1280, 16)
AI_RGB888P_HEIGHT = 720

sensor = Sensor()
sensor.reset()
# 设置水平镜像和垂直翻转，不同板子的方向不同，通过配置这两个参数使画面转正
#sensor.set_hmirror(False)
#sensor.set_vflip(False)

# 配置sensor的多通道出图，每个通道的出图格式和分辨率可以不同，最多可以出三路图，参考sensor API文档
# 通道0直接给到显示VO，格式为YUV420
sensor.set_framesize(width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT,chn=CAM_CHN_ID_0)
sensor.set_pixformat(Sensor.YUV420SP,chn=CAM_CHN_ID_0)
# 通道1给到AI做算法处理，格式为RGB888P
sensor.set_framesize(width = AI_RGB888P_WIDTH , height = AI_RGB888P_HEIGHT, chn=CAM_CHN_ID_1)
# 设置通道1的出图格式
sensor.set_pixformat(Sensor.RGBP888, chn=CAM_CHN_ID_1)

# 绑定通道0的摄像头图像到屏幕，防止另一个通道的AI推理过程太慢影响显示过程，导致出现卡顿效果
sensor_bind_info = sensor.bind_info(x = 0, y = 0, chn = CAM_CHN_ID_0)
Display.bind_layer(**sensor_bind_info, layer = Display.LAYER_VIDEO1)

# OSD图像初始化,创建一帧和屏幕分辨率同样大的透明图像，用于绘制AI推理结果
osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

# 设置为LT9611显示，默认1920x1080
#Display.init(Display.LT9611,width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1, to_ide = True)
## 如果使用ST7701的LCD屏幕显示，默认800*480,还支持640*480等，具体参考Display模块API文档
Display.init(Display.ST7701, width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1, to_ide=True)

# 限制bind通道的帧率，防止生产者太快
sensor._set_chn_fps(chn = CAM_CHN_ID_0, fps = Display.fps())

# media初始化
MediaManager.init()
# 启动sensor
sensor.run()
while True:
    #------------------------从摄像头dump一帧图像并处理----------------------------------
    print("---------------------------------")
    # 从摄像头1通道dump一帧RGB888P格式的Image图像
    img=sensor.snapshot(chn=CAM_CHN_ID_1)
    print(img)
    # 转换成ulab.numpy.ndarray格式的数据，CHW
    img_np=img.to_numpy_ref()
    print(img_np.shape)
    # 创建nncase_runtime.runtime_tensor用于进行后续的预处理
    runtime_tensor=nn.from_numpy(img_np)
    print(type(runtime_tensor))
    osd_img.clear()
    osd_img.draw_string_advanced( 20 , 20, 32, "这里模拟绘制结果", color=(0,255,0))
    print("---------------------------------")
    #------------------------在屏幕显示检测框结果----------------------------------------
    Display.show_image(osd_img)
    gc.collect()

sensor.stop()
Display.deinit()
time.sleep_ms(50)
MediaManager.deinit()
nn.shrink_memory_pool()
```

CanMV IDE的串口输出为：

```shell
---------------------------------
{"w":1280, "h":720, "type":"rgbp888", "size":2764800}
(3, 720, 1280)
<class 'runtime_tensor'>
---------------------------------
---------------------------------
{"w":1280, "h":720, "type":"rgbp888", "size":2764800}
(3, 720, 1280)
<class 'runtime_tensor'>
---------------------------------
```
  
#### UVC视频流输入

k230 MicroPython在1.3版本之后支持USB摄像头。UVC模块提供了摄像头检测、配置和图像采集功能，支持单摄像头操作。获取的视频流图像也可以作为kmodel模型的输入实现推理。UVC推理流程如下图所示：

![uvc_process](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/99bf4c229c83.png)

这里给出创建`runtime_tensor`的代码，其他步骤在后面章节介绍。示例代码如下：

```python
from libs.Utils import *
import os,sys,ujson,gc,math, urandom
from media.display import *
from media.media import *
from media.uvc import *
import nncase_runtime as nn
import ulab.numpy as np
import image
from nonai2d import CSC

# 显示屏幕分辨率
DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# 定义AI推理帧分辨率,仅支持usb摄像头支持的分辨率
AI_RGB888P_WIDTH = 640
AI_RGB888P_HEIGHT = 480

# CSC模块实现格式转换
csc = CSC(0, CSC.PIXEL_FORMAT_RGB_888)

# 使用ST7701的LCD屏幕显示，默认800*480,还支持640*480等，具体参考Display模块API文档
Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

# MediaManager初始化
MediaManager.init()

# 等待USB摄像头被检测到
while True:
    plugin, dev = UVC.probe()
    if plugin:
        print(f"detect USB Camera {dev}")
        break
    time.sleep_ms(100)

# 设置UVC输出: 640x480 @ 30 FPS, MJPEG 格式
mode = UVC.video_mode(640, 480, UVC.FORMAT_MJPEG, 30)
succ, mode = UVC.select_video_mode(mode)
print(f"select mode success: {succ}, mode: {mode}")

# 启动UVC
UVC.start(cvt=True)

while True:
    print("-------------------------------------------")
    # 从UVC获取一帧图像
    img = UVC.snapshot()
    print(type(img))
    if img is not None:
        # CSC将图片转换成RGB888
        img = csc.convert(img)
        print(img)
        #转换成Ulab.Numpy.ndarray
        img_np_hwc = img.to_numpy_ref()
        print(img_np_hwc.shape)
        # HWC->CHW,使用libs.Utils中的hwc2chw方法
        img_np_chw = hwc2chw(img_np_hwc)
        print(img_np_chw.shape)
        # 创建nncase_runtime.runtime_tensor
        runtime_tensor=nn.from_numpy(img_np_chw)
        print(type(runtime_tensor))
        ############################################
        # 这里可以实现模型预处理->推理->后处理->绘制结果
        ############################################
        # 屏幕显示图像
        Display.show_image(img)
        # 释放img缓存
        img.__del__()
        gc.collect()
    print("-------------------------------------------")
Display.deinit()
csc.destroy()
UVC.stop()
time.sleep_ms(100)
MediaManager.deinit()
```

CanMV IDE的串口输出为：

```shell
-------------------------------------------
<class 'py_video_frame_info'>
{"w":640, "h":480, "type":"rgb888", "size":921600}
(480, 640, 3)
(3, 480, 640)
<class 'runtime_tensor'>
-------------------------------------------
-------------------------------------------
<class 'py_video_frame_info'>
{"w":640, "h":480, "type":"rgb888", "size":921600}
(480, 640, 3)
(3, 480, 640)
<class 'runtime_tensor'>
-------------------------------------------
```
  
### 图像tensor预处理

我们之前已经成功把图像数据变成了一个 tensor，但问题来了——这个 tensor 可能跟模型“胃口不合”。比如大小不对、颜色通道不对。这时候，就需要我们出马，把 tensor 加工一下，让它变成模型可以接受的格式。这整个处理过程就叫“预处理”，而完成这个工作的，就是我们今天的主角 —— ai2d 模块！

**🛠️ 为什么要做预处理？**
模型是“挑食”的，它只接受特定尺寸、格式的数据，比如：输入要是 320x320 大小；要是 RGB 顺序，而不是 BGR；通道在前（CHW）还是通道在后（HWC）也得对上。如果不对，就会识别错误，甚至模型直接罢工报错。

**⚡ ai2d 模块：硬件加速，飞快处理！**
ai2d 是 K230 平台上专门用于图像tensor预处理的模块，运行在硬件上，非常快，适合嵌入式实时任务。它可以帮你完成：缩放、裁剪、填充、仿射变换等操作，使得图像数据被处理成符合模型输入要求的tensor数据。

下图展示了在 K230 平台上通过 ai2d 模块进行预处理的输入输出流程和格式：

![preprocess](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/a57682171f6d.png)

#### 预处理过程介绍

在部署模型时，输入图像的 `runtime_tensor` 并不一定符合模型的输入规格。例如，摄像头采集的图像尺寸可能为 `1280×720`，而模型的输入要求是 `320×320`，此时就需要对图像进行**预处理**。

预处理操作包括但不限于以下常见方式：

- **缩放（Resize）**：将原始图像调整为模型输入所需尺寸；
- **裁剪（Crop）**：保留图像的关键区域，去除冗余部分；
- **归一化（Normalization）**：将像素值映射到指定区间（如 `[0, 1]` 或 `[-1, 1]`）；
- **填充（Padding）**：为保持图像纵横比进行边缘填充，避免拉伸变形。

具体应采用哪些预处理方式，需根据 **ONNX 模型的训练预处理流程**进行对标设置。同时，在将 ONNX 模型转换为 KModel 的过程中，部分预处理步骤（如标准化、颜色通道转换等）可通过编译器参数封装进模型内部，这些操作在部署时**无需再次实现**，由 KModel 自动完成。

> ⚠️ **注意**：
> 对预处理流程需有清晰理解，尤其在进行图像**等比例填充（Aspect Ratio Padding）**时，用户可选择不同策略：
>
> - **双边填充**：在图像的上下和左右两侧均进行填充，使图像居中；
> - **单边填充**：仅在图像一侧（如上/左或下/右）填充，保持一边对齐。
>
> 不同填充方式会影响模型推理输出坐标的复原逻辑，因此在后处理阶段需要**匹配相应的坐标变换规则**，确保结果正确映射回原始图像。

#### ai2d模块介绍

在 MicroPython 方案中，常见的图像预处理操作通常通过 `nncase_runtime.ai2d` 模块由硬件加速实现。该模块支持五种主要的预处理方法，包括：

- **缩放（Resize）**
- **裁剪（Crop）**
- **填充（Pad）**
- **仿射变换（Affine）**
- **比特位右移（Shift）**

使用 `ai2d` 模块可有效降低 CPU 运算负担，提高预处理效率，适用于模型推理前的图像适配操作。相关 API 使用方法详见官方文档：[ai2d API 文档](./api/nncase/k230_canmv_nncase_runtime_api_manual.md#nncase-runtime-ai2d)。

```{attention}
(1) **Affine 与 Resize 互斥**：二者不可同时启用，仅能选择其中一种进行几何变换。  
(2) **Shift 仅支持 Raw16 输入格式**，用于特定格式的高位移位操作。  
(3) **Pad Value 按通道配置**：应提供与输入图像通道数一致的列表，例如 RGB 图像需配置三个通道的填充值。  
(4) **功能执行顺序为 Crop → Shift → Resize/Affine → Pad**：配置多个预处理步骤时必须遵循此顺序。如果预处理流程不符合此顺序，建议初始化多个 `ai2d` 实例，逐步完成所需处理。
```

通过合理配置 `ai2d` 模块，可实现高效、灵活的图像预处理，以满足不同模型对输入数据的要求。

这里以**打印数字识别**任务使用的等比例缩放填充预处理过程为例，介绍`ai2d`模块的使用方法。**核心代码**(此代码仅用于说明，无法直接运行)如下：

```python
import os,sys
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc

# 计算padding缩放比例和上下左右四个方向填充的大小，这里是单侧填充，上左填充大小均为0，在下右进行填充
def letterbox_pad_param(input_size,output_size):
    ratio_w = output_size[0] / input_size[0]  # 宽度缩放比例
    ratio_h = output_size[1] / input_size[1]   # 高度缩放比例
    ratio = min(ratio_w, ratio_h)  # 取较小的缩放比例
    new_w = int(ratio * input_size[0])  # 新宽度
    new_h = int(ratio * input_size[1])  # 新高度
    dw = (output_size[0] - new_w) / 2  # 宽度差
    dh = (output_size[1] - new_h) / 2  # 高度差
    top = int(round(0))
    bottom = int(round(dh * 2 + 0.1))
    left = int(round(0))
    right = int(round(dw * 2 - 0.1))
    return top, bottom, left, right,ratio


# 定义AI推理帧分辨率
AI_RGB888P_WIDTH = ALIGN_UP(1280, 16)
AI_RGB888P_HEIGHT = 720

# 模型输入分辨率
model_input_size=[320,320]

# 假设这里有一个大小为[AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT]的图像tensor，它可以从上一节的数据源中得到
ai2d_input_tensor
# 初始化一个空的tensor，用于ai2d输出
input_init_data = np.ones((1,3,model_input_size[1],model_input_size[0]),dtype=np.uint8)
ai2d_output_tensor = nn.from_numpy(input_init_data)

#------------------------配置ai2d预处理方法----------------------------------------
# 初始化ai2d预处理，并配置ai2d pad+resize预处理，预处理过程输入分辨率为图片分辨率，输出分辨率模型输入的需求分辨率，实现tensor->ai2d preprocess->tensor->kmodel的过程
ai2d=nn.ai2d()
# 配置ai2d模块的输入输出数据类型和格式
ai2d.set_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
# 根据长边比例计算四个方向需要填充的大小
top,bottom,left,right,ratio=letterbox_pad_param([AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT],model_input_size)
# 设置填充pad的参数，上下左右填充的大小和三个通道填充的具体像素值
ai2d.set_pad_param(True,[0,0,0,0,top,bottom,left,right], 0, [128,128,128])
# 设置resize参数，配置插值方法
ai2d.set_resize_param(True,nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
# 设置ai2d模块的输入输出维度，并构建builder实例
ai2d_builder = ai2d.build([1,3,AI_RGB888P_HEIGHT,AI_RGB888P_WIDTH], [1,3,model_input_size[1],model_input_size[0]])

#------------------------执行ai2d预处理步骤----------------------------------------
# 执行预处理过程
ai2d_builder.run(ai2d_input_tensor, ai2d_output_tensor)
# 将预处理后的runtime_tensor转换成ulab.numpy.ndarray格式
ai2d_output_np=ai2d_output_tensor.to_numpy()
print("ai2d output shape:",ai2d_output_np.shape)

#退出循环，释放资源
del ai2d
nn.shrink_memory_pool()
```

预处理后的数据的shape如下：

```shell
ai2d output shape: (1, 3, 320, 320)
```

#### AIDemo中的Ai2d模块

基于 `nncase_runtime` 模块提供的接口，应用层对 `nncase_runtime.ai2d` 进行了**二次封装**，其底层实现和使用`nncase_runtime.ai2d`是一样的。

封装模块在烧录固件后的 `/sdcard/libs/AI2D.py` 内，提供的接口见：[ai2d_module_api_manual](./api/aidemo/ai2d_module_api_manual.md)。

为了帮助用户更好的实现预处理过程，Ai2d文档提供了针对五种预处理方法的示例，并将处理结果实现可视化，示例文档见链接：[Ai2d示例文档](./example/ai/ai2d_examples.md)。
  
### KPU推理

前面我们已经把图像预处理好了，输入 tensor 也准备就绪——现在终于轮到**主角登场**啦，那就是我们的“神经网络加速单元”——**KPU**！

KPU 是 K230 上专门用来跑神经网络模型的硬件加速器，它的作用就是：**模型交给我，推理我来搞！**
不过在开始之前，我们得先告诉它：嘿，我要用哪个模型！所以你需要提前把 `.kmodel` 文件放进 K230 的板子里，然后在代码里把这个模型加载进 KPU。

接着，就要设置输入啦——我们之前用 ai2d 模块处理好的 tensor 就派上用场了，作为模型输入传给 KPU。然后，就可以让 KPU 开始飞速地跑模型啦！

模型一跑完，KPU 会把结果返回给我们，这个结果是一个 **输出 tensor**，里面就是模型推理出来的原始数据。但是这个格式人看不懂也不好用，所以我们还得做一步“翻译”：把输出 tensor 转成 `ulab.numpy.ndarray` 这种数组格式，方便我们做后续分析，比如判断识别出的是哪个数字、它的位置在哪儿等等。

下图是使用 KPU 实现模型推理的过程，模型推理过程包括加载模型、设置模型输入、执行模型推理、获取模型输出：

![kpu_run](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/262abdc53cda.png)

KPU是一个专门用于深度学习的加速引擎，实现对神经网络模型的计算过程进行加速。在MicroPython中，`nncase_runtime.kpu` 模块提供了调用KPU推理模型的接口。该模块的API文档见链接：[nncase_runtime API文档](./api/nncase/k230_canmv_nncase_runtime_api_manual.md)。

这里给出使用`nncase_runtime.kpu`模块进行KPU推理的核心代码（此代码仅用于说明，无法直接运行）如下：

```python
import os,sys
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc
from libs.Utils import *

# 假设这里有一个ai2d模块处理完成后的tensor
ai2d_output_tensor

#-----------------------------AI模型初始化+推理部分-------------------------------
# Kmodel模型路径
kmodel_path="/sdcard/best.kmodel"

# 创建kpu实例
kpu=nn.kpu()
# 加载kmodel模型
kpu.load_kmodel(kmodel_path)

# 设置kpu的第0个输入为ai2d预处理后的tensor，如果有多个，可以依次设置
kpu.set_input_tensor(0,ai2d_output_tensor)
# 在kpu上执行模型推理
kpu.run()
#------------------------获取模型推理结束的输出----------------------------------------
# 获取模型推理的输出tensor，并将其转换成ulab.numpy.ndarray数据进行后处理
results=[]
for i in range(kpu.outputs_size()):
    output_i_tensor = kpu.get_output_tensor(i)
    result_i = output_i_tensor.to_numpy()
    print(f"output {i}:",result_i.shape)
    results.append(result_i)
    del output_i_tensor
del ai2d
del kpu
time.sleep_ms(50)
nn.shrink_memory_pool()
```

对于**四类打印数字识别任务**，kpu模型推理的输出只有一个，输出shape为[1,8,2100]。输出的数据shape如下图：

![output_shape](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/5276f4bf5f71.png)

### 后处理

模型推理已经跑完啦，KPU 给了我们一大串“数字数组”当作结果，但别高兴太早——这些数字乍一看根本不知道是什么意思。所以，接下来的工作，就是要把这些数据**翻译成人类能看懂的内容**，比如：画面里出现了哪个数字？在什么位置？这个识别结果靠不靠谱？

举个例子，我们这个“四类打印数字识别”模型的输出形状是`[1, 8, 2100]`，意思是总共有 2100 个候选框，每个框用 8 个数字来描述。具体是什么呢？前 4 个是框的位置（中心点的 X、Y 坐标，加上宽度和高度），后 4 个是四种数字（0、1、2、3）的“得分”，也就是模型对每类的判断信心。

我们要做的第一步，就是从这 4 个得分里，挑出得分最高的那个，拿到它的类别编号和对应的分数，这就代表这个框最可能是什么数字，以及模型有多确定是这个数字。

然后，再处理一下位置。模型输出的是框的“中心点 + 宽高”，但我们通常更习惯用“左上角坐标 + 右下角坐标”的方式，这样才能方便后面做 NMS 操作。

那 NMS（非极大值抑制） 是啥呢？你可以理解为“去重”。有时候模型太“热情”，对同一个数字框出好几个，我们不需要那么多——只保留得分最高的那一个，其它重叠太多的全删掉，干干净净！这一步就叫做 NMS，几乎所有目标检测的模型后处理都会有这一步，非常关键！

最后，还有个细节就是：模型是对输入尺寸做推理的，比如我们输入的是 320×320 的图像，但原图可能是别的大小，所以我们还要把这些坐标按比例“复原”到原图上，才能正确画框。

这样一通操作下来，我们就从模型输出的一堆“谜之数字”，得到了清晰的识别结果：**画面中出现了哪个数字、它在哪儿、识别有多靠谱，框框也画好了！**这一步就是传说中的“后处理”阶段，整个流程才算真正跑通了！

下图说明了后处理过程的主要工作：

![postprocess](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/97e39e174ae7.png)

模型推理结束后，模型的输出`tensor`被转换成`ulab.numpy.ndarray`格式存放在`results`中。用户可以根据应用场景的需求实现后处理。比如，对YOLOv8模型的输出实现后处理得到检测框的坐标和类别信息。首先要了解输出的含义，对于[1,8,2100]的输出，8表示4个数据是坐标信息和4个类的分数，后处理过程需要找到分数最大的类别索引和类别分数，并将坐标信息使用预处理时计算的比例复原回原图尺寸，从**中心点+宽高格式**转换成**左上右下坐标格式**，然后使用置信度阈值筛掉一部分框，再使用NMS（非极大值抑制）方法筛掉冗余重叠框，最后得到的才是基于原图的检测框信息。针对**四类打印数字识别**，我们给出该任务后处理的MicroPython**核心代码**（此代码仅用于说明，无法直接运行）如下：

```python
import os,sys
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc
from libs.Utils import *

# 多目标检测非最大值抑制方法实现
def nms(boxes,scores,thresh):
    """Pure Python NMS baseline."""
    x1,y1,x2,y2 = boxes[:, 0],boxes[:, 1],boxes[:, 2],boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = np.argsort(scores,axis = 0)[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        new_x1,new_y1,new_x2,new_y2,new_areas = [],[],[],[],[]
        for order_i in order:
            new_x1.append(x1[order_i])
            new_x2.append(x2[order_i])
            new_y1.append(y1[order_i])
            new_y2.append(y2[order_i])
            new_areas.append(areas[order_i])
        new_x1 = np.array(new_x1)
        new_x2 = np.array(new_x2)
        new_y1 = np.array(new_y1)
        new_y2 = np.array(new_y2)
        xx1 = np.maximum(x1[i], new_x1)
        yy1 = np.maximum(y1[i], new_y1)
        xx2 = np.minimum(x2[i], new_x2)
        yy2 = np.minimum(y2[i], new_y2)
        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        new_areas = np.array(new_areas)
        ovr = inter / (areas[i] + new_areas - inter)
        new_order = []
        for ovr_i,ind in enumerate(ovr):
            if ind < thresh:
                new_order.append(order[ovr_i])
        # 这里存的是框索引，用uint16避免框数超过255时溢出（ulab支持uint8/int8/uint16/int16/float）
        order = np.array(new_order,dtype=np.uint16)
    return keep

# 假设results中包含模型推理的输出数据
results=[]

#------------------------推理输出的后处理步骤----------------------------------------
# 模型输出只有1个，也就是results[0]的shape为[1, 8，2100]，转换成[2100,8]方便依次处理每个框
output_data=results[0][0].transpose()
# 每个框前四个数据为中心点坐标和宽高
boxes_ori = output_data[:,0:4]
# 剩余数据为每个类别的分数，通过argmax找到分数最大的类别编号和分数值
class_ori = output_data[:,4:]
class_res=np.argmax(class_ori,axis=-1)
scores_ = np.max(class_ori,axis=-1)
# 通过置信度阈值筛选框（小于置信度阈值的丢弃），同时处理坐标为x1,y1,x2,y2，为框的左上和右下的坐标,注意比例变换，将输入分辨率坐标(model_input_size)转换成原图坐标(AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT)
boxes,inds,scores=[],[],[]
for i in range(len(boxes_ori)):
    if scores_[i]>confidence_threshold:
        x,y,w,h=boxes_ori[i][0],boxes_ori[i][1],boxes_ori[i][2],boxes_ori[i][3]
        x1 = int((x - 0.5 * w)/ratio)
        y1 = int((y - 0.5 * h)/ratio)
        x2 = int((x + 0.5 * w)/ratio)
        y2 = int((y + 0.5 * h)/ratio)
        boxes.append([x1,y1,x2,y2])
        inds.append(class_res[i])
        scores.append(scores_[i])
#如果第一轮筛选后还有框，继续下一帧处理
if len(boxes)!=0:
    # 将list转换成ulab.numpy.ndarray方便处理
    boxes = np.array(boxes)
    scores = np.array(scores)
    inds = np.array(inds)
    # NMS过程,去除重叠的冗余框，keep为NMS处理后剩余框的索引列表
    keep = nms(boxes,scores,nms_threshold)
    dets = np.concatenate((boxes, scores.reshape((len(boxes),1)), inds.reshape((len(boxes),1))), axis=1)
    # 得到最后的检测框的结果
    det_res = []
    for keep_i in keep:
        det_res.append(dets[keep_i])
    det_res = np.array(det_res)
    print("boxes number:",det_res.shape[0])
```

上述代码给出了YOLOv8 四类打印数字识别模型的后处理步骤，这里的后处理全部使用MicroPython模块实现，效率不高。

针对这一特点，我们使用C++对YOLO相关的后处理做了封装。YOLO相关的模型可以使用该方法，参考：[yolo_battle](./example/ai/yolo_battle.md)。
  
### 结果绘制

现在我们已经得到了识别结果啦！每个数字的“身份”和“位置”我们都知道了，接下来就是让这些结果**变得“看得见”**——也就是在图像上画出检测框、标上数字，告诉大家：“看！这里有个 1！”、“那边是个 3！”

不过，事情没那么简单——你的模型是对 320×320 的图像做的识别，但屏幕可能是 800×480、1920×1080，甚至别的尺寸。如果直接把模型的框画在屏幕上，那位置可能就全歪了！所以我们要做一件非常重要的事：**把图像坐标“映射”成屏幕坐标**，也就是说把框的位置按比例转换一下，让它在屏幕上刚刚好。

画这些识别信息的时候，我们一般不会直接动原图，而是创建一个叫做 **OSD（On-Screen Display）和屏幕一样大**的“透明图层”，就像在照片上贴了一张玻璃膜，我们就在这上面画框、标类别，不会影响底下的画面。

最后一步，就是把这个 OSD 图层和原始图像叠加在一起，一起显示到屏幕上！这样你就能清楚地看到：每个数字被识别出来了，框也画得妥妥的！

下图给出了绘制结果的流程：

![draw_result](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/388cdce4fc79.png)

以**四类打印数字识别**的检测框为例，我们计算得到的检测框坐标是基于输入原图分辨率的，如果要在屏幕上实现显示，我们需要将坐标等比例转换成屏幕坐标分辨率下的坐标，然后将效果绘制在初始化透明图像的`osd_img`上，然后调用`Display`模块的`show_image`方法实现显示。这里给出核心代码（此代码仅用于说明，无法直接运行）如下：

```python
import os,sys
from media.display import *
import ulab.numpy as np
import time,image,random,gc
from libs.Utils import *

#-----------------------------Display初始化部分-------------------------------

# 定义屏幕显示分辨率
DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# 定义AI推理帧分辨率
AI_RGB888P_WIDTH = ALIGN_UP(1280, 16)
AI_RGB888P_HEIGHT = 720
labels=["0","1","2","3"]
max_boxes_num = 30
# 获取颜色值
colors=get_colors(len(labels))

# OSD图像初始化,创建一帧和屏幕分辨率同样大的透明图像，用于绘制AI推理结果
osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

# 设置为st7701,默认800*480
Display.init(Display.ST7701,width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1, to_ide = True)

# 这里取了前max_boxes_num的框，防止框数量过多
det_res = det_res[:max_boxes_num, :]
#------------------------绘制检测框结果----------------------------------------
osd_img.clear()
# 分别处理每一个框，将原图坐标(AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT)转换成显示屏幕坐标(DISPLAY_WIDTH,DISPLAY_HEIGHT)
for det in det_res:
    x_1, y_1, x_2, y_2 = map(lambda pos: int(round(pos, 0)), det[:4])
    draw_x= int(x_1 * DISPLAY_WIDTH // AI_RGB888P_WIDTH)
    draw_y= int(y_1 * DISPLAY_HEIGHT // AI_RGB888P_HEIGHT)
    draw_w = int((x_2 - x_1) * DISPLAY_WIDTH // AI_RGB888P_WIDTH)
    draw_h = int((y_2 - y_1) * DISPLAY_HEIGHT // AI_RGB888P_HEIGHT)
    osd_img.draw_rectangle(draw_x,draw_y, draw_w, draw_h, color=colors[int(det[5])],thickness=4)
    osd_img.draw_string_advanced( draw_x , max(0,draw_y-50), 24, labels[int(det[5])] + " {0:.3f}".format(det[4]), color=colors[int(det[5])])
#------------------------在屏幕显示检测框结果----------------------------------------
Display.show_image(osd_img)
```

通过上述步骤，我们基本上就完成了使用MicroPython的开发一个应用的完整步骤。用户从转模型开始，需要对模型推理的整个过程有比较好的了解。
  
### 显示设备介绍

对于显示输出，k230提供了三种显示设备，你可以选择使用`HDMI/LCD屏幕/IDE`三种方式中的一种。对应模块的API文档见链接：[Display模块API文档](./api/mpp/k230_canmv_display_module_api_manual.md)。下面分别介绍这三种方式：

🏷️ **HDMI**：设备类型为`LT9611`，可以参照API文档查看初始化时支持的分辨率、帧率、osd数目和是否IDE同步显示。在双通道AI推理下，一般还会创建一帧和屏幕显示分辨率同样大的OSD透明图像用于绘制推理结果。调用`Display.show_image`接口时需要注意OSD显示的图层编号，OSD仅支持在`LAYER_OSD0`/`LAYER_OSD1`/`LAYER_OSD2`/`LAYER_OSD3`四层显示。示例代码如下：

```python
import os,sys
from media.display import *
from media.media import *

# 定义屏幕显示分辨率
DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# OSD图像初始化,创建一帧和屏幕分辨率同样大的透明图像，用于绘制AI推理结果
osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

# 设置为LT9611显示，默认1920x1080
Display.init(Display.LT9611,width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1, to_ide = True)

MediaManager.init()
```

🏷️ **LCD**：设备类型为`ST7701`或`HX8399`，可以参照API文档查看初始化时支持的分辨率、帧率、osd数目和是否IDE同步显示。在双通道AI推理下，一般还会创建一帧和屏幕显示分辨率同样大的OSD透明图像用于绘制推理结果。调用`Display.show_image`接口时需要注意OSD显示的图层编号，OSD仅支持在`LAYER_OSD0`/`LAYER_OSD1`/`LAYER_OSD2`/`LAYER_OSD3`四层显示。示例代码如下：

```python
import os,sys
from media.display import *
from media.media import *

# 定义屏幕显示分辨率
DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# OSD图像初始化,创建一帧和屏幕分辨率同样大的透明图像，用于绘制AI推理结果
osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

## 如果使用ST7701的LCD屏幕显示，默认800*480,还支持640*480等，具体参考Display模块API文档
Display.init(Display.ST7701, width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1, to_ide=True)

MediaManager.init()
```

🏷️ **CanMV IDE预览窗口**：设备类型为`VIRT`，可以参照API文档查看初始化时支持的分辨率、帧率、osd数目。该模式下只会在IDE的右上方预览窗口中查看图像效果，不在外接屏幕上显示内容。用户可在[64,64]到[4096,4096]和帧率1~200之间进行配置。示例代码如下：

```python
import os,sys
from media.display import *
from media.media import *

# 定义屏幕显示分辨率
DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# OSD图像初始化,创建一帧和屏幕分辨率同样大的透明图像，用于绘制AI推理结果
osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

## 如果使用VIRT在CanMV IDE上显示
Display.init(Display.VIRT, width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1)

MediaManager.init()
```

🏷️ **CanMV IDE预览图片**：设备类型为`VIRT`，可以参照API文档查看初始化时支持的分辨率、帧率、osd数目。该模式下只会在IDE的右上方预览窗口中查看图像效果，不在外接屏幕上显示内容。用户使用`image`实例调用`compress_for_ide()`实现在CanMV IDE预览窗口显示静态图像。示例代码如下：

```python
import os,sys
import image

#-----------------------------读取图片部分-------------------------------
# 请自行将测试图片拷贝到开发板data目录下
img_path="/data/test.jpg"

# 使用图片创建Image实例，类型为jpeg
img_data = image.Image(img_path)
# 将图片数据转换成rgb888格式的Image实例，该类型数据是RGB三通道，颜色范围为[0,255]
img_rgb888=img_data.to_rgb888()

img_rgb888.compress_for_ide()
```

### 类打印数字识别部署代码

我们已经为你准备好了完整的“0”、“1”、“2”、“3”四类打印数字识别的示例代码，**不仅支持单张图片的推理**，还支持**实时视频流的连续识别**！无论你是想在静态图片上测试模型效果，还是在接入摄像头后实时检测，都可以快速上手。你只需要用前面步骤中导出的 `kmodel` 模型，配合我们提供的示例脚本，就可以轻松在 K230 开发板上部署运行啦！

如果你想验证模型在图片上的识别精度和定位效果，可以直接跑我们的 **图片识别代码**；如果你想实时体验识别过程中的“视频效果”，那就试试 **双通道视频识别代码**，看看数字出现在屏幕上的那一刻，框框是不是能精准追踪到位！

接下来你就可以大胆动手试试部署流程，感受 K230 端侧 AI 的运行效果，AI 就能读懂你拍下的数字世界！

#### 图片识别代码

这里给出完整的**4类打印数字识别**图片推理代码，您可以使用上面步骤得到的kmodel进行测试：

```python
import os,sys
from media.sensor import *
from media.display import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc
from libs.Utils import *

#-----------------------------其他必要方法---------------------------------------------
# 多目标检测 非最大值抑制方法实现
def nms(boxes,scores,thresh):
    """Pure Python NMS baseline."""
    x1,y1,x2,y2 = boxes[:, 0],boxes[:, 1],boxes[:, 2],boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = np.argsort(scores,axis = 0)[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        new_x1,new_y1,new_x2,new_y2,new_areas = [],[],[],[],[]
        for order_i in order:
            new_x1.append(x1[order_i])
            new_x2.append(x2[order_i])
            new_y1.append(y1[order_i])
            new_y2.append(y2[order_i])
            new_areas.append(areas[order_i])
        new_x1 = np.array(new_x1)
        new_x2 = np.array(new_x2)
        new_y1 = np.array(new_y1)
        new_y2 = np.array(new_y2)
        xx1 = np.maximum(x1[i], new_x1)
        yy1 = np.maximum(y1[i], new_y1)
        xx2 = np.minimum(x2[i], new_x2)
        yy2 = np.minimum(y2[i], new_y2)
        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        new_areas = np.array(new_areas)
        ovr = inter / (areas[i] + new_areas - inter)
        new_order = []
        for ovr_i,ind in enumerate(ovr):
            if ind < thresh:
                new_order.append(order[ovr_i])
        # 这里存的是框索引，用uint16避免框数超过255时溢出（ulab支持uint8/int8/uint16/int16/float）
        order = np.array(new_order,dtype=np.uint16)
    return keep

# 计算padding缩放比例和上下左右padding大小
def letterbox_pad_param(input_size,output_size):
    ratio_w = output_size[0] / input_size[0]  # 宽度缩放比例
    ratio_h = output_size[1] / input_size[1]   # 高度缩放比例
    ratio = min(ratio_w, ratio_h)  # 取较小的缩放比例
    new_w = int(ratio * input_size[0])  # 新宽度
    new_h = int(ratio * input_size[1])  # 新高度
    dw = (output_size[0] - new_w) / 2  # 宽度差
    dh = (output_size[1] - new_h) / 2  # 高度差
    top = int(round(0))
    bottom = int(round(dh * 2 + 0.1))
    left = int(round(0))
    right = int(round(dw * 2 - 0.1))
    return top, bottom, left, right,ratio


if __name__=="__main__":
    # 请自行将测试图片拷贝到开发板sdcard目录下
    img_path="/sdcard/test.jpg"
    
    # 使用图片创建Image实例，类型为jpeg
    img_data = image.Image(img_path)
    img_width=img_data.width()
    img_height=img_data.height()
    # 将图片数据转换成rgb888格式的Image实例，该类型数据是RGB三通道，颜色范围为[0,255]
    img_rgb888=img_data.to_rgb888()
    # 将Image实例转换成ulab.numpy.ndarray类型,这是数据是HWC类型的
    img_hwc=img_rgb888.to_numpy_ref()
    # 获取hwc排布的shape,使用ulab.numpy的transpose方法将hwc转换为chw排布
    shape=img_hwc.shape
    img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
    img_trans = img_tmp.transpose()
    img_tmp=img_trans.copy()
    img_chw=img_tmp.reshape((shape[2],shape[0],shape[1]))
    # 使用chw数据创建nncase_runtime runtime_tensor，可以给kmodel模型推理使用
    ai2d_input_tensor=nn.from_numpy(img_chw)
    
    
    #-----------------------------AI模型初始化部分-------------------------------
    # Kmodel模型路径
    kmodel_path="/sdcard/best.kmodel"
    # 类别标签
    labels = ["0","1","2","3"]
    # 模型输入分辨率
    model_input_size=[320,320]
    # 其它参数设置，包括阈值、最大检测框数量等
    confidence_threshold = 0.5
    nms_threshold = 0.4
    max_boxes_num = 30
    # 不同类别框的颜色
    colors=get_colors(len(labels))
    
    # 初始化ai2d预处理，并配置ai2d padding+resize预处理，预处理过程输入分辨率为图片分辨率，输出分辨率模型输入的需求分辨率，实现image->preprocess->model的过程
    ai2d=nn.ai2d()
    # 配置ai2d模块的输入输出数据类型和格式
    ai2d.set_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
    # 设置padding的参数，上下左右padding的大小和三个通道padding的具体值
    top,bottom,left,right,ratio=letterbox_pad_param([img_width,img_height],model_input_size)
    ai2d.set_pad_param(True,[0,0,0,0,top,bottom,left,right], 0, [128,128,128])
    # 设置resize参数，配置插值方法
    ai2d.set_resize_param(True,nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
    # 设置ai2d模块的输入输出维度，并构建builder实例
    ai2d_builder = ai2d.build([1,3,img_height,img_width], [1,3,model_input_size[1],model_input_size[0]])
    # 初始化一个空的tensor，用于ai2d输出
    input_init_data = np.ones((1,3,model_input_size[1],model_input_size[0]),dtype=np.uint8)
    kpu_input_tensor = nn.from_numpy(input_init_data)
    
    # 创建kpu实例
    kpu=nn.kpu()
    # 加载kmodel模型
    kpu.load_kmodel(kmodel_path)
    
    #------------------------推理前的预处理步骤----------------------------------------
    # 执行预处理过程
    ai2d_builder.run(ai2d_input_tensor, kpu_input_tensor)
    #------------------------使用kpu完成模型推理--------------------------------------
    # 设置kpu的第0个输入为ai2d预处理后的tensor，如果有多个，可以依次设置
    kpu.set_input_tensor(0,kpu_input_tensor)
    # 在kpu上执行模型推理
    kpu.run()
    #------------------------获取模型推理结束的输出----------------------------------------
    # 获取模型推理的输出tensor，并将其转换成ulab.numpy.ndarray数据进行后处理
    results=[]
    for i in range(kpu.outputs_size()):
        output_i_tensor = kpu.get_output_tensor(i)
        result_i = output_i_tensor.to_numpy()
        results.append(result_i)
        del output_i_tensor
    #------------------------推理输出的后处理步骤----------------------------------------
    # 模型输出只有1个，也就是results[0]的shape为[1, 8，2100]，转换成[2100,8]方便依次处理每个框
    output_data=results[0][0].transpose()
    # 每个框前四个数据为中心点坐标和宽高
    boxes_ori = output_data[:,0:4]
    # 剩余数据为每个类别的分数，通过argmax找到分数最大的类别编号和分数值
    class_ori = output_data[:,4:]
    class_res=np.argmax(class_ori,axis=-1)
    scores_ = np.max(class_ori,axis=-1)
    # 通过置信度阈值筛选框（小于置信度阈值的丢弃），同时处理坐标为x1,y1,x2,y2，为框的左上和右下的坐标,注意比例变换，将输入分辨率坐标(model_input_size)转换成原图坐标(img_width,img_height)
    boxes,inds,scores=[],[],[]
    for i in range(len(boxes_ori)):
        if scores_[i]>confidence_threshold:
            x,y,w,h=boxes_ori[i][0],boxes_ori[i][1],boxes_ori[i][2],boxes_ori[i][3]
            x1 = int((x - 0.5 * w)/ratio)
            y1 = int((y - 0.5 * h)/ratio)
            x2 = int((x + 0.5 * w)/ratio)
            y2 = int((y + 0.5 * h)/ratio)
            boxes.append([x1,y1,x2,y2])
            inds.append(class_res[i])
            scores.append(scores_[i])
    #如果第一轮筛选后有框，继续下一帧处理
    if len(boxes)!=0:
        # 将list转换成ulab.numpy.ndarray方便处理
        boxes = np.array(boxes)
        scores = np.array(scores)
        inds = np.array(inds)
        # NMS过程,去除重叠的冗余框，keep为NMS去除重叠框后的索引列表
        keep = nms(boxes,scores,nms_threshold)
        dets = np.concatenate((boxes, scores.reshape((len(boxes),1)), inds.reshape((len(boxes),1))), axis=1)
        # 得到最后的检测框的结果
        det_res = []
        for keep_i in keep:
            det_res.append(dets[keep_i])
        det_res = np.array(det_res)
        # 去前max_box_num个，防止检测框过多
        det_res = det_res[:max_boxes_num, :]
        #------------------------绘制检测框结果----------------------------------------
        # 分别处理每一个框,绘制结果
        for det in det_res:
            x_1, y_1, x_2, y_2 = map(lambda pos: int(round(pos, 0)), det[:4])
            draw_x= int(x_1)
            draw_y= int(y_1)
            draw_w = int((x_2 - x_1))
            draw_h = int((y_2 - y_1))
            img_rgb888.draw_rectangle(draw_x,draw_y, draw_w, draw_h, color=colors[int(det[5])],thickness=4)
            img_rgb888.draw_string_advanced( draw_x , max(0,draw_y-50), 24, "类别:"+labels[int(det[5])] + "  分数:{0:.3f}".format(det[4]), color=colors[int(det[5])])
        #------------------------在屏幕显示检测框结果----------------------------------------
        img_rgb888.compress_for_ide()
    #释放资源
    del ai2d
    del kpu
    del ai2d_input_tensor
    del kpu_input_tensor
    nn.shrink_memory_pool()
    gc.collect()
```

#### 双通道视频识别代码

这里给出完整的**4类打印数字识别**视频推理代码，您可以使用上面步骤得到的kmodel进行测试：

```python
import os,sys
from media.sensor import *
from media.display import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc
from libs.Utils import *

#-----------------------------其他必要方法---------------------------------------------
# 多目标检测 非最大值抑制方法实现
def nms(boxes,scores,thresh):
    """Pure Python NMS baseline."""
    x1,y1,x2,y2 = boxes[:, 0],boxes[:, 1],boxes[:, 2],boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = np.argsort(scores,axis = 0)[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        new_x1,new_y1,new_x2,new_y2,new_areas = [],[],[],[],[]
        for order_i in order:
            new_x1.append(x1[order_i])
            new_x2.append(x2[order_i])
            new_y1.append(y1[order_i])
            new_y2.append(y2[order_i])
            new_areas.append(areas[order_i])
        new_x1 = np.array(new_x1)
        new_x2 = np.array(new_x2)
        new_y1 = np.array(new_y1)
        new_y2 = np.array(new_y2)
        xx1 = np.maximum(x1[i], new_x1)
        yy1 = np.maximum(y1[i], new_y1)
        xx2 = np.minimum(x2[i], new_x2)
        yy2 = np.minimum(y2[i], new_y2)
        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        new_areas = np.array(new_areas)
        ovr = inter / (areas[i] + new_areas - inter)
        new_order = []
        for ovr_i,ind in enumerate(ovr):
            if ind < thresh:
                new_order.append(order[ovr_i])
        # 这里存的是框索引，用uint16避免框数超过255时溢出（ulab支持uint8/int8/uint16/int16/float）
        order = np.array(new_order,dtype=np.uint16)
    return keep

# 计算padding缩放比例和上下左右padding大小
def letterbox_pad_param(input_size,output_size):
    ratio_w = output_size[0] / input_size[0]  # 宽度缩放比例
    ratio_h = output_size[1] / input_size[1]   # 高度缩放比例
    ratio = min(ratio_w, ratio_h)  # 取较小的缩放比例
    new_w = int(ratio * input_size[0])  # 新宽度
    new_h = int(ratio * input_size[1])  # 新高度
    dw = (output_size[0] - new_w) / 2  # 宽度差
    dh = (output_size[1] - new_h) / 2  # 高度差
    top = int(round(0))
    bottom = int(round(dh * 2 + 0.1))
    left = int(round(0))
    right = int(round(dw * 2 - 0.1))
    return top, bottom, left, right,ratio


#-----------------------------Sensor/Display初始化部分-------------------------------

# 定义屏幕显示分辨率
DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

# 定义AI推理帧分辨率
AI_RGB888P_WIDTH = ALIGN_UP(1280, 16)
AI_RGB888P_HEIGHT = 720

sensor = Sensor()
sensor.reset()
# 设置水平镜像和垂直翻转，不同板子的方向不同，通过配置这两个参数使画面转正
#sensor.set_hmirror(False)
#sensor.set_vflip(False)

# 配置sensor的多通道出图，每个通道的出图格式和分辨率可以不同，最多可以出三路图，参考sensor API文档
# 通道0直接给到显示VO，格式为YUV420
sensor.set_framesize(width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT,chn=CAM_CHN_ID_0)
sensor.set_pixformat(Sensor.YUV420SP,chn=CAM_CHN_ID_0)
# 通道1给到AI做算法处理，格式为RGB888P
sensor.set_framesize(width = AI_RGB888P_WIDTH , height = AI_RGB888P_HEIGHT, chn=CAM_CHN_ID_1)
sensor.set_pixformat(Sensor.RGBP888, chn=CAM_CHN_ID_1)

# 绑定通道0的摄像头图像到屏幕，防止另一个通道的AI推理过程太慢影响显示过程，导致出现卡顿效果
sensor_bind_info = sensor.bind_info(x = 0, y = 0, chn = CAM_CHN_ID_0)
Display.bind_layer(**sensor_bind_info, layer = Display.LAYER_VIDEO1)

# OSD图像初始化,创建一帧和屏幕分辨率同样大的透明图像，用于绘制AI推理结果
osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

## 设置为LT9611显示，默认1920x1080
#Display.init(Display.LT9611,width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1, to_ide = True)
# 如果使用ST7701的LCD屏幕显示，默认800*480,还支持640*480等，具体参考Display模块API文档
Display.init(Display.ST7701, width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,osd_num=1, to_ide=True)

# 限制bind通道的帧率，防止生产者太快
sensor._set_chn_fps(chn = CAM_CHN_ID_0, fps = Display.fps())


#-----------------------------AI模型初始化部分-------------------------------
# Kmodel模型路径
kmodel_path="/sdcard/best.kmodel"
# 类别标签
labels = ["0","1","2","3"]
# 模型输入分辨率
model_input_size=[320,320]
# 其它参数设置，包括阈值、最大检测框数量等
confidence_threshold = 0.3
nms_threshold = 0.4
max_boxes_num = 50
# 不同类别框的颜色
colors=get_colors(len(labels))

# 初始化ai2d预处理，并配置ai2d padding+resize预处理，预处理过程输入分辨率为图片分辨率，输出分辨率模型输入的需求分辨率，实现image->preprocess->model的过程
ai2d=nn.ai2d()
# 配置ai2d模块的输入输出数据类型和格式
ai2d.set_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)
# 设置padding的参数，上下左右padding的大小和三个通道padding的具体值
top,bottom,left,right,ratio=letterbox_pad_param([AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT],model_input_size)
ai2d.set_pad_param(True,[0,0,0,0,top,bottom,left,right], 0, [128,128,128])
# 设置resize参数，配置插值方法
ai2d.set_resize_param(True,nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
# 设置ai2d模块的输入输出维度，并构建builder实例
ai2d_builder = ai2d.build([1,3,AI_RGB888P_HEIGHT,AI_RGB888P_WIDTH], [1,3,model_input_size[1],model_input_size[0]])
# 初始化一个空的tensor，用于ai2d输出和kpu输入，因为一般ai2d的输出会直接送给kpu，因此这里使用一个变量共用
input_init_data = np.ones((1,3,model_input_size[1],model_input_size[0]),dtype=np.uint8)
kpu_input_tensor = nn.from_numpy(input_init_data)


# 创建kpu实例
kpu=nn.kpu()
# 加载kmodel模型
kpu.load_kmodel(kmodel_path)

# media初始化
MediaManager.init()
# 启动sensor
sensor.run()
# 测试帧率
fps = time.clock()
while True:
    fps.tick()
    #------------------------从摄像头dump一帧图像并处理----------------------------------
    # 从摄像头1通道dump一帧RGB888P格式的Image图像
    img=sensor.snapshot(chn=CAM_CHN_ID_1)
    # 转换成ulab.numpy.ndarray格式的数据，CHW
    img_np=img.to_numpy_ref()
    # 创建nncase_runtime.tensor用于给到ai2d进行预处理
    ai2d_input_tensor=nn.from_numpy(img_np)
    #------------------------推理前的预处理步骤----------------------------------------
    # 执行预处理过程
    ai2d_builder.run(ai2d_input_tensor, kpu_input_tensor)
    #------------------------使用kpu完成模型推理--------------------------------------
    # 设置kpu的第0个输入为ai2d预处理后的tensor，如果有多个，可以依次设置
    kpu.set_input_tensor(0,kpu_input_tensor)
    # 在kpu上执行模型推理
    kpu.run()
    #------------------------获取模型推理结束的输出----------------------------------------
    # 获取模型推理的输出tensor，并将其转换成ulab.numpy.ndarray数据进行后处理
    results=[]
    for i in range(kpu.outputs_size()):
        output_i_tensor = kpu.get_output_tensor(i)
        result_i = output_i_tensor.to_numpy()
        results.append(result_i)
        del output_i_tensor
    #------------------------推理输出的后处理步骤----------------------------------------
    # YOLOv8检测模型输出只有1个，也就是results[0]的shape为[1,box_dim，box_num]，results[0][0]表示[box_dim,box_num]，转换成[box_num,box_dim]方便依次处理每个框
    output_data=results[0][0].transpose()
    # 每个框前四个数据为中心点坐标和宽高
    boxes_ori = output_data[:,0:4]
    # 剩余数据为每个类别的分数，通过argmax找到分数最大的类别编号和分数值
    class_ori = output_data[:,4:]
    class_res=np.argmax(class_ori,axis=-1)
    scores_ = np.max(class_ori,axis=-1)
    # 通过置信度阈值筛选框（小于置信度阈值的丢弃），同时处理坐标为x1,y1,x2,y2，为框的左上和右下的坐标,注意比例变换，将输入分辨率坐标(model_input_size)转换成原图坐标(AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT)
    boxes,inds,scores=[],[],[]
    for i in range(len(boxes_ori)):
        if scores_[i]>confidence_threshold:
            x,y,w,h=boxes_ori[i][0],boxes_ori[i][1],boxes_ori[i][2],boxes_ori[i][3]
            x1 = int((x - 0.5 * w)/ratio)
            y1 = int((y - 0.5 * h)/ratio)
            x2 = int((x + 0.5 * w)/ratio)
            y2 = int((y + 0.5 * h)/ratio)
            boxes.append([x1,y1,x2,y2])
            inds.append(class_res[i])
            scores.append(scores_[i])
    osd_img.clear()
    #如果第一轮筛选后有框，继续下一帧处理
    if len(boxes)!=0:
        # 将list转换成ulab.numpy.ndarray方便处理
        boxes = np.array(boxes)
        scores = np.array(scores)
        inds = np.array(inds)
        # NMS过程,去除重叠的冗余框，keep为NMS去除重叠框后的索引列表
        keep = nms(boxes,scores,nms_threshold)
        dets = np.concatenate((boxes, scores.reshape((len(boxes),1)), inds.reshape((len(boxes),1))), axis=1)
        # 得到最后的检测框的结果
        det_res = []
        for keep_i in keep:
            det_res.append(dets[keep_i])
        det_res = np.array(det_res)
        # 去前max_box_num个，防止检测框过多
        det_res = det_res[:max_boxes_num, :]
        #------------------------绘制检测框结果----------------------------------------
        osd_img.clear()
        # 分别处理每一个框，将原图坐标(AI_RGB888P_WIDTH,AI_RGB888P_HEIGHT)转换成显示屏幕坐标(DISPLAY_WIDTH,DISPLAY_HEIGHT)
        for det in det_res:
            x_1, y_1, x_2, y_2 = map(lambda pos: int(round(pos, 0)), det[:4])
            draw_x= int(x_1 * DISPLAY_WIDTH // AI_RGB888P_WIDTH)
            draw_y= int(y_1 * DISPLAY_HEIGHT // AI_RGB888P_HEIGHT)
            draw_w = int((x_2 - x_1) * DISPLAY_WIDTH // AI_RGB888P_WIDTH)
            draw_h = int((y_2 - y_1) * DISPLAY_HEIGHT // AI_RGB888P_HEIGHT)
            osd_img.draw_rectangle(draw_x,draw_y, draw_w, draw_h, color=colors[int(det[5])],thickness=4)
            osd_img.draw_string_advanced( draw_x , max(0,draw_y-50), 24, "类别:"+labels[int(det[5])] + " 分数:{0:.3f}".format(det[4]), color=colors[int(det[5])])
    #------------------------在屏幕显示检测框结果----------------------------------------
    Display.show_image(osd_img)
    print("det fps:",fps.fps())
    gc.collect()

#退出循环，释放资源
del ai2d
del kpu
sensor.stop()
Display.deinit()
time.sleep_ms(50)
MediaManager.deinit()
nn.shrink_memory_pool()
```

## YOLO部署库

YOLO 是视觉任务中常用的模型，支持分类、检测、分割、旋转目标检测、关键点检测等任务。我们选择YOLO系列模型中经典的YOLOv5、YOLOv8、YOLO11和YOLO26为基础，封装了对应的MicroPython部署库（`libs/YOLO.py`），方便用户快速部署YOLO模型。具体内容见链接：[yolo_battle](./example/ai/yolo_battle.md)，API说明见：[YOLO 模块API手册](./api/aidemo/yolo_module_api_manual.md)。

### YOLOv5猫狗分类

基于YOLOv5模型实现猫狗分类模型在K230上的部署。

#### YOLOv5源码及训练环境搭建

`YOLOv5` 训练环境搭建请参考[ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5)

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

如果您已搭建好环境，请忽略此步骤。

#### 训练数据准备

请下载提供的示例数据集，示例数据集以猫狗分类为场景，使用YOLOv5完成训练。

```shell
cd yolov5
wget https://download.kendryte.com/developer/k230/yolo_dataset/cat_dog.zip
unzip cat_dog.zip
```

⚠️ **windows系统请直接复制链接到浏览器下载，并解压到对应目录**。

如果您已下载好数据，请忽略此步骤。

#### 使用YOLOv5训练猫狗分类模型

在 `yolov5` 目录下执行命令，使用 `yolov5` 训练猫狗分类模型：

```shell
python classify/train.py --model yolov5n-cls.pt --data cat_dog --epochs 100 --batch-size 8 --imgsz 224 --device '0'
```

#### 转换猫狗分类kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

下载脚本工具，将模型转换脚本工具 `test_yolov5.zip` 解压到 `yolov5` 目录下；

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

按照如下命令，对 `runs/train-cls/exp/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
python export.py --weight runs/train-cls/exp/weights/best.pt --imgsz 224 --batch 1 --include onnx
cd test_yolov5/classify
# 将test目录下的图片换成你自己的训练数据的一部分，转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/train-cls/exp/weights/best.onnx --dataset ../test --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

💡 **模型转换脚本(to_kmodel.py)参数说明**：

| 参数名称     | 描述     | 说明                                                         | 类型  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | 目标平台 | 可选项为k230/cpu，对应k230 kpu和cpu；                         | str   |
| model        | 模型路径 | 待转换的ONNX模型路径；                                        | str   |
| dataset      | 校准图片集  | 模型转换时使用的图片数据，在量化阶段使用，可以从训练数据中取一部分                    | str   |
| input_width  | 输入宽度 | 模型输入的宽度                                             | int   |
| input_height | 输入高度 | 模型输入的高度                                             | int   |
| ptq_option   | 量化方式 | 量化策略为`Kld`和`NoClip`,组合data和weights的量化精度,0为`NoClip`+[uint8,uint8], 1为`NoClip`+[uint8,int16], 2为`NoClip`+[int16,uint8]，3为`Kld`+[uint8,uint8], 4为`Kld`+[uint8,int16], 5为`Kld`+[int16,uint8] | 0/1/2/3/4/5 |

#### 在k230上使用MicroPython部署模型

##### 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请按照您的开发板类型下载最新的 [Dalily Build固件](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](./userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230))，在 IDE 中编写代码并运行。

##### 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

##### YOLOv5 模块

`YOLOv5` 类集成了 `YOLOv5` 的三种任务，包括分类(classify)、检测(detect)、分割(segment)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLOv5` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLOv5
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持三类任务，可选项为'classify'/'detect'/'segment'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv5模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

##### 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["cat","dog"]
    model_input_size=[224,224]

    confidence_threshold = 0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLOv5实例
    yolo=YOLOv5(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

##### 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["cat","dog"]
    model_input_size=[224,224]

    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定hdmi/lcd/st7701等，取值见PipeLine手册
    display_mode="auto"
    # None表示使用屏驱动的默认分辨率；需要指定时填[宽, 高]
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # create之后再取实际显示分辨率
    display_size=pl.get_display_size()
    # 初始化YOLOv5实例
    yolo=YOLOv5(task_type="classify",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

##### 部署效果

选择两张猫狗图片使用kmodel进行分类。效果如下图：

![cat_dog_cls_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/8545917e935e.png)

<a id="yolov8-fall-detection"></a>

### YOLOv8跌倒检测

基于YOLOv8模型实现跌倒检测模型在K230上的部署。

#### YOLOv8源码及训练环境搭建

`YOLOv8` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

#### 训练数据准备

下载提供的跌倒检测数据集，并解压。

```shell
cd yolov8
wget https://download.kendryte.com/developer/k230/yolo_dataset/fall_det.zip
unzip fall_det.zip
```

⚠️ **windows系统请直接复制链接到浏览器下载，并解压到对应目录**。

如果您已下载好数据，请忽略此步骤。

#### 使用YOLOv8训练跌倒检测模型

在 `yolov8` 目录下执行命令，使用 `yolov8` 训练跌倒检测模型：

```shell
yolo detect train data=fall_det.yaml model=yolov8n.pt epochs=300 imgsz=320
```

#### 转换跌倒检测kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

下载脚本工具，将模型转换脚本工具 `test_yolov8.zip` 解压到 `yolov8` 目录下；

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

按照如下命令，对 `runs/detect/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/detect
# 将test目录下的图片换成你自己的训练数据的一部分，转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 1
cd ../../
```

💡 **模型转换脚本(to_kmodel.py)参数说明**：

| 参数名称     | 描述     | 说明                                                         | 类型  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | 目标平台 | 可选项为k230/cpu，对应k230 kpu和cpu；                              | str   |
| model        | 模型路径 | 待转换的ONNX模型路径；                                        | str   |
| dataset      | 校准图片集  | 模型转换时使用的图片数据，在量化阶段使用，可以从训练集中取一部分图片替换                   | str   |
| input_width  | 输入宽度 | 模型输入的宽度                                             | int   |
| input_height | 输入高度 | 模型输入的高度                                             | int   |
| ptq_option   | 量化方式 | 量化策略为`Kld`和`NoClip`,组合data和weights的量化精度,0为`NoClip`+[uint8,uint8], 1为`NoClip`+[uint8,int16], 2为`NoClip`+[int16,uint8]，3为`Kld`+[uint8,uint8], 4为`Kld`+[uint8,int16], 5为`Kld`+[int16,uint8] | 0/1/2/3/4/5 |

#### 在k230上使用MicroPython部署模型

##### 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请按照您的开发板类型下载最新的 [Dalily Build固件](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](./userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230))，在 IDE 中编写代码并运行。

##### 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

##### YOLOv8 模块

`YOLOv8` 类集成了 `YOLOv8` 的五种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)、关键点检测(pose)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLOv8` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLOv8
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLOv8模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| kp_num           | 关键点个数     | 关键点检测任务中关键点的数量；                              | int        |
| kp_dim           | 关键点维度     | 关键点检测任务中关键点的维度，仅支持2和3，由训练模型决定；    | int【2/3】  |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

##### 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["fall"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    nms_threshold=0.45
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLOv8实例
    yolo=YOLOv8(task_type="detect",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

##### 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLOv8
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["fall"]
    model_input_size=[320,320]

    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定hdmi/lcd/st7701等，取值见PipeLine手册
    display_mode="auto"
    # None表示使用屏驱动的默认分辨率；需要指定时填[宽, 高]
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.5
    nms_threshold=0.45
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # create之后再取实际显示分辨率
    display_size=pl.get_display_size()
    # 初始化YOLOv8实例
    yolo=YOLOv8(task_type="detect",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            # 逐帧推理
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

##### 部署效果

选择一张跌倒图片使用kmodel进行跌倒检测。原图和推理结果的对比如下图：

![fall_det_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/fb96a4b49819.png)

### YOLO11水果分割

#### YOLO11源码及训练环境搭建

`YOLO11` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

#### 训练数据准备

下载提供的水果分割数据集，并解压。

```shell
cd yolo11
wget https://download.kendryte.com/developer/k230/yolo_dataset/fruit_seg.zip
unzip fruit_seg.zip
```

⚠️ **windows系统请直接复制链接到浏览器下载，并解压到对应目录**。

如果您已下载好数据，请忽略此步骤。

#### 使用YOLO11训练水果分割模型

在 `yolo11` 目录下执行命令，使用 `yolo11` 训练三类水果分割模型：

```shell
yolo segment train data=fruits_seg.yaml model=yolo11n-seg.pt epochs=100 imgsz=320
```

#### 转换水果分割kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

下载脚本工具，将模型转换脚本工具 `test_yolo11.zip` 解压到 `yolo11` 目录下；

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

按照如下命令，对 `runs/segment/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/segment
# test中的图片可以从训练集中选取一部分替换，转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 1
cd ../../
```

💡 **模型转换脚本(to_kmodel.py)参数说明**：

| 参数名称     | 描述     | 说明                                                         | 类型  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | 目标平台 | 可选项为k230/cpu，对应k230 kpu和cpu；                              | str   |
| model        | 模型路径 | 待转换的ONNX模型路径；                                        | str   |
| dataset      | 校准图片集  | 模型转换时使用的图片数据，在量化阶段使用，可以从训练集中取一部分替换                    | str   |
| input_width  | 输入宽度 | 模型输入的宽度                                             | int   |
| input_height | 输入高度 | 模型输入的高度                                             | int   |
| ptq_option   | 量化方式 | 量化策略为`Kld`和`NoClip`,组合data和weights的量化精度,0为`NoClip`+[uint8,uint8], 1为`NoClip`+[uint8,int16], 2为`NoClip`+[int16,uint8]，3为`Kld`+[uint8,uint8], 4为`Kld`+[uint8,int16], 5为`Kld`+[int16,uint8] | 0/1/2/3/4/5 |

#### 在k230上使用MicroPython部署模型

##### 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请按照您的开发板类型下载最新的 [Dalily Build固件](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](./userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230))，在 IDE 中编写代码并运行。

##### 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

##### YOLO11 模块

`YOLO11` 类集成了 `YOLO11` 的五种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)、关键点检测(pose)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLO11` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLO11
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLO11模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| kp_num           | 关键点个数     | 关键点检测任务中关键点的数量；                              | int        |
| kp_dim           | 关键点维度     | 关键点检测任务中关键点的维度，仅支持2和3，由训练模型决定；    | int【2/3】  |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

##### 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="segment",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

##### 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ["apple","banana","orange"]
    model_input_size=[320,320]

    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定hdmi/lcd/st7701等，取值见PipeLine手册
    display_mode="auto"
    # None表示使用屏驱动的默认分辨率；需要指定时填[宽, 高]
    display_size=None
    rgb888p_size=[320,320]
    confidence_threshold = 0.5
    nms_threshold=0.45
    mask_threshold=0.5
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # create之后再取实际显示分辨率
    display_size=pl.get_display_size()
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="segment",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,mask_thresh=mask_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            # 逐帧推理
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

##### 部署效果

选择一张水果图片使用kmodel进行水果分割。原图和推理结果的对比如下图：

![fruit_seg_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/6620fa927b45.png)

### YOLO11旋转目标检测

#### YOLO11源码及训练环境搭建

`YOLO11` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

#### 训练数据准备

下载桌面签字笔旋转目标检测数据集，并解压。

```shell
cd yolo11
wget https://download.kendryte.com/developer/k230/yolo_dataset/pen_obb.zip
unzip pen_obb.zip
```

⚠️ **windows系统请直接复制链接到浏览器下载，并解压到对应目录**。

如果您已下载好数据，请忽略此步骤。

#### 使用YOLO11旋转目标检测模型

在 `yolo11` 目录下执行命令，使用 `yolo11` 训练单类旋转目标检测模型：

```shell
yolo obb train data=pen_obb.yaml model=yolo11n-obb.pt epochs=100 imgsz=320
```

#### 转换旋转目标检测kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.11.0
pip install nncase-kpu==2.11.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx==1.15.0
pip install onnxruntime==1.19.0
pip install onnxsim==0.4.36
```

下载脚本工具，将模型转换脚本工具 `test_yolo11.zip` 解压到 `yolo11` 目录下；

```shell
wget https://download.kendryte.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

按照如下命令，对 `runs/obb/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/obb/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/obb
# test下图片可以从训练集中选择一部分替换，转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/obb/train/weights/best.onnx --dataset ../test_obb --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **模型转换脚本(to_kmodel.py)参数说明**：

| 参数名称     | 描述     | 说明                                                         | 类型  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | 目标平台 | 可选项为k230/cpu，对应k230 kpu和cpu；                              | str   |
| model        | 模型路径 | 待转换的ONNX模型路径；                                        | str   |
| dataset      | 校准图片集  | 模型转换时使用的图片数据，在量化阶段使用，可以从训练集中取一部分替换                    | str   |
| input_width  | 输入宽度 | 模型输入的宽度                                             | int   |
| input_height | 输入高度 | 模型输入的高度                                             | int   |
| ptq_option   | 量化方式 | 量化策略为`Kld`和`NoClip`,组合data和weights的量化精度,0为`NoClip`+[uint8,uint8], 1为`NoClip`+[uint8,int16], 2为`NoClip`+[int16,uint8]，3为`Kld`+[uint8,uint8], 4为`Kld`+[uint8,int16], 5为`Kld`+[int16,uint8] | 0/1/2/3/4/5 |

#### 在k230上使用MicroPython部署模型

##### 烧录镜像并安装CanMV IDE

💡 **固件介绍**：请按照您的开发板类型下载最新的 [Dalily Build固件](https://download.kendryte.com/developer/releases/canmv_k230_micropython/daily_build/) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](./userguide/how_to_build.md)。

下载并安装 CanMV IDE (下载链接：[CanMV IDE download](https://www.kendryte.com/zh/resource/ide,k230))，在 IDE 中编写代码并运行。

##### 模型文件拷贝

连接IDE，将转换好的模型和测试图片拷贝到路径 `CanMV/data` 目录下。该路径可以自定义，只需要在编写代码时修改对应路径即可。

##### YOLO11 模块

`YOLO11` 类集成了 `YOLO11` 的四种任务，包括分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)；支持两种推理模式，包括图片(image)和视频流(video)；该类封装了 `YOLO11` 的 kmodel 推理流程。

- **导入方法**

```python
from libs.YOLO import YOLO11
```

- **参数说明**

| 参数名称         | 描述           | 说明                                                         | 类型         |
| ---------------- | -------------- | ------------------------------------------------------------ | ------------ |
| task_type        | 任务类型       | 支持四类任务，可选项为'classify'/'detect'/'segment'/'obb'；        | str          |
| mode             | 推理模式       | 支持两种推理模式，可选项为'image'/'video'，'image'表示推理图片，'video'表示推理摄像头采集的实时视频流； | str          |
| kmodel_path      | kmodel路径     | 拷贝到开发板上kmodel路径；                                   | str          |
| labels           | 类别标签列表   | 不同类别的标签名称；                                         | list[str]    |
| rgb888p_size     | 推理帧分辨率   | 推理当前帧分辨率，如[1920,1080]、[1280,720]、[640,640];      | list[int]    |
| model_input_size | 模型输入分辨率 | YOLO11模型训练时的输入分辨率，如[224,224]、[320,320]、[640,640]； | list[int]    |
| display_size     | 显示分辨率     | 推理模式为'video'时设置，支持hdmi([1920,1080])和lcd([800,480]); | list[int]    |
| conf_thresh      | 置信度阈值     | 分类任务类别置信度阈值，检测分割任务的目标置信度阈值，如0.5； | float【0~1】 |
| nms_thresh       | nms阈值        | 非极大值抑制阈值，检测和分割任务必填；                       | float【0~1】 |
| mask_thresh      | mask阈值       | 分割任务中的对检测框中对象做分割时的二值化阈值；             | float【0~1】 |
| max_boxes_num    | 最大检测框数   | 一帧图像中允许返回的最多检测框数目；                         | int          |
| kp_num           | 关键点个数     | 关键点检测任务中关键点的数量；                              | int        |
| kp_dim           | 关键点维度     | 关键点检测任务中关键点的维度，仅支持2和3，由训练模型决定；    | int【2/3】  |
| debug_mode       | 调试模式       | 计时函数是否生效，可选项0/1，0为不计时，1为计时；            | int【0/1】   |

##### 部署模型实现图片推理

图片推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义参数变量**；

```python
from libs.YOLO import YOLO11
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的测试图片、模型路径、标签名称、模型输入大小
    img_path="/data/test_obb.jpg"
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    confidence_threshold = 0.1
    nms_threshold=0.6
    img,img_ori=read_image(img_path)
    rgb888p_size=[img.shape[2],img.shape[1]]
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="obb",mode="image",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=100,debug_mode=0)
    yolo.config_preprocess()
    res=yolo.run(img)
    yolo.draw_result(res,img_ori)
    yolo.deinit()
    gc.collect()
```

##### 部署模型实现视频推理

视频推理，请参考下述代码，**根据实际情况修改 `__main__` 中的定义变量**；

```python
from libs.PipeLine import PipeLine
from libs.Utils import *
from libs.YOLO import YOLO11
import os,sys,gc
import ulab.numpy as np
import image

if __name__=="__main__":
    # 这里仅为示例，自定义场景请修改为您自己的模型路径、标签名称、模型输入大小
    kmodel_path="/data/best.kmodel"
    labels = ['pen']
    model_input_size=[320,320]

    # 显示模式，"auto"按开发板型号自动选择屏驱动；也可显式指定hdmi/lcd/st7701等，取值见PipeLine手册
    display_mode="auto"
    # None表示使用屏驱动的默认分辨率；需要指定时填[宽, 高]
    display_size=None
    rgb888p_size=[640,360]
    confidence_threshold = 0.1
    nms_threshold=0.6
    # 初始化PipeLine
    pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
    pl.create()
    # create之后再取实际显示分辨率
    display_size=pl.get_display_size()
    # 初始化YOLO11实例
    yolo=YOLO11(task_type="obb",mode="video",kmodel_path=kmodel_path,labels=labels,rgb888p_size=rgb888p_size,model_input_size=model_input_size,display_size=display_size,conf_thresh=confidence_threshold,nms_thresh=nms_threshold,max_boxes_num=50,debug_mode=0)
    yolo.config_preprocess()
    while True:
        with ScopedTiming("total",1):
            # 逐帧推理
            img=pl.get_frame()
            res=yolo.run(img)
            yolo.draw_result(res,pl.osd_img)
            pl.show_image()
            gc.collect()
    yolo.deinit()
    pl.destroy()
```

##### 部署效果

选择一张桌面签字笔图片使用kmodel进行旋转目标检测。原图和推理结果的对比如下图：

![pen_obb_res](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/224584a9acac.png)

## 辅助工具

### 在线训练平台

#### 云训练平台简介

Canaan开发者社区模型训练功能是为简化开发流程，提高开发效率开放的训练平台。该平台使用户关注视觉场景的落地实现，更加快捷的完成从数据标注到获得部署包中的KModel模型的过程，并在搭载嘉楠科技Kendryte®系列AIoT芯片中K230、K230D芯片开发板上进行部署。用户仅需上传数据集，简单的配置参数就可以开始训练了。

![plat](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/04792fdbd787.png)

📌平台地址：**[嘉楠云训练平台](https://www.kendryte.com/zh/training/start)**

📌平台使用文档参考：**[嘉楠云训练平台文档教程](https://www.kendryte.com/web/CloudPlatDoc.html)**，请注意数据集的格式！

#### 支持任务介绍

云训练平台中对于K230系列芯片支持的视觉任务有7种，任务介绍如下表：

💡 **任务介绍**：

| 任务名称  | 任务说明                                                                                                           |
| ----- | --------------------------------------------------------------------------------------------------------------------- |
| 图像分类  | 对图片进行分类，得到图片的类别结果和分数。                                                                            |
| 图像检测  | 在图片中检测出目标物体，并给出物体的位置信息、类别信息和分数。                                                          |
| 语义分割  | 对图片中的目标区域进行分割，将图片中的不同标签区域切割出来，属于像素级任务。                                              |
| OCR检测 | 在图片中检测出文本区域，并给出文本区域的位置信息。                                                                        |
| OCR识别 | 在图片中识别出文本内容。                                                                                                |
| 度量学习  | 训练可以将图片特征化的模型，使用该模型创建特征库，通过特征对比，在不重新训练模型的前提下对新的类别进行分类，也可称为自学习。   |
| 多标签分类 | 对图片进行多类别分类，一些图片可能不只是属于某个单一的类别，天空和大海可以同时存在，得到图片的多标签分类结果。               |

#### 部署步骤

##### 部署包说明

训练结束后可以下载对应训练任务的部署包，下载的部署zip包解压后，目录如下：

```shell
📦 task_name
├── 📁 **_result
│   ├── test_0.jpg
│   ├── test_1.jpg
│   └──...
├── mp_deployment_source
├── **_image_1_2_2.py
├── **_image_1_3.py
├── **_video_1_2_2.py
├── **_video_1_3.py
└── README.pdf
```

内容如图所示：

![部署包](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/407be353913e.jpg)

其中`mp_deployment_source`即是在K230 MicroPython 镜像上部署的代码包，内部包含部署的配置文件和部署的KModel模型。

##### 文件拷贝

✅ **固件选择**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](./userguide/how_to_build.md)。

✅ **固件烧录**： 按照开发板类型烧录固件，固件烧录参考：[固件烧录](./userguide/how_to_burn_firmware.md)。

✅ **部署脚本**：固件烧录成功后，上电开机，您可以在文件系统根目录下发现`CanMV/sdcard`目录，将`mp_deployment_source`拷贝到`CanMV/sdcard`目录下。

##### 脚本运行

打开CanMV IDE K230，选择左上角`文件(F)`->`打开文件`->`选择CanMV/sdcard/examples/19-CloudPlatScripts`中的不同任务的脚本运行。

💡 **脚本介绍**：

|脚本名称|脚本说明|
|--|--|
|deploy_cls_image.py|图像分类单图推理脚本，您需要在自行增加测试图片，并修改脚本内读入图片的路径。|
|deploy_cls_video.py|图像分类视频流推理脚本，脚本详情见脚本内注释。|
|deploy_det_image.py|目标检测单图推理脚本，您需要在自行增加测试图片，并修改脚本内读入图片的路径。|
|deploy_det_video.py|目标检测视频流推理脚本，脚本详情见脚本内注释。|
|deploy_seg_image.py|语义分割单图推理脚本，您需要在自行增加测试图片，并修改脚本内读入图片的路径。|
|deploy_seg_video.py|语义分割视频流推理脚本，脚本详情见脚本内注释。|
|deploy_ocrdet_image.py|OCR检测单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。|
|deploy_ocrdet_video.py|OCR检测视频流推理脚本，脚本详情见脚本内注释。|
|deploy_ocrrec_image.py|OCR识别单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。考虑到平台OCR识别模型单次推理读入的数据为长条状文本，因此**不支持**视频流推理。|
|deploy_ocr_image.py|OCR单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。双模型任务，需要同时添加OCR检测和OCR识别的部署包，注意修改脚本内目录路径。|
|deploy_ocr_video.py|OCR视频流推理脚本，脚本详情见脚本内注释。双模型任务，需要同时添加OCR检测和OCR识别的部署包，注意修改脚本内目录路径。|
|deploy_ml_image.py|度量学习单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。输出为对应维度的特征，后续操作视应用场景修改。|
|deploy_ml_video.py|度量学习视频流推理脚本，脚本详情见脚本内注释。输出为对应维度的特征，后续操作视应用场景修改。|
|deploy_multl_image.py|多标签分类单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。|
|deploy_multl_video.py|多标签分类视频流推理脚本，脚本详情见脚本内注释。|

##### 部署说明

- 📢 在部署模型时如果效果不理想，首先调整对应任务的阈值和推理图像的分辨率，测试结果是否可以有好转！

- 📢 学会定位问题，比如查看部署包中的`**_results`目录下的测试图片，如果该图片正常，则可能是部署代码、模型转换或者阈值的问题！

- 📢 调整模型训练的参数，比如`epoch`、`learning_rate`等，防止出现训练不充分的情况！

### AICube

#### AICube简介

AICube是嘉楠为开发者提供的离线训练工具，该平台保证了数据安全性，实现可视化的本地训练。该平台支持图像分类、目标检测、语义分割、OCR检测、OCR识别、度量学习、多标签分类、异常检测共8个任务。其相对于在线训练平台，可以保证用户使用本地的GPU实现模型训练，并将模型转换成kmodel部署在K230上。

#### 环境准备和软件安装

在安装AICube前，请关注一下前提条件是否具备：

- 带有NVIDIA GPU的设备，推荐显存8G以上；

- 计算机已安装CUDA 11.7以及以上版本，已安装CUDNN；

- 计算机已安装dotnet 7.0，并将安装路径添加到环境变量；

- 推荐计算机内存在8GB以上，硬盘剩余空间至少20GB以上；

如果您的计算机满足上述条件，可以下载AICube并解压使用。AICube提供了ubuntu版本和windows版本的安装包，因为安装包内包含了配套的**torch训练环境、多个预训练模型和示例数据集**，因此安装包较大，**请在合适的网络环境下载**，下载地址见: [AICube下载](https://www.kendryte.com/zh/resource?selected=4-2)。使用步骤请参考对应版本的用户指南。

📢 **下载时请选择最新版本下载**。

#### 支持任务介绍

AICube中对于K230系列芯片支持的视觉任务有8种，任务介绍如下表：

💡 **任务介绍**：

| 任务名称  | 任务说明                                                                                                           |
| ----- | --------------------------------------------------------------------------------------------------------------------- |
| 图像分类  | 对图片进行分类，得到图片的类别结果和分数。                                                                            |
| 图像检测  | 在图片中检测出目标物体，并给出物体的位置信息、类别信息和分数。                                                          |
| 语义分割  | 对图片中的目标区域进行分割，将图片中的不同标签区域切割出来，属于像素级任务。                                              |
| OCR检测 | 在图片中检测出文本区域，并给出文本区域的位置信息。                                                                        |
| OCR识别 | 在图片中识别出文本内容。                                                                                                |
| 度量学习  | 训练可以将图片特征化的模型，使用该模型创建特征库，通过特征对比，在不重新训练模型的前提下对新的类别进行分类，也可称为自学习。   |
| 多标签分类 | 对图片进行多类别分类，一些图片可能不只是属于某个单一的类别，天空和大海可以同时存在，得到图片的多标签分类结果。               |
|异常检测| 用于检测某类产品中的异常类别，常用于工业质检等领域。|

#### 使用说明

##### 功能页介绍

AI Cube包含5个功能页，“项目”页面主要实现项目管理功能，展示当前项目和最近项目；“图像”页面展示当前项目的数据集信息，便于用户查看数据集的图片；“拆分”页面展示拆分信息，统计拆分类别和不同拆分集的图片；“训练”页面实现训练参数配置，训练信息和训练曲线的显示；“评估”页面实现模型评估和评估信息的展示，并且可以配置部署必要参数生成部署包。

🗂️ **项目页面**图示：

![项目页面](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/3baf7a9989c4.jpg)

🗂️ **图像页面**图示：

![图像页面](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/3eacf59a5b00.jpg)

🗂️ **拆分页面**图示：

![拆分页面](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/5511218dd06f.jpg)

🗂️ **训练页面**图示：

![训练页面](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/dd2455af26b8.jpg)

🗂️ **评估页面**图示：

![评估页面](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/00d6cc5f736e.jpg)

##### 创建数据集

按照不同任务的数据集格式组织数据集。对应数据集格式在`项目页面`点击新建项目查看，同时我们提供了不同任务的示例数据集，在`example_dataset`目录下；并使用这些示例数据集创建了示例项目，位于`example_projects`目录下。

关于不同任务的示例数据集和示例任务，对应关系如下：

| 数据集名称     | 示例任务   | 说明                   |
| -------------- | ---------- | ---------------------- |
| vegetable_cls  | 图像分类   | 蔬菜分类场景           |
| insect         | 目标检测   | 昆虫检测场景           |
| Ocular_lesions | 语义分割   | 眼球病变区域分割场景   |
| dataset_td100  | OCR检测    | OCR文字检测场景        |
| ProductionDate | OCR识别    | 生产日期识别场景       |
| drink          | 度量学习   | 饮料瓶分类场景         |
| multilabel2000 | 多标签分类 | 自然风光多标签分类场景 |
| bottle         | 异常检测   | 瓶口异常检测场景       |

您可以使用我们提供的示例数据集，也可以自己按照`新建项目界面`对应任务格式组织您的数据集。AICube遇到的大多数问题都是数据的问题，我们只对数据集的目录结构实现了检查，并没有对数据内部的标注信息做检查，请谨慎的处理数据。

##### 创建项目

进入`项目页面`--->点击`新建项目`按钮--->选择任务类型--->导入数据集--->选择项目的存储路径--->添加项目的名称--->创建项目。

新建项目界面如下图所示：

![新建项目](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/6f47221812b4.jpg)

项目新建完成后，会自动跳转到`图像页面`，您可以查看您的数据集详情。进入`拆分页面`，您可以按照自定义比例对数据集进行拆分，并查看拆分集的统计信息。

##### 启动训练

进入`训练页面`，在左侧配置**模型、数据增强和训练参数**。

常见参数解析：

| 平台参数名称     | 常用参数定义            | 参数含义解析                                                 |
| ---------------- | ----------------------- | ------------------------------------------------------------ |
| 模型             | model                   | 不同结构的网络模型，用于实现不同的任务；                     |
| Backbone         | model backbone          | 模型中的特征提取部分网络结构，比如检测和分割任务的模型；     |
| 是否预训练       | pretrain                | 是否加载AICube提供的预训练模型;                             |
| 预训练模型语言   | pretrain language       | **OCR识别**的特定任务参数，选择训练预训练模型的样本语言；其他任务忽略；        |
| 模型大小         | model size              | n、s、m、l、x，同一模型的变体，区别是模型尺寸，用于平衡准确率和速率； |
| 模型宽度         | model width             | 宽度越大，参数量越大;                                        |
| 图像尺寸         | model input size        | 模型输入分辨率，单值表示输入为[x,x]，双值表示输入为[x,y];    |
| ASPP空洞率       | ASPP dilation rate      | **语义分割**的特定任务参数，不同空洞卷积和池化操作的尺度，不同的空洞率进行空洞卷积可以扩大感受野，获得更广阔的的上下文信息； |
| 编码长度         | embedding length        | **度量学习**的特定任务参数，样本被向量化的向量长度；             |
| 自动数据增强     | TrivialAugment          | 无参数单图随机自动数据增强;                                  |
| 其他数据增强方法 | —                       | 亮度、对比度、饱和度、色度、锐度增强，翻转，旋转，随机缩放，随机裁剪，透视变换，高斯模糊，直方图均衡化，灰度世界算法，CutOut，Random Erasing，Mask; |
| 学习率           | learning rate           | 优化算法的参数，每次迭代的调整步长；                         |
| 迭代轮数         | epoch                   | 一个epoch是神经网络使用全部训练样本训练一次的过程；          |
| 训练批大小       | batchsize               | 每次前向和反向传播使用的样本数量；                           |
| 优化器           | optimizer               | 优化网络的时候使用的优化函数，比如SGD、Adam等；              |
| AutoAnchor       | autoanchor              | 目标检测任务中的锚框自适应；                                 |
| NMS选项          | nms option              | 目标检测任务中区别类内和类间的非极大值抑制选项；             |
| 置信度阈值       | confidience threshold   | 用于预测框类别的过滤，低于此阈值的预测框都将被删除；         |
| 交并比阈值       | IOU threshold           | 对多个重叠框进行极大值筛选，计算所有检测框的得分，依次与得分最高的检测框对比，大于此阈值的检测框被删除；OCR检测中的Box阈值类似； |
| 自动混合精度     | AMP                     | 针对不同层采用不同的数据精度，以节省显存并提高计算速度；     |
| 指数移动平均     | EMA                     | 平滑方法，防止异常值的影响，权重随时间指数递减；             |
| 早停             | Early Stopping          | 增加模型泛化性和防止过拟合的方法；                           |
| 预热策略         | WarmUp                  | 操作训练初始阶段的learning rate，使模型更快的收敛；          |
| 多尺度训练       | MST                     | 实现对不同尺度的输入图像进行训练，提高检测模型对不同大小物体的检测泛化性； |
| 损失函数         | loss function           | 用于评估模型预测值和真实值的差距程度，损失越小，模型性能越好； |
| 学习率调度       | learning rate scheduler | 学习率调整策略，训练过程中动态的调整学习率以适应梯度下降过程，包括StepLR、CosineAnnealingLR、LinearLR、MultiStepLR等； |
| 损失刷新步长     | loss refresh step       | 界面Loss曲线绘制频率，以batch为单位；                        |
| GPU索引          | gpu index               | 显卡索引；                                                 |

按照不同的任务配置好对应参数后，可以点击`增强样本按钮`查看经过数据增强的部分示例样本；点击`学习率曲线`可以查看不同的学习率策略导致的学习率变化；点击`开始训练按钮`，训练的信息会在右上方面板显示，损失曲线和指标曲线会在中间位置绘制；示例样本的预测结果会在右下面板迭代显示每个epoch的变化。训练时界面如下图：

![训练过程](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/dd2455af26b8.jpg)

##### 模型测试

进入`评估页面`，选择训练好的模型，然后选择测试方式。测试方式如下：

| 测试方式     | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| 测试集测试   | 对拆分得到的测试集进行测试评估，输出测试指标数据；           |
| 额外数据测试 | 使用和训练数据集相同格式的带标注数据进行测试，输出测试指标数据； |
| 图像目录测试 | 只选择使用训练的模型和参数对图片目录下的所有无标注样本进行推理，无测试指标； |

点击“开始测试”按钮，进行测试，测试结束后，根据评估指标查看您的模型性能；双击测试数据列表的条目可以查看推理结果大图。

##### 模型部署

如果模型的性能符合您的需求，您可以在芯片适配面板配置部署参数，主要是模型的输入分辨率和一些基础参数，点击`部署按钮`生成部署包。

![部署包生成](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/b9afb50048f9.jpg)

部署产物生成后您可以在当前项目的根目录下找到如下文件，我们主要使用`kmodel`和配置文件`deploy_config.json`：

```shell
📦 task_name
├── 📁 cpp_deployment_source
├── 📁 mp_deployment_source
└── README.md
```

![项目文件](https://www.kendryte.com/api/imagecdn/zh/sdk/canmv_k230_sdk/attachments/d454806222db.jpg)

其中`mp_deployment_source`目录是在K230 MicroPython方案上部署的资源，包含Kmodel文件和部署配置文件！

#### 部署步骤

##### 部署包说明

训练结束后可以得到对应训练任务的部署产物。

##### 文件拷贝

✅ **固件选择**：请在 `github` 按照您的开发板类型下载最新的 [PreRelease固件](https://github.com/kendryte/canmv_k230/releases/tag/PreRelease) 以保证**最新的特性**被支持！或者使用最新的代码自行编译固件，教程见：[固件编译](./userguide/how_to_build.md)。

✅ **固件烧录**： 按照开发板类型烧录固件，固件烧录参考：[固件烧录](./userguide/how_to_burn_firmware.md)。

✅ **部署脚本**：固件烧录成功后，上电开机，您可以在文件系统根目录下发现`CanMV/sdcard`目录，将`mp_deployment_source`拷贝到`CanMV/sdcard`目录下。

##### 脚本运行

AICube 训练产出的部署包与在线训练平台共用同一套部署脚本。打开CanMV IDE K230，选择左上角`文件(F)`->`打开文件`->`选择CanMV/sdcard/examples/19-CloudPlatScripts`中的不同任务的脚本运行。或者选择部署资源目录中的部署脚本运行。

除此之外，`CanMV/sdcard/examples/16-AI-Cube` 目录下提供了一组**直接调用 `aicube` 原生后处理模块**的独立示例，不依赖 `libs/PlatTasks.py` 封装，便于您参考如何自行对接 AICube 模型：

|脚本名称|脚本说明|
|--|--|
|ClassificationApp.py|图像分类任务示例。|
|DetectionApp.py|目标检测任务示例，支持 `AnchorBaseDet`/`AnchorFreeDet`/`GFLDet` 三种检测头，通过部署配置文件中的 `model_type` 自动选择对应的 `aicube` 后处理接口。|
|SegmentationApp.py|语义分割任务示例。|
|MultiLabelApp.py|多标签分类任务示例。|
|OCR_Det.py|OCR检测任务示例。|
|SelfLearningApp.py|自学习（度量学习）任务示例，通过特征库比对实现免重训的新类别识别。|
|DataCollectionCamera.py|数据采集脚本，按开发板上的 key 按键拍照，图像保存到 `/sdcard/examples/data/`。将其改名为 `main.py` 放到 `/sdcard` 下可开机自动运行。|

💡 **在线训练平台部署脚本介绍**：

|脚本名称|脚本说明|
|--|--|
|deploy_cls_image.py|图像分类单图推理脚本，您需要在自行增加测试图片，并修改脚本内读入图片的路径。|
|deploy_cls_video.py|图像分类视频流推理脚本，脚本详情见脚本内注释。|
|deploy_det_image.py|目标检测单图推理脚本，您需要在自行增加测试图片，并修改脚本内读入图片的路径。|
|deploy_det_video.py|目标检测视频流推理脚本，脚本详情见脚本内注释。|
|deploy_seg_image.py|语义分割单图推理脚本，您需要在自行增加测试图片，并修改脚本内读入图片的路径。|
|deploy_seg_video.py|语义分割视频流推理脚本，脚本详情见脚本内注释。|
|deploy_ocrdet_image.py|OCR检测单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。|
|deploy_ocrdet_video.py|OCR检测视频流推理脚本，脚本详情见脚本内注释。|
|deploy_ocrrec_image.py|OCR识别单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。考虑到平台OCR识别模型单次推理读入的数据为长条状文本，因此**不支持**视频流推理。|
|deploy_ocr_image.py|OCR单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。双模型任务，需要同时添加OCR检测和OCR识别的部署包，注意修改脚本内目录路径。|
|deploy_ocr_video.py|OCR视频流推理脚本，脚本详情见脚本内注释。双模型任务，需要同时添加OCR检测和OCR识别的部署包，注意修改脚本内目录路径。|
|deploy_ml_image.py|度量学习单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。输出为对应维度的特征，后续操作视应用场景修改。|
|deploy_ml_video.py|度量学习视频流推理脚本，脚本详情见脚本内注释。输出为对应维度的特征，后续操作视应用场景修改。|
|deploy_multl_image.py|多标签分类单图推理脚本，您需要在自行增加测试图片，并脚本修改读入图片的路径。|
|deploy_multl_video.py|多标签分类视频流推理脚本，脚本详情见脚本内注释。|

##### 部署说明

- 📢 在部署模型时如果效果不理想，首先调整对应任务的阈值和推理图像的分辨率，测试结果是否可以有好转！

- 📢 学会定位问题，比如查看AICube模型评估的结果，如果该图片正常，则可能是部署代码、模型转换或者阈值的问题，您可以选择调整量化方式或者调整部署参数进行优化！

- 📢 AICube存在大量的训练参数，对深度学习了解的用户可以根据可能的优化方向调整训练参数，调整模型训练的参数实现重新训练转换！

<a id="ai-resource-management"></a>

## AI资源管理与内存优化

K230 的 AI 推理涉及三类内存：MicroPython 的堆、nncase 运行时的内存池、以及 media 模块的物理内存。其中 **nncase 内存池只增不减**——加载过的 kmodel 即使释放了 kpu 实例，内存仍然留在池子里，必须显式归还。这是长时间运行的 AI 应用最容易踩的坑：单个模型跑得好好的，一旦做"模型切换"或"应用切换"，第二个模型就加载失败甚至直接 abort。

本章先对比例程中的两种主循环写法，再说明正确的资源释放方式。

<a id="ai-standard-template"></a>

<a id="main-loop-patterns"></a>

### 两种主循环写法

例程里存在两种主循环写法，新写代码时建议参照第二种。

**写法一：简洁式（多数例程采用）**

`05-AI-Demo` 的大部分例程、`20-YOLO-Module-Examples` 的全部例程、`21-AI-With-Others/ai_uart.py` 等都采用这种写法，本文档和 API 手册中的示例与这些例程保持一致：

```python
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode, display_size=display_size)
    pl.create()
    display_size = pl.get_display_size()        # create 之后再取实际显示分辨率
    app = MyApp(..., rgb888p_size=rgb888p_size, display_size=display_size)
    app.config_preprocess()
    while True:
        with ScopedTiming("total", 1):
            img = pl.get_frame()
            res = app.run(img)
            app.draw_result(pl, res)
            pl.show_image()
            gc.collect()
    app.deinit()
    pl.destroy()
```

```{admonition} 注意
:class: warning
这种写法的 `while True` 没有正常出口，**末尾的 `app.deinit()` 和 `pl.destroy()` 实际不会执行**。在 IDE 里点停止会以异常方式打断脚本，资源不会被释放，再次运行就可能因 nncase 内存不足而失败（此时重新上电即可恢复）。

例程这样写是为了突出算法逻辑、减少干扰。跑 demo 体验没有问题，但**编写自己的应用时请改用写法二**。
```

**写法二：带资源回收（新例程采用）**

`05-AI-Demo` 中较新的例程——`bytetrack.py`、`ocsort.py`、`deepsort.py`、`botsort.py`、`face_masking_count.py`、`nanotracker.py`、`keyword_spotting.py`、`multi_kws.py`、`tts_zh.py`——以及 `21-AI-With-Others` 的两个 UVC 例程，都采用了带资源回收的写法。以 `bytetrack.py` 为例：

```python
import os, gc

def main():
    # auto按开发板选择默认驱动；可手动改为hdmi/lcd/st7701/nt35516等模式
    display_mode="auto"
    # None使用SDK默认分辨率；更换屏幕规格时手动指定，如[640,480]
    display_size=None
    rgb888p_size=[1280,720]
    # ... 其它参数省略

    pl=None
    app=None
    img=None
    res=None
    os.exitpoint(os.EXITPOINT_ENABLE)           # 允许IDE的停止按钮打断主循环
    try:
        pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode,display_size=display_size)
        pl.create()
        display_size=pl.get_display_size()      # create 之后再取实际显示分辨率
        app=MyApp(...)
        app.config_preprocess()

        while True:
            os.exitpoint()                      # 响应停止请求
            with ScopedTiming("total",1):
                img=pl.get_frame()
                res=app.run(img)
                app.draw_result(pl,res)
                pl.show_image()
                gc.collect()
    except KeyboardInterrupt:
        print("stopped")
    except Exception as error:
        if "IDE interrupt" in str(error):       # IDE停止会抛异常，不算错误
            print("stopped")
        else:
            raise
    finally:
        os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
        img=None
        res=None
        # 释放顺序：先模型，后PipeLine；逐个用 try 包住，避免一个失败影响后面的
        try:
            if app is not None:
                app.deinit()
        except BaseException as error:
            print("cleanup app failed:", error)
        app=None
        try:
            if pl is not None:
                pl.destroy()
        except BaseException as error:
            print("cleanup pipeline failed:", error)
        pl=None
        gc.collect()
```

要点：

| 要点 | 说明 |
|------|------|
| `display_mode="auto"` + `display_size=None` | 由 `libs/DisplayConfig.py` 按 `os.uname()` 查表选屏，同一份脚本可在不同开发板运行。取值见 [PipeLine 手册](./api/aidemo/pipeline_module_api_manual.md#init) |
| `create()` 后取 `get_display_size()` | 屏驱动可能不支持请求的分辨率而使用自己的默认值，构造时传入的 `display_size` 会被实际值覆盖 |
| `os.exitpoint()` | 不加的话，IDE 点停止无法及时中断主循环 |
| `try ... finally` | 保证任何退出路径都释放资源。释放顺序是先模型（`deinit()`）后 PipeLine（`destroy()`） |
| 每项释放单独 `try` | 某个资源释放失败时，后面的资源仍能被释放 |

### 释放顺序

AI 应用的资源存在依赖关系，释放顺序不能颠倒：

```text
AI 模型实例 (deinit)  →  PipeLine (destroy)
      ↓
  kpu.release()                 解释器持有输入/输出 tensor 的引用，
      ↓                          必须先释放解释器再释放 tensor
  tensor / results 清空
      ↓
  ai2d.deinit()
      ↓
  gc.collect() + nn.shrink_memory_pool()
```

好消息是这套流程 [`AIBase.deinit()`](./api/aidemo/aibase_module_api_manual.md#deinit) 已经封装好了，**包括最后的 `gc.collect()` 和 `shrink_memory_pool()`**。继承 `AIBase` 的应用只要按[两种主循环写法](#main-loop-patterns)在 `finally` 里依次调用 `app.deinit()` 和 `pl.destroy()` 即可，不需要自己去碰 `kpu.release()` 这一层。

```{admonition} 注意
:class: warning
一定要用 `try ... finally` 包住主循环。在 IDE 中点击停止按钮会向脚本抛出异常，如果没有 `finally`，模型资源不会被释放，下次运行就可能因内存不足而失败。同时建议在开头调用 `os.exitpoint(os.EXITPOINT_ENABLE)`，并在循环内调用 `os.exitpoint()`，让 IDE 的停止请求能及时生效。
```

<a id="multi-model-switching"></a>

### 多模型切换

同一个脚本里先后加载多个 kmodel 时，**必须在加载下一个模型之前把上一个模型彻底释放**：

```python
# 错误：直接覆盖变量，旧模型的内存没有归还给 nncase 内存池
app = ModelA(...)
app = ModelB(...)          # 大概率在这里因内存不足失败

# 正确
app = ModelA(...)
...
app.deinit()               # 内部已含 gc.collect() + shrink_memory_pool()
app = None
app = ModelB(...)
```

开发板上的 `28-APP_CENTER/model_cleanup.py` 提供了两个可以直接复用的辅助函数：

| 函数 | 用途 |
|------|------|
| `deinit_model(model, pipelines=(), tensor_lists=())` | 在 `AIBase.deinit()` 之外，额外释放子类自行创建的 tensor 列表和 `Ai2d` 实例。适合多级预处理、多输入模型 |
| `deinit_with_retry(model)` | 释放失败时先 `gc.collect()` 再重试一次。`deinit()` 是幂等的，重试安全 |

### 共存的模型要算内存账

多个模型同时驻留时，占用的是各自权重加上各自输出张量的总和。以人体分割模型 `body_seg.kmodel` 为例：权重约 25 MB，输出张量为 `512*512*15*4 B ≈ 15.7 MB`，单独运行就接近内存上限，再并排加载第二个模型必然失败。

因此多模型应用有两条路：

- **串行**：用完一个释放一个，见上一节。适合"检测 → 识别"这类前后依赖的流程，但每次切换都有加载耗时。
- **并行**：确认总内存够用后同时驻留。适合帧率敏感、模型都比较小的场景（如 `21-AI-With-Others/ai_multi_thread.py`）。注意 **KPU 是互斥资源**，多线程推理时需要串行化访问 KPU。

### Ai2d 与 tensor 的所有权

- `Ai2d.run()` 返回的是实例**复用**的输出 tensor，下一次 `run()` 会覆盖其内容。不要自行 `release()`，也不要跨帧保存引用。
- 分割任务的 mask 缓冲区由调用方分配并复用（`aidemo.*_seg_postprocess` 的最后一个参数），不要每帧重新分配。
- `image.Image(..., alloc=image.ALLOC_REF, data=...)` 创建的 Image 只是引用，底层数据的生命周期由数据的所有者决定，底层数据失效后不要再使用该 Image。

### 排查内存问题

| 现象 | 可能原因 |
|------|----------|
| 第二次运行脚本就失败，重启后正常 | 上次退出时没有 `deinit()`，内存没归还。检查 `try/finally` |
| 加载第二个模型时报内存不足 | 切换模型前没有 `deinit()`，或模型太大无法共存 |
| 长时间运行后越来越卡最终崩溃 | 主循环里缺少 `gc.collect()`，或每帧都在新建对象（如每帧 `image.Image(...)`、每帧重新 `build()` ai2d） |
| `deinit()` 抛异常 | 某个原生资源释放失败。资源会被保留以便重试，可参考 `deinit_with_retry` 先 `gc.collect()` 再调一次 |

也可以用 `nncase_runtime.version()` 确认板上 runtime 版本与 PC 端转换 kmodel 所用的 nncase 编译器大版本一致，版本不匹配同样会导致 kmodel 加载失败。

## 进阶开发

这里针对不同的场景给出一些复杂示例，以AI+其他模块为基础，实现进阶开发。

### AI多线程推理

使用多线程实现多个AI模型同时推理，注意KPU互斥占用。这里以YOLOv8检测和人脸检测为例，给出如何使用多线程实现同时推理。示例代码如下：

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import nncase_runtime as nn
import ulab.numpy as np
import aidemo
from media.display import *
from media.media import *
from media.sensor import *
import time, os, sys, gc
import lvgl as lv
from machine import TOUCH
from machine import RTC
import _thread

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

sensor = None
rgb888p_size=[1280,720]
display_size = [800, 480]
face_det_stop=False
yolo_det_stop=False
face_osd_img=None
yolo_osd_img=None
lock = _thread.allocate_lock()

# 自定义YOLOv8检测类
class ObjectDetectionApp(AIBase):
    def __init__(self,kmodel_path,labels,model_input_size,max_boxes_num,confidence_threshold=0.5,nms_threshold=0.2,rgb888p_size=[224,224],display_size=[1920,1080],debug_mode=0):
        super().__init__(kmodel_path,model_input_size,rgb888p_size,debug_mode)
        self.kmodel_path=kmodel_path
        self.labels=labels
        self.model_input_size=model_input_size
        self.confidence_threshold=confidence_threshold
        self.nms_threshold=nms_threshold
        self.max_boxes_num=max_boxes_num
        self.rgb888p_size=[ALIGN_UP(rgb888p_size[0],16),rgb888p_size[1]]
        self.display_size=[ALIGN_UP(display_size[0],16),display_size[1]]
        self.debug_mode=debug_mode
        self.color_four=get_colors(len(self.labels))
        self.x_factor = float(self.rgb888p_size[0])/self.model_input_size[0]
        self.y_factor = float(self.rgb888p_size[1])/self.model_input_size[1]
        self.ai2d=Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT,nn.ai2d_format.NCHW_FMT,np.uint8, np.uint8)

    # 配置预处理操作，这里使用了resize，Ai2d支持crop/shift/pad/resize/affine，具体代码请打开/sdcard/libs/AI2D.py查看
    def config_preprocess(self,input_image_size=None):
        with ScopedTiming("set preprocess config",self.debug_mode > 0):
            ai2d_input_size=input_image_size if input_image_size else self.rgb888p_size
            top,bottom,left,right,self.scale=letterbox_pad_param(self.rgb888p_size,self.model_input_size)
            self.ai2d.pad([0,0,0,0,top,bottom,left,right], 0, [128,128,128])
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])

    def postprocess(self,results):
        with ScopedTiming("postprocess",self.debug_mode > 0):
            new_result=results[0][0].transpose()
            det_res = aidemo.yolov8_det_postprocess(new_result.copy(),[self.rgb888p_size[1],self.rgb888p_size[0]],[self.model_input_size[1],self.model_input_size[0]],[self.display_size[1],self.display_size[0]],len(self.labels),self.confidence_threshold,self.nms_threshold,self.max_boxes_num)
            return det_res

    def draw_result(self,osd_img,dets):
        with ScopedTiming("display_draw",self.debug_mode >0):
            osd_img.clear()
            if dets:
                for i in range(len(dets[0])):
                    x, y, w, h = map(lambda x: int(round(x, 0)), dets[0][i])
                    osd_img.draw_rectangle(x,y, w, h, color=self.color_four[dets[1][i]],thickness=4)
                    osd_img.draw_string_advanced(x, y-50,32," " + self.labels[dets[1][i]] + " " + str(round(dets[2][i],2)) , color=self.color_four[dets[1][i]])


# 自定义人脸检测类，继承自AIBase基类
class FaceDetectionApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, anchors, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)  # 调用基类的构造函数
        self.kmodel_path = kmodel_path  # 模型文件路径
        self.model_input_size = model_input_size  # 模型输入分辨率
        self.confidence_threshold = confidence_threshold  # 置信度阈值
        self.nms_threshold = nms_threshold  # NMS（非极大值抑制）阈值
        self.anchors = anchors  # 锚点数据，用于目标检测
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]  # sensor给到AI的图像分辨率，并对宽度进行16的对齐
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]  # 显示分辨率，并对宽度进行16的对齐
        self.debug_mode = debug_mode  # 是否开启调试模式
        self.ai2d = Ai2d(debug_mode)  # 实例化Ai2d，用于实现模型预处理
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)  # 设置Ai2d的输入输出格式和类型

    # 配置预处理操作，这里使用了pad和resize，Ai2d支持crop/shift/pad/resize/affine，具体代码请打开/sdcard/libs/AI2D.py查看
    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("set preprocess config", self.debug_mode > 0):  # 计时器，如果debug_mode大于0则开启
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size  # 初始化ai2d预处理配置，默认为sensor给到AI的尺寸，可以通过设置input_image_size自行修改输入尺寸
            top, bottom, left, right,_ = letterbox_pad_param(self.rgb888p_size,self.model_input_size)
            self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])  # 填充边缘
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)  # 缩放图像
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])  # 构建预处理流程

    # 自定义当前任务的后处理，results是模型输出array列表，这里使用了aidemo库的face_det_post_process接口
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
            post_ret = aidemo.face_det_post_process(self.confidence_threshold, self.nms_threshold, self.model_input_size[1], self.anchors, self.rgb888p_size, results)
            if len(post_ret) == 0:
                return post_ret
            else:
                return post_ret[0]

    # 绘制检测结果到画面上
    def draw_result(self, osd_img, dets):
        with ScopedTiming("display_draw", self.debug_mode > 0):
            osd_img.clear()
            if dets:
                for det in dets:
                    # 将检测框的坐标转换为显示分辨率下的坐标
                    x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                    x = x * self.display_size[0] // self.rgb888p_size[0]
                    y = y * self.display_size[1] // self.rgb888p_size[1]
                    w = w * self.display_size[0] // self.rgb888p_size[0]
                    h = h * self.display_size[1] // self.rgb888p_size[1]
                    osd_img.draw_rectangle(x, y, w, h, color=(255, 255, 0, 255), thickness=2)


def face_det_thread():
    global sensor,osd_img,rgb888p_size,display_size,face_osd_img
    # 设置模型路径和其他参数
    kmodel_path = "/sdcard/examples/kmodel/face_detection_320.kmodel"
    # 其它参数
    confidence_threshold = 0.5
    nms_threshold = 0.2
    anchor_len = 4200
    det_dim = 4
    anchors_path = "/sdcard/examples/utils/prior_data_320.bin"
    anchors = np.fromfile(anchors_path, dtype=np.float)
    anchors = anchors.reshape((anchor_len, det_dim))
    face_det = FaceDetectionApp(kmodel_path, model_input_size=[320, 320], anchors=anchors, confidence_threshold=confidence_threshold, nms_threshold=nms_threshold, rgb888p_size=rgb888p_size, display_size=display_size, debug_mode=0)
    face_det.config_preprocess()  # 配置预处理
    while True:
        if face_det_stop:
            break
        img_2 = sensor.snapshot(chn = CAM_CHN_ID_2)
        img_np =img_2.to_numpy_ref()
        with lock:
            res = face_det.run(img_np)         # 推理当前帧
        face_det.draw_result(face_osd_img, res)   # 绘制结果
        Display.show_image(face_osd_img, 0, 0, Display.LAYER_OSD2)
        gc.collect()
    face_det.deinit()


def yolov8_det_thread():
    global sensor,osd_img,rgb888p_size,display_size,yolo_osd_img
    kmodel_path="/sdcard/examples/kmodel/yolov8n_224.kmodel"
    labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
    confidence_threshold = 0.3
    nms_threshold = 0.4
    ob_det=ObjectDetectionApp(kmodel_path,labels=labels,model_input_size=[224,224],max_boxes_num=50,confidence_threshold=confidence_threshold,nms_threshold=nms_threshold,rgb888p_size=rgb888p_size,display_size=display_size,debug_mode=0)
    ob_det.config_preprocess()
    while True:
        if yolo_det_stop:
            break
        img_2 = sensor.snapshot(chn = CAM_CHN_ID_2)
        img_np =img_2.to_numpy_ref()
        with lock:
            det_res = ob_det.run(img_np)
        ob_det.draw_result(yolo_osd_img, det_res)
        Display.show_image(yolo_osd_img, 0, 0, Display.LAYER_OSD1)
        gc.collect()
    ob_det.deinit()


def media_init():
    global sensor,osd_img,rgb888p_size,display_size,face_osd_img,yolo_osd_img
    Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True, osd_num=3)
    sensor = Sensor(fps=30)
    sensor.reset()
    sensor.set_framesize(w = 800, h = 480,chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.YUV420SP)
    sensor.set_framesize(w = rgb888p_size[0], h = rgb888p_size[1], chn=CAM_CHN_ID_2)
    sensor.set_pixformat(Sensor.RGBP888, chn=CAM_CHN_ID_2)

    sensor_bind_info = sensor.bind_info(x = 0, y = 0, chn = CAM_CHN_ID_0)
    Display.bind_layer(**sensor_bind_info, layer = Display.LAYER_VIDEO1)
    face_osd_img = image.Image(display_size[0], display_size[1], image.ARGB8888)
    yolo_osd_img = image.Image(display_size[0], display_size[1], image.ARGB8888)
    MediaManager.init()
    sensor.run()

def media_deinit():
    global sensor
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    sensor.stop()
    Display.deinit()
    time.sleep_ms(50)
    MediaManager.deinit()

if __name__ == "__main__":
    media_init()
    _thread.start_new_thread(yolov8_det_thread,())
    _thread.start_new_thread(face_det_thread,())
    try:
        while True:
            time.sleep_ms(50)
    except BaseException as e:
        import sys
        sys.print_exception(e)
        yolo_det_stop=True
        face_det_stop=True
    media_deinit()
    gc.collect()
```

### AI+UART通信

AI推理结束后，如何将识别到的内容通过串口发送到上位机，这里以YOLOv8检测作为AI部分为例，给出如何使用UART通信实现AI+UART通信。示例代码如下：

```{warning}
本例需要连接物理 UART 引脚。接线前必须确认开发板使用 1.8 V 还是 3.3 V I/O 电平，禁止使用 5 V 信号及文档图片所示的劣质 CH340G 模块。完整要求见 [串口电平与转接模块安全](./example/peripheral/uart.md)。
```

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import os, sys, ujson, gc, math
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import aidemo
from machine import UART
from machine import FPIOA
import time

# Custom YOLOv8 object detection class
class ObjectDetectionApp(AIBase):
    def __init__(self, kmodel_path, labels, model_input_size, max_boxes_num, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        """
        Initialize object detection system.

        Parameters:
        - kmodel_path: Path to YOLOv8 KModel.
        - labels: List of class labels.
        - model_input_size: Model input resolution.
        - max_boxes_num: Max detection results to keep.
        - confidence_threshold: Detection score threshold.
        - nms_threshold: Non-max suppression threshold.
        - rgb888p_size: Camera input size (aligned to 16-width).
        - display_size: Output display size.
        - debug_mode: Enable debug timing logs.
        """
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        self.kmodel_path = kmodel_path
        self.labels = labels
        self.model_input_size = model_input_size
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.max_boxes_num = max_boxes_num

        # Align width to multiple of 16 for hardware compatibility
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode

        # Predefined colors for each class
        self.color_four = get_colors(len(self.labels))

        # Input scaling factors
        self.x_factor = float(self.rgb888p_size[0]) / self.model_input_size[0]
        self.y_factor = float(self.rgb888p_size[1]) / self.model_input_size[1]

        # Ai2d instance for preprocessing
        self.ai2d = Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)

        # Configure UART pins using FPIOA
        self.fpioa = FPIOA()
        self.fpioa.set_function(3, self.fpioa.UART1_TXD, ie=1, oe=1)
        self.fpioa.set_function(4, self.fpioa.UART1_RXD, ie=1, oe=1)

        # Initialize UART1
        self.uart = UART(UART.UART1, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

    def config_preprocess(self, input_image_size=None):
        """
        Configure pre-processing: padding and resizing using Ai2d.
        """
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            top, bottom, left, right, self.scale = letterbox_pad_param(self.rgb888p_size, self.model_input_size)
            self.ai2d.pad([0,0,0,0,top,bottom,left,right], 0, [128,128,128])
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build(
                [1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                [1, 3, self.model_input_size[1], self.model_input_size[0]]
            )

    def preprocess(self, input_np):
        """
        Prepare numpy image for inference.
        """
        with ScopedTiming("preprocess", self.debug_mode > 0):
            return [nn.from_numpy(input_np)]

    def postprocess(self, results):
        """
        Apply YOLOv8 post-processing including NMS and thresholding.
        """
        with ScopedTiming("postprocess", self.debug_mode > 0):
            new_result = results[0][0].transpose()
            det_res = aidemo.yolov8_det_postprocess(
                new_result.copy(),
                [self.rgb888p_size[1], self.rgb888p_size[0]],
                [self.model_input_size[1], self.model_input_size[0]],
                [self.display_size[1], self.display_size[0]],
                len(self.labels),
                self.confidence_threshold,
                self.nms_threshold,
                self.max_boxes_num
            )
            return det_res

    def draw_result(self, pl, dets):
        """
        Draw detection results and send label info via UART.
        """
        with ScopedTiming("display_draw", self.debug_mode > 0):
            if dets:
                pl.osd_img.clear()
                for i in range(len(dets[0])):
                    x, y, w, h = map(lambda x: int(round(x, 0)), dets[0][i])
                    pl.osd_img.draw_rectangle(x, y, w, h, color=self.color_four[dets[1][i]], thickness=4)
                    pl.osd_img.draw_string_advanced(
                        x, y - 50, 32,
                        " " + self.labels[dets[1][i]] + " " + str(round(dets[2][i], 2)),
                        color=self.color_four[dets[1][i]]
                    )
                    # Send detected label over UART
                    uart_write_res = self.labels[dets[1][i]] + " "
                    self.uart.write(uart_write_res.encode("utf-8"))
            else:
                pl.osd_img.clear()

if __name__ == "__main__":
    # Display mode: "auto" 按开发板型号自动选择屏驱动；也可显式指定 hdmi/lcd/st7701 等
    display_mode = "auto"
    # None 表示使用屏驱动的默认分辨率
    display_size = None
    rgb888p_size = [224, 224]
    kmodel_path = "/sdcard/examples/kmodel/yolov8n_224.kmodel"

    # Class labels for COCO dataset
    labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
              "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
              "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
              "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
              "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
              "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote",
              "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
              "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

    confidence_threshold = 0.3
    nms_threshold = 0.4
    max_boxes_num = 30

    # Initialize the PipeLine. rgb888p_size is the AI input resolution and display_size is the display resolution
    pl = PipeLine(rgb888p_size=rgb888p_size, display_mode=display_mode, display_size=display_size)
    # Create the PipeLine. Pass sensor_id to select a camera when needed, for example pl.create(sensor_id=2)
    pl.create()
    display_size = pl.get_display_size()

    # Initialize detection app
    ob_det = ObjectDetectionApp(
        kmodel_path,
        labels=labels,
        model_input_size=[224, 224],
        max_boxes_num=max_boxes_num,
        confidence_threshold=confidence_threshold,
        nms_threshold=nms_threshold,
        rgb888p_size=rgb888p_size,
        display_size=display_size,
        debug_mode=0
    )
    ob_det.config_preprocess()

    # Real-time processing loop
    while True:
        with ScopedTiming("total", 1):
            img = pl.get_frame()                         # Capture frame
            res = ob_det.run(img)                        # Run inference
            ob_det.draw_result(pl, res)                  # Draw results
            pl.show_image()                              # Display results
            gc.collect()                                 # Free memory

    ob_det.deinit()
    pl.destroy()
```

### AI多摄推理

多摄像头AI推理是指同时使用多个摄像头进行AI推理，这里以使用两个摄像头进行YOLOv8检测和人脸检测为例，给出如何使用双摄多线程实现AI推理。示例代码如下：

```python
import os,sys
from media.sensor import *
from media.display import *
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import time,image,random,gc
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import aidemo
import _thread

# 一些初始化设置
DISPLAY_WIDTH=ALIGN_UP(1920, 16)
DISPLAY_HEIGHT=1080
display_size=[DISPLAY_WIDTH//2,DISPLAY_HEIGHT//2]
sensor1 = None
sensor2 = None
yolo_rgb888p_size=[224,224]
face_rgb888p_size=[640,360]
face_det_run=True
yolo_det_run=True
face_osd_img=None
yolo_osd_img=None
lock = _thread.allocate_lock()

# 自定义YOLOv8检测类
class ObjectDetectionApp(AIBase):
    def __init__(self,kmodel_path,labels,model_input_size,max_boxes_num,confidence_threshold=0.5,nms_threshold=0.2,rgb888p_size=[224,224],display_size=[1920,1080],debug_mode=0):
        super().__init__(kmodel_path,model_input_size,rgb888p_size,debug_mode)
        self.kmodel_path=kmodel_path
        self.labels=labels
        # 模型输入分辨率
        self.model_input_size=model_input_size
        # 阈值设置
        self.confidence_threshold=confidence_threshold
        self.nms_threshold=nms_threshold
        self.max_boxes_num=max_boxes_num
        # sensor给到AI的图像分辨率
        self.rgb888p_size=[ALIGN_UP(rgb888p_size[0],16),rgb888p_size[1]]
        # 显示分辨率
        self.display_size=[ALIGN_UP(display_size[0],16),display_size[1]]
        self.debug_mode=debug_mode
        # 检测框预置颜色值
        self.color_four=get_colors(len(self.labels))
        # 宽高缩放比例
        self.x_factor = float(self.rgb888p_size[0])/self.model_input_size[0]
        self.y_factor = float(self.rgb888p_size[1])/self.model_input_size[1]
        # Ai2d实例，用于实现模型预处理
        self.ai2d=Ai2d(debug_mode)
        # 设置Ai2d的输入输出格式和类型
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT,nn.ai2d_format.NCHW_FMT,np.uint8, np.uint8)

    # 配置预处理操作，这里使用了resize，Ai2d支持crop/shift/pad/resize/affine，具体代码请打开/sdcard/libs/AI2D.py查看
    def config_preprocess(self,input_image_size=None):
        with ScopedTiming("set preprocess config",self.debug_mode > 0):
            # 初始化ai2d预处理配置，默认为sensor给到AI的尺寸，您可以通过设置input_image_size自行修改输入尺寸
            ai2d_input_size=input_image_size if input_image_size else self.rgb888p_size
            top,bottom,left,right,self.scale=letterbox_pad_param(self.rgb888p_size,self.model_input_size)
            # 配置padding预处理
            self.ai2d.pad([0,0,0,0,top,bottom,left,right], 0, [128,128,128])
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])

    def preprocess(self,input_np):
        with ScopedTiming("preprocess",self.debug_mode > 0):
            return [nn.from_numpy(input_np)]

    # 自定义当前任务的后处理
    def postprocess(self,results):
        with ScopedTiming("postprocess",self.debug_mode > 0):
            new_result=results[0][0].transpose()
            det_res = aidemo.yolov8_det_postprocess(new_result.copy(),[self.rgb888p_size[1],self.rgb888p_size[0]],[self.model_input_size[1],self.model_input_size[0]],[self.display_size[1],self.display_size[0]],len(self.labels),self.confidence_threshold,self.nms_threshold,self.max_boxes_num)
            return det_res
    # 资源释放
    def deinit(self):
         del self.kpu
         del self.ai2d
         self.tensors.clear()
         del self.tensors
         gc.collect()
         time.sleep_ms(50)


 # 自定义人脸检测类，继承自AIBase基类
class FaceDetectionApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, anchors, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
         super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)  # 调用基类的构造函数
         self.kmodel_path = kmodel_path  # 模型文件路径
         self.model_input_size = model_input_size  # 模型输入分辨率
         self.confidence_threshold = confidence_threshold  # 置信度阈值
         self.nms_threshold = nms_threshold  # NMS（非极大值抑制）阈值
         self.anchors = anchors  # 锚点数据，用于目标检测
         self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]  # sensor给到AI的图像分辨率，并对宽度进行16的对齐
         self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]  # 显示分辨率，并对宽度进行16的对齐
         self.debug_mode = debug_mode  # 是否开启调试模式
         self.ai2d = Ai2d(debug_mode)  # 实例化Ai2d，用于实现模型预处理
         self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)  # 设置Ai2d的输入输出格式和类型

    # 配置预处理操作，这里使用了pad和resize，Ai2d支持crop/shift/pad/resize/affine，具体代码请打开/sdcard/libs/AI2D.py查看
    def config_preprocess(self, input_image_size=None):
         with ScopedTiming("set preprocess config", self.debug_mode > 0):  # 计时器，如果debug_mode大于0则开启
             ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size  # 初始化ai2d预处理配置，默认为sensor给到AI的尺寸，可以通过设置input_image_size自行修改输入尺寸
             top, bottom, left, right,_ = letterbox_pad_param(self.rgb888p_size,self.model_input_size)
             self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])  # 填充边缘
             self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)  # 缩放图像
             self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])  # 构建预处理流程

    # 自定义当前任务的后处理，results是模型输出array列表，这里使用了aidemo库的face_det_post_process接口
    def postprocess(self, results):
         with ScopedTiming("postprocess", self.debug_mode > 0):
             post_ret = aidemo.face_det_post_process(self.confidence_threshold, self.nms_threshold, self.model_input_size[1], self.anchors, self.rgb888p_size, results)
             if len(post_ret) == 0:
                 return post_ret
             else:
                 return post_ret[0]

    # 资源释放
    def deinit(self):
         del self.kpu
         del self.ai2d
         self.tensors.clear()
         del self.tensors
         gc.collect()
         time.sleep_ms(50)

#人脸检测线程
def face_det_thread():
     global display_size,sensor1,osd_img,face_rgb888p_size,face_osd_img
     # 设置模型路径和其他参数
     kmodel_path = "/sdcard/examples/kmodel/face_detection_320.kmodel"
     # 其它参数
     confidence_threshold = 0.5
     nms_threshold = 0.2
     anchor_len = 4200
     det_dim = 4
     anchors_path = "/sdcard/examples/utils/prior_data_320.bin"
     anchors = np.fromfile(anchors_path, dtype=np.float)
     anchors = anchors.reshape((anchor_len, det_dim))
     face_det = FaceDetectionApp(kmodel_path, model_input_size=[320, 320], anchors=anchors, confidence_threshold=confidence_threshold, nms_threshold=nms_threshold, rgb888p_size=face_rgb888p_size, display_size=display_size, debug_mode=0)
     face_det.config_preprocess()  # 配置预处理
     while face_det_run:
         img = sensor1.snapshot(chn = CAM_CHN_ID_1)
         img_np =img.to_numpy_ref()
         with lock:
             res = face_det.run(img_np)         # 推理当前帧
         face_osd_img.clear()
         if res:
             for det in res:
                 # 将检测框的坐标转换为显示分辨率下的坐标
                 x, y, w, h = map(lambda x: int(round(x, 0)), det[:4])
                 x = x * display_size[0] // face_rgb888p_size[0]
                 y = y * display_size[1] // face_rgb888p_size[1]
                 w = w * display_size[0] // face_rgb888p_size[0]
                 h = h * display_size[1] // face_rgb888p_size[1]
                 face_osd_img.draw_rectangle(x, y, w, h, color=(255, 255, 0, 255), thickness=2)
         Display.show_image(face_osd_img, 0, 0, Display.LAYER_OSD1)
         del img
         del img_np
         gc.collect()
     del face_osd_img
     face_det.deinit()

# YOLOv8检测线程
def yolov8_det_thread():
     global display_size,sensor2,osd_img,yolo_rgb888p_size,yolo_osd_img
     kmodel_path="/sdcard/examples/kmodel/yolov8n_224.kmodel"
     labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
     confidence_threshold = 0.3
     nms_threshold = 0.4
     color_four=get_colors(len(labels))
     ob_det=ObjectDetectionApp(kmodel_path,labels=labels,model_input_size=[224,224],max_boxes_num=50,confidence_threshold=confidence_threshold,nms_threshold=nms_threshold,rgb888p_size=yolo_rgb888p_size,display_size=display_size,debug_mode=0)
     ob_det.config_preprocess()
     while yolo_det_run:
         img = sensor2.snapshot(chn = CAM_CHN_ID_1)
         img_np =img.to_numpy_ref()
         with lock:
             res = ob_det.run(img_np)

         yolo_osd_img.clear()
         for i in range(len(res[0])):
             x, y, w, h = map(lambda x: int(round(x, 0)), res[0][i])
             x=x+display_size[0]
             y=y+display_size[1]
             yolo_osd_img.draw_rectangle(x,y, w, h, color=color_four[res[1][i]],thickness=4)
             yolo_osd_img.draw_string_advanced( x , y-50,32," " + labels[res[1][i]] + " " + str(round(res[2][i],2)) , color=color_four[res[1][i]])

         Display.show_image(yolo_osd_img, 0, 0, Display.LAYER_OSD2)
         del img
         del img_np
         gc.collect()
     del yolo_osd_img
     ob_det.deinit()

def media_init():
    global display_size,sensor1,sensor2,yolo_rgb888p_size,face_rgb888p_size,face_osd_img,yolo_osd_img
    #-----------------------------Sensor1初始化部分-------------------------------
    sensor1 = Sensor(id=1)
    sensor1.reset()
    # 设置水平镜像和垂直翻转，不同板子的方向不同，通过配置这两个参数使画面转正
    #sensor1.set_hmirror(False)
    #sensor1.set_vflip(False)
    # 配置sensor1的多通道出图，每个通道的出图格式和分辨率可以不同，最多可以出三路图，参考sensor API文档
    # 通道0直接给到显示VO，格式为YUV420
    sensor1.set_framesize(width = display_size[0], height = display_size[1],chn=CAM_CHN_ID_0)
    sensor1.set_pixformat(Sensor.YUV420SP,chn=CAM_CHN_ID_0)
    # 通道1给到AI做算法处理，格式为RGB888P
    sensor1.set_framesize(width = face_rgb888p_size[0] , height = face_rgb888p_size[1], chn=CAM_CHN_ID_1)
    # set chn1 output format
    sensor1.set_pixformat(Sensor.RGBP888, chn=CAM_CHN_ID_1)

    # 绑定通道0的摄像头图像到屏幕，防止另一个通道的AI推理过程太慢影响显示过程，导致出现卡顿效果
    sensor_bind_info1 = sensor1.bind_info(x = 0, y = 0, chn = CAM_CHN_ID_0)
    Display.bind_layer(**sensor_bind_info1, layer = Display.LAYER_VIDEO1)

    #-----------------------------Sensor2初始化部分-------------------------------
    sensor2 = Sensor(id=2)
    sensor2.reset()
    # 设置水平镜像和垂直翻转，不同板子的方向不同，通过配置这两个参数使画面转正
    #sensor2.set_hmirror(False)
    #sensor2.set_vflip(False)

    # 配置sensor2的多通道出图，每个通道的出图格式和分辨率可以不同，最多可以出三路图，参考sensor API文档
    # 通道0直接给到显示VO，格式为YUV420
    sensor2.set_framesize(width = display_size[0], height = display_size[1],chn=CAM_CHN_ID_0)
    sensor2.set_pixformat(Sensor.YUV420SP,chn=CAM_CHN_ID_0)
    # 通道1给到AI做算法处理，格式为RGB888P
    sensor2.set_framesize(width = yolo_rgb888p_size[0] , height = yolo_rgb888p_size[1], chn=CAM_CHN_ID_1)
    # set chn1 output format
    sensor2.set_pixformat(Sensor.RGBP888, chn=CAM_CHN_ID_1)

    # 绑定通道0的摄像头图像到屏幕，防止另一个通道的AI推理过程太慢影响显示过程，导致出现卡顿效果
    sensor_bind_info2 = sensor2.bind_info(x = display_size[0], y = display_size[1], chn = CAM_CHN_ID_0)
    Display.bind_layer(**sensor_bind_info2, layer = Display.LAYER_VIDEO2)


    # OSD图像初始化,创建一帧和屏幕分辨率同样大的透明图像，用于绘制AI推理结果
    face_osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    yolo_osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    # 设置为LT9611显示
    Display.init(Display.LT9611,osd_num=2, to_ide=True)

    # media初始化
    MediaManager.init()
    sensor1.run()

def media_deinit():
    global sensor1,sensor2,face_osd_img,yolo_osd_img
    sensor1.stop()
    sensor2.stop()
    Display.deinit()
    time.sleep_ms(50)
    MediaManager.deinit()
    nn.shrink_memory_pool()


if __name__=="__main__":
    media_init()
    _thread.start_new_thread(yolov8_det_thread,())
    _thread.start_new_thread(face_det_thread,())

    try:
        while True:
            time.sleep_ms(50)
    except BaseException as e:
        import sys
        sys.print_exception(e)
        yolo_det_run=False
        face_det_run=False
    time.sleep_ms(500)
    media_deinit()
    gc.collect()

```

### AI+UVC硬解码推理

使用UVC摄像头获取图像，并使用硬件CSC将图像转换成RGB888格式，创建tensor，将tensor输入到AI模型中，获取AI模型的输出结果，最后将输出结果绘制到屏幕上。这里AI推理场景为YOLOv8检测。完整代码对应开发板上的 **此电脑->CanMV->sdcard->examples->21-AI-With-Others->ai_uvc_hard_decode.py**，示例代码如下：

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import os,sys,ujson,gc,math, urandom
from media.display import *
from libs.DisplayConfig import init_display, DisplayImage
from media.media import *
from media.uvc import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import aidemo
from nonai2d import CSC

# Custom YOLOv8 object detection class
class ObjectDetectionApp(AIBase):
    def __init__(self, kmodel_path, labels, model_input_size, max_boxes_num, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        """
        Initialize object detection system.

        Parameters:
        - kmodel_path: Path to YOLOv8 KModel.
        - labels: List of class labels.
        - model_input_size: Model input size.
        - max_boxes_num: Max detection results to keep.
        - confidence_threshold: Detection score threshold.
        - nms_threshold: Non-max suppression threshold.
        - rgb888p_size: Camera input size (aligned to 16-width).
        - display_size: Output display size.
        - debug_mode: Enable debug timing logs.
        """
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        self.kmodel_path = kmodel_path
        self.labels = labels
        self.model_input_size = model_input_size
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.max_boxes_num = max_boxes_num

        # Align width to multiple of 16 for hardware compatibility
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode

        # Predefined colors for each class
        self.color_four = get_colors(len(self.labels))

        # Input scaling factors
        self.x_factor = float(self.rgb888p_size[0]) / self.model_input_size[0]
        self.y_factor = float(self.rgb888p_size[1]) / self.model_input_size[1]

        # Ai2d instance for preprocessing
        self.ai2d = Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.RGB_packed, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)

    def config_preprocess(self, input_image_size=None):
        """
        Configure pre-processing: padding and resizing using Ai2d.
        """
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            top, bottom, left, right, self.scale = letterbox_pad_param(self.rgb888p_size, self.model_input_size)
            self.ai2d.pad([0,0,0,0,top,bottom,left,right], 0, [128,128,128])
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build(
                [1, ai2d_input_size[1], ai2d_input_size[0], 3],
                [1, 3, self.model_input_size[1], self.model_input_size[0]]
            )

    def postprocess(self, results):
        """
        Apply YOLOv8 post-processing including NMS and thresholding.
        """
        with ScopedTiming("postprocess", self.debug_mode > 0):
            new_result = results[0][0].transpose()
            det_res = aidemo.yolov8_det_postprocess(
                new_result.copy(),
                [self.rgb888p_size[1], self.rgb888p_size[0]],
                [self.model_input_size[1], self.model_input_size[0]],
                [self.display_size[1], self.display_size[0]],
                len(self.labels),
                self.confidence_threshold,
                self.nms_threshold,
                self.max_boxes_num
            )
            return det_res

    def draw_result(self, img, dets):
        """
        Draw detection results and send label info via UART.
        """
        with ScopedTiming("display_draw",self.debug_mode >0):
            if dets:
                for i in range(len(dets[0])):
                    x, y, w, h = map(lambda x: int(round(x, 0)), dets[0][i])
                    img.draw_rectangle(x,y, w, h, color=self.color_four[dets[1][i]],thickness=4)
                    img.draw_string_advanced( x , y-50,32," " + self.labels[dets[1][i]] + " " + str(round(dets[2][i],2)) , color=self.color_four[dets[1][i]])


if __name__ == "__main__":

    display_mode = "auto"
    requested_display_size = None  # Optional [width, height] override.

    # Create CSC instance for pixel format conversion (e.g., to RGB888)
    csc = CSC(CSC.PIXEL_FORMAT_RGB_888)

    display_size = init_display(display_mode, requested_display_size, to_ide=True)
    # Reuse AI2D configuration; inference and annotations stay in source coordinates.
    display_resize = None

    # Initialize media manager to manage frame buffers and UVC stream


    # Wait for USB camera to be detected
    while True:
        plugin, dev = UVC.probe()
        if plugin:
            print(f"detect USB Camera {dev}")
            break
        time.sleep_ms(100)

    # Select and configure UVC video mode: 640x480 @ 30 FPS, MJPEG format
    mode = UVC.video_mode(640, 480, UVC.FOURCC_MJPEG, 30)
    succ, mode = UVC.select_video_mode(mode)
    print(f"select mode success: {succ}, mode: {mode}")

    # Define input image from USB camera (sensor side)
    rgb888p_size = [640, 480]

    # Path to the YOLOv8n kmodel
    kmodel_path = "/sdcard/examples/kmodel/yolov8n_224.kmodel"

    # COCO class labels used for detection
    labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
              "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
              "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
              "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
              "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
              "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote",
              "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
              "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

    # Detection parameters
    confidence_threshold = 0.3  # Minimum confidence to accept a detection
    nms_threshold = 0.4         # Non-Maximum Suppression threshold
    max_boxes_num = 30          # Max boxes per frame after filtering

    # Initialize object detection application with YOLOv8 model
    ob_det = ObjectDetectionApp(
        kmodel_path,
        labels=labels,
        model_input_size=[224, 224],
        max_boxes_num=max_boxes_num,
        confidence_threshold=confidence_threshold,
        nms_threshold=nms_threshold,
        rgb888p_size=rgb888p_size,
        display_size=rgb888p_size,
        debug_mode=0
    )

    # Configure Ai2d preprocessing (resize + letterbox pad)
    ob_det.config_preprocess()

    # Start UVC video stream with pixel format conversion enabled
    UVC.start(cvt=True)

    clock = time.clock()

    try:
        # Main loop: acquire frame, run inference, draw and display
        while True:
            clock.tick()
            img = UVC.snapshot()
            if img is not None:
                # Convert format (e.g., to RGB888)
                img = csc.convert(img)
                # Convert to Ulab.Numpy.ndarray
                img_np_hwc = img.to_numpy_ref()

                img_np_nhwc=img_np_hwc.reshape((1,img_np_hwc.shape[0],img_np_hwc.shape[1],3))

                # Run YOLOv8 inference on the current frame
                res = ob_det.run(img_np_nhwc)

                # Draw detection results on the frame
                ob_det.draw_result(img, res)

                # Show result on display
                if [img.width(), img.height()] == display_size:
                    Display.show_image(img)
                else:
                    if display_resize is None:
                        display_resize = DisplayImage(display_size)
                    display_img = display_resize.run(img.to_numpy_ref())
                    Display.show_image(display_img)

                # Explicitly release image buffer
                img.__del__()

                gc.collect()

            # Print current frame rate
            print(f"fps: {clock.fps()}")
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up: stop display and media system
        try:
            UVC.stop()
            time.sleep_ms(100)
            ob_det.deinit()
            csc.destroy()
        finally:
            try:
                if display_resize is not None:
                    display_resize.deinit()
            finally:
                Display.deinit()
```

### AI+UVC软解码推理

使用UVC摄像头获取图像，并使用软件解码将图像转换成RGB888格式，创建tensor，将tensor输入到AI模型中，获取AI模型的输出结果，最后将输出结果绘制到屏幕上。这里AI推理场景为YOLOv8检测。完整代码对应开发板上的 **此电脑->CanMV->sdcard->examples->21-AI-With-Others->ai_uvc_soft_decode.py**，示例代码如下：

```python
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import os,sys,ujson,gc,math, urandom
from media.display import *
from libs.DisplayConfig import init_display, DisplayImage
from media.media import *
from media.uvc import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import aidemo

# Custom YOLOv8 object detection class
class ObjectDetectionApp(AIBase):
    def __init__(self, kmodel_path, labels, model_input_size, max_boxes_num, confidence_threshold=0.5, nms_threshold=0.2, rgb888p_size=[224,224], display_size=[1920,1080], debug_mode=0):
        """
        Initialize object detection system.

        Parameters:
        - kmodel_path: Path to YOLOv8 KModel.
        - labels: List of class labels.
        - model_input_size: Model input size.
        - max_boxes_num: Max detection results to keep.
        - confidence_threshold: Detection score threshold.
        - nms_threshold: Non-max suppression threshold.
        - rgb888p_size: Camera input size (aligned to 16-width).
        - display_size: Output display size.
        - debug_mode: Enable debug timing logs.
        """
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        self.kmodel_path = kmodel_path
        self.labels = labels
        self.model_input_size = model_input_size
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.max_boxes_num = max_boxes_num

        # Align width to multiple of 16 for hardware compatibility
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode

        # Predefined colors for each class
        self.color_four = get_colors(len(self.labels))

        # Input scaling factors
        self.x_factor = float(self.rgb888p_size[0]) / self.model_input_size[0]
        self.y_factor = float(self.rgb888p_size[1]) / self.model_input_size[1]

        # Ai2d instance for preprocessing
        self.ai2d = Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)

    def config_preprocess(self, input_image_size=None):
        """
        Configure pre-processing: padding and resizing using Ai2d.
        """
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            top, bottom, left, right, self.scale = letterbox_pad_param(self.rgb888p_size, self.model_input_size)
            self.ai2d.pad([0,0,0,0,top,bottom,left,right], 0, [128,128,128])
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build(
                [1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                [1, 3, self.model_input_size[1], self.model_input_size[0]]
            )

    def postprocess(self, results):
        """
        Apply YOLOv8 post-processing including NMS and thresholding.
        """
        with ScopedTiming("postprocess", self.debug_mode > 0):
            new_result = results[0][0].transpose()
            det_res = aidemo.yolov8_det_postprocess(
                new_result.copy(),
                [self.rgb888p_size[1], self.rgb888p_size[0]],
                [self.model_input_size[1], self.model_input_size[0]],
                [self.display_size[1], self.display_size[0]],
                len(self.labels),
                self.confidence_threshold,
                self.nms_threshold,
                self.max_boxes_num
            )
            return det_res

    def draw_result(self, img, dets):
        """
        Draw detection results and send label info via UART.
        """
        with ScopedTiming("display_draw",self.debug_mode >0):
            if dets:
                for i in range(len(dets[0])):
                    x, y, w, h = map(lambda x: int(round(x, 0)), dets[0][i])
                    img.draw_rectangle(x,y, w, h, color=self.color_four[dets[1][i]],thickness=4)
                    img.draw_string_advanced( x , y-50,32," " + self.labels[dets[1][i]] + " " + str(round(dets[2][i],2)) , color=self.color_four[dets[1][i]])


if __name__ == "__main__":

    display_mode = "auto"
    requested_display_size = None  # Optional [width, height] override.

    display_size = init_display(display_mode, requested_display_size, to_ide=True)
    # Reuse AI2D configuration; inference and annotations stay in source coordinates.
    display_resize = None

    # Initialize media manager to manage frame buffers and UVC stream


    # Wait for USB camera to be detected
    while True:
        plugin, dev = UVC.probe()
        if plugin:
            print(f"detect USB Camera {dev}")
            break
        time.sleep_ms(100)

    # Select and configure UVC video mode: 640x480 @ 30 FPS, MJPEG format
    mode = UVC.video_mode(640, 480, UVC.FOURCC_MJPEG, 30)
    succ, mode = UVC.select_video_mode(mode)
    print(f"select mode success: {succ}, mode: {mode}")

    # Define input image from USB camera (sensor side)
    rgb888p_size = [640, 480]

    # Path to the YOLOv8n kmodel
    kmodel_path = "/sdcard/examples/kmodel/yolov8n_224.kmodel"

    # COCO class labels used for detection
    labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
              "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
              "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
              "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
              "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
              "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote",
              "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
              "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

    # Detection parameters
    confidence_threshold = 0.3  # Minimum confidence to accept a detection
    nms_threshold = 0.4         # Non-Maximum Suppression threshold
    max_boxes_num = 30          # Max boxes per frame after filtering

    # Initialize object detection application with YOLOv8 model
    ob_det = ObjectDetectionApp(
        kmodel_path,
        labels=labels,
        model_input_size=[224, 224],
        max_boxes_num=max_boxes_num,
        confidence_threshold=confidence_threshold,
        nms_threshold=nms_threshold,
        rgb888p_size=rgb888p_size,
        display_size=rgb888p_size,
        debug_mode=0
    )

    # Configure Ai2d preprocessing (resize + letterbox pad)
    ob_det.config_preprocess()

    # Start UVC video stream with pixel format conversion enabled
    UVC.start(cvt=False)

    clock = time.clock()

    try:
        # Main loop: acquire frame, run inference, draw and display
        while True:
            clock.tick()
            img = UVC.snapshot()
            if img is not None:
                # Convert format (e.g., to RGB888)
                img = img.to_rgb888()
                # Convert to Ulab.Numpy.ndarray
                img_np_hwc = img.to_numpy_ref()
                # HWC->CHW
                img_np_chw = hwc2chw(img_np_hwc)

                # Run YOLOv8 inference on the current frame
                res = ob_det.run(img_np_chw)

                # Draw detection results on the frame
                ob_det.draw_result(img, res)

                # Show result on display
                if [img.width(), img.height()] == display_size:
                    Display.show_image(img)
                else:
                    if display_resize is None:
                        display_resize = DisplayImage(display_size)
                    display_img = display_resize.run(img.to_numpy_ref())
                    Display.show_image(display_img)

                # Explicitly release image buffer
                img.__del__()

                gc.collect()

            # Print current frame rate
            print(f"fps: {clock.fps()}")
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up: stop display and media system
        try:
            UVC.stop()
            time.sleep_ms(100)
            ob_det.deinit()
        finally:
            try:
                if display_resize is not None:
                    display_resize.deinit()
            finally:
                Display.deinit()
```

### AI+LVGL图形界面

在 AI 推理的基础上叠加 LVGL 图形界面，用触摸屏控制推理任务的启停。示例中 YOLOv8 目标检测和人脸检测各跑在独立线程中，结果分别绘制到两个 OSD 图层上，LVGL 界面绘制在另一个图层，互不干扰。

关键点：

- **多 OSD 图层**：通过 `init_display(..., osd_num=2)` 申请多个 OSD 层，AI 结果和 LVGL 界面分层绘制，避免互相覆盖。
- **LVGL 显示驱动对接**：实现 `disp_drv_flush_cb` 把 LVGL 渲染的缓冲区刷到 Display。
- **触摸输入**：通过 `lv.indev_create()` 注册 POINTER 类型输入设备，在回调中读取 `TOUCH` 数据并换算成 LVGL 坐标。
- **线程与资源释放**：每个检测任务一个线程，注意 KPU 是互斥资源，多线程推理时需要串行化访问；退出时按"线程停止 → 模型 `deinit()` → LVGL 反初始化 → media 反初始化"的顺序释放。

```python
from libs.DisplayConfig import init_display
import lvgl as lv
import _thread

def media_init():
    # 申请 2 个 OSD 图层：一个给 AI 结果，一个给 LVGL 界面
    display_size = init_display(display_mode, requested_display_size, to_ide=True, osd_num=2)
    ...

def disp_drv_flush_cb(disp_drv, area, color):
    # 把 LVGL 渲染结果刷到 Display 的 OSD 图层
    ...

def lvgl_init():
    lv.init()
    disp_drv = lv.disp_create(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    disp_drv.set_flush_cb(disp_drv_flush_cb)
    ...

# 两个检测任务各起一个线程
_thread.start_new_thread(face_det_thread, ())
_thread.start_new_thread(yolov8_det_thread, ())
```

完整代码见开发板上的 **此电脑->CanMV->sdcard->examples->21-AI-With-Others->ai_lvgl.py**。

### AI+保存MP4

在实时目标检测的过程中，检测到指定目标（示例中为 `apple`）时自动把视频编码保存成标准 MP4 文件，可用于事件抓拍、告警录像等场景。

关键点：

- **双通道出图**：一路 RGB888P 给 AI 推理，一路 YUV 给硬件编码器，互不影响。
- **硬件编码**：使用 `media.vencoder` 做 H.264/H.265 硬件编码，示例默认 `K_PT_H265`，码率 512 kbps。
- **MP4 封装**：通过 `mpp.mp4_format` 创建 muxer 和 video track，把编码后的码流写成标准 MP4。
- **从 I 帧开始录制**：编码器输出的第一包必须是 IDR 帧，否则录出来的文件无法正常播放。示例中用 `save_idr` 缓存 SPS/PPS 和 IDR 帧，确保每个文件都以关键帧开头。

```python
from media.vencoder import *
from mpp.mp4_format import *

def draw_result(self, osd_img, dets):
    has_apple = False
    for i in range(len(dets[0])):
        if self.labels[dets[1][i]] == "apple":
            has_apple = True
        ...
    return has_apple

# 主循环中：检测到目标才开始录制
has_apple = ob_det.draw_result(osd_img, res)
if has_apple:
    file_name = "/data/has_apple_" + str(mp4_id) + ".mp4"
    mp4_handle = mp4_muxer_init(file_name, fmp4_flag)
    mp4_muxer_create_video_track(mp4_handle, mp4_size[0], mp4_size[1], venc_payload_type)
    ...
```

完整代码见开发板上的 **此电脑->CanMV->sdcard->examples->21-AI-With-Others->ai_save_mp4.py**。

```{admonition} 提示
录制文件保存在 `/data` 目录下。请注意该分区容量有限，长时间录制前需要自行清理或改用 SD 卡路径。
```

### AI+MP4文件推理

前面的示例都是对摄像头实时画面推理。本示例演示对**本地 MP4 文件**推理：解封装 MP4 取出视频码流，经硬件解码得到图像帧，再送入 AI 模型，适合离线视频的批量分析。示例使用 YuNet 人脸检测模型。

关键点：

- **解封装 + 解码**：用 `mpp.mp4_format` 解封装 MP4，用 `media.vdecoder` 做 H.264/H.265 硬件解码。
- **格式转换**：解码输出为 YUV，通过 `nonai2d` 的 `CSC` 模块硬件转换成 RGB888 供 AI 使用。
- **显示适配**：视频分辨率与屏幕分辨率通常不一致，用 `libs.DisplayConfig` 的 `DisplayImage` 把画面缩放到实际显示分辨率，详见 [DisplayConfig 模块API手册](./api/aidemo/display_config_module_api_manual.md)。

```python
from mpp.mp4_format import *
import media.vdecoder as vdecoder
from nonai2d import CSC
from libs.DisplayConfig import get_display_type, init_display, DisplayImage

# display_type 为 None 时按开发板型号自动选择屏驱动
display_type = None
requested_display_size = None
```

完整代码见开发板上的 **此电脑->CanMV->sdcard->examples->21-AI-With-Others->face_detect_yunet_from_mp4.py**。

## FAQ
  
### 开发过程中如何查找问题所在？

📝 首先根据不同的阶段和错误采取不同的方法：

- 如果模型转换阶段出现错误，可能是转换代码存在问题，需要阅读nncase的使用方法，调整转换代码；
- 如果模型转换成功，但是效果不及预期，可以考虑调整阈值、更改模型转换的量化方式、训练时调整训练参数；
- 如果模型转换成功，但是帧率较低，可以考虑更换更轻量的模型或者降低模型输入分辨率；
- 如果部署报错，请查看部署代码报错行数，根据API文档查找报错原因，调整代码；

### nncase支持哪些算子？

📝 nncase支持的onnx算子和tflite算子见链接：[onnx算子支持](https://github.com/kendryte/nncase/blob/master/docs/onnx_ops.md) 和 [tflite算子支持](https://github.com/kendryte/nncase/blob/master/docs/tflite_ops.md)

### 在转换模型时报错“ImportError: DLL load failed while importing _nncase”

📝 请参考如下链接的解决方法：[ImportError: DLL load failed while importing _nncase](https://github.com/kendryte/nncase/issues/451)

### 转换模型时报错“RuntimeError: Failed to initialize hostfxr”

📝 请安装dotnet-sdk-7.0， 请不要再Anaconda虚拟环境中安装dotnet-sdk。

Linux:

```shell
sudo apt-get update
sudo apt-get install dotnet-sdk-7.0
If you still have problems after installation, maybe you install dotnet in a virtual enviroment, set the environment variables. dotnet error
export DOTNET_ROOT=/usr/share/dotnet
```

Windows: 请参考微软官方网站。

### 在线训练平台和AICube的区别？

📝 在线训练平台的使用云端算力，资源紧张时需要排队，同时参数配置比较简单，一键训练，灵活性较低；AICube使用本地私人算力，环境和参数配置比较复杂，灵活性高。他们的目的都是获得kmodel和配置文件，使用固件中的`CanMV/sdcard/examples/19-CloudPlatScripts`的脚本即可实现部署。

<a id="faq-script-autostart"></a>

### 如何将调试好的脚本设置为自启动？

📝 将脚本保存在`/sdcard`目录下以`main.py`命名。或者使用CanMV IDE的`工具(T)`->`Save open script to CanMV board (as main.py)`保存后，重新上电启动。

### YOLO库中支持哪些任务？

📝 YOLOv5支持分类、检测、分割三类任务；YOLOv8、YOLO11和YOLO26支持分类、检测、分割、旋转目标检测和关键点检测五类任务。各类支持情况见 [YOLO 模块API手册](./api/aidemo/yolo_module_api_manual.md)。

另外，YOLO26 模型直接输出带有语义信息的结果，构造函数中**不再包含** `nms_thresh` 参数。

### UVC的软硬件解码有什么区别？

📝 硬件解码使用CSC实现格式转换，将UVC图像数据转换成RGB888的Image实例；软件解码使用Image实例的`to_rgb888`接口将图像数据转换成RGB888格式的Image实例。硬件解码比软件解码更快，帧率更高。

### 如何获取支持？

📝 在开发过程中遇到问题，您可以前往嘉楠开发者社区问答论坛发帖提问。论坛地址：[Canaan问答论坛](https://www.kendryte.com/answer/)。

## 附录

### API

K230 MicroPython API文档见链接：[API文档](./api/index.md)

### KTS

`K230_training_scripts（KTS）`是实现的端到端的训练处理过程，但是该项目的代码是基于双系统C++开发的，您可以使用该工具获取kmodel，但该工具中不包含MicroPython部署代码，您需要自行编写。项目地址：[K230_training_scripts](https://github.com/kendryte/K230_training_scripts)。
