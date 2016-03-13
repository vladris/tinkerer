'''
    Tags Test
    ~~~~~~~~~

    Tests Tinkerer post tags.

    :copyright: Copyright 2011-2016 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
from tinkerer import paths, post
from tinkertest import utils


# test case
class TestTags(utils.BaseTinkererTest):
    def test_tags(self):
        utils.test = self

        # create some tagged posts
        for new_post in [("Post1", "tag #1"),
                         ("Post2", "tag #2"),
                         ("Post12", "tag #1, tag #2")]:
            p = post.create(new_post[0], datetime.date(2010, 10, 1))
            p.write(tags=new_post[1])

        utils.hook_extension("test_tags")
        self.build()


# test tags through extension
def build_finished(app, exception):
    blog_tags = app.builder.env.filing["tags"]

    # check collected tags
    utils.test.assertEquals(set(["tag #1", "tag #2"]), set(blog_tags))

    # check tagged posts
    for result in [(set(["2010/10/01/post1", "2010/10/01/post12"]), "tag #1"),
                   (set(["2010/10/01/post2", "2010/10/01/post12"]), "tag #2")]:
        utils.test.assertEquals(result[0], set(blog_tags[result[1]]))

    # check post metadata
    for result in [([("tag__1", "tag #1")], "2010/10/01/post1"),
                   ([("tag__2", "tag #2")], "2010/10/01/post2"),
                   ([("tag__1", "tag #1"), ("tag__2", "tag #2")],
                    "2010/10/01/post12")]:
        utils.test.assertEquals(
            result[0],
            app.builder.env.blog_metadata[result[1]].filing["tags"])

    # check tag pages were generated
    for page in ["tag__1.html", "tag__2.html"]:
        utils.test.assertTrue(os.path.exists(os.path.join(paths.html, "tags",
                                                          page)))


# extension setup
def setup(app):
    if utils.is_module(app):
        return
    app.connect("build-finished", build_finished)
