'''
    utils
    ~~~~~

    Tinkerer utility functions.

    :copyright: Copyright 2011-2013 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
import re
import shutil

from docutils.core import publish_doctree
from docutils.nodes import GenericNodeVisitor
import docutils.parsers.rst.directives


def name_from_title(title):
    '''
    Returns a doc name from a title by replacing all characters which are not
    alphanumeric or '_' with '_'.
    '''
    return re.sub(r"[\W_]", "_", title).lower()



def name_from_path(path):
    '''
    Returns a doc name from a path by extracting the filename without
    extension.
    '''
    return os.path.splitext(os.path.basename(path))[0]



def get_path(*args):
    '''
    Creates a path if it doesn't already exist.
    '''
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path)
    return path



def split_date(date=None):
    '''
    Splits a date into formatted year, month and day strings. If not date is
    provided, current date is used.
    '''
    if not date:
        date = datetime.datetime.today()

    return date.strftime("%Y/%m/%d").split("/")



# ============== About Move a Post ===============



def related_images(post_path):
    '''
    find all related images about the post, return images filename. 
    '''
    # reload for directive register re-initialize
    try:
        from imp import reload
    except ImportError:
        pass
    reload(docutils.parsers.rst.directives)

    class ImageExtractor(GenericNodeVisitor):
        def __init__(self, doctree):
            super().__init__(doctree)
            self.uris = set()

        def default_visit(self, node):
            if node.tagname == 'image':
                self.uris.add(node.get('uri'))
            return True

    # Read file
    with open(post_path, encoding = 'utf8') as f:
        string = f.read()

    # Parse file
    doctree = publish_doctree(string, settings_overrides = {'report_level': 5})
    ie = ImageExtractor(doctree)
    doctree.walk(ie)
    images = ie.uris # All images be used in reST

    # Remove "not in the same folder" images and empty filename
    images = [img for img in images if
         img and (os.path.dirname(img) == '' or os.path.dirname(img) == '.')]

    return images

def move(original_post, target_dir):
    '''
    Move a reST post to another folder, include images.
    '''
    original_dir, post_filename = os.path.split(original_post)

    # Get related images filename
    images = related_images(original_post)

    # Calc source and target position.
    here_and_there = [item for item in zip(
        [os.path.join(original_dir, img) for img in images],
        [os.path.join(target_dir, img) for img in images])]

    # Avoid overwrite or file lost.
    for here, there in here_and_there:
        if not os.path.exists(here):
            Exception('Attach image "%s" are not exist!' % here)
        elif os.path.exists(there):
            Exception('Image "%s" exists at "%s"!' %
                      (os.path.basename(there), target_dir))

    # Avoid ... for .reST file.
    target_post = os.path.join(target_dir, post_filename)
    if not os.path.exists(original_post):
        Exception('Post file are not exists!')
    elif os.path.exists(target_post):
        Exception('Post "%s" already exists at "%s"' % 
                  (post_filename, target_dir))

    # Real move
    here_and_there.append((original_post, target_post))
    for here, there in here_and_there:
        shutil.move(here, there)
