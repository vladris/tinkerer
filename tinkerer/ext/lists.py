'''
    lists
    ~~~~~

    Sidebar lists.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
import tinkerer.utils


# add lists to sidebar
def initialize(app):
    if "**" not in app.config.html_sidebars:
        app.config.html_sidebars["**"] = []
    app.config.html_sidebars["**"].append("lists.html")


# process lists and pass them to template
def add_lists(app, context):
    context["link_lists"] = app.config.lists


