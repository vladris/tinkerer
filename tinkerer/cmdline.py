'''
    Tinkerer command line
    ~~~~~~~~~~~~~~~~~~~~~

    Automates the following blog operations:

    setup - to create a new blog
    build - to clean build blog
    post - to create a new post
    page - to create a new page

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import argparse
import os
import shutil
import sphinx
import subprocess
from datetime import datetime
import paths
import tinkerer


# recursively create directories
def get_path(directory, subdirectories):
    if not subdirectories:
        return directory

    directory = os.path.join(directory, subdirectories[0])
    if not os.path.exists(directory):
        os.mkdir(directory)
    return get_path(directory, subdirectories[1:])


# setup a new blog
def setup():
    if not os.path.exists("_static"):
        os.mkdir("_static")

    with open(paths.master_file, "w") as f:
        f.write("""\
Sitemap
=======

.. toctree::
   :maxdepth: 1

  
""")

    with open(paths.conf_file, "w") as f:
        f.write("""\
import tinkerer
import tinkerer.paths        


# TODO: Edit the lines below
project = 'My blog'                                       # Change this to the name of your blog
tagline = 'Add intelligent tagline here'                  # Change this to the tagline of your blog
copyright = '1984, Winston Smith'                         # Change this to your copyright string
website = 'http://127.0.0.1'                              # Change this to your URL (required for RSS)


# More tweaks
disqus_shortname = None                                   # Add your Disqus shortname to enable comments
html_favicon = 'tinkerer.ico'                             # Favicon
html_theme = 'metropolish'                                # Tinkerer theme (or your own)
html_theme_options = { }                                  # Theme-specific options, see docs


# Edit lines below to further customize Sphinx build
extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus'] # Add other Sphinx extensions here
templates_path = ['_templates', tinkerer.paths.templates] # Add other template paths here
html_static_path = ['_static', tinkerer.paths.static]     # Add other static paths here
html_theme_path = [tinkerer.paths.themes]                 # Add other theme paths here
exclude_patterns = []                                     # Add file patterns to exclude from build


# Do not modify below lines as the values are required by Tinkerer to play nice with Sphinx
source_suffix = tinkerer.source_suffix
master_doc = tinkerer.master_doc
version = tinkerer.__version__
release = tinkerer.__version__
html_title = project
html_use_index = False
html_show_sourcelink = False""")

    print("")
    print("Your new blog is almost ready!")
    print("You just need to edit a couple of lines in ./sources/conf.py")


# clean build blog
def build():
    if os.path.exists(paths.blog):
        shutil.rmtree(paths.blog)
    sphinx.main(["sphinx-build", "-d", paths.doctree, "-b", "html", ".", paths.html])


# add new post
def post(post_name):
    year, month, day = datetime.today().strftime("%Y/%m/%d").split("/")

    # create post file
    post_path = os.path.join(get_path(paths.root, [year, month, day]), post_name)
    with open(post_path + tinkerer.source_suffix, "w") as f:
        f.write("""\
Title 
=====

.. tags:: none
.. comments:: """)

    # update toc root
    post = "   " + "/".join([year, month, day, post_name]) + "\n"

    # load master file, insert post after "maxdepth" directive and rewrite the file
    with open(paths.master_file, "r") as f:
        lines = f.readlines()

    for line_no, line in enumerate(lines):
        if "maxdepth" in line:
            break
    lines.insert(line_no + 2, post)

    with open(paths.master_file, "w") as f:
        f.writelines(lines)
        
    # recreate index.html file to redirect to latest post
    redirect_to = "/".join([".", paths.html, year, month, day, post_name])
    with open(os.path.join(paths.root, "index.html"), "w") as f:
        f.write("""\
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="REFRESH" content="0; url=%s.html" />
    </head>
    <body/>
</html>""" % redirect_to)


# add new page
def page(page_name):
    # create page file
    page_path = os.path.join(get_path(paths.root, ["pages"]), page_name)
    with open(page_path + tinkerer.source_suffix, "w") as f:
        f.write("""\
Title
=====""")

    # update toc root
    page = "   pages/" + page_name + "\n"

    # append page to master file
    with open(paths.master_file, "a") as f:
        f.write(page)


def main(argv=[]):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--setup", action="store_true", help="setup a new blog")
    group.add_argument("--build", action="store_true", help="build blog")
    group.add_argument("--post", nargs=1, help="create a new post")
    group.add_argument("--page", nargs=1, help="create a new page")

    command = parser.parse_args()
    if command.setup:
        setup()
    elif command.build:
        build()
    elif command.post:
        post(command.post[0])
    elif command.page:
        page(command.page[0])
    else:
        parser.print_help()

