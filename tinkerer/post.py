'''
    post
    ~~~~

    Handles creating new posts and inserting them in the master document.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENCE file
'''
from datetime import datetime
import os
import shutil
import tinkerer
from tinkerer import master, paths, utils, writer



class Post():
    '''
    The class provides methods to create a new post and insert it into the 
    master document.
    '''

    def __init__(self, title=None, path=None, date=None):
        '''
        Initializes a new post and creates path to it if it doesn't already
        exist.
        '''
        self.title = title

        # get year, month and day from date
        self.year, self.month, self.day = utils.split_date(date)

        # get name from path if specified, otherwise from title
        if path:
            self.name = utils.name_from_path(path)
        else:
            self.name = utils.name_from_title(title)

        # create post directory if it doesn't exist and get post path
        self.path = os.path.join(
                            utils.get_path(
                                    paths.root,
                                    self.year,
                                    self.month,
                                    self.day),
                            self.name) + tinkerer.source_suffix

        # docname as it should appear in TOC
        self.docname = "/".join([self.year, self.month, self.day, self.name])



    def write(self, content="", author="default", 
            categories="none", tags="none"):
        '''
        Writes the post template with given arguments.
        '''
        writer.render("post.rst", self.path,
               { "title"     : self.title,
                 "content"   : content,
                 "author"    : author,
                 "categories": categories,
                 "tags"      : tags})



def create(title, date=None):
    '''
    Creates a new post given its title.
    '''
    post = Post(title, path=None, date=date)
    post.write()
    master.prepend_doc(post.docname)
    return post



def move(path, date=None):
    '''
    Moves a post given its path.
    '''
    post = Post(title=None, path=path, date=date)
    shutil.move(path, post.path)
    master.prepend_doc(post.docname)
    return post

