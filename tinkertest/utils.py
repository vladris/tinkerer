'''
    Test utilities
    ~~~~~~~~~~~~~~

    Base test case class inherited by all test cases. Utility functions.

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import mock
import os
import shutil
import sys
from tinkerer import cmdline, output, paths, writer
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
    def build(self):
        print("")

        with mock.patch.object(sys, 'exit') as mock_exit:
            cmdline.build()
            mock_exit.assert_called_once_with(0)

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


# nose mistakenly calls Sphinx extension setup functions thinking they are
# test setups with a module parameter
def is_module(m):
    return isinstance(m, types.ModuleType)


# used by Sphinx to lookup extensions
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
