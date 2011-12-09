'''
    Metadata Test
    ~~~~~~~~~~~~~

    Tests metadata collected by Tinkerer during build.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import datetime
from tinkerer import page, paths, post
import utils


# test case
class TestMetadata(utils.BaseTinkererTest):
    def test_metadata(self):
        utils.test = self

        # create some posts
        for i in range(20):
            post.create("Post %d" % i, datetime.date(2010, 10, i + 1)).write(
                content=" ".join("a" * 100))

        # ... and some pages
        for i in range(10):
            page.create("Page %d" % i)

        utils.hook_extension("test_metadata")
        self.build()


# test metadata through extension
def build_finished(app, exception):
    env = app.builder.env

    # check posts were identified as such
    posts = ["2010/10/%02d/post_%d" % (i + 1, i) for i in range(20)]
    utils.test.assertEquals(set(posts), set(env.blog_posts))

    # check pages were identified as such
    pages = ["pages/page_%d" % i for i in range(10)]
    utils.test.assertEquals(set(pages), set(env.blog_pages))

    # body should contain the whole 100 word string
    utils.test.assertIn(" ".join("a" * 100), 
            env.blog_metadata[env.blog_posts[0]].body)


# extension setup
def setup(app):
    app.connect("build-finished", build_finished)
