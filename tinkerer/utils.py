'''
    utils
    ~~~~~

    Tinkerer utility functions.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
import re
import tinkerer



def filename_from_title(title):
    '''
    Returns a filename from a title by replacing all characters which are not
    alphanumeric or '_' with '_'.
    '''
    return re.sub(r"[\W_]", "_", title)



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
