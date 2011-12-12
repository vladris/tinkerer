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


class Page():
    '''
    The class provides methods to create a new page and insert it into the
    master document.
    '''
    def __init__(self, title):
        '''
        Determines page filename based on title and creates the path to the
        page if it doesn't already exist.
        '''
        self.title = title

        # get post name from title
        self.name = tinkerer.utils.filename_from_title(title).lower()

        # create page directory if it doesn't exist and get page path
        self.path = os.path.join(
                            tinkerer.utils.get_path(
                                tinkerer.paths.root, 
                                "pages"), 
                            self.name) + tinkerer.source_suffix



    def write(self):
        '''
        Writes the page template.
        '''
        tinkerer.writer.render("page.rst", self.path,
                { "title": self.title })


    # update master document by inserting page
    # pages are always inserted at the bottom of the toc
    def update_master(self):
        '''
        Updates the master document by appending the new page at the end of the 
        file. This should become the last item in the toc, thus the last 
        document.
        '''
        page = "   pages/" + self.name + "\n"

        # append page to master file
        with open(tinkerer.paths.master_file, "a") as f:
            f.write(page)
        


def create(title):
    '''
    Creates a new page given its title.
    '''
    page = Page(title)
    page.write()
    page.update_master()
    return page

