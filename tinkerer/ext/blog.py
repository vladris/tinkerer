'''
    blog
    ~~~~

    Master blog extension.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from tinkerer.ext import aggregator, author, filing, metadata, rss 
import gettext



def initialize(app):
    '''
    Initializes extension after environment is initialized.
    '''
    # ensure website config value ends with "/"
    if not app.config.website[-1] == "/":
        app.config.website += "/"

    # initialize other components
    metadata.initialize(app)
    filing.initialize(app)

    lang = app.config.language if app.config.language else ""

    locale_dir = ""
    try:
        from pkg_resources import resource_filename
    except ImportError:
        resource_filename = None

    if resource_filename is not None:
        try:
            locale_dir = resource_filename(__name__, "/locale")
        except NotImplementedError:
            # resource_filename doesn't work with non-egg zip files
            pass

    app.t = gettext.translation(
                    "tinkerer",
                    locale_dir,
                    languages=[lang],
                    fallback=True)
    _ = app.t.gettext
    app.t.install()

def source_read(app, docname, source):
    '''
    Processes document after source is read.
    '''
    metadata.get_metadata(app, docname)



def env_updated(app, env):
    '''
    Processes data after environment is updated (all docs are read).
    '''
    metadata.process_metadata(app, env)



def html_page_context(app, pagename, templatename, context, doctree):
    '''
    Passes data to templating engine.
    '''
    metadata.add_metadata(app, pagename, context)
    rss.add_rss(app, context)



def html_collect_pages(app):
    '''
    Generates additional pages.
    '''
    for name, context, template in rss.generate_feed(app):
        yield (name, context, template)

    for name, context, template in filing.make_tag_pages(app):
        yield (name, context, template)

    for name, context, template in filing.make_category_pages(app):
        yield (name, context, template)

    for name, context, template in aggregator.make_aggregated_pages(app):
        yield (name, context, template)

    for name, context, template in filing.make_archive(app):
        yield (name, context, template)



def setup(app):
    '''
    Sets up the extension.
    '''
    # new config values
    app.add_config_value("tagline", "My blog", True)
    app.add_config_value("author", "Winston Smith", True)
    app.add_config_value("rss_service", None, True)
    app.add_config_value("website", "http://127.0.0.1/blog/html/", True)

    # new directives
    app.add_directive("author", author.AuthorDirective)
    app.add_directive("comments", metadata.CommentsDirective)
    app.add_directive("tags", 
            filing.create_filing_directive("tags"))
    app.add_directive("categories", 
            filing.create_filing_directive("categories"))

    # event handlers
    app.connect("builder-inited", initialize)
    app.connect("source-read", source_read)
    app.connect("env-updated", env_updated)
    app.connect("html-page-context", html_page_context)
    app.connect("html-collect-pages", html_collect_pages)
