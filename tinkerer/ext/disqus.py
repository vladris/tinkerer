'''
    disqus
    ~~~~~~

    Handler for `comments` directive using Disqus.
    Disqus shortname must be provided in `conf.py` as `disqus_shortname`.
    
    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from sphinx.util.compat import Directive
from docutils import nodes



'''
Disqus JS script file.
'''
DISQUS_SCRIPT = "_static/disqus.js"



def create_thread(disqus_shortname, identifier):
    '''
    Returns JS code to create a new Disqus thread.
    '''
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



def enable_count(disqus_shortname):
    '''
    Returns JS code required to enable comment counting on a page.
    '''
    return str(
'<script type="text/javascript">'
'    var disqus_shortname = "%s";'
'    disqus_count();'
'</script>' 
            % disqus_shortname)



def get_count(link, identifier):
    '''
    Returns HTML required by Disqus to retrieve comment count.
    '''
    return str('<a href="%s#disqus_thread" data-disqus-identifier="%s">%s</a>' % 
            (link, identifier, "Leave a comment"))



def add_disqus_block(app, pagename, templatename, context, doctree):
    '''
    Adds Disqus to page.
    '''
    # return if no shortname was provided
    if not app.config.disqus_shortname:
        return

    env = app.builder.env

    # append disqus.js if not already in context
    if DISQUS_SCRIPT not in context["script_files"]:
        context["script_files"].append(DISQUS_SCRIPT)

    # if page is blog post and has comments
    if pagename in env.blog_metadata and env.blog_metadata[pagename].comments:
        context["comments"] = create_thread(app.config.disqus_shortname, pagename)

        # store code required to retrieve comment count for this post in metadata
        env.blog_metadata[pagename].comment_count = get_count(
                "%s%s.html" % (app.config.website,
                                env.blog_metadata[pagename].link),
                pagename)

    # just enable comment counting on the page
    else:
        context["comment_enabler"] = enable_count(app.config.disqus_shortname)



def setup(app):
    '''
    Sets up Disqus comment handler.
    '''
    # disqus_shortname contains shortname provided to Disqus
    app.add_config_value("disqus_shortname", None, True)

    # connect event
    app.connect("html-page-context", add_disqus_block)

