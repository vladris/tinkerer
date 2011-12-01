'''
    Command Line Test
    ~~~~~~~~~~~~~~~~~

    Tests Tinkerer command line (setup, post, page and build)

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import datetime
import os
import tinkerer.cmdline
import unittest
import utils


# test tinkerer command line
class TestCmdLine(utils.BaseTinkererTest):
    # test blog setup
    def test_setup(self):
        # no need to do anything as blog is creat as part of test setup
        for item in os.listdir(utils.TEST_ROOT):
            self.assertIn(item, ["_static", "conf.py", "index.rst"])


    # test post
    def test_post(self):
        file_path = tinkerer.cmdline.post("My Test Post", datetime.date(2010, 10, 1))

        # assert correct file path was returned
        self.assertEquals(file_path, 
                os.path.abspath(
                        os.path.join(utils.TEST_ROOT, 
                                "2010", "10", "01", "my_test_post.rst")))

        # assert file exists
        self.assertTrue(os.path.exists(file_path))

        # check content
        with open(file_path, "r") as f:
            self.assertEquals(f.readlines(),
                    ["My Test Post\n",
                     "============\n",
                     "\n",
                     ".. tags:: none\n",
                     ".. comments::\n"])


    # test page
    def test_page(self):
        tinkerer.cmdline.page("My Test Page")

        file_path = os.path.join(utils.TEST_ROOT, "pages", "my_test_page.rst")

        # assert file exsits
        self.assertTrue(os.path.exists(file_path))

        # check content
        with open(file_path, "r") as f:
            self.assertEquals(f.readlines(),
                    ["My Test Page\n",
                     "============\n"])


    # test build
    def test_build(self):
        tinkerer.cmdline.post("My Post", datetime.date(2010, 10, 1))

        self.build()

        # assert html is produced
        self.assertTrue(os.path.exists(                
            os.path.join(utils.TEST_ROOT, "blog", "html", "2010", 
                         "10", "01", "my_post.html")))

