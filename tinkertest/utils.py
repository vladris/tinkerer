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
import tinkerer.cmdline
import tinkerer.paths
import tinkerer.renderer
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

        tinkerer.paths.set_paths(TEST_ROOT)

        # setup blog
        tinkerer.cmdline.setup(quiet=True)


    # invoke build
    def build(self):
        print("")
        self.assertEquals(0, tinkerer.cmdline.build(quiet=True))


    # common teardown - cleanup working directory
    def tearDown(self):
        shutil.rmtree(TEST_ROOT)


# hook extension to conf.py
def hook_extension(ext):
    tinkerer.renderer.render_conf_file(extensions=["tinkerer.ext.blog", ext])


# used by Sphinx to lookup extensions
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
