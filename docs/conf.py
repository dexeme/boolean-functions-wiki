# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

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
]

templates_path = ['_templates']
exclude_patterns = []
language = 'en'
default_role = 'math'
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'classic'
html_static_path = ['_static']
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