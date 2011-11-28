'''
    twitter
    ~~~~~~~

    Twitter extension. 

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''

# add twitter_id to page context 
def add_rss(app, pagename, templatename, context, doctree):
    context["twitter_id"] = app.config.twitter_id


# setup feed generator
def setup(app):
    app.add_config_value("twitter_id", None, True)

    app.connect("html-page-context", add_rss)

