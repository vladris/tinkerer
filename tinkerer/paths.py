'''
    paths
    ~~~~~

    Tinkerer path information.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import os
import tinkerer

# package path
__package_path = os.path.abspath(os.path.dirname(__file__))

# absolute path to assets
__static_abs_path = os.path.join(__package_path, "static")
__templates_abs_path = os.path.join(__package_path, "templates")
__internal_templates_abs_path = os.path.join(__package_path, "__templates")
themes = os.path.join(__package_path, "themes")

# set other paths based on root path
def set_paths(root_path="."):
    # blog paths
    global root, blog, doctree, html, master_file, conf_file
    root = os.path.abspath(root_path)
    blog = os.path.join(root, "blog")
    doctree = os.path.join(blog, "doctrees")
    html = os.path.join(blog, "html")
    master_file = os.path.join(root, tinkerer.master_doc + tinkerer.source_suffix)
    conf_file = os.path.join(root, "conf.py")

    # relative path to assets required by conf.py
    global themes, templates, static
    templates = os.path.relpath(__templates_abs_path, root)
    static = os.path.relpath(__static_abs_path, root)


set_paths()
