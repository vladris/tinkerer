'''
    Disqus Test
    ~~~~~~~~~~~

    Tests Disqus extension

    :copyright: Copyright 2011-2016 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
from tinkerer import post
from tinkerer.ext import disqus
from tinkertest import utils


# test case
class TestDisqus(utils.BaseTinkererTest):
    # test disqus extension
    def test_disqus(self):
        TEST_SHORTNAME = "test_shortname"

        # add disqus_shortname in conf.py
        utils.update_conf(
            {"disqus_shortname = None":
             'disqus_shortname = "%s"' % TEST_SHORTNAME})

        # create a post
        post.create("post1", datetime.date(2010, 10, 1))
        POST_ID = "2010/10/01/post1"
        POST_LINK = "http://127.0.0.1/blog/html/" + POST_ID + ".html"

        # build blog
        self.build()

        # ensure disqus script is added to html output
        output = os.path.join(utils.TEST_ROOT,
                              "blog", "html", "2010", "10", "01", "post1.html")
        output_html = open(output, "r").read()

        self.assertTrue(
            disqus.create_thread(TEST_SHORTNAME, POST_ID) in output_html)

        output = os.path.join(utils.TEST_ROOT,
                              "blog", "html", "index.html")
        output_html = open(output, "r").read()

        # ensure script to enable comment count is added to aggregated page
        self.assertTrue(
            disqus.enable_count(TEST_SHORTNAME) in output_html)

        # ensure comment count is added to aggregated page
        self.assertTrue(
            disqus.get_count(POST_LINK, POST_ID) in output_html)
