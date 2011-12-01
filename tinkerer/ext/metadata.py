'''
    metadata
    ~~~~~~~~

    Blog metadata extension

    :copyright: Copyright 2011 by Vlad Riscutia.
'''
import re
from datetime import date
from sphinx.util.compat import Directive


# initialize metadata
def initialize(app):
    env = app.builder.env

    env.blog_metadata = dict()
    env.blog_pages = []
    env.blog_posts = []


# Metadata associated with each post/page
class Metadata:
    def __init__(self):
        self.is_post, self.first_post, self.last_post = False, False, False
        self.year, self.month, self.day, self.date = None, None, None, None
        self.tags = []
        self.comments = False


# comments directive
class CommentsDirective(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = False

    def run(self):
        env = self.state.document.settings.env

        # mark page as having comments
        env.blog_metadata[env.docname].comments = True

        return []


# add metadata to environment
def get_metadata(app, docname, source):
    env = app.builder.env

    env.blog_metadata[docname] = Metadata()
    metadata = env.blog_metadata[docname]

    # posts are identified by ($YEAR)/($MONTH)/($DAY) paths
    match = re.match(r"(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/", docname)

    if not match:
        env.blog_pages.append(docname)
        return
    env.blog_posts.append(docname)
    metadata.is_post = True

    g = match.groupdict()
    metadata.year, metadata.month, metadata.day = int(g["year"]), int(g["month"]), int(g["day"])
    metadata.date = date(metadata.year, metadata.month, metadata.day)


# process metadata after environment is ready
def process_metadata(app, env):
    env.blog_page_list = [(page, env.titles[page].astext()) for page in env.blog_pages]

    if env.blog_posts:
        env.blog_metadata[env.blog_posts[0]].first_post = True
        env.blog_metadata[env.blog_posts[-1]].last_post = True

        env.blog_page_list[0] = (env.blog_posts[-1], "Blog")
        env.blog_latest_posts = [(page, env.titles[page].astext()) for page in env.blog_posts[-1:-6:-1]]
    else:
        env.blog_page_list.pop(0)
        env.blog_latest_posts = [("index", "")]        


# pass metadata to templating engine
def add_metadata(app, pagename, templatename, context, doctree):
    env = app.builder.env

    # blog tagline, latest posts and pages
    context["tagline"] = app.config.tagline
    context["latest"] = env.blog_latest_posts
    context["pages"] = env.blog_page_list

    # if there is metadata for the page, it is not an auto-generated one
    if pagename in env.metadata:
        context["metadata"] = env.blog_metadata[pagename]
    # otherwise provide default metadata
    else:
        context["metadata"] = Metadata()


# setup metadata
def setup(app):
    app.add_config_value("tagline", "My blog", True)

    app.add_directive("comments", CommentsDirective)

    app.connect("builder-inited", initialize)
    app.connect("source-read", get_metadata)
    app.connect("env-updated", process_metadata)
    app.connect("html-page-context", add_metadata)

