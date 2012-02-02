'''
    rss
    ~~~

    RSS feed generator for blog. 

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import cgi
import email.utils
import time
from tinkerer.ext import patch



def add_rss(app, context):
    '''
    Adds RSS service link to page context.
    '''
    context["rss_service"] = app.config.rss_service



def generate_feed(app):
    '''
    Generates RSS feed.
    '''
    env = app.builder.env
 
    # don't do anything if no posts are available
    if not env.blog_posts:
        return

    context = dict()

    # feed items
    context["items"] = []
    for post in env.blog_posts:
        link = "%s%s.html" % (app.config.website, post)

        timestamp = email.utils.formatdate(
                time.mktime(env.blog_metadata[post].date.timetuple()),
                usegmt=True)

        categories = [category[1] for category in env.blog_metadata[post].filing["categories"]]

        context["items"].append({
                    "title": env.titles[post].astext(),
                    "link": link,
                    "description": patch.patch_links(
                            env.blog_metadata[post].body, 
                            app.config.website + post[:11]),
                    "categories": categories,
                    "pubDate": timestamp
                })

    # feed metadata 
    context["title"] = app.config.project
    context["link"] = app.config.website
    context["description"] = app.config.tagline
    context["language"] = "en-us"
  
    # feed pubDate is equal to latest post pubDate
    context["pubDate"] = context["items"][0]["pubDate"]

    yield ("rss", context, "rss.html")

