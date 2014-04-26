'''
    rss
    ~~~

    RSS feed generator for blog. 

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import cgi
import email.utils
import time

import pyquery

from tinkerer.ext import patch
from tinkerer import utils


def remove_header_link(body):
    """Remove any headerlink class anchor tags from the body.
    """
    doc = pyquery.PyQuery(body)
    doc.remove('a.headerlink')
    body = doc.html()
    return body


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

    posts = env.blog_posts
    if app.config.rss_max_items > 0:
        posts = posts[:app.config.rss_max_items]

    context = make_feed_context(app, None, posts)
    yield ("rss", context, "rss.html")


def make_feed_context(app, feed_name, posts):
    env = app.builder.env
    context = dict()

    # feed items
    context["items"] = []
    for post in posts:
        link = "%s%s.html" % (app.config.website, post)

        timestamp = email.utils.formatdate(
                time.mktime(env.blog_metadata[post].date.timetuple()),
                localtime=True)

        categories = [category[1] for category in env.blog_metadata[post].filing["categories"]]

        description = patch.strip_xml_declaration(
            patch.patch_links(
                env.blog_metadata[post].body,
                app.config.website + post[:11], # first 11 characters is path (YYYY/MM/DD/)
                post[11:], # following characters represent filename
                replace_read_more_link=not app.config.rss_generate_full_posts,
            ),
        )
        description = remove_header_link(description)

        context["items"].append({
                    "title": env.titles[post].astext(),
                    "link": link,
                    "description": description,
                    "categories": categories,
                    "pubDate": timestamp
                })

    # feed metadata
    if feed_name:
        context["title"] = "%s - %s" % (app.config.project, feed_name)
    else:
        context["title"] = app.config.project
    context["link"] = app.config.website
    context["tagline"] = app.config.tagline
    context["language"] = "en-us"

    # feed pubDate is equal to latest post pubDate
    if context['items']:
        context["pubDate"] = context["items"][0]["pubDate"]

    return context
