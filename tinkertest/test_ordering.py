'''
    Ordering Test
    ~~~~~~~~~~~~~

    Tests that Tinkerer adds posts and pages in the correct order

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import datetime
import unittest
import utils
import tinkerer
from tinkerer import page, post


# test case
class TestOrdering(utils.BaseTinkererTest):
    def test_ordering(self):
        utils.test = self

        # create some pages and posts 
        page.create("First Page")
        post.create("Oldest Post", datetime.date(2010, 10, 1))
        post.create("Newer Post", datetime.date(2010, 10, 1))
        page.create("Another Page")
        post.create("Newest Post", datetime.date(2010, 10, 1))

        utils.hook_extension("test_ordering")
        self.build()


ordering = {
    tinkerer.master_doc : [None, None, "2010/10/01/newest_post"],
    "2010/10/01/newest_post": [tinkerer.master_doc, tinkerer.master_doc, "2010/10/01/newer_post"],
    "2010/10/01/newer_post": [tinkerer.master_doc, "2010/10/01/newest_post", "2010/10/01/oldest_post"],
    "2010/10/01/oldest_post": [tinkerer.master_doc, "2010/10/01/newer_post", "pages/first_page"],
    "pages/first_page": [tinkerer.master_doc, "2010/10/01/oldest_post", "pages/another_page"],
    "pages/another_page": [tinkerer.master_doc, "pages/first_page", None]
}


# test ordering through extension
def build_finished(app, exception):
    env = app.builder.env

    # check post and pages have the correct relations
    relations = env.collect_relations()

    for docname in ordering:
        utils.test.assertEquals(relations[docname], ordering[docname])

    # check metadata ordering is correct
    utils.test.assertEquals([
            "2010/10/01/newest_post",
            "2010/10/01/newer_post",
            "2010/10/01/oldest_post"],
            env.blog_posts)

    utils.test.assertEquals([
            "pages/first_page",
            "pages/another_page"],
            env.blog_pages)


# extension setup    
def setup(app):
    app.connect("build-finished", build_finished)
