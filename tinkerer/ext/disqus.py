'''
    disqus
    ~~~~~~

    Handler for `comments` directive using Disqus.
    Disqus shortname must be provided in `conf.py` as `disqus_shortname`.
    
    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
from sphinx.util.compat import Directive
from docutils import nodes


DISQUS_SCRIPT = "_static/disqus.js"


# create Disqus thread
def create_thread(disqus_shortname, identifier):
    # code provided by Disqus
    return str(
'<div id="disqus_thread"></div>'
'<script type="text/javascript">'
'    var disqus_shortname = "%s";'
'    var disqus_identifier = "%s";'
'    disqus_thread();'
'</script>'
'<noscript>Please enable JavaScript to view the '
'   <a href=\"http://disqus.com/?ref_noscript\">comments powered by Disqus.</a>'
'</noscript>' % (disqus_shortname, identifier))


# enable comment count
def enable_count(disqus_shortname):
    return str(
'<script type="text/javascript">'
'    var disqus_shortname = "%s";'
'    disqus_count();'
'</script>' 
            % disqus_shortname)


# get comment count for post
def get_count(link, identifier, title):
    return str('<a href="%s#disqus_thread" data-disqus-identifier="%s">%s</a>' % 
            (link, identifier, title))


# enable disqus comments
def add_disqus_block(app, pagename, templatename, context, doctree):
    if not app.config.disqus_shortname:
        return

    env = app.builder.env

    if DISQUS_SCRIPT not in context["script_files"]:
        context["script_files"].append(DISQUS_SCRIPT)

    if pagename in env.blog_metadata and env.blog_metadata[pagename].comments:
        context["comments"] = create_thread(app.config.disqus_shortname, pagename)
        env.blog_metadata[pagename].comment_count = get_count(
                "%s%s.html" % (app.config.website,
                                env.blog_metadata[pagename].link),
                pagename,
                env.blog_metadata[pagename].title)
    else:
        context["comment_enabler"] = enable_count(app.config.disqus_shortname)


# setup Disqus
def setup(app):
    # disqus_shortname contains shortname provided to Disqus
    app.add_config_value("disqus_shortname", None, True)

    # connect events
    app.connect("html-page-context", add_disqus_block)

