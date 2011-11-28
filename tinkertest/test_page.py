'''
    Page Creation Test
    ~~~~~~~~~~~~~~~~~~

    Tests creating pages.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
from tinkerer import page
import tinkerer
import utils


# test creating new page
class TestPost(utils.BaseTinkererTest):
    # test create call
    def test_create(self):
        # create page
        new_page = page.create("My Page")

        self.assertEquals(
                os.path.abspath(os.path.join(
                                    utils.TEST_ROOT, 
                                    "pages", 
                                    "my_page.rst")),
                new_page.path)

        self.assertTrue(os.path.exists(new_page.path))


    # test updating master document
    def test_master_update(self):
        page.create("Page 1")
        page.create("Page 2")

        with open(tinkerer.paths.master_file, "r") as f:
            lines = f.readlines()

            self.assertEquals("   pages/page_1\n", lines[-2])
            self.assertEquals("   pages/page_2\n", lines[-1])


    # test content
    def test_content(self):
        new_page = page.create("My Page")

        # check expected empty page content
        with open(new_page.path) as f:
            self.assertEquals(f.readlines(),
                    ["My Page\n",
                     "=======\n"])

