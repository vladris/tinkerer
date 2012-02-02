'''
    page
    ~~~~

    Handles creating new pages and inserting them in the master document.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import os
import shutil
import tinkerer
from tinkerer import master, paths, utils, writer



class Page():
    '''
    The class provides methods to create a new page and insert it into the
    master document.
    '''
    def __init__(self, title=None, path=None):
        '''
        Determines page filename based on title or given path and creates the 
        path to the page if it doesn't already exist.
        '''
        self.title = title

        # get name from path if specified, otherwise from title
        if path:
            self.name = utils.name_from_path(path)
        else:
            self.name = utils.name_from_title(title)

        # create page directory if it doesn't exist and get page path
        self.path = os.path.join(
                            utils.get_path(
                                paths.root, 
                                "pages"), 
                            self.name) + tinkerer.source_suffix

        # docname as it should appear in TOC
        self.docname = "pages/" + self.name


    def write(self):
        '''
        Writes the page template.
        '''
        writer.render("page.rst", self.path,
                { "title": self.title })



def create(title):
    '''
    Creates a new page given its title.
    '''
    page = Page(title, path=None)
    page.write()
    master.append_doc(page.docname)
    return page



def move(path, date=None):
    '''
    Moves a page given its path.
    '''
    page = Page(title=None, path=path)
    shutil.move(path, page.path)
    master.append_doc(page.docname)
    return page
