'''
    Test utilities
    ~~~~~~~~~~~~~~

    Base test case class inherited by all test cases. Utility functions.

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import datetime
import os
import shutil
import sys
from tinkerer import cmdline, page, paths, post, writer
import unittest


# test root directory
TEST_ROOT = "root"


# stored test instance to assert from extensions while running Sphinx build
test = None


# base tinkerer test case
class BaseTinkererTest(unittest.TestCase):
    # common setup
    def setUp(self):
        setup()


    # invoke build
    def build(self):
        print("")
        self.assertEquals(0, cmdline.build(quiet=True))


    # common teardown - cleanup working directory
    def tearDown(self):
        cleanup()


# hook extension to conf.py
def hook_extension(ext):
    writer.write_conf_file(extensions=["tinkerer.ext.blog", ext])


# build test blog with given theme
def build_theme(use_theme):
    # setup blog
    setup()

    # write conf file with given theme
    writer.write_conf_file(theme=use_theme)

    # load content
    lorem = open(os.path.join(
                os.path.dirname(__file__), "content", "lorem.rst")).read()

    # create posts
    post.create("This is a post", datetime.date(2010, 10, 1)).write(
            tags="tag #1, tag #2",
            content=lorem)
    post.create("This is another post", datetime.date(2010, 11, 2)).write(
            tags="tag #1",
            content=lorem)
    post.create("This is yet another post", datetime.date(2010, 12, 3)).write(
            tags="tag #2",
            content=lorem)

    # create pages
    page.create("First page").write()
    page.create("Second page").write()

    # build
    cmdline.build(quiet=True)



# setup blog using TEST_ROOT working directory
def setup():
    # create path
    if not os.path.exists(TEST_ROOT):
        os.mkdir(TEST_ROOT)

    paths.set_paths(TEST_ROOT)

    # setup blog
    writer.setup_blog()


# cleanup test directory
def cleanup():
    shutil.rmtree(TEST_ROOT)


# used by Sphinx to lookup extensions
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
