'''
    draft
    ~~~~~

    Handles creating drafts.

    :copyright: Copyright 2011-2013 by Vlad Riscutia and contributors (see
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

    if os.path.exists(path):
        raise Exception("Draft '%s' already exists at '%s" %
                        (title, path)) 

    writer.render(paths.post_template, path,
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
    target_dir = utils.get_path(paths.root, "drafts")
    utils.move(path, target_dir)

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
