'''
    Tinkerer output
    ~~~~~~~~~~~~~~~

    Handles writing output

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import logging
import sys


# output writer
write = logging.getLogger("write")


# used in "filename only" mode
filename = logging.getLogger("filename")


# global quiet is used to pass -q to Sphinx build
quiet = False



def init(quiet_mode, filename_only):
    """
    Initialize output based on quiet/filename-only flags
    """
    global quiet

    # global quiet is used to pass -q to Sphinx build so it should be set when
    # either in quiet mode or filename-only mode
    quiet = quiet_mode or filename_only

    # always handle write as it also output all errors
    write.addHandler(logging.StreamHandler())

    if filename_only:
        # in filename-only mode, also handle filename and suppress other
        # messages below ERROR level
        filename.addHandler(logging.StreamHandler(sys.stdout))
        write.setLevel(logging.ERROR)
        filename.setLevel(logging.INFO)
    elif quiet:
        # in quiet mode, only display ERROR and above
        write.setLevel(logging.ERROR)
    else:
        # otherwise display INFO
        write.setLevel(logging.INFO)

