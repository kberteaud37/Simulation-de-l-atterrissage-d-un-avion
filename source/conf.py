# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath("../simulation_atterrissage"))

# -- Project information -----------------------------------------------------

project = "Simulation d'atterrissage"
copyright = '2025, Loranchet Pierrick - Berteaud Kilian - Chenuet Alexis'
author = 'Loranchet Pierrick - Berteaud Kilian - Chenuet Alexis'
release = 'Juin 2025'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
