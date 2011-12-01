'''
    Internal template renderer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Jinja2-based renderer for internal templates

    :copyright: Copyright 2011 by Vlad Riscutia
'''
from jinja2 import Environment, PackageLoader
import re
import tinkerer.paths

env = Environment(loader=PackageLoader("tinkerer", "__templates"))


# render an internal template
def render(template, destination, context={}):
    with open(destination, "w") as f:
        f.write(env.get_template(template).render(context))


# render master document
def render_master_file():
    render("master.rst", tinkerer.paths.master_file)


# render conf.py
def render_conf_file(extensions=["tinkerer.ext.blog", "tinkerer.ext.disqus"]):
    render("conf.py", tinkerer.paths.conf_file,
           {"extensions": ", ".join(["'%s'" % ext for ext in extensions])})


# render new post
def render_post(post_file, title="Title", tags="none"):
    render("post.rst", post_file, 
           {"title": title,
            "tags" : tags})


# render new page
def render_page(page_file, title="Title"):
    render("page.rst", page_file,
           {"title": title})

