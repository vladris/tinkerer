'''
    rss
    ~~~

    RSS feed generator for blog. 

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import time
import cgi
import email.utils


# initialize RSS feed
def initialize(app):
    app.builder.env.rss_items = []


# RSS item
class RssItem:
    def __init__(self, link, title, description, pub_date):
        self.link = link
        self.title = title
        self.description = description
        self.pub_date = pub_date


# generate feed item from page
def get_post_feed(app, pagename, templatename, context, doctree):
    env = app.builder.env

    # only generate feed for posts
    if pagename not in env.blog_posts:
        return

    # convert timestamp to RFC-822
    timestamp = email.utils.formatdate(
                    time.mktime(env.blog_metadata[pagename].date.timetuple()), 
                    usegmt=True)
    title = cgi.escape(env.titles[pagename].astext())
    description = context["body"]
    link = "%s/blog/html/%s.html" % (app.config.website, pagename)

    # add item
    env.rss_items.append(RssItem(link, title, description, timestamp))


# generate RSS feed
def generate_feed(app):
    env = app.builder.env
  
    # feed metadata 
    context = dict()
    context["title"] = app.config.project
    context["link"] = app.config.website
    context["description"] = app.config.tagline
    context["language"] = "en-us"
    context["pubDate"] = env.rss_items[-1].pub_date

    # items
    context["items"] = env.rss_items[::-1]

    yield ("rss", context, "rss.html")


# setup feed generator
def setup(app):
    app.add_config_value("website", "http://127.0.0.1", True)

    app.connect("builder-inited", initialize)
    app.connect("html-page-context", get_post_feed)
    app.connect("html-collect-pages", generate_feed)

