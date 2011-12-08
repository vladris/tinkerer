'''
    latest
    ~~~~~~

    Widget to displays latest posts.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import tinkerer


# get latest 6 posts from metadata
def get_latest(app, env):
    if not env.blog_posts:
        return

    app.config.lists.insert(0, ["Latest Posts"] + 
            # append "~" at beginning so template knows to compute relative path
            # see tinkerbase/lists.html
            [(env.titles[page].astext(), "~" + page) for page in env.blog_posts[:6]])


# setup widget
def setup(app):
    app.connect("env-updated", get_latest)
            
