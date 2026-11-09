# CanMV K230 Documentation / 开发文档

本仓库提供嘉楠 Kendryte K230 平台 CanMV 的中英文文档，涵盖开发板入门、固件烧录与编译、CanMV Visual Studio Code 扩展、MicroPython API，以及 AI、图像、多媒体、网络和外设开发示例。

This repository contains the Chinese and English documentation for CanMV on the Canaan Kendryte K230 platform, covering development boards, firmware flashing and builds, the CanMV Visual Studio Code extension, MicroPython APIs, and examples for AI, imaging, multimedia, networking, and peripherals.

## 阅读文档 / Documentation

| 内容 / Topic | 中文 | English |
| --- | --- | --- |
| 文档首页 / Overview | [文档首页](zh/index.md) | [Overview](en/index.md) |
| 快速入门 / Quick start | [快速入门](zh/quick_start.md) | [Quick start](en/quick_start.md) |
| 开发板 / Development boards | [开发板介绍](zh/userguide/boards/index.md) | [Development boards](en/userguide/boards/index.md) |
| 烧录固件 / Flash firmware | [烧录指南](zh/userguide/how_to_burn_firmware.md) | [Flashing guide](en/userguide/how_to_burn_firmware.md) |
| 编译固件 / Build firmware | [编译指南](zh/userguide/how_to_build.md) | [Build guide](en/userguide/how_to_build.md) |
| CanMV 扩展 / CanMV extension | [扩展使用说明](zh/userguide/how_to_use_ide.md) | [Extension guide](en/userguide/how_to_use_ide.md) |
| 运行示例 / Run examples | [运行示例](zh/userguide/how_to_run_examples.md) | [Run examples](en/userguide/how_to_run_examples.md) |
| 示例程序 / Examples | [示例程序](zh/example/index.md) | [Examples](en/example/index.md) |
| API 参考 / API reference | [API 参考](zh/api/index.md) | [API reference](en/api/index.md) |
| AI 开发 / AI development | [AI 开发指南](zh/ai_dev_doc.md) | [AI development](en/ai_dev_doc.md) |
| 常见问题 / FAQ | [常见问题](zh/faq.md) | [FAQ](en/faq.md) |
| 更新日志 / Changelog | [更新日志](zh/changelog.md) | [Changelog](en/changelog.md) |

## 构建文档网站 / Build the documentation website

可以直接在仓库中阅读 Markdown 文档。构建 HTML 网站需要 Python、Sphinx 依赖，以及提供网站模板和静态资源的服务器。请先将环境变量 `WEB_DOCS_BUILDER_URL` 设置为可访问的模板服务器地址，再运行以下命令。

You can read the Markdown files directly in this repository. Building the HTML website requires Python, the Sphinx dependencies, and a server providing the website templates and static assets. Set the `WEB_DOCS_BUILDER_URL` environment variable to a reachable template server before running:

```sh
python3 -m pip install -r requirements.txt
make html
```

生成的中文和英文页面分别位于 `_build/html/zh/` 和 `_build/html/en/`。

The generated Chinese and English pages are written to `_build/html/zh/` and `_build/html/en/`, respectively.

## 参与贡献 / Contributing

发现文档问题或希望完善内容，请提交 [Issue](https://github.com/kendryte/k230_canmv_docs/issues) 或 Pull Request，并参考[贡献指南](.github/CONTRIBUTING.md)。文档页面请使用小写英文文件名，并尽量同步更新中英文内容；仓库根目录的入口文件使用 `README.md`。

Report documentation issues or suggest improvements through [Issues](https://github.com/kendryte/k230_canmv_docs/issues) and pull requests. Read the [contribution guide](.github/CONTRIBUTING.md). Use lowercase English filenames for documentation pages and update both language versions where possible; the repository's root entry file is `README.md`.
