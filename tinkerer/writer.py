'''
    writer
    ~~~~~~

    Internal template writer - handles template rendering and blog setup.

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader
import os
import shutil
from tinkerer import paths, utils


# jinja environment
env = Environment(loader=ChoiceLoader([
        # first choice is _templates subdir from blog root
        FileSystemLoader(paths.templates),
        # if template is not there, use tinkerer builtin
        PackageLoader("tinkerer", "__templates")]))


def render(template, destination, context={}, safe=False):
    '''
    Renders the given template at the given destination with the given context.
    '''
    with open(destination, "wb") as dest:
        dest.write(env.get_template(template).render(context).encode("utf8"))



def render_safe(template, destination, context={}):
    '''
    Similar to render but only renders the template if the destination doesn't
    already exist.
    '''
    # if safe is set to True, abort if file already exists
    if os.path.exists(destination):
        return False

    render(template, destination, context)

    return True



def write_master_file():
    '''
    Writes the blog master document.
    '''
    return render_safe("master.rst", paths.master_file)



def write_index_file():
    '''
    Writes the root index.html file.
    '''
    return render_safe("index.html", paths.index_file)



'''
Default Tinkerer extensions.
'''
DEFAULT_EXTENSIONS = [
    "tinkerer.ext.blog",
    "tinkerer.ext.disqus"
]



def write_conf_file(extensions=DEFAULT_EXTENSIONS, theme="flat"):
    '''
    Writes the Sphinx configuration file.
    '''
    return render_safe("conf.py", paths.conf_file,
                {"extensions": ", ".join(["'%s'" % ext for ext in extensions]),
                 "theme": theme })



def copy_templates():
    '''
    Copies Tinkerer post and page templates to blog _templates directory.
    '''
    for template in [paths.post_template, paths.page_template]:
        if not os.path.exists(os.path.join(paths.root, "_templates", template)):
            shutil.copy(
                os.path.join(paths.__internal_templates_abs_path, template),
                    os.path.join(paths.root, "_templates"))



def setup_blog():
    '''
    Sets up a new blog.
    '''
    utils.get_path(paths.root, "_static")
    utils.get_path(paths.root, "_templates")
    utils.get_path(paths.root, "drafts")
    copy_templates()
    write_master_file()
    write_index_file()
    return write_conf_file()

