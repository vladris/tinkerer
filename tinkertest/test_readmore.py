'''
    ReadMore Directive Test 
    ~~~~~~~~~~~~~~~~~~~~~~~

    Tests readmore directive.

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
from tinkerer import cmdline, draft, master, page, post
from tinkertest import utils


# test readmore directive
class TestReadMore(utils.BaseTinkererTest):
    def test_readmore(self):
        post.create("Post1", datetime.date(2010, 10, 1)).write(
            content="Text\n\n.. more::\n\nMore text")

        self.build()

        post_path = os.path.join(
            utils.TEST_ROOT, "blog", "html", "2010", "10", "01", "Post1.html")
        post_html = open(post_path, "r").read()

        # ensure readmore div is added to post
        self.assertTrue('<div id="more"> </div>' in post_html)

        # ensure readmore is patched in aggregated page
        index_path = os.path.join(
            utils.TEST_ROOT, "blog", "html", "index.html")
        index_html = open(index_path, "r").read()

        self.assertTrue(
            '<p class="readmorewrapper"><a class="readmore"'
            ' href="2010/10/01/post1.html#more">Read more...</a></p>' in index_html)
        
        
