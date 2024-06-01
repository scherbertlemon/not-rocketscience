# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "src"))
project = 'not-rocketscience'
copyright = '2024, Andreas Roth <kommentare@s-lemon.de>'
author = 'Andreas Roth <kommentare@s-lemon.de>'
release = '0.2.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc"
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "_static/logo.png"
html_theme_options = {
    "logo_only": False,
    "display_version": True
}
html_css_files = [
    "custom.css"
]
