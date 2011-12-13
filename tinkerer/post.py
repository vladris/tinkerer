'''
    Post creator
    ~~~~~~~~~~~~

    Handles creating new posts and inserting them in the master document.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENCE file
'''
from datetime import datetime
import os
import tinkerer.paths
import tinkerer.utils
import tinkerer.writer



class Post():
    '''
    The class provides methods to create a new post and insert it into the 
    master document.
    '''

    def __init__(self, title, date=None):
        '''
        Determines post filename based on title and creates the path to the
        post if it doesn't already exist.
        '''
        self.title = title

        # get year, month and day from date
        self.year, self.month, self.day = tinkerer.utils.split_date(date)

        # get post name from title
        self.name = tinkerer.utils.filename_from_title(title).lower()

        # create post directory if it doesn't exist and get post path
        self.path = os.path.join(
                            tinkerer.utils.get_path(
                                    tinkerer.paths.root,
                                    self.year,
                                    self.month,
                                    self.day),
                            self.name) + tinkerer.source_suffix



    def write(self, content="", author="default", 
            categories="none", tags="none"):
        '''
        Writes the post template with given arguments.
        '''
        tinkerer.writer.render("post.rst", self.path,
               { "title"     : self.title,
                 "content"   : content,
                 "author"    : author,
                 "categories": categories,
                 "tags"      : tags})



    def update_master(self):
        '''
        Updates master document by inserting the new post. Posts are always 
        inserted at the top of the toc so latest post is first document.
        '''
        post = "   " + "/".join(
                [self.year, self.month, self.day, self.name]) + "\n"

        # load master file, insert post after "maxdepth" directive and rewrite the file
        with open(tinkerer.paths.master_file, "r") as f:
            lines = f.readlines()

        # look for 'maxdepth' option and insert line 2 lines after it
        for line_no, line in enumerate(lines):
            if "maxdepth" in line:
                break
        lines.insert(line_no + 2, post)

        # rewrite file
        with open(tinkerer.paths.master_file, "w") as f:
            f.writelines(lines)


def create(title, date=None):
    '''
    Creates a new post given its title.
    '''
    post = Post(title, date)
    post.write()
    post.update_master()
    return post

