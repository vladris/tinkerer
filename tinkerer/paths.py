'''
    paths
    ~~~~~

    Tinkerer path information.

    :copyright: Copyright 2011-2017 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import os
import tinkerer
import sys


# package path
__package_path = os.path.abspath(os.path.dirname(__file__))


# absolute path to assets
__internal_templates_abs_path = os.path.join(__package_path, "__templates")
templates = os.path.join(os.path.abspath("."), "_templates")
themes = os.path.join(__package_path, "themes")
static = os.path.join(__package_path, "static")


# template names
post_template = "post.rst"
page_template = "page.rst"


# favicon
favicon = "tinkerer.ico"


# add "./exts" path to os search path so Sphinx can pick up any extensions
# from there
sys.path.append(os.path.abspath("./_exts"))


def set_paths(root_path="."):
    '''
    Computes required relative paths based on given root path.
    '''
    global root, blog, doctree, html, master_file, index_file, conf_file
    root = os.path.abspath(root_path)
    blog = os.path.join(root, os.getenv("TINKERER_BLOG_PATH", "blog"))
    doctree = os.path.join(blog, "doctrees")
    html = os.path.join(blog, "html")
    master_file = os.path.join(root,
                               tinkerer.master_doc + tinkerer.source_suffix)
    index_file = os.path.join(root, "index.html")
    conf_file = os.path.join(root, "conf.py")

    # relative path to assets required by conf.py
    global themes, templates, static


# compute paths on import
set_paths()
