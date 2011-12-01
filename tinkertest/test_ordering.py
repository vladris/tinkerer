'''
    Ordering Test
    ~~~~~~~~~~~~~

    Tests that Tinkerer adds posts and pages in the correct order

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import datetime
import unittest
import utils
from tinkerer import page, post


# test case
class TestOrdering(utils.BaseTinkererTest):
    def test_ordering(self):
        utils.test = self

        # create some pages and posts 
        page.create("First Page")
        post.create("Oldest Post", datetime.date(2010, 10, 1))
        post.create("Newer Post", datetime.date(2010, 11, 2))
        page.create("Second Page")
        post.create("Newest Post", datetime.date(2010, 12, 3))

        utils.hook_extension("test_ordering")
        self.build()


ordering = {
    "index" : [None, None, "2010/12/03/newest_post"],
    "2010/12/03/newest_post": ["index", "index", "2010/11/02/newer_post"],
    "2010/11/02/newer_post": ["index", "2010/12/03/newest_post", "2010/10/01/oldest_post"],
    "2010/10/01/oldest_post": ["index", "2010/11/02/newer_post", "pages/first_page"],
    "pages/first_page": ["index", "2010/10/01/oldest_post", "pages/second_page"],
    "pages/second_page": ["index", "pages/first_page", None]
}


# test ordering through extension
def build_finished(app, exception):
    # check post and pages have the correct relations
    relations = app.builder.env.collect_relations()

    for docname in ordering:
        utils.test.assertEquals(relations[docname], ordering[docname])


# extension setup    
def setup(app):
    app.connect("build-finished", build_finished)
