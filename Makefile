# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXMULTIVERSION ?= sphinx-multiversion
SOURCEDIR     = .
CONFDIR       = .
BUILDDIR      = _build
SOURCEDIR_EN  = en
SOURCEDIR_ZH  = zh
WEB_DOCS_BUILDER_URL ?= https://ai.b-bug.org/~zhengshanshan/web-docs-builder
TEMPLATE = _static/init_mermaid.js _static/mermaid.min.js _templates/versionsFlex.html _templates/Fleft.html _templates/Footer.html _templates/Fright.html  _templates/layout.html _static/topbar.css _static/custom-theme.css
TEMPLATE_EN = _static/init_mermaid.js _static/mermaid.min.js _templates/versionsFlex.html _templates/FleftEn.html _templates/FooterEn.html _templates/FrightEn.html  _templates/layout.html _static/topbar.css _static/custom-theme.css
# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# %: Makefile $(TEMPLATE)
# 	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html: html-en html-zh

html-zh: Makefile $(TEMPLATE)
	SPHINX_LANGUAGE=zh_CN $(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html/zh" -c "$(CONFDIR)"

html-en: Makefile $(TEMPLATE_EN)
	SPHINX_LANGUAGE=en $(SPHINXBUILD) -b html "$(SOURCEDIR_EN)" "$(BUILDDIR)/html/en" -c "$(CONFDIR)"

mhtml: mhtml_cn mhtml_en

mhtml_cn: $(TEMPLATE)
	SPHINX_LANGUAGE=zh_CN $(SPHINXMULTIVERSION) "$(SOURCEDIR)" "$(BUILDDIR)/zh" $(SPHINXOPTS) -c "$(CONFDIR)"
# 英文
mhtml_en: $(TEMPLATE_EN)
	SPHINX_LANGUAGE=en $(SPHINXMULTIVERSION) "$(SOURCEDIR_EN)" "$(BUILDDIR)/en" $(SPHINXOPTS) -c "$(CONFDIR)"

# mhtml: $(TEMPLATE)
# 	@$(SPHINXMULTIVERSION) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

_templates:
	mkdir $@

_static/init_mermaid.js:
	@wget -q $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/topbar.css:
	@wget -q $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/custom-theme.css:
	@wget -q $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/versionsFlex.html: _templates
	@wget -q $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/layout.html: _templates
	@wget -q $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/Fleft.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/Footer.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/Fright.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/FleftEn.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/FooterEn.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/FrightEn.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/mermaid.min.js: 
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@
