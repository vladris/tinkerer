'''
    filing
    ~~~~~~

    Handles post filing by date, caregories and tags.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from sphinx.util.compat import Directive
from tinkerer import utils



def create_filing_directive(name):
    class FilingDirective(Directive):
        '''
        Filing directive used to groups posts. The directive is not rendered, 
        just stored in the metadata and passed to the templating engine.
        '''
        required_arguments = 0
        optional_arguments = 100
        has_content = False

        def run(self):
            '''
            Called when parsing the document.
            '''
            env = self.state.document.settings.env

            for item in " ".join(self.arguments).split(","):
                item = item.strip()
                if item == "none":
                    continue

                if item not in env.filing[name]:
                    env.filing[name][item] = []
                env.filing[name][item].append(env.docname)
                env.blog_metadata[env.docname].filing[name].append(
                        (utils.name_from_title(item), item))

            return []

    return FilingDirective



def initialize(app):
    '''
    Initializes tags and categories.
    '''
    app.builder.env.filing = { "tags": dict(), "categories": dict() }



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
    yield make_archive_page(app.builder.env, _("Blog Archive"), "archive") 



def make_tag_pages(app):
    '''
    Generates archive pages for each tag.
    '''
    env = app.builder.env
    for tag in env.filing["tags"]:
        yield make_archive_page(env,
                _('Posts tagged with <span class="title_tag">%s</span>') % tag,
                "tags/" + utils.name_from_title(tag),
                lambda post: post in env.filing["tags"][tag])



def make_category_pages(app):
    '''
    Generates archive pages for each category.
    '''
    env = app.builder.env
    for category in env.filing["categories"]:
        yield make_archive_page(env,
                _('Filed under <span class="title_category">%s</span>') % category,
                "categories/" + utils.name_from_title(category),
                lambda post: post in env.filing["categories"][category])

