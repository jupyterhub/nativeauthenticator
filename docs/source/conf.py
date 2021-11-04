# Configuration file for the Sphinx documentation builder.
#
# -- Project information -----------------------------------------------------

project = "Native Authenticator"
copyright = "2021, Leticia Portella"
author = "Leticia Portella"


# -- General MyST configuration ----------------------------------------------
# ref: https://myst-parser.readthedocs.io/en/latest/syntax/optional.html

myst_enable_extensions = [
    "substitution",
]


# -- General Sphinx configuration --------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_copybutton",
    "myst_parser",
]
templates_path = ["_templates"]
source_suffix = [".rst", ".md"]
root_doc = master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for linkcheck builder -------------------------------------------
# ref: http://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder

linkcheck_ignore = [
    r"(.*)github\.com(.*)#",  # javascript based anchors
]


# -- Options for HTML output -------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# pydata_spinx_theme's html_theme_options reference:
# https://pydata-sphinx-theme.readthedocs.io/en/latest/user_guide/configuring.html
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/jupyterhub/nativeauthenticator/",
    "use_edit_page_button": True,
}
html_context = {
    "github_user": "jupyterhub",
    "github_repo": "nativeauthenticator",
    "github_version": "main",
    "doc_path": "docs/source",
}

html_static_path = ["_static"]

# FIXME: This should be configured.
#
# html_favicon = "_static/logo/favicon.ico"
# html_logo = "_static/logo/logo.png"
