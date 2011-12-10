'''
    rss
    ~~~

    RSS feed generator for blog. 

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import time
import cgi
import email.utils


# add rss service link to page context 
def add_rss(app, context):
    context["rss_service"] = app.config.rss_service


# generate RSS feed
def generate_feed(app):
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

        context["items"].append({
                    "title": env.titles[post].astext(),
                    "link": link,
                    "description": env.blog_metadata[post].body,
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

