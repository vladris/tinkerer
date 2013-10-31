'''
    Tinkerer command line
    ~~~~~~~~~~~~~~~~~~~~~

    Automates the following blog operations:

    setup - to create a new blog
    build - to clean build blog
    post - to create a new post
    page - to create a new page
    serve - to serve the blog locally for testing

    :copyright: Copyright 2011-2013 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import argparse
from datetime import datetime
import os
import shutil
import sphinx
import tinkerer
from tinkerer import draft, output, page, paths, post, writer, server



def setup():
    '''
    Sets up a new blog in the current directory.
    '''
    # it is a new blog if conf.py doesn't already exist
    new_blog = writer.setup_blog()

    output.filename.info("conf.py")
    if new_blog:
        output.write.info("Your new blog is almost ready!")
        output.write.info("You just need to edit a couple of lines in %s" % (os.path.relpath(paths.conf_file), ))
    else:
        output.write.info("Done")



def build():
    '''
    Runs a clean Sphinx build of the blog.
    '''
    # clean build directory
    if os.path.exists(paths.blog):
        shutil.rmtree(paths.blog)

    flags = ["sphinx-build"]
    # silence Sphinx if in quiet mode
    if output.quiet:
        flags.append("-q")
    flags += ["-d", paths.doctree, "-b", "html", paths.root, paths.html]

    # build always prints "index.html"
    output.filename.info("index.html")

    # copy some extra files to the output directory
    if os.path.exists("_copy"):
        shutil.copytree("_copy/", paths.html)

    return sphinx.main(flags)



def create_post(title, date=None, word_sep='_'):
    '''
    Creates a new post with the given title or makes an existing file a post.
    '''
    move = os.path.exists(title)

    if move:
        new_post = post.move(title, date)
    else:
        new_post = post.create(title, date, word_sep=word_sep)

    output.filename.info(new_post.path)
    if move:
        output.write.info("Draft moved to post '%s'" % new_post.path)
    else:
        output.write.info("New post created as '%s'" % new_post.path)



def create_page(title, word_sep='_'):
    '''
    Creates a new page with the given title or makes an existing file a page.
    '''
    move = os.path.exists(title)

    if move:
        new_page = page.move(title)
    else:
        new_page = page.create(title, word_sep=word_sep)

    output.filename.info(new_page.path)
    if move:
        output.write.info("Draft moved to page '%s'" % new_page.path)
    else:
        output.write.info("New page created as '%s'" % new_page.path)



def create_draft(title, word_sep='_'):
    '''
    Creates a new draft with the given title or makes an existing file a draft.
    '''
    move = os.path.exists(title)

    if move:
        new_draft = draft.move(title)
    else:
        new_draft = draft.create(title, word_sep=word_sep)

    output.filename.info(new_draft)
    if move:
        output.write.info("File moved to draft '%s'" % new_draft)
    else:
        output.write.info("New draft created as '%s'" % new_draft)



def preview_draft(draft_file):
    '''
    Rebuilds the blog, including the given draft.
    '''
    if not os.path.exists(draft_file):
        raise Exception("Draft named '%s' does not exist" % draft_file)

    # promote draft
    preview_post = post.move(draft_file)

    try:
        # rebuild
        result = build()
    finally:
        # demote post back to draft
        draft.move(preview_post.path)

    return result



def serve_blog(port):
    '''
    Serve the blog at http://localhost:8000 for local debugging purposes.
    '''
    output.write.info("Serving your blog at %s:%i. Use Ctrl-C to shut down the server." % ('127.0.0.1', port))

    # serve the blog for review
    server.serve(port)
    
    output.write.info("Shutting down the server based on user input.\nFinished.")




def main(argv=None):
    '''
    Parses command line and executes required action.
    '''
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--setup", action="store_true", help="setup a new blog")
    group.add_argument("-b", "--build", action="store_true", help="build blog")
    group.add_argument("-p", "--post", nargs=1,
            help="create a new post with the title POST (if a file named POST "
                 "exists, it is moved to a new post instead)")
    group.add_argument("--page", nargs=1,
            help="create a new page with the title PAGE (if a file named PAGE "
                 "exists, it is moved to a new page instead)")
    group.add_argument("-d", "--draft", nargs=1,
            help="creates a new draft with the title DRAFT (if a file named DRAFT "
                 "exists, it is moved to a new draft instead)")
    group.add_argument("--preview", nargs=1,
            help="rebuilds the blog, including the draft PREVIEW, without permanently "
                 "promoting the draft to a post")
    group.add_argument("-S", "--serve", nargs='?', const=8000, default=8000,
            type=int, metavar='PORT', help="serve blog locally for review at "
            "http://localhost:PORT (default: %(default)i)")
    group.add_argument("-v", "--version", action="store_true",
            help="display version information")

    parser.add_argument("--date", nargs=1,
            help="optionally specify a date as 'YYYY/mm/dd' for the post, useful when "
                 " migrating blogs; can only be used together with -p/--post")

    parser.add_argument("--word-sep-dash", action="store_true",
            help="when making page and post names, separate words with dashes instead of underscores")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q", "--quiet", action="store_true", help="quiet mode")
    group.add_argument("-f", "--filename", action="store_true",
            help="output filename only - useful to pipe Tinkerer commands")

    command = parser.parse_args(argv)

    output.init(command.quiet, command.filename)

    # tinkerer should be run from the blog root unless in setup mode or -v
    if not command.setup and not command.version and not os.path.exists(paths.conf_file):
        output.write.error("Tinkerer must be run from your blog root "
                    "(directory containing 'conf.py')")
        return -1

    post_date = None
    if command.date:
        # --date only works with --post
        if not command.post:
            output.write.error("Can only use --date with -p/--post.")
            return -1

        try:
            post_date = datetime.strptime(command.date[0], "%Y/%m/%d")
        except:
            output.write.error("Invalid post date: format should be YYYY/mm/dd")
            return -1
    
    word_sep = "_"
    if command.word_sep_dash:
        word_sep = '-'

    if command.setup:
        setup()
    elif command.build:
        return build()
    elif command.post:
        create_post(command.post[0], post_date, word_sep=word_sep)
    elif command.page:
        create_page(command.page[0], word_sep=word_sep)
    elif command.draft:
        create_draft(command.draft[0], word_sep=word_sep)
    elif command.preview:
        preview_draft(command.preview[0])
    elif command.serve:
        serve_blog(command.serve)
    elif command.version:
        output.write.info("Tinkerer version %s" % tinkerer.__version__)
    else:
        parser.print_help()

    return 0
