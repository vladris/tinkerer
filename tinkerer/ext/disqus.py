'''
    disqus
    ~~~~~~

    Handler for `comments` directive using Disqus.
    Disqus shortname must be provided in `conf.py` as `disqus_shortname`.
    
    :copyright: Copyright 2011 by Vlad Riscutia
'''
from sphinx.util.compat import Directive
from docutils import nodes

# get JS code required for Disqus comments
def get_disqus_js(disqus_shortname):
    # code provided by Disqus
    return str(
"<div id=\"disqus_thread\"></div>"
"<script type=\"text/javascript\">"
"var disqus_shortname = '%s';"
"   (function() {"
"       var dsq = document.createElement('script');"
"       dsq.type = 'text/javascript'; dsq.async = true;"
"       dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';"
"       (document.getElementsByTagName('head')[0] || "
"        document.getElementsByTagName('body')[0]).appendChild(dsq);"
"   })();"
"</script>"
"<noscript>Please enable JavaScript to view the "
"   <a href=\"http://disqus.com/?ref_noscript\">comments powered by Disqus.</a>"
"</noscript>"
"<a href=\"http://disqus.com\" class=\"dsq-brlink\">blog comments powered by "
"   <span class=\"logo-disqus\">Disqus</span>"
"</a>" % disqus_shortname)


# add disqus comments to page
def add_disqus_block(app, pagename, templatename, context, doctree):
    env = app.builder.env

    if not app.config.disqus_shortname:
        return

    if pagename in env.blog_metadata and env.blog_metadata[pagename].comments:
        context["comments"] = get_disqus_js(env.config.disqus_shortname)
    

# setup Disqus
def setup(app):
    # disqus_shortname contains shortname provided to Disqus
    app.add_config_value("disqus_shortname", None, True)

    # connect events
    app.connect("html-page-context", add_disqus_block)

