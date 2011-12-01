'''
    Post creator
    ~~~~~~~~~~~~

    Handles creating new posts and inserting them in the master document.

    :copyright: Copyright 2011 by Vlad Riscutia
'''
from datetime import datetime
import os
import tinkerer.paths
import tinkerer.utils
import tinkerer.writer


# post class
class Post():
    def __init__(self, title, date=None):
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


    # write post file
    def write(self, content="", tags="none"):
        tinkerer.writer.render("post.rst", self.path,
               { "title"  : self.title,
                 "content": content,
                 "tags"   : tags})


    # update master document by inserting new post
    # posts are always inserted at the top of the toc so latest post is first document
    def update_master(self):
        post = "   " + "/".join(
                [self.year, self.month, self.day, self.name]) + "\n"

        # load master file, insert post after "maxdepth" directive and rewrite the file
        with open(tinkerer.paths.master_file, "r") as f:
            lines = f.readlines()

        for line_no, line in enumerate(lines):
            if "maxdepth" in line:
                break
        lines.insert(line_no + 2, post)

        with open(tinkerer.paths.master_file, "w") as f:
            f.writelines(lines)


# creates a new post
def create(title, date=None):
    post = Post(title, date)
    post.write()
    post.update_master()
    return post

