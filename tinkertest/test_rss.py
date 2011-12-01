'''
    RSS Generator Test
    ~~~~~~~~~~~~~~~~~~

    Tests the RSS feed generator.

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import datetime
import os
import tinkerer.cmdline
import tinkerer.paths
import utils
import xml.dom.minidom


# test case
class TestRSS(utils.BaseTinkererTest):
    def test_rss(self):
        utils.test = self

        timestamp = datetime.date(2010, 10, 1)

        # create some posts
        for post in ["Post 1", "Post 2", "Post 3"]:
            tinkerer.cmdline.post(post, timestamp)

        self.build()

        feed_path = os.path.join(tinkerer.paths.html, "rss.html")

        # check feed was created
        self.assertTrue(os.path.exists(feed_path))

        # check feed content
        doc = xml.dom.minidom.parse(feed_path)

        # TODO: validate content
  
