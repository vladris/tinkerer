'''
    Test Tags
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
        self.retag_post("Post1", datetime.date(2010, 10, 1), "tag1")
        self.retag_post("Post2", datetime.date(2010, 10, 1), "tag2")
        self.retag_post("Post12", datetime.date(2010, 10, 1), "tag1, tag2")

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
    utils.test.assertIn("tag1", blog_tags)
    utils.test.assertIn("tag2", blog_tags)
    utils.test.assertEquals(2, len(blog_tags))

    # check tagged posts
    utils.test.assertIn("2010/10/01/post1", blog_tags["tag1"])
    utils.test.assertIn("2010/10/01/post12", blog_tags["tag1"])
    utils.test.assertEquals(2, len(blog_tags["tag1"]))
    utils.test.assertIn("2010/10/01/post2", blog_tags["tag2"])
    utils.test.assertIn("2010/10/01/post12", blog_tags["tag2"])
    utils.test.assertEquals(2, len(blog_tags["tag2"]))

    # check post metadata
    metadata = app.builder.env.blog_metadata
    utils.test.assertEquals(["tag1"], metadata["2010/10/01/post1"].tags)
    utils.test.assertEquals(["tag2"], metadata["2010/10/01/post2"].tags)
    utils.test.assertEquals(["tag1", "tag2"], metadata["2010/10/01/post12"].tags)

    # check tag pages were generated
    utils.test.assertTrue(os.path.exists(os.path.join(tinkerer.paths.html,
        "tags", "tag1.html")))
    utils.test.assertTrue(os.path.exists(os.path.join(tinkerer.paths.html,
        "tags", "tag2.html")))

# extension setup
def setup(app):
    app.connect("build-finished", build_finished)
    
