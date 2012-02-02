'''
    metadata
    ~~~~~~~~

    Blog metadata extension. The extension extracts and computes metadata 
    associated with blog posts/pages and stores it in the environment.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import re
import datetime 
from sphinx.util.compat import Directive
import tinkerer



def initialize(app):
    '''
    Initializes metadata in environment.
    '''
    app.builder.env.blog_metadata = dict()



class Metadata:
    '''
    Metadata associated with each post/page.
    '''
    def __init__(self):
        '''
        Initializes metadata with default values.
        '''
        self.is_post = False
        self.title = None
        self.link = None
        self.date = None
        self.body = None
        self.author = None
        self.filing = { "tags": [], "categories": [] }
        self.comments, self.comment_count = False, False

               

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

    env.blog_metadata[docname] = Metadata()
    metadata = env.blog_metadata[docname]

    # posts are identified by ($YEAR)/($MONTH)/($DAY) paths
    match = re.match(r"\d{4}/\d{2}/\d{2}/", docname)

    # if not post return
    if not match:
        return

    metadata.is_post = True
    metadata.link = docname
    metadata.date = datetime.datetime.strptime(match.group(), "%Y/%m/%d/")



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
                else:
                    env.blog_pages.append(doc)
     
    env.blog_page_list = [("index", _("Home"))] + [(page, env.titles[page].astext()) for page in env.blog_pages]



def add_metadata(app, pagename, context):
    '''
    Passes metadata to the templating engine.
    '''
    env = app.builder.env

    # blog tagline and pages
    context["tagline"] = app.config.tagline
    context["pages"] = env.blog_page_list
    
    # set translation context variables
    context["text_recent_posts"] = _("Recent Posts")
    context["text_posted_by"] = _("Posted by")
    context["text_blog_archive"] = _("Blog Archive")
    context["text_filed_under"] = _("Filed under")
    context["text_tags"] = _("Tags")
    context["timestamp_format"] = _('%B %d, %Y')    

    # recent posts
    context["recent"] = [(post, env.titles[post].astext()) for post 
            in env.blog_posts[:20]]

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

