'''
    Command Line Test
    ~~~~~~~~~~~~~~~~~

    Tests Tinkerer command line (setup, post, page and build)

    :copyright: Copyright 2011-2013 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import logging
import os
import tinkerer
from tinkerer import cmdline, paths, post
from tinkertest import utils


# test tinkerer command line
class TestCmdLine(utils.BaseTinkererTest):
    # these tests cause lots of output, disable logging while they are running
    def setUp(self):
        logging.disable(logging.CRITICAL)
        utils.setup()


    # re-enable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)
        utils.cleanup()


    # test blog setup
    def test_setup(self):
        # blog is setup as part of test setup, tear it down and re-create it via
        # cmdline
        self.tearDown()
        cmdline.main(["--setup", "--quiet"])

        self.assertEqual(
            set(os.listdir(utils.TEST_ROOT)),
            set([
                "_static",
                "_templates",
                "drafts",
                "conf.py",
                "index.html",
                tinkerer.master_doc + ".rst"
            ]))


    # test post from title
    def test_post_from_title(self):
        cmdline.main(["--post", "My Test Post", "--quiet"])

        # this might fail at midnight :P
        year, month, day = tinkerer.utils.split_date()

        file_path = os.path.join(utils.TEST_ROOT, year, month, day, "my_test_post.rst")

        # assert file exists
        self.assertTrue(os.path.exists(file_path))


    # test post from existing file
    def test_post_from_path(self):
        # create file
        draft_file = os.path.join(utils.TEST_ROOT, "drafts", "draft_post.rst")

        with open(draft_file, "w") as f:
            f.write("Content")

        cmdline.main(["--post", draft_file, "--quiet"])

        # this might also fail at midnight :P
        year, month, day = tinkerer.utils.split_date()

        file_path = os.path.join(utils.TEST_ROOT, year, month, day, "draft_post.rst")

        # assert file exists and check content
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "r") as f:
            self.assertEquals("Content", f.read())


    # test post with explicit date
    def test_post_with_date(self):
        cmdline.main(["--post", "Dated Post", "--date", "2011/11/20"])

        file_path = os.path.join(utils.TEST_ROOT, "2011/11/20", "dated_post.rst")

        # assert file exists
        self.assertTrue(os.path.exists(file_path))


    # test date is only allowed with post argument
    def test_date_only_on_post(self):
        self.assertNotEqual(0,
                cmdline.main(["--page", "Test Page", "--date", "2011/11/20"]))

        self.assertNotEqual(0,
                cmdline.main(["--draft", "Test Draft", "--date", "2011/11/20"]))

        self.assertNotEqual(0,
                cmdline.main(["--build", "--date", "2011/11/20"]))

        self.assertNotEqual(0,
                cmdline.main(["--serve", "--date", "2011/11/20"]))


    # test page from title
    def test_page_from_title(self):
        cmdline.main(["--page", "My Test Page", "--quiet"])

        file_path = os.path.join(utils.TEST_ROOT, "pages", "my_test_page.rst")

        # assert file exsits
        self.assertTrue(os.path.exists(file_path))


    # test page from existing file
    def test_post_from_path(self):
        # create file
        draft_file = os.path.join(utils.TEST_ROOT, "drafts", "draft_page.rst")

        with open(draft_file, "w") as f:
            f.write("Content")

        cmdline.main(["--page", draft_file, "--quiet"])

        file_path = os.path.join(utils.TEST_ROOT, "pages", "draft_page.rst")

        # assert file exists and check content
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "r") as f:
            self.assertEquals("Content", f.read())


    # test draft
    def test_draft(self):
        cmdline.main(["--draft", "My Draft", "--quiet"])

        file_path = os.path.join(utils.TEST_ROOT, "drafts", "my_draft.rst")

        # assert draft was created
        self.assertTrue(os.path.exists(file_path))


    # test build
    def test_build(self):
        # create a new post
        new_post = post.create("My Post", datetime.date(2010, 10, 1))

        self.build()

        # assert html is produced
        self.assertTrue(os.path.exists(
            os.path.join(utils.TEST_ROOT, "blog", "html", "2010",
                         "10", "01", "my_post.html")))


    # ensure tinkerer only runs from blog root (dir containing conf.py) except
    # when running setup
    def test_root_only(self):
        # remove "conf.py" created by test setup
        os.remove(os.path.join(paths.root, "conf.py"))

        self.assertNotEqual(0,
                cmdline.main(["--page", "Test Post", "--quiet"]))

        self.assertNotEqual(0,
                cmdline.main(["--post", "Test Page", "--quiet"]))

        self.assertNotEqual(0,
                cmdline.main(["--build", "--quiet"]))

        self.assertNotEqual(0,
                cmdline.main(["--serve", "8000", "--quiet"]))

        # setup should work fine from anywhere
        self.assertEqual(0,
                cmdline.main(["--setup", "--quiet"]))

