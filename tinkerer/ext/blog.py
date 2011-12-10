'''
    blog
    ~~~~

    Master blog extension.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
from tinkerer.ext import aggregator, author, lists, metadata, rss, tags, twitter


# initialize extension after builder is initialized
def initialize(app):
    if not app.config.website[-1] == "/":
        app.config.website += "/"

    metadata.initialize(app)
    lists.initialize(app)
    tags.initialize(app)


# called after source is read
def source_read(app, docname, source):
    metadata.get_metadata(app, docname)


# called after environment is updated
def env_updated(app, env):
    metadata.process_metadata(app, env)


# called before pages are rendered
def html_page_context(app, pagename, templatename, context, doctree):
    env = app.builder.env

    metadata.add_metadata(app, pagename, context)
    lists.add_lists(app, context)
    rss.add_rss(app, context)
    twitter.add_twitter_id(app, context)


# generate additional pages
def html_collect_pages(app):
    for name, context, template in rss.generate_feed(app):
        yield (name, context, template)

    for name, context, template in tags.make_tag_pages(app):
        yield (name, context, template)

    for name, context, template in aggregator.make_aggregated_pages(app):
        yield (name, context, template)


# setup extensions
def setup(app):
    app.add_config_value("tagline", "My blog", True)
    app.add_config_value("author", "Winston Smith", True)
    app.add_config_value("lists", [], True)
    app.add_config_value("rss_service", None, True)
    app.add_config_value("twitter_id", None, True)
    app.add_config_value("website", "http://127.0.0.1/blog/html/", True)

    app.add_directive("author", author.AuthorDirective)
    app.add_directive("comments", metadata.CommentsDirective)
    app.add_directive("tags", tags.TagsDirective)

    app.connect("builder-inited", initialize)
    app.connect("source-read", source_read)
    app.connect("env-updated", env_updated)
    app.connect("html-page-context", html_page_context)
    app.connect("html-collect-pages", html_collect_pages)
