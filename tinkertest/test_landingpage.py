'''
    Landing Page Test
    ~~~~~~~~~~~~~~~~~

    Tests landing page option.

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import os

from tinkerer import page, post

from tinkertest import utils


class TestLandingPage(utils.BaseTinkererTest):
    # test using landing page option
    def test_landingpage(self):
        # landing page name
        LANDING_PAGE = "test_page"

        # set landing_page option in conf.py
        conf_path = os.path.join(utils.TEST_ROOT, "conf.py")
        conf_text = open(conf_path, "r").read()

        open(conf_path, "w").write(
            conf_text.replace("landing_page = None",
                              'landing_page = "%s"' % LANDING_PAGE))

        # create some posts
        for new_post in [("Post1", "Post2", "Post3")]:
            post.create(new_post[0]).write()

        # create the landing page
        page.create(LANDING_PAGE)

        self.build()

        index_path = os.path.join(utils.TEST_ROOT,
                                  "blog",
                                  "html",
                                  "index.html")
        index_text = open(index_path, "r").read()

        self.assertTrue(
            '<meta http-equiv="REFRESH" content="0; url=./pages/%s.html" />'
            % LANDING_PAGE in index_text)
