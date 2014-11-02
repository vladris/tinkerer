'''
    Landing Page Test
    ~~~~~~~~~~~~~~~~~

    Tests landing page option.

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import mock
import os
import sys
from tinkerer import page, post
from tinkertest import utils


# landing page name
FIRST_PAGE_TITLE = "test_first_page"


class TestFirstPageTitle(utils.BaseTinkererTest):
    # test using conf.py option
    def test_firstpagetitle(self):
        utils.update_conf(
            {"first_page_title = None": 'first_page_title = "%s"' % 
            FIRST_PAGE_TITLE})

        # create a post
        post.create("Post1").write()

        self.build()

        index_path = os.path.join(utils.TEST_ROOT,
                                  "blog",
                                  "html",
                                  "index.html")
        index_text = open(index_path, "r").read()

        # index.html should contain the title
        self.assertTrue(
            '<a href="#">%s</a>' % FIRST_PAGE_TITLE in index_text)
