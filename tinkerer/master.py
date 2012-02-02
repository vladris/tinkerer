'''
    master
    ~~~~~~

    Handles updating the master document.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from tinkerer import paths



def read_master():
    '''
    Reads master file into a list.
    '''
    with open(paths.master_file, "r") as f:
        return f.readlines()



def write_master(lines):
    '''
    Overwrites master file with given lines.
    '''
    with open(paths.master_file, "w") as f:
        f.writelines(lines)



def prepend_doc(docname):
    '''
    Inserts document at the top of the TOC.
    '''
    lines = read_master()

    # find maxdepth directive
    for line_no, line in enumerate(lines):
        if "maxdepth" in line:
            break

    # insert docname after it with 3 space alignement
    lines.insert(line_no + 2, "   %s\n" % docname)
    
    write_master(lines)



def append_doc(docname):
    '''
    Appends document at the end of the TOC.
    '''
    lines = read_master()

    # find second blank line after maxdepth directive
    blank = 0    
    for line_no, line in enumerate(read_master()):
        if blank == 3: break
        if "maxdepth" in line: blank = 1
        if blank and line == "\n": blank += 1

    lines.insert(line_no, "   %s\n" % docname)

    write_master(lines) 
   
    
    
def remove_doc(docname):
    '''
    Removes document from the TOC.
    '''
    # rewrite file filtering line containing docname
    write_master(filter(
            lambda line: line != "   %s\n" % docname, 
            read_master()))
