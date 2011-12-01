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
from tinkerer import cmdline, paths, writer
import unittest


# test root directory
TEST_ROOT = "root"


# stored test instance to assert from extensions while running Sphinx build
test = None


# base tinkerer test case
class BaseTinkererTest(unittest.TestCase):
    # common setup - use "root" working directory
    def setUp(self):
        if not os.path.exists(TEST_ROOT):
            os.mkdir(TEST_ROOT)

        paths.set_paths(TEST_ROOT)

        # setup blog
        writer.setup_blog()


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


# cleanup test directory
def cleanup():
    shutil.rmtree(TEST_ROOT)


# used by Sphinx to lookup extensions
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
