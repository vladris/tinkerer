'''
    Build utility for Tinkerer blog
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Builds the blog with all themes and either generates the theme previews or
    opens each theme in the browser.

    :copyright: Copyright 2011-2016 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import argparse
import os
import shutil
import sys
from tinkerer import cmdline



DEFAULT_THEME = "flat"

OTHER_THEMES = ["modern5", "minimal5", "responsive", "dark"]



def update_conf(theme):
    '''
    Updates conf.py with the given theme
    '''
    CONF = "conf.py"

    lines = open(CONF).readlines()
    lines = ["html_theme = '%s'\n" % (theme, ) if "html_theme =" in line
                else line for line in lines]
    open(CONF, "w").writelines(lines)



def update_index(theme):
    '''
    Updates index_<THEME>.hml files to point to the correct static dir
    '''
    index = os.path.join("blog", "html", "index_%s.html" % (theme,))

    text = open(index, encoding="utf-8").read()
    text = text.replace("_static", "_static_%s" % (theme, ))

    open(index, "w").write(text)



def move_theme(theme):
    '''
    Moves the build output of the given theme
    '''
    src = os.path.join("blog", "html")
    dest = os.path.join("themes", theme)

    print("Moving %s to %s" % (src, dest))
    shutil.move(src, dest)



def open_all():
    '''
    Opens all themes in browser
    '''
    for theme in OTHER_THEMES:
        os.startfile(os.path.join("themes", theme, "index.html"))
    os.startfile("index.html")



def copy_previews():
    '''
    Copies themes to preview directory for Tinkerer website
    '''
    for theme in OTHER_THEMES:
        shutil.move(
            os.path.join("themes", theme, "index.html"), 
            os.path.join("blog", "html", "index_%s.html" % (theme, )))
        shutil.move(
            os.path.join("themes", theme, "_static"),
            os.path.join("blog", "html", "_static_%s" % (theme, )))
        update_index(theme)       



def parse(argv):
    '''
    Parses command line arguments
    '''
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-o", "--open", action="store_true", 
        help="open all themes in browser")
    group.add_argument("-p", "--preview", action="store_true",
        help="generates previews for all themes")

    return parser.parse_args(argv)



def build_all_themes():
    '''
    Builds all themes
    '''
    # remove previous theme build output if any
    shutil.rmtree("themes", True)

    for theme in OTHER_THEMES:
        print("Building theme %s" % (theme,))
        update_conf(theme)
        cmdline.build()
        move_theme(theme)

    update_conf(DEFAULT_THEME)
    cmdline.build()



command = parse(sys.argv[1:])

if command.open:
    build_all_themes()
    open_all()   
elif command.preview:
    build_all_themes()
    copy_previews()
