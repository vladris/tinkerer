'''
    Tinkerer command line
    ~~~~~~~~~~~~~~~~~~~~~

    Automates the following blog operations:

    setup - to create a new blog
    build - to clean build blog
    post - to create a new post
    page - to create a new page

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import argparse
from datetime import datetime
import jinja2
import os
import shutil
import sphinx
import subprocess
import sys
from tinkerer import page, paths, post, utils, writer


# setup a new blog
def setup(quiet=False):
    writer.setup_blog()

    if not quiet:
        print("")
        print("Your new blog is almost ready!")
        print("You just need to edit a couple of lines in %s" % (os.path.relpath(paths.conf_file), ))


# clean build blog
def build(quiet=False):
    if os.path.exists(paths.blog):
        shutil.rmtree(paths.blog)

    flags = ["sphinx-build"]
    if quiet: 
        flags.append("-q")
    flags += ["-d", paths.doctree, "-b", "html", paths.root, paths.html]

    return sphinx.main(flags)


# entry point
def main(argv=None):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--setup", action="store_true", help="setup a new blog")
    group.add_argument("--build", action="store_true", help="build blog")
    group.add_argument("--post", nargs=1, help="create a new post")
    group.add_argument("--page", nargs=1, help="create a new page")

    command = parser.parse_args(argv)
    if command.setup:
        setup()
    elif command.build:
        build()
    elif command.post:
        post.create(command.post[0])
    elif command.page:
        page.create(command.page[0])
    else:
        parser.print_help()

