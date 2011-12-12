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



def setup(quiet=False, filename_only=False):
    '''
    Sets up a new blog in the current directory.
    '''
    writer.setup_blog()

    if filename_only:
        print("conf.py")
    elif not quiet:
        print("")
        print("Your new blog is almost ready!")
        print("You just need to edit a couple of lines in %s" % (os.path.relpath(paths.conf_file), ))
        print("")



def build(quiet=False, filename_only=False):
    '''
    Runs a clean Sphinx build of the blog.
    '''
    # clean build directory
    if os.path.exists(paths.blog):
        shutil.rmtree(paths.blog)

    flags = ["sphinx-build"]
    # silence Sphinx if in quiet mode
    if quiet or filename_only: 
        flags.append("-q")
    flags += ["-d", paths.doctree, "-b", "html", paths.root, paths.html]

    # build always prints "index.html"
    if filename_only:
        print("index.html")
    
    return sphinx.main(flags)



def create_post(title, quiet=False, filename_only=False):
    '''
    Creates a new post with the given title.
    '''
    new_post = post.create(title)
    if filename_only:
        print(new_post.path)
    elif not quiet:
        print("")
        print("New post titled '%s' created as '%s'" % 
                (new_post.title, new_post.path))
        print("")
    

 
def create_page(title, quiet=False, filename_only=False):
    '''
    Creates a new page with the given title.
    '''
    new_page = page.create(title)
    if filename_only:
        print(new_page.path)
    elif not quiet:
        print("")
        print("New page titled '%s' craeted as '%s'" %
                (new_page.title, new_page.path))
        print("")



def main(argv=None):
    '''
    Parses command line and executes required action.
    '''
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--setup", action="store_true", help="setup a new blog")
    group.add_argument("-b", "--build", action="store_true", help="build blog")
    group.add_argument("-p", "--post", nargs=1, help="create a new post")
    group.add_argument("--page", nargs=1, help="create a new page")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q", "--quiet", action="store_true", help="quiet mode")
    group.add_argument("-f", "--filename", action="store_true", 
            help="output filename only - useful to pipe Tinkerer commands") 

    command = parser.parse_args(argv)
    if command.setup:
        setup(command.quiet, command.filename)
    elif command.build:
        build(command.quiet, command.filename)
    elif command.post:
        create_post(command.post[0], command.quiet, command.filename)
    elif command.page:
        create_page(command.page[0], command.quiet, command.filename)
    else:
        parser.print_help()

