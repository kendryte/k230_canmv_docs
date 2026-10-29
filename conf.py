# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime
import os
import sys

sys.path.append(os.path.abspath("exts"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = os.getenv("PROJECT") or "CanMV K230"
copyright = (
    str(datetime.datetime.now().year)
    + " 嘉楠 | "
    + "京ICP备2025124317号 | 京公网安备11010802045870号"
)
# author = os.getenv('AUTHOR') or 'Canaan'
# release = '0.1'
root_doc = os.getenv("ROOT_DOC") or "index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_copybutton",
    "myst_parser",
    "sphinx.ext.mathjax",
    "sphinx_multiversion",
    "sphinxcontrib.mermaid",
]
html_js_files = ["mermaid.min.js", "init_mermaid.js", "transform.js"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
html_title = "CanMV K230"
templates_path = ["_templates"]
exclude_patterns = ["**/.*", "**/--*"]

# language = 'zh_CN'
language = os.getenv("SPHINX_LANGUAGE", "en")

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

myst_heading_anchors = 6
suppress_warnings = ["myst.header"]

html_copy_source = True
html_show_sourcelink = False

html_favicon = "favicon.ico"

# html_show_sphinx = False

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

myst_enable_extensions = [
    "dollarmath",  # 支持 $...$ 行内公式
    "amsmath",  # 支持 \begin{align} 等多行公式
]

html_css_files = ["topbar.css", "custom-theme.css", "auto-nums.css"]
locale_dirs = ["locale"]

html_theme_options = {
    "collapse_navigation": True,
    "repository_url": "https://github.com/kendryte/k230_canmv_docs",
    "navigation_depth": 7,
    "use_repository_button": True,
    "primary_sidebar_end": ["versionsFlex.html"],
    "footer_start": ["Fleft.html"],
    "footer_center": ["Footer.html"],
    "footer_end": ["Fright.html"],
    "navbar_start": ["logo.html"],
    "navbar_center": ["nav.html"],
    "navbar_end": ["login.html", "lang.html"],
    "article_footer_items": ["content.html"],
}

if language == "en":
    html_theme_options["footer_start"] = ["FleftEn.html"]
    html_theme_options["footer_center"] = ["FooterEn.html"]
    html_theme_options["footer_end"] = ["FrightEn.html"]
    html_theme_options["article_footer_items"] = ["contentEn.html"]
    html_theme_options["navbar_center"] = ["navEn.html"]
    html_theme_options["navbar_end"] = ["lang.html"]
    html_theme_options["article_footer_items"] = ["contentEn.html"]
    copyright = (
        str(datetime.datetime.now().year)
        + " Canaan | "
        + "Beijing ICP No. 2025124317 | Beijing Public Security Network No. 11010802045870"
    )

# -- Options for sphinx-multiversion (核心多版本配置) --------------------------
#
# 哪些分支/标签会生成 HTML 版本，由 **两个地方** 共同决定：
#
#   第一步 - 文档构建脚本中的预处理阶段:
#     决定哪些远程分支/标签被拉取到本地并进行预处理（heading修正、链接修复等）。
#     只有经此步骤处理过的 ref 才会成为本地分支/标签，供 sphinx-multiversion 发现。
#     要增减版本 → 修改构建脚本中的 BRANCHES / TAGS 变量逻辑。
#
#   第二步 - 构建阶段 (smv_branch_whitelist / smv_tag_whitelist):
#     sphinx-multiversion 扫描所有本地分支/标签，通过这两个正则过滤。
#     只有匹配 whitelist 的本地 ref 才会被真正构建成 HTML。
#     要过滤版本 → 修改下面的 smv_branch_whitelist / smv_tag_whitelist 正则。
#
#   两步缺一不可：预处理创建了本地 ref + whitelist 放行 → 最终出现在文档版本列表中。

smv_branch_whitelist = r"^(v(1\.[2-9]|[2-9]|[1-9]\d+)(\.\d+)*.*|main|dev\/.*|feat\/.*)$"
smv_tag_whitelist = None
smv_remote_whitelist = None
smv_latest_version = "main"
