'''
    Patch Test
    ~~~~~~~~~~

    Tests link patching on aggreated pages and RSS feed.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
from tinkerer import paths, post
from tinkertest import utils
import sys


# test case
class TestPatch(utils.BaseTinkererTest):
    def test_patch(self):
        # create an image file
        with open(os.path.join(paths.root, "img.png"), "w") as f:
            f.write("content not important")

        # write a couple of posts with following content:
        # 1 cross reference (link should get patched)
        # 1 external link (link should be unchanged)
        # 1 image (source should get patched)
        for new_post in [
                    ("Post1", ":ref:`x`\n`Arch Linux <www.archlinux.org>`_"),
                    ("Post2", ".. _x:\n\nX\n-\n.. image:: ../../../img.png")]:
            post.create(new_post[0], datetime.date(2010, 10, 1)).write(
                content= new_post[1])

        # build and check output
        self.build()

        # for some reason Sphinx on Python 3 creates different relative links:
        # Post1 referencing Post2 which is in same dir results in a href like
        # "../01/post2.html" while on Python 2 href is "post2.html"
        python3 = sys.version_info[0] == 3


        # validate output - each tuple represents a file and the list of 
        # strings expected in the file
        tests = [(["2010", "10", "01", "post1.html"], 
                    ['href="../01/post2.html#x"' if python3 else 
                                'href="post2.html"',
                     'href="www.archlinux.org"']),
                 (["2010", "10", "01", "post2.html"],
                    # images get places in _images directory under root
                    ['src="../../../_images/img.png"']),
                 (["index.html"],
                    # index.html should have links patched with relative address
                    ['href="2010/10/01/../01/post2.html#x"' if python3 else 
                                'href="2010/10/01/post2.html#x"',
                     'href="www.archlinux.org"',
                     'src="2010/10/01/../../../_images/img.png"']),
                 (["rss.html"],
                    # RSS feed should have links patched with absolute address
                    ['href="http://127.0.0.1/blog/html/2010/10/01/../01/post2.html#x' if python3 else
                                'href="http://127.0.0.1/blog/html/2010/10/01/post2.html#x"',
                     'href="www.archlinux.org"',
                     'src="http://127.0.0.1/blog/html/2010/10/01/../../../_images/img.png"'])]

        for test in tests:
            with open(os.path.join(paths.html, *test[0]), "r") as f:
                content = f.read()
                for data in test[1]:
                    self.assertIn(data, content)

