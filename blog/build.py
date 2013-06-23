'''
    Build utility for Tinkerer blog
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Builds the blog with all themes and either generates the theme previews or
    opens each theme in the browser.

    :copyright: Copyright 2011-2013 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import os
import shutil
from tinkerer import cmdline



DEFAULT_THEME = "flat"

OTHER_THEMES = ["modern5"] #  "minimal5", "responsive", "dark"]



def update_conf(theme):
    '''
    Updates conf.py with the given theme
    '''
    CONF = "conf.py"

    lines = open(CONF).readlines()
    lines = ["html_theme = '%s'\n" % (theme, ) if "html_theme =" in line 
                else line for line in lines]
    open(CONF, "w").writelines(lines)
     


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



# remove previous theme build output if any
shutil.rmtree("themes", True)

for theme in OTHER_THEMES:
    print("Building theme %s" % (theme,))
    update_conf(theme)
    cmdline.build()
    move_theme(theme)

update_conf(DEFAULT_THEME)
cmdline.build()

open_all()
