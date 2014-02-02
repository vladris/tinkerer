'''
    utils
    ~~~~~

    Tinkerer utility functions.

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import imp
import os
import re


UNICODE_ALNUM_PTN = re.compile(r"[\W_]+", re.U)


def name_from_title(title):
    '''
    Returns a doc name from a title by replacing all groups of 
    characters which are not alphanumeric or '_' with the word 
    separator character.
    '''
    try:
        word_sep = get_conf().slug_word_separator
    except:
        word_sep = "_"

    return UNICODE_ALNUM_PTN.sub(word_sep, title
        ).lower().strip(word_sep)



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

    return "%04d" % date.year, "%02d" % date.month, "%02d" % date.day



def get_conf():
    '''
    Import conf.py from current directory.
    '''
    return imp.load_source("conf", "./conf.py")
