'''
    Test utilities
    ~~~~~~~~~~~~~~

    Base test case class inherited by all test cases. Utility functions.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
import shutil
import sys
from tinkerer import cmdline, page, paths, post, writer
import unittest


# test root directory
TEST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "root"))


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


# load test content
def load_content():
    return open(os.path.join(
            os.path.dirname(__file__), "content", "lorem.rst")).read()


# build test blog with given theme
def build_theme(use_theme):
    # setup blog
    setup()

    # write conf file with given theme
    writer.write_conf_file(theme=use_theme)

    # load content
    lorem = load_content()

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


# benchmark build
def benchmark(post_count, iterations):
    print("Running benchmark with %d posts, %d iterations" % 
            (post_count, iterations))

    times = []

    # setup blog
    setup()

    # load content
    lorem = load_content()

    # create posts
    for i in range(post_count):
        post.create("Post %d" % i).write(
                tags="tag #%d" % i,
                content=lorem)

    for i in range(iterations):
        print("Iteration %d..." % i)

        start = datetime.datetime.now()
        cmdline.build(quiet=True)
        times.append(datetime.datetime.now() - start)

        print(times[-1])

    # cleanup test dir
    cleanup()

    print("Average time: %s" % (sum(times, datetime.timedelta(0)) / len(times)))


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
    if os.path.exists(TEST_ROOT):
        shutil.rmtree(TEST_ROOT)


# used by Sphinx to lookup extensions
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
