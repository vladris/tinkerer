'''
    draft
    ~~~~~

    Handles creating drafts.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENCE file
'''
import os
import re
import shutil
import tinkerer
from tinkerer import master, paths, utils, writer



def create(title):
    '''
    Creates a new post draft.
    '''
    name = utils.name_from_title(title)

    path = os.path.join(
                    utils.get_path(
                        paths.root, 
                        "drafts"), 
                    name + tinkerer.source_suffix)

    writer.render("post.rst", path,
            { "title"     : title,
              "content"   : "",
              "author"    : "default",
              "categories": "none",
              "tags"      : "none"})

    return path



def move(path):
    '''
    Demotes given file to draft.
    '''
    # get dirname and filename
    dirname, filename = os.path.split(path)

    # get docname without extension
    docname = os.path.splitext(filename)[0]

    draft = os.path.join(utils.get_path(paths.root, "drafts"), filename)

    # move file
    shutil.move(path, draft)

    # check if file is a post or a page
    if os.path.basename(dirname) == "pages":
        docname = "pages/" + docname
    else:
        match = re.match(r".*(?P<y>\d{4}).(?P<m>\d{2}).(?P<d>\d{2})$", dirname)
        if not match:
            return draft
        g = match.group
        docname = "/".join([g("y"), g("m"), g("d"), docname])

    # remove file from TOC
    master.remove_doc(docname)

    return draft
