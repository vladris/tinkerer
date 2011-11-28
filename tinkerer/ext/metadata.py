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
import xml.dom.minidom


# initialize metadata
def initialize(app):
    env = app.builder.env

    env.blog_metadata = dict()


# Metadata associated with each post/page
class Metadata:
    def __init__(self):
        self.is_post = False
        self.year, self.month, self.day, self.date = None, None, None, None
        self.body, self.summary = None, None
        self.author = None
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

    # if not post
    if not match:
        return

    metadata.is_post = True

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
            # ignore if parent is not master (eg. nested pages)
            if relations[doc][0] == tinkerer.master_doc:
                if env.blog_metadata[doc].is_post:
                    env.blog_posts.append(doc)
                else:
                    env.blog_pages.append(doc)
     
    env.blog_page_list = [(page, env.titles[page].astext()) for page in env.blog_pages]

    # if there is at least one post
    if env.blog_posts:
        # add a page linking to the first post
        env.blog_page_list.insert(0, (env.blog_posts[0], "Home"))


# get 50 word summary of post from body
def get_summary(body):
    dom = xml.dom.minidom.parseString(body.encode("ascii", "ignore"))
    summarize(dom, 0)

    # skip auto-inserted xml version
    return dom.toxml()[22:]


# recursively summarize dom
def summarize(dom, length, depth=0):
    done = False

    for child in dom.childNodes[:]:
        # strip childs when done to remain with summary
        if done:
            dom.removeChild(child)
        # if node is text
        elif child.nodeValue:
            # trim text if exceeding length
            l = len(child.nodeValue.split())
            if length + l >= 50:
                child.nodeValue = " ".join(child.nodeValue.split()[:50 - length])
                done = True
            # update current length
            else:
                length += l
        # if node is not text, recurse
        else:
            done = summarize(child, length, depth + 1)
    return done


# pass metadata to templating engine, store body for RSS feed
def add_metadata(app, pagename, templatename, context, doctree):
    env = app.builder.env

    # blog tagline and pages
    context["tagline"] = app.config.tagline
    context["pages"] = env.blog_page_list

    # if there is metadata for the page, it is not an auto-generated one
    if pagename in env.metadata:
        context["metadata"] = env.blog_metadata[pagename]

        # if this is a post
        if pagename in env.blog_posts:
            # save body and summary
            env.blog_metadata[pagename].body = context["body"]
            env.blog_metadata[pagename].summary = get_summary(context["body"])

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


# setup metadata
def setup(app):
    app.add_config_value("tagline", "My blog", True)

    app.add_directive("comments", CommentsDirective)

    app.connect("builder-inited", initialize)
    app.connect("source-read", get_metadata)
    app.connect("env-updated", process_metadata)
    app.connect("html-page-context", add_metadata)

