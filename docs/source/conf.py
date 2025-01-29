
import os
import sys
sys.path.insert(0, os.path.abspath('../../')) 

# Configuration file for the Sphinx documentation builder.
project = 'my_package'
author = 'Your_author_name'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]
templates_path = ['_templates']
exclude_patterns = []

# HTML output theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['./docs/build/_static']
