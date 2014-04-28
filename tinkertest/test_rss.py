'''
    RSS Generator Test
    ~~~~~~~~~~~~~~~~~~

    Tests the RSS feed generator.

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import email.utils
import os
import time
import xml.dom.minidom

from tinkerer import paths, post
from tinkerer.ext import rss

from tinkertest import utils

import mock


# get expected pubdate based on date
def expected_pubdate(year, month, day):
    return email.utils.formatdate(
                time.mktime(datetime.date(year, month, day).timetuple()),
                localtime=True)


# test case
class TestRSS(utils.BaseTinkererTest):
    def test_rss(self):
        # create some posts
        for new_post in [
                ("Post 1",
                    datetime.date(2010, 10, 1),
                    "Lorem ipsum",
                    "category 1"),
                ("Post 2",
                    datetime.date(2010, 11, 2),
                    "dolor sit",
                    "category 2"),
                ("Post 3",
                    datetime.date(2010, 12, 3),
                    "amet, consectetuer",
                    "category 3")]:
            post.create(new_post[0], new_post[1]).write(
                    content=new_post[2],
                    categories=new_post[3])

        self.build()

        feed_path = os.path.join(paths.html, "rss.html")

        # check feed was created
        self.assertTrue(os.path.exists(feed_path))

        # check feed content
        doc = xml.dom.minidom.parse(feed_path)
        doc = doc.getElementsByTagName("rss")[0].getElementsByTagName("channel")[0]

        # validate XML channel data against expected content
        data = {
                "title": None,
                "link": None,
                "description": None,
                "language": None,
                "pubDate": None
               }

        data = self.get_data(doc, data)

        self.assertEquals("My blog", data["title"])
        self.assertEquals("http://127.0.0.1/blog/html/", data["link"])
        self.assertEquals("Add intelligent tagline here", data["description"])
        self.assertEquals("en-us", data["language"])
        self.assertEquals(expected_pubdate(2010, 12, 3), data["pubDate"])

        # validate XML "item" node content against expected content
        data = {
                "link": None,
                "guid": None,
                "title": None,
                "description": None,
                "category": None,
                "pubDate": None
               }

        for item in [{"index": 0,
                      "link" : "http://127.0.0.1/blog/html/2010/12/03/post_3.html",
                      "title": "Post 3",
                      "description": "amet, consectetuer",
                      "category": "category 3",
                      "pubDate": expected_pubdate(2010, 12, 3)},

                     {"index": 1,
                      "link" : "http://127.0.0.1/blog/html/2010/11/02/post_2.html",
                      "title": "Post 2",
                      "description": "dolor sit",
                      "category": "category 2",
                      "pubDate": expected_pubdate(2010, 11, 2)},

                     {"index": 2,
                      "link" : "http://127.0.0.1/blog/html/2010/10/01/post_1.html",
                      "title": "Post 1",
                      "description": "Lorem ipsum",
                      "category": "category 1",
                      "pubDate": expected_pubdate(2010, 10, 1)}]:

            data = self.get_data(
                    doc.getElementsByTagName("item")[item["index"]], data)
            self.assertEquals(item["link"], data["link"])
            self.assertEquals(item["link"], data["guid"])
            self.assertEquals(item["title"], data["title"])
            self.assertTrue(item["description"] in data["description"])
            self.assertTrue(item["category"] in data["category"])
            self.assertEquals(item["pubDate"], data["pubDate"])



    # get a dictionary of the given data in an XML node
    def get_data(self, node, data):
        for child in data.keys():
            data[child] = node.getElementsByTagName(
                    child)[0].childNodes[0].nodeValue

        return data

    def test_empty_blog(self):
        # empty blog should not generate rss
        self.build()

        self.assertFalse(os.path.exists(os.path.join(paths.html, "rss.html")))


# Set up a fake app with some "blog posts" -- since we aren't
# going to process the posts, it doesn't matter what type of
# object we use.
class FauxConfig(object):
    rss_max_items = 0
    website = None
    project = 'faux project'
    tagline = 'faux tagline'


class FauxEnv(object):

    def __init__(self, num_posts=5):
        self.blog_posts = [
            'post %d' % i
            for i in range(num_posts)
        ]


class FauxBuilder(object):

    def __init__(self):
        self.env = FauxEnv()


class FauxApp(object):

    def __init__(self):
        self.builder = FauxBuilder()
        self.config = FauxConfig()


class TestRSSItemCount(utils.BaseTinkererTest):

    def setUp(self):
        super(utils.BaseTinkererTest, self).setUp()
        self.app = FauxApp()

    @mock.patch('tinkerer.ext.rss.make_feed_context')
    def test_more_posts_than_max(self, make_feed_context):
        self.app.config.rss_max_items = 1
        # Call the mocked function for creating the feed context and
        # verify the number of items it contains.
        list(rss.generate_feed(self.app))
        make_feed_context.assert_called_once_with(
            self.app,
            None,
            [self.app.builder.env.blog_posts[0]],
        )

    @mock.patch('tinkerer.ext.rss.make_feed_context')
    def test_fewer_posts_than_max(self, make_feed_context):
        self.app.config.rss_max_items = 10
        # Call the mocked function for creating the feed context and
        # verify the number of items it contains.
        list(rss.generate_feed(self.app))
        make_feed_context.assert_called_once_with(
            self.app,
            None,
            self.app.builder.env.blog_posts,
        )

    @mock.patch('tinkerer.ext.rss.make_feed_context')
    def test_same_posts_and_max(self, make_feed_context):
        self.app.config.rss_max_items = len(self.app.builder.env.blog_posts)
        # Call the mocked function for creating the feed context and
        # verify the number of items it contains.
        list(rss.generate_feed(self.app))
        make_feed_context.assert_called_once_with(
            self.app,
            None,
            self.app.builder.env.blog_posts,
        )

    @mock.patch('tinkerer.ext.rss.make_feed_context')
    def test_no_posts(self, make_feed_context):
        make_feed_context.side_effect = AssertionError('should not be called')
        self.app.builder.env.blog_posts = []
        list(rss.generate_feed(self.app))


class TestRSSTitle(utils.BaseTinkererTest):

    def setUp(self):
        super(utils.BaseTinkererTest, self).setUp()
        self.app = FauxApp()

    def test_with_title(self):
        context = rss.make_feed_context(self.app, 'title here', [])
        self.assertTrue('faux project' in context['title'])
        self.assertTrue('title here' in context['title'])

    def test_without_title(self):
        context = rss.make_feed_context(self.app, None, [])
        self.assertEqual('faux project', context['title'])
