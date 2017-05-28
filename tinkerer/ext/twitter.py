"""
Twitter buttons
===============

Adds a twitter button to each post for readers to recommend the post
on Twitter.  Twitter username must be provided in `conf.py` as
`twitter_username`.

:copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
CONTRIBUTORS file)
:license: FreeBSD, see LICENSE file

"""

TWITTER_CODE = \
    '<a href="https://twitter.com/share" class="twitter-share-button" ' \
    'data-text="%s" data-url="%s" data-via="%s" data-lang="en" ' \
    'data-related="anywhereTheJavascriptAPI" data-dnt="true" ' \
    'data-count="horiontal">Tweet</a><script>!function(d,s,id){var ' \
    'js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){' \
    'js=d.createElement(s);js.id=id;js.src="https://platform.twitte' \
    'r.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(docum' \
    'ent,"script","twitter-wjs");</script>'


def add_twitter_buttons(app, pagename, *args, **kwargs):
    """Adds Twitter buttons to page."""
    # return if no username was provided
    if not app.config.twitter_username:
        return

    env = app.builder.env

    # if page is blog post and has comments
    if pagename in env.blog_metadata:

        title = env.blog_metadata[pagename].title
        link = "%s%s.html" % (app.config.website,
                              env.blog_metadata[pagename].link)
        username = app.config.twitter_username
        twitter_button_code = str(TWITTER_CODE % (title, link, username))
        env.blog_metadata[pagename].twitter_button = twitter_button_code


def setup(app):
    '''
    Sets up Twitter button handler.
    '''
    # twitter_username contains username provided to Twitter
    app.add_config_value("twitter_username", None, True)

    # connect event
    app.connect("html-page-context", add_twitter_buttons)
