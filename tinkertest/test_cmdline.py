'''
    Command Line Test
    ~~~~~~~~~~~~~~~~~

    Tests Tinkerer command line (setup, post, page and build)

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
import tinkerer
from tinkerer import cmdline, post
import unittest
import utils


# test tinkerer command line
class TestCmdLine(utils.BaseTinkererTest):
    # test blog setup
    def test_setup(self):
        # blog is setup as part of test setup, tear it down and re-create it via 
        # cmdline
        self.tearDown()
        cmdline.main(["--setup", "--quiet"])

        self.assertEqual(
            set(os.listdir(utils.TEST_ROOT)),
            {"_static", "conf.py", "index.html", tinkerer.master_doc + ".rst"})


    # test post
    def test_post(self):
        cmdline.main(["--post", "My Test Post", "--quiet"])

        # this might fail at midnight :P
        year, month, day = tinkerer.utils.split_date()

        file_path = os.path.join(utils.TEST_ROOT, year, month, day, "my_test_post.rst")

        # assert file exists
        self.assertTrue(os.path.exists(file_path))


    # test page
    def test_page(self):
        cmdline.main(["--page", "My Test Page", "--quiet"])

        file_path = os.path.join(utils.TEST_ROOT, "pages", "my_test_page.rst")

        # assert file exsits
        self.assertTrue(os.path.exists(file_path))


    # test build
    def test_build(self):
        # create a new post
        new_post = post.create("My Post", datetime.date(2010, 10, 1))

        self.build()

        # assert html is produced
        self.assertTrue(os.path.exists(                
            os.path.join(utils.TEST_ROOT, "blog", "html", "2010", 
                         "10", "01", "my_post.html")))

