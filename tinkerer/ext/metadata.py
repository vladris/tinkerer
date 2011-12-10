'''
    metadata
    ~~~~~~~~

    Blog metadata extension.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
import re
from datetime import date
from sphinx.util.compat import Directive
import tinkerer


# initialize metadata
def initialize(app):
    env = app.builder.env

    env.blog_metadata = dict()


# Metadata associated with each post/page
class Metadata:
    def __init__(self):
        self.is_post = False
        self.title = None
        self.link = None
        self.year, self.month, self.day, self.date = None, None, None, None
        self.body = None
        self.author = None
        self.tags = []
        self.comments, self.comment_count = False, False


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
def get_metadata(app, docname):
    env = app.builder.env

    env.blog_metadata[docname] = Metadata()
    metadata = env.blog_metadata[docname]

    # posts are identified by ($YEAR)/($MONTH)/($DAY) paths
    match = re.match(r"(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/", docname)

    # if not post
    if not match:
        return

    metadata.is_post = True
    metadata.link = docname

    g = match.groupdict()
    metadata.year, metadata.month, metadata.day = int(g["year"]), int(g["month"]), int(g["day"])
    metadata.date = date(metadata.year, metadata.month, metadata.day)


# process metadata after environment is ready
def process_metadata(app, env):
    # get ordered lists of posts and pages
    env.blog_posts, env.blog_pages = [], []
    relations = env.collect_relations()

    # start from root
    doc = tinkerer.master_doc

    # while not last doc
    while relations[doc][2]:
        doc = relations[doc][2]

        # if this is a post or a page (has metadata)
        if doc in env.blog_metadata:
            # set title
            env.blog_metadata[doc].title = env.titles[doc].astext()

            # ignore if parent is not master (eg. nested pages)
            if relations[doc][0] == tinkerer.master_doc:
                if env.blog_metadata[doc].is_post:
                    env.blog_posts.append(doc)
                else:
                    env.blog_pages.append(doc)
     
    env.blog_page_list = [("index", "Home")] + [(page, env.titles[page].astext()) for page in env.blog_pages]



# pass metadata to templating engine, store body for RSS feed
def add_metadata(app, pagename, context):
    env = app.builder.env

    # blog tagline and pages
    context["tagline"] = app.config.tagline
    context["pages"] = env.blog_page_list
    context["recent"] = [(post, env.titles[post].astext()) for post 
            in env.blog_posts[:20]]

    # if there is metadata for the page, it is not an auto-generated one
    if pagename in env.metadata:
        context["metadata"] = env.blog_metadata[pagename]

        # if this is a post
        if pagename in env.blog_posts:
            # save body and inject hyperlink in title
            env.blog_metadata[pagename].body = context["body"].replace(
                        env.blog_metadata[pagename].title,
                        '<a href="%s.html">%s</a>' % 
                                (pagename, env.blog_metadata[pagename].title),
                        1)

            # no prev link if first post, no next link for last post
            if pagename == env.blog_posts[0]:
                context["prev"] = None
            elif pagename == env.blog_posts[-1]:
                context["next"] = None
        else:
            # no prev/next for non-posts
            context["prev"], context["next"] = None, None

    # otherwise provide default metadata
    else:
        context["metadata"] = Metadata()

