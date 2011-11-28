'''
    latest
    ~~~~~~

    Widget to displays latest posts.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import tinkerer


# add template to sidebar
def init_latest(app):
    if "**" not in app.config.html_sidebars:
        app.config.html_sidebars["**"] = []
    app.config.html_sidebars["**"].append("latest.html")


# get latest 6 posts from metadata
def get_latest(app, env):
    if env.blog_posts:
        env.blog_latest_posts = [(page, env.titles[page].astext()) for
                    page in env.blog_posts[:6]]
    else:
        env.blog_latest_posts = [(tinkerer.master_doc, "")]


# pass latest posts to template
def add_latest(app, pagename, templatename, context, doctree):
    context["latest"] = app.builder.env.blog_latest_posts


# setup widget
def setup(app):
    app.connect("builder-inited", init_latest)
    app.connect("env-updated", get_latest)
    app.connect("html-page-context", add_latest)
            
