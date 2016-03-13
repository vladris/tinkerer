'''
    Landing Page Test
    ~~~~~~~~~~~~~~~~~

    Tests landing page option.

    :copyright: Copyright 2011-2016 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import mock
import os
import sys
from tinkerer import page, post
from tinkertest import utils


# landing page name
LANDING_PAGE = "test_page"


class TestLandingPage(utils.BaseTinkererTest):
    # test using landing page option
    def test_landingpage(self):
        # set landing_page option in conf.py
        utils.update_conf(
            {"landing_page = None": 'landing_page = "%s"' % LANDING_PAGE})

        # create some posts
        for new_post in [("Post1", "Post2", "Post3")]:
            post.create(new_post[0]).write()

        # create the landing page
        page.create(LANDING_PAGE)

        self.build()

        # index.html should redirect to landing page
        self.assertTrue(
            '<meta http-equiv="REFRESH" content="0; url=./pages/%s.html" />'
            % LANDING_PAGE in self.__get_index_text())

        # there should be page1.html aggregated page
        self.assertTrue(
            os.path.exists(os.path.join(
                utils.TEST_ROOT,
                "blog",
                "html",
                "page1.html")))

    # not using landing page should not have redirect in index.html
    def test_nolandingpage(self):
        # create some posts
        for new_post in [("Post1", "Post2", "Post3")]:
            post.create(new_post[0]).write()

        # create the landing page
        page.create(LANDING_PAGE)

        self.build()

        # index.html should not redirect to landing page
        self.assertFalse(
            '<meta http-equiv="REFRESH" content="0; url=./pages/%s.html" />'
            % LANDING_PAGE in self.__get_index_text())

        # there should be no page1.html aggregated page
        self.assertFalse(
            os.path.exists(os.path.join(
                utils.TEST_ROOT,
                "blog",
                "html",
                "page1.html")))

    # missing landing page should fail build
    def test_missing(self):
        # set landing_page option in conf.py
        utils.update_conf(
            {"landing_page = None": 'landing_page = "%s"' % LANDING_PAGE})

        # create some posts
        for new_post in [("Post1", "Post2", "Post3")]:
            post.create(new_post[0]).write()

        # hide Sphinx stderr output for the extension exception
        with mock.patch.object(sys, "stderr"):
            # build should fail
            self.build(expected_return=1)

    # helper function to get content of index.html file
    def __get_index_text(self):
        index_path = os.path.join(utils.TEST_ROOT,
                                  "blog",
                                  "html",
                                  "index.html")
        return open(index_path, "r").read()
