import datetime
import importlib
import pathlib
import sys

import recommonmark.transform
from sphinx_gallery.sorting import ExplicitOrder
from sphinx_gallery.sorting import NumberOfCodeLinesSortKey

here = pathlib.Path(__file__).parent
sys.path.append(str(here / ".."))


author = "Markus Quade"
project = "reg_bench"


# -------------------------------
# No need to edit below this line
# -------------------------------

copyright = f"{datetime.datetime.now().year}, {author}"

module = importlib.import_module(project.lower())
version = release = getattr(module, "__version__")

master_doc = "index"
rst_epilog = ".. |version| replace:: %s" % version

extensions = [
    "sphinx.ext.mathjax",
    "recommonmark",
    "sphinxcontrib.apidoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx_gallery.gen_gallery",
]


def get_version(version):
    return str(version), f"/{version}"


html_context = {
    "current_version": str(version),
    "versions": [get_version(v) for v in ["stable", "latest", "0.1.0"]],
    "READTHEDOCS": True,
    "extra_css_files": ["_static/custom.css"],
}

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

apidoc_module_dir = f"../{project.lower()}"
apidoc_excluded_paths = ["tests"]
apidoc_toc_file = False
apidoc_separate_modules = True
apidoc_extra_args = ["-P"]

autodoc_default_options = {"members": True, "private-members": False}
autodoc_member_order = "bysource"
autoclass_content = "init"

sphinx_gallery_conf = {
    "examples_dirs": "../example",  # path to your example scripts
    "gallery_dirs": "examples",  # path where to save gallery generated examples
    # "subsection_order": ExplicitOrder(["../examples/abstract", "../examples/concrete"]),
    "within_subsection_order": NumberOfCodeLinesSortKey,
    "filename_pattern": "/*.py",
    "ignore_pattern": r"__init__\.py",
    # "show_memory": True,
}


language = None

html_static_path = ["static"]


if (here / "static/logo.png").exists():

    html_logo = latex_logo = "./static/logo.png"


exclude_patterns = ["build", "_build"]
# pygments_style = "sphinx"

add_module_names = True
add_function_parentheses = False
todo_include_todos = True

html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": -1, "explore": False}
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

latex_show_pagerefs = True
latex_use_latex_multicolumn = True
latex_show_urls = "footnote"
latex_documents = [(master_doc, f"{project.lower()}.tex", f"{project} Documentation", author, "manual", True)]

default_role = None

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.7", None),
    "numpy": ("http://docs.scipy.org/doc/numpy/", None),
    "pandas": ("http://pandas.pydata.org/pandas-docs/stable/", None),
    "geopandas": ("http://geopandas.org/", None),
}

intersphinx_aliases = {
    ("py:class", "geopandas.geoseries.GeoSeries"): ("py:class", "geopandas.GeoSeries"),
    ("py:class", "pandas.core.series.Series"): ("py:class", "pandas.Series"),
}


# Work around for Issue #5603(https://github.com/sphinx-doc/sphinx/issues/5603)
def add_intersphinx_aliases_to_inv(app):
    from sphinx.ext.intersphinx import InventoryAdapter

    inventories = InventoryAdapter(app.builder.env)

    for alias, target in app.config.intersphinx_aliases.items():
        alias_domain, alias_name = alias
        target_domain, target_name = target
        try:
            found = inventories.main_inventory[target_domain][target_name]
            try:
                inventories.main_inventory[alias_domain][alias_name] = found
            except KeyError:
                continue
        except KeyError:
            continue


def setup(app):
    app.add_config_value("recommonmark_config", {"auto_toc_tree_section": "Contents"}, True)
    app.add_config_value("intersphinx_aliases", {}, "env")
    app.connect("builder-inited", add_intersphinx_aliases_to_inv)
    app.add_transform(recommonmark.transform.AutoStructify)
