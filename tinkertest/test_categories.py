'''
    Categories Test
    ~~~~~~~~~~~~~~~

    Tests Tinkerer post categoires.

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
from tinkerer import paths, post
from tinkertest import utils


# test case
class TestCategories(utils.BaseTinkererTest):
    def test_categories(self):
        utils.test = self

        # create some posts with categories

        # missing category for Post1 ("cateogry #1,") should work,
        # just issue a warning
        for new_post in [("Post1", "category #1,"),
                         ("Post2", "category #2"),
                         ("Post12", "category #1, category #2")]:
            post.create(new_post[0], datetime.date(2010, 10, 1)).write(
                categories=new_post[1])

        utils.hook_extension("test_categories")
        self.build()


# test categories through extension
def build_finished(app, exception):
    blog_categories = app.builder.env.filing["categories"]

    # check collected categories
    utils.test.assertEquals(set(["category #1", "category #2"]),
                            set(blog_categories))

    # check categories
    for result in [(set(["2010/10/01/post1", "2010/10/01/post12"]),
                    "category #1"),
                   (set(["2010/10/01/post2", "2010/10/01/post12"]),
                    "category #2")]:
        utils.test.assertEquals(result[0], set(blog_categories[result[1]]))

    # check post metadata
    for result in [([("category__1", "category #1")], "2010/10/01/post1"),
                   ([("category__2", "category #2")], "2010/10/01/post2"),
                   ([("category__1", "category #1"),
                     ("category__2", "category #2")], "2010/10/01/post12")]:
        utils.test.assertEquals(
            result[0],
            app.builder.env.blog_metadata[result[1]].filing["categories"])

    # check category pages were generated
    for page in ["category__1.html", "category__2.html"]:
        utils.test.assertTrue(os.path.exists(os.path.join(paths.html,
                                                          "categories",
                                                          page)))


# extension setup
def setup(app):
    if utils.is_module(app):
        return
    app.connect("build-finished", build_finished)
