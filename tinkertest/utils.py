'''
    Test utilities
    ~~~~~~~~~~~~~~

    Base test case class inherited by all test cases. Utility functions.

    :copyright: Copyright 2011-2018 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import os
import shutil
import sys
from sphinx.cmd.build import main as build_main
from tinkerer import output, paths, writer
import types
import unittest


# test root directory
TEST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "root"))


# stored test instance to assert from extensions while running Sphinx build
test = None


# base tinkerer test case
class BaseTinkererTest(unittest.TestCase):
    # common setup
    def setUp(self):
        output.quiet = True
        setup()

    # invoke build
    def build(self, expected_return=0):
        print("")
        sys.argv = ["-q", "-d", paths.doctree, "-b",
                    "html", paths.root, paths.html]
        build_main(sys.argv)

    # common teardown - cleanup working directory
    def tearDown(self):
        cleanup()


# hook extension to conf.py
def hook_extension(ext):
    writer.write_conf_file(extensions=["tinkerer.ext.blog", ext])


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


# update conf.py given a dictionary of strings to replace (from -> to)
def update_conf(settings):
    conf_path = os.path.join(TEST_ROOT, "conf.py")
    conf_text = open(conf_path, "r").read()

    for setting in settings:
        conf_text = conf_text.replace(setting, settings[setting])

    open(conf_path, "w").write(conf_text)


# nose mistakenly calls Sphinx extension setup functions thinking they are
# test setups with a module parameter
def is_module(m):
    return isinstance(m, types.ModuleType)


# used by Sphinx to lookup extensions
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
