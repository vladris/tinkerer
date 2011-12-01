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
from datetime import datetime
import jinja2
import os
import shutil
import sphinx
import subprocess
import tinkerer
import tinkerer.paths
import tinkerer.renderer
import tinkerer.utils


# setup a new blog
def setup(quiet=False):
    tinkerer.utils.get_path(tinkerer.paths.root, "_static")
    tinkerer.renderer.render_master_file()
    tinkerer.renderer.render_conf_file()

    if not quiet:
        print("")
        print("Your new blog is almost ready!")
        print("You just need to edit a couple of lines in %s" % (os.path.relpath(tinkerer.paths.conf_file), ))


# clean build blog
def build(quiet=False):
    if os.path.exists(tinkerer.paths.blog):
        shutil.rmtree(tinkerer.paths.blog)

    flags = ["sphinx-build"]
    if quiet: 
        flags.append("-q")
    flags += ["-d", tinkerer.paths.doctree, "-b", "html", tinkerer.paths.root, tinkerer.paths.html]

    return sphinx.main(flags)


# add new post
def post(post_title, date=None):
    if not date:
        date = datetime.today()

    year, month, day = date.strftime("%Y/%m/%d").split("/")
    post_name = tinkerer.utils.filename_from_title(post_title).lower()

    # create post file
    post_path = os.path.join(
                    tinkerer.utils.get_path(
                        tinkerer.paths.root, year, month, day), post_name
                    ) + tinkerer.source_suffix

    tinkerer.renderer.render_post(post_path, post_title)
    
    # update toc root
    post = "   " + "/".join([year, month, day, post_name]) + "\n"

    # load master file, insert post after "maxdepth" directive and rewrite the file
    with open(tinkerer.paths.master_file, "r") as f:
        lines = f.readlines()

    for line_no, line in enumerate(lines):
        if "maxdepth" in line:
            break
    lines.insert(line_no + 2, post)

    with open(tinkerer.paths.master_file, "w") as f:
        f.writelines(lines)
        
    # recreate index.html file to redirect to latest post
    redirect_to = "/".join([".", tinkerer.paths.html, year, month, day, post_name])
    with open(os.path.join(tinkerer.paths.root, "index.html"), "w") as f:
        f.write("""\
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="REFRESH" content="0; url=%s.html" />
    </head>
    <body/>
</html>""" % redirect_to)

    return post_path


# add new page
def page(page_title):
    page_name = tinkerer.utils.filename_from_title(page_title).lower()

    # create page file
    page_path = os.path.join(tinkerer.utils.get_path(tinkerer.paths.root, "pages"), page_name)

    tinkerer.renderer.render_page(page_path + tinkerer.source_suffix, page_title)

    # update toc root
    page = "   pages/" + page_name + "\n"

    # append page to master file
    with open(tinkerer.paths.master_file, "a") as f:
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

