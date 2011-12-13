'''
    Post Creation Test
    ~~~~~~~~~~~~~~~~~~

    Tests creating posts.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
from tinkerer import post
import tinkerer
import utils


# test creating new post
class TestPost(utils.BaseTinkererTest):
    # test create call
    def test_create(self):
        # create post with current date
        new_post = post.create("My Post")

        year, month, day = tinkerer.utils.split_date()
        self.assertEquals(year, new_post.year)
        self.assertEquals(month, new_post.month)
        self.assertEquals(day, new_post.day)

        self.assertEquals(
                os.path.abspath(os.path.join(
                                    utils.TEST_ROOT, 
                                    year, 
                                    month, 
                                    day, 
                                    "my_post.rst")),
                new_post.path)                                        

        self.assertTrue(os.path.exists(new_post.path))

        # create post with given date
        new_post = post.create("Date Post", datetime.date(2010, 10, 1))
        self.assertEquals("2010", new_post.year)
        self.assertEquals("10", new_post.month)
        self.assertEquals("01", new_post.day)

        self.assertEquals(
                os.path.abspath(os.path.join(
                                    utils.TEST_ROOT,
                                    "2010",
                                    "10",
                                    "01",
                                    "date_post.rst")),
                new_post.path)

        self.assertTrue(os.path.exists(new_post.path))


    # test updating master document
    def test_master_update(self):
        post.create("Post 1", datetime.date(2010, 10, 1))
        post.create("Post 2", datetime.date(2010, 11, 2))

        with open(tinkerer.paths.master_file, "r") as f:
            lines = f.readlines()

            for lineno, line in enumerate(lines):
                if "maxdepth" in line:
                    break

            self.assertEquals("\n", lines[lineno+1])
            self.assertEquals("   2010/11/02/post_2\n", lines[lineno+2])
            self.assertEquals("   2010/10/01/post_1\n", lines[lineno+3])
            self.assertEquals("\n", lines[lineno+4])


    # test content
    def test_content(self):
        # create post with no content
        new_post = post.create("My Post")

        year, month, day = tinkerer.utils.split_date()

        # check expected empty post content
        with open(new_post.path) as f:
            self.assertEquals(f.readlines(),
                    ["My Post\n",
                     "=======\n",
                     "\n",
                     "\n",
                     "\n",
                     ".. author:: default\n",
                     ".. categories:: none\n",
                     ".. tags:: none\n",
                     ".. comments::\n"])

        # update post
        new_post.write(author="Mr. Py", categories="category 1, category 2", 
                tags="tag 1, tag 2", content="Lorem ipsum")

        with open(new_post.path) as f:
            self.assertEquals(f.readlines(),
                    ["My Post\n",
                     "=======\n",
                     "\n",
                     "Lorem ipsum\n",
                     "\n",
                     ".. author:: Mr. Py\n",
                     ".. categories:: category 1, category 2\n",
                     ".. tags:: tag 1, tag 2\n",
                     ".. comments::\n"])


