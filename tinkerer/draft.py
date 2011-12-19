'''
    draft
    ~~~~~

    Handles creating drafts.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENCE file
'''
import tinkerer
import os
from tinkerer import paths, utils, writer



def create(title):
    '''
    Creates a new post draft.
    '''
    name = utils.name_from_title(title)
    path = os.path.join(paths.root, "drafts", name + tinkerer.source_suffix)
    writer.render("post.rst", path,
            { "title"     : title,
              "content"   : "",
              "author"    : "default",
              "categories": "none",
              "tags"      : "none"})
    return path

