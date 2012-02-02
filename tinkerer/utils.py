'''
    utils
    ~~~~~

    Tinkerer utility functions.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
import re
import tinkerer



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
