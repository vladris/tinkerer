'''
    writer
    ~~~~~~

    Internal template writer - handles template rendering and blog setup.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from jinja2 import Environment, PackageLoader
from tinkerer import paths, utils


# jinja environment
env = Environment(loader=PackageLoader("tinkerer", "__templates"))



def render(template, destination, context={}):
    '''
    Renders the given template at the given destination with the given context.
    '''
    with open(destination, "w") as f:
        f.write(env.get_template(template).render(context))



def write_master_file():
    '''
    Writes the blog master document.
    '''
    render("master.rst", paths.master_file)



def write_index_file():
    '''
    Writes the root index.html file.
    '''
    render("index.html", paths.index_file)



'''
Default Tinkerer extensions.
'''
DEFAULT_EXTENSIONS = [
    "tinkerer.ext.blog",
    "tinkerer.ext.disqus"
]



def write_conf_file(extensions=DEFAULT_EXTENSIONS, theme="modern"):
    '''
    Writes the Sphinx configuration file.
    '''
    render("conf.py", paths.conf_file,
           {"extensions": ", ".join(["'%s'" % ext for ext in extensions]),
            "theme": theme })



def setup_blog():
    '''
    Sets up a new blog.
    '''
    utils.get_path(paths.root, "_static")
    utils.get_path(paths.root, "drafts")
    write_master_file()
    write_index_file()
    write_conf_file()
    
