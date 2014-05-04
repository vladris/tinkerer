'''
    metadata
    ~~~~~~~~

    Blog metadata extension. The extension extracts and computes metadata
    associated with blog posts/pages and stores it in the environment.

    :copyright: Copyright 2011-2014 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import re
import datetime
import locale
from functools import partial
from sphinx.util.compat import Directive
from babel.core import Locale
from babel.dates import format_date
import tinkerer
from tinkerer.ext.uistr import UIStr
from tinkerer.utils import name_from_title



def initialize(app):
    '''
    Initializes metadata in environment.
    '''
    app.builder.env.blog_metadata = dict()


class Metadata:
    '''
    Metadata associated with each post/page.
    '''
    num = 1
    def __init__(self):
        '''
        Initializes metadata with default values.
        '''
        self.is_post = False
        self.is_page = False
        self.title = None
        self.link = None
        self.date = None
        self.formatted_date = None
        self.formatted_date_short = None
        self.body = None
        self.author = None
        self.filing = { "tags": [], "categories": [] }
        self.comments, self.comment_count = False, False
        self.num = Metadata.num
        Metadata.num += 1



class CommentsDirective(Directive):
    '''
    Comments directive. The directive is not rendered by this extension, only
    added to the metadata, so plug-in comment handlers can be used.
    '''
    required_arguments = 0
    optional_arguments = 0
    has_content = False

    def run(self):
        '''
        Called when parsing the document.
        '''
        env = self.state.document.settings.env

        # mark page as having comments
        env.blog_metadata[env.docname].comments = True

        return []



def get_metadata(app, docname):
    '''
    Extracts metadata from a document.
    '''
    env = app.builder.env
    language = app.config.language
    locale = Locale.parse(language) if language else Locale('en', 'US')
    format_ui_date = partial(
        format_date, format=UIStr.TIMESTAMP_FMT, locale=locale)
    format_short_ui_short = partial(
        format_date, format=UIStr.TIMESTAMP_FMT_SHORT, locale=locale)

    env.blog_metadata[docname] = Metadata()
    metadata = env.blog_metadata[docname]

    # if it's a page
    if docname.startswith("pages/"):
      metadata.is_page = True
      return

    # posts are identified by ($YEAR)/($MONTH)/($DAY) paths
    match = re.match(r"\d{4}/\d{2}/\d{2}/", docname)

    # if not post return
    if not match:
        return

    metadata.is_post = True
    metadata.link = docname
    metadata.date = datetime.datetime.strptime(match.group(), "%Y/%m/%d/")

    # we format date here instead of inside template due to localization issues
    # and Python2 vs Python3 incompatibility
    metadata.formatted_date = format_ui_date(metadata.date)
    metadata.formatted_date_short = format_short_ui_short(metadata.date)


def process_metadata(app, env):
    '''
    Processes metadata after all sources are read - the function determines
    post and page ordering, stores doc titles and adds "Home" link to page
    list.
    '''
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
                elif env.blog_metadata[doc].is_page:
                    env.blog_pages.append(doc)

    env.blog_page_list = [("index", UIStr.HOME)] + [(page, env.titles[page].astext()) for page in env.blog_pages]



def add_metadata(app, pagename, context):
    '''
    Passes metadata to the templating engine.
    '''
    env = app.builder.env

    # page data
    context['website'] = app.config.website

    # blog tagline and pages
    context["tagline"] = app.config.tagline
    context["description"] = app.config.description
    context["pages"] = env.blog_page_list

    # set translation context variables
    context["text_recent_posts"] = UIStr.RECENT_POSTS
    context["text_posted_by"] = UIStr.POSTED_BY
    context["text_blog_archive"] = UIStr.BLOG_ARCHIVE
    context["text_filed_under"] = UIStr.FILED_UNDER
    context["text_tags"] = UIStr.TAGS
    context["text_tags_cloud"] = UIStr.TAGS_CLOUD
    context["text_categories"] = UIStr.CATEGORIES

    # recent posts
    context["recent"] = [(post, env.titles[post].astext()) for post
            in env.blog_posts[:20]]
    # tags & categories
    tags = dict((t, 0) for t in env.filing["tags"])
    taglinks = dict((t, name_from_title(t)) for t in env.filing["tags"])
    categories = dict((c, 0) for c in env.filing["categories"])
    catlinks = dict([(c, name_from_title(c)) for c in env.filing["categories"]])
    for post in env.blog_posts:
        p = env.blog_metadata[post]
        for tag in p.filing["tags"]:
            tags[tag[1]] += 1
        for cat in p.filing["categories"]:
            categories[cat[1]] += 1
    context["tags"] = tags
    context["taglinks"] = taglinks
    context["categories"] = categories
    context["catlinks"] = catlinks

    # if there is metadata for the page, it is not an auto-generated one
    if pagename in env.blog_metadata:
        context["metadata"] = env.blog_metadata[pagename]

        # if this is a post
        if pagename in env.blog_posts:
            # save body
            env.blog_metadata[pagename].body = context["body"]

            # no prev link if first post, no next link for last post
            if pagename == env.blog_posts[0]:
                context["prev"] = None
            if pagename == env.blog_posts[-1]:
                context["next"] = None
        # if this is not documententation
        elif not (pagename.startswith("doc/") or pagename.startswith("docs/")):
            # no rellinks for non-posts/docs
            context["prev"], context["next"] = None, None

    # otherwise provide default metadata
    else:
        context["metadata"] = Metadata()
