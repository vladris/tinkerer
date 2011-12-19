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
class TestPage(utils.BaseTinkererTest):
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
        self.assertEquals("pages/my_page", new_page.docname)


    # test moving existing file
    def test_move(self):
        # create a "pre-existing" file
        draft_file = os.path.join(utils.TEST_ROOT, "drafts", "afile.rst")
        
        with open(draft_file, "w") as f:
            f.write("Content")

        # move file to page
        moved_page = page.move(draft_file)

        self.assertEquals(
                os.path.abspath(os.path.join(
                                    utils.TEST_ROOT,
                                    "pages",
                                    "afile.rst")),
                 moved_page.path)

        self.assertTrue(os.path.exists(moved_page.path))
        self.assertFalse(os.path.exists(draft_file))
        self.assertEquals("pages/afile", moved_page.docname)


    # test updating master document
    def test_master_update(self):
        page.create("Page 1")
        page.create("Page 2")

        with open(tinkerer.paths.master_file, "r") as f:
            lines = f.readlines()

            self.assertEquals("   pages/page_1\n", lines[-3])
            self.assertEquals("   pages/page_2\n", lines[-2])


    # test content
    def test_content(self):
        new_page = page.create("My Page")

        # check expected empty page content
        with open(new_page.path) as f:
            self.assertEquals(f.readlines(),
                    ["My Page\n",
                     "=======\n"])

