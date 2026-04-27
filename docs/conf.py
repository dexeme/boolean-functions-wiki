# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os, sys
sys.path.append(os.path.abspath("_ext"))


project = 'Boolean Functions'
copyright = '2026, Tiago Siqueira'
author = 'Tiago Siqueira'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sage_block',
    'sagecell_directive',
    'link',
    'lazy_chunks',
]

templates_path = ['_templates']
exclude_patterns = [
    'content/_includes/*.rst',
    '_includes/*.rst',
    'pages/_includes/*.rst',
]
language = 'en'
default_role = 'math'
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# https://github.com/flintlib/flint/blob/main/doc/source/conf.py
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'a4paper',
    'fontpkg': '',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    'preamble': '\\usepackage{lmodern}\n\\setcounter{tocdepth}{2}\n\\urlstyle{tt}',
    'preamble': '\\usepackage{mathrsfs}\n\\usepackage{lmodern}\n\\setcounter{tocdepth}{2}\n\\urlstyle{tt}',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

html_theme = 'classic'
html_static_path = ['_static']
html_js_files = [
    'https://sagecell.sagemath.org/static/embedded_sagecell.js',
    'sagecell-init.js',
]
html_css_files = [
    'custom.css',
]
html_theme_options = {
    'sidebarwidth' : 300,
    'collapsiblesidebar': True,
    'bodyfont': "'arial', sans-serif",
    'headfont': "'arial', sans-serif",
    'sidebarbtncolor': '#666',
    'sidebarbgcolor': '#444',
    'sidebarlinkcolor': '#ddd',
    'relbarbgcolor': '#333',
    'footerbgcolor': '#333',
    'headbgcolor': '#fff',
}
