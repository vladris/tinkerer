'''
    lists
    ~~~~~

    Sidebar lists.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
import tinkerer.utils


# add lists to sidebar
def init_lists(app):
    if "**" not in app.config.html_sidebars:
        app.config.html_sidebars["**"] = []
    app.config.html_sidebars["**"].append("lists.html")


# process lists and pass them to template
def add_lists(app, pagename, templatename, context, doctree):
    context["link_lists"] = app.config.lists


# setup lists
def setup(app):
    app.add_config_value("lists", [], True)

    app.connect("builder-inited", init_lists)
    app.connect("html-page-context", add_lists)

