'''
    Draft Creation Test
    ~~~~~~~~~~~~~~~~~~~

    Tests creating drafts.

    :copyright: Copyright 2011-2016 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import mock
import os
from tinkerer import cmdline, draft, master, page, paths, post
from tinkertest import utils


# test creating drafts
class TestDraft(utils.BaseTinkererTest):
    # test creating draft from title
    def test_create(self):
        # create draft with given title
        new_draft = draft.create("My Draft")

        self.assertEquals(
            os.path.abspath(os.path.join(
                utils.TEST_ROOT,
                "drafts",
                "my_draft.rst")),
            new_draft)

        self.assertTrue(os.path.exists(new_draft))

    # test moving draft from existing files
    def test_move(self):
        # create a post and a page
        new_post = post.create("A post", datetime.datetime(2010, 10, 1))
        new_page = page.create("A page")

        # page and posts should be in master doc (precondition)
        lines = master.read_master()
        self.assertTrue("   %s\n" % new_post.docname in lines)
        self.assertTrue("   %s\n" % new_page.docname in lines)

        new_draft = draft.move(os.path.join(
            utils.TEST_ROOT, "pages", "a_page.rst"))
        self.assertTrue(os.path.exists(new_draft))

        # page should no longer be in TOC
        lines = master.read_master()
        self.assertTrue("   %s\n" % new_post.docname in lines)
        self.assertFalse("   %s\n" % new_page.docname in lines)

        new_draft = draft.move(os.path.join(
            utils.TEST_ROOT, "2010", "10", "01", "a_post.rst"))
        self.assertTrue(os.path.exists(new_draft))

        # post should no longer be in TOC either
        lines = master.read_master()
        self.assertFalse("   %s\n" % new_post.docname in lines)
        self.assertFalse("   %s\n" % new_page.docname in lines)

    # test draft preview
    def test_preview(self):
        # create a post
        new_post = post.create("A post", datetime.datetime(2010, 10, 1))

        # post should be in master doc (precondition)
        lines = master.read_master()
        self.assertTrue("   %s\n" % new_post.docname in lines)

        # create a draft
        new_draft = draft.create("draft")
        self.assertTrue(os.path.exists(new_draft))

        # preview it (build should succeed)
        self.assertEquals(0, cmdline.main(["--preview", new_draft, "-q"]))

        # draft should not be in TOC
        for line in master.read_master():
            self.assertFalse("draft" in line)

    # test content
    def test_content(self):
        # create draft with no content
        new_draft = draft.create("My Draft")

        # check expected empty post content
        with open(new_draft) as f:
            self.assertEquals(
                f.readlines(),
                ["My Draft\n",
                 "========\n",
                 "\n",
                 "\n",
                 "\n",
                 ".. author:: default\n",
                 ".. categories:: none\n",
                 ".. tags:: none\n",
                 ".. comments::\n"])

    @mock.patch('tinkerer.writer.render')
    def test_create_without_template(self, render):
        draft.create('no-template')
        render.assert_called_once_with(
            paths.post_template,
            mock.ANY,
            mock.ANY,
        )

    @mock.patch('tinkerer.writer.render')
    def test_create_with_template(self, render):
        draft.create('with-template', template='the_template.rst')
        render.assert_called_once_with(
            'the_template.rst',
            mock.ANY,
            mock.ANY,
        )
