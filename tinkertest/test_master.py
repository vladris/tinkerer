'''
    Master Document Update Test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests updating the master document.

    :copyright: Copyright 2011-2016 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from tinkerer import master
from tinkertest import utils


# test updating master document
class TestMaster(utils.BaseTinkererTest):
    # head and tail of master doc checked in each test
    MASTER_HEAD = [
        "Sitemap\n",
        "=======\n",
        "\n",
        ".. toctree::\n",
        "   :maxdepth: 1\n",
        "\n"]

    MASTER_TAIL = ["\n"]

    # validate master doc created by setup
    def test_setup(self):
        self.assertEquals(
            TestMaster.MASTER_HEAD + TestMaster.MASTER_TAIL,
            master.read_master())

    # test appending at the end of the TOC
    def test_append(self):
        new_docs = ["somewhere/somedoc", "anotherdoc"]

        master.append_doc(new_docs[0])

        # first doc should be appendend in the correct place
        self.assertEquals(
            TestMaster.MASTER_HEAD +
            ["   %s\n" % new_docs[0]] +
            TestMaster.MASTER_TAIL,
            master.read_master())

        master.append_doc(new_docs[1])

        # second doc should be appended in the correct place
        self.assertEquals(
            TestMaster.MASTER_HEAD +
            ["   %s\n" % new_docs[0], "   %s\n" % new_docs[1]] +
            TestMaster.MASTER_TAIL,
            master.read_master())

    # test prepending at the beginning of the TOC
    def test_prepend(self):
        new_docs = ["somewhere/somedoc", "anotherdoc"]

        # first doc should be prepended in the correct place
        master.prepend_doc(new_docs[0])

        self.assertEquals(
            TestMaster.MASTER_HEAD +
            ["   %s\n" % new_docs[0]] +
            TestMaster.MASTER_TAIL,
            master.read_master())

        master.prepend_doc(new_docs[1])

        # order should be second doc then first doc
        self.assertEquals(
            TestMaster.MASTER_HEAD +
            ["   %s\n" % new_docs[1], "   %s\n" % new_docs[0]] +
            TestMaster.MASTER_TAIL,
            master.read_master())

    # test removing from the TOC
    def test_remove(self):
        # append 4 docs
        new_docs = ["a", "b", "c", "d"]
        for doc in new_docs:
            master.append_doc(doc)

        # remove 3 of them while checking master each time
        for doc_to_remove in ["c", "b", "d"]:
            master.remove_doc(doc_to_remove)
            new_docs.remove(doc_to_remove)

            self.assertEquals(
                TestMaster.MASTER_HEAD +
                ["   %s\n" % doc for doc in new_docs] +
                TestMaster.MASTER_TAIL,
                master.read_master())
