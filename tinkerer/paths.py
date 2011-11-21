'''
    paths
    ~~~~~

    Tinkerer path information.

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import os
import tinkerer

# blog paths
root = os.path.abspath(".")
source = "source"
blog = "blog"
doctree = os.path.join(blog, "doctrees")
html = os.path.join(blog, "html")
master_file = os.path.join(root, source, tinkerer.master_doc + tinkerer.source_suffix)
conf_file = os.path.join(root, source, "conf.py")

# package path
__package_path = os.path.abspath(os.path.dirname(__file__))

# absolute path to assets
__static_abs_path = os.path.join(__package_path, "static")
__themes_abs_path = os.path.join(__package_path, "themes")
__templates_abs_path = os.path.join(__package_path, "templates")

# relative path to assets required by conf.py
themes = os.path.relpath(__themes_abs_path, source)
templates = os.path.relpath(__templates_abs_path, source)
static = os.path.relpath(__static_abs_path, source)

