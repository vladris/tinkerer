'''
    Page creator
    ~~~~~~~~~~~~

    Handles creating new pages and inserting them in the master document.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import os
import tinkerer.paths
import tinkerer.utils
import tinkerer.writer


# page class
class Page():
    def __init__(self, title):
        self.title = title

        # get post name from title
        self.name = tinkerer.utils.filename_from_title(title).lower()

        # create page directory if it doesn't exist and get page path
        self.path = os.path.join(
                            tinkerer.utils.get_path(
                                tinkerer.paths.root, 
                                "pages"), 
                            self.name) + tinkerer.source_suffix


    # write page file
    def write(self):
        tinkerer.writer.render("page.rst", self.path,
                { "title": self.title })


    # update master document by inserting page
    # pages are always inserted at the bottom of the toc
    def update_master(self):
        # update toc root
        page = "   pages/" + self.name + "\n"

        # append page to master file
        with open(tinkerer.paths.master_file, "a") as f:
            f.write(page)
        

# create a new page
def create(title):
    page = Page(title)
    page.write()
    page.update_master()
    return page

