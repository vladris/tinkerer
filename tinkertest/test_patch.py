'''
    Patch Test
    ~~~~~~~~~~

    Tests link patching on aggreated pages and RSS feed.

    :copyright: Copyright 2011-2016 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
import sys
from tinkerer import paths, post
from tinkertest import utils


# test case
class TestPatch(utils.BaseTinkererTest):

    def check_posts(self, filenames, posts, expected):
        # helper function which creates given list of files and posts, runs a
        # build, then ensures expected content exists in each file
        for filename in filenames:
            with open(os.path.join(paths.root, filename), "w") as f:
                f.write("content not important")

        # posts are tuples consisting of post title and content
        # all posts are created on 2010/10/1 as date is not relevant here
        for new_post in posts:
            post.create(new_post[0], datetime.date(2010, 10, 1)).write(
                content=new_post[1]
            )

        # build and check output
        self.build()

        # tests are tuples consisting of file path (as a list) and the list of
        # expected content
        for test in expected:
            with open(os.path.join(paths.html, *test[0]), "r") as f:
                content = f.read()
                for data in test[1]:
                    if data not in content:
                        print(data)
                        print(content)
                    self.assertTrue(data in content)

    def test_patch_a_and_img(self):
        filenames = ["img.png"]
        posts = [
            ("Post1", ":ref:`x`\n`Arch Linux <www.archlinux.org>`_"),
            ("Post2", ".. _x:\n\nX\n-\n.. image:: ../../../img.png")
        ]

        expected = [
            # Sphinx running on Python3 has an achor here, Python2 doesn't
            (["2010", "10", "01", "post1.html"],
             [('href="post2.html#x"' if sys.version_info[0] == 3 else
               'href="post2.html"'),
              'href="www.archlinux.org"']),

            # images get places in _images directory under root
            (["2010", "10", "01", "post2.html"],
             ['src="../../../_images/img.png"']),

            # index.html should have links patched with relative address
            (["index.html"],
             ['href="2010/10/01/post2.html#x"',
              'href="www.archlinux.org"',
              'src="_images/img.png"']),

            # RSS feed should have links patched with absolute address
            (["rss.html"],
             ['href="http://127.0.0.1/blog/html/2010/10/01/post2.html#x"',
              'href="www.archlinux.org"',
              'src="http://127.0.0.1/blog/html/_images/img.png"'])
        ]

        self.check_posts(filenames, posts, expected)

    def test_patch_target(self):
        # tests patching links for images with :target: specified
        filenames = ["img1.png", "img2.png", "img3.png"]

        posts = [
            ("Post1",
             # relative target
             ".. image:: ../../../img1.png\n"
             "   :target: ../../../_images/img1.png\n"
             "\n"
             # absolute target
             ".. image:: ../../../img2.png\n"
             "   :target: /_images/img2.png\n"
             "\n"
             # external target
             ".. image:: ../../../img3.png\n"
             "   :target: www.archlinux.org\n")
        ]

        expected = [
            (["2010", "10", "01", "post1.html"],
             [
                 # nothing should be changed
                 'href="../../../_images/img1.png"',
                 'href="/_images/img2.png"',
                 'href="www.archlinux.org"']),

            (["index.html"],
             [
                # relative target should get patched
                'href="_images/img1.png"',

                # absolute and external targets should be unchanged
                'href="/_images/img2.png"',
                'href="www.archlinux.org"']),
            (["rss.html"],
             [
                # relative and absolute targets should get patched
                'href="http://127.0.0.1/blog/html/_images/img1.png"',

                # absolute target doesn't get patched
                # 'href="http://127.0.0.1/_images/img2.png"',
                'href="www.archlinux.org"'])
        ]

        self.check_posts(filenames, posts, expected)

    def test_patch_bad_link(self):
        # post with an invalid link, which doesn't produce a proper <a> tag
        posts = [
            ("Post1",
             # bad link
             "`http://book.cakephp.org/3.0/en/appendices/3-0-migration-\n"
             "guide.html`_")
        ]

        expected = [
            (["2010", "10", "01", "post1.html"],
             [
                # should be marked as problematic by Sphinx
                '<a href="#id1"><span class="problematic" id="id2">'
                '`http://book.cakephp.org/3.0/en/appendices/3-0-migration-\n'
                'guide.html`_</span></a>'])
        ]

        self.check_posts([], posts, expected)
