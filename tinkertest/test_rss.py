'''
    RSS Generator Test
    ~~~~~~~~~~~~~~~~~~

    Tests the RSS feed generator.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
from tinkerer import paths, post
import utils
import string
import xml.dom.minidom


# test case
class TestRSS(utils.BaseTinkererTest):
    def test_rss(self):
        # create some posts
        for new_post in [("Post 1", datetime.date(2010, 10, 1), "Lorem ipsum"),
                         ("Post 2", datetime.date(2010, 11, 2), "dolor sit"),
                         ("Post 3", datetime.date(2010, 12, 3), "amet, consectetuer")]:
            post.create(new_post[0], new_post[1]).write(content=new_post[2])

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
        self.assertIn("03 Dec 2010", data["pubDate"])

        # validate XML "item" node content against expected content
        data = { 
                "link": None, 
                "guid": None, 
                "title": None, 
                "description": None, 
                "pubDate": None
               }

        for item in [{"index": 0,
                      "link" : "http://127.0.0.1/blog/html/2010/12/03/post_3.html",
                      "title": "Post 3",
                      "description": "amet, consectetuer",
                      "pubDate": "03 Dec 2010"},

                     {"index": 1,
                      "link" : "http://127.0.0.1/blog/html/2010/11/02/post_2.html",
                      "title": "Post 2",
                      "description": "dolor sit",
                      "pubDate": "02 Nov 2010"},
                        
                     {"index": 2,
                      "link" : "http://127.0.0.1/blog/html/2010/10/01/post_1.html",
                      "title": "Post 1",
                      "description": "Lorem ipsum",
                      "pubDate": "01 Oct 2010"}]:

            data = self.get_data(
                    doc.getElementsByTagName("item")[item["index"]], data)
            self.assertEquals(item["link"], data["link"])
            self.assertEquals(item["link"], data["guid"])
            self.assertEquals(item["title"], data["title"])
            self.assertIn(item["description"], data["description"])
            self.assertIn(item["pubDate"], data["pubDate"])


    # get a dictionary of the given data in an XML node
    def get_data(self, node, data):
        for child in data.keys():
            data[child] = node.getElementsByTagName(
                    child)[0].childNodes[0].nodeValue

        return data
