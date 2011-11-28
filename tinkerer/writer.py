'''
    Internal writer
    ~~~~~~~~~~~~~~~

    Handles template rendering and blog setup.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
from jinja2 import Environment, PackageLoader
from tinkerer import paths, utils


# jinja environment
env = Environment(loader=PackageLoader("tinkerer", "__templates"))


# render an internal template
def render(template, destination, context={}):
    with open(destination, "w") as f:
        f.write(env.get_template(template).render(context))


# write master document
def write_master_file():
    render("master.rst", paths.master_file)


# default extensions for conf.py
DEFAULT_EXTENSIONS = [
    "tinkerer.ext.blog",
    "tinkerer.ext.disqus",
    "tinkerer.ext.latest"
]


# write conf.py
def write_conf_file(extensions=DEFAULT_EXTENSIONS, theme="minimal"):
    render("conf.py", paths.conf_file,
           {"extensions": ", ".join(["'%s'" % ext for ext in extensions]),
            "theme": theme })


# setup blog
def setup_blog():
    utils.get_path(paths.root, "_static")
    write_master_file()
    write_conf_file()
    
