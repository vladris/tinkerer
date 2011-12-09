'''
    archive
    ~~~~~~~

    Archive generator - groups posts by date and tags.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
from sphinx.util.compat import Directive
from tinkerer import utils



class TagsDirective(Directive):
    '''
    Tags directive. The directive is not rendered, just stored in the
    metadata and passed to the templating engine.
    '''
    required_arguments = 0
    optional_arguments = 100
    has_content = False

    def run(self):
        '''
        Called when parsing the document.
        '''
        env = self.state.document.settings.env

        for tag in " ".join(self.arguments).split(","):
            tag = tag.strip()
            if tag == "none":
                continue

            if tag not in env.blog_tags:
                env.blog_tags[tag] = []
            env.blog_tags[tag].append(env.docname)
            env.blog_metadata[env.docname].tags.append((utils.filename_from_title(tag), tag))

        return []



def initialize(app):
    '''
    Initializes tags.
    '''
    app.builder.env.blog_tags = dict()



def make_archive_page(env, title, pagename, post_filter=None):
    '''
    Generates archive page with given title by applying the given filter to
    all posts and aggregating results by year.
    '''
    context = { "title": title }
    context["years"] = dict()

    for post in filter(post_filter, env.blog_posts):
        year = env.blog_metadata[post].date.year
        if year not in context["years"]:
            context["years"][year] = []
        context["years"][year].append(env.blog_metadata[post])

    return (pagename, context, "archive.html")



def make_archive(app):
    '''
    Generates blog archive including all posts.
    '''
    yield make_archive_page(app.builder.env, "Blog Archive", "archive") 



def make_tag_pages(app):
    '''
    Generates archive pages for each tag.
    '''
    env = app.builder.env
    for tag in env.blog_tags:
        yield make_archive_page(env,
                'Posts tagged with <span class="title_tag">%s</span>' % tag,
                "tags/" + utils.filename_from_title(tag),
                lambda post: post in env.blog_tags[tag])
