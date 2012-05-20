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
from tinkerer.utils import name_from_title



def add_rss(app, context):
    '''
    Adds RSS service link to page context.
    '''
    context["rss_service"] = app.config.rss_service



def generate_feed(app, name, posts):
    '''
    Generates RSS feed.
    '''
    env = app.builder.env
 
    # don't do anything if no posts are available
    if not posts:
        return

    context = dict()

    # feed items
    context["items"] = []
    for post in posts:
        link = "%s%s.html" % (app.config.website, post)

        timestamp = email.utils.formatdate(
                time.mktime(env.blog_metadata[post].date.timetuple()),
                localtime=True)

        categories = [category[1] for category in env.blog_metadata[post].filing["categories"]]

        context["items"].append({
                    "title": env.titles[post].astext(),
                    "link": link,
                    "description": patch.strip_xml_declaration(patch.patch_links(
                            env.blog_metadata[post].body, 
                            app.config.website + post[:11])),
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

    return (name, context, "rss.html")



def generate_all_feed(app):
    '''
    Generates all RSS feed.
    '''

    env = app.builder.env
 
    yield generate_feed(app, "rss/all", env.blog_posts)



def generate_feed_for(app, feed_type="categories"):
    '''
    Generates RSS feed for categories or tags.
    '''
    env = app.builder.env
 
    # only for categories and tags
    if feed_type not in ("categories", "tags"):
        return []

    # don't do anything if no posts are available
    if not env.blog_posts:
        return []

    # don't do anything if option is not set
    if (feed_type == "categories" and not app.config.rss_for_categories) or \
       (feed_type == "tags" and not app.config.rss_for_tags):
        return []

    context = dict()
    # posts for categories/tags
    posts = {}

    # categories or tags to build rss feed
    list_to_build = app.config.rss_categories_to_build if feed_type == "categories" \
                    else app.config.rss_tags_to_build

    # get posts by category or tag
    for post in env.blog_posts:
        cts = [ct[1] for ct in env.blog_metadata[post].filing[feed_type]]
        for ct in cts:
            if not list_to_build or ct in list_to_build:
                p = posts.setdefault(ct, [])
                p.append(post)

    return posts



def generate_feed_for_categories(app):
    '''
    Generates RSS feed for categories.
    '''
    posts = generate_feed_for(app, "categories") 
    for ct in posts:
        name = "rss/%s/%s" % ("categories", name_from_title(ct))
        yield generate_feed(app, name, posts[ct])



def generate_feed_for_tags(app):
    '''
    Generates RSS feed for tags.
    '''
    posts = generate_feed_for(app, "tags") 
    for ct in posts:
        name = "rss/%s/%s" % ("tags", name_from_title(ct))
        yield generate_feed(app, name, posts[ct])
