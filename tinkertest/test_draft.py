'''
    Draft Creation Test
    ~~~~~~~~~~~~~~~~~~~

    Tests creating drafts.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import os
import tinkerer
from tinkerer import draft
import utils


# test creating drafts
class TestDraft(utils.BaseTinkererTest):
    # test create call
    def test_create(self):
        # create draft with given title
        new_draft = draft.create("My Draft")

        self.assertEquals(
                os.path.abspath(os.path.join(
                                    utils.TEST_ROOT, 
                                    "drafts", 
                                    "my_draft.rst")),
                new_draft)                                        

        self.assertTrue(os.path.exists(new_draft))


    # test content
    def test_content(self):
        # create draft with no content
        new_draft = draft.create("My Draft")

        # check expected empty post content
        with open(new_draft) as f:
            self.assertEquals(f.readlines(),
                    ["My Draft\n",
                     "========\n",
                     "\n",
                     "\n",
                     "\n",
                     ".. author:: default\n",
                     ".. categories:: none\n",
                     ".. tags:: none\n",
                     ".. comments::\n"])

