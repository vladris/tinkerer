'''
    Tags Test
    ~~~~~~~~~

    Tests Tinkerer post tags

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import datetime
import os
import unittest
import utils
import tinkerer.cmdline
import tinkerer.paths
import tinkerer.renderer


# test case
class TestTags(utils.BaseTinkererTest):
    def test_tags(self):
        utils.test = self

        # create some tagged posts
        self.retag_post("Post1", datetime.date(2010, 10, 1), "tag #1")
        self.retag_post("Post2", datetime.date(2010, 10, 1), "tag #2")
        self.retag_post("Post12", datetime.date(2010, 10, 1), "tag #1, tag #2")

        utils.hook_extension("test_tags")
        self.build()

    # use Tinkerer to add a post then re-render it with given tags
    def retag_post(self, title, timestamp, tag_string):
        post_path = tinkerer.cmdline.post(title, timestamp)
        tinkerer.renderer.render_post(post_path, title,
                tags=tag_string)


# test tags through extension
def build_finished(app, exception):
    blog_tags = app.builder.env.blog_tags

    # check collected tags
    utils.test.assertEquals({"tag #1", "tag #2"}, set(blog_tags))

    # check tagged posts
    utils.test.assertEquals({"2010/10/01/post1", "2010/10/01/post12"}, set(blog_tags["tag #1"]))
    utils.test.assertEquals({"2010/10/01/post2", "2010/10/01/post12"}, set(blog_tags["tag #2"]))

    # check post metadata
    metadata = app.builder.env.blog_metadata
    utils.test.assertEquals(["tag #1"], metadata["2010/10/01/post1"].tags)
    utils.test.assertEquals(["tag #2"], metadata["2010/10/01/post2"].tags)
    utils.test.assertEquals(["tag #1", "tag #2"], metadata["2010/10/01/post12"].tags)

    # check tag pages were generated
    for page in ["tag__1.html", "tag__2.html"]:
        utils.test.assertTrue(os.path.exists(os.path.join(tinkerer.paths.html,
            "tags", page)))


# extension setup
def setup(app):
    app.connect("build-finished", build_finished)
    
